from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.constants import ALLOWED_IMAGE_EXTENSIONS, MAX_IMAGE_SIZE_MB
from app.core.exceptions import DetectionNotFoundError, ImageValidationError
from app.models.detection import Detection
from app.repositories.detection_repository import DetectionRepository
from app.services.image_service import ImageService
from app.vision.yolo_detector import yolo_detector


class DetectionService:
    def __init__(self, db: Session):
        self.repository = DetectionRepository(db)
        self.image_service = ImageService()

    async def detect_from_image(self, file: UploadFile) -> Detection:
        self._validate_image(file)

        file_bytes = await file.read()
        filename = file.filename or "unknown"
        stored_path = self.image_service.save_upload(file_bytes, filename)

        detections = yolo_detector.detect_persons(stored_path)

        annotated_path = self.image_service.annotate_image(stored_path, detections)

        items = [
            {
                "label": d.label,
                "confidence": d.confidence,
                "x_min": d.x_min,
                "y_min": d.y_min,
                "x_max": d.x_max,
                "y_max": d.y_max,
            }
            for d in detections
        ]

        detection = self.repository.create(
            original_filename=filename,
            stored_image_path=stored_path,
            annotated_image_path=annotated_path,
            person_count=len(detections),
            items=items,
        )

        return detection

    def get_detection(self, detection_id: int) -> Detection:
        detection = self.repository.get_by_id(detection_id)
        if not detection:
            raise DetectionNotFoundError(detection_id)
        return detection

    def get_all_detections(self, skip: int = 0, limit: int = 50) -> list[Detection]:
        return self.repository.get_all(skip=skip, limit=limit)

    def _validate_image(self, file: UploadFile) -> None:
        if not file.filename:
            raise ImageValidationError("Filename is required")

        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise ImageValidationError(
                f"Unsupported image format '{ext}'. "
                f"Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
            )

        if file.size and file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise ImageValidationError(
                f"Image size exceeds {MAX_IMAGE_SIZE_MB}MB limit"
            )
