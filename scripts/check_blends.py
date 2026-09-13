"""Reopen editable files; synchronize embedded source/specs without rerendering.
The approved CTRL001 file is read and inspected, never saved.
"""
from pathlib import Path
import json,bpy,argparse,sys
parser=argparse.ArgumentParser();parser.add_argument('--ids',nargs='*');parser.add_argument('--read-only',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[1]
items=json.loads((ROOT/'specs/catalog.json').read_text(encoding='utf-8'))
results=[]
for m in items:
    if not m['steps'] or (args.ids and m['id'] not in args.ids):continue
    p=ROOT/'blender'/f'{m["id"]}_visual_v2.blend'
    bpy.ops.wm.open_mainfile(filepath=str(p))
    scenes=[s for s in bpy.data.scenes if s.camera]
    assert len(scenes)>=len(m['steps']),(m['id'],len(scenes))
    assert len(bpy.data.meshes)>0
    for s in scenes:assert s.camera.data.type=='ORTHO'
    if m['id']!='CTRL001' and not args.read_only:
        for name in ['primary_visuals.py','blender_common.py','visual_standard.py']:
            t=bpy.data.texts.get(name) or bpy.data.texts.new(name);t.clear();t.write((ROOT/'scripts'/name).read_text(encoding='utf-8'))
        t=bpy.data.texts.get('assembly.json') or bpy.data.texts.new('assembly.json');t.clear();t.write(json.dumps(m,indent=2,ensure_ascii=False))
        bpy.context.preferences.filepaths.save_version=0
        bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
    results.append(dict(id=m['id'],scenes=len(scenes),meshes=len(bpy.data.meshes),orthographic=True))
(ROOT/'work/validation/blends.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('BLEND_CHECK',len(results),'passed')
