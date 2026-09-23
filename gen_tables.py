# -*- coding: utf-8 -*-
"""从台账 JSON 生成三个任务的方法+效果 Markdown 表格主体。"""
import json

DUMP = r'C:\Users\FB\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.sessions\38442478683482882\agents\m_0cwprxb4apa\taizhang_dump.json'
OUT_DIR = r'D:\freebuff\virtual-embryo-challenge\journey_repo'

d = json.load(open(DUMP, encoding='utf-8'))

def mark(v):
    return '—' if v in ('', '待抓', '待补') else v

def build_table(sheet):
    rows = d[sheet]
    header = rows[0]
    lines = []
    data_rows = []
    summary_rows = []
    # 数据行 vs 汇总行：汇总行的'方法'列通常为中文标签（当前最佳/地板/榜首等），数据行含文件/版本
    for r in rows[1:]:
        if not any(x.strip() for x in r):
            continue
        method = r[2].strip() if len(r) > 2 else ''
        if method.startswith(('当前最佳', '官方地板行', '实测地板上传', '全榜最高', '与官方地板差', '与榜首差', '待传', '未提交')):
            summary_rows.append(r)
        else:
            data_rows.append(r)
    # 表头
    hdr = ['#', '日期', '版本', '方法（文件名）', '总分']
    metric_names = {
        'T1_val': ['de', 'dir', 'mmd', 'vario'],
        'T2_embryo_interp': ['de', 'dir', 'mmd', 'vario', 'd2', 'occ', 'scale', 'nh'],
        'T2_heart_interp': ['de', 'dir', 'mmd', 'vario', 'd2', 'occ', 'scale', 'nh'],
        'T2_heart_extrap': ['de', 'dir', 'mmd', 'vario', 'd2', 'occ', 'scale', 'nh'],
        'T3_gata4': ['de', 'dir', 'sev', 'mmd', 'vario'],
    }
    hdr += metric_names[sheet] + ['rank', '结论/备注']
    lines.append('| ' + ' | '.join(hdr) + ' |')
    lines.append('|' + '---|' * len(hdr))
    idx = 0
    for r in data_rows:
        idx += 1
        # 版本列=1, 方法=2, 总分=3, 指标从4开始, rank列位置随表不同
        version = mark(r[1])
        method = r[2].strip()
        total = mark(r[3])
        if sheet in ('T1_val',):
            metrics = [mark(x) for x in r[4:8]]
            rank = mark(r[8]) if len(r) > 8 else '—'
            note = r[9] if len(r) > 9 else ''
        elif sheet in ('T2_embryo_interp', 'T2_heart_interp'):
            metrics = [mark(x) for x in r[4:12]]
            rank = mark(r[12]) if len(r) > 12 else '—'
            note = r[13] if len(r) > 13 else ''
        elif sheet == 'T2_heart_extrap':
            metrics = [mark(x) for x in r[4:12]]
            rank = mark(r[12]) if len(r) > 12 else '—'
            note = r[13] if len(r) > 13 else ''
        elif sheet == 'T3_gata4':
            metrics = [mark(x) for x in r[4:9]]
            rank = mark(r[9]) if len(r) > 9 else '—'
            note = r[10] if len(r) > 10 else ''
        else:
            metrics = []; rank = '—'; note = ''
        note = note.strip()
        # 截断过长的备注
        if len(note) > 240:
            note = note[:237] + '…'
        lines.append('| %d | %s | %s | %s | %s | %s | %s | %s |' % (
            idx, mark(r[0]), version, method.replace('|', '/'), total,
            ' | '.join(metrics), rank, note.replace('|', '/')))
    return lines, summary_rows, hdr

def summary_block(summary_rows, hdr):
    lines = []
    for r in summary_rows:
        vals = [mark(x) for x in r]
        # 汇总行只取 方法=值 形式
        lines.append('- **%s**：%s' % (vals[2] if len(vals) > 2 else '', vals[3] if len(vals) > 3 else ''))
    return lines

for sheet, out_name, title in [
    ('T1_val', 'methods_t1.md', 'T1：单细胞时间外推（E8.5→E9.5→预测 E10.5）'),
    ('T2_embryo_interp', 'methods_t2_embryo_interp.md', 'T2：胚胎插值（E6.75→E7.25→E8.0 预测中间阶段）'),
    ('T2_heart_interp', 'methods_t2_heart_interp.md', 'T2：心脏插值（E8.25/E8.75 预测中间阶段）'),
    ('T2_heart_extrap', 'methods_t2_heart_extrap.md', 'T2：心脏外推（预测 E9.5 之后）'),
    ('T3_gata4', 'methods_t3.md', 'T3：Gata4 KO 扰动响应预测'),
]:
    lines, summary_rows, hdr = build_table(sheet)
    with open(OUT_DIR + '\\' + out_name, 'w', encoding='utf-8') as f:
        f.write('# %s\n\n' % title)
        f.write('## 方法与效果总表（数据来自官方评分台账，时间 UTC）\n\n')
        f.write('\n'.join(lines) + '\n\n')
        f.write('## 汇总行\n\n')
        f.write('\n'.join(summary_block(summary_rows, hdr)) + '\n')
    print('written', out_name, 'rows', len(lines) - 2)
