"""Reference catalogue for the IEEE MS-MRI survey draft.

The base catalogue contains MS-specific clinical, dataset, task and translation
sources.  This module adds primary architecture, optimisation, reporting and
deployment sources used in the IEEE rewrite.  The build script emits only
items actually cited, in order of first appearance.
"""

from __future__ import annotations

import re

from references import REFERENCES as BASE_REFERENCES


REFERENCES = dict(BASE_REFERENCES)
REFERENCES.update({
    "magnims2016": "M. Filippi et al., MRI criteria for the diagnosis of multiple sclerosis: MAGNIMS consensus guidelines, Lancet Neurol., vol. 15, pp. 292–303, 2016, doi:10.1016/S1474-4422(15)00393-2.",
    "filippi2019": "M. Filippi et al., Assessment of lesions on magnetic resonance imaging in multiple sclerosis: practical guidelines, Brain, vol. 142, pp. 1858–1875, 2019, doi:10.1093/brain/awz144.",
    "sati2016": "P. Sati et al., The central vein sign and its clinical evaluation for the diagnosis of multiple sclerosis: a consensus statement, Nat. Rev. Neurol., vol. 12, pp. 714–722, 2016, doi:10.1038/nrneurol.2016.166.",
    "bagnato2024": "F. Bagnato et al., Imaging chronic active lesions in multiple sclerosis: a consensus statement, Brain, vol. 147, pp. 2913–2933, 2024, doi:10.1093/brain/awae013.",
    "absinta2016": "M. Absinta et al., Persistent 7-tesla phase rim predicts poor outcome in new multiple sclerosis patient lesions, J. Clin. Invest., vol. 126, pp. 2597–2609, 2016, doi:10.1172/JCI86198.",
    "ofsep_protocol": "A. Cotton et al., MRI protocol and quality control for the OFSEP cohort, J. Neuroradiol., vol. 42, pp. 133–140, 2015, doi:10.1016/j.neurad.2014.12.001.",
    "unet": "O. Ronneberger, P. Fischer, and T. Brox, U-Net: convolutional networks for biomedical image segmentation, in Proc. MICCAI, 2015, pp. 234–241, doi:10.1007/978-3-319-24574-4_28.",
    "unet3d": "Ö. Çiçek, A. Abdulkadir, S. S. Lienkamp, T. Brox, and O. Ronneberger, 3D U-Net: learning dense volumetric segmentation from sparse annotation, in Proc. MICCAI, 2016, pp. 424–432, doi:10.1007/978-3-319-46723-8_49.",
    "resnet": "K. He, X. Zhang, S. Ren, and J. Sun, Deep residual learning for image recognition, in Proc. IEEE CVPR, 2016, pp. 770–778, doi:10.1109/CVPR.2016.90.",
    "vnet": "F. Milletari, N. Navab, and S.-A. Ahmadi, V-Net: fully convolutional neural networks for volumetric medical image segmentation, in Proc. 3DV, 2016, pp. 565–571, doi:10.1109/3DV.2016.79.",
    "r2unet": "M. Z. Alom, C. Yakopcic, M. Hasan, T. M. Taha, and V. K. Asari, Recurrent residual U-Net for medical image segmentation, J. Med. Imaging, vol. 6, art. 014006, 2019, doi:10.1117/1.JMI.6.1.014006.",
    "densenet": "G. Huang, Z. Liu, L. van der Maaten, and K. Q. Weinberger, Densely connected convolutional networks, in Proc. IEEE CVPR, 2017, pp. 4700–4708, doi:10.1109/CVPR.2017.243.",
    "hdenseunet": "X. Li et al., H-DenseUNet: hybrid densely connected UNet for liver and tumor segmentation from CT volumes, IEEE Trans. Med. Imaging, vol. 37, pp. 2663–2674, 2018, doi:10.1109/TMI.2018.2845918.",
    "attentionunet": "O. Oktay et al., Attention U-Net: learning where to look for the pancreas, arXiv:1804.03999, 2018.",
    "nnunet": "F. Isensee, P. F. Jaeger, S. A. A. Kohl, J. Petersen, and K. H. Maier-Hein, nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation, Nat. Methods, vol. 18, pp. 203–211, 2021, doi:10.1038/s41592-020-01008-z.",
    "deepmedic": "K. Kamnitsas et al., Efficient multi-scale 3D CNN with fully connected CRF for accurate brain lesion segmentation, Med. Image Anal., vol. 36, pp. 61–78, 2017, doi:10.1016/j.media.2016.10.004.",
    "vit": "A. Dosovitskiy et al., An image is worth 16×16 words: transformers for image recognition at scale, in Proc. ICLR, 2021, arXiv:2010.11929.",
    "swin": "Z. Liu et al., Swin Transformer: hierarchical vision transformer using shifted windows, in Proc. IEEE ICCV, 2021, pp. 10012–10022, doi:10.1109/ICCV48922.2021.00986.",
    "unetr": "A. Hatamizadeh et al., UNETR: transformers for 3D medical image segmentation, in Proc. IEEE WACV, 2022, pp. 574–584, doi:10.1109/WACV51458.2022.00181.",
    "transunet": "J. Chen et al., TransUNet: rethinking the U-Net architecture design for medical image segmentation through the lens of transformers, Med. Image Anal., vol. 97, art. 103280, 2024, doi:10.1016/j.media.2024.103280.",
    "cotr": "Y. Xie, J. Zhang, C. Shen, and Y. Xia, CoTr: efficiently bridging CNN and Transformer for 3D medical image segmentation, in Proc. MICCAI, 2021, pp. 171–180, arXiv:2103.03024.",
    "swin_ssl": "Y. Tang et al., Self-supervised pre-training of Swin Transformers for 3D medical image analysis, in Proc. IEEE CVPR, 2022, pp. 20730–20740.",
    "s4": "A. Gu, K. Goel, and C. Ré, Efficiently modeling long sequences with structured state spaces, in Proc. ICLR, 2022.",
    "mamba": "A. Gu and T. Dao, Mamba: linear-time sequence modeling with selective state spaces, in Proc. COLM, 2024.",
    "segmamba": "Z. Xing et al., SegMamba: long-range sequential modeling Mamba for 3D medical image segmentation, in Proc. MICCAI, 2024, pp. 578–588, doi:10.1007/978-3-031-72111-3_54.",
    "swinumamba": "J. Liu et al., Swin-UMamba: adapting Mamba-based vision foundation models for medical image segmentation, IEEE Trans. Med. Imaging, vol. 44, pp. 3898–3908, 2025, doi:10.1109/TMI.2024.3508698.",
    "unrolling": "V. Monga, Y. Li, and Y. C. Eldar, Algorithm unrolling: interpretable, efficient deep learning for signal and image processing, IEEE Signal Process. Mag., vol. 38, pp. 18–44, 2021, doi:10.1109/MSP.2020.3016905.",
    "modl": "H. K. Aggarwal, M. P. Mani, and M. Jacob, MoDL: model-based deep learning architecture for inverse problems, IEEE Trans. Med. Imaging, vol. 38, pp. 394–405, 2019, doi:10.1109/TMI.2018.2865356.",
    "varnet": "A. Sriram et al., End-to-end variational networks for accelerated MRI reconstruction, in Proc. MICCAI, 2020, pp. 64–73, doi:10.1007/978-3-030-59713-9_7.",
    "gan": "I. J. Goodfellow et al., Generative adversarial nets, in Proc. NeurIPS, 2014, pp. 2672–2680.",
    "pix2pix": "P. Isola, J.-Y. Zhu, T. Zhou, and A. A. Efros, Image-to-image translation with conditional adversarial networks, in Proc. IEEE CVPR, 2017, pp. 5967–5976, doi:10.1109/CVPR.2017.632.",
    "cyclegan": "J.-Y. Zhu, T. Park, P. Isola, and A. A. Efros, Unpaired image-to-image translation using cycle-consistent adversarial networks, in Proc. IEEE ICCV, 2017, pp. 2242–2251, doi:10.1109/ICCV.2017.244.",
    "vae": "D. P. Kingma and M. Welling, Auto-encoding variational Bayes, in Proc. ICLR, 2014, arXiv:1312.6114.",
    "ddpm": "J. Ho, A. Jain, and P. Abbeel, Denoising diffusion probabilistic models, in Proc. NeurIPS, 2020, pp. 6840–6851.",
    "scoresde": "Y. Song et al., Score-based generative modeling through stochastic differential equations, in Proc. ICLR, 2021.",
    "gessert": "N. Gessert, J. Krüger, R. Opfer, A. Ostwaldt, P. Manogaran, and A. Schlaefer, Multiple sclerosis lesion activity segmentation with attention-guided two-path CNNs, Comput. Med. Imaging Graph., vol. 84, art. 101772, 2020, doi:10.1016/j.compmedimag.2020.101772.",
    "kruger": "J. Krüger et al., Fully automated longitudinal segmentation of new or enlarged multiple sclerosis lesions using 3D convolutional neural networks, NeuroImage Clin., vol. 28, art. 102445, 2020, doi:10.1016/j.nicl.2020.102445.",
    "kamraoui": "R. A. Kamraoui, B. Mansencal, J. V. Manjón, and P. Coupé, Longitudinal detection of new MS lesions using deep learning, Front. Neuroimaging, vol. 1, art. 948235, 2022, doi:10.3389/fnimg.2022.948235.",
    "to2021": "M.-S. To et al., Self-supervised lesion change detection and localisation in longitudinal multiple sclerosis brain imaging, in Proc. MICCAI, 2021, pp. 670–680, doi:10.1007/978-3-030-87234-2_63.",
    "modelsgenesis": "Z. Zhou et al., Models Genesis, Med. Image Anal., vol. 67, art. 101840, 2021, doi:10.1016/j.media.2020.101840.",
    "simclr": "T. Chen, S. Kornblith, M. Norouzi, and G. Hinton, A simple framework for contrastive learning of visual representations, in Proc. ICML, vol. 119, 2020, pp. 1597–1607.",
    "moco": "K. He, H. Fan, Y. Wu, S. Xie, and R. Girshick, Momentum contrast for unsupervised visual representation learning, in Proc. IEEE CVPR, 2020, pp. 9729–9738, doi:10.1109/CVPR42600.2020.00975.",
    "mae": "K. He et al., Masked autoencoders are scalable vision learners, in Proc. IEEE CVPR, 2022, pp. 16000–16009, doi:10.1109/CVPR52688.2022.01553.",
    "dino": "M. Caron et al., Emerging properties in self-supervised vision transformers, in Proc. IEEE ICCV, 2021, pp. 9650–9660, doi:10.1109/ICCV48922.2021.00951.",
    "sam": "A. Kirillov et al., Segment anything, in Proc. IEEE ICCV, 2023, pp. 4015–4026, doi:10.1109/ICCV51070.2023.00371.",
    "medsam": "J. Ma et al., Segment anything in medical images, Nat. Commun., vol. 15, art. 654, 2024, doi:10.1038/s41467-024-44824-z.",
    "gdl": "C. H. Sudre, W. Li, T. Vercauteren, S. Ourselin, and M. J. Cardoso, Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations, in Proc. DLMIA/ML-CDS, 2017, pp. 240–248, doi:10.1007/978-3-319-67558-9_28.",
    "tversky": "S. S. M. Salehi, D. Erdogmus, and A. Gholipour, Tversky loss function for image segmentation using 3D fully convolutional deep networks, in Proc. MLMI, 2017, pp. 379–387, doi:10.1007/978-3-319-67389-9_44.",
    "focal": "T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollár, Focal loss for dense object detection, in Proc. IEEE ICCV, 2017, pp. 2999–3007, doi:10.1109/ICCV.2017.324.",
    "boundaryloss": "H. Kervadec, J. Bouchtiba, C. Desrosiers, É. Granger, J. Dolz, and I. B. Ayed, Boundary loss for highly unbalanced segmentation, Med. Image Anal., vol. 67, art. 101851, 2021, doi:10.1016/j.media.2020.101851.",
    "hausdorffloss": "D. Karimi and S. E. Salcudean, Reducing the Hausdorff distance in medical image segmentation with convolutional neural networks, IEEE Trans. Med. Imaging, vol. 39, pp. 499–513, 2020, doi:10.1109/TMI.2019.2930068.",
    "mean_teacher": "A. Tarvainen and H. Valpola, Mean teachers are better role models: weight-averaged consistency targets improve semi-supervised deep learning results, in Proc. NeurIPS, 2017, pp. 1195–1204.",
    "cox": "D. R. Cox, Regression models and life-tables, J. R. Stat. Soc. B, vol. 34, pp. 187–202, 1972, doi:10.1111/j.2517-6161.1972.tb00899.x.",
    "deepsurv": "J. L. Katzman et al., DeepSurv: personalized treatment recommender system using a Cox proportional hazards deep neural network, BMC Med. Res. Methodol., vol. 18, art. 24, 2018, doi:10.1186/s12874-018-0482-1.",
    "deephit": "C. Lee, W. R. Zame, J. Yoon, and M. van der Schaar, DeepHit: a deep learning approach to survival analysis with competing risks, in Proc. AAAI, vol. 32, 2018, doi:10.1609/aaai.v32i1.11842.",
    "stard_ai": "D. Sounderajah et al., STARD-AI: reporting guidelines for diagnostic accuracy studies using artificial intelligence, Nat. Med., 2025, doi:10.1038/s41591-025-03953-8.",
    "miclaim": "B. Norgeot et al., Minimum information about clinical artificial intelligence modeling: the MI-CLAIM checklist, Nat. Med., vol. 26, pp. 1320–1324, 2020, doi:10.1038/s41591-020-1041-y.",
    "cheers_ai": "J. Elvidge et al., Consolidated Health Economic Evaluation Reporting Standards for interventions that use artificial intelligence (CHEERS-AI), Value Health, 2024, doi:10.1016/j.jval.2024.05.006.",
    "algorithm_audit": "X. Liu et al., The medical algorithmic audit, Lancet Digit. Health, vol. 4, pp. e384–e397, 2022, doi:10.1016/S2589-7500(22)00003-6.",
    "nair_uncertainty": "T. Nair, D. Precup, D. L. Arnold, and T. Arbel, Exploring uncertainty measures in deep networks for multiple sclerosis lesion detection and segmentation, Med. Image Anal., vol. 59, art. 101557, 2020, doi:10.1016/j.media.2019.101557.",
    "mehrtash_calibration": "A. Mehrtash et al., Confidence calibration and predictive uncertainty estimation for deep medical image segmentation, IEEE Trans. Med. Imaging, vol. 39, pp. 3868–3878, 2020, doi:10.1109/TMI.2020.3006437.",
    "calibration": "B. Van Calster et al., Calibration: the Achilles heel of predictive analytics, BMC Med., vol. 17, art. 230, 2019, doi:10.1186/s12916-019-1466-7.",
    "decisioncurve": "A. J. Vickers and E. B. Elkin, Decision curve analysis: a novel method for evaluating prediction models, Med. Decis. Making, vol. 26, pp. 565–574, 2006, doi:10.1177/0272989X06295361.",
    "marten_ood": "G. Mårtensson et al., The reliability of a deep learning model in clinical out-of-distribution MRI data, Med. Image Anal., vol. 66, art. 101714, 2020, doi:10.1016/j.media.2020.101714.",
    "federated_ms": "Y. Liu et al., Federated learning for multi-center multiple sclerosis lesion segmentation, Front. Neurosci., vol. 17, art. 1167612, 2023, doi:10.3389/fnins.2023.1167612.",
    "federated_ms2": "W. Bai et al., Privacy-preserving federated learning for multiple sclerosis MRI analysis, Artif. Intell. Med., vol. 154, art. 102872, 2024, doi:10.1016/j.artmed.2024.102872.",
    "gender_bias": "A. J. Larrazabal, N. Nieto, V. Peterson, D. H. Milone, and E. Ferrante, Gender imbalance in medical imaging datasets produces biased classifiers for computer-aided diagnosis, Proc. Natl. Acad. Sci. USA, vol. 117, pp. 12592–12594, 2020, doi:10.1073/pnas.1919012117.",
    "radiology_workflow": "A. S. Tejani et al., Integrating artificial intelligence into radiology practice: a multisociety expert statement, Radiology, vol. 311, art. 232653, 2024, doi:10.1148/radiol.232653.",
    "imdrf_samd": "International Medical Device Regulators Forum, Software as a Medical Device (SaMD): Clinical Evaluation, IMDRF/SaMD WG/N41FINAL:2017, 2017.",
    "imdrf_gmlp": "International Medical Device Regulators Forum, Good Machine Learning Practice for Medical Device Development: Guiding Principles, IMDRF/AIML WG/N88FINAL:2025, 2025.",
})


# Publisher-, Crossref-, and PubMed-verified corrections.  These late overrides
# deliberately leave the legacy catalogue untouched while ensuring that the IEEE
# build uses the version-of-record title and bibliographic data.
REFERENCES.update({
    "dl_systematic": "P. Belwal and S. Singh, \"Deep learning techniques to detect and analysis of multiple sclerosis through MRI: A systematic literature review,\" Comput. Biol. Med., vol. 185, art. 109530, 2025, doi:10.1016/j.compbiomed.2024.109530. PMID:39693692.",
    "carass_data": "A. Carass, S. Roy, A. Jog, et al., \"Longitudinal multiple sclerosis lesion segmentation data resource,\" Data Brief, vol. 12, pp. 346–350, 2017, doi:10.1016/j.dib.2017.04.004. PMID:28491937.",
    "msseg_challenge": "O. Commowick, F. Cervenansky, F. Cotton, and M. Dojat, \"Objective evaluation of multiple sclerosis lesion segmentation using a data management and processing infrastructure,\" Sci. Rep., vol. 8, art. 13650, 2018, doi:10.1038/s41598-018-31911-7. PMID:30209345.",
    "msseg2": "A. Masson et al., \"Performances of experts and automated methods on new multiple sclerosis lesions detection: Insights from the MSSeg2 challenge,\" Sci. Rep., vol. 16, art. 23247, 2026, doi:10.1038/s41598-026-52150-1. PMID:42168373.",
    "mslesseg": "F. Guarnera, A. Rondinella, E. Crispino, et al., \"MSLesSeg: Baseline and benchmarking of a new multiple sclerosis lesion segmentation dataset,\" Sci. Data, vol. 12, art. 920, 2025, doi:10.1038/s41597-025-05250-y. PMID:40450079.",
    "msbaghdad": "A. M. Muslim, S. Mashohor, G. Al Gawwam, et al., \"Brain MRI dataset of multiple sclerosis with consensus manual lesion segmentation and patient meta information,\" Data Brief, vol. 42, art. 108139, 2022, doi:10.1016/j.dib.2022.108139. PMID:35496484.",
    "sibbms": "A. Tuchinov et al., \"SibBMS: Siberian brain multiple sclerosis dataset with lesion segmentation and patient meta information,\" Mach. Learn. Biomed. Imaging, vol. 3, pp. 905–912, 2025, doi:10.59275/j.melba.2025-f798.",
    "ms3seg": "M. B. Bawil, M. Shamsi, A. Ghalehasadi, A. F. Jafargholkhanloo, and A. S. Bavil, \"A multiple sclerosis MRI dataset with tri-mask annotations for lesion segmentation,\" Sci. Data, vol. 13, art. 867, 2026, doi:10.1038/s41597-026-07184-5. PMID:41980977.",
    "pedims": "M. Popa, G. A. Vișa, and C. R. Șofariu, \"PediMS: A pediatric multiple sclerosis lesion segmentation dataset,\" Sci. Data, vol. 12, art. 1184, 2025, doi:10.1038/s41597-025-05346-5. PMID:40640191.",
    "mspaths": "E. M. Mowry, R. A. Bermel, J. R. Williams, et al., \"Harnessing real-world data to inform decision-making: Multiple Sclerosis Partners Advancing Technology and Health Solutions (MS PATHS),\" Front. Neurol., vol. 11, art. 632, 2020, doi:10.3389/fneur.2020.00632. PMID:32849170.",
    "naims7t": "D. M. Harrison et al., \"Pooled analysis of multiple sclerosis findings on multisite 7 Tesla MRI: Protocol and initial observations,\" Hum. Brain Mapp., vol. 45, no. 12, art. e26816, 2024, doi:10.1002/hbm.26816. PMID:39169546.",
    "mindglide": "R. Goebl et al., \"Enabling new insights from old scans by repurposing clinical MRI archives for multiple sclerosis research,\" Nat. Commun., vol. 16, art. 3149, 2025, doi:10.1038/s41467-025-58274-8. PMID:40195318.",
    "giraldo": "D. L. Giraldo et al., \"Perceptual super-resolution in multiple sclerosis MRI,\" Front. Neurosci., vol. 18, art. 1473132, 2024, doi:10.3389/fnins.2024.1473132. PMID:39502711.",
    "cerri": "S. Cerri, O. Puonti, D. S. Meier, et al., \"A contrast-adaptive method for simultaneous whole-brain and lesion segmentation in multiple sclerosis,\" NeuroImage, vol. 225, art. 117471, 2021, doi:10.1016/j.neuroimage.2020.117471. PMID:33099007.",
    "bianca": "G. Gentile et al., \"BIANCA-MS: An optimized tool for automated multiple sclerosis lesion segmentation,\" Hum. Brain Mapp., vol. 44, no. 14, pp. 4893–4913, 2023, doi:10.1002/hbm.26424. PMID:37530598.",
    "chaves": "H. Chaves et al., \"Assessing robustness and generalization of a deep neural network for brain MS lesion segmentation on real-world data,\" Eur. Radiol., vol. 34, no. 3, pp. 2024–2035, 2024, doi:10.1007/s00330-023-10093-5. PMID:37650967.",
    "greselin": "P. Greselin et al., \"Contrast-enhancing lesion segmentation in multiple sclerosis: A deep learning approach validated in a multicentric cohort,\" Bioengineering, vol. 11, no. 8, art. 858, 2024, doi:10.3390/bioengineering11080858. PMID:39199815.",
    "benveniste": "P.-L. Benveniste et al., \"Generalizable spinal cord multiple sclerosis lesion segmentation across MRI contrasts, protocols, and centers,\" Mult. Scler., vol. 32, no. 6, pp. 598–613, 2026, doi:10.1177/13524585261427333. PMID:42028790.",
    "larosa7t": "F. La Rosa et al., \"Multiple sclerosis cortical lesion detection with deep learning at ultra-high-field MRI,\" NMR Biomed., vol. 35, no. 8, art. e4730, 2022, doi:10.1002/nbm.4730. PMID:35297114.",
    "molchanova": "N. Molchanova et al., \"A comparative study of deep learning for cortical lesion MRI segmentation with explainability analysis in multiple sclerosis,\" NeuroImage Clin., vol. 50, art. 104007, 2026, doi:10.1016/j.nicl.2026.104007. PMID:42224860.",
    "seok": "J. M. Seok et al., \"Differentiation between multiple sclerosis and neuromyelitis optica spectrum disorder using a deep learning model,\" Sci. Rep., vol. 13, art. 11625, 2023, doi:10.1038/s41598-023-38271-x. PMID:37468553.",
    "lavrova": "E. Lavrova et al., \"Exploratory radiomic analysis of conventional vs. quantitative brain MRI: Toward automatic diagnosis of early multiple sclerosis,\" Front. Neurosci., vol. 15, art. 679941, 2021, doi:10.3389/fnins.2021.679941. PMID:34421515.",
    "combes": "B. Combès et al., \"A clinically-compatible workflow for computer-aided assessment of brain disease activity in multiple sclerosis patients,\" Front. Med., vol. 8, art. 740248, 2021, doi:10.3389/fmed.2021.740248.",
    "peters2024": "S. Peters, G. Kellermann, J. Watkinson, et al., \"AI supported detection of cerebral multiple sclerosis lesions decreases radiologic reporting times,\" Eur. J. Radiol., vol. 178, art. 111638, 2024, doi:10.1016/j.ejrad.2024.111638. PMID:39067268.",
    "mastilovic2025": "M. Mastilović et al., \"Evaluation of two AI techniques for the detection of new T2/FLAIR lesions in the follow-up of multiple sclerosis patients,\" Front. Neurol., vol. 16, art. 1678073, 2025, doi:10.3389/fneur.2025.1678073. PMID:41132873.",
    "pixyl_reread": "M. Mastilović et al., \"Artificial intelligence in the detection of multiple sclerosis plaques: Can it influence the treatment decision?\" J. Neuroradiol., vol. 53, no. 1, art. 101406, 2026, doi:10.1016/j.neurad.2025.101406. PMID:41349455.",
    "storelli": "L. Storelli et al., \"A deep learning approach to predicting disease progression in multiple sclerosis using magnetic resonance imaging,\" Invest. Radiol., vol. 57, no. 7, pp. 423–432, 2022, doi:10.1097/RLI.0000000000000854. PMID:35093968.",
    "pontillo": "G. Pontillo, S. Cocozza, M. Di Stasi, et al., \"A combined radiomics and machine learning approach to overcome the clinicoradiologic paradox in multiple sclerosis,\" AJNR Am. J. Neuroradiol., vol. 42, no. 11, pp. 1927–1933, 2021, doi:10.3174/ajnr.A7274. PMID:34531195.",
    "denissen": "C. Marzi, A. d'Ambrosio, S. Diciotti, et al., \"Prediction of the information processing speed performance in multiple sclerosis using a machine learning approach in a large multicenter magnetic resonance imaging data set,\" Hum. Brain Mapp., vol. 44, no. 1, pp. 186–202, 2023, doi:10.1002/hbm.26106. PMID:36255155.",
    "sharrad": "D. F. Sharrad et al., \"Defining progression independent of relapse activity (PIRA) in adult patients with relapsing multiple sclerosis: A systematic review,\" Mult. Scler. Relat. Disord., vol. 78, art. 104899, 2023, doi:10.1016/j.msard.2023.104899. PMID:37499338.",
    "poretto": "V. Poretto, W. Endrizzi, M. Betti, et al., \"Machine learning analysis applied to prediction of early progression independent of relapse activity in multiple sclerosis patients,\" Eur. J. Neurol., vol. 32, no. 12, art. e70417, 2025, doi:10.1111/ene.70417. PMID:41312659.",
    "cagol": "A. Cagol, P. Benkert, S. Schaedelin, et al., \"Assessing the relative importance of imaging and serum biomarkers in capturing disability, cognitive impairment, and clinical progression in multiple sclerosis,\" Adv. Sci., vol. 13, no. 10, art. e12946, 2026, doi:10.1002/advs.202512946. PMID:41527428.",
    "ofsep_protocol": "A. Cotton et al., \"OFSEP, a nationwide cohort of people with multiple sclerosis: Consensus minimal MRI protocol,\" J. Neuroradiol., vol. 42, no. 3, pp. 133–140, 2015, doi:10.1016/j.neurad.2014.12.001.",
    "stard_ai": "V. Sounderajah, A. Guni, X. Liu, et al., \"The STARD-AI reporting guideline for diagnostic accuracy studies using artificial intelligence,\" Nat. Med., vol. 31, no. 10, pp. 3283–3289, 2025, doi:10.1038/s41591-025-03953-8.",
    "cheers_ai": "J. Elvidge et al., \"Consolidated Health Economic Evaluation Reporting Standards for interventions that use artificial intelligence (CHEERS-AI),\" Value Health, vol. 27, no. 9, pp. 1196–1205, 2024, doi:10.1016/j.jval.2024.05.006.",
    "federated_ms": "D. Liu, M. Cabezas, D. Wang, et al., \"Multiple sclerosis lesion segmentation: Revisiting weighting mechanisms for federated learning,\" Front. Neurosci., vol. 17, art. 1167612, 2023, doi:10.3389/fnins.2023.1167612. PMID:37274196.",
    "federated_ms2": "L. Bai, D. Wang, H. Wang, et al., \"Improving multiple sclerosis lesion segmentation across clinical sites: A federated learning approach with noise-resilient training,\" Artif. Intell. Med., vol. 152, art. 102872, 2024, doi:10.1016/j.artmed.2024.102872. PMID:38701636.",
    "radiology_workflow": "A. S. Tejani, T. S. Cook, M. Hussain, T. Sippel Schmidt, and K. P. O'Donnell, \"Integrating and adopting AI in the radiology workflow: A primer for standards and Integrating the Healthcare Enterprise (IHE) profiles,\" Radiology, vol. 311, no. 3, art. e232653, 2024, doi:10.1148/radiol.232653. PMID:38888474.",
})


# Primary-record web and report entries were rechecked on the stated access
# date.  A database decision is cited as a device-specific 510(k) record, not as
# evidence of clinical benefit or of authorization outside the United States.
REFERENCES.update({
    "fda_pixyl": "U.S. Food and Drug Administration, \"Pixyl.Neuro, 510(k) premarket notification K213253,\" decision: substantially equivalent, Jun. 30, 2023. [Online]. Available: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K213253. Accessed: Aug. 29, 2026.",
    "fda_icobrain": "U.S. Food and Drug Administration, \"Icobrain, 510(k) premarket notification K192130,\" decision: substantially equivalent, Dec. 13, 2019. [Online]. Available: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K192130. Accessed: Aug. 29, 2026.",
    "fda_neuroquant": "U.S. Food and Drug Administration, \"NeuroQuant, 510(k) premarket notification K241098,\" decision: substantially equivalent, Aug. 22, 2024. [Online]. Available: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K241098. Accessed: Aug. 29, 2026.",
    "nice_mib291": "National Institute for Health and Care Excellence, \"icobrain ms for active relapsing–remitting multiple sclerosis,\" Medtech Innovation Briefing MIB291, Mar. 29, 2022. [Online]. Available: https://www.nice.org.uk/advice/mib291. Accessed: Aug. 29, 2026.",
    "assistms": "ISRCTN Registry, \"Artificial intelligence-assisted magnetic resonance imaging for quality, efficiency and equity in the NHS care of multiple sclerosis (AssistMS),\" ISRCTN99207647, recruiting; no results posted as of Aug. 29, 2026, doi:10.1186/ISRCTN99207647. [Online]. Available: https://www.isrctn.com/ISRCTN99207647. Accessed: Aug. 29, 2026.",
    "imdrf_samd": "International Medical Device Regulators Forum, \"Software as a Medical Device (SaMD): Clinical evaluation,\" IMDRF/SaMD WG/N41FINAL:2017, Sep. 21, 2017. [Online]. Available: https://www.imdrf.org/documents/software-medical-device-samd-clinical-evaluation. Accessed: Aug. 29, 2026.",
    "imdrf_gmlp": "International Medical Device Regulators Forum, \"Good machine learning practice for medical device development: Guiding principles,\" IMDRF/AIML WG/N88 FINAL:2025, Jan. 29, 2025. [Online]. Available: https://www.imdrf.org/documents/good-machine-learning-practice-medical-device-development-guiding-principles. Accessed: Aug. 29, 2026.",
    "shifts2": "A. Malinin, N. Band, Y. Gal, et al., \"Shifts 2.0: Extending the dataset real distributional shift benchmark,\" in Proc. NeurIPS Datasets Benchmarks, 2022, arXiv:2206.15407, dataset doi:10.5281/zenodo.7051658.",
    "alpaca": "F. Hu, Z. Ren, L. Chen, et al., \"Automated segmentation of multiple sclerosis lesions, paramagnetic rims, and central vein sign on MRI provides reliable diagnostic biomarkers,\" Imaging Neurosci., vol. 3, art. IMAG.a.932, 2025, doi:10.1162/IMAG.a.932. PMID:41089191.",
})


def _initials_first(author: str) -> str:
    """Convert a verified NLM-style ``Surname INITIALS`` token to IEEE order."""

    author = author.strip()
    if author in {"et al", "et al."}:
        return "et al."
    match = re.match(r"^(?P<surname>.+?)\s+(?P<initials>[A-ZÀ-ÖØ-ÞŽŠŹĆŁĐÞ-]+)$", author)
    if not match:
        return author
    initials = "".join(f"{char}." if char.isalpha() else char for char in match.group("initials"))
    initials = initials.replace("..", ".")
    initials = re.sub(r"(?<=\.)((?=[A-ZÀ-ÖØ-ÞŽŠŹĆŁ]))", " ", initials)
    return f"{initials} {match.group('surname')}"


def _format_nlm_authors(raw: str) -> str:
    parts = [part.strip() for part in raw.rstrip(".").split(",") if part.strip()]
    converted = [_initials_first(part) for part in parts]
    if not converted:
        return raw.rstrip(".")
    if converted[-1] == "et al.":
        return ", ".join(converted[:-1]) + " et al."
    if len(converted) == 1:
        return converted[0]
    if len(converted) == 2:
        return f"{converted[0]} and {converted[1]}"
    return ", ".join(converted[:-1]) + f", and {converted[-1]}"


def _split_ieee_author_title(prefix: str) -> tuple[str, str] | None:
    if " et al., " in prefix:
        authors, title = prefix.split(" et al., ", 1)
        return authors + " et al.", title
    match = re.match(r"^(.*?, and [^,]+), (.+)$", prefix)
    if match:
        return match.group(1), match.group(2)
    match = re.match(r"^([^,]+ and [^,]+), (.+)$", prefix)
    if match:
        return match.group(1), match.group(2)
    match = re.match(r"^([A-ZÀ-ÖØ-Þ](?:[A-ZÀ-ÖØ-Þ.\- ]+)?\s+[^,]+), (.+)$", prefix)
    if match:
        return match.group(1), match.group(2)
    return None


def _format_reference_ieee(value: str) -> str:
    """Apply one IEEE prose layout without adding unverified metadata."""

    value = re.sub(r"\s+", " ", value.strip())
    if '"' in value or "[Online]." in value:
        return value

    # Legacy biomedical entries use NLM order and compact year/volume/pages.
    first_stop = value.find(". ")
    if first_stop > 0 and not re.match(r"^[A-Z](?:\.|-)", value):
        authors_raw = value[:first_stop]
        remainder = value[first_stop + 2 :]
        title_stop = remainder.find(". ")
        if title_stop > 0:
            title = remainder[:title_stop]
            bibliographic = remainder[title_stop + 2 :]
            authors = _format_nlm_authors(authors_raw)
            match = re.match(
                r"^(?P<journal>.+?) (?P<year>\d{4});(?P<volume>[^:]+):(?P<locator>[^.]+)\.(?P<tail>.*)$",
                bibliographic,
            )
            if match:
                locator = match.group("locator")
                loc_label = "pp." if "–" in locator or "-" in locator else "art."
                tail = match.group("tail").strip()
                result = (
                    f'{authors}, "{title}," {match.group("journal")}, vol. {match.group("volume")}, '
                    f'{loc_label} {locator}, {match.group("year")}'
                )
                return result + (f", {tail}" if tail else ".")
            match = re.match(r"^(?P<venue>.+?) (?P<year>\d{4})\.(?P<tail>.*)$", bibliographic)
            if match:
                tail = match.group("tail").strip()
                result = f'{authors}, "{title}," {match.group("venue")}, {match.group("year")}'
                return result + (f", {tail}" if tail else ".")

    # The architecture catalogue was already in IEEE field order; add the
    # missing article-title quotation marks deterministically.
    if ", in Proc. " in value:
        prefix, venue = value.split(", in Proc. ", 1)
        pair = _split_ieee_author_title(prefix)
        if pair:
            return f'{pair[0]}, "{pair[1]}," in Proc. {venue}'
    if ", arXiv:" in value:
        prefix, venue = value.split(", arXiv:", 1)
        pair = _split_ieee_author_title(prefix)
        if pair:
            return f'{pair[0]}, "{pair[1]}," arXiv:{venue}'
    if ", vol. " in value:
        before_volume, volume_tail = value.split(", vol. ", 1)
        if ", " in before_volume:
            author_title, journal = before_volume.rsplit(", ", 1)
            pair = _split_ieee_author_title(author_title)
            if pair:
                return f'{pair[0]}, "{pair[1]}," {journal}, vol. {volume_tail}'
    return value


_VENUE_ABBREVIATIONS = {
    "Lancet Neurol": "Lancet Neurol.",
    "Radiol Artif Intell": "Radiol. Artif. Intell.",
    "Nat Med": "Nat. Med.",
    "Magn Reson Imaging": "Magn. Reson. Imaging",
    "Comput Med Imaging Graph": "Comput. Med. Imaging Graph.",
    "Mult Scler": "Mult. Scler.",
    "Sci Rep": "Sci. Rep.",
    "Front Neurol": "Front. Neurol.",
    "Front Neurosci": "Front. Neurosci.",
    "Hum Brain Mapp": "Hum. Brain Mapp.",
    "NMR Biomed": "NMR Biomed.",
    "Neuroimage Clin": "NeuroImage Clin.",
    "Invest Radiol": "Invest. Radiol.",
    "Brain Commun": "Brain Commun.",
    "Proc Mach Learn Res": "Proc. Mach. Learn. Res.",
    "Neurol Res": "Neurol. Res.",
    "Nat Commun": "Nat. Commun.",
    "Brain Sci": "Brain Sci.",
    "JAMA Neurol": "JAMA Neurol.",
    "Imaging Neurosci": "Imaging Neurosci.",
    "NPJ Digit Med": "npj Digit. Med.",
}


def _normalize_ieee_punctuation(value: str) -> str:
    value = re.sub(r",\s+et al\.,", " et al.,", value)
    for source, target in _VENUE_ABBREVIATIONS.items():
        value = value.replace(f'," {source}, vol.', f'," {target}, vol.')
    return value


REFERENCES = {
    key: _normalize_ieee_punctuation(_format_reference_ieee(value))
    for key, value in REFERENCES.items()
}
