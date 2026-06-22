from abc import ABC, abstractmethod
from typing import List
from backend.integrations.github.models import GitHubRepoMetadata, GitHubBranch

class BaseGitHubService(ABC):
    @abstractmethod
    def validate_url(self, url: str) -> bool:
        """Validate if the string is a valid GitHub repository URL."""
        pass

    @abstractmethod
    def get_metadata(self, url: str) -> GitHubRepoMetadata:
        """Fetch metadata for the given GitHub URL."""
        pass

    @abstractmethod
    def get_branches(self, url: str) -> List[GitHubBranch]:
        """Fetch all branches of the repository."""
        pass

    @abstractmethod
    def clone_repository(self, url: str, destination_path: str) -> bool:
        """Clones a repository to local destination path."""
        pass

class GitHubService(BaseGitHubService):
    def validate_url(self, url: str) -> bool:
        # Stub logic
        return url.startswith("https://github.com/") or url.startswith("git@github.com:")

    def get_metadata(self, url: str) -> GitHubRepoMetadata:
        # Stub logic returning dummy model
        parts = url.rstrip("/").split("/")
        repo_name = parts[-1]
        owner = parts[-2] if len(parts) >= 2 else "unknown"
        return GitHubRepoMetadata(
            name=repo_name,
            owner=owner,
            description="Codebase cloned via GitHubIntegrationService",
            html_url=url
        )

    def get_branches(self, url: str) -> List[GitHubBranch]:
        # Stub logic
        return [
            GitHubBranch(name="main", commit_sha="abc123def456"),
            GitHubBranch(name="develop", commit_sha="789xyz012qrs")
        ]

    def clone_repository(self, url: str, destination_path: str) -> bool:
        # Stub logic for clone
        # In a real impl, this would call git clone or use GitPython
        return True
