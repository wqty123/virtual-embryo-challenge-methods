# Virtual Embryo Challenge · 方法旅程实验记录

> Virtual Embryo Challenge 2026（NeurIPS 2026 竞赛，主办：Stanford Qiu Lab）
> 本仓库记录我们从第一天开始尝试过的**全部方法（每个方法一个实验条目：技术 / 工具 / 遇到的问题 / 效果）**、
> 踩过的**所有坑**、以及用过的**所有工具**。
> 定位：方法学分享 + 实验记录（符合官方规则 §15：参赛者保留方法所有权，公开方法受鼓励；社区贡献奖欢迎教导类提交）。
> 所有分数均来自官方评分返回（虚拟胚胎挑战赛公开 leaderboard），不含任何 held-out 阶段数据。

## 任务与板块

| 任务 | 板块 | 目标 | 评分指标 |
|---|---|---|---|
| T1 | `T1:val` | 单细胞时间外推：E8.5→E9.5 预测 E10.5 | de_score / de_direction / mmd_u / variogram |
| T2 | `T2:embryo:val_interp` | 胚胎插值：E6.75/E7.25/E8.0 预测中间阶段 | 8 项：de/dir/mmd/vario + d2_shape/occupancy_dice/scale_log_ratio/neighborhood_mmd |
| T2 | `T2:heart:val_interp` | 心脏插值：E8.25/E8.75 预测中间阶段 | 同上 8 项 |
| T2 | `T2:heart:val_extrap` | 心脏外推：预测 E9.5 之后 | 同上 8 项 |
| T3 | `T3:gata4` | Gata4 KO 扰动响应预测（E8.75） | de_score / de_direction / severity_slope / mmd_u / variogram |

**评分口径**：地板（copy_last / wt_identity）固定在 50，天花板（自半对半估计）为 100；每队每板取历史最佳。T1 总分 ≈ `0.25·de + 0.25·dir + 0.30·mmd + 0.20·vario`；T3 ≈ `0.298·de + 0.250·dir + 0.251·sev + 0.120·mmd + 0.080·vario`。

## 当前成绩快照（截至 2026-09-23，均为本队最佳）

| 板块 | 最佳方法 | 分数 | rank |
|---|---|---|---|
| T1:val | kp7_m_b050_n2000（成熟度加权抽样） | **53.67** | 93/254 |
| T2:embryo:val_interp | cpf015r5k（同源配对） | **65.31** | 65/200 |
| T2:heart:val_interp | mix_brkts（混合+bracket+scale 满档） | **65.01** | 54/191 |
| T2:heart:val_extrap | scale_only（仅 scale 调整） | **54.51** | 68/185 |
| T3:gata4 | kbb_n6000_b055_k65（真实 WT 稀释 KO 组合） | **66.61** | 48/187 |

三任务合计 ≈ **181.89**（超过 150 地板门槛；排名按官方 leaderboard）。

## 仓库结构

| 文件 | 内容 |
|---|---|
| `README.md` | 本文件：总览、成绩快照、索引 |
| `experiments_t1.md` | T1 实验报告（19 个方法族，65 条提交明细） |
| `experiments_t2_embryo_interp.md` | T2 胚胎插值实验报告（10 个方法族） |
| `experiments_t2_heart_interp.md` | T2 心脏插值实验报告（6 个方法族） |
| `experiments_t2_heart_extrap.md` | T2 心脏外推实验报告（14 个方法族） |
| `experiments_t3.md` | T3 实验报告（15 个方法族，42 条提交明细） |
| `pitfalls.md` | 所有踩过的坑：方法学/生物学类 + 工程/流程类 |
| `tools.md` | 工具与参考索引：全部第三方工具链接、参考过的思路与数据源（WOT/官方基线/GSE/社区工具）、自建管线 |
| `gen_experiments.py` | 实验报告生成器（输入：台账 JSON，按方法族分组渲染） |

**每个实验族都按统一结构记录**：技术（具体算法、参数、数据、实现文件）→ 工具（具体脚本/评分器）→ 遇到的问题（具体分数与现象）→ 结论（具体判断）→ 提交明细（全部效果数据）。

## 方法主线（按时间线的具体技术序列）

1. **T1**：`pseudobulk shift（全局漂移）` 48.13 → damp 网格 48.85 → `OT 混合（WOT 耦合+类型转移重采样）` 47.52 → `Markov 通量`（证伪 44.19）→ `程序混合`（vario 崩 47.34）→ `momentum mask` 49.49 → `mm 库大小归一化` 49.93 → `vs 方差放大` 50.67 → **`kp 知识程序位移+方差放大/成熟度加权`（kp3_w 52.18 → kp7_m_b050 53.67，当前最佳）**
2. **T2 embryo**：`v1（kNN 配对 log-linear 插值）` 59.0 → `mix_brkt` 59.07 → `bgm` 62.94 → `gps33s 高斯过程（scale 校准）` 63.19 → **`cpf015r5k 同源配对` 65.31（当前最佳）**
3. **T2 heart interp**：`v1（类型分层+全局配对）` 61.9 → `mix_brkt` 62.6 → **`mix_brkts（scale 满档）` 65.01（当前最佳）**
4. **T2 heart extrap**：`v3/v4`（≈50 平台）→ 形态线四次证伪（`r6b70a20` 38.97 / `comp_c100` 32.8 / `vmorph_s120` 46.8 / `cpfx` d2_shape 5.7）→ **`scale_only` 54.51（当前最佳）**——只动 scale/构成、不动形态是唯一有效路线
5. **T3**：`transfer 全局Δ`（证伪 40.98）→ `cardiac 限制`（证伪 44.85）→ `文献先验`（平地板 45.80）→ `mix 混合 KO` 64.60 → `cmp celltype^β 重采样` 64.93 → `cmpw 载体稀释` 65.49 → `kb 真实 WT 稀释 KO` 66.36 → **`kbb 组合` 66.61（当前最佳）**

## 合规声明

- 本仓库只含方法描述、官方公开分数、公开规则引用；**不含**任何 held-out 阶段（T1 E10.5/E12.5；T2 embryo E7.5/E7.75、heart E8.5/E10.5/E12.5；T3 Gata4/β-catenin KO E8.75）的测量数据。
- 不含通过 score 反推 held-out 属性的内容；分数仅用于选择预测、不用于计算预测（官方规则 §10）。
- 官方规则全文：https://virtualembryo.ai/challenge/rules

## 参考与致谢

所有参考过的思路、使用过的第三方工具与外部数据源均在 `tools.md` 集中标注链接；实验族内"工具"字段同步内联来源（如 WOT、官方基线配方、GSE208162 数据）。无确切 URL 的来源（如教科书发育程序清单）只标名称与出处，不编造链接。
