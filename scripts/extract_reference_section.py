"""
Script:
    extract_reference_section.py

Purpose:
    Extract a raw references section from a PDF artefact using embedded PDF
    text, preserving page-level provenance in the output file.

Project:
    Australasian Educational Research

Author:
    Ben

Status:
    v0.1

Inputs:
    PDF artefact path

Outputs:
    Raw reference-section text file under data/working/reference_sections/

Notes:
    This script is an early extraction workflow for formal reference sections.

    It does not:
    - perform OCR
    - parse individual references
    - clean references aggressively
    - write citation inventories
    - write database records
    - mutate source artefacts
    - mutate acquisition manifests

    It uses embedded PDF text only.

    Artefacts without a formal references section should exit gracefully.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path("data/working/reference_sections")

# Reference-section marker patterns are intentionally anchored to whole lines.
# This avoids matching ordinary prose such as "see references below" while
# allowing formal section headings such as "7. References".
#
# Use [ \t] rather than \s inside these patterns because \s can match newlines.
# Without this guard, a page number on one line followed by "References" on the
# next line can be incorrectly captured as one marker.
REFERENCE_MARKER_PATTERNS = [
    re.compile(
        r"^[ \t]*(?:\d+(?:\.\d+)*\.?[ \t]+)?references[ \t]*$",
        re.IGNORECASE | re.MULTILINE,
    ),
    re.compile(
        r"^[ \t]*(?:\d+(?:\.\d+)*\.?[ \t]+)?reference list[ \t]*$",
        re.IGNORECASE | re.MULTILINE,
    ),
    re.compile(
        r"^[ \t]*(?:\d+(?:\.\d+)*\.?[ \t]+)?bibliography[ \t]*$",
        re.IGNORECASE | re.MULTILINE,
    ),
]

DEFAULT_STOP_MARKER_PATTERNS = [
    re.compile(
        r"^\s*Centre for Education Statistics and Evaluation\s*$",
        re.IGNORECASE | re.MULTILINE,
    ),
    re.compile(
        r"^\s*NSW Department of Education\s*$",
        re.IGNORECASE | re.MULTILINE,
    ),
    re.compile(
        r"^\s*Please cite this publication as:\s*$",
        re.IGNORECASE | re.MULTILINE,
    ),
]


@dataclass
class ReferenceMarker:
    """Location of a detected references-section marker."""

    page_number: int
    marker_text: str
    start_index: int


@dataclass
class StopMarker:
    """Location of a detected post-references stop marker."""

    page_number: int
    marker_text: str
    start_index: int


def import_pypdf():
    """
    Import pypdf with a clear error message if it is unavailable.

    pypdf is used for embedded text extraction only.
    OCR is intentionally not performed by this script.
    """
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError:
        print()
        print("Missing dependency: pypdf")
        print()
        print("Install it inside the project virtual environment:")
        print()
        print("    venv/bin/python -m pip install pypdf")
        print()
        print("Then add it to requirements.txt if adopted:")
        print()
        print("    venv/bin/python -m pip freeze > requirements.txt")
        print()
        return None

    return PdfReader


def normalise_whitespace(text: str) -> str:
    """
    Normalise whitespace enough for marker detection and readable output.

    This is intentionally light-touch. The purpose is not to clean references
    into canonical form, but to preserve a usable raw extraction layer.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_page_text(reader) -> list[str]:
    """Extract embedded text from each PDF page."""
    page_texts: list[str] = []

    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception as error:  # noqa: BLE001
            text = f"[TEXT EXTRACTION ERROR: {error}]"

        page_texts.append(normalise_whitespace(text))

    return page_texts


def find_reference_marker(page_texts: list[str]) -> ReferenceMarker | None:
    """
    Find the first likely references-section marker.

    Returns:
        ReferenceMarker if found, otherwise None.
    """
    for page_index, page_text in enumerate(page_texts):
        candidates: list[ReferenceMarker] = []

        for pattern in REFERENCE_MARKER_PATTERNS:
            match = pattern.search(page_text)

            if match:
                candidates.append(
                    ReferenceMarker(
                        page_number=page_index + 1,
                        marker_text=match.group(0).strip(),
                        start_index=match.start(),
                    )
                )

        if candidates:
            return sorted(candidates, key=lambda item: item.start_index)[0]

    return None


def find_stop_marker_after_reference_start(
    page_texts: list[str],
    reference_marker: ReferenceMarker,
) -> StopMarker | None:
    """
    Find the first likely post-references stop marker after the reference start.

    This is deliberately conservative. If no stop marker is found, extraction
    continues to the end of the document.
    """
    for page_index, page_text in enumerate(page_texts):
        page_number = page_index + 1

        if page_number < reference_marker.page_number:
            continue

        search_start_index = 0

        if page_number == reference_marker.page_number:
            search_start_index = reference_marker.start_index + len(
                reference_marker.marker_text
            )

        candidates: list[StopMarker] = []

        for pattern in DEFAULT_STOP_MARKER_PATTERNS:
            match = pattern.search(page_text, search_start_index)

            if match:
                candidates.append(
                    StopMarker(
                        page_number=page_number,
                        marker_text=match.group(0).strip(),
                        start_index=match.start(),
                    )
                )

        if candidates:
            return sorted(candidates, key=lambda item: item.start_index)[0]

    return None


def extract_reference_section_pages(
    page_texts: list[str],
    reference_marker: ReferenceMarker,
    stop_marker: StopMarker | None,
) -> list[tuple[int, str]]:
    """
    Extract raw references text while preserving page numbers.

    Returns:
        A list of tuples:
            (one-based page number, page-level extracted references text)
    """
    extracted_pages: list[tuple[int, str]] = []

    for page_index, page_text in enumerate(page_texts):
        page_number = page_index + 1

        if page_number < reference_marker.page_number:
            continue

        if stop_marker and page_number > stop_marker.page_number:
            break

        start_index = 0
        end_index = len(page_text)

        if page_number == reference_marker.page_number:
            start_index = reference_marker.start_index

        if stop_marker and page_number == stop_marker.page_number:
            end_index = stop_marker.start_index

        extracted_text = page_text[start_index:end_index].strip()

        if extracted_text:
            extracted_pages.append((page_number, extracted_text))

    return extracted_pages


def build_output_text(
    pdf_path: Path,
    reference_marker: ReferenceMarker,
    stop_marker: StopMarker | None,
    extracted_pages: list[tuple[int, str]],
) -> str:
    """Build the raw reference-section output file text."""
    if extracted_pages:
        first_page = extracted_pages[0][0]
        last_page = extracted_pages[-1][0]
    else:
        first_page = reference_marker.page_number
        last_page = reference_marker.page_number

    header_lines = [
        f"Source PDF: {pdf_path}",
        "",
        "Extraction method: embedded PDF text via pypdf",
        "OCR performed: no",
        "Extraction type: raw reference section",
        "",
        f"Reference marker: {reference_marker.marker_text}",
        f"Reference marker page: {reference_marker.page_number}",
        f"Extracted page range: {first_page}-{last_page}",
    ]

    if stop_marker:
        header_lines.extend(
            [
                f"Stop marker: {stop_marker.marker_text}",
                f"Stop marker page: {stop_marker.page_number}",
            ]
        )
    else:
        header_lines.append("Stop marker: none detected")

    header_lines.extend(
        [
            "",
            "=" * 80,
            "",
        ]
    )

    body_lines: list[str] = []

    for page_number, page_text in extracted_pages:
        body_lines.extend(
            [
                f"[PAGE {page_number}]",
                "-" * 80,
                page_text,
                "",
            ]
        )

    return "\n".join(header_lines + body_lines).rstrip() + "\n"


def write_reference_section_output(
    pdf_path: Path,
    output_dir: Path,
    output_text: str,
) -> Path:
    """Write the extracted reference section to the working directory."""
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{pdf_path.stem}_references.txt"
    output_path.write_text(output_text, encoding="utf-8")

    return output_path


def extract_reference_section(
    pdf_path: Path,
    output_dir: Path,
) -> int:
    """Extract the raw references section from one PDF."""
    PdfReader = import_pypdf()

    if PdfReader is None:
        return 1

    pdf_path = pdf_path.resolve()
    output_dir = output_dir.resolve()

    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        return 1

    if not pdf_path.is_file():
        print(f"Path is not a file: {pdf_path}")
        return 1

    if pdf_path.suffix.lower() != ".pdf":
        print(f"Path does not appear to be a PDF: {pdf_path}")
        return 1

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as error:  # noqa: BLE001
        print(f"Could not open PDF: {pdf_path}")
        print(f"Error: {error}")
        return 1

    page_count = len(reader.pages)
    page_texts = extract_page_text(reader)

    pages_with_text = [
        page_number
        for page_number, page_text in enumerate(page_texts, start=1)
        if page_text.strip()
    ]

    total_extracted_characters = sum(len(page_text) for page_text in page_texts)

    print()
    print("Reference section extraction")
    print("=" * 28)
    print(f"PDF: {pdf_path}")
    print(f"Pages: {page_count}")
    print(f"Pages with extracted text: {len(pages_with_text)}")
    print(f"Extracted characters: {total_extracted_characters}")
    print("OCR performed: no")
    print()

    if page_count == 0:
        print("Status: FAIL")
        print("Reason: PDF has no pages.")
        return 1

    if total_extracted_characters == 0:
        print("Status: FAIL")
        print("Reason: no embedded text was extracted.")
        return 1

    reference_marker = find_reference_marker(page_texts)

    if reference_marker is None:
        print("Reference marker: none detected")
        print()
        print("Status: NO_REFERENCE_SECTION")
        print("Reason: no formal references-section marker was found.")
        return 0

    stop_marker = find_stop_marker_after_reference_start(
        page_texts=page_texts,
        reference_marker=reference_marker,
    )

    extracted_pages = extract_reference_section_pages(
        page_texts=page_texts,
        reference_marker=reference_marker,
        stop_marker=stop_marker,
    )

    output_text = build_output_text(
        pdf_path=pdf_path,
        reference_marker=reference_marker,
        stop_marker=stop_marker,
        extracted_pages=extracted_pages,
    )

    output_path = write_reference_section_output(
        pdf_path=pdf_path,
        output_dir=output_dir,
        output_text=output_text,
    )

    if extracted_pages:
        first_page = extracted_pages[0][0]
        last_page = extracted_pages[-1][0]
    else:
        first_page = reference_marker.page_number
        last_page = reference_marker.page_number

    print(f"Reference marker: {reference_marker.marker_text}")
    print(f"Reference marker page: {reference_marker.page_number}")

    if stop_marker:
        print(f"Stop marker: {stop_marker.marker_text}")
        print(f"Stop marker page: {stop_marker.page_number}")
    else:
        print("Stop marker: none detected")

    print(f"Extracted page range: {first_page}-{last_page}")
    print(f"Output written to: {output_path}")
    print()
    print("Status: PASS")

    return 0


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description=(
            "Extract a raw references section from embedded PDF text and "
            "write it to data/working/reference_sections/."
        )
    )

    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to the PDF artefact to inspect.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for extracted reference-section text output.",
    )

    args = parser.parse_args()

    return extract_reference_section(
        pdf_path=args.pdf_path,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    sys.exit(main())