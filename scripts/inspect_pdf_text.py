"""
Script:
    inspect_pdf_text.py

Purpose:
    Inspect embedded text extraction from a PDF artefact and report whether
    likely reference-section markers can be found.

Project:
    Australasian Educational Research

Author:
    Ben

Status:
    v0.1

Inputs:
    PDF artefact path

Outputs:
    Console inspection report
    Optional extracted text file under data/working/text_inspection/

Notes:
    This script is for extraction reconnaissance only.

    It does not:
    - perform OCR
    - parse individual references
    - write citation inventories
    - write database records
    - mutate source artefacts
    - mutate acquisition manifests

    It uses embedded PDF text only.

    Reference marker detection supports both plain and section-numbered
    headings, for example:

        References
        Reference list
        Bibliography
        7. References
        7 References
        1.2 References

    This is marker reconnaissance only. The script reports candidate markers;
    it does not decide whether a detected section is suitable for parsing.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path("data/working/text_inspection")

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
        print("Then consider adding it to requirements.txt if adopted.")
        print()
        return None

    return PdfReader


def normalise_whitespace(text: str) -> str:
    """Normalise whitespace enough for marker detection and readable output."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_page_text(reader) -> list[str]:
    """Extract embedded text from each page in the PDF."""
    page_texts: list[str] = []

    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception as error:  # noqa: BLE001
            text = f"[TEXT EXTRACTION ERROR: {error}]"

        page_texts.append(normalise_whitespace(text))

    return page_texts


def find_reference_markers(page_texts: list[str]) -> list[tuple[int, str]]:
    """
    Find likely reference-section markers.

    Returns:
        A list of tuples:
            (one-based page number, matched marker text)
    """
    matches: list[tuple[int, str]] = []

    for page_index, page_text in enumerate(page_texts):
        for pattern in REFERENCE_MARKER_PATTERNS:
            match = pattern.search(page_text)

            if match:
                matches.append((page_index + 1, match.group(0).strip()))

    return matches


def build_combined_text(pdf_path: Path, page_texts: list[str]) -> str:
    """Build a simple page-delimited text inspection file."""
    sections = [
        f"Source PDF: {pdf_path}",
        "",
        "Extraction method: embedded PDF text via pypdf",
        "OCR performed: no",
        "",
        "=" * 80,
        "",
    ]

    for page_number, page_text in enumerate(page_texts, start=1):
        sections.extend(
            [
                f"[PAGE {page_number}]",
                "-" * 80,
                page_text,
                "",
            ]
        )

    return "\n".join(sections)


def write_text_output(
    pdf_path: Path,
    page_texts: list[str],
    output_dir: Path,
) -> Path:
    """Write extracted text to the working inspection directory."""
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{pdf_path.stem}.txt"
    output_text = build_combined_text(pdf_path, page_texts)

    output_path.write_text(output_text, encoding="utf-8")

    return output_path


def inspect_pdf_text(
    pdf_path: Path,
    output_text: bool,
    output_dir: Path,
) -> int:
    """Inspect embedded text extraction from a PDF."""
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

    empty_pages = page_count - len(pages_with_text)

    total_extracted_characters = sum(len(page_text) for page_text in page_texts)

    reference_markers = find_reference_markers(page_texts)

    print()
    print("PDF text inspection")
    print("=" * 19)
    print(f"PDF: {pdf_path}")
    print(f"Pages: {page_count}")
    print(f"Pages with extracted text: {len(pages_with_text)}")
    print(f"Pages without extracted text: {empty_pages}")
    print(f"Extracted characters: {total_extracted_characters}")
    print("OCR performed: no")
    print()

    print("Reference marker candidates")
    print("-" * 27)

    if reference_markers:
        for page_number, marker in reference_markers:
            print(f"- Page {page_number}: {marker}")

        print()
    else:
        print("- None found")
        print()

    if output_text:
        output_path = write_text_output(
            pdf_path=pdf_path,
            page_texts=page_texts,
            output_dir=output_dir,
        )

        print(f"Extracted text written to: {output_path}")
        print()

    if page_count == 0:
        print("Status: FAIL")
        print("Reason: PDF has no pages.")
        return 1

    if total_extracted_characters == 0:
        print("Status: FAIL")
        print("Reason: no embedded text was extracted.")
        return 1

    print("Status: PASS")
    return 0


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description=(
            "Inspect embedded text extraction from a PDF and identify likely "
            "reference-section markers."
        )
    )

    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to the PDF artefact to inspect.",
    )

    parser.add_argument(
        "--write-text",
        action="store_true",
        help=(
            "Write extracted embedded text to "
            "data/working/text_inspection/."
        ),
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for optional extracted text inspection output.",
    )

    args = parser.parse_args()

    return inspect_pdf_text(
        pdf_path=args.pdf_path,
        output_text=args.write_text,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    sys.exit(main())