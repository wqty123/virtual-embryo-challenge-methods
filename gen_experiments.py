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
    '工具：baselines/t1_shift.py、veckit 本地计分器、台账回填。',
    '遇到的问题：① variogram 全族偏低（35.7~44.5），全局平移破坏基因-基因协方差结构；② de_score 封顶 ≈45.3，全局标量猜不中"被点名的基因"；③ damp>2.5 无增益（S2.5 是拐点）；④ 非对称变体（up1.5/dn0.5、up1.5/dn0.75）比对称更差；⑤ 弥散探针 P4@0.5+s0.5 只有 42.29，噪声直接毁 vario(-19) 和 mmd。',
    '结论：shift 是最强简单基线，族峰值 shift@2.5 = 48.85（rank 142/202，de 45.3/dir 56.4/mmd 55.4/vario 34.1），超过实测地板 46.84 约 2 分；但"用 vario 换 de"到头，被后续按类型/按状态的生成超越。']),
 'otmix': ('OT 混合（WOT 耦合 + 类型转移重采样）', [
    '技术：用 WOT 在 E8.5→E9.5 上学细胞耦合矩阵，按类型转移概率重采样生成 E9.5 细胞；掩膜A（边掩膜 378→61 条边，去低质量耦合边）变体 otmixp 含生长因子π（出生-死亡过程），otmixm 无生长。实现：baselines/t1_otmix.py。',
    '工具：baselines/t1_otmix.py、wot_analysis/（WOT 耦合矩阵与边掩膜）、veckit。',
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
 'covsafe': ('covsafe（协方差安全化）', [
    '技术：mm 系 + 协方差安全化（l=25 低秩修正，保护基因-基因协方差）。',
    '工具：T1 生成器脚本族、veckit、真榜回填。',
    '遇到的问题：真榜 48.09 低于生产参考 shift@2.5 的 48.85（-0.76）——只改善 variogram（+16.3），de/dir/mmd 全降。',
    '结论：**保护结构不能代替正确的未来阶段转移方向**；covsafe 族关闭，不再上传 l10/l50 变体。']),
 'vs': ('vs（虚拟状态）', [
    '技术：虚拟状态重采样——在 E9.5 载体上构造虚拟中间状态（虚拟发育位置），按 vs 参数（200/500 载体）与 c 系数（c15/c135/c165）重采样；vs_kp6 是 vs×kp6 组合（a=0.30）。',
    '工具：T1 生成器脚本族、veckit。',
    '遇到的问题：vs200_c165 50.52 首破官方地板 50（mmd 55.7 当时新高）；vs500_c135 只有 50.01（de 40.9 弱）；vs_kp6_a030_n1249 50.67 继续刷新。',
    '结论：vs 族是 T1 破 50 的转折点——虚拟状态重采样比纯漂移更贴近真实连续发育；族峰值 50.67。']),
 'otf3': ('otf3（OT 流变体）', [
    '技术：OT flow 三阶段变体（n=2500，om2 掩膜）。',
    '工具：T1 生成器脚本族、veckit。',
    '遇到的问题：47.09 低于官方地板 50 与 mm_n1249_b070 的 49.93；de 38.8 弱。',
    '结论：OT 流变体未超 vs 族；关闭。']),
 'statepop': ('state_population_dynamics（状态群体动力学）', [
    '技术：状态群体动力学模型（显式 population state 动力学 + 表达生成）。',
    '工具：T1 生成器脚本族、veckit。',
    '遇到的问题：47.93 低于官方地板 50；de 43.0 高于 otf3 但仍弱、vario 41.6 偏弱。',
    '结论：动力学建模方向正确但实现未过线；后续并入 composition-support 研究接口。']),
 'kp': ('kp 族（成熟度加权混合管线）', [
    '技术：kp 管线 = 按细胞"成熟度"加权的混合生成（类型程序 w / 无 w 的 wo / 原始 raw / 仅 a 的 aonly / t00 变体）+ 库大小 b（b500c15 系列）+ n=2000 采样。关键参数：kp3_w_a025_b500c15_n2000（a=0.25）；kp7_m_b050_n2000（成熟度加权 β=0.50）；b=0.00 为对照。',
    '工具：T1 生成器脚本族（kp 系列）、check_submission.py、veckit、真榜回填。',
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
    '工具：baselines/t3_wt_identity.py、veckit。',
    '遇到的问题：实测地板 45.81；与 F 同文件双传烧 1 名额。',
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
    '技术：把预测构造为"真实 WT 载体 + KO 响应推断"的混合——mix 比例 p∈{20,30,40,50,60,70}% 的 KO 细胞与 WT 载体混合；kofeat 变体控制 KO 特征基因输入比例 feat∈{0.05,0.1,0.2,0.35}；muld_m05 是 mix70 的幅度变体；cardiac/knn 是谱系与最近邻变体。',
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
 'pkctl': ('pk/ctl（26 基因程序）', [
    '技术：pk26g18（26 个程序基因 g=18 变体）/ ctlp26（对照 26 基因）。',
    '工具：T3 生成器脚本族、veckit。',
    '遇到的问题：pk26g18 38.91（mmd 21.4/vario 10.8 双崩）；ctlp26 43.14（mmd 7.9/vario 19.4 双崩）。',
    '结论：26 基因程序族确认失败，关停。']),
 'mx50amp': ('mx50amp（50% 混合 + 幅度）', [
    '技术：50% 混合 + 幅度 0.92 构造。',
    '工具：T3 生成器脚本族、veckit。',
    '遇到的问题：57.15——severity_slope 90.6 高但 variogram 15.8 崩。',
    '结论：幅度构造毁 vario；关闭。']),
 'cmp': ('cmp（精准 KO 效应构造）', [
    '技术：cmp = 从真实 KO 数据推断"响应方向 + 幅度"，只对被点名的 KO 响应基因打效应，其余细胞完全复制（b 参数控制响应强度：b=0.70/0.55/1.00，n=6000）。',
    '工具：T3 生成器脚本族（cmp 系列）、veckit。',
    '遇到的问题：① cmp_n6000_b070 64.93 破 64.6 平台（de 56.3/sev 97.0 大涨，mmd/vario 各降约 10）——证明"精准打 KO 效应"优先于"多混真实细胞"；② b=1.00 63.35 五项全低于 b070；③ b=0.55 65.31（de 56.3 持平、dir 60.3/sev 97.1 微升、mmd/vario 双升）——b 低侧更优。',
    '结论：cmp_n6000_b055 = 65.31；**T3 杠杆点 = de(0.30 权重) + severity_slope(0.25 权重)**。']),
 'cmpw': ('cmpw（分布保真换机制）', [
    '技术：cmpw = cmp 的换机制版，k=70 控制响应基因集大小；de/sev 让位、mmd/vario 优先。',
    '工具：T3 生成器脚本族（cmpw 系列）、veckit。',
    '遇到的问题：cmpw_n6000_k70 65.49 超 cmp_b055（+0.18）：de 54.8(-1.5)/sev 92.4(-4.7) 让位，mmd 55.2(+11.0)/vario 53.9(+6.8) 暴涨。',
    '结论：换机制路线（分布优先）可小胜，但 T3 权重结构决定 sev 才是大头——cmpw 是过渡，kb 系在此基础上补齐 sev。']),
 'pw': ('pw（程序加权）', [
    '技术：pw = 程序加权构造，p 参数 0.50/1.00（n=6000）。',
    '工具：T3 生成器脚本族（pw 系列）、veckit。',
    '遇到的问题：pw050 64.47（mmd/vario 高于 cmp 但 de 54.8/dir 58.1 略低，未超 64.93）；pw100 62.87（de/dir 更低）。',
    '结论：pw 分布保真路线稳定但缺 KO 效应；关闭。']),
 'prw': ('prw（GSE 先验加权）', [
    '技术：prw = 程序加权 + GSE 外部先验（s=0.10，仅 1.2MB 小模型）。',
    '工具：T3 生成器脚本族（prw 系列）、veckit。',
    '遇到的问题：54.49——severity_slope 70.6 远低于 cmp 的 97.0（KO 效应未打出）；de 44.9/dir 51.3 弱。',
    '结论：外部先验加权不补 KO 效应；关闭。']),
 'kb': ('kb（成熟度加权响应）', [
    '技术：kb = 成熟度加权响应（kb6000 系列，k 控制成熟度分段 k=65/75），kbb 为 kb6000×b055 组合（k=65, b=0.55）。',
    '工具：T3 生成器脚本族（kb 系列）、veckit。',
    '遇到的问题：① kb6000_k65 66.36 超 cmpw（de 56.3/dir 62.2 dir 新高/sev 97.9 sev 新高/mmd 45.0/vario 50.5）——de/sev 回 cmp 系高位且 dir/sev 双新高；② kbb_n6000_b055_k65 66.61：de/dir 持平、sev 98.0/mmd 46.1/vario 51.8 三涨；③ kb6000_k75 65.32 五项全线下滑（vario -3.0）——k=65 才是最优。',
    '结论：**kbb_n6000_b055_k65 = 66.61**（rank 48/187），当前 T3 最佳。成熟度分段 k=65 + 响应强度 b=0.55 为最优参数组合；k=75 方向错误。']),
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
 'tls': ('tls2n5000（类型层级重采样）', [
    '技术：类型层级（tree）重采样，n=5000。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：59.01——d2_shape 23.8/occupancy_dice 17.6 崩坏（无约束抽样数量分布毁空间指标）；曾误投 T1 面板被拒（32285 vs 498）。',
    '结论：层级重采样毁空间占用；关闭。']),
 'gpsnnu': ('gpsnnu（高斯过程无约束变体）', [
    '技术：gps 族无约束（nnu）变体。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：61.81 < gps33s 63.19——d2 55.6 与 gps33s 同档但 de 53.5/mmd 61.6/vario 53.4 偏弱。',
    '结论：无约束版丢失 gps 的分布优势；关闭。']),
 'cpf': ('cpf015r5k（配对条件流）', [
    '技术：cpf = 配对条件流生成（r=0.15 正则，n=5000 采样，5k 版在 cpf015r 超上限被拒后按 583–5000 上限重采样）。',
    '工具：t2 生成器脚本族（cpf 系列）、check_submission.py、veckit。',
    '遇到的问题：cpf015r 原版 9000 cells 超本板上限被拒；cpf015r5k 65.31——de 55.8/dir 70.6/mmd 68.8/vario 67.1/d2 56.1 全面领先、occ 43.4 略弱。',
    '结论：**cpf015r5k = 65.31**（65/200）当前 T2 embryo interp 最佳。d2_shape/occupancy_dice 是剩余主要提升空间。']),
 'vlk8': ('vlK8（K=8 变体）', [
    '技术：vlK8 族（K=8 近邻条件）c125 变体。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：64.75——与 cpf015r5k 高度同构（dir/mmd/vario/d2/occ/scale 几乎一致），差距在 de 55.2(-0.6)/mmd 67.1(-1.7)/nh 63.4(-0.9)。',
    '结论：vlK8c125 64.75 是 cpf 的近亲平台，未超 65.31；两者共享 d2/occ 短板。']),
 'vg': ('vg_ourmixs（变基因混合）', [
    '技术：vg_ourmixs = 变异基因（variable genes）混合采样提交。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：55.93——scale 98.7 强但 d2 52.8/occ 48.2/nh 41.5 偏弱，低于 bgm 62.94。',
    '结论：vg 混合未超 gps/bgm 平台；关闭。']),
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
 'v1g2000': ('v1g2000s（v1 + 几何采样）', [
    '技术：v1 加几何约束采样（n=2000）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：60.0——几何约束变体低于 v1 的 61.9 与 mix_brkts 65.01。',
    '结论：几何结构变体不加分；关闭。']),
 'v1geom': ('v1geom5000s（v1 + 几何 5000）', [
    '技术：v1 + 几何约束 5000 采样。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：53.12——vario 37.6 崩（几何变换破坏表达分布）。',
    '结论：几何采样幅度大毁 vario；关闭。']),
 'v1vc': ('v1vc100（v1 + 方差控制）', [
    '技术：v1 + 方差控制（vc=100）。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：53.61——vario 34.7 仍弱。',
    '结论：方差控制未解决 vario 短板；关闭。']),
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
 'w005': ('w005（全指标均衡型）', [
    '技术：w 系（权重 0.05）均衡构造。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：54.43（rank 72/204）——de 46.8/dir 49.8/mmd 50.5/vario 50.1/d2 49.9/occ 54.1/scale 100/nh 51.1，全指标均衡型次佳。',
    '结论：均衡型与 scale_only 接近；w005 = 54.43 第二高。']),
 'selday': ('selday（选择天，关闭）', [
    '技术：selday 族——按发育日选择细胞（selday30/50_scale），对 E9.5 载体做 30%/50% 日期选择后仅 scale 调整。',
    '工具：t2 生成器脚本族、veckit。',
    '遇到的问题：27.54 / 28.9——全旅程最低分（mmd/vario/d2/occ 全面崩坏），日期选择破坏了 E9.5 的细胞构成。',
    '结论：日期选择对 extrap 无效；正式关闭。']),
 'cpfx': ('cpfx（cpf 外推变体）', [
    '技术：cpf（配对条件流）外推变体（n=8000, a=0.10）。',
    '工具：t2 生成器脚本族（cpf 系列）、veckit。',
    '遇到的问题：52.12——d2_shape 5.7 崩（形态外推被重罚）；occupancy_dice 42.0。',
    '结论：条件流外推动形态同样死；形态线第四次证伪，extrap 板形态路线全部关闭。']),
}

# ---------- 汇总行 ----------
SUMM = {
 'T1_val': [('当前最佳','53.67'),('官方地板行 (copy_last / wt_identity)','50'),('实测地板上传（本队）','46.84'),('全榜最高（榜首）','68.7')],
 'T2_embryo_interp': [('当前最佳','65.31'),('官方地板行 (copy_last / wt_identity)','50'),('全榜最高（榜首）','75.6')],
 'T2_heart_interp': [('当前最佳','65.01'),('官方地板行 (copy_last / wt_identity)','50'),('全榜最高（榜首）','73.4')],
 'T2_heart_extrap': [('当前最佳','54.51'),('官方地板行 (copy_last / wt_identity)','50'),('全榜最高（榜首）','60.5')],
 'T3_gata4': [('当前最佳','66.61'),('官方地板行 (copy_last / wt_identity)','50'),('实测地板上传（本队）','45.81'),('全榜最高（榜首）','75.2')],
}
# 汇总行也放进族输出
def build_summary_lines(sheet):
    return ['- **%s**：%s' % (k, v) for k, v in SUMM.get(sheet, [])]

def render(sheet, fam, title, intro, overview):
    rows = d[sheet]
    out = ['# ' + title, '', intro, '', '## 实验总览（按时间线，具体技术序列）', '', overview, '', '## 实验记录（按方法族分组）', '']
    # 按族顺序输出
    order = list(fam.keys())
    grouped = {}
    for r in rows[1:]:
        if not any(x.strip() for x in r):
            continue
        method = str(r[2]).strip()
        if method.startswith(('当前最佳','官方地板','实测地板','全榜最高','与官方地板差','与榜首差','待传')):
            continue
        # 汇总行：日期列带标签、方法列为空
        if str(r[0]).strip() in ('当前最佳','官方地板行 (copy_last / wt_identity)','实测地板上传（本队）','全榜最高（榜首）','与官方地板差','与榜首差'):
            continue
        f = family_of(sheet, r)
        grouped.setdefault(f, []).append(r)
    for f in order:
        if f not in grouped:
            continue
        name, paras = fam[f]
        out.append('### 实验族：' + name)
        out.append('')
        for p in paras:
            out.append(p)
            out.append('')
        # 提交明细
        out.append('**提交明细（全部效果，时间 UTC）**')
        out.append('')
        if sheet == 'T1_val':
            out.append('| 日期 | 版本 | 方法（文件） | 总分 | de | dir | mmd | vario | rank | 备注 |')
            out.append('|---|---|---|---|---|---|---|---|---|---|')
            for r in grouped[f]:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]) if len(r)>8 else '—', esc(r[9]) if len(r)>9 else ''))
        elif sheet in ('T2_embryo_interp','T2_heart_interp','T2_heart_extrap'):
            out.append('| 日期 | 版本 | 方法（文件） | 总分 | de | dir | mmd | vario | d2 | occ | scale | nh | rank | 备注 |')
            out.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
            for r in grouped[f]:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]), mark(r[9]), mark(r[10]), mark(r[11]), mark(r[12]) if len(r)>12 else '—', esc(r[13]) if len(r)>13 else ''))
        elif sheet == 'T3_gata4':
            out.append('| 日期 | 版本 | 方法（文件） | 总分 | de | dir | sev | mmd | vario | rank | 备注 |')
            out.append('|---|---|---|---|---|---|---|---|---|---|---|')
            for r in grouped[f]:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]), mark(r[9]) if len(r)>9 else '—', esc(r[10]) if len(r)>10 else ''))
        out.append('')
    # 兜底：未归类的提交不丢
    if 'other' in grouped:
        out.append('### 实验族：其他（未归类提交，保持完整记录）')
        out.append('')
        out.append('**提交明细（全部效果，时间 UTC）**')
        out.append('')
        if sheet == 'T1_val':
            out.append('| 日期 | 版本 | 方法（文件） | 总分 | de | dir | mmd | vario | rank | 备注 |')
            out.append('|---|---|---|---|---|---|---|---|---|---|')
            for r in grouped['other']:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]) if len(r)>8 else '—', esc(r[9]) if len(r)>9 else ''))
        elif sheet in ('T2_embryo_interp','T2_heart_interp','T2_heart_extrap'):
            out.append('| 日期 | 版本 | 方法（文件） | 总分 | de | dir | mmd | vario | d2 | occ | scale | nh | rank | 备注 |')
            out.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
            for r in grouped['other']:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]), mark(r[9]), mark(r[10]), mark(r[11]), mark(r[12]) if len(r)>12 else '—', esc(r[13]) if len(r)>13 else ''))
        elif sheet == 'T3_gata4':
            out.append('| 日期 | 版本 | 方法（文件） | 总分 | de | dir | sev | mmd | vario | rank | 备注 |')
            out.append('|---|---|---|---|---|---|---|---|---|---|---|')
            for r in grouped['other']:
                out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                    mark(r[0]), esc(r[1]), esc(r[2]), mark(r[3]), mark(r[4]), mark(r[5]), mark(r[6]), mark(r[7]), mark(r[8]), mark(r[9]) if len(r)>9 else '—', esc(r[10]) if len(r)>10 else ''))
        out.append('')
    out.append('## 汇总行')
    out.append('')
    out.extend(build_summary_lines(sheet))
    out.append('')
    return '\n'.join(out)

jobs = [
    ('T1_val', T1_FAM, 'T1 实验报告：单细胞时间外推（E8.5→E9.5 → 预测 E10.5）', '评分指标：de_score / de_direction / mmd_u / variogram；总分 ≈ 0.25·de + 0.25·dir + 0.30·mmd + 0.20·vario。官方地板 50（copy_last），实测地板（本队）46.84。每个实验族记录：技术、工具、遇到的问题、结论，族内提交明细为全量效果数据（来自官方评分台账，时间 UTC）。',
     '`pseudobulk shift（全局漂移）` 48.13 → damp 网格 shift@2.5 48.85 → `OT 混合` 47.52 → `Markov 通量` 44.19（证伪）→ `程序混合` 47.34（vario 31.7 崩）→ `multiplicative` 48.27 → `marker 动量` 48.80 → `copy_last` 实测地板 46.84 → `sel 族` 30.21~47.02（全崩）→ `dir24/dirprop` 47.19 → `momentum mask` 49.49 → `mm 库大小归一化` 49.93 → `covsafe` 48.09（证伪）→ `vs 虚拟状态` 50.67 → **`kp 成熟度加权混合管线`：kp3_w_a025 52.18 → kp7_m_b050 53.67（当前最佳）**'),
    ('T2_embryo_interp', T2E_FAM, 'T2 实验报告：胚胎插值（E6.75/E7.25/E8.0 → 预测中间阶段）', '评分指标 8 项：de_score / de_direction / mmd_u / variogram / d2_shape / occupancy_dice / scale_log_ratio / neighborhood_mmd；官方地板 50。面板：498 genes（官方发布面板，非目标文件基因集）。',
     '`v1（kNN 配对 log-linear 归一化 + 配对几何）` 59.0 → `mix_brkt` 59.07（d2/occ 弱）→ `bgm` 62.94 → `v1replica` 56.99（控制变量）→ `gps33 高斯过程` 62.37 → `gps33s（scale 校准）` 63.19 → `tls2n5000` 59.01（d2 23.8 崩）→ `gpsnnu` 61.81 → `vg_ourmixs` 55.93 → **`cpf015r5k 配对条件流` 65.31（当前最佳）** → `vlK8c125` 64.75（未超）'),
    ('T2_heart_interp', T2H_FAM, 'T2 实验报告：心脏插值（E8.25/E8.75 → 预测中间阶段）', '评分指标 8 项（同上）；官方地板 50。面板：500 genes，必须逐元素按官方顺序对齐（曾因缺 Casp4/Pnliprp1 被拒）。',
     '`v1（类型分层 + 全局配对）` 61.9 → `mix_brkt` 62.6 → **`mix_brkts（scale_log_ratio 71.1→100.0 满档）` 65.01（当前最佳）**；`gps50n1185` 50.2（无效）、`v1g2000s` 60.0、`v1geom5000s` 53.12（vario 37.6 崩）、`v1vc100` 53.61 均未超'),
    ('T2_heart_extrap', T2X_FAM, 'T2 实验报告：心脏外推（预测 E9.5 之后）', '评分指标 8 项（同上）；官方地板 50。铁律：**只动 scale/构成、不动形态**。',
     '`v1 早期候选` 46.4 → `v3（置信收缩+坐标×1.31）` 48.71 → `v4 population_growth` 49.26 → `v2ga6` 53.59 / `v4a10` 50.08（微过地板）→ **形态线四次证伪**：`r6b70a20` 38.97 / `comp_c100` 32.8 / `vmorph_s120` 46.8 / `cpfx`（d2_shape 5.7）52.12 → **`scale_only` 54.51（当前最佳）**，`w005` 54.43、`mix20_scale` 53.9、`compw30_scale` 53.7 次之；`selday30/50` 27.5/28.9（全旅程最低，关闭）'),
    ('T3_gata4', T3_FAM, 'T3 实验报告：Gata4 KO 扰动响应预测（E8.75）', '评分指标：de_score / de_direction / severity_slope / mmd_u / variogram；总分 ≈ 0.298·de + 0.250·dir + 0.251·sev + 0.120·mmd + 0.080·vario。官方地板 50（wt_identity），实测地板（本队）45.81。',
     '`transfer 全局Δ` 40.98（证伪：vario 49.8→12.2）→ `wt_identity` 实测地板 45.81 → `cardiac 限制` 44.85（证伪）→ `文献先验（Mab21l2 靶基因）` 45.80（平地板）→ `state 程序` 45.78（零增益）→ `mix 混合 KO`（mix20 61.5 → mix70 64.60）→ `kodir` 43.96 / `koq` 58.04 / `pk/ctl 26 基因` 38.91/43.14（关停）→ `mx50amp` 57.15 → **`cmp 精准 KO 效应`（b070 64.93 → b055 65.31）** → `cmpw` 65.49 → `pw` 64.47 / `prw` 54.49 → **`kb 成熟度加权`（k65 66.36）→ `kbb（k65×b055 组合）` 66.61（当前最佳）**，`kb k75` 65.32（方向错误）'),
]
for sheet, fam, title, intro, overview in jobs:
    md = render(sheet, fam, title, intro, overview)
    fname = {'T1_val':'experiments_t1.md','T2_embryo_interp':'experiments_t2_embryo_interp.md','T2_heart_interp':'experiments_t2_heart_interp.md','T2_heart_extrap':'experiments_t2_heart_extrap.md','T3_gata4':'experiments_t3.md'}[sheet]
    open(OUT + '\\' + fname, 'w', encoding='utf-8').write(md)
    print('written', fname)
print('done')
