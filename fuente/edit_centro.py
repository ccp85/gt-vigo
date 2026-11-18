import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= CENTRO MÁS REALISTA (Policarpo Sanz, Porta do Sol, Príncipe, Colón…) =================
# Referencia visual: Google Earth (solo para fijarse en materiales y estilo; no se copia nada).
# · Colores de fachada propios de la zona: blanco roto, crema, arena y granito gris claro con juntas de sillería.
# · Relieve en las fachadas que dan a la calle: miradores blancos, balcones de hierro, escaparates con rótulo
#   y toldo, cornisa arriba y buhardillas sobre el tejado.
# Las calles no se tocan.

# zona (coordenadas del juego): de Porta do Sol a Policarpo Sanz / Colón
r("const SUBE={cola:[],on:false,n:0};",r"""const ZONAS_C=[[84.2,13.4,96.9,24.5],[93.5,17,103,24],[94.5,22.5,101,33],[93,8.8,106,15]];   // centro, Urzaiz, Gran Vía, Areal (x0,y0,x1,y1)
const enZonaC=(x,y)=>ZONAS_C.some(Z=>x>Z[0]&&x<Z[2]&&y>Z[1]&&y<Z[3]);
// paleta observada: [prob. acumulada, r,g,b, tipo] tipo 2 = enlucido, 3 = granito (sillería)
const ZPAL=[[.30,.93,.9,.84,2],[.52,.97,.96,.92,2],[.80,.82,.8,.76,3],[.90,.9,.83,.69,2],[.96,.87,.78,.72,2],[1.01,.74,.73,.71,3]];
const SUBE={cola:[],on:false,n:0};""")
# 1) shader de fachada: color por edificio y sillería de granito
r("sh.vertexShader='attribute float fsh;varying float vFs;varying vec3 vWF;\\n'","sh.vertexShader='attribute float fsh;attribute vec4 fcol;varying float vFs;varying vec4 vFc;varying vec3 vWF;\\n'")
r("vWF=(modelMatrix*vec4(transformed,1.)).xyz;vFs=fsh;","vWF=(modelMatrix*vec4(transformed,1.)).xyz;vFs=fsh;vFc=fcol;")
r("sh.fragmentShader='uniform float uLuz,uNf;uniform vec3 uZen,uHor;varying vec3 vWF;varying float vFs;float gla;vec3 celF;",
  "sh.fragmentShader='uniform float uLuz,uNf;uniform vec3 uZen,uHor;varying vec3 vWF;varying float vFs;varying vec4 vFc;float gla;vec3 celF;")
r("gla=1.-smoothstep(.82,.9,sampledDiffuseColor.a);diffuseColor.rgb*=sampledDiffuseColor.rgb;",
  r"""gla=1.-smoothstep(.82,.9,sampledDiffuseColor.a);
    if(vFc.a>1.5){vec3 base=vFc.rgb;
     if(vFc.a>2.5){float ry=vWF.y*115.;float row=floor(ry);float u=(vWF.x+vWF.z)*58.+fract(row*.5)*.5*2.;   // sillería: hiladas y juntas alternas
      float jh=smoothstep(.0,.07,fract(ry))*smoothstep(1.,.93,fract(ry)),jv=smoothstep(.0,.05,fract(u))*smoothstep(1.,.95,fract(u));
      float bl=hF(vec3(floor(u),row,7.));base*=(.9+.13*bl)*mix(.78,1.,jh*jv);}
     else base*=.97+.05*hF(floor(vWF*240.));
     diffuseColor.rgb=base*mix(vec3(1.),sampledDiffuseColor.rgb*1.12,.85);}
    else diffuseColor.rgb*=sampledDiffuseColor.rgb;""")
# 2) color por edificio dentro de la zona (en la misma pasada que sube la planta baja)
r("const A=new Float32Array(n);let k=0;if(sh.size)for(let i=0;i<n;i++){const v=sh.get(fd(i));if(v){A[i]=v;k++}}",
  r"""{const zc=new Map();for(const[c,e] of C){V.fromBufferAttribute(pos,e.v[0]).applyMatrix4(mw);if(!enZonaC(V.x,V.z))continue;
   const hh=Math.abs(Math.sin(V.x*127.1+V.z*311.7)*43758.5453)%1;zc.set(c,ZPAL.find(q=>hh<q[0]))}
  if(zc.size){const FC=new Float32Array(n*4);for(let i=0;i<n;i++){const p=zc.get(fd(i));if(p){FC[i*4]=p[1];FC[i*4+1]=p[2];FC[i*4+2]=p[3];FC[i*4+3]=p[4]}else FC[i*4+3]=0}g.setAttribute('fcol',new THREE.BufferAttribute(FC,4))}}
 const A=new Float32Array(n);let k=0;if(sh.size)for(let i=0;i<n;i++){const v=sh.get(fd(i));if(v){A[i]=v;k++}}""")
# 3) relieve en las fachadas de la zona: mismo sistema que los adornos del circuito, con reglas propias del centro
r("function fachadasInit(L){FACH.L=L;","function fachadasInit(L){const BASE=FACH.L?FACH.L.length:0;FACH.L=(FACH.L||[]).concat(L);{const M0=fachMats();if(!M0.tam){M0.tam=new THREE.MeshStandardMaterial({color:0xd9d3c6,roughness:.85});M0.cupp=new THREE.MeshStandardMaterial({color:0x8a93a0,roughness:.5,metalness:.15});M0.cupv=new THREE.MeshStandardMaterial({color:0x7fc2b0,roughness:.45,metalness:.1})}}")
r("const im=new THREE.InstancedMesh(BOX,M[k],A.length);","const im=new THREE.InstancedMesh(k==='tam'?FGEO.cil:(k==='cupv'||k==='cupp')?FGEO.cup:BOX,M[k],A.length);")
r("function fachadasInit(L){","const FGEO={cil:new THREE.CylinderGeometry(1,1,1,16),cup:new THREE.SphereGeometry(1,18,9,0,Math.PI*2,0,Math.PI/2)};\nfunction fachadasInit(L){")
r("let SEG=-1;const add=","let SEG=BASE-1;const add=")
r("for(const[ax,ay,bx,by,nx,ny,z0,h,pl,fc,sd] of L){SEG++;","for(const[ax,ay,bx,by,nx,ny,z0,h,pl,fc,sd,zona] of L){SEG++;")
r("const sa=(ax*ux+ay*uy)/BAY,sb=sa+Ln/BAY;const tienda=pl>=3,gal=sd%5===0,balc=sd%3!==0;const nf=Math.min(pl,Math.floor((h-.02)/FL));",
  r"""const sa=(ax*ux+ay*uy)/BAY,sb=sa+Ln/BAY;const tienda=pl>=3,gal=sd%5===0,balc=sd%3!==0;const nf=Math.min(pl,Math.floor((h-.02)/FL));
  if(zona===2){const mid=(ax+bx)/2,midy=(ay+by)/2,cx=mid-nx*.04,cy=midy-ny*.04,top=z0+h,ver=sd%3===0;
   add('tam',M.tam,V.set(cx,top+.022,cy),Q,S.set(.042,.044,.042),null);add('los',M.los,V.set(cx,top+.045,cy),Q,S.set(.09,.005,.09),null);
   add(ver?'cupv':'cupp',ver?M.cupv:M.cupp,V.set(cx,top+.047,cy),Q,S.set(.044,.052,.044),null);add('tam',M.tam,V.set(cx,top+.108,cy),Q,S.set(.006,.024,.006),null)}
  if(zona){// centro: miradores en el eje de la fachada, balcones de hierro, balcón corrido en la 1ª planta, cornisa y buhardillas
   const galW=sd%3!==1,corr=sd%4===0,buh=sd%2===0;const mid=(ax+bx)/2,midy=(ay+by)/2;
   add('los',M.los,V.set(mid+nx*.006,z0+Math.max(.06,h-.004),midy+ny*.006),Q,S.set(Ln,.007,.013),null);
   if(nf>=3&&corr)add('bar',M.bar,V.set(mid+nx*.0135,z0+.02+FL+.011,midy+ny*.0135),Q,S.set(Ln*.96,.014,.001),null),add('los',M.los,V.set(mid+nx*.007,z0+.02+FL+.003,midy+ny*.007),Q,S.set(Ln*.96,.003,.014),null);
   for(let n=Math.ceil(sa-.5);n<=Math.floor(sb-.5);n++){const tt=((n+.5)-sa)*BAY/Ln;if(tt<.05||tt>.95)continue;const b=n;const px=ax+dx*tt,py=ay+dy*tt;
    const P=(off,y)=>V.set(px+nx*off,z0+y,py+ny*off);const enEje=Math.abs(tt-.5)<Math.max(.13,.6*BAY/Ln);
    if(nf>=2){add('esc',M.esc,P(.0025,.034),Q,S.set(BAY*.88,.058,.004),null);add('rot',M.rot,P(.004,.073),Q,S.set(BAY*1.0,.014,.006),c.set(ROT[((sd+b)%ROT.length+ROT.length)%ROT.length]).clone());
     if(((b+sd)%3+3)%3===0){Qp.setFromAxisAngle(AX,sg*.42);const qq=Q.clone().multiply(Qp);add('tol',M.tol,P(.013,.086),qq,S.set(BAY*.9,.002,.026),c.set(TOL[(((sd+(b>>1))%TOL.length)+TOL.length)%TOL.length]).clone())}}
    for(let f=1;f<nf;f++){const y=.02+f*FL;if(f===1&&corr)continue;
     if(galW&&enEje&&f<nf){add('gal',M.gal,P(.008,y+FL*.5),Q,S.set(BAY*.95,FL*.94,.016),null);continue}
     if(((b*7+f*3+sd)%5+5)%5<3){add('los',M.los,P(.007,y+.003),Q,S.set(BAY*.8,.003,.014),null);add('bar',M.bar,P(.0135,y+.011),Q,S.set(BAY*.8,.014,.001),null)}}
    if(buh&&((b+sd)%2+2)%2===0&&nf>=3)add('gal',M.gal,P(-.006,h+.013),Q,S.set(BAY*.5,.021,.014),null)}
   continue}""")
# 4) extraer las fachadas que dan a la calle en la zona, cuando el centro y su suelo están listos
r("function subeZonas(){for(const z of ZROOTS){const rt=z.root;if(!rt.parent||rt.userData.sube)continue;rt.userData.sube=1;",
  "function subeZonas(){for(const z of ZROOTS){const rt=z.root;if(rt.parent&&rt.name==='centro'&&!rt.userData.fachC){rt.userData.fachC=1;setTimeout(()=>{try{centroFachadas(rt)}catch(e){console.warn('centroFachadas',e)}},200)}if(!rt.parent||rt.userData.sube)continue;rt.userData.sube=1;")
r("function subePaso(){",r"""function centroFachadas(rt){const L=[],a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3(),n=new THREE.Vector3(),e1=new THREE.Vector3(),e2=new THREE.Vector3();
 const calle=t=>t===1||t===2||t===4||t===5,rc=new THREE.Raycaster();rc.firstHitOnly=true;const dn=new THREE.Vector3(0,-1,0),o_=new THREE.Vector3(),vis=new Set();
 rt.traverse(o=>{if(!o.isMesh||o.isInstancedMesh)return;const m=o.material;if(Array.isArray(m)||!m||!m.userData.real)return;const g=o.geometry,pos=g.attributes.position,ix=g.index;if(!ix)return;o.updateMatrixWorld(true);const mw=o.matrixWorld;
  for(let t=0;t<ix.count;t+=3){a.fromBufferAttribute(pos,ix.getX(t)).applyMatrix4(mw);if(!enZonaC(a.x,a.z))continue;b.fromBufferAttribute(pos,ix.getX(t+1)).applyMatrix4(mw);c.fromBufferAttribute(pos,ix.getX(t+2)).applyMatrix4(mw);
   e1.subVectors(b,a);e2.subVectors(c,a);n.crossVectors(e1,e2);const nl=n.length();if(nl<1e-10)continue;n.divideScalar(nl);if(Math.abs(n.y)>.12)continue;
   const W=[a,b,c].sort((p,q)=>p.y-q.y);if(W[1].y-W[0].y>.002||W[2].y-W[1].y<.03)continue;
   const ax=W[0].x,ay=W[0].z,bx=W[1].x,by=W[1].z,Ln=Math.hypot(bx-ax,by-ay);if(Ln<.03)continue;const key=Math.round((ax+bx)*200)+','+Math.round((ay+by)*200);if(vis.has(key))continue;vis.add(key);
   let nx=n.x,ny=n.z;const l2=Math.hypot(nx,ny);nx/=l2;ny/=l2;const mx=(ax+bx)/2,my=(ay+by)/2;
   if(!calle(cell(mx+nx*.025,my+ny*.025).t)){if(calle(cell(mx-nx*.025,my-ny*.025).t)){nx=-nx;ny=-ny}else continue}
   const g1=sueloRap(ax+nx*.02,ay+ny*.02),g2=sueloRap(bx+nx*.02,by+ny*.02),gz=Math.min(g1??W[0].y,g2??W[0].y);
   // altura real de la fachada: rayo desde arriba sobre el propio edificio, justo detrás de la pared
   let top=W[2].y;o_.set(mx-nx*.008,top+3,my-ny*.008);rc.set(o_,dn);rc.far=6;const hh=rc.intersectObject(o,false);if(hh.length)top=Math.max(top,hh[0].point.y);
   const h=top-gz;if(h<.1)continue;const sd=Math.abs(Math.round(Math.sin(mx*91.7+my*47.3)*1e4));
   L.push([ax,ay,bx,by,nx,ny,gz,h,Math.floor(h/.075),'',sd,Ln<.075&&h>.3&&sd%5<3?2:1])}});
 window.__CENTRO_FACH=L.length;if(L.length)fachadasInit(L)}
function subePaso(){""")
# escaparates algo más claros de día (vidrio que refleja la calle)
r("gr.addColorStop(0,'#5a6b80');gr.addColorStop(1,'#1d2430');","gr.addColorStop(0,'#9db0c2');gr.addColorStop(.55,'#6d8196');gr.addColorStop(1,'#3a4656');")
# tejados de pizarra/zinc (mansardas) en la zona: atributo por edificio en las mallas de tejado
r("function tejadoReal(m){if(m.userData.tj||m.map)return;m.userData.tj=1;","function tejadoReal(m){if(m.userData.tj||m.map)return;m.userData.tj=1;m.userData.tej=1;")
r("sh.vertexShader='varying vec3 vWT;\\n'+sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\\n vWT=(modelMatrix*vec4(transformed,1.)).xyz;');",
  "sh.vertexShader='attribute float rtip;varying float vRt;varying vec3 vWT;\\n'+sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\\n vWT=(modelMatrix*vec4(transformed,1.)).xyz;vRt=rtip;');")
r("sh.fragmentShader='varying vec3 vWT;\\nfloat hT(","sh.fragmentShader='varying vec3 vWT;varying float vRt;\\nfloat hT(")
r("diffuseColor.rgb*=mix(1.,mix(grava*junta,teja,roj),fine*.9+.1);}}`)};",
  "if(vRt>.5&&roj>.3){float sb=fract(b*60.);diffuseColor.rgb=vec3(.31,.34,.39)*(.86+.18*hT(vec3(floor(b*60.),floor(a*9.),1.)))*(1.-.3*smoothstep(.86,.95,sb))*(1.+.12*smoothstep(.0,.6,fila));}\\n     else diffuseColor.rgb*=mix(1.,mix(grava*junta,teja,roj),fine*.9+.1);}}`)};")
r("function subeZonas(){for(const z of ZROOTS){const rt=z.root;","function subeZonas(){for(const z of ZROOTS){const rt=z.root;if(rt.parent&&!rt.userData.tejZ){rt.userData.tejZ=1;rt.traverse(o=>{if(o.isMesh&&!o.isInstancedMesh&&o.material&&!Array.isArray(o.material)&&o.material.userData.tej)tejadoZona(o)})}")
r("function subePaso(){",r"""function tejadoZona(o){const g=o.geometry,pos=g.attributes.position,n=pos.count,ix=g.index;if(g.attributes.rtip||!n)return;o.updateMatrixWorld(true);const mw=o.matrixWorld,V=new THREE.Vector3();
 V.copy(g.boundingSphere?g.boundingSphere.center:(g.computeBoundingSphere(),g.boundingSphere.center)).applyMatrix4(mw);
 // solo mallas que tocan la zona (para no recorrer toda la ciudad)
 const R=g.boundingSphere.radius*o.matrixWorld.getMaxScaleOnAxis();if(!ZONAS_C.some(Z=>V.x+R>Z[0]&&V.x-R<Z[2]&&V.z+R>Z[1]&&V.z-R<Z[3]))return;
 const par=new Int32Array(n);for(let i=0;i<n;i++)par[i]=i;const fd=i=>{while(par[i]!==i){par[i]=par[par[i]];i=par[i]}return i};
 if(ix)for(let t=0;t<ix.count;t+=3){const a=fd(ix.getX(t));par[fd(ix.getX(t+1))]=a;par[fd(ix.getX(t+2))]=a}
 const C=new Map();for(let i=0;i<n;i++){const c=fd(i);if(!C.has(c))C.set(c,i)}const tip=new Map();
 for(const[c,i] of C){V.fromBufferAttribute(pos,i).applyMatrix4(mw);if(!enZonaC(V.x,V.z))continue;const hh=Math.abs(Math.sin(V.x*71.3+V.z*193.1)*24634.6345)%1;if(hh<.5)tip.set(c,1)}
 const A=new Float32Array(n);if(tip.size)for(let i=0;i<n;i++)if(tip.get(fd(i)))A[i]=1;g.setAttribute('rtip',new THREE.BufferAttribute(A,1))}
function subePaso(){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok centro')
