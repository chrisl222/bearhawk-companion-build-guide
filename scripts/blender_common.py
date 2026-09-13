"""Approved CTRL001 primitive and camera helpers reused by Phase 3."""
import math
from visual_standard import PALETTE_3D, RENDER_SCALE
def helpers():
    import bpy
    from mathutils import Vector
    V=Vector
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
        s['authority']='See embedded assembly.json for exact sources. ILLUSTRATIVE — NOT TO SCALE.'
        s['verification']='See HUMAN_REVIEW_REQUIRED.md. No dimensional validation from illustration.'
        return s
    return locals()
