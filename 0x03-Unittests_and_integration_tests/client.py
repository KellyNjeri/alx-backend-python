# 0x03-Unittests_and_integration_tests/client.py
#!/usr/bin/env python3
"""
Github API client module
"""

from utils import get_json
from typing import List, Dict


class GithubOrgClient:
    """
    A client for the Github Organization API
    """

    def __init__(self, org_name: str):
        """
        Initialize with organization name
        """
        self._org_name = org_name

    @property
    def org(self) -> Dict:
        """
        Get organization information
        """
        return get_json(f"https://api.github.com/orgs/{self._org_name}")

    @property
    def _public_repos_url(self) -> str:
        """
        Get public repos URL from organization info
        """
        return self.org["repos_url"]

    def public_repos(self, license: str = None) -> List[str]:
        """
        Get list of public repository names
        """
        repos = get_json(self._public_repos_url)
        
        if license:
            repos = [repo for repo in repos if self.has_license(repo, license)]
            
        return [repo["name"] for repo in repos]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """
        Check if repository has a specific license
        """
        return repo.get("license", {}).get("key") == license_key