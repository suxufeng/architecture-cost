#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""《架构的代价》内容合法性 + 大纲一致性审计扫描器（只读）。

用法： python scripts/audit_content.py [项目根目录]

输出为「候选线索」，命中 != 违规，必须人工复核后定性。
分四部分：
  A 涉密 / 侵权 / 信息保护（候选）
  B 臆测 / 客观性 / 中立性（收紧后的候选）
  C 证据标签配套与台账交叉
  D 大纲与正文逐项一致性（硬比对）
"""
import os
import re
import sys
import json
import glob
from collections import defaultdict

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BODY_GLOBS = ['manuscript/**/*.md']
SITE_GLOBS = ['manuscript/**/*.md', 'index.md', 'about.md', 'README.md', 'outline/*.md', 'references/*.md']
HAN = re.compile(r'[\u4e00-\u9fff]')


def files(globs):
    out = []
    for g in globs:
        for p in glob.glob(os.path.join(ROOT, g), recursive=True):
            if os.path.isfile(p):
                out.append(os.path.relpath(p, ROOT).replace('\\', '/'))
    return sorted(set(out))


def read(rel):
    return open(os.path.join(ROOT, rel), encoding='utf-8').read()


def split_paras(text):
    res = []
    pos = 0
    for m in re.finditer(r'\n\s*\n', text):
        seg = text[pos:m.start()].strip()
        if seg:
            res.append((text.count('\n', 0, pos) + 1, seg))
        pos = m.end()
    if text[pos:].strip():
        res.append((text.count('\n', 0, pos) + 1, text[pos:].strip()))
    return res


# ---------- A：涉密 / 侵权 / 信息保护 ----------
A = [
    ('A1 联系方式/证件号（候选）', re.compile(r'[\w.\-]+@[\w.\-]+\.[A-Za-z]{2,}|(?<!\d)1[3-9]\d{9}(?!\d)|(?<!\d)\d{17}[\dXx](?!\d)')),
    ('A2 内部项目/产品名（候选）', re.compile(r'亲邻|小范管家|小范同学|云梯控|QADN|QADX|QFAD|G25|U6\b|G202|云对讲|Y5\b|新城悦|盘古花园|皓邻|社区智能体平台|代收代付|非机动车门禁|水印盒子')),
    ('A3 内部数据字段词（需人工判是否作通用术语）', re.compile(r'通过率|合格率|闭环率|告警量|维修单量|压测值|批次台数|毛利率|物料单价')),
    ('A4 可定位组合：地名+数字（规范禁止两项组合）', re.compile(r'(深圳|广州|上海|北京|杭州|苏州|南京|成都|武汉|天河区|华南理工)[^\n。；]{0,50}?\d{2,}')),
    ('A5 大段整句引号（可能为标准原文照搬）', re.compile(r'[「"『][^」"』\n]{100,}[」"』]')),
    ('A6 第三人称负面点名', re.compile(r'(某公司|某厂商|某云服务商|某供应商)[^\n。]{0,50}(事故|泄露|缺陷|违规|被罚|处罚)')),
]

# ---------- B：臆测 / 客观性（收紧） ----------
B = [
    ('B1 无源断言套话（正文）', re.compile(r'业内通常|行业普遍|据统计|研究表明|一般认为|众所周知|普遍认为|毋庸置疑|毫无疑问')),
    ('B2 强绝对化（正文）', re.compile(r'必然|绝不|百分之百|绝无|永远不|一定是|所有都|任何情况下都')),
    ('B3 已取消的证据标签（反引号包裹才算）', re.compile(r'[`\'\"](实测|设计态)[`\'\"]')),
    ('B4 内部经验自述', re.compile(r'我们发现|我们踩过|我们的经验是|我们做过|我们自研了')),
    ('B5 过时口径（仅大纲/规范/首页）', re.compile(r'30\.1\s*万|301,000|60\s*条判断点|30\s*章\s*×|31\s*章（?收口|V1\.2（7 篇 31 章）|十几年|后记：我判断错过的三次|M3 全书 \| 余下 25 章 \+ 后记')),
    ('B6 状态过时：初稿（仅首页/README）', re.compile(r'初稿')),
]

TAG = re.compile(r'[`\'\"](公开|引用|推演|场景)[`\'\"]')
STD = re.compile(r'\b(?:GB/T|GB|ISO/IEC|ISO|IEC|NIST|OWASP|OASIS|MIL-STD|SP\s*800|RFC)\s*[\d.\-—:：A-Za-z]*\d[\d.\-—:：A-Za-z]*')
SCENE_MARK = re.compile(r'由\s*(?:\d+|N)\s*个公开(?:案例|来源)|不对应任何单一项目|由\s*(?:\d+|N)\s*个公开案例与通用实践重构|复合场景.*?重构')


def main():
    body = files(BODY_GLOBS)
    site = files(SITE_GLOBS)
    outline = [f for f in site if f.startswith('outline/')]
    hits = defaultdict(list)

    for rel in site:
        text = read(rel)
        scope_body = rel in body
        scope_meta = (not scope_body)
        patterns = A + [(n, p) for n, p in B if (n.startswith('B1') or n.startswith('B2') or n.startswith('B3') or n.startswith('B4')) == scope_body or scope_meta]
        for name, pat in patterns:
            if name.startswith('B5') and (scope_body or rel.startswith('outline/99_')):
                continue
            if name.startswith('B6') and rel not in ('index.md', 'README.md'):
                continue
            for m in pat.finditer(text):
                ln = text.count('\n', 0, m.start()) + 1
                hits[name].append((rel, ln, text[max(0, m.start() - 28):m.end() + 28].replace('\n', ' ')))

    # ---- C：证据标签配套 ----
    tag_count = defaultdict(int)
    inference_total = 0
    inference_with_nearby_assumption = 0
    scene_by_chapter = defaultdict(int)
    std_body = defaultdict(set)

    for rel in body:
        text = read(rel)
        plist = split_paras(text)
        for tag in TAG.findall(text):
            tag_count[tag] += 1
        for i, (ln, p) in enumerate(plist):
            if '推演' in p:
                inference_total += 1
                window = ' '.join(x[1] for x in plist[max(0, i - 1):i + 3])
                if re.search(r'假设|推翻条件|前提|若.{0,20}(?:不成立|改变|不成立)', window):
                    inference_with_nearby_assumption += 1
            if SCENE_MARK.search(p):
                scene_by_chapter[rel] += 1
            for s in STD.findall(p):
                std_body[rel].add(s.strip())

    ledger = read('references/index.md')
    ledger_std = set(s.strip() for s in STD.findall(ledger))
    body_std_union = set().union(*std_body.values()) if std_body else set()
    missing_std = sorted(s for s in body_std_union if not any(s in t or t in s for t in ledger_std))

    # ---- D：大纲与正文一致性（硬比对） ----
    d_outline = read('outline/03_全书大纲.md')
    # 章级总目录：| 1 | 基座：编排器不听你的话 | ... | 6,000 |
    outline_ch = {}
    for m in re.finditer(r'^\|\s*(\d{1,2})\s*\|\s*([^|]+?)\s*\|\s*[^|]*\|\s*([\d,]+)\s*\|', d_outline, re.M):
        outline_ch[int(m.group(1))] = (m.group(2).replace('**', '').strip(), int(m.group(3).replace(',', '')))
    body_ch = {}
    body_words = {}
    for rel in body:
        text = read(rel)
        m = re.search(r'^title:\s*第\s*(\d{1,2})\s*章\s*·\s*(.+)$', text, re.M)
        if m:
            n = int(m.group(1))
            body_ch[n] = (m.group(2).strip(), rel)
            body_words[n] = len(HAN.findall(text))
    preface_words = len(HAN.findall(read('manuscript/00-preface.md')))
    total_words = sum(len(HAN.findall(read(f))) for f in body)

    print('=' * 78)
    print('扫描范围：正文 %d 章 + 站点源 %d 文件；正文汉字 %d' % (len(body_ch), len(site), total_words))
    print('=' * 78)

    for name, _ in A + B:
        lst = hits.get(name, [])
        print('\n[%s] %d 处' % (name, len(lst)))
        for rel, ln, frag in lst[:10]:
            print('  %s:%d  %s' % (rel, ln, frag[:105]))
        if len(lst) > 10:
            print('  ... 另 %d 处' % (len(lst) - 10))

    print('\n' + '=' * 78)
    print('C 证据标签与台账')
    print('=' * 78)
    print('标签出现次数:', dict(tag_count))
    print('含「推演」段落:', inference_total, '| 前后 3 段内含假设/推翻条件:', inference_with_nearby_assumption)
    print('有场景构造说明的章节:', len([k for k, v in scene_by_chapter.items() if v]), '/', len(body_ch))
    print('无场景构造说明的章:', [body_ch[n][1].split('/')[-1] for n in sorted(body_ch) if scene_by_chapter.get(body_ch[n][1], 0) == 0])
    print('正文标准号（去重）:', len(body_std_union), '| 台账标准号:', len(ledger_std))
    print('正文有、台账未命中:', missing_std)

    print('\n' + '=' * 78)
    print('D 大纲 ↔ 正文 一致性')
    print('=' * 78)
    print('大纲章数:', len(outline_ch), '| 正文带 title 的章数:', len(body_ch))
    for n in sorted(set(list(outline_ch) + list(body_ch))):
        o = outline_ch.get(n)
        b = body_ch.get(n)
        if not o or not b:
            print('  ✗ 章 %d 缺失：大纲=%s 正文=%s' % (n, bool(o), bool(b)))
            continue
        name_match = o[0] == b[0] or o[0].replace('：', '：') in b[0] or b[0] in o[0]
        print('  章 %2d %s | 大纲「%s」/ 正文「%s」| 计划 %d / 实收 %d' %
              (n, '✓' if name_match else '✗ 标题不一致', o[0], b[0], o[1], body_words.get(n, 0)))
    print('\n总量口径：')
    print('  大纲头部 30.1 万字 / 合计 301,000 | 首页 index.md 28.1 万 | 正文实收 %d' % total_words)
    print('  前言：大纲 6,000 | 实收 %d' % preface_words)
    print('  大纲列「后记：我判断错过的三次」3,000 字 | 正文后记文件:', '存在' if os.path.exists(os.path.join(ROOT, 'manuscript/35-afterword.md')) else '不存在')
    print('  大纲第 34 章名「%s」 | 正文「%s」' % (outline_ch.get(34, ('?',))[0], body_ch.get(34, ('?',))[0]))

    with open(os.path.join(ROOT, '.audit_hits.json'), 'w', encoding='utf-8') as fp:
        json.dump({k: v for k, v in hits.items()}, fp, ensure_ascii=False, indent=1)
    print('\n完整候选清单：.audit_hits.json')


if __name__ == '__main__':
    main()
