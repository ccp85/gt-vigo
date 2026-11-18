import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= EDIFICIOS «HUNDIDOS» =================
# Los edificios del modelo bajan un poco por debajo de la acera (para que no queden huecos en las cuestas) y la textura
# contaba las plantas desde esa base: la planta baja (escaparates, portales) quedaba medio enterrada.
# Ahora, cuando el suelo de la zona ya está listo, se mide la acera junto a cada edificio y la textura se desplaza para que
# la planta baja empiece justo a la altura de la calle (atributo «fsh», en plantas, que el shader resta).

# 1) shader de fachada: resta el desplazamiento
r("function fachadaReal(m,k){m.userData.fv=1;","function fachadaReal(m,k){m.userData.fv=1;m.userData.real=1;")
r("""  sh.vertexShader='varying vec3 vWF;\\n'+sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\\n vWF=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='uniform float uLuz,uNf;uniform vec3 uZen,uHor;varying vec3 vWF;float gla;vec3 celF;""",
  """  sh.vertexShader='attribute float fsh;varying float vFs;varying vec3 vWF;\\n'+sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\\n vWF=(modelMatrix*vec4(transformed,1.)).xyz;vFs=fsh;');
  sh.fragmentShader='uniform float uLuz,uNf;uniform vec3 uZen,uHor;varying vec3 vWF;varying float vFs;float gla;vec3 celF;""")
r("vec2 uvF=vMapUv;float pl=(1.-uvF.y)*18.;","vec2 uvF=vMapUv;float pl=max((1.-uvF.y)*18.-vFs,0.);")   # por debajo de la planta baja: zócalo liso

# 2) medición y desplazamiento, por edificio, cuando el suelo (BVH) de las zonas está listo
r("const BVHQ=[];let bvhOn=false;",r"""const SUBE={cola:[],on:false,n:0};window.__SUBE=SUBE;
function subeZonas(){for(const z of ZROOTS){const rt=z.root;if(!rt.parent||rt.userData.sube)continue;rt.userData.sube=1;
  rt.traverse(o=>{if(o.isMesh&&!o.isInstancedMesh){const m=o.material;if(!Array.isArray(m)&&m&&m.userData.real)SUBE.cola.push(o)}})}
 if(SUBE.cola.length&&!SUBE.on){SUBE.on=true;setTimeout(subePaso,30)}}
function subePaso(){const tA=performance.now();while(SUBE.cola.length&&performance.now()-tA<12)subeUno();if(!SUBE.cola.length){SUBE.on=false;return}setTimeout(subePaso,30)}
function subeUno(){
 // primero el edificio más cercano a donde estás
 const fx=driving?P.x:ctl.target.x,fy=driving?P.y:ctl.target.z;let bi=0,bd=1e9;for(let i=0;i<SUBE.cola.length;i++){const o=SUBE.cola[i];if(!o.userData.bc){const g=o.geometry;if(!g.boundingBox)g.computeBoundingBox();o.updateMatrixWorld(true);o.userData.bc=g.boundingBox.getCenter(new THREE.Vector3()).applyMatrix4(o.matrixWorld)}const c=o.userData.bc,d=Math.hypot(c.x-fx,c.z-fy);if(d<bd){bd=d;bi=i}}
 const o=SUBE.cola.splice(bi,1)[0];{let rr=o;while(rr.parent)rr=rr.parent;if(rr!==scene)return}const t0=performance.now();try{subeMalla(o)}catch(e){console.warn('sube',e)}SUBE.ms=(SUBE.ms||0)+performance.now()-t0}
// suelo rápido: solo se lanzan rayos contra las piezas de suelo cuya caja contiene el punto, y basta el primer impacto
const _rcS=new THREE.Raycaster();_rcS.firstHitOnly=true;const _oS=new THREE.Vector3(),_dS=new THREE.Vector3(0,-1,0);
function sueloRap(x,z){let best=null;for(const o of GROUND){let b=o.userData.bbw;if(!b){if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();b=o.userData.bbw=o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld)}
  if(x<b.min.x||x>b.max.x||z<b.min.z||z>b.max.z)continue;_oS.set(x,b.max.y+1,z);_rcS.set(_oS,_dS);_rcS.far=b.max.y-b.min.y+2;const h=_rcS.intersectObject(o,false);if(h.length&&(best==null||h[0].point.y>best))best=h[0].point.y}
 return best}
function subeMalla(o){const g=o.geometry,pos=g.attributes.position,uv=g.attributes.uv,n=pos.count,ix=g.index;if(!uv||g.attributes.fsh||!n)return;
 const mp=o.material.map,ry=mp?mp.repeat.y:1,oy=mp?mp.offset.y:0,plOf=i=>(1-(uv.getY(i)*ry+oy))*18;
 o.updateMatrixWorld(true);const mw=o.matrixWorld,sc=new THREE.Vector3();o.getWorldScale(sc);
 // edificios = vértices unidos por triángulos o en la misma posición
 const par=new Int32Array(n);for(let i=0;i<n;i++)par[i]=i;const fd=i=>{while(par[i]!==i){par[i]=par[par[i]];i=par[i]}return i};
 if(ix)for(let t=0;t<ix.count;t+=3){const a=fd(ix.getX(t));par[fd(ix.getX(t+1))]=a;par[fd(ix.getX(t+2))]=a}
 {const key=new Map();for(let i=0;i<n;i++){const k=((Math.round(pos.getX(i)*2048)+50000)*100000+(Math.round(pos.getY(i)*2048)+50000))*100000+(Math.round(pos.getZ(i)*2048)+50000);const j=key.get(k);if(j!==undefined)par[fd(i)]=fd(j);else key.set(k,i)}}
 // altura de una planta (mundo) según cómo reparte el uv las 18 plantas
 const F=[];if(ix)for(let t=0;t<ix.count&&F.length<60;t+=3)for(const[a,b] of [[ix.getX(t),ix.getX(t+1)],[ix.getX(t+1),ix.getX(t+2)]]){const da=plOf(a)-plOf(b);if(Math.abs(da)>.5)F.push((pos.getY(a)-pos.getY(b))/da)}
 if(F.length<3)return;F.sort((a,b)=>a-b);const fhW=F[F.length>>1]*sc.y;if(!(fhW>1e-4))return;
 // base de cada edificio
 const C=new Map();for(let i=0;i<n;i++){const c=fd(i),y=pos.getY(i);let e=C.get(c);if(!e){e={y,v:[]};C.set(c,e)}if(y<e.y-1e-6){e.y=y;e.v=[i]}else if(y<e.y+1e-6&&e.v.length<24)e.v.push(i)}
 const V=new THREE.Vector3(),sh=new Map();
 const DIRS=[[.016,0],[-.016,0],[0,.016],[0,-.016],[.011,.011],[-.011,.011],[.011,-.011],[-.011,-.011]];
 for(const[c,e] of C){const fsL=[];for(const i of e.v){V.fromBufferAttribute(pos,i).applyMatrix4(mw);let gy=null;
   // solo los lados que dan a la calle: la acera o la calzada de delante marcan dónde empieza la planta baja
   for(const[dx,dz] of DIRS){const t=cell(V.x+dx,V.z+dz).t;if(t!==1&&t!==2&&t!==5)continue;const g_=sueloRap(V.x+dx,V.z+dz);if(g_!=null&&(gy==null||g_>gy))gy=g_}
   if(gy==null)continue;fsL.push(plOf(i)+(gy-V.y)/fhW)}
  if(!fsL.length)continue;fsL.sort((a,b)=>a-b);const fs=fsL[Math.floor((fsL.length-1)*.1)];if(fs>.06)sh.set(c,Math.min(1.6,fs))}   // el lado más bajo que da a la calle manda
 const A=new Float32Array(n);let k=0;if(sh.size)for(let i=0;i<n;i++){const v=sh.get(fd(i));if(v){A[i]=v;k++}}
 g.setAttribute('fsh',new THREE.BufferAttribute(A,1));SUBE.n+=sh.size}
const BVHQ=[];let bvhOn=false;""")
r("function pasoBVH(){const o=BVHQ.shift();if(!o){bvhOn=false;return}","function pasoBVH(){const o=BVHQ.shift();if(!o){bvhOn=false;subeZonas();return}")
# si una zona termina su suelo antes que todos los obstáculos, no esperar a la cola entera: revisar cada 3 s
r("const BVHQ=[];let bvhOn=false;","const BVHQ=[];let bvhOn=false;setInterval(()=>{if(!BVHQ.some(o=>o.userData.suelo))subeZonas()},3000);")

# 3) adornos de fachada del circuito (escaparates, rótulos, toldos, balcones): mismo ajuste, por tramo, al verse por primera vez
r("function fachadasInit(L){","function fachadasInit(L){FACH.L=L;")
r("const add=(k,m,pos,quat,sc,col)=>{const key=Math.floor(pos.x/4)+','+Math.floor(pos.z/4);let t=G.get(key);if(!t){t={x:0,y:0,n:0,L:{}};G.set(key,t)}t.x+=pos.x;t.y+=pos.z;t.n++;(t.L[k]=t.L[k]||[]).push([pos.clone(),quat.clone(),sc.clone(),col])};",
  "let SEG=-1;const add=(k,m,pos,quat,sc,col)=>{const key=Math.floor(pos.x/4)+','+Math.floor(pos.z/4);let t=G.get(key);if(!t){t={x:0,y:0,n:0,L:{}};G.set(key,t)}t.x+=pos.x;t.y+=pos.z;t.n++;(t.L[k]=t.L[k]||[]).push([pos.clone(),quat.clone(),sc.clone(),col,SEG])};")
r("for(const[ax,ay,bx,by,nx,ny,z0,h,pl,fc,sd] of L){","for(const[ax,ay,bx,by,nx,ny,z0,h,pl,fc,sd] of L){SEG++;")
r("A.forEach(([p,q,sc,col],i)=>{M4.compose(p,q,sc);im.setMatrixAt(i,M4);if(col)im.setColorAt(i,col)});im.castShadow=k!=='esc';im.receiveShadow=true;grp.add(im)}\n  grp.visible=false;scene.add(grp);FACH.trozos.push({g:grp,x:t.x/t.n,y:t.y/t.n})}",
  "A.forEach(([p,q,sc,col],i)=>{M4.compose(p,q,sc);im.setMatrixAt(i,M4);if(col)im.setColorAt(i,col)});im.castShadow=k!=='esc';im.receiveShadow=true;im.userData.A=A;grp.add(im)}\n  grp.visible=false;scene.add(grp);FACH.trozos.push({g:grp,x:t.x/t.n,y:t.y/t.n})}")
r("for(const t of FACH.trozos){const v=R_>0&&Math.abs(t.x-fx)<R_&&Math.abs(t.y-fy)<R_&&enZona(t.x,t.y,.5);t.g.visible=v}",
  "for(const t of FACH.trozos){const v=R_>0&&Math.abs(t.x-fx)<R_&&Math.abs(t.y-fy)<R_&&enZona(t.x,t.y,.5);t.g.visible=v;if(v&&!t.sub)fachSube(t)}")
r("function fachadasTick(){",r"""const FSEG=new Map();
function fachSegShift(i){if(FSEG.has(i))return FSEG.get(i);const[ax,ay,bx,by,nx,ny,z0]=FACH.L[i];let m=null;
 for(const[x,y] of [[ax,ay],[bx,by],[(ax+bx)/2,(ay+by)/2]]){const g=sueloOk2(x+nx*.004,y+ny*.004);if(g!=null)m=m==null?g:Math.min(m,g)}
 if(m==null)return null;const d=Math.max(0,Math.min(.12,m-z0));FSEG.set(i,d);return d}
function fachSube(t){if(!GROUND.length)return;let ok=true;const M4=new THREE.Matrix4(),p=new THREE.Vector3(),q=new THREE.Quaternion(),sc=new THREE.Vector3();
 for(const im of t.g.children){const A=im.userData.A;if(!A)continue;A.forEach(([pp,qq,ss,col,sg],i)=>{const d=fachSegShift(sg);if(d==null){ok=false;return}if(d<.002)return;p.copy(pp);p.y+=d;M4.compose(p,qq,ss);im.setMatrixAt(i,M4)});im.instanceMatrix.needsUpdate=true}
 t.sub=ok}
function fachadasTick(){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok suelo')
