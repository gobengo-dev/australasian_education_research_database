# PIPELINE_MAP.md

Status: canonical high-level workflow map
Version: v0.1
Last updated: 2026-05-24

---

# 1. v0.1 Workflow Philosophy

The v0.1 pipeline is intentionally narrow.

Primary focus:
- CESE
- AERO
- publication acquisition
- provenance preservation
- reference extraction
- minimally viable analysis

The pipeline should remain:
- reproducible
- reviewable
- rebuildable
- operationally simple

---

# 2. Canonical Workflow Layers

## Layer 1 — Acquisition

Purpose:
- identify and retrieve source artefacts

Outputs:
- PDFs
- landing-page metadata
- retrieval metadata
- acquisition manifests

---

## Layer 2 — Preservation

Purpose:
- preserve immutable evidentiary artefacts

Requirements:
- hashes/checksums
- retrieval timestamps
- no silent overwrite policy

Core principle:
- same URL + different hash = different artefact

---

## Layer 3 — Extraction

Purpose:
- extract references and source claims

Outputs:
- raw extracted references
- extraction provenance
- extraction logs

Important:
- preserve raw source claims before canonicalisation

---

## Layer 4 — Canonicalisation

Purpose:
- derive tentative canonical entities

Current v0.1 expectation:
- minimal viable canonicalisation only

Important:
- canonical entities are interpretations, not raw truth

---

## Layer 5 — Enrichment

Purpose:
- optionally attach external metadata

Current v0.1 status:
- selective and minimal only

Large-scale enrichment is deferred.

---

## Layer 6 — Analysis

Purpose:
- support reproducible analytical questions

Initial intended outputs:
- cited researchers
- cited institutions
- cited journals
- cited works

---

## Layer 7 — Publication

Purpose:
- produce reproducible snapshots/reports

Requirements:
- provenance-aware
- rebuildable
- versionable

---

# 3. Explicitly Deferred Workflow Areas

Deferred unless operationally justified:

- broad ecosystem harvesting
- ontology-heavy systems
- advanced topic modelling
- broad NLP infrastructure
- graph database migration
- large-scale enrichment systems

---

# 4. Current Implementation Principle

Current implementation priority order:

1. acquisition
2. preservation
3. extraction
4. validation
5. minimally viable analysis

Sophistication follows demonstrated operational need.