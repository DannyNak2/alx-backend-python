#!/usr/bin/env python3
"""
Unit and integration tests for client.GithubOrgClient.
"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and calls get_json with the expected URL.
        """
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org()
        self.assertEqual(result, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos url."""
        payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        with patch.object(GithubOrgClient, "org", return_value=payload):
            client = GithubOrgClient("test_org")
            result = client._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns correct repo list and uses cache.
        """
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ]
        with patch.object(
            GithubOrgClient, "_public_repos_url",
            return_value="https://api.github.com/orgs/test_org/repos"
        ) as mock_url:
            client = GithubOrgClient("test_org")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected result."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)









@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests with fixtures"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get to return example payloads"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # side_effect allows returning different values for each call
        cls.mock_get.side_effect = [
            cls.org_payload,  # first call returns org data
            cls.repos_payload  # second call returns repo list
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        client = GithubOrgClient("org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license"""
        client = GithubOrgClient("org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

