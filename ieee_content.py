"""Single source of truth for IEEE figures, tables, equations, and accessibility text.

The manuscript contains only numbered placement markers.  Both the LaTeX and
Word renderers import this module, so captions, alt text, table cells, and
equations cannot drift between deliverables.
"""

from __future__ import annotations


FIGURES = {
    "FIGURE1": {
        "stem": "fig01_survey_map",
        "caption": (
            "Evidence-centered survey map. Synthetic FLAIR, susceptibility-sensitive, and cervical-cord MRI "
            "provide the imaging substrate; data provenance, input representation, and learning mechanism are "
            "orthogonal design dimensions that combine according to task; and the evidence profile separates "
            "internal testing, held-out centers, prospective workflow evaluation, and patient net benefit. The "
            "single vertical arrow denotes increasing validation maturity, not increasing model performance."
        ),
        "alt": (
            "Three panels show synthetic MS-oriented brain and cord MRI, combinable data-representation-method "
            "dimensions, and an evidence-maturity profile from internal testing to patient net benefit."
        ),
    },
    "FIGURE2": {
        "stem": "fig02_mri_inputs",
        "caption": (
            "MRI inputs for MS-oriented AI. Synthetic schematic anatomy illustrates complementary T1-weighted, "
            "T2-weighted, FLAIR, post-contrast T1-weighted, susceptibility-sensitive, and cervical-cord appearances; "
            "it is not patient data. Vector annotations connect sequence information to white-matter lesions, "
            "enhancement, CVS, PRL, cord lesions, 2-D/2.5-D/3-D representations, preprocessing, "
            "and acquisition-domain variables."
        ),
        "alt": (
            "Synthetic grayscale brain and cord MRI tiles are connected to MS biomarkers, tensor representations, "
            "preprocessing operations, and scanner and protocol sources of domain shift."
        ),
    },
    "FIGURE3": {
        "stem": "fig03_data_realism",
        "caption": (
            "Patient-level partitioning and multireader reference construction. Every visit from one patient is "
            "assigned to a single training, validation, or test partition; placing baseline and follow-up visits "
            "across partitions creates identity leakage. Reader-specific vector contours on synthetic FLAIR anatomy "
            "are retained before consensus or adjudication so that disagreement remains auditable. Patient letters "
            "and rows are illustrative identifiers, not a cohort-size statement."
        ),
        "alt": (
            "A patient-by-visit matrix keeps longitudinal examinations within one split, a counterexample shows "
            "visit-level leakage, and three reader contours are combined into an adjudicated lesion reference."
        ),
    },
    "FIGURE4": {
        "stem": "fig04_unet_3d_residual",
        "caption": (
            "U-Net, 3D U-Net, and residual U-Net. Pale blue denotes encoder features, pale red decoder features and "
            "predictions, and gray neutral operators. Long matching-resolution U-Net skips use channel concatenation "
            "(C/Concat). The residual block instead uses a short identity or projection branch with element-wise "
            "addition (+/Add). Arrows run from input to prediction."
        ),
        "alt": (
            "Three architecture panels show a two-dimensional U-Net with concatenating skips, a volumetric 3D U-Net, "
            "and a residual U-Net whose convolutional block contains a short additive identity path."
        ),
    },
    "FIGURE5": {
        "stem": "fig05_dense_attention_nnunet",
        "caption": (
            "Dense U-Net, attention U-Net, and nnU-Net. A dense block concatenates all preceding features into each "
            "later layer; it does not add them. The attention gate combines an encoder feature with a decoder gating "
            "signal to estimate an attention coefficient, multiplies that coefficient with the skip feature "
            "(⊙/Multiply), and then concatenates the gated skip in the decoder. nnU-Net is shown as rule-based "
            "configuration from a dataset fingerprint through preprocessing, 2-D/3-D/cascade planning, cross-validation, "
            "ensembling, and validation-selected postprocessing, not as a novel convolutional block."
        ),
        "alt": (
            "Three panels distinguish all-preceding dense concatenation, multiplicative attention gating of a skip, "
            "and the nnU-Net self-configuration and model-selection pipeline."
        ),
    },
    "FIGURE6": {
        "stem": "fig06_vit_swin",
        "caption": (
            "Vision Transformer and Swin Transformer. ViT partitions an image or volume into patches, applies linear "
            "embedding and positional encoding, and repeats pre-normalized MHSA and MLP sublayers with residual addition "
            "before a task-specific head or decoder. Swin alternates window attention (W-MSA) and shifted-window attention "
            "(SW-MSA) and uses patch merging to form hierarchical features. Gray nodes are token or normalization "
            "operations; pale blue blocks are encoders."
        ),
        "alt": (
            "ViT uses globally interacting patch tokens with positional encoding, while Swin uses regular and shifted "
            "attention windows and patch merging to construct a multiscale hierarchy."
        ),
    },
    "FIGURE7": {
        "stem": "fig07_unetr_transunet",
        "caption": (
            "UNETR and a CNN-Transformer hybrid represented by TransUNet. UNETR embeds 3-D patches, extracts hidden "
            "states at several Transformer depths, reshapes them into spatial features, and joins them to a CNN decoder. "
            "TransUNet first extracts local CNN features, tokenizes the deepest feature map for global Transformer "
            "modeling, and then decodes with retained higher-resolution CNN skips. Pale blue is encoding, pale red is "
            "decoding/output, and C denotes channel concatenation."
        ),
        "alt": (
            "UNETR sends multidepth Transformer hidden states to a 3D CNN decoder; TransUNet places global token modeling "
            "after a local CNN encoder and before a convolutional decoder."
        ),
    },
    "FIGURE8": {
        "stem": "fig08_emerging_models",
        "caption": (
            "Emerging and longitudinal architectures. Each deep-unfolding stage contains a learned prior followed by a "
            "data-consistency operation constrained by the same measured k-space. Separate panels distinguish VAE, GAN, "
            "and diffusion mechanisms; selective state-space scans; and longitudinal analysis with baseline and follow-up "
            "registration, shared-weight encoders, feature comparison, and change-map or risk output. The MRI textures are "
            "synthetic schematic anatomy, not patient data."
        ),
        "alt": (
            "Four technical panels show measurement-constrained unfolding, three distinct generative mechanisms, "
            "selective state-space scanning, and registered longitudinal MRI processed by shared-weight encoders."
        ),
    },
    "FIGURE9": {
        "stem": "fig09_error_loss_mapping",
        "caption": (
            "Clinically distinct segmentation errors require different objective emphasis and reporting bundles. "
            "Synthetic FLAIR thumbnails with vector contours illustrate small-lesion omission, a false-positive lesion, "
            "boundary displacement, and volume bias. Focal, Tversky, specificity-aware overlap, regional, boundary, "
            "surface, and volume-aware terms address different error components, but no loss guarantees lesion recovery. "
            "No empirical performance values are shown."
        ),
        "alt": (
            "Four synthetic FLAIR panels map small-lesion miss, false positive, boundary displacement, and volume bias "
            "to a compatible loss emphasis and a complementary lesion-, surface-, or volume-level metric bundle."
        ),
    },
    "FIGURE10": {
        "stem": "fig10_evaluation_frameworks",
        "caption": (
            "Evaluation logic from leakage control to governed clinical use. Five panels connect patient-level splitting "
            "and locked external testing, complementary segmentation metrics, bounded diagnostic and prognostic claims, "
            "stratified aggregation with uncertainty and abstention, and an evidence ladder from internal testing to "
            "patient net benefit. Pale blue denotes technical measurement and validation operations, pale red denotes "
            "clinical or governance actions, and gray denotes neutral constraints. Metric adequacy does not establish "
            "evidence strength or clinical utility. No empirical performance values are shown."
        ),
        "alt": (
            "Five technical panels link leakage-resistant study design, task-specific segmentation metrics, diagnostic "
            "and prognostic claims, stratified aggregation and uncertainty, and evidence levels to bounded clinical "
            "decisions and deployment governance."
        ),
    },
    "FIGURE11": {
        "stem": "fig11_validation_roadmap",
        "caption": (
            "Domain variability and validation priorities for MS MRI AI. Synthetic FLAIR anatomy illustrates reference-like, "
            "low-resolution, intensity-shifted, noisy, motion-degraded, and alternate-protocol inputs; it is not patient data. "
            "The three research planes separate robustness tests, trust safeguards, and translation endpoints. The downward "
            "arrow denotes increasing clinical consequence, while the individual glyphs specify site-held-out testing, "
            "protocol stress, supported missing modalities, failure localization, multirater uncertainty, subgroup audit, "
            "abstention, transparent review, locked external validation, human--AI workflow evaluation, net benefit, and "
            "governed monitoring or rollback. No empirical performance values are shown."
        ),
        "alt": (
            "A strip of six synthetic FLAIR domain variants sits above three research planes for robustness, trust, and "
            "translation, ending in locked external validation, human review, net benefit, and monitored revalidation."
        ),
    },
}


TABLES = {
    "TABLE1": {
        "caption": "MRI SEQUENCES, AI INPUTS, AND MS TARGETS",
        "headers": ["MRI input", "Typical AI representation", "MS-relevant target", "Primary limitation"],
        "widths": [0.16, 0.22, 0.28, 0.34],
        "rows": [
            ["T1-weighted", "2-D/3-D anatomy channel", "Tissue segmentation, regional volume, atrophy", "Lesions may be subtle; scanner-dependent contrast"],
            ["T2-weighted / PD", "Single or paired channels", "Water-rich lesions and cord abnormalities", "CSF and nonspecific hyperintensity reduce specificity"],
            ["FLAIR", "2-D, 2.5-D, or 3-D volume", "White-matter burden; new or enlarging lesions", "Motion, thick slices, confluent lesions, and vascular mimics"],
            ["Post-contrast T1", "Registered pre/post or post-only volume", "Active enhancing lesions", "Rare positives, vessels, and acquisition timing"],
            ["DIR / PSIR", "High-resolution cortical contrast", "Cortical and leukocortical lesions", "Limited availability and high rater uncertainty"],
            ["SWI / T2* / QSM", "Magnitude/phase or susceptibility maps", "CVS and PRL", "Eligibility rules, orientation, and specialized acquisition"],
            ["Spinal T2/STIR/PSIR", "Sagittal plus axial 2-D/3-D inputs", "Cord area and intramedullary lesions", "Small anatomy, pulsation, partial volume, and incomplete coverage"],
        ],
        "note": "PD, proton density; FLAIR, fluid-attenuated inversion recovery; DIR, double inversion recovery; PSIR, phase-sensitive inversion recovery; SWI, susceptibility-weighted imaging; QSM, quantitative susceptibility mapping; CVS, central vein sign; PRL, paramagnetic rim lesion.",
    },
    "TABLE2": {
        "caption": "MS MRI DATASETS, BENCHMARKS, AND CONTROLLED COHORTS",
        "headers": ["Resource", "Independent people / scans", "Sequences and task", "Centers / scanners", "Longitudinal", "Reference standard", "Access mode", "License", "Main limitation"],
        "widths": [0.09, 0.12, 0.135, 0.095, 0.065, 0.115, 0.09, 0.075, 0.215],
        "rows": [
            ["ISBI 2015 [@carass2017; @carass_data]", "19 / 82", "T1, PD/T2, FLAIR; white-matter lesions", "1 site; 3-T Philips", "4–6 visits", "Two manual raters", "Registration-controlled", "NR", "Only 19 people; visit-level leakage risk"],
            ["MSSEG 2016 [@msseg_descriptor; @msseg_challenge]", "53 / 53", "T1, FLAIR, PD/T2; white-matter lesions", "3 sites; 4 scanners", "No", "Seven experts and fusion", "Registration-controlled", "NR", "Small labeled training set; target depends on fusion rule"],
            ["MSSEG-2 [@msseg2]", "100 / 200", "Paired FLAIR; new lesions", "15 scanners; 3 vendors", "Two visits", "Four readers plus senior adjudication", "Registration-controlled", "NR", "FLAIR-only; difficult lesions concentrate disagreement"],
            ["3D-MR-MS [@lesjak3d]", "30 / 30", "T1, T2, FLAIR, post-Gd T1; lesions", "1 site; 3-T Siemens", "No", "Three-expert consensus", "Open download", "NR", "Small single-scanner cohort"],
            ["Long-MR-MS [@lesjaklong]", "20 / 40", "T1, T2, PD, FLAIR; lesion change", "1 site; 1.5-T Philips", "Two visits", "Two-expert consensus", "Open download", "NR", "One interval and 3-mm sections"],
            ["MSLesSeg [@mslesseg]", "75 / 115", "T1, T2, FLAIR; white-matter lesions", "Several 1.5-T systems", "1–4 visits", "One rater; three-expert review", "Open download", "NR", "Most participants have one visit"],
            ["MS-Baghdad [@msbaghdad]", "60 / 60", "Routine T1/T2/FLAIR; lesions", "20 centers; 1.5 T", "No", "Three-expert consensus", "Open download", "NR", "Limited harmonized protocol metadata"],
            ["MS3SEG [@ms3seg]", "100 / 100", "Routine MRI; MS lesion versus other WMH", "1 site; 1.5 T", "No", "Junior and senior tri-mask review", "Open download", "NR", "Lesions below 3 mm excluded"],
            ["PediMS [@pedims]", "9 / 28", "T1, T2, FLAIR; pediatric lesions", "Predominantly one 3-T site", "1–6 visits", "Specialist-validated masks", "Open download", "NR", "Too small for independent model development"],
            ["Multicenter cord study [@benveniste]", "1,849 / 4,428 annotated MRI images", "Six cord contrasts; lesions", "23 centers; 1.5/3/7 T", "Mixed", "Expert annotations; external labeled sets", "Proprietary/not released (MRI); model public", "MRI reuse NR; code separately licensed", "Images are the source unit, not independent exams or volumes"],
            ["MS PATHS [@mspaths]", "16,568 enrolled; 8,364 with MRI / 14,414 studies", "MPRAGE and SPACE-FLAIR; outcomes", "10 institutions; Siemens 3 T", "Subset", "No dense masks at cohort scale", "Application-controlled", "NR; access agreement applies", "Standardized but vendor-specific acquisition"],
            ["MindGlide sources [@mindglide]", "Training patients NR (source discrepancy); 4,247 development scans; 1,001 people / 14,952 external scans", "Mixed trial and clinical contrasts", "592 development / 186 external scanners", "Extensive", "Trial/cohort-derived labels", "Proprietary", "NR", "Scale limits independent reproduction; patient discrepancy"],
        ],
        "note": "Counts preserve each source's unit and separate people from scans, studies, and annotated images. For MindGlide, the abstract reports 2,934 development patients and the Methods report 2,871; the value is therefore NR (source discrepancy). Access mode and license are separate: an open article or public model does not imply reusable MRI data. NR, not reported or not verified; WMH, white-matter hyperintensity.",
    },
    "TABLE3": {
        "caption": "DEEP LEARNING ARCHITECTURE FAMILIES",
        "headers": ["Family", "Input", "Core mechanism", "MS MRI task", "Resource determinants", "Principal advantage", "Typical failure", "MS-specific validation record used here"],
        "widths": [0.09, 0.08, 0.16, 0.13, 0.12, 0.13, 0.15, 0.14],
        "rows": [
            ["U-Net", "2-D", "Encoder–decoder; matching-scale Concat skips", "Brain lesion segmentation", "Pixel area, feature widths, and number of scales", "Preserves local detail", "No through-plane context; texture shortcuts", "MS task use reported; isolated family effect: NR"],
            ["3D U-Net", "3-D volume or patch", "Volumetric operators and Concat skips", "Brain and cord segmentation", "Patch voxels, feature widths, and activation storage", "Models volumetric continuity", "Patch context and anisotropy", "Canonical 3D U-Net MS external validation: NR"],
            ["Residual U-Net", "2-D/3-D", "Short identity Add paths inside blocks", "Deeper segmentation", "Block depth, feature widths, and projection paths", "Improves gradient propagation", "Parameter cost and overfitting", "Isolated MS validation: NR"],
            ["Dense U-Net", "2-D/3-D", "All-preceding feature Concat", "Lesion segmentation", "Growth rate and accumulated feature channels", "Feature reuse", "Channel growth and texture dependence", "Isolated MS validation: NR"],
            ["Attention U-Net", "2-D/3-D", "Decoder-gated encoder skips with ⊙/Multiply", "Small-lesion localization", "Number and spatial size of gated skip features", "Suppresses irrelevant skip regions", "Can suppress subtle true lesions", "Attention U-Net specifically in MS: NR"],
            ["nnU-Net", "2-D/3-D/cascade", "Dataset fingerprint and rule-based pipeline planning", "General segmentation baseline", "Planned patch/batch size, folds, candidate models, and ensemble", "Reproducible configuration baseline", "Cannot repair biased data or labels", "Framework-specific MS external validation: NR"],
            ["Vision Transformer", "2-D/3-D tokens", "Global MHSA with positional encoding", "Classification or encoder backbone", "Token count (quadratic attention), width, depth, and heads", "Long-range interaction", "Data demand and coarse-token detail loss", "Stand-alone ViT in MS: NR"],
            ["Swin Transformer", "2-D/3-D tokens", "W-MSA, SW-MSA, and patch merging", "Dense prediction", "Window size, stage depth, token count, and feature width", "Hierarchical scalable context", "Window and merging losses", "Swin-specific MS external validation: NR"],
            ["UNETR", "3-D volume", "Transformer encoder; multidepth CNN decoder skips", "Volumetric segmentation", "3-D token count, encoder depth/width, and decoder activations", "Global 3-D context", "Memory and token-resolution limits", "UNETR-specific MS external validation: NR"],
            ["CNN–Transformer hybrid", "2-D/3-D", "Local CNN features followed by global token modeling", "Segmentation and classification", "CNN feature maps plus token count, width, and depth", "Combines local and global bias", "Downsampling and token bottleneck", "TransUNet/CoTr-specific MS external validation: NR"],
        ],
        "note": "Architecture labels are mechanisms, not maturity ratings. Task-level evidence for a derived MS system cannot identify the causal contribution of one family unless that family is isolated under the same data and validation protocol. Resource use is therefore described by determinants rather than unsupported low/moderate/high labels. NR, not reported or not established; MHSA, multi-head self-attention; W-MSA, window multi-head self-attention; SW-MSA, shifted-window multi-head self-attention.",
    },
    "TABLE4": {
        "caption": "LOSS FUNCTIONS AND TASK-SPECIFIC METRICS",
        "headers": ["Objective family", "Examples", "Best-matched task", "Strength", "Failure mode and required metric"],
        "widths": [0.16, 0.20, 0.19, 0.19, 0.26],
        "rows": [
            ["Voxel reconstruction", "L1, L2, Huber", "Reconstruction and synthesis", "Stable intensity fidelity", "Blur or outlier sensitivity; add SSIM, NMSE, and lesion-preservation tests"],
            ["Perceptual / adversarial", "Feature and GAN losses", "Synthesis and harmonization", "Plausible texture", "Hallucination; adjudicate lesion addition and deletion"],
            ["Data consistency", "Measured k-space residual", "Accelerated reconstruction", "Preserves acquired measurements", "Does not guarantee pathology; evaluate downstream tasks"],
            ["Voxel classification", "Cross-entropy and focal", "Segmentation and detection", "Probabilistic local target", "Imbalance and noisy labels; add lesion sensitivity and PPV"],
            ["Regional overlap", "Dice, generalized Dice, Tversky", "Imbalanced segmentation", "Optimizes overlap", "Volume dominance and empty masks; add lesion-instance metrics"],
            ["Boundary geometry", "Boundary and Hausdorff-oriented", "Contour refinement", "Penalizes shape error", "Cannot recover a completely missed lesion; report HD95"],
            ["Representation", "Contrastive and masked reconstruction", "Self-supervised pretraining", "Uses unlabeled images", "Invalid invariances; test downstream external data"],
            ["Consistency", "Teacher–student and pseudo-label", "Semi-supervised learning", "Uses unlabeled images", "Confirms teacher errors; audit calibration"],
            ["Outcome", "Regression, ranking, Cox, DeepHit", "EDSS, PIRA, and cognition", "Handles continuous or censored targets", "Confounding; report calibration, C-index, and net benefit"],
        ],
        "note": "HD95, 95th-percentile Hausdorff distance; PPV, positive predictive value; PIRA, progression independent of relapse activity. Surface Dice is an evaluation metric and is not assumed to be a unique standard loss.",
    },
    "TABLE5": {
        "caption": "TASK-SPECIFIC TECHNICAL PERFORMANCE AND CLINICAL EVIDENCE",
        "headers": ["Task and source", "Dataset or cohort condition", "Reported evaluation", "Validation level", "Evidence-supported interpretation", "Clinical evidence gap"],
        "widths": [0.16, 0.20, 0.16, 0.14, 0.18, 0.16],
        "rows": [
            ["New-lesion benchmark [@msseg2]", "100 paired-FLAIR patients: 40 development and 60 hidden test; 35 hidden-test cases had new lesions", "Among 35 positive hidden cases, best expert mean lesion F1 0.679 (SD 0.345) and best submitted method 0.698 (SD 0.295); across the 60-case hidden test, best three-category accuracy was 85% for both", "L2 hidden benchmark with expert comparison", "Case classification can be useful while lesion matching remains difficult", "Distribution-specific; no prospective workflow or outcome test"],
            ["MS lesion vs. other WMH [@ms3seg]", "100 patients; one 1.5-T scanner; lesions <3 mm excluded", "Five-fold internal U-Net Dice: 0.7469 binary and 0.6686 multiclass", "L1 internal cross-validation", "Demonstrates feasibility for the resource-defined distinction", "Single scanner and lesion exclusion preclude transportability claims"],
            ["Multicontrast cord lesions [@benveniste]", "1,849 people; 4,428 annotated MRI images; 23 centers; six contrasts at 1.5/3/7 T", "Neuroradiologist Likert comparison favored the proposed model (p < 0.01); a single harmonized segmentation estimate is NR here", "L3 retrospective multicenter/external evaluation", "Tests contrast, center, level, and resolution heterogeneity", "Effect size, prospective correction burden, and patient benefit are NR"],
            ["Federated brain-lesion segmentation [@federated_ms]", "Public and in-house multi-client experiments; patient counts and common sequence set NR in the audited record", "Case-wise/voxel-wise Dice: 65.20%/74.30% (public scenario) and 53.66%/62.31% (in-house scenario)", "L1 internal multi-client experiments", "Shows optimization behavior under decentralized non-IID clients", "Not an unseen-center or prospective clinical validation"],
            ["Routine longitudinal activity [@barnett]", "282 patients; 397 scan pairs; principally three scanners/centers", "Case-level sensitivity/specificity: AI 93.3%/97.6%, standard radiology 58.3%/98.8%, core laboratory 85.0%/96.4%; stable-protocol subset sensitivity 91.7% for AI and core laboratory", "L3 retrospective real-world validation with human comparators", "Supports assistive monitoring under the studied conditions", "Consensus adjudication and retrospective design limit autonomous or outcome claims"],
            ["AI-supported reporting time [@peters2024]", "Four radiologists; 50 lesion-burden studies and 50 follow-up studies; patient overlap NR", "Mean time fell from 286.85 to 196.34 s (burden) and 196.17 to 120.87 s (follow-up)", "L4 retrospective crossover reader study", "Demonstrates a reader-time effect in the tested workflow", "Multicenter generalizability and patient outcomes are NR"],
            ["Automated serial-reading time [@sieber]", "35 consecutive single-site patients; baseline plus three follow-ups", "Mean reading time 9.05 min; AI assistance reduced it by 2.83 min", "L4 retrospective paired-reader study", "Suggests workflow efficiency for serial review", "Small single-site study; safety and net benefit remain NR"],
            ["Year-3 PIRA prediction [@poretto]", "719 newly diagnosed patients from three Italian centers; 92 developed year-3 PIRA; structured clinical/radiological variables, not image tensors", "Random-forest test AUC 0.75 ± 0.06 under nested randomized cross-validation", "L1 internal nested cross-validation", "Supports cohort-level prognostic association under observed care", "External calibration, treatment-confounding control, and decision net benefit are NR"],
            ["Archive-scale quantitative analysis [@mindglide]", "4,247 development scans/592 scanners; 14,952 external scans from 1,001 people/186 scanners", "Single task-comparable aggregate result: NR", "L3 external multiscanner evaluation", "Demonstrates evaluation across heterogeneous archives", "Patient-count discrepancy and proprietary composition limit reproduction"],
        ],
        "note": "Each row is interpreted only under its stated cohort, case condition, metric, and validation level; numerical results are neither pooled nor ranked across rows. L1, internal resampling; L2, sequestered benchmark; L3, external-site/scanner or real-world retrospective validation; L4, human–AI reader/workflow study. NR, not reported or not verified; AUC, area under the receiver-operating-characteristic curve; WMH, white-matter hyperintensity; PIRA, progression independent of relapse activity; non-IID, non-identically distributed.",
    },
    "TABLE6": {
        "caption": "CHALLENGES, EVIDENCE GAPS, AND RESEARCH PRIORITIES",
        "headers": ["Challenge", "Typical evidence gap", "Priority action", "Validation requirement", "Clinical endpoint"],
        "widths": [0.16, 0.20, 0.22, 0.22, 0.20],
        "rows": [
            ["Small or unrepresentative data", "Academic, trial, or regional concentration", "Consecutive multicenter cohorts", "Patient- and site-held-out testing", "Subgroup-safe errors"],
            ["Scanner and protocol shift", "Same-ecosystem hold-out", "Vendor, field-strength, protocol, and upgrade stress tests", "Geographic and temporal external sets", "Stable actionable findings"],
            ["Noisy reference labels", "One fused binary mask", "Multirater probabilistic reference and adjudication record", "Agreement and lesion-size-stratified analysis", "Reviewable candidates"],
            ["Tiny lesions and imbalance", "Aggregate Dice only", "Lesion-aware sampling and complementary objectives", "Negative cases; lesion sensitivity and false positives per scan", "Activity detection"],
            ["Missing or longitudinal inputs", "Complete-case or matched protocols", "Modality dropout and variable-time models", "Every supported sequence subset plus drift analysis", "Reliable interval change"],
            ["Uncertainty and calibration", "AUC or Dice without reliability", "Calibrated abstention linked to review", "External calibration and out-of-distribution tests", "Safe manual verification"],
            ["Privacy and fairness", "No subgroup or model-update audit", "Federated evaluation and bias monitoring", "Site and demographic strata", "Equitable performance"],
            ["Compute and integration", "No latency or failure reporting", "Efficient models and PACS engineering", "End-to-end operational test", "Time and correction burden"],
            ["Clinical utility", "Retrospective technical endpoint", "Prospective human–AI evaluation", "Randomized or stepped-wedge study plus monitoring", "Decisions, outcomes, and net benefit"],
        ],
        "note": "Regulatory authorization, technical validation, workflow efficiency, and patient benefit are distinct evidence levels. PACS, picture archiving and communication system.",
    },
}


EQUATIONS = {
    "EQ1": {
        "latex": r"L_{\mathrm{CE}}=-\sum_i\left[y_i\log p_i+(1-y_i)\log(1-p_i)\right],",
        "label": "eq:ce",
        "linear": "L_CE = -sum_i [y_i log(p_i) + (1-y_i) log(1-p_i)]",
        "mathml": """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><msub><mi>L</mi><mtext>CE</mtext></msub><mo>=</mo><mo>-</mo><munder><mo>∑</mo><mi>i</mi></munder><mo>[</mo><msub><mi>y</mi><mi>i</mi></msub><mi>log</mi><mo>(</mo><msub><mi>p</mi><mi>i</mi></msub><mo>)</mo><mo>+</mo><mo>(</mo><mn>1</mn><mo>-</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mi>log</mi><mo>(</mo><mn>1</mn><mo>-</mo><msub><mi>p</mi><mi>i</mi></msub><mo>)</mo><mo>]</mo></mrow></math>""",
    },
    "EQ2": {
        "latex": r"L_{\mathrm{Dice}}=1-\frac{2\sum_i p_i y_i+\epsilon}{\sum_i p_i+\sum_i y_i+\epsilon},",
        "label": "eq:dice",
        "linear": "L_Dice = 1 - (2 sum_i p_i y_i + epsilon)/(sum_i p_i + sum_i y_i + epsilon)",
        "mathml": """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><msub><mi>L</mi><mtext>Dice</mtext></msub><mo>=</mo><mn>1</mn><mo>-</mo><mfrac><mrow><mn>2</mn><munder><mo>∑</mo><mi>i</mi></munder><msub><mi>p</mi><mi>i</mi></msub><msub><mi>y</mi><mi>i</mi></msub><mo>+</mo><mi>ε</mi></mrow><mrow><munder><mo>∑</mo><mi>i</mi></munder><msub><mi>p</mi><mi>i</mi></msub><mo>+</mo><munder><mo>∑</mo><mi>i</mi></munder><msub><mi>y</mi><mi>i</mi></msub><mo>+</mo><mi>ε</mi></mrow></mfrac></mrow></math>""",
    },
    "EQ3": {
        "latex": r"L_{\mathrm{T}}=1-\frac{\mathrm{TP}+\epsilon}{\mathrm{TP}+\alpha\mathrm{FP}+\beta\mathrm{FN}+\epsilon}.",
        "label": "eq:tversky",
        "linear": "L_T = 1 - (TP + epsilon)/(TP + alpha FP + beta FN + epsilon)",
        "mathml": """<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><msub><mi>L</mi><mtext>T</mtext></msub><mo>=</mo><mn>1</mn><mo>-</mo><mfrac><mrow><mtext>TP</mtext><mo>+</mo><mi>ε</mi></mrow><mrow><mtext>TP</mtext><mo>+</mo><mi>α</mi><mtext>FP</mtext><mo>+</mo><mi>β</mi><mtext>FN</mtext><mo>+</mo><mi>ε</mi></mrow></mfrac></mrow></math>""",
    },
}


ROMAN_TABLE_NUMBERS = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}
