# CrowdLens

AI-powered person detection and counting system. Upload an image and get back the number of people detected, annotated bounding boxes, and a full detection history.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Vision:** YOLOv8n (Ultralytics), OpenCV
- **Database:** SQLite
- **Frontend:** React + TypeScript + Vite *(coming soon)*
- **Deployment:** Docker, Docker Compose

## Project Structure

```
vision_ai/
├── backend/
│   ├── app/
│   │   ├── api/v1/routes/     # API endpoints
│   │   ├── core/              # Config, constants, exceptions
│   │   ├── db/                # Database engine and session
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── repositories/      # Database access layer
│   │   ├── schemas/           # Pydantic request/response models
│   │   ├── services/          # Business logic layer
│   │   ├── vision/            # YOLO detection wrapper
│   │   └── main.py            # FastAPI app entrypoint
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/                  # (coming soon)
├── docker-compose.yml
└── .gitignore
```

## Architecture

```
Route → Service → Repository → SQLite
                → YoloDetector (inference)
                → ImageService (OpenCV annotation)
```

Routes are thin. Business logic lives in services. Database access is isolated in repositories. YOLO inference is wrapped in a dedicated vision module.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/detections/image` | Upload image, detect and count persons |
| GET | `/api/v1/detections` | List all detection results |
| GET | `/api/v1/detections/{id}` | Get a single detection with bounding boxes |
| GET | `/api/v1/health` | Health check |

## Getting Started

### Prerequisites

- Python 3.9+
- Docker *(optional, for containerized setup)*

### Local Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Swagger docs at `http://localhost:8000/docs`.

### Docker Setup

```bash
docker compose up --build
```

## Usage

Upload an image with people:

```bash
curl -X POST http://localhost:8000/api/v1/detections/image \
  -F "file=@path/to/image.jpg"
```

Response:

```json
{
  "id": 1,
  "original_filename": "image.jpg",
  "annotated_image_path": "uploads/annotated/abc_annotated.jpg",
  "person_count": 3,
  "status": "completed",
  "created_at": "2026-03-28T10:30:00",
  "items": [
    {
      "id": 1,
      "label": "person",
      "confidence": 0.92,
      "x_min": 120.0,
      "y_min": 48.0,
      "x_max": 240.0,
      "y_max": 410.0
    }
  ]
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | Vision AI | Application name |
| `DEBUG` | true | Debug mode |
| `DATABASE_URL` | sqlite:///./data/vision_ai.db | SQLite connection string |
| `UPLOAD_DIR` | uploads | Directory for stored images |
| `YOLO_MODEL` | yolov8n.pt | YOLO model file |
| `CONFIDENCE_THRESHOLD` | 0.5 | Minimum detection confidence |

## License

MIT
