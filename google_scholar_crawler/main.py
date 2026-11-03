"""Fetch a complete Scholar profile before replacing the published statistics."""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
import yaml
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parent
PAGE_SIZE = 100
MAX_PAGES = 100


class FetchError(RuntimeError):
    pass


def scholar_id():
    value = os.getenv("GOOGLE_SCHOLAR_ID", "").strip()
    if not value:
        with (ROOT.parent / "_config.yml").open(encoding="utf-8") as source:
            config = yaml.safe_load(source)
        value = config.get("author", {}).get("googlescholar", "") or ""
    if "://" in value:
        value = parse_qs(urlparse(value).query).get("user", [""])[0]
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise FetchError("Set GOOGLE_SCHOLAR_ID or author.googlescholar in _config.yml.")
    return value


def count(value):
    text = re.sub(r"[,\s]", "", str(value)).rstrip("*")
    if not re.fullmatch(r"[0-9]+", text):
        raise FetchError("Scholar returned an invalid citation count.")
    return int(text)


def get(session, url, params):
    try:
        response = session.get(url, params=params, timeout=(10, 30))
        response.raise_for_status()
        return response
    except requests.RequestException as error:
        status = error.response.status_code if error.response is not None else "network error"
        # Do not log request URLs: SerpApi URLs contain the API key.
        raise FetchError(f"Request to {urlparse(url).hostname} failed ({status}).") from None


def parse_profile(html, author_id):
    soup = BeautifulSoup(html, "html.parser")
    name = soup.select_one("#gsc_prf_in")
    indices = soup.select("#gsc_rsb_st .gsc_rsb_std")
    if not name or not indices or soup.select_one("#gsc_a_b") is None:
        raise FetchError(
            "Google Scholar returned a verification page or an incomplete profile. "
            "Check that the profile is public; if access is blocked, configure "
            "SERPAPI_API_KEY or use a working HTTPS_PROXY."
        )
    author = {"scholar_id": author_id, "name": name.get_text(strip=True),
              "source": "google_scholar", "publications": {}, "cites_per_year": {}}
    keys = ("citedby", "citedby5y", "hindex", "hindex5y", "i10index", "i10index5y")
    for key, cell in zip(keys, indices):
        author[key] = count(cell.get_text(strip=True))
    affiliation = soup.select_one(".gsc_prf_il")
    if affiliation:
        author["affiliation"] = affiliation.get_text(" ", strip=True)
    years = [node.get_text(strip=True) for node in soup.select(".gsc_g_t")]
    author["cites_per_year"] = {year: 0 for year in years}
    for bar in soup.select(".gsc_g_a"):
        year = parse_qs(urlparse(bar.get("href", "")).query).get("as_ylo", [None])[0]
        if year is None:
            index = re.search(r"z-index\s*:\s*(\d+)", bar.get("style", ""))
            if index and 0 < int(index[1]) <= len(years):
                year = years[-int(index[1])]
        amount = bar.select_one(".gsc_g_al")
        if year and amount:
            author["cites_per_year"][year] = count(amount.get_text(strip=True))
    rows = soup.select("#gsc_a_b .gsc_a_tr")
    for row in rows:
        title = row.select_one(".gsc_a_at")
        citation = row.select_one(".gsc_a_ac")
        if title is None or citation is None:
            raise FetchError("Scholar returned an incomplete publication row.")
        paper_id = parse_qs(urlparse(title.get("href", "")).query).get("citation_for_view", [""])[0]
        if not paper_id.startswith(author_id + ":") or paper_id in author["publications"]:
            raise FetchError("Scholar returned an invalid or duplicate publication ID.")
        year = row.select_one(".gsc_a_y")
        author["publications"][paper_id] = {
            "author_pub_id": paper_id,
            "bib": {"title": title.get_text(" ", strip=True),
                    "pub_year": year.get_text(strip=True) if year else ""},
            "num_citations": count(citation.get_text(strip=True) or "0"),
        }
    more = soup.select_one("#gsc_bpf_more")
    if more is None and len(rows) >= PAGE_SIZE:
        raise FetchError("Scholar pagination is missing; refusing to publish partial data.")
    return author, more is not None and not more.has_attr("disabled")


def fetch_direct(session, author_id):
    author = None
    start = 0
    for _ in range(MAX_PAGES):
        response = get(session, "https://scholar.google.com/citations", {
            "user": author_id, "hl": "en", "cstart": start, "pagesize": PAGE_SIZE,
        })
        page, more = parse_profile(response.text, author_id)
        if author is None:
            author = page
        else:
            if not page["publications"] or author["publications"].keys() & page["publications"].keys():
                raise FetchError("Scholar pagination made no progress; keeping previous data.")
            author["publications"].update(page["publications"])
        if not more:
            return author
        if not page["publications"]:
            raise FetchError("Scholar returned an empty page before pagination finished.")
        start = len(author["publications"])
    raise FetchError("Scholar pagination limit reached; keeping previous data.")


def fetch_serpapi(session, author_id, api_key):
    author = None
    start = 0
    for _ in range(MAX_PAGES):
        response = get(session, "https://serpapi.com/search.json", {
            "engine": "google_scholar_author", "author_id": author_id,
            "api_key": api_key, "hl": "en", "start": start, "num": PAGE_SIZE,
        })
        try:
            page = response.json()
            if page.get("error"):
                raise FetchError("SerpApi could not fetch the profile; check the key, quota and author ID.")
            if author is None:
                author = {
                    "scholar_id": author_id, "name": page["author"]["name"],
                    "source": "serpapi", "citedby": count(page["cited_by"]["table"][0]["citations"]["all"]),
                    "publications": {},
                    "cites_per_year": {
                        str(item["year"]): count(item["citations"])
                        for item in page["cited_by"].get("graph", [])
                    },
                }
                for row in page["cited_by"]["table"]:
                    for source, target in (("h_index", "hindex"), ("i10_index", "i10index")):
                        if source in row:
                            author[target] = count(row[source]["all"])
            articles = page["articles"]
            for article in articles:
                paper_id = article["citation_id"]
                if not paper_id.startswith(author_id + ":") or paper_id in author["publications"]:
                    raise FetchError("SerpApi returned an invalid or duplicate publication ID.")
                author["publications"][paper_id] = {
                    "author_pub_id": paper_id,
                    "bib": {"title": article["title"], "pub_year": str(article.get("year", ""))},
                    "num_citations": count(article.get("cited_by", {}).get("value") or 0),
                }
            if not page.get("serpapi_pagination", {}).get("next"):
                return author
            if not articles:
                raise FetchError("SerpApi returned an empty page before pagination finished.")
            start += len(articles)
        except (KeyError, IndexError, TypeError, ValueError, AttributeError):
            raise FetchError("SerpApi returned incomplete or invalid profile data.") from None
    raise FetchError("SerpApi pagination limit reached; keeping previous data.")


def write_results(author, output_dir):
    author["updated"] = datetime.now(timezone.utc).isoformat()
    badge = {"schemaVersion": 1, "label": "citations", "message": str(author["citedby"])}
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, data in (("gs_data.json", author), ("gs_data_shieldsio.json", badge)):
        target = output_dir / filename
        temporary = target.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(target)


def main():
    try:
        author_id = scholar_id()
        with requests.Session() as session:
            retry = Retry(total=2, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
                          respect_retry_after_header=False)
            session.mount("https://", HTTPAdapter(max_retries=retry))
            session.headers.update({"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})
            api_key = os.getenv("SERPAPI_API_KEY", "").strip()
            author = fetch_serpapi(session, author_id, api_key) if api_key else fetch_direct(session, author_id)
        write_results(author, ROOT / "results")
        print(f"Updated {author['name']}: {author['citedby']} citations, "
              f"{len(author['publications'])} publications ({author['source']}).")
        return 0
    except (FetchError, OSError, yaml.YAMLError) as error:
        print(f"Scholar update failed; previous statistics are unchanged: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
