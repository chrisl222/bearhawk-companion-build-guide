"""Publish the catalog with stable routes, review status and shared illustrations.

python scripts/publish_all.py             # new PDFs, index PDF, web + queue
python scripts/publish_all.py --web-only  # web + queue without PDF changes
python scripts/publish_all.py --ids ID... # only selected PDFs, then refresh indexes
CTRL001's approved PDF is preserved unless explicitly released with publish.py.
"""
from pathlib import Path
import argparse,json,html,shutil,hashlib
from urllib.parse import quote
from collections import Counter
from PIL import Image
from publish import release,favicon
ROOT=Path(__file__).resolve().parents[1]
E=html.escape

def catalog():return json.loads((ROOT/'specs/catalog.json').read_text(encoding='utf-8'))
def assetdir(m):return 'control-sticks' if m['id']=='CTRL001' else m['id'].lower()
def badge(m):return f'<span class="status {m["status"].lower().replace(" ","-")}">{E(m["status"])}</span>'
def review_items(items):
    result=[]
    for m in items:
        for issue in m['issues']:
            result.append(dict(manual=m['id'],number=m['number'],title=m['title'],status=m['status'],slug=m['slug'],**issue))
    return result
def head(title,base=''):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · Bearhawk Companion</title><link rel="stylesheet" href="{base}assets/css/manual.css">{favicon()}</head>'
def bar(base='',action=''):
    return f'<header class="bar"><a class="brand" href="{base}index.html">BEARHAWK <span>COMPANION</span></a>{action}</header>'
def footer(base=''):
    return f'<footer>ILLUSTRATIVE — NOT TO SCALE<br>Companion plans control design. Current Companion count sheet controls explicit QB hardware.<br><a href="{base}review/index.html">Human review queue</a> · <a href="{base}photos/index.html">Photo references</a> · <a href="{base}references/index.html">Beartracks / factory alerts</a> · <a href="{base}index.html">Contents</a></footer>'
def reviewed_links(m,base):
    ids=[m['photo']] if m.get('photo') else []
    if m['id']=='WING005':ids.append('G3-FLAP-ROD')
    if m['id']=='WING003':ids.append('G3-AILERON-CRANK')
    if m['id']=='FINAL001':ids.append('G3-LIFT-STRUT')
    if m['id'] in ['GEAR001','GEAR002']:ids.append('BT24-COMPANION-GEAR')
    if m['id'] in ['CTRL002','GEAR004']:ids.append('FACTORY-BRAKE-STOP')
    if m['id']=='CTRL004':ids.append('FACTORY-AFT-PULLEY')
    if m['id'] in ['WING006','WING007']:ids.append('BT22-HINGE-FIT')
    if m['section']=='empennage' and m['steps']:ids+=['FM13-TAIL','FM15-HINGES']
    return ' · '.join(f'<a href="{base}photos/index.html#{E(id)}">{E(id)}</a>' for id in dict.fromkeys(ids)) or 'No applicable installation photograph established.'

def publish_queue(items):
    issues=review_items(items)
    text=['# Human review required','',f'{len(issues)} open items across {len(items)} attempted scope entries. No items have been silently resolved.','',
      'RELEASED means the limited illustrated operation has no recorded source conflict; it is not an aircraft airworthiness or final rigging approval. REVIEW REQUIRED manuals show supported relationships with unresolved operations explicitly identified. BLOCKED entries have no installation PDF.','',
      'New illustrations show fastener axes and a hardware inventory. Where an installed washer/bushing stack is unresolved, the inventory is not stack order. Do not infer drill coordinates, dimensions, grip length, torque, cable lengths or rigging settings from a scene.','']
    for r in issues:
        text += [f'## {r["key"]} — {r["manual"]}: {r["title"]}',f'- Manual / step: {r["number"]:02d} / {r["steps"]}',f'- Status: {r["status"]}',f'- Issue: {r["issue"]}',f'- Source / missing information: {r["source"]}',f'- Human check required: {r["check"]}','']
    (ROOT/'HUMAN_REVIEW_REQUIRED.md').write_text('\n'.join(text).rstrip()+'\n',encoding='utf-8')
    (ROOT/'specs/review_queue.json').write_text(json.dumps(issues,indent=2,ensure_ascii=False),encoding='utf-8')
    path=ROOT/'docs/review';path.mkdir(exist_ok=True)
    cards=[]
    for r in issues:
        cards.append(f'<article class="review-item" id="{r["key"]}"><p class="eyebrow">{r["key"]} · STEP {E(r["steps"])} · {E(r["status"])}</p><h2><a href="../{E(r["slug"])}/index.html">{r["number"]:02d} {E(r["title"])}</a></h2><p>{E(r["issue"])}</p><p class="hint"><strong>Source / gap:</strong> {E(r["source"])}</p><p><strong>Check:</strong> {E(r["check"])}</p></article>')
    (path/'index.html').write_text(head('Human review','../')+'<body>'+bar('../')+f'<main class="contents"><p class="eyebrow">PRIMARY BUILD · OPEN ITEMS</p><h1>Human review</h1><p>{len(issues)} items. Resolve the listed source or kit question before completing the affected operation.</p>'+''.join(cards)+footer('../')+'</main></body></html>',encoding='utf-8')
    return issues

def publish_photos():
    data=json.loads((ROOT/'specs/photo_index.json').read_text(encoding='utf-8'))
    def ref(s):
        first,*rest=s.split(' | ',1)
        return (f'<a href="{E(first)}" target="_blank" rel="noopener">Open reference ↗</a>'+(' · '+E(rest[0]) if rest else '')) if first.startswith('https://') else E(s)
    cards=[]
    for r in data['reviewed']:
        cards.append(f'<article class="review-item" id="{E(r["id"])}"><p class="eyebrow">{E(r["id"])} · {E(r["subsystem"])}</p><h2>{E(r["model"])}</h2><p>{ref(r["reference"])}</p><p>{E(r["detail"])}</p><p class="hint">{E(r["applicability"])}</p></article>')
    candidates=''.join(f'<li>{E(r["gallery"])} · <a href="{E(r["reference"])}">{E(r["name"])}</a> · {E(r["subsystem"])} — not opened</li>' for r in data['candidates'])
    path=ROOT/'docs/photos';path.mkdir(exist_ok=True)
    (path/'index.html').write_text(head('Photo references','../')+'<body>'+bar('../')+'<main class="contents"><p class="eyebrow">SELECTIVE GALLERY INDEX</p><h1>Photo references</h1><p>Photos establish appearance and orientation only. They do not establish critical specifications or hardware identity. Gallery 1 is Five; the other gallery model labels are unknown. Only localized relationships supported by Companion plans are used.</p>'+''.join(cards)+'<h2>Indexed candidates</h2><p>Open only when relevant. Folder indexing does not mean the images were reviewed.</p><ul>'+candidates+'</ul>'+footer('../')+'</main></body></html>',encoding='utf-8')

def publish_references():
    data=json.loads((ROOT/'specs/beartracks_index.json').read_text(encoding='utf-8'))
    cards=[]
    md=['# Beartracks and factory reference index','',f'Reviewed {data["review_date"]}. {len(data["files"])} supplied PDFs / {sum(f["pages"] for f in data["files"])} PDF sheets.','',data['scope'],'',data['authority'],'','## Coverage','']
    for f in data['files']:md.append(f'- {f["file"]}: {f["pages"]} PDF sheets. {f["screening"]}')
    md+=['','## References and dispositions','']
    for r in data['references']:
        url=f'<p><a href="{E(r["url"])}" target="_blank" rel="noopener">Open factory alert ↗</a></p>' if r.get('url') else ''
        cards.append(f'<article class="review-item" id="{E(r["id"])}"><p class="eyebrow">{E(r["id"])} · {E(r["topic"])}</p><h2>{E(r["decision"])}</h2><p><strong>{E(r["source"])}</strong></p><p class="hint">Model: {E(r["model"])}</p><p>{E(r["summary"])}</p>{url}</article>')
        md += [f'### {r["id"]}',f'- Source: {r["source"]}',f'- Model / topic: {r["model"]} / {r["topic"]}',f'- Use: {r["decision"]}. {r["summary"]}']
        if r.get('url'):md.append(f'- Factory source: {r["url"]}')
        md.append('')
    (ROOT/'BEARTRACKS_INDEX.md').write_text('\n'.join(md).rstrip()+'\n',encoding='utf-8')
    p=ROOT/'docs/references';p.mkdir(exist_ok=True)
    page=head('Beartracks and factory alerts','../')+'<body>'+bar('../')+'<main class="contents"><p class="eyebrow">SUPPLEMENTAL SOURCES · 2026-09-13 REVIEW</p><h1>Beartracks &amp;<br>factory alerts</h1><p>10 supplied PDFs · 409 PDF sheets screened · 32 selected references.</p><p class="scope-note">Original newsletters stay in your reference library. Page numbers identify both the combined PDF sheet and printed issue page where available. This selective index is not a complete aircraft compliance audit.</p><p>Current factory alerts are linked directly. Manufacturer alert identifiers are reproduced as published. Historical notices and builder examples do not automatically apply to the Companion.</p><nav class="jump"><a href="#FACTORY-AD002">Brake cylinders</a><a href="#FACTORY-AD004">Flap pulley</a><a href="#FACTORY-OA001">Gear spread</a><a href="#FACTORY-OA002">Flap-speed conflict</a></nav>'+''.join(cards)+footer('../')+'</main></body></html>'
    (p/'index.html').write_text(page,encoding='utf-8')

def publish_web():
    items=catalog();issues=publish_queue(items);publish_photos();publish_references()
    for ix,m in enumerate(items):
        route=ROOT/'docs'/m['slug'];route.mkdir(parents=True,exist_ok=True)
        base='../'*len(Path(m['slug']).parts)
        images=ROOT/'docs/assets/images'/assetdir(m)
        pdfhref=base+'pdf/'+quote(m['pdf'])
        action=f'<a class="pdf" href="{pdfhref}" download>Download PDF ↓</a>' if m['steps'] else ''
        refs=[r for r in issues if r['manual']==m['id']]
        reviewnav=''.join(f'<li><a href="{base}review/index.html#{r["key"]}">{r["key"]}</a> · {E(r["issue"])}</li>' for r in refs)
        figures=[]
        for s in m['steps']:
            n=s['number'];path=images/s['image'];preview=path.with_suffix('.webp')
            if not preview.exists() or preview.stat().st_mtime<path.stat().st_mtime:
                with Image.open(path) as im:im.thumbnail((1800,1800));im.convert('RGB').save(preview,quality=90,method=6)
            full=base+'assets/images/'+assetdir(m)+'/'+quote(path.name)
            small=base+'assets/images/'+assetdir(m)+'/'+quote(preview.name)
            prev=f'<a href="#step-{n-1}">← Previous step</a>' if n>1 else f'<a href="{base}index.html">← Contents</a>'
            nex=f'<a href="#step-{n+1}">Next step →</a>' if n<len(m['steps']) else '<a href="#top">Back to top ↑</a>'
            figures.append(f'<figure class="step" id="step-{n}"><figcaption><span>{n:02d} / {len(m["steps"]):02d}</span><h2>{E(s["title"].capitalize())}</h2><a href="{full}" target="_blank" rel="noopener">Full size ↗</a></figcaption><a class="page-image" href="{full}" target="_blank" rel="noopener" aria-label="Zoom step {n}"><img src="{small}" width="1800" height="1227" alt="Step {n}: {E(s["title"].capitalize())}. Assembly, hardware and source flags." loading="{"eager" if n==1 else "lazy"}" decoding="async"></a><nav class="step-nav" aria-label="Step {n}">{prev}<span>{n} of {len(m["steps"])}</span>{nex}</nav></figure>')
        jump=''.join(f'<a href="#step-{s["number"]}">{s["number"]:02d}</a>' for s in m['steps'])
        scope=('<p class="scope-note">Supported relationships are illustrated. Resolve the <a href="#review">open items below</a> before completing affected operations. Hardware inventories do not specify unresolved stack order.</p>' if refs and m['steps'] else '<p class="scope-note">No installation PDF: controlling information is insufficient for this operation.</p>' if not m['steps'] else '')
        if m.get('before_build'):
            scope+='<section class="scope-note"><h2>Before this operation</h2>'+''.join(f'<p>{E(t)}</p>' for t in m['before_build'])+'</section>'
        nav=[]
        if ix:nav.append(f'<a href="{base}{E(items[ix-1]["slug"])}/index.html">← {items[ix-1]["number"]:02d} {E(items[ix-1]["title"])}</a>')
        if ix<len(items)-1:nav.append(f'<a href="{base}{E(items[ix+1]["slug"])}/index.html">{items[ix+1]["number"]:02d} {E(items[ix+1]["title"])} →</a>')
        page=head(m['title'],base)+'<body id="top"><a class="skip" href="#steps">Skip to steps</a>'+bar(base,action)
        page+=f'<main class="manual"><div class="assembly-heading"><p class="eyebrow">{m["number"]:02d} · {E(m["section"].upper())} · {m["id"]} · v{m["revision"]}</p><h1>{E(m["title"])}</h1>{badge(m)}{scope}<p class="hint">Tap an illustration for full-size viewing.</p><nav class="jump" aria-label="Jump to step">{jump}</nav></div><div id="steps">'+''.join(figures)+'</div>'
        if refs:page+='<section class="source-panel" id="review"><h2>Open items</h2><ul>'+reviewnav+'</ul></section>'
        supplemental=' · '.join(f'<a href="{base}references/index.html#{E(id)}">{E(id)}</a>' for id in m.get('supplements',[]))
        if supplemental:page+='<section class="source-panel"><h2>Beartracks / factory updates</h2><p>'+supplemental+'</p></section>'
        page+='<details class="source-panel"><summary>Sources and visual references</summary><ul>'+''.join(f'<li>{E(s)}</li>' for s in m['sources'])+'</ul><p>'+reviewed_links(m,base)+'</p></details><nav class="manual-nav" aria-label="Manual navigation">'+''.join(nav)+'</nav>'+footer(base)+'</main></body></html>'
        (route/'index.html').write_text(page,encoding='utf-8')
    counts=Counter(m['status'] for m in items)
    rows=[]
    for m in items:
        pdf=f'<a href="pdf/{quote(m["pdf"])}" download>PDF ↓</a>' if m['steps'] else '<span class="hint">No PDF</span>'
        rows.append(f'<li class="manual-row"><span class="manual-number">{m["number"]:02d}</span><div><a class="manual-title" href="{E(m["slug"])}/index.html">{E(m["title"])}</a><p class="hint">{m["id"]} · {len(m["steps"])} steps · v{m["revision"]}</p></div><div class="row-status">{badge(m)}{pdf}</div></li>')
    intro=f'<p>{sum(bool(m["steps"]) for m in items)} individual manuals · {sum(len(m["steps"]) for m in items)} instruction pages · {len(items)} scope entries</p><p class="hint">{counts["RELEASED"]} released · {counts["REVIEW REQUIRED"]} review required · {counts["BLOCKED"]} blocked</p>'
    content=head('Visual build guide')+'<body>'+bar('', '<a class="pdf" href="pdf/00_Manual_Index.pdf" download>Download index ↓</a>')+'<main class="contents"><p class="eyebrow">PRIMARY BUILD · VISUAL INSTRUCTIONS</p><h1>Bearhawk Companion<br>Visual Build Guide</h1>'+intro+'<p class="scope-note">Review status applies to each illustrated operation. This guide does not release unresolved hardware, drilling or final rigging. <a href="review/index.html">Open the consolidated review queue</a>.</p><nav class="jump"><a href="review/index.html">Human review</a><a href="photos/index.html">Photo index</a></nav><ol class="manual-list">'+''.join(rows)+'</ol>'+footer()+'</main></body></html>'
    (ROOT/'docs/index.html').write_text(content,encoding='utf-8');(ROOT/'docs/.nojekyll').touch()
    content=content.replace('<ol class="manual-list">','<section class="scope-note"><strong>Beartracks review added:</strong> check the <a href="references/index.html#FACTORY-AD002">brake-cylinder alert</a>, <a href="references/index.html#FACTORY-AD004">aft flap-pulley alert</a>, <a href="references/index.html#FACTORY-OA001">gear-spread guidance</a>, and <a href="references/index.html#FACTORY-OA002">flap-speed source conflict</a>.</section><ol class="manual-list">')
    (ROOT/'docs/index.html').write_text(content,encoding='utf-8')
    print('WEB',len(items),'sections;',len(issues),'review items')

def index_pdf():
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.colors import HexColor
    items=catalog();p=ROOT/'pdf/00_Manual_Index.pdf'
    c=Canvas(str(p),pagesize=(792,540),pageCompression=1,invariant=1)
    c.setTitle('Bearhawk Companion - Primary Build Manual Index');c.setAuthor('Bearhawk Companion Visual Build Guide')
    for page in range(2):
        c.setFillColor(HexColor('#172C3C'));c.setFont('Helvetica-Bold',24);c.drawString(36,502,'BEARHAWK COMPANION')
        c.setFont('Helvetica',15);c.drawString(36,479,'Primary build - individual manual index')
        counts=Counter(m['status'] for m in items)
        c.setFont('Helvetica',9);c.drawString(36,459,f'{sum(bool(m["steps"]) for m in items)} manuals / {sum(len(m["steps"]) for m in items)} instruction pages. {counts["RELEASED"]} RELEASED / {counts["REVIEW REQUIRED"]} REVIEW REQUIRED / {counts["BLOCKED"]} BLOCKED.')
        c.drawString(36,444,'Open HUMAN_REVIEW_REQUIRED.md or the website review queue before completing flagged operations.')
        xs=[36,66,374,447,498,549]
        c.setFont('Helvetica-Bold',9)
        for x,t in zip(xs,['NO.','MANUAL','ID','REV.','PAGES','STATUS']):c.drawString(x,419,t)
        for j,m in enumerate(items[page*18:(page+1)*18]):
            y=396-j*19
            c.setStrokeColor(HexColor('#D4DDE3'));c.line(36,y-6,756,y-6)
            vals=[f'{m["number"]:02d}',m['title'],m['id'],f'v{m["revision"]}',str(len(m['steps'])) if m['steps'] else '-',m['status']]
            for k,(x,t) in enumerate(zip(xs,vals)):
                size=9 if k!=5 else 8
                if k==1:
                    while c.stringWidth(t,'Helvetica',size)>300:size-=.25
                c.setFillColor(HexColor('#9B3C12' if m['status']!='RELEASED' and k==5 else '#172C3C'))
                c.setFont('Helvetica',size);c.drawString(x,y,t)
            if m['steps']:c.linkURL(quote(m['pdf']),(66,y-4,368,y+11),relative=1,thickness=0)
        c.setFillColor(HexColor('#596976'));c.setFont('Helvetica',8)
        c.drawString(36,28,'ILLUSTRATIVE - NOT TO SCALE. Plans / current Companion QB callout control. Review status is not airworthiness approval.')
        c.drawRightString(756,28,f'INDEX v3 / {page+1:02d}');c.showPage()
    c.save();shutil.copyfile(p,ROOT/'docs/pdf'/p.name)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--web-only',action='store_true');parser.add_argument('--ids',nargs='*');args=parser.parse_args()
    if not args.web_only:
        for m in catalog():
            if m['steps'] and m['id']!='CTRL001' and (not args.ids or m['id'] in args.ids):
                release(ROOT/'docs/assets/images'/assetdir(m)/'assembly.json',pdf_only=True)
        index_pdf()
    publish_web()
if __name__=='__main__':main()
