import contextlib
import io
import os
import unittest
from unittest.mock import Mock, patch

import requests
import yaml

import main
import subscription_proxy as proxy


class SubscriptionProxyTests(unittest.TestCase):
    def test_encodes_credentials_and_uses_remote_socks_dns(self):
        node = {"type": "socks5", "server": "proxy.example", "port": 1080,
                "username": "user@example", "password": "p:a/ss#word"}
        self.assertEqual(proxy.proxy_url(node),
                         "socks5h://user%40example:p%3Aa%2Fss%23word@proxy.example:1080")

    def test_http_tls_and_ipv6(self):
        node = {"type": "http", "server": "2001:db8::1", "port": "443", "tls": True}
        self.assertEqual(proxy.proxy_url(node), "https://[2001:db8::1]:443")

    def test_unsupported_nodes_cannot_silently_use_direct_access(self):
        for node in [None, {"type": "direct"}, {"type": "ss"},
                     {"type": "http", "server": "example", "port": 0},
                     {"type": "http", "server": "example/path", "port": 80},
                     {"type": "socks5", "server": "example", "port": 443, "tls": True},
                     {"type": "http", "server": "example", "port": 80, "dialer-proxy": "other"}]:
            with self.subTest(node=node):
                self.assertIsNone(proxy.proxy_url(node))

    def test_subscription_errors_never_reveal_private_data(self):
        private_url = "https://private.example/subscription/secret-token"
        for error in [requests.ConnectionError(private_url), yaml.YAMLError("private-node-password")]:
            with patch.object(proxy.requests, "Session") as factory:
                factory.return_value.__enter__.return_value.get.side_effect = error
                with self.assertRaises(proxy.SubscriptionError) as caught:
                    proxy.load_subscription(private_url)
            self.assertNotIn(private_url, str(caught.exception))
            self.assertNotIn("private-node-password", str(caught.exception))
        with self.assertRaises(proxy.SubscriptionError):
            proxy.load_subscription("http://private.example/secret-token")

    def test_subscription_must_contain_a_proxy_list(self):
        with patch.object(proxy.requests, "Session") as factory:
            factory.return_value.__enter__.return_value.get.return_value.text = "proxies: wrong-type"
            with self.assertRaises(proxy.SubscriptionError):
                proxy.load_subscription("https://example/subscription")

    def test_subscription_http_error_reports_status_without_credentials(self):
        private_url = "https://private.example/subscription/secret-token"
        for status in [403, 429, 503]:
            response = requests.Response()
            response.status_code = status
            response.url = private_url
            response._content = b"private-node-password"
            with self.subTest(status=status), patch.object(proxy.requests, "Session") as factory:
                factory.return_value.__enter__.return_value.get.return_value = response
                with self.assertRaises(proxy.SubscriptionError) as caught:
                    proxy.load_subscription(private_url)
            self.assertIn(f"HTTP {status}", str(caught.exception))
            self.assertNotIn(private_url, str(caught.exception))
            self.assertNotIn("private-node-password", str(caught.exception))

    def test_failed_proxy_then_success_without_logging_credentials(self):
        nodes = [{"name": "private-node", "type": "http", "server": "proxy.example",
                  "port": port, "username": "private-user", "password": "private-password"}
                 for port in [8001, 8002]]
        output = io.StringIO()
        callback = Mock(side_effect=[RuntimeError("private-password"), {"citedby": 42}])
        with patch.object(proxy, "load_subscription", return_value=nodes), \
                patch.dict(os.environ, {"GOOGLE_SCHOLAR_PROXY_NODE": ""}), \
                patch.object(proxy.requests, "Session") as factory, \
                contextlib.redirect_stdout(output):
            result = proxy.fetch_via_subscription("private-url", callback)
            session = factory.return_value.__enter__.return_value
            self.assertFalse(session.trust_env)
            self.assertEqual(session.proxies["https"], "http://private-user:private-password@proxy.example:8002")
        self.assertEqual(result, {"citedby": 42})
        for secret in ["private-url", "private-user", "private-password", "private-node", "proxy.example"]:
            self.assertNotIn(secret, output.getvalue())

    def test_failed_attempts_are_bounded(self):
        nodes = [{"type": "http", "server": "proxy.example", "port": 8000 + index}
                 for index in range(10)]
        callback = Mock(side_effect=RuntimeError("private-error"))
        with patch.object(proxy, "load_subscription", return_value=nodes), \
                patch.dict(os.environ, {"GOOGLE_SCHOLAR_PROXY_NODE": ""}), \
                contextlib.redirect_stdout(io.StringIO()), self.assertRaises(proxy.SubscriptionError):
            proxy.fetch_via_subscription("private-url", callback)
        self.assertEqual(callback.call_count, proxy.MAX_PROXY_ATTEMPTS)

    def test_selects_named_node_without_exposing_its_name(self):
        nodes = [{"name": "selected", "type": "http", "server": "proxy.example", "port": 8080}]
        with patch.object(proxy, "load_subscription", return_value=nodes), \
                patch.dict(os.environ, {"GOOGLE_SCHOLAR_PROXY_NODE": "missing-private-node"}), \
                self.assertRaises(proxy.SubscriptionError) as caught:
            proxy.fetch_via_subscription("private-url", Mock())
        self.assertNotIn("missing-private-node", str(caught.exception))

    def test_main_uses_subscription_before_other_providers(self):
        author = {"name": "Test Author", "citedby": 42, "publications": {}, "source": "google_scholar"}
        with patch.dict(os.environ, {"CLASH_SUBSCRIPTION_URL": "private-url", "SERPAPI_API_KEY": "unused"}), \
                patch.object(main, "scholar_id", return_value="test"), \
                patch.object(main, "fetch_via_subscription", return_value=author) as fetch, \
                patch.object(main, "fetch_serpapi") as api, patch.object(main, "write_results"), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main.main(), 0)
        self.assertEqual(fetch.call_args.args[0], "private-url")
        api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
