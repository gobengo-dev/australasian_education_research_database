# ARCHITECTURAL_PRINCIPLES.md

Status: constitutional architectural document  
Project: Australasian Educational Research  
Version: v0.1-draft  
Prepared: 2026-05-24  
Status of assertions: mixed; unresolved items must remain explicitly labelled.

---

# 1. Purpose

This document establishes the foundational architectural principles governing the Australasian Educational Research infrastructure project.

It defines:

- operational philosophy
- provenance philosophy
- scope boundaries
- workflow discipline
- reproducibility standards
- governance expectations
- canonicalisation principles
- architectural constraints
- anti-drift safeguards

This document is intended to:

- constrain future architectural drift
- preserve operational defensibility
- reduce ambiguity
- support reproducibility
- prioritise deliverability
- maintain bounded scope
- support future scholarly credibility

This document is intentionally conservative.

---

# 2. Project Framing

## 2.1 Current v0.1 Scope

The current v0.1 project scope is:

> a provenance-aware analytical infrastructure for examining the evidence base cited by selected Australian educational evidence organisations.

Current in-scope organisations:

- CESE
- AERO

Current v0.1 objectives:

- preserve publication artefacts
- extract references
- preserve source claims
- identify cited researchers
- identify cited institutions
- identify cited journals/sources
- preserve identifiers and provenance
- support reproducible analytical snapshots

The v0.1 project is NOT:

- a universal scholarly graph
- a comprehensive Australasian research corpus
- a Google Scholar replacement
- a real-time indexing platform
- a public search engine
- a SaaS platform
- a full-text repository
- a national research infrastructure

---

# 3. Foundational Philosophy

## 3.1 Provenance First

Preservation of provenance overrides aggressive cleaning, simplification, or canonicalisation.

The system must preserve:

- where information came from
- when it was obtained
- how it was obtained
- which workflow produced it
- which transformations affected it
- which interpretations were later derived from it

The system must preserve source claims before canonical interpretation.

---

## 3.2 Raw Artefacts Are Evidentiary Objects

Downloaded source artefacts are immutable evidentiary objects.

Source artefacts must not be silently overwritten.

Principle:

> same URL + different hash = different artefact

Artefact preservation should include, where possible:

- retrieval timestamp
- source organisation
- landing page URL
- direct download URL
- source filename
- local filename
- checksum/hash
- retrieval workflow
- retrieval provenance
- file size
- HTTP metadata where available

---

## 3.3 Canonical Entities Are Interpretations

Canonical entities are derived interpretations, not raw truth.

Canonicalisation must therefore:

- preserve reversibility
- preserve provenance
- preserve conflicting claims where relevant
- remain rebuildable
- avoid destructive rewriting

The system must distinguish:

| Type | Meaning |
|---|---|
| source claim | assertion made by a source |
| canonical interpretation | system-level reconciliation |
| analytical interpretation | analysis-layer interpretation |

---

## 3.4 Explicit Uncertainty

Uncertainty must be preserved rather than hidden.

The project should prefer:

> explicit uncertainty over false precision.

Architectural claims, classifications, and interpretations should be labelled where appropriate as:

- confirmed
- inferred
- likely
- uncertain
- unresolved
- deferred
- speculative

---

# 4. Scope Discipline

## 4.1 Bounded v0.1 Scope

The v0.1 scope must remain intentionally narrow.

The project must resist drift toward:

- ecosystem-scale scholarly infrastructure
- comprehensive educational research harvesting
- broad bibliometric platforms
- ontology-heavy architectures
- excessive entity systems
- premature analytical expansion

Future expansion remains possible but is not assumed.

---

## 4.2 Expansion Requires Justification

New architectural complexity requires explicit justification.

Before introducing any new subsystem, ask:

- Is this necessary now?
- Is this reversible?
- Is this reproducible?
- Is this operationally defensible?
- Is this maintainable by a solo researcher?
- Is this analytically justified?
- Can this be deferred?

If the answer is unclear, defer.

---

# 5. Architectural Layer Separation

The architecture must maintain strict conceptual separation between layers.

| Layer | Responsibility |
|---|---|
| acquisition | obtaining source artefacts and metadata |
| preservation | immutable evidentiary storage |
| extraction | parsing references and source claims |
| canonicalisation | resolving/interpreting entities |
| enrichment | attaching external metadata |
| analysis | analytical interpretation |
| publication | outputs/reports/snapshots |

No layer should silently overwrite or erase upstream evidence.

---

# 6. Reproducibility Principles

## 6.1 Rebuildability

Derived outputs should be reproducible from:

- preserved source artefacts
- preserved raw claims
- deterministic scripts where feasible
- documented workflows
- versioned manifests

Derived layers should not become irreplaceable black boxes.

---

## 6.2 Snapshot Philosophy

The project should prefer snapshot-based reproducibility over mutable “live truth”.

Analytical outputs should ideally be traceable to:

- source artefact set
- workflow version
- script versions
- processing run IDs
- enrichment state
- canonicalisation state

---

## 6.3 Deterministic Preference

Deterministic scripting is preferred wherever feasible.

Where deterministic behaviour is not possible:

- the non-determinism must be disclosed
- the workflow must remain reviewable
- the workflow must remain procedurally documented

---

# 7. AI Assistance Principles

## 7.1 AI Is Advisory, Not Authoritative

AI may assist:

- architecture design
- workflow design
- script drafting
- exploratory interpretation
- documentation drafting
- analytical ideation

AI must not silently mutate authoritative data.

---

## 7.2 AI-Assisted Transformations

AI-assisted transformations affecting canonical or analytical layers should:

- be reviewable
- be logged
- preserve provenance
- distinguish proposal from authoritative transformation
- produce deterministic scripts where feasible

Human review remains authoritative.

---

## 7.3 AI Drift Awareness

LLM-assisted projects naturally drift toward:

- abstraction expansion
- ontology proliferation
- inferred assumptions
- undocumented architectural mutation

The project must actively resist these tendencies.

---

# 8. Operational Philosophy

## 8.1 Boring Technology Preference

Prefer:

- stable tooling
- mature libraries
- understandable workflows
- explicit documentation
- operational simplicity

Avoid:

- novelty-driven tooling
- unnecessary infrastructure
- premature distributed systems
- architecture requiring a software team

---

## 8.2 GUI Tools Are Secondary

GUI tools may support:

- exploration
- inspection
- query testing
- manual review

However:

No authoritative transformation may exist solely inside GUI tooling.

All authoritative workflows must ultimately exist in:

- scripts
- manifests
- operational documentation
- reproducible procedures

---

## 8.3 Solo Researcher Constraint

The architecture must assume:

- a capable but non-specialist solo operator
- finite maintenance capacity
- finite operational oversight
- intermittent project continuity

The architecture must therefore optimise for:

- recoverability
- readability
- procedural clarity
- bounded operational burden
- explicit documentation

---

# 9. Governance Principles

## 9.1 Prototype Artefacts

Prototype artefacts are historical evidence, not canonical architecture.

Historical materials may contain:

- useful operational insight
- reusable scripts
- failed assumptions
- temporary workarounds
- prototype drift

Prototype artefacts must be critically interrogated before reuse.

---

## 9.2 No Silent Architecture Drift

Changes affecting:

- schema
- provenance rules
- workflow ordering
- canonicalisation logic
- preservation rules
- authoritative tables

must be:

- explicitly proposed
- documented
- reviewable
- versioned

---

## 9.3 Documentation as Infrastructure

Operational documents are part of the infrastructure.

Documentation should preserve:

- assumptions
- unresolved questions
- workflow boundaries
- verification requirements
- known risks
- deferred concerns

---

# 10. Legal and Ethical Principles

The project must remain legally conservative.

The project must not rely on:

- authenticated scraping
- access-control bypassing
- legally ambiguous harvesting
- copyright circumvention

unless explicitly approved and documented.

The project should preserve:

- source attribution
- retrieval provenance
- auditability
- defensible acquisition procedures

---

# 11. Identity Resolution Principles

Identity resolution is valuable but secondary to provenance preservation.

The system should tolerate:

- ambiguity
- duplicates
- partial resolution
- uncertain mappings

Useful analysis should not depend on perfect identity resolution.

The architecture should support layered identity handling:

| Layer | Meaning |
|---|---|
| raw identity | source-native identity |
| candidate identity | possible grouping |
| canonical identity | reviewed interpretation |
| analytical identity | context-specific grouping |

---

# 12. Workflow Discipline

## 12.1 Acquisition Before Sophistication

The project should prioritise:

1. inventory
2. acquisition
3. preservation
4. extraction
5. provenance
6. validation

before sophisticated enrichment or analytics.

---

## 12.2 Exploratory Analysis Is Legitimate

Exploratory analysis is a formal and necessary stage of infrastructure design.

However:

exploration must not silently become authoritative transformation.

---

## 12.3 Preserve Historical Lineage

Where historical processing lineage is incomplete:

- uncertainty should be acknowledged
- reconstructed provenance should be labelled
- historical ambiguity should not be hidden

---

# 13. Future Expansion Principles

Future expansion may eventually include:

- broader educational literature
- institutional repositories
- grey literature
- citation networks
- policy ecosystems
- broader Australasian coverage

However:

future possibilities must not silently distort current architectural priorities.

---

# 14. Architectural Anti-Patterns

The project should actively resist:

- ontology explosion
- premature optimisation
- over-engineering
- irreversible cleaning
- silent canonical overwrites
- hidden manual workflows
- GUI-only transformations
- schema proliferation without need
- architecture requiring permanent AI supervision
- infrastructure assuming a software engineering team

---

# 15. Operational Priority Hierarchy

When trade-offs occur, prioritise in this order:

1. legal defensibility
2. provenance preservation
3. recoverability
4. reproducibility
5. operational simplicity
6. maintainability
7. analytical usefulness
8. completeness
9. sophistication
10. scale

---

# 16. Constitutional Rule

If future architectural proposals conflict with these principles:

- the proposal must justify the deviation explicitly
- the deviation must be documented
- the deviation must be reviewable
- the deviation must not be silently adopted

This document is intended to constrain future architectural drift, including drift introduced through AI-assisted development.