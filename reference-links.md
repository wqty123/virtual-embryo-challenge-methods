# 参考思路与外部工具链接总账（References & External Links）

创建：2026-09-23。登记本仓库在 virtualembryo 挑战中**参考过的思路**和**使用/评估过的外部工具、数据、模型**，每条给出链接、用途、合规结论与最终去向。所有链接可点击、可溯源；无确切 URL 的只标名称与出处，不编造链接。

---

## 一、官方资源（比赛本身）

| 资源 | 链接 | 用途 |
|---|---|---|
| 比赛主页 | https://virtualembryo.ai/challenge | 规则、数据、提交、榜 |
| 规则 | https://virtualembryo.ai/challenge/rules | 合规硬线（held-out 禁止，§10） |
| 数据说明/下载 | https://virtualembryo.ai/challenge/data | 各板 h5ad 下载与格式契约 |
| 评分说明 | https://virtualembryo.ai/challenge/evaluation | 各板指标定义（de/dir/mmd/vario…） |
| 排行榜 | https://virtualembryo.ai/challenge/leaderboard | 五个板真榜读数 |
| 提交 | https://virtualembryo.ai/challenge/submit | 上传 h5ad、消耗配额 |
| 数据 manifest | https://kg.virtualembryo.ai/challenge/data/manifest | 官方文件清单 |
| 数据直链 | https://kg.virtualembryo.ai/challenge/data/link?key=<KEY> | 单文件下载 |
| 知识图谱（KG） | https://kg.virtualembryo.ai/kg | 平台自带 KG（KEGG 等）——**已证伪**：与真值 DE 交集为空 |
| 官方打分器 | https://github.com/aristoteleo/veckit | **本地计分器**（`pip install git+https://github.com/aristoteleo/veckit.git@46d41e63`），进程内跑官方分；**连未出现的类型也能算**（mmd/vario 与标签无关，de/dir 走 pseudobulk 也不依赖标签） |
| 官方 baseline | https://github.com/aristoteleo/vec_baselines | 官方示例 baseline |

## 二、社区工具（clone / 参考过，全部带链接）

| 工具 | 链接 | 用途与去向 |
|---|---|---|
| **vecbench** | https://github.com/AJK0921/vecbench | 本地评分/噪声底/holdout 排序工具。**已深入使用**：`vec_noisefloor.py --calibrate` 校准出 T3 阈值 1.48（非 0.64）；实测复合噪声比独立假设高 1.4–1.6 倍；TF 判据"反相关仪器"警告来源 |
| **vec-scalecheck** | https://github.com/wqty123/vec-scalecheck | 提交文件格式/规模检查器，**自建仓库**（clone 到本地工作区改造），README 自带徽章与说明；已申报社区贡献奖 |
| **vec-submit-check** | https://github.com/gh-dv-openclaw/vec-submit-check | 内容层面提交检查，clone 到本地工作区 |
| **vec-community-kit** | https://github.com/xxx12e/vec-community-kit | 五合一社区工具包（榜契约校验器/本地打分/格式检查/清单），clone 到本地工作区；含 `vec_local_score` 在伪切分上跑 veckit |
| **vec-evidence-check** | https://github.com/bestdeeplearning-star/vec-evidence-check | 证据文件组装检查器（参照官方规则 §9 与 veckit PR 记录实现）；社区贡献（待审核） |
| **EmbryoMatch** | https://github.com/ShaoliZhao/virtual-embryo-EmbryoMatch | 阶段感知外部数据推荐器：按细胞状态与器官成熟度匹配，而非固定胚胎日换算。含 10 条文献证据、11 条推荐、可运行的阶段对齐基线（`scripts/recommend.py`、`align_states.py`）。我们参考其阶段对齐思想 |
| **Intuition Lab** | https://github.com/i-habib/virtual-embryo-community/tree/main/intuition-lab | 评分器诊断实验集：固定预测、只破坏一个变量，看哪个计分项动——我们 T1/T2/T3 的结构定理（de/dir/sev 只依赖 pseudobulk、vario 依赖细胞内基因对差异）与其同一思想 |
| **VEC First-Submission Kit** | https://github.com/cadentann/virtual-embryo-community-kit | 首次提交走通教程 + 只读 h5ad 预检（pseudobulk_shift 教学法 + 结构 QC）；模块：task1_walkthrough / data_inspector |
| **VirtualEmbryo-basline** | https://github.com/Shashwat-srivastav/VirtualEmbryo-basline | 类型条件插值 baseline（T2 风格：预测两个观测阶段之间的未见阶段），比 copy_nearest 强 |

## 三、预训练模型（合规审计过，逐条给出结论）

| 模型 | 出处 | 训练语料 | 合规结论 | 去向 |
|---|---|---|---|---|
| **TF-Sapiens** | https://github.com/czi-ai/transcriptformer 权重 https://czi-transcriptformer.s3.amazonaws.com/weights/{model}.tar.gz | 57M 细胞**纯人类**（mouse 标 −） | **✅ 可用** | 本地+云端跑通端到端；作判据在 T1 上**反相关 −0.69，判据线关闭**；改作 T3 载体稀释的 embedding 推演；生成侧 decoder 框架搭好等 T1 embedding |
| **TranscriptFormer**（非 Sapiens 版） | https://github.com/czi-ai/transcriptformer | CZI CellxGene Census，跨物种跨阶段，**含小鼠胚胎时程** | **⛔ 高风险**（默认禁用） | 未用 |
| **UCE**（Universal Cell Embedding） | 内部审计记录（见附文档索引） | 3390 万细胞人+小鼠，285 数据集 | **⛔ 实证禁用** | 未用 |
| **scGPT whole-human** | 内部审计记录（见附文档索引） | 33M 纯人类 CellxGene | **✅ 可用** | 未落地（纯人迁移价值有限） |
| **Geneformer** | 内部审计记录（见附文档索引） | Genecorpus-30M 人类为主 | **✅ 可用** | 未落地 |
| **GeneCompass** | Cell Research 2024（跨物种基础模型） | 跨物种 | 仅评估 | 未用（调研记录） |
| **Gene-Chronos** | 预训练单细胞基础模型发育时间推断 | — | 仅评估 | 未用 |
| **CAMEX** | https://www.nature.com/articles/s41467-026-69696-3 | 器官发育对齐方法 | 仅参考 | 阶段对齐思路参考（EmbryoMatch 引用） |

## 四、算法/方法类（参考思路，参数在我们自己的数据上拟合，无条件可用）

| 方法 | 参考出处 | 用途/结论 |
|---|---|---|
| **WOT（Waddington-OT）** | https://github.com/broadinstitute/wot（官方运输矩阵与生长率） | 成分外推**已闭环**：growth_by_type/descendant_fraction/transport 已算；单靠生长率无法预测新类型出现（46% 新类型在早期阶段不存在）；谱系速度与全局方向 corr +0.954 无独立信息 |
| **OT / 最优传输** | moscot / CellOT | T1 otmix/otfix 族：mask 修复后本地四项全优，但**独立真值下净 −0.003 假象**；OT v2 16-seed 配对检验 d2 收益消失（p=0.97） |
| **scVelo / CellRank / Dynamo** | 算法类 | **数据契约证伪**：全部 h5ad 无 spliced/unspliced 层；Dynamo 需剪接/代谢标记数据不适用；Spateo 需空间分量不适用；Dynast 需 4sU 不适用；Monocle/Bio-Babel 只给伪时间轴 |
| **GPMM / Deformetrica / Esteban** | 几何形变方法 | **真榜 4 次证伪**：改形态必崩（selday/r6/vmorph/comp 全低于 scale_only 54.51）；Deformetrica 外推风险=我们的精确处境 |
| **SPHARM-PDM / ASM / PGA / ARAP / AtlasNet / NRICP** | 点云几何方法 | 已排除（需群体样本/网格/对应/大数据） |
| **Harmony / scVI** | 批次整合 | 明确**不用**（会把真实时间变化当 batch 消掉）；统一化只做 gene-wise rank/程序形状对齐 |
| **Bures subspace / PopTransport / persistent wot macrostate** | 榜单顶级队伍方法名 | **参考思路**：顶级队伍做的是分布/Bures 几何与群体传输，不是细胞级位移（分析记录） |
| **moscot 结构外推 / MIOFlow** | 算法类 | **REJECT / kill test 未过阈**，保守族晋级路线关闭 |
| **CellChat / 配受体** | — | 仅评估未用 |
| **KEGG 知识图谱** | 平台自带 | **已证伪**：KG 覆盖 108/32285，真值 DE 集 64/32285，交集为空；扩表更差 |

## 五、外部数据集（合规审计逐条记录）

| 数据 | 来源 | 用途/结论 |
|---|---|---|
| **GSE208162**（E12.5 心室，Gata4 KO/Het） | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208162 | **T3 training-only（官方标注）可用**；已下载解析 4 个 h5ad；267 panel 基因与 Mab21l2 响应正交（0.180=随机），预测 <1 分 |
| **GSE282547**（发育中心脏 Visium） | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE282547 | E14.5 心脏，500/500 基因全覆盖+真实坐标，**已通过 validator 推荐**（external-data-catalog） |
| **GSE247450**（MERFISH 内皮） | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247450 | E9.5，68/500 基因窄面板，仅 x/y；已验证但价值有限 |
| **sc3D / GSE197353**（Slide-seq） | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE197353 + https://figshare.com/articles/dataset/E9_0_Embryo_h5ad/21695879/1 | **已关闭（合规阻断）**：含 Tbx6 突变体、面板重叠 38%（T1 仅 8.3%）、12.2GB 未实跑 |
| **Extended Mouse Atlas** | https://marionilab.github.io/ExtendedMouseAtlas/ + https://bioinformatics.stemcells.cam.ac.uk/rlh60/Supplemental/ExtendedMouseAtlas/ | **已审计**：430,339 细胞；leak 测试 pearson 0.39–0.50 独立来源；但含受保护阶段，对应板价值被削 |
| **Tabula Muris** | https://registry.opendata.aws/tabula-muris/ | 降级历史候选（下载路线未复现，且不敌心脏图谱） |
| **Cardoso-Moreira 2019 脑发育** | 人 E-MTAB-6814 / 猕猴 E-MTAB-6813 / 小鼠 E-MTAB-6798 / 大鼠 E-MTAB-6811 / 兔 E-MTAB-6782（ArrayExpress） | 跨物种曲线方案主数据；**小鼠列含受保护阶段禁 T1**；人/猕猴/大鼠/兔可用（形状对齐用） |
| **人类 CS7–CS13 时空图谱** | HRA007143 / PRJCA025127（CNGB） | **最干净外部线**（非小鼠、非 held-out）；组织/物种不匹配，价值待实测 |
| **景乃禾 Geo-seq** | GSE98101 / GSE104243 | 小鼠密集时程；**含受保护阶段禁 T2** |
| **小鼠原肠胚图谱** | GSE236766 | EmbryoMatch 参考 |
| **灵长类原肠胚图谱** | GSE193007 | EmbryoMatch 参考 |
| **发育转录组** | GSE149457 | EmbryoMatch 参考 |
| **鼠心脏嵌合实验** | GSE236400 | EmbryoMatch 阶段对照参考（嵌合效应不可作通用映射） |
| **T3 来源** | GSE283967 | EmbryoMatch T3 报告参考 |
| **GSE278603**（whole embryo） | — | 跨 agent 方向一致性检验：与全局方向 cosine −0.383，同阶段 replicate 极稳（0.944/0.990）⇒ 阶段方向本身不可外推 |
| **Tyser 心脏原始数据** | — | T2 方向一致性检验：cosine −0.046/−0.049 近噪声 |

> 合规句式说明：上表"受保护阶段禁 T1/T2"均指官方规则定义的 held-out 阶段（数据不得用于对应板预测），属合规判定，不包含任何 held-out 测量反推内容。

## 六、数据/资源平台

| 平台 | 链接 | 用途 |
|---|---|---|
| GEO | https://www.ncbi.nlm.nih.gov/geo/ | 外部数据主来源 |
| ArrayExpress | https://www.ebi.ac.uk/biostudies/arrayexpress | 跨物种脑发育数据 |
| CellxGene Discover | https://cellxgene.cziscience.com/ | 预训练模型语料审计（确认含小鼠 held-out 与否） |
| CNGB | https://db.cngb.org/ | 人类 CS7–CS13 时空图谱 |
| Figshare | https://figshare.com/ | sc3D 便捷 h5ad 对象 |
| Gene Ontology | https://geneontology.org/docs/go-citation-policy/ | 程序基因集打分（CC BY 4.0，公开基因集非数据） |
| AutoDL（云 GPU） | 云端 GPU 平台 | TF-Sapiens 推理/训练；**凭据严禁入仓库** |

## 七、我们参考过的核心"思路"（非工具，方法论）

1. **结构定理**（多板通用）：de/dir/sev 只依赖 pseudobulk；variogram 依赖细胞内基因对差异；任何改变 pseudobulk 排序的 per-gene 变换必然毁 variogram；只有替换/重采样真实细胞能避开。→ 五板最优解全部是"真实细胞+不修改表达"。
2. **载体稀释**（T3 新最佳来源）：kb 族 = 用真实细胞稀释 KO 比例，`kbb_n6000_b055_k65` 66.61。
3. **成熟度软加权**（T1 +2.30）：用方向分数重采样真实细胞（kp7_m_b050 53.67），不改表达。
4. **位移+零膨胀掩膜**（T3 counts 真机制）：`np.where(nz, X+d, X)` 而不是 `X+d`（kodir/mx/koq 五族 vario 崩因）。
5. **分布级传输 vs 细胞级位移**（榜单顶级队伍启示）：Bures 几何、群体传输。
6. **先证伪后投入**：每一条外部工具线都先做数据契约核查（scVelo 无层、Dynamo 无剪接、Deformetrica 参数爆炸、KG 交集为空），再做合规审计，最后才花 GPU/名额。

---

## 附：链接的既有内部文档（文件名保留作索引，不随仓公开）

- `COMPLIANCE_CROSS_SPECIES_2026-09-22.md` —— 跨物种数据逐条合规判定
- `PRETRAINED_CORPUS_AUDIT_2026-09-22.md` / `PRETRAINED_MODEL_COMPLIANCE_2026-09-22.md` —— 预训练模型语料核查
- `EXTERNAL_DATA_AUDIT_2026-09-21.md` —— 外部数据清单
- `external-data-catalog`（本地 clone）—— 外部数据验证器与 SOURCE_TERMS
- `CONCLUSION_2026-09-24.md` / `COMPLIANCE_AND_CLOUD_2026-09-24.md` —— sc3D 关闭、atlas 泄漏结论
- `TF_SAPIENS_LINE_2026-09-22.md` —— TF-Sapiens 完整评估
- `KG_DIRECTION_FALSIFIED_2026-09-22.md` —— KG 证伪细节
- `CROSS_SPECIES_2026-09-22.md` —— 跨物种曲线方案
- `FORGOTTEN_LINES_2026-09-23.md` —— 遗忘线索总账（v2）

> 上述文档位于私有工作区，为内部证据链；公开仓库只引用文件名作索引，不包含其内容。
