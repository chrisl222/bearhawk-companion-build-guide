"""CTRL001 — illustrative Companion control-stick assembly.

Run with ordinary Python + Pillow: python scripts/ctrl001_visual_v2.py
Optional: --blender PATH, --compose-only, --preview (steps 1, 4, 5 only).
Blender worker: blender -b --python ctrl001_visual.py -- --worker

Authority: Bob Barrows Companion sheets 28, 17, 18 (PDF pages 4,15,14).
Visual context: BHManual-Fuselage1-25Rev1 pp17–18.
Hardware checked against factory Companion-Hardware-Customer-Sheet1-2.pdf,
Control Stick Assembly HK-CS4, 2026-09-13.
https://www.bearhawkaircraft.com/s/Companion-Hardware-Customer-Sheet1-2.pdf

Illustration units approximately inches; not manufacturing geometry.
Axes: X aircraft right, Y aft, Z up. Neutral pose is illustrative, not rigging.
Bellcrank mounting is existing context: lateral position/spacers unverified.
The factory lists both AN316-4R and AN345-524 for the pushrod. Their application
is unresolved: both are shown in a separate verification tray, NOT installed.
Do not infer a nut stack or thread compatibility from that tray.
No cable system, rigging limits, torque, or motion clearance is certified here.
"""
from pathlib import Path
import sys, math, argparse

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'work' / 'renders'
ASSETS = ROOT / 'docs' / 'assets' / 'images' / 'control-sticks'
sys.path.insert(0, str(ROOT / 'scripts'))
from visual_standard import PALETTE_3D, RENDER_SCALE

def worker():
    import bpy
    from mathutils import Vector
    V = Vector
    bpy.ops.wm.read_factory_settings(use_empty=True)
    RAW.mkdir(parents=True, exist_ok=True)
    colors = PALETTE_3D
    mats={}
    for name, col in colors.items():
        m=bpy.data.materials.new(name); m.diffuse_color=col; mats[name]=m
    current=None
    def collection(name):
        nonlocal current
        current=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(current)
        return current
    def finish(obj,name,mat):
        obj.name=name
        for c in list(obj.users_collection): c.objects.unlink(obj)
        current.objects.link(obj)
        obj.data.materials.append(mats[mat]); obj.color=colors[mat]
        return obj
    def tube(name,a,b,r=.25,mat='old',vertices=24):
        a,b=V(a),V(b); d=b-a
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d.length,location=(a+b)/2)
        o=bpy.context.object; o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
        if vertices>8:
            for poly in o.data.polygons:
                if len(poly.vertices)==4:poly.use_smooth=True
        return finish(o,name,mat)
    def box(name,p,size,mat='old'):
        bpy.ops.mesh.primitive_cube_add(size=1,location=p)
        o=bpy.context.object; o.scale=size
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        return finish(o,name,mat)
    def ring(name,p,axis,outer,inner,depth,mat='hardware',vertices=32):
        axis=V(axis).normalized(); q=axis.to_track_quat('Z','Y')
        verts=[]
        for z,r in [(-depth/2,outer),(depth/2,outer),(-depth/2,inner),(depth/2,inner)]:
            for i in range(vertices):
                a=i*math.tau/vertices
                verts.append(V(p)+q@V((r*math.cos(a),r*math.sin(a),z)))
        faces=[]
        for i in range(vertices):
            j=(i+1)%vertices
            faces += [(i,j,vertices+j,vertices+i),
                      (2*vertices+i,3*vertices+i,3*vertices+j,2*vertices+j),
                      (i,2*vertices+i,2*vertices+j,j),
                      (vertices+i,vertices+j,3*vertices+j,3*vertices+i)]
        mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
        o=bpy.data.objects.new(name,mesh); current.objects.link(o)
        if vertices>8:
            for poly in mesh.polygons:
                if poly.index % 4 < 2:poly.use_smooth=True
        o.data.materials.append(mats[mat]); o.color=colors[mat]; return o
    def plate(name,points,axis,depth,mat='old',holes=()):
        ax=V(axis).normalized(); pts=[V(p) for p in points]; n=len(pts)
        verts=[p+ax*s*depth/2 for s in [-1,1] for p in pts]
        faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
        faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
        o=bpy.data.objects.new(name,mesh); current.objects.link(o); o.data.materials.append(mats[mat]);o.color=colors[mat]
        for p,r in holes:
            cut=tube('cut',V(p)-ax*2,V(p)+ax*2,r,'white',32)
            mod=o.modifiers.new('illustrative hole','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut
            bpy.context.view_layer.objects.active=o
            bpy.ops.object.modifier_apply(modifier=mod.name); bpy.data.objects.remove(cut,do_unlink=True)
        return o
    def arrow(name,a,b,width=.10):
        a,b=V(a),V(b); d=(b-a).normalized(); head=min(.65,(b-a).length*.3)
        tube(name+'_shaft',a,b-d*head,width,'arrow',16)
        bpy.ops.mesh.primitive_cone_add(vertices=20,radius1=width*3.2,radius2=0,depth=head,location=b-d*head/2)
        o=bpy.context.object;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();finish(o,name+'_head','arrow')
    def dashed(a,b):
        a,b=V(a),V(b)
        for i in range(0,12,2):tube('alignment',a+(b-a)*i/12,a+(b-a)*(i+1)/12,.026,'old',8)
    def bolt(name,p,axis,length=.85,diam=.19,explode=0,castle=False,cotter=False):
        p,ax=V(p),V(axis).normalized()
        # p is the center of the joined parts. Diagram spacing is exaggerated.
        start=p-ax*(length/2+explode)
        tube(name+'_shank',start,start+ax*length,diam/2,'hardware')
        tube(name+'_head',start-ax*.15,start,diam*.95,'hardware',6)
        wp=p+ax*(length/2+.06+explode*.8)
        ring(name+'_washer',wp,ax,diam*1.02,diam*.52,.065)
        np=wp+ax*(.18+explode*.55)
        nut=ring(name+('_castle_nut' if castle else '_lock_nut'),np,ax,diam*.98,diam*.52,.19,'hardware',6)
        if castle:
            q=ax.to_track_quat('Z','Y')
            for i in range(6):
                a=math.tau*i/6; pos=np+ax*.145+q@V((diam*.76*math.cos(a),diam*.76*math.sin(a),0))
                tube(name+'_castle_turret',pos-ax*.06,pos+ax*.06,diam*.18,'hardware',6)
        if cotter:
            q=ax.to_track_quat('Z','Y'); cp=np+ax*(.28+explode*.3)
            ring(name+'_cotter_symbol',cp,q@V((0,1,0)),.12,.08,.045)
            tube(name+'_cotter_symbol_leg',cp,cp+q@V((0,0,.32)),.035,'hardware',8)
        if explode: dashed(p-ax*3,p+ax*3)
    def context():
        collection('FUSELAGE_CONTEXT')
        # Local C-S station and adjoining lower structure only.
        for x in [-14,14]:
            tube('lower_longeron', (x,-7,-.8),(x,7,-.8),.38,'context')
        tube('station_C_lower',(-14,2,-.8),(14,2,-.8),.38,'context')
        tube('station_S_upper',(-14,4,6.5),(14,4,6.5),.31,'context')
        for x in [-14,14]:tube('station_C_S_side',(x,2,-.8),(x,4,6.5),.32,'context')
        for x in [-5.8,5.8]:
            tube('local_floor_support',(x,-5,-.8),(x,2,-.8),.32,'context')
            box('fuselage_mount_tab',(x,0,-.34),(1.35,3.25,.14),'context')
        # Bellcrank bearing support; spacers and lateral location require verification.
        tube('bellcrank_existing_support',(0,2,-.8),(0,4,6.5),.32,'context')
    def frame(mat='old',dz=0):
        collection('CONTROL_SYSTEM.frame')
        def P(x,y,z):return (x,y,z+dz)
        tube('transverse_torque_tube',P(-9,0,.45),P(9,0,.45),.56,mat)
        for x in [-5.8,5.8]:
            ring('mount_bearing_saddle',P(x,0,.45),(1,0,0),.70,.57,1.0,mat)
            box('mount_foot',P(x,0,-.14),(1.25,2.8,.18),mat)
            for yy in [-.6,.6]:box('saddle_web',P(x,yy,.13),(.9,.12,.55),mat)
        for x in [-9,9]:
            direction=1 if x<0 else -1
            # Open U channel, with the control stick inside its two cheeks.
            for y in [-.34,.34]:
                plate('stick_pivot_channel_cheek',[P(x-.55,y,.5),P(x+.55,y,.5),P(x+.48,y,5.3),P(x-.48,y,5.3)],(0,1,0),.10,mat,[(P(x,y,4.9),.14)])
            box('channel_back',P(x+.5*direction,0,2.65),(.12,.64,4.3),mat)
            plate('inboard_triangular_brace',[P(x+.5*direction,0,.5),P(x+.5*direction,0,4.8),P(x+4.0*direction,0,.5)],(0,1,0),.10,mat)
        for x in [-.35,.35]:
            plate('elevator_drive_horn',[P(x,-.5,.7),P(x,.5,.7),P(x,.28,3.2),P(x,-.28,3.2)],(1,0,0),.12,mat,[(P(x,0,2.95),.12)])
    def sticks(mat='old',offset=(0,0,0)):
        off=V(offset)
        for x,label in [(-9,'left'),(9,'right')]:
            collection('CONTROL_SYSTEM.'+label+'_stick')
            points=[(x,-1,.15),(x,0,4.9),(x,0,6.5),(x,-3.3,7.2),(x,-4.2,13),(x,-4.2,18.0)]
            for i,(a,b) in enumerate(zip(points,points[1:])):tube(label+'_stick_tube_'+str(i),V(a)+off,V(b)+off,.30,mat)
            # Bottom flattened end, carrying the interconnect attachment.
            plate(label+'_lower_end',[V((x-.28,-1,-.2))+off,V((x+.28,-1,-.2))+off,V((x+.30,-1,.9))+off,V((x-.30,-1,.9))+off],(0,1,0),.16,mat,[(V((x,-1,.15))+off,.11)])
            ring(label+'_pivot_bushing',V((x,0,4.9))+off,(0,1,0),.25,.13,.66,mat)
    def interconnect(mat='old',offset=(0,0,0)):
        collection('CONTROL_SYSTEM.interconnect');off=V(offset)
        tube('stick_interconnect_tube',V((-7.7,-1,.15))+off,V((7.7,-1,.15))+off,.19,mat)
        for x in [-9,9]:
            s=1 if x<0 else -1
            for y in [-.75,-1.25]:
                plate('interconnect_end_fork',[V((x-s*.5,y,-.15))+off,V((x+s*1.4,y,-.15))+off,V((x+s*1.4,y,.45))+off,V((x-s*.5,y,.45))+off],(0,1,0),.08,mat,[(V((x,y,.15))+off,.10)])
            ring('interconnect_press_in_bushing',V((x,-1,.15))+off,(0,1,0),.145,.098,.46,mat)
    A=V((0,0,2.95));B=V((0,3.8,4.25))
    def bellcrank(mat='old'):
        collection('CONTROL_SYSTEM.elevator_bellcrank')
        yz=[(3.48,4.40),(5.10,5.80),(5.38,5.53),(4.60,-2.6),(4.05,-2.6),(3.50,3.90)]
        for x in [-.31,.31]:
            points=[(x,y,z) for y,z in yz]
            plate('bellcrank_side_plate',points,(1,0,0),.10,mat,
                  [((x,3.8,4.25),.13),((x,4.98,5.48),.13),((x,4.34,-2.27),.13),((x,4.15,1.0),.36),((x,4.5,3.4),.45)])
        ring('bellcrank_pivot_sleeve',(0,4.15,1.0),(1,0,0),.45,.30,1.05,mat)
    def rodend(name,eye,dir,mat='old'):
        eye=V(eye);d=V(dir).normalized()
        ring(name+'_eye',eye,(1,0,0),.31,.115,.25,mat)
        ring(name+'_ball',eye,(1,0,0),.20,.105,.32,'hardware')
        tube(name+'_unthreaded_symbolic_shank',eye+d*.24,eye+d*.90,.15,mat)
    def pushrod(mat='old',off=(0,0,0),exploded=False):
        collection('CONTROL_SYSTEM.forward_elevator_pushrod');off=V(off);d=(B-A).normalized()
        ring('elevator_pushrod_tube',(A+B)/2+off,d,.25,.165,(B-A).length-1.5,mat)
        ext=.95 if exploded else 0
        rodend('RSM4B_forward',A-d*ext+off,d,mat);rodend('RSM4B_aft',B+d*ext+off,-d,mat)
        if exploded:
            collection('ANNOTATIONS.rod_end_installation')
            arrow('forward_rodend',A-d*.8+off+V((.7,0,0)),A+off+V((.7,0,0)),.055)
            arrow('aft_rodend',B+d*.8+off+V((.7,0,0)),B+off+V((.7,0,0)),.055)
    def nuts_tray():
        collection('HARDWARE.UNVERIFIED_nut_application')
        for i,name in enumerate(['AN316-4R','AN345-524']):
            for j in range(2):
                o=ring(name+'_VERIFY_APPLICATION',(2+i*.9,1+j*.75,2.5),(1,0,0),.25 if i==0 else .29,.13 if i==0 else .17,.12 if i==0 else .22,'hardware',6)
                o['verification']='Separate parts tray; NOT an installed nut stack. Confirm application against plans/factory.'
    def hardware(stage,exploded=False):
        collection('HARDWARE.assembly_mounts')
        if stage>=1:
            for x in [-5.8,5.8]:
                for y in [-1.02,1.02]:bolt('AN3-4A',(x,y,-.24),(0,0,-1),.58,explode=1.3 if exploded and stage==1 else 0)
        if stage>=2:
            collection('HARDWARE.stick_pivots')
            for x in [-9,9]:bolt('AN174-20',(x,0,4.9),(0,1,0),1.05,.25,2 if exploded and stage==2 else 0,True,True)
        if stage>=3:
            collection('HARDWARE.interconnect')
            for x in [-9,9]:bolt('AN3-6',(x,-1,.15),(0,1,0),1.0,.19,1.8 if exploded and stage==3 else 0,True,True)
        if stage>=5:
            collection('HARDWARE.pushrod_attachments')
            for p in [A,B]:bolt('AN3-7A',p,(1,0,0),1.10,.19,1.1 if exploded and stage==5 else 0)
    def camera(pos,target,scale,res=(1500,1200)):
        collection('CAMERAS');sc=bpy.context.scene
        data=bpy.data.cameras.new('Orthographic');o=bpy.data.objects.new('Orthographic_isometric',data);current.objects.link(o)
        o.location=pos;o.rotation_euler=(V(target)-o.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=scale
        sc.camera=o;sc.render.resolution_x=res[0]*RENDER_SCALE;sc.render.resolution_y=res[1]*RENDER_SCALE;sc.render.resolution_percentage=100
        return o
    def scene(name):
        s=bpy.data.scenes.new(name);bpy.context.window.scene=s
        s.render.engine='BLENDER_WORKBENCH';s.world=bpy.data.worlds.new(name+'_world');s.world.color=(1,1,1)
        sh=s.display.shading;sh.light='STUDIO';sh.studiolight_rotate_z=.3;sh.color_type='MATERIAL';sh.show_shadows=False
        sh.show_cavity=True;sh.cavity_type='BOTH';sh.curvature_ridge_factor=.8;sh.curvature_valley_factor=.65
        sh.show_object_outline=True;sh.object_outline_color=(.27,.31,.34);sh.background_type='WORLD';sh.show_specular_highlight=False
        s.view_settings.view_transform='Standard';s.render.image_settings.file_format='PNG';s.render.film_transparent=True
        s['authority']='Geometry: Barrows Companion 28/17/18. QB hardware: supplied current Companion count sheet, page 2 HK-CS4. ILLUSTRATIVE — NOT TO SCALE.'
        s['verification']='Bellcrank lateral placement/spacers and pushrod nut application require verification. Neutral pose is not rigging.'
        return s
    def render(s,name):
        bpy.context.window.scene=s;s.render.filepath=str(RAW/(name+'.png'));bpy.ops.render.render(write_still=True)
        if name=='main_02':
            import json
            from bpy_extras.object_utils import world_to_camera_view
            points={key:list(world_to_camera_view(s,s.camera,V(p)))[:2] for key,p in [('LEFT',(-9,-6.6,20.5)),('RIGHT',(9,-6.6,20.5))]}
            (RAW/'landmarks.json').write_text(json.dumps(points))
    def full(stage,canonical=False):
        s=scene('00_ASSEMBLED_EDITABLE' if canonical else f'{stage:02d}_STEP')
        context();bellcrank()
        frame('new' if stage==1 else 'old',2.2 if stage==1 and not canonical else 0)
        if stage>=2:sticks('new' if stage==2 else 'old',(0,-2.4,2.5) if stage==2 and not canonical else (0,0,0))
        if stage>=3:interconnect('new' if stage==3 else 'old',(0,-3,0) if stage==3 and not canonical else (0,0,0))
        if stage>=5:pushrod('new' if stage==5 else 'old',(-2.2,0,1.2) if stage==5 and not canonical else (0,0,0))
        hardware(stage,not canonical and stage<6)
        collection('ANNOTATIONS')
        if not canonical:
            if stage==1:
                for x in [-5.8,5.8]:arrow('lower_frame',(x,-2.0,3.8),(x,-2.0,.2),.15)
            if stage==2:
                for x in [-9,9]:arrow('stick_insert',(x+.9,-2.4,8.0),(x+.9,-.25,5.4),.14);dashed((x,-2.4,7.4),(x,0,4.9))
            if stage==3:
                for x in [-7,7]:arrow('interconnect_install',(x,-3.7,.15),(x,-1.2,.15),.13)
            if stage==5:
                arrow('pushrod_install',(-2.0,2,4.8),(-.2,2,3.7),.12)
                dashed(A+V((-2.2,0,1.2)),A);dashed(B+V((-2.2,0,1.2)),B)
            if stage==6:
                for x in [-9,9]:
                    arrow('fore_aft_movement',(x,-6.3,17),(x,-3.0,17),.12)
                    arrow('fore_aft_reverse',(x,-3,17),(x,-6.3,17),.12)
                arrow('lateral_movement',(-10.6,-4.2,19),(-7.4,-4.2,19),.12)
                arrow('lateral_reverse',(-7.4,-4.2,19),(-10.6,-4.2,19),.12)
        camera((31,-40,30),(0,.5,3.7) if stage==1 else (0,.5,7),35,(1500,1300))
        return s
    canonical=full(6,True)
    collection('HARDWARE.UNVERIFIED_parts_tray');nuts_tray()
    # Keep the review tray editable but hidden in the assembled scene.
    current.hide_render=True;current.hide_viewport=True
    for stage in [1,2,3,5,6]:
        s=full(stage)
        if '--preview' not in sys.argv or stage in [1,5]:render(s,f'main_{stage:02d}')
    # Step four deliberately isolates the pushrod and unresolved nut tray.
    s=scene('04_STEP');pushrod('new',exploded=True);nuts_tray()
    camera((10,-5,10),(.6,1.9,3.2),8.5,(1500,1200));render(s,'main_04')
    # Connection details show separated hardware on the actual connection axis.
    for stage in [1,2,3,5]:
        s=scene(f'{stage:02d}_DETAIL')
        if stage==1:
            collection('FUSELAGE_CONTEXT');box('mount_tab',(-5.8,0,-.34),(1.5,3.3,.16),'context')
            frame('new');collection('HARDWARE')
            for y in [-1.02,1.02]:bolt('AN3-4A',(-5.8,y,-.24),(0,0,-1),.58,.19,.85)
            camera((2,-9,6),(-5.8,0,-.1),5.6,(900,700))
        elif stage==2:
            frame();sticks('new');collection('HARDWARE')
            bolt('AN174-20',(-9,0,4.9),(0,1,0),1.05,.25,1.25,True,True)
            camera((-16,-10,10),(-9,0,4.9),6,(900,700))
        elif stage==3:
            frame();sticks();interconnect('new');collection('HARDWARE')
            bolt('AN3-6',(-9,-1,.15),(0,1,0),1,.19,1.3,True,True)
            camera((-18,-4,4),(-9,-1,.2),7.3,(900,700))
        else:
            bellcrank();frame();pushrod('new');collection('HARDWARE')
            for p in [A,B]:bolt('AN3-7A',p,(1,0,0),1.1,.19,.9)
            camera((-11,-3,10),(0,2.2,3.5),8,(900,700))
        if '--preview' not in sys.argv or stage in [1,5]:render(s,f'detail_{stage:02d}')
    # Separate large identification graphics. The connection inset remains the
    # authority for the depicted stack; these symbols are a parts inventory.
    for kind in ['bolt','washer','locknut','castle','cotter','rodend','checknut','hexnut','bushing']:
        s=scene('ICON_'+kind);collection('HARDWARE.symbol.'+kind)
        if kind=='bolt':
            tube('bolt_shank',(-.65,0,0),(.75,0,0),.13,'hardware')
            tube('bolt_head',(-.90,0,0),(-.65,0,0),.27,'hardware',6)
        elif kind=='cotter':
            ring('cotter_loop',(-.4,0,0),(0,-1,0),.20,.12,.09)
            tube('cotter_leg_A',(-.25,0,.08),(.6,0,.08),.055,'hardware',12)
            tube('cotter_leg_B',(-.25,0,-.08),(.7,0,-.18),.055,'hardware',12)
        elif kind=='rodend':
            rodend('RSM4B',(0,0,.25),(0,0,-1),'hardware')
        else:
            outer=.43;inner=.23;depth={'washer':.10,'checknut':.13,'hexnut':.32,'bushing':.6}.get(kind,.36)
            ring(kind,(0,0,0),(0,-1,0),outer,inner,depth,'hardware',32 if kind in ['washer','bushing'] else 6)
            if kind=='castle':
                for i in range(6):
                    a=i*math.tau/6
                    tube('castle_turret',(.34*math.cos(a),-.35,.34*math.sin(a)),(.34*math.cos(a),-.14,.34*math.sin(a)),.09,'hardware',6)
        camera((3,-7,4),(0,0,0),2.4,(300,180))
        render(s,'icon_'+kind)
    # Default opens on the completed model with orthographic viewport.
    bpy.context.window.scene=canonical
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                area.spaces.active.region_3d.view_perspective='CAMERA'
                area.spaces.active.shading.color_type='MATERIAL'
    text=bpy.data.texts.new('ctrl001_visual_v2.py');text.write(Path(__file__).read_text(encoding='utf-8'))
    text=bpy.data.texts.new('visual_standard.py');text.write((ROOT/'scripts'/'visual_standard.py').read_text(encoding='utf-8'))
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender'/'CTRL001_visual_v2.blend'))

def compose():
    from PIL import Image, ImageDraw
    import json
    from visual_standard import Page, INK, BLUE, WARNING, MUTED, RULE
    ASSETS.mkdir(parents=True, exist_ok=True)
    titles = ['MOUNT CONTROL-STICK ASSEMBLY', 'INSTALL CONTROL STICKS',
              'CONNECT STICK INTERCONNECT', 'ASSEMBLE ELEVATOR PUSHROD',
              'CONNECT PUSHROD TO BELLCRANK', 'CHECK CONTROL MOVEMENT']
    rows = {
        1: [('bolt',4,'AN3-4A'), ('washer',4,'AN960-10L'), ('locknut',4,'AN365-1032A')],
        2: [('bolt',2,'AN174-20'), ('washer',2,'AN960-416L'), ('castle',2,'AN320-4'), ('cotter',2,'MS24665-208')],
        3: [('bolt',2,'AN3-6'), ('washer',2,'AN960-10L'), ('castle',2,'AN310-3'), ('cotter',2,'MS24665-132')],
        4: [('rodend',2,'RSM4B'), ('checknut',2,'AN316-4R  ?'), ('hexnut',2,'AN345-524  ?')],
        5: [('bolt',2,'AN3-7A'), ('washer',2,'AN960-10L'), ('locknut',2,'AN365-1032A')],
    }
    detail_titles={1:'MOUNT DETAIL · 2 OF 4', 2:'PIVOT DETAIL · 1 OF 2',
                   3:'INTERCONNECT · 1 OF 2', 5:'BOTH PUSHROD ENDS'}
    for stage in range(1, 7):
        if not (RAW / f'main_{stage:02d}.png').exists():
            if '--preview' in sys.argv: continue
            raise FileNotFoundError(f'Missing render for step {stage}')
        p = Page()
        p.rect((65,55,190,180), fill=INK)
        p.text((86,66), f'{stage:02d}',82,'white',True)
        p.text((230,53),'BEARHAWK COMPANION / CTRL–001',25,MUTED,True)
        p.text((230,98),titles[stage-1],49,INK,True,max_width=1900)
        p.line((65,215,2135,215))
        bounds = p.image(RAW/f'main_{stage:02d}.png',(35,245,1320,1110))
        if stage==2:
            for label,uv in json.loads((RAW/'landmarks.json').read_text()).items():
                x=bounds[0]+uv[0]*bounds[2]; y=bounds[1]+(1-uv[1])*bounds[3]
                p.line((x+12,y+5,x+62,y+17),MUTED,2)
                p.text((x+70,y-22),label,28,INK,True)
        p.line((1370,260,1370,1360),RULE,2)
        p.text((1410,260),'HARDWARE' if stage<6 else 'MOVEMENT CHECK',28,MUTED,True)
        for i,(kind,qty,pn) in enumerate(rows.get(stage, [])):
            y=315+i*76
            p.image(RAW/f'icon_{kind}.png',(1400,y,160,76))
            p.text((1580,y+20),f'{qty}×',35,BLUE,True)
            p.text((1660,y+20),pn,34,INK,True,max_width=480)
        if stage in detail_titles:
            p.text((1410,640),detail_titles[stage],28,MUTED,True)
            p.rect((1385,690,2135,1273),outline=RULE)
            p.image(RAW/f'detail_{stage:02d}.png',(1390,695,740,573))
        if stage==1:
            p.text((1410,1320),'SEE PLAN 28',28,INK,True)
        elif stage==2:
            p.warning(1310,'SOURCE CONFLICT — VERIFY')
        elif stage==3:
            p.image(RAW/'icon_bushing.png',(1400,1288,105,78))
            p.text((1530,1302),'PRESS-IN BUSHING',27,INK,True)
            p.text((1530,1340),'SEE PLAN 28',26,MUTED)
        elif stage==4:
            p.warning(660,'? VERIFY HARDWARE',40)
            p.text((1410,740),'NUT APPLICATION',30,INK,True)
            p.text((1410,790),'SEE PLAN 28 / FACTORY',28,MUTED,True)
            p.text((1410,895),'NUTS SHOWN SEPARATELY',27,MUTED)
        elif stage==5:
            p.warning(1290,'SOURCE CONFLICT — VERIFY')
            p.warning(1335,'? VERIFY POSITION · BELLCRANK',27)
        else:
            for i,label in enumerate(['FORE / AFT', 'LEFT / RIGHT', '? VERIFY CLEARANCE', 'SEE PLAN 28']):
                p.text((1410,345+i*76),label,34,WARNING if label.startswith('?') else INK,True)
            p.warning(760,'? VERIFY HARDWARE',34)
            p.text((1410,815),'PUSHROD NUT APPLICATION',28,INK)
            p.warning(940,'? VERIFY POSITION',34)
            p.text((1410,995),'BELLCRANK / SPACERS',28,INK)
            p.text((1410,1150),'ILLUSTRATIVE NEUTRAL POSE',27,MUTED)
        if stage!=4:
            p.line((205,1280,100,1330),INK,5)
            p.polygon([(100,1330),(115,1305),(126,1330)],INK)
            p.text((80,1340),'FWD',28,INK,True)
        else:
            p.text((75,1325),'BENCH ASSEMBLY',27,MUTED,True)
        if stage<6:
            p.text((380,1325),'BLUE: NEW PART',25,BLUE,True)
            p.text((735,1325),'ARROW: INSTALL',25,WARNING,True)
        else:p.text((380,1325),'ARROWS: CHECK MOVEMENT',25,WARNING,True)
        p.footer('CTRL–001',stage)
        p.save(ASSETS/f'CTRL001_step_{stage:02d}_v2.png')
    pages=[ASSETS/f'CTRL001_step_{i:02d}_v2.png' for i in range(1,7)]
    if all(path.exists() for path in pages):
        overview=Image.new('RGB',(2250,1100),'#E7ECEF')
        draw=ImageDraw.Draw(overview)
        draw.text((25,18),'CTRL–001 v2 / BEARHAWK COMPANION',font=Page().font(16,True),fill=INK)
        for i,path in enumerate(pages):
            im=Image.open(path);im.thumbnail((720,491),Image.Resampling.LANCZOS)
            overview.paste(im,(25+(i%3)*740,80+(i//3)*505))
        overview.save(ASSETS/'CTRL001_overview_v2.png')
        manifest={
            'id':'CTRL001','revision':2,'title':'Control sticks / forward elevator controls',
            'slug':'controls/control-sticks', 'pdf':'01_Control_Sticks.pdf',
            'steps':[{'number':i,'title':title,'image':f'CTRL001_step_{i:02d}_v2.png'} for i,title in enumerate(titles,1)],
            'warnings':['Pushrod nut application','Bellcrank position / spacers','Source conflicts: steps 02 and 05'],
            'hardware_authority':'Companion+Hardware+Customer+-+Sheet1-2.pdf, supplied 2026-09-13, page 2, HK-CS4',
            'geometry_authority':'Bob Barrows Companion sheets 28, 17, 18',
        }
        (ASSETS/'assembly.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

if __name__=='__main__':
    if '--worker' in sys.argv:worker()
    else:
        p=argparse.ArgumentParser();p.add_argument('--blender',default=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe');p.add_argument('--compose-only',action='store_true');p.add_argument('--preview',action='store_true');args=p.parse_args()
        if not args.compose_only:
            import subprocess
            RAW.mkdir(parents=True,exist_ok=True)
            command=[args.blender,'--background','--python',str(Path(__file__).resolve()),'--','--worker']
            if args.preview:command.append('--preview')
            with open(RAW/'blender.log','w',encoding='utf-8') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
        compose()
