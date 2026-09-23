# Pitfalls Log

> All pitfalls are classified into two dimensions: **methodological/biological** (insights about "how to model") and **engineering/process** (insights about "how to submit/record").
> Each entry records: phenomenon → root cause → lesson. All scores come from official scoring returns.

<p align="center"><a href="pitfalls.md">中文</a> · English</p>

---

## I. Methodological / biological

### 1. Global-scalar assumption: the shift family's de_score ceiling
- **Phenomenon**: sweeping every damp of shift (pseudobulk drift, uniform-amplitude scaling across genes) caps de_score at ≈45.3 (48.85 is the peak).
- **Root cause**: real developmental change is per-gene / per-type **heterogeneous**; one scalar parameter cannot describe heterogeneity.
- **Lesson**: de_score specifically judges "a few named genes" — a mean shift can never guess which genes will be named. The real bottleneck is not dimensionality reduction losing features, it is that prediction algorithms are bad at naming individual genes.

### 2. Time-homogeneity assumption falsified: Markov flux collapses
- **Phenomenon**: `markov_flux` (apply the transition rule learned from E8.5→E9.5 to E9.5→E10.5) 44.19, below the floor and below all shift-family scores.
- **Root cause**: the transition rule itself **changes over time** — the E8.5→E9.5 rule cannot be carried to the next step. Two time points cannot learn "the law of how rules change".
- **Lesson**: strong assumptions must be given an "exam paper" (local pseudo-validation on intermediate points) — test whether the assumption holds before spending real-board quota.

### 3. "Large generation amplitude collapses variance": the S-am lesson
- **Phenomenon**: shift + anonymous program mixture 47.34, variogram collapses to 31.7, total below pure shift@1.0.
- **Root cause**: anonymous mixture treats "linear combinations of known programs" as new content; a large amplitude destroys the gene–gene covariance structure.
- **Lesson**: generated content must be small in amplitude, position-controlled, and added last. Per-gene independent extrapolation also destroys vario (gene–gene covariance unconstrained).

### 4. Scatter (noise) falsified
- **Phenomenon**: shift@0.5+s0.5 (scatter probe) 42.29, vario −19 and mmd also drops.
- **Root cause**: adding noise to the prediction directly destroys the distribution structure.
- **Lesson**: noise belongs only in local calibration and variance analysis, never in predictions.

### 5. Convex-hull deadlock: program mixtures can only "interpolate old states"
- **Phenomenon**: all program-mixture types (OT program mixture, anonymous mixture) either score low or destroy vario.
- **Root cause**: linear combinations of known programs can only sample inside the convex hull — the "new states" generated are essentially interpolations of old states, the opposite of the official verdict (seen-bias).
- **Lesson**: to genuinely generate "new categories/states" you must handle birth/death in population composition, not interpolate inside old states.

### 6. "Missing one predicted type = heavy penalty, not a point deduction"
- **Phenomenon**: T1 submissions missing one type drop sharply; mmd_u treats the two cell clouds as distributions, and a missing block forms an obvious hole.
- **Root cause**: the scorer does not know biology, it only knows whether distributions look alike. Filtering out a genuinely new type collapses mmd.
- **Lesson**: cell-type time-window priors can only be used **in reverse** ("filter out types that should not appear"), never forward ("only allow known types to appear") — and we only have one pair of time points, so we cannot even prove the "disappearance law".

### 7. Adding marker axes is wrong (fault-finding conclusion on three user ideas)
- **Phenomenon**: wanted to use "the most specific gene of a cell" as a dimension/marker line for cell types.
- **Root cause**: ① redundancy — true markers are usually high-variance genes whose information is already absorbed by the leading PCA components; ② subjective choice distorts the distance space → spurious clusters; ③ using type-knowledge distances to "validate" type predictions is circular.
- **Lesson**: do not "add axes"; either "change the objective" (supervised projection, LDA-style) or "give marker genes higher weight at the prediction stage".

### 8. "Two points determine a line, not a curve"
- **Phenomenon**: wanted to fit a cell-growth curve and extrapolate (E8.5, E9.5, two points).
- **Root cause**: n points determine at most an n−1 degree polynomial; two points determine a line, not a curve.
- **Lesson**: with few data points, any "curve extrapolation" is guessing; "linear vs exponential" is a false dichotomy (transition rates can be linear while counts still grow exponentially — Kendall 1948 birth–death process).

### 9. T2 extrap board: changing morphology = death
- **Phenomenon**: every extrapolation submission that moves morphology/geometry collapses — `r6b70a20` 38.97, `comp_c100` 32.8, `vmorph_s120` 46.8, `cpfx` (d2_shape 5.7) 52.12; meanwhile **scale/composition-only** `scale_only` 54.51 is the solid best, `w005` 54.43 second.
- **Root cause**: the spatial structure of the extrapolation target (after E9.5) cannot be reliably extrapolated from E8.25/E8.75; touching morphology is necessarily penalized by d2_shape/occupancy_dice.
- **Lesson**: the only correct route on the extrap board = **distribution fidelity first** (full-mark scale + balanced metrics); do not touch morphology.

### 10. Local proxies are untrustworthy: proxy vs real board diverge
- **Phenomenon**: markov local proxy 0.964 (looked safe) → real board 44.19; T2 geometric-metric local ranking is **inverted** vs the real board (v1replica local 89.7 > bgm 71.1, real 50.9 < 57.8); nh/occ local three-point calibration R²=0.025.
- **Root cause**: the local proxy target (E9.5) has a different structure from the real-board target (E10.5); geometric metrics are extremely sensitive to scorer seeds/sampling.
- **Lesson**: **local experiments can only exclude bad candidates, never select good ones**. The real board is the only arbiter; "tellable counts as verifiable" is the proxy's own error.

### 11. Scorer noise floor: real-board backfills must carry a noise band
- **Phenomenon** (calibrated after vecbench integration): same champion file, 6 scorer seeds — de/dir/severity **sd=0 (zero-noise axes)**, mmd_u ±5.75 skill points, variogram ±2.20, energy ±2.27.
- **Lesson**: a single-point mmd/vario difference below 3 points is not evidence; de/dir/sev differences are decisive. Earlier "noise-level" judgements lacked instrument calibration.

### 12. Structure preservation ≠ correct transition direction (covsafe loses on the real board)
- **Phenomenon**: `t1_covsafe_mm_n1249_l25` 48.09 vs production reference shift@2.5 48.85 — only variogram improves (+16.3), de/dir/mmd all drop, headline −0.76.
- **Root cause**: preserving structure (covariance safeguarding) suppresses the real transition.
- **Lesson**: **preserving structure cannot replace a correct future-stage transition direction**. T1's covsafe/appearance/parent-map/sparse-rank/structure-transfer are all closed.

### 13. Small-panel OOF conclusions do not transfer to the 32285 panel (kp7 lesson)
- **Phenomenon**: kp7 maturity-weighted sampling was once rejected by a 500-gene-panel OOF, but the real board gives +2.30 (53.67).
- **Root cause**: small-panel generalization conclusions do not apply to the full 32,285-gene panel.
- **Lesson**: the OOF panel convention must match the real board; (K,c) ranking can only be decided by the real board — structural axes have no reliable local arbiter (F1/F3 sign flips).

### 14. Deep-generation route: insufficient supervision, not conceptual denial
- **Phenomenon**: VGFM / CVAE / diffusion (including residual, carrier-bypass, FiLM-gate, and a dozen other variants) never stably exceed copy-last on the T2 ladder.
- **Root cause**: the currently visible ladder provides **insufficient supervision** for future states; blind sweeps over epoch/hidden/K/noise give no information gain.
- **Lesson**: it is not "deep generation" that is denied — the boundary of data supervision was reached first. Stacking more models is inferior to adding independent data.

### 15. The largest exploitable gap = population composition / state support
- **Phenomenon** (Tyser identifiability decomposition): a mean-only oracle reduces RMSE but destroys the distribution; mean-direction/carrier-residual are limited; the **composition oracle shows the clearest upper bound on variance correlation and sliced Wasserstein**.
- **Root cause**: deployable methods lack enough independent evidence to recover those oracle signals (missing true replicate samples and verifiable birth events).
- **Lesson**: the largest gap is "which cell types appear/disappear", not the expression values themselves.

### 16. T3 transfer family fully falsified
- **Phenomenon**: global Δ (KO@E9.5 − WT@E9.5 applied to the E8.75 carrier) 40.98, vario 49.8→12.2; cardiac restriction 44.36/44.85 (distribution held but de drops below the floor); literature prior (Mab21l2 targets) 45.78, tied with the floor.
- **Root cause**: the Mab21l2-derived response source is **anti-correlated** with Gata4's true response; the "response signal" is not portable across expression channels.
- **Lesson**: T3 must infer the response from real KO data (the mix method); literature/transfer alone is a dead end.

### 17. T3 metric leverage: severity_slope is the big one
- **Phenomenon**: the cmp family breaks the 64.6 plateau after pushing de/sev to 56.3/97.0; the mix family buys mmd by mixing more real cells but sev cannot climb.
- **Root cause**: T3 weights de 0.30 + sev 0.25 = 0.55 vs mmd 0.12 + vario 0.08 = 0.20.
- **Lesson**: **hitting the KO effect precisely (de+sev) outranks distribution fidelity (mmd+vario)** — the exact opposite of T2 extrap.

### 18. Parameter-sweep conclusions (multiple families, optimal parameters set by the real board)
- `kb` family: k=65 optimal (66.36); k=75 drops all five metrics (vario −3.0) — increasing k is the wrong direction.
- `cmp` family: the low-β side is better — b=0.55 (65.31) > b=0.70 (64.93) > b=1.00 (63.35, all five below b070).
- `kp7_m`: b=0.50 beats the b=0.00 control by 2.30 (de −4.1 / dir −3.2 / mmd −1.7) — b is the key kp7 parameter.
- `kp3_w`: a=0.25 optimal; all raw variants fail, aonly (without the b500c15 component) drops all three lines.
- `sel` family all collapse (selpc1 lowest 30.21, mmd 15.7/vario 19.6 double collapse); the `26-gene pk/ctl` family is confirmed shut down; `koq` fails; the `vs` family caps at 50.67.
- **Lesson**: the real board is the only arbiter; "more complicated-looking components" are often negative optimization.

### 19. The scorer is rotation-sensitive (community finding, veckit#7)
- **Phenomenon** (intuition-lab): a pure rigid rotation changes sliced_wasserstein / occupancy_dice (PCA handedness issue).
- **Lesson**: tiny changes in T2 geometric metrics may be biologically meaningless; before manipulating coordinates, confirm what the metrics are sensitive to.

---

## II. Engineering / process

### 1. Duplicate submissions burn quota (recurring)
- copy5118 same-file double upload, mix70_ko re-upload, heart-extrap v3 same-SHA-256 three-time re-upload, ancestor_donor_birth double upload, dirprop suspected rename-reupload (metric-by-metric identical), early otmix/shift double uploads.
- **Lesson**: every upload must pass the **hash-anti-duplicate gate** (t1_/t3_pre_upload_gate + slot_ledger); portal daily quota is limited (T1 8/8, T2 3/8, T3 6/8, reset at 00:00 UTC).

### 2. Submission format rejections (three typical cases)
- `cpf015r`: 9000 cells exceeded this board's 583–5000 cap (rejected).
- `t2_embryo_tls2n5000` mistakenly uploaded to the T1 board: 32285 vs 498 gene-panel mismatch (rejected).
- heart interp: 500 vs 498 genes, missing Casp4/Pnliprp1 (rejected).
- **Lesson**: element-wise check the official panel order before submitting (T1 32285 / embryo 498 / heart 500); do not be greedy with cell counts (>2000 cells are discarded before measurement by the heaviest metrics; bigger only adds memory, not points).

### 3. Ledger/document lag and errors
- t1_slot_ledger only recorded to P5, missing six E4b files; README wrote "not uploaded" while actually uploaded; UPLOAD_SHEET filename misattached (damp0.75 never uploaded, damp0.25 recorded as P2@0.5).
- **Lesson**: **trust the disk, not memory**; start each session by running thread_start_gate to reload from disk.

### 4. Ledger row-insertion breaks merged cells (hit twice)
- `insert_rows` breaks merged cells; writing to a `MergedCell` throws read-only; two-step in-memory translation relying on intermediate disk state can overwrite summary regions.
- **Lesson**: the correct approach = backup-fill: unmerge the region to be shifted → translate values+styles from a snapshot wholesale (`copy.copy`) → re-merge the new region → clone the previous row's style for new values → independently re-read and diff=0 against the snapshot.

### 5. Data/script engineering errors (EXPERIMENT_REPORT fix list)
- T1/T2 mixed intersection dropped to 500 genes (should have been per-cohort aligned and mapped back to 32,285).
- proxy copy baseline double random resampling caused spurious wins (fixed: spurious joint wins disappeared).
- section residual identical to global (section and sample one-to-one bound, no nested replicates, not identifiable).
- adapter uncertainty direction inverted (`se2/(se2+scale)` should be `scale/(se2+scale)`; larger variance should get higher weight, it was reversed).
- sign support wrongly allowed 50/50 split (taking positive/negative maxima — should only take block proportions consistent with the aggregate sign).
- old test3 file falsely reported pending (historical copy not in the manifest; audit excluded and warning issued).
- aggregate JSON overwritten (run_otmix_sweep aggregate-JSON overwrite root cause fixed).
- remote launcher missing optional tools, nested-heredoc quoting errors.
- T2/T3 released h5ad have duplicate observation names (made unique only in the in-memory view, source data untouched).
- obs x/y/z were once wrongly preferred as spatial coordinates (should prefer X_spatial; the two coordinate sets reported separately).

### 6. Context management
- Reading tens of MB of raw exports into context causes confusion (the "too much context" lesson).
- **Lesson**: read only core conclusion sections; leave details on disk for on-demand lookup; use summary files.

### 7. Data-compliance discipline (pitfalls that avoid crossing the line)
- Never read/used held-out stage data; near-E9.5 candidates (GSE76118/GNomEx/GSE210521/Feng2022) not downloaded, awaiting accession-level rule confirmation or exclusion.
- GSE278603 shared genes only 15,669 (47.06%) — usable only as an early-spatial prior, not to supplement T1 expression.
- External data closer to held-out is treated as held-out (midpoint boundary) — **nearness counts; the stage label is not the test**.
- **Lesson**: any external source must be disclosed in the method summary with the submission (undisclosed = violation); when in doubt, ask the organizers first.

---

## III. One-sentence lesson summary

1. **Methods differ not in "who is fancier" but in the strength of their assumption about the nature of change** — stronger assumptions raise the theoretical ceiling but increase single-point failure risk.
2. **Local proxies can only exclude bad candidates, never select good ones; the real board is the only arbiter.**
3. **Real-board differences < 2× the noise band count as a tie** (mmd/vario ±3–6 points; de/dir/sev zero-noise).
4. **Each board has its own key metrics**: T1 is variogram structure + de_score; T2 extrap is scale_log_ratio + the morphology forbidden zone (d2_shape/occupancy_dice); T3 is severity_slope + de_score.
5. **Four explicitly falsified dead ends** (Markov time-homogeneity, anonymous mixture, the transfer family, morphology extrapolation) — no further real-board quota will be spent on them.
6. **Discipline matters more than any single method**: preregistration, fault-finding, falsification, switching channels without downgrading the deliverable, hash gates, disk-based memory — these processes pay off long-term and no single method can replace them.
