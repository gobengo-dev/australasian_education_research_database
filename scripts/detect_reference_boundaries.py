"""
Script:
    detect_reference_boundaries.py

Purpose:
    Detect candidate individual reference boundaries within a raw extracted
    reference-section text file.

Project:
    Australasian Educational Research

Author:
    Ben

Status:
    v0.1

Inputs:
    Raw reference-section text file produced by extract_reference_section.py

Outputs:
    Console boundary-detection report
    Optional candidate references text file under data/working/reference_candidates/
    Optional candidate references JSONL file under data/working/reference_candidates/

Notes:
    This script performs first-pass reference boundary detection only.

    It does not:
    - parse references into structured citation fields
    - write citation inventories
    - write database records
    - perform DOI matching
    - perform URL checking
    - perform metadata enrichment
    - mutate source files
    - mutate extracted reference-section files

    Boundary detection in CESE author-date references cannot rely on line-level
    start detection alone, because continuation lines can contain names and
    years that look like new reference starts.

    Testing so far has shown that CESE references may use more than one
    author-date variant:

        Older observed style:
            Anderson, R 1977, ...
            Centre for Education Statistics and Evaluation 2017, ...

        Later observed style:
            Adams AM, Wilson HK and Fearn J (2019) ...
            ACER (Australian Council for Educational Research) (2016) ...

    The boundary detector therefore supports both unparenthesised and
    parenthesised year tokens.

    The first-pass boundary heuristic is:

        A candidate reference boundary is recognised when:
        1. the accumulated candidate ends with plausible terminal punctuation;
           and
        2. the next non-empty line looks like a plausible new reference start.

    Testing also showed that PDF text extraction can collapse two adjacent
    references into the same line, for example:

        ... pp. 114-127. Angus, M, McDonald, T ... 2009 ...

    In that situation, next-line detection cannot see the boundary. This script
    therefore applies a second pass that looks for embedded boundaries inside
    candidate text:

        terminal punctuation + space + plausible author-date reference start

    Organisation-like embedded starts must include a date token or a recognised
    date marker such as "forthcoming". This reduces false splits such as:

        Goss ... Creating classrooms that improve learning. Grattan Institute.

    where "Grattan Institute" is the publisher, not a new reference.

    Extracted reference sections may begin with a section-numbered heading such
    as "7. References". These headings are filtered out before boundary
    detection.

    This remains a heuristic boundary detector, not a canonical parser.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT_DIR = Path("data/working/reference_candidates")

PAGE_MARKER_PATTERN = re.compile(r"^\[PAGE\s+(\d+)\]\s*$", re.MULTILINE)

# Reference headings are intentionally matched as whole lines only.
#
# Use [ \t] rather than \s inside the pattern because \s can match newlines.
# Without this guard, a page number on one line followed by "References" on the
# next line can be incorrectly captured as one heading.
#
# Examples matched:
#     References
#     7. References
#     7 References
#     1.2 References
REFERENCE_HEADING_PATTERN = re.compile(
    r"^[ \t]*(?:\d+(?:\.\d+)*\.?[ \t]+)?references[ \t]*$",
    re.IGNORECASE,
)

SEPARATOR_LINE_PATTERN = re.compile(r"^-{5,}\s*$")

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

# A date token is used only for boundary detection. It is not parsed as a
# structured year field here.
#
# Supported examples:
#     2017
#     2017a
#     (2017)
#     (2017a)
#     forthcoming
#     n.d.
#     (n.d.)
DATE_TOKEN = r"""
(?:
    \(?
    (?:19|20)\d{2}
    [a-z]?
    \)?
    |
    forthcoming
    |
    \(?n\.d\.\)?
)
"""

DATE_TOKEN_PATTERN = re.compile(DATE_TOKEN, re.VERBOSE | re.IGNORECASE)

# Personal author starts, older CESE style.
#
# Examples:
#     Alter, P & Haydon, T 2017
#     Angus, M, McDonald, T, Ormond, C ... 2009
#     O'Connor, E, Dearing, E & Collins, B 2011
#     van Gerven, P, Paas, F ... 2002
#     de Jong, T 2010
#     van Merrienboer, J, Kester, L & Paas, F (2006)
PERSONAL_AUTHOR_COMMA_START_PATTERN = re.compile(
    rf"""
    ^
    (?:
        (?:van|de|der|den)\s+
    )?
    [A-ZÀ-ÖØ-ÞO]
    [A-Za-zÀ-ÖØ-öø-ÿ’'\-\s]*
    ,
    \s+
    [A-Z]
    [A-Za-zÀ-ÖØ-öø-ÿ’'.,\-\s&]{{0,180}}
    \s+
    {DATE_TOKEN}
    \b
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Personal author starts, later CESE style.
#
# Examples:
#     Adams AM, Wilson HK, Money J, Palmer-Conn S and Fearn J (2019)
#     Allen K-A and Kern ML (2017)
#     Hughes JN, Luo W, Kwok OM and Loyd LK (2008)
#
# This is not an author parser. It only checks whether the beginning of text
# looks enough like a person-authored reference to justify a candidate boundary.
PERSONAL_AUTHOR_NO_COMMA_START_PATTERN = re.compile(
    rf"""
    ^
    (?:
        (?:van|de|der|den)\s+
    )?
    [A-ZÀ-ÖØ-ÞO]
    [A-Za-zÀ-ÖØ-öø-ÿ’'\-]+
    (?:
        \s+
        [A-Z]
        [A-Z\-]{{0,5}}
        \.?
    ){{1,4}}
    (?:
        (?:
            ,
            |
            \s+and\s+
            |
            \s+&\s+
        )
        [A-ZÀ-ÖØ-ÞO]
        [A-Za-zÀ-ÖØ-öø-ÿ’'\-]+
        (?:
            \s+
            [A-Z]
            [A-Z\-]{{0,5}}
            \.?
        ){{0,4}}
    ){{0,12}}
    \s+
    {DATE_TOKEN}
    \b
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Damaged personal author starts.
#
# PDF extraction sometimes turns a surname such as "Shin" into "S hin" or
# "Woolfolk" into "W oolfolk". This pattern is only used for boundary detection.
# The original candidate text is preserved in output.
DAMAGED_PERSONAL_AUTHOR_START_PATTERN = re.compile(
    rf"""
    ^
    [A-Z]
    \s+
    [a-z]{{2,}}
    [A-Za-zÀ-ÖØ-öø-ÿ’'\-]*
    (?:
        \s+
        [A-Z][A-Za-zÀ-ÖØ-öø-ÿ’'\-]+
    )?
    ,
    \s+
    [A-Z]
    [A-Za-zÀ-ÖØ-öø-ÿ’'.,\-\s&]{{0,180}}
    \s+
    {DATE_TOKEN}
    \b
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Organisation author starts.
#
# Examples:
#     Australian Council for Educational Research (ACER) 2018
#     Centre for Education Statistics and Evaluation 2017
#     Centre for Education Statistics and Evaluation, forthcoming
#     Education Endowment Foundation (EEF) 2019
#     NSW Department of Education 2019
#     OECD 2019
#     ACER (Australian Council for Educational Research) (2016)
#
# Organisation starts require a date token or a recognised date marker. This is
# deliberately stricter than "capitalised phrase", because capitalised phrases
# also occur as publishers at the end of references.
ORGANISATION_AUTHOR_START_PATTERN = re.compile(
    rf"""
    ^
    [A-Z]
    [A-Za-zÀ-ÖØ-öø-ÿ’'().&,\-\s]{{2,160}}
    (?:
        \s+
        {DATE_TOKEN}
        \b
        |
        ,
        \s+
        forthcoming
        \b
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Common false-positive pattern from continuation lines:
#
#     A & Winterton, A 2009, ...
#
# This contains a year and looks start-like, but the single initial at the
# beginning indicates it is probably a continuation of a multi-author entry.
LEADING_INITIAL_CONTINUATION_PATTERN = re.compile(
    rf"""
    ^
    [A-Z]
    \s*
    &
    \s+
    [A-Z][A-Za-zÀ-ÖØ-öø-ÿ’'\-]+
    ,
    \s+
    [A-Z]
    \s+
    {DATE_TOKEN}
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Common false-positive type from title continuations:
#
#     PISA 2015: Presenting Australia's results...
#
# This is usually a title continuation, not an author-date reference start.
ACRONYM_TITLE_CONTINUATION_PATTERN = re.compile(
    r"""
    ^
    [A-Z]{2,}
    \s+
    (?:19|20)\d{2}
    [a-z]?
    \b
    \s*
    :
    """,
    re.VERBOSE,
)

# Text-damage flag.
#
# This is intentionally narrower than "capital letter + lowercase word", because
# that created noisy flags in ordinary titles. It looks for likely damaged
# surnames such as:
#
#     S hin,
#     S imonsen,
#     S kiba,
#     S now,
#     W oolfolk Hoy,
DAMAGED_NAME_IN_TEXT_PATTERN = re.compile(
    r"""
    \b
    [A-Z]
    \s+
    [a-z]{2,}
    [A-Za-zÀ-ÖØ-öø-ÿ’'\-]*
    (?:
        \s+
        [A-Z][A-Za-zÀ-ÖØ-öø-ÿ’'\-]+
    )?
    \s*
    ,
    """,
    re.VERBOSE,
)

# This pattern identifies possible split-word damage inside reference text. It
# is used for review triage only, not boundary detection.
SPACED_INTERNAL_WORD_PATTERN = re.compile(
    r"""
    \b
    [a-z]
    \s+
    [a-z]{2,}
    \b
    """,
    re.VERBOSE,
)


@dataclass
class PageSection:
    """A page-delimited section from an extracted references text file."""

    page_number: int
    text: str


@dataclass
class TextLine:
    """A non-empty content line with source-page provenance."""

    page_number: int | None
    text: str


@dataclass
class AssembledCandidate:
    """A line-assembled candidate group before embedded splitting."""

    start_page: int | None
    end_page: int | None
    lines: list[str]
    boundary_reason: str
    confidence: str

    @property
    def text(self) -> str:
        """Return the assembled candidate as whitespace-normalised text."""
        return normalise_reference_text(" ".join(self.lines))

    @property
    def source_line_count(self) -> int:
        """Return the number of source lines in the assembled candidate."""
        return len(self.lines)


@dataclass
class CandidateReference:
    """A candidate individual reference."""

    candidate_id: int
    start_page: int | None
    end_page: int | None
    text: str
    source_line_count: int
    boundary_reason: str
    confidence: str
    terminal_punctuation: bool
    embedded_boundary_split: bool
    possible_text_damage: bool


def read_text_file(path: Path) -> str:
    """Read a UTF-8 text file."""
    return path.read_text(encoding="utf-8")


def remove_header_before_first_page(text: str) -> str:
    """Remove extraction metadata header before the first page marker."""
    first_marker = PAGE_MARKER_PATTERN.search(text)

    if not first_marker:
        return text

    return text[first_marker.start() :]


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


def build_text_lines(page_sections: list[PageSection]) -> list[TextLine]:
    """Build non-empty content lines while preserving page provenance."""
    text_lines: list[TextLine] = []

    for section in page_sections:
        for raw_line in section.text.splitlines():
            line = raw_line.strip()

            if not line:
                continue

            if SEPARATOR_LINE_PATTERN.match(line):
                continue

            if REFERENCE_HEADING_PATTERN.match(line):
                continue

            if PAGE_NUMBER_ONLY_LINE_PATTERN.match(line):
                continue

            text_lines.append(
                TextLine(
                    page_number=section.page_number,
                    text=line,
                )
            )

    return text_lines


def looks_like_likely_reference_start(text: str) -> bool:
    """
    Return True if text looks like a plausible new reference start.

    This is intentionally conservative. Some continuation lines contain names
    and years, so this function rejects known false-positive patterns before
    testing author-date start patterns.
    """
    stripped = text.strip()

    if not stripped:
        return False

    if LEADING_INITIAL_CONTINUATION_PATTERN.search(stripped):
        return False

    if ACRONYM_TITLE_CONTINUATION_PATTERN.search(stripped):
        return False

    if PERSONAL_AUTHOR_COMMA_START_PATTERN.search(stripped):
        return True

    if PERSONAL_AUTHOR_NO_COMMA_START_PATTERN.search(stripped):
        return True

    if DAMAGED_PERSONAL_AUTHOR_START_PATTERN.search(stripped):
        return True

    if ORGANISATION_AUTHOR_START_PATTERN.search(stripped):
        return True

    return False


def has_plausible_terminal_punctuation(text: str) -> bool:
    """
    Return True if accumulated text appears to end a reference.

    This is not used to split on every full stop. It is used only on the end of
    an accumulated candidate and in combination with another boundary signal.

    Bare ">" is accepted because CESE URL references can end with an angle
    bracket and no final full stop.
    """
    stripped = text.strip()

    if not stripped:
        return False

    terminal_endings = (
        ".",
        ">",
        ".>",
        ">.",
        ").",
        ".)",
    )

    return stripped.endswith(terminal_endings)


def normalise_reference_text(text: str) -> str:
    """
    Lightly normalise candidate reference text for readable output.

    This deliberately avoids aggressive correction. The purpose is to join
    wrapped lines into a candidate reference while preserving the original
    wording as much as possible.
    """
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ,", ",")
    text = text.replace(" .", ".")
    text = text.replace(" :", ":")
    text = text.replace(" ;", ";")
    text = text.replace(" /", "/")
    text = text.replace("/ ", "/")
    text = text.replace("< ", "<")
    text = text.replace(" >", ">")
    return text.strip()


def contains_possible_text_damage(text: str) -> bool:
    """
    Return True if text contains simple signs of PDF extraction damage.

    This flag is used for review confidence. It does not repair text.
    """
    if DAMAGED_NAME_IN_TEXT_PATTERN.search(text):
        return True

    if SPACED_INTERNAL_WORD_PATTERN.search(text):
        return True

    if "￾" in text:
        return True

    return False


def count_pattern(pattern: re.Pattern[str], text: str) -> int:
    """Count regex pattern matches in text."""
    return len(pattern.findall(text))


def find_embedded_boundary_positions(text: str) -> list[int]:
    """
    Find positions where candidate text appears to contain embedded references.

    The split position is the start of the likely next reference.

    We do this procedurally rather than with one large regex so that embedded
    detection uses exactly the same reference-start logic as line-level
    detection. This reduces the chance that the two passes drift apart.
    """
    positions: list[int] = []

    for match in re.finditer(r"(?<=[.>])\s+", text):
        candidate_start = match.end()
        following_text = text[candidate_start:]

        if looks_like_likely_reference_start(following_text):
            positions.append(candidate_start)

    return positions


def split_candidate_text_on_embedded_boundaries(text: str) -> list[str]:
    """
    Split a candidate reference text if it contains embedded reference starts.

    This handles cases where PDF extraction collapses two adjacent references
    into the same line, such as:

        ... pp. 114-127. Angus, M, McDonald, T ... 2009 ...

    The split occurs after terminal punctuation and before the next plausible
    author-date reference start.
    """
    text = normalise_reference_text(text)
    boundary_positions = find_embedded_boundary_positions(text)

    if not boundary_positions:
        return [text]

    fragments: list[str] = []
    start_index = 0

    for boundary_position in boundary_positions:
        fragment = text[start_index:boundary_position].strip()

        if fragment:
            fragments.append(fragment)

        start_index = boundary_position

    final_fragment = text[start_index:].strip()

    if final_fragment:
        fragments.append(final_fragment)

    return fragments


def assemble_line_based_candidates(
    text_lines: list[TextLine],
) -> list[AssembledCandidate]:
    """
    Assemble candidate groups using line-level terminal + next-start signals.

    The second pass may split these groups further if embedded reference starts
    are found inside the assembled candidate text.
    """
    assembled: list[AssembledCandidate] = []

    if not text_lines:
        return assembled

    current_lines: list[str] = []
    current_start_page: int | None = None
    current_end_page: int | None = None

    for index, text_line in enumerate(text_lines):
        if not current_lines:
            current_start_page = text_line.page_number

        current_lines.append(text_line.text)
        current_end_page = text_line.page_number

        current_text = normalise_reference_text(" ".join(current_lines))
        terminal_punctuation = has_plausible_terminal_punctuation(current_text)

        next_line: TextLine | None = None

        if index + 1 < len(text_lines):
            next_line = text_lines[index + 1]

        next_line_started_reference = (
            next_line is not None
            and looks_like_likely_reference_start(next_line.text)
        )

        if terminal_punctuation and next_line_started_reference:
            assembled.append(
                AssembledCandidate(
                    start_page=current_start_page,
                    end_page=current_end_page,
                    lines=list(current_lines),
                    boundary_reason=(
                        "terminal punctuation followed by likely next-line "
                        "reference start"
                    ),
                    confidence="high",
                )
            )

            current_lines = []
            current_start_page = None
            current_end_page = None

    if current_lines:
        final_text = normalise_reference_text(" ".join(current_lines))

        if has_plausible_terminal_punctuation(final_text):
            confidence = "medium"
            reason = "final line-based candidate ended with terminal punctuation"
        else:
            confidence = "low"
            reason = (
                "final line-based candidate did not end with expected terminal "
                "punctuation"
            )

        assembled.append(
            AssembledCandidate(
                start_page=current_start_page,
                end_page=current_end_page,
                lines=list(current_lines),
                boundary_reason=reason,
                confidence=confidence,
            )
        )

    return assembled


def choose_candidate_confidence(
    base_confidence: str,
    terminal_punctuation: bool,
    embedded_split_occurred: bool,
    possible_text_damage: bool,
) -> str:
    """Choose a conservative confidence label for a candidate reference."""
    confidence = base_confidence

    if embedded_split_occurred:
        confidence = "medium"

    if possible_text_damage and confidence == "high":
        confidence = "medium"

    if not terminal_punctuation:
        confidence = "low"

    return confidence


def build_candidate_references(
    assembled_candidates: list[AssembledCandidate],
) -> list[CandidateReference]:
    """
    Build final candidate references, including embedded-boundary splits.

    Embedded-boundary splits receive medium confidence because they are useful
    but more heuristic than line-level terminal + next-start boundaries.
    """
    candidates: list[CandidateReference] = []

    for assembled_candidate in assembled_candidates:
        fragments = split_candidate_text_on_embedded_boundaries(
            assembled_candidate.text
        )

        embedded_split_occurred = len(fragments) > 1

        for fragment in fragments:
            terminal_punctuation = has_plausible_terminal_punctuation(fragment)
            possible_text_damage = contains_possible_text_damage(fragment)

            if embedded_split_occurred:
                boundary_reason = (
                    "embedded terminal punctuation followed by likely "
                    "reference start"
                )
                base_confidence = "medium"
            else:
                boundary_reason = assembled_candidate.boundary_reason
                base_confidence = assembled_candidate.confidence

            if not terminal_punctuation:
                boundary_reason = (
                    boundary_reason
                    + "; candidate does not end with expected terminal "
                    "punctuation"
                )

            confidence = choose_candidate_confidence(
                base_confidence=base_confidence,
                terminal_punctuation=terminal_punctuation,
                embedded_split_occurred=embedded_split_occurred,
                possible_text_damage=possible_text_damage,
            )

            candidates.append(
                CandidateReference(
                    candidate_id=len(candidates) + 1,
                    start_page=assembled_candidate.start_page,
                    end_page=assembled_candidate.end_page,
                    text=fragment,
                    source_line_count=assembled_candidate.source_line_count,
                    boundary_reason=boundary_reason,
                    confidence=confidence,
                    terminal_punctuation=terminal_punctuation,
                    embedded_boundary_split=embedded_split_occurred,
                    possible_text_damage=possible_text_damage,
                )
            )

    return candidates


def candidate_to_dict(candidate: CandidateReference) -> dict[str, Any]:
    """Convert a candidate reference to a JSON-serialisable dictionary."""
    return {
        "candidate_id": candidate.candidate_id,
        "start_page": candidate.start_page,
        "end_page": candidate.end_page,
        "source_line_count": candidate.source_line_count,
        "confidence": candidate.confidence,
        "boundary_reason": candidate.boundary_reason,
        "terminal_punctuation": candidate.terminal_punctuation,
        "embedded_boundary_split": candidate.embedded_boundary_split,
        "possible_text_damage": candidate.possible_text_damage,
        "contains_url": bool(URL_PATTERN.search(candidate.text)),
        "contains_doi": bool(DOI_PATTERN.search(candidate.text)),
        "text": candidate.text,
    }


def build_text_output(
    input_path: Path,
    candidates: list[CandidateReference],
) -> str:
    """Build a human-readable candidate reference output file."""
    lines: list[str] = [
        f"Source reference section: {input_path}",
        "",
        "Detection method: terminal punctuation + next reference start",
        "Embedded split method: terminal punctuation + embedded likely start",
        "Supported date styles: 2017, 2017a, (2017), (2017a), forthcoming, n.d.",
        "Output type: candidate reference boundaries",
        "",
        "=" * 80,
        "",
    ]

    for candidate in candidates:
        lines.extend(
            [
                f"[REFERENCE {candidate.candidate_id}]",
                f"Pages: {candidate.start_page}-{candidate.end_page}",
                f"Confidence: {candidate.confidence}",
                f"Boundary reason: {candidate.boundary_reason}",
                f"Source line count: {candidate.source_line_count}",
                f"Embedded boundary split: {candidate.embedded_boundary_split}",
                f"Possible text damage: {candidate.possible_text_damage}",
                "-" * 80,
                candidate.text,
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def build_jsonl_output(candidates: list[CandidateReference]) -> str:
    """Build JSONL output for candidate references."""
    return "\n".join(
        json.dumps(
            candidate_to_dict(candidate),
            ensure_ascii=False,
            sort_keys=True,
        )
        for candidate in candidates
    ) + "\n"


def write_outputs(
    input_path: Path,
    output_dir: Path,
    candidates: list[CandidateReference],
    write_text: bool,
    write_jsonl: bool,
) -> list[Path]:
    """Write optional candidate output files."""
    written_paths: list[Path] = []

    if not write_text and not write_jsonl:
        return written_paths

    output_dir.mkdir(parents=True, exist_ok=True)

    output_stem = input_path.stem.replace("_references", "")

    if write_text:
        text_output_path = output_dir / f"{output_stem}_reference_candidates.txt"
        text_output_path.write_text(
            build_text_output(
                input_path=input_path,
                candidates=candidates,
            ),
            encoding="utf-8",
        )
        written_paths.append(text_output_path)

    if write_jsonl:
        jsonl_output_path = output_dir / f"{output_stem}_reference_candidates.jsonl"
        jsonl_output_path.write_text(
            build_jsonl_output(candidates),
            encoding="utf-8",
        )
        written_paths.append(jsonl_output_path)

    return written_paths


def print_candidate_examples(
    candidates: list[CandidateReference],
    example_limit: int,
) -> None:
    """Print abbreviated candidate reference examples."""
    if not candidates:
        return

    print("Candidate examples")
    print("-" * 18)

    for candidate in candidates[:example_limit]:
        candidate_text = candidate.text

        if len(candidate_text) > 180:
            candidate_text = candidate_text[:177] + "..."

        print(
            f"- #{candidate.candidate_id} "
            f"p.{candidate.start_page}-{candidate.end_page} "
            f"[{candidate.confidence}]: {candidate_text}"
        )

    print()


def print_review_flags(candidates: list[CandidateReference]) -> None:
    """Print a compact list of candidates that should be reviewed."""
    review_candidates = [
        candidate
        for candidate in candidates
        if (
            candidate.confidence != "high"
            or candidate.embedded_boundary_split
            or candidate.possible_text_damage
        )
    ]

    if not review_candidates:
        return

    print("Review flags")
    print("-" * 12)

    for candidate in review_candidates[:25]:
        print(
            f"- #{candidate.candidate_id}: "
            f"confidence={candidate.confidence}; "
            f"embedded_split={candidate.embedded_boundary_split}; "
            f"text_damage={candidate.possible_text_damage}; "
            f"pages={candidate.start_page}-{candidate.end_page}"
        )

    if len(review_candidates) > 25:
        print(f"- ... {len(review_candidates) - 25} additional review flags")

    print()


def detect_reference_boundaries(
    reference_section_path: Path,
    output_dir: Path,
    write_text: bool,
    write_jsonl: bool,
    example_limit: int,
) -> int:
    """Detect candidate reference boundaries in one extracted references file."""
    reference_section_path = reference_section_path.resolve()
    output_dir = output_dir.resolve()

    if not reference_section_path.exists():
        print(f"Reference-section file not found: {reference_section_path}")
        return 1

    if not reference_section_path.is_file():
        print(f"Path is not a file: {reference_section_path}")
        return 1

    source_text = read_text_file(reference_section_path)
    reference_text_only = remove_header_before_first_page(source_text)
    page_sections = split_into_page_sections(source_text)
    text_lines = build_text_lines(page_sections)

    assembled_candidates = assemble_line_based_candidates(text_lines)
    candidates = build_candidate_references(assembled_candidates)

    high_confidence_count = sum(
        1 for candidate in candidates if candidate.confidence == "high"
    )
    medium_confidence_count = sum(
        1 for candidate in candidates if candidate.confidence == "medium"
    )
    low_confidence_count = sum(
        1 for candidate in candidates if candidate.confidence == "low"
    )
    embedded_split_count = sum(
        1 for candidate in candidates if candidate.embedded_boundary_split
    )
    text_damage_count = sum(
        1 for candidate in candidates if candidate.possible_text_damage
    )

    print()
    print("Reference boundary detection")
    print("=" * 28)
    print(f"Input file: {reference_section_path}")
    print(f"Page sections: {len(page_sections)}")
    print(f"Non-empty content lines: {len(text_lines)}")
    print(f"Line-based candidate groups: {len(assembled_candidates)}")
    print(f"Candidate references after embedded splitting: {len(candidates)}")
    print()
    print("Candidate confidence")
    print("-" * 20)
    print(f"High: {high_confidence_count}")
    print(f"Medium: {medium_confidence_count}")
    print(f"Low: {low_confidence_count}")
    print()
    print("Boundary refinement signals")
    print("-" * 27)
    print(f"Candidates produced by embedded splitting: {embedded_split_count}")
    print(f"Candidates with possible text damage: {text_damage_count}")
    print()
    print("Content signals")
    print("-" * 15)
    print(f"URLs detected: {count_pattern(URL_PATTERN, reference_text_only)}")
    print(f"DOIs detected: {count_pattern(DOI_PATTERN, reference_text_only)}")
    print()
    print("Possible extraction artefacts")
    print("-" * 29)
    print(
        "Split-word line breaks: "
        f"{count_pattern(SPLIT_WORD_PATTERN, reference_text_only)}"
    )
    print(
        "Split-initial lines: "
        f"{count_pattern(SPLIT_INITIAL_PATTERN, reference_text_only)}"
    )
    print(
        "Hyphenated line breaks: "
        f"{count_pattern(HYPHENATED_LINE_BREAK_PATTERN, reference_text_only)}"
    )
    print()

    print_candidate_examples(
        candidates=candidates,
        example_limit=example_limit,
    )

    print_review_flags(candidates)

    written_paths = write_outputs(
        input_path=reference_section_path,
        output_dir=output_dir,
        candidates=candidates,
        write_text=write_text,
        write_jsonl=write_jsonl,
    )

    if written_paths:
        print("Outputs written")
        print("-" * 15)

        for path in written_paths:
            print(f"- {path}")

        print()

    print("Interpretation")
    print("-" * 14)

    if not page_sections:
        print("Status: REVIEW_REQUIRED")
        print("Reason: no page sections were detected.")
        return 0

    if not candidates:
        print("Status: REVIEW_REQUIRED")
        print("Reason: no candidate references were detected.")
        return 0

    if low_confidence_count > 0:
        print("Status: CANDIDATES_WITH_REVIEW_REQUIRED")
        print(
            "Reason: at least one candidate reference has low-confidence "
            "boundary detection."
        )
        return 0

    if text_damage_count > 0:
        print("Status: CANDIDATES_WITH_TEXT_DAMAGE")
        print(
            "Reason: candidate references were detected, but some contain "
            "likely PDF text extraction damage."
        )
        return 0

    if embedded_split_count > 0:
        print("Status: CANDIDATES_WITH_EMBEDDED_SPLITS")
        print(
            "Reason: candidate references were detected, including boundaries "
            "found inside collapsed extracted text."
        )
        return 0

    if (
        count_pattern(SPLIT_WORD_PATTERN, reference_text_only) > 0
        or count_pattern(SPLIT_INITIAL_PATTERN, reference_text_only) > 0
    ):
        print("Status: CANDIDATES_WITH_LAYOUT_ARTEFACTS")
        print(
            "Reason: candidate references were detected, but extraction "
            "artefacts may affect later citation parsing."
        )
        return 0

    print("Status: CANDIDATES_READY_FOR_REVIEW")
    print(
        "Reason: candidate references were detected with no low-confidence "
        "boundaries or simple layout artefacts flagged."
    )

    return 0


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description=(
            "Detect candidate individual reference boundaries in an extracted "
            "raw reference-section text file."
        )
    )

    parser.add_argument(
        "reference_section_path",
        type=Path,
        help="Path to an extracted *_references.txt file.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for optional candidate reference outputs.",
    )

    parser.add_argument(
        "--write-text",
        action="store_true",
        help="Write human-readable candidate references to a text file.",
    )

    parser.add_argument(
        "--write-jsonl",
        action="store_true",
        help="Write candidate references to JSONL.",
    )

    parser.add_argument(
        "--example-limit",
        type=int,
        default=10,
        help="Number of candidate examples to print.",
    )

    args = parser.parse_args()

    return detect_reference_boundaries(
        reference_section_path=args.reference_section_path,
        output_dir=args.output_dir,
        write_text=args.write_text,
        write_jsonl=args.write_jsonl,
        example_limit=args.example_limit,
    )


if __name__ == "__main__":
    sys.exit(main())