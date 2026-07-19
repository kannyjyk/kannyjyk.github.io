#!/usr/bin/env python3
"""
Fetch the Google Scholar citation count and write it into index.html.

Runs weekly from .github/workflows/update-citations.yml.

Two ways to fetch, tried in order:
  1. SerpAPI  -- reliable. Set a repo secret SERPAPI_KEY (free tier: 100
     searches/month; weekly = ~4/month). https://serpapi.com
  2. scholarly -- free, no key, but Google Scholar often blocks CI runner
     IPs, so it may fail. On any failure we simply skip (never break the
     page / fail the job).

Only the number inside  <div class="n" id="cite-count">NNN</div>  is touched.
"""
import os
import re
import sys

SCHOLAR_USER = "WXj0_dEAAAAJ"          # Yukang Jiang's Google Scholar user id
HTML_FILE = "index.html"
MARKER = re.compile(r'(<div class="n" id="cite-count">)\d+(</div>)')


def from_serpapi(key: str) -> int:
    import json
    import urllib.request
    url = (
        "https://serpapi.com/search.json"
        f"?engine=google_scholar_author&author_id={SCHOLAR_USER}&api_key={key}"
    )
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.load(resp)
    return int(data["cited_by"]["table"][0]["citations"]["all"])


def from_scholarly() -> int:
    from scholarly import scholarly
    author = scholarly.search_author_id(SCHOLAR_USER)
    author = scholarly.fill(author, sections=["indices"])
    return int(author["citedby"])


def get_citations() -> int:
    key = os.environ.get("SERPAPI_KEY", "").strip()
    if key:
        return from_serpapi(key)
    return from_scholarly()


def main() -> None:
    try:
        cites = get_citations()
    except Exception as exc:  # noqa: BLE001 - best-effort; never fail the job
        print(f"::warning::Could not fetch citations ({exc}); leaving page unchanged.")
        return
    if not cites or cites < 1:
        print("::warning::Got a non-positive citation count; leaving page unchanged.")
        return

    with open(HTML_FILE, encoding="utf-8") as fh:
        html = fh.read()

    if not MARKER.search(html):
        print("::error::Could not find the cite-count marker in index.html.")
        sys.exit(1)

    new_html = MARKER.sub(rf"\g<1>{cites}\g<2>", html)
    if new_html == html:
        print(f"Citations unchanged ({cites}).")
        return

    with open(HTML_FILE, "w", encoding="utf-8") as fh:
        fh.write(new_html)
    print(f"Updated citation count to {cites}.")


if __name__ == "__main__":
    main()
