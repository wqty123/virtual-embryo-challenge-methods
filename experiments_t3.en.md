# T3 experiment report: Gata4 KO perturbation response prediction (E8.75)

<p align="center"><a href="experiments_t3.md">中文</a> · English</p>

Metrics: de_score / de_direction / severity_slope / mmd_u / variogram; total ≈ 0.298·de + 0.250·dir + 0.251·sev + 0.120·mmd + 0.080·vario. Official floor 50 (wt_identity), measured floor (our upload) 45.81.

## Experiment overview (chronological concrete technique sequence)

`transfer global Δ` 40.98 (falsified: vario 49.8→12.2) → `wt_identity` measured floor 45.81 → `cardiac restricted` 44.85 (falsified) → `literature prior (Mab21l2 targets)` 45.80 (ties floor) → `state program` 45.78 (zero gain) → `mix KO mixture` (mix20 61.5 → mix70 64.60) → `kodir` 43.96 / `koq` 58.04 / `pk/ctl 26 genes` 38.91/43.14 (shut down) → `mx50amp` 57.15 → **`cmp celltype^β resampling` (b070 64.93 → b055 65.31)** → `cmpw carrier dilution` 65.49 → `pw` 64.47 / `prw` 54.49 → **`kb real-WT dilution of KO` (k65 66.36) → `kbb (k65×b055 combo)` 66.61 (current best)**, `kb k75` 65.32 (wrong direction)

## Experiment log (grouped by method family)

### Experiment family: transfer (global Δ perturbation transfer)

Method: add the global response Δ learned from E9.5 WT→Mab21l2 KO (mean KO − WT expression difference) to the E8.75 carrier (damp 1.0/1.5).

Tools: baselines/t3_shift_transfer.py, veckit.

Issues: damp1.5 real board 40.98 — variogram collapses 49.8→12.2; damp1.0 was never successfully submitted (no such file on the portal).

Conclusion: **global Δ destroys the distribution**: the KO response cannot be applied as a global scalar shift; the transfer family is closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 未提交 | A | transfer@1.0（全局 shift transfer） | 未提交 | — | — | — | — | — | — | portal 提交列表无此文件——从未成功提交；'板分未贴'之谜即此 |
| 2026-09-04 13:22 | B | transfer@1.5（全局） | 40.98 | 38.8 | 48.4 | 50 | 31.2 | 12.2 | 118/141 | 全局 Δ 推毁分布：vario 49.8→12.2 |

### Experiment family: wt_identity (floor probe)

Method: copy the WT expression directly as the prediction (E8.75 carrier + WT distribution).

Tools: baselines/t3_wt_identity.py (wt_identity is the official baseline definition, https://virtualembryo.ai/challenge/baselines), veckit.

Conclusion: T3 measured floor = 45.81, official floor scale = 50; every method is first compared against this.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-04 13:22 | F-dup | wt_identity（与 F 同文件重复上传） | 45.81 | 38.8 | 46.4 | 50 | 50.5 | 49.8 | — | 双传烧掉 1 名额（t3_slot_ledger 已记）；portal 两条 45.8 记录 |
| 2026-09-04 13:23 | F | wt_identity（地板探针） | 45.81 | 38.8 | 46.4 | 50 | 50.5 | 49.8 | 118/141 | 地板实榜=45.81；已被 mix60_ko 64.51 取代 |
| 2026-09-16 21:34 | wt-copy7000 | wt_copy_7000（WT 复制 7000 采样；文件名 t3_gata4_wt_copy_7000.h5ad） | 46.76 | 39.2 | 50.6 | 50 | 49.6 | 48.7 | 53/170 | 低于地板；rank 53/170；方法细节待补充 |

### Experiment family: cardiac (lineage-restricted transfer)

Method: apply the global Δ only to cardiac-lineage cells (lineage-restricted version).

Tools: baselines/t3_shift_transfer.py, veckit.

Issues: damp0.5 44.36 / damp0.25 44.85 — distribution metrics hold (mmd 48.8/49.8) but de drops to 37.4/37.7 (KO effect cannot be expressed).

Conclusion: lineage restriction protects the distribution but loses the effect; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-04 14:36 | C | cardiac@0.5（谱系限制 transfer） | 44.36 | 37.4 | 47 | 50 | 48.8 | 37.9 | 119/141 | 批次2 |
| 2026-09-04 14:36 | D | cardiac@0.25（谱系限制 transfer） | 44.85 | 37.7 | 46.9 | 50 | 49.8 | 41.5 | 119/141 | 批次2 |

### Experiment family: Gata4 state program (a25/a35/a50)

Method: E8.75 carrier 10pct + within-type normalization + Gata4 state program (a coefficients 0.25/0.35/0.50).

Tools: t3_rewrite script family, veckit.

Issues: the three variants score 45.78/45.79/45.80, tied with the floor (+0.00) — the state program produces no KO response.

Conclusion: three consecutive uploads each burn a quota with zero gain; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-05 20:55 | state-a25 | Gata4 状态程序 a25（E8.75 载体 10pct，型内归一化） | 45.78 | 38.5 | 46.7 | 50 | 50.7 | 49.8 | 126/149 | t3_rewrite 已上传；与 F 地板平齐（+0.00） |
| 2026-09-05 20:55 | state-a35 | Gata4 状态程序 a35（同上） | 45.79 | 38.5 | 46.7 | 50 | 50.7 | 49.8 | 126/149 | 同上；三连发之一 |
| 2026-09-05 20:55 | state-a50 | Gata4 状态程序 a50（同上） | 45.8 | 38.5 | 46.8 | 50 | 50.7 | 49.7 | 126/149 | 同上；三连发各占 1 名额，零增益 |

### Experiment family: mix (KO-mixture inference)

Method: construct the prediction as a mixture of "real KO cells + WT carrier" — mix ratio p∈{20,30,40,50,60,70}% (p% KO cells + (100−p)% WT carrier; p is the KO cell fraction); kofeat variants feed a Gata4 target-gene feature list (feat∈{0.05,0.1,0.2,0.35}, measured: larger amplitude monotonically worse); muld_m05 is the mix70 amplitude variant; cardiac/knn are lineage and nearest-neighbor variants.

Tools: T3 generator script family (mix series), veckit.

Issues: ① mix40_early 50.09 (+0.09) — mixing an early carrier gives almost nothing; ② cardiac/knn variants (59.72/61.82) lose to the original mix40_ko 63.58; ③ kofeat variants 64.06–64.52, smaller feat closer to the peak; ④ muld_m05 64.39 (sev 92.9 then-new high but mmd 50.4 drags); ⑤ mix70_ko 64.60 family peak, severity_slope 92.3 then-new high; ⑥ re-uploading mix70_ko (same file, 64.60 unchanged) burned quota.

Conclusion: higher mix ratio gives higher sev (mix70 sev 92.3); family peak 64.60. Mixing real cells buys mmd but sev cannot climb — "mix more" is not the main lever.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-16 21:34 | mix40-ko | mix40_ko（Gata4 混合 KO 推断；文件名 t3_gata4_mix40_ko.h5ad） | 63.58 | 51.9 | 59.5 | 86.2 | 58.2 | 57.3 | 53/170 | 已被 mix60_ko 64.51 取代（09-17）；仍超地板（+13.58）；rank 53/170；方法细节待补充 |
| 2026-09-16 21:34 | mix40-early | mix40_early（混合 40% 早期载体；文件名 t3_gata4_mix40_early.h5ad） | 50.09 | 47.1 | 58.4 | 50 | 47.2 | 40.2 | 53/170 | 略超地板（+0.09）；rank 53/170；方法细节待补充 |
| 2026-09-17 06:19 | mix20-ko | mix20_ko（Gata4 混合 KO 推断 20%；文件名 t3_gata4_mix20_ko.h5ad） | 61.5 | 52.6 | 58.9 | 79.5 | 55.6 | 55.3 | 49/170 | mix 比例 20%；rank 49/170；方法细节待补充 |
| 2026-09-17 06:19 | mix30-ko | mix30_ko（混合 KO 推断 30%；文件名 t3_gata4_mix30_ko.h5ad） | 62.37 | 51.3 | 59.5 | 83.2 | 56.1 | 57.3 | 49/170 | mix 比例 30%；severity_slope 83.2；rank 49/170；方法细节待补充 |
| 2026-09-17 06:19 | mix40-ko-cardiac | mix40_ko cardiac 变体（文件名 t3_gata4_mix40_ko_cardiac.h5ad） | 59.72 | 50 | 56.9 | 84.4 | 46.1 | 48.3 | 49/170 | cardiac 变体不敌原版 mix40_ko 63.58；mmd 46.1 最弱；rank 49/170；方法细节待补充 |
| 2026-09-17 06:19 | mix40-ko-knn | mix40_ko knn 变体（文件名 t3_gata4_mix40_ko_knn.h5ad） | 61.82 | 52.6 | 57.3 | 80.8 | 58.8 | 55.6 | 49/170 | knn 变体不敌原版 mix40_ko 63.58；rank 49/170；方法细节待补充 |
| 2026-09-17 06:19 | mix50-ko | mix50_ko（混合 KO 推断 50%；文件名 t3_gata4_mix50_ko.h5ad） | 64.37 | 52.6 | 59.7 | 88.5 | 58.8 | 56.1 | 49/170 | mix 比例 50%；rank 49/170；方法细节待补充 |
| 2026-09-17 06:19 | mix60-ko | mix60_ko（混合 KO 推断 60%；文件名 t3_gata4_mix60_ko.h5ad） | 64.51 | 53.3 | 59.8 | 90.4 | 54.8 | 54.7 | 49/170 | 已被 mix70_ko 64.60 取代（09-17）；mix 60% 时 severity_slope 90.4；rank 49/170；方法细节待补充 |
| 2026-09-17 15:09 | mix70-ko | mix70_ko（混合 KO 推断 70%；文件名 t3_gata4_mix70_ko.h5ad） | 64.6 | 53.3 | 59.8 | 92.3 | 52.3 | 53.7 | 50/172 | 超 mix60_ko 64.51；已被 cmp_n6000_b070 64.93 取代（09-19）；mix 比例 70% 续升、severity_slope 92.3 新高；rank 50/172；方法细节待补充 |
| 2026-09-18 03:21 | mix70-muld-m05 | mix70_muld_m05（mix70 变体 muld m0.5；文件名 t3_gata4_mix70_muld_m05.h5ad） | 64.39 | 54.1 | 58.6 | 92.9 | 50.4 | 53.1 | 51/175 | mix70 变体 muld_m05；64.39 低于 mix70_ko 64.60（差 0.21）；sev 92.9 新高但 mmd 50.4 拖累；rank 51/175；方法细节待补充 |
| 2026-09-18 12:11 | mix70-kofeat01 | mix70_kofeat01（mix70 变体 feat=0.1；文件名 t3_gata4_mix70_kofeat01.h5ad） | 64.45 | 53.3 | 59.7 | 92.2 | 52 | 53.1 | 53/175 | mix70 kofeat 族 feat=0.1；64.45 低于 mix70_ko 64.60（差 0.15）；rank 53/175；方法细节待补充 |
| 2026-09-18 12:11 | mix70-kofeat02 | mix70_kofeat02（mix70 变体 feat=0.2；文件名 t3_gata4_mix70_kofeat02.h5ad） | 64.3 | 53.3 | 59.6 | 92 | 51.7 | 52.7 | 53/175 | mix70 kofeat 族 feat=0.2；64.30 族内次低；rank 53/175；方法细节待补充 |
| 2026-09-18 12:12 | mix70-kofeat005 | mix70_kofeat005（mix70 变体 feat=0.05；文件名 t3_gata4_mix70_kofeat005.h5ad） | 64.52 | 53.3 | 59.7 | 92.2 | 52.1 | 53.4 | 53/175 | mix70 kofeat 族 feat=0.05；64.52 族内最高、仍低于 mix70_ko 64.60（差 0.08）；feat 越小越接近峰值；rank 53/175；方法细节待补充 |
| 2026-09-18 12:12 | mix70-kofeat035 | mix70_kofeat035（mix70 变体 feat=0.35；文件名 t3_gata4_mix70_kofeat035.h5ad） | 64.06 | 53.3 | 59.3 | 91.7 | 51.1 | 52 | 53/175 | mix70 kofeat 族 feat=0.35；64.06 族内最低；rank 53/175；方法细节待补充 |
| 2026-09-19 16:01 | mix70_ko-redo | mix70_ko 重投（同文件再传，得分不变） | 64.6 | 53.3 | 59.8 | 92.3 | 52.3 | 53.7 | 53/177 | 重投烧名额，分数与 09-18 一致 |

### Experiment family: kodir (KO direction)

Method: construct the response along the KO direction (a=0.10).

Tools: T3 generator script family, veckit.

Issues: 43.96 below the floor, variogram 18.1 collapse.

Conclusion: direction construction destroys the distribution; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-17 15:09 | kodir-a10 | kodir_a10（文件名 t3_gata4_kodir_a10.h5ad） | 43.96 | 42.6 | 49.6 | 50 | 40.4 | 18.1 | 50/172 | kodir 族 a10；43.96 低于地板，vario 18.1 崩；方法细节待补充 |

### Experiment family: ko2 (KO dual-path)

Method: dual-path KO response construction, n∈{5000,6000}, b=0.60.

Tools: T3 generator script family, veckit.

Issues: 64.68 (n6000) / 64.75 (n5000), not above cmp_n6000_b070 (64.93).

Conclusion: ko2 is cmp's predecessor but does not fully express the KO effect; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-19 18:43 | ko2_n6000_b60 | ko2_n6000_b60（文件名 t3_gata4_ko2_n6000_b60.h5ad） | 64.68 | 54.8 | 60.2 | 97.2 | 43.4 | 46.2 | 53/178 | ko2 变体；未超 cmp_n6000_b070 64.93 |
| 2026-09-19 18:43 | ko2_n5000_b60 | ko2_n5000_b60（文件名 t3_gata4_ko2_n5000_b60.h5ad） | 64.75 | 55.6 | 59.8 | 97.1 | 43.4 | 45.9 | 53/178 | ko2 变体；未超 cmp_n6000_b070 64.93 |

### Experiment family: koq (KO quantized)

Method: quantized KO response construction (n=5000).

Tools: T3 generator script family, veckit.

Issues: 58.04 — mmd 24.8/vario 27.1 double collapse.

Conclusion: the koq line fails; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-19 19:04 | koq50_n5000 | koq50_n5000（文件名 t3_gata4_koq50_n5000.h5ad） | 58.04 | 50 | 58.2 | 93.4 | 24.8 | 27.1 | 53/178 | mmd 24.8/vario 27.1 双崩；koq 线失败 |

### Experiment family: pk/ctl (26-gene per-gene transforms)

Method: pk26g18 (26 program genes, g=18 variant) / ctlp26 (control 26 genes) — apply per-gene transforms to the named genes only, leave the rest untouched; belongs to the T3 per-gene transform family (pk/ctlp/koq/kodir/mx50amp, variogram 5/5 collapse to 10.8–27.1).

Tools: T3 generator script family, veckit.

Issues: pk26g18 38.91 (mmd 21.4/vario 10.8 double collapse); ctlp26 43.14 (mmd 7.9/vario 19.4 double collapse).

Conclusion: none of the nine per-gene transform routes on T3 survives; the 26-gene program family is shut down.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-21 02:04 | pk26g18 | pk26g18（文件名 t3_gata4_pk26g18.h5ad） | 38.91 | 37 | 47.5 | 50 | 21.4 | 10.8 | 47/182 | pk26g18 族；38.91 低于官方地板 50 与 cmp_n6000_b070 64.93；severity_slope 50.0 为地板档、mmd 21.4/vario 10.8 双崩；方法细节待补充 |
| 2026-09-21 02:36 | ctlp26 | ctlp26（文件名 t3_gata4_ctlp26.h5ad） | 43.14 | 49.4 | 53.3 | 50 | 7.9 | 19.4 | 47/182 | ctlp26 族；43.14 高于 pk26g18 38.91，仍低于官方地板 50 与 cmp_n6000_b070 64.93；severity_slope 50.0 为地板档、mmd 7.9/vario 19.4 双崩；26 族确认失败关停 |

### Experiment family: mx50amp (50% mixture + amplitude)

Method: 50% mixture (mx50) + amplitude 0.92 (amp) construction — apply a transform of amplitude 0.92 along the KO-response direction; belongs to the T3 per-gene/amplitude transform family (variogram 5/5 collapse to 10.8–27.1).

Tools: tools/_t3_mx50_amp.py, veckit.

Issues: 57.15 — severity_slope 90.6 high but variogram 15.8 collapse.

Conclusion: amplitude construction destroys vario; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-21 05:04 | mx50amp092 | mx50amp092（文件名 t3_gata4_mx50amp092.h5ad） | 57.15 | 46 | 55.4 | 90.6 | 46.6 | 15.8 | 47/182 | mx50amp092 族；57.15 超官方地板 50（+7.15）但低于 cmp_n6000_b070 64.93；severity_slope 90.6 高、mmd 46.6 偏弱，vario 15.8 崩；方法细节待补充 |

### Experiment family: cmp (celltype^β resampling)

Method: cmp = resample by cell type (celltype^β exponential flattening of the type distribution, β=0.70/0.55/1.00, n=6000; β=1.00 is the natural type proportion, β<1 compresses the celltype distribution).

Tools: T3 generator script family (cmp series), veckit.

Issues: ① cmp_n6000_b070 64.93 breaks the 64.6 plateau (de 56.3/sev 97.0 jump, mmd/vario each drop ≈10); ② b=1.00 63.35, all five metrics below b070; ③ b=0.55 65.31 (de 56.3 flat, dir 60.3/sev 97.1 up, mmd/vario both up) — the low-β side is better; larger β is worse (slope ≈ −5.3 points per unit β).

Conclusion: cmp_n6000_b055 = 65.31; **compressing the celltype distribution (β<1) is the core T3 gain**.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-19 16:02 | cmp_n6000_b070 | cmp_n6000_b070（新机制 cmp；文件名 t3_gata4_cmp_n6000_b070.h5ad） | 64.93 | 56.3 | 60.1 | 97 | 42.7 | 45.4 | 53/177 | 破 64.6 平台；de 56.3/sev 97.0 大涨，代价 mmd 42.7/vario 45.4 各降 ~10；T3 杠杆点=精准打 KO 效应而非多混真实细胞 |
| 2026-09-23 16:44 | cmp_n6000_b100 | cmp_n6000_b100（cmp 族 b100 变体；文件名 t3_gata4_cmp_n6000_b100.h5ad，12MB） | 63.35 | 54.1 | 59.2 | 96.8 | 39.4 | 42.7 | 48/186 | cmp 族 b100 变体；63.35 超官方地板（+13.35）但未超 cmp_n6000_b070 64.93（差 1.58）；de 54.1/dir 59.2/sev 96.8/mmd 39.4/vario 42.7 五项全低于 b070（56.3/60.1/97.0/42.7/45.4）；b=100 非甜点，b=70 仍最佳；方法细节待补充 |
| 2026-09-23 17:02 | cmp_n6000_b055 | cmp_n6000_b055（cmp 族 b055 变体；文件名 t3_gata4_cmp_n6000_b055.h5ad，12MB） | 65.31 | 56.3 | 60.3 | 97.1 | 44.2 | 47.1 | 48/187 | cmp 族 b055 变体；65.31 超 cmp_n6000_b070 64.93 成为新最佳（+0.38）；de 56.3 持平、dir 60.3/sev 97.1 微升、mmd 44.2(+1.5)/vario 47.1(+1.7) 双升——五项全面不输 b070；b 参数低侧更优，b=0.55 新甜点；板人数 186→187；方法细节待补充 |

### Experiment family: cmpw (KO pool + E8.75 WT carrier dilution)

Method: cmpw = flat KO pool from cmp_b070 diluted with the E8.75 WT carrier — 70% KO pool (β=0.70) + 30% carrier, k = carrier fraction (k=1.00 is cmp_b070 itself, k50–k85 the dilution series; n=6000).

Tools: tools/_t3_cmpw_make.py, _t3_cmpw_axes2.py, veckit.

Issues: cmpw_n6000_k70 65.49 beats cmp_b055 (+0.18): de 54.8 (−1.5)/sev 92.4 (−4.7) give way, mmd 55.2 (+11.0)/vario 53.9 (+6.8) jump.

Conclusion: carrier dilution redeems the distribution axes (mmd/vario) but pays a sev cost (≈4.6 points, confirmed on two independent paths); cmpw is transitional, the kb family completes sev on top of it.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-23 17:32 | cmpw_n6000_k70 | cmpw_n6000_k70（cmpw 族 k70 变体；文件名 t3_gata4_cmpw_n6000_k70.h5ad，12MB） | 65.49 | 54.8 | 60.1 | 92.4 | 55.2 | 53.9 | 48/187 | cmpw 族 k70 变体；65.49 超 cmp_n6000_b055 65.31 成为新最佳（+0.18）；换机制：de 54.8(-1.5)/sev 92.4(-4.7) 让位，mmd 55.2(+11.0)/vario 53.9(+6.8) 暴涨——分布保真优先路线（与 pw050 同逻辑但幅度更大）；板人数 187 不变；方法细节待补充 |

### Experiment family: pw (prior weighting, falsified)

Method: pw = prior weighting — additive weighting on cmp along the prior axis (cell-type variance axis) (p=0.50/1.00, n=6000); root cause: treated "additive perturbation dp→dp+Δ" as "constant scaling dp→c·dp" (rank invariance only protects the latter); measured |d(pb)|=0.0414 is the additive term.

Tools: T3 generator script family (pw series), veckit.

Issues: pw050 64.47 (mmd/vario above cmp but de 54.8/dir 58.1 slightly lower, not above 64.93); pw100 62.87 (de/dir lower) — monotonically decreasing in β 0→0.5→1.0.

Conclusion: prior weighting is net-negative (monotone in β), falsified; on T3 any operation that deviates from the natural KO-cell distribution weakens de.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-23 14:07 | pw050 | pw050（文件名 t3_gata4_pw050_n6000.h5ad，12MB） | 64.47 | 54.8 | 58.1 | 97.4 | 44.2 | 48.3 | 48/186 | pw 族 pw050 变体；64.47 超官方地板（+14.47）但未超 cmp_n6000_b070 64.93（差 0.46）；mmd 44.2/vario 48.3 均高于最佳（cmp 42.7/45.4），de 54.8/dir 58.1 略低；板人数 182→186；方法细节待补充 |
| 2026-09-23 14:07 | pw100 | pw100（文件名 t3_gata4_pw100_n6000.h5ad，12MB） | 62.87 | 52.6 | 56 | 97.7 | 41.7 | 45.7 | 48/186 | pw 族 pw100 变体；62.87 超官方地板（+12.87）但低于 pw050 64.47 与最佳 64.93；de 52.6/dir 56.0 低于 pw050；sev 97.7 为族内新高；方法细节待补充 |

### Experiment family: prw (official population_reweight + GSE prior)

Method: prw = official population_reweight operator: resample the WT carrier with a WT-vs-KO classifier (this operator cannot produce a strong enough response in principle) + GSE external prior (s=0.10, 1.2MB small model; the GSE208162 prior is orthogonal to the Mab21l2 response: 48/267 in the DE set = random expectation).

Tools: tools/_gse_cells_make.py, _t3_gse_prior.py, veckit; GSE208162 external prior data (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208162).

Issues: 54.49 — severity_slope 70.6 far below cmp's 97.0 (KO effect not expressed); de 44.9/dir 51.3 weak; mmd 53.1/vario 51.9 distribution fidelity achieved.

Conclusion: distribution preserved but the effect cannot be expressed (sev 70.6 vs cmp 97.0); external prior direction alignment does not predict the score; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-23 16:45 | prw_gse_s010 | prw_gse_s010（prw 族 gse 变体 s=0.10；文件名 t3_gata4_prw_gse_s010.h5ad，1.2MB） | 54.49 | 44.9 | 51.3 | 70.6 | 53.1 | 51.9 | 48/186 | prw 族 gse s010 变体；54.49 超官方地板（+4.49）但远低于最佳 cmp_n6000_b070 64.93（差 10.44）；sev 70.6 远低于 cmp 97.0（KO 效应未打出），de 44.9/dir 51.3 弱；mmd 53.1/vario 51.9 高（分布保真但缺效应）；文件仅 1.2MB 小模型；方法细节待补充 |

### Experiment family: kb (real WT dilution of KO, A/B falsification re-check)

Method: kb = dilute KO with real WT cells (kbgen: flat KO pool + WT carrier dilution, k=65/75 dilution ratios, n=6000; kbb is the kb6000×b055 combination k=65, b=0.55); a local A/B half-split experiment once judged it "universally worse than doing nothing, the advantage is self-justifying", but the re-check found that falsification used two already-falsified local axes + a wrong carrier recipe (the kb carrier wrongly used E9.5 WT; the true-value carrier is reverse-engineered through Gata4 means as E8.75 WT), so it does not constitute a counter-argument to the real-board scores (66.36/66.61).

Tools: tools/_t3_kbgen.py, _t3_kb_ab.py, veckit.

Issues: ① kb6000_k65 66.36 beats cmpw (de 56.3/dir 62.2 new dir high/sev 97.9 new sev high/mmd 45.0/vario 50.5); ② kbb_n6000_b055_k65 66.61: de/dir flat, sev 98.0/mmd 46.1/vario 51.8 all up; ③ kb6000_k75 65.32, all five metrics down (vario −3.0) — k=65 is optimal.

Conclusion: **kbb_n6000_b055_k65 = 66.61** (rank 48/187), current T3 best. Dilution ratio k=65 + β=0.55 is optimal; k=75 is the wrong direction.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-19 19:17 | kb6000_k65 | kb6000_k65（kb 族 k65 变体；文件名 t3_gata4_kb6000_k65.h5ad，12MB） | 66.36 | 56.3 | 62.2 | 97.9 | 45 | 50.5 | 48/187 | kb 族 k65 变体；66.36 超 cmpw_n6000_k70 65.49 成为新最佳（+0.87）；09-19 19:17 已提交但此前漏记（现补录，rank 48/187 为当前板状态）；de 56.3/dir 62.2（dir 新高）/sev 97.9（sev 新高）/mmd 45.0/vario 50.5——de/sev 回 cmp 系高位且 dir/sev 双新高，mmd/vario 介于 cmp 系与 cmpw 系之间；方法细节待补充 |
| 2026-09-23 17:42 | kbb_n6000_b055_k65 | kbb_n6000_b055_k65（kb6000 与 b055 组合变体；文件名 t3_gata4_kbb_n6000_b055_k65.h5ad，12MB） | 66.61 | 56.3 | 62.2 | 98 | 46.1 | 51.8 | 48/187 | kbb 系（kb6000×b055 组合）；66.61 超 kb6000_k65 66.36 成为新最佳（+0.25）；de 56.3/dir 62.2 持平、sev 98.0（新高）/mmd 46.1(+1.1)/vario 51.8(+1.3) 三涨——kb 系五维全面提升，破 66.36 平台；方法细节待补充 |
| 2026-09-23 17:43 | kb6000_k75 | kb6000_k75（kb 族 k75 变体；文件名 t3_gata4_kb6000_k75.h5ad，12MB） | 65.32 | 54.8 | 61.3 | 97.5 | 44.9 | 47.5 | 48/187 | kb 族 k75 变体；65.32 未超 kb6000_k65 66.36（五项全线下滑：de -1.5/dir -0.9/sev -0.4/mmd -0.1/vario -3.0）——k=65 仍甜点，k=75 方向错误；方法细节待补充 |

## Summary rows

- **Current best**: 66.61
- **Official floor (copy_last / wt_identity)**: 50
- **Measured floor (our upload)**: 45.81
- **Board top (leader)**: 75.2
