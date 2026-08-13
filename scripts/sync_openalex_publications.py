#!/usr/bin/env python3
"""
sync_openalex_publications.py

Fetch works for ORCID 0000-0002-8332-3408 from the OpenAlex API and write a
hidden Sphinx test page (Publications/openalex.rst) in the site's publications
list-table layout.

Input:  OpenAlex works endpoint (no local data files)
Output: Publications/openalex.rst (overwritten when the publication list changes)

Created by Michael Sieler
Last updated: 2026-08-13
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ORCID = "0000-0002-8332-3408"
MAILTO = "Michael.SielerJr@UniGe.ch"
OWN_NAME = "**Michael J. Sieler Jr.**"
USER_AGENT = f"michaelsieler.com OpenAlex publications sync (mailto:{MAILTO})"
PER_PAGE = 200
SKIP_TYPES = {"paratext"}
ARTICLE_TYPES = {"article", "review", "letter"}
PREPRINT_TYPES = {"preprint"}
SKIP_DOI_PREFIXES = ("10.6084/",)  # Figshare supplementary objects
SKIP_TITLE_PREFIXES = ("additional file", "supplementary")

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_RST = REPO_ROOT / "Publications" / "openalex.rst"


def fetch_works() -> list[dict]:
    """Return all OpenAlex works for ORCID, following cursor pagination."""
    works: list[dict] = []
    cursor = "*"
    while cursor:
        query = urllib.parse.urlencode(
            {
                "filter": f"author.orcid:{ORCID}",
                "per-page": PER_PAGE,
                "cursor": cursor,
                "mailto": MAILTO,
            }
        )
        url = f"https://api.openalex.org/works?{query}"
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise SystemExit(f"OpenAlex request failed: {exc}") from exc

        works.extend(payload.get("results") or [])
        cursor = (payload.get("meta") or {}).get("next_cursor")

    return works


def normalize_doi(doi: str | None) -> str:
    if not doi:
        return ""
    value = doi.strip().lower()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    return value


def normalize_title(title: str) -> str:
    lowered = title.lower()
    stripped = re.sub(r"[^a-z0-9]+", " ", lowered)
    return stripped.strip()


def work_doi(work: dict) -> str:
    ids = work.get("ids") or {}
    return normalize_doi(ids.get("doi") or "")


def work_url(work: dict) -> str:
    doi = work_doi(work)
    if doi:
        return f"https://doi.org/{doi}"
    location = work.get("primary_location") or {}
    return (location.get("landing_page_url") or "").strip()


def work_venue(work: dict) -> str:
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    return (source.get("display_name") or "").strip()


def work_year(work: dict) -> str:
    year = work.get("publication_year")
    return str(year) if year else ""


def is_own_author(name: str) -> bool:
    lowered = name.lower()
    return "michael" in lowered and "sieler" in lowered


def format_authors(work: dict) -> str:
    names: list[str] = []
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        raw = (author.get("display_name") or authorship.get("raw_author_name") or "").strip()
        if not raw:
            continue
        names.append(OWN_NAME if is_own_author(raw) else raw)
    return ", ".join(names)


def work_type(work: dict) -> str:
    return (work.get("type") or "").strip().lower()


def is_supplement(work: dict) -> bool:
    """Drop Figshare/supplementary objects that OpenAlex sometimes types as articles."""
    if work.get("is_paratext"):
        return True
    title = (work.get("display_name") or "").strip().lower()
    if any(title.startswith(prefix) for prefix in SKIP_TITLE_PREFIXES):
        return True
    doi = work_doi(work)
    return any(doi.startswith(prefix) for prefix in SKIP_DOI_PREFIXES)


def type_rank(work: dict) -> int:
    """Lower is better when choosing among duplicates (article over preprint)."""
    kind = work_type(work)
    if kind in ARTICLE_TYPES:
        return 0
    if kind in PREPRINT_TYPES:
        return 1
    return 2


def deduplicate(works: list[dict]) -> list[dict]:
    """Keep one record per DOI; if a preprint and article share a title, keep the article."""
    by_doi: dict[str, dict] = {}
    no_doi: list[dict] = []

    for work in works:
        kind = work_type(work)
        if kind in SKIP_TYPES or is_supplement(work):
            continue
        if kind not in ARTICLE_TYPES | PREPRINT_TYPES:
            continue

        doi = work_doi(work)
        if not doi:
            no_doi.append(work)
            continue
        current = by_doi.get(doi)
        if current is None or type_rank(work) < type_rank(current):
            by_doi[doi] = work

    chosen = list(by_doi.values()) + no_doi
    by_title: dict[str, dict] = {}
    for work in chosen:
        title_key = normalize_title(work.get("display_name") or "")
        if not title_key:
            continue
        current = by_title.get(title_key)
        if current is None or type_rank(work) < type_rank(current):
            by_title[title_key] = work

    return list(by_title.values())


def escape_rst_title(title: str) -> str:
    """Make a title safe inside an RST quoted hyperlink."""
    cleaned = title.replace("`", "'").replace('"', "'")
    return " ".join(cleaned.split())


def escape_rst_italic(text: str) -> str:
    return text.replace("*", r"\*")


def rst_entry(work: dict) -> str:
    title = escape_rst_title(work.get("display_name") or "Untitled")
    url = work_url(work)
    venue = escape_rst_italic(work_venue(work))
    authors = format_authors(work) or "*authors unavailable*"
    year = work_year(work) or "n.d."

    if url:
        title_part = f'`"{title}" <{url}>`_'
    else:
        title_part = f'"{title}"'

    venue_part = f" *{venue}*" if venue else ""
    return (
        f"   * - {title_part}{venue_part}\n"
        f"\n"
        f"       - {authors}\n"
        f"     - {year}\n"
    )


def list_table(works: list[dict]) -> str:
    rows = [rst_entry(work) for work in works]
    return (
        ".. list-table::\n"
        "   :widths: 90 10\n"
        "\n"
        + "".join(rows)
    )


def split_sections(works: list[dict]) -> tuple[list[dict], list[dict]]:
    articles: list[dict] = []
    preprints: list[dict] = []
    for work in works:
        if work_type(work) in PREPRINT_TYPES:
            preprints.append(work)
        else:
            articles.append(work)

    def sort_key(work: dict) -> tuple[int, str]:
        year = work.get("publication_year") or 0
        title = (work.get("display_name") or "").lower()
        return (-int(year), title)

    articles.sort(key=sort_key)
    preprints.sort(key=sort_key)
    return articles, preprints


def body_without_timestamp(rst: str) -> str:
    return re.sub(r"^Last synced:.*$", "Last synced:", rst, count=1, flags=re.MULTILINE)


def render_rst(articles: list[dict], preprints: list[dict], synced_at: str) -> str:
    article_block = (
        list_table(articles)
        if articles
        else "No peer-reviewed works were returned by OpenAlex.\n"
    )
    preprint_block = (
        list_table(preprints)
        if preprints
        else "No preprints were returned by OpenAlex.\n"
    )

    title = "OpenAlex publications (test)"
    underline = "=" * len(title)
    section = "Peer-reviewed publications"
    section_line = "-" * len(section)
    preprint_heading = "Preprints"
    preprint_line = '"' * len(preprint_heading)

    return (
        ":orphan:\n"
        "\n"
        ".. meta::\n"
        "   :robots: noindex\n"
        "\n"
        ".. _Top:\n"
        "\n"
        "\n"
        f"{title}\n"
        f"{underline}\n"
        "\n"
        "This page is generated from `OpenAlex <https://openalex.org/>`_ using ORCID "
        f"`{ORCID} <https://orcid.org/{ORCID}>`_. It is a test of automated publication "
        "sync and is not linked from the site navigation. See the official "
        "`Publications <publications.html>`_ page for the curated list.\n"
        "\n"
        "Do not edit this file by hand; it is overwritten by "
        "``scripts/sync_openalex_publications.py``.\n"
        "\n"
        f"Last synced: {synced_at} UTC\n"
        "\n"
        f"{section}\n"
        f"{section_line}\n"
        "\n"
        f"{article_block}"
        "\n"
        f"{preprint_heading}\n"
        f"{preprint_line}\n"
        "\n"
        f"{preprint_block}"
        "\n"
        "------\n"
        "\n"
        "Return to `top`_.\n"
        "\n"
        "------\n"
    )


def main() -> int:
    works = fetch_works()
    unique_works = deduplicate(works)
    articles, preprints = split_sections(unique_works)
    synced_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    rst = render_rst(articles, preprints, synced_at)

    OUTPUT_RST.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_RST.exists():
        existing = OUTPUT_RST.read_text(encoding="utf-8")
        if body_without_timestamp(existing) == body_without_timestamp(rst):
            print(
                f"No publication changes "
                f"({len(articles)} articles, {len(preprints)} preprints)."
            )
            return 0

    OUTPUT_RST.write_text(rst, encoding="utf-8")
    print(
        f"Wrote {OUTPUT_RST.relative_to(REPO_ROOT)} "
        f"({len(articles)} articles, {len(preprints)} preprints)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
