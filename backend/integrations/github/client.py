import re
import requests
from typing import Dict, Any, List
from backend.core.config import Settings
from backend.core.exceptions import (
    GitHubException,
    RepoNotFoundException,
    InvalidGitHubURLException
)

class GitHubClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.session = requests.Session()
        
        # Set up default headers
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "codebase-intel/1.0"
        })
        
        # Authenticate with GITHUB_TOKEN if provided
        if settings.GITHUB_TOKEN:
            self.session.headers.update({
                "Authorization": f"token {settings.GITHUB_TOKEN}"
            })

    def parse_github_url(self, github_url: str) -> tuple[str, str]:
        """Return (owner, repo_name) from any valid github.com URL.
        
        Accepts:
            https://github.com/owner/repo
            https://github.com/owner/repo.git
            and standard variations with optional http/https, www, or trailing slash.
        """
        url = github_url.strip()
        pattern = r"^(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$"
        match = re.match(pattern, url, re.IGNORECASE)
        if not match:
            raise InvalidGitHubURLException(f"Invalid GitHub URL: {github_url}")
        return match.group(1), match.group(2)

    def validate_repo(self, github_url: str) -> dict:
        """Validate repository and return its metadata.
        
        Raises RepoNotFoundException if not found, GitHubException on other errors.
        """
        owner, repo = self.parse_github_url(github_url)
        url = f"https://api.github.com/repos/{owner}/{repo}"
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise RepoNotFoundException(f"Repo {owner}/{repo} not found")
            elif response.status_code in (401, 403):
                raise GitHubException("GitHub auth failed — check GITHUB_TOKEN")
            else:
                raise GitHubException(
                    f"GitHub API returned error status: {response.status_code}",
                    detail={"status_code": response.status_code}
                )
        except requests.RequestException as e:
            raise GitHubException(f"Network error: {str(e)}", detail={"error": str(e)})

    def get_branches(self, owner: str, repo: str) -> List[str]:
        """Fetch list of branches from the repository."""
        url = f"https://api.github.com/repos/{owner}/{repo}/branches"
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return [b["name"] for b in response.json()]
            return ["main"]
        except Exception:
            return ["main"]

