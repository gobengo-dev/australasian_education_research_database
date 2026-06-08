# ACTIVE_ISSUES.md

Status: canonical operational issues register  
Version: v0.4  
Last updated: 2026-06-08

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
- continue treating current extraction and parsing work as minimum viable evidence-gathering, not full citation infrastructure
- continue to avoid enrichment, matching, and analytical claims until individual reference records exist

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

This risk is heightened when valid future analytical requirements are identified before the prerequisite extraction and parsing layers are complete.

Current mitigation:

- acquisition-first sequencing
- extraction-before-enrichment sequencing
- reference-boundary review before structured parsing
- implementation milestones
- visible deliverables
- architecture chat separation
- defer schema and canonicalisation decisions until concrete parsed examples exist
- treat current reference-boundary outputs as draft candidates, not final citation records
- treat the first structured parser as a working experiment, not a database design exercise

Status:  
Active

---

## ISSUE-003

Title:  
Extraction and boundary-detection layer complexity

Severity:  
High

Description:

Reference extraction from PDFs introduces substantially more complexity than acquisition.

Raw reference-section extraction has now been demonstrated on selected CESE PDFs, draft individual reference-boundary detection has been implemented for formal reference sections, and candidate outputs have been reviewed under a manual and AI-assisted review protocol.

However, structured individual reference parsing has not yet been implemented, and boundary detection remains heuristic.

Known complexity includes:

- two-column PDF layouts
- image-adjacent reference text
- split letters and split words in extracted text
- compressed adjacent references
- publisher or institution tails being mistaken for new references
- section-numbered reference headings
- APA-style references with parenthesised years and initials
- older CESE author-date references with unparenthesised years
- legal or statutory references
- URL-bearing references absorbing following references
- artefacts with citations but no formal references section
- footnote-only citation formats
- distinction between raw section extraction, boundary detection, structured reference parsing, and later citation inventories

Current mitigation:

- acquisition layer completed and validated first
- embedded-text inspection implemented
- raw reference-section extraction implemented
- numbered reference-heading detection implemented
- reference-section inspection implemented
- draft reference-boundary detection implemented
- candidate review protocol established
- candidate review results recorded
- first structured parsing input selected conservatively
- OCR deferred unless clearly required
- infographic and footnote-style citation extraction deferred
- APA-style boundary problems identified and deferred as a separate style class
- current outputs treated as candidate references requiring review, not final citation inventory records

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

The risk increases during exploratory implementation periods when several scripts, review outputs, and temporary working artefacts are created before commit discipline catches up.

Current mitigation:

- canonical operational documents
- scripting conventions
- acquisition manifests
- Git version control
- repository discipline
- chat registry
- commit tracking
- small bounded implementation milestones
- clean up temporary draft files before committing
- avoid preserving draft script versions in the repository once a canonical script version exists
- record review decisions in repository documents rather than relying on chat history

Status:  
Active

---

## ISSUE-005

Title:  
Premature analytical infrastructure

Severity:  
High

Description:

There is pressure to begin designing databases, schemas, enrichment workflows, citation-quality metrics, and analytical systems before structured individual reference parsing requirements are understood.

Current mitigation:

- acquisition before extraction
- raw extraction before reference parsing
- reference-boundary detection before structured parsing
- candidate-boundary review before structured parsing
- structured reference parsing before citation inventories
- citation inventories before enrichment
- enrichment before analysis
- defer DOI omission and dead-link analysis until individual citation records exist
- defer schema design until enough real parsed citation examples have been inspected

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
- do not implement before citation inventory structure exists
- treat URL status as timestamped check evidence, not permanent truth
- treat missing DOI as a derived claim requiring matched-work evidence
- notify architecture chat before schema or canonicalisation decisions are made

Status:  
Active

---

## ISSUE-007

Title:  
Reference-boundary false splits from publisher or institution tails

Severity:  
Medium

Description:

Draft reference-boundary detection can mistakenly split publisher or institution tails into separate candidate references.

Observed examples include:

- a publisher tail such as “Grattan Institute.”
- an institution tail after an abbreviation such as “U.S. Department of Education, Washington, DC.”

This occurs because embedded boundary detection treats terminal punctuation followed by a plausible organisation-like phrase as a possible new reference.

This is a known boundary-detector issue, not a raw extraction failure.

Current mitigation:

- treat boundary outputs as candidate references requiring review
- retain confidence and embedded-split flags in candidate outputs
- document known false splits in reference-candidate review results
- do not treat reference candidates as final citation records
- defer refinement until this issue blocks the next implementation stage or recurs across enough examples to justify a bounded fix

Status:  
Active

---

## ISSUE-008

Title:  
Structured parsing scope creep

Severity:  
High

Description:

The next implementation step is minimum viable structured reference parsing.

There is risk that this step expands into:

- full citation parsing
- comprehensive reference-style handling
- database schema design
- OpenAlex or Crossref matching
- DOI discovery
- URL validation
- canonical work/entity modelling
- bibliographic correctness checking

This would create substantial hidden complexity and could delay delivery of a minimal working pipeline.

Current mitigation:

- first parser input selected: 2017-cognitive-load-theory_reference_candidates.txt
- parser should preserve raw reference text unchanged
- parser should extract only conservative fields
- parser should explicitly record parse uncertainty
- parser should not write database records
- parser should not perform enrichment, matching, DOI discovery, or URL checking
- parser should not attempt to handle all reference styles in the first iteration
- APA-style references remain deferred until later boundary refinement

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
Minimum viable individual reference parsing workflow

Status:  
Partially resolved

Question:

How should candidate reference boundaries be transformed into individual reference records suitable for later citation inventory work?

Current context:

The following scripts now exist:

- scripts/inspect_pdf_text.py
- scripts/extract_reference_section.py
- scripts/inspect_reference_section.py
- scripts/detect_reference_boundaries.py

The following review documents now exist or are being prepared:

- docs/REFERENCE_CANDIDATE_REVIEW_PROTOCOL.md
- docs/REFERENCE_CANDIDATE_REVIEW_RESULTS.md

Current reviewed candidate outputs show that the 2017 cognitive load candidate output is suitable as the first structured parsing baseline.

The first structured parsing experiment should use:

- data/working/reference_candidates/2017-cognitive-load-theory_reference_candidates.txt
- preferably the paired JSONL candidate output if available

The parser does not yet exist.

Known considerations:

- preserve raw reference text unchanged
- preserve candidate ID and source pages
- preserve boundary confidence and boundary flags
- extract conservative fields only
- record parse status and parse notes
- avoid overfitting to one document while still keeping the first parser bounded
- do not introduce enrichment, DOI matching, URL checking, or database writes

---

## UNKNOWN-002

Title:  
Reference-boundary validation threshold

Status:  
Partially resolved

Question:

What level of accuracy is sufficient for draft candidate reference boundaries before moving to structured parsing?

Current context:

A manual and AI-assisted review protocol has been created, and four candidate outputs have been reviewed.

Current reviewed classifications:

- 2017 cognitive load: SUITABLE_FOR_PARSING_EXPERIMENT
- 2020 classroom management: SUITABLE_WITH_KNOWN_WARNINGS
- revisiting gifted education: SUITABLE_WITH_KNOWN_WARNINGS
- 2015 tutoring interventions: DEFERRED_STYLE_CLASS

Operational decision:

The threshold for beginning a first structured parsing experiment has been met for the 2017 cognitive load candidate output only.

Still unresolved:

- formal quantitative acceptance threshold
- how many reviewed documents are required before broader parsing work
- how to treat candidate-level warnings during structured parsing
- whether boundary review outcomes should become a persistent machine-readable manifest

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

Candidate reference-boundary detection currently records:

- source reference-section path
- candidate ID
- start page
- end page
- source line count
- boundary reason
- confidence
- terminal punctuation flag
- embedded boundary split flag
- possible text damage flag
- contains URL flag
- contains DOI flag
- raw candidate text

Reference-candidate review records currently identify:

- source PDF
- reference-section file
- candidate output file
- review date
- reviewer
- console summary
- manual boundary checks
- style class
- classification
- decision
- notes

Still unresolved:

- extraction manifests
- persistent provenance for individual reference parsing
- provenance for text cleaning or repair
- provenance for rejected or uncertain references
- relationship between raw reference-section extraction, candidate boundaries, review classifications, parsed references, and later matched works

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
- candidate reference boundary record
- reference-candidate review status
- individual raw reference string
- parsed citation fields
- parsing confidence
- source-visible DOI, if present
- source-visible URL, if present
- later matched work identifiers
- later quality checks

No schema should be designed until structured reference parsing examples exist.

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

## UNKNOWN-009

Title:  
Treatment of non-formal citation formats

Status:  
Unresolved

Question:

How should the project handle CESE artefacts that contain citations but do not contain a formal reference section?

Current context:

At least two non-formal classes have been observed:

- infographic-style artefacts with limited citations or footnote-like source notes
- older CESE reports using page-level footnote references rather than a consolidated references section

Known considerations:

These require a different extraction workflow from formal reference-section extraction.

They should not be forced into extract_reference_section.py or detect_reference_boundaries.py.

---

## UNKNOWN-010

Title:  
APA-style boundary detection

Status:  
Deferred style class

Question:

How should boundary detection handle APA-style references with parenthesised years and author initials?

Current context:

The 2015 tutoring intervention report exposed a systematic failure mode where embedded splitting over-splits author initials.

Example pattern:

- “Britz, M. W., Dixon, J., & McLaughlin, T. F. (1989).”

The current detector may split incorrectly after initials such as “M.” or “P.” if the following text later resembles a reference start.

Reference-candidate review classified this document as:

- DEFERRED_STYLE_CLASS

Known considerations:

This appears to be a general style-class issue rather than a single idiosyncratic reference.

It should be addressed separately from older CESE author-date boundary detection.

It should not block the first structured parsing experiment, which will use the 2017 cognitive load candidate output.

---

## UNKNOWN-011

Title:  
Parser output format

Status:  
Unresolved

Question:

What should the minimum viable structured parser output look like?

Current context:

The first parser should probably read candidate JSONL and produce a working output under data/working/.

Possible conservative fields include:

- candidate_id
- source candidate file
- source pages
- raw reference text
- boundary confidence
- embedded boundary split flag
- possible text damage flag
- source-visible URL flag
- source-visible DOI flag
- detected year
- first author or organisation string
- title-like segment, only if safely detectable
- parse status
- parse notes

Known considerations:

- JSONL is likely appropriate for provenance-preserving intermediate output
- CSV may be useful for manual inspection
- raw reference text must be preserved unchanged
- uncertain fields should be explicit rather than silently guessed
- no database writes should occur in the first parser

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
- reference-section inspection implemented
- draft reference-boundary detection implemented
- numbered reference-section headings detected by PDF inspection
- numbered reference-section headings handled by reference-section extraction
- numbered reference-section headings filtered from boundary detection input
- selected long formal CESE reference section processed into candidate references
- statutory reference example handled as a candidate reference
- reference-candidate review protocol drafted
- first set of candidate outputs reviewed
- first structured parsing input selected

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
- broad CESE acquisition expansion beyond current seed corpus
- citation inventory implementation
- extraction manifests
- database schema design
- OpenAlex enrichment
- Crossref enrichment
- DOI omission analysis
- URL dead-link analysis
- infographic citation extraction
- footnote-only citation extraction
- APA-style boundary refinement
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

- distinction between raw source citation, extracted reference section, candidate reference boundary, reference-candidate review outcome, parsed reference, matched work, and derived quality claim
- whether reference-candidate review outcomes should be persisted as first-class provenance records
- provenance expectations for structured reference parsing
- provenance expectations for DOI omission analysis
- provenance expectations for URL integrity checking
- whether URL status should be modelled as a timestamped observation rather than a citation attribute
- how to represent citation-quality findings without overstating certainty
- whether citation-quality analysis belongs in v0.1 or should remain a later analytical layer
- how extraction-stage confidence should relate to later citation inventory records
- whether candidate reference boundaries should be persisted as a first-class intermediate artefact

No immediate architecture decision is required before the first minimum viable structured parsing experiment.

---

# 7. Next Issue Review Trigger

Review this document when one of the following occurs:

- structured reference parsing begins
- first parser output is generated
- parser output format becomes stable enough to document
- parser uncertainty handling proves inadequate
- extraction manifests are proposed
- citation inventory structure is proposed
- OpenAlex or Crossref integration is proposed
- URL checking is proposed
- DOI omission analysis is proposed
- publisher-tail false splits block progress
- APA-style reference handling becomes the next implementation focus
- non-formal citation formats become the next implementation focus
- new infrastructure is proposed
- scope expands significantly
- operational complexity increases materially
- a current mitigation proves inadequate

Do not update this document merely because work progresses.

Only update it when risks, unknowns, or deferred concerns materially change.