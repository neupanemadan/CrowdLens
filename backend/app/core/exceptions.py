from fastapi import HTTPException, status


class ImageValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class DetectionNotFoundError(HTTPException):
    def __init__(self, detection_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Detection with id {detection_id} not found",
        )


class ModelInferenceError(HTTPException):
    def __init__(self, detail: str = "Model inference failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
