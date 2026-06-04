# CHAT_INDEX.md

Status: canonical chat registry  
Version: v0.1  
Last updated: 2026-06-04  

---

# 1. Purpose

This document records the active and retired ChatGPT chats used in the Australasian Educational Research project.

It is intended to:

- reduce chat drift
- clarify chat authority
- preserve operational continuity
- identify which chats produced which artefacts
- link project work to Git commits
- prevent retired chats from being used for new decisions

This document is not a transcript archive.

---

# 2. Chat Status Terms

## Active

The chat may be used for new project work within its defined role.

## Retired

The chat may be interrogated for clarification, but must not be used for new project decisions, new implementation work, or canonical document revisions.

## Superseded

The chat has been replaced by a later chat or canonical document.

## Historical

The chat is preserved only as background evidence of prior thinking.

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

---

# 4. Chat Registry

## PM-001 — Operation Coordination Focus

Status: Retired  
Role: Project management / operational coordination  
Started: 2026-05-24  
Retired: 2026-06-04  

Purpose:

Established the operational management layer for the project and moved the project from governance/planning into active acquisition implementation.

Major outcomes:

- Confirmed PM role boundaries
- Reviewed prototype operational artefacts
- Produced fresh canonical operational documents
- Established repository structure
- Established Python environment discipline
- Established Git/GitHub workflow
- Created scripting conventions
- Implemented first acquisition workflow
- Acquired first CESE artefact
- Implemented batch CESE acquisition
- Acquired initial CESE seed corpus
- Updated CURRENT_STATE.md
- Updated ACTIVE_ISSUES.md
- Planned transition to PM-002

Canonical artefacts produced or updated:

- docs/MASTER_PROJECT_BRIEF.md
- docs/CURRENT_STATE.md
- docs/ACTIVE_ISSUES.md
- docs/PIPELINE_MAP.md
- docs/CHAT_HANDOFF_PROTOCOL.md
- docs/SCRIPTING_CONVENTIONS.md
- manifests/acquisition_manifest.jsonl
- manifests/acquisition_inputs/cese_initial_seed_urls.txt
- scripts/acquire_single_report.py
- scripts/acquire_cese_reports.py
- README.md
- requirements.txt
- .gitignore

Commit register:

| Commit | Commit message | Status | Notes |
|---|---|---|---|
| 04a1837 | unknown GitHub starter commit | overwritten | Pre-existing remote commit overwritten during initial repository synchronisation. |
| 8f015c4 | Initial operational scaffold | confirmed | First confirmed local project commit; force-pushed to remote with --force-with-lease. |
| unknown | Add scripting conventions | pending verification | Commit was recommended in PM-001; hash not confirmed in chat. |
| unknown | Implement first provenance-aware acquisition workflow | pending verification | Commit was recommended in PM-001; hash not confirmed in chat. |
| unknown | Acquire initial CESE report corpus | pending verification | Commit was recommended in PM-001; hash not confirmed in chat. |
| unknown | Update current state and active issues | pending verification | Work reported complete before PM-002 planning; hash not confirmed in chat. |

Status note:

This chat is retired. It may be interrogated for clarification, but must not be used for new project decisions, implementation work, or canonical document revisions.

---

# 5. Active Chat

## PM-002 — Implementation Coordination

Status: Proposed  
Role: Project management / operational coordination  
Started: not yet started  

Purpose:

Coordinate implementation after acquisition proof-of-concept and initial CESE seed corpus acquisition.

Expected focus:

- acquisition validation
- extraction planning
- bounded implementation milestones
- operational continuity
- scope discipline
- handoff from PM-001

Authoritative starting documents:

- docs/ARCHITECTURAL_PRINCIPLES.md
- docs/MASTER_PROJECT_BRIEF.md
- docs/CURRENT_STATE.md
- docs/ACTIVE_ISSUES.md
- docs/PIPELINE_MAP.md
- docs/CHAT_HANDOFF_PROTOCOL.md
- docs/SCRIPTING_CONVENTIONS.md
- docs/CHAT_INDEX.md

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

CHAT_INDEX.md should be updated when:

- a new project chat is created
- a chat is retired
- a chat produces or substantially revises canonical artefacts
- commits are made under the coordination of a chat

Routine conversational details should not be recorded here.