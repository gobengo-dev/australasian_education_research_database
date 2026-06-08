# CURRENT_STATE.md

Status: Active  
Last updated: 2026-06-08

---

# 1. Project Status

The Australasian Educational Research project is in active implementation.

Governance, operational scaffolding, repository structure, initial acquisition workflows, acquisition validation workflows, minimum viable reference-section extraction workflows, reference-section inspection, draft reference-boundary detection, and reference-candidate review have been established.

The project has successfully transitioned from planning and governance establishment into operational execution.

The project now possesses:

- a validated initial CESE acquisition corpus
- a repeatable acquisition validation script
- a PDF embedded-text inspection script
- a minimum viable raw reference-section extraction script
- a reference-section inspection script
- a draft reference-boundary detection script
- a manual and AI-assisted reference-candidate review protocol
- reviewed candidate-reference boundary outputs for four selected CESE reports
- a selected first input for minimum viable structured reference parsing
- successful extraction tests on selected CESE reports
- successful candidate-reference boundary detection on selected formal CESE reference sections

The project does not yet possess:

- structured individual reference parsing
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
- Reference-section quality inspection
- Draft candidate reference-boundary detection
- Manual and AI-assisted candidate-reference review
- Preparation for minimum viable structured reference parsing

Current objective:

Begin a minimum viable structured reference parsing experiment using the reviewed 2017 cognitive load candidate-reference output as the first parser baseline.

The project is not yet focused on:

- citation analysis
- metadata enrichment
- entity resolution
- analytical database construction
- canonicalisation
- publication-grade analytical outputs

The extraction layer has begun, but only at the raw reference-section and candidate-boundary level.

Structured individual reference parsing has not yet been implemented.

The next implementation step should remain narrow:

- parse reviewed candidate references conservatively
- preserve raw reference text unchanged
- extract only low-risk fields
- record uncertainty explicitly
- avoid enrichment, matching, URL checking, and database writes

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
- ASCII-safe filenames
- verb_object.py naming convention where practical
- one primary responsibility per script
- Git used for version control rather than filename versioning
- scripts should be conservative, inspectable, and reproducible

Temporary draft script filenames used during exploratory work should not be committed.

Generated files under data/working/ should generally remain reproducible working artefacts unless the project explicitly decides to version them.

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
- support plain and numbered reference-section headings
- optionally write extracted text for manual inspection

The script does not:

- perform OCR
- parse individual references
- write citation inventories
- write database records
- mutate source artefacts
- mutate acquisition manifests

Tested reconnaissance sample includes:

- 2017-cognitive-load-theory.pdf
- 2020-classroom-management-literature-review.pdf
- 2020-classroom-management-infographic.pdf
- 2014-school-improvement-frameworks-the-evidence-base.pdf
- 2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students.pdf
- revisiting-gifted-education-literature-review.pdf

Key inspection results:

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

2014-school-improvement-frameworks-the-evidence-base.pdf:

- pages: 23
- pages with extracted text: 23
- pages without extracted text: 0
- extracted characters: 78,993
- OCR performed: no
- reference marker detected: none
- status: PASS
- finding: document appears to use page-level footnote references rather than a consolidated formal reference section

2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students.pdf:

- pages: 12
- pages with extracted text: 12
- pages without extracted text: 0
- extracted characters: 38,534
- OCR performed: no
- reference marker detected: References
- reference marker page: 10
- status: PASS
- finding: formal reference section uses APA-style parenthesised-year references

revisiting-gifted-education-literature-review.pdf:

- pages: 32
- pages with extracted text: 32
- pages without extracted text: 0
- extracted characters: 143,803
- OCR performed: no
- reference marker detected: 7. References
- reference marker page: 20
- status: PASS
- finding: numbered reference-section heading now detected correctly

Reconnaissance finding:

Embedded text extraction is viable for selected CESE PDFs.

OCR is not required for the selected test artefacts.

However, CESE citation and reference formats vary across report types and publication years.

---

# 8. Reference-Section Extraction Status

Minimum viable raw reference-section extraction has been implemented and tested.

Extraction script:

    scripts/extract_reference_section.py

Purpose:

- extract raw reference sections from formal report PDFs
- use embedded PDF text only
- detect formal reference-section markers
- support plain and numbered reference-section headings
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
- handle page-level footnote references as a first-class workflow

Tested extraction sample includes:

- 2017-cognitive-load-theory.pdf
- 2020-classroom-management-literature-review.pdf
- 2020-classroom-management-infographic.pdf
- 2014-school-improvement-frameworks-the-evidence-base.pdf
- 2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students.pdf
- revisiting-gifted-education-literature-review.pdf

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

2014-school-improvement-frameworks-the-evidence-base.pdf:

- pages: 23
- pages with extracted text: 23
- extracted characters: 78,993
- OCR performed: no
- reference marker: none detected
- status: NO_REFERENCE_SECTION
- reason: no formal references-section marker was found
- interpretation: document appears to use page-level footnote references

2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students.pdf:

- pages: 12
- pages with extracted text: 12
- extracted characters: 38,534
- OCR performed: no
- reference marker: References
- reference marker page: 10
- stop marker: Centre for Education Statistics and Evaluation
- stop marker page: 12
- extracted page range: 10-11
- output file:

        data/working/reference_sections/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_references.txt

- status: PASS

revisiting-gifted-education-literature-review.pdf:

- pages: 32
- pages with extracted text: 32
- extracted characters: 143,803
- OCR performed: no
- reference marker: 7. References
- reference marker page: 20
- stop marker: Please cite this publication as:
- stop marker page: 32
- extracted page range: 20-31
- output file:

        data/working/reference_sections/revisiting-gifted-education-literature-review_references.txt

- status: PASS

Extraction conclusion:

Minimum viable embedded-text reference-section extraction has been demonstrated on selected CESE PDFs.

Formal report PDFs can have raw reference sections extracted with page-level provenance.

Infographic-style artefacts and footnote-style reports without formal reference sections are handled gracefully and deferred from the first extraction pathway.

---

# 9. Reference-Section Inspection Status

Reference-section inspection has been implemented.

Inspection script:

    scripts/inspect_reference_section.py

Purpose:

- inspect one extracted _references.txt file
- count page sections
- count characters and lines inspected
- estimate likely reference starts
- detect URLs and DOIs
- flag simple extraction artefacts
- provide page-level summary
- provide a coarse interpretation of whether the section appears parse-ready

The script does not:

- parse references into structured fields
- create citation inventories
- write database records
- perform DOI matching
- perform URL checking
- mutate source files

Tested files include:

    data/working/reference_sections/2017-cognitive-load-theory_references.txt
    data/working/reference_sections/2020-classroom-management-literature-review_references.txt
    data/working/reference_sections/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_references.txt
    data/working/reference_sections/revisiting-gifted-education-literature-review_references.txt

Findings:

2017-cognitive-load-theory_references.txt:

- page sections: 3
- likely reference starts: 88
- URLs detected: 3
- DOIs detected: 0
- status: USABLE_WITH_LAYOUT_ARTEFACTS

2020-classroom-management-literature-review_references.txt:

- page sections: 4
- likely reference starts: 87
- URLs detected: 1
- DOIs detected: 0
- status: USABLE_WITH_LAYOUT_ARTEFACTS

2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_references.txt:

- page sections: 2
- likely reference starts: 0
- URLs detected: 10
- DOIs detected: 0
- status: REVIEW_REQUIRED
- interpretation: current inspection heuristic does not recognise APA-style starts well enough

revisiting-gifted-education-literature-review_references.txt:

- page sections: 12
- likely reference starts: 367
- URLs detected: 1
- DOIs detected: 0
- status: LIKELY_PARSE_READY
- interpretation: useful coarse signal, but detailed candidate output review remains necessary

Inspection conclusion:

Reference-section inspection is useful as a coarse preflight check.

It does not replace review of candidate boundary outputs.

Its current likely-start heuristic is stronger for older CESE author-date references than for APA-style references.

---

# 10. Reference-Boundary Detection Status

Draft reference-boundary detection has been implemented.

Boundary detection script:

    scripts/detect_reference_boundaries.py

Purpose:

- take one extracted _references.txt file
- remove reference-section heading lines
- identify candidate individual references
- preserve raw candidate text as much as possible
- preserve page-level source information
- flag confidence and possible extraction artefacts
- optionally write text and JSONL candidate outputs

Default output location:

    data/working/reference_candidates/

The script does not:

- parse references into structured citation fields
- create citation inventories
- write database records
- perform DOI matching
- perform URL checking
- perform metadata enrichment
- mutate source reference-section files
- repair damaged source text aggressively

Implemented boundary logic currently supports:

- older CESE author-date references with unparenthesised years
- later CESE-like references with parenthesised years
- some organisation-authored references
- some statutory/title-style references
- embedded boundary splitting where extracted text collapses adjacent references
- numbered reference-section headings filtered before boundary detection

Tested files include:

    data/working/reference_sections/2017-cognitive-load-theory_references.txt
    data/working/reference_sections/2020-classroom-management-literature-review_references.txt
    data/working/reference_sections/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_references.txt
    data/working/reference_sections/revisiting-gifted-education-literature-review_references.txt

Current test results:

2017-cognitive-load-theory_references.txt:

- page sections: 3
- non-empty content lines: 291
- line-based candidate groups: 92
- candidate references after embedded splitting: 94
- high confidence: 81
- medium confidence: 13
- low confidence: 0
- URLs detected: 3
- DOIs detected: 0
- status: CANDIDATES_WITH_TEXT_DAMAGE
- interpretation: candidate count and boundaries appear broadly successful for this test case

2020-classroom-management-literature-review_references.txt:

- page sections: 4
- non-empty content lines: 375
- line-based candidate groups: 82
- candidate references after embedded splitting: 99
- high confidence: 54
- medium confidence: 45
- low confidence: 0
- URLs detected: 1
- DOIs detected: 0
- status: CANDIDATES_WITH_TEXT_DAMAGE
- interpretation: broadly successful, but known false split remains around publisher/institution tails

2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_references.txt:

- page sections: 2
- non-empty content lines: 175
- line-based candidate groups: 28
- candidate references after embedded splitting: 68
- high confidence: 13
- medium confidence: 55
- low confidence: 0
- URLs detected: 10
- DOIs detected: 0
- status: CANDIDATES_WITH_TEXT_DAMAGE
- interpretation: exposes APA-style over-splitting around author initials; not yet reliable for this style class

revisiting-gifted-education-literature-review_references.txt:

- page sections: 12
- non-empty content lines: 1267
- line-based candidate groups: 341
- candidate references after embedded splitting: 372
- high confidence: 269
- medium confidence: 103
- low confidence: 0
- URLs detected: 1
- DOIs detected: 0
- status: CANDIDATES_WITH_TEXT_DAMAGE
- interpretation: broadly successful on long older-style formal CESE reference section; statutory reference “Education Act 1990 (NSW).” handled correctly; publisher/institution-tail false split remains a known issue

Boundary detection conclusion:

Draft boundary detection is viable for selected formal CESE reference sections, especially older CESE author-date formats.

The output should be treated as candidate reference boundaries, not final parsed citation records.

The script is not yet reliable for APA-style references with author initials.

Known recurring false split class:

- publisher or institution tails can be mistaken for separate references after internal punctuation

Known style classes requiring separate handling:

- APA-style parenthesised-year references with initials
- page-level footnote references
- infographic-style citation notes

---

# 11. Reference-Candidate Review Status

A manual and AI-assisted review protocol has been drafted.

Review protocol document:

    docs/REFERENCE_CANDIDATE_REVIEW_PROTOCOL.md

Review results document:

    docs/REFERENCE_CANDIDATE_REVIEW_RESULTS.md

Purpose:

- assess candidate reference boundary quality
- decide whether candidate outputs are suitable for structured parsing experiments
- identify known boundary failure classes
- avoid relying on chat history for review decisions
- prevent premature movement into parsing, enrichment, or database design

The review protocol does not:

- validate bibliographic accuracy
- parse references
- match works
- check URLs
- discover DOIs
- create citation inventories

Reviewed candidate outputs:

    data/working/reference_candidates/2017-cognitive-load-theory_reference_candidates.txt

    data/working/reference_candidates/2020-classroom-management-literature-review_reference_candidates.txt

    data/working/reference_candidates/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_reference_candidates.txt

    data/working/reference_candidates/revisiting-gifted-education-literature-review_reference_candidates.txt

Review classifications:

2017-cognitive-load-theory_reference_candidates.txt:

- classification: SUITABLE_FOR_PARSING_EXPERIMENT
- recommended use: first structured parsing baseline
- reason: strongest reviewed boundary quality; manageable count; no major unresolved boundary failures

2020-classroom-management-literature-review_reference_candidates.txt:

- classification: SUITABLE_WITH_KNOWN_WARNINGS
- recommended use: second parsing test after baseline
- reason: mostly usable older CESE author-date style, with known publisher-tail false split and page-19 text damage

revisiting-gifted-education-literature-review_reference_candidates.txt:

- classification: SUITABLE_WITH_KNOWN_WARNINGS
- recommended use: larger stress-test after baseline
- reason: large formal reference section; statutory reference handled; known publisher/institution-tail and URL-boundary warnings

2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_reference_candidates.txt:

- classification: DEFERRED_STYLE_CLASS
- recommended use: later APA-style boundary refinement test
- reason: systematic over-splitting around APA-style initials and recurring merged URL-bearing references

Review conclusion:

The first structured parsing experiment should use:

    data/working/reference_candidates/2017-cognitive-load-theory_reference_candidates.txt

or, preferably, the paired JSONL output if available:

    data/working/reference_candidates/2017-cognitive-load-theory_reference_candidates.jsonl

The 2015 tutoring candidate output should not be used for the first parser experiment.

---

# 12. Provenance Status

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
- candidate reference-boundary outputs with confidence and review flags
- manual and AI-assisted review protocol for candidate reference outputs
- documented review classifications for current candidate outputs

Partially implemented:

- extraction provenance
- boundary detection provenance
- reference-candidate review provenance

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

Candidate boundary outputs currently include:

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

Reference-candidate review records currently include:

- source PDF
- reference-section file
- candidate output file
- review date
- reviewer
- console summary
- manual checks
- style class
- classification
- decision
- notes

Not yet implemented:

- extraction manifests
- transformation provenance
- structured individual citation provenance
- analytical provenance
- canonical entity provenance

---

# 13. Current Milestone

Current milestone:

Minimum viable formal reference-section extraction, draft candidate boundary detection, and first candidate-output review cycle completed.

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
- numbered reference-section markers detected
- raw reference sections extracted from selected report PDFs
- extraction output preserves page-level provenance
- non-reference-section infographic handled gracefully without false extraction
- footnote-style report recognised as outside the formal reference-section pathway
- reference-section inspection implemented
- draft reference-boundary detection implemented
- candidate reference outputs generated for selected formal reference sections
- long formal CESE reference section processed successfully into candidate references
- statutory reference example handled successfully as a candidate reference
- manual and AI-assisted reference-candidate review protocol drafted
- four candidate outputs reviewed
- first structured parsing input selected

Current corpus:

- 16 CESE artefacts
- 16 acquisition records
- 0 acquisition failures
- 0 acquisition validation failures

Current extraction test outputs:

- 4 successful raw reference-section extractions
- 1 graceful no-reference-section infographic result
- 1 graceful no-reference-section footnote-style report result

Current candidate-boundary test outputs:

- 4 candidate reference output pairs generated
- older CESE author-date examples broadly successful
- APA-style example not yet reliable

Current candidate review outputs:

- 1 candidate output classified as SUITABLE_FOR_PARSING_EXPERIMENT
- 2 candidate outputs classified as SUITABLE_WITH_KNOWN_WARNINGS
- 1 candidate output classified as DEFERRED_STYLE_CLASS

---

# 14. Current Missing Components

Not yet established:

- structured individual reference parsing
- parser output format
- citation inventory
- extraction manifest
- structured parsing validation workflow
- robust APA-style boundary detection
- footnote-reference extraction workflow
- infographic citation extraction workflow
- OpenAlex integration
- Crossref integration
- canonical schema
- analytical database
- publication-grade analytical outputs

Partially resolved:

- candidate-boundary review threshold for first structured parsing experiment
- first parser input selection

These components remain intentionally deferred until minimum viable structured parsing produces concrete examples.

---

# 15. Confirmed Extraction and Review Findings

Confirmed findings from current extraction reconnaissance:

- selected CESE PDFs contain embedded text
- OCR is not currently required for selected test artefacts
- formal report PDFs can contain detectable "References" markers
- some formal reports use numbered reference headings such as "7. References"
- reference-section extraction can stop before CESE contact/citation pages using conservative stop markers
- raw reference-section extraction is feasible for selected formal CESE reports
- long formal reference sections can be extracted and processed into candidate references
- older CESE author-date reference sections are broadly viable for draft candidate-boundary detection
- APA-style reference sections require separate refinement
- infographic-style artefacts may contain citations without formal reference sections
- some older CESE reports use page-level footnote references rather than consolidated reference sections
- non-reference-section artefacts should be excluded from the first formal reference-section extraction pathway

Confirmed findings from candidate review:

- 2017 cognitive load candidate output is suitable for the first structured parsing experiment
- 2020 classroom management candidate output is suitable with warnings
- revisiting gifted education candidate output is suitable with warnings
- 2015 tutoring interventions candidate output should be deferred as an APA-style boundary-detection case
- candidate outputs are not final citation records
- candidate review should remain separate from bibliographic validation

Known extraction and boundary-detection quality issues:

- two-column and image-adjacent layouts can degrade text extraction quality
- the 2020 classroom management literature review shows degradation on page 19
- observed artefacts include split letters, split words, awkward line breaks, and compressed adjacent references
- publisher or institution tails may be incorrectly split into separate candidate references
- APA-style initials may be incorrectly split into separate candidate references
- URL-bearing references may absorb following references
- page transition material can contaminate candidate output
- candidate references are not yet structured parsed citation records

Current implementation decision:

Minimum viable extraction will target formal reference sections in selectable-text PDFs.

Candidate boundary detection will remain explicitly draft.

Structured parsing will begin with the 2017 cognitive load candidate output only.

OCR, infographic citation handling, footnote-only citation extraction, APA-style boundary refinement, aggressive text repair, enrichment, and citation-quality analysis are deferred.

---

# 16. Immediate Next Actions

Priority order:

1. Save updated canonical review documents.
2. Save updated ACTIVE_ISSUES.md.
3. Save updated CURRENT_STATE.md.
4. Check Git status.
5. Stage review documentation and updated state documents.
6. Commit review documentation and state updates.
7. Update CHAT_INDEX.md with the resulting commit hash.
8. Commit CHAT_INDEX.md update.
9. Push commits.
10. Begin minimum viable structured parser design for the 2017 cognitive load candidate output only.

Current document files expected to be committed:

    docs/REFERENCE_CANDIDATE_REVIEW_PROTOCOL.md
    docs/REFERENCE_CANDIDATE_REVIEW_RESULTS.md
    docs/ACTIVE_ISSUES.md
    docs/CURRENT_STATE.md

CHAT_INDEX.md should be updated after the implementation/documentation commit hash exists.

Recommended next implementation milestone after commit closure:

Minimum viable structured reference parsing using:

    data/working/reference_candidates/2017-cognitive-load-theory_reference_candidates.jsonl

or, if needed:

    data/working/reference_candidates/2017-cognitive-load-theory_reference_candidates.txt

The next implementation milestone should remain narrowly scoped.

The project should avoid premature expansion into:

- enrichment
- entity resolution
- large-scale acquisition
- analytical infrastructure
- advanced database design
- citation matching
- canonical entity modelling
- DOI discovery
- URL checking

until structured reference parsing is working.

---

# 17. Active Risks

Current project risks:

- scope creep
- premature architecture elaboration
- premature schema design
- premature infrastructure expansion
- acquisition success creating pressure for over-expansion
- extraction success creating pressure for premature enrichment
- parser implementation expanding into full citation infrastructure
- hidden complexity entering extraction and parsing workflows
- extraction workflow complexity
- text extraction artefacts affecting reference parsing
- layout-dependent PDF extraction errors
- candidate boundary errors being mistaken for final citation records
- review classifications being mistaken for bibliographic validation
- non-standard citation-bearing artefacts being mistaken for extraction failures
- excessive reliance on chat history instead of canonical documents

Mitigation strategy:

- maintain bounded milestones
- validate each layer before adding the next
- preserve operational simplicity
- continue acquisition-before-sophistication discipline
- treat raw extraction, candidate boundary detection, candidate review, structured parsing, enrichment, and analysis as separate stages
- perform candidate review before structured citation parsing
- use 2017 cognitive load as the first parser baseline
- avoid enrichment and canonicalisation until raw extraction and reference parsing are working
- handle infographics, footnote-style citations, APA-style references, and publisher-tail false splits as separate work classes
- clean working tree before committing
- update canonical documents before retiring or handing over chat responsibility

---

# 18. Operational Notes

The project now possesses:

- governance documentation
- operational documentation
- reproducible acquisition workflows
- provenance-aware acquisition records
- acquisition manifest validation
- a validated initial CESE acquisition corpus
- embedded-text PDF inspection
- minimum viable raw reference-section extraction
- reference-section inspection
- draft candidate reference-boundary detection
- reference-candidate review protocol
- reference-candidate review results
- a selected first structured parsing input
- a small but functioning educational research corpus

The project does not yet possess:

- structured individual reference parsing
- citation inventories
- analytical workflows
- citation networks
- research-ready datasets

The acquisition layer should be considered operational and validated for the current CESE seed corpus.

The extraction layer should be considered operational only for:

- embedded-text inspection
- formal reference-section extraction
- coarse reference-section inspection
- draft candidate reference-boundary detection for selected formal CESE reference sections
- candidate-output review for selected outputs

The extraction layer should not yet be considered operational for:

- APA-style reference parsing
- footnote-style reference extraction
- infographic citation extraction
- structured citation inventories
- citation-quality analysis

The immediate next task is commit closure for the review documentation and state updates.

The next implementation task after commit closure is minimum viable structured reference parsing.

---

# 19. Commit Tracking Notes

Confirmed commits already recorded or known:

    34b6ffa Add acquisition manifest validation script
    c0e5c28 Add PDF text inspection script
    8850670 Add reference section extraction script
    0c9c07e Update project state and gitignore
    e7f8126 Update chat index commit register
    545d1e9 Update active issues for citation quality requirements
    c630aad Add reference inspection and boundary detection workflows
    cadd9bd Update chat index commit register

Commits still to make or confirm:

- REFERENCE_CANDIDATE_REVIEW_PROTOCOL.md
- REFERENCE_CANDIDATE_REVIEW_RESULTS.md
- ACTIVE_ISSUES.md update
- CURRENT_STATE.md update
- CHAT_INDEX.md update after commit hash exists

CHAT_INDEX.md should be updated with all commits made under PM-002 coordination.

Generated files under data/working/ should generally remain reproducible working artefacts unless the project explicitly decides to version them.