"""Artifact integrity checks and PDF rasterization for visual QA."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,argparse,subprocess
from PIL import Image,ImageDraw
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'work/validation';WORK.mkdir(parents=True,exist_ok=True)
items=json.loads((ROOT/'specs/catalog.json').read_text(encoding='utf-8'))
class PageLinks(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        for key in ['href','src']:
            if key in attrs:self.links.append(attrs[key])
def validate():
    n=0;pdfs=[];photos=json.loads((ROOT/'specs/photo_index.json').read_text(encoding='utf-8'));photoids={x['id'] for x in photos['reviewed']}
    for m in items:
        if m.get('photo'):assert m['photo'] in photoids,m['id']
        assert (ROOT/'docs'/m['slug']/'index.html').is_file()
        if not m['steps']:
            assert m['status']=='BLOCKED';assert not (ROOT/'pdf'/m['pdf']).exists();continue
        assert (ROOT/'blender'/f'{m["id"]}_visual_v2.blend').is_file()
        p=ROOT/'pdf'/m['pdf'];pdfs.append(p)
        assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256((ROOT/'docs/pdf'/p.name).read_bytes()).digest()
        reader=PdfReader(p);assert len(reader.pages)==len(m['steps']);assert len(reader.outline)==len(m['steps'])
        ad='control-sticks' if m['id']=='CTRL001' else m['id'].lower()
        for page,s in zip(reader.pages,m['steps']):
            assert list(map(float,page.mediabox))==[0,0,792,540]
            assert len(page.images)==1
            with Image.open(ROOT/'docs/assets/images'/ad/s['image']) as im:
                assert im.size==(4400,3000)
                assert hashlib.sha256(im.convert('RGB').tobytes()).digest()==hashlib.sha256(page.images[0].image.convert('RGB').tobytes()).digest(),m['id']
            n+=1
    idx=ROOT/'pdf/00_Manual_Index.pdf';r=PdfReader(idx);assert len(r.pages)==2
    assert hashlib.sha256(idx.read_bytes()).digest()==hashlib.sha256((ROOT/'docs/pdf'/idx.name).read_bytes()).digest()
    for m in items:assert m['id'] in ''.join(p.extract_text() for p in r.pages)
    pages={}
    for f in (ROOT/'docs').rglob('*.html'):
        p=PageLinks();p.feed(f.read_text(encoding='utf-8'));pages[f.resolve()]=p
    checked=0
    for f,p in pages.items():
        for href in p.links:
            u=urlsplit(href)
            if u.scheme or u.netloc:continue
            target=(f.parent/unquote(u.path)).resolve() if u.path else f
            if target.is_dir():target=target/'index.html'
            assert target.is_relative_to((ROOT/'docs').resolve()),(f,href,'escaped site root')
            assert target.exists(),(f,href,'missing target')
            if u.fragment and target in pages:assert unquote(u.fragment) in pages[target].ids,(f,href,'missing anchor')
            checked+=1
    queue=json.loads((ROOT/'specs/review_queue.json').read_text(encoding='utf-8'))
    assert len(queue)==sum(len(m['issues']) for m in items)
    assert len({r['key'] for r in queue})==len(queue),'Duplicate review identifiers'
    result=dict(manuals=len(pdfs),instruction_pages=n,index_pages=2,pdf_files=len(pdfs)+1,scope_sections=len(items),html_pages=len(pages),local_links_checked=checked,review_items=len(queue),largest_pdf_bytes=max(p.stat().st_size for p in pdfs),pixel_match=f'All {n} PDF instruction images exactly match released PNGs',errors=[])
    (WORK/'integrity.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
    return pdfs+[idx]
def render_pdf(p):
    prefix=WORK/p.stem
    subprocess.run(['pdftoppm','-scale-to','1200','-png',str(p),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def sheets():
    files=sorted(WORK.glob('*.png'));size=(800,565)
    for i in range(0,len(files),6):
        out=Image.new('RGB',(1600,1695),'#dde4e9');d=ImageDraw.Draw(out)
        for j,f in enumerate(files[i:i+6]):
            x=j%2*800;y=j//2*565
            with Image.open(f) as im:im.thumbnail((800,535));out.paste(im,(x,y+22))
            d.text((x+10,y+5),f.stem,fill='black')
        out.save(WORK/f'contact-{i//6:02d}.jpg',quality=91)
    print('QA_PAGES',len(files))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--render',action='store_true');args=parser.parse_args()
    pdfs=validate()
    if args.render:
        with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(render_pdf,pdfs))
        sheets()
