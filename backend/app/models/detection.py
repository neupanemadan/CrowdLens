from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.detection_item import DetectionItem


class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    stored_image_path: Mapped[str] = mapped_column(String, nullable=False)
    annotated_image_path: Mapped[str] = mapped_column(String, nullable=False)
    person_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String, default="completed")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    items: Mapped[list[DetectionItem]] = relationship(
        "DetectionItem", back_populates="detection", cascade="all, delete-orphan"
    )
