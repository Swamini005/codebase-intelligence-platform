import os
import stat
import shutil
import logging
from pathlib import Path
from typing import List
import git
from backend.core.config import Settings
from backend.integrations.github.client import GitHubClient
from backend.integrations.github.models import GitHubRepoMetadata, GitHubBranch
from backend.core.exceptions import (
    GitHubException,
    RepoCloneException
)

logger = logging.getLogger(__name__)

def safe_rmtree(path: Path) -> None:
    """Safely delete directory by clearing read-only attributes on Windows."""
    if not path.exists():
        return
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.chmod(file_path, stat.S_IWRITE)
                os.remove(file_path)
            except Exception:
                pass
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.chmod(dir_path, stat.S_IWRITE)
                os.rmdir(dir_path)
            except Exception:
                pass
    try:
        shutil.rmtree(path, ignore_errors=True)
    except Exception:
        pass

class GitHubService:
    def __init__(self, settings: Settings):
        self.settings = settings
        # Ensure REPOS_BASE_DIR exists
        os.makedirs(self.settings.REPOS_BASE_DIR, exist_ok=True)
        self.client = GitHubClient(settings)
        logger.info("Initialized GitHubService with base directory: %s", self.settings.REPOS_BASE_DIR)

    def get_local_path(self, github_url: str) -> Path:
        """Derive a safe folder name: replace '/' and '.' with '__' in 'owner/repo'."""
        owner, repo = self.client.parse_github_url(github_url)
        owner_repo = f"{owner}/{repo}"
        folder_name = owner_repo.replace("/", "__").replace(".", "__")
        return Path(self.settings.REPOS_BASE_DIR) / folder_name

    def is_cloned(self, github_url: str) -> bool:
        """Return True if get_local_path() exists and contains a valid .git folder."""
        local_path = self.get_local_path(github_url)
        git_dir = local_path / ".git"
        return local_path.exists() and git_dir.exists() and git_dir.is_dir()

    def clone_repo(self, github_url: str) -> Path:
        """Clone a repository locally or pull updates if already cloned."""
        logger.info("Validating repository URL: %s", github_url)
        self.client.validate_repo(github_url)
        
        local_path = self.get_local_path(github_url)
        
        if self.is_cloned(github_url):
            logger.info("Repo already cloned, pulling latest")
            try:
                repo = git.Repo(local_path)
                repo.remotes.origin.pull()
                logger.info("Successfully pulled latest changes for %s", github_url)
            except git.exc.GitCommandError as e:
                err_msg = str(e)
                if self.settings.GITHUB_TOKEN:
                    err_msg = err_msg.replace(self.settings.GITHUB_TOKEN, "******")
                raise RepoCloneException(f"Failed to pull latest changes: {err_msg}", detail={"url": github_url})
        else:
            owner, repo_name = self.client.parse_github_url(github_url)
            if self.settings.GITHUB_TOKEN:
                clone_url = f"https://{self.settings.GITHUB_TOKEN}@github.com/{owner}/{repo_name}"
            else:
                clone_url = github_url
                
            logger.info("Cloning repository %s to %s", github_url, local_path)
            try:
                git.Repo.clone_from(clone_url, local_path, depth=1)
                logger.info("Successfully cloned repository %s to %s", github_url, local_path)
            except git.exc.GitCommandError as e:
                logger.error("Failed to clone repository: %s", github_url)
                if local_path.exists():
                    safe_rmtree(local_path)
                err_msg = str(e)
                if self.settings.GITHUB_TOKEN:
                    err_msg = err_msg.replace(self.settings.GITHUB_TOKEN, "******")
                raise RepoCloneException(f"Failed to clone repository: {err_msg}", detail={"url": github_url})
                
        return local_path

    def delete_repo(self, github_url: str) -> None:
        """Delete the local cloned repository."""
        local_path = self.get_local_path(github_url)
        if not local_path.exists():
            raise FileNotFoundError(f"Repository directory does not exist: {local_path}")
        logger.info("Deleting repository at %s", local_path)
        safe_rmtree(local_path)
        logger.info("Successfully deleted repository at %s", local_path)

    # Legacy Compatibility methods
    def validate_url(self, url: str) -> bool:
        try:
            self.client.parse_github_url(url)
            return True
        except Exception:
            return False

    def get_metadata(self, url: str) -> GitHubRepoMetadata:
        metadata = self.client.validate_repo(url)
        return GitHubRepoMetadata(
            name=metadata.get("name", ""),
            owner=metadata.get("owner", {}).get("login", ""),
            description=metadata.get("description", ""),
            html_url=metadata.get("html_url", ""),
            default_branch=metadata.get("default_branch", "main")
        )

    def get_branches(self, url: str) -> List[GitHubBranch]:
        owner, repo = self.client.parse_github_url(url)
        branches = self.client.get_branches(owner, repo)
        # Mock commit shas since get_branches returns List[str] in Client
        return [GitHubBranch(name=b, commit_sha="mocksha12345") for b in branches]

    def clone_repository(self, url: str, destination_path: str) -> bool:
        try:
            self.clone_repo(url)
            return True
        except Exception:
            return False

