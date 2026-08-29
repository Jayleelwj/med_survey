# Figure Content, Topology, and Rendering Audit

Audit date: 2026-08-29

## Production boundary

The final set contains eleven research figure plates. ImageGen supplies only synthetic, non-patient MRI, cord, longitudinal, spatial-feature, and acquisition-variation subjects. Scientific text, module names, tensor symbols, operators, masks, contours, legends, brackets, and arrows are deterministic vector objects. Pale blue denotes encoder/input or technical-validation content; pale red denotes decoder/output or clinical/governance content; light gray denotes neutral operations. The figures contain no empirical performance values or untraceable dataset statistics.

| Figure | Content and correspondence audit | Topology, operator, or arrow audit | Redundancy and final-size audit | Result |
|---|---|---|---|---|
| Fig. 1 | Integrates an MS-oriented imaging substrate, orthogonal data/representation/method design dimensions, and evidence maturity. It supports the survey's data–method–task–evidence logic. | Only the evidence profile is directional; its arrow means increasing validation maturity, not performance. Design dimensions are explicitly combinable rather than a forced pipeline. | No model ranking, pseudo-statistics, or decorative neural-network motif. | Pass |
| Fig. 2 | Shows registered synthetic T1-weighted, T2-weighted, FLAIR, and post-contrast T1 appearances, specialized susceptibility and cord views, 2-D/2.5-D/3-D/multisequence representations, preprocessing choices, and domain variation. | Preprocessing modules are attached to an AI-input hub and labeled as task-dependent, so no universal order is implied. Sequence-to-target callouts are local and noncausal. | The same synthetic anatomy is used for contrast and domain comparisons; no patient data or performance value. | Pass |
| Fig. 3 | Shows patient-level longitudinal partitioning, the invalid visit-level leakage case, and multireader reference construction with adjudication. | Every visit from one patient remains within one split. Reader contours precede consensus/adjudication. The red cross marks the invalid split; it is not a data-flow edge. | Patient letters and rows are illustrative and explicitly do not encode cohort size. | Pass |
| Fig. 4 | Distinguishes U-Net, 3D U-Net, and residual U-Net with MRI input and mask output anchors. | Encoder resolution decreases through explicit downsampling; decoder resolution increases through explicit upsampling. Long skips enter `C`/Concat. The residual inset uses `+`/Add and a projection only when shape or channels differ. | No invented layer counts, channels, or tensor sizes. | Pass |
| Fig. 5 | Distinguishes dense U-Net, attention U-Net, and nnU-Net. The nnU-Net panel is an experiment-planning and locked-inference system, not a convolution block. | Dense layers receive all preceding features by channel concatenation. Attention uses aligned encoder and gating projections, element-wise Add, sigmoid coefficient, element-wise Multiply, then decoder Concat. nnU-Net follows fingerprinting, rule-based planning, applied preprocessing, candidate cross-validation, validated selection/ensemble, optional validated postprocessing, and locked test inference. | Test data provide no feedback to planning. The final Operator-audit text was re-spaced after page-level inspection. | Pass |
| Fig. 6 | Contrasts global ViT token modeling with hierarchical Swin modeling. | ViT applies patching, linear embedding, positional Add, and pre-LN MHSA/MLP residual Add operations before a task head or dense decoder. Swin separates W-MSA, SW-MSA with masking, and interstage patch merging. | A bare ViT is not depicted as a complete segmentation system; no unverified performance claim. | Pass |
| Fig. 7 | Shows volumetric UNETR and the representative CNN–Transformer hybrid TransUNet. | UNETR reshapes/projects multidepth Transformer states and joins them to a 3-D CNN decoder; the shallow CNN stem supplies the finest skip. TransUNet extracts local multiscale CNN features before tokenization/global modeling and uses retained CNN skips in decoding. Every `C` node has two shape-aligned operands. | No claim that non-MS demonstrations establish MS clinical performance. | Pass |
| Fig. 8 | Separates deep unfolding, VAE/GAN/diffusion, selective state-space recurrence, and registered longitudinal modeling. | Each unfolding stage applies a learned prior followed by data consistency using the same measured k-space and forward operator. VAE, GAN, and diffusion paths have distinct training/sampling semantics. The longitudinal panel receives fixed baseline and moving follow-up images, estimates registration, uses shared-weight encoders, then produces separate change-map and post-index risk outputs. | No arrow carries measured k-space directly into an image prior. No generative model is credited with lesion fidelity without evaluation. | Pass |
| Fig. 9 | Uses synthetic FLAIR and vector contours to distinguish a small-lesion miss, false positive, boundary displacement, and volume bias, linking each error to compatible objective emphasis and a complementary metric bundle. | Arrows run only from loss emphasis to the reporting bundle; they do not claim that a loss guarantees correction. Reference and prediction contours are distinct. | No curve, formula overload, empirical value, or cross-dataset ranking. | Pass |
| Fig. 10 | Replaces the rejected data-curve figure with five technical panels: leakage-resistant design, segmentation operators, bounded diagnostic/prognostic claims, hierarchical aggregation/uncertainty, and clinical evidence/governance. | Patient groups feed development only; the locked model points to one-shot external/protocol testing. Segmentation operators are parallel, not ranked. Evidence levels progress from internal testing to patient net benefit. | Contains no axes, ROC/calibration/decision/survival/drift curves, bars, scatter marks, or empirical values. | Pass |
| Fig. 11 | Uses six synthetic acquisition variants above three research planes: robustness, trust, and translation. | The central downward arrow links observed variability to prespecified validation; the right vertical arrow denotes increasing clinical consequence. Glyphs specify site-held-out testing, stress testing, supported missing modalities, failure localization, multirater uncertainty, subgroup audit, abstention, review, locked validation, human–AI workflow, net benefit, and monitored rollback. | No regulatory status, performance number, leaderboard, or decorative branch. | Pass |

## Global acceptance checks

- Inputs and outputs are explicit in every architecture panel.
- `C`/Concat, `+`/Add, and `⊙`/Multiply are used for different operations and are never interchanged.
- Solid arrows denote directed data, feature, inference, or evidence flow. Dashed lines denote physical constraints, shared parameters, training dependencies, or alignment and are labeled locally.
- Figure 10 contains no statistical plot and therefore has no unnecessary axes, ticks, or schematic result curves.
- ImageGen-generated material contains no labels, formulas, arrows, or scientific claims; all such content is vector-controlled.
- All 11 figure PDFs contain embedded vector fonts. Raster objects correspond only to intentional synthetic imaging or spatial-feature subjects.
- All 11 PNG companions are 4,296 px wide and exported at 600 dpi from the same figure objects as the vector PDFs.
- Captions and alt text are maintained in `ieee_content.py` and are shared by the Word and LaTeX builds.
- Final LaTeX PDF: 25 US-Letter pages; no missing figure, undefined reference/citation, overfull box, clipping, or blank page.
- Final Microsoft Word native QA export: 27 US-Letter pages; no blank page, cropped figure, truncated caption, table-row split without a repeated header, or discontinuous page number.

## Source and reproducibility

- Master builder: `make_ieee_figures.py`
- Shared vector grammar and ImageGen crops: `figure_v3_common.py`
- Overview/data plates: `figure_v3_overview.py`
- Architecture plates: `figure_v3_architectures.py`
- Error/evidence/translation plates: `figure_v3_evidence.py`
- Per-figure machine-readable assertions: `output/figures_ieee/FIGURE_VECTOR_AUDIT.md`
