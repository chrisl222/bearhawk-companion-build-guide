"""Blender shape-family icons, never dimensional hardware specifications."""
from pathlib import Path
import sys,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import bpy
from blender_common import helpers
from mathutils import Vector as V
bpy.ops.wm.read_factory_settings(use_empty=True)
globals().update(helpers())
for kind in ['nutplate','rivet','rivet_flush','screw_round','screw_flat','pin','shackle','turnbuckle','spring','hose','clamp','strainer','fitting','tubenut','pulley']:
    sc=scene('ICON_'+kind);collection(kind)
    if kind=='nutplate':
        plate('base',[(-1.6,-.4,0),(1.6,-.4,0),(1.6,.4,0),(-1.6,.4,0)],(0,0,1),.15,'hardware', [((-1.2,0,0),.12),((1.2,0,0),.12)])
        ring('threaded_boss',(0,0,.3),(0,0,1),.48,.20,.6,'hardware',6)
    elif kind in ['rivet','rivet_flush','screw_round','screw_flat','pin']:
        tube('shank',(-1,0,0),(1,0,0),.18,'hardware')
        if kind in ['rivet_flush','screw_flat']:
            bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=.40,radius2=.18,depth=.28,location=(-1.03,0,0),rotation=(0,math.pi/2,0));finish(bpy.context.object,'countersunk_head','hardware')
        else:tube('head',(-1.2,0,0),(-1,0,0),.36,'hardware')
        if kind=='pin':ring('cross_hole_symbol',(.75,0,0),(0,1,0),.12,.065,.35,'hardware')
        if kind.startswith('screw'):
            # A light recessed cross distinguishes a screw from a structural bolt.
            for y,z,sy,sz in [(0,0,.42,.055),(0,0,.055,.42)]:box('drive_recess',(-1.22,y,z),(.025,sy,sz),'old')
    elif kind=='shackle':
        for z in [-.4,.4]:
            plate('clevis_arm',[(-1,-.45,z),(1,-.45,z),(1,.45,z),(-1,.45,z)],(0,0,1),.16,'hardware',[((.6,0,z),.20)])
        box('closed_end',(-1,0,0),(.2,.9,.85),'hardware')
    elif kind=='turnbuckle':
        tube('barrel',(-.8,0,0),(.8,0,0),.30,'hardware')
        for sign in [-1,1]:
            tube('threaded_end',(sign*.8,0,0),(sign*1.4,0,0),.12,'hardware');ring('eye',(sign*1.65,0,0),(0,0,1),.30,.17,.15,'hardware')
    elif kind=='spring':
        pts=[(-1.3+2.6*i/180,.32*math.cos(i*math.tau/20),.32*math.sin(i*math.tau/20)) for i in range(181)]
        for i,(a,b) in enumerate(zip(pts,pts[1:])):tube('coil'+str(i),a,b,.045,'hardware',8)
        for sign in [-1,1]:ring('end_hook',(sign*1.55,0,0),(0,0,1),.24,.18,.07,'hardware')
    elif kind in ['hose','clamp']:
        ring(kind,(0,0,0),(1,0,0),.60,.43,2.6 if kind=='hose' else .45,'hardware')
        if kind=='clamp':box('worm_housing',(0,0,.65),(.65,.40,.30),'hardware')
    elif kind=='strainer':
        tube('threaded_base',(-1.4,0,0),(-.7,0,0),.38,'hardware',6)
        for x in [-.6,-.1,.4,.9,1.4]:ring('screen_end',(x,0,0),(1,0,0),.29,.25,.04,'hardware')
        for i in range(12):
            a=i*math.tau/12;tube('screen_wire',(-.7,.27*math.cos(a),.27*math.sin(a)),(1.4,.27*math.cos(a),.27*math.sin(a)),.025,'hardware',8)
    elif kind=='fitting':
        ring('union_hex',(0,0,0),(1,0,0),.50,.20,.50,'hardware',6)
        for s in [-1,1]:ring('thread_end',(s*.8,0,0),(1,0,0),.32,.20,1.1,'hardware')
    elif kind=='tubenut':
        ring('nut',(0,0,0),(1,0,0),.55,.25,1.1,'hardware',6);ring('end',(0.6,0,0),(1,0,0),.4,.25,.25,'hardware')
    else:
        ring('pulley',(0,0,0),(0,0,1),1.1,.18,.3,'hardware');ring('rim',(0,0,.17),(0,0,1),1.1,.9,.06,'hardware')
    camera((7,-10,7),(0,0,0),4.5,(320,160));sc.render.filepath=str(ROOT/'docs/assets/images/hardware'/f'icon_{kind}.png')
    bpy.ops.render.render(write_still=True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/hardware_icons.blend'),compress=True)
