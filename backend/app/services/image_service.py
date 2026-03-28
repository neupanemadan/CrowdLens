import uuid
from pathlib import Path

import cv2

from app.core.config import settings
from app.vision.yolo_detector import DetectedObject


class ImageService:
    def __init__(self):
        self._ensure_dirs()

    def _ensure_dirs(self):
        settings.upload_original_path.mkdir(parents=True, exist_ok=True)
        settings.upload_annotated_path.mkdir(parents=True, exist_ok=True)

    def save_upload(self, file_bytes: bytes, original_filename: str) -> str:
        ext = Path(original_filename).suffix
        unique_name = f"{uuid.uuid4().hex}{ext}"
        save_path = settings.upload_original_path / unique_name
        save_path.write_bytes(file_bytes)
        return str(save_path)

    def annotate_image(self, image_path: str, detections: list[DetectedObject]) -> str:
        image = cv2.imread(image_path)

        for det in detections:
            x1, y1 = int(det.x_min), int(det.y_min)
            x2, y2 = int(det.x_max), int(det.y_max)

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            label_text = f"{det.label} {det.confidence:.2f}"
            cv2.putText(
                image,
                label_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        stem = Path(image_path).stem
        annotated_path = settings.upload_annotated_path / f"{stem}_annotated.jpg"
        cv2.imwrite(str(annotated_path), image)
        return str(annotated_path)
