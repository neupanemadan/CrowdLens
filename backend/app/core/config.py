from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "Vision AI"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///./data/vision_ai.db"

    UPLOAD_DIR: str = "uploads"
    ORIGINAL_DIR: str = "originals"
    ANNOTATED_DIR: str = "annotated"

    YOLO_MODEL: str = "yolov8n.pt"
    CONFIDENCE_THRESHOLD: float = 0.5
    PERSON_CLASS_ID: int = 0  # COCO class 0 = person

    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"

    @property
    def upload_original_path(self) -> Path:
        return Path(self.UPLOAD_DIR) / self.ORIGINAL_DIR

    @property
    def upload_annotated_path(self) -> Path:
        return Path(self.UPLOAD_DIR) / self.ANNOTATED_DIR


settings = Settings()
