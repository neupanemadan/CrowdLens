from __future__ import annotations

from dataclasses import dataclass

from ultralytics import YOLO

from app.core.config import settings


@dataclass
class DetectedObject:
    label: str
    confidence: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float


class YoloDetector:
    def __init__(self):
        self._model: YOLO | None = None

    @property
    def model(self) -> YOLO:
        if self._model is None:
            self._model = YOLO(settings.YOLO_MODEL)
        return self._model

    def detect_persons(self, image_path: str) -> list[DetectedObject]:
        results = self.model(
            image_path,
            conf=settings.CONFIDENCE_THRESHOLD,
            classes=[settings.PERSON_CLASS_ID],
        )

        detections: list[DetectedObject] = []
        for result in results:
            for box in result.boxes:
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                label = result.names[int(box.cls[0])]

                detections.append(
                    DetectedObject(
                        label=label,
                        confidence=round(confidence, 4),
                        x_min=round(x_min, 2),
                        y_min=round(y_min, 2),
                        x_max=round(x_max, 2),
                        y_max=round(y_max, 2),
                    )
                )

        return detections


# Singleton instance — loaded once, reused across requests
yolo_detector = YoloDetector()
