f='index.html';s=open(f).read()
# ================= RAMPAS DE GRAN VÍA: PÉRGOLAS POLIGONALES DE COLORES CON VEGETACIÓN =================
# Antes: arcos semicirculares en arcoíris continuo. Ahora, como las rampas reales (fotos del autor como referencia):
#  - pórticos de perfil quebrado (paredes rectas y tejado a dos aguas con la cumbrera desplazada) en vez de arcos
#  - cada tramo de rampa es un bloque de un solo color (rosa, rojo, naranja, amarillo, lima, verde, turquesa, azul...)
#  - los pórticos de cada bloque van inclinados hacia un lado, alternando, para dar el zigzag
#  - cubierta de cristal facetada siguiendo el perfil de cada bloque
#  - jardineras a los lados: césped, flores rojas, cipreses recortados en cono y arbustos
a0=s.find(" // túnel de pórticos arcoíris cubiertos de cristal")
a1=s.find(" // la cinta se mueve hacia arriba")
assert a0>0 and a1>a0 and s.count(" // túnel de pórticos arcoíris cubiertos de cristal")==1
NEW=r""" // pérgolas poligonales: un bloque de color por tramo, pórticos inclinados en zigzag y cristal facetado
 const PALR=[0xd8327f,0xe23b3b,0xef7a1f,0xf4c21a,0xa6cf2a,0x45b649,0x1fa98f,0x1d9fc4,0x2f6fd6,0x5a4fcf],NB=TR.length;
 const colB=b=>PALR[Math.round(b*(PALR.length-1)/Math.max(1,NB-1))];
 const blq=t=>Math.min(NB-1,Math.max(0,Math.floor((t+.04)/.7)));
 // perfil de cada bloque: [desplazamiento lateral, altura]; la cumbrera se mueve a un lado u otro
 const HW=.036,perf=b=>{const ax=(b%2?1:-1)*(.008+(b%3)*.004),hp=.03+(b%3)*.003,hc=.058+((b*7)%3)*.004;return[[-HW,0],[-HW,hp],[ax,hc],[HW,hp+((b%2)?.006:-.004)],[HW,0]]};
 const barra=(a,b_,e)=>{const dx=b_[0]-a[0],dy=b_[1]-a[1],l=Math.hypot(dx,dy),g=new THREE.BoxGeometry(l+e,e,e);g.rotateZ(Math.atan2(dy,dx));g.translate((a[0]+b_[0])/2,(a[1]+b_[1])/2,0);return g};
 const du=new THREE.Object3D();du.rotation.order='YXZ';
 for(let b=0;b<NB;b++){const pr=perf(b).map(([o,h])=>[-o,h]),parts=[];for(let k=0;k<pr.length-1;k++)parts.push(barra(pr[k],pr[k+1],.0034));
  const fg=mergeGeometries(parts),t0=TR[b][0]-.04,t1=b<NB-1?TR[b+1][0]-.04:L+.03,n=Math.max(2,Math.round((t1-t0)/.027)),lean=(b%2?1:-1)*.28;
  const im=new THREE.InstancedMesh(fg,new THREE.MeshStandardMaterial({color:colB(b),roughness:.45,metalness:.25}),n);
  for(let i=0;i<n;i++){const t=t0+(i+.5)*(t1-t0)/n,p=at(t,0);du.position.set(p[0],gy(t)+.006,p[1]);du.rotation.set(lean,angT(t)+Math.PI/2,0);du.updateMatrix();im.setMatrixAt(i,du.matrix)}
  im.castShadow=!window.LITE;im.receiveShadow=true;im.computeBoundingSphere();G.add(im);
  // cubierta de cristal facetada del bloque
  const P5=perf(b),m_=Math.max(2,Math.ceil((t1-t0)/.05)),pos=[],idx=[];
  for(let i=0;i<=m_;i++){const t=t0+(t1-t0)*i/m_,y0=gy(t)+.006;for(const[o,h]of P5){const p=at(t,o);pos.push(p[0],y0+h,p[1])}}
  const K=P5.length;for(let i=0;i<m_;i++)for(let k=0;k<K-1;k++){const a=i*K+k,c=a+K;idx.push(a,c,a+1,a+1,c,c+1)}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();
  const tec=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:0xe6f6ff,roughness:.05,metalness:.2,transparent:true,opacity:.2,side:THREE.DoubleSide,depthWrite:false}));tec.renderOrder=2;G.add(tec)}
 // jardineras a ambos lados: césped, flores, cipreses en cono y arbustos
 {const CES=new THREE.MeshStandardMaterial({color:0x5f9a3e,roughness:1,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}),
   BOR=new THREE.MeshStandardMaterial({color:0xb9b4aa,roughness:.9});
  for(const sd of[-1,1]){tira(-.03,L+.03,sd*.049,.016,0,.0045,CES);pared(-.03,L+.03,sd*.058,.004,.002,BOR);pared(-.03,L+.03,sd*.04,.004,.002,BOR)}
  const cip=[],arb=[],flo=[];let rs=13;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
  for(let t=0;t<L;t+=.03){for(const sd of[-1,1]){const r=rn();const p=at(t+rn()*.02,sd*(.049+(rn()-.5)*.008));
   if(r<.05)cip.push([p[0],p[1],gy(t),.8+rn()*.5]);else if(r<.5)arb.push([p[0],p[1],gy(t),.7+rn()*.6]);
   for(let k=0;k<3;k++){const q=at(t+rn()*.03,sd*(.049+(rn()-.5)*.013));flo.push([q[0],q[1],gy(t)])}}}
  const mm=new THREE.Matrix4(),q=new THREE.Quaternion(),V=new THREE.Vector3(),S=new THREE.Vector3(),cc=new THREE.Color();
  const inst=(geo,mat,L_,f_)=>{if(!L_.length)return;const im=new THREE.InstancedMesh(geo,mat,L_.length);L_.forEach((e,i)=>f_(im,e,i));im.castShadow=!window.LITE;im.receiveShadow=true;im.computeBoundingSphere();G.add(im)};
  const cono=new THREE.ConeGeometry(.0065,.022,7).translate(0,.011,0),bola=new THREE.IcosahedronGeometry(.0065,0),flor=new THREE.BoxGeometry(.004,.003,.004);
  inst(cono,new THREE.MeshStandardMaterial({color:0x2f6b35,roughness:.9,flatShading:true}),cip,(im,[x,y,z,k],i)=>{mm.compose(V.set(x,z+.005,y),q,S.set(k,k,k));im.setMatrixAt(i,mm)});
  inst(bola,new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9,flatShading:true}),arb,(im,[x,y,z,k],i)=>{mm.compose(V.set(x,z+.009,y),q,S.set(k,k*.8,k));im.setMatrixAt(i,mm);im.setColorAt(i,cc.setHex([0x4f8f3a,0x3f7d34,0x6a9a3a,0x86a83a][i%4]))});
  inst(flor,new THREE.MeshStandardMaterial({color:0xffffff,roughness:.8}),flo,(im,[x,y,z],i)=>{mm.compose(V.set(x,z+.007,y),q,S.set(1,1,1));im.setMatrixAt(i,mm);im.setColorAt(i,cc.setHex(i%5?0xc8262e:0xf2c14e))})}
"""
s=s[:a0]+NEW+s[a1:]
open(f,'w').write(s)
print('ok rampas2')
