"""Build the integrated, progressively enhanced photo library from reviewed metadata."""
from pathlib import Path
import json,html,re,hashlib
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'specs/photo-library'
E=html.escape
MODELS=['Companion','Four','Patrol','Five','Unknown']
SOURCE_TYPES=['Designer / Plans','Bearhawk Factory','Beartracks','Builder Manual','Builder Log','Bearhawk Forum','Photo Gallery','Other']
CLASSIFICATIONS=['SPECIFIED','STANDARD PRACTICE','COMMON BUILDER PRACTICE','INDIVIDUAL BUILDER SOLUTION','MODIFICATION','INFERENCE','UNKNOWN']
NOTICE='PHOTO REFERENCE ONLY — verify dimensions, hardware, and structural details against controlling Bearhawk documentation.'
def read(name):return json.loads((DATA/name).read_text(encoding='utf-8'))
def public_photos():return [p for p in read('photos.json') if p['reviewStatus'] in ['curated','approved']]
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def photo_route(p):return f'photos/image/{p["id"]}/index.html'
def guides(p,base,manuals):
    return ''.join(f'<a href="{base}{E(manuals[i]["slug"])}/index.html">{E(manuals[i]["title"])} →</a> ' for i in p['guideIds'] if i in manuals)
def guide_link(m,base):
    photos=[p for p in public_photos() if m['id'] in p['guideIds']]
    if not photos:return ''
    categories={p['category'] for p in photos}
    target='photos/'+next(iter(categories))+'/index.html' if len(categories)==1 else 'photos/index.html?guide='+m['id']
    return f'<section class="source-panel"><h2>See the real installation</h2><a href="{base}{E(target)}">View {len(photos)} reference photos →</a><p class="hint">Model and source are shown on every photo. Photos supply visual context only.</p></section>'
def card(p,base):
    model={'Four':'FOUR-PLACE','Unknown':'MODEL UNKNOWN'}.get(p['aircraftModel'],p['aircraftModel'].upper())
    badge='LEGACY' if p['authorityLevel']==3 else {'Beartracks':'BEARTRACKS','Bearhawk Factory':'FACTORY','Designer / Plans':'DESIGNER','Bearhawk Forum':'FORUM'}.get(p['sourceType'],'BUILDER')
    source_link=f'<a href="{E(p["sourceUrl"])}" target="_blank" rel="noopener">View original source ↗</a>' if p['sourceUrl'] else ''
    return f'''<article class="photo-card" data-photo="{E(p['id'])}"><a class="photo-open" href="{base}{photo_route(p)}" data-open="{E(p['id'])}"><div class="photo-frame"><img src="{base}{E(p['thumbnail'])}" width="{p['width']}" height="{p['height']}" alt="{E(p['title'])}" loading="lazy"><span class="enlarge">View photo ↗</span></div><div class="photo-copy"><div class="photo-badges"><span class="model">{model}</span><span>{badge}</span></div><p class="photo-builder">{E(p['builder'])}</p><h3>{E(p['title'])}</h3></div></a><div class="photo-copy photo-context"><p>{E(p['whyUseful'])}</p><p class="photo-category">{E(p['subsystem'])} / {E(p['component'])}</p><p class="photo-source">{E(p['sourceName'])} · {E(p['sourcePage'])}<br>{source_link}</p><div class="photo-tags">{''.join('<span>'+E(t)+'</span>' for t in p['tags'][:3])}</div><p class="photo-applicability">{'Companion builder example; verify your configuration.' if p['aircraftModel']=='Companion' else 'Model unknown · Companion applicability unverified.' if p['aircraftModel']=='Unknown' else E(p['aircraftModel'])+' example · verify Companion applicability.'}</p></div></article>'''
def detail(p,base,manuals):
    source=f'<a href="{E(p["sourceUrl"])}" target="_blank" rel="noopener">View original source ↗</a>' if p['sourceUrl'] else 'Project-provided document; no public source URL established.'
    return f'''<div class="photo-detail-image"><a href="{base}{E(p['originalImage'])}" target="_blank" rel="noopener"><img src="{base}{E(p['image'])}" alt="{E(p['title'])}" width="{p['width']}" height="{p['height']}"></a><p>{p['width']} × {p['height']} source pixels · <a href="{base}{E(p['originalImage'])}" target="_blank" rel="noopener">Open original-size image ↗</a></p></div><div class="photo-detail-copy"><p class="eyebrow">{E(p['aircraftModel'])} · {E(p['sourceType'])}</p><h1 id="photo-title">{E(p['title'])}</h1><p>{E(p['whyUseful'])}</p><p class="scope-note">{E(p['applicabilityNotes'])}</p><dl><dt>Builder / source</dt><dd>{E(p['builder'])} · {E(p['sourceName'])}</dd><dt>Component</dt><dd>{E(p['section'])} / {E(p['subsystem'])} / {E(p['component'])}</dd><dt>Stage / viewpoint</dt><dd>{E(p['buildStage'])} / {E(', '.join(p['viewpoint']) or 'Not recorded')}</dd><dt>Classification / configuration</dt><dd>{E(p['classification'])} / {E(p['stockOrModified'])}</dd><dt>Document / page</dt><dd>{E(p['sourceDocument'])} · {E(p['sourcePage'])}</dd><dt>Original caption</dt><dd>{E(p['originalCaption'] or 'No unambiguous image-specific caption transcribed; see the source page.')}</dd><dt>Original filename / directory</dt><dd>{E(p['originalFilename'])}<br>{E(p['originalPath'])}</dd><dt>Source link</dt><dd>{source}</dd><dt>Tags</dt><dd>{E(', '.join(p['tags']))}</dd><dt>Attribution</dt><dd>{E(p['copyrightNotes'])}</dd></dl><p class="hint">{NOTICE}</p><div class="related-guides">{guides(p,base,manuals)}</div><p><a href="{base}photos/{E(p['category'])}/index.html">More {E(p['component'].lower())} photos →</a></p></div>'''
def select(name,label,values):
    return f'<label>{E(label)}<select name="{name}" id="filter-{name}"><option value="">All {E(label.lower())}</option>'+''.join(f'<option value="{E(v)}">{E("Four-Place" if v=="Four" else "Other / Unknown" if v=="Unknown" else v)}</option>' for v in values)+'</select></label>'
def validate_metadata(p):
    """Validate the schema constraints used here without a runtime dependency."""
    def check(value,rule,path):
        types={'string':str,'object':dict,'array':list,'integer':int}
        if 'type' in rule and not isinstance(value,types[rule['type']]):raise ValueError(path+': incorrect type')
        if 'enum' in rule and value not in rule['enum']:raise ValueError(path+': unsupported value')
        if isinstance(value,str):
            if len(value)<rule.get('minLength',0):raise ValueError(path+': missing text')
            if 'pattern' in rule and not re.search(rule['pattern'],value):raise ValueError(path+': invalid format')
        if isinstance(value,int):
            if value<rule.get('minimum',value) or value>rule.get('maximum',value):raise ValueError(path+': outside range')
        if isinstance(value,list):
            if len(value)<rule.get('minItems',0):raise ValueError(path+': missing items')
            if rule.get('uniqueItems') and len({json.dumps(v,sort_keys=True) for v in value})!=len(value):raise ValueError(path+': duplicate items')
            for i,item in enumerate(value):check(item,rule.get('items',{}),path+f'[{i}]')
        if isinstance(value,dict):
            for key in rule.get('required',[]):
                if key not in value:raise ValueError(path+': missing '+key)
            for key,child in rule.get('properties',{}).items():
                if key in value:check(value[key],child,path+'.'+key)
    check(p,read('photo.schema.json'),'photo')
    if p['reviewStatus']=='approved' and not p.get('humanReviewer'):raise ValueError('A human reviewer is required')
    if p['classification']!='UNKNOWN' and not p['evidence']:raise ValueError('Classification needs evidence')
def validate():
    taxonomy={c['id']:c for c in read('taxonomy.json')};ids=set();hashes=set()
    for p in read('photos.json'):
        assert p['id'] not in ids and re.fullmatch(r'[a-z0-9-]+',p['id']);ids.add(p['id'])
        assert p['aircraftModel'] in MODELS and p['sourceType'] in SOURCE_TYPES
        assert p['classification'] in CLASSIFICATIONS
        assert p['reviewStatus'] in ['pending','curated','approved','rejected']
        if p['reviewStatus'] not in ['curated','approved']:continue
        validate_metadata(p)
        assert p['whyUseful'] and p['sourceName'] and p['originalFilename'] and p['copyrightNotes'] and p['rightsBasis']
        assert p['reviewedBy'] and p['reviewedAt'] and p['reviewNotes'] and p['evidence']
        if p['reviewStatus']=='approved':assert p.get('humanReviewer'),p['id']
        assert p['category'] in taxonomy
        assert all(p[k]==taxonomy[p['category']][k] for k in ['section','subsystem','component'])
        assert p['sha256'] not in hashes,'Duplicate source image';hashes.add(p['sha256'])
        for key in ['image','thumbnail','originalImage']:
            file=(ROOT/'docs'/p[key]).resolve(); assert file.is_relative_to((ROOT/'docs/assets/photos').resolve()) and file.is_file()
        assert hashlib.sha256((ROOT/'docs'/p['originalImage']).read_bytes()).hexdigest()==p['sha256']
        for key in ['sourceUrl']:
            assert not p[key] or p[key].startswith(('https://','http://'))
    return len(public_photos())
def build():
    from publish_all import head,bar,footer,catalog
    validate(); photos=sorted(public_photos(),key=lambda p:(MODELS.index(p['aircraftModel']),p['id']));cats=read('taxonomy.json');manuals={m['id']:m for m in catalog()}
    def shell(title,base,content,extra=''):
        return head(title,base).replace('</head>',f'<link rel="stylesheet" href="{base}assets/css/photo-library.css"></head>')+'<body>'+bar(base)+'<main class="photo-library">'+content+'</main>'+extra+'</body></html>'
    def write(route,text):
        path=ROOT/'docs'/route;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
    counts=Counter(p['category'] for p in photos)
    routes={'':{}}
    for c in cats:
        parts=c['id'].split('/')
        routes[parts[0]]={'section':c['section']}
        routes['/'.join(parts[:2])]={'section':c['section'],'subsystem':c['subsystem']}
        routes[c['id']]={k:c[k] for k in ['section','subsystem','component']}
    facets=[('aircraftModel','Aircraft model',MODELS),('section','Aircraft section',list(dict.fromkeys(c['section'] for c in cats))),('component','Component',sorted({c['component'] for c in cats})),('sourceType','Source type',SOURCE_TYPES),('subsystem','Subsystem',sorted({c['subsystem'] for c in cats})),('builder','Builder',sorted({p['builder'] for p in photos})),('buildStage','Build stage',['Assembly','Before covering','Completed','Unknown']),('tag','Tag',sorted({t for p in photos for t in p['tags']}))]
    for route,defaults in routes.items():
        base='../'*(len(route.split('/'))+1 if route else 1)
        title=list(defaults.values())[-1] if defaults else 'Photo Library'
        selected=[p for p in photos if all(p[k]==v for k,v in defaults.items())]
        nav=[]
        for sec in dict.fromkeys(c['section'] for c in cats):
            sc=[c for c in cats if c['section']==sec];total=sum(counts[c['id']] for c in sc)
            nav.append(f'<details {"open" if defaults.get("section")==sec or not defaults and sec=="Fuselage" else ""}><summary>{E(sec)} <span>{total}</span></summary><a class="section-all" href="{base}photos/{slug(sec)}/index.html">All {E(sec.lower())}</a>')
            for sys in dict.fromkeys(c['subsystem'] for c in sc):
                nav.append(f'<details class="category-system" {"open" if defaults.get("subsystem")==sys else ""}><summary>{E(sys)}</summary>')
                for c in sc:
                    if c['subsystem']==sys:nav.append(f'<a {"aria-current=page" if c["id"]==route else ""} href="{base}photos/{c["id"]}/index.html">{E(c["component"])} <span>{counts[c["id"]]}</span></a>')
                nav.append('</details>')
            nav.append('</details>')
        primary=''.join(select(*f) for f in facets[:3]);advanced=''.join(select(*f) for f in facets[3:])
        crumbs=f'<a href="{base}index.html">Build guide</a> / <a href="{base}photos/index.html">Photo Library</a>'+(' / '+E(' / '.join(defaults.values())) if defaults else '')
        links=''.join(f'<a href="{base}{m["slug"]}/index.html">{E(m["title"])} →</a> ' for m in manuals.values() if any(m['id'] in p['guideIds'] for p in selected)) if defaults else ''
        content=f'''<div class="photo-intro"><p class="breadcrumb">{crumbs}</p><p class="eyebrow">REAL BUILDS · VISUAL REFERENCES</p><h1>{E(title)}</h1><p>Find the angle that makes the assembly clear.</p><p class="hint">{len(photos)} selected photos · Companion examples first · more sources ready for review</p><p class="photo-rule">{NOTICE}</p><nav class="library-links"><a href="{base}photos/sources/index.html">Sources &amp; authority</a><a href="{base}photos/review/index.html">Import review queue</a><a href="{base}photos/reference-index/index.html">Original reference index</a></nav></div><div class="photo-layout"><aside class="category-nav"><details class="category-browser" open><summary>Browse aircraft sections</summary><nav aria-label="Photo categories"><a href="{base}photos/index.html">All photos <span>{len(photos)}</span></a>{''.join(nav)}</nav></details></aside><section class="photo-results" aria-label="Photo results"><form id="photo-filters"><label class="photo-search">Search the library<input type="search" name="q" placeholder="Try bellcrank, underside, Jay…" autocomplete="off"></label><div class="photo-filter-row">{primary}</div><details class="more-filters"><summary>More filters · source, subsystem, builder, stage, tags</summary><div class="photo-filter-row advanced">{advanced}</div></details><div class="filter-actions"><button type="reset">Reset filters</button><button type="submit">Search photos</button></div></form><div class="results-heading"><p id="photo-count" role="status" aria-live="polite">{len(selected)} photos</p><label>Sort <select id="photo-sort"><option value="companion">Companion first</option><option value="title">Title</option><option value="builder">Builder</option></select></label></div><div class="related-guides">{links}</div><div id="photo-grid" class="photo-grid">{''.join(card(p,base) for p in selected)}</div><div id="photo-empty" {"hidden" if selected else ""}><h2>No reviewed photos here yet</h2><p>Try fewer filters or browse the source directory. Unreviewed images are never counted as published photos.</p><a href="{base}photos/sources/index.html">Browse sources →</a></div><button id="photo-more" hidden>Show more photos</button><noscript><p>Enable JavaScript for search and filtering. Category links and individual photo pages work without it.</p></noscript></section></div>'''
        if not route:
            legacy=read_legacy()
            content+='<details class="legacy-links"><summary>Earlier reference bookmarks</summary>'+''.join(f'<p id="{E(r["id"])}"><a href="reference-index/index.html#{E(r["id"])}">{E(r["id"])} — original reference</a></p>' for r in legacy)+'</details>'
        payload={'photos':photos,'base':base,'defaults':defaults,'manuals':{k:{'title':v['title'],'slug':v['slug']} for k,v in manuals.items()}}
        data=json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')
        extra=f'<script id="photo-data" type="application/json">{data}</script><script src="{base}assets/js/photo-library.js" defer></script><dialog id="photo-dialog" aria-labelledby="dialog-title"><div class="dialog-toolbar"><button id="dialog-close" autofocus>Close ✕</button><a id="dialog-permalink">Open photo page ↗</a><button id="dialog-prev" aria-label="Previous photo">←</button><button id="dialog-next" aria-label="Next photo">→</button></div><div id="dialog-body"></div></dialog>'
        write('photos/'+(route+'/' if route else '')+'index.html',shell(title,base,content+footer(base),extra))
    for p in photos:
        base='../../../';related=[q for q in photos if q['id']!=p['id'] and (q['category']==p['category'] or set(q['guideIds'])&set(p['guideIds']))][:4]
        content=f'<p class="breadcrumb"><a href="{base}photos/index.html">Photo Library</a> / <a href="{base}photos/{p["category"]}/index.html">{E(p["component"])}</a></p><div class="photo-detail">{detail(p,base,manuals)}</div><h2>Related views</h2><div class="photo-grid">'+''.join(card(q,base) for q in related)+'</div>'+footer(base)
        write(photo_route(p),shell(p['title'],base,content))
    build_sources(shell,write,footer)
    (ROOT/'docs/photos/library.json').write_text(json.dumps({'schemaVersion':1,'photos':photos},indent=2,ensure_ascii=False),encoding='utf-8')
    print('PHOTO_LIBRARY',len(photos),'photos;',len(routes),'category routes')
def read_legacy():return json.loads((ROOT/'specs/photo_index.json').read_text(encoding='utf-8'))['reviewed']
def build_sources(shell,write,footer):
    sources=read('sources.json'); base='../../'
    authority=['Bob Barrows / designer plans, drawings, specifications and engineering documentation','Current Bearhawk factory manuals, service information and hardware callouts','Applicable legacy Bearhawk / AviPro manuals','Eric Newton Bearhawk Builder Manuals','Companion builder logs','Four-Place / Patrol / Five builder logs','Bearhawk Forums technical discussions','FAA AC 43.13 and accepted aircraft construction practice']
    meaning=['Explicitly required by controlling documentation.','Applicable accepted aircraft construction practice.','Observed across multiple builds; not a design requirement.','Observed on one aircraft.','A documented deviation from standard configuration.','Supported interpretation, not explicitly documented.','Insufficient evidence; no technical requirement established.']
    content='<p class="breadcrumb"><a href="../index.html">Photo Library</a> / Sources</p><h1>Sources &amp; authority</h1><p>Source discovery is separate from permission to reproduce images. Link-only and unreviewed collections are not photo counts.</p><section class="source-panel"><h2>Controlling documentation comes first</h2><ol>'+''.join('<li>'+E(a)+'</li>' for a in authority)+'</ol><p>Designer requirements control where explicit. Photographs never establish dimensions, thickness, bolt size or grip, nut type, edge distance or structural and flight-control hardware specifications.</p><p>FAA AC 43.13 is an applicable-practice reference; it does not override manufacturer design data.</p></section><details class="source-panel"><summary>How conclusions are classified</summary><dl>'+''.join(f'<dt>{c}</dt><dd>{E(d)}</dd>' for c,d in zip(CLASSIFICATIONS,meaning))+'</dl></details><h2>Source directory</h2>'
    for s in sources:
        link=f'<a href="{E(s["url"])}" target="_blank" rel="noopener">Open source ↗</a>' if s['url'] else '<span>Local project reference</span>'
        content+=f'<article class="review-item"><p class="eyebrow">{E(s["type"])} · {E(s["status"])}</p><h2>{E(s["name"])}</h2><p>{E(s["notes"])}</p><p class="hint">Model: {E(s["model"])} · Builder: {E(s.get("builder") or "Not established")}</p>{link}</article>'
    write('photos/sources/index.html',shell('Photo sources','../../',content+footer(base)))
    queue=read('review-queue.json');content='<p class="breadcrumb"><a href="../index.html">Photo Library</a> / Review queue</p><h1>Import review queue</h1><p>New imports remain unpublished until a human checks identity, captions, applicability, provenance and image-use rights. The initial curated examples are separately identified in their metadata.</p><p>Imported original directories, HTML indexes and contextual text stay in the local staging folder.</p>'
    for q in queue:content+=f'<article class="review-item"><p class="eyebrow">{E(q["id"])} · NEEDS REVIEW</p><h2>{E(q["title"])}</h2><p>{E(q["reason"])}</p>'+ (f'<a href="{E(q["sourceUrl"])}" target="_blank" rel="noopener">Open source ↗</a>' if q.get('sourceUrl') else '')+'</article>'
    if not queue:content+='<p>No image batches awaiting review.</p>'
    content+='<p class="hint">No private staged image or full source text is published on this page.</p>'+footer(base)
    write('photos/review/index.html',shell('Photo import review',base,content))
if __name__=='__main__':build()
