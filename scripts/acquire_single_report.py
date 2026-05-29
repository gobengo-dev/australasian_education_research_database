"""
Script:
    acquire_single_report.py

Purpose:
    Download a single PDF artefact and record acquisition metadata.

Project:
    Australasian Educational Research

Author:
    Ben

Status:
    v0.1

Inputs:
    Hard-coded source URL for first CESE acquisition test.

Outputs:
    PDF artefact saved to data/raw/cese/
    Acquisition metadata appended to manifests/acquisition_manifest.jsonl
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests


SOURCE_ORGANISATION = "CESE"
SOURCE_URL = (
    "https://education.nsw.gov.au/content/dam/main-education/about-us/"
    "educational-data/cese/2020-classroom-management-literature-review.pdf"
)
RETRIEVED_BY = "ben"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "cese"
MANIFEST_PATH = PROJECT_ROOT / "manifests" / "acquisition_manifest.jsonl"


def get_source_filename(url: str) -> str:
    """Extract the source filename from the URL path."""
    path = urlparse(url).path
    filename = Path(path).name

    if not filename:
        raise ValueError(f"Could not determine filename from URL: {url}")

    return filename


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 hash for a local file."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def download_file(url: str, destination: Path) -> str:
    """Download a file from URL to destination and return response MIME type."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)

    return response.headers.get("Content-Type", "unknown")


def append_manifest_record(record: dict) -> None:
    """Append a JSON record to the acquisition manifest."""
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    with MANIFEST_PATH.open("a", encoding="utf-8") as manifest:
        manifest.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    source_filename = get_source_filename(SOURCE_URL)
    local_path = RAW_DIR / source_filename

    print(f"Downloading: {SOURCE_URL}")
    print(f"Saving to: {local_path}")

    mime_type = download_file(SOURCE_URL, local_path)
    sha256 = calculate_sha256(local_path)
    file_size_bytes = local_path.stat().st_size

    record = {
        "source_organisation": SOURCE_ORGANISATION,
        "source_url": SOURCE_URL,
        "source_filename": source_filename,
        "local_filename": source_filename,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "retrieved_by": RETRIEVED_BY,
        "acquisition_method": "script",
        "acquisition_script": "acquire_single_report.py",
        "retrieval_status": "success",
        "mime_type": mime_type,
        "sha256": sha256,
        "file_size_bytes": file_size_bytes,
    }

    append_manifest_record(record)

    print("Acquisition complete.")
    print(f"SHA-256: {sha256}")
    print(f"File size: {file_size_bytes} bytes")
    print(f"Manifest updated: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()