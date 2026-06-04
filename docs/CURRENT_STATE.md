# CURRENT_STATE.md

Status: Active
Last updated: 2026-06-04

---

# 1. Project Status

The Australasian Educational Research project is in active implementation.

Governance, operational scaffolding, repository structure, and initial acquisition workflows have been established.

The current focus is building a provenance-aware acquisition corpus before developing extraction, enrichment, canonicalisation, or analytical workflows.

The project has successfully transitioned from planning and governance establishment into operational execution.

---

# 2. Current Phase

Current phase:

- Acquisition implementation
- Initial corpus construction
- Provenance workflow validation

Current objective:

Establish a reproducible acquisition layer capable of preserving educational research artefacts and their provenance metadata.

The project is not yet focused on:

- reference extraction
- citation analysis
- metadata enrichment
- entity resolution
- analytical database construction

Those activities remain deferred until acquisition workflows have been validated.

---

# 3. Repository Status

Repository status:

- Local repository operational
- Git repository established
- GitHub repository synchronised
- Python virtual environment established
- requirements.txt established
- .gitignore established

Repository structure:

    docs/
    scripts/
    manifests/
    data/raw/
    data/working/
    logs/

Current scripting conventions:

- documented in SCRIPTING_CONVENTIONS.md
- snake_case filenames
- verb_object.py naming convention
- one primary responsibility per script
- Git used for version control rather than filename versioning

---

# 4. Acquisition Infrastructure

Established:

- acquisition_manifest.jsonl
- acquire_single_report.py
- acquire_cese_reports.py

Current acquisition principles:

- preserve source filenames
- preserve source URLs
- record acquisition timestamps
- record acquisition operator
- record acquisition script
- record SHA-256 hashes
- record file sizes
- preserve downloaded artefacts unchanged

Acquisition records are stored in:

    manifests/acquisition_manifest.jsonl

Acquisition input artefacts are stored in:

    manifests/acquisition_inputs/

---

# 5. Current Corpus State

Confirmed acquired artefacts:

CESE:

- 16 PDF artefacts

Current storage location:

    data/raw/cese/

AERO acquisition has not yet commenced.

Current storage location reserved:

    data/raw/aero/

Current corpus should be regarded as:

- an initial seed corpus
- a workflow validation corpus
- not yet a comprehensive collection

---

# 6. Provenance Status

Implemented:

- acquisition provenance
- source URL preservation
- source filename preservation
- retrieval timestamp recording
- retrieval operator recording
- SHA-256 artefact fingerprinting
- acquisition script recording

Not yet implemented:

- extraction provenance
- transformation provenance
- citation provenance
- analytical provenance
- canonical entity provenance

---

# 7. Current Milestone

Current milestone:

Initial acquisition corpus established.

Success criteria achieved:

- acquisition workflow implemented
- acquisition workflow validated
- provenance metadata captured
- multiple artefacts successfully acquired
- acquisition process reproducible

Current corpus:

- 16 CESE artefacts
- 16 acquisition records
- 0 acquisition failures

---

# 8. Current Missing Components

Not yet established:

- reference extraction workflow
- citation inventory
- extraction manifests
- extraction provenance records
- OpenAlex integration
- Crossref integration
- canonical schema
- analytical database
- publication-grade analytical outputs

These components remain intentionally deferred.

---

# 9. Immediate Next Actions

Priority order:

1. Validate acquisition corpus integrity
2. Review acquisition manifest quality
3. Review corpus naming patterns
4. Identify acquisition edge cases
5. Design minimum viable reference extraction workflow

The next implementation milestone should remain narrowly scoped.

The project should avoid premature expansion into:

- enrichment
- entity resolution
- large-scale acquisition
- analytical infrastructure
- advanced database design

until extraction requirements are better understood.

---

# 10. Active Risks

Current project risks:

- scope creep
- premature architecture elaboration
- premature schema design
- premature infrastructure expansion
- acquisition success creating pressure for over-expansion
- hidden complexity entering extraction workflows

Mitigation strategy:

- maintain bounded milestones
- validate each layer before adding the next
- preserve operational simplicity
- continue acquisition-before-sophistication discipline

---

# 11. Operational Notes

The project now possesses:

- governance documentation
- operational documentation
- reproducible acquisition workflows
- provenance-aware acquisition records
- a small but functioning educational research corpus

The project does not yet possess:

- extraction workflows
- analytical workflows
- citation networks
- research-ready datasets

The acquisition layer should be considered operational.

The extraction layer remains the next major implementation target.