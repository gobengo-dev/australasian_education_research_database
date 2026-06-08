# REFERENCE_CANDIDATE_REVIEW_RESULTS.md

Status: operational review results  
Version: v0.1  
Last updated: 2026-06-08

---

# 1. Purpose

This document records the first manual and AI-assisted review results for candidate reference outputs produced by:

    scripts/detect_reference_boundaries.py

These results support the next implementation decision:

> Which candidate reference output should be used first for minimum viable structured reference parsing?

This document does not create final citation records.

This document does not validate bibliographic accuracy.

This document does not perform DOI matching, URL checking, metadata enrichment, or citation-quality analysis.

---

# 2. Review Basis

Reviews were conducted according to:

    docs/REFERENCE_CANDIDATE_REVIEW_PROTOCOL.md

The review focus was candidate boundary quality.

The review question was:

> Does each candidate usually correspond to one source-visible reference?

The review did not assess:

- whether each reference is bibliographically correct
- whether each cited work can be matched to OpenAlex or Crossref
- whether source-visible URLs are alive
- whether source-visible DOIs are missing
- whether references are analysis-ready

Candidate outputs remain intermediate working artefacts.

---

# 3. Files Reviewed

The following candidate outputs were reviewed:

    data/working/reference_candidates/2017-cognitive-load-theory_reference_candidates.txt

    data/working/reference_candidates/2020-classroom-management-literature-review_reference_candidates.txt

    data/working/reference_candidates/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_reference_candidates.txt

    data/working/reference_candidates/revisiting-gifted-education-literature-review_reference_candidates.txt

Associated source PDFs:

    data/raw/cese/2017-cognitive-load-theory.pdf

    data/raw/cese/2020-classroom-management-literature-review.pdf

    data/raw/cese/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students.pdf

    data/raw/cese/revisiting-gifted-education-literature-review.pdf

---

# 4. Summary Classification Table

| Source document | Candidate output | Classification | Recommended use |
|---|---|---|---|
| 2017-cognitive-load-theory.pdf | 2017-cognitive-load-theory_reference_candidates.txt | SUITABLE_FOR_PARSING_EXPERIMENT | First structured parsing baseline |
| 2020-classroom-management-literature-review.pdf | 2020-classroom-management-literature-review_reference_candidates.txt | SUITABLE_WITH_KNOWN_WARNINGS | Second parsing test after baseline |
| revisiting-gifted-education-literature-review.pdf | revisiting-gifted-education-literature-review_reference_candidates.txt | SUITABLE_WITH_KNOWN_WARNINGS | Larger stress-test after baseline |
| 2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students.pdf | 2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_reference_candidates.txt | DEFERRED_STYLE_CLASS | Later APA-style boundary refinement test |

---

# 5. Review Result: 2017 Cognitive Load Theory

## 5.1 File Identity

Source PDF:

    data/raw/cese/2017-cognitive-load-theory.pdf

Reference-section file:

    data/working/reference_sections/2017-cognitive-load-theory_references.txt

Candidate output file:

    data/working/reference_candidates/2017-cognitive-load-theory_reference_candidates.txt

Review date:

    2026-06-08

Reviewer:

    AI-assisted review

## 5.2 Console Summary

- Page sections: 3
- Candidate references: 94
- High confidence: 81
- Medium confidence: 13
- Low confidence: 0
- URLs detected: 3
- DOIs detected: 0
- Script status: CANDIDATES_WITH_TEXT_DAMAGE

## 5.3 Boundary Review

First references:

- The first candidates begin with real references.
- The reference-section heading is not included as a candidate.
- Early references appear correctly separated.

Last references:

- The final candidates are real references.
- CESE contact and publication material is excluded.
- Final references appear correctly separated.

Known difficult zones:

- Embedded split examples around adjacent references appear correctly handled.
- The parenthesised-year variant near the end of the section is handled acceptably.

Obvious false splits:

- None requiring correction were identified during review.

Obvious merged references:

- None identified during review.

Heading/footer contamination:

- None identified.

URL/DOI preservation:

- URLs appear preserved.
- No DOIs were detected.

Text damage affecting boundaries:

- Some text-damage flags remain.
- Visible text-damage examples do not appear to compromise reference boundaries.

## 5.4 Style Class

- Older CESE author-date references
- Formal reference section
- Manageable reference count
- Limited URL presence
- One observed parenthesised-year variant

## 5.5 Classification

    SUITABLE_FOR_PARSING_EXPERIMENT

## 5.6 Decision

Use as the first structured parsing experiment.

## 5.7 Notes

This is the strongest current baseline for minimum viable structured parsing.

It should be used before attempting larger, noisier, or stylistically different candidate outputs.

---

# 6. Review Result: 2020 Classroom Management Literature Review

## 6.1 File Identity

Source PDF:

    data/raw/cese/2020-classroom-management-literature-review.pdf

Reference-section file:

    data/working/reference_sections/2020-classroom-management-literature-review_references.txt

Candidate output file:

    data/working/reference_candidates/2020-classroom-management-literature-review_reference_candidates.txt

Review date:

    2026-06-08

Reviewer:

    AI-assisted review

## 6.2 Console Summary

- Page sections: 4
- Candidate references: 99
- High confidence: 54
- Medium confidence: 45
- Low confidence: 0
- URLs detected: 1
- DOIs detected: 0
- Script status: CANDIDATES_WITH_TEXT_DAMAGE

## 6.3 Boundary Review

First references:

- The first candidates begin with real references.
- The reference-section heading is not included as a candidate.
- Early references appear generally correct.

Last references:

- The final candidates correspond to real references.
- The final reference list ends before CESE contact/publication material.
- Text quality is degraded near the end, but boundaries remain mostly usable.

Known difficult zones:

- Page 19 contains substantial text extraction damage.
- Several page 19 references contain split letters or internal spacing artefacts.

Obvious false splits:

- One confirmed publisher-tail false split:

        Goss, P, Sonnemann, J & Griffiths, K 2017, Engaging students: Creating classrooms that improve learning.
        Grattan Institute.

  These should be one reference.

Obvious merged references:

- No major recurring merged-reference pattern identified during review.

Heading/footer contamination:

- No major heading/footer or publication-note contamination identified.

URL/DOI preservation:

- The visible URL-bearing CASEL reference is preserved.
- No DOIs were detected.

Text damage affecting boundaries:

- Page 19 contains numerous extraction artefacts.
- Examples include split words and damaged author names such as:

        S hin
        S imonsen
        S kiba
        S now
        W oolfolk Hoy

- These affect downstream parsing quality, but most reference boundaries remain usable.

## 6.4 Style Class

- Older CESE author-date references
- Formal reference section
- Organisation-authored references present
- One URL-bearing reference
- Page-level text damage near end of reference section

## 6.5 Classification

    SUITABLE_WITH_KNOWN_WARNINGS

## 6.6 Decision

Use after the 2017 cognitive load baseline as a second structured parsing test.

Proceed only with explicit warnings.

## 6.7 Notes

This file is useful because it is more challenging than the 2017 cognitive load file but still mostly within the same older CESE author-date style class.

It should not be used as the first parser baseline.

Known issues should be preserved in parser test notes.

---

# 7. Review Result: Revisiting Gifted Education Literature Review

## 7.1 File Identity

Source PDF:

    data/raw/cese/revisiting-gifted-education-literature-review.pdf

Reference-section file:

    data/working/reference_sections/revisiting-gifted-education-literature-review_references.txt

Candidate output file:

    data/working/reference_candidates/revisiting-gifted-education-literature-review_reference_candidates.txt

Review date:

    2026-06-08

Reviewer:

    AI-assisted review

## 7.2 Console Summary

- Page sections: 12
- Candidate references: 372
- High confidence: 269
- Medium confidence: 103
- Low confidence: 0
- URLs detected: 1
- DOIs detected: 0
- Script status: CANDIDATES_WITH_TEXT_DAMAGE

## 7.3 Boundary Review

First references:

- The first candidates begin with real references.
- The numbered heading "7. References" is not included as a candidate.
- Early references appear correctly separated.

Last references:

- The final candidates correspond to real references.
- CESE publication/contact material is excluded.
- Final references appear usable.

Known difficult zones:

- The statutory reference "Education Act 1990 (NSW)." is correctly treated as its own candidate.
- Organisation-heavy references are mostly handled.
- URL-bearing reference area contains a boundary issue.

Obvious false splits:

- One confirmed publisher/institution-tail false split:

        Callahan, C & McIntire, J 1994 ...
        Department of Education, Washington, DC.

  These should be one reference.

Obvious merged references:

- One confirmed merged reference around the URL-bearing NSW Department of Education reference.
- The NSW Department of Education 2018 URL reference is merged with the following O'Boyle et al. 2005 reference.

Heading/footer contamination:

- No major heading/footer contamination identified.
- The numbered reference-section heading is successfully removed.

URL/DOI preservation:

- The visible URL appears preserved.
- The URL-bearing candidate has a boundary issue because the following reference is absorbed.
- No DOIs were detected.

Text damage affecting boundaries:

- Text-damage flags are common.
- Most appear to be warning signals rather than catastrophic boundary failures.

## 7.4 Style Class

- Older CESE author-date references
- Long formal reference section
- Organisation-heavy references
- Legal/statutory reference present
- URL-bearing reference present
- Large candidate set

## 7.5 Classification

    SUITABLE_WITH_KNOWN_WARNINGS

## 7.6 Decision

Use as a larger stress-test after the first baseline parser experiment.

Do not use as the first structured parsing baseline.

## 7.7 Notes

This file is valuable because it tests scale and variety.

It should be used after the parser can handle the smaller and cleaner 2017 cognitive load reference output.

Known boundary problems should be retained as test examples for later refinement.

---

# 8. Review Result: 2015 Tutoring Interventions in Mathematics

## 8.1 File Identity

Source PDF:

    data/raw/cese/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students.pdf

Reference-section file:

    data/working/reference_sections/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_references.txt

Candidate output file:

    data/working/reference_candidates/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_reference_candidates.txt

Review date:

    2026-06-08

Reviewer:

    AI-assisted review

## 8.2 Console Summary

- Page sections: 2
- Candidate references: 68
- High confidence: 13
- Medium confidence: 55
- Low confidence: 0
- URLs detected: 10
- DOIs detected: 0
- Script status: CANDIDATES_WITH_TEXT_DAMAGE

## 8.3 Boundary Review

First references:

- The first reference is split incorrectly.
- The ACARA reference is split into an author/year fragment and a title/URL fragment.
- The second fragment also absorbs the following Baker et al. reference.

Early APA-style initials:

- Author initials are repeatedly treated as embedded boundaries.
- Example:

        Britz, M.
        W., Dixon, J., & McLaughlin, T. F. (1989) ...

  These should be one reference.

Last references:

- The final Won Jun reference is correctly isolated.
- However, preceding references contain major false splits and merges.

Known difficult zones:

- APA-style initials are a systematic failure mode.
- URL-bearing references are frequently merged with following references.
- Page transition introduces contamination.

Obvious false splits:

- Severe and recurring.
- Examples include references beginning with:

        Cohen
        Cook
        Ginsburg-Block
        Greenwood
        Lauer
        Leung
        Robinson
        Ritter
        Topping

  These are split across author initials.

Obvious merged references:

- Severe and recurring.
- Examples include:

        Cook et al. merged with Deke et al.
        Springer merged with multiple Thomson references and Tian
        University of Chicago 2013 merged with University of Chicago 2014
        U.S. Department of Education merged with Wasik

Heading/footer contamination:

- Page transition material is absorbed into one candidate.
- Example contamination includes CESE page header/footer material around page 11.

URL/DOI preservation:

- URLs are generally preserved.
- URL-bearing entries are a major source of boundary failure.
- No DOIs were detected.

Text damage affecting boundaries:

- Some text damage is present.
- The dominant problem is not simple extraction damage but mismatch between current embedded-boundary logic and APA-style punctuation.

## 8.4 Style Class

- APA-style references
- Parenthesised years
- Heavy author initials
- Multiple URL-bearing references
- Page transition contamination

## 8.5 Classification

    DEFERRED_STYLE_CLASS

## 8.6 Decision

Do not use for the first structured parsing experiment.

Defer until APA-style boundary handling is addressed separately.

## 8.7 Notes

This file is useful as a diagnostic case.

It demonstrates that the current boundary detector works better for older CESE author-date references than for APA-style reference lists.

This is not a raw reference-section extraction failure.

It is a style-class boundary-detection issue.

---

# 9. Cross-File Findings

## 9.1 Current Strengths

The current workflow performs well when:

- the PDF has selectable embedded text
- the document has a formal reference section
- the reference section uses older CESE author-date style
- references mostly end in predictable terminal punctuation
- author-year starts are visible at line or embedded-boundary positions
- reference-section headings are plain or numbered
- footer/contact material is separated by a detectable stop marker

## 9.2 Current Weaknesses

The current workflow is not yet reliable when:

- references use APA-style author initials with many full stops
- URL-bearing references are followed immediately by another reference
- PDF extraction collapses adjacent references without clean line breaks
- page transition headers/footers are absorbed into extracted reference text
- publisher or institution tails look like new organisation-authored references

## 9.3 Known Boundary Issue Classes

Known issue classes:

- publisher or institution tails split into separate candidates
- APA author initials split into separate candidates
- URL-bearing references merged with following references
- text damage from PDF extraction affecting downstream parsing
- page transition contamination
- footnote-only citation formats outside current workflow
- infographic/source-note citation formats outside current workflow

---

# 10. Current Parser Input Decision

The first structured parsing experiment should use:

    data/working/reference_candidates/2017-cognitive-load-theory_reference_candidates.txt

Rationale:

- strongest reviewed boundary quality
- manageable candidate count
- formal reference section
- no low-confidence candidates
- no major heading/footer contamination
- no obvious recurring false-split or merged-reference pattern
- suitable older CESE author-date style
- some URLs present, but not enough to dominate the test

The second structured parsing test should use:

    data/working/reference_candidates/2020-classroom-management-literature-review_reference_candidates.txt

Rationale:

- same broad style class as the first baseline
- more challenging text quality
- known publisher-tail false split
- useful for testing warning propagation

A later larger stress test should use:

    data/working/reference_candidates/revisiting-gifted-education-literature-review_reference_candidates.txt

Rationale:

- long formal reference section
- large candidate count
- legal/statutory reference present
- organisation-heavy references
- useful scale test

The following file should be deferred:

    data/working/reference_candidates/2015-effectiveness-of-tutoring-interventions-in-mathematics-for-disadvantaged-students_reference_candidates.txt

Rationale:

- APA-style reference format is not currently handled reliably
- over-splitting is systematic
- merged references are frequent
- this should be treated as a later style-class refinement case

---

# 11. Next Implementation Step

Recommended next implementation step:

Create a minimum viable structured parser for the 2017 cognitive load candidate output only.

The parser should remain conservative.

It should not:

- write database records
- perform metadata enrichment
- perform DOI matching
- check URLs
- infer canonical works
- repair citation text aggressively
- attempt to support all reference styles

The parser may extract conservative fields such as:

- candidate_id
- source candidate file
- source pages
- raw reference text
- boundary confidence
- first author or organisation string
- detected year
- title-like segment, if safely detectable
- source-visible URL flag
- source-visible DOI flag
- parse status
- parse notes

The parser should preserve raw reference text unchanged.

The parser should treat uncertainty explicitly.

---

# 12. Status

Current status:

- Candidate reference outputs have been reviewed.
- The first parser input has been selected.
- APA-style parsing is deferred.
- Known boundary risks have been identified.
- The project is ready to begin a minimum viable structured parsing experiment, provided current documentation is committed first.