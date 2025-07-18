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
    @patch("client.get_json", return_value={})
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and calls get_json with the expected URL.
        """
        gh = GithubOrgClient(org_name)
        _ = gh.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos url."""
        fake_payload = {"repos_url": "https://api.github.com/orgs/foo/repos"}
        with patch.object(GithubOrgClient, "org",
                          return_value=fake_payload):
            gh = GithubOrgClient("foo")
            self.assertEqual(
                gh._public_repos_url,
                fake_payload["repos_url"]
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns repo names from get_json
        and calls get_json and _public_repos_url exactly once.
        """
        fake_url = "https://api.github.com/orgs/foo/repos"
        fake_repos = [
            {"name": "a", "license": {"key": "mit"}},
            {"name": "b", "license": {"key": "apache-2.0"}}
        ]
        mock_get_json.return_value = fake_repos

        with patch.object(
            GithubOrgClient, "_public_repos_url",
            new_callable=Mock, return_value=fake_url
        ) as mock_url:
            gh = GithubOrgClient("foo")
            repos = gh.public_repos(license_key=None)

            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(fake_url)
            self.assertEqual(repos, ["a", "b"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct Boolean for given repo."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get to return fixture payloads."""
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        def _json_side_effect(url):
            if url.endswith("/orgs/org"):
                return cls.org_payload
            return cls.repos_payload

        mock_resp = Mock()
        mock_resp.json.side_effect = _json_side_effect
        mock_get.return_value = mock_resp

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Integration test for public_repos without license filter
        using fixture data.
        """
        gh = GithubOrgClient("org")
        repos = gh.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Integration test for public_repos with 'apache-2.0'
        license filter using fixture data.
        """
        gh = GithubOrgClient("org")
        repos = gh.public_repos(license_key="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
