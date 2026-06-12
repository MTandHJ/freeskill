#!/usr/bin/env python

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

USER_AGENT = "paperpost-skill/0.1"
HREF_PATTERN = re.compile(r"""href=["'](?P<href>[^"']+)["']""", re.IGNORECASE)
PDF_META_PATTERN = re.compile(
    r"""<meta[^>]+name=["']citation_pdf_url["'][^>]+content=["'](?P<url>[^"']+)["']""",
    re.IGNORECASE,
)


class ResolveInputError(RuntimeError):
    r"""Error raised when a paper path or URL cannot be resolved into a local PDF."""


def main(argv: Optional[Sequence[str]] = None) -> int:
    r"""Resolve a paper path or URL and print a JSON description.

    Parameters
    ----------
    argv : Optional[Sequence[str]], optional
        Command-line arguments. When omitted, arguments are read from `sys.argv`.
    """

    parser = argparse.ArgumentParser(description="Resolve a paper path or URL into a local PDF.")
    parser.add_argument(
        "source",
        metavar="PATH_OR_URL",
        help="Local PDF path, arXiv URL, PDF URL, or paper URL.",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="Network timeout in seconds.")
    namespace = parser.parse_args(argv)

    try:
        result = resolve_input(namespace.source, timeout=namespace.timeout)
    except ResolveInputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def resolve_input(source: str, timeout: float = 30.0) -> Dict[str, Any]:
    r"""Return a normalized JSON-ready description for a paper path or URL."""

    path = Path(source).expanduser()
    if path.exists():
        return resolve_local_pdf(path)

    if not is_url(source):
        raise ResolveInputError(f"local PDF does not exist; provide a valid PDF path: {source}")

    arxiv = parse_arxiv_url(source)
    if arxiv is not None:
        kind, arxiv_id, pdf_url = arxiv
        return download_pdf(
            pdf_url,
            kind=kind,
            source=source,
            timeout=timeout,
            arxiv_id=arxiv_id,
        )

    if looks_like_pdf_url(source):
        return download_pdf(source, kind="pdf_url", source=source, timeout=timeout)

    pdf_url = find_pdf_url(source, timeout=timeout)
    return download_pdf(pdf_url, kind="paper_url", source=source, timeout=timeout)


def resolve_local_pdf(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise ResolveInputError(f"local path exists but is not a file: {path}")

    warnings: List[str] = []
    if path.suffix.lower() != ".pdf":
        warnings.append("local file extension is not .pdf; verify that it is a PDF")

    return {
        "source": str(path),
        "kind": "local_pdf",
        "pdf_path": str(path.resolve()),
        "pdf_url": "",
        "source_url": "",
        "arxiv_id": "",
        "warnings": warnings,
    }


def parse_arxiv_url(url: str) -> Optional[tuple[str, str, str]]:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.lower() not in {"arxiv.org", "www.arxiv.org"}:
        return None

    path = parsed.path.strip("/")
    if path.startswith("abs/"):
        arxiv_id = path.removeprefix("abs/").removesuffix(".pdf")
        return "arxiv_abs", arxiv_id, build_arxiv_pdf_url(arxiv_id)

    if path.startswith("pdf/"):
        arxiv_id = path.removeprefix("pdf/").removesuffix(".pdf")
        return "arxiv_pdf", arxiv_id, build_arxiv_pdf_url(arxiv_id)

    return None


def build_arxiv_pdf_url(arxiv_id: str) -> str:
    return f"https://arxiv.org/pdf/{arxiv_id}.pdf"


def is_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def looks_like_pdf_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return parsed.path.lower().endswith(".pdf")


def find_pdf_url(page_url: str, timeout: float) -> str:
    html_text = read_url_text(page_url, timeout=timeout)
    candidates = extract_pdf_candidates(page_url, html_text)
    if not candidates:
        raise ResolveInputError(
            "could not find a PDF link from the paper URL; ask the user to provide a PDF"
        )
    return candidates[0]


def extract_pdf_candidates(page_url: str, html_text: str) -> List[str]:
    candidates: List[str] = []

    for match in PDF_META_PATTERN.finditer(html_text):
        add_candidate(candidates, page_url, html.unescape(match.group("url")))

    for match in HREF_PATTERN.finditer(html_text):
        add_candidate(candidates, page_url, html.unescape(match.group("href")))

    return candidates


def add_candidate(candidates: List[str], page_url: str, href: str) -> None:
    url = urllib.parse.urljoin(page_url, href.strip())
    arxiv = parse_arxiv_url(url)
    if arxiv is not None:
        url = arxiv[2]

    if looks_like_pdf_url(url) and url not in candidates:
        candidates.append(url)


def read_url_text(url: str, timeout: float) -> str:
    request = build_request(url)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except urllib.error.URLError as exc:
        raise ResolveInputError(
            f"failed to read paper URL; ask the user to provide a PDF: {exc}"
        ) from exc


def download_pdf(
    url: str,
    kind: str,
    source: str,
    timeout: float,
    arxiv_id: str = "",
) -> Dict[str, Any]:
    request = build_request(url)
    output_path = build_temp_pdf_path(url, arxiv_id=arxiv_id)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read()
    except urllib.error.URLError as exc:
        raise ResolveInputError(
            f"failed to download PDF; ask the user to provide a PDF: {exc}"
        ) from exc

    if not data.startswith(b"%PDF"):
        raise ResolveInputError(f"downloaded content is not a PDF: {url}")

    output_path.write_bytes(data)
    return {
        "source": source,
        "kind": kind,
        "pdf_path": str(output_path),
        "pdf_url": url,
        "source_url": source,
        "arxiv_id": arxiv_id,
        "warnings": [],
    }


def build_temp_pdf_path(url: str, arxiv_id: str = "") -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="paperpost-"))
    if arxiv_id:
        name = sanitize_filename(arxiv_id) + ".pdf"
    else:
        name = sanitize_filename(Path(urllib.parse.urlparse(url).path).name or "paper.pdf")
        if not name.lower().endswith(".pdf"):
            name += ".pdf"
    return temp_dir / name


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")
    return cleaned or "paper.pdf"


def build_request(url: str) -> urllib.request.Request:
    return urllib.request.Request(url, headers={"User-Agent": USER_AGENT})


if __name__ == "__main__":
    raise SystemExit(main())
