# Vision AI — AWS Deployment Guide

## Architecture

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────┐
│  S3 Bucket  │       │   EC2 Instance   │       │     ECR     │
│  (Frontend) │──────▶│   (Backend API)  │◀──────│  (Docker    │
│  Vue SPA    │       │   Docker + YOLO  │       │   Images)   │
└─────────────┘       └──────────────────┘       └─────────────┘
```

- **Frontend**: Vue 3 SPA hosted on S3 (static website hosting)
- **Backend**: FastAPI + YOLOv8 running in Docker on EC2
- **ECR**: Stores backend Docker images; EC2 pulls from here
- **CI/CD**: GitHub Actions — lint gates (Ruff / ESLint) → deploy on merge to `main`

---

## Prerequisites

- AWS CLI v2 configured (`aws configure`)
- An AWS account with permissions for EC2, S3, ECR, IAM, CloudFormation

---

## Initial Setup (One-Time)

### 1. Create ECR Repository

```bash
chmod +x deploy/*.sh
export AWS_REGION=ap-northeast-1
./deploy/setup-ecr.sh
```

### 2. Launch Infrastructure via CloudFormation

```bash
aws cloudformation create-stack \
  --stack-name vision-ai \
  --template-body file://deploy/cloudformation.yml \
  --parameters ParameterKey=KeyName,ParameterValue=<YOUR_KEY_PAIR> \
  --capabilities CAPABILITY_NAMED_IAM \
  --region ap-northeast-1
```

This creates:
- EC2 instance (t3.micro) with IAM role for ECR access
- Security group (ports 22 + 8000)
- Auto-installs Docker, pulls image from ECR, and starts the backend

### 3. Configure GitHub Secrets

Go to **Settings → Secrets and variables → Actions** in your GitHub repo and add:

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `EC2_HOST` | EC2 public IP (from CloudFormation outputs) |
| `EC2_USERNAME` | `ubuntu` |
| `EC2_SSH_KEY` | Private SSH key (contents of `.pem` file) |
| `S3_BUCKET` | S3 bucket name (e.g. `vision-ai-frontend-demo`) |
| `BACKEND_API_URL` | `http://<EC2_IP>:8000/api/v1` |
| `CLOUDFRONT_DISTRIBUTION_ID` | *(optional)* CloudFront distribution ID |

---

## CI/CD (GitHub Actions)

Two workflows trigger on push to `main`:

| Workflow | Trigger | Pipeline |
|---|---|---|
| `deploy-backend.yml` | `backend/**` | Ruff lint + format → Docker build → ECR push → SSH deploy to EC2 |
| `deploy-frontend.yml` | `frontend/**` | ESLint + vue-tsc type check → Vite build → S3 sync |

Lint must pass before deploy runs. If Ruff or ESLint fails, deployment is blocked.

---

## File Overview

```
deploy/
├── cloudformation.yml   # AWS infrastructure (EC2 + IAM + SG)
├── setup-ecr.sh         # Create ECR repository (run once)
└── DEPLOYMENT.md        # This file
.github/workflows/
├── deploy-backend.yml   # Backend CI/CD pipeline
└── deploy-frontend.yml  # Frontend CI/CD pipeline
frontend/
└── .env.production      # Backend API URL for production build
```

---

## Tear Down

To delete all AWS resources and stop costs:

```bash
aws cloudformation delete-stack --stack-name vision-ai --region ap-northeast-1
aws ecr delete-repository --repository-name vision-ai-backend --force --region ap-northeast-1
aws s3 rb s3://vision-ai-frontend-demo --force
```

---

## Security Notes

- The CORS `allow_origins` in `backend/app/main.py` is set to `["*"]`. For production, restrict it to your S3 website URL.
- Consider adding HTTPS via CloudFront (frontend) and an ALB or Nginx reverse proxy (backend).
- The S3 bucket policy allows public read. If you use CloudFront, switch to an Origin Access Identity instead.
