# Local Tools

> **The full link ledger of external references, third-party tools used, pretrained models, algorithms, external datasets and platforms is in [`reference-links.md`](reference-links.md)** (official resources, community tools, compliance-audit conclusions, and methodology).
> This file lists only **locally built pipelines** (long-maintained, reusable frameworks in the local workspace), so that "what already exists is inspected before rebuilding" — avoiding reinventing wheels.

<p align="center"><a href="tools.md">中文</a> · English</p>

---

## I. Submission hygiene and gates

| Tool | Responsibility |
|---|---|
| `check_submission.py` | Submission format check: gene-panel order, non-negative finite X, T2/T3 spatial_3D, cell-count range |
| `submission_gate.py` | Post-generation automatic `strip_training_annotations` + `check_submission`; FAIL terminates the main flow |
| `t1_pre_upload_gate.py` / `t3_pre_upload_gate.py` | Upload gate: **hash-anti-duplicate lock** + five checks (format/labels/hash/quota/authorization) |
| `t1_slot_ledger.json` / `t3_slot_ledger.json` | Quota ledger (daily 8/3/6 caps, anti-duplicate submission) |
| `validate_t2_submission.py` | T2 strict output check: panel/coordinates/no-label-columns/no-extra containers |
| `audit_t2.py` + `t2_data_contract.py` | T2 data contract + recursive read-only audit (102/102 file panel checks) |
| `t2_experiment_gate.py` | T2 experiment gate: manifest check, source isolation, DE reference, hash and output path |
| `audit_t3_external_gse208162.py` | T3 external-data read-only compliance gate (not downloaded / sample list / cohort isolation) |

## II. Scoring and calibration

| Tool | Responsibility |
|---|---|
| `veckit/` | Official local scorer (see section I of reference-links.md for the official link) |
| `noise_calibrate.py` | Multi-seed noise calibration: scorer seeds × builder seeds → mean±sd raw bands + skill bands; real-board differences < 2×band count as a tie |
| `refit_headline.py` + `HEADLINE_FORMULA.md` | Headline formula lock (T1 / T3 weighted conventions) |
| `thread_start_gate.py` | **Per-session opening ritual**: reload from disk the review lessons, real-board calibration anchors, quota ledger, pending batches ("trust the disk, not memory") |

## III. Method generators (baselines family)

| Tool | Responsibility |
|---|---|
| `baselines/t1_shift.py` | T1 pseudobulk shift baseline (damp grid; recipe per official baselines page) |
| `baselines/t1_otmix.py` | OT-mixture baseline (WOT coupling + type-transfer resampling + growth/mask variants; WOT in reference-links.md) |
| `baselines/t3_wt_identity.py` / `t3_shift_transfer.py` / `t3_prior_shift.py` | T3 floor / global-Δ transfer / literature prior (GATA4 target-gene directed response) |
| `wot_analysis/` | WOT coupling matrix, marker audit (378→61-edge mask), edge-mask generator |
| `category_generation.py` | Cross-task "new-category generation" research generator (soft parent categories + program shift + parent-cell residuals; proxy only, never writes to the upload queue) |
| `deepgen_t1/` | Deep-generation family: VGFM (flow matching) / CVAE / diffusion + residual correction, carrier bypass, FiLM gate, structure-axis, composition-support, multi-KO response adapter (all research interfaces, not candidate generators) |
| ledger row-insertion script family | backup-fill method (unmerge → snapshot shift → re-merge → clone styles → independent re-read), incl. verify_*.py comparison scripts |

## IV. Award candidates (Community Contribution direction, all locally implemented)

| Tool | Description |
|---|---|
| `vec_scalecheck` | Local format checker (self-built repo https://github.com/wqty123/vec-scalecheck; three over-claims in its README noted as to-fix: exaggerated harm scope / wrong "zero-mechanism-risk" / PASS conflating consistency with validity) |
| `t1_pre_upload_gate` | Anti-duplicate lock + five checks in one (submittable standalone) |
| `t2_data_contract` | T2 data contract (48KB toolkit) |
| `slot_ledger` | Submission quota ledger |

---

## V. Tool-coverage conclusions (read before rebuilding)

1. **Format/structure checks** (data_inspector ≈ vec-submit-check ≈ vec_submit_check ≈ check_submission + vec_scalecheck; links in section II of reference-links.md) — already crowded, **do not rebuild**.
2. **Teaching-type** (task1_walkthrough ≈ scigantic ≈ xxx12e tutorial_zh) — saturated, **do not rebuild**.
3. **Agent-track evidence** (vec-evidence-check ≈ vec_agent_evidence) — not used by the Human Team, **do not rebuild**.
4. **Real incremental value**: vecbench's noise-floor calibration (integrated), intuition-lab's metric-sensitivity conclusions (knowledge base), external-data-catalog's GSE282547 (T2 heart data material, pending rule confirmation), EmbryoMatch's E-MTAB-11763 (T1 data material, pending compliance audit).
5. **Our applications stay differentiated**: t1_pre_upload_gate (anti-duplicate lock + five checks), t2_data_contract, vec_scalecheck — none conflicts with existing community facilities.
