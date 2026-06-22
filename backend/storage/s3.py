from typing import BinaryIO
from backend.storage.base import StorageProvider
from backend.core.config import settings

class S3Storage(StorageProvider):
    """AWS S3 Storage Provider stub."""
    def __init__(self):
        self.bucket_name = settings.AWS_S3_BUCKET
        self.access_key = settings.AWS_ACCESS_KEY
        self.secret_key = settings.AWS_SECRET_KEY

    def save_file(self, file_path: str, content: BinaryIO) -> str:
        # TODO: Implement boto3 client uploads
        # Return S3 URL
        return f"s3://{self.bucket_name}/{file_path}"

    def get_file(self, identifier: str) -> BinaryIO:
        # TODO: Implement boto3 download
        raise NotImplementedError("S3 get_file is not implemented yet.")

    def delete_file(self, identifier: str) -> bool:
        # TODO: Implement boto3 delete
        return True

    def list_files(self, prefix: str = "") -> list[str]:
        # TODO: Implement boto3 listing
        return []
