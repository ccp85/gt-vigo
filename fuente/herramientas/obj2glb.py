import sys,io,numpy as np
from PIL import Image
import pygltflib as G
obj,tex,out=sys.argv[1:4]
P=[];T=[];N=[];faces=[]
for l in open(obj):
    t=l.split()
    if not t:continue
    if t[0]=='v':P.append(list(map(float,t[1:4])))
    elif t[0]=='vt':T.append(list(map(float,t[1:3])))
    elif t[0]=='vn':N.append(list(map(float,t[1:4])))
    elif t[0]=='f':
        c=[tuple(int(x)-1 for x in k.split('/')) for k in t[1:]]
        for i in range(1,len(c)-1):faces.append((c[0],c[i],c[i+1]))
P,T,N=map(np.array,(P,T,N))
# girar para que mire a +X (frente original +Z): (x,y,z)->(z,y,-x)
rot=lambda a:np.stack([a[:,2],a[:,1],-a[:,0]],1)
P=rot(P);N=rot(N)
def parte(tri):
    Q=P[[k[0] for k in tri]];c=Q.mean(0);x,y,z=c  # z = -x original (lateral)
    if Q[:,1].max()<.40 and abs(z)>.005:return 'piernaA' if z<0 else 'piernaB'
    if abs(z)>.155 and .34<y<.72:return 'brazoA' if z<0 else 'brazoB'
    return 'cuerpo'
grupos={}
for f in faces:grupos.setdefault(parte(f),[]).append(f)
for k,v in grupos.items():print(k,len(v))
# textura a 1024
im=Image.open(tex).convert('RGB').resize((1024,1024),Image.LANCZOS);b=io.BytesIO();im.save(b,'JPEG',quality=85);img=b.getvalue()
blob=bytearray();views=[];accs=[];meshes=[];nodes=[]
def add(data,target=None):
    while len(blob)%4:blob.append(0)
    off=len(blob);blob.extend(data);views.append(G.BufferView(buffer=0,byteOffset=off,byteLength=len(data),target=target));return len(views)-1
for nom in ['cuerpo','piernaA','piernaB','brazoA','brazoB']:
    fs=grupos[nom];idx={};pos=[];uv=[];nr=[];ind=[]
    for f in fs:
        for k in f:
            if k not in idx:idx[k]=len(pos);pos.append(P[k[0]]);uv.append(T[k[1]]);nr.append(N[k[2]])
            ind.append(idx[k])
    pos=np.array(pos,np.float32);uv=np.array(uv,np.float32);uv[:,1]=1-uv[:,1];nr=np.array(nr,np.float32);nr/=np.linalg.norm(nr,axis=1,keepdims=True)+1e-9
    ind=np.array(ind,np.uint16)
    a0=len(accs);accs.append(G.Accessor(bufferView=add(pos.tobytes(),G.ARRAY_BUFFER),componentType=G.FLOAT,count=len(pos),type='VEC3',min=pos.min(0).tolist(),max=pos.max(0).tolist()))
    accs.append(G.Accessor(bufferView=add(nr.tobytes(),G.ARRAY_BUFFER),componentType=G.FLOAT,count=len(nr),type='VEC3'))
    accs.append(G.Accessor(bufferView=add(uv.tobytes(),G.ARRAY_BUFFER),componentType=G.FLOAT,count=len(uv),type='VEC2'))
    accs.append(G.Accessor(bufferView=add(ind.tobytes(),G.ELEMENT_ARRAY_BUFFER),componentType=G.UNSIGNED_SHORT,count=len(ind),type='SCALAR'))
    meshes.append(G.Mesh(name=nom,primitives=[G.Primitive(attributes=G.Attributes(POSITION=a0,NORMAL=a0+1,TEXCOORD_0=a0+2),indices=a0+3,material=0)]))
    nodes.append(G.Node(name=nom,mesh=len(meshes)-1))
iv=add(img)
g=G.GLTF2(scene=0,scenes=[G.Scene(nodes=list(range(len(nodes))))],nodes=nodes,meshes=meshes,accessors=accs,bufferViews=views,
  buffers=[G.Buffer(byteLength=0)],images=[G.Image(bufferView=iv,mimeType='image/jpeg')],textures=[G.Texture(source=0,sampler=0)],samplers=[G.Sampler(magFilter=9729,minFilter=9987)],
  materials=[G.Material(name='protagonista',pbrMetallicRoughness=G.PbrMetallicRoughness(baseColorTexture=G.TextureInfo(index=0),metallicFactor=0,roughnessFactor=.7))])
while len(blob)%4:blob.append(0)
g.buffers[0].byteLength=len(blob);g.set_binary_blob(bytes(blob));g.save_binary(out)
import os;print(out,os.path.getsize(out))
