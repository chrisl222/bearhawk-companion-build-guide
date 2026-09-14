/* Dependency-free search and accessible native-dialog enhancement. */
(() => {
  'use strict';
  const payload = JSON.parse(document.getElementById('photo-data').textContent);
  const {photos, base, defaults, manuals} = payload;
  const form = document.getElementById('photo-filters');
  const grid = document.getElementById('photo-grid');
  const dialog = document.getElementById('photo-dialog');
  const sort = document.getElementById('photo-sort');
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fields = ['q','aircraftModel','section','subsystem','component','sourceType','builder','buildStage','tag'];
  const searchable = new Map(photos.map(p => [p.id, [p.title,p.caption,p.whyUseful,p.component,p.subsystem,p.section,p.builder,p.sourceName,p.originalCaption,...p.tags].join(' ').toLowerCase()]));
  let filtered = [], shown = 24, active = null, opener = null;
  const route = p => `${base}photos/image/${p.id}/index.html`;
  const model = p => ({Four:'FOUR-PLACE',Unknown:'MODEL UNKNOWN'}[p.aircraftModel] || p.aircraftModel.toUpperCase());
  function card(p) {
    const badge = p.authorityLevel === 3 ? 'LEGACY' : ({'Beartracks':'BEARTRACKS','Bearhawk Factory':'FACTORY','Designer / Plans':'DESIGNER','Bearhawk Forum':'FORUM'}[p.sourceType] || 'BUILDER');
    const sourceLink=p.sourceUrl?`<a href="${esc(p.sourceUrl)}" target="_blank" rel="noopener">View original source ↗</a>`:'';
    return `<article class="photo-card"><a class="photo-open" href="${route(p)}" data-open="${p.id}"><div class="photo-frame"><img src="${base}${esc(p.thumbnail)}" width="${p.width}" height="${p.height}" alt="${esc(p.title)}" loading="lazy"><span class="enlarge">View photo ↗</span></div><div class="photo-copy"><div class="photo-badges"><span class="model">${model(p)}</span><span>${badge}</span></div><p class="photo-builder">${esc(p.builder)}</p><h3>${esc(p.title)}</h3></div></a><div class="photo-copy photo-context"><p>${esc(p.whyUseful)}</p><p class="photo-category">${esc(p.subsystem)} / ${esc(p.component)}</p><p class="photo-source">${esc(p.sourceName)} · ${esc(p.sourcePage)}<br>${sourceLink}</p><div class="photo-tags">${p.tags.slice(0,3).map(t=>`<span>${esc(t)}</span>`).join('')}</div><p class="photo-applicability">${p.aircraftModel==='Companion'?'Companion builder example; verify your configuration.':p.aircraftModel==='Unknown'?'Model unknown · Companion applicability unverified.':`${esc(p.aircraftModel)} example · verify Companion applicability.`}</p></div></article>`;
  }
  function stateFromUrl() {
    const params = new URLSearchParams(location.search);
    for (const field of fields) form.elements[field].value = params.has(field) ? params.get(field) : (defaults[field] || '');
    sort.value = params.get('sort') || 'companion';
  }
  function saveUrl() {
    const params = new URLSearchParams(location.search);
    for (const field of fields) {
      const value = form.elements[field].value;
      if (value || defaults[field]) params.set(field,value); else params.delete(field);
    }
    if (sort.value==='companion') params.delete('sort'); else params.set('sort',sort.value);
    const query=params.toString(); history.replaceState(null,'',location.pathname+(query?'?'+query:'')+location.hash);
  }
  function render(updateUrl=true) {
    const values = Object.fromEntries(fields.map(k=>[k,form.elements[k].value]));
    const words=values.q.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const guide = new URLSearchParams(location.search).get('guide');
    filtered = photos.filter(p => (!guide || p.guideIds.includes(guide)) && words.every(w=>searchable.get(p.id).includes(w)) && fields.slice(1).every(k=>!values[k] || (k==='tag'?p.tags.includes(values[k]):p[k]===values[k])));
    const modelOrder={Companion:0,Four:1,Patrol:2,Five:3,Unknown:4};
    filtered.sort((a,b)=>sort.value==='title'?a.title.localeCompare(b.title):sort.value==='builder'?a.builder.localeCompare(b.builder)||a.title.localeCompare(b.title):(modelOrder[a.aircraftModel]-modelOrder[b.aircraftModel]||a.title.localeCompare(b.title)));
    grid.innerHTML=filtered.slice(0,shown).map(card).join('');
    document.getElementById('photo-empty').hidden=filtered.length>0;
    document.getElementById('photo-more').hidden=shown>=filtered.length;
    document.getElementById('photo-count').textContent=`${filtered.length} ${filtered.length===1?'photo':'photos'}${guide&&manuals[guide]?' · '+manuals[guide].title:''}`;
    if(updateUrl) saveUrl();
  }
  function openPhoto(id,changeUrl=true) {
    const p=photos.find(p=>p.id===id);if(!p)return;
    active=id;
    if(!dialog.open) opener=document.activeElement;
    const dl=(label,value)=>`<dt>${label}</dt><dd>${value}</dd>`;
    const related=photos.filter(q=>q.id!==id&&(q.category===p.category||q.guideIds.some(g=>p.guideIds.includes(g)))).slice(0,4);
    const source=p.sourceUrl?`<a href="${esc(p.sourceUrl)}" target="_blank" rel="noopener">View original source ↗</a>`:'Project-provided document; no public URL established.';
    const guideLinks=p.guideIds.filter(g=>manuals[g]).map(g=>`<a href="${base}${esc(manuals[g].slug)}/index.html">${esc(manuals[g].title)} →</a>`).join(' ');
    document.getElementById('dialog-body').innerHTML=`<div class="photo-detail"><div class="photo-detail-image"><a href="${base}${esc(p.originalImage)}" target="_blank" rel="noopener"><img src="${base}${esc(p.image)}" width="${p.width}" height="${p.height}" alt="${esc(p.title)}"></a><p>${p.width} × ${p.height} source pixels · <a href="${base}${esc(p.originalImage)}" target="_blank" rel="noopener">Original size ↗</a></p><h2>Related views</h2><div class="related-thumbs">${related.map(q=>`<a href="${route(q)}" data-open="${q.id}"><img src="${base}${esc(q.thumbnail)}" alt="${esc(q.title)}"><span>${esc(q.title)}</span></a>`).join('')||'<p>No second reviewed view yet.</p>'}</div></div><div class="photo-detail-copy"><p class="eyebrow">${model(p)} · ${esc(p.sourceType)}</p><h2 id="dialog-title">${esc(p.title)}</h2><p>${esc(p.whyUseful)}</p><p class="scope-note">${esc(p.applicabilityNotes)}</p><dl>${dl('Builder / source',esc(p.builder)+' · '+esc(p.sourceName))}${dl('Component',[p.section,p.subsystem,p.component].map(esc).join(' / '))}${dl('Stage / viewpoint',esc(p.buildStage)+' / '+esc(p.viewpoint.join(', ')||'Not recorded'))}${dl('Classification / configuration',esc(p.classification)+' / '+esc(p.stockOrModified))}${dl('Document / page',esc(p.sourceDocument)+' · '+esc(p.sourcePage))}${dl('Original caption',esc(p.originalCaption||'No unambiguous image-specific caption transcribed; see the source page.'))}${dl('Original filename / directory',esc(p.originalFilename)+'<br>'+esc(p.originalPath))}${dl('Original source',source)}${dl('Tags',esc(p.tags.join(', ')))}${dl('Attribution',esc(p.copyrightNotes))}</dl><p class="photo-rule">PHOTO REFERENCE ONLY — verify dimensions, hardware, and structural details against controlling Bearhawk documentation.</p><div class="related-guides">${guideLinks}</div></div></div>`;
    document.getElementById('dialog-permalink').href=route(p);
    const index=filtered.findIndex(q=>q.id===id);
    document.getElementById('dialog-prev').disabled=index<=0;
    document.getElementById('dialog-next').disabled=index<0||index>=filtered.length-1;
    if(!dialog.open)dialog.showModal();
    dialog.scrollTop=0;document.getElementById('dialog-close').focus();
    if(changeUrl){const u=new URL(location.href);u.searchParams.set('photo',id);history.pushState(null,'',u);}
  }
  function clearPhoto() {
    active=null;const u=new URL(location.href);u.searchParams.delete('photo');history.replaceState(null,'',u);if(opener?.isConnected)opener.focus();
  }
  function navigatePhoto(delta){const i=filtered.findIndex(p=>p.id===active);if(filtered[i+delta])openPhoto(filtered[i+delta].id);}
  document.addEventListener('click',event=>{const link=event.target.closest('[data-open]');if(!link||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;event.preventDefault();openPhoto(link.dataset.open);});
  document.getElementById('dialog-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',clearPhoto);
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
  dialog.addEventListener('keydown',e=>{if(e.key==='ArrowRight')navigatePhoto(1);if(e.key==='ArrowLeft')navigatePhoto(-1);});
  document.getElementById('dialog-prev').addEventListener('click',()=>navigatePhoto(-1));
  document.getElementById('dialog-next').addEventListener('click',()=>navigatePhoto(1));
  let timer;
  form.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>{shown=24;render();},120);});
  form.addEventListener('change',()=>{clearTimeout(timer);shown=24;render();});
  form.addEventListener('submit',e=>{e.preventDefault();clearTimeout(timer);shown=24;render();});
  form.addEventListener('reset',()=>{setTimeout(()=>{for(const k of fields)form.elements[k].value=defaults[k]||'';sort.value='companion';const u=new URL(location.href);u.searchParams.delete('guide');history.replaceState(null,'',u);shown=24;render();},0);});
  sort.addEventListener('change',()=>{shown=24;render();});
  document.getElementById('photo-more').addEventListener('click',()=>{shown+=24;render(false);});
  window.addEventListener('popstate',()=>{stateFromUrl();render(false);const id=new URLSearchParams(location.search).get('photo');if(id)openPhoto(id,false);else if(dialog.open)dialog.close();});
  if(window.matchMedia('(max-width: 760px)').matches)document.querySelector('.category-browser').open=false;
  document.addEventListener('error',e=>{if(e.target.tagName==='IMG'){e.target.alt='Image unavailable — open the source or photo page.';e.target.classList.add('image-unavailable');}},true);
  stateFromUrl();render(false);
  const initialPhoto=new URLSearchParams(location.search).get('photo');if(initialPhoto)openPhoto(initialPhoto,false);
  if(location.hash){const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(target?.closest('.legacy-links')){target.closest('details').open=true;target.scrollIntoView();}}
})();
