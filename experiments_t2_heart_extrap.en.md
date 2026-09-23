# T2 experiment report: heart extrapolation (predict after E9.5)

<p align="center"><a href="experiments_t2_heart_extrap.md">中文</a> · English</p>

Eight metrics (same as above); official floor 50. Iron rule: **move only scale/composition, never morphology**.

## Experiment overview (chronological concrete technique sequence)

`v1 early candidate` 46.4 → `v3 (shrinkage + coordinates ×1.31)` 48.71 → `v4 population_growth` 49.26 → `v2ga6` 53.59 / `v4a10` 50.08 (marginally above floor) → **morphology-line falsified four times**: `r6b70a20` 38.97 / `comp_c100` 32.8 / `vmorph_s120` 46.8 / `cpfx type-level displacement shift` (d2_shape 5.7) 52.12 → **`scale_only` 54.51 (current best)**, then `w005 (displacement 0.05)` 54.43, `mix20_scale` 53.9, `compw30_scale` 53.7; `selday30/50` 27.5/28.9 (journey-lowest, closed)

## Experiment log (grouped by method family)

### Experiment family: v1 early candidate

Method: early candidate (09-04 first version, no version suffix).

Tools: t2 generator script family, veckit.

Issues: starts at 46.4, below the floor 50.

Conclusion: extrap-board starting point; explored step by step.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-04 17:31 | v1 | 早期候选（文件名无版本后缀） | 46.4 | — | — | — | — | — | — | — | — | — | 09-04 首次上传；逐项待 portal 展开补抓 |

### Experiment family: v3 (shrinkage type trend + uniform carrier + coordinate amplification)

Method: confidence-shrinkage type trend damp0.75 + uniform E9.5 carrier + coordinates ×1.31.

Tools: t2 generator script family, veckit.

Issues: 48.71 (mmd 33.6 largest loss, scale 100 full marks); the same file was double-uploaded on 09-06 and re-uploaded a third time on 09-14 (historical record — never upload again).

Conclusion: coordinate amplification + shrinkage trend is the wrong direction; the v3 family is closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-05 18:43 | v3 | 置信收缩类型趋势 damp0.75 + 均匀 E9.5 载体 + 坐标×1.31 | 48.71 | 51.2 | 50.2 | 33.6 | 47.9 | 53.8 | 52.2 | 100 | 44.2 | 143/180 | 已被 v4 取代；scale 满分 100.0、mmd 33.6 为最大失分；09-06 07:49 同文件双传（重复烧 1 名额）；09-14 03:46 第三次重传同文件（得分不变 48.71，rank 143/180；板队伍数 157→180，排名不可与 v4 的 121/157 直接比较） |

### Experiment family: v4 population_growth (population growth projection)

Method: E9.5 carrier + population-growth amplitude projection.

Tools: t2 generator script family, veckit.

Issues: 49.26 — d2_shape 30.6 largest loss; de 52.8 the family's highest, scale 100 full marks, but the total still below the floor 50.

Conclusion: population-growth projection fails to move morphology; v4 closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-06 08:11 | v4 | population_growth（群体增长投影；E9.5 载体 + 增长幅值） | 49.26 | 52.8 | 51.5 | 36.5 | 47.3 | 30.6 | 49.5 | 100 | 47.3 | 121/157 | 已被 scale_only 54.51 取代（09-16）；d2_shape 30.6 为最大失分，de 52.8 全族最高；scale 满分 100 |

### Experiment family: v2ga6 (geometric amplitude)

Method: v2 geometric amplitude a=6.

Tools: t2 generator script family, veckit.

Issues: 53.6, close to the floor but does not break it.

Conclusion: geometric amplitude does not break 50; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-19 18:45 |  |  | 53.59 | 47.1 | 48.6 | 48.3 | 49.9 | 49.9 | 54.1 | 100 | 49.8 | 70/195 | scale 满分 100、各指标均衡，但未超 scale_only 54.51 |

### Experiment family: v4a10 (growth amplitude 10)

Method: population-growth amplitude 10.

Tools: t2 generator script family, veckit.

Issues: 50.1, marginally above the floor.

Conclusion: growth-amplitude tuning gains almost nothing; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-19 19:05 |  |  | 50.08 | 47.8 | 48.2 | 42 | 48.5 | 49.9 | 54.1 | 100 | 45.7 | 70/195 | 刚过 floor；scale 满分但 mmd 42.0 偏弱；未超 scale_only 54.51 |

### Experiment family: r6b70a20 (morphology extrapolation)

Method: morphology extrapolation r6 (b=0.70, a=0.20 morphology/geometry amplitudes).

Tools: t2 generator script family, veckit.

Issues: 38.97 — morphology extrapolation is heavily penalized.

Conclusion: changing morphology is heavily penalized (38.97, d2 11.9 collapse) — the first morphology-line falsification point on the extrap board.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-19 16:00 |  |  | 38.97 | 52.8 | 53.4 | 30.9 | 28 | 11.9 | 58.8 | 97.5 | 34.4 | 70/194 | 低于 floor；mmd 30.9/vario 28.0/d2 11.9 三崩；再次证实 extrap 板改形态=死，scale_only 54.51 仍天花板 |

### Experiment family: comp_c100 (composition + morphology)

Method: composition mixture + morphology transform (c=100).

Tools: t2 generator script family, veckit.

Issues: 32.8 — the lowest score of the whole journey, the worst morphology-line falsification point.

Conclusion: morphology transforms are irreversible; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18 15:32 | comp_c100 | comp_c100（comp 族 c100 变体；文件名 t2_heart_val_extrap_comp_c100.h5ad，16MB） | 32.8 | — | — | — | — | — | — | — | — | — | 09-18 15:32 提交漏记补录（portal 对账）；32.8 远低于官方地板 50 与最佳 scale_only 54.51；comp 族形态变体；per-metric 待 portal 展开补抓 |

### Experiment family: vmorph_s120 (virtual morphology)

Method: virtual morphology transform s=120.

Tools: t2 generator script family, veckit.

Issues: 46.8 — geometric metrics such as d2 are penalized.

Conclusion: the virtual-morphology route fails; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18 15:32 | vmorph_s120 | vmorph_s120（vmorph 族 s120 变体；文件名 t2_heart_val_extrap_vmorph_s120.h5ad，16MB） | 46.8 | — | — | — | — | — | — | — | — | — | 09-18 15:32 提交漏记补录（portal 对账）；46.8 低于官方地板 50 与最佳 scale_only 54.51；vmorph 形态变体；per-metric 待补 |

### Experiment family: scale_only (scale adjustment only)

Method: adjust only library size/composition toward the extrapolation-target-stage proportions, coordinates and morphology completely untouched (scale_log_ratio calibrated to 100 full marks).

Tools: t2 generator script family (scale series), veckit.

Issues: 54.51, current extrap best (68/185) — scale full marks 100, balanced metrics (de 46.8/dir 49.8/mmd 50.5/vario 50.1/d2 49.9/occ 54.1/nh 51.1).

Conclusion: **moving only scale/composition, not morphology**, is the only correct route on the extrap board.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-16 21:34 | scale | scale_only（仅 scale 调整；文件名 t2_heart_val_extrap_scale_only.h5ad） | 54.51 | 46.8 | 50 | 50.6 | 50.2 | 49.9 | 54.1 | 100 | 51.2 | 68/185 | 超官方地板 50（+4.51）；rank 68/185；方法细节待补充 |

### Experiment family: mix20_scale (mixture + scale)

Method: 20% mixture + scale calibration.

Tools: t2 generator script family, veckit.

Issues: 53.9, below scale_only 54.51.

Conclusion: mixing adds no points; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-16 21:34 | mix20 | mix20_scale（混合 20% + scale；文件名 t2_heart_val_extrap_mix20_scale.h5ad） | 53.86 | 49.6 | 52.9 | 49.1 | 44.7 | 49.5 | 57.2 | 100 | 49.2 | 68/185 | 超地板（+3.86）；rank 68/185；方法细节待补充 |

### Experiment family: compw30_scale (composition weighting + scale)

Method: 30% composition weighting + scale.

Tools: t2 generator script family, veckit.

Issues: 53.7, below scale_only.

Conclusion: composition weighting adds no points; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-16 21:34 | compw30 | compw30_scale（组成加权 30% + scale；文件名 t2_heart_val_extrap_compw30_scale.h5ad） | 53.66 | 46.8 | 50 | 49.4 | 52.1 | 44.3 | 50 | 100 | 51 | 68/185 | 超地板（+3.66）；rank 68/185；方法细节待补充 |

### Experiment family: w005 (minimal displacement 0.05 along the scale_only end)

Method: w005 = minimal displacement along the scale_only end (displacement amplitude 0.05): move only a tiny amount of coordinate displacement, keep the de/dir-end advantage, leave a little room for distribution improvement (alternatives w010 = displacement 0.10, wk20/wk50 = move only 20–50 genes for distribution fine-tuning).

Tools: t2 generator script family, veckit.

Issues: 54.43 (rank 72/204) — de 46.8/dir 49.8/mmd 50.5/vario 50.1/d2 49.9/occ 54.1/scale 100/nh 51.1, a balanced runner-up, only 0.08 from scale_only 54.51.

Conclusion: the balanced variant is close to scale_only but does not beat it; w005 = 54.43, second highest.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-19 19:18 | w005 | w005（w 族 005 变体；文件名 t2_heart_val_extrap_w005.h5ad，17MB） | 54.43 | 46.8 | 49.8 | 50.5 | 50.1 | 49.9 | 54.1 | 100 | 51.1 | 72/204 | 09-19 19:18 提交漏记补录（portal 对账）；54.43 超官方地板（+4.4），距最佳 scale_only 54.51 仅 0.08——T2 extrap 第二高分；全指标均衡型（de 46.8/dir 49.8/mmd 50.5/vario 50.1/d2 49.9/occ 54.1/scale 100.0/nh 51.1），分布保真优先路线（与 T3 cmpw/pw 同逻辑）；未超最佳 |

### Experiment family: selday (selection day, closed)

Method: selday family — select cells by developmental day (selday30/50_scale), apply 30%/50% day selection to the E9.5 carrier then scale-adjust only.

Tools: t2 generator script family, veckit.

Issues: 27.54 / 28.9 — the lowest scores of the whole journey (mmd/vario/d2/occ all collapse); day selection destroys the E9.5 cell composition.

Conclusion: day selection is useless for extrap; formally closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-17 06:15 | selday30 | selday30_scale（文件名 t2_heart_val_extrap_selday30_scale.h5ad） | 27.54 | 46.4 | 47.4 | 16 | 25.8 | 19.8 | 46.1 | 100 | 20.6 | 69/185 | mmd 16.0/vario 25.8/d2 19.8/nh 20.6 全崩，远低于地板；与 T1 selday_f20 同族失败；方法细节待补充 |
| 2026-09-17 06:15 | selday50 | selday50_scale（文件名 t2_heart_val_extrap_selday50_scale.h5ad） | 28.9 | 46.4 | 47.2 | 17.1 | 26.8 | 25.5 | 48.7 | 100 | 22.1 | 69/185 | 同族崩盘，28.90 仍远低于地板；方法细节待补充 |

### Experiment family: cpfx (type-level displacement shift extrapolation)

Method: cpfx = cpf-family extrapolation variant: expression unchanged, coordinates displaced at the type level (n=8000, a=0.10); d2_distance normalizes and compares pairwise distance distributions — rigid scaling does not change shape, translation changes inter-type relative positions — d2 collapses to 5.7.

Tools: tools/_heart_extrap_cpfx.py, veckit.

Issues: 52.12 — d2_shape 5.7 collapse (morphology extrapolation heavily penalized); occupancy_dice 42.0.

Conclusion: conditional-flow extrapolation moving morphology dies the same way; the fourth morphology-line falsification — all morphology routes on the extrap board are closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-23 16:44 | cpfx_n8000_a10 | cpfx_n8000_a10（cpfx 族 n8000 a10 变体；文件名 t2_heart_val_extrap_cpfx_n8000_a10.h5ad，16MB） | 52.12 | 52.8 | 54.5 | 53.3 | 52.4 | 5.7 | 42 | 98.9 | 53 | 72/203 | cpfx 族（胚胎板 cpf015r5k 同族）用于 heart extrap；52.12 超官方地板（+2.12）但未超 scale_only 54.51（差 2.39）；d2_shape 5.7 崩为最大失分、occ 42.0 偏弱，mmd/vario/de 均衡尚可（53.3/52.4/52.8）；scale 98.9 略低于满分——extrap 板改形态再证伪（与 r6b70a20 同病），scale 类仍天花板；板人数 185→203；方法细节待补充 |

## Summary rows

- **Current best**: 54.51
- **Official floor (copy_last / wt_identity)**: 50
- **Board top (leader)**: 60.5
