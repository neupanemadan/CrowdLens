from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.detection import Detection


class DetectionItem(Base):
    __tablename__ = "detection_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    detection_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("detections.id"), nullable=False
    )
    label: Mapped[str] = mapped_column(String, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    x_min: Mapped[float] = mapped_column(Float, nullable=False)
    y_min: Mapped[float] = mapped_column(Float, nullable=False)
    x_max: Mapped[float] = mapped_column(Float, nullable=False)
    y_max: Mapped[float] = mapped_column(Float, nullable=False)

    detection: Mapped[Detection] = relationship("Detection", back_populates="items")
