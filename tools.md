# 自建工具清单（Local Tools）

> **外部参考、使用过的第三方工具、预训练模型、算法、外部数据集与平台的完整链接总账见 [`reference-links.md`](reference-links.md)**（含官方资源、社区工具、合规审计结论与方法论）。
> 本文件只列**自建管线**（本地工作区长期维护、可复用框架），目的是给"重新建造前先看已存在设施"提供索引，避免重复造轮子。

<p align="center"><sub>中文 · <a href="tools.en.md">English</a></sub></p>

---

## 一、提交卫生与门禁

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

## 二、评分与校准

| 工具 | 职责 |
|---|---|
| `veckit/` | 官方本地计分器（见 reference-links.md 第一节官方链接） |
| `noise_calibrate.py` | 多 seed 噪声校准：scorer 种子 × builder 种子 → 均值±sd 原始带 + skill 带；真榜差异 <2×band 视为平局 |
| `refit_headline.py` + `HEADLINE_FORMULA.md` | 总分公式锁定（T1 / T3 加权口径） |
| `thread_start_gate.py` | **每会话开工仪式**：从盘上重载复盘教训、真榜校准锚点、名额台账、待传批次（"相信盘，别信记忆"） |

## 三、方法生成器（baselines 族）

| 工具 | 职责 |
|---|---|
| `baselines/t1_shift.py` | T1 pseudobulk shift 基线（damp 网格；配方见官方 baselines 页） |
| `baselines/t1_otmix.py` | OT 混合基线（WOT 耦合 + 类型转移重采样 + growth/掩膜变体；WOT 见 reference-links.md） |
| `baselines/t3_wt_identity.py` / `t3_shift_transfer.py` / `t3_prior_shift.py` | T3 地板 / 全局 Δ transfer / 文献先验（GATA4 靶基因定向响应） |
| `wot_analysis/` | WOT 耦合矩阵、marker 审计（378→61 边掩膜）、边掩膜生成器 |
| `category_generation.py` | 跨任务"新类别生成"研究生成器（软父类别+程序偏移+父细胞残差；proxy only，不写上传队列） |
| `deepgen_t1/` | 深度生成模型族：VGFM（flow matching）/ CVAE / diffusion + 残差修正、carrier bypass、FiLM gate、structure-axis、composition-support、multi-KO response adapter（全部研究接口，非候选生成器） |
| 台账插行脚本族 | backup-fill 法（拆合并区→快照平移→re-merge→clone 样式→独立回读），含 verify_*.py 对照脚本 |

## 四、申报候选（社区贡献奖方向，均本地实现）

| 工具 | 说明 |
|---|---|
| `vec_scalecheck` | 本地格式检查器（自建仓库 https://github.com/wqty123/vec-scalecheck；README 三处宣传过度已指出待改：伤害范围夸大 /"零机制风险"错误 / PASS 混淆一致与合格） |
| `t1_pre_upload_gate` | 防重锁 + 五闸合一（可作为独立申报） |
| `t2_data_contract` | T2 数据契约（48KB 工具包） |
| `slot_ledger` | 提交名额台账 |

---

## 五、工具覆盖结论（重新建造前必读）

1. **格式/结构检查**（data_inspector ≈ vec-submit-check ≈ vec_submit_check ≈ check_submission + vec_scalecheck，链接见 reference-links.md 第二节）——已严重拥挤，**勿重造**。
2. **教学类**（task1_walkthrough ≈ scigantic ≈ xxx12e tutorial_zh）——已饱和，**勿重造**。
3. **agent 轨道证据**（vec-evidence-check ≈ vec_agent_evidence）——Human Team 用不上，**勿重造**。
4. **真正有增量价值**：vecbench 的噪声底标定（已集成）、intuition-lab 的指标敏感度结论（知识库）、external-data-catalog 的 GSE282547（T2 heart 数据素材，待规则确认）、EmbryoMatch 的 E-MTAB-11763（T1 数据素材，待合规审计）。
5. **我方申报仍差异化**：t1_pre_upload_gate（防重锁+五闸）、t2_data_contract、vec_scalecheck——与社区现有设施均不冲突。
