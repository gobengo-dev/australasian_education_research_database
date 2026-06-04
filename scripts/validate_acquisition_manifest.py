"""
Script:
    validate_acquisition_manifest.py

Purpose:
    Validate that acquisition manifest records correspond to preserved local
    artefacts, and that recorded file sizes and SHA-256 hashes still match.

Project:
    Australasian Educational Research

Author:
    Ben

Status:
    v0.1

Inputs:
    manifests/acquisition_manifest.jsonl
    data/raw/

Outputs:
    Console validation report

Notes:
    This script is read-only. It does not repair files, rewrite manifests,
    rename artefacts, or mutate project data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST_PATH = Path("manifests/acquisition_manifest.jsonl")
DEFAULT_RAW_ROOT = Path("data/raw")


PATH_KEYS = [
    "local_path",
    "local_file_path",
    "file_path",
    "path",
]

FILENAME_KEYS = [
    "local_filename",
    "filename",
    "file_name",
    "source_filename",
]

ORG_KEYS = [
    "source_organisation",
    "source_organization",
    "organisation",
    "organization",
    "source",
]

SHA256_KEYS = [
    "sha256",
    "sha_256",
    "sha256_hash",
    "file_sha256",
    "checksum",
]

SIZE_KEYS = [
    "file_size",
    "size_bytes",
    "file_size_bytes",
    "bytes",
]


def calculate_sha256(path: Path) -> str:
    """Calculate SHA-256 hash for a local file."""
    hash_object = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            hash_object.update(chunk)

    return hash_object.hexdigest()


def first_present_value(record: dict[str, Any], keys: list[str]) -> Any | None:
    """Return the first non-empty value found in a record for the given keys."""
    for key in keys:
        value = record.get(key)
        if value not in (None, ""):
            return value
    return None


def normalise_org_name(value: Any) -> str | None:
    """Normalise a source organisation value for use as a folder name."""
    if value is None:
        return None

    text = str(value).strip().lower()

    if text in {"cese", "aero"}:
        return text

    return text or None


def resolve_manifest_file_path(
    record: dict[str, Any],
    raw_root: Path,
) -> Path | None:
    """
    Resolve the local artefact path from a manifest record.

    Resolution order:
    1. Use explicit local path if present.
    2. Use organisation + filename if present.
    3. Search data/raw recursively for a unique matching filename.
    """
    explicit_path = first_present_value(record, PATH_KEYS)

    if explicit_path is not None:
        path = Path(str(explicit_path))

        if path.is_absolute():
            return path

        return Path.cwd() / path

    filename = first_present_value(record, FILENAME_KEYS)

    if filename is None:
        return None

    filename = str(filename)
    org_name = normalise_org_name(first_present_value(record, ORG_KEYS))

    if org_name is not None:
        candidate = raw_root / org_name / filename
        if candidate.exists():
            return candidate

    matches = list(raw_root.rglob(filename))

    if len(matches) == 1:
        return matches[0]

    return None


def parse_manifest(manifest_path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Read newline-delimited JSON manifest records."""
    records: list[dict[str, Any]] = []
    errors: list[str] = []

    if not manifest_path.exists():
        errors.append(f"Manifest not found: {manifest_path}")
        return records, errors

    with manifest_path.open("r", encoding="utf-8") as manifest_file:
        for line_number, line in enumerate(manifest_file, start=1):
            stripped_line = line.strip()

            if not stripped_line:
                continue

            try:
                record = json.loads(stripped_line)
            except json.JSONDecodeError as error:
                errors.append(
                    f"Line {line_number}: invalid JSON "
                    f"({error.msg})"
                )
                continue

            if not isinstance(record, dict):
                errors.append(
                    f"Line {line_number}: manifest entry is not a JSON object"
                )
                continue

            record["_manifest_line_number"] = line_number
            records.append(record)

    return records, errors


def find_raw_pdf_files(raw_root: Path) -> set[Path]:
    """Return all PDF files currently present under the raw data directory."""
    if not raw_root.exists():
        return set()

    return {path.resolve() for path in raw_root.rglob("*.pdf") if path.is_file()}


def validate_manifest(
    manifest_path: Path,
    raw_root: Path,
) -> int:
    """Validate manifest records against local raw artefacts."""
    manifest_path = manifest_path.resolve()
    raw_root = raw_root.resolve()

    records, parse_errors = parse_manifest(manifest_path)

    missing_files: list[str] = []
    unresolved_paths: list[str] = []
    hash_mismatches: list[str] = []
    size_mismatches: list[str] = []
    missing_hash_values: list[str] = []
    missing_size_values: list[str] = []
    checked_files: list[Path] = []

    for record in records:
        line_number = record.get("_manifest_line_number", "?")
        resolved_path = resolve_manifest_file_path(record, raw_root)

        if resolved_path is None:
            unresolved_paths.append(
                f"Line {line_number}: could not resolve local file path"
            )
            continue

        resolved_path = resolved_path.resolve()

        if not resolved_path.exists():
            missing_files.append(
                f"Line {line_number}: missing file: {resolved_path}"
            )
            continue

        checked_files.append(resolved_path)

        recorded_hash = first_present_value(record, SHA256_KEYS)
        if recorded_hash is None:
            missing_hash_values.append(
                f"Line {line_number}: no recorded SHA-256 value"
            )
        else:
            recorded_hash = str(recorded_hash).lower()
            actual_hash = calculate_sha256(resolved_path)

            if recorded_hash != actual_hash:
                hash_mismatches.append(
                    f"Line {line_number}: hash mismatch for {resolved_path}"
                )

        recorded_size = first_present_value(record, SIZE_KEYS)
        if recorded_size is None:
            missing_size_values.append(
                f"Line {line_number}: no recorded file size"
            )
        else:
            try:
                recorded_size_int = int(recorded_size)
                actual_size = resolved_path.stat().st_size

                if recorded_size_int != actual_size:
                    size_mismatches.append(
                        "Line "
                        f"{line_number}: size mismatch for {resolved_path} "
                        f"(manifest={recorded_size_int}, actual={actual_size})"
                    )
            except ValueError:
                size_mismatches.append(
                    f"Line {line_number}: recorded file size is not an integer"
                )

    checked_file_set = {path.resolve() for path in checked_files}
    raw_pdf_files = find_raw_pdf_files(raw_root)
    orphan_files = sorted(raw_pdf_files - checked_file_set)

    file_counter = Counter(checked_files)
    duplicate_manifest_paths = [
        path for path, count in file_counter.items() if count > 1
    ]

    hash_values = [
        str(first_present_value(record, SHA256_KEYS)).lower()
        for record in records
        if first_present_value(record, SHA256_KEYS) is not None
    ]
    duplicate_hashes = [
        hash_value
        for hash_value, count in Counter(hash_values).items()
        if count > 1
    ]

    failures = (
        parse_errors
        + unresolved_paths
        + missing_files
        + hash_mismatches
        + size_mismatches
        + missing_hash_values
        + missing_size_values
    )

    print()
    print("Acquisition manifest validation")
    print("=" * 33)
    print(f"Manifest: {manifest_path}")
    print(f"Raw root: {raw_root}")
    print()
    print(f"Manifest records: {len(records)}")
    print(f"Files checked: {len(checked_files)}")
    print(f"Raw PDF files found: {len(raw_pdf_files)}")
    print(f"JSON parse errors: {len(parse_errors)}")
    print(f"Unresolved manifest paths: {len(unresolved_paths)}")
    print(f"Missing files: {len(missing_files)}")
    print(f"Hash mismatches: {len(hash_mismatches)}")
    print(f"Size mismatches: {len(size_mismatches)}")
    print(f"Missing hash values: {len(missing_hash_values)}")
    print(f"Missing size values: {len(missing_size_values)}")
    print(f"Orphan PDF files: {len(orphan_files)}")
    print(f"Duplicate manifest paths: {len(duplicate_manifest_paths)}")
    print(f"Duplicate recorded hashes: {len(duplicate_hashes)}")
    print()

    if failures:
        print("Validation problems")
        print("-" * 19)

        for problem in failures:
            print(f"- {problem}")

        print()

    if orphan_files:
        print("Orphan PDF files")
        print("-" * 16)

        for path in orphan_files:
            print(f"- {path}")

        print()

    if duplicate_manifest_paths:
        print("Duplicate manifest paths")
        print("-" * 24)

        for path in duplicate_manifest_paths:
            print(f"- {path}")

        print()

    if duplicate_hashes:
        print("Duplicate recorded hashes")
        print("-" * 25)

        for hash_value in duplicate_hashes:
            print(f"- {hash_value}")

        print()

    if failures or orphan_files:
        print("Status: FAIL")
        return 1

    print("Status: PASS")
    return 0


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Validate acquisition manifest records against raw files."
    )

    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST_PATH,
        help="Path to acquisition manifest JSONL file.",
    )

    parser.add_argument(
        "--raw-root",
        type=Path,
        default=DEFAULT_RAW_ROOT,
        help="Path to raw artefact root directory.",
    )

    args = parser.parse_args()

    return validate_manifest(
        manifest_path=args.manifest,
        raw_root=args.raw_root,
    )


if __name__ == "__main__":
    sys.exit(main())