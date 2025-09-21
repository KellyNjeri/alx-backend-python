#!/usr/bin/env python3
"""
Test module for client.py classes using unittest.
Covers GithubOrgClient class and its methods with patching and fixtures.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org method returns expected JSON from get_json."""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct repos URL."""
        client = GithubOrgClient("test_org")
        payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        with patch.object(GithubOrgClient, "org", new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = payload
            self.assertEqual(client._public_repos_url, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names using mocked get_json."""
        client = GithubOrgClient("test_org")
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=unittest.mock.PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up patched requests.get to return fixture payloads."""
        cls.get_patcher = patch("utils.requests.get")
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: cls.org_payload),
            unittest.mock.Mock(json=lambda: cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patched requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names from fixture."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns expected repo names filtered by license."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
