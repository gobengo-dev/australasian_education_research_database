"""
Script:
    acquire_cese_reports.py

Purpose:
    Download a small set of CESE PDF artefacts and record acquisition metadata.

Project:
    Australasian Educational Research

Author:
    Ben

Status:
    v0.1

Inputs:
    Hard-coded list of CESE PDF URLs.

Outputs:
    PDF artefacts saved to data/raw/cese/
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
RETRIEVED_BY = "ben"
ACQUISITION_SCRIPT = "acquire_cese_reports.py"

REPORT_URLS = [
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2020-classroom-management-infographic.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2017-cognitive-load-theory-summary.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2017-cognitive-load-theory.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/revisiting-gifted-education-literature-review.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2019-revisiting-gifted-education-summary.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2013-gtil-what-does-the-evidence-tell-us-about-effective-teaching.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2013-rural-and-remote-education.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2014-children-with-disability-in-inclusive-early-childhood-education-and-care.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2014-elements-of-effective-professional-development.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2014-qualifications-for-early-childhood-educators-working-with-0-to-2-year-olds.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2014-school-improvement-frameworks-the-evidence-base.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2015-school-assets-and-student-outcomes.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2015-student-wellbeing-summary.pdf",
    "https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2015-student-wellbeing.pdf",
]

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


def read_manifest_source_urls() -> set[str]:
    """Read existing source URLs from the acquisition manifest."""
    if not MANIFEST_PATH.exists():
        return set()

    source_urls = set()

    with MANIFEST_PATH.open("r", encoding="utf-8") as manifest:
        for line in manifest:
            line = line.strip()
            if not line:
                continue

            record = json.loads(line)
            source_url = record.get("source_url")

            if source_url:
                source_urls.add(source_url)

    return source_urls


def acquire_report(url: str, existing_source_urls: set[str]) -> str:
    """Acquire one report unless it already appears in the manifest."""
    if url in existing_source_urls:
        print(f"Already recorded in manifest, skipping: {url}")
        return "skipped_manifest"

    source_filename = get_source_filename(url)
    local_path = RAW_DIR / source_filename

    if local_path.exists():
        print(f"File already exists locally, skipping download: {local_path}")
        sha256 = calculate_sha256(local_path)
        file_size_bytes = local_path.stat().st_size
        mime_type = "unknown_existing_file"
    else:
        print(f"Downloading: {url}")
        print(f"Saving to: {local_path}")

        mime_type = download_file(url, local_path)
        sha256 = calculate_sha256(local_path)
        file_size_bytes = local_path.stat().st_size

    record = {
        "source_organisation": SOURCE_ORGANISATION,
        "source_url": url,
        "source_filename": source_filename,
        "local_filename": source_filename,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "retrieved_by": RETRIEVED_BY,
        "acquisition_method": "script",
        "acquisition_script": ACQUISITION_SCRIPT,
        "retrieval_status": "success",
        "mime_type": mime_type,
        "sha256": sha256,
        "file_size_bytes": file_size_bytes,
    }

    append_manifest_record(record)
    print(f"Recorded acquisition: {source_filename}")

    return "acquired"


def main() -> None:
    existing_source_urls = read_manifest_source_urls()

    acquired_count = 0
    skipped_count = 0
    failed_count = 0

    for url in REPORT_URLS:
        try:
            result = acquire_report(url, existing_source_urls)

            if result == "acquired":
                acquired_count += 1
                existing_source_urls.add(url)
            elif result == "skipped_manifest":
                skipped_count += 1

        except Exception as error:
            failed_count += 1
            print(f"FAILED: {url}")
            print(f"Reason: {error}")

    print("Batch acquisition complete.")
    print(f"Acquired: {acquired_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Failed: {failed_count}")
    print(f"Manifest updated: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()