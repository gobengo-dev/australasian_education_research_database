# CHAT_INDEX.md

Status: canonical chat registry  
Version: v0.4  
Last updated: 2026-06-04

---

# 1. Purpose

This document records the active and retired ChatGPT chats used in the Australasian Educational Research project.

Its purpose is to:

- reduce conversational drift
- clarify chat authority
- preserve operational continuity
- identify which chats produced which artefacts
- link project work to Git commits
- prevent retired chats from being used for new decisions
- provide a navigable history of project development

This document is not a transcript archive.

Chat transcripts remain in ChatGPT or external archives.

Only operationally significant information should be recorded here.

---

# 2. Chat Status Terms

## Active

The chat may be used for new project work within its defined role.

## Retired

The chat may be interrogated for clarification but must not be used for new project decisions, implementation work, or canonical document revisions.

## Superseded

The chat has been replaced by a later chat or canonical artefact.

## Historical

The chat is preserved as background evidence of prior thinking.

---

# 3. Chat Naming Convention

Recommended format:

    ROLE-### Short Descriptive Name

Roles:

- ARCH = Architecture
- PM = Project management / operational coordination
- BUILD = Implementation
- REVIEW = Review / audit
- BRANCH = exploratory branch

Examples:

    ARCH-001 Constitutional Architecture
    PM-001 Operational Coordination
    PM-002 Implementation Coordination
    BUILD-001 Acquisition Workflow
    REVIEW-001 Prototype Artefact Review

Chat numbers should never be reused.

---

# 4. Chat Registry

## ARCH-001 — Initial Conversation

Status: Retired

Role:

Architecture establishment

Purpose:

Create and refine the constitutional architecture prompt for the project.

Major outcomes:

- Defined architecture-chat responsibilities
- Defined architecture-chat boundaries
- Produced architecture-chat initiation prompt
- Established architectural philosophy

Canonical artefacts:

- Architectural initiation prompt
- chats/prompts/ARCH-001.txt

Commit range:

0c9c07e

Status note:

Retired following creation of ARCH-002.

---

## ARCH-002 — Prototype Review Plan

Status: Active

Role:

Architectural authority

Purpose:

Review prototype artefacts and establish constitutional architectural principles for the project.

Major outcomes:

- Prototype review
- Architectural review
- Creation of ARCHITECTURAL_PRINCIPLES.md
- Establishment of constitutional architecture authority
- Notified of deferred citation-quality analytical requirement concerning DOI omission and URL integrity analysis

Canonical artefacts:

- docs/ARCHITECTURAL_PRINCIPLES.md

Commit range:

Not tracked through this chat.

Status note:

Current architectural authority.

No immediate architectural decision is required on citation-quality analysis, but later schema/provenance design should account for the distinction between raw source citation, parsed reference, matched work, URL status observation, and derived citation-quality claim.

---

## PM-001 — Operation Coordination Focus

Status: Retired

Role:

Project management / operational coordination

Started:

2026-05-24

Retired:

2026-06-04

Purpose:

Move the project from governance establishment into operational implementation.

Major outcomes:

- Established PM governance model
- Reviewed prototype operational artefacts
- Produced canonical operational documents
- Established repository structure
- Established Python environment discipline
- Established Git/GitHub workflow
- Established scripting conventions
- Implemented acquisition workflows
- Acquired first CESE artefact
- Acquired initial CESE seed corpus
- Established operator governance
- Established chat governance

Canonical artefacts produced or substantially revised:

- docs/MASTER_PROJECT_BRIEF.md
- docs/CURRENT_STATE.md
- docs/ACTIVE_ISSUES.md
- docs/PIPELINE_MAP.md
- docs/CHAT_HANDOFF_PROTOCOL.md
- docs/SCRIPTING_CONVENTIONS.md
- docs/CHAT_INDEX.md
- docs/OPERATOR_WORKFLOW.md
- manifests/acquisition_manifest.jsonl
- manifests/acquisition_inputs/cese_initial_seed_urls.txt
- scripts/acquire_single_report.py
- scripts/acquire_cese_reports.py
- README.md
- requirements.txt
- .gitignore
- chats/prompts/PM-001_init.txt
- chats/prompts/retirement.txt

Commit range:

8f015c4 → 4495c08

Commit register:

| Commit | Message |
|----------|----------|
| 8f015c4 | Initial operational scaffold |
| b0151fd | Add scripting conventions |
| e27cacf | Add first acquisition workflow |
| 9c744af | Implement first provenance-aware acquisition workflow |
| eefafc5 | Acquire initial CESE report corpus |
| 5c452c2 | Acquire initial CESE report corpus |
| 4495c08 | Add chat and user management |

Status note:

This chat is retired.

It may be interrogated for clarification but must not be used for new project decisions, implementation work, or canonical document revisions.

---

## PM-002 — Implementation Coordination

Status: Active

Role:

Project management / operational coordination

Started:

2026-06-04

Purpose:

Coordinate implementation after PM-001 retirement, maintain bounded milestones, track commits, prevent scope drift, support acquisition validation, extraction-readiness work, and bounded implementation progress.

Major outcomes:

- Validated acquisition manifest against preserved raw artefacts
- Added acquisition manifest validation script
- Established embedded-text PDF inspection workflow
- Confirmed selected CESE PDFs contain extractable embedded text
- Confirmed OCR is not required for selected test artefacts
- Identified formal reference-section markers in selected CESE report PDFs
- Confirmed infographic-style artefacts may contain citations without formal reference sections
- Added minimum viable raw reference-section extraction workflow
- Successfully extracted raw reference sections from selected CESE report PDFs
- Confirmed non-reference-section infographic exits gracefully without false extraction
- Updated CURRENT_STATE.md to reflect validated acquisition and raw reference-section extraction state
- Updated CHAT_INDEX.md
- Updated .gitignore for generated/local artefacts
- Added curated chat prompt files under chats/prompts/
- Recorded deferred citation-quality requirement covering missing DOI analysis and URL integrity checking
- Notified ARCH-002 of deferred citation-quality analytical requirement
- Pushed PM-002 implementation commits to GitHub

Canonical artefacts produced or substantially revised:

- scripts/validate_acquisition_manifest.py
- scripts/inspect_pdf_text.py
- scripts/extract_reference_section.py
- docs/CURRENT_STATE.md
- docs/ACTIVE_ISSUES.md
- docs/CHAT_INDEX.md
- .gitignore
- chats/prompts/ARCH-001.txt
- chats/prompts/PM-001_init.txt
- chats/prompts/PM-002_init.txt
- chats/prompts/retirement.txt

Working artefacts generated but not necessarily versioned:

- data/working/text_inspection/2017-cognitive-load-theory.txt
- data/working/text_inspection/2020-classroom-management-literature-review.txt
- data/working/text_inspection/2020-classroom-management-infographic.txt
- data/working/reference_sections/2017-cognitive-load-theory_references.txt
- data/working/reference_sections/2020-classroom-management-literature-review_references.txt

Commit range:

34b6ffa → 545d1e9

Commit register:

| Commit | Message |
|----------|----------|
| 34b6ffa | Add acquisition manifest validation script |
| c0e5c28 | Add PDF text inspection script |
| 8850670 | Add reference section extraction script |
| 0c9c07e | Update project state and gitignore |
| e7f8126 | Update chat index commit register |
| 545d1e9 | Update active issues for citation quality requirements |
| c630aad | Add reference inspection and boundary detection workflows |
| cadd9bd | Update chat index commit register |

Status note:

Current active PM chat.

The immediate next implementation task is reference-section quality inspection, not citation parsing, metadata enrichment, URL checking, DOI omission analysis, or database construction.

---

# 5. Current Active Chats

## ARCH-002 — Prototype Review Plan

Status:

Active

Role:

Architectural authority

Current note:

ARCH-002 has been notified of a deferred analytical requirement concerning citation-quality analysis:

- citations where CESE omits a DOI despite the matched work having one
- citations containing dead, redirected, unstable, or otherwise unavailable URLs

No immediate architectural decision is required.

This should inform later schema, provenance, canonicalisation, and enrichment design.

---

## PM-002 — Implementation Coordination

Status:

Active

Role:

Project management / operational coordination

Current milestone:

Reference-section quality inspection readiness.

Next bounded implementation task:

    scripts/inspect_reference_section.py

Current deferrals:

- individual reference parsing
- citation inventory implementation
- OpenAlex enrichment
- Crossref enrichment
- DOI omission analysis
- URL integrity checking
- database schema design
- analytical outputs

---

# 6. Retirement Protocol

When a chat is retired, paste the following into that chat:

    This chat is now retired.

    From this point onward:
    - do not make new project decisions in this chat
    - do not develop new workflows in this chat
    - do not revise canonical project documents from this chat
    - do not treat this chat as active operational authority

    Permitted uses:
    - answer questions about what happened in this chat
    - clarify prior reasoning
    - identify decisions made here
    - support handover into active chats

    Current authoritative project state now lives in:
    - repository files
    - canonical docs
    - active PM / Architecture / Build chats

    If future work is requested here, redirect the user to the current active chat listed in CHAT_INDEX.md.

---

# 7. Maintenance Rule

Update CHAT_INDEX.md when:

- a new project chat is created
- a chat is retired
- a chat produces a canonical artefact
- a chat substantially revises a canonical artefact
- commits occur under the coordination of a chat

Record all commits associated with a chat.

Do not attempt to classify commits as major or minor.

Routine conversational details should not be recorded.