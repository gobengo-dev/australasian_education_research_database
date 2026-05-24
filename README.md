# Australasian Educational Research

Status: v0.1 rebuild phase

---

# Purpose

This repository supports the Australasian Educational Research project.

Current v0.1 focus:

> building a provenance-aware analytical substrate for examining the evidence base cited by selected Australian educational evidence organisations.

Current in-scope organisations:
- CESE
- AERO

---

# Current Priorities

Current implementation priorities:

1. acquisition
2. immutable preservation
3. extraction
4. provenance tracking
5. minimally viable analysis

---

# Project Principles

The project prioritises:

- provenance preservation
- rebuildability
- operational simplicity
- explicit uncertainty
- reproducibility
- auditability
- bounded scope

The project intentionally resists:

- premature optimisation
- ontology explosion
- irreversible transformations
- hidden workflows
- excessive infrastructure complexity

---

# Important Notes

Prototype artefacts may exist in the repository history.

Prototype artefacts should be treated as:
- historical operational evidence
- exploratory infrastructure
- non-authoritative unless explicitly adopted

Canonical operational authority currently exists in:
- ARCHITECTURAL_PRINCIPLES.md
- operational documents

---

# Current Status

The project is currently in:
- governance stabilisation
- operational reconstruction
- acquisition planning

No authoritative production pipeline currently exists.

---

# Working Assumptions

Current environment assumptions:

- macOS (arm64)
- Python + venv
- DuckDB
- Git for scripts/docs/manifests
- large datasets excluded from Git

---

# Operational Philosophy

The project assumes:
- interruptions will occur
- workflows must remain recoverable
- the system must remain maintainable by a solo researcher
- bounded delivery is more important than theoretical completeness

---

# Canonical bootstrap sequence

git clone <repo>
cd australasian_education_research_database

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

---

# v0.1 Success Condition

The intended v0.1 success condition is:

> a provenance-aware analytical substrate capable of supporting real research questions reproducibly.