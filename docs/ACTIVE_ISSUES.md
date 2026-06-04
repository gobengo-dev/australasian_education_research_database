# ACTIVE_ISSUES.md

Status: canonical operational issues register
Version: v0.1
Last updated: 2026-06-04

---

# 1. Purpose

This document records active operational risks, unresolved questions, and deferred concerns.

Only items that currently affect delivery, continuity, scope control, or operational execution should appear here.

This is not a backlog.

Resolved issues should be removed rather than accumulated.

---

# 2. Active Risks

## ISSUE-001

Title:
Scope expansion pressure

Severity:
Critical

Description:

The project naturally encourages expansion toward ecosystem-scale infrastructure, large-scale acquisition, advanced metadata systems, identity resolution, and analytical platforms.

This creates risk of delaying delivery of a functioning v0.1 system.

Current mitigation:

- bounded v0.1 scope
- constitutional architectural principles
- milestone-based delivery
- explicit deferral policy

Status:
Active

---

## ISSUE-002

Title:
Architecture elaboration replacing implementation

Severity:
Critical

Description:

Project effort may drift toward designing future systems rather than implementing current capabilities.

Current mitigation:

- acquisition-first sequencing
- implementation milestones
- visible deliverables
- architecture chat separation

Status:
Active

---

## ISSUE-003

Title:
Extraction layer complexity

Severity:
High

Description:

The next project phase introduces significant uncertainty.

Reference extraction from PDFs may prove substantially more complex than acquisition.

Current mitigation:

- acquisition layer completed first
- extraction deliberately deferred
- extraction scope not yet expanded

Status:
Active

---

## ISSUE-004

Title:
Operational continuity after interruption

Severity:
High

Description:

The project is expected to progress intermittently.

Extended interruptions may increase restart friction and decision drift.

Current mitigation:

- canonical operational documents
- scripting conventions
- acquisition manifests
- Git version control
- repository discipline

Status:
Active

---

## ISSUE-005

Title:
Premature analytical infrastructure

Severity:
High

Description:

There is pressure to begin designing databases, schemas, enrichment workflows, and analytical systems before extraction requirements are understood.

Current mitigation:

- acquisition before extraction
- extraction before enrichment
- enrichment before analysis

Status:
Active

---

# 3. Current Operational Unknowns

The following questions remain unresolved.

These are not blockers.

They should be resolved when required by implementation.

---

## UNKNOWN-001

Title:
Reference extraction workflow

Status:
Unresolved

Question:

What is the minimum viable workflow for extracting references from acquired PDFs?

---

## UNKNOWN-002

Title:
Extraction provenance model

Status:
Unresolved

Question:

What provenance information must be recorded for extraction activities?

---

## UNKNOWN-003

Title:
Citation inventory structure

Status:
Unresolved

Question:

How should extracted references be stored and tracked?

---

## UNKNOWN-004

Title:
OpenAlex integration strategy

Status:
Unresolved

Question:

How should OpenAlex be introduced after extraction is operational?

---

## UNKNOWN-005

Title:
Crossref integration strategy

Status:
Unresolved

Question:

How should Crossref be introduced after extraction is operational?

---

# 4. Resolved Since Project Commencement

Resolved:

- repository structure established
- Git repository operational
- GitHub repository synchronised
- Python environment established
- acquisition manifest established
- acquisition workflow implemented
- single-report acquisition validated
- batch acquisition validated
- initial CESE acquisition corpus established
- scripting conventions established

These items should not be re-opened unless implementation experience identifies a genuine deficiency.

---

# 5. Deferred Concerns

The following items are intentionally out of scope for the current phase.

Deferred means:

- not required for current milestone
- not actively being designed
- not currently blocking delivery

---

Deferred:

- broad AU/NZ ecosystem acquisition
- advanced identity resolution
- ORCID reconciliation
- institutional reconciliation
- graph databases
- semantic web infrastructure
- large-scale enrichment pipelines
- advanced NLP workflows
- publication infrastructure
- DOI assignment strategy
- ecosystem-wide analytical products

---

# 6. Next Issue Review Trigger

Review this document when one of the following occurs:

- extraction work begins
- new infrastructure is proposed
- scope expands significantly
- operational complexity increases materially
- a current mitigation proves inadequate

Do not update this document merely because work progresses.

Only update it when risks, unknowns, or deferred concerns materially change.