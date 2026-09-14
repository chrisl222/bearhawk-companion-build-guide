"""Local-only batch ingestion. Importing never publishes; approval is explicit metadata."""
from pathlib import Path
import argparse,json,hashlib,shutil,re
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
from PIL import Image,ImageOps
from photo_library import DATA,ROOT,MODELS,SOURCE_TYPES,CLASSIFICATIONS,validate_metadata

IMAGE_EXT={'.jpg','.jpeg','.png','.webp','.tif','.tiff','.bmp','.heic'}
def dump(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def contained(root,relative):
    path=(root/relative).resolve()
    if not path.is_relative_to(root.resolve()):raise ValueError('Path leaves the source folder: '+str(relative))
    return path
def batch_dir(out):
    out=Path(out).resolve()
    if out.is_relative_to((ROOT/'docs').resolve()):raise ValueError('Stage imports outside the public docs directory.')
    out.mkdir(parents=True,exist_ok=False);(out/'originals').mkdir();return out
def draft(file,original,source,args,**extra):
    data=file.read_bytes();digest=hashlib.sha256(data).hexdigest()
    return dict(id='import-'+hashlib.sha256((args.source_name+'|'+original).encode()).hexdigest()[:16],image='',thumbnail='',originalImage='',title='',caption='',whyUseful='',aircraftModel='Unknown',aircraftSerial='',builder=args.builder or '',section='',subsystem='',component='',buildStage='Unknown',viewpoint=[],tags=[],sourceType=args.source_type,sourceName=args.source_name,sourceUrl=args.source_url or '',sourceDocument=source,sourcePage='',originalFilename=file.name,originalPath=original,originalCaption='',authorityLevel=None,stockOrModified='Unknown',classification='UNKNOWN',applicabilityNotes='',copyrightNotes='',rightsBasis='',reviewStatus='pending',humanReviewer='',reviewedBy='',reviewedAt='',reviewNotes='',evidence=[],guideIds=[],category='',sha256=digest,stagedPath='originals/'+original,**extra)
class ContextParser(HTMLParser):
    def __init__(self):super().__init__();self.images=[];self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag.lower()=='img' and a.get('src'):self.images.append({'src':a['src'],'alt':a.get('alt',''),'title':a.get('title','')})
    def handle_data(self,data):
        if data.strip():self.text.append(data.strip())
def directory(args):
    src=Path(args.source).resolve();out=batch_dir(args.out);records=[];contexts=[];hashes={}
    if not src.is_dir():raise ValueError('Expected an existing source directory')
    if out.is_relative_to(src):raise ValueError('Batch output must be outside the source directory')
    for file in sorted(src.rglob('*')):
        if not file.is_file():continue
        rel=file.relative_to(src).as_posix();contained(src,rel)
        ext=file.suffix.lower()
        if ext not in IMAGE_EXT|{'.htm','.html'}:continue
        target=contained(out/'originals',rel);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(file,target)
        if ext in {'.html','.htm'}:
            parser=ContextParser();parser.feed(file.read_text(encoding='utf-8',errors='replace'))
            contexts.append({'originalHtmlPath':rel,'images':parser.images,'contextText':'\n'.join(parser.text)})
        else:
            r=draft(file,rel,src.name,args)
            if r['sha256'] in hashes:r['duplicateOf']=hashes[r['sha256']]
            else:hashes[r['sha256']]=r['id']
            records.append(r)
    bypath={r['originalPath']:r for r in records}
    for context in contexts:
        parent=Path(context['originalHtmlPath']).parent
        for image in context['images']:
            parsed=urlsplit(image['src'])
            if parsed.scheme or parsed.netloc:continue
            try:relative=contained(src,parent/unquote(parsed.path)).relative_to(src).as_posix()
            except ValueError:continue
            if relative in bypath:
                r=bypath[relative];r.setdefault('htmlContexts',[]).append(dict(index=context['originalHtmlPath'],alt=image['alt'],title=image['title']))
                if image['alt'] and not r['originalCaption']:r['originalCaption']=image['alt']
    dump(out/'context.json',contexts);dump(out/'manifest.json',records)
    print(f'Staged {len(records)} images and {len(contexts)} HTML indexes. All records NEED REVIEW. Nothing published.')
def pdf(args):
    from pypdf import PdfReader
    src=Path(args.source).resolve();out=batch_dir(args.out);reader=PdfReader(src);records=[];contexts=[];seen={}
    pages=list(range(1,len(reader.pages)+1)) if not args.pages else [int(n) for n in args.pages.split(',')]
    for n in pages:
        if n<1 or n>len(reader.pages):raise ValueError('PDF page outside document')
        page=reader.pages[n-1];contexts.append({'document':src.name,'page':n,'contextText':page.extract_text()})
        for index,obj in enumerate(page.images):
            if min(obj.image.size)<args.min_size:continue
            original=f'{src.stem}/page-{n:04}/{index:03}-{Path(obj.name).name}'
            target=contained(out/'originals',original);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(obj.data)
            r=draft(target,original,src.name,args);r['originalFilename']=obj.name;r['sourcePage']=f'PDF p{n}';r['width'],r['height']=obj.image.size
            r['evidence']=[{'type':'source-document-sha256','reference':hashlib.sha256(src.read_bytes()).hexdigest()}]
            if r['sha256'] in seen:r['duplicateOf']=seen[r['sha256']]
            else:seen[r['sha256']]=r['id']
            records.append(r)
    dump(out/'manifest.json',records);dump(out/'context.json',contexts)
    print(f'Staged {len(records)} PDF images. All records NEED REVIEW. Nothing published.')
def publish(args):
    batch=Path(args.batch).resolve();records=json.loads((batch/'manifest.json').read_text(encoding='utf-8'))
    accepted=[r for r in records if r['reviewStatus']=='approved'];published=json.loads((DATA/'photos.json').read_text(encoding='utf-8'))
    ids={p['id'] for p in published};hashes={p['sha256'] for p in published};categories={c['id']:c for c in json.loads((DATA/'taxonomy.json').read_text())}
    ready=[]
    for r in accepted:
        if r.get('duplicateOf') or r['sha256'] in hashes:continue
        if r['id'] in ids:raise ValueError('ID already published: '+r['id'])
        if not re.fullmatch(r'[a-z0-9-]+',r['id']):raise ValueError('Invalid identifier')
        if not r.get('humanReviewer') or not r.get('reviewedAt') or not r.get('reviewNotes'):raise ValueError('Human review is required')
        if r['category'] not in categories:raise ValueError('Choose a valid category')
        if any(r[k]!=categories[r['category']][k] for k in ['section','subsystem','component']):raise ValueError('Category labels do not match')
        if not r.get('rightsBasis') or not r.get('copyrightNotes'):raise ValueError('Image-use rights must be recorded')
        file=contained(batch,r['stagedPath'])
        if hashlib.sha256(file.read_bytes()).hexdigest()!=r['sha256']:raise ValueError('Source image hash changed')
        with Image.open(file) as image:image.verify()
        p={k:v for k,v in r.items() if k not in ['stagedPath','htmlContexts','duplicateOf']};p['reviewedBy']=r['humanReviewer']
        rel='assets/photos/'+r['id'];p['image']=rel+'/image.webp';p['thumbnail']=rel+'/thumb.webp';p['originalImage']=rel+'/original'+file.suffix.lower()
        with Image.open(file) as image:p['width'],p['height']=ImageOps.exif_transpose(image).size
        validate_metadata(p)
        ready.append((p,file));ids.add(p['id']);hashes.add(p['sha256'])
    # Validate the entire accepted batch before changing the published library.
    for p,file in ready:
        dest=ROOT/'docs/assets/photos'/p['id'];dest.mkdir(parents=True,exist_ok=False);shutil.copy2(file,ROOT/'docs'/p['originalImage'])
        with Image.open(file) as image:
            im=ImageOps.exif_transpose(image).convert('RGB');im.thumbnail((2200,2200));im.save(dest/'image.webp',quality=92,method=6);im.thumbnail((640,480));im.save(dest/'thumb.webp',quality=85,method=6)
        published.append(p)
    dump(DATA/'photos.json',published)
    print(f'Added {len(ready)} human-approved images. Run publish_all.py --web-only to rebuild pages. Pending records were excluded.')
def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    for name in ['directory','pdf']:
        p=sub.add_parser(name);p.add_argument('source');p.add_argument('--out',required=True);p.add_argument('--source-name',required=True);p.add_argument('--source-type',choices=SOURCE_TYPES,default='Other');p.add_argument('--source-url',default='');p.add_argument('--builder',default='')
        if name=='pdf':p.add_argument('--pages');p.add_argument('--min-size',type=int,default=100)
    p=sub.add_parser('publish-reviewed');p.add_argument('batch')
    args=parser.parse_args();{'directory':directory,'pdf':pdf,'publish-reviewed':publish}[args.command](args)
if __name__=='__main__':main()
