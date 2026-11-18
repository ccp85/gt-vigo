import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= RAMPAS MECÁNICAS DE GRAN VÍA (Vigo Vertical) =================
# En el bulevar central de Gran Vía, desde el cruce con Venezuela unos 200 m hacia arriba: tramos de cinta mecánica
# que se mueven, barandillas de cristal, rellanos y un túnel de pórticos metálicos con los colores del arcoíris
# cubiertos por cristal transparente. Referencia: Google Earth y noticias de la obra (solo para ubicación y estilo).
r("function subeZonas(){for(const z of ZROOTS){const rt=z.root;","function subeZonas(){if(!RAMPA.celdas&&MAPA&&MI)rampaCeldas();for(const z of ZROOTS){const rt=z.root;if(rt.parent&&!rt.userData.rampaV){rt.userData.rampaV=1;setTimeout(()=>{try{rampaOculta(rt)}catch(e){console.warn('rampaO',e)}},180)}}if(!RAMPA.hecha&&sueloRap(93.95,29.52)!=null&&sueloRap(95.6,25.78)!=null&&sueloRap(96.72,23.29)!=null){RAMPA.hecha=1;setTimeout(()=>{try{rampaGV()}catch(e){console.warn('rampa',e);RAMPA.hecha=0}},500)}for(const z of ZROOTS){const rt=z.root;")
r("function subePaso(){",r"""const RAMPA={hecha:0};window.__RAMPA=RAMPA;
// quita las antiguas cubiertas verdes del bulevar (las del modelo) para poner las rampas nuevas
const RAMPA_P=[[93.95,29.52],[94.38,28.56],[95.04,27.1],[95.6,25.78],[96.72,23.29]],RAMPA_A=RAMPA_P[0],RAMPA_B=RAMPA_P[RAMPA_P.length-1];
// muestreo de la polilínea del bulevar: punto, tangente y longitud acumulada
const RAMPA_S=(()=>{const P=RAMPA_P,acc=[0];for(let i=1;i<P.length;i++)acc.push(acc[i-1]+Math.hypot(P[i][0]-P[i-1][0],P[i][1]-P[i-1][1]));
 const L=acc[acc.length-1],en=t=>{t=Math.max(-.2,Math.min(L+.2,t));let i=1;while(i<P.length-1&&acc[i]<t)i++;const a=P[i-1],b=P[i],l=acc[i]-acc[i-1],u=(t-acc[i-1])/l,ux=(b[0]-a[0])/l,uy=(b[1]-a[1])/l;return[a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u,ux,uy]};return{L,en}})();
function rampaOculta(rt){const RP=RAMPA_P,dSeg=(x,z)=>{let m=1e9;for(let i=1;i<RP.length;i++){const p=RP[i-1],q=RP[i],dx=q[0]-p[0],dz=q[1]-p[1],t=Math.max(-.06/Math.hypot(dx,dz),Math.min(1+.06/Math.hypot(dx,dz),((x-p[0])*dx+(z-p[1])*dz)/(dx*dx+dz*dz)));m=Math.min(m,Math.hypot(x-p[0]-t*dx,z-p[1]-t*dz))}return m},a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();let k=0;
 rt.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||GROUND.includes(o)||(RAMPA.G&&o.parent===RAMPA.G))return;const g=o.geometry,ix=g.index,pos=g.attributes.position;if(!ix||!pos)return;if(!g.boundingBox)g.computeBoundingBox();o.updateMatrixWorld(true);
  const bb=g.boundingBox.clone().applyMatrix4(o.matrixWorld);if(bb.max.x<93.7||bb.min.x>97||bb.max.z<23||bb.min.z>29.8)return;const mw=o.matrixWorld;let ch=0;
  for(let t=0;t<ix.count;t+=3){a.fromBufferAttribute(pos,ix.getX(t)).applyMatrix4(mw);b.fromBufferAttribute(pos,ix.getX(t+1)).applyMatrix4(mw);c.fromBufferAttribute(pos,ix.getX(t+2)).applyMatrix4(mw);
   const mx=(a.x+b.x+c.x)/3,mz=(a.z+b.z+c.z)/3,my=Math.max(a.y,b.y,c.y);
   if(dSeg(mx,mz)<.05&&my>groundY(mx,mz)+.008){const i0=ix.getX(t);ix.setX(t+1,i0);ix.setX(t+2,i0);ch++}}if(ch){ix.needsUpdate=true;k+=ch}});RAMPA.oc=(RAMPA.oc||0)+k}
// el bulevar de las rampas se puede atravesar: en el mapa de celdas pasa a ser zona peatonal (antes estaba bloqueado)
function rampaCeldas(){RAMPA.celdas=1;const RP=RAMPA_P,d=(x,z)=>{let m=1e9;for(let i=1;i<RP.length;i++){const p=RP[i-1],q=RP[i],dx=q[0]-p[0],dz=q[1]-p[1],t=Math.max(0,Math.min(1,((x-p[0])*dx+(z-p[1])*dz)/(dx*dx+dz*dz)));m=Math.min(m,Math.hypot(x-p[0]-t*dx,z-p[1]-t*dz))}return m};let n=0;
 for(let x=93.6;x<=97;x+=.5/MAPA.res)for(let y=23;y<=29.9;y+=.5/MAPA.res){if(d(x,y)>.06)continue;const i=Math.round((x-MAPA.ox)*MAPA.res),j=Math.round((y-MAPA.oy)*MAPA.res);if(i<0||j<0||i>=MAPA.w||j>=MAPA.h)continue;const o=(j*MAPA.w+i)*4,t=Math.round(MI[o]/40);if(t===3||t===6){MI[o]=200;n++}}RAMPA.nCeldas=n}
function rampaGV(){const L=RAMPA_S.L,EN=RAMPA_S.en,angT=t=>{const e=EN(t);return Math.atan2(-e[3],e[2])},G=new THREE.Group();G.name='rampasGranVia';
 const gy=t=>{const e=EN(t),v=sueloRap(e[0],e[1]);return v==null?groundY(e[0],e[1]):v},at=(t,o)=>{const e=EN(t);return[e[0]-e[3]*o,e[1]+e[2]*o]};
 // tramos de rampa con rellanos entre medias
 const TR=[];for(let t0=0;t0<L-.1;t0+=.7)TR.push([t0,Math.min(L,t0+.62)]);const W=.026;
 const cv=document.createElement('canvas');cv.width=32;cv.height=128;{const c=cv.getContext('2d');c.fillStyle='#3a3d44';c.fillRect(0,0,32,128);c.fillStyle='#55595f';for(let y=0;y<128;y+=8)c.fillRect(0,y,32,3);c.fillStyle='#d9b23a';c.fillRect(0,0,2,128);c.fillRect(30,0,2,128)}
 const tx=new THREE.CanvasTexture(cv);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.colorSpace=THREE.SRGBColorSpace;
 const BELT=new THREE.MeshStandardMaterial({map:tx,roughness:.6,metalness:.3}),ACE=new THREE.MeshStandardMaterial({color:0xc9ced6,roughness:.35,metalness:.7}),
  CRI=new THREE.MeshStandardMaterial({color:0xbfe8ff,roughness:.05,metalness:.1,transparent:true,opacity:.3,depthWrite:false}),PAV=new THREE.MeshStandardMaterial({color:0x8c8a86,roughness:.9});
 const tira=(t0,t1,o,w,h,y0,mat)=>{const n=Math.max(2,Math.ceil((t1-t0)/.05)),pos=[],idx=[],uv=[];for(let i=0;i<=n;i++){const t=t0+(t1-t0)*i/n,y=gy(t)+y0;for(const s_ of[-1,1]){const p=at(t,o+s_*w/2);pos.push(p[0],y+(h||0)*(s_>0?1:0)*0,p[1]);uv.push(s_>0?1:0,(t-t0)*14)}}
  for(let i=0;i<n;i++){const a=i*2;idx.push(a,a+1,a+2,a+1,a+3,a+2)}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();const m=new THREE.Mesh(g,mat);m.receiveShadow=true;G.add(m);return m};
 const pared=(t0,t1,o,h,y0,mat)=>{const n=Math.max(2,Math.ceil((t1-t0)/.05)),pos=[],idx=[];for(let i=0;i<=n;i++){const t=t0+(t1-t0)*i/n,p=at(t,o),y=gy(t)+y0;pos.push(p[0],y,p[1],p[0],y+h,p[1])}for(let i=0;i<n;i++){const a=i*2;idx.push(a,a+2,a+1,a+1,a+2,a+3)}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();const m=new THREE.Mesh(g,mat);G.add(m);return m};
 tira(-.05,L+.05,0,.085,0,.002,PAV);
 for(const[t0,t1]of TR){for(const o of[-.017,.017]){tira(t0,t1,o,W*.62,0,.006,BELT);for(const s_ of[-1,1]){pared(t0,t1,o+s_*W*.36,.013,.006,CRI);tira(t0,t1,o+s_*W*.36,.0025,0,.019,ACE)}}
  for(const t of[t0,t1]){const p=at(t,0),b=new THREE.Mesh(new THREE.BoxGeometry(.012,.012,.07),ACE);b.position.set(p[0],gy(t)+.008,p[1]);b.rotation.y=angT(t);G.add(b)}}
 // túnel de pórticos arcoíris cubiertos de cristal
 const NP=Math.round((L+.05)/.02),arc=new THREE.TorusGeometry(.04,.0028,6,18,Math.PI),pm=new THREE.MeshBasicMaterial({color:0xffffff}),
  im=new THREE.InstancedMesh(arc,pm,NP),du=new THREE.Object3D(),cc=new THREE.Color();
 for(let i=0;i<NP;i++){const t=-.02+i*.02,p=at(t,0);du.position.set(p[0],gy(t)+.006,p[1]);du.rotation.set(0,angT(t)+Math.PI/2,0);du.scale.set(1,1.15,1);du.updateMatrix();im.setMatrixAt(i,du.matrix);im.setColorAt(i,cc.setHSL(Math.min(TR.length-1,Math.max(0,Math.floor((t+.04)/.7)))/Math.max(1,TR.length-1)*.72,.85,.52))}
 im.castShadow=true;im.frustumCulled=false;G.add(im);
 {const n=Math.ceil(L/.05),pos=[],idx=[];const SEG=12;for(let i=0;i<=n;i++){const t=-.02+(L+.04)*i/n;for(let k=0;k<=SEG;k++){const a=Math.PI*k/SEG,o=Math.cos(a)*.039,h=Math.sin(a)*.046,p=at(t,o);pos.push(p[0],gy(t)+.006+h,p[1])}}
  for(let i=0;i<n;i++)for(let k=0;k<SEG;k++){const a=i*(SEG+1)+k,b=a+SEG+1;idx.push(a,b,a+1,a+1,b,b+1)}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();
  const tec=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:0xd8f0ff,roughness:.05,metalness:.2,transparent:true,opacity:.16,side:THREE.DoubleSide,depthWrite:false}));tec.renderOrder=2;G.add(tec)}
 // la cinta se mueve hacia arriba
 const mv=G.children.find(o=>o.material===BELT);if(mv)mv.onBeforeRender=()=>{tx.offset.y=(performance.now()/1000*.9)%1};
 scene.add(G);RAMPA.G=G}
function subePaso(){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok rampas')
