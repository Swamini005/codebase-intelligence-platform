from typing import Any, Dict, List
import httpx

class GitHubClient:
    """Mock/Stub GitHub API Client using httpx."""
    def __init__(self, token: str = None):
        self.token = token
        self.headers = {"Accept": "application/vnd.github+json"}
        if token:
            self.headers["Authorization"] = f"token {token}"

    def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch metadata about a repository."""
        # Stub implementation
        return {
            "name": repo,
            "full_name": f"{owner}/{repo}",
            "html_url": f"https://github.com/{owner}/{repo}",
            "description": "Mocked codebase intelligence repo",
            "stargazers_count": 42,
            "language": "Python"
        }

    def get_branches(self, owner: str, repo: str) -> List[str]:
        """Fetch list of branches."""
        # Stub implementation
        return ["main", "develop"]
