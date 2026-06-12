#!/usr/bin/env python

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

URL_PATTERN = re.compile(r"https?://[^\s)<>\"]+")
ABSTRACT_PATTERN = re.compile(
    r"\babstract\b\s*[:.\-]?\s*(?P<abstract>.*?)(?:\n\s*(?:1\.?\s+)?introduction\b|\n\s*keywords\b)",
    re.IGNORECASE | re.DOTALL,
)


class PDFParseError(RuntimeError):
    r"""Error raised when a PDF cannot be parsed into JSON-ready content."""


def main(argv: Optional[Sequence[str]] = None) -> int:
    r"""Parse a local PDF and print extracted paper text as JSON.

    Parameters
    ----------
    argv : Optional[Sequence[str]], optional
        Command-line arguments. When omitted, arguments are read from `sys.argv`.
    """

    parser = argparse.ArgumentParser(description="Parse a local PDF for paperpost.")
    parser.add_argument("pdf", type=Path, help="Path to a local PDF file.")
    namespace = parser.parse_args(argv)

    try:
        result = parse_pdf(namespace.pdf)
    except PDFParseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def parse_pdf(pdf_path: Path) -> Dict[str, Any]:
    r"""Extract title, metadata, text, links, and warnings from a PDF."""

    path = pdf_path.expanduser()
    if not path.exists():
        raise PDFParseError(f"PDF does not exist: {path}")
    if not path.is_file():
        raise PDFParseError(f"PDF path is not a file: {path}")

    parser = choose_pdf_parser()
    metadata, pages = parser(path)
    text = "\n\n".join(page for page in pages if page.strip())
    warnings = build_warnings(metadata, text, pages)

    return {
        "pdf_path": str(path.resolve()),
        "title": infer_title(metadata, pages),
        "authors": split_authors(metadata.get("author", "")),
        "abstract": extract_abstract(text),
        "page_count": len(pages),
        "text": text,
        "links": extract_links(text),
        "warnings": warnings,
    }


def choose_pdf_parser() -> Any:
    if importlib.util.find_spec("pypdf") is not None:
        return parse_with_pypdf

    if importlib.util.find_spec("fitz") is not None:
        return parse_with_pymupdf

    raise PDFParseError(
        "missing PDF parser dependency; install pypdf or pymupdf, then rerun parse_pdf.py"
    )


def parse_with_pypdf(path: Path) -> Tuple[Dict[str, str], List[str]]:
    from pypdf import PdfReader  # type: ignore[import-not-found]

    try:
        reader = PdfReader(str(path))
    except Exception as exc:
        raise PDFParseError(f"pypdf failed to open PDF: {exc}") from exc

    info = reader.metadata or {}
    metadata = {
        "title": clean_text(str(info.get("/Title", "") or "")),
        "author": clean_text(str(info.get("/Author", "") or "")),
    }
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")
    return metadata, pages


def parse_with_pymupdf(path: Path) -> Tuple[Dict[str, str], List[str]]:
    import fitz  # type: ignore[import-not-found]

    try:
        document = fitz.open(path)
    except Exception as exc:
        raise PDFParseError(f"pymupdf failed to open PDF: {exc}") from exc

    metadata = {
        "title": clean_text(document.metadata.get("title", "")),
        "author": clean_text(document.metadata.get("author", "")),
    }
    pages = [page.get_text("text") for page in document]
    document.close()
    return metadata, pages


def infer_title(metadata: Dict[str, str], pages: List[str]) -> str:
    title = metadata.get("title", "").strip()
    if title:
        return title

    for line in first_page_lines(pages):
        lowered = line.lower()
        if lowered not in {"abstract", "introduction"} and len(line) > 8:
            return line
    return ""


def first_page_lines(pages: List[str]) -> List[str]:
    if not pages:
        return []
    return [clean_text(line) for line in pages[0].splitlines() if clean_text(line)]


def split_authors(author_text: str) -> List[str]:
    author_text = clean_text(author_text)
    if not author_text:
        return []

    if ";" in author_text:
        return [part.strip() for part in author_text.split(";") if part.strip()]
    if " and " in author_text:
        return [part.strip() for part in author_text.split(" and ") if part.strip()]
    return [author_text]


def extract_abstract(text: str) -> str:
    match = ABSTRACT_PATTERN.search(text)
    if match is None:
        return ""
    abstract = clean_text(match.group("abstract"))
    return abstract[:4000]


def extract_links(text: str) -> List[str]:
    links = []
    for match in URL_PATTERN.finditer(text):
        url = match.group(0).rstrip(".,;]")
        if url not in links:
            links.append(url)
    return links


def build_warnings(metadata: Dict[str, str], text: str, pages: List[str]) -> List[str]:
    warnings = []
    if not metadata.get("title") and not infer_title(metadata, pages):
        warnings.append("title was not confidently extracted")
    if not metadata.get("author"):
        warnings.append("authors were not extracted from PDF metadata")
    if not extract_abstract(text):
        warnings.append("abstract was not confidently extracted")
    if len(text) < 1000:
        warnings.append("extracted text is short; this may be a scanned or protected PDF")
    return warnings


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


if __name__ == "__main__":
    raise SystemExit(main())
