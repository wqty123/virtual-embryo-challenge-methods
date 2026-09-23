# Virtual Embryo Challenge · 方法旅程记录

> Virtual Embryo Challenge 2026（NeurIPS 2026 竞赛，主办：Stanford Qiu Lab）
> 本仓库记录我们从第一天开始尝试过的**所有方法及其效果**、踩过的**所有坑**、以及用过的**所有工具**。
> 定位：方法学分享 + 经验记录（符合官方规则 §15：参赛者保留方法所有权，公开方法受鼓励；社区贡献奖欢迎教导类提交）。
> 所有分数均来自官方评分返回（虚拟胚胎挑战赛公开 leaderboard），不包含任何 held-out 阶段数据。

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
| T1:val | kp7_m_b050_n2000（成熟度加权抽样 kp7 族） | **53.67** | 93/254 |
| T2:embryo:val_interp | cpf015r5k（cpf 族） | **65.31** | 65/200 |
| T2:heart:val_interp | mix_brkts（混合+bracket + scale 满档） | **65.01** | 54/191 |
| T2:heart:val_extrap | scale_only（仅 scale 调整） | **54.51** | 68/185 |
| T3:gata4 | kbb_n6000_b055_k65（kb6000×b055 组合） | **66.61** | 48/187 |

三任务合计 ≈ **181.89**（超过 150 地板门槛；排名按官方 leaderboard）。

## 仓库结构

| 文件 | 内容 |
|---|---|
| `README.md` | 本文件：总览、成绩快照、索引 |
| `methods_t1.md` | T1 全部方法 × 效果（71 条提交记录） |
| `methods_t2_embryo_interp.md` | T2 胚胎插值全部方法 × 效果 |
| `methods_t2_heart_interp.md` | T2 心脏插值全部方法 × 效果 |
| `methods_t2_heart_extrap.md` | T2 心脏外推全部方法 × 效果 |
| `methods_t3.md` | T3 全部方法 × 效果（48 条提交记录） |
| `pitfalls.md` | 所有踩过的坑：方法学/生物学类 + 工程/流程类 |
| `tools.md` | 用过的全部工具：自建管线 + 社区工具 |

## 方法演化主线（一句话版）

1. **T1**：`shift（伪bulk漂移）` → damp 网格 → `OT混合（掩膜+生长）` → `Markov通量`（证伪）→ `程序混合`（vario 崩）→ `mom-mask`（破 49）→ `mm 库大小归一化`（49.93）→ `vs 虚拟状态`（破 50）→ **`kp3_w 混合管线`（52.18）→ `kp7_m 成熟度加权`（53.67，当前最佳）**
2. **T2 embryo**：`kNN配对+log线性插值 v1`（59.0）→ `mix_brkt`（59.1）→ `bgm`（62.9）→ `gps33 高斯过程`（63.2）→ **`cpf015r5k`（65.31，当前最佳）**
3. **T2 heart interp**：`类型分层+全局配对 v1`（61.9）→ `mix_brkt`（62.6）→ **`mix_brkts（scale 满档）`（65.01）**
4. **T2 heart extrap**：形态/几何路线全灭（v3/v4/r6b70a20/comp_c100/vmorph_s120/cpfx 全部证伪）→ **`scale_only`（54.51，当前最佳）**——"只动 scale/构成、不动形态"是唯一正确路线
5. **T3**：`transfer 全局Δ`（证伪）→ `cardiac 限制`（证伪）→ `文献先验` → `mix 混合KO`（64.6）→ **`cmp`（64.93）→ `kb6000 成熟度`（66.36）→ `kbb 组合`（66.61，当前最佳）**

## 合规声明

- 本仓库只含方法描述、官方公开分数、公开规则引用；**不含**任何 held-out 阶段（T1 E10.5/E12.5；T2 embryo E7.5/E7.75、heart E8.5/E10.5/E12.5；T3 Gata4/β-catenin KO E8.75）的测量数据。
- 不含通过 score 反推 held-out 属性的内容；分数仅用于选择预测、不用于计算预测（官方规则 §10）。
- 官方规则全文：https://virtualembryo.ai/challenge/rules
