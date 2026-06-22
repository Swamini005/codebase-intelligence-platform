from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class GitHubRepoMetadata(BaseModel):
    name: str
    owner: str
    description: Optional[str] = None
    html_url: str
    default_branch: str = "main"

class GitHubBranch(BaseModel):
    name: str
    commit_sha: str
