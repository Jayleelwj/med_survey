# ImageGen source assets for the IEEE survey figures

These files are synthetic visual subjects, not patient data and not empirical
results. They were generated without scientific labels, network arrows,
performance values, or legends. Exact terminology, operators, masks, and data
flow are added later as deterministic vector graphics.

| Asset | Intended use | Visual inspection |
|---|---|---|
| `ms_mri_asset_sheet.png` | Matched multisequence brain MRI, susceptibility-marker close-ups, cortical-lesion view, and cervical cord | Anatomy and panel grid inspected; no generated text or network topology is used. The enhancement and susceptibility panels are treated as illustrative appearances, not diagnostic examples. |
| `longitudinal_flair_asset_sheet.png` | Registered baseline/follow-up FLAIR and a schematic change image | Time direction and anatomical correspondence inspected; the image is used only to explain longitudinal modeling, not lesion-growth performance. |
| `feature_space_asset_sheet.png` | Patch lattice, volumetric input, attention field, multiscale features, generative/fidelity subject, and mask contours | Retained only as spatial/texture subjects. All arrows, patch/token labels, operators, and reference/prediction semantics are redrawn as vectors. |
| `domain_variability_asset_sheet.png` | Same-case contrast, resolution, bias/noise, motion, and field-of-view variability | Used to illustrate plausible acquisition-domain changes. No panel is assigned a vendor, field strength, or quantitative degradation level. |

The unused `ms_mri_asset_sheet_v1.png` is retained as an intermediate ImageGen
iteration for provenance; it is not embedded in the final figures.
