# -*- coding: utf-8 -*-
"""从台账 JSON 生成实验报告体 Markdown：按方法族分组，族级实验段落 + 全量提交明细。"""
import json
import re

DUMP = r'C:\Users\FB\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.sessions\38442478683482882\agents\m_0cwprxb4apa\taizhang_dump.json'
OUT = r'D:\freebuff\virtual-embryo-challenge\journey_repo'

d = json.load(open(DUMP, encoding='utf-8'))

def mark(v):
    return '—' if v in ('', '待抓', '待补') else str(v)

def esc(s):
    return str(s).replace('|', '/').replace('\n', ' ')

# ---------- 族映射规则：返回族 id ----------
def family_of(sheet, r):
    ver = str(r[1]).strip().lower()
    met = str(r[2]).strip().lower()
    fname = str(r[2]).strip()
    note = str(r[13] if sheet in ('T2_heart_extrap','T2_heart_interp','T2_embryo_interp') and len(r) > 13 else (r[9] if len(r) > 9 else '')).strip().lower()
    if sheet == 'T1_val':
        if str(r[1]).strip() == '待传' or 'e4c' in met or 'lineage' in met or '型特异' in met or (not met and not ver and 'e4c' in str(r[9]).lower()): return 'e4c'
        if 'kp' in met or 'kp' in ver: return 'kp'
        if 'vs' in met or ver.startswith('vs'): return 'vs'
        if 'otf3' in met or 'otf3' in ver: return 'otf3'
        if 'state_population' in met: return 'statepop'
        if 'covsafe' in met: return 'covsafe'
        if 'mm_n1249' in met or 'mm' == ver or 'mm' in ver: return 'mm'
        if 'mommask' in met or 'mom-mask' in met or 'mom' in ver: return 'mommask'
        if 'ancestor' in met: return 'ancestor'
        if 'robust' in met: return 'robust'
        if 'dirprop' in met or 'dir24' in met: return 'dir'
        if 'selday' in met or 'selpc1' in met or 'selanti' in met: return 'sel'
        if 'copy' in met: return 'copylast'
        if 'mix20' in met: return 'mix20e85'
        if 'marker_program_momentum' in met: return 'mpm'
        if 'multiplicative' in met: return 'mult'
        if '匿名' in met: return 'anonymous'
        if '程序混合' in met or 'ot_program' in met or 'ot 分配' in met: return 'otprog'
        if 'markov' in met or 'mk' in ver: return 'markov'
        if 'otmix' in met or 'otmix' in ver: return 'otmix'
        if 'shift' in met or ver in ('l1','l2','l3','l4','l5','l6','p1','p2','p2-dup','p4','p5','s2.5','s-sr'): return 'shift'
        return 'other'
    if sheet == 'T2_embryo_interp':
        if 'vlk8' in met: return 'vlk8'
        if 'vg_' in met or 'vg_ourmixs' in met: return 'vg'
        if 'cpf' in met: return 'cpf'
        if 'tls2n5000' in met: return 'tls'
        if 'gpsnnu' in met: return 'gpsnnu'
        if 'gps' in met: return 'gps'
        if 'bgm' in met: return 'bgm'
        if 'v1replica' in met: return 'v1rep'
        if 'mix_brkt' in met: return 'mixbrkt'
        if 'v1' in ver or 'v1' in met: return 'v1'
        return 'other'
    if sheet == 'T2_heart_interp':
        if 'v1vc100' in met: return 'v1vc'
        if 'v1geom' in met: return 'v1geom'
        if 'v1g2000s' in met: return 'v1g2000'
        if 'gps50' in met: return 'gps50'
        if 'mix_brkts' in met or 'mix_brkt' in met: return 'mixbrkt'
        if '类型分层' in met or ver == 'v1': return 'v1'
        return 'other'
    if sheet == 'T2_heart_extrap':
        # 三行空方法列按日期补全（备注可证）
        if str(r[0]).strip() == '2026-09-19 16:00': return 'r6'
        if str(r[0]).strip() == '2026-09-19 18:45': return 'v2ga6'
        if str(r[0]).strip() == '2026-09-19 19:05': return 'v4a10'
        if 'cpfx' in met: return 'cpfx'
        if 'selday' in met: return 'selday'
        if 'scale_only' in met: return 'scaleonly'
        if 'mix20_scale' in met: return 'mix20scale'
        if 'compw30' in met: return 'compw30'
        if 'vmorph' in met: return 'vmorph'
        if 'comp_c100' in met: return 'compc100'
        if 'r6b70a20' in met: return 'r6'
        if 'v4a10' in met: return 'v4a10'
        if 'v2ga6' in met: return 'v2ga6'
        if 'population_growth' in met or 'v4' in ver: return 'v4'
        if 'w005' in met: return 'w005'
        if 'v3' in ver or 'v3' in met: return 'v3'
        if 'v1' in ver: return 'v1'
        return 'other'
    if sheet == 'T3_gata4':
        if 'kb' in met or 'kb' in ver: return 'kb'
        if 'cmpw' in met: return 'cmpw'
        if 'prw' in met: return 'prw'
        if met.startswith('pw'): return 'pw'
        if 'cmp' in met: return 'cmp'
        if 'mx50amp' in met: return 'mx50amp'
        if 'pk26' in met or 'ctlp26' in met: return 'pkctl'
        if 'koq' in met: return 'koq'
        if 'ko2' in met: return 'ko2'
        if 'kodir' in met: return 'kodir'
        if 'mix' in met: return 'mix'
        if 'gata4 状态程序' in met: return 'state'
        if 'cardiac' in met: return 'cardiac'
        if 'wt_identity' in met or 'wt 复制' in met: return 'wt'
        if 'transfer' in met: return 'transfer'
        return 'other'
    return 'other'

# ---------- 族实验段落（技术/工具/问题/结论，全部具体） ----------
T1_FAM = {
 'shift': ('pseudobulk shift（全局漂移）', [
    '技术：以 E9.5 细胞为载体，逐基因加全局漂移量（Δgene = mean_gene(E9.5) − mean_gene(E8.5) × damp），damp∈{0.25,0.5,1.0,1.25,1.5,2.0,2.5}；非对称变体上/下幅度取不同系数（up1.5/dn0.5、up1.5/dn0.75）；弥散探针 shift@0.5+s0.5 在漂移上叠加高斯噪声；shift@2.5 是 damp 拐点测试。实现：baselines/t1_shift.py。',
    '工具：baselines/t1_shift.py（配方参考官方基线 pseudobulk shift，https://virtualembryo.ai/challenge/baselines）、veckit 本地计分器、台账回填。',
    '遇到的问题：① variogram 全族偏低（35.7~44.5），全局平移破坏基因-基因协方差结构；② de_score 封顶 ≈45.3，全局标量猜不中"被点名的基因"；③ damp>2.5 无增益（S2.5 是拐点）；④ 非对称变体（up1.5/dn0.5、up1.5/dn0.75）比对称更差；⑤ 弥散探针 P4@0.5+s0.5 只有 42.29，噪声直接毁 vario(-19) 和 mmd。',
    '结论：shift 是最强简单基线，族峰值 shift@2.5 = 48.85（rank 142/202，de 45.3/dir 56.4/mmd 55.4/vario 34.1），超过实测地板 46.84 约 2 分；但"用 vario 换 de"到头，被后续按类型/按状态的生成超越。']),
 'otmix': ('OT 混合（WOT 耦合 + 类型转移重采样）', [
    '技术：用 WOT 在 E8.5→E9.5 上学细胞耦合矩阵，按类型转移概率重采样生成 E9.5 细胞；掩膜A（边掩膜 378→61 条边，去低质量耦合边）变体 otmixp 含生长因子π（出生-死亡过程），otmixm 无生长。实现：baselines/t1_otmix.py。',
    '工具：baselines/t1_otmix.py、wot_analysis/（WOT 耦合矩阵与边掩膜，WOT 库 https://github.com/broadinstitute/wot）、veckit。',
    '遇到的问题：① otmixp@1.0 的 variogram 崩到 28.8（生成幅度毁变异结构）；② 无 shift 骨架的 OT 混合（otmixm）de 44.3/mmd 53.6 尚可但总分被 vario 拖累；③ damp 变体（0.3）46.75 低于 shift 族。',
    '结论：OT 混合路线失败——类型转移重采样不能替代表达层面的受控生成；族峰值 otmixp@1.0 = 47.52。']),
 'markov': ('Markov 通量（时间齐性转移规则）', [
    '技术：把 E8.5→E9.5 学到的转移矩阵当作固定规则，套用到 E9.5 载体上生成"下一阶段"（时间齐性假设）。full 版与非 full 版同日提交。',
    '工具：t1_rewrite 脚本族、veckit。',
    '遇到的问题：两个版本同分 44.19（de 38.2/dir 52.2/mmd 46.1/vario 38.8），低于实测地板 46.84；本地 proxy 曾给 0.964 的乐观信号，真榜直接证伪——转移规则本身随时间在变。',
    '结论：**时间齐性假设证伪**，Markov 通量族关闭。本地 proxy 不可信的典型案例。']),
 'otprog': ('OT 分配 + 程序混合（程序线性组合）', [
    '技术：OT 分配耦合 + 已知"程序"（基因程序模块）的线性组合生成新细胞；ablation 变体去 birth（no_birth）、去 growth（no_growth）。',
    '工具：t1_rewrite 脚本族、veckit。',
    '遇到的问题：无 shift 骨架时 45.22 低于实测地板 46.74；去 birth 降 0.67、去 growth 降 0.42（都有微弱正增益但骨架太弱）；程序混合只能在已知程序凸包内插值，生成不出真正的新状态。',
    '结论：凸包困境——"新状态"必须处理 population birth/death，程序线性组合不够；族峰值 45.22，关闭。']),
 'anonymous': ('shift + 匿名程序混合', [
    '技术：在 shift@1.0 骨架上叠加匿名程序混合（未知程序源的线性组合）。',
    '工具：t1_rewrite 脚本族、veckit。',
    '遇到的问题：de 44.1 达到 shift@1.25 档，但 variogram 崩到 31.7，总分 47.34 低于纯 shift@1.0 的 48.13——混合幅度一大就毁掉协方差结构。',
    '结论：生成内容幅度必须小、位置受控、最后加；匿名混合关闭。']),
 'mult': ('multiplicative（乘性低秩生长）', [
    '技术：E9.5 表达 × exp(0.25 · rank8 低秩矩阵 × 掩膜祖先) 的乘性模型（rank8 低秩生长因子）。',
    '工具：t1_rewrite 脚本族、veckit。',
    '遇到的问题：de 39.6 弱于 shift 族；mmd 51.0/vario 48.1 优于 L4 但总分 48.27 仍低于 shift@2.0 的 48.74。',
    '结论：乘性变体未超过加性 shift；低秩乘性生长不匹配真实 de 响应，关闭。']),
 'mpm': ('marker 程序动量', [
    '技术：per-program 动量（r ∝ (s/ś)^+0.5 型特异速率）在 shift@2.5 骨架上的 marker-program 版。',
    '工具：t1_rewrite 脚本族、veckit。',
    '遇到的问题：48.80 与 shift@2.5 的 48.85 持平，de/vario 略降、dir/mmd 微升——per-program 动量没有超过全局 damp。',
    '结论：per-program 动量未超全局 damp，阶段 C 探针关闭。']),
 'mix20e85': ('mix20 + E8.5 载体混合', [
    '技术：80% E9.5 预测 + 20% E8.5 原始细胞的混合提交。',
    '工具：veckit、台账。',
    '遇到的问题：46.37 低于实测地板 46.84 和 shift@2.5 的 48.85。',
    '结论：混入旧阶段细胞降低分布贴合度，关闭。']),
 'copylast': ('copy_last（复制上一阶段，地板探针）', [
    '技术：直接把 E9.5 表达复制为预测（5118 细胞采样）。',
    '工具：veckit、台账。',
    '遇到的问题：实测地板 46.84（09-16 版）比早期 L4 探针 46.74 高 0.10；同文件两次双传烧掉名额（21:44 与 21:45 完全同分）。',
    '结论：实测地板 = 46.84，官方地板 = 50（官方以 50 为 floor 刻度）；copy_last 是零信息基线，一切方法先与此比较。']),
 'sel': ('sel 选择族（selday/selpc1/selanti）', [
    '技术：按"选择"逻辑生成——selday（按发育日选择比例）、selpc1（按 PC1 选择）、selanti（反选择），比例 f∈{20,30,40,50}%。',
    '工具：T1 生成器脚本族、veckit。',
    '遇到的问题：全族崩盘——selpc1_f20 30.21 是全旅程最低分（mmd 15.7/vario 19.6 双崩）；selday 只有 f50 超地板 47.02 但仍低于 shift@2.5；selanti_f50 42.66（mmd 37.2 弱）。',
    '结论：基于人工"选择规则"生成方向错误，全族关闭。']),
 'dir': ('dir24 / dirprop（方向类）', [
    '技术：按 24 方向类别（dir24）或方向比例（dirprop B 族）重采样，k∈{2000,3000}。',
    '工具：T1 生成器脚本族、veckit。',
    '遇到的问题：dir24_k2000_s100 与 dirprop_B_k2000 逐项完全同分（47.19/44.2/53.1/49.2/40.4），疑似同文件改名重传；k3000 变体 vario 37.8 更弱。',
    '结论：方向类重采样 de 44.2 全族最高但 vario 40.4 拖累；族峰值 47.19，未破地板，关闭。']),
 'robust': ('robust_consensus（鲁棒共识）', [
    '技术：多候选鲁棒共识 + damp 0.45 漂移。',
    '工具：T1 生成器脚本族、veckit。',
    '遇到的问题：47.94 超实测地板 46.84 但未超 shift@2.5 的 48.85；de 40.1 弱。',
    '结论：鲁棒共识只能稳住分布指标（mmd 49.8/vario 48.6），不能提升 de；关闭。']),
 'ancestor': ('ancestor_donor_birth（祖先-供体出生混合）', [
    '技术：祖先细胞 × 供体出生混合（10% 混合比）。',
    '工具：T1 生成器脚本族、veckit。',
    '遇到的问题：46.74 微低于实测地板 46.84（-0.10）；同文件重复重传烧 1 名额（04:35 与 04:46 逐项同分）。',
    '结论：出生混合 10% 无增益；关闭。']),
 'mommask': ('momentum mask（动量掩膜）', [
    '技术：在 shift 骨架上用动量掩膜 α=0.01 限制生成幅度（只对动量显著的基因/细胞类型施加漂移）。',
    '工具：T1 生成器脚本族、veckit。',
    '遇到的问题：de 43.8/dir 53.6/mmd 50.8 略逊 shift@2.5，但 variogram 49.5 比 shift@2.5 的 34.1 暴涨 15.4，总分 49.49 超 48.85（+0.64）。',
    '结论：T1 首破 49。教训：**掩膜限制幅度保住了 variogram 结构**，比无脑加大 damp 更有效。']),
 'mm': ('mm（库大小归一化）', [
    '技术：mm 生成器在 log1p 空间做库大小归一化，使中位库大小对齐到 10000（参考基线 E9.5 base 的精确 10000）；n=1249 采样，b=0.70。',
    '工具：T1 生成器脚本族、veckit。',
    '遇到的问题：mm_n1249_b070 49.93，距官方地板 50 仅 0.07；mmd 52.2/vario 50.7 双过线，de 43.1 仍弱。',
    '结论：库大小归一化是必要的基线修正（对 de 排序无影响，但保分布）；mm 族把分布指标拉到过线水平，破 50 只差临门一脚。']),
 'covsafe': ('covsafe（协方差安全化，deepgen 工作线）', [
    '技术：mm 系（库大小归一化生成器）基础上做协方差安全化（l=25 = 保护基因-基因协方差的强度参数）。',
    '工具：deepgen_t1 候选管线、check_submission.py、veckit、真榜回填。',
    '遇到的问题：真榜 48.09 低于生产参考 shift@2.5 的 48.85（-0.76）——只改善 variogram（+16.3），de/dir/mmd 全降；归因结论：本地协方差保持不足，残差方向对 E10.5 校准错误。',
    '结论：**保护结构不能代替正确的未来阶段转移方向**；covsafe 族关闭，不再上传 l10/l50 变体。']),
 'vs': ('vs（方差放大）', [
    '技术：方差放大——对 E9.5 载体中方差最大的 K 个基因的偏离乘以放大系数 c 写回（vs200=K200、vs500=K500；c15/c135/c165=系数 1.5/1.35/1.65），只动协方差不碰 pseudobulk；vs_kp6_a030_n1249 为 vs × 知识程序 kp6 叠加（知识位移 a=0.30，n=1249）；方向验证：3 种子×25 组共 75 点全正。',
    '工具：tools/_t1_vs_make.py、veckit。',
    '遇到的问题：vs200_c165 50.52 首破官方地板 50（mmd 55.7 当时新高）；vs500_c135 只有 50.01（de 40.9 弱）；vs_kp6_a030_n1249 50.67 继续刷新。',
    '结论：vs 族是 T1 破 50 的转折点——方差放大（动协方差）比纯全局漂移更贴近真实发育方差结构；族峰值 50.67。']),
 'otf3': ('otf3（otfix：OT 方向 + 掩膜 + 极小幅度）', [
    '技术：otfix——OT 混合方向 + 掩膜 + 极小幅度（n=2500，om2 掩膜变体；本地独立真值子集曾显示四轴全面更优）。',
    '工具：tools/_t1_otf3_robust.py、veckit。',
    '遇到的问题：47.09 低于官方地板 50 与 mm_n1249_b070 的 49.93；四轴全面劣于 mm 系（加权 −2.87 vs 实际 −2.84）——T1 本地代理不可用的直接证据（本地曾显示四轴更优）。',
    '结论：OT 流变体未超 vs 族；关闭。']),
 'statepop': ('state_population_dynamics（状态群体动力学）', [
    '技术：双组件动力学（实现见 baselines/t1_state_population_dynamics.py 模块 docstring）：① 类型级 birth/death 动量——从 E8.5→E9.5 组成变化估计动量并保守外推一步，载体从外推群体采样（而非按自然 E9.5 比例复制）；② 状态动力学——每基因归入表达程序（cardiac/endodermal/neural_crest/mesodermal/vascular 五程序），用各载体细胞状态偏离其类型质心的量调制类型速度，E9.5 新类型给显式出生状态速度（E9.5 残差仍保留为载体）。仅用已发布 E8.5/E9.5 数据，无隐藏阶段输入。',
    '工具：baselines/t1_state_population_dynamics.py、veckit。',
    '遇到的问题：47.93 低于官方地板 50；de 43.0 高于 otf3 但仍弱、vario 41.6 偏弱。',
    '结论：动力学建模方向正确但实现未过线；关闭。']),
 'kp': ('kp 族（知识程序位移 + 方差放大 / 成熟度加权）', [
    '技术：两机制叠加：A=知识程序位移——教科书发育程序枚举 10 程序 271 基因（印记/神经/ECM/多能/核糖体/糖酵解/应激/上皮等；程序清单为发育生物学领域知识，无单一 URL），对 pseudobulk 加位移（a∈{0.15,0.25,0.35} 幅度；u=平权 / w=按程序命中加权）；B=方差放大——方差最大 K=500 基因偏离 ×c=1.5（b500c15 即 K=500、c=1.5；n=2000 采样）。变体：kp2/3/4/5 为机制组合序号与消融（raw=原始输入、wo=无加权、aonly=仅 A）；kp7_m 为成熟度加权变体（m 机制 + b=0.50 成熟度指数，b=0.00 为对照）。关键设计决策：生物学知识应作"筛选程序基因集"而非逐基因位移。',
    '工具：tools/_t1_kp_make.py、_t1_kp_make3.py、check_submission.py、veckit、真榜回填。',
    '遇到的问题：① kp 探路 kp_a015u 只有 48.88；② raw 化变体全败（kp5_kw/kp4_so/kp2_raw/kp3_w_raw 全部 47~48，vario 46.6 崩）；③ aonly_raw 去 b500c15 组件后三线全掉（47.37）；④ wo 变体 51.91 未超 w 全管线；⑤ kp7_m_b000 对照 51.37，比 b050 的 53.67 低 2.3（de -4.1/dir -3.2/mmd -1.7）——b=0.50 是关键参数；⑥ kp3_w_a025_b500c15_n2000 52.18 曾创 T1 最佳（dir/mmd/vario 三线过线）。',
    '结论：kp7_m_b050_n2000 = **53.67**（rank 93/254，de 44.2 破 42 瓶颈/dir 57.6/mmd 57.6/vario 54.7 四项新高），当前 T1 最佳。kp7 成熟度加权曾遭 500 面板 OOF 否决，但 32285 面板真榜 +2.30——小面板 OOF 结论不能外推到完整面板。']),
 'e4c': ('E4c 待传候选（lineage Δ / 动量）', [
    '技术：E4c-lineage Δ（掩膜A 祖先混合，无重采样）；E4c-mom 型特异速率 r∝(s/ś)^+0.5（动量）。',
    '工具：t1_rewrite 脚本族。',
    '遇到的问题：尚未按 label-free 格式门重新生成；本地剖面疑似 copy_last 伪影。',
    '结论：待传状态，未上传未评分。']),
}
T3_FAM = {
 'transfer': ('transfer（全局 Δ 扰动迁移）', [
    '技术：用 E9.5 WT→Mab21l2 KO 学到的全局响应 Δ（KO − WT 平均表达差）加到 E8.75 载体上（damp 1.0/1.5）。',
    '工具：baselines/t3_shift_transfer.py、veckit。',
    '遇到的问题：damp1.5 真榜 40.98——variogram 49.8→12.2 崩盘；damp1.0 从未成功提交（portal 无此文件）。',
    '结论：**全局 Δ 毁分布**：KO 响应不能当全局标量平移；transfer 家族关闭。']),
 'wt': ('wt_identity（地板探针）', [
    '技术：直接把 WT 表达复制为预测（E8.75 载体 + WT 分布）。',
    '工具：baselines/t3_wt_identity.py（wt_identity 为官方基线定义，https://virtualembryo.ai/challenge/baselines）、veckit。',
    '结论：T3 实测地板 = 45.81，官方地板刻度 = 50；一切方法先与此比较。']),
 'cardiac': ('cardiac（谱系限制 transfer）', [
    '技术：只对 cardiac 谱系细胞施加全局 Δ（谱系限制版）。',
    '工具：baselines/t3_shift_transfer.py、veckit。',
    '遇到的问题：damp0.5 44.36 / damp0.25 44.85——分布指标保住（mmd 48.8/49.8）但 de 掉到 37.4/37.7（KO 效应打不出来）。',
    '结论：谱系限制保护了分布、丢了效应；关闭。']),
 'state': ('Gata4 状态程序（a25/a35/a50）', [
    '技术：E8.75 载体 10pct + 型内归一化 + Gata4 状态程序（a 系数 0.25/0.35/0.50）。',
    '工具：t3_rewrite 脚本族、veckit。',
    '遇到的问题：三个变体 45.78/45.79/45.80，与地板平齐（+0.00）——状态程序没有产生 KO 响应。',
    '结论：三连发各占 1 名额零增益；关闭。']),
 'mix': ('mix（混合 KO 推断）', [
    '技术：把预测构造为"真实 KO 细胞 + WT 载体"的混合——mix 比例 p∈{20,30,40,50,60,70}%（p% KO 细胞 + (100−p)% WT 载体；p 是 KO 细胞比例）；kofeat 变体为 Gata4 靶基因特征清单输入（feat∈{0.05,0.1,0.2,0.35}，实测 amp 越大越差单调下降）；muld_m05 是 mix70 的幅度变体；cardiac/knn 是谱系与最近邻变体。',
    '工具：T3 生成器脚本族（mix 系列）、veckit。',
    '遇到的问题：① mix40_early 50.09（+0.09）——混早期载体几乎无增益；② cardiac/knn 变体（59.72/61.82）不敌原版 mix40_ko 63.58；③ kofeat 变体 64.06~64.52，feat 越小越接近峰值；④ muld_m05 64.39（sev 92.9 新高但 mmd 50.4 拖累）；⑤ mix70_ko 64.60 族峰值，severity_slope 92.3 当时新高；⑥ mix70_ko 重投一次（同文件再传，64.60 不变）烧名额。',
    '结论：mix 比例越高 sev 越高（mix70 sev 92.3）；族峰值 64.60。混真实细胞换 mmd 但 sev 上不去——"多混"不是主杠杆。']),
 'kodir': ('kodir（KO 方向）', [
    '技术：按 KO 方向（a=0.10）构造响应。',
    '工具：T3 生成器脚本族、veckit。',
    '遇到的问题：43.96 低于地板，variogram 18.1 崩。',
    '结论：方向构造毁分布；关闭。']),
 'ko2': ('ko2（KO 双路）', [
    '技术：KO 响应双路构造，n∈{5000,6000}，b=0.60。',
    '工具：T3 生成器脚本族、veckit。',
    '遇到的问题：64.68（n6000）/64.75（n5000），未超 cmp_n6000_b070 的 64.93。',
    '结论：ko2 是 cmp 的前身但未打满 KO 效应；关闭。']),
 'koq': ('koq（KO 量化）', [
    '技术：KO 响应量化构造（n=5000）。',
    '工具：T3 生成器脚本族、veckit。',
    '遇到的问题：58.04——mmd 24.8/vario 27.1 双崩。',
    '结论：koq 线失败；关闭。']),
 'pkctl': ('pk/ctl（26 基因逐基因变换）', [
    '技术：pk26g18（26 个程序基因、g=18 变体）/ ctlp26（对照 26 基因）——对点名基因逐个施加变换、其余不动；属 T3 逐基因变换族（pk/ctlp/koq/kodir/mx50amp 同族，variogram 5/5 崩到 10.8–27.1）。',
    '工具：T3 生成器脚本族、veckit。',
    '遇到的问题：pk26g18 38.91（mmd 21.4/vario 10.8 双崩）；ctlp26 43.14（mmd 7.9/vario 19.4 双崩）。',
    '结论：T3 逐基因变换九条路线无一生还，26 基因程序族关停。']),
 'mx50amp': ('mx50amp（50% 混合 + 幅度）', [
    '技术：50% 混合（mx50）+ 幅度 0.92（amp）构造——在 KO 响应方向上按幅度 0.92 施加变换；属 T3 逐基因/幅度变换族（variogram 5/5 崩到 10.8–27.1）。',
    '工具：tools/_t3_mx50_amp.py、veckit。',
    '遇到的问题：57.15——severity_slope 90.6 高但 variogram 15.8 崩。',
    '结论：幅度构造毁 vario；关闭。']),
 'cmp': ('cmp（celltype^β 重采样）', [
    '技术：cmp = 按细胞类型重采样（celltype^β 指数压平类型分布，β=0.70/0.55/1.00，n=6000；β=1.00 即自然类型比例，β<1 压缩 celltype 分布）。',
    '工具：T3 生成器脚本族（cmp 系列）、veckit。',
    '遇到的问题：① cmp_n6000_b070 64.93 破 64.6 平台（de 56.3/sev 97.0 大涨，mmd/vario 各降约 10）；② b=1.00 63.35 五项全低于 b070；③ b=0.55 65.31（de 56.3 持平、dir 60.3/sev 97.1 微升、mmd/vario 双升）——β 低侧更优，β 越大越差（斜率 ≈ −5.3 分/单位 β）。',
    '结论：cmp_n6000_b055 = 65.31；**压缩 celltype 分布（β<1）是 T3 的核心收益**。']),
 'cmpw': ('cmpw（KO 池 + E8.75 WT 载体稀释）', [
    '技术：cmpw = cmp_b070 平坦 KO 池加 E8.75 WT 载体稀释——KO 池 70%（β=0.70）+ 载体 30%，k 为载体比例（k=1.00 即 cmp_b070 本身，k50–k85 为稀释序列；n=6000）。',
    '工具：tools/_t3_cmpw_make.py、_t3_cmpw_axes2.py、veckit。',
    '遇到的问题：cmpw_n6000_k70 65.49 超 cmp_b055（+0.18）：de 54.8(-1.5)/sev 92.4(-4.7) 让位，mmd 55.2(+11.0)/vario 53.9(+6.8) 暴涨。',
    '结论：载体稀释赎回分布轴（mmd/vario）但付 sev 代价（≈4.6 分，两条独立路径确认）；cmpw 是过渡，kb 系在此基础上补齐 sev。']),
 'pw': ('pw（prior 加权，证伪）', [
    '技术：pw = prior 加权——在 cmp 基础上按 prior 轴（细胞类型方差轴）做加性加权（p=0.50/1.00，n=6000）；错因：把"加性扰动 dp→dp+Δ"当成"常数缩放 dp→c·dp"（rank 无关性只保护后者），实测 |d(pb)|=0.0414 是加性项。',
    '工具：T3 生成器脚本族（pw 系列）、veckit。',
    '遇到的问题：pw050 64.47（mmd/vario 高于 cmp 但 de 54.8/dir 58.1 略低，未超 64.93）；pw100 62.87（de/dir 更低）——β 单调下降 0→0.5→1.0。',
    '结论：prior 加权净负（β 单调递减），证伪；T3 上任何偏离纯 KO 细胞自然分布的操作都削弱 de。']),
 'prw': ('prw（官方 population_reweight + GSE 先验）', [
    '技术：prw = 官方 population_reweight 算子：对 WT 载体做 WT-vs-KO 分类器重采样（该算子原理上无法产生足够强响应）+ GSE 外部先验（s=0.10，1.2MB 小模型；GSE208162 先验与 Mab21l2 响应正交：落入 DE 集 48/267=随机期望）。',
    '工具：tools/_gse_cells_make.py、_t3_gse_prior.py、veckit；GSE208162 外部先验数据（https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208162）。',
    '遇到的问题：54.49——severity_slope 70.6 远低于 cmp 的 97.0（KO 效应未打出）；de 44.9/dir 51.3 弱；mmd 53.1/vario 51.9 分布保真做到了。',
    '结论：分布保住、效应打不出（sev 70.6 vs cmp 97.0）；外部先验方向对齐度不预测分数，关闭。']),
 'kb': ('kb（真实 WT 稀释 KO，A/B 证伪复核）', [
    '技术：kb = 真实 WT 细胞稀释 KO（kbgen：平坦 KO 池 + WT 载体稀释，k=65/75 稀释比例，n=6000；kbb 为 kb6000×b055 组合 k=65、b=0.55）；本地轴 A/B 半分割实验曾判其"全面劣于什么都不做、优势是自证"，复核查明该证伪用了两条已证伪的本地轴 + 错误载体配方（kb 载体误用 E9.5 WT，真值载体经 Gata4 均值反解为 E8.75 WT），不构成对真榜分数（66.36/66.61）的反证。',
    '工具：tools/_t3_kbgen.py、_t3_kb_ab.py、veckit。',
    '遇到的问题：① kb6000_k65 66.36 超 cmpw（de 56.3/dir 62.2 dir 新高/sev 97.9 sev 新高/mmd 45.0/vario 50.5）；② kbb_n6000_b055_k65 66.61：de/dir 持平、sev 98.0/mmd 46.1/vario 51.8 三涨；③ kb6000_k75 65.32 五项全线下滑（vario -3.0）——k=65 才是最优。',
    '结论：**kbb_n6000_b055_k65 = 66.61**（rank 48/187），当前 T3 最佳。稀释比例 k=65 + β=0.55 最优；k=75 方向错误。']),
}
T2E_FAM = {
 'v1': ('v1（单最近邻 log-linear 归一化 + 配对几何）', [
    '技术：以 E8.0 为训练载体，E7.25→E8.0 学 kNN 配对（k=1），对配对细胞做 log-linear 归一化插值 + 配对几何（坐标随配对平移），生成中间阶段预测。',
    '工具：t2 生成器脚本族、t2_data_contract.py、veckit。',
    '遇到的问题：59.00（95/152）为起点基线；几何配对只搬最近邻，状态连续性差。',
    '结论：v1 是 T2 embryo 首版，59.00 超地板 50；后续各族在此基础上叠加不同机制。']),
 'mixbrkt': ('mix_brkt（混合 + bracket）', [
    '技术：混合真实载体 + bracket 约束（只允许 E6.75/E7.25/E8.0 三者之间的类型转移），再叠加配对生成。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：59.07 只比 v1 高 0.07——d2_shape 26.3/occupancy_dice 19.0 偏弱（坐标生成不足）；scale 73.0 也拖累。',
    '结论：bracket 约束保住 de 57.0 但空间指标差；是 v1→bgm 的过渡。']),
 'bgm': ('bgm（背景混合生成）', [
    '技术：bgm = 在载体上叠加"背景程序混合"生成中间状态（f=0.15 变体控制混合强度）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：bgm 62.94 超 mix_brkt（+3.87）——dir 70.6/mmd 68.7/vario 67.3 全面领先，d2 49.2/occ 41.0 偏弱；f0.15 变体 57.97 反而更低。',
    '结论：bgm 是 embryo interp 第一个 62+ 平台；d2/occ 仍是短板。']),
 'v1rep': ('v1replica（v1 复刻）', [
    '技术：v1 严格复刻（控制变量）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：56.99，与 v1 的 59.00 有出入（采样不同）——本地与真榜排序不一致的典型案例。',
    '结论：控制变量复刻确认 v1 基线区间 ≈57~59。']),
 'gps': ('gps33（高斯过程插值）', [
    '技术：对配对细胞用高斯过程回归插值（33 个基因模块 gps33 / n=583 下采样变体），输出中间状态表达。',
    '工具：t2 生成器脚本族（gps 系列）、veckit。',
    '遇到的问题：gps33 62.37 < bgm 62.94（d2 55.6 更优但 scale 88.9 拖累）；gps33n583 61.36（de 58.2 全板最强档但整体低）；gps33s 63.19——与 gps33 同指标、仅 scale 88.9→98.7（+9.8），总分 +0.82。',
    '结论：**scale_log_ratio 是低成本高分项**：把库大小校准到参考尺度，一分不花提 0.8+ 分；gps33s = 63.19。']),
 'tls': ('tls2n5000（类型级整体平移）', [
    '技术：类型级整体平移（type-level shift）——对每类细胞整体平移表达（n=5000）；真榜 nh +7.8 成功但 d2 −31.8/occ −27.9 抵消。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：59.01——d2_shape 23.8/occupancy_dice 17.6 崩坏（类型级平移毁类型间相对位置）；曾误投 T1 面板被拒（32285 vs 498）。',
    '结论：类型级整体平移毁空间指标；关闭。']),
 'gpsnnu': ('gpsnnu（几何继承 + 最近邻唯一化）', [
    '技术：gps 族 nnu 变体——换表达来源：几何继承 + 最近邻唯一化（去掉约束配对，表达从几何最近邻继承）；本地 nh 代理曾精准命中 62.4，真榜 mmd −7.0/vario −13.4 吃光收益。',
    '工具：tools/_t2_gpsnn.py、_t2_gpsnn_u.py、veckit。',
    '遇到的问题：61.81 < gps33s 63.19——d2 55.6 与 gps33s 同档但 de 53.5/mmd 61.6/vario 53.4 偏弱。',
    '结论：无约束版丢失 gps 的分布优势；关闭。']),
 'cpf': ('cpf015r5k（同源配对 + 位置插值）', [
    '技术：cpf = 同源配对构造：同源配对 + 位置插值 pos_f=0.15 + 尺度修正（r 变体 anchor 200.88；n=5000 采样，5k 版在 cpf015r 超上限被拒后按 583–5000 上限重采样；本地预测 +2.4~2.5）。',
    '工具：tools/_cpf005_probe.py、check_submission.py、veckit。',
    '遇到的问题：cpf015r 原版 9000 cells 超本板上限被拒；cpf015r5k 65.31——de 55.8/dir 70.6/mmd 68.8/vario 67.1/d2 56.1 全面领先、occ 43.4 略弱。',
    '结论：**cpf015r5k = 65.31**（65/200）当前 T2 embryo interp 最佳。d2_shape/occupancy_dice 是剩余主要提升空间。']),
 'vlk8': ('vlK8（方差放大 K=8）', [
    '技术：vlK8 = 方差放大变体（对 K=8 个最高方差基因放大系数 c=1.25）；与 cpf015r5k 高度同构，唯一变量是方差放大——T1 上该杠杆值 +3.5（3 个真榜点），T2 上为负（收益打折一半以上而 nh 代价照付）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：64.75——与 cpf015r5k 高度同构（dir/mmd/vario/d2/occ/scale 几乎一致），差距在 de 55.2(-0.6)/mmd 67.1(-1.7)/nh 63.4(-0.9)。',
    '结论：vlK8c125 64.75 是 cpf 的近亲平台，未超 65.31；方差放大不迁移到 T2，关闭。']),
 'vg': ('vg_ourmixs（v1 配对位移场移植）', [
    '技术：vg_ourmixs = 改几何：v1 配对位移场移植（把 v1 的配对位移场移植到混合表达上）；nh 从 57.8 崩到 41.5（加权 −4.10）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：55.93——scale 98.7 强但 d2 52.8/occ 48.2/nh 41.5 偏弱，低于 bgm 62.94。',
    '结论：几何移植毁 nh；关闭。']),
}
T2H_FAM = {
 'v1': ('v1（类型分层 + 全局配对）', [
    '技术：按细胞类型分层，类型内做 E8.25→E8.75 全局配对插值（log-linear 归一化 + 配对几何）。',
    '工具：t2 生成器脚本族、t2_data_contract.py、veckit。',
    '遇到的问题：61.86（74/148）——heart interp 首版基线；500 vs 498 面板坑（缺 Casp4/Pnliprp1 被拒一次）。',
    '结论：v1 是 heart interp 起点 61.9；面板必须逐元素对齐官方 500 基因。']),
 'mixbrkt': ('mix_brkt / mix_brkts（混合 + bracket + scale）', [
    '技术：混合真实载体（E8.25/E8.75）+ bracket 类型约束 + 配对生成；mix_brkts 额外做库大小 scale 校准（scale_log_ratio 71.1→100.0 满档）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：mix_brkt 62.6 与 mix_brkts 除 scale 外逐项同分（de 52.1/dir 55.7/mmd 50.7/vario 34.7/d2 42.2/occ 54.4/nh 50.8）；scale 满档贡献 ≈ +2.4。',
    '结论：**mix_brkts = 65.01**（54/191）当前 heart interp 最佳；scale_log_ratio 从 71.1 提到 100.0 满档，总分提升约 +2.4。']),
 'gps50': ('gps50n1185（高斯过程）', [
    '技术：高斯过程插值（n=1185）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：50.2 与地板平齐——heart interp 的 gps 变体明显弱于 embryo 板。',
    '结论：gps 不适合 heart interp；关闭。']),
 'v1g2000': ('v1g2000s（手工复刻 v1 几何）', [
    '技术：v1g = 手工复刻 v1 几何（v1 配对位移场的复刻版，n=2000）；复刻不完整——d2 只有 48.7（v1 原版 88.1）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：60.0——几何约束变体低于 v1 的 61.9 与 mix_brkts 65.01；d2 48.7 远低于 v1 的 88.1。',
    '结论：v1 几何复刻不完整（v1 原件已不在本地）；关闭。']),
 'v1geom': ('v1geom5000s（v1 几何变体）', [
    '技术：v1 几何变体（n=5000；v1 原件已不在本地，坐标实际来自 v1replicas 另一套坐标）；真榜 d2 46.2 证明 v1 的几何没有被保存在任何本地文件。',
    '工具：tools/_t2hi_v1geo.py、veckit。',
    '遇到的问题：53.12——vario 37.6 崩（几何变换破坏表达分布）；scale 100.0 满档。',
    '结论：几何采样幅度大毁 vario；v1 系路线全部关闭。']),
 'v1vc': ('v1vc100（v1 + 方差控制，代理外推证伪）', [
    '技术：v1 + 方差控制（vc=100，坐标来自 v1replicas 而非 v1 原件）；错因 A：本地 nh 代理读数 0.00852 落在四点标定曲线区间 [0.04217, 0.13902] 之外，报告"62.04"是最左段线性外推（实测 50.8，误差 +11.24）；错因 B：引用本地不存在 v1 原件的真榜 d2=88.1 做类比（实测 42.2，差 46 分）。',
    '工具：tools/_heart_vc_sweep.py、veckit。',
    '遇到的问题：53.61——vario 34.7 弱；d2 42.2（−38.3 最大单轴损失）；相对 mix_brkts 65.01 净 −11.40。',
    '结论：**代理读数必须先落在标定区间内**；v1 系路线全部关闭（v1vc100/v1geom5000s/v1g2000s/gps50n1185）。']),
}
T2X_FAM = {
 'v1': ('v1 早期候选', [
    '技术：早期候选（09-04 首版，无版本后缀）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：46.4 起步，低于地板 50。',
    '结论：extrap 板起点，逐步探索。']),
 'v3': ('v3（置信收缩类型趋势 + 均匀载体 + 坐标放大）', [
    '技术：置信收缩类型趋势 damp0.75 + 均匀 E9.5 载体 + 坐标 ×1.31。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：48.71（mmd 33.6 最大失分，scale 100 满分）；同文件 09-06 双传、09-14 第三次重传（历史记录，禁止再次上传）。',
    '结论：坐标放大 + 置信收缩方向错误；v3 族关闭。']),
 'v4': ('v4 population_growth（群体增长投影）', [
    '技术：E9.5 载体 + 群体增长幅值投影（population growth）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：49.26——d2_shape 30.6 最大失分；de 52.8 全族最高、scale 100 满分但总分仍低于地板 50。',
    '结论：群体增长投影动形态失败；v4 关闭。']),
 'v2ga6': ('v2ga6（几何幅度）', [
    '技术：v2 几何幅度 a=6。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：53.6 接近地板但未破。',
    '结论：几何幅度未破 50；关闭。']),
 'v4a10': ('v4a10（增长幅值 10）', [
    '技术：population growth 幅值 10。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：50.1 微过地板。',
    '结论：增长幅值调参收益极小；关闭。']),
 'r6': ('r6b70a20（形态外推）', [
    '技术：形态外推 r6（b=0.70, a=0.20 形态/几何幅度）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：38.97——形态外推重罚。',
    '结论：改形态被重罚（38.97，d2 11.9 崩）——extrap 板第一个形态线证伪点。']),
 'compc100': ('comp_c100（构成 + 形态）', [
    '技术：构成混合 + 形态变换（c=100）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：32.8——全旅程最低分，形态线最惨证伪点。',
    '结论：形态变换不可逆；关闭。']),
 'vmorph': ('vmorph_s120（虚拟形态）', [
    '技术：虚拟形态变换 s=120。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：46.8——d2 等几何指标惩罚。',
    '结论：虚拟形态路线失败；关闭。']),
 'scaleonly': ('scale_only（仅 scale 调整）', [
    '技术：只把库大小/构成按外推目标阶段比例调整，坐标与形态完全不动（scale_log_ratio 校准到 100 满档）。',
    '工具：t2 生成器脚本族（scale 系列）、veckit。',
    '遇到的问题：54.51 当前 extrap 最佳（68/185）——scale 满分 100、各指标均衡（de 46.8/dir 49.8/mmd 50.5/vario 50.1/d2 49.9/occ 54.1/nh 51.1）。',
    '结论：**只动 scale/构成、不动形态**是 extrap 板唯一正确路线。']),
 'mix20scale': ('mix20_scale（混合 + scale）', [
    '技术：20% 混合 + scale 校准。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：53.9 低于 scale_only 54.51。',
    '结论：混合不加分；关闭。']),
 'compw30': ('compw30_scale（构成加权 + scale）', [
    '技术：构成加权 30% + scale。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：53.7 低于 scale_only。',
    '结论：构成加权不加分；关闭。']),
 'w005': ('w005（沿 scale_only 端最小位移 0.05）', [
    '技术：w005 = 沿 scale_only 端做最小位移（位移幅度 0.05）：只动极少量坐标位移、保住 de/dir 端优势，留一点点分布改善空间（备选 w010=位移 0.10、wk20/wk50=只动 20–50 个基因做分布微调）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：54.43（rank 72/204）——de 46.8/dir 49.8/mmd 50.5/vario 50.1/d2 49.9/occ 54.1/scale 100/nh 51.1，全指标均衡型次佳，距 scale_only 54.51 仅 0.08。',
    '结论：均衡型与 scale_only 接近但未超；w005 = 54.43 第二高。']),
 'selday': ('selday（选择天，关闭）', [
    '技术：selday 族——按发育日选择细胞（selday30/50_scale），对 E9.5 载体做 30%/50% 日期选择后仅 scale 调整。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：27.54 / 28.9——全旅程最低分（mmd/vario/d2/occ 全面崩坏），日期选择破坏了 E9.5 的细胞构成。',
    '结论：日期选择对 extrap 无效；正式关闭。']),
 'cpfx': ('cpfx（类型级位移平移外推）', [
    '技术：cpfx = cpf 同族外推变体：表达不变、坐标做类型级位移平移（n=8000, a=0.10）；d2_distance 规范化后比较成对距离分布，刚体缩放不改变形状、平移改变类型间相对位置——d2 崩 5.7。',
    '工具：tools/_heart_extrap_cpfx.py、veckit。',
    '遇到的问题：52.12——d2_shape 5.7 崩（形态外推被重罚）；occupancy_dice 42.0。',
    '结论：条件流外推动形态同样死；形态线第四次证伪，extrap 板形态路线全部关闭。']),
}

# ---------- 英文族段落（与中文族一一对应，机制数据/参数/分数原样保留） ----------
T1_EN = {
 'shift': ('pseudobulk shift (global drift)', [
    'Method: use E9.5 cells as the carrier and add a per-gene global drift (Δgene = mean_gene(E9.5) − mean_gene(E8.5) × damp), damp∈{0.25,0.5,1.0,1.25,1.5,2.0,2.5}; asymmetric variants use different up/down coefficients (up1.5/dn0.5, up1.5/dn0.75); scattered probe shift@0.5+s0.5 adds Gaussian noise on the drift; shift@2.5 is the damp-knee test. Implementation: baselines/t1_shift.py.',
    'Tools: baselines/t1_shift.py (recipe follows the official pseudobulk shift baseline, https://virtualembryo.ai/challenge/baselines), local veckit scorer, ledger backfill.',
    'Issues: ① variogram low across the family (35.7–44.5) — the global shift breaks the gene–gene covariance structure; ② de_score caps at ≈45.3 — a global scalar cannot hit the "named genes"; ③ damp>2.5 gives no gain (S2.5 is the knee); ④ asymmetric variants (up1.5/dn0.5, up1.5/dn0.75) are worse than symmetric; ⑤ scattered probe P4@0.5+s0.5 only 42.29 — noise directly destroys vario (−19) and mmd.',
    'Conclusion: shift is the strongest simple baseline; family peak shift@2.5 = 48.85 (rank 142/202, de 45.3/dir 56.4/mmd 55.4/vario 34.1), ≈2 points above the measured floor 46.84; but "trade vario for de" reaches its limit here and is superseded by per-type / per-state generators.']),
 'otmix': ('OT mixture (WOT coupling + type-transfer resampling)', [
    'Method: learn a cell coupling matrix with WOT on E8.5→E9.5, resample E9.5 cells by type-transition probability; masked variant A (edge mask 378→61 edges, dropping low-quality coupling edges) — otmixp includes growth factor π (birth–death process), otmixm without growth. Implementation: baselines/t1_otmix.py.',
    'Tools: baselines/t1_otmix.py, wot_analysis/ (WOT coupling matrix and edge mask, WOT library https://github.com/broadinstitute/wot), veckit.',
    'Issues: ① otmixp@1.0 variogram collapses to 28.8 (generation amplitude destroys the variance structure); ② OT mixture without the shift skeleton (otmixm) gets de 44.3/mmd 53.6 but is dragged down by vario; ③ damp variant (0.3) 46.75 below the shift family.',
    'Conclusion: the OT-mixture route fails — type-transfer resampling cannot replace controlled generation at the expression level; family peak otmixp@1.0 = 47.52.']),
 'markov': ('Markov flux (time-homogeneous transition rule)', [
    'Method: treat the transition matrix learned on E8.5→E9.5 as a fixed rule and apply it to the E9.5 carrier to generate the "next stage" (time-homogeneity assumption). The full and non-full versions were submitted on the same day.',
    'Tools: t1_rewrite script family, veckit.',
    'Issues: both versions score identically 44.19 (de 38.2/dir 52.2/mmd 46.1/vario 38.8), below the measured floor 46.84; a local proxy once gave an optimistic 0.964 signal, the real board falsified it — the transition rule itself changes over time.',
    'Conclusion: **the time-homogeneity assumption is falsified**; the Markov flux family is closed. A textbook case of an untrustworthy local proxy.']),
 'otprog': ('OT assignment + program mixture (linear combination of programs)', [
    'Method: OT-assignment coupling plus a linear combination of known "programs" (gene program modules) to generate new cells; ablation variants remove birth (no_birth) and growth (no_growth).',
    'Tools: t1_rewrite script family, veckit.',
    'Issues: 45.22 without the shift skeleton, below the measured floor 46.74; removing birth loses 0.67, removing growth loses 0.42 (both weakly positive but the skeleton is too weak); program mixtures can only interpolate inside the convex hull of known programs and cannot generate genuinely new states.',
    'Conclusion: convex-hull deadlock — "new states" require handling population birth/death; linear program combination is not enough; family peak 45.22, closed.']),
 'anonymous': ('shift + anonymous program mixture', [
    'Method: stack an anonymous program mixture (linear combination of unknown program sources) on the shift@1.0 skeleton.',
    'Tools: t1_rewrite script family, veckit.',
    'Issues: de 44.1 reaches the shift@1.25 tier, but variogram collapses to 31.7 and the total 47.34 is below pure shift@1.0 (48.13) — a large mixture amplitude destroys the covariance structure.',
    'Conclusion: generated content must be small in amplitude, position-controlled and added last; anonymous mixture closed.']),
 'mult': ('multiplicative (low-rank multiplicative growth)', [
    'Method: E9.5 expression × exp(0.25 · rank8 low-rank matrix × masked ancestors), a multiplicative model with a rank-8 low-rank growth factor.',
    'Tools: t1_rewrite script family, veckit.',
    'Issues: de 39.6 weaker than the shift family; mmd 51.0/vario 48.1 better than L4, but the total 48.27 still below shift@2.0 (48.74).',
    'Conclusion: the multiplicative variant does not beat additive shift; low-rank multiplicative growth does not match the real de response; closed.']),
 'mpm': ('marker program momentum', [
    'Method: per-program momentum (r ∝ (s/ś)^+0.5, type-specific rate) on the shift@2.5 skeleton, marker-program version.',
    'Tools: t1_rewrite script family, veckit.',
    'Issues: 48.80 ties shift@2.5 (48.85) — de/vario slightly lower, dir/mmd slightly higher; per-program momentum does not beat the global damp.',
    'Conclusion: per-program momentum does not beat global damp; stage-C probe closed.']),
 'mix20e85': ('mix20 + E8.5 carrier mixture', [
    'Method: a submission mixing 80% E9.5 prediction with 20% original E8.5 cells.',
    'Tools: veckit, ledger.',
    'Issues: 46.37 below the measured floor 46.84 and shift@2.5 (48.85).',
    'Conclusion: mixing in old-stage cells reduces distribution fit; closed.']),
 'copylast': ('copy_last (copy previous stage, floor probe)', [
    'Method: copy the E9.5 expression directly as the prediction (5118-cell sample).',
    'Tools: veckit, ledger.',
    'Issues: measured floor 46.84 (09-16 build) is 0.10 above the early L4 probe 46.74; uploading the same file twice burned quota (21:44 and 21:45 identical scores).',
    'Conclusion: measured floor = 46.84, official floor = 50 (the official scale fixes the floor at 50); copy_last is the zero-information baseline every method must be compared against.']),
 'sel': ('sel selection family (selday/selpc1/selanti)', [
    'Method: generate by "selection" logic — selday (select by developmental day proportion), selpc1 (select by PC1), selanti (anti-selection), proportion f∈{20,30,40,50}%.',
    'Tools: T1 generator script family, veckit.',
    'Issues: the whole family collapses — selpc1_f20 30.21 is the lowest score of the whole journey (mmd 15.7/vario 19.6 double collapse); selday only exceeds the floor at f50 (47.02) but still below shift@2.5; selanti_f50 42.66 (mmd 37.2 weak).',
    'Conclusion: generating by hand-made "selection rules" is the wrong direction; the family is closed.']),
 'dir': ('dir24 / dirprop (direction class)', [
    'Method: resample by 24 direction classes (dir24) or direction proportions (dirprop B family), k∈{2000,3000}.',
    'Tools: T1 generator script family, veckit.',
    'Issues: dir24_k2000_s100 and dirprop_B_k2000 are identical metric-by-metric (47.19/44.2/53.1/49.2/40.4), likely the same file renamed and re-uploaded; the k3000 variant has weaker vario 37.8.',
    'Conclusion: direction-class resampling gets the family-highest de 44.2 but vario 40.4 drags it down; family peak 47.19, does not break the floor; closed.']),
 'robust': ('robust_consensus (robust consensus)', [
    'Method: multi-candidate robust consensus + damp 0.45 drift.',
    'Tools: T1 generator script family, veckit.',
    'Issues: 47.94 exceeds the measured floor 46.84 but not shift@2.5 (48.85); de 40.1 weak.',
    'Conclusion: robust consensus only stabilizes the distribution metrics (mmd 49.8/vario 48.6) and cannot lift de; closed.']),
 'ancestor': ('ancestor_donor_birth (ancestor–donor birth mixture)', [
    'Method: ancestor cells × donor birth mixture (10% mixing ratio).',
    'Tools: T1 generator script family, veckit.',
    'Issues: 46.74, marginally below the measured floor 46.84 (−0.10); re-uploading the same file burned one quota (04:35 and 04:46 identical metrics).',
    'Conclusion: 10% birth mixture gives no gain; closed.']),
 'mommask': ('momentum mask', [
    'Method: on the shift skeleton, use a momentum mask α=0.01 to limit the generation amplitude (drift only applied to genes/cell types with significant momentum).',
    'Tools: T1 generator script family, veckit.',
    'Issues: de 43.8/dir 53.6/mmd 50.8 slightly below shift@2.5, but variogram 49.5 jumps +15.4 over shift@2.5 (34.1), total 49.49 beats 48.85 (+0.64).',
    'Conclusion: T1 first breaks 49. Lesson: **masking the amplitude preserves the variogram structure** — more effective than blindly raising damp.']),
 'mm': ('mm (library-size normalization)', [
    'Method: the mm generator normalizes library size in log1p space so the median library size aligns to 10000 (matching the reference E9.5 base exact 10000); n=1249 sampling, b=0.70.',
    'Tools: T1 generator script family, veckit.',
    'Issues: mm_n1249_b070 49.93, only 0.07 from the official floor 50; mmd 52.2/vario 50.7 both pass, de 43.1 still weak.',
    'Conclusion: library-size normalization is a necessary baseline fix (no effect on de ranking, but preserves the distribution); mm brings the distribution metrics to pass level — 50 is one step away.']),
 'covsafe': ('covsafe (covariance safeguarding, deepgen line)', [
    'Method: on the mm family (library-size-normalized generator) add covariance safeguarding (l=25, the strength parameter protecting gene–gene covariance).',
    'Tools: deepgen_t1 candidate pipeline, check_submission.py, veckit, real-board backfill.',
    'Issues: real board 48.09 below the production reference shift@2.5 (48.85, −0.76) — only variogram improves (+16.3) while de/dir/mmd all drop; attribution: local covariance preservation is insufficient and the residual direction is miscalibrated for E10.5.',
    'Conclusion: **preserving structure cannot replace a correct future-stage transition direction**; covsafe is closed, no l10/l50 variants uploaded.']),
 'vs': ('vs (variance amplification)', [
    'Method: variance amplification — multiply the deviation of the K most-variable genes in the E9.5 carrier by coefficient c and write back (vs200=K200, vs500=K500; c15/c135/c165 = coefficients 1.5/1.35/1.65), touching only covariance, not pseudobulk; vs_kp6_a030_n1249 is vs × knowledge-program kp6 (knowledge shift a=0.30, n=1249); direction check: 3 seeds × 25 groups = 75 points, all positive.',
    'Tools: tools/_t1_vs_make.py, veckit.',
    'Issues: vs200_c165 50.52 first breaks the official floor 50 (mmd 55.7, then a new high); vs500_c135 only 50.01 (de 40.9 weak); vs_kp6_a030_n1249 50.67 keeps refreshing.',
    'Conclusion: the vs family is T1\'s turning point past 50 — variance amplification (moving covariance) is closer to the real developmental variance structure than pure global drift; family peak 50.67.']),
 'otf3': ('otf3 (otfix: OT direction + mask + tiny amplitude)', [
    'Method: otfix — OT-mixture direction + mask + tiny amplitude (n=2500, om2 masked variant; a local independent-truth subset once showed all four axes better).',
    'Tools: tools/_t1_otf3_robust.py, veckit.',
    'Issues: 47.09 below the official floor 50 and mm_n1249_b070 (49.93); all four axes worse than the mm family (weighted −2.87 vs actual −2.84) — direct evidence that the T1 local proxy is unusable (locally all four axes looked better).',
    'Conclusion: the OT-flow variant does not beat the vs family; closed.']),
 'statepop': ('state_population_dynamics (state population dynamics)', [
    'Method: two-component dynamics (implementation in baselines/t1_state_population_dynamics.py module docstring): ① type-level birth/death momentum — estimate momentum from the E8.5→E9.5 composition change and conservatively extrapolate one step, sampling the carrier from the extrapolated population (not by natural E9.5 proportions); ② state dynamics — assign each gene to an expression program (cardiac/endodermal/neural_crest/mesodermal/vascular, five programs), modulate the type velocity by how far each carrier cell\'s state deviates from its type centroid, and give explicit birth-state velocities to new E9.5 types (E9.5 residuals kept in the carrier). Uses only published E8.5/E9.5 data; no hidden-stage input.',
    'Tools: baselines/t1_state_population_dynamics.py, veckit.',
    'Issues: 47.93 below the official floor 50; de 43.0 above otf3 but still weak, vario 41.6 weak.',
    'Conclusion: the dynamics-modeling direction is right but the implementation does not pass the line; closed.']),
 'kp': ('kp family (knowledge-program shift + variance amplification / maturity weighting)', [
    'Method: two mechanisms stacked: A = knowledge-program shift — textbook developmental programs enumerating 10 programs / 271 genes (imprinting/neural/ECM/pluripotency/ribosomal/glycolysis/stress/epithelial etc.; the program list is developmental-biology domain knowledge with no single URL), add a shift to pseudobulk (a∈{0.15,0.25,0.35}; u=uniform / w=weighted by program hits); B = variance amplification — multiply the deviation of the K=500 most-variable genes by c=1.5 (b500c15 means K=500, c=1.5; n=2000 sampling). Variants: kp2/3/4/5 are mechanism-combination indices and ablations (raw=raw input, wo=no weighting, aonly=A only); kp7_m is the maturity-weighting variant (m mechanism + maturity index b=0.50, b=0.00 as control). Key design decision: biological knowledge should be used to "select the program gene set" rather than shift genes one by one.',
    'Tools: tools/_t1_kp_make.py, _t1_kp_make3.py, check_submission.py, veckit, real-board backfill.',
    'Issues: ① kp probe kp_a015u only 48.88; ② all raw variants fail (kp5_kw/kp4_so/kp2_raw/kp3_w_raw all 47–48, vario 46.6 collapse); ③ aonly_raw without the b500c15 component drops all three lines (47.37); ④ wo variant 51.91 does not beat the w full pipeline; ⑤ kp7_m_b000 control 51.37, 2.3 below b050 (53.67) (de −4.1/dir −3.2/mmd −1.7) — b=0.50 is the key parameter; ⑥ kp3_w_a025_b500c15_n2000 52.18 once set the T1 best (dir/mmd/vario all pass).',
    'Conclusion: kp7_m_b050_n2000 = **53.67** (rank 93/254, de 44.2 breaks the 42 bottleneck / dir 57.6 / mmd 57.6 / vario 54.7, four new highs), current T1 best. kp7 maturity weighting was once rejected by a 500-panel OOF, but the 32285-panel real board gives +2.30 — small-panel OOF conclusions do not generalize to the full panel.']),
 'e4c': ('E4c pending candidates (lineage Δ / momentum)', [
    'Method: E4c-lineage Δ (masked-A ancestor mixture, no resampling); E4c-mom type-specific rate r∝(s/ś)^+0.5 (momentum).',
    'Tools: t1_rewrite script family.',
    'Issues: not yet regenerated under the label-free format gate; the local profile looks like a copy_last artifact.',
    'Conclusion: pending state — not uploaded, not scored.']),
}

T3_EN = {
 'transfer': ('transfer (global Δ perturbation transfer)', [
    'Method: add the global response Δ learned from E9.5 WT→Mab21l2 KO (mean KO − WT expression difference) to the E8.75 carrier (damp 1.0/1.5).',
    'Tools: baselines/t3_shift_transfer.py, veckit.',
    'Issues: damp1.5 real board 40.98 — variogram collapses 49.8→12.2; damp1.0 was never successfully submitted (no such file on the portal).',
    'Conclusion: **global Δ destroys the distribution**: the KO response cannot be applied as a global scalar shift; the transfer family is closed.']),
 'wt': ('wt_identity (floor probe)', [
    'Method: copy the WT expression directly as the prediction (E8.75 carrier + WT distribution).',
    'Tools: baselines/t3_wt_identity.py (wt_identity is the official baseline definition, https://virtualembryo.ai/challenge/baselines), veckit.',
    'Conclusion: T3 measured floor = 45.81, official floor scale = 50; every method is first compared against this.']),
 'cardiac': ('cardiac (lineage-restricted transfer)', [
    'Method: apply the global Δ only to cardiac-lineage cells (lineage-restricted version).',
    'Tools: baselines/t3_shift_transfer.py, veckit.',
    'Issues: damp0.5 44.36 / damp0.25 44.85 — distribution metrics hold (mmd 48.8/49.8) but de drops to 37.4/37.7 (KO effect cannot be expressed).',
    'Conclusion: lineage restriction protects the distribution but loses the effect; closed.']),
 'state': ('Gata4 state program (a25/a35/a50)', [
    'Method: E8.75 carrier 10pct + within-type normalization + Gata4 state program (a coefficients 0.25/0.35/0.50).',
    'Tools: t3_rewrite script family, veckit.',
    'Issues: the three variants score 45.78/45.79/45.80, tied with the floor (+0.00) — the state program produces no KO response.',
    'Conclusion: three consecutive uploads each burn a quota with zero gain; closed.']),
 'mix': ('mix (KO-mixture inference)', [
    'Method: construct the prediction as a mixture of "real KO cells + WT carrier" — mix ratio p∈{20,30,40,50,60,70}% (p% KO cells + (100−p)% WT carrier; p is the KO cell fraction); kofeat variants feed a Gata4 target-gene feature list (feat∈{0.05,0.1,0.2,0.35}, measured: larger amplitude monotonically worse); muld_m05 is the mix70 amplitude variant; cardiac/knn are lineage and nearest-neighbor variants.',
    'Tools: T3 generator script family (mix series), veckit.',
    'Issues: ① mix40_early 50.09 (+0.09) — mixing an early carrier gives almost nothing; ② cardiac/knn variants (59.72/61.82) lose to the original mix40_ko 63.58; ③ kofeat variants 64.06–64.52, smaller feat closer to the peak; ④ muld_m05 64.39 (sev 92.9 then-new high but mmd 50.4 drags); ⑤ mix70_ko 64.60 family peak, severity_slope 92.3 then-new high; ⑥ re-uploading mix70_ko (same file, 64.60 unchanged) burned quota.',
    'Conclusion: higher mix ratio gives higher sev (mix70 sev 92.3); family peak 64.60. Mixing real cells buys mmd but sev cannot climb — "mix more" is not the main lever.']),
 'kodir': ('kodir (KO direction)', [
    'Method: construct the response along the KO direction (a=0.10).',
    'Tools: T3 generator script family, veckit.',
    'Issues: 43.96 below the floor, variogram 18.1 collapse.',
    'Conclusion: direction construction destroys the distribution; closed.']),
 'ko2': ('ko2 (KO dual-path)', [
    'Method: dual-path KO response construction, n∈{5000,6000}, b=0.60.',
    'Tools: T3 generator script family, veckit.',
    'Issues: 64.68 (n6000) / 64.75 (n5000), not above cmp_n6000_b070 (64.93).',
    'Conclusion: ko2 is cmp\'s predecessor but does not fully express the KO effect; closed.']),
 'koq': ('koq (KO quantized)', [
    'Method: quantized KO response construction (n=5000).',
    'Tools: T3 generator script family, veckit.',
    'Issues: 58.04 — mmd 24.8/vario 27.1 double collapse.',
    'Conclusion: the koq line fails; closed.']),
 'pkctl': ('pk/ctl (26-gene per-gene transforms)', [
    'Method: pk26g18 (26 program genes, g=18 variant) / ctlp26 (control 26 genes) — apply per-gene transforms to the named genes only, leave the rest untouched; belongs to the T3 per-gene transform family (pk/ctlp/koq/kodir/mx50amp, variogram 5/5 collapse to 10.8–27.1).',
    'Tools: T3 generator script family, veckit.',
    'Issues: pk26g18 38.91 (mmd 21.4/vario 10.8 double collapse); ctlp26 43.14 (mmd 7.9/vario 19.4 double collapse).',
    'Conclusion: none of the nine per-gene transform routes on T3 survives; the 26-gene program family is shut down.']),
 'mx50amp': ('mx50amp (50% mixture + amplitude)', [
    'Method: 50% mixture (mx50) + amplitude 0.92 (amp) construction — apply a transform of amplitude 0.92 along the KO-response direction; belongs to the T3 per-gene/amplitude transform family (variogram 5/5 collapse to 10.8–27.1).',
    'Tools: tools/_t3_mx50_amp.py, veckit.',
    'Issues: 57.15 — severity_slope 90.6 high but variogram 15.8 collapse.',
    'Conclusion: amplitude construction destroys vario; closed.']),
 'cmp': ('cmp (celltype^β resampling)', [
    'Method: cmp = resample by cell type (celltype^β exponential flattening of the type distribution, β=0.70/0.55/1.00, n=6000; β=1.00 is the natural type proportion, β<1 compresses the celltype distribution).',
    'Tools: T3 generator script family (cmp series), veckit.',
    'Issues: ① cmp_n6000_b070 64.93 breaks the 64.6 plateau (de 56.3/sev 97.0 jump, mmd/vario each drop ≈10); ② b=1.00 63.35, all five metrics below b070; ③ b=0.55 65.31 (de 56.3 flat, dir 60.3/sev 97.1 up, mmd/vario both up) — the low-β side is better; larger β is worse (slope ≈ −5.3 points per unit β).',
    'Conclusion: cmp_n6000_b055 = 65.31; **compressing the celltype distribution (β<1) is the core T3 gain**.']),
 'cmpw': ('cmpw (KO pool + E8.75 WT carrier dilution)', [
    'Method: cmpw = flat KO pool from cmp_b070 diluted with the E8.75 WT carrier — 70% KO pool (β=0.70) + 30% carrier, k = carrier fraction (k=1.00 is cmp_b070 itself, k50–k85 the dilution series; n=6000).',
    'Tools: tools/_t3_cmpw_make.py, _t3_cmpw_axes2.py, veckit.',
    'Issues: cmpw_n6000_k70 65.49 beats cmp_b055 (+0.18): de 54.8 (−1.5)/sev 92.4 (−4.7) give way, mmd 55.2 (+11.0)/vario 53.9 (+6.8) jump.',
    'Conclusion: carrier dilution redeems the distribution axes (mmd/vario) but pays a sev cost (≈4.6 points, confirmed on two independent paths); cmpw is transitional, the kb family completes sev on top of it.']),
 'pw': ('pw (prior weighting, falsified)', [
    'Method: pw = prior weighting — additive weighting on cmp along the prior axis (cell-type variance axis) (p=0.50/1.00, n=6000); root cause: treated "additive perturbation dp→dp+Δ" as "constant scaling dp→c·dp" (rank invariance only protects the latter); measured |d(pb)|=0.0414 is the additive term.',
    'Tools: T3 generator script family (pw series), veckit.',
    'Issues: pw050 64.47 (mmd/vario above cmp but de 54.8/dir 58.1 slightly lower, not above 64.93); pw100 62.87 (de/dir lower) — monotonically decreasing in β 0→0.5→1.0.',
    'Conclusion: prior weighting is net-negative (monotone in β), falsified; on T3 any operation that deviates from the natural KO-cell distribution weakens de.']),
 'prw': ('prw (official population_reweight + GSE prior)', [
    'Method: prw = official population_reweight operator: resample the WT carrier with a WT-vs-KO classifier (this operator cannot produce a strong enough response in principle) + GSE external prior (s=0.10, 1.2MB small model; the GSE208162 prior is orthogonal to the Mab21l2 response: 48/267 in the DE set = random expectation).',
    'Tools: tools/_gse_cells_make.py, _t3_gse_prior.py, veckit; GSE208162 external prior data (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208162).',
    'Issues: 54.49 — severity_slope 70.6 far below cmp\'s 97.0 (KO effect not expressed); de 44.9/dir 51.3 weak; mmd 53.1/vario 51.9 distribution fidelity achieved.',
    'Conclusion: distribution preserved but the effect cannot be expressed (sev 70.6 vs cmp 97.0); external prior direction alignment does not predict the score; closed.']),
 'kb': ('kb (real WT dilution of KO, A/B falsification re-check)', [
    'Method: kb = dilute KO with real WT cells (kbgen: flat KO pool + WT carrier dilution, k=65/75 dilution ratios, n=6000; kbb is the kb6000×b055 combination k=65, b=0.55); a local A/B half-split experiment once judged it "universally worse than doing nothing, the advantage is self-justifying", but the re-check found that falsification used two already-falsified local axes + a wrong carrier recipe (the kb carrier wrongly used E9.5 WT; the true-value carrier is reverse-engineered through Gata4 means as E8.75 WT), so it does not constitute a counter-argument to the real-board scores (66.36/66.61).',
    'Tools: tools/_t3_kbgen.py, _t3_kb_ab.py, veckit.',
    'Issues: ① kb6000_k65 66.36 beats cmpw (de 56.3/dir 62.2 new dir high/sev 97.9 new sev high/mmd 45.0/vario 50.5); ② kbb_n6000_b055_k65 66.61: de/dir flat, sev 98.0/mmd 46.1/vario 51.8 all up; ③ kb6000_k75 65.32, all five metrics down (vario −3.0) — k=65 is optimal.',
    'Conclusion: **kbb_n6000_b055_k65 = 66.61** (rank 48/187), current T3 best. Dilution ratio k=65 + β=0.55 is optimal; k=75 is the wrong direction.']),
}
T2E_EN = {
 'v1': ('v1 (single-nearest-neighbor log-linear normalization + paired geometry)', [
    'Method: train on the E8.0 carrier, learn kNN pairs (k=1) from E7.25→E8.0, apply log-linear normalized interpolation + paired geometry (coordinates translated with the pair) to generate intermediate-stage predictions.',
    'Tools: t2 generator script family, t2_data_contract.py, veckit.',
    'Issues: 59.00 (95/152) as the starting baseline; geometric pairing only moves nearest neighbors, poor state continuity.',
    'Conclusion: v1 is the first T2-embryo version, 59.00 above the floor 50; later families stack different mechanisms on top.']),
 'mixbrkt': ('mix_brkt (mixture + bracket)', [
    'Method: mix real carriers + bracket constraint (only type transitions among E6.75/E7.25/E8.0 allowed), then add paired generation.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 59.07, only 0.07 above v1 — d2_shape 26.3/occupancy_dice 19.0 weak (insufficient coordinate generation); scale 73.0 also drags.',
    'Conclusion: the bracket constraint keeps de 57.0 but spatial metrics are poor; a transition from v1 to bgm.']),
 'bgm': ('bgm (background mixture generation)', [
    'Method: bgm = overlay "background program mixture" on the carrier to generate intermediate states (the f=0.15 variant controls mixture strength).',
    'Tools: t2 generator script family, veckit.',
    'Issues: bgm 62.94 beats mix_brkt (+3.87) — dir 70.6/mmd 68.7/vario 67.3 all lead, d2 49.2/occ 41.0 weak; the f0.15 variant 57.97 is even lower.',
    'Conclusion: bgm is the first 62+ plateau on embryo interp; d2/occ remain the short board.']),
 'v1rep': ('v1replica (v1 replica)', [
    'Method: strict v1 replica (controlled variable).',
    'Tools: t2 generator script family, veckit.',
    'Issues: 56.99, inconsistent with v1\'s 59.00 (different sampling) — a typical case of local vs real-board ranking disagreement.',
    'Conclusion: the controlled replica confirms the v1 baseline range ≈57–59.']),
 'gps': ('gps33 (Gaussian process interpolation)', [
    'Method: Gaussian process regression interpolation on paired cells (33 gene modules gps33 / n=583 downsampled variant), outputting intermediate-state expression.',
    'Tools: t2 generator script family (gps series), veckit.',
    'Issues: gps33 62.37 < bgm 62.94 (d2 55.6 better but scale 88.9 drags); gps33n583 61.36 (de 58.2, the board\'s strongest tier, but overall lower); gps33s 63.19 — same metrics as gps33 except scale 88.9→98.7 (+9.8), total +0.82.',
    'Conclusion: **scale_log_ratio is a cheap high-score item**: calibrating library size to the reference scale gains 0.8+ points for free; gps33s = 63.19.']),
 'tls': ('tls2n5000 (type-level global shift)', [
    'Method: type-level global shift — shift expression uniformly within each cell type (n=5000); the real board shows nh +7.8 success but d2 −31.8/occ −27.9 cancel it out.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 59.01 — d2_shape 23.8/occupancy_dice 17.6 collapse (type-level shift destroys inter-type relative positions); once mistakenly uploaded to the T1 panel and rejected (32285 vs 498).',
    'Conclusion: type-level global shift destroys spatial metrics; closed.']),
 'gpsnnu': ('gpsnnu (geometric inheritance + nearest-neighbor uniquification)', [
    'Method: gps-family nnu variant — switch the expression source: geometric inheritance + nearest-neighbor uniquification (drop the constrained pairing, inherit expression from geometric nearest neighbors); the local nh proxy once hit 62.4 precisely, the real board shows mmd −7.0/vario −13.4 eating the gain.',
    'Tools: tools/_t2_gpsnn.py, _t2_gpsnn_u.py, veckit.',
    'Issues: 61.81 < gps33s 63.19 — d2 55.6 same tier as gps33s but de 53.5/mmd 61.6/vario 53.4 weaker.',
    'Conclusion: the unconstrained version loses gps\'s distribution advantage; closed.']),
 'cpf': ('cpf015r5k (homologous pairing + positional interpolation)', [
    'Method: cpf = homologous-pair construction: homologous pairing + positional interpolation pos_f=0.15 + scale correction (r variant anchor 200.88; n=5000 sampling, the 5k version resampled under the 583–5000 cell cap after cpf015r was rejected for exceeding it; local prediction +2.4~2.5).',
    'Tools: tools/_cpf005_probe.py, check_submission.py, veckit.',
    'Issues: the original cpf015r at 9000 cells was rejected for exceeding the board cap; cpf015r5k 65.31 — de 55.8/dir 70.6/mmd 68.8/vario 67.1/d2 56.1 all lead, occ 43.4 slightly weak.',
    'Conclusion: **cpf015r5k = 65.31** (65/200), current T2-embryo-interp best. d2_shape/occupancy_dice are the main remaining improvement room.']),
 'vlk8': ('vlK8 (variance amplification K=8)', [
    'Method: vlK8 = variance-amplification variant (amplify the K=8 highest-variance genes by coefficient c=1.25); highly isomorphic with cpf015r5k, the only variable is variance amplification — on T1 this lever is worth +3.5 (3 real-board points), on T2 it is negative (the gain is halved or worse while nh cost is paid in full).',
    'Tools: t2 generator script family, veckit.',
    'Issues: 64.75 — highly isomorphic with cpf015r5k (dir/mmd/vario/d2/occ/scale almost identical), the gap is de 55.2 (−0.6)/mmd 67.1 (−1.7)/nh 63.4 (−0.9).',
    'Conclusion: vlK8c125 64.75 is cpf\'s near-relative plateau, not above 65.31; variance amplification does not transfer to T2; closed.']),
 'vg': ('vg_ourmixs (v1 paired displacement-field transplant)', [
    'Method: vg_ourmixs = change the geometry: transplant v1\'s paired displacement field onto the mixture expression; nh collapses 57.8→41.5 (weighted −4.10).',
    'Tools: t2 generator script family, veckit.',
    'Issues: 55.93 — scale 98.7 strong but d2 52.8/occ 48.2/nh 41.5 weak, below bgm 62.94.',
    'Conclusion: geometric transplant destroys nh; closed.']),
}

T2H_EN = {
 'v1': ('v1 (type stratification + global pairing)', [
    'Method: stratify by cell type, within-type global pairing interpolation from E8.25→E8.75 (log-linear normalization + paired geometry).',
    'Tools: t2 generator script family, t2_data_contract.py, veckit.',
    'Issues: 61.86 (74/148) — heart-interp first version baseline; the 500 vs 498 gene-panel trap (rejected once for missing Casp4/Pnliprp1).',
    'Conclusion: v1 is the heart-interp starting point 61.9; the panel must be element-wise aligned to the official 500 genes.']),
 'mixbrkt': ('mix_brkt / mix_brkts (mixture + bracket + scale)', [
    'Method: mix real carriers (E8.25/E8.75) + bracket type constraint + paired generation; mix_brkts additionally calibrates library-size scale (scale_log_ratio 71.1→100.0 full marks).',
    'Tools: t2 generator script family, veckit.',
    'Issues: mix_brkt 62.6 and mix_brkts are identical metric-by-metric except scale (de 52.1/dir 55.7/mmd 50.7/vario 34.7/d2 42.2/occ 54.4/nh 50.8); full-mark scale contributes ≈ +2.4.',
    'Conclusion: **mix_brkts = 65.01** (54/191), current heart-interp best; scale_log_ratio from 71.1 to 100.0 full marks lifts the total by ≈ +2.4.']),
 'gps50': ('gps50n1185 (Gaussian process)', [
    'Method: Gaussian process interpolation (n=1185).',
    'Tools: t2 generator script family, veckit.',
    'Issues: 50.2, tied with the floor — the gps variant on heart interp is clearly weaker than on the embryo board.',
    'Conclusion: gps is unsuitable for heart interp; closed.']),
 'v1g2000': ('v1g2000s (hand-replicated v1 geometry)', [
    'Method: v1g = hand-replicated v1 geometry (replica of v1\'s paired displacement field, n=2000); the replication is incomplete — d2 only 48.7 (v1 original 88.1).',
    'Tools: t2 generator script family, veckit.',
    'Issues: 60.0 — the geometric-constraint variant is below v1 (61.9) and mix_brkts (65.01); d2 48.7 far below v1\'s 88.1.',
    'Conclusion: v1-geometry replication is incomplete (the v1 original is no longer available locally); closed.']),
 'v1geom': ('v1geom5000s (v1 geometry variant)', [
    'Method: v1 geometry variant (n=5000; the v1 original is no longer local, coordinates actually come from another coordinate set of v1replicas); the real-board d2 46.2 proves v1\'s geometry is not preserved in any local file.',
    'Tools: tools/_t2hi_v1geo.py, veckit.',
    'Issues: 53.12 — vario 37.6 collapse (geometric transformation breaks the expression distribution); scale 100.0 full marks.',
    'Conclusion: large geometric sampling amplitude destroys vario; the whole v1 line is closed.']),
 'v1vc': ('v1vc100 (v1 + variance control, proxy-extrapolation falsification)', [
    'Method: v1 + variance control (vc=100, coordinates from v1replicas rather than the v1 original); mistake A: the local nh proxy reading 0.00852 falls outside the four-point calibration interval [0.04217, 0.13902], the reported "62.04" was a linear extrapolation of the left segment (measured 50.8, error +11.24); mistake B: cited a real-board d2=88.1 analogy from the v1 original that does not exist locally (measured 42.2, 46 points off).',
    'Tools: tools/_heart_vc_sweep.py, veckit.',
    'Issues: 53.61 — vario 34.7 weak; d2 42.2 (−38.3, largest single-axis loss); net −11.40 vs mix_brkts 65.01.',
    'Conclusion: **a proxy reading must first fall inside the calibration interval**; the whole v1 line is closed (v1vc100/v1geom5000s/v1g2000s/gps50n1185).']),
}
T2X_EN = {
 'v1': ('v1 early candidate', [
    'Method: early candidate (09-04 first version, no version suffix).',
    'Tools: t2 generator script family, veckit.',
    'Issues: starts at 46.4, below the floor 50.',
    'Conclusion: extrap-board starting point; explored step by step.']),
 'v3': ('v3 (shrinkage type trend + uniform carrier + coordinate amplification)', [
    'Method: confidence-shrinkage type trend damp0.75 + uniform E9.5 carrier + coordinates ×1.31.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 48.71 (mmd 33.6 largest loss, scale 100 full marks); the same file was double-uploaded on 09-06 and re-uploaded a third time on 09-14 (historical record — never upload again).',
    'Conclusion: coordinate amplification + shrinkage trend is the wrong direction; the v3 family is closed.']),
 'v4': ('v4 population_growth (population growth projection)', [
    'Method: E9.5 carrier + population-growth amplitude projection.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 49.26 — d2_shape 30.6 largest loss; de 52.8 the family\'s highest, scale 100 full marks, but the total still below the floor 50.',
    'Conclusion: population-growth projection fails to move morphology; v4 closed.']),
 'v2ga6': ('v2ga6 (geometric amplitude)', [
    'Method: v2 geometric amplitude a=6.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 53.6, close to the floor but does not break it.',
    'Conclusion: geometric amplitude does not break 50; closed.']),
 'v4a10': ('v4a10 (growth amplitude 10)', [
    'Method: population-growth amplitude 10.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 50.1, marginally above the floor.',
    'Conclusion: growth-amplitude tuning gains almost nothing; closed.']),
 'r6': ('r6b70a20 (morphology extrapolation)', [
    'Method: morphology extrapolation r6 (b=0.70, a=0.20 morphology/geometry amplitudes).',
    'Tools: t2 generator script family, veckit.',
    'Issues: 38.97 — morphology extrapolation is heavily penalized.',
    'Conclusion: changing morphology is heavily penalized (38.97, d2 11.9 collapse) — the first morphology-line falsification point on the extrap board.']),
 'compc100': ('comp_c100 (composition + morphology)', [
    'Method: composition mixture + morphology transform (c=100).',
    'Tools: t2 generator script family, veckit.',
    'Issues: 32.8 — the lowest score of the whole journey, the worst morphology-line falsification point.',
    'Conclusion: morphology transforms are irreversible; closed.']),
 'vmorph': ('vmorph_s120 (virtual morphology)', [
    'Method: virtual morphology transform s=120.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 46.8 — geometric metrics such as d2 are penalized.',
    'Conclusion: the virtual-morphology route fails; closed.']),
 'scaleonly': ('scale_only (scale adjustment only)', [
    'Method: adjust only library size/composition toward the extrapolation-target-stage proportions, coordinates and morphology completely untouched (scale_log_ratio calibrated to 100 full marks).',
    'Tools: t2 generator script family (scale series), veckit.',
    'Issues: 54.51, current extrap best (68/185) — scale full marks 100, balanced metrics (de 46.8/dir 49.8/mmd 50.5/vario 50.1/d2 49.9/occ 54.1/nh 51.1).',
    'Conclusion: **moving only scale/composition, not morphology**, is the only correct route on the extrap board.']),
 'mix20scale': ('mix20_scale (mixture + scale)', [
    'Method: 20% mixture + scale calibration.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 53.9, below scale_only 54.51.',
    'Conclusion: mixing adds no points; closed.']),
 'compw30': ('compw30_scale (composition weighting + scale)', [
    'Method: 30% composition weighting + scale.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 53.7, below scale_only.',
    'Conclusion: composition weighting adds no points; closed.']),
 'w005': ('w005 (minimal displacement 0.05 along the scale_only end)', [
    'Method: w005 = minimal displacement along the scale_only end (displacement amplitude 0.05): move only a tiny amount of coordinate displacement, keep the de/dir-end advantage, leave a little room for distribution improvement (alternatives w010 = displacement 0.10, wk20/wk50 = move only 20–50 genes for distribution fine-tuning).',
    'Tools: t2 generator script family, veckit.',
    'Issues: 54.43 (rank 72/204) — de 46.8/dir 49.8/mmd 50.5/vario 50.1/d2 49.9/occ 54.1/scale 100/nh 51.1, a balanced runner-up, only 0.08 from scale_only 54.51.',
    'Conclusion: the balanced variant is close to scale_only but does not beat it; w005 = 54.43, second highest.']),
 'selday': ('selday (selection day, closed)', [
    'Method: selday family — select cells by developmental day (selday30/50_scale), apply 30%/50% day selection to the E9.5 carrier then scale-adjust only.',
    'Tools: t2 generator script family, veckit.',
    'Issues: 27.54 / 28.9 — the lowest scores of the whole journey (mmd/vario/d2/occ all collapse); day selection destroys the E9.5 cell composition.',
    'Conclusion: day selection is useless for extrap; formally closed.']),
 'cpfx': ('cpfx (type-level displacement shift extrapolation)', [
    'Method: cpfx = cpf-family extrapolation variant: expression unchanged, coordinates displaced at the type level (n=8000, a=0.10); d2_distance normalizes and compares pairwise distance distributions — rigid scaling does not change shape, translation changes inter-type relative positions — d2 collapses to 5.7.',
    'Tools: tools/_heart_extrap_cpfx.py, veckit.',
    'Issues: 52.12 — d2_shape 5.7 collapse (morphology extrapolation heavily penalized); occupancy_dice 42.0.',
    'Conclusion: conditional-flow extrapolation moving morphology dies the same way; the fourth morphology-line falsification — all morphology routes on the extrap board are closed.']),
}

# ---------- 汇总行 ----------
SUMM = {
 'T1_val': [('当前最佳','53.67'),('官方地板行 (copy_last / wt_identity)','50'),('实测地板上传（本队）','46.84'),('全榜最高（榜首）','68.7')],
 'T2_embryo_interp': [('当前最佳','65.31'),('官方地板行 (copy_last / wt_identity)','50'),('全榜最高（榜首）','75.6')],
 'T2_heart_interp': [('当前最佳','65.01'),('官方地板行 (copy_last / wt_identity)','50'),('全榜最高（榜首）','73.4')],
 'T2_heart_extrap': [('当前最佳','54.51'),('官方地板行 (copy_last / wt_identity)','50'),('全榜最高（榜首）','60.5')],
 'T3_gata4': [('当前最佳','66.61'),('官方地板行 (copy_last / wt_identity)','50'),('实测地板上传（本队）','45.81'),('全榜最高（榜首）','75.2')],
}
SUMM_EN = {
 'T1_val': [('Current best','53.67'),('Official floor (copy_last / wt_identity)','50'),('Measured floor (our upload)','46.84'),('Board top (leader)','68.7')],
 'T2_embryo_interp': [('Current best','65.31'),('Official floor (copy_last / wt_identity)','50'),('Board top (leader)','75.6')],
 'T2_heart_interp': [('Current best','65.01'),('Official floor (copy_last / wt_identity)','50'),('Board top (leader)','73.4')],
 'T2_heart_extrap': [('Current best','54.51'),('Official floor (copy_last / wt_identity)','50'),('Board top (leader)','60.5')],
 'T3_gata4': [('Current best','66.61'),('Official floor (copy_last / wt_identity)','50'),('Measured floor (our upload)','45.81'),('Board top (leader)','75.2')],
}
L10N = {
 'zh': {
   'overview': '## 实验总览（按时间线，具体技术序列）', 'records': '## 实验记录（按方法族分组）',
   'family': '### 实验族：', 'other': '### 实验族：其他（未归类提交，保持完整记录）',
   'detail': '**提交明细（全部效果，时间 UTC）**', 'summary': '## 汇总行',
   'hdr_t1': '| 日期 | 版本 | 方法（文件） | 总分 | de | dir | mmd | vario | rank | 备注 |',
   'hdr_t2': '| 日期 | 版本 | 方法（文件） | 总分 | de | dir | mmd | vario | d2 | occ | scale | nh | rank | 备注 |',
   'hdr_t3': '| 日期 | 版本 | 方法（文件） | 总分 | de | dir | sev | mmd | vario | rank | 备注 |',
   'sep_t1': '|---|---|---|---|---|---|---|---|---|---|',
   'sep_t2': '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|',
   'sep_t3': '|---|---|---|---|---|---|---|---|---|---|---|',
 },
 'en': {
   'overview': '## Experiment overview (chronological concrete technique sequence)', 'records': '## Experiment log (grouped by method family)',
   'family': '### Experiment family: ', 'other': '### Experiment family: other (unclassified submissions, full record kept)',
   'detail': '**Submission log (all results, UTC)**', 'summary': '## Summary rows',
   'hdr_t1': '| Date | Version | Method (file) | Total | de | dir | mmd | vario | rank | Notes |',
   'hdr_t2': '| Date | Version | Method (file) | Total | de | dir | mmd | vario | d2 | occ | scale | nh | rank | Notes |',
   'hdr_t3': '| Date | Version | Method (file) | Total | de | dir | sev | mmd | vario | rank | Notes |',
   'sep_t1': '|---|---|---|---|---|---|---|---|---|---|',
   'sep_t2': '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|',
   'sep_t3': '|---|---|---|---|---|---|---|---|---|---|---|',
 },
}
# 汇总行也放进族输出
def build_summary_lines(sheet, lang):
    s = SUMM if lang == 'zh' else SUMM_EN
    return ['- **%s**：%s' % (k, v) for k, v in s.get(sheet, [])] if lang == 'zh' else ['- **%s**: %s' % (k, v) for k, v in s.get(sheet, [])]

def render(sheet, fam, fam_en, title, intro, overview, lang='zh', base_zh='', base_en=''):
    l = L10N[lang]
    rows = d[sheet]
    switcher = ('<p align="center"><sub>中文 · <a href="%s">English</a></sub></p>' % base_en) if lang == 'zh' else ('<p align="center"><a href="%s">中文</a> · English</p>' % base_zh)
    out = ['# ' + title, '', switcher, '', intro, '', l['overview'], '', overview, '', l['records'], '']
    # 按族顺序输出
    order = list(fam.keys())
    grouped = {}
    for r in rows[1:]:
        if not any(x.strip() for x in r):
            continue
        method = str(r[2]).strip()
        if method.startswith(('当前最佳','官方地板','实测地板','全榜最高','与官方地板差','与榜首差','待传')):
            continue
        if str(r[0]).strip() in ('当前最佳','官方地板行 (copy_last / wt_identity)','实测地板上传（本队）','全榜最高（榜首）','与官方地板差','与榜首差'):
            continue
        f = family_of(sheet, r)
        grouped.setdefault(f, []).append(r)
    for f in order:
        if f not in grouped:
            continue
        name, paras = (fam_en[f] if lang == 'en' else fam[f])
        out.append(l['family'] + name)
        out.append('')
        for p in paras:
            out.append(p)
            out.append('')
        out.append(l['detail'])
        out.append('')
        if sheet == 'T1_val':
            out.append(l['hdr_t1'])
            out.append(l['sep_t1'])
            for r in grouped[f]:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]) if len(r)>8 else '—', esc(r[9]) if len(r)>9 else ''))
        elif sheet in ('T2_embryo_interp','T2_heart_interp','T2_heart_extrap'):
            out.append(l['hdr_t2'])
            out.append(l['sep_t2'])
            for r in grouped[f]:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]), mark(r[9]), mark(r[10]), mark(r[11]), mark(r[12]) if len(r)>12 else '—', esc(r[13]) if len(r)>13 else ''))
        elif sheet == 'T3_gata4':
            out.append(l['hdr_t3'])
            out.append(l['sep_t3'])
            for r in grouped[f]:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]), mark(r[9]) if len(r)>9 else '—', esc(r[10]) if len(r)>10 else ''))
        out.append('')
    # 兜底：未归类的提交不丢
    if 'other' in grouped:
        out.append(l['other'])
        out.append('')
        out.append(l['detail'])
        out.append('')
        if sheet == 'T1_val':
            out.append(l['hdr_t1'])
            out.append(l['sep_t1'])
            for r in grouped['other']:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]) if len(r)>8 else '—', esc(r[9]) if len(r)>9 else ''))
        elif sheet in ('T2_embryo_interp','T2_heart_interp','T2_heart_extrap'):
            out.append(l['hdr_t2'])
            out.append(l['sep_t2'])
            for r in grouped['other']:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]), mark(r[9]), mark(r[10]), mark(r[11]), mark(r[12]) if len(r)>12 else '—', esc(r[13]) if len(r)>13 else ''))
        elif sheet == 'T3_gata4':
            out.append(l['hdr_t3'])
            out.append(l['sep_t3'])
            for r in grouped['other']:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]), mark(r[9]) if len(r)>9 else '—', esc(r[10]) if len(r)>10 else ''))
        out.append('')
    out.append(l['summary'])
    out.append('')
    out.extend(build_summary_lines(sheet, lang))
    out.append('')
    return '\n'.join(out)

jobs = [
    ('T1_val', T1_FAM, T1_EN, 'T1 实验报告：单细胞时间外推（E8.5→E9.5 → 预测 E10.5）', 'T1 experiment report: single-cell temporal extrapolation (E8.5→E9.5 → predict E10.5)',
     '评分指标：de_score / de_direction / mmd_u / variogram；总分 ≈ 0.25·de + 0.25·dir + 0.30·mmd + 0.20·vario。官方地板 50（copy_last），实测地板（本队）46.84。每个实验族记录：技术、工具、遇到的问题、结论，族内提交明细为全量效果数据（来自官方评分台账，时间 UTC）。',
     'Metrics: de_score / de_direction / mmd_u / variogram; total ≈ 0.25·de + 0.25·dir + 0.30·mmd + 0.20·vario. Official floor 50 (copy_last), measured floor (our upload) 46.84. Each family records: method, tools, issues, conclusion; the in-family submission log is the full result data (from the official scoring ledger, UTC).',
     '`pseudobulk shift（全局漂移）` 48.13 → damp 网格 shift@2.5 48.85 → `OT 混合` 47.52 → `Markov 通量` 44.19（证伪）→ `程序混合` 47.34（vario 31.7 崩）→ `multiplicative` 48.27 → `marker 动量` 48.80 → `copy_last` 实测地板 46.84 → `sel 族` 30.21~47.02（全崩）→ `dir24/dirprop` 47.19 → `momentum mask` 49.49 → `mm 库大小归一化` 49.93 → `covsafe` 48.09（证伪）→ `vs 方差放大` 50.67 → **`kp 知识程序位移+方差放大/成熟度加权`：kp3_w_a025 52.18 → kp7_m_b050 53.67（当前最佳）**',
     '`pseudobulk shift (global drift)` 48.13 → damp grid shift@2.5 48.85 → `OT mixture` 47.52 → `Markov flux` 44.19 (falsified) → `program mixture` 47.34 (vario 31.7 collapse) → `multiplicative` 48.27 → `marker momentum` 48.80 → `copy_last` measured floor 46.84 → `sel family` 30.21~47.02 (all collapse) → `dir24/dirprop` 47.19 → `momentum mask` 49.49 → `mm library-size normalization` 49.93 → `covsafe` 48.09 (falsified) → `vs variance amplification` 50.67 → **`kp knowledge-program shift + variance amplification / maturity weighting`: kp3_w_a025 52.18 → kp7_m_b050 53.67 (current best)**'),
    ('T2_embryo_interp', T2E_FAM, T2E_EN, 'T2 实验报告：胚胎插值（E6.75/E7.25/E8.0 → 预测中间阶段）', 'T2 experiment report: embryo interpolation (E6.75/E7.25/E8.0 → predict intermediate stage)',
     '评分指标 8 项：de_score / de_direction / mmd_u / variogram / d2_shape / occupancy_dice / scale_log_ratio / neighborhood_mmd；官方地板 50。面板：498 genes（官方发布面板，非目标文件基因集）。',
     'Eight metrics: de_score / de_direction / mmd_u / variogram / d2_shape / occupancy_dice / scale_log_ratio / neighborhood_mmd; official floor 50. Panel: 498 genes (the official published panel, not the target-file gene set).',
     '`v1（kNN 配对 log-linear 归一化 + 配对几何）` 59.0 → `mix_brkt` 59.07（d2/occ 弱）→ `bgm` 62.94 → `v1replica` 56.99（控制变量）→ `gps33 高斯过程` 62.37 → `gps33s（scale 校准）` 63.19 → `tls2n5000 类型级整体平移` 59.01（d2 23.8 崩）→ `gpsnnu 几何继承` 61.81 → `vg_ourmixs 几何移植` 55.93 → **`cpf015r5k 同源配对` 65.31（当前最佳）** → `vlK8 方差放大` 64.75（未超）',
     '`v1 (kNN-pair log-linear normalization + paired geometry)` 59.0 → `mix_brkt` 59.07 (d2/occ weak) → `bgm` 62.94 → `v1replica` 56.99 (controlled variable) → `gps33 Gaussian process` 62.37 → `gps33s (scale calibration)` 63.19 → `tls2n5000 type-level global shift` 59.01 (d2 23.8 collapse) → `gpsnnu geometric inheritance` 61.81 → `vg_ourmixs geometry transplant` 55.93 → **`cpf015r5k homologous pairing` 65.31 (current best)** → `vlK8 variance amplification` 64.75 (not above)'),
    ('T2_heart_interp', T2H_FAM, T2H_EN, 'T2 实验报告：心脏插值（E8.25/E8.75 → 预测中间阶段）', 'T2 experiment report: heart interpolation (E8.25/E8.75 → predict intermediate stage)',
     '评分指标 8 项（同上）；官方地板 50。面板：500 genes，必须逐元素按官方顺序对齐（曾因缺 Casp4/Pnliprp1 被拒）。',
     'Eight metrics (same as above); official floor 50. Panel: 500 genes, must be element-wise aligned to the official order (once rejected for missing Casp4/Pnliprp1).',
     '`v1（类型分层 + 全局配对）` 61.9 → `mix_brkt` 62.6 → **`mix_brkts（scale_log_ratio 71.1→100.0 满档）` 65.01（当前最佳）**；`gps50n1185` 50.2（无效）、`v1g2000s` 60.0、`v1geom5000s` 53.12（vario 37.6 崩）、`v1vc100` 53.61 均未超',
     '`v1 (type stratification + global pairing)` 61.9 → `mix_brkt` 62.6 → **`mix_brkts (scale_log_ratio 71.1→100.0 full marks)` 65.01 (current best)**; `gps50n1185` 50.2 (ineffective), `v1g2000s` 60.0, `v1geom5000s` 53.12 (vario 37.6 collapse), `v1vc100` 53.61 — none above'),
    ('T2_heart_extrap', T2X_FAM, T2X_EN, 'T2 实验报告：心脏外推（预测 E9.5 之后）', 'T2 experiment report: heart extrapolation (predict after E9.5)',
     '评分指标 8 项（同上）；官方地板 50。铁律：**只动 scale/构成、不动形态**。',
     'Eight metrics (same as above); official floor 50. Iron rule: **move only scale/composition, never morphology**.',
     '`v1 早期候选` 46.4 → `v3（置信收缩+坐标×1.31）` 48.71 → `v4 population_growth` 49.26 → `v2ga6` 53.59 / `v4a10` 50.08（微过地板）→ **形态线四次证伪**：`r6b70a20` 38.97 / `comp_c100` 32.8 / `vmorph_s120` 46.8 / `cpfx 类型级位移平移`（d2_shape 5.7）52.12 → **`scale_only` 54.51（当前最佳）**，`w005（位移 0.05）` 54.43、`mix20_scale` 53.9、`compw30_scale` 53.7 次之；`selday30/50` 27.5/28.9（全旅程最低，关闭）',
     '`v1 early candidate` 46.4 → `v3 (shrinkage + coordinates ×1.31)` 48.71 → `v4 population_growth` 49.26 → `v2ga6` 53.59 / `v4a10` 50.08 (marginally above floor) → **morphology-line falsified four times**: `r6b70a20` 38.97 / `comp_c100` 32.8 / `vmorph_s120` 46.8 / `cpfx type-level displacement shift` (d2_shape 5.7) 52.12 → **`scale_only` 54.51 (current best)**, then `w005 (displacement 0.05)` 54.43, `mix20_scale` 53.9, `compw30_scale` 53.7; `selday30/50` 27.5/28.9 (journey-lowest, closed)'),
    ('T3_gata4', T3_FAM, T3_EN, 'T3 实验报告：Gata4 KO 扰动响应预测（E8.75）', 'T3 experiment report: Gata4 KO perturbation response prediction (E8.75)',
     '评分指标：de_score / de_direction / severity_slope / mmd_u / variogram；总分 ≈ 0.298·de + 0.250·dir + 0.251·sev + 0.120·mmd + 0.080·vario。官方地板 50（wt_identity），实测地板（本队）45.81。',
     'Metrics: de_score / de_direction / severity_slope / mmd_u / variogram; total ≈ 0.298·de + 0.250·dir + 0.251·sev + 0.120·mmd + 0.080·vario. Official floor 50 (wt_identity), measured floor (our upload) 45.81.',
     '`transfer 全局Δ` 40.98（证伪：vario 49.8→12.2）→ `wt_identity` 实测地板 45.81 → `cardiac 限制` 44.85（证伪）→ `文献先验（Mab21l2 靶基因）` 45.80（平地板）→ `state 程序` 45.78（零增益）→ `mix 混合 KO`（mix20 61.5 → mix70 64.60）→ `kodir` 43.96 / `koq` 58.04 / `pk/ctl 26 基因` 38.91/43.14（关停）→ `mx50amp` 57.15 → **`cmp celltype^β 重采样`（b070 64.93 → b055 65.31）** → `cmpw 载体稀释` 65.49 → `pw` 64.47 / `prw` 54.49 → **`kb 真实 WT 稀释 KO`（k65 66.36）→ `kbb（k65×b055 组合）` 66.61（当前最佳）**，`kb k75` 65.32（方向错误）',
     '`transfer global Δ` 40.98 (falsified: vario 49.8→12.2) → `wt_identity` measured floor 45.81 → `cardiac restricted` 44.85 (falsified) → `literature prior (Mab21l2 targets)` 45.80 (ties floor) → `state program` 45.78 (zero gain) → `mix KO mixture` (mix20 61.5 → mix70 64.60) → `kodir` 43.96 / `koq` 58.04 / `pk/ctl 26 genes` 38.91/43.14 (shut down) → `mx50amp` 57.15 → **`cmp celltype^β resampling` (b070 64.93 → b055 65.31)** → `cmpw carrier dilution` 65.49 → `pw` 64.47 / `prw` 54.49 → **`kb real-WT dilution of KO` (k65 66.36) → `kbb (k65×b055 combo)` 66.61 (current best)**, `kb k75` 65.32 (wrong direction)'),
]
fname_map = {'T1_val':'experiments_t1.md','T2_embryo_interp':'experiments_t2_embryo_interp.md','T2_heart_interp':'experiments_t2_heart_interp.md','T2_heart_extrap':'experiments_t2_heart_extrap.md','T3_gata4':'experiments_t3.md'}
for sheet, fam, fam_en, t_zh, t_en, i_zh, i_en, o_zh, o_en in jobs:
    base = fname_map[sheet]
    base_en = base.replace('.md', '.en.md')
    md_zh = render(sheet, fam, fam_en, t_zh, i_zh, o_zh, 'zh', base, base_en)
    md_en = render(sheet, fam, fam_en, t_en, i_en, o_en, 'en', base, base_en)
    open(OUT + '\\' + base, 'w', encoding='utf-8').write(md_zh)
    open(OUT + '\\' + base_en, 'w', encoding='utf-8').write(md_en)
    print('written', base, '+ .en.md')
print('done')