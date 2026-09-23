# 工具与参考清单（Tools & References）

> 两个来源：**自建管线**（工作区长期维护、可复用框架）与**社区/外部工具**（官方社区贡献名单，调研/集成结论）。
> 本文件同时是**参考索引**：凡参考过的思路、使用过的外部工具与数据源，均带链接或来源标注；无确切 URL 的只标名称与出处，不编造链接。
> 目的：给"重新建造前先看已存在设施"提供索引，避免重复造轮子。

---

## 一、官方工具与页面（使用/参考基础）

| 工具 / 页面 | 类型 | 用途 | 链接 |
|---|---|---|---|
| `veckit` | 官方本地计分器 | T1/T2/T3 全部指标离线可跑；所有实验的评分基础 | 官方评估页 https://virtualembryo.ai/challenge/evaluation（veckit 随官方入门套件发布） |
| 官方基线定义（copy_last / wt_identity / pseudobulk shift） | 官方基线 | T1 `baselines/t1_shift.py`、T3 `t3_wt_identity.py` 等按官方配方重建 | https://virtualembryo.ai/challenge/baselines |
| 官方评估指标说明 | 官方文档 | 8+5 项指标口径、地板/天花板刻度 | https://virtualembryo.ai/challenge/evaluation |
| 官方面板文件（genes / index.json） | 官方数据 | 各板基因面板（T1 32285 / T2E 498 / T2H 500）与细胞数上限 | https://virtualembryo.ai/challenge/panels/index.json |
| 官方规则 | 官方文档 | 合规声明依据（§10 分数用途 / §15 方法所有权） | https://virtualembryo.ai/challenge/rules |

## 二、参考过的思路 / 外部数据源（在实验族内也已标注）

| 思路 / 数据 | 用在哪（族） | 来源说明 |
|---|---|---|
| WOT（Waddington-OT，最优传输耦合） | T1 OT 混合族（`baselines/t1_otmix.py`、`wot_analysis/`） | https://github.com/broadinstitute/wot |
| 教科书发育程序（10 程序 271 基因：印记/神经/ECM/多能/核糖体/糖酵解/应激/上皮等） | T1 kp 族（知识程序位移） | 发育生物学领域知识清单，无单一 URL；以"筛选程序基因集"方式使用 |
| GSE208162（T3 GSE 先验数据） | T3 prw 族（GSE 外部先验 s=0.10） | GEO：https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208162 |
| GSE282547（发育心脏 Visium，500/500 面板全覆盖） | T2 heart 潜在素材（观察中，未用） | 来自 `i-habib/external-data-catalog`；GEO：https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE282547 |
| GSE247450（MERFISH，68/500） | T2 heart 潜在素材（观察中，未用） | GEO：https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247450 |
| E-MTAB-11763 / E-MTAB-13645（Extended Mouse Atlas） | T1 backbone 候选（观察中，需合规审计） | 来自 `ShaoliZhao/virtual-embryo-EmbryoMatch`；EMBL-EBI：https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-11763 |

---

## 三、自建管线（本地工作区，全部为可复用框架/模板）

### 提交卫生与门禁
| 工具 | 职责 |
|---|---|
| `check_submission.py` | 提交格式校验：基因面板顺序、非负有限 X、T2/T3 spatial_3D、细胞数范围 |
| `submission_gate.py` | 生成后自动 `strip_training_annotations` + `check_submission`，FAIL 即终止主流程 |
| `t1_pre_upload_gate.py` / `t3_pre_upload_gate.py` | 上传门禁：**hash 防重锁** + 五闸（格式/标签/哈希/名额/授权） |
| `t1_slot_ledger.json` / `t3_slot_ledger.json` | 名额台账（每日 8/3/6 上限，防重复提交） |
| `validate_t2_submission.py` | T2 严格输出检查：面板/坐标/无标签列/无多余容器 |
| `audit_t2.py` + `t2_data_contract.py` | T2 数据契约 + 递归只读审计（102/102 文件面板核对） |
| `t2_experiment_gate.py` | T2 实验门禁：manifest 校验、来源隔离、DE reference、哈希与输出路径 |
| `audit_t3_external_gse208162.py` | T3 外部数据只读合规门（未下载/样本清单/队列隔离） |

### 评分与校准
| 工具 | 职责 |
|---|---|
| `veckit/` | 官方本地计分器（见第一节官方链接） |
| `noise_calibrate.py` | 多 seed 噪声校准：scorer 种子 × builder 种子 → 均值±sd 原始带 + skill 带；真榜差异 <2×band 视为平局 |
| `refit_headline.py` + `HEADLINE_FORMULA.md` | 总分公式锁定（T1 / T3 加权口径） |
| `thread_start_gate.py` | **每会话开工仪式**：从盘上重载复盘教训、真榜校准锚点、名额台账、待传批次（"相信盘，别信记忆"） |

### 方法生成器（baselines 族）
| 工具 | 职责 |
|---|---|
| `baselines/t1_shift.py` | T1 pseudobulk shift 基线（damp 网格；配方见官方 baselines 页） |
| `baselines/t1_otmix.py` | OT 混合基线（WOT 耦合 + 类型转移重采样 + growth/掩膜变体；WOT 见第二节） |
| `baselines/t3_wt_identity.py` / `t3_shift_transfer.py` / `t3_prior_shift.py` | T3 地板 / 全局 Δ transfer / 文献先验（GATA4 靶基因定向响应） |
| `wot_analysis/` | WOT 耦合矩阵、marker 审计（378→61 边掩膜）、边掩膜生成器 |
| `category_generation.py` | 跨任务"新类别生成"研究生成器（软父类别+程序偏移+父细胞残差；proxy only，不写上传队列） |
| `deepgen_t1/` | 深度生成模型族：VGFM（flow matching）/ CVAE / diffusion + 残差修正、carrier bypass、FiLM gate、structure-axis、composition-support、multi-KO response adapter（全部研究接口，非候选生成器） |
| 台账插行脚本族 | backup-fill 法（拆合并区→快照平移→re-merge→clone 样式→独立回读），含 verify_*.py 对照脚本 |

### 申报候选（社区贡献奖方向，均本地实现）
| 工具 | 说明 |
|---|---|
| `vec_scalecheck` | 本地格式检查器（自有；README 三处宣传过度已指出待改：伤害范围夸大 /"零机制风险"错误 / PASS 混淆一致与合格） |
| `t1_pre_upload_gate` | 防重锁 + 五闸合一（可作为独立申报） |
| `t2_data_contract` | T2 数据契约（48KB 工具包） |
| `slot_ledger` | 提交名额台账 |

---

## 四、使用过的社区工具（官方社区贡献名单，全部带链接）

### 已接受贡献（官方名单，归功于制作者）
| 仓库（链接） | 内容 | 我们的使用结论 |
|---|---|---|
| [AJK0921/vecbench](https://github.com/AJK0921/vecbench) | 本地计分背带（包装官方 veckit）：官方锚点换算、scorer 噪声底、稳定性 6/6 | **已集成，最高价值**：标定 de/dir/sev 零噪声轴、mmd ±5.75/vario ±2.20 skill 分；发现上游 stability() bug 已规避 |
| [scigantic 教程（virtual-embryo-challenge-t1）](https://scigantic.com/sample/virtual-embryo-challenge-t1) | T1 教程笔记本 | 教学类，我方已远超，无增量 |
| [xxx12e/vec-community-kit](https://github.com/xxx12e/vec-community-kit) | 五件套：[tutorial_zh](https://github.com/xxx12e/vec-community-kit/blob/main/docs/tutorial_zh.md) / [vec_agent_evidence](https://github.com/xxx12e/vec-community-kit/tree/main/vec_agent_evidence) / [vec_local_score](https://github.com/xxx12e/vec-community-kit/tree/main/vec_local_score) / [vec_baselines](https://github.com/xxx12e/vec-community-kit/tree/main/vec_baselines) / [vec_submit_check](https://github.com/xxx12e/vec-community-kit/tree/main/vec_submit_check) | 格式/教学类，与自建 check_submission 等价；agent 证据仅 agent 轨道相关 |
| [gh-dv-openclaw/vec-submit-check](https://github.com/gh-dv-openclaw/vec-submit-check) | 轻量格式检查器 + 中文合同解读 | 与 check_submission 等价，边际价值为中文文档 |
| [ShaoliZhao/virtual-embryo-EmbryoMatch](https://github.com/ShaoliZhao/virtual-embryo-EmbryoMatch) | 外部数据注册库（文献证据 + 任务画像） | **已集成**：发现 E-MTAB-11763/13645（Extended Mouse Atlas，T1 backbone 候选，需 accession 合规审计） |

### 已提交待审核（被列入名单 ≠ 背书）
| 仓库（链接） | 内容 | 我们的判断 |
|---|---|---|
| [bestdeeplearning-star/vec-evidence-check](https://github.com/bestdeeplearning-star/vec-evidence-check) | agent 轨道证据完整性审计（SHA-256 + seal/audit + 200/600/1200MB 上限） | 与 vec_agent_evidence 重叠；我方走 Human Team 用不上 |
| [Shashwat-srivastav/VirtualEmbryo-basline](https://github.com/Shashwat-srivastav/VirtualEmbryo-basline) | T2 插值 baseline：copy_nearest/linear/celltype_interpolate | 新手向；我方 T2 embryo 65.31 远超 |
| [i-habib/virtual-embryo-community（intuition-lab）](https://github.com/i-habib/virtual-embryo-community/tree/main/intuition-lab) | 评分器受控实验（打乱单因素看指标）；发现**刚体旋转改变 sliced_wasserstein/occupancy_dice（veckit#7）** | 知识库参考：解释我方 extrap 形态线 d2_shape 崩的机制面 |
| [i-habib/external-data-catalog](https://github.com/i-habib/external-data-catalog) | 外部数据集目录：**GSE282547 发育心脏 Visium（500/500 面板全覆盖）**、GSE247450 MERFISH（68/500）、Mouse GO（1111 边） | T2 heart 潜在素材（需先查规则 E13.5 之后可用）；已列入观察 |
| [cadentann/virtual-embryo-community-kit（task1_walkthrough）](https://github.com/cadentann/virtual-embryo-community-kit/tree/main/modules/task1_walkthrough) | T1 首次提交演练 + fetch-contract 拉面板缓存 | 教学类，已饱和 |
| [cadentann/virtual-embryo-community-kit（data_inspector）](https://github.com/cadentann/virtual-embryo-community-kit/tree/main/modules/data_inspector) | .h5ad 只读体检：流式 SHA-256 指纹、X 有限/负值/稀疏、面板比对+reorder 计划 | 与 vec-submit-check / check_submission 拥挤，勿重造 |

---

## 五、工具覆盖结论（重新建造前必读）

1. **格式/结构检查**（data_inspector ≈ vec-submit-check ≈ vec_submit_check ≈ check_submission + vec_scalecheck）——已严重拥挤，**勿重造**。
2. **教学类**（task1_walkthrough ≈ scigantic ≈ xxx12e tutorial_zh）——已饱和，**勿重造**。
3. **agent 轨道证据**（vec-evidence-check ≈ vec_agent_evidence）——Human Team 用不上，**勿重造**。
4. **真正有增量价值**：vecbench 的噪声底标定（已集成）、intuition-lab 的指标敏感度结论（知识库）、external-data-catalog 的 GSE282547（T2 heart 数据素材，待规则确认）、EmbryoMatch 的 E-MTAB-11763（T1 数据素材，待合规审计）。
5. **我方申报仍差异化**：t1_pre_upload_gate（防重锁+五闸）、t2_data_contract、vec_scalecheck——与社区现有设施均不冲突。
