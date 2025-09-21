#!/usr/bin/env python3
"""
Fixtures for integration tests
"""

TEST_PAYLOAD = [
    (
        {"repos_url": "https://api.github.com/orgs/testorg/repos"},
        [
            {
                "name": "repo1",
                "license": {"key": "mit"},
                "owner": {"login": "testorg"}
            },
            {
                "name": "repo2", 
                "license": {"key": "apache-2.0"},
                "owner": {"login": "testorg"}
            },
            {
                "name": "repo3",
                "license": {"key": "apache-2.0"},
                "owner": {"login": "testorg"}
            }
        ],
        ["repo1", "repo2", "repo3"],
        ["repo2", "repo3"]
    )
]