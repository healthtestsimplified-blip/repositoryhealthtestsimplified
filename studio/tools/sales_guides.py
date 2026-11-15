"""Sales Team Test Guide videos (Suraksha Sales Academy): website entries.
Each test: (name, code, tat, method, sample, why, when, pitch). Text summarised from the guide videos.
Run: python3 studio/tools/sales_guides.py  -> encodes videos/posters and inserts entries into data.js"""
import json, os, subprocess, sys

A = "/mnt/user-data/attachments/ec966ba6-8f99-574b-b1df-53ce08cf4cc1"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

G = [
 ("sg01", "697d4383-290048.mp4", "Haem-Onc: Broad NGS Panels", "Haematologists, haemato-oncologists, BMT physicians",
  "Send fresh EDTA blood or bone marrow, not frozen. Attach the CBC / flow cytometry report.", [
  ("Onco-Haem DNA Only Panel (40 genes)", "confirm", "22 days", "NGS", "EDTA blood / bone marrow",
   "Finds mutations such as FLT3, NPM1 and IDH in AML, MDS and MPN.", "At diagnosis, for risk grouping and to choose targeted drugs.",
   "\"One 40-gene test covers the key myeloid mutations for diagnosis, risk and targeted drugs.\""),
  ("Onco-Haem RNA Only Fusion Panel (29 genes)", "confirm", "22 days", "NGS", "EDTA blood / bone marrow",
   "Detects leukaemia fusions such as BCR-ABL1, PML-RARA and KMT2A.", "When leukaemia is diagnosed or suspected and fusion status decides treatment.",
   "\"Fusions change the treatment plan; this panel checks 29 of them together.\""),
  ("Comprehensive Myeloid & Lymphoid Panel", "confirm", "21-25 days", "NGS", "EDTA blood / bone marrow",
   "Broad work-up covering myeloid and lymphoid cancers (ALL, CLL, lymphoma).", "When a blood cancer is suspected but the type is not yet clear.",
   "\"When you are not sure if it is myeloid or lymphoid, one panel covers both.\""),
  ("Comprehensive Myeloid Panel (DNA + RNA fusions, 69 genes)", "PTMP0188", "22 days", "NGS", "EDTA blood / bone marrow",
   "Complete AML / MDS work-up: mutations and fusions in one test.", "At diagnosis of AML or MDS, for classification and risk.",
   "\"Mutations plus fusions in one report: no need to send two samples.\"")]),
 ("sg02", "24104488-290049.mp4", "Transplant & HLA", "BMT physicians, nephrologists, transplant surgeons",
  "Chimerism needs pre-transplant samples of BOTH recipient and donor. Plan before the transplant.", [
  ("Post-Transplant Chimerism Study (24 STR markers)", "confirm", "4-5 days", "Fragment analysis", "EDTA blood / bone marrow (recipient + donor)",
   "After a bone marrow transplant, shows how much of the blood comes from the donor.", "Regularly after BMT; an early sign of graft failure or relapse.",
   "\"Store pre-transplant samples of recipient and donor with us now, so follow-up chimerism is ready.\""),
  ("Tacrolimus Metabolism Genotype (CYP3A4 / CYP3A5)", "PTMP0251", "4 days", "Sanger", "EDTA whole blood",
   "Shows how fast the body breaks down tacrolimus.", "Before starting tacrolimus in kidney, liver or BMT transplant.",
   "\"Helps set the right starting dose of tacrolimus from day one.\""),
  ("HLA-A, B, C, DR, DQ High Resolution by Sequencing", "confirm", "7 days", "NGS", "EDTA whole blood",
   "High-resolution tissue typing of the patient and possible donors.", "Before BMT or organ transplant: patient and family donors.",
   "\"High-resolution HLA for donor matching, patient and family together.\"")]),
 ("sg03", "88a8211a-290050.mp4", "Lung Cancer", "Medical oncologists, pulmonologists, thoracic surgeons, pathologists",
  "Every new non-small cell lung cancer should be tested BEFORE treatment starts.", [
  ("EGFR Mutation Analysis (Exons 18-21)", "PTMP0047", "12 days", "Sanger / Real time PCR", "FFPE tumour block",
   "Finds EGFR mutations in non-small cell lung cancer (adenocarcinoma).", "Before starting EGFR tablets.", "\"No EGFR result, no EGFR tablet.\""),
  ("EGFR Mutation by Real Time PCR", "PTMP0021", "9 days", "Real time PCR", "FFPE tumour block",
   "Quicker check of the common EGFR mutations.", "When the oncologist needs a fast EGFR answer.", "\"Common EGFR mutations in 9 days.\""),
  ("Lung Cancer Panel: 12 Gene with PD-L1 (DAKO 22C3)", "PTMP0153", "22 days", "NGS + IHC", "FFPE tumour block",
   "12 key lung cancer genes plus PD-L1 for immunotherapy.", "At diagnosis of advanced NSCLC: one-stop work-up.", "\"Targeted drugs and immunotherapy answered from one block.\""),
  ("Lung Cancer Panel Liquid Biopsy, 12 Gene", "PTMP0199", "22 days", "NGS", "Streck blood (10 ml)",
   "The same key lung genes read from blood (ctDNA).", "When tissue is too little or biopsy is not possible; tracking drug resistance.",
   "\"No tissue? A blood sample can still guide targeted treatment.\""),
  ("Lung Panel: EGFR Sequencing + ALK FISH + ROS1 FISH", "PTMP0141", "10 days", "Sanger + FISH", "FFPE",
   "The 3 key drivers (EGFR, ALK, ROS1) together.", "At diagnosis of advanced NSCLC.", "\"The three most important lung drivers in one order.\""),
  ("ALK / EML4 Rearrangement by FISH", "PTMP0043", "9 days", "FISH", "FFPE tumour block",
   "Confirms ALK-positive lung cancer.", "Before ALK-targeted tablets.", "\"ALK-positive patients get ALK tablets.\""),
  ("ROS-1 Rearrangement by FISH", "PTMP0044", "9 days", "FISH", "FFPE tumour block",
   "Confirms ROS1-positive lung cancer.", "Before ROS1-targeted tablets; to confirm a positive ROS1 IHC.", "\"ROS1-positive patients get ROS1 tablets.\""),
  ("MET Gene Amplification by FISH", "PTMP0114", "9 days", "FISH", "FFPE tumour block",
   "Detects MET amplification.", "Resistance after EGFR tablets; MET-targeted options.", "\"When EGFR tablets stop working, check MET.\""),
  ("PD-L1 SP263", "PTHC0151", "5 days", "IHC (Ventana)", "FFPE tumour block",
   "Measures PD-L1 on the tumour.", "To decide eligibility for immunotherapy.", "\"Immunotherapy eligibility in 5 days.\""),
  ("ALK (D5F3) IHC", "confirm", "5 days", "IHC (Ventana)", "FFPE tumour block",
   "Fast screening for ALK.", "When a quick ALK answer is needed.", "\"ALK screening in 5 days.\""),
  ("ROS1 (D4D6) IHC", "confirm", "5 days", "IHC (Ventana)", "FFPE tumour block",
   "Fast screening for ROS1; a positive result is confirmed by FISH.", "As a quick first ROS1 check.", "\"Screen fast; confirm positives by FISH.\"")]),
 ("sg04", "7f98f9c3-290051.mp4", "Breast, Ovarian & Hereditary Cancer", "Medical oncologists, breast surgeons, gynae-oncologists, gynaecologists",
  "ER/PR/HER2 for every breast cancer. HER2 IHC 2+ goes to HER2 FISH.", [
  ("BRCA 1 & BRCA 2 Germline Sequencing", "PTMP0058", "25 days", "NGS", "EDTA whole blood",
   "Finds inherited BRCA1/2 changes.", "Breast or ovarian cancer patient, or strong family history; before PARP drugs; family testing.",
   "\"One result helps the patient (PARP drugs) and her family.\""),
  ("BRCA 1 & BRCA 2 Somatic Mutation Test", "PTMP0091", "25 days", "NGS", "FFPE tumour block",
   "Finds BRCA changes inside the tumour (e.g. ovarian cancer).", "To decide PARP drug eligibility.", "\"Tumour BRCA can open PARP drugs even when blood BRCA is normal.\""),
  ("BRCA1 & BRCA2 Advanced Panel (NGS + MLPA)", "PTMP0152", "23 days", "NGS + MLPA", "EDTA blood / FFPE",
   "Most complete BRCA test: also finds large deletions.", "When a full BRCA answer is needed.", "\"Sequencing plus MLPA: deletions are not missed.\""),
  ("Breast Cancer Comprehensive Panel (BRCA 1 & 2) by NGS", "PTMP0059", "15 days", "NGS", "EDTA blood / FFPE",
   "BRCA plus other breast cancer genes.", "Breast cancer patients or families needing more than BRCA.", "\"More genes, 15 days.\""),
  ("PIK3CA Mutation Screening", "PTMP0093", "12 days", "Real time PCR", "FFPE tumour block",
   "Finds PIK3CA mutations.", "HR-positive, HER2-negative advanced breast cancer: before a PIK3CA-targeted drug.", "\"PIK3CA result decides the targeted drug.\""),
  ("Homologous Recombination Deficiency (HRD Assay)", "PTMP0253", "20 days", "NGS + genomic scarring", "FFPE tumour block",
   "Shows who benefits from PARP drugs beyond BRCA.", "Ovarian cancer, when planning maintenance therapy.", "\"Finds PARP-eligible patients that BRCA alone misses.\""),
  ("HRR Gene Panel - Germline", "PTMP0129", "15 days", "NGS", "EDTA whole blood",
   "Homologous recombination repair genes.", "Prostate, ovarian, breast and pancreatic cancer: for PARP drugs.", "\"One panel across four cancers for PARP eligibility.\""),
  ("HER2/neu Amplification by FISH", "PTMP0003", "18 days", "FISH", "FFPE tumour block",
   "Confirms HER2 status.", "When HER2 IHC is 2+ (equivocal).", "\"Every IHC 2+ needs FISH before deciding anti-HER2 therapy.\""),
  ("Hereditary Cancer Risk Panel", "PTMP0201", "21 days", "NGS", "EDTA whole blood",
   "Checks many hereditary cancer syndromes.", "Cancer at a young age, or many relatives with cancer.", "\"One test for many family cancer syndromes.\""),
  ("Breast Panel - ER, PR, HER2, Ki67", "PTHC0158", "5 days", "IHC (Ventana)", "FFPE tumour block",
   "Receptor status and growth rate.", "Every new breast cancer: hormone therapy, anti-HER2, growth rate.", "\"The basic panel every breast cancer needs, in 5 days.\""),
  ("Breast Panel - ER, PR, HER2", "PACK0009", "5 days", "IHC (Ventana)", "FFPE tumour block",
   "Basic receptor status of breast cancer.", "Every new breast cancer.", "\"Receptor status in 5 days.\"")]),
 ("sg05", "c2442785-290052.mp4", "GI & Colorectal Cancer", "Medical oncologists, GI surgeons, gastroenterologists",
  "Every new colorectal cancer: MMR / MSI. Metastatic: RAS + BRAF before anti-EGFR drugs.", [
  ("BRAF V600E Mutation Analysis", "PTMP0057", "10 days", "Real time PCR / Sanger", "FFPE tumour block",
   "Detects BRAF V600E.", "Metastatic colorectal cancer: prognosis and BRAF-targeted drugs.", "\"BRAF changes prognosis and opens targeted options.\""),
  ("KRAS (Codon 12, 13, 61) Mutation Analysis", "PTMP0048", "13 days", "Real time PCR / Sanger", "FFPE tumour block",
   "Checks KRAS status.", "Before anti-EGFR drugs (cetuximab / panitumumab) in colorectal cancer.", "\"RAS must be known before anti-EGFR drugs.\""),
  ("NRAS (Codon 12, 13, 61) Mutation Analysis", "PTMP0049", "15 days", "Real time PCR / Sanger", "FFPE tumour block",
   "Checks NRAS status (same purpose as KRAS).", "Before anti-EGFR drugs.", "\"Complete the RAS picture.\""),
  ("KRAS & NRAS Combined Mutation Panel", "PTMP0146", "15 days", "Real time PCR / Sanger", "FFPE tumour block",
   "Full RAS status in one test.", "Before anti-EGFR drugs.", "\"Full RAS in one order.\""),
  ("Colorectal Targeted NGS Panel (KRAS / NRAS / BRAF / PIK3CA)", "PTMP0169", "20 days", "NGS", "FFPE tumour block",
   "Four key colorectal genes together.", "Metastatic colorectal cancer work-up.", "\"Four genes, one block, one report.\""),
  ("ColoComprehensive (MSI + BRAF + KRAS + NRAS)", "confirm", "20 days", "IHC + NGS", "FFPE block + EDTA blood",
   "Complete colon work-up including immunotherapy eligibility and Lynch screening.", "New colorectal cancer needing a full work-up.", "\"Everything the colon cancer patient needs in one order.\""),
  ("Microsatellite Instability (MSI) by PCR / CE", "PTMP0143", "13 days", "Fragment analysis", "FFPE block + blood",
   "Measures MSI.", "Immunotherapy eligibility and Lynch syndrome screening.", "\"MSI-high opens immunotherapy and flags Lynch families.\""),
  ("GIST Targeted Panel (c-KIT & PDGFRA)", "PTMP0184", "23 days", "NGS", "FFPE tumour block",
   "KIT and PDGFRA mutations in GIST.", "GIST: predicts response to imatinib and other drugs.", "\"Mutation type predicts imatinib response.\""),
  ("MSI Panel - IHC (MMR proteins)", "PTHC0042", "5 days", "IHC (Ventana)", "FFPE tumour block",
   "Mismatch-repair protein check.", "Every new colorectal cancer.", "\"Fast MMR check in 5 days.\"")]),
 ("sg06", "51b0746c-290053.mp4", "Neuro-Oncology", "Neurosurgeons, neuro-oncologists, radiation oncologists, neuropathologists",
  "WHO 2021 brain tumour classification needs these molecular tests for the final diagnosis.", [
  ("CSF Cell-Free Tumour DNA", "confirm", "ask lab", "NGS", "CSF",
   "Reads tumour DNA in spinal fluid.", "When a brain tumour biopsy is not possible.", "\"A diagnosis option when the tumour cannot be biopsied.\""),
  ("Histone Mutation Analysis (H3K27M, H3G34)", "confirm", "ask lab", "IHC / NGS", "FFPE tumour block",
   "Histone mutations in gliomas.", "Midline and diffuse hemispheric gliomas, often in children and young adults.", "\"Needed for the WHO 2021 diagnosis.\""),
  ("KIAA1549 : BRAF Fusion (Pilocytic Astrocytoma)", "confirm", "ask lab", "Break-apart FISH", "FFPE tumour block",
   "Detects the KIAA1549-BRAF fusion.", "To confirm pilocytic astrocytoma, mostly in children.", "\"Confirms the diagnosis in childhood tumours.\""),
  ("BRAF V600E Mutation Analysis", "confirm", "ask lab", "IHC / Real time PCR / Sanger", "FFPE tumour block",
   "Detects BRAF V600E.", "Some gliomas, where BRAF-targeted drugs are possible.", "\"Opens a targeted option.\""),
  ("EGFR Amplification", "confirm", "ask lab", "Dual FISH", "FFPE tumour block",
   "EGFR amplification in brain tumours.", "As a molecular feature of glioblastoma.", "\"Part of the glioblastoma molecular picture.\""),
  ("CDKN2A / 2B Homozygous Deletion", "confirm", "ask lab", "Dual FISH", "FFPE tumour block",
   "Detects CDKN2A/B deletion.", "Grading IDH-mutant astrocytoma (grade 4 if deleted).", "\"Changes the grade, so it changes treatment.\""),
  ("IDH1 / IDH2 Sequencing (Adult Diffuse Glioma)", "confirm", "ask lab", "Sanger", "FFPE tumour block",
   "IDH status of gliomas.", "Classifies adult glioma and predicts outlook.", "\"The first molecular question in every adult glioma.\""),
  ("TERT Gene Promoter Mutation Analysis", "confirm", "15 days", "Sanger", "FFPE tumour block",
   "TERT promoter mutations.", "Glioblastoma and oligodendroglioma classification.", "\"Completes the WHO 2021 classification.\""),
  ("MGMT Promoter Methylation Analysis", "confirm", "15 days", "RQ-PCR", "FFPE tumour block",
   "MGMT methylation status.", "Glioblastoma: predicts benefit from temozolomide chemo.", "\"Tells whether temozolomide is likely to help.\""),
  ("1p/19q Deletion by FISH (Oligodendroglioma)", "PTMP0195", "12 days", "Dual FISH", "FFPE tumour block",
   "1p/19q co-deletion.", "To confirm oligodendroglioma.", "\"Confirms oligodendroglioma.\"")]),
 ("sg07", "eda719a5-290054.mp4", "Pan-Cancer, Liquid Biopsy & Pathology", "Medical oncologists, pathologists, surgical oncologists",
  "No tissue? Offer liquid biopsy. Need speed? Oncomine 50-gene panel in 7-10 days.", [
  ("Solid Tumors Focus Fusion Panel (52 genes)", "PTMP0221", "20 days", "NGS", "FFPE tumour block",
   "Gene fusions (ALK, ROS1, RET, NTRK...) across solid tumours.", "Solid tumours where a fusion could open a targeted drug.", "\"Fusion drugs work across cancer types; find the fusion first.\""),
  ("Oncocept Solid Single Gene (POLE)", "PTMP0168", "15 days", "NGS", "FFPE tumour block",
   "POLE status.", "Endometrial cancer molecular classification.", "\"Needed to classify endometrial cancer.\""),
  ("Comprehensive Genomic Profiling (CGP / OCA Plus, 500+ genes)", "PTMP0181", "35 days", "Comprehensive NGS", "FFPE tumour block",
   "500+ cancer genes.", "Advanced or rare cancers when standard options are exhausted.", "\"When nothing else is left, look at every gene.\""),
  ("Liquid Biopsy Comprehensive Pan-Cancer Panel (cfDNA)", "PTMP0167", "20 days", "NGS", "Streck blood (10 ml)",
   "Cancer genes from blood.", "When tissue is not available; monitoring and resistance.", "\"Tumour genes from a blood sample.\""),
  ("Liquid Biopsy 34 Genes (NGS)", "confirm", "ask lab", "NGS", "Streck blood (10 ml)",
   "Focused blood-based panel.", "When a focused blood panel is enough.", "\"A focused option from blood.\""),
  ("Liquid Biopsy 104 Genes (NGS)", "confirm", "ask lab", "NGS", "Streck blood (10 ml)",
   "Broader blood-based panel.", "When more genes are needed from blood.", "\"Broader coverage from blood.\""),
  ("Oncomine Precision Assay (50 gene panel), tissue", "confirm", "7-10 days", "NGS", "FFPE tumour block",
   "Fast 50-gene solid tumour panel.", "When speed matters.", "\"50 genes in 7-10 days.\""),
  ("Oncomine Precision Assay (50 gene panel), blood", "confirm", "7-10 days", "NGS", "Streck blood (10 ml)",
   "Same 50-gene panel from blood.", "Fast results when tissue is not available.", "\"The fast panel, from blood.\""),
  ("PDGFR Alpha (4q12) Rearrangement by FISH", "PTMP0173", "9 days", "FISH", "FFPE tumour block",
   "PDGFRA rearrangement.", "Blood cancers with high eosinophils.", "\"Imatinib-responsive: worth finding.\""),
  ("Final Diagnosis Panel", "PTHC0036", "5 days", "IHC (Ventana)", "FFPE tumour block",
   "Tumour typing by IHC.", "When the histology is unclear.", "\"Settles the diagnosis in 5 days.\""),
  ("IHC - Single Marker (any)", "PTHC0003", "5 days", "IHC (Ventana)", "FFPE tumour block",
   "Any one marker the pathologist needs.", "When a single extra marker is needed.", "\"Any single marker, 5 days.\"")]),
 ("sg08", "db90f527-290055.mp4", "Rare Disease: Exome & Genome", "Paediatricians, paediatric neurologists, neurologists, geneticists, IVF specialists",
  "After an exome finds a variant, offer family testing: cheaper and faster.", [
  ("NX GEN Whole Exome Sequencing", "PTMP0130", "21 days", "NGS", "EDTA whole blood",
   "Reads all ~20,000 genes.", "Suspected genetic disorder with no diagnosis.", "\"One test instead of many single-gene tests.\""),
  ("Whole Exome Sequencing, POC", "PTMP0212", "21 days", "NGS", "Products of conception",
   "Exome on pregnancy-loss tissue.", "Pregnancy loss or fetal anomaly.", "\"Finds the cause to plan the next pregnancy.\""),
  ("NX GEN Clinical Whole Exome Sequencing", "PTMP0137", "21 days", "NGS", "EDTA whole blood",
   "Focus on known disease-causing genes.", "Clinical suspicion of a genetic disorder.", "\"Focused on genes known to cause disease.\""),
  ("WES + Mitochondrial Genome Sequencing", "PTMP0218", "21 days", "NGS", "EDTA whole blood",
   "Exome plus the mitochondrial genome.", "Suspected mitochondrial disease: muscle, brain and energy problems.", "\"Covers nuclear and mitochondrial genes together.\""),
  ("Clinical Exome Sequencing (CES / Omixome 5,000 genes)", "PTMP0137 (confirm)", "48 days", "NGS", "EDTA whole blood",
   "About 5,000 disease genes.", "Clinical suspicion of a genetic disorder.", "\"Same code as above: confirm with the lab.\""),
  ("Shotgun Sequencing", "confirm", "ask lab", "NGS", "EDTA whole blood",
   "Genome-level sequencing.", "When genome-level testing is needed: confirm details with the lab.", "\"Confirm scope and report time with the lab.\""),
  ("Single Variant Validation by Sanger Sequencing", "PTMP0239", "28 days", "Sanger", "EDTA whole blood",
   "Confirms one known variant.", "After an exome finds a variant.", "\"Confirm the finding before acting on it.\""),
  ("Additional Family Member Testing (Sanger) - 2 variants", "PTMP0103", "28 days", "Sanger", "EDTA whole blood",
   "Tests parents or siblings for the family's known variants.", "After a variant is found in the family.", "\"Family testing is cheaper and faster than a new exome.\"")]),
 ("sg09", "ac9a286b-290056.mp4", "Rare Disease: Neuromuscular & Neurodegenerative", "Neurologists, paediatric neurologists, paediatricians",
  "Testing healthy relatives (e.g. Huntington) needs genetic counselling first.", [
  ("Spinal Muscular Atrophy (SMN1 / SMN2 Exon 7/8 by MLPA)", "PTMP0073", "15 days", "MLPA", "EDTA whole blood",
   "Counts SMN1 and SMN2 copies.", "Floppy, weak baby or child: SMA diagnosis.", "\"Treatment exists now; early diagnosis matters.\""),
  ("DMD / BMD Gene Deletion / Duplication (79 exons MLPA)", "PTMP0235", "15 days", "MLPA", "EDTA whole blood",
   "Deletions and duplications in the dystrophin gene.", "Boy with frequent falls, big calves, high CK.", "\"High CK in a boy: test DMD.\""),
  ("Spinocerebellar Ataxia Panel (SCA 1, 2, 3, 6, 7, 12)", "PTMP0081", "20 days", "TP-PCR", "EDTA whole blood",
   "Repeat expansions in the common SCA genes.", "Adult with progressive imbalance, especially with family history.", "\"Six SCA types in one test.\""),
  ("SCA Single Type Targeted Confirmation", "PTMP0082", "15 days", "TP-PCR", "EDTA whole blood",
   "Tests one known SCA type.", "When the family's SCA type is known in a relative.", "\"Targeted and quicker for families.\""),
  ("Huntington Disease (HTT CAG repeats)", "PTMP0110", "23 days", "TP-PCR", "EDTA whole blood",
   "Counts HTT CAG repeats.", "Involuntary movements, behaviour change, family history.", "\"Counselling first for healthy relatives.\""),
  ("Friedreich Ataxia (FXN GAA repeats)", "PTMP0079", "18 days", "PCR / fragment", "EDTA whole blood",
   "Counts FXN GAA repeats.", "Young-onset ataxia, absent reflexes, scoliosis, heart muscle disease.", "\"Young ataxia with a heart problem: think Friedreich.\""),
  ("DMPK Repeat Expansion (Myotonic Dystrophy)", "confirm", "ask lab", "TP-PCR", "EDTA blood",
   "Counts DMPK repeats.", "Cannot release grip (myotonia), weakness, early cataract.", "\"Grip that will not let go: test DMPK.\"")]),
 ("sg10", "f32fcf32-290057.mp4", "Rare Disease: Neurodevelopmental & Syndromic", "Paediatricians, paediatric neurologists, developmental paediatricians, cardiologists",
  "Unclear syndrome? Microarray first, then exome. Specific signs: targeted test.", [
  ("Fragile-X Syndrome (FMR1 repeat expansion)", "PTMP0078", "18 days", "TP-PCR", "EDTA whole blood",
   "Counts FMR1 CGG repeats.", "Learning difficulty or autism, especially in boys; family history.", "\"Exome can miss it: order it by name.\""),
  ("DiGeorge Syndrome (22q11.2 microdeletion) by FISH", "PTMP0177", "10 days", "FISH", "Heparin blood / amniotic fluid",
   "Detects the 22q11.2 deletion.", "Heart defect, cleft palate, low calcium, frequent infections.", "\"Heart defect plus low calcium: check 22q11.\""),
  ("Williams Syndrome (7q11.23 microdeletion) by FISH", "confirm", "5 days", "FISH", "Heparin blood / amniotic fluid",
   "Detects the 7q11.23 deletion.", "Typical face, narrowed aorta, very friendly nature, high calcium.", "\"A 5-day answer for a typical picture.\""),
  ("Prader-Willi / Angelman Syndrome by MS-MLPA", "confirm", "20 days", "MS-MLPA", "EDTA whole blood",
   "Methylation test for 15q11-q13.", "PWS: floppy newborn, later overeating. AS: severe delay, no speech, happy.", "\"One test covers both syndromes.\""),
  ("Beckwith-Wiedemann / Russell-Silver Syndrome (MS-MLPA)", "confirm", "ask lab", "MS-MLPA", "EDTA blood",
   "Methylation test for 11p15.", "BWS: overgrowth, big tongue, low sugar. RSS: poor growth.", "\"Growth too much or too little: test 11p15.\""),
  ("Rett Syndrome (MECP2) Deletion / Duplication", "confirm", "ask lab", "MLPA", "EDTA blood",
   "MECP2 deletions and duplications.", "Girl losing skills, hand-wringing; MECP2 duplication in boys.", "\"About 1 in 10 Rett changes need MLPA to find.\""),
  ("Rett Syndrome Gene Panel", "confirm", "ask lab", "NGS", "EDTA blood",
   "Sequencing of Rett-related genes (MECP2, CDKL5, FOXG1).", "Classic or atypical Rett picture.", "\"Covers atypical Rett genes too.\"")]),
 ("sg11", "2791d537-290058.mp4", "Haemoglobinopathies & Bleeding Disorders", "Haematologists, paediatricians, gynaecologists, IVF specialists",
  "HPLC first. Both partners carriers: DNA test of both, then CVS at 11-14 weeks.", [
  ("Thalassemia v2 NGS", "confirm", "21 days", "NGS", "EDTA whole blood",
   "Complete alpha and beta globin genes in one test.", "Complex cases.", "\"Both globin genes in one test.\""),
  ("Alpha Thalassemia Mutation Analysis", "PTMP0105", "15 days", "Sanger + MLPA", "Amniotic fluid / blood / CVS",
   "Alpha globin gene changes.", "Small red cells with normal HbA2 and iron; couples; prenatal.", "\"Small red cells, normal HbA2 and iron: think alpha.\""),
  ("Beta Thalassemia Mutation Analysis", "PTMP0074", "16 days", "Sanger + MLPA", "Amniotic fluid / blood / CVS",
   "Beta globin gene changes.", "Carrier couple and prenatal diagnosis (CVS / amniocentesis).", "\"Carrier couple: DNA test both, then prenatal (disease only, PCPNDT).\""),
  ("Hemophilia Complete Work-up (F8 / F9 seq + inversions)", "confirm", "ask lab", "NGS + PCR", "EDTA whole blood",
   "F8 and F9 genes including inversions.", "Haemophilia A or B: diagnosis and carrier testing of female relatives.", "\"Finds carrier women in the family.\"")]),
 ("sg12", "4875556e-290059.mp4", "Endocrine, Metabolic & GI Genetics", "Endocrinologists, diabetologists, gastroenterologists, paediatricians, pulmonologists",
  "Young diabetic with strong family history and no antibodies: think MODY.", [
  ("Maturity Onset Diabetes of the Young (MODY) by NGS", "PTMP0216", "21 days", "NGS", "EDTA whole blood",
   "MODY genes.", "Diabetes at a young age, strong family history, antibody-negative.", "\"Some MODY types need tablets, not insulin.\""),
  ("Hereditary Pancreatitis Panel", "confirm", "ask lab", "NGS", "EDTA whole blood",
   "Pancreatitis genes.", "Repeated or chronic pancreatitis at a young age.", "\"Young recurrent pancreatitis deserves a genetic look.\""),
  ("Congenital Adrenal Hyperplasia (CYP21A2 seq + MLPA)", "PTMP0225", "10 days", "Sanger + MLPA", "EDTA whole blood",
   "CYP21A2 gene changes.", "Salt-losing newborn, high 17-OHP, early puberty; carrier testing.", "\"Confirms CAH and finds carriers.\""),
  ("Cystic Fibrosis Complete Gene Sequencing (CFTR)", "confirm", "ask lab", "NGS", "EDTA whole blood",
   "Full CFTR gene sequencing.", "Repeated chest infections, salty sweat, poor digestion; some male infertility.", "\"Full gene, not just common mutations.\""),
  ("Gilbert Syndrome (UGT1A1 promoter mutation)", "PTMP0155", "10 days", "Sanger", "EDTA whole blood",
   "UGT1A1 promoter variant.", "Mild, harmless jaundice; also before irinotecan chemo.", "\"Reassures patients and guides irinotecan.\"")]),
 ("sg13", "c7616cd0-290060.mp4", "Pharmacogenomics", "Psychiatrists, cardiologists, neurologists, oncologists, gastroenterologists, rheumatologists",
  "Test BEFORE the first dose: one result is valid for life.", [
  ("UniPharmGx 19-Gene Comprehensive PGx Panel", "confirm", "ask lab", "NGS", "EDTA whole blood",
   "One test that guides many medicines.", "Mental health, heart, pain and more.", "\"One test, valid for life, for many medicines.\""),
  ("MTHFR Mutations C677T / A1298C", "PTMP0089", "5 days", "PCR", "EDTA whole blood",
   "MTHFR variants.", "High homocysteine work-up, as the doctor advises.", "\"5-day result when the doctor asks for it.\""),
  ("TPMT and NUDT15 Gene Analysis (Thiopurine toxicity)", "PTMP0178", "15 days", "Sanger / PCR", "EDTA whole blood",
   "TPMT and NUDT15 variants.", "Before azathioprine or 6-mercaptopurine: avoids marrow suppression.", "\"Prevents dangerous low blood counts.\""),
  ("DPYD Gene Mutation Analysis (5-FU toxicity)", "PTMP0151", "11 days", "RT-PCR / Sanger", "EDTA whole blood",
   "DPYD variants.", "Before 5-FU or capecitabine chemo: avoids severe toxicity.", "\"Test before the first dose of 5-FU.\"")]),
]

def dur(f):
    s = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    return f"{int(s // 60)}:{int(round(s % 60)):02d}"

def main():
    os.chdir(ROOT)
    js = open("studio/tools/data.js", encoding="utf-8").read()
    if 'id:"sales"' not in js:
        js = js.replace('  {id:"high", name:"High-End Tests",', '  {id:"sales", name:"Sales Test Guides", blurb:"Suraksha Sales Academy: which tests, why, when, and how to pitch them to doctors."},\n  {id:"high", name:"High-End Tests",')
    entries, keys = "", ""
    for sid, fn, title, meet, tip, tests in G:
        src = f"{A}/{fn}"
        if not os.path.exists(f"site/v/{sid}.mp4"):
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", src, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "30", "-preset", "veryfast",
                            "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", f"site/v/{sid}.mp4"], check=True)
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", "2.5", "-i", src, "-frames:v", "1", "-vf", "scale=360:640", "-q:v", "4", f"site/p/{sid}.jpg"], check=True)
        if f'id:"{sid}"' in js: continue
        x = [["Doctors to meet", meet], ["Pitch tip", tip]]
        for (n, code, tat, meth, samp, why, when, pitch) in tests:
            c = "Code to confirm in the Rate Finder" if code.startswith("confirm") else f"Code {code}"
            x.append([n, f"What: {why} When: {when} Sales pitch: {pitch} [{c} · {tat} · {meth} · {samp}]"])
        s = (f"Sales team test guide: {len(tests)} tests in {title}. For each test: what it checks, when doctors use it, the sample, report time, "
             f"method and how to pitch it. Doctors to meet: {meet}. Always confirm MRP and code in the Rate Finder.")
        entries += "{id:" + json.dumps(sid) + ', c:"sales", t:' + json.dumps(f"Sales Guide: {title}") + ', l:"English", d:"' + dur(src) + '",\n  s:' + json.dumps(s) + ",\n  x:" + json.dumps(x, ensure_ascii=False) + "},\n "
        keys += f' {sid}:' + json.dumps("sales guide, " + title.lower() + ", " + ", ".join(t[0] for t in tests) + ", Suraksha, Kolkata") + ",\n"
    js = js.replace('{id:"tumour", c:"tests"', entries + '{id:"tumour", c:"tests"', 1)
    js = js.replace(' tumour:"', keys + ' tumour:"', 1)
    open("studio/tools/data.js", "w", encoding="utf-8").write(js)
    print("added", js.count('c:"sales"'))

if __name__ == "__main__":
    main()
