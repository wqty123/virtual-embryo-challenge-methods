# Virtual Embryo Challenge · Method Journey Experiment Log

> Virtual Embryo Challenge 2026 (NeurIPS 2026 competition, hosted by Stanford Qiu Lab)
> This repository records **every method we tried from day one** (each method = one experiment entry: method / tools / issues / results),
> **all the pitfalls we hit**, and **all the tools we used**.
> Positioning: methodology sharing + experiment log (consistent with official rule §15: participants keep ownership of their methods, and sharing methods is encouraged; the Community Contribution award welcomes teaching-type submissions).
> All scores come from official scoring returns (public Virtual Embryo Challenge leaderboard) and contain **no held-out stage data**.

<p align="center"><a href="README.md">中文</a> · English</p>

## Tasks and boards

| Task | Board | Goal | Metrics |
|---|---|---|---|
| T1 | `T1:val` | single-cell temporal extrapolation: E8.5→E9.5, predict E10.5 | de_score / de_direction / mmd_u / variogram |
| T2 | `T2:embryo:val_interp` | embryo interpolation: E6.75/E7.25/E8.0, predict intermediate stage | 8 metrics: de/dir/mmd/vario + d2_shape/occupancy_dice/scale_log_ratio/neighborhood_mmd |
| T2 | `T2:heart:val_interp` | heart interpolation: E8.25/E8.75, predict intermediate stage | same 8 metrics |
| T2 | `T2:heart:val_extrap` | heart extrapolation: predict after E9.5 | same 8 metrics |
| T3 | `T3:gata4` | Gata4 KO perturbation response prediction (E8.75) | de_score / de_direction / severity_slope / mmd_u / variogram |

**Scoring**: the floor (copy_last / wt_identity) is fixed at 50, the ceiling (self half-split estimate) at 100; each team is ranked by its historical best per board. T1 total ≈ `0.25·de + 0.25·dir + 0.30·mmd + 0.20·vario`; T3 ≈ `0.298·de + 0.250·dir + 0.251·sev + 0.120·mmd + 0.080·vario`.

## Current score snapshot (as of 2026-09-23, our team best)

| Board | Best method | Score | rank |
|---|---|---|---|
| T1:val | kp7_m_b050_n2000 (maturity-weighted sampling) | **53.67** | 93/254 |
| T2:embryo:val_interp | cpf015r5k (homologous pairing) | **65.31** | 65/200 |
| T2:heart:val_interp | mix_brkts (mixture+bracket+full-mark scale) | **65.01** | 54/191 |
| T2:heart:val_extrap | scale_only (scale adjustment only) | **54.51** | 68/185 |
| T3:gata4 | kbb_n6000_b055_k65 (real-WT dilution of KO combo) | **66.61** | 48/187 |

Three-task total ≈ **181.89** (above the 150 floor threshold; ranking per official leaderboard).

## Repository structure

| File | Content |
|---|---|
| `README.md` | This file (Chinese): overview, score snapshot, index |
| `README.en.md` | This file (English) |
| `experiments_t1.md` / `.en.md` | T1 experiment report (19 method families, 65 submission rows) — Chinese / English |
| `experiments_t2_embryo_interp.md` / `.en.md` | T2 embryo-interp experiment report (10 families) |
| `experiments_t2_heart_interp.md` / `.en.md` | T2 heart-interp experiment report (6 families) |
| `experiments_t2_heart_extrap.md` / `.en.md` | T2 heart-extrap experiment report (14 families) |
| `experiments_t3.md` / `.en.md` | T3 experiment report (15 families, 42 submission rows) |
| `pitfalls.md` / `.en.md` | All the pitfalls: methodological/biological + engineering/process |
| `tools.md` / `.en.md` | Local tool list: submission hygiene / scoring & calibration / method generators / award candidates + tool-coverage conclusions |
| `reference-links.md` / `.en.md` | **Reference ledger**: official resources, community tools, pretrained models, algorithm methods, external datasets, platforms — all with links and compliance-audit conclusions |
| `gen_experiments.py` | Experiment report generator (input: ledger JSON, grouped by method family, bilingual output) |

**Every experiment family follows one structure**: method (concrete algorithm, parameters, data, implementation file) → tools (concrete scripts/scorer) → issues (concrete scores and phenomena) → conclusion (concrete judgement) → submission log (all result data).

## Method timeline (concrete technique sequence)

1. **T1**: `pseudobulk shift (global drift)` 48.13 → damp grid 48.85 → `OT mixture (WOT coupling + type-transfer resampling)` 47.52 → `Markov flux` (falsified 44.19) → `program mixture` (vario collapse 47.34) → `momentum mask` 49.49 → `mm library-size normalization` 49.93 → `vs variance amplification` 50.67 → **`kp knowledge-program shift + variance amplification / maturity weighting` (kp3_w 52.18 → kp7_m_b050 53.67, current best)**
2. **T2 embryo**: `v1 (kNN-pair log-linear interpolation)` 59.0 → `mix_brkt` 59.07 → `bgm` 62.94 → `gps33s Gaussian process (scale calibrated)` 63.19 → **`cpf015r5k homologous pairing` 65.31 (current best)**
3. **T2 heart interp**: `v1 (type stratification + global pairing)` 61.9 → `mix_brkt` 62.6 → **`mix_brkts (full-mark scale)` 65.01 (current best)**
4. **T2 heart extrap**: `v3/v4` (≈50 plateau) → morphology line falsified four times (`r6b70a20` 38.97 / `comp_c100` 32.8 / `vmorph_s120` 46.8 / `cpfx` d2_shape 5.7) → **`scale_only` 54.51 (current best)** — moving only scale/composition, never morphology, is the only valid route
5. **T3**: `transfer global Δ` (falsified 40.98) → `cardiac restricted` (falsified 44.85) → `literature prior` (ties floor 45.80) → `mix KO mixture` 64.60 → `cmp celltype^β resampling` 64.93 → `cmpw carrier dilution` 65.49 → `kb real-WT dilution of KO` 66.36 → **`kbb combo` 66.61 (current best)**

## Compliance statement

- This repository contains only method descriptions, official public scores, and public rule references; it contains **no** measurements of any held-out stage (T1 E10.5/E12.5; T2 embryo E7.5/E7.75, heart E8.5/E10.5/E12.5; T3 Gata4/β-catenin KO E8.75).
- It contains nothing that reverse-engineers held-out properties from scores; scores are used only to select predictions, never to compute predictions (official rule §10).
- Full rules: https://virtualembryo.ai/challenge/rules

## References and acknowledgments

All referenced ideas, third-party tools, pretrained models, and external data sources are listed with links and compliance-audit conclusions in [`reference-links.md`](reference-links.md); the "tools" field of each experiment family also inlines sources (e.g. WOT, official baseline recipes, GSE208162 data). Sources without a concrete URL (e.g. the textbook developmental-program list) are labeled by name and provenance only; no links are fabricated.

## Contact

Feel free to add me on WeChat for detailed discussion: `hui13866591135`
