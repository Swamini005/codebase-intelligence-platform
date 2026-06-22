from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageProvider(ABC):
    @abstractmethod
    def save_file(self, file_path: str, content: BinaryIO) -> str:
        """Saves a file to storage and returns the URI/identifier."""
        pass

    @abstractmethod
    def get_file(self, identifier: str) -> BinaryIO:
        """Retrieves a file from storage."""
        pass

    @abstractmethod
    def delete_file(self, identifier: str) -> bool:
        """Deletes a file from storage."""
        pass

    @abstractmethod
    def list_files(self, prefix: str = "") -> list[str]:
        """Lists files matching prefix."""
        pass
