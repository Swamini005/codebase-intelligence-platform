import os
from typing import BinaryIO
from backend.storage.base import StorageProvider
from backend.core.config import settings

class LocalStorage(StorageProvider):
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or settings.STORAGE_DIR
        os.makedirs(self.base_dir, exist_ok=True)

    def save_file(self, file_path: str, content: BinaryIO) -> str:
        full_path = os.path.join(self.base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(content.read())
        return full_path

    def get_file(self, identifier: str) -> BinaryIO:
        if not os.path.exists(identifier):
            raise FileNotFoundError(f"File not found: {identifier}")
        return open(identifier, "rb")

    def delete_file(self, identifier: str) -> bool:
        if os.path.exists(identifier):
            os.remove(identifier)
            return True
        return False

    def list_files(self, prefix: str = "") -> list[str]:
        # Simple recursive file search matching prefix
        results = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), self.base_dir)
                if rel_path.startswith(prefix):
                    results.append(rel_path)
        return results
