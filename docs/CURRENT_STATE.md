# CURRENT_STATE.md

Status: Active  
Last updated: 2026-06-04

---

# 1. Project Status

The Australasian Educational Research project is in active implementation.

Governance, operational scaffolding, repository structure, initial acquisition workflows, acquisition validation workflows, and minimum viable reference-section extraction workflows have been established.

The project has successfully transitioned from planning and governance establishment into operational execution.

The project now possesses:

- a validated initial CESE acquisition corpus
- a repeatable acquisition validation script
- a PDF embedded-text inspection script
- a minimum viable raw reference-section extraction script
- successful extraction tests on selected CESE reports

The project does not yet possess:

- individual reference parsing
- citation inventories
- metadata enrichment workflows
- OpenAlex or Crossref integration
- canonical work/entity schemas
- analytical datasets
- research outputs

---

# 2. Current Phase

Current phase:

- Validated acquisition
- Extraction reconnaissance
- Minimum viable raw reference-section extraction
- Preparation for reference-section quality inspection

Current objective:

Confirm that formal CESE report PDFs can have raw reference sections extracted from embedded text with enough provenance to support later reference parsing.

The project is not yet focused on:

- citation analysis
- metadata enrichment
- entity resolution
- analytical database construction
- canonicalisation
- publication-grade analytical outputs

The extraction layer has begun, but only at the raw reference-section level.

Individual reference parsing has not yet been implemented.

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

    chats/
    data/raw/
    data/working/
    docs/
    logs/
    manifests/
    scripts/

Current scripting conventions:

- documented in SCRIPTING_CONVENTIONS.md
- snake_case filenames
- verb_object.py naming convention
- one primary responsibility per script
- Git used for version control rather than filename versioning
- scripts should be conservative, inspectable, and reproducible

---

# 4. Acquisition Infrastructure

Established:

- acquisition_manifest.jsonl
- acquire_single_report.py
- acquire_cese_reports.py
- validate_acquisition_manifest.py

Current acquisition principles:

- preserve source filenames
- preserve source URLs
- record acquisition timestamps
- record acquisition operator
- record acquisition script
- record SHA-256 hashes
- record file sizes
- preserve downloaded artefacts unchanged
- validate preserved artefacts against acquisition manifest records

Acquisition records are stored in:

    manifests/acquisition_manifest.jsonl

Acquisition input artefacts are stored in:

    manifests/acquisition_inputs/

Raw acquisition artefacts are stored in:

    data/raw/

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
- a validated acquisition corpus
- not yet a comprehensive collection

---

# 6. Acquisition Validation Status

Acquisition validation has been implemented and run successfully.

Validation script:

    scripts/validate_acquisition_manifest.py

Validation command:

    venv/bin/python scripts/validate_acquisition_manifest.py

Validation result:

- manifest records: 16
- files checked: 16
- raw PDF files found: 16
- JSON parse errors: 0
- unresolved manifest paths: 0
- missing files: 0
- hash mismatches: 0
- size mismatches: 0
- missing hash values: 0
- missing size values: 0
- orphan PDF files: 0
- duplicate manifest paths: 0
- duplicate recorded hashes: 0

Validation status:

    PASS

Validation commit:

    34b6ffa Add acquisition manifest validation script

The acquisition layer is validated against the current manifest and local raw artefact store.

---

# 7. Text Extraction Reconnaissance Status

PDF embedded-text inspection has been implemented and tested.

Inspection script:

    scripts/inspect_pdf_text.py

Purpose:

- inspect embedded text extraction from selected PDFs
- report page count
- report pages with extracted text
- report extracted character count
- detect likely reference-section markers
- optionally write extracted text for manual inspection

The script does not:

- perform OCR
- parse individual references
- write citation inventories
- write database records
- mutate source artefacts
- mutate acquisition manifests

Tested reconnaissance sample:

- 2017-cognitive-load-theory.pdf
- 2020-classroom-management-literature-review.pdf
- 2020-classroom-management-infographic.pdf

Inspection results:

2017-cognitive-load-theory.pdf:

- pages: 12
- pages with extracted text: 12
- pages without extracted text: 0
- extracted characters: 50,635
- OCR performed: no
- reference marker detected: References
- reference marker page: 9
- status: PASS

2020-classroom-management-literature-review.pdf:

- pages: 20
- pages with extracted text: 20
- pages without extracted text: 0
- extracted characters: 80,459
- OCR performed: no
- reference marker detected: References
- reference marker page: 16
- status: PASS

2020-classroom-management-infographic.pdf:

- pages: 1
- pages with extracted text: 1
- pages without extracted text: 0
- extracted characters: 2,119
- OCR performed: no
- reference marker detected: none
- status: PASS

Reconnaissance finding:

Embedded text extraction is viable for the selected CESE PDFs.

OCR is not required for the selected test artefacts.

---

# 8. Reference-Section Extraction Status

Minimum viable raw reference-section extraction has been implemented and tested.

Extraction script:

    scripts/extract_reference_section.py

Purpose:

- extract raw reference sections from formal report PDFs
- use embedded PDF text only
- detect formal reference-section markers
- preserve page-level provenance in output
- write raw reference-section text files to a working directory

Default output location:

    data/working/reference_sections/

The script does not:

- perform OCR
- parse individual references
- clean references aggressively
- write citation inventories
- write database records
- mutate source artefacts
- mutate acquisition manifests
- handle infographic footnote citations as a first-class workflow

Tested extraction sample:

- 2017-cognitive-load-theory.pdf
- 2020-classroom-management-literature-review.pdf
- 2020-classroom-management-infographic.pdf

Extraction results:

2017-cognitive-load-theory.pdf:

- pages: 12
- pages with extracted text: 12
- extracted characters: 50,635
- OCR performed: no
- reference marker: References
- reference marker page: 9
- stop marker: Centre for Education Statistics and Evaluation
- stop marker page: 12
- extracted page range: 9-11
- output file:

        data/working/reference_sections/2017-cognitive-load-theory_references.txt

- status: PASS

2020-classroom-management-literature-review.pdf:

- pages: 20
- pages with extracted text: 20
- extracted characters: 80,459
- OCR performed: no
- reference marker: References
- reference marker page: 16
- stop marker: Centre for Education Statistics and Evaluation
- stop marker page: 20
- extracted page range: 16-19
- output file:

        data/working/reference_sections/2020-classroom-management-literature-review_references.txt

- status: PASS

2020-classroom-management-infographic.pdf:

- pages: 1
- pages with extracted text: 1
- extracted characters: 2,119
- OCR performed: no
- reference marker: none detected
- status: NO_REFERENCE_SECTION
- reason: no formal references-section marker was found

Extraction conclusion:

Minimum viable embedded-text reference-section extraction has been demonstrated on selected CESE PDFs.

Formal report PDFs can have raw reference sections extracted with page-level provenance.

Infographic-style artefacts without formal reference sections are handled gracefully and deferred from the first extraction pathway.

---

# 9. Provenance Status

Implemented:

- acquisition provenance
- source URL preservation
- source filename preservation
- retrieval timestamp recording
- retrieval operator recording
- SHA-256 artefact fingerprinting
- file size recording
- acquisition script recording
- acquisition manifest validation
- page-level raw text inspection outputs
- page-level raw reference-section extraction outputs

Partially implemented:

- extraction provenance

Extraction provenance currently includes:

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

Not yet implemented:

- extraction manifests
- transformation provenance
- individual citation provenance
- analytical provenance
- canonical entity provenance

---

# 10. Current Milestone

Current milestone:

Minimum viable raw reference-section extraction demonstrated.

Success criteria achieved:

- acquisition workflow implemented
- acquisition workflow validated
- provenance metadata captured
- multiple artefacts successfully acquired
- acquisition process reproducible
- acquisition manifest validation script established
- manifest records validated against preserved raw artefacts
- SHA-256 hashes validated
- file sizes validated
- no missing files identified
- no orphan PDF files identified
- no duplicate manifest paths identified
- no duplicate recorded hashes identified
- embedded PDF text inspection implemented
- selected CESE PDFs confirmed to contain extractable embedded text
- formal reference-section markers detected in selected report PDFs
- raw reference sections extracted from selected report PDFs
- extraction output preserves page-level provenance
- non-reference-section infographic handled gracefully without false extraction

Current corpus:

- 16 CESE artefacts
- 16 acquisition records
- 0 acquisition failures
- 0 acquisition validation failures

Current extraction test outputs:

- 2 successful raw reference-section extractions
- 1 graceful no-reference-section result

---

# 11. Current Missing Components

Not yet established:

- reference-section quality inspection script
- individual reference parsing
- reference boundary detection
- citation inventory
- extraction manifest
- extraction validation workflow
- OpenAlex integration
- Crossref integration
- canonical schema
- analytical database
- publication-grade analytical outputs

These components remain intentionally deferred until raw extraction quality is better understood.

---

# 12. Confirmed Extraction Findings

Confirmed findings from current extraction reconnaissance:

- selected CESE PDFs contain embedded text
- OCR is not currently required for selected test artefacts
- formal report PDFs can contain detectable "References" markers
- reference-section extraction can stop before CESE contact/citation pages using conservative stop markers
- raw reference-section extraction is feasible for selected formal CESE reports
- infographic-style artefacts may contain citations without formal references sections
- non-reference-section artefacts should be excluded from the first formal reference-section extraction pathway

Known extraction quality issue:

- two-column and image-adjacent layouts can degrade text extraction quality
- the 2020 classroom management literature review shows degradation on page 19
- observed artefacts include split letters, split words, awkward line breaks, and compressed adjacent references
- this affects downstream individual reference parsing, not raw section extraction itself

Current implementation decision:

Minimum viable extraction will target formal reference sections in selectable-text PDFs.

OCR, infographic citation handling, footnote-only citation extraction, and aggressive text repair are deferred until standard report extraction and quality inspection are working.

---

# 13. Immediate Next Actions

Priority order:

1. Commit scripts and dependency changes, if not already committed
2. Confirm whether generated working outputs should remain untracked
3. Inspect raw extracted reference-section outputs manually
4. Create a lightweight reference-section quality inspection script
5. Use the quality inspection script on the two extracted reference-section files
6. Identify minimum viable requirements for individual reference boundary detection

Recommended next script:

    scripts/inspect_reference_section.py

Recommended purpose:

- take one extracted _references.txt file
- count page sections included
- estimate likely reference starts
- flag obvious extraction artefacts
- report whether the section appears suitable for first-pass reference parsing
- do not split references into records yet
- do not write database records

Suggested test files:

    data/working/reference_sections/2017-cognitive-load-theory_references.txt
    data/working/reference_sections/2020-classroom-management-literature-review_references.txt

The next implementation milestone should remain narrowly scoped.

The project should avoid premature expansion into:

- enrichment
- entity resolution
- large-scale acquisition
- analytical infrastructure
- advanced database design
- citation matching
- canonical entity modelling

until reference-section quality and reference boundary detection are better understood.

---

# 14. Active Risks

Current project risks:

- scope creep
- premature architecture elaboration
- premature schema design
- premature infrastructure expansion
- acquisition success creating pressure for over-expansion
- hidden complexity entering extraction workflows
- extraction workflow complexity
- text extraction artefacts affecting reference parsing
- layout-dependent PDF extraction errors
- non-standard citation-bearing artefacts being mistaken for extraction failures

Mitigation strategy:

- maintain bounded milestones
- validate each layer before adding the next
- preserve operational simplicity
- continue acquisition-before-sophistication discipline
- treat raw extraction and reference parsing as separate stages
- perform quality inspection before citation parsing
- avoid enrichment and canonicalisation until raw extraction and reference parsing are working
- handle infographics and footnote-style citations as deferred edge cases

---

# 15. Operational Notes

The project now possesses:

- governance documentation
- operational documentation
- reproducible acquisition workflows
- provenance-aware acquisition records
- acquisition manifest validation
- a validated initial CESE acquisition corpus
- embedded-text PDF inspection
- minimum viable raw reference-section extraction
- a small but functioning educational research corpus

The project does not yet possess:

- individual reference parsing
- citation inventories
- analytical workflows
- citation networks
- research-ready datasets

The acquisition layer should be considered operational and validated for the current CESE seed corpus.

The extraction layer has begun and should be considered operational only at the raw reference-section extraction level.

The immediate next task is reference-section quality inspection, not full citation parsing, metadata enrichment, or database construction.

---

# 16. Commit Tracking Notes

Confirmed commit:

    34b6ffa Add acquisition manifest validation script

Commits still to confirm or record:

- inspect_pdf_text.py, if committed
- extract_reference_section.py, if committed
- requirements.txt updates, if pypdf was added
- CURRENT_STATE.md update after this document is applied

CHAT_INDEX.md should be updated with all commits made under PM-002 coordination.

Generated files under data/working/ should generally remain reproducible working artefacts unless the project explicitly decides to version them.