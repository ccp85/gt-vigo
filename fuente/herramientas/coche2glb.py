# Convierte el coche de Tripo (.obj de ~1M triángulos + texturas PBR) en coche500.glb para el juego.
# Uso: python3 coche2glb.py modelo.obj basecolor.jpg normal.png roughness.png metallic.png coche500.glb [caras]
# 1) reduce la malla con pymeshlab (conserva las UV) a ~30k triángulos
# 2) la gira para que el frente (+Z en Tripo) mire a +X, apoya las ruedas en y=0 y la escala a lo largo del coche del juego (.165)
# 3) empaqueta base 1024, normal 1024 y metal/rugosidad 512 (canal G = rugosidad, B = metal) en un .glb
import sys,io,os,tempfile,numpy as np
from PIL import Image
import pygltflib as G
obj,fb,fn,fr,fm,out=sys.argv[1:7];caras=int(sys.argv[7]) if len(sys.argv)>7 else 30000
LARGO=.165
import pymeshlab as ml
ms=ml.MeshSet();ms.load_new_mesh(obj)
ms.meshing_decimation_quadric_edge_collapse_with_texture(targetfacenum=caras,qualitythr=.5,preserveboundary=True,preservenormal=True,optimalplacement=True,extratcoordw=1)
tmp=os.path.join(tempfile.mkdtemp(),'dec.obj');ms.save_current_mesh(tmp,save_textures=False)
P=[];T=[];faces=[]
for l in open(tmp):
    t=l.split()
    if not t:continue
    if t[0]=='v':P.append(list(map(float,t[1:4])))
    elif t[0]=='vt':T.append(list(map(float,t[1:3])))
    elif t[0]=='f':
        c=[tuple(int(x)-1 for x in k.split('/')[:2]) for k in t[1:]]
        for i in range(1,len(c)-1):faces.append((c[0],c[i],c[i+1]))
P=np.array(P);T=np.array(T)
P=np.stack([P[:,2],P[:,1],-P[:,0]],1)          # frente +Z -> +X
lo,hi=P.min(0),P.max(0);P-=[(lo[0]+hi[0])/2,lo[1],(lo[2]+hi[2])/2];P*=LARGO/(hi[0]-lo[0])
# normales suaves por vértice (ponderadas por área)
F=np.array([[k[0] for k in f] for f in faces]);N=np.zeros_like(P)
fn_=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]])
for j in range(3):np.add.at(N,F[:,j],fn_)
N/=np.linalg.norm(N,axis=1,keepdims=True)+1e-12
idx={};pos=[];uv=[];nr=[];ind=[]
for f in faces:
    for k in f:
        if k not in idx:idx[k]=len(pos);pos.append(P[k[0]]);uv.append(T[k[1]]);nr.append(N[k[0]])
        ind.append(idx[k])
pos=np.array(pos,np.float32);uv=np.array(uv,np.float32);uv[:,1]=1-uv[:,1];nr=np.array(nr,np.float32)
ind=np.array(ind,np.uint16 if len(pos)<65536 else np.uint32)
print('vertices',len(pos),'triangulos',len(ind)//3,'tamaño',pos.max(0)-pos.min(0))
def jpg(im,n,q=85):im=im.convert('RGB').resize((n,n),Image.LANCZOS);b=io.BytesIO();im.save(b,'JPEG',quality=q);return b.getvalue()
img_b=jpg(Image.open(fb),1024)
img_n=jpg(Image.open(fn),1024,90)
r=np.array(Image.open(fr).convert('L').resize((512,512),Image.LANCZOS));m=np.array(Image.open(fm).convert('L').resize((512,512),Image.LANCZOS))
img_mr=jpg(Image.fromarray(np.stack([np.zeros_like(r),r,m],2)),512,90)
blob=bytearray();views=[]
def add(data,target=None):
    while len(blob)%4:blob.append(0)
    off=len(blob);blob.extend(data);views.append(G.BufferView(buffer=0,byteOffset=off,byteLength=len(data),target=target));return len(views)-1
accs=[G.Accessor(bufferView=add(pos.tobytes(),G.ARRAY_BUFFER),componentType=G.FLOAT,count=len(pos),type='VEC3',min=pos.min(0).tolist(),max=pos.max(0).tolist()),
 G.Accessor(bufferView=add(nr.tobytes(),G.ARRAY_BUFFER),componentType=G.FLOAT,count=len(nr),type='VEC3'),
 G.Accessor(bufferView=add(uv.tobytes(),G.ARRAY_BUFFER),componentType=G.FLOAT,count=len(uv),type='VEC2'),
 G.Accessor(bufferView=add(ind.tobytes(),G.ELEMENT_ARRAY_BUFFER),componentType=G.UNSIGNED_SHORT if ind.dtype==np.uint16 else G.UNSIGNED_INT,count=len(ind),type='SCALAR')]
ims=[G.Image(bufferView=add(d),mimeType='image/jpeg') for d in (img_b,img_n,img_mr)]
g=G.GLTF2(scene=0,scenes=[G.Scene(nodes=[0])],nodes=[G.Node(name='coche500',mesh=0)],
  meshes=[G.Mesh(name='coche500',primitives=[G.Primitive(attributes=G.Attributes(POSITION=0,NORMAL=1,TEXCOORD_0=2),indices=3,material=0)])],
  accessors=accs,bufferViews=views,buffers=[G.Buffer(byteLength=0)],images=ims,
  textures=[G.Texture(source=i,sampler=0) for i in range(3)],samplers=[G.Sampler(magFilter=9729,minFilter=9987)],
  materials=[G.Material(name='coche500',normalTexture=G.NormalMaterialTexture(index=1),
   pbrMetallicRoughness=G.PbrMetallicRoughness(baseColorTexture=G.TextureInfo(index=0),metallicRoughnessTexture=G.TextureInfo(index=2),metallicFactor=1,roughnessFactor=1))])
while len(blob)%4:blob.append(0)
g.buffers[0].byteLength=len(blob);g.set_binary_blob(bytes(blob));g.save_binary(out)
print(out,os.path.getsize(out))
