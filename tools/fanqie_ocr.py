#!/usr/bin/env python3
# 番茄小说抽取：目录抓取 + 章节正文 OCR（本地渲染站点字体绕过字形反爬）
# usage:
#   抓目录/直连抓取:  python3 -I fanqie_ocr.py <reader_url> [--out DIR] [--start N] [--end N] [--catalog-only]
#   从浏览器导出重建:  python3 -I fanqie_ocr.py --from-raw [--out DIR]   # 读 <out>/raw/batch-*.json
# deps: uv run --with fonttools --with brotli --with pillow python3 -I fanqie_ocr.py ...
#       以及 ocr-vision（macOS Vision OCR；OCR_VISION 环境变量指定路径，或放同目录；
#       编译：bash tools/build_ocr.sh（tools/ocr.swift → tools/ocr-vision））
# 注意: curl/urllib 直连会被番茄降级为 200 字试读（isChapterLock=true），必须用浏览器
#       页上下文 fetch 导出到 raw/batch-*.json 后走 --from-raw
#       （见 skills/novel-to-drama/references/browser-dump.md）
import argparse, glob, json, re, subprocess, sys, time, urllib.request, html as htmllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
FS, LH, WIDTH, MARGIN, MAX_IMG_H = 36, 56, 1400, 56, 1600  # OCR 召回实测最优参数

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")

def parse_state(html):
    i = html.find("window.__INITIAL_STATE__=")
    if i < 0:
        raise RuntimeError("page has no __INITIAL_STATE__ (maybe login/verify wall)")
    seg = html[i + len("window.__INITIAL_STATE__="):]
    depth = 0
    for j, ch in enumerate(seg):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    fixed = re.sub(r"\bundefined\b", "null", seg[:end])
    fixed = re.sub(r",\s*([}\]])", r"\1", fixed)
    return json.loads(fixed)

def get_font(state, out_dir):
    """页面 CSS 里的 subset 字体是按批次随机的，必须从页面动态取。"""
    css = state.get("common", {}).get("css", "")
    m = re.search(r"url\((https://[^)]+\.woff2)\)", css)
    if not m:
        raise RuntimeError("no @font-face woff2 in page css")
    dest = out_dir / "subset.woff2"
    req = urllib.request.Request(m.group(1), headers={"User-Agent": UA})
    dest.write_bytes(urllib.request.urlopen(req, timeout=25).read())
    otf = out_dir / "subset.otf"
    from fontTools.ttLib import TTFont
    f = TTFont(str(dest))
    f.flavor = None
    f.save(str(otf))
    return otf

def build_catalog(state):
    chapters = state["page"]["chapterListWithVolume"][0]
    cat = [{"itemId": str(c["itemId"]), "title": c["title"], "order": int(c["realChapterOrder"])}
           for c in chapters]
    cat.sort(key=lambda x: x["order"])
    return cat

def content_to_lines(content_html):
    text = re.sub(r"</p>", "\n", content_html)
    text = re.sub(r"<[^>]+>", "", text)
    text = htmllib.unescape(text)
    return [ln.strip() for ln in text.split("\n") if ln.strip()]

class Renderer:
    def __init__(self, subset_otf, out_dir):
        from PIL import ImageFont
        from fontTools.ttLib import TTFont
        self.pua = set(TTFont(str(subset_otf)).getBestCmap())
        self.f_sub = ImageFont.truetype(str(subset_otf), FS)
        fb = out_dir / "NotoSansSC-VF.ttf"  # 非 PUA 字渲染用，任意 CJK 字体即可
        if not fb.exists():
            url = "https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/Variable/TTF/Subset/NotoSansSC-VF.ttf"
            print("downloading NotoSansSC-VF.ttf ...")
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            fb.write_bytes(urllib.request.urlopen(req, timeout=120).read())
        self.f_fb = ImageFont.truetype(str(fb), FS)

    def font_of(self, ch):
        return self.f_sub if ord(ch) in self.pua else self.f_fb

    def render(self, lines, prefix, work):
        from PIL import Image, ImageDraw
        wrapped, limit = [], WIDTH - 2 * MARGIN
        for ln in lines:
            cur, w = "", 0.0
            for ch in ln:
                cw = self.font_of(ch).getlength(ch)
                if w + cw > limit and cur:
                    wrapped.append(cur)
                    cur, w = "", 0.0
                cur += ch
                w += cw
            if cur:
                wrapped.append(cur)
        paths, idx = [], 0
        rows = max(1, (MAX_IMG_H - 2 * MARGIN) // LH)
        while idx < len(wrapped) or not paths:
            chunk = wrapped[idx:idx + rows]
            img = Image.new("RGB", (WIDTH, min(MAX_IMG_H, 2 * MARGIN + len(chunk) * LH)), "white")
            d = ImageDraw.Draw(img)
            y = MARGIN
            for ln in chunk:
                x = MARGIN
                for ch in ln:
                    f = self.font_of(ch)
                    d.text((x, y), ch, font=f, fill="black")
                    x += f.getlength(ch)
                y += LH
            p = work / f"render-{prefix}-{len(paths)}.png"
            img.save(str(p))
            paths.append(p)
            idx += rows
            if not chunk:
                break
        return paths

def ocr(paths, ocr_bin):
    r = subprocess.run([str(ocr_bin)] + [str(p) for p in paths], capture_output=True, text=True)
    return r.stdout.replace("\f", "")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?", default="")
    ap.add_argument("--out", default=".")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=10**9)
    ap.add_argument("--catalog-only", action="store_true")
    ap.add_argument("--from-raw", action="store_true", help="从 <out>/raw/batch-*.json 重建（浏览器导出，绕过截断）")
    a = ap.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = out / ".work"
    work.mkdir(exist_ok=True)
    ocr_bin = Path(__import__("os").environ.get("OCR_VISION", HERE / "ocr-vision"))
    if not ocr_bin.exists():
        sys.exit("ocr-vision missing: set OCR_VISION to the macOS Vision OCR binary (built via tools/build_ocr.sh)")
    novel = out / "novel"
    novel.mkdir(exist_ok=True)

    if a.from_raw:
        cat = json.load(open(out / "catalog.json"))
        order_of = {c["itemId"]: c["order"] for c in cat}
        chapters = {}
        for f in glob.glob(str(out / "raw" / "batch-*.json")):
            if f.endswith("batches.json"):
                continue
            for item_id, v in json.load(open(f)).items():
                if "error" not in v:
                    chapters[item_id] = v
        print(f"raw chapters: {len(chapters)}")
        subset_otf = get_font(parse_state(http(f"https://fanqienovel.com/reader/{cat[0]['itemId']}")), work)
        renderer = Renderer(subset_otf, out)
        for item_id, order in sorted(order_of.items(), key=lambda x: x[1]):
            v = chapters.get(item_id)
            if not v:
                print(f"ch{order:03d} MISSING RAW")
                continue
            if a.start <= order <= a.end:
                dest = novel / f"ch{order:03d}.txt"
                expected = int(v.get("words") or 0)
                if dest.exists() and dest.stat().st_size > 400:
                    body_len = len(dest.read_text().split("\n\n", 1)[-1].strip())
                    if expected == 0 or body_len > expected * 0.6:
                        continue
                lines = content_to_lines(v["content"])
                paths = renderer.render(lines, f"ch{order:03d}", work)
                text = ocr(paths, ocr_bin)
                dest.write_text(f"# {v.get('title','')}\n# itemId={item_id} words={expected}\n\n{text.strip()}\n")
                for p in paths:
                    p.unlink(missing_ok=True)
                print(f"ch{order:03d} ok chars={len(text.strip())}")
        return

    if not a.url:
        sys.exit("need url (or --from-raw)")
    state = parse_state(http(a.url))
    if "chapterData" not in state.get("reader", {}):
        sys.exit("url is not a reader page; pass a /reader/<id> url")
    book_id = state["reader"]["chapterData"]["bookId"]
    book_state = parse_state(http(f"https://fanqienovel.com/page/{book_id}"))
    cat = build_catalog(book_state)
    (out / "catalog.json").write_text(json.dumps(cat, ensure_ascii=False, indent=1))
    meta = {k: book_state["page"].get(k) for k in ("bookName", "author", "wordNumber", "chapterTotal", "abstract")}
    (out / "book-meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"book: {meta['bookName']} / {meta['author']} / {meta['chapterTotal']}章")
    if a.catalog_only:
        return

    subset_otf = get_font(state, work)
    renderer = Renderer(subset_otf, out)
    for entry in cat:
        order = entry["order"]
        if order < a.start or order > a.end:
            continue
        dest = novel / f"ch{order:03d}.txt"
        if dest.exists() and dest.stat().st_size > 400:
            continue
        for attempt in range(3):
            try:
                st = parse_state(http(f"https://fanqienovel.com/reader/{entry['itemId']}"))["reader"]["chapterData"]
                break
            except Exception as e:
                print(f"ch{order:03d} retry: {e}")
                time.sleep(2 + 2 * attempt)
        else:
            print(f"ch{order:03d} FAILED")
            continue
        lines = content_to_lines(st.get("content", ""))
        paths = renderer.render(lines, f"ch{order:03d}", work)
        text = ocr(paths, ocr_bin)
        dest.write_text(f"# {st.get('title','')} # {entry['title']}\n# itemId={entry['itemId']} words={st.get('chapterWordNumber')}\n\n{text.strip()}\n")
        for p in paths:
            p.unlink(missing_ok=True)
        print(f"ch{order:03d} ok chars={len(text.strip())}")
        time.sleep(0.4)

if __name__ == "__main__":
    main()
