# T2 experiment report: heart interpolation (E8.25/E8.75 → predict intermediate stage)

<p align="center"><a href="experiments_t2_heart_interp.md">中文</a> · English</p>

Eight metrics (same as above); official floor 50. Panel: 500 genes, must be element-wise aligned to the official order (once rejected for missing Casp4/Pnliprp1).

## Experiment overview (chronological concrete technique sequence)

`v1 (type stratification + global pairing)` 61.9 → `mix_brkt` 62.6 → **`mix_brkts (scale_log_ratio 71.1→100.0 full marks)` 65.01 (current best)**; `gps50n1185` 50.2 (ineffective), `v1g2000s` 60.0, `v1geom5000s` 53.12 (vario 37.6 collapse), `v1vc100` 53.61 — none above

## Experiment log (grouped by method family)

### Experiment family: v1 (type stratification + global pairing)

Method: stratify by cell type, within-type global pairing interpolation from E8.25→E8.75 (log-linear normalization + paired geometry).

Tools: t2 generator script family, t2_data_contract.py, veckit.

Issues: 61.86 (74/148) — heart-interp first version baseline; the 500 vs 498 gene-panel trap (rejected once for missing Casp4/Pnliprp1).

Conclusion: v1 is the heart-interp starting point 61.9; the panel must be element-wise aligned to the official 500 genes.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-05 | v1 | 类型分层训练/表达匹配 + 全局空间配对 k=1 + log 插值 + 10k 归一化 | 61.86 | 58.3 | 65.7 | 57 | 39.2 | 88.1 | 48.3 | 89.9 | 60.1 | 74/148 | d2_shape 88.1/scale 89.9 仍全板最强；已被 mix_brkt 62.61 取代（09-17） |

### Experiment family: mix_brkt / mix_brkts (mixture + bracket + scale)

Method: mix real carriers (E8.25/E8.75) + bracket type constraint + paired generation; mix_brkts additionally calibrates library-size scale (scale_log_ratio 71.1→100.0 full marks).

Tools: t2 generator script family, veckit.

Issues: mix_brkt 62.6 and mix_brkts are identical metric-by-metric except scale (de 52.1/dir 55.7/mmd 50.7/vario 34.7/d2 42.2/occ 54.4/nh 50.8); full-mark scale contributes ≈ +2.4.

Conclusion: **mix_brkts = 65.01** (54/191), current heart-interp best; scale_log_ratio from 71.1 to 100.0 full marks lifts the total by ≈ +2.4.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-17 06:17 | mix-brkt | mix_brkt（混合+bracket；文件名 t2_heart_val_interp_mix_brkt.h5ad） | 62.61 | 62.4 | 66.6 | 62.2 | 55.1 | 80.5 | 49.9 | 71.1 | 59.4 | 88/179 | 62.61 超 v1 61.86；d2 80.5 强；方法细节待补充；已被 mix_brkts 65.01 取代（09-20） |
| 2026-09-17 06:17 | mix-brkt-scale | mix_brkt + scale（文件名 t2_heart_val_interp_mix_brkt_scale.h5ad） | 62.04 | 62.4 | 66.6 | 62.2 | 55.1 | 80.5 | 49.9 | 64.3 | 59.4 | 88/179 | 同 mix_brkt，仅 scale 64.3（原 71.1）略降；方法细节待补充 |
| 2026-09-20 16:49 | mix_brkts | mix_brkts（文件名 t2_heart_val_interp_mix_brkts.h5ad） | 65.01 | 62.4 | 66.6 | 62.2 | 55.1 | 80.5 | 49.9 | 100 | 59.4 | 54/191 | mix_brkts 族；65.01 超 mix_brkt 62.61；与 mix_brkt 同指标、仅 scale 71.1→100.0 满档（+2.4 总分）；方法细节待补充 |

### Experiment family: gps50n1185 (Gaussian process)

Method: Gaussian process interpolation (n=1185).

Tools: t2 generator script family, veckit.

Issues: 50.2, tied with the floor — the gps variant on heart interp is clearly weaker than on the embryo board.

Conclusion: gps is unsuitable for heart interp; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18 03:20 | gps50n1185 | gps50n1185（gps 族 n=1185；文件名 t2_heart_val_interp_gps50n1185.h5ad） | 50.24 | 61.2 | 68 | 59.7 | 55.5 | 40.7 | 55.7 | 87.8 | 35.2 | 91/187 | gps 族 gps50n1185；50.24 低于 mix_brkt 62.61；de 61.2 全板最强档但 nh 35.2/d2 40.7 拖累；方法细节待补充 |

### Experiment family: v1g2000s (hand-replicated v1 geometry)

Method: v1g = hand-replicated v1 geometry (replica of v1's paired displacement field, n=2000); the replication is incomplete — d2 only 48.7 (v1 original 88.1).

Tools: t2 generator script family, veckit.

Issues: 60.0 — the geometric-constraint variant is below v1 (61.9) and mix_brkts (65.01); d2 48.7 far below v1's 88.1.

Conclusion: v1-geometry replication is incomplete (the v1 original is no longer available locally); closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-20 16:29 | v1g2000s | v1g2000s（文件名 t2_heart_val_interp_v1g2000s.h5ad） | 59.95 | 60.6 | 68.9 | 58.3 | 54.2 | 48.7 | 52.2 | 100 | 51.4 | 94/191 | v1g2000s 族；59.95 低于 mix_brkt 62.61；scale 100.0 满档但 vario 54.2/d2 48.7 偏弱；方法细节待补充 |

### Experiment family: v1geom5000s (v1 geometry variant)

Method: v1 geometry variant (n=5000; the v1 original is no longer local, coordinates actually come from another coordinate set of v1replicas); the real-board d2 46.2 proves v1's geometry is not preserved in any local file.

Tools: tools/_t2hi_v1geo.py, veckit.

Issues: 53.12 — vario 37.6 collapse (geometric transformation breaks the expression distribution); scale 100.0 full marks.

Conclusion: large geometric sampling amplitude destroys vario; the whole v1 line is closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-20 18:50 | v1geom5000s | v1geom5000s（文件名 t2_heart_val_interp_v1geom5000s.h5ad） | 53.12 | 51.2 | 56.6 | 47.3 | 37.6 | 46.2 | 50 | 100 | 49.9 | 54/192 | v1geom5000s 族；53.12 低于 mix_brkts 65.01；scale 100.0 满档但 vario 37.6 崩、mmd 47.3/d2 46.2 偏弱；方法细节待补充 |

### Experiment family: v1vc100 (v1 + variance control, proxy-extrapolation falsification)

Method: v1 + variance control (vc=100, coordinates from v1replicas rather than the v1 original); mistake A: the local nh proxy reading 0.00852 falls outside the four-point calibration interval [0.04217, 0.13902], the reported "62.04" was a linear extrapolation of the left segment (measured 50.8, error +11.24); mistake B: cited a real-board d2=88.1 analogy from the v1 original that does not exist locally (measured 42.2, 46 points off).

Tools: tools/_heart_vc_sweep.py, veckit.

Issues: 53.61 — vario 34.7 weak; d2 42.2 (−38.3, largest single-axis loss); net −11.40 vs mix_brkts 65.01.

Conclusion: **a proxy reading must first fall inside the calibration interval**; the whole v1 line is closed (v1vc100/v1geom5000s/v1g2000s/gps50n1185).

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-23 14:25 | v1vc100 | v1vc100（文件名 t2_heart_val_interp_v1vc100.h5ad，2.4MB） | 53.61 | 52.1 | 55.7 | 50.7 | 34.7 | 42.2 | 54.4 | 100 | 50.8 | 48/198 |  |

## Summary rows

- **Current best**: 65.01
- **Official floor (copy_last / wt_identity)**: 50
- **Board top (leader)**: 73.4
