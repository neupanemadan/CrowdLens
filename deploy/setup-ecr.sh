#!/usr/bin/env bash
# =============================================================================
# setup-ecr.sh — Create an ECR repository for Vision AI backend
# =============================================================================
set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────────────────
AWS_REGION="${AWS_REGION:-ap-northeast-1}"
ECR_REPO_NAME="${ECR_REPO_NAME:-vision-ai-backend}"

echo "==> Creating ECR repository: ${ECR_REPO_NAME} in ${AWS_REGION}"

# Create the repository (ignore error if it already exists)
aws ecr create-repository \
  --repository-name "${ECR_REPO_NAME}" \
  --region "${AWS_REGION}" \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256 \
  2>/dev/null || echo "    Repository already exists, skipping creation."

# Get the repository URI
ECR_URI=$(aws ecr describe-repositories \
  --repository-names "${ECR_REPO_NAME}" \
  --region "${AWS_REGION}" \
  --query 'repositories[0].repositoryUri' \
  --output text)

echo "==> ECR Repository URI: ${ECR_URI}"

# Set lifecycle policy — keep only the last 10 images
echo "==> Setting lifecycle policy (keep last 10 images)..."
aws ecr put-lifecycle-policy \
  --repository-name "${ECR_REPO_NAME}" \
  --region "${AWS_REGION}" \
  --lifecycle-policy-text '{
    "rules": [
      {
        "rulePriority": 1,
        "description": "Keep only last 10 images",
        "selection": {
          "tagStatus": "any",
          "countType": "imageCountMoreThan",
          "countNumber": 10
        },
        "action": {
          "type": "expire"
        }
      }
    ]
  }'

echo ""
echo "==> ECR setup complete!"
echo "    Repository: ${ECR_URI}"
echo ""
echo "    Next: run deploy/build-and-push.sh to build & push the Docker image."
