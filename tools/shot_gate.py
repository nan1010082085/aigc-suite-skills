#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shot_gate —— 出片通用硬闸（aigc-suite-skills 套件工具，2026-10-29 出片五律｜2026-11-24 本地真相源）。
任何项目通用：项目侧放 gen_gate.config.json + asset_registry.json（本地派生；Notion 可选）。

用法:
  # 1a) 从本地 assets.json / 已有 registry 刷新（默认）
  python3 -I tools/shot_gate.py --config <proj>/gen_gate.config.json --build-registry

  # 1b) 可选：启用 Notion 适配构建注册表并回写台账
  python3 -I tools/shot_gate.py --config <proj>/gen_gate.config.json --build-registry --notion

  # 2) 出片前过闸（任一 FAIL 拒绝生成；付费 confirm/run 前必过）
  python3 -I tools/shot_gate.py --config <proj>/gen_gate.config.json \\
      --shot 001-1 --prompt-file pkg/prompt.txt --ref-ids <id1,id2,...> [--status 生成中]

  # 3) 从本地镜块逐字导出锁版 prompt
  python3 -I tools/shot_gate.py --config <proj>/gen_gate.config.json \\
      --shot 001-1 --emit-prompt pkg/prompt.txt

闸门（对应出片五律｜本地默认）:
  G-PARITY   ⑤本地镜块为真相源；--notion 时额外校验外部内容列 SHA
  G-VERBATIM ①prompt ↔ 镜块四段式逐字节一致（唯一机械处理=换行归一化）——禁压缩/改写/自创
  G-REFBIND  ③④@锁名→注册表→ref 资源 ID 三者逐个对应
  G-MODEL    ②模型/比例/分辨率在项目策略内；超上限=回本地分镜设计变更
  G-REVIEW   ②本地/参数状态=放行值（默认「生成中」）或用户已批；--notion 时可读外部表
"""
import argparse, hashlib, json, os, re, sys, time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
SECTIONS = ['【基础设定】', '【氛围与画质】', '【画面内容】', '【声音】']


def norm(t):
    """唯一允许的机械处理：可选 Notion <br/> 还原 + markdown 转义还原 + 换行归一化。"""
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'<br\s*/?>', '\n', t)
    t = re.sub(r'\\([_*~^\[\]()>#+\-.!])', r'\1', t)
    t = t.replace('\r\n', '\n')
    return '\n'.join(l.rstrip() for l in t.split('\n')).strip()


def sha(t):
    return hashlib.sha256(norm(t).encode('utf-8')).hexdigest()


# ---------- 可选 Notion 适配 ----------

def notion_call(tool, args):
    from notion_mcp_client import MCP
    m = None
    for a in range(10):
        try:
            m = MCP(); break
        except Exception:
            time.sleep(10)
    for att in range(10):
        try:
            r = m.call(tool, args)
        except Exception:
            time.sleep(10); continue
        s = json.dumps(r, ensure_ascii=False)
        if '"isError"' not in s and 'validation_error' not in s:
            return r
        time.sleep(8)
    raise RuntimeError('notion call failed')


def query_rows(ds, view=None):
    rows, cur = [], None
    for _ in range(30):
        if view:
            args = {'mode': 'view', 'view_url': view, 'page_size': 100, 'is_archived': False}
            if cur: args['start_cursor'] = cur
        else:
            args = {'mode': 'sql', 'data_source_urls': [ds], 'query': f'SELECT * FROM [{ds}] LIMIT 100'}
        r = notion_call('notion-query-data-sources', {'data': args})
        d = json.loads(r['result']['content'][0]['text'])
        rows += d.get('results', [])
        if not d.get('has_more'):
            break
        cur = d.get('next_cursor'); time.sleep(1)
    return rows


# ---------- 注册表 ----------

STATE_RULES = {
    '信物手链': {'原色': '原色|正红|深红|接口打死结', '浅红': '浅红|残粉|褪|剩粉|几乎看不见|断头'},
    '毛绒钥匙扣': {'渗雾': '渗雾|雾丝|异变', '': ''},
    '借命登记簿': {'翻开': '翻开|打开', '': ''},
    '灰白道具甲': {'人脸浮现': '人脸|浮现', '': ''},
}
ALIAS = {'信物手链': '信物', '道具乙拐杖': '道具乙', '毛绒钥匙扣': '毛绒', '白瓷茶壶': '茶壶',
         '灰白道具甲': '道具甲', '锈迹铁盒': '铁盒', '铸铁哑铃': '哑铃', '塑料工牌': '工牌',
         '九张塑封照片': '塑封照片', '第十张照片': '第十张', '借命登记簿': '登记簿', '银灰盾徽': '盾徽'}


def canon(name):
    n = re.sub(r'^(人物|场景|道具)-', '', name)
    n = re.sub(r'-(基础形象[A-C]|常服立绘|剧情立绘|成神样本)$', '', n)
    n = re.sub(r'-(全景|中景|特写)(_[^-\s]+)?$', '', n)
    for k, v in ALIAS.items():
        if k in n:
            return v
    return n


def name_match(a_want, b_name):
    a, b = canon(a_want), canon(b_name)
    return bool(a) and (a == b)


def collect_lock_names(cfg):
    shot_dir = os.path.join(cfg['root'], cfg['shot_dir'])
    META = {'引用', '完整描述', '资产锁', '双保险', '素材待建'}
    lock_names = set()
    if not os.path.isdir(shot_dir):
        return lock_names
    for f in os.listdir(shot_dir):
        if not f.endswith('.md'): continue
        for nm in re.findall(r'@([^\s：:，。、；;（）【】｜／/]+)',
                             open(os.path.join(shot_dir, f), encoding='utf-8').read()):
            if nm not in META and '引用' not in nm:
                lock_names.add(nm)
    return lock_names


def build_registry_local(cfg):
    """从本地 assets.json 或已有 registry 刷新 asset_registry.json。"""
    proj = cfg['root']
    out = os.path.join(proj, 'asset_registry.json')
    assets_path = os.path.join(proj, cfg.get('assets_file', 'assets.json'))
    reg = []
    if os.path.isfile(assets_path):
        data = json.load(open(assets_path, encoding='utf-8'))
        for section in ('characters', 'scenes', 'props', 'outfits'):
            for item in data.get(section, []) or []:
                name = item.get('name') or item.get('lock_name') or item.get('id') or ''
                rid = item.get('resource_id') or item.get('即梦资源ID') or ''
                nid = item.get('node_id') or item.get('画布节点ID') or ''
                lock = item.get('lock_name') or item.get('visual_id') or canon(name)
                kws = item.get('state_keywords', '')
                reg.append({
                    'file': name, 'resource_id': rid, 'node_id': nid,
                    'lock_name': lock, 'state_keywords': kws,
                })
        # character three_view / expressions as separate lock entries when present
        for ch in data.get('characters', []) or []:
            for key in ('three_view', 'face_card'):
                val = ch.get(key)
                if isinstance(val, dict):
                    reg.append({
                        'file': val.get('file') or f"{ch.get('name')}-{key}",
                        'resource_id': val.get('resource_id', ''),
                        'node_id': val.get('node_id', ''),
                        'lock_name': val.get('lock_name') or ch.get('visual_id') or ch.get('name'),
                        'state_keywords': '',
                    })
    elif os.path.isfile(out):
        reg = json.load(open(out, encoding='utf-8')).get('assets', [])
        print(f'ℹ 无 assets.json，沿用已有 registry {len(reg)} 条')
    else:
        print('⚠ 无 assets.json 且无 asset_registry.json——写出空注册表，出片前须补素材登记')
    json.dump({'built_at': time.strftime('%F %T'), 'source': 'local', 'assets': reg},
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'✓ 本地注册表 {len(reg)} 条 → {out}')
    return reg


def build_registry_notion(cfg):
    """可选：Notion 素材台账 → asset_registry.json；回写「分镜锁名/状态关键词」列。"""
    proj = cfg['root']
    rows = query_rows(cfg['notion']['asset_ds'])
    lock_names = collect_lock_names(cfg)
    reg = []
    for x in rows:
        fname = x.get('Name', '')
        rid = x.get('即梦资源ID', '')
        nid = x.get('画布节点ID', '')
        hit = next((l for l in lock_names if name_match(l, fname)), None)
        if not hit:
            hit = canon(fname)
        kws = ''
        for lock, variants in STATE_RULES.items():
            if lock in fname or name_match(hit, lock) or name_match(fname, lock):
                hit = lock
                for tag, pat in variants.items():
                    if tag and tag in fname:
                        kws = pat
                break
        reg.append({'file': fname, 'resource_id': rid, 'node_id': nid,
                    'lock_name': hit, 'state_keywords': kws})
    out = os.path.join(proj, 'asset_registry.json')
    json.dump({'built_at': time.strftime('%F %T'), 'source': 'notion', 'assets': reg},
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for x, r in zip(rows, reg):
        pid = x['url'].rsplit('/', 1)[-1]
        notion_call('notion-update-page', {'page_id': pid, 'command': 'update_properties',
                    'properties': {'分镜锁名': r['lock_name'], '状态关键词': r['state_keywords']}})
        time.sleep(0.2)
    print(f'✓ 注册表 {len(reg)} 条 → {out}；已回写 Notion「分镜锁名/状态关键词」（--notion）')
    return reg


def load_shot(cfg, shot):
    n, idx = shot.split('-')
    fp = os.path.join(cfg['root'], cfg['shot_file'].format(n=int(n)))
    txt = open(fp, encoding='utf-8').read()
    for p in re.split(r'(?=\n### 镜 ?\d+)', txt):
        m = re.match(r'\n?### 镜 ?(\d+)', p)
        if m and int(m.group(1)) == int(idx):
            i = max(p.find('【镜头】'), p.find('【基础设定】'))
            return p[i:] if i >= 0 else p
    raise SystemExit(f'找不到镜 {shot}')


def load_local_status(cfg, shot):
    """读项目本地放行状态：gen_status.json 或 config.status_file。"""
    path = os.path.join(cfg['root'], cfg.get('status_file', 'gen_status.json'))
    if not os.path.isfile(path):
        return ''
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception:
        return ''
    if isinstance(data, dict):
        if shot in data:
            v = data[shot]
            return v.get('状态') if isinstance(v, dict) else str(v)
        if '状态' in data:
            return str(data['状态'])
        shots = data.get('shots') or data.get('status') or {}
        if isinstance(shots, dict) and shot in shots:
            v = shots[shot]
            return v.get('状态') if isinstance(v, dict) else str(v)
    return ''


def notion_seg(cfg, shot):
    rows = query_rows(cfg['notion']['storyboard_ds'], view=cfg['notion'].get('view'))
    for x in rows:
        if str(x.get('镜号')) in (shot, shot.split('-')[0].lstrip('0') + '-' + shot.split('-')[1], shot.replace('-', '-0')):
            c = x.get('内容') or ''
            i = max(c.find('【镜头】'), c.find('【基础设定】'))
            return c[i:] if i >= 0 else c
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--build-registry', action='store_true')
    ap.add_argument('--notion', action='store_true',
                    help='启用 Notion 外部适配（注册表构建/内容列对账/状态读取）')
    ap.add_argument('--shot'); ap.add_argument('--prompt-file')
    ap.add_argument('--emit-prompt', help='从本地镜块逐字写出锁版 prompt（默认）；--notion 时改从外部内容列取')
    ap.add_argument('--ref-ids', default='', help='实际传给生成调用的资源 ID（逗号分隔）')
    ap.add_argument('--status', default='', help='放行状态（留空则读本地 gen_status.json；--notion 可读外部表）')
    a = ap.parse_args()
    cfg = json.load(open(a.config))
    if cfg.get('root') in (None, '', '.'):
        cfg['root'] = os.path.dirname(os.path.abspath(a.config))
    sys.path.insert(0, cfg.get('mcp_tools', os.path.dirname(os.path.abspath(__file__))))

    if a.build_registry:
        if a.notion:
            build_registry_notion(cfg)
        else:
            build_registry_local(cfg)
        return

    if a.emit_prompt:
        if not a.shot:
            raise SystemExit('--emit-prompt 需要 --shot')
        if a.notion:
            seg_n = notion_seg(cfg, a.shot)
            assert seg_n, f'Notion 内容列无 {a.shot}'
            open(a.emit_prompt, 'w', encoding='utf-8').write(norm(seg_n))
            print(f'✓ 提示词已从 Notion 逐字取出 → {a.emit_prompt}（sha={sha(seg_n)[:16]}…）')
        else:
            seg = load_shot(cfg, a.shot)
            open(a.emit_prompt, 'w', encoding='utf-8').write(norm(seg))
            print(f'✓ 提示词已从本地镜块逐字写出 → {a.emit_prompt}（sha={sha(seg)[:16]}…）')
        return

    fails = []
    seg = load_shot(cfg, a.shot)
    prompt = open(a.prompt_file, encoding='utf-8').read()

    # G-PARITY ⑤
    if a.notion:
        seg_n = notion_seg(cfg, a.shot)
        if not seg_n:
            fails.append('G-PARITY: Notion 内容列无该镜（已启用 --notion）')
        elif sha(seg_n) != sha(seg):
            fails.append(f'G-PARITY: 本地镜块与 Notion 内容列不一致（{sha(seg)[:12]}≠{sha(seg_n)[:12]}）')
        else:
            print(f'G-PARITY ✓ 本地↔Notion 一致 sha={sha(seg)[:16]}…')
    else:
        if not seg.strip():
            fails.append('G-PARITY: 本地镜块为空——项目本地真相源缺失')
        else:
            print(f'G-PARITY ✓ 本地镜块为真相源 sha={sha(seg)[:16]}…')

    ref_ids = [r.strip() for r in a.ref_ids.split(',') if r.strip()]
    pol = cfg['model_policy']

    # G-VERBATIM ①
    if sha(prompt) != sha(seg):
        fails.append(f'G-VERBATIM: prompt 与镜块不一致（{sha(prompt)[:12]}≠{sha(seg)[:12]}）——禁压缩/改写/自创描述块')
    else:
        print(f'G-VERBATIM ✓ 逐字一致 sha={sha(seg)[:16]}…')

    # G-MODEL ②-长度
    if len(norm(seg)) > pol['prompt_limit']:
        fails.append(f'G-MODEL: 镜块 {len(seg)} 字超 {pol["prompt_limit"]} 上限——回本地分镜设计变更，禁止传输时压缩')
    for s in SECTIONS:
        if s not in prompt:
            fails.append(f'G-VERBATIM: 缺{s}')

    # G-REFBIND ③④
    reg_path = os.path.join(cfg['root'], 'asset_registry.json')
    if not os.path.isfile(reg_path):
        fails.append('G-REFBIND: 缺 asset_registry.json——先 --build-registry（本地）')
        reg = []
    else:
        reg = json.load(open(reg_path, encoding='utf-8'))['assets']
    META = {'引用', '完整描述', '资产锁', '双保险', '素材待建'}
    wants = [w for w in dict.fromkeys(re.findall(r'@([^\s：:，。、；;（）【】｜／/]+)', seg)) if w not in META and '引用' not in w]
    shot_size = re.search(r'景别：([^\s。：:]{1,3})', seg)
    shot_size = shot_size.group(1)[:2] if shot_size else ''
    expected = []
    for w in wants:
        cands = [r for r in reg if r['lock_name'] == w or name_match(w, r['file']) or name_match(w, r['lock_name'])]
        if not cands:
            fails.append(f'G-REFBIND: @{w} 在本地素材注册表无登记')
            continue
        pick = next((c for c in cands if c['state_keywords'] and re.search(c['state_keywords'], seg)), None)
        if not pick and shot_size:
            pick = next((c for c in cands if c['file'].replace('.png', '').endswith(f'-{shot_size}')), None)
        pick = pick or next((c for c in cands if not c['state_keywords']), None) or cands[0]
        expected.append(pick)
    exp_ids = [e['resource_id'] for e in expected if e.get('resource_id')]
    if ref_ids:
        miss = [e['file'] for e in expected if e.get('resource_id') and e['resource_id'] not in ref_ids]
        wrong = [i for i in ref_ids if i not in exp_ids]
        if miss:
            fails.append(f'G-REFBIND: 镜块 @素材 未绑定参考图: {miss}')
        if wrong:
            fails.append(f'G-REFBIND: 引用了镜块没写的素材（@取错/引用错误）: {wrong}')
        if not miss and not wrong:
            print(f'G-REFBIND ✓ {len(expected)} 个 @素材 ↔ 资源 ID 一一对应: {[(e["lock_name"], e["file"]) for e in expected]}')
    else:
        fails.append('G-REFBIND: 未提供 --ref-ids（生成调用实际引用）')

    # G-REVIEW ②（付费前审查——本地默认）
    st = a.status or load_local_status(cfg, a.shot)
    if not st and a.notion:
        rows = query_rows(cfg['notion']['storyboard_ds'], view=cfg['notion'].get('view'))
        st = next((x.get('状态') for x in rows if str(x.get('镜号')) in (a.shot, a.shot.replace('-', '-0'))), '')
    gate_val = cfg.get('status_gate', '生成中')
    if st != gate_val:
        fails.append(f'G-REVIEW: 状态={st or "空"}（须={gate_val}；写 gen_status.json 或传 --status）')
    else:
        print(f'G-REVIEW ✓ 状态={gate_val}（审查记录在案）')

    print(f'=== shot_gate {a.shot} ===')
    if fails:
        for f in fails: print('FAIL', f)
        print('✗ 硬闸未过——禁止生成'); sys.exit(1)
    print('✓ 全闸通过，可进入 quote→批→run')


if __name__ == '__main__':
    main()
