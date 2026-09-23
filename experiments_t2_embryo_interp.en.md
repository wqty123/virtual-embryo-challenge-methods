# T2 experiment report: embryo interpolation (E6.75/E7.25/E8.0 → predict intermediate stage)

<p align="center"><a href="experiments_t2_embryo_interp.md">中文</a> · English</p>

Eight metrics: de_score / de_direction / mmd_u / variogram / d2_shape / occupancy_dice / scale_log_ratio / neighborhood_mmd; official floor 50. Panel: 498 genes (the official published panel, not the target-file gene set).

## Experiment overview (chronological concrete technique sequence)

`v1 (kNN-pair log-linear normalization + paired geometry)` 59.0 → `mix_brkt` 59.07 (d2/occ weak) → `bgm` 62.94 → `v1replica` 56.99 (controlled variable) → `gps33 Gaussian process` 62.37 → `gps33s (scale calibration)` 63.19 → `tls2n5000 type-level global shift` 59.01 (d2 23.8 collapse) → `gpsnnu geometric inheritance` 61.81 → `vg_ourmixs geometry transplant` 55.93 → **`cpf015r5k homologous pairing` 65.31 (current best)** → `vlK8 variance amplification` 64.75 (not above)

## Experiment log (grouped by method family)

### Experiment family: v1 (single-nearest-neighbor log-linear normalization + paired geometry)

Method: train on the E8.0 carrier, learn kNN pairs (k=1) from E7.25→E8.0, apply log-linear normalized interpolation + paired geometry (coordinates translated with the pair) to generate intermediate-stage predictions.

Tools: t2 generator script family, t2_data_contract.py, veckit.

Issues: 59.00 (95/152) as the starting baseline; geometric pairing only moves nearest neighbors, poor state continuity.

Conclusion: v1 is the first T2-embryo version, 59.00 above the floor 50; later families stack different mechanisms on top.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-04 | v1 | E7.25→E8.0 单最近邻 log-linear 归一化 + 配对几何 | 59 | 55.8 | 68.1 | 52.9 | 62.8 | 50 | 59.5 | 89.3 | 50.9 | 95/152 | 已被 mix_brkt 59.07 取代（09-17） |

### Experiment family: mix_brkt (mixture + bracket)

Method: mix real carriers + bracket constraint (only type transitions among E6.75/E7.25/E8.0 allowed), then add paired generation.

Tools: t2 generator script family, veckit.

Issues: 59.07, only 0.07 above v1 — d2_shape 26.3/occupancy_dice 19.0 weak (insufficient coordinate generation); scale 73.0 also drags.

Conclusion: the bracket constraint keeps de 57.0 but spatial metrics are poor; a transition from v1 to bgm.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-17 06:16 | mix-brkt | mix_brkt（混合+bracket；文件名 t2_embryo_val_interp_mix_brkt.h5ad） | 59.07 | 57 | 70.6 | 67 | 67.2 | 26.3 | 19 | 73 | 66 | 121/185 | 已被 bgm 62.94 取代（09-17）；d2 26.3/occ 19.0 偏弱；方法细节待补充 |
| 2026-09-17 06:17 | mix-brkt-scale | mix_brkt + scale（文件名 t2_embryo_val_interp_mix_brkt_scale.h5ad） | 56.48 | 57 | 70.6 | 67 | 67.2 | 26.3 | 19 | 41.9 | 66 | 121/185 | 同 mix_brkt，仅 scale 41.9（原 73.0）拖累总分；方法细节待补充 |

### Experiment family: bgm (background mixture generation)

Method: bgm = overlay "background program mixture" on the carrier to generate intermediate states (the f=0.15 variant controls mixture strength).

Tools: t2 generator script family, veckit.

Issues: bgm 62.94 beats mix_brkt (+3.87) — dir 70.6/mmd 68.7/vario 67.3 all lead, d2 49.2/occ 41.0 weak; the f0.15 variant 57.97 is even lower.

Conclusion: bgm is the first 62+ plateau on embryo interp; d2/occ remain the short board.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-17 15:08 | bgm | bgm（文件名 t2_embryo_val_interp_bgm.h5ad） | 62.94 | 55.2 | 70.6 | 68.7 | 67.3 | 49.2 | 41 | 98.7 | 57.8 | 88/188 | 62.94 超 mix_brkt 59.07；dir 70.6/mmd 68.7/vario 67.3 全面领先；d2 49.2/occ 41.0 偏弱；方法细节待补充；已被 gps33s 63.19 取代（09-20） |
| 2026-09-17 15:08 | bgm-f015 | bgm_f015（文件名 t2_embryo_val_interp_bgm_f015.h5ad） | 57.97 | 55.8 | 69 | 60.2 | 61.6 | 41.8 | 32.4 | 98.7 | 51 | 88/188 | 同族 f0.15 变体，57.97 低于 mix_brkt 59.07；方法细节待补充 |

### Experiment family: v1replica (v1 replica)

Method: strict v1 replica (controlled variable).

Tools: t2 generator script family, veckit.

Issues: 56.99, inconsistent with v1's 59.00 (different sampling) — a typical case of local vs real-board ranking disagreement.

Conclusion: the controlled replica confirms the v1 baseline range ≈57–59.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18 03:16 | v1replica | v1replica（v1 复刻；文件名 t2_embryo_val_interp_v1replica.h5ad） | 56.99 | 52.5 | 62.3 | 52.2 | 61.7 | 51 | 52.4 | 89.2 | 50.4 | 92/194 | v1 复刻；56.99 中位；方法细节待补充 |

### Experiment family: gps33 (Gaussian process interpolation)

Method: Gaussian process regression interpolation on paired cells (33 gene modules gps33 / n=583 downsampled variant), outputting intermediate-state expression.

Tools: t2 generator script family (gps series), veckit.

Issues: gps33 62.37 < bgm 62.94 (d2 55.6 better but scale 88.9 drags); gps33n583 61.36 (de 58.2, the board's strongest tier, but overall lower); gps33s 63.19 — same metrics as gps33 except scale 88.9→98.7 (+9.8), total +0.82.

Conclusion: **scale_log_ratio is a cheap high-score item**: calibrating library size to the reference scale gains 0.8+ points for free; gps33s = 63.19.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18 03:15 | gps33 | gps33（文件名 t2_embryo_val_interp_gps33.h5ad） | 62.37 | 55.2 | 70.7 | 68.6 | 66.8 | 55.6 | 45.5 | 88.9 | 55.3 | 92/194 | gps 族 gps33；62.37 低于 bgm 62.94；d2 55.6 优于 bgm（49.2）但 scale 88.9 拖累；方法细节待补充 |
| 2026-09-18 03:17 | gps33n583 | gps33n583（gps 族 n=583；文件名 t2_embryo_val_interp_gps33n583.h5ad） | 61.36 | 58.2 | 69.3 | 67.7 | 66.6 | 57.4 | 46.8 | 88.9 | 50.1 | 92/194 | gps 族 gps33n583；61.36 低于 bgm 62.94；de 58.2 全板最强档、d2 57.4 亦高；方法细节待补充 |
| 2026-09-20 16:56 | gps33s | gps33s（文件名 t2_embryo_val_interp_gps33s.h5ad） | 63.19 | 55.2 | 70.7 | 68.6 | 66.8 | 55.6 | 45.5 | 98.7 | 55.3 | 93/199 | gps 族 gps33s；63.19 超 bgm 62.94；与 gps33 同指标、仅 scale 88.9→98.7（+0.82 总分）；方法细节待补充；已被 cpf015r5k 65.31 取代（09-20） |

### Experiment family: tls2n5000 (type-level global shift)

Method: type-level global shift — shift expression uniformly within each cell type (n=5000); the real board shows nh +7.8 success but d2 −31.8/occ −27.9 cancel it out.

Tools: t2 generator script family, veckit.

Issues: 59.01 — d2_shape 23.8/occupancy_dice 17.6 collapse (type-level shift destroys inter-type relative positions); once mistakenly uploaded to the T1 panel and rejected (32285 vs 498).

Conclusion: type-level global shift destroys spatial metrics; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-20 16:59 | tls2n5000 | tls2n5000（文件名 t2_embryo_tls2n5000.h5ad） | 59.01 | 54.6 | 68 | 65.7 | 63.9 | 23.8 | 17.6 | 98.7 | 63.1 | 93/199 | tls2n5000 族；59.01 低于 gps33s 63.19；scale 98.7/nh 63.1 尚可但 d2 23.8/occ 17.6 崩坏拖累；方法细节待补充 |

### Experiment family: gpsnnu (geometric inheritance + nearest-neighbor uniquification)

Method: gps-family nnu variant — switch the expression source: geometric inheritance + nearest-neighbor uniquification (drop the constrained pairing, inherit expression from geometric nearest neighbors); the local nh proxy once hit 62.4 precisely, the real board shows mmd −7.0/vario −13.4 eating the gain.

Tools: tools/_t2_gpsnn.py, _t2_gpsnn_u.py, veckit.

Issues: 61.81 < gps33s 63.19 — d2 55.6 same tier as gps33s but de 53.5/mmd 61.6/vario 53.4 weaker.

Conclusion: the unconstrained version loses gps's distribution advantage; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-20 17:12 | gpsnnu | gpsnnu（文件名 t2_embryo_val_interp_gpsnnu.h5ad） | 61.81 | 53.5 | 67.4 | 61.6 | 53.4 | 55.6 | 45.5 | 98.7 | 61.9 | 93/199 | gps 族 gpsnnu；61.81 低于 gps33s 63.19；d2 55.6 与 gps33s 同档但 de 53.5/mmd 61.6/vario 53.4 偏弱；方法细节待补充 |

### Experiment family: cpf015r5k (homologous pairing + positional interpolation)

Method: cpf = homologous-pair construction: homologous pairing + positional interpolation pos_f=0.15 + scale correction (r variant anchor 200.88; n=5000 sampling, the 5k version resampled under the 583–5000 cell cap after cpf015r was rejected for exceeding it; local prediction +2.4~2.5).

Tools: tools/_cpf005_probe.py, check_submission.py, veckit.

Issues: the original cpf015r at 9000 cells was rejected for exceeding the board cap; cpf015r5k 65.31 — de 55.8/dir 70.6/mmd 68.8/vario 67.1/d2 56.1 all lead, occ 43.4 slightly weak.

Conclusion: **cpf015r5k = 65.31** (65/200), current T2-embryo-interp best. d2_shape/occupancy_dice are the main remaining improvement room.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-20 18:50 | cpf015r5k | cpf015r5k（文件名 t2_embryo_val_interp_cpf015r5k.h5ad） | 65.31 | 55.8 | 70.6 | 68.8 | 67.1 | 56.1 | 43.4 | 97.4 | 64.3 | 65/200 | cpf015r5k 族；65.31 超 gps33s 63.19；de 55.8/dir 70.6/mmd 68.8/vario 67.1/d2 56.1 全面领先、occ 43.4 略弱；方法细节待补充 |

### Experiment family: vlK8 (variance amplification K=8)

Method: vlK8 = variance-amplification variant (amplify the K=8 highest-variance genes by coefficient c=1.25); highly isomorphic with cpf015r5k, the only variable is variance amplification — on T1 this lever is worth +3.5 (3 real-board points), on T2 it is negative (the gain is halved or worse while nh cost is paid in full).

Tools: t2 generator script family, veckit.

Issues: 64.75 — highly isomorphic with cpf015r5k (dir/mmd/vario/d2/occ/scale almost identical), the gap is de 55.2 (−0.6)/mmd 67.1 (−1.7)/nh 63.4 (−0.9).

Conclusion: vlK8c125 64.75 is cpf's near-relative plateau, not above 65.31; variance amplification does not transfer to T2; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-23 16:47 | vlK8c125 | vlK8c125（vlK8 族 c125 变体；文件名 t2_embryo_val_interp_vlK8c125.h5ad，9.8MB） | 64.75 | 55.2 | 70.5 | 67.1 | 67.1 | 56.1 | 43.4 | 97.4 | 63.4 | 67/206 | vlK8 族 c125 变体；64.75 超官方地板（+14.75）但未超最佳 cpf015r5k 65.31（差 0.56）；与 cpf015r5k 高度同构（dir 70.5/mmd 67.1/vario 67.1/d2 56.1/occ 43.4/scale 97.4 几乎一致），差距在 de 55.2(-0.6)/mmd 67.1(-1.7)/nh 63.4(-0.9)；板人数 200→206；方法细节待补充 |

### Experiment family: vg_ourmixs (v1 paired displacement-field transplant)

Method: vg_ourmixs = change the geometry: transplant v1's paired displacement field onto the mixture expression; nh collapses 57.8→41.5 (weighted −4.10).

Tools: t2 generator script family, veckit.

Issues: 55.93 — scale 98.7 strong but d2 52.8/occ 48.2/nh 41.5 weak, below bgm 62.94.

Conclusion: geometric transplant destroys nh; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-20 16:24 | vg_ourmixs | vg_ourmixs（文件名 t2_embryo_val_interp_vg_ourmixs.h5ad） | 55.93 | 54.1 | 68.2 | 66.4 | 65.2 | 52.8 | 48.2 | 98.7 | 41.5 | 95/199 | vg_ourmixs 族；55.93 低于 bgm 62.94；scale 98.7 强但 d2 52.8/occ 48.2/nh 41.5 偏弱；方法细节待补充 |

## Summary rows

- **Current best**: 65.31
- **Official floor (copy_last / wt_identity)**: 50
- **Board top (leader)**: 75.6
