#!/usr/bin/env python3
"""
Fixture data for GithubOrgClient integration tests.
"""

# Organization payload fixture
org_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}

# Repositories payload fixture
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}}
]

# Expected repository names from payload
expected_repos = ["repo1", "repo2", "repo3"]

# Expected repositories filtered by license apache-2.0
apache2_repos = ["repo1", "repo3"]
