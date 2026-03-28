from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DetectionItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    confidence: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float


class DetectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    annotated_image_path: str
    person_count: int
    status: str
    created_at: datetime
    items: list[DetectionItemResponse] = []


class DetectionListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    person_count: int
    status: str
    created_at: datetime
