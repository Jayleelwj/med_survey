# Reference Verification Record

## Scope and Result

The IEEE survey reference catalogue contains **153 records**, exceeding the requested minimum of 110. At the time of this audit, **134 records contain a DOI**, **67 contain a PMID**, and no duplicate DOI is present after case-insensitive normalization. The current manuscript snapshot resolves **147 unique citation keys** with no undefined key; six catalogue records are presently unused (`consort_ai`, `cvs_review`, `lavrova`, `pixyl_reread`, `spirit_ai`, and `styner2008`). The catalogue is intentionally broader than the final emitted bibliography: the build system should include only keys cited in the final manuscript, figures, tables, or captions, in order of first appearance.

Verification prioritized version-of-record metadata and claims that materially affect dataset size, validation level, or clinical interpretation. DOI-bearing records were checked against publisher/Crossref metadata where available; PMID-bearing biomedical records were checked against PubMed; challenge and repository records were checked against their official descriptors. The 147 emitted entries are normalized at import to IEEE prose order: initials precede surnames, article and proceedings titles are quoted, publication fields follow the title, and a DOI is included only when present in the verified catalogue. Reports and web records use an organization author, document identifier where available, official URL, and access date. A syntactically valid DOI is not treated as evidence that a numerical result is correct—the claim-level conditions are documented separately in `EVIDENCE_LEDGER.md`.

## Corrected Catalogue Records

The following late overrides in `references_ieee.py` replace inaccurate or incomplete legacy metadata without changing the imported base catalogue:

- **Reviews and public resources:** `dl_systematic`, `carass_data`, `msseg_challenge`, `msseg2`, `mslesseg`, `msbaghdad`, `sibbms`, `ms3seg`, `pedims`, `mspaths`, `naims7t`, and `mindglide`.
- **Segmentation, harmonization, and diagnostic methods:** `giraldo`, `cerri`, `bianca`, `chaves`, `greselin`, `benveniste`, `larosa7t`, `molchanova`, `seok`, `lavrova`, and `combes`.
- **Workflow, longitudinal, and prognostic studies:** `peters2024`, `mastilovic2025`, `pixyl_reread`, `storelli`, `pontillo`, `denissen`, `sharrad`, `poretto`, and `cagol`.
- **Guidance and distributed learning:** `ofsep_protocol`, `stard_ai`, `cheers_ai`, `federated_ms`, `federated_ms2`, and `radiology_workflow`.

The corrections include formal titles, author order where the existing record named the wrong first author, journal volume/issue, pages or article number, DOI, PMID where verified, and publication status through the stated survey cutoff.

## High-Risk Factual Corrections

| Topic | Verified treatment in the revised survey | Source key(s) |
|---|---|---|
| MS PATHS denominators | Report **16,568 total enrollees**, **8,364 unique participants with MRI**, and **14,414 MRI studies** as separate quantities. Of the MRI participants, 3,822 had longitudinal imaging. Do not call 14,414 the number of patients | `mspaths` |
| MindGlide development patients | Use **NR (source discrepancy)** because the abstract reports 2,934 patients whereas Methods reports 2,871. The common verified quantities are 4,247 development scans from 592 scanners and an external evaluation of 14,952 scans from 1,001 patients and 186 scanners | `mindglide` |
| MSSEG-2 reader difficulty | The approximately 40% figure refers to final-reference lesions initially marked by no more than two of four readers and then subjected to senior-expert adjudication. It must not be generalized to “40% without expert agreement” or used to dismiss expert labels globally | `msseg2` |
| Benveniste spinal-cord study | Formal title is *Generalizable spinal cord multiple sclerosis lesion segmentation across MRI contrasts, protocols, and centers*; the source reports 1,849 people, 4,428 annotated MRI **images**, 23 centers, six contrasts, and 1.5/3/7-T acquisitions. “Images” is retained rather than silently converting this unit to independent examinations or 3-D volumes. Neuroradiologist Likert ratings favored the proposed model over contrast-specific pipelines (p < 0.01), while a single harmonized segmentation estimate is not imported. The model is public in Spinal Cord Toolbox; the constituent MRI are not presented as a reusable public dataset | `benveniste` |
| Federated-learning study 1 | Formal title is *Multiple sclerosis lesion segmentation: Revisiting weighting mechanisms for federated learning* and first author is D. Liu. Public- and in-house-scenario Dice values are treated as internal multi-client experiments, not independent external validation | `federated_ms` |
| Federated-learning study 2 | Formal title is *Improving multiple sclerosis lesion segmentation across clinical sites: A federated learning approach with noise-resilient training*; first author is L. Bai; journal volume is 152, not 154 | `federated_ms2` |
| MS-Baghdad | Formal title, 60-patient count, 1.5-T T1/T2/FLAIR input, multisite provenance, and consensus mask description were aligned to the Data in Brief record | `msbaghdad` |
| MSLesSeg | Formal title and Scientific Data article metadata were corrected. The survey reports 75 patients and 115 scans and avoids treating repeated scans as independent patients | `mslesseg` |
| MS3SEG | Formal title and 2026 Scientific Data metadata were corrected. The internal five-fold U-Net baseline is explicitly labeled internal; its binary and multiclass Dice values are not compared with other datasets | `ms3seg` |
| PediMS | Formal title and 2025 Scientific Data metadata were corrected. Nine pediatric patients and 28 scans remain separate units; repeated time points require patient-level splitting | `pedims` |
| Poretto PIRA model | Formal title and article metadata were corrected. The AUC 0.75 ± 0.06 belongs to nested randomized cross-validation in 719 patients and is not external or prospective validation | `poretto` |
| Cagol biomarker study | Formal title and 2026 article metadata were corrected. The two cohorts support replication of biomarker associations; no unverified single predictive-performance statistic is claimed | `cagol` |
| Shifts 2.0 MS component | Official Zenodo DOI `10.5281/zenodo.7051658` was verified. The MS component derives from existing MSSeg/OFSEP resources and is registration/request controlled; it must not be counted as a new independent cohort | `shifts2` |

## Identifier and Metadata Notes

- The catalogue deliberately uses IEEE-style abbreviated author lists (`et al.`) for long collaborations. This is a formatting choice, not a claim that the omitted authors are unknown.
- Several foundational architecture records are conference proceedings or arXiv records without a PMID. Their lack of a PMID is expected and must not be filled with an invented identifier.
- CVF accepted-version pagination can differ from Crossref/IEEE aggregate proceedings pagination for some computer-vision papers (for example DenseNet, Swin Transformer, UNETR, MoCo, MAE, DINO, and SAM). The catalogue retains the pagination of the cited primary accepted-version record rather than mixing numbering systems.
- `shifts2` uses a verified Zenodo dataset DOI rather than a journal DOI. Repository access conditions should remain distinct from copyright/license terms.
- Online-first year, issue year, and database-indexing year can differ. The catalogue uses the version-of-record issue metadata when an issue assignment was available by the survey cutoff.

## Access, License, and Regulatory Recheck on 29 August 2026

The following primary records were reopened on **29 August 2026**. This check records what the cited page states; it does not extrapolate to other versions, jurisdictions, or intended uses.

| Record | Primary record checked | Verified status used in the manuscript |
|---|---|---|
| Pixyl.Neuro K213253 | FDA 510(k) database, `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K213253` | Device name Pixyl.Neuro; decision date 30 June 2023; decision “Substantially Equivalent.” The entry is not represented as proof of MS outcome benefit |
| Icobrain K192130 | FDA 510(k) database, `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K192130` | Device name Icobrain; decision date 13 December 2019; decision “Substantially Equivalent.” No claim is made about jurisdictions outside the cited record |
| NeuroQuant K241098 | FDA 510(k) database and decision summary, `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K241098` | Device name NeuroQuant; decision date 22 August 2024; decision “Substantially Equivalent”; intended use concerns automated labeling, visualization, and volumetric quantification, not demonstrated patient benefit |
| NICE MIB291 | NICE MIB page, `https://www.nice.org.uk/advice/mib291` | The page remains a Medtech Innovation Briefing titled *icobrain ms for active relapsing–remitting multiple sclerosis*, published 29 March 2022. It is cited as a briefing, not an adoption recommendation or outcome trial |
| IMDRF N41 | IMDRF final-document page, `https://www.imdrf.org/documents/software-medical-device-samd-clinical-evaluation` | Status remains Final; published 21 September 2017; code IMDRF/SaMD WG/N41FINAL:2017 |
| IMDRF N88 | IMDRF final-document page, `https://www.imdrf.org/documents/good-machine-learning-practice-medical-device-development-guiding-principles` | Status remains Final; published 29 January 2025; code IMDRF/AIML WG/N88 FINAL:2025 |
| AssistMS | ISRCTN PDF/API-facing record, DOI `10.1186/ISRCTN99207647` | Prospectively registered; recruiting/ongoing; last edited 6 March 2026; no results posted in the record by the recheck date. The manuscript therefore does not assume trial outcomes |

Dataset access was audited separately from license. Table II now has distinct columns. A download link is recorded as `open download`, a challenge account as `registration-controlled`, a governed cohort request as `application-controlled`, and nonreleased trial/institutional MRI as `proprietary`. If the data license was not explicit in the official resource record reviewed for this draft, the table states `NR`; article open-access status is not substituted for a data license.

## Remaining NR or Manual-Verification Items

1. **MindGlide patient denominator:** unresolved by the source itself; retain `NR (source discrepancy)` unless the authors publish a correction.
2. **Non-DOI foundational records:** `attentionunet`, `vit`, `vae`, `gan`, `ddpm`, `scoresde`, `s4`, `mamba`, `mean_teacher`, `simclr`, and the current `cotr` record are identifier/manual records. They should be cited for architecture or training concepts, not for MS clinical performance.
3. **Regulatory and web records:** FDA, NICE, IMDRF, and the AssistMS registry were rechecked on **29 August 2026** as documented above. These records remain temporally unstable after that date; absent jurisdiction-specific status remains `NR`, and technical validation is not described as regulatory clearance.
4. **Dataset access versus license:** “open download,” “registration-controlled,” “application-controlled,” and “proprietary” describe access. They do not by themselves specify a reuse license. If a license was not explicit in the official record, report it as `NR` rather than inferring openness.
5. **Abstract-only quantities:** where only abstract-level metadata were sufficient to verify a bibliographic record but not the full cohort/split conditions, the evidence ledger leaves the missing fields as `NR` and omits the numerical performance claim.
6. **Final citation reachability:** the frozen build emitted 147 cited records. Every emitted reference has at least one citation in text, table, figure caption, or note, and every citation key resolves to the catalogue.

## Final-Build Checks Completed

The following checks were rerun after the manuscript and captions were frozen:

1. All `[@key]` citations resolve in `references_ieee.REFERENCES`; undefined keys: 0.
2. Only cited records are emitted; final bibliography: 147 unique references.
3. DOI strings were normalized case-insensitively; duplicate DOI count: 0.
4. No cited record contains `TBD`, `unknown DOI`, an invented PMID, or another placeholder identifier.
5. Retained performance statements were compared with `EVIDENCE_LEDGER.md`; incomplete conditions are reported qualitatively or as `NR`.
6. The 29 August 2026 regulatory/access recheck is preserved in the final build record and remains the temporal cutoff for those statuses.
