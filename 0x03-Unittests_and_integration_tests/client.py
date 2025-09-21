#!/usr/bin/env python3
"""
Client module to interact with GitHub API.

Includes:
- GithubOrgClient: Fetch organization info and repositories.
"""

from typing import Any, Dict, List
from utils import get_json

class GithubOrgClient:
    """
    GitHub organization client to fetch org info and repos.

    Attributes:
        org_name (str): Name of the GitHub organization.
    """

    def __init__(self, org_name: str):
        """Initialize with organization name."""
        self.org_name = org_name

    @property
    def org(self) -> Dict:
        """Return JSON representation of the organization."""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self) -> str:
        """Return the URL for the organization's public repositories."""
        return self.org.get("repos_url", "")

    def public_repos(self, license: str = None) -> List[str]:
        """
        Return list of public repository names.

        Args:
            license (str, optional): License key to filter repos. Defaults to None.

        Returns:
            List[str]: List of repository names.
        """
        repos = get_json(self._public_repos_url)
        names = [repo["name"] for repo in repos]
        if license:
            names = [repo["name"] for repo in repos if self.has_license(repo, license)]
        return names

    def has_license(self, repo: Dict[str, Any], license_key: str) -> bool:
        """
        Check if a repository has a specific license.

        Args:
            repo (dict): Repository JSON.
            license_key (str): License key to check.

        Returns:
            bool: True if repo has license_key, else False.
        """
        return repo.get("license", {}).get("key") == license_key
