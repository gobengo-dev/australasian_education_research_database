"""
Script:
    inspect_reference_section.py

Purpose:
    Inspect an extracted raw reference-section text file and report whether it
    appears suitable for first-pass individual reference boundary detection.

Project:
    Australasian Educational Research

Author:
    Ben

Status:
    v0.1

Inputs:
    Raw reference-section text file produced by extract_reference_section.py

Outputs:
    Console inspection report

Notes:
    This script is for reference-section quality inspection only.

    It does not:
    - parse references into records
    - write citation inventories
    - write database records
    - perform DOI detection
    - perform URL checking
    - perform metadata enrichment
    - mutate source files
    - mutate extracted reference-section files

    It reports likely reference starts and obvious extraction artefacts to help
    decide whether the extracted section is ready for first-pass reference
    boundary detection.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PAGE_MARKER_PATTERN = re.compile(r"^\[PAGE\s+(\d+)\]\s*$", re.MULTILINE)

# Australian Government / Harvard-like author-date references commonly begin
# with an author or organisation name followed by a four-digit year.
#
# This is intentionally heuristic. It is not a reference parser.
LIKELY_REFERENCE_START_PATTERN = re.compile(
    r"""
    ^
    (?P<start>
        [A-Z][A-Za-zÀ-ÖØ-öø-ÿ’'().&,\-\s]+
        \s+
        (?:19|20)\d{2}
        [a-z]?
        \b
    )
    """,
    re.VERBOSE,
)

URL_PATTERN = re.compile(
    r"""
    (?:
        https?://[^\s<>]+
        |
        www\.[^\s<>]+
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

DOI_PATTERN = re.compile(
    r"""
    (?:
        doi:\s*
        |
        https?://doi\.org/
    )?
    10\.\d{4,9}/[^\s<>]+
    """,
    re.VERBOSE | re.IGNORECASE,
)

SPLIT_WORD_PATTERN = re.compile(
    r"""
    [A-Za-z]
    \n
    [a-z]{2,}
    """,
    re.VERBOSE,
)

SPLIT_INITIAL_PATTERN = re.compile(
    r"""
    ^
    [A-Z]
    \s*$
    """,
    re.VERBOSE | re.MULTILINE,
)

HYPHENATED_LINE_BREAK_PATTERN = re.compile(
    r"""
    [A-Za-z]-
    \n
    [A-Za-z]
    """,
    re.VERBOSE,
)

PAGE_NUMBER_ONLY_LINE_PATTERN = re.compile(
    r"""
    ^
    \s*
    \d{1,4}
    \s*
    $
    """,
    re.VERBOSE | re.MULTILINE,
)


@dataclass
class PageSection:
    """A page-delimited section from an extracted references text file."""

    page_number: int
    text: str


@dataclass
class InspectionResult:
    """Summary of reference-section quality inspection."""

    input_path: Path
    page_count: int
    character_count: int
    line_count: int
    likely_reference_starts: int
    url_count: int
    doi_count: int
    split_word_count: int
    split_initial_count: int
    hyphenated_line_break_count: int
    page_number_only_line_count: int


def read_text_file(path: Path) -> str:
    """Read a UTF-8 text file."""
    return path.read_text(encoding="utf-8")


def split_into_page_sections(text: str) -> list[PageSection]:
    """Split extracted reference-section text into page-delimited sections."""
    markers = list(PAGE_MARKER_PATTERN.finditer(text))

    if not markers:
        return []

    sections: list[PageSection] = []

    for marker_index, marker in enumerate(markers):
        page_number = int(marker.group(1))
        section_start = marker.end()

        if marker_index + 1 < len(markers):
            section_end = markers[marker_index + 1].start()
        else:
            section_end = len(text)

        page_text = text[section_start:section_end].strip()

        # Remove the separator line inserted by extract_reference_section.py.
        page_text = re.sub(r"^-{5,}\s*", "", page_text).strip()

        sections.append(
            PageSection(
                page_number=page_number,
                text=page_text,
            )
        )

    return sections


def remove_header_before_first_page(text: str) -> str:
    """Remove extraction metadata header before the first page marker."""
    first_marker = PAGE_MARKER_PATTERN.search(text)

    if not first_marker:
        return text

    return text[first_marker.start() :]


def count_likely_reference_starts(text: str) -> int:
    """Count likely individual reference starts."""
    count = 0

    for line in text.splitlines():
        stripped_line = line.strip()

        if not stripped_line:
            continue

        if LIKELY_REFERENCE_START_PATTERN.search(stripped_line):
            count += 1

    return count


def collect_likely_reference_start_examples(
    text: str,
    limit: int,
) -> list[str]:
    """Collect examples of likely reference starts for manual review."""
    examples: list[str] = []

    for line in text.splitlines():
        stripped_line = line.strip()

        if not stripped_line:
            continue

        if LIKELY_REFERENCE_START_PATTERN.search(stripped_line):
            examples.append(stripped_line)

        if len(examples) >= limit:
            break

    return examples


def count_pattern(pattern: re.Pattern[str], text: str) -> int:
    """Count regex pattern matches in text."""
    return len(pattern.findall(text))


def inspect_reference_section(path: Path, example_limit: int) -> int:
    """Inspect one extracted reference-section text file."""
    path = path.resolve()

    if not path.exists():
        print(f"Reference-section file not found: {path}")
        return 1

    if not path.is_file():
        print(f"Path is not a file: {path}")
        return 1

    text = read_text_file(path)
    reference_text_only = remove_header_before_first_page(text)
    page_sections = split_into_page_sections(text)

    likely_reference_starts = count_likely_reference_starts(reference_text_only)

    result = InspectionResult(
        input_path=path,
        page_count=len(page_sections),
        character_count=len(reference_text_only),
        line_count=len(reference_text_only.splitlines()),
        likely_reference_starts=likely_reference_starts,
        url_count=count_pattern(URL_PATTERN, reference_text_only),
        doi_count=count_pattern(DOI_PATTERN, reference_text_only),
        split_word_count=count_pattern(SPLIT_WORD_PATTERN, reference_text_only),
        split_initial_count=count_pattern(
            SPLIT_INITIAL_PATTERN,
            reference_text_only,
        ),
        hyphenated_line_break_count=count_pattern(
            HYPHENATED_LINE_BREAK_PATTERN,
            reference_text_only,
        ),
        page_number_only_line_count=count_pattern(
            PAGE_NUMBER_ONLY_LINE_PATTERN,
            reference_text_only,
        ),
    )

    print()
    print("Reference-section inspection")
    print("=" * 28)
    print(f"File: {result.input_path}")
    print(f"Page sections: {result.page_count}")
    print(f"Characters inspected: {result.character_count}")
    print(f"Lines inspected: {result.line_count}")
    print()
    print("Likely content signals")
    print("-" * 22)
    print(f"Likely reference starts: {result.likely_reference_starts}")
    print(f"URLs detected: {result.url_count}")
    print(f"DOIs detected: {result.doi_count}")
    print()
    print("Possible extraction artefacts")
    print("-" * 29)
    print(f"Split-word line breaks: {result.split_word_count}")
    print(f"Split-initial lines: {result.split_initial_count}")
    print(f"Hyphenated line breaks: {result.hyphenated_line_break_count}")
    print(f"Page-number-only lines: {result.page_number_only_line_count}")
    print()

    if page_sections:
        print("Page section summary")
        print("-" * 20)

        for page_section in page_sections:
            page_reference_starts = count_likely_reference_starts(
                page_section.text
            )
            page_urls = count_pattern(URL_PATTERN, page_section.text)
            page_dois = count_pattern(DOI_PATTERN, page_section.text)
            page_split_words = count_pattern(
                SPLIT_WORD_PATTERN,
                page_section.text,
            )
            page_split_initials = count_pattern(
                SPLIT_INITIAL_PATTERN,
                page_section.text,
            )

            print(
                f"- Page {page_section.page_number}: "
                f"{page_reference_starts} likely starts, "
                f"{page_urls} URLs, "
                f"{page_dois} DOIs, "
                f"{page_split_words} split words, "
                f"{page_split_initials} split initials"
            )

        print()
    else:
        print("Page section summary")
        print("-" * 20)
        print("- No [PAGE n] sections detected")
        print()

    examples = collect_likely_reference_start_examples(
        reference_text_only,
        limit=example_limit,
    )

    if examples:
        print("Likely reference start examples")
        print("-" * 31)

        for example in examples:
            print(f"- {example}")

        print()

    print("Interpretation")
    print("-" * 14)

    if result.page_count == 0:
        print("Status: REVIEW_REQUIRED")
        print("Reason: no page sections were detected.")
        return 0

    if result.likely_reference_starts == 0:
        print("Status: REVIEW_REQUIRED")
        print("Reason: no likely reference starts were detected.")
        return 0

    if result.split_word_count > 0 or result.split_initial_count > 0:
        print("Status: USABLE_WITH_LAYOUT_ARTEFACTS")
        print(
            "Reason: likely reference starts were detected, but extraction "
            "artefacts may affect reference boundary detection."
        )
        return 0

    print("Status: LIKELY_PARSE_READY")
    print(
        "Reason: likely reference starts were detected and no major simple "
        "layout artefacts were flagged."
    )

    return 0


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description=(
            "Inspect a raw extracted reference-section text file for likely "
            "reference starts and extraction artefacts."
        )
    )

    parser.add_argument(
        "reference_section_path",
        type=Path,
        help="Path to an extracted *_references.txt file.",
    )

    parser.add_argument(
        "--example-limit",
        type=int,
        default=10,
        help="Number of likely reference start examples to print.",
    )

    args = parser.parse_args()

    return inspect_reference_section(
        path=args.reference_section_path,
        example_limit=args.example_limit,
    )


if __name__ == "__main__":
    sys.exit(main())