# ACTIVE_ISSUES.md

Status: canonical operational issues register  
Version: v0.2  
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

The project naturally encourages expansion toward ecosystem-scale infrastructure, large-scale acquisition, advanced metadata systems, identity resolution, analytical platforms, and citation-quality analysis.

This creates risk of delaying delivery of a functioning v0.1 system.

Current mitigation:

- bounded v0.1 scope
- constitutional architectural principles
- milestone-based delivery
- explicit deferral policy
- maintain distinction between current implementation tasks and future analytical requirements

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

This risk is heightened when valid future analytical requirements are identified before the prerequisite extraction layers are complete.

Current mitigation:

- acquisition-first sequencing
- extraction-before-enrichment sequencing
- implementation milestones
- visible deliverables
- architecture chat separation
- defer schema and canonicalisation decisions until concrete extracted examples exist

Status:  
Active

---

## ISSUE-003

Title:  
Extraction layer complexity

Severity:  
High

Description:

Reference extraction from PDFs introduces substantially more complexity than acquisition.

Raw reference-section extraction has now been demonstrated on selected CESE PDFs, but individual reference parsing has not yet been implemented.

Known complexity includes:

- two-column PDF layouts
- image-adjacent reference text
- split letters and split words in extracted text
- compressed adjacent references
- artefacts with citations but no formal references section
- distinction between raw section extraction and individual citation parsing

Current mitigation:

- acquisition layer completed and validated first
- embedded-text inspection implemented
- raw reference-section extraction implemented
- OCR deferred unless clearly required
- infographic and footnote-style citation extraction deferred
- next step limited to reference-section quality inspection

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
- chat registry
- commit tracking
- small bounded implementation milestones

Status:  
Active

---

## ISSUE-005

Title:  
Premature analytical infrastructure

Severity:  
High

Description:

There is pressure to begin designing databases, schemas, enrichment workflows, citation-quality metrics, and analytical systems before individual reference parsing requirements are understood.

Current mitigation:

- acquisition before extraction
- raw extraction before reference parsing
- reference parsing before enrichment
- enrichment before analysis
- defer DOI omission and dead-link analysis until individual citation records exist

Status:  
Active

---

## ISSUE-006

Title:  
Citation quality analysis scope expansion

Severity:  
Medium

Description:

A new analytical requirement has been identified:

The project should eventually support analysis of citation quality in CESE and related documents, including:

- references where the source citation omits a DOI even though the cited work appears to have one
- references containing URLs that are dead, redirected, unstable, or otherwise unavailable when checked

This is valuable and aligned with the project’s provenance and research infrastructure aims, but it depends on later implementation layers that do not yet exist.

Current mitigation:

- record as a deferred analytical requirement
- do not implement before individual reference parsing
- treat URL status as timestamped check evidence, not permanent truth
- treat missing DOI as a derived claim requiring matched-work evidence
- notify architecture chat before schema or canonicalisation decisions are made

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
Reference-section quality inspection workflow

Status:  
Unresolved

Question:

What is the minimum viable workflow for inspecting extracted raw reference sections before attempting individual reference parsing?

Current context:

Raw reference-section extraction has been demonstrated.

The next implementation step is expected to be:

    scripts/inspect_reference_section.py

---

## UNKNOWN-002

Title:  
Individual reference parsing workflow

Status:  
Unresolved

Question:

How should raw extracted reference sections be split into individual reference records?

Known considerations:

- author-date citation style
- multi-line reference entries
- page-layout artefacts
- split words and initials
- compressed adjacent references
- non-standard artefacts without formal reference sections

---

## UNKNOWN-003

Title:  
Extraction provenance model

Status:  
Partially resolved

Question:

What provenance information must be recorded for extraction activities?

Current context:

Raw reference-section extraction currently records:

- source PDF path
- extraction method
- OCR status
- extraction type
- reference marker text
- reference marker page
- extracted page range
- stop marker text, where detected
- stop marker page, where detected
- page-delimited extracted text

Still unresolved:

- extraction manifests
- provenance for individual reference parsing
- provenance for text cleaning or repair
- provenance for rejected or uncertain references

---

## UNKNOWN-004

Title:  
Citation inventory structure

Status:  
Unresolved

Question:

How should extracted individual references be stored and tracked?

Known considerations:

The citation inventory will likely need to distinguish:

- source document
- raw reference-section extraction
- individual raw reference string
- parsed citation fields
- parsing confidence
- source-visible DOI, if present
- source-visible URL, if present
- later matched work identifiers
- later quality checks

No schema should be designed until reference parsing examples exist.

---

## UNKNOWN-005

Title:  
OpenAlex integration strategy

Status:  
Unresolved

Question:

How should OpenAlex be introduced after extraction and reference parsing are operational?

Known considerations:

OpenAlex may be useful for:

- matching parsed references to works
- identifying works with DOI metadata
- supporting later analysis of citations where CESE omitted available DOIs

This should not be implemented before individual reference records exist.

---

## UNKNOWN-006

Title:  
Crossref integration strategy

Status:  
Unresolved

Question:

How should Crossref be introduced after extraction and reference parsing are operational?

Known considerations:

Crossref may be useful for:

- DOI discovery
- bibliographic metadata verification
- confirming whether a cited work has a DOI
- supporting DOI omission analysis

This should not be implemented before individual reference records exist.

---

## UNKNOWN-007

Title:  
URL integrity checking strategy

Status:  
Unresolved

Question:

How should URLs appearing in source citations be checked, recorded, and interpreted?

Known considerations:

URL status is time-dependent.

Any future URL integrity workflow should record:

- URL as cited
- check timestamp
- checking script/version
- HTTP status code, where available
- redirect target, where applicable
- failure reason, where applicable
- whether the URL appears dead at the time checked

Dead-link status should be treated as timestamped evidence rather than a permanent property.

---

## UNKNOWN-008

Title:  
DOI omission analysis strategy

Status:  
Unresolved

Question:

How should the project determine whether a source citation omitted a DOI that was available for the cited work?

Known considerations:

A DOI omission finding requires at minimum:

- individual source citation text
- determination of whether the source citation visibly included a DOI
- matched-work evidence from a metadata source such as Crossref or OpenAlex
- confidence level for the match
- timestamped metadata retrieval provenance

DOI omission should be treated as a derived analytical claim, not a raw extraction fact.

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
- acquisition manifest validation implemented
- current CESE acquisition corpus validated against manifest
- embedded PDF text inspection implemented
- selected CESE PDFs confirmed to contain extractable embedded text
- raw reference-section extraction implemented
- selected formal CESE report reference sections extracted successfully
- infographic-style artefact handled gracefully as no formal reference section

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
- broad AERO acquisition expansion
- individual reference parsing beyond quality inspection
- citation inventory implementation
- extraction manifests
- OpenAlex enrichment
- Crossref enrichment
- DOI omission analysis
- URL dead-link analysis
- infographic citation extraction
- footnote-only citation extraction
- OCR workflows
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

# 6. Architecture Escalation Notes

The following items should be raised with the architecture chat before schema, canonicalisation, or enrichment design begins:

- distinction between raw source citation, parsed reference, matched work, and derived quality claim
- provenance expectations for DOI omission analysis
- provenance expectations for URL integrity checking
- whether URL status should be modelled as a timestamped observation rather than a citation attribute
- how to represent citation-quality findings without overstating certainty
- whether citation-quality analysis belongs in v0.1 or should remain a later analytical layer

No immediate architecture decision is required before reference-section quality inspection.

---

# 7. Next Issue Review Trigger

Review this document when one of the following occurs:

- reference-section quality inspection is implemented
- individual reference parsing begins
- extraction manifests are proposed
- citation inventory structure is proposed
- OpenAlex or Crossref integration is proposed
- URL checking is proposed
- DOI omission analysis is proposed
- new infrastructure is proposed
- scope expands significantly
- operational complexity increases materially
- a current mitigation proves inadequate

Do not update this document merely because work progresses.

Only update it when risks, unknowns, or deferred concerns materially change.