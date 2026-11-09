"""Use HTTP/SOCKS nodes from a private Clash subscription without saving it."""

import os
from urllib.parse import quote, urlsplit

import requests
import yaml
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MAX_PROXY_ATTEMPTS = 5


class SubscriptionError(RuntimeError):
    pass


def load_subscription(url):
    if urlsplit(url).scheme != "https":
        raise SubscriptionError("CLASH_SUBSCRIPTION_URL must use HTTPS.")
    try:
        with requests.Session() as session:
            retry = Retry(total=2, backoff_factor=1, allowed_methods={"GET"},
                          status_forcelist=[429, 500, 502, 503, 504],
                          respect_retry_after_header=False, raise_on_status=False)
            session.mount("https://", HTTPAdapter(max_retries=retry))
            response = session.get(url, timeout=(10, 30))
            response.raise_for_status()
            document = yaml.safe_load(response.text)
        if not isinstance(document, dict) or not isinstance(document.get("proxies"), list):
            raise ValueError("Missing proxies list")
        return document["proxies"]
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else "unknown"
        # Report only the status; URLs, response bodies and exceptions may contain credentials.
        raise SubscriptionError(
            f"Could not load the private Clash subscription (HTTP {status}); credentials withheld."
        ) from None
    except requests.RequestException:
        raise SubscriptionError(
            "Could not load the private Clash subscription after retries (network error); credentials withheld."
        ) from None
    except (yaml.YAMLError, ValueError):
        raise SubscriptionError(
            "The private subscription did not return valid Clash YAML with a proxies list; contents withheld."
        ) from None


def proxy_url(node):
    """Return a requests-compatible URL; credentials stay in memory."""
    if not isinstance(node, dict):
        return None
    kind = node.get("type")
    if kind not in ("http", "socks5"):
        return None
    # requests cannot represent these Clash-specific connection options.
    if node.get("dialer-proxy") or node.get("headers") or (kind == "socks5" and node.get("tls")):
        return None
    server = node.get("server")
    port = node.get("port")
    if not isinstance(server, str) or not server or any(char in server for char in "/@?#\r\n "):
        return None
    try:
        port = int(port)
    except (TypeError, ValueError):
        return None
    if not 1 <= port <= 65535:
        return None
    if ":" in server and not server.startswith("["):
        server = "[" + server + "]"
    username = node.get("username", "")
    password = node.get("password", "")
    if not isinstance(username, str) or not isinstance(password, str):
        return None
    authentication = ""
    if username or password:
        authentication = quote(username, safe="") + ":" + quote(password, safe="") + "@"
    scheme = "socks5h" if kind == "socks5" else ("https" if node.get("tls") else "http")
    return f"{scheme}://{authentication}{server}:{port}"


def fetch_via_subscription(url, fetch_author):
    nodes = load_subscription(url)
    preferred = os.getenv("GOOGLE_SCHOLAR_PROXY_NODE", "").strip()
    if preferred:
        nodes = [node for node in nodes if isinstance(node, dict) and node.get("name") == preferred]
    candidates = []
    for node in nodes:
        candidate = proxy_url(node)
        if candidate and candidate not in candidates:
            candidates.append(candidate)
    if not candidates:
        raise SubscriptionError("No compatible HTTP/SOCKS5 nodes found in the subscription or selected node.")
    attempts = candidates[:MAX_PROXY_ATTEMPTS]
    for index, candidate in enumerate(attempts, 1):
        with requests.Session() as session:
            # Explicit proxies only: environment settings must not cause direct access.
            session.trust_env = False
            session.proxies = {"http": candidate, "https": candidate}
            session.headers.update({"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})
            try:
                author = fetch_author(session)
            except (RuntimeError, requests.RequestException):
                print(f"Subscription proxy attempt {index}/{len(attempts)} failed; credentials withheld.")
                continue
            print(f"Fetched Scholar through subscription proxy attempt {index}.")
            return author
    raise SubscriptionError(
        "The tested subscription nodes could not retrieve a complete Scholar profile. "
        "Set GOOGLE_SCHOLAR_PROXY_NODE to select another node."
    ) from None
