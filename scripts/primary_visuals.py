"""Bulk Blender illustrations in the approved CTRL001 visual language.

Run ordinary Python: primary_visuals.py [--ids CTRL002 WING003] [--compose-only]
All geometry is illustrative. Specs identify supported operations and omissions.
The scene is never a drilling pattern, rigging jig or manufacturing drawing.
"""
from pathlib import Path
import sys,json,math,argparse,subprocess
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
RAW=ROOT/'work/primary-renders'
BLENDER=Path(r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe')

def worker(ids):
    import bpy
    from mathutils import Vector
    from blender_common import helpers
    V=Vector
    def polyline(name,pts,r=.12,mat='old'):
        for i,(a,b) in enumerate(zip(pts,pts[1:])):tube(f'{name}.{i}',a,b,r,mat)
    def label3(name,text,loc,size=.8,mat='hardware'):
        curve=bpy.data.curves.new(name,'FONT');curve.body=text;curve.size=size;curve.align_x='CENTER'
        o=bpy.data.objects.new(name,curve);bpy.context.scene.collection.objects.link(o);o.location=loc
        o.data.materials.append(mats[mat]);return o
    def fastener(p,axis=(0,0,1),name='documented_bolt',length=2,exploded=False):
        # Washer positions are deliberately not synthesized here. The page says
        # when the full stack is unresolved; detail depicts the supported axis.
        a=V(axis).normalized();p=V(p);q=p-a*(length/2+(1 if exploded else 0))
        tube(name,q,q+a*length,.13,'hardware')
        if name.startswith(('AN507','MS20426')):
            bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=.26,radius2=.13,depth=.20,location=q-a*.1)
            o=bpy.context.object;o.rotation_euler=a.to_track_quat('Z','Y').to_euler();finish(o,name+'_flush_head','hardware')
        else:tube(name+'_head',q-a*.2,q,.26,'hardware',32 if name.startswith(('AN526','CCP-','AN393','AN394')) else 6)
        if exploded:dashed(p-a*3,p+a*3);arrow('insert',q-a*1.2,q-a*.3,.075)
    def lug(p,axis=(1,0,0),mat='old',r=.48):
        return ring('attachment_eye',p,axis,r,.16,.22,mat)
    def rod(a,b,mat='new',radius=.18):
        a,b=V(a),V(b);d=(b-a).normalized()
        tube('pushrod',a+d*.45,b-d*.45,radius,mat)
        for p in [a,b]:lug(p,(1,0,0),mat,.38)
    def cable(pts,mat='new'):
        polyline('cable',pts,.065,mat)
    def terminal(p,d=(0,1,0),mat='new'):
        p=V(p);d=V(d).normalized();lug(p,(0,0,1),mat,.43)
        tube('cable_sleeve',p+d*.7,p+d*1.1,.19,mat)
        cable([p+d*.25,p+d*3],mat)
    def fork(p,axis=(0,0,1),mat='old'):
        p=V(p);a=V(axis)
        for side in [-1,1]:lug(p+a*.42*side,axis,mat,.50)
    def spring(a,b,mat='new'):
        a,b=V(a),V(b);d=b-a;q=d.normalized().to_track_quat('Z','Y')
        pts=[a+q@V((.28*math.cos(i*math.tau/12),.28*math.sin(i*math.tau/12),d.length*i/120)) for i in range(121)]
        polyline('spring_symbol',pts,.055,mat)
    def floor_frame():
        for x in [-13,13]:tube('longeron',(x,-7,-1),(x,13,-1),.36,'context')
        for y in [-5,6,12]:tube('cross_tube',(-13,y,-1),(13,y,-1),.33,'context')
    def pedals(toes=True,cylinders=False,highlight='base',lift=0):
        floor_frame()
        for y in [-.6,.6]:tube('rudder_torque_tube',(-12,y,lift),(12,y,lift),.38,'new' if highlight=='base' else 'old')
        for i,x in enumerate([-9,-3,3,9]):
            yy=-.6 if i%2==0 else .6
            mm='new' if highlight=='base' else 'old'
            tube('pedal_upright',(x,yy,lift),(x,yy+1,5+lift),.29,mm)
            tube('rudder_foot_bar',(x-2.0,yy+1,5+lift),(x+2.0,yy+1,5+lift),.38,mm)
            if toes:
                mm='new' if highlight=='toe' else 'old'
                polyline('toe_pedal',[(x,yy+.7,5+lift),(x,yy+.6,6.5+lift),(x,yy-.1,8+lift)],.23,mm)
                tube('toe_bar',(x-1.6,yy-.1,8+lift),(x+1.6,yy-.1,8+lift),.20,mm)
                ring('toe_pivot',(x,yy+1,5+lift),(1,0,0),.53,.39,1.1,mm)
            if cylinders:
                mm='new' if highlight=='cylinder' else 'old';a=V((x,-4,-.4));b=V((x,-1,6.5));d=(b-a).normalized()
                tube('master_cylinder_body',a+d*.4,a+(b-a)*.68,.43,mm)
                tube('master_cylinder_rod',a+(b-a)*.65,b,.16,'hardware')
                for p in [a,b]:lug(p,(1,0,0),mm)
        for x in [-11,11]:
            box('mount_foot',(x,0,-.45+lift),(1.5,3,.15),'new' if highlight=='base' else 'old')
            ring('pedal_saddle',(x,0,lift),(1,0,0),.85,.40,1.15,'old')
        # The V couples the opposed assemblies; no fabricated dimensions.
        polyline('center_coupling',[(-2,-.6,lift),(0,-2,lift),(2,.6,lift)],.30,'old')
    def wing_context(length=30):
        # Three neighboring ribs only: explicitly partial structural context.
        for y,h in [(0,4),(17,2.3)]:box('spar_partial',(length/2,y,h/2),(length,.18,h),'context')
        for x in [0,length/2,length]:
            pts=[(x,-7,0),(x,-6,1.6),(x,-3,3.4),(x,0,4),(x,7,3.5),(x,17,2.3),(x,23,.15),(x,23,0),(x,-7,0)]
            polyline('rib_perimeter_partial',pts,.17,'context')
            for y,r in [(2,1.35),(9,1.0),(15,.65)]:ring('rib_lightening_hole',(x,y,1.7),(1,0,0),r+.11,r,.15,'context')
        return length
    def flat_panel(name,x0,x1,y0,y1,z,mat='new',hole=None):
        pts=[(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)]
        return plate(name,pts,(0,0,1),.10,mat,holes=hole or [])
    def outline_rect(name,x0,x1,y0,y1,z,mat='old',r=.13):
        polyline(name,[(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z),(x0,y0,z)],r,mat)
    def tail_frame():
        for z in [-7,0]:
            for x in [-2.5,2.5]:tube('tail_longeron',(x,-8,z),(x,19,z),.3,'context')
        tube('tailpost',(0,18,-7),(0,18,18),.32,'context')
        tube('fin_front',(0,-8,0),(0,17,18),.3,'context')
        for y in [-6,8,18]:tube('tail_cross',(-2.5,y,0),(2.5,y,0),.25,'context')
    def stabilizers(mat='old',elevator=False,spread=0):
        tail_frame()
        for sign in [-1,1]:
            def P(x,y,z=0):return(sign*(x+spread),y,z)
            if not elevator:
                pts=[P(2,-5),P(12,-4.2),P(25,-1.5),P(34,3),P(38,8),P(39,12),P(2,12),P(2,-5)]
                polyline('stabilizer_outline',pts,.28,mat)
                for x,y in [(10,-4),(20,-2.7),(30,1.0)]:tube('stabilizer_rib',P(x,y),P(x,12),.12,mat)
                tube('stabilizer_diagonal',P(2,-5),P(30,12),.18,mat)
            else:
                pts=[P(2,12.8),P(39,12.8),P(38,17),P(34,21),P(26,24),P(13,26),P(2,26),P(2,12.8)]
                polyline('elevator_outline',pts,.24,mat)
                for x,yy in [(10,26),(20,25),(30,22.5)]:tube('elevator_rib',P(x,12.8),P(x,yy),.12,mat)
                outline_rect('trim_tab',sign*10,sign*20,23,26,0,'old',.14)
    def hinge(p,vertical=False,active=True):
        p=V(p);axis=V((0,0,1) if vertical else (1,0,0))
        ring('hinge_wrap',p,axis,.61,.42,.9,'new' if active else 'old')
        boltaxis=(0,1,0) if vertical else (0,0,1)
        a=V(boltaxis)
        for s in [-1,1]:box('hinge_strap_end',p+V((0,.7,0))+a*.48*s,(1.05,.9,.15),'new' if active else 'old')
        return p+V((0,.7,0))
    def horns(mat='new',trim=False):
        tube('elevator_torque_tube',(-8,0,0),(8,0,0),.45,'old')
        for x in [-.4,.4]:
            plate('elevator_horn',[(x,0,-3.5),(x,0,3.5),(x,1,2.5),(x,1,-2.5)],(1,0,0),.12,mat,
                  [((x,.4,z),.16) for z in [-3,-1.8,1.8,3]])
    def gear(which='front',shock_mode=False):
        floor_frame()
        for s in [-1,1]:
            a=(s*11,-4,-1);b=(s*11,9,-1);c=(s*21,-1,-19)
            tube('main_gear_forward',a,c,.70,'old' if shock_mode else 'new')
            tube('main_gear_rear',b,c,.51,'old' if shock_mode else 'new')
            tube('axle',c,(s*25,-1,-19),.5,'old')
            for p in [a,b]:lug(p,(0,1,0),'old',.8)
            u=V((s*2,4,-2));l=V((s*19,-1,-16));d=l-u
            tube('shock_body',u,u+d*.65,.55,'new' if shock_mode else 'old')
            tube('shock_rod',u+d*.60,l,.27,'hardware')
            lug(u,(0,1,0),'new' if shock_mode else 'old',.7);lug(l,(0,1,0),'new' if shock_mode else 'old',.7)
        return (2,4,-2) if which=='upper' else (19,-1,-16) if which=='lower' else (11,-4,-1) if which=='front' else (11,9,-1)
    def airsurface(kind='flap',edge=False,balance=False):
        for x in [0,6,12,18,24,30]:
            polyline('surface_rib',[(x,0,0),(x,1,1.7),(x,4,1.6),(x,9,.8),(x,13,.1)],.12,'old')
        tube('surface_front_spar',(0,2,1),(30,2,1),.3,'old')
        outline_rect('trailing_edge',0,30,12,13.3,3 if edge else .1,'new')
        if balance:
            tube('balance_tube',(-4,.8,.8),(29,.8,.8),.38,'new')
            tube('sealed_outboard_end',(28.7,.8,.8),(29,.8,.8),.4,'hardware')
            arrow('insert_balance',(-7,.8,.8),(-4.5,.8,.8),.13)
        if edge:
            for x in [5,25]:arrow('fit_edge',(x,14,4),(x,13,.7),.14)
    def model(m,s):
        typ=m['model'];view=s['view'];collection('ASSEMBLY.'+m['id']+'.'+view)
        cfg=dict(target=(0,0,0),scale=35,cam=(35,-45,30),detail=(0,0,0),dscale=8,direction='FWD',caption='')
        def set_(target,scale,detail=None,dscale=8,cam=None,caption=''):
            cfg.update(target=target,scale=scale,detail=detail if detail is not None else target,dscale=dscale,caption=caption)
            cfg['cam']=tuple(V(target)+V(cam or (35,-45,30)))
        if typ=='pedals':
            pedals(view=='toe',highlight='toe' if view=='toe' else 'base',lift=2 if view=='mount' else 0)
            if view=='mount':
                for x in [-11,11]:arrow('lower_assembly',(x,4,4),(x,4,.3),.17)
                fastener((11,1,-.1),name='AN3-4A',exploded=True)
            else:fastener((9,1.6,5),(1,0,0),'AN4-21',3,True)
            set_((0,2,2),36,(9,1,3.5),12)
        elif typ=='brakes':
            pedals(True,True,'cylinder');p=(9,-4,-.4) if view=='lower' else (9,-1,6.5)
            fastener(p,(1,0,0),'AN3-6' if view=='lower' else 'AN3-7',2,True);set_((0,0,3),37,p,9)
        elif typ=='rudder_cable':
            if view=='pedal':
                tube('pedal_base',(-8,0,0),(6,0,0),.45,'old')
                plate('adjustment_tab',[(6,-3,3),(6,4,3),(6,4,4),(6,-3,4)],(1,0,0),.16,'new', [((6,y,3.5),.16) for y in [-2,0,2,3]])
                tube('rudder_cable_arm',(6,0,0),(6,0,3.5),.23,'old');fork((6,3,3.5),(1,0,0),'new')
                cable([(6,3,3.5),(6,10,3.5)]);spring((6,-2,3.5),(6,-6,3.5),'old')
                fastener((6,3,3.5),(1,0,0),'AN3-5',2,True);set_((2,2,2),21,(6,3,3.5),8)
            else:
                tube('rudder_post',(0,1,-1),(0,1,10),.4,'context')
                plate('rudder_horn',[(-6,0,0),(6,0,0),(2,2,0),(-2,2,0)],(0,0,1),.18,'old')
                for x in [-5.5,5.5]:fork((x,.4,0),(0,0,1),'new');terminal((x,-1,0),(0,-1,0));fastener((x,.4,0),name='AN4-6',exploded=x>0)
                set_((0,-1,1),21,(5.5,.4,0),8)
        elif typ=='flap_handle':
            if view=='splitter':
                for x in [-12,12]:tube('baggage_frame',(x,0,-6),(x,0,12),.35,'context')
                tube('baggage_upper',(-12,0,12),(12,0,12),.35,'context')
                plate('splitter',[(-1.7,0,0),(1.7,0,0),(0,0,-2)],(0,1,0),.18,'new', [((-1.3,0,-.2),.16),((1.3,0,-.2),.16),((0,0,-1.6),.16)])
                cable([(0,0,-7),(0,0,-1.6)])
                for x in [-1.3,1.3]:
                    rod((x,0,-.2),(x*2,0,2),'new',.20);cable([(x*2,0,2),(12 if x>0 else -12,0,11)])
                    ring('upper_flap_pulley',(12 if x>0 else -12,0,11),(0,1,0),1.0,.18,.3,'old')
                set_((0,0,3),31,(0,0,0),9,cam=(20,-42,15),caption='REAR BAGGAGE · RELATIONSHIPS ONLY')
            else:
                floor_frame();tube('pivot_support',(0,4,0),(0,4,6),.36,'context')
                tube('flap_handle',(0,4,6),(0,-11,9),.43,'new');tube('handle_grip',(0,-11,9),(0,-14,9.6),.55,'new')
                angles=[math.pi*.5+i*math.pi*.5/32 for i in range(33)]
                pts=[(0,4+6.6*math.cos(a),6+6.6*math.sin(a)) for a in angles]+[(0,4+5.3*math.cos(a),6+5.3*math.sin(a)) for a in reversed(angles)]
                holes=[((0,4+5.35*math.cos(a),6+5.35*math.sin(a)),.30) for a in [math.pi*f for f in [.57,.70,.83,.94]]]
                plate('notched_quadrant',pts,(1,0,0),.19,'old',holes)
                tube('release_rod',(.42,-11,9.35),(.42,-1.2,7.4),.12,'hardware')
                tube('detent_pin',(-.5,-1.2,7.4),(.65,-1.2,7.4),.14,'hardware')
                tube('quadrant_lower_support',(0,-2,6),(0,-2,-1),.25,'old')
                plate('cable_pull_arm',[(0,4,6),(0,7,0),(0,6,0)],(1,0,0),.2,'new')
                if view=='cable':fork((0,6.4,.4),(1,0,0),'new');cable([(0,6.4,.4),(0,12,.4)]);fastener((0,6.4,.4),(1,0,0),'AN3-5',2,True)
                else:arrow('engagement',(2,-2,9),(2,-1.2,7.5),.13)
                set_((0,-1,3),30,(0,6.4,.4) if view=='cable' else (0,-1.2,7.4),9,cam=(35,15,25))
        elif typ=='elevator_horn':
            horns('new' if view=='union' else 'old')
            zs=[-1.8,1.8] if view=='union' else [-3,3]
            for z in zs:
                ring('aluminum_bushing' if view=='union' else 'steel_bushing',(0,.4,z),(1,0,0),.25,.14,.68,'new')
                fastener((0,.4,z),(1,0,0),'AN3-6A' if view=='union' else 'AN3-6',2,True)
                if view=='cables':cable([(0,.4,z),(0,-8,z)]);lug((0,.4,z),(1,0,0),'new',.38)
            set_((0,-1,0),20,(0,.4,3 if view=='cables' else 1.8),8,cam=(28,-38,18))
        elif typ=='floors':
            floor_frame()
            for y in [-4,8]:tube('control_torque_tube',(-12,y,.3),(12,y,.3),.52,'old')
            for a,b in [(-11,-1),(1,11)]:
                flat_panel('floor_panel',a,b,-2.6,6.5,3 if view=='fit' else -.35,'new')
                if view=='fit':arrow('lower_panel',((a+b)/2,2,5),((a+b)/2,2,.4),.17)
            if view=='attach':box('mount_tab',(10,6,-.65),(2,2,.14),'context');fastener((10,6,-.4),name='AN526C-632-6',exploded=True)
            set_((0,2,0),33,(10,6,-.4),8,caption='FLOOR SHAPES FIT TO AIRFRAME')
        elif typ=='stabilizer':
            stabilizers('new' if view=='halves' else 'old',spread=4 if view=='halves' else 0)
            if view=='carry':
                tube('forward_carry_through',(-6,-5,1),(6,-5,1),.4,'new')
                for x in [-2,2]:fastener((x,-5,1),name='AN4-22A',exploded=True)
            elif view=='halves':
                for sign in [-1,1]:arrow('slide_half',(sign*10,-7,2),(sign*4,-7,2),.22)
            else:
                for sign in [-1,1]:rod((sign*2.5,-4,-7),(sign*27,0,0),'new',.28);fork((sign*27,0,0),(0,0,1),'new')
            set_((0,4,0),100,(27,0,0) if view=='brace' else (2,-5,0),11)
        elif typ=='elevators':
            stabilizers('context');stabilizers('new',True)
            xx=4 if view=='inboard' else 29
            for sign in [-1,1]:p=hinge((sign*xx,12,0));fastener(p,name='AN4-14A' if view=='inboard' else 'AN4-18A',length=2,exploded=sign>0)
            set_((0,10,0),97,(xx,12,0),9)
        elif typ=='rudder':
            tail_frame();polyline('rudder_outline',[(0,19,0),(0,19,20),(0,22,22),(0,28,19),(0,32,12),(0,30,3),(0,19,0)],.27,'new')
            for z,y in [(6,31),(12,32),(18,29)]:tube('rudder_rib',(0,19,z),(0,y,z),.13,'new')
            for z in [2,16]:hinge((0,18,z),True,z==16)
            if view=='upper':fastener((0,18.7,16),(0,1,0),'AN4-17A',2,True)
            set_((0,15,7),42,(0,18.7,16),9,cam=(40,40,23),caption='LOWER HINGE HARDWARE UNRESOLVED')
        elif typ=='tail_wires':
            stabilizers('old');
            for sign in [-1,1]:
                for y in [-3,12]:
                    a=(0,18,17);b=(sign*29,y,0);cable([a,b]);terminal(b,(0,1,0),'new')
            set_((0,7,6),97,(29,12,0),11,caption='WIRE LENGTHS / TENSION NOT DEPICTED')
        elif typ=='trim':
            if view=='wheel':
                tube('spar_carry_through',(-9,0,4),(9,0,4),.6,'context')
                for x in [-.6,.6]:tube('trim_standoff',(x,0,4),(x,4,3),.22,'old')
                ring('trim_wheel',(0,4,3),(1,0,0),3.2,2.8,.3,'new');ring('chain_sprocket',(0,4,3),(1,0,0),.8,.2,.7,'hardware')
                for z in [2.2,3.8]:cable([(0,4,z),(0,12,z)],'new')
                fastener((0,4,3),(1,0,0),'AN4-22',3,True);set_((0,4,3),24,(0,4,3),11)
            else:
                tube('trim_torque_tube',(-11,0,0),(11,0,0),.3,'old')
                for x in [-7,7]:
                    tube('trim_actuating_arm',(x,0,0),(x,0,-2),.19,'old')
                    rod((x,0,-2),(x,9,-2),'new');flat_panel('trim_tab',x-2,x+2,8,12,-.7,'old')
                    tube('tab_horn',(x,9,-.7),(x,9,-2),.18,'old');fastener((x,9,-2),(1,0,0),'AN3-6A',2,x>0)
                set_((0,4,-1),30,(7,9,-2),8)
        elif typ in ['gear','shock']:
            p=gear(view,typ=='shock');fastener(p,(0,1,0),s['hardware'][0][2],3,True)
            gc=(42,60,30) if view=='rear' else (-42,-60,30) if view=='lower' else (42,-60,30)
            set_((0,2,-8),61,p,12,cam=gc,caption='SUPPORTED ASSEMBLY · ALIGNMENT NOT SET')
        elif typ=='seats':
            floor_frame()
            for sign in [-1,1]:
                x=sign*6
                outline_rect('seat_base',x-4,x+4,-3,7,3,'old',.3)
                for xx in [x-3,x+3]:tube('seat_track',(xx,-5,0),(xx,11,0),.28,'context')
                pts=[(x-4-sign*.4,7,3),(x-4-sign*.4,9,15),(x+4-sign*.4,9,15),(x+4-sign*.4,7,3)]
                polyline('seat_back',pts,.3,'new' if view=='backs' else 'old')
                for xx in [x-3,x+3]:
                    for y in [-2,6]:ring('seat_roller',(xx,y,.65),(1,0,0),.6,.16,.6,'new' if view=='rollers' else 'old')
            p=(9,6,.65) if view=='rollers' else (9.6,7,3);fastener(p,(1,0,0) if view=='rollers' else (-1,0,0),s['hardware'][0][2],2,True)
            set_((0,2,6),41,p,9,cam=(35,40,25) if view=='backs' else (35,-45,30))
        elif typ=='stringers':
            for x in [-5,5]:tube('longeron',(x,-12,0),(x,14,0),.33,'context')
            for y in [-9,0,9]:
                tube('cross_structure',(-5,y,0),(5,y,0),.3,'context')
                for x in [-3,3]:
                    tube('standoff',(x,y,0),(x,y,2),.17,'old')
                    box('saddle_base',(x,y,2),(1.2,1.2,.1),'old')
                    for xx in [x-.5,x+.5]:box('saddle_side',(xx,y,2.35),(.1,1.2,.7),'old')
            for x in [-3,3]:box('stringer',(x,0,4 if view=='fit' else 2.45),(.7,28,.7),'new')
            if view=='fit':arrow('seat_stringer',(5,0,5),(5,0,2.5),.13)
            else:fastener((3,0,2.45),(1,0,0),'CCP-42',1.7,True)
            set_((0,0,2),34,(3,0,2.3),7,caption='LOCAL STANDOFF RELATIONSHIP')
        elif typ=='fuel_valve':
            floor_frame();plate('selector_bracket',[(-3,-5,0),(7,-5,0),(7,9,0)],(0,0,1),.15,'new' if view=='bracket' else 'old')
            if view=='valve':
                box('selector_body',(5,-3,1.2),(2.7,2.7,2.2),'new');tube('selector_round_face',(5,-3,2.3),(5,-3,2.5),1.8,'new')
                tube('selector_handle',(5,-3,2.6),(5,-1.3,2.6),.28,'hardware')
                for p in [(4,-4,0),(6,-4,0),(5,-1.5,0)]:fastener(p,name='AN507C632R6',length=1.5,exploded=False)
            else:arrow('bracket_lower',(4,2,6),(4,2,1),.18)
            set_((2,1,1),30,(5,-3,1),10,caption='PORTS / GASCOLATOR NOT RECONSTRUCTED')
        elif typ=='wing_prep':
            wing_context(42);flat_panel('tank_cover',2,13,1,14,7,'new');flat_panel('pocket_skin',27,39,20,22,5,'new')
            if view=='labels':box('serial_tag',(0,-2,3),(1.8,.10,.8),'hardware');arrow('retain_tag',(-6,-2,6),(-1,-2,3),.14)
            else:box('inventory_box',(29,7,5),(7,6,4),'new');arrow('remove_box',(29,7,8),(29,7,12),.2)
            set_((19,7,3),59,(3,6,5) if view=='labels' else (29,7,5),18,caption='PARTIAL WING · MATCH FACTORY LABELS')
        elif typ=='tank_cover':
            wing_context();outline_rect('tank_bay',16,29,0,17,0,'old',.25)
            if view=='cover':flat_panel('matched_tank_cover',16,29,0,17,-4,'new');arrow('raise_cover',(23,8,-7),(23,8,-1),.18)
            else:
                for x in [17,20,23,26,29]:box('forward_nutplate',(x,0,-.3),(1.0,.5,.3),'new')
                for x in [17,20,23,26,29]:box('aft_nutplate_pending',(x,17,-.3),(1.0,.5,.3),'old')
            set_((16,7,0),45,(23,0,-.3),10,cam=(30,-40,-28),caption='MAIN TANK BAY · PREPARATION ONLY')
        elif typ=='aileron_bellcrank':
            wing_context();tube('aileron_crossmember',(15,1,2),(15,18,2),.36,'old')
            p=V((15,13,2));axis=V((0,0,1))
            if view!='pulley':
                # Factory photos show the bearing axis through wing thickness,
                # with the output arm extending aft through the factory opening.
                for o in list(bpy.context.scene.objects):
                    if o.name.startswith('spar_partial') and abs(o.location.y-17)<.01:bpy.data.objects.remove(o,do_unlink=True)
                for x,length in [(7,14),(23,14)]:box('rear_spar_partial',(x,17,1.15),(length,.18,2.3),'context')
                ring('bellcrank_pivot',p,axis,.8,.51,2.2,'new')
                tube('bellcrank_output_arm',p-axis*.85,(15,20,1.15),.23,'new');lug((15,20,1.15),axis,'new')
                tube('bellcrank_diagonal',p+axis*.85,(15,18,1.15),.18,'new')
                tube('bellcrank_cable_arm',(15,16,1.15),(15,16,2.8),.19,'new');lug((15,16,2.8),axis,'new')
                for sign in [-1,1]:ring('R4FF',p+axis*sign*(2.1 if view=='bearings' else 1.05),axis,.52,.17,.35,'hardware')
                if view=='bearings':ring('bearing_inner_spacer',p,axis,.25,.15,1.3,'hardware');arrow('press',p+axis*4,p+axis*2.5,.14)
                else:
                    for sign in [-1,1]:ring('AN970-4',p+axis*sign*1.55,axis,.73,.17,.12,'hardware')
                    fastener(p,axis,'AN4-27A',4,True)
            else:
                p=V((15,2,2));ring('AN210-4A',p,(0,0,1),1.35,.18,.45,'new');ring('cable_guard',p,(0,0,1),1.56,1.4,.65,'old');fastener(p,name='AN4-24A',length=3,exploded=True)
            set_((15,10,2),39,p,12,cam=(32,40,35) if view=='pulley' else (32,-5,40),caption='' if view=='pulley' else 'PARTIAL STRUCTURE · FACTORY OPENING NOT A TEMPLATE')
        elif typ=='wing_cables':
            wing_context(42)
            if view=='actuation':
                pts=[(4,-5,-10),(4,1,1.8),(28,1,1.8),(28,14,1.8)]
                for x,y in [(4,1),(28,1)]:ring('cable_pulley',(x,y,1.8),(0,0,1),1.0,.16,.3,'old')
                cable(pts);arrow('route',(17,0,3),(23,0,3),.15);detail=(28,1,1.8)
            else:
                cable([(-9,16,2),(0,16,2),(21,16,2),(28,14,2)])
                for x in [0,21]:ring('cable_fairlead',(x,16,2),(1,0,0),.6,.25,.6,'new')
                arrow('toward_cabin',(-2,19,3),(-7,19,3),.15);detail=(21,16,2)
            set_((17,9,0),57,detail,11,cam=(32,-5,60),caption='RELATIONSHIPS ONLY · NOT A HOLE MAP')
        elif typ=='flap_tube':
            wing_context();tube('flap_support',(15,5,2),(15,18,2),.32,'old')
            tube('flap_torque_tube',(-3,12,2),(18,12,2),.42,'new' if view=='tube' else 'old')
            for x in [14,16]:
                ring('arm_collar',(x,12,2),(1,0,0),.62,.43,.7,'new')
                tube('flap_actuator_arm',(x,12,2),(x,16,-1),.25,'new');lug((x,16,-1),(1,0,0),'new')
            if view in ['pushrod','spring']:
                tube('pushrod_cross_tube',(14,16,-1),(16,16,-1),.30,'new')
                rod((15,16,-1),(15,23,-1),'new');fastener((15,16,-1),(1,0,0),'AN3-26',4,True)
            if view=='spring':spring((15,13,1),(15,7,2));tube('rubber_bumper',(14,16,2),(16,16,2),.53,'hardware')
            set_((13,12,1),37,(15,16,-1),12,caption='JIG POSITION MUST COME FROM FACTORY DATA')
        elif typ in ['flap_surface','aileron_surface']:
            airsurface(typ,view=='fit',view=='balance')
            if view=='rivet':
                for x in [0,6,12,18,24,30]:fastener((x,12.7,.1),name='CCP-42',length=.7)
            set_((14,7,1),40,(12,12.7,.2) if view!='balance' else (0,.8,.8),9,caption='SURFACE PREPARATION · FINAL MOUNT NOT SHOWN')
        elif typ=='wing_fuel':
            wing_context();box('main_tank',(22,8,2),(12,12,4),'old')
            for y in [3,13]:
                p=(15.8,y,1);ring('feed_port',p,(1,0,0),.55,.3,.5,'old')
                tube('AN816-6D',(13.7,y,1),(15.8,y,1),.31,'new',6)
                if view!='fittings':
                    tube('feed_tube',(-6,y,1),(14,y,1),.19,'new')
                    for x in [0,15]:ring('AN931-6-10',(x,y,1),(1,0,0),.55,.22,.2,'hardware')
            if view=='fittings':
                for y in [3,13]:tube('05-17700_strainer',(11.5,y,1),(13.5,y,1),.25,'new');arrow('insert',(10,y,2),(12,y,2),.12)
            if view=='sight':
                for z in [.5,3.5]:
                    tube('sight_line',(0,8,z),(16,8,z),.125,'new');ring('AN832-4D',(0,8,z),(1,0,0),.32,.15,.7,'hardware')
                    tube('gauge_connection',(-2,8,z),(0,8,z),.125,'new')
                tube('clear_sight_gauge_symbol',(-2,8,.5),(-2,8,3.5),.22,'new')
            set_((15,8,1),49,(14,3,1) if view!='sight' else (0,8,2),12,cam=(-45,-10,50),caption='PORT LOCATIONS TRANSFER FROM ACTUAL TANK')
        elif typ=='pitot':
            wing_context();flat_panel('mast_base',9,14,0,5,-.3,'new')
            box('pitot_mast',(11.5,2,-4),(1.1,2.5,7),'new');tube('pitot_head',(11.5,2,-7),(11.5,-3,-7),.4,'new')
            if view=='lines':
                for x in [11,12]:cable([(x,2,0),(x,4,2),(x,16,2),(-7,16,2)])
                arrow('clear_control',(13,3,4),(13,6,4),.15)
            else:
                for x in [9.5,13.5]:
                    for y in [.5,2.5,4.5]:fastener((x,y,-.3),name='AN526C-632R6',length=1.2)
            set_((12,8,-2),43,(11.5,2,-1),13,cam=(-35,35,35) if view=='lines' else (-35,35,-28),caption='SA06BL / GAP26 EXAMPLE ONLY')
        elif typ=='conduit':
            wing_context();tube('optional_conduit',(-2,10,1.7),(32,10,1.7),.42,'new')
            for x in [0,15,30]:ring('conduit_bracket',(x,10,1.7),(1,0,0),.55,.43,.35,'hardware');box('bracket_foot',(x,10,.9),(.2,1.4,.2),'new')
            if view=='plan':arrow('route_services',(-5,10,4),(5,10,4),.18)
            set_((14,8,2),42,(15,10,1.7),10,caption='OPTIONAL FACTORY METHOD · PARTIAL WING')
        elif typ=='inspection':
            # Actual nested rectangular ring geometry; ring stays same orientation.
            for a,b,c,d in [(-10,10,-8,-3.7),(-10,10,3.7,8),(-10,-4.2,-3.7,3.7),(4.2,10,-3.7,3.7)]:flat_panel('wing_skin',a,b,c,d,0,'context')
            z=-3 if view=='match' else 1.0
            for a,b,c,d in [(-5,5,-4.5,-3.7),(-5,5,3.7,4.5),(-5,-4.2,-3.7,3.7),(4.2,5,-3.7,3.7)]:flat_panel('inspection_ring',a,b,c,d,z,'new')
            flat_panel('matched_cover',-4.6,4.6,-4.1,4.1,-5 if view=='match' else -4,'old')
            arrow('move_ring_inside',(7,0,-3),(7,0,1),.16)
            for x in [-4.6,4.6]:
                for y in [-3.9,3.9]:box('nutplate',(x,y,z-.3),(.8,.45,.3),'hardware')
            set_((0,0,0),30,(4.6,3.9,z),8,cam=(28,-40,-28) if view=='match' else (28,-40,28),caption='MATCH ORIENTATION · HOLES ARE SYMBOLIC')
        elif typ=='closing':
            wing_context(42)
            panels={'root':(0,9,0,20),'main':(10,42,0,17),'aft':(0,10,17,22)}
            for name,(x0,x1,y0,y1) in panels.items():flat_panel(name+'_skin',x0,x1,y0,y1,-2 if name==view else 0,'new' if name==view else 'context')
            a,b,c,d=panels[view];arrow('close_skin',((a+b)/2,(c+d)/2,-7),((a+b)/2,(c+d)/2,-2.5),.25)
            for x in [a+1,(a+b)/2,b-1]:tube('cleco_symbol',(x,c+1,-2),(x,c+1,-3),.15,'hardware')
            set_((20,9,-1),60,((a+b)/2,c+1,-2),13,cam=(35,-45,-35),caption='SEQUENCE ONLY · VERIFY EVERY RIVET STACK')
        elif typ=='pocket':
            wing_context(42)
            for i,(a,b) in enumerate([(0,8),(9,32),(33,42)]):
                y=24 if view=='fit' else 21
                # Concave pocket skin, open aft; sheet profile is illustrative.
                pts=[(a,y+1.1-1.1*math.cos(t),1+1.05*math.sin(t)) for t in [-math.pi/2+j*math.pi/24 for j in range(25)]]
                verts=pts+[(b,yy,zz) for _,yy,zz in pts]
                mesh=bpy.data.meshes.new('pocket_skin');mesh.from_pydata(verts,[],[(j,j+1,j+26,j+25) for j in range(24)]);mesh.update()
                o=bpy.data.objects.new('pocket_skin_'+str(i),mesh);bpy.context.scene.collection.objects.link(o);o.data.materials.append(mats['new'])
                if view=='fit':arrow('fit_pocket',((a+b)/2,27,1),((a+b)/2,24.5,1),.15)
            set_((20,15,1),56,(25,21,1),12,caption='THREE PIECES · RETAIN ORIGINAL WING / POSITION')
        elif typ=='tip':
            wing_context()
            profile=[(-7,0),(-6,1.6),(-3,3.4),(0,4),(7,3.5),(17,2.3),(23,.15),(17,0),(7,-.15),(0,-.1)]
            verts=[]
            for x,shrink in [(31,1),(35,.94),(38,.70),(39,.1)]:
                verts.extend((x,8+(y-8)*shrink,z*shrink) for y,z in profile)
            faces=[tuple(range(9,-1,-1)),tuple(range(30,40))]+[(i*10+j,i*10+(j+1)%10,(i+1)*10+(j+1)%10,(i+1)*10+j) for i in range(3) for j in range(10)]
            mesh=bpy.data.meshes.new('tip_shell');mesh.from_pydata(verts,[],faces);mesh.update()
            o=bpy.data.objects.new('composite_tip',mesh);bpy.context.scene.collection.objects.link(o);o.data.materials.append(mats['new'])
            if view=='fit':arrow('slide_tip',(39,13,5),(31,13,5),.18)
            else:
                for y,z in [(-3,3.4),(3,3.8),(9,3.2),(15,2.6),(21,.8)]:fastener((31,y,z),name='AN526C-632-6',length=.8)
            set_((23,8,1),49,(31,9,3.2),11,caption='TIP PROFILE / TRIM FIT TO ACTUAL KIT')
        elif typ=='wing_attach':
            for x in [-4,4]:
                for y in [0,13]:tube('cabin_corner',(x,y,-12),(x,y,8),.4,'context')
                tube('cabin_lower_longeron',(x,0,-9),(x,13,-9),.4,'context')
            for y in [0,13]:tube('cabin_carry_through',(-4,y,8),(4,y,8),.5,'context')
            for sign in [-1,1]:
                for y in [0,13]:box('wing_spar_partial',(sign*18,y,8),(27,.3,2),'new' if view=='root' else 'old')
                if view=='strut':
                    tube('single_lift_strut',(sign*4,4,-9),(sign*27,0,7),.42,'new')
            p=(4,0,8) if view=='root' else (27,0,7);fork(p,(0,1,0),'old');fastener(p,(0,1,0),'AN6-15A',3,True)
            set_((0,6,0),75,p,12,caption='ATTACHMENT RELATIONSHIPS · WINGS SUPPORTED')
        elif typ=='root_connections':
            if view=='cable':
                cable([(-13,0,0),(-3,0,0)]);cable([(3,0,0),(13,0,0)])
                tube('AN140-22S_barrel',(-2,0,0),(2,0,0),.38,'new');lug((-3,0,0),(0,0,1),'new');lug((3,0,0),(0,0,1),'new')
                set_((0,0,0),31,(0,0,0),13,caption='CARRY-THROUGH JOINT · SAFETYING NOT SHOWN')
            else:
                tube('wing_feed',(-9,0,0),(-.6,0,0),.3,'old');tube('fuselage_feed',(.6,0,0),(9,0,0),.3,'old')
                ring('05-03598_sleeve',(0,0,0),(1,0,0),.5,.31,5,'new')
                for x in [-1.5,1.5]:ring('clamp_symbol',(x,0,0),(1,0,0),.62,.5,.2,'hardware')
                set_((0,0,0),24,(0,0,0),10,caption='ONE CONNECTION SYMBOL · CLAMP ALLOCATION UNVERIFIED')
        else:raise ValueError(typ)
        return cfg

    items=json.loads((ROOT/'specs/catalog.json').read_text(encoding='utf-8'))
    for m in items:
        if not m['steps'] or m['id']=='CTRL001' or (ids and m['id'] not in ids):continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        globals().update(helpers())
        out=RAW/m['id'];out.mkdir(parents=True,exist_ok=True)
        configs=[]
        for s in m['steps']:
            sc=scene(f'{s["number"]:02d}_{s["view"].upper()}');cfg=model(m,s);configs.append(cfg)
            sc['sources']=' | '.join(m['sources']);sc['review']=json.dumps(m['issues'])
            camera(cfg['cam'],cfg['target'],cfg['scale'],(1320,1000))
            bpy.context.view_layer.update()
            from bpy_extras.object_utils import world_to_camera_view
            origin=world_to_camera_view(sc,sc.camera,V(cfg['target']))
            forward=world_to_camera_view(sc,sc.camera,V(cfg['target'])+V((0,-5,0)))
            dx=(forward.x-origin.x)*1320;dy=-(forward.y-origin.y)*1000
            norm=math.hypot(dx,dy) or 1;cfg['fwd']=[dx/norm,dy/norm]
            sc.render.filepath=str(out/f'main_{s["number"]:02d}.png');bpy.ops.render.render(write_still=True)
            # A second camera in the same editable scene makes the detail inspectable.
            maincam=sc.camera;dt=V(cfg['detail']);offset=(V(cfg['cam'])-V(cfg['target'])).normalized()*30
            camera(dt+offset,dt,cfg['dscale'],(740,573))
            sc.camera.name='Detail_camera';sc.render.filepath=str(out/f'detail_{s["number"]:02d}.png');bpy.ops.render.render(write_still=True)
            sc.camera=maincam;sc.render.resolution_x=2640;sc.render.resolution_y=2000
        # Canonical scene is the last supported installation state, not a claim
        # that unresolved downstream operations have been completed.
        bpy.context.window.scene=bpy.data.scenes[[s.name for s in bpy.data.scenes].index(sc.name)]
        for path in [Path(__file__),ROOT/'scripts/blender_common.py',ROOT/'scripts/visual_standard.py']:
            t=bpy.data.texts.new(path.name);t.write(path.read_text(encoding='utf-8'))
        t=bpy.data.texts.new('assembly.json');t.write(json.dumps(m,indent=2,ensure_ascii=False))
        bpy.context.preferences.filepaths.save_version=0
        bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender'/f'{m["id"]}_visual_v2.blend'),compress=True)
        (out/'views.json').write_text(json.dumps(configs,default=list),encoding='utf-8')
        print('MANUAL_RENDERED',m['id'],flush=True)

def compose(ids):
    from visual_standard import Page,INK,BLUE,MUTED,RULE,WARNING
    items=json.loads((ROOT/'specs/catalog.json').read_text(encoding='utf-8'))
    icons=ROOT/'docs/assets/images/hardware'
    for m in items:
        if not m['steps'] or m['id']=='CTRL001' or (ids and m['id'] not in ids):continue
        src=RAW/m['id'];configs=json.loads((src/'views.json').read_text(encoding='utf-8'))
        dest=ROOT/'docs/assets/images'/m['id'].lower();dest.mkdir(parents=True,exist_ok=True)
        for s,cfg in zip(m['steps'],configs):
            p=Page();n=s['number']
            p.rect((65,55,190,180),fill=INK);p.text((86,66),f'{n:02d}',82,'white',True)
            p.text((230,53),'BEARHAWK COMPANION / '+m['id']+' · '+m['status'],25,MUTED,True)
            size=49
            while p.draw.textlength(s['title'],font=p.font(size,True))>1850*2:size-=1
            p.text((230,98),s['title'],size,INK,True,max_width=1880)
            p.line((65,215,2135,215));p.image(src/f'main_{n:02d}.png',(35,245,1320,1030))
            p.line((1370,260,1370,1360),RULE,2)
            p.text((1410,260),'HARDWARE' if s['hardware'] else 'ASSEMBLY CHECK',28,MUTED,True)
            for i,(kind,qty,pn) in enumerate(s['hardware']):
                y=315+i*76;p.image(icons/f'icon_{kind}.png',(1400,y,160,76))
                qs=str(qty)+'×' if isinstance(qty,int) else str(qty)
                qsize=35
                while p.draw.textlength(qs,font=p.font(qsize,True))>88*2:qsize-=1
                p.text((1565,y+20),qs,qsize,BLUE,True)
                size=34
                while p.draw.textlength(pn,font=p.font(size,True))>475*2:size-=1
                p.text((1660,y+20),pn,size,INK,True,max_width=480)
            if not s['hardware']:
                p.text((1410,335),'MATCH THE SUPPLIED PARTS',28,INK,True)
                p.text((1410,390),'KEEP ACCESS TO CONNECTIONS',28,MUTED)
            p.text((1410,640),s['detail'],25,MUTED,True,max_width=720)
            p.rect((1385,690,2135,1210),outline=RULE);p.image(src/f'detail_{n:02d}.png',(1390,695,740,510))
            # Small FWD marker is a page orientation key; X right / Y aft / Z up.
            # Compute from camera basis so composition also repairs old caches.
            cx,cy,cz=[a-b for a,b in zip(cfg['cam'],cfg['target'])]
            horizontal=math.hypot(cx,cy);length=math.sqrt(cx*cx+cy*cy+cz*cz)
            dx=-cx/horizontal;dy=-cy*cz/(horizontal*length)
            norm=math.hypot(dx,dy) or 1;dx/=norm;dy/=norm
            a=(190-dx*45,1275-dy*45);b=(190+dx*45,1275+dy*45)
            p.line((*a,*b),WARNING,5);p.polygon([b,(b[0]-dx*26-dy*12,b[1]-dy*26+dx*12),(b[0]-dx*26+dy*12,b[1]-dy*26-dx*12)],WARNING)
            p.text((130,1190),'FWD',28,INK,True)
            if cfg['caption']:p.text((300,1300),cfg['caption'],22,MUTED,True,max_width=1030)
            if s['hardware']:p.text((300,1350),'FASTENER AXES SHOWN · INVENTORY IS NOT STACK ORDER',20,MUTED,max_width=1030)
            if s['note']:
                size=27
                while p.draw.textlength(s['note'],font=p.font(size,True))>720*2:size-=1
                p.text((1410,1240),s['note'],size,INK,True,max_width=720)
            for i,flag in enumerate(s['flags']):p.warning(1300+i*39,flag,27)
            p.footer(m['id'],n);p.save(dest/s['image'])
        (dest/'assembly.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
        print('COMPOSED',m['id'],len(m['steps']),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');parser.add_argument('--compose-only',action='store_true');parser.add_argument('--ids',nargs='*');parser.add_argument('--blender',default=str(BLENDER))
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    if args.worker:worker(args.ids)
    else:
        RAW.mkdir(parents=True,exist_ok=True)
        if not args.compose_only:
            cmd=[args.blender,'-b','--python-exit-code','1','--python',str(Path(__file__)),'--','--worker']
            if args.ids:cmd+=['--ids']+args.ids
            with (RAW/'blender.log').open('w',encoding='utf-8') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
        compose(args.ids)
