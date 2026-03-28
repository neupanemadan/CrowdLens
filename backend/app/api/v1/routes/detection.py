from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.detection import (
    DetectionListResponse,
    DetectionResponse,
)
from app.services.detection_service import DetectionService

router = APIRouter(prefix="/detections", tags=["detections"])


@router.post("/image", response_model=DetectionResponse)
async def detect_from_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    service = DetectionService(db)
    detection = await service.detect_from_image(file)
    return detection


@router.get("", response_model=list[DetectionListResponse])
def get_detections(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = DetectionService(db)
    return service.get_all_detections(skip=skip, limit=limit)


@router.get("/{detection_id}", response_model=DetectionResponse)
def get_detection(
    detection_id: int,
    db: Session = Depends(get_db),
):
    service = DetectionService(db)
    return service.get_detection(detection_id)
