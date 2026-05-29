# SCRIPTING_CONVENTIONS.md

Status: canonical implementation guidance
Version: v0.1
Last updated: 2026-05-29

---

# 1. Purpose

This document records project scripting conventions for the Australasian Educational Research project.

The purpose of these conventions is to:

- improve consistency across implementation work
- reduce context drift between chats
- reduce restart friction after interruptions
- improve readability and maintainability
- support reproducibility and recoverability

These conventions are intended to remain lightweight.

They should only expand when recurring implementation experience demonstrates a genuine need.

---

# 2. General Principles

Scripts should prioritise:

- clarity over cleverness
- explicitness over abstraction
- reproducibility over convenience
- maintainability over sophistication
- recoverability after interruption

A future contributor should be able to understand the purpose of a script quickly, even after a long period away from the project.

---

# 3. Script Naming Convention

Scripts should use:

- snake_case
- ASCII-safe filenames
- descriptive names
- a verb-object structure where practical

Recommended pattern:

    verb_object.py

Examples:

    acquire_single_report.py
    acquire_cese_reports.py
    extract_pdf_metadata.py
    extract_pdf_references.py
    validate_manifest.py
    build_snapshot.py

Script names should describe the primary responsibility of the script.

---

# 4. Versioning Policy

Version numbers should not be encoded in script filenames.

Avoid:

    acquire_single_report_v2.py
    acquire_single_report_final.py
    acquire_single_report_final2.py

Git provides version history.

Script evolution should be tracked through commits rather than filenames.

---

# 5. Script Scope

Each script should have one primary responsibility.

Examples:

Good:

    acquire_single_report.py

Responsibility:

    Acquire and preserve a single report.

Less desirable:

    acquire_extract_enrich_snapshot.py

Responsibilities:

    Multiple unrelated workflow stages.

If a script develops multiple independent responsibilities, consider splitting it into separate scripts.

---

# 6. Standard Script Header

All project scripts should begin with a descriptive header block.

Recommended format:

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
        URL

    Outputs:
        PDF artefact
        acquisition_manifest.jsonl
    """

The purpose of the header is to support:

- interruption recovery
- maintainability
- rapid understanding
- collaboration

The header is documentation, not executable metadata.

---

# 7. Future Amendments

Additional scripting conventions should only be added when:

- recurring implementation experience reveals a need
- a convention is being repeatedly re-established
- a convention reduces future ambiguity

Avoid expanding this document prematurely.

The project should prefer a small number of useful conventions over an extensive engineering rulebook.