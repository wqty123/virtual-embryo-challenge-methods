# T1 experiment report: single-cell temporal extrapolation (E8.5→E9.5 → predict E10.5)

<p align="center"><a href="experiments_t1.md">中文</a> · English</p>

Metrics: de_score / de_direction / mmd_u / variogram; total ≈ 0.25·de + 0.25·dir + 0.30·mmd + 0.20·vario. Official floor 50 (copy_last), measured floor (our upload) 46.84. Each family records: method, tools, issues, conclusion; the in-family submission log is the full result data (from the official scoring ledger, UTC).

## Experiment overview (chronological concrete technique sequence)

`pseudobulk shift (global drift)` 48.13 → damp grid shift@2.5 48.85 → `OT mixture` 47.52 → `Markov flux` 44.19 (falsified) → `program mixture` 47.34 (vario 31.7 collapse) → `multiplicative` 48.27 → `marker momentum` 48.80 → `copy_last` measured floor 46.84 → `sel family` 30.21~47.02 (all collapse) → `dir24/dirprop` 47.19 → `momentum mask` 49.49 → `mm library-size normalization` 49.93 → `covsafe` 48.09 (falsified) → `vs variance amplification` 50.67 → **`kp knowledge-program shift + variance amplification / maturity weighting`: kp3_w_a025 52.18 → kp7_m_b050 53.67 (current best)**

## Experiment log (grouped by method family)

### Experiment family: pseudobulk shift (global drift)

Method: use E9.5 cells as the carrier and add a per-gene global drift (Δgene = mean_gene(E9.5) − mean_gene(E8.5) × damp), damp∈{0.25,0.5,1.0,1.25,1.5,2.0,2.5}; asymmetric variants use different up/down coefficients (up1.5/dn0.5, up1.5/dn0.75); scattered probe shift@0.5+s0.5 adds Gaussian noise on the drift; shift@2.5 is the damp-knee test. Implementation: baselines/t1_shift.py.

Tools: baselines/t1_shift.py (recipe follows the official pseudobulk shift baseline, https://virtualembryo.ai/challenge/baselines), local veckit scorer, ledger backfill.

Issues: ① variogram low across the family (35.7–44.5) — the global shift breaks the gene–gene covariance structure; ② de_score caps at ≈45.3 — a global scalar cannot hit the "named genes"; ③ damp>2.5 gives no gain (S2.5 is the knee); ④ asymmetric variants (up1.5/dn0.5, up1.5/dn0.75) are worse than symmetric; ⑤ scattered probe P4@0.5+s0.5 only 42.29 — noise directly destroys vario (−19) and mmd.

Conclusion: shift is the strongest simple baseline; family peak shift@2.5 = 48.85 (rank 142/202, de 45.3/dir 56.4/mmd 55.4/vario 34.1), ≈2 points above the measured floor 46.84; but "trade vario for de" reaches its limit here and is superseded by per-type / per-state generators.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-04 11:21 | A | shift@1.0（伪bulk 漂移） | 48.13 | 43.3 | 55 | 52 | 39.8 | 155/192 | E3 主力 |
| 2026-09-04 12:24 | P4 | shift@0.5+s0.5（弥散探针） | 42.29 | 41.7 | 53.6 | 44.8 | 25.3 | — | 弥散证伪：噪声毁 vario(-19)+mmd |
| 2026-09-04 12:29 | P2 | shift@0.5 | 47.29 | 40.6 | 53.9 | 50.5 | 42.6 | — | portal 文件名校正：47.29 实为 damp0.5（UPLOAD_SHEET 曾挂 P3@0.75） |
| 2026-09-04 12:29 | P2-dup | shift@0.5（重复上传） | 47.29 | 40.6 | 53.9 | 50.5 | 42.6 | — | 同文件双传；已撤回——'误重复'即此行 |
| 2026-09-04 12:33 | P1 | shift@0.25 | 46.7 | 38.6 | 52.9 | 49.8 | 44.5 | — | portal 文件名校正：46.70 实为 damp0.25（曾挂 P2@0.5）；damp0.75 从未上传 |
| 2026-09-05 16:57 | L1 | shift@1.25 | 48.34 | 43.8 | 55.4 | 52.7 | 38.7 | — | E4b |
| 2026-09-05 17:01 | L2 | shift@1.5 | 48.53 | 44.2 | 55.8 | 53.4 | 37.6 | — | E4b；E4 暂定候选（vario 更高档） |
| 2026-09-05 17:02 | L3 | shift@2.0 | 48.74 | 44.8 | 56.2 | 54.5 | 35.7 | 136/195 | 已被 S2.5 48.85 取代（09-08）；E4b 最高档 |
| 2026-09-05 17:04 | L5 | shift up1.5/dn0.5（非对称） | 46.42 | 41 | 54.9 | 50.8 | 36 | — | 非对称双输（de/vario 均差于对称） |
| 2026-09-05 17:06 | L6 | shift up1.5/dn0.75（非对称） | 47.1 | 42.3 | 55.2 | 51.4 | 36.4 | — | dn0.75 族内优于 dn0.5，族输对称 |
| 2026-09-08 03:00 | S2.5 | shift@2.5（damp2.5 拐点测试） | 48.85 | 45.3 | 56.4 | 55.4 | 34.1 | 142/202 | 已被 mommask0p01 49.49 取代（09-18）；de 45.3/vario 34.1 拐点未到，用 vario 换 de 到头 |
| 2026-09-08 03:00 | S-sr | shift+稳定性残差（shift_stability_residual） | 47.63 | 43.3 | 55.1 | 52.9 | 35.7 | 142/202 | 残差分支低于同档 shift（对比 S1.25 48.34），无增益；剖面≈shift@1.25 |

### Experiment family: OT mixture (WOT coupling + type-transfer resampling)

Method: learn a cell coupling matrix with WOT on E8.5→E9.5, resample E9.5 cells by type-transition probability; masked variant A (edge mask 378→61 edges, dropping low-quality coupling edges) — otmixp includes growth factor π (birth–death process), otmixm without growth. Implementation: baselines/t1_otmix.py.

Tools: baselines/t1_otmix.py, wot_analysis/ (WOT coupling matrix and edge mask, WOT library https://github.com/broadinstitute/wot), veckit.

Issues: ① otmixp@1.0 variogram collapses to 28.8 (generation amplitude destroys the variance structure); ② OT mixture without the shift skeleton (otmixm) gets de 44.3/mmd 53.6 but is dragged down by vario; ③ damp variant (0.3) 46.75 below the shift family.

Conclusion: the OT-mixture route fails — type-transfer resampling cannot replace controlled generation at the expression level; family peak otmixp@1.0 = 47.52.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-04 11:15 | B | otmixp@1.0（掩膜A OT+生长π） | 47.52 | 44.9 | 56.6 | 54.6 | 28.8 | — | E3 结构赌注；variogram 崩（28.8） |
| 2026-09-04 11:17 | C | otmixm@1.0（掩膜A OT 无生长） | 46.86 | 44.3 | 55.1 | 53.6 | 29.7 | — | E3 干净 mmd 备选，殿后 |
| 2026-09-04 12:25 | P5 | otmixm@0.3 | 46.75 | 41.4 | 53.9 | 50.7 | 38.6 | — | E4a |

### Experiment family: Markov flux (time-homogeneous transition rule)

Method: treat the transition matrix learned on E8.5→E9.5 as a fixed rule and apply it to the E9.5 carrier to generate the "next stage" (time-homogeneity assumption). The full and non-full versions were submitted on the same day.

Tools: t1_rewrite script family, veckit.

Issues: both versions score identically 44.19 (de 38.2/dir 52.2/mmd 46.1/vario 38.8), below the measured floor 46.84; a local proxy once gave an optimistic 0.964 signal, the real board falsified it — the transition rule itself changes over time.

Conclusion: **the time-homogeneity assumption is falsified**; the Markov flux family is closed. A textbook case of an untrustworthy local proxy.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-07 04:53 | Mk | markov_flux_full damp0.5（马尔可夫通量全模型） | 44.19 | 38.2 | 52.2 | 46.1 | 38.8 | 139/198 | 新提交；de 38.2 全族最低档、mmd 46.1/vario 38.8 双弱，44.19 低于地板且低于全部 shift 族，零增益 |
| 2026-09-07 05:07 | Mk2 | markov_flux damp0.5（马尔可夫通量，非 full 版） | 44.19 | 38.2 | 52.2 | 46.1 | 38.8 | 139/198 | 与 full 版（04:53）同分 44.19、同剖面，零增益；两版等效，双传各占 1 名额 |

### Experiment family: OT assignment + program mixture (linear combination of programs)

Method: OT-assignment coupling plus a linear combination of known "programs" (gene program modules) to generate new cells; ablation variants remove birth (no_birth) and growth (no_growth).

Tools: t1_rewrite script family, veckit.

Issues: 45.22 without the shift skeleton, below the measured floor 46.74; removing birth loses 0.67, removing growth loses 0.42 (both weakly positive but the skeleton is too weak); program mixtures can only interpolate inside the convex hull of known programs and cannot generate genuinely new states.

Conclusion: convex-hull deadlock — "new states" require handling population birth/death; linear program combination is not enough; family peak 45.22, closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-08 02:57 | OTP | OT 分配+程序混合（prod ot_program_mix） | 45.22 | 39.7 | 54.7 | 46.8 | 37.8 | 142/202 | 无 shift 骨架的 OT+程序混合低于实测地板（45.22<46.74），零增益 |
| 2026-09-08 02:58 | OTP-nb | OT 程序混合 无 birth（no_birth） | 44.55 | 38.3 | 53.7 | 46.3 | 38.2 | 142/202 | ablation：去 birth 降 0.67，birth 有微弱增益但骨架弱 |
| 2026-09-08 02:59 | OTP-ng | OT 程序混合 无 growth（no_growth） | 44.8 | 38.6 | 54 | 46.6 | 38.3 | 142/202 | ablation：去 growth 降 0.42；growth 增益亦微弱 |

### Experiment family: shift + anonymous program mixture

Method: stack an anonymous program mixture (linear combination of unknown program sources) on the shift@1.0 skeleton.

Tools: t1_rewrite script family, veckit.

Issues: de 44.1 reaches the shift@1.25 tier, but variogram collapses to 31.7 and the total 47.34 is below pure shift@1.0 (48.13) — a large mixture amplitude destroys the covariance structure.

Conclusion: generated content must be small in amplitude, position-controlled and added last; anonymous mixture closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-08 02:59 | S-am | shift+匿名程序混合（shift_anonymous_program_mix） | 47.34 | 44.1 | 55.5 | 53.6 | 31.7 | 142/202 | de 达 shift@1.25 档但 vario 崩（31.7），总分低于纯 shift@1.0（48.13）——匿名混合毁变异结构 |

### Experiment family: multiplicative (low-rank multiplicative growth)

Method: E9.5 expression × exp(0.25 · rank8 low-rank matrix × masked ancestors), a multiplicative model with a rank-8 low-rank growth factor.

Tools: t1_rewrite script family, veckit.

Issues: de 39.6 weaker than the shift family; mmd 51.0/vario 48.1 better than L4, but the total 48.27 still below shift@2.0 (48.74).

Conclusion: the multiplicative variant does not beat additive shift; low-rank multiplicative growth does not match the real de response; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-05 21:41 | mult | multiplicative_full_a25（E9.5×exp(0.25·rank8 低秩×掩膜祖先乘性） | 48.27 | 39.6 | 53.7 | 51 | 48.1 | 138/198 | t1_rewrite 已上传（其 README 曾写“not uploaded”）；de 39.6 弱于 shift 族，mmd/vario 优于 L4 |

### Experiment family: marker program momentum

Method: per-program momentum (r ∝ (s/ś)^+0.5, type-specific rate) on the shift@2.5 skeleton, marker-program version.

Tools: t1_rewrite script family, veckit.

Issues: 48.80 ties shift@2.5 (48.85) — de/vario slightly lower, dir/mmd slightly higher; per-program momentum does not beat the global damp.

Conclusion: per-program momentum does not beat global damp; stage-C probe closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-08 13:43 | Mpm | marker_program_momentum@2.5（marker 程序动量） | 48.8 | 45 | 56.6 | 55.5 | 33.7 | 143/202 | 阶段 C 探针1：持平 shift@2.5（48.80 vs 48.85），de/vario 略降、dir/mmd 微升——per-program 动量未超全局 damp |

### Experiment family: mix20 + E8.5 carrier mixture

Method: a submission mixing 80% E9.5 prediction with 20% original E8.5 cells.

Tools: veckit, ledger.

Issues: 46.37 below the measured floor 46.84 and shift@2.5 (48.85).

Conclusion: mixing in old-stage cells reduces distribution fit; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-16 21:44 | mix20-e85 | mix20 + E8.5（文件名 t1_val_mix20_e85.h5ad） | 46.37 | 38.4 | 51.3 | 47.6 | 48.3 | 166/232 | 低于实测地板与 48.85；方法细节待补充 |

### Experiment family: copy_last (copy previous stage, floor probe)

Method: copy the E9.5 expression directly as the prediction (5118-cell sample).

Tools: veckit, ledger.

Issues: measured floor 46.84 (09-16 build) is 0.10 above the early L4 probe 46.74; uploading the same file twice burned quota (21:44 and 21:45 identical scores).

Conclusion: measured floor = 46.84, official floor = 50 (the official scale fixes the floor at 50); copy_last is the zero-information baseline every method must be compared against.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-05 06:49 | L4 | copy_last（damp0.0 地板探针） | 46.74 | 37.9 | 51.4 | 49.1 | 48.5 | — | 地板实榜=46.74（列表显示 46.7）；逐项已抓 2026-09-06 |
| 2026-09-16 21:44 | copy5118 | copy_last 5118 采样（文件名 t1_val_copy_5118.h5ad） | 46.84 | 38.5 | 52.4 | 48.1 | 48.5 | 166/232 | 新实测地板（46.84 超 L4 的 46.74）；方法细节待补充；09-16 21:45 同文件再传（双传烧 1 名额） |
| 2026-09-16 21:45 | copy5118-dup | copy_last 5118 采样（同文件重复上传） | 46.84 | 38.5 | 52.4 | 48.1 | 48.5 | 166/232 | 与 21:44 同文件双传（烧 1 名额）；分数相同 |
| 2026-09-18 03:34 | copy-last-5118 | copy_last_5118（copy_last 族 5118 采样；文件名 t1_copy_last_5118.h5ad） | 46.56 | 37.7 | 51.3 | 49 | 48.2 | 171/238 | copy_last 族（5118 采样）；46.56 低于实测地板 46.84/48.85；mmd 49.0/vario 48.2 正常但 de 37.7 弱；rank 171/238；方法细节待补充 |

### Experiment family: sel selection family (selday/selpc1/selanti)

Method: generate by "selection" logic — selday (select by developmental day proportion), selpc1 (select by PC1), selanti (anti-selection), proportion f∈{20,30,40,50}%.

Tools: T1 generator script family, veckit.

Issues: the whole family collapses — selpc1_f20 30.21 is the lowest score of the whole journey (mmd 15.7/vario 19.6 double collapse); selday only exceeds the floor at f50 (47.02) but still below shift@2.5; selanti_f50 42.66 (mmd 37.2 weak).

Conclusion: generating by hand-made "selection rules" is the wrong direction; the family is closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-17 06:13 | selday-f20 | selday_f20（文件名 t1_val_selday_f20.h5ad） | 39.92 | 41.6 | 53.3 | 31.1 | 34.4 | 166/232 | mmd 31.1/vario 34.4 双崩，39.92 远低于地板；方法细节待补充 |
| 2026-09-17 06:20 | selpc1-f20 | selpc1_f20（文件名 t1_val_selpc1_f20.h5ad） | 30.21 | 39.7 | 46.6 | 15.7 | 19.6 | 166/232 | selpc1 族 f20；30.21 为 sel 族最低，mmd 15.7/vario 19.6 双崩 |
| 2026-09-17 06:20 | selday-f30 | selday_f30（文件名 t1_val_selday_f30.h5ad） | 43.35 | 42.1 | 55.1 | 37.8 | 38.6 | 166/232 | selday 族；低于实测地板 46.84；mmd 37.8/vario 38.6 偏弱 |
| 2026-09-17 06:22 | selpc1-f30 | selpc1_f30（文件名 t1_val_selpc1_f30.h5ad） | 32.77 | 39 | 46.2 | 21.4 | 25.3 | 166/232 | selpc1 族；32.77 崩盘级（mmd 21.4/vario 25.3 双崩） |
| 2026-09-17 06:23 | selanti-f50 | selanti_f50（文件名 t1_val_selanti_f50.h5ad） | 42.66 | 40.6 | 48 | 37.2 | 46.8 | 166/232 | selanti 族；低于实测地板；mmd 37.2 偏弱 |
| 2026-09-17 06:23 | selday-f40 | selday_f40（文件名 t1_val_selday_f40.h5ad） | 45.46 | 42.1 | 56.1 | 42.3 | 41.2 | 166/232 | selday 族；仍低于实测地板；mmd 42.3/vario 41.2 |
| 2026-09-17 06:24 | selpc1-f50 | selpc1_f50（文件名 t1_val_selpc1_f50.h5ad） | 37.59 | 38.3 | 45.6 | 31.6 | 35.6 | 166/232 | selpc1 族；37.59 崩（mmd 31.6/vario 35.6） |
| 2026-09-17 06:24 | selday-f50 | selday_f50（文件名 t1_val_selday_f50.h5ad） | 47.02 | 42.2 | 56.3 | 45.6 | 43.5 | 166/232 | selday 族；唯一超实测地板 46.84，仍低于 48.85；mmd 45.6 全族最高 |

### Experiment family: dir24 / dirprop (direction class)

Method: resample by 24 direction classes (dir24) or direction proportions (dirprop B family), k∈{2000,3000}.

Tools: T1 generator script family, veckit.

Issues: dir24_k2000_s100 and dirprop_B_k2000 are identical metric-by-metric (47.19/44.2/53.1/49.2/40.4), likely the same file renamed and re-uploaded; the k3000 variant has weaker vario 37.8.

Conclusion: direction-class resampling gets the family-highest de 44.2 but vario 40.4 drags it down; family peak 47.19, does not break the floor; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18 04:32 | dir24-k2000-s100 | dir24_k2000_s100（dir24 族 k2000/s100；文件名 t1_val_dir24_k2000_s100.h5ad） | 47.19 | 44.2 | 53.1 | 49.2 | 40.4 | 171/238 | dir24 族 k2000/s100；47.19 超实测地板 46.84、未超当时峰值；de 44.2 全族最高但 vario 40.4 偏弱；rank 171/238；方法细节待补充 |
| 2026-09-18 04:32 | dir24-k3000-s100 | dir24_k3000_s100（dir24 族 k3000/s100；文件名 t1_val_dir24_k3000_s100.h5ad） | 46.71 | 44.1 | 53.5 | 49.1 | 37.8 | 171/238 | dir24 族 k3000/s100；46.71 低于 k2000 版 47.19；de 44.1 相近、vario 37.8 更弱；rank 171/238；方法细节待补充 |
| 2026-09-18 04:36 | dirprop-B-k2000 | dirprop_B_k2000（dirprop B 族 k2000；文件名 t1_val_dirprop_B_k2000.h5ad） | 47.19 | 44.2 | 53.1 | 49.2 | 40.4 | 171/238 | dirprop_B 族 k2000；47.19 与 dir24_k2000_s100（R39）逐项完全同分（47.19/44.2/53.1/49.2/40.4），疑似同名文件改名重传；如确认重传则烧 1 名额；方法细节待补充 |

### Experiment family: robust_consensus (robust consensus)

Method: multi-candidate robust consensus + damp 0.45 drift.

Tools: T1 generator script family, veckit.

Issues: 47.94 exceeds the measured floor 46.84 but not shift@2.5 (48.85); de 40.1 weak.

Conclusion: robust consensus only stabilizes the distribution metrics (mmd 49.8/vario 48.6) and cannot lift de; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18 04:11 | robust-consensus-d045 | robust_consensus_d045（robust_consensus 族 damp 0.45；文件名 t1_robust_consensus_d045.h5ad） | 47.94 | 40.1 | 53 | 49.8 | 48.6 | 171/238 | robust_consensus 族 d0.45；47.94 超实测地板 46.84、未超 48.85；mmd 49.8/vario 48.6 稳、de 40.1 仍弱；rank 171/238；方法细节待补充 |

### Experiment family: ancestor_donor_birth (ancestor–donor birth mixture)

Method: ancestor cells × donor birth mixture (10% mixing ratio).

Tools: T1 generator script family, veckit.

Issues: 46.74, marginally below the measured floor 46.84 (−0.10); re-uploading the same file burned one quota (04:35 and 04:46 identical metrics).

Conclusion: 10% birth mixture gives no gain; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18 04:35 | ancestor-donor-birth-mix10 | ancestor_donor_birth_mix10（祖先-供体出生混合 10%；文件名 t1_ancestor_donor_birth_mix10.h5ad） | 46.74 | 37.5 | 51.6 | 49.2 | 48.4 | 171/238 | ancestor_donor_birth 族 mix10；46.74 微低于实测地板 46.84（-0.10）；de 37.5 弱；mmd 49.2/vario 48.4 正常；rank 171/238；方法细节待补充；04:46 同文件重复重传（逐项同分 46.74），烧 1 名额 |

### Experiment family: mm (library-size normalization)

Method: the mm generator normalizes library size in log1p space so the median library size aligns to 10000 (matching the reference E9.5 base exact 10000); n=1249 sampling, b=0.70.

Tools: T1 generator script family, veckit.

Issues: mm_n1249_b070 49.93, only 0.07 from the official floor 50; mmd 52.2/vario 50.7 both pass, de 43.1 still weak.

Conclusion: library-size normalization is a necessary baseline fix (no effect on de ranking, but preserves the distribution); mm brings the distribution metrics to pass level — 50 is one step away.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-18 05:58 | mommask-0p01 | mommask0p01（momentum mask α=0.01；文件名 t1_val_mommask0p01.h5ad） | 49.49 | 43.8 | 53.6 | 50.8 | 49.5 | 159/238 | 49.49 超 S2.5 48.85（+0.64，T1 首破 49）；de 43.8/dir 53.6/mmd 50.8 略逊 S2.5，但 vario 49.5 暴涨（S2.5 仅 34.1）补回有余；rank 159/238；方法细节待补充 |
| 2026-09-19 18:40 | mm_n1249_b070 | mm_n1249_b070（新机制；文件名 t1_val_mm_n1249_b070.h5ad，155MB） | 49.93 | 43.1 | 53.4 | 52.2 | 50.7 | 154/242 | 距 floor 仅 0.07；mmd 52.2/vario 50.7 双过线；de 43.1 仍弱 |

### Experiment family: vs (variance amplification)

Method: variance amplification — multiply the deviation of the K most-variable genes in the E9.5 carrier by coefficient c and write back (vs200=K200, vs500=K500; c15/c135/c165 = coefficients 1.5/1.35/1.65), touching only covariance, not pseudobulk; vs_kp6_a030_n1249 is vs × knowledge-program kp6 (knowledge shift a=0.30, n=1249); direction check: 3 seeds × 25 groups = 75 points, all positive.

Tools: tools/_t1_vs_make.py, veckit.

Issues: vs200_c165 50.52 first breaks the official floor 50 (mmd 55.7, then a new high); vs500_c135 only 50.01 (de 40.9 weak); vs_kp6_a030_n1249 50.67 keeps refreshing.

Conclusion: the vs family is T1's turning point past 50 — variance amplification (moving covariance) is closer to the real developmental variance structure than pure global drift; family peak 50.67.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-21 19:05 | vs200_c15 | vs200_c15（文件名 t1_val_vs200_c15.h5ad，155MB） | 50.39 | 42.1 | 53.2 | 55.2 | 50 | 148/249 | vs200_c15 族；50.39 首破官方地板 50（+0.39），超 mm_n1249_b070 49.93；mmd 55.2/vario 50.0 双过线、de 42.1 仍弱；方法细节待补充 |
| 2026-09-21 19:06 | vs500_c135 | vs500_c135（文件名 t1_val_vs500_c135.h5ad，155MB） | 50.01 | 40.9 | 53.2 | 55.2 | 49.7 | 148/249 | vs500_c135 族；50.01 微过官方地板 50（+0.01）；de 40.9 弱；方法细节待补充 |
| 2026-09-21 19:09 | vs200_c165 | vs200_c165（文件名 t1_val_vs200_c165.h5ad，155MB） | 50.52 | 42.2 | 53.2 | 55.7 | 49.7 | 147/249 | vs200_c165 族；50.52 新 T1 最佳（超 mm_n1249_b070 49.93 与 vs200_c15 50.39）；mmd 55.7 新高；总览全绿达成；方法细节待补充 |
| 2026-09-23 00:54 | covsafe_mm_n1249_l25 | covsafe_mm_n1249_l25（文件名 t1_covsafe_mm_n1249_l25.h5ad，155MB） | 48.09 | 39.1 | 52.7 | 50.2 | 50.4 | 112/252 | covsafe_mm 族；48.09 低于官方地板 50；de 39.1 弱、mmd 50.2 未过线；mm 系协方差安全化（covsafe）变体，vario 50.4 过线但不足以破地板；方法细节待补充 |

### Experiment family: otf3 (otfix: OT direction + mask + tiny amplitude)

Method: otfix — OT-mixture direction + mask + tiny amplitude (n=2500, om2 masked variant; a local independent-truth subset once showed all four axes better).

Tools: tools/_t1_otf3_robust.py, veckit.

Issues: 47.09 below the official floor 50 and mm_n1249_b070 (49.93); all four axes worse than the mm family (weighted −2.87 vs actual −2.84) — direct evidence that the T1 local proxy is unusable (locally all four axes looked better).

Conclusion: the OT-flow variant does not beat the vs family; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-20 17:06 | otf3_n2500_om2 | otf3_n2500_om2（文件名 t1_val_otf3_n2500_om2.h5ad） | 47.09 | 38.8 | 51.5 | 49.4 | 48.4 | 156/244 | otf3_n2500_om2 族；47.09 低于官方地板 50 与 mm_n1249_b070 49.93；de 38.8 弱；方法细节待补充 |

### Experiment family: state_population_dynamics (state population dynamics)

Method: two-component dynamics (implementation in baselines/t1_state_population_dynamics.py module docstring): ① type-level birth/death momentum — estimate momentum from the E8.5→E9.5 composition change and conservatively extrapolate one step, sampling the carrier from the extrapolated population (not by natural E9.5 proportions); ② state dynamics — assign each gene to an expression program (cardiac/endodermal/neural_crest/mesodermal/vascular, five programs), modulate the type velocity by how far each carrier cell's state deviates from its type centroid, and give explicit birth-state velocities to new E9.5 types (E9.5 residuals kept in the carrier). Uses only published E8.5/E9.5 data; no hidden-stage input.

Tools: baselines/t1_state_population_dynamics.py, veckit.

Issues: 47.93 below the official floor 50; de 43.0 above otf3 but still weak, vario 41.6 weak.

Conclusion: the dynamics-modeling direction is right but the implementation does not pass the line; closed.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-21 10:13 | state_population_dynamics_v1 | state_population_dynamics_v1（文件名 t1_state_population_dynamics_v1.h5ad，155MB） | 47.93 | 43 | 53.7 | 51.4 | 41.6 | 157/247 | state_population_dynamics_v1 族；47.93 低于官方地板 50 与 mm_n1249_b070 49.93；de 43.0 高于 otf3 38.8 但仍弱、vario 41.6 偏弱；未超地板与当前最佳；方法细节待补充 |

### Experiment family: kp family (knowledge-program shift + variance amplification / maturity weighting)

Method: two mechanisms stacked: A = knowledge-program shift — textbook developmental programs enumerating 10 programs / 271 genes (imprinting/neural/ECM/pluripotency/ribosomal/glycolysis/stress/epithelial etc.; the program list is developmental-biology domain knowledge with no single URL), add a shift to pseudobulk (a∈{0.15,0.25,0.35}; u=uniform / w=weighted by program hits); B = variance amplification — multiply the deviation of the K=500 most-variable genes by c=1.5 (b500c15 means K=500, c=1.5; n=2000 sampling). Variants: kp2/3/4/5 are mechanism-combination indices and ablations (raw=raw input, wo=no weighting, aonly=A only); kp7_m is the maturity-weighting variant (m mechanism + maturity index b=0.50, b=0.00 as control). Key design decision: biological knowledge should be used to "select the program gene set" rather than shift genes one by one.

Tools: tools/_t1_kp_make.py, _t1_kp_make3.py, check_submission.py, veckit, real-board backfill.

Issues: ① kp probe kp_a015u only 48.88; ② all raw variants fail (kp5_kw/kp4_so/kp2_raw/kp3_w_raw all 47–48, vario 46.6 collapse); ③ aonly_raw without the b500c15 component drops all three lines (47.37); ④ wo variant 51.91 does not beat the w full pipeline; ⑤ kp7_m_b000 control 51.37, 2.3 below b050 (53.67) (de −4.1/dir −3.2/mmd −1.7) — b=0.50 is the key parameter; ⑥ kp3_w_a025_b500c15_n2000 52.18 once set the T1 best (dir/mmd/vario all pass).

Conclusion: kp7_m_b050_n2000 = **53.67** (rank 93/254, de 44.2 breaks the 42 bottleneck / dir 57.6 / mmd 57.6 / vario 54.7, four new highs), current T1 best. kp7 maturity weighting was once rejected by a 500-panel OOF, but the 32285-panel real board gives +2.30 — small-panel OOF conclusions do not generalize to the full panel.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-22 23:46 | kp_a015u_b500c115_n2000 | kp_a015u_b500c115_n2000（文件名 t1_val_kp_a015u_b500c115_n2000.h5ad，248MB） | 48.88 | 39.6 | 54.1 | 51.8 | 49.5 | 146/252 | kp 族探路；48.88 低于官方地板 50；de 39.6 弱、mmd 51.8/vario 49.5 未过线；方法细节待补充 |
| 2026-09-22 23:47 | vs_kp6_a030_n1249 | vs_kp6_a030_n1249（文件名 t1_val_vs_kp6_a030_n1249.h5ad，155MB） | 50.67 | 42.3 | 53.3 | 56.1 | 49.7 | 146/252 | vs_kp6_a030_n1249 族；50.67 新 T1 最佳（超 vs200_c165 50.52）；mmd 56.1 新高；de 42.3 仍弱；方法细节待补充 |
| 2026-09-22 23:49 | kp5_kw_a025_b500c15o_raw_n2000 | kp5_kw_a025_b500c15o_raw_n2000（文件名 t1_val_kp5_kw_a025_b500c15o_raw_n2000.h5ad，248MB） | 47.66 | 38 | 52.3 | 52.5 | 46.6 | 146/252 | kp5_kw 族；47.66 低于官方地板 50；de 38.0 弱、vario 46.6 崩；方法细节待补充 |
| 2026-09-22 23:49 | kp3_w_b500c15_n2000 | kp3_w_b500c15_n2000（文件名 t1_val_kp3_w_b500c15_n2000.h5ad，248MB） | 52.09 | 41.3 | 55.7 | 56.7 | 54.2 | 116/252 | kp3_w 族；52.09 新 T1 最佳（超 vs_kp6_a030_n1249 50.67）；de_direction 55.7/mmd 56.7/vario 54.2 均创新高、三线过线；de 41.3 仍弱；方法细节待补充 |
| 2026-09-22 23:49 | kp4_so_a025_b500c15o_raw_n2000 | kp4_so_a025_b500c15o_raw_n2000（文件名 t1_val_kp4_so_a025_b500c15o_raw_n2000.h5ad，248MB） | 47.68 | 38 | 52.3 | 52.6 | 46.6 | 116/252 | kp4_so 族；47.68 低于官方地板 50；de 38.0 弱、vario 46.6 崩（与 kp5_kw 同构，kw/so 变体均败）；方法细节待补充 |
| 2026-09-22 23:53 | kp2_raw_a015w_b500c15_n2000 | kp2_raw_a015w_b500c15_n2000（文件名 t1_val_kp2_raw_a015w_b500c15_n2000.h5ad，248MB） | 48.02 | 38.6 | 52.5 | 53.1 | 46.6 | 116/252 | kp2_raw 族；48.02 低于官方地板 50；de 38.6 弱、vario 46.6 崩（w 系 raw 变体，比 kp3_w 差）；方法细节待补充 |
| 2026-09-23 00:10 | kp3_w_a025_b500c15_n2000 | kp3_w_a025_b500c15_n2000（文件名 t1_val_kp3_w_a025_b500c15_n2000.h5ad，248MB） | 52.18 | 41.5 | 55.7 | 56.7 | 54.2 | 112/252 | kp3_w_a025 族；52.18 新 T1 最佳（超 kp3_w_b500c15_n2000 52.09）；dir 55.7/mmd 56.7/vario 54.2 持平新高、三线过线；de 41.5 仍弱；方法细节待补充 |
| 2026-09-23 00:10 | kp3_w_aonly_raw_n2000 | kp3_w_aonly_raw_n2000（文件名 t1_val_kp3_w_aonly_raw_n2000.h5ad，248MB） | 47.37 | 39.6 | 52.4 | 49.2 | 48 | 112/252 | kp3_w_aonly_raw 族；47.37 低于官方地板 50；de 39.6 弱、mmd 49.2 崩（aonly raw 变体，去 b500c15 组件后三线全掉）；方法细节待补充 |
| 2026-09-23 00:14 | kp3_w_raw_n2000 | kp3_w_raw_n2000（文件名 t1_val_kp3_w_raw_n2000.h5ad，248MB） | 47.62 | 37.7 | 52.3 | 52.7 | 46.6 | 112/252 | kp3_w_raw 族；47.62 低于官方地板 50；de 37.7 弱、vario 46.6 崩（raw 变体，b500c15 组件虽在但 raw 化后三线掉）；方法细节待补充 |
| 2026-09-23 12:22 | kp3_wo_a025_b500c15_n2000 | kp3_wo_a025_b500c15_n2000（文件名 t1_val_kp3_wo_a025_b500c15_n2000.h5ad，248MB） | 51.91 | 41.9 | 55.7 | 56.1 | 53.3 | 112/254 | kp3_wo 族；51.91 过官方地板 50（+1.91）但未超 kp3_w_a025 52.18；de 41.9（T1 最高档）/dir 55.7/mmd 56.1/vario 53.3；wo 变体略逊于 w 全管线；方法细节待补充 |
| 2026-09-23 12:23 | kp3_t00_a035_b500c15_n2000 | kp3_t00_a035_b500c15_n2000（文件名 t1_val_kp3_t00_a035_b500c15_n2000.h5ad，248MB） | 52.21 | 41.6 | 55.7 | 56.7 | 54.3 | 112/254 | kp3_t00 族；52.21 新 T1 最佳（超 kp3_w_a025 52.18）；vario 54.3 新高；dir 55.7/mmd 56.7 持平新高、三线过线；de 41.6 仍弱；方法细节待补充 |
| 2026-09-23 13:20 | kp7_m_b050_n2000 | kp7_m_b050_n2000（文件名 t1_val_kp7_m_b050_n2000.h5ad，248MB） | 53.67 | 44.2 | 57.6 | 57.6 | 54.7 | 93/254 | kp7_m 族；53.67 新 T1 最佳（超 kp3_t00 52.21，+1.46）；四项全新高：de 44.2（破 42 瓶颈、T1 最高）/dir 57.6/mmd 57.6/vario 54.7；rank 93/254；kp7 新家族，b=0.50；方法细节待补充 |
| 2026-09-23 13:21 | kp7_m_b000_n2000 | kp7_m_b000_n2000（文件名 t1_val_kp7_m_b000_n2000.h5ad，248MB） | 51.37 | 40.1 | 54.4 | 55.9 | 54.7 | 93/254 | kp7_m 族 b=0.00 变体；51.37 过官方地板 50（+1.37）但远低于 kp7_m_b050 53.67；对比 b050：de -4.1/dir -3.2/mmd -1.7（vario 持平）——b 参数对 kp7_m 是关键，b000 明显弱；方法细节待补充 |

### Experiment family: E4c pending candidates (lineage Δ / momentum)

Method: E4c-lineage Δ (masked-A ancestor mixture, no resampling); E4c-mom type-specific rate r∝(s/ś)^+0.5 (momentum).

Tools: t1_rewrite script family.

Issues: not yet regenerated under the label-free format gate; the local profile looks like a copy_last artifact.

Conclusion: pending state — not uploaded, not scored.

**Submission log (all results, UTC)**

| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 待传 | E4c-lin | lineage Δ（掩膜A 祖先混合，无重采样） | — | — | — | — | — | — | E4c 候选；需按新 label-free 格式门重生成 |
| 待传 | E4c-mom | 型特异速率 r∝(s/ś)^+0.5（动量） | — | — | — | — | — | — | E4c 候选；同上 |
| 待传 |  |  | — | — | — | — | — | — | E4c 候选；本地≈copy_last 剖面（伪影） |

## Summary rows

- **Current best**: 53.67
- **Official floor (copy_last / wt_identity)**: 50
- **Measured floor (our upload)**: 46.84
- **Board top (leader)**: 68.7
