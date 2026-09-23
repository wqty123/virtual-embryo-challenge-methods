# References & External Links

Created: 2026-09-23. Registers the **ideas we referenced** and the **external tools, data and models we used/evaluated** in the virtualembryo challenge, each with a link, use, compliance conclusion and final disposition. All links are clickable and traceable; sources without a concrete URL are labeled by name and provenance only — no links are fabricated.

<p align="center"><a href="reference-links.md">中文</a> · English</p>

---

## I. Official resources (the competition itself)

| Resource | Link | Use |
|---|---|---|
| Challenge home | https://virtualembryo.ai/challenge | rules, data, submissions, leaderboard |
| Rules | https://virtualembryo.ai/challenge/rules | compliance hard line (held-out forbidden, §10) |
| Data description/download | https://virtualembryo.ai/challenge/data | per-board h5ad download and format contract |
| Evaluation | https://virtualembryo.ai/challenge/evaluation | per-board metric definitions (de/dir/mmd/vario…) |
| Leaderboard | https://virtualembryo.ai/challenge/leaderboard | real-board readings for the five boards |
| Submit | https://virtualembryo.ai/challenge/submit | upload h5ad, consumes quota |
| Data manifest | https://kg.virtualembryo.ai/challenge/data/manifest | official file list |
| Data direct links | https://kg.virtualembryo.ai/challenge/data/link?key=<KEY> | single-file download |
| Knowledge graph (KG) | https://kg.virtualembryo.ai/kg | platform-built KG (KEGG etc.) — **falsified**: intersection with true DE is empty |
| Official scorer | https://github.com/aristoteleo/veckit | **local scorer** (`pip install git+https://github.com/aristoteleo/veckit.git@46d41e63`), runs official scores in-process; **can even score types that never appeared** (mmd/vario are label-free; de/dir go through pseudobulk and do not depend on labels) |
| Official baselines | https://github.com/aristoteleo/vec_baselines | official example baselines |

## II. Community tools (cloned / referenced, all with links)

| Tool | Link | Use and disposition |
|---|---|---|
| **vecbench** | https://github.com/AJK0921/vecbench | Local scoring / noise floor / holdout-ranking tool. **Heavily used**: `vec_noisefloor.py --calibrate` calibrated the T3 threshold to 1.48 (not 0.64); measured compound noise is 1.4–1.6× the independence assumption; source of the TF "anti-correlated instrument" warning |
| **vec-scalecheck** | https://github.com/wqty123/vec-scalecheck | Submission format/size checker, **self-built repo** (cloned into the local workspace and modified), README with badges and docs; submitted for the Community Contribution award |
| **vec-submit-check** | https://github.com/gh-dv-openclaw/vec-submit-check | Content-level submission check, cloned into the local workspace |
| **vec-community-kit** | https://github.com/xxx12e/vec-community-kit | Five-in-one community kit (board-contract validator / local scoring / format check / checklist), cloned into the local workspace; includes `vec_local_score` running veckit on pseudo-splits |
| **vec-evidence-check** | https://github.com/bestdeeplearning-star/vec-evidence-check | Evidence-file assembly checker (implemented per official rule §9 and veckit PR records); community contribution (pending review) |
| **EmbryoMatch** | https://github.com/ShaoliZhao/virtual-embryo-EmbryoMatch | Stage-aware external-data recommender: matches by cell state and organ maturity rather than fixed embryonic-day conversion. Contains 10 literature-evidence entries, 11 recommendations, runnable stage-alignment baselines (`scripts/recommend.py`, `align_states.py`). We referenced its stage-alignment idea |
| **Intuition Lab** | https://github.com/i-habib/virtual-embryo-community/tree/main/intuition-lab | Scorer diagnostic experiment set: fix the prediction, break only one variable, watch which metric moves — our T1/T2/T3 structure theorems (de/dir/sev depend only on pseudobulk; vario depends on within-cell gene-pair differences) share this idea |
| **VEC First-Submission Kit** | https://github.com/cadentann/virtual-embryo-community-kit | First-submission walkthrough + read-only h5ad precheck (pseudobulk_shift teaching + structural QC); modules: task1_walkthrough / data_inspector |
| **VirtualEmbryo-basline** | https://github.com/Shashwat-srivastav/VirtualEmbryo-basline | Type-conditional interpolation baseline (T2-style: predict an unseen stage between two observed stages), stronger than copy_nearest |

## III. Pretrained models (compliance-audited, per-item conclusion)

| Model | Source | Training corpus | Compliance conclusion | Disposition |
|---|---|---|---|---|
| **TF-Sapiens** | https://github.com/czi-ai/transcriptformer weights https://czi-transcriptformer.s3.amazonaws.com/weights/{model}.tar.gz | 57M cells **purely human** (mouse flagged −) | **✅ usable** | End-to-end runs locally and on the cloud; as a criterion on T1 it is **anti-correlated −0.69, criterion line closed**; repurposed as embedding inference for T3 carrier dilution; decoder framework built awaiting T1 embeddings |
| **TranscriptFormer** (non-Sapiens) | https://github.com/czi-ai/transcriptformer | CZI CellxGene Census, cross-species cross-stage, **includes mouse embryo time course** | **⛔ high risk** (disabled by default) | unused |
| **UCE** (Universal Cell Embedding) | internal audit record (see appendix index) | 33.9M cells human+mouse, 285 datasets | **⛔ empirically disabled** | unused |
| **scGPT whole-human** | internal audit record (see appendix index) | 33M pure-human CellxGene | **✅ usable** | not deployed (pure-human transfer value limited) |
| **Geneformer** | internal audit record (see appendix index) | Genecorpus-30M, mostly human | **✅ usable** | not deployed |
| **GeneCompass** | Cell Research 2024 (cross-species foundation model) | cross-species | evaluated only | unused (research note) |
| **Gene-Chronos** | pretrained single-cell foundation model for developmental-time inference | — | evaluated only | unused |
| **CAMEX** | https://www.nature.com/articles/s41467-026-69696-3 | organ-development alignment method | reference only | stage-alignment idea referenced (cited by EmbryoMatch) |

## IV. Algorithms / methods (referenced ideas; parameters fit on our own data; unconditional usability)

| Method | Reference | Use / conclusion |
|---|---|---|
| **WOT (Waddington-OT)** | https://github.com/broadinstitute/wot (official transport matrix and growth rates) | Composition extrapolation **closed loop**: growth_by_type/descendant_fraction/transport computed; growth rates alone cannot predict new types appearing (46% of new types do not exist in the early stage); lineage velocity corr +0.954 with the global direction, no independent information |
| **OT / optimal transport** | moscot / CellOT | T1 otmix/otfix family: after mask repair all four axes look good locally, but under independent truth the net −0.003 is an artifact; OT v2 16-seed paired test: d2 gain disappears (p=0.97) |
| **scVelo / CellRank / Dynamo** | algorithm class | **data-contract falsified**: all h5ad lack spliced/unspliced layers; Dynamo needs splicing/metabolic-labeling data, not applicable; Spateo needs spatial components, not applicable; Dynast needs 4sU, not applicable; Monocle/Bio-Babel only give pseudo-time axes |
| **GPMM / Deformetrica / Esteban** | geometric-deformation methods | **falsified 4× on the real board**: changing morphology always collapses (selday/r6/vmorph/comp all below scale_only 54.51); Deformetrica's extrapolation risk is exactly our situation |
| **SPHARM-PDM / ASM / PGA / ARAP / AtlasNet / NRICP** | point-cloud geometry methods | excluded (need population samples / meshes / correspondences / big data) |
| **Harmony / scVI** | batch integration | explicitly **not used** (would treat real temporal change as batch and erase it); harmonization only does gene-wise rank / program-shape alignment |
| **Bures subspace / PopTransport / persistent wot macrostate** | method names of top leaderboard teams | **referenced idea**: top teams work on distribution/Bures geometry and population transport, not cell-level displacement (analysis note) |
| **moscot structure extrapolation / MIOFlow** | algorithm class | **REJECT / kill test below threshold**, conservative-family promotion route closed |
| **CellChat / ligand-receptor** | — | evaluated only, unused |
| **KEGG knowledge graph** | platform built-in | **falsified**: KG covers 108/32285, true DE set 64/32285, intersection empty; table expansion worse |

## V. External datasets (per-item compliance audit)

| Data | Source | Use / conclusion |
|---|---|---|
| **GSE208162** (E12.5 ventricle, Gata4 KO/Het) | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208162 | **T3 training-only (officially labeled) usable**; downloaded and parsed 4 h5ad; 267 panel genes orthogonal to the Mab21l2 response (0.180 = random), prediction < 1 point |
| **GSE282547** (developing heart Visium) | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE282547 | E14.5 heart, 500/500 genes full coverage + real coordinates, **passed the validator recommendation** (external-data-catalog) |
| **GSE247450** (MERFISH endothelium) | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247450 | E9.5, narrow 68/500-gene panel, x/y only; validated but of limited value |
| **sc3D / GSE197353** (Slide-seq) | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE197353 + https://figshare.com/articles/dataset/E9_0_Embryo_h5ad/21695879/1 | **closed (compliance block)**: contains Tbx6 mutants, 38% panel overlap (T1 only 8.3%), 12.2GB not actually run |
| **Extended Mouse Atlas** | https://marionilab.github.io/ExtendedMouseAtlas/ + https://bioinformatics.stemcells.cam.ac.uk/rlh60/Supplemental/ExtendedMouseAtlas/ | **audited**: 430,339 cells; leak test pearson 0.39–0.50 independent source; but contains protected stages, value reduced for corresponding boards |
| **Tabula Muris** | https://registry.opendata.aws/tabula-muris/ | demoted historical candidate (download route not reproduced, and no match for the heart atlas) |
| **Cardoso-Moreira 2019 brain development** | human E-MTAB-6814 / macaque E-MTAB-6813 / mouse E-MTAB-6798 / rat E-MTAB-6811 / rabbit E-MTAB-6782 (ArrayExpress) | main data for the cross-species-curve plan; **mouse column contains protected stages, forbidden for T1**; human/macaque/rat/rabbit usable (for shape alignment) |
| **Human CS7–CS13 spatiotemporal atlas** | HRA007143 / PRJCA025127 (CNGB) | **cleanest external line** (non-mouse, non-held-out); tissue/species mismatch, value pending actual measurement |
| **Jing Naihe Geo-seq** | GSE98101 / GSE104243 | mouse dense time course; **contains protected stages, forbidden for T2** |
| **Mouse gastrulation atlas** | GSE236766 | EmbryoMatch reference |
| **Primate gastrulation atlas** | GSE193007 | EmbryoMatch reference |
| **Developmental transcriptome** | GSE149457 | EmbryoMatch reference |
| **Mouse heart chimera experiments** | GSE236400 | EmbryoMatch stage-comparison reference (chimera effects are not a general mapping) |
| **T3 source** | GSE283967 | EmbryoMatch T3 report reference |
| **GSE278603** (whole embryo) | — | cross-agent direction-consistency check: cosine −0.383 with the global direction; same-stage replicates extremely stable (0.944/0.990) ⇒ the stage direction itself is not extrapolable |
| **Tyser heart raw data** | — | T2 direction-consistency check: cosine −0.046/−0.049, near noise |

> Compliance phrasing note: in the table above, "contains protected stages, forbidden for T1/T2" refers to the held-out stages defined by the official rules (data must not be used for predictions on the corresponding board). This is a compliance judgment and contains no reverse-engineered held-out measurements.

## VI. Data / resource platforms

| Platform | Link | Use |
|---|---|---|
| GEO | https://www.ncbi.nlm.nih.gov/geo/ | main external-data source |
| ArrayExpress | https://www.ebi.ac.uk/biostudies/arrayexpress | cross-species brain-development data |
| CellxGene Discover | https://cellxgene.cziscience.com/ | pretrained-model corpus audit (confirming whether mouse held-out stages are included) |
| CNGB | https://db.cngb.org/ | human CS7–CS13 spatiotemporal atlas |
| Figshare | https://figshare.com/ | convenient sc3D h5ad objects |
| Gene Ontology | https://geneontology.org/docs/go-citation-policy/ | program gene-set scoring (CC BY 4.0; public gene sets, not data) |
| AutoDL (cloud GPU) | cloud GPU platform | TF-Sapiens inference/training; **credentials must never enter the repository** |

## VII. Core "ideas" we referenced (not tools, methodology)

1. **Structure theorem** (common across boards): de/dir/sev depend only on pseudobulk; variogram depends on within-cell gene-pair differences; any per-gene transform that changes pseudobulk ranking necessarily destroys variogram; only replacing/resampling real cells avoids this. → All five boards' best solutions are "real cells + expression untouched".
2. **Carrier dilution** (T3's new-best source): the kb family dilutes the KO ratio with real cells, `kbb_n6000_b055_k65` 66.61.
3. **Maturity soft weighting** (T1 +2.30): resample real cells by direction score (kp7_m_b050 53.67), expression untouched.
4. **Displacement + zero-inflation mask** (T3 counts true mechanism): `np.where(nz, X+d, X)` instead of `X+d` (the reason the kodir/mx/koq five families' vario collapses).
5. **Distribution-level transport vs cell-level displacement** (lesson from top leaderboard teams): Bures geometry, population transport.
6. **Falsify before investing**: every external tool line first gets a data-contract check (scVelo no layers, Dynamo no splicing, Deformetrica parameter explosion, KG empty intersection), then a compliance audit, and only then GPU/quota.

---

## Appendix: related internal documents (filenames kept as an index, not distributed with the repo)

- `COMPLIANCE_CROSS_SPECIES_2026-09-22.md` — per-item compliance judgement on cross-species data
- `PRETRAINED_CORPUS_AUDIT_2026-09-22.md` / `PRETRAINED_MODEL_COMPLIANCE_2026-09-22.md` — pretrained-model corpus checks
- `EXTERNAL_DATA_AUDIT_2026-09-21.md` — external-data list
- `external-data-catalog` (local clone) — external-data validator and SOURCE_TERMS
- `CONCLUSION_2026-09-24.md` / `COMPLIANCE_AND_CLOUD_2026-09-24.md` — sc3D closure, atlas leak conclusions
- `TF_SAPIENS_LINE_2026-09-22.md` — full TF-Sapiens evaluation
- `KG_DIRECTION_FALSIFIED_2026-09-22.md` — KG falsification details
- `CROSS_SPECIES_2026-09-22.md` — cross-species-curve plan
- `FORGOTTEN_LINES_2026-09-23.md` — forgotten-lines ledger (v2)

> The documents above live in a private workspace as the internal evidence chain; the public repo cites only their filenames as an index and contains none of their content.
