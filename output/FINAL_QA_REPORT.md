# Final IEEE Survey QA Report

Audit date: 2026-08-29

## Deliverables

- `Artificial_Intelligence_in_Multiple_Sclerosis_MRI_Survey_IEEE.docx`
- `Artificial_Intelligence_in_Multiple_Sclerosis_MRI_Survey_IEEE.pdf`
- Eleven independent vector-PDF/600-dpi-PNG figure pairs under `figures_ieee/`
- `FIGURE_CONTENT_AUDIT.md`, `FIGURE_VECTOR_AUDIT.md`, `EVIDENCE_LEDGER.md`, `REFERENCE_VERIFICATION.md`, and `IEEE_BUILD_AUDIT.json`

## Manuscript and evidence checks

- Abstract: 219 words under the build counter.
- Main text: 6,998 words from Introduction through Conclusion after removing citation tokens and placement markers.
- Required six-part framework is present in both formats.
- Figures: 11; tables: 6; native Word equations: 3.
- References: 147 entries, all actually cited; no undefined citation, duplicate DOI, placeholder citation, or uncited bibliography entry in the generated manuscript.
- Performance claims are conditioned on dataset/cohort, case condition, metric, and validation level in the evidence ledger. Heterogeneous datasets are not directly ranked.
- Figure 10 is an evaluation-logic plate with no data curves or pseudo-results.

## LaTeX PDF checks

- Compiled with `latexmk -pdf -halt-on-error -file-line-error` from the provided IEEE LaTeX template.
- 25 US-Letter pages; no undefined references/citations, missing figures, overfull boxes, blank page, or clipped content.
- All fonts are embedded/subset. Figure labels remain vector text; only intentional synthetic imaging subjects are raster.
- Fig. 11 and Table VI precede Conclusion and References. References run continuously through `[147]`.
- Every page was rendered and inspected at normal scale; architecture and evidence pages were also inspected at enlarged scale.

## Word checks

- DOCX ZIP integrity and key XML parts passed `unzip -t` and `xmllint` parsing.
- Microsoft Word opened the final DOCX and exported a native QA PDF without repair prompts.
- Native Word rendering contains 27 US-Letter pages with continuous numbering, no blank page, cropped artwork, overlapping text, missing caption, or near-empty terminal page.
- Long tables retain non-splittable rows; when Table VI continues, its header row repeats on the next page.
- The document inherits the supplied IEEE Word template, uses a 0.5-in column gap, native OMML equations, alt text, bookmarks/REF fields, and PAGE fields.

## Cross-format checks

- Word and LaTeX are generated from the same manuscript, figure-caption/alt-text, table, equation, and reference modules.
- Title, abstract, numbered sections, eleven figure captions, six table titles, equations, declarations, and references are present in both outputs.
- Different pagination (25 LaTeX pages versus 27 Word pages) reflects the native layout engines, not content drift.

## Build result

`IEEE_BUILD_AUDIT.json` status: **pass**.
