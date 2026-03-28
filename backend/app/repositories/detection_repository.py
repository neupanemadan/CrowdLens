from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.detection import Detection
from app.models.detection_item import DetectionItem


class DetectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        original_filename: str,
        stored_image_path: str,
        annotated_image_path: str,
        person_count: int,
        items: list[dict],
    ) -> Detection:
        detection = Detection(
            original_filename=original_filename,
            stored_image_path=stored_image_path,
            annotated_image_path=annotated_image_path,
            person_count=person_count,
        )
        self.db.add(detection)
        self.db.flush()  # get the id before adding items

        for item in items:
            detection_item = DetectionItem(
                detection_id=detection.id,
                label=item["label"],
                confidence=item["confidence"],
                x_min=item["x_min"],
                y_min=item["y_min"],
                x_max=item["x_max"],
                y_max=item["y_max"],
            )
            self.db.add(detection_item)

        self.db.commit()
        self.db.refresh(detection)
        return detection

    def get_by_id(self, detection_id: int) -> Detection | None:
        return self.db.query(Detection).filter(Detection.id == detection_id).first()

    def get_all(self, skip: int = 0, limit: int = 50) -> list[Detection]:
        return (
            self.db.query(Detection)
            .order_by(Detection.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
