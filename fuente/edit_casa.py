import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MISIÓN DE INFILTRACIÓN: EL REGALO BAJO EL ÁRBOL SIN QUE TE VEAN =================
# Conduces hasta una casa de las afueras, entras a escondidas y, en una vista de casa de muñecas (sin techo, desde
# arriba), dejas el regalo bajo el árbol y sales por la puerta. Los de la casa tienen un cono de visión: papá recorre
# el recibidor, mamá va y viene por la cocina y el niño, en el sofá, mira la tele y de vez en cuando mira alrededor.
# Los muebles y paredes tapan la vista. Si te ven, vuelves a empezar desde fuera.
r("function campMision(k){return campMisionB(k)}",
  """const esCasaK=k=>k===2||(k>12&&(k-13)%6===0);
function campMision(k){if(esCasaK(k))return{v:'coche',casa:true,txt:'🏠 Misión sigilo · el regalo bajo el árbol'};let c=0;for(let i=0;i<k;i++)if(esCasaK(i))c++;return campMisionB(k-c)}""")
r("if(MODO==='nado'){updateNado(dt);return}","if(MODO==='nado'){updateNado(dt);return}if(MODO==='casa'){updateCasa(dt);return}")
r("function buscarObjetivo(){objetivo=null;","function buscarObjetivo(){objetivo=null;if(CASM.on){const t_=casaObjetivo();if(t_!==undefined)return t_}")
r("function accion(){if(!driving)return;","function accion(){if(!driving)return;if(CASM.on&&casaAccion())return;")
r("if(m.buceo&&BUC.on){buceoTick(dt||.016);return}","if(m.buceo&&BUC.on){buceoTick(dt||.016);return}if(m.casa&&CASM.on){casaTick(dt||.016);return}")
r(" REP.mis=m;if(m.rad>REP.rad)REP.rad=m.rad;if(MODO!=='coche'){repCocheCalle();"," if(m.casa&&casaInicio(m,k))return;REP.mis=m;if(m.rad>REP.rad)REP.rad=m.rad;if(MODO!=='coche'){repCocheCalle();")
r("MODO!=='nado')navEstela(","MODO!=='nado'&&MODO!=='casa')navEstela(")
r("function repCocheCalle(){",r"""const CASM={on:false};window.__CASM=CASM;
// plano de la casa (unidades locales: x hacia el este, z hacia el sur; la puerta está abajo)
const CASA_W=1.8,CASA_D=1.2,CASA_H=.15;
const CASA_MUROS=[[0,0,1.8,.03],[0,0,.03,1.2],[1.77,0,.03,1.2],[0,1.17,.26,.03],[.42,1.17,1.38,.03],
 [.7,0,.03,.25],[.7,.38,.03,.42],[.7,.93,.03,.27],[0,.55,.3,.03],[.45,.55,.25,.03],[.73,.6,.37,.03],[1.26,.6,.54,.03]];
// muebles: [x,z,ancho,fondo,alto,color,tapaVista]
const CASA_MUEB=[[.05,.62,.1,.07,.09,0x7a4a2a,1],[.06,.06,.24,.3,.05,0xd8d2e8,0],[.52,.04,.14,.06,.13,0x6b4426,1],[.06,.38,.08,.08,.06,0x8a5a32,0],
 [.75,1.08,1.0,.08,.07,0xe8e4dc,0],[1.1,.78,.28,.13,.06,0xd8d0c0,0],[1.55,.66,.2,.05,.13,0xe8e4dc,1],
 [.92,.36,.32,.11,.06,0x3f6a8a,0],[1.33,.3,.14,.14,.04,0x8a5a32,0],[.92,.05,.3,.04,.1,0x22252a,1]];
const CASA_ARBOL=[1.6,.14],CASA_PUERTA=[.34,1.18];
function casaSitio(){const R_=REP.rad||REP_R0,dep=d=>Math.hypot(d[1]-REP_DEP[1],d[2]-REP_DEP[2]);let L=repPool().filter(d=>dep(d)>5&&dep(d)<R_-.5&&!AV_TODO.test(d[0]));if(!L.length)L=repPool().filter(d=>dep(d)>4&&dep(d)<R_-.3);if(!L.length)return null;
 L.sort((a,b)=>Math.hypot(a[1]-P.x,a[2]-P.y)-Math.hypot(b[1]-P.x,b[2]-P.y));const q=L.slice(Math.floor(L.length*.3),Math.floor(L.length*.7));return(q.length?q:L)[Math.floor(Math.random()*(q.length||L.length))]}
function casaInicio(m,k){const d=casaSitio();if(!d)return false;REP.mis=m;if(MODO!=='coche')repCocheCalle();Object.assign(CASM,{on:true,fase:'ir',d,t:0,av:0});REP.fase='casa';
 campDestino(['🏠 Casa en '+d[0],d[1],d[2]]);aviso('🏠 Misión '+(k+1)+' · ¡Sigilo navideño!',2.2,'cuenta');
 setTimeout(()=>{if(REP.on&&!REP.fin&&CASM.fase==='ir')mostrar('Ve a la casa de las afueras: hay que dejar un regalo bajo el árbol sin que te vean')},2400);return true}
function casaObjetivo(){const C=CASM;if(C.fase==='puerta'&&MODO==='coche'){objetivo={k:'casa'};return '🏠 Entrar a escondidas'}if(MODO==='casa'){if(!C.regalo&&Math.hypot(C.px-CASA_ARBOL[0],C.pz-CASA_ARBOL[1])<.17){objetivo={k:'casa'};return '🎁 Dejar el regalo'}objetivo=null;return null}}
function casaAccion(){const C=CASM;if(C.fase==='puerta'&&MODO==='coche'){casaEntra();return true}
 if(MODO==='casa'){if(!C.regalo&&Math.hypot(C.px-CASA_ARBOL[0],C.pz-CASA_ARBOL[1])<.17){C.dejando=0.001;return true}mostrar(C.regalo?'Sal por la puerta sin que te vean':'Llega hasta el árbol del salón sin que te vean');return true}return false}
function casaTick(dt){const C=CASM;C.t+=dt;if(C.fase==='ir'||C.fase==='puerta'){if(MODO!=='coche')return;const dd=Math.hypot(C.d[1]-P.x,C.d[2]-P.y);if(C.fase==='ir'&&dd<.3){C.fase='puerta';C.av=0}else if(C.fase==='puerta'&&dd>.55)C.fase='ir';
  if(C.fase==='puerta'){C.av-=dt;if(C.av<=0){C.av=3;mostrar(document.body.classList.contains('pad')?'Ⓐ para entrar a escondidas':'E (o el botón de acción) para entrar a escondidas')}}}}
// ---------- la casa por dentro
function casaConstruye(){const C=CASM,G=new THREE.Group();G.name='casaDentro';const M=(c,r_=.8,e=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r_,emissive:e?c:0,emissiveIntensity:e});
 const ox=C.ox,oz=C.oz,b=C.base,box=(x,z,w,d,h,mat,y0=0)=>{const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);m.position.set(ox+x+w/2,b+y0+h/2,oz+z+d/2);m.castShadow=m.receiveShadow=true;G.add(m);return m};
 // jardín nevado alrededor, suelos de madera y baldosa
 const jar=new THREE.Mesh(new THREE.PlaneGeometry(8,8),M(0xdfe6ef,1));jar.rotation.x=-Math.PI/2;jar.position.set(ox+CASA_W/2,b-.003,oz+CASA_D/2);jar.receiveShadow=true;G.add(jar);
 box(0,0,.7,.55,.004,M(0x9a6a44,.7));box(0,.55,.7,.65,.004,M(0xb7845a,.7));box(.7,0,1.1,.6,.004,M(0xa8744a,.7));box(.7,.6,1.1,.6,.004,M(0xd9d6cc,.5));
 const alf=box(1.0,.12,.5,.36,.002,M(0x8a1f2a,.9),.004);
 const MUR=M(0xf0e6d6,.85),ZOC=M(0x6b4426,.7);for(const w of CASA_MUROS){box(w[0],w[1],w[2],w[3],CASA_H,MUR);box(w[0]-.001,w[1]-.001,w[2]+.002,w[3]+.002,.012,ZOC)}
 box(.26,1.17,.16,.03,.004,M(0x5a3a1e,.6));for(const m of CASA_MUEB)box(m[0],m[1],m[2],m[3],m[4],M(m[5],.6));
 // detalles: tele encendida, lámparas, chimenea con fuego, almohadas, fogones
 box(.95,.06,.24,.015,.06,M(0x66b8ff,.3,1.2),.04);box(.07,.06,.22,.05,.012,M(0xffffff,.9),.05);box(1.73,.25,.04,.2,.1,M(0x7a3a2a,.9));box(1.725,.29,.03,.12,.05,M(0xff7a1a,.5,2.2));
 for(const[x,z]of[[.62,.47],[1.7,.52],[.09,1.08]]){box(x-.006,z-.006,.012,.012,.08,M(0x333333,.5));const p=new THREE.Mesh(new THREE.ConeGeometry(.025,.03,12,1,true),M(0xfff0c8,.6,1.4));p.position.set(ox+x,b+.09,oz+z);G.add(p)}
 // árbol de Navidad del salón con bolas que brillan
 {const[ax,az]=CASA_ARBOL;for(let q=0;q<3;q++){const c=new THREE.Mesh(new THREE.ConeGeometry(.07-q*.017,.07,12),M(0x1f6a3a,.8));c.position.set(ox+ax,b+.05+q*.04,oz+az);c.castShadow=true;G.add(c)}
  const est=new THREE.Mesh(new THREE.OctahedronGeometry(.012),M(0xffe08a,.4,1.6));est.position.set(ox+ax,b+.165,oz+az);G.add(est);
  const CB=[0xff3b3b,0xffd24a,0x4aa8ff,0xff4fb0,0xffffff];for(let k=0;k<22;k++){const t=k/22,a=k*2.2,rr=.065*(1-t*.8),bo=new THREE.Mesh(new THREE.SphereGeometry(.006,6,5),M(CB[k%5],.4,1.3));bo.position.set(ox+ax+Math.cos(a)*rr,b+.03+t*.12,oz+az+Math.sin(a)*rr);G.add(bo)}
  C.hueco=new THREE.Mesh(new THREE.RingGeometry(.09,.11,24),new THREE.MeshBasicMaterial({color:0xffd24a,transparent:true,opacity:.7,depthWrite:false}));C.hueco.rotation.x=-Math.PI/2;C.hueco.position.set(ox+ax,b+.008,oz+az);G.add(C.hueco)}
 // salida: alfombrilla brillante en la puerta (se activa con el regalo dejado)
 C.salida=new THREE.Mesh(new THREE.RingGeometry(.05,.07,20),new THREE.MeshBasicMaterial({color:0x3fe07a,transparent:true,opacity:.8,depthWrite:false}));C.salida.rotation.x=-Math.PI/2;C.salida.position.set(ox+CASA_PUERTA[0],b+.008,oz+CASA_PUERTA[1]+.08);C.salida.visible=false;G.add(C.salida);
 // los de la casa: cuerpo, cabeza y cono de visión
 const gente=[{n:'Papá',col:0x2a4fa8,ruta:[[.14,.88],[.6,.88],[.6,.7],[.14,.7]],v:.085,esp:1},{n:'Mamá',col:0xc23f6a,ruta:[[.86,.92],[1.66,.92]],v:.075,esp:1.4},{n:'Niño',col:0x2fa84f,fijo:[.98,.3],mira:Math.PI/2,barre:1.25,per:6.5,peq:1}];
 C.gente=gente.map(g=>{const o=new THREE.Group(),s_=g.peq?.75:1;const cu=new THREE.Mesh(new THREE.CylinderGeometry(.013*s_,.016*s_,.05*s_,10),M(g.col,.7));cu.position.y=.032*s_;o.add(cu);
  const ca=new THREE.Mesh(new THREE.SphereGeometry(.011*s_,10,8),M(0xf0c8a8,.7));ca.position.y=.068*s_;o.add(ca);const ojo=new THREE.Mesh(new THREE.BoxGeometry(.004,.003,.014*s_),M(0x111111,.5));ojo.position.set(.01*s_,.07*s_,0);o.add(ojo);
  const RG=.4,AN=.62,cg=new THREE.CircleGeometry(RG,28,-AN,AN*2);cg.rotateX(-Math.PI/2);const cono=new THREE.Mesh(cg,new THREE.MeshBasicMaterial({color:0xffe066,transparent:true,opacity:.22,depthWrite:false}));cono.position.y=.006;cono.renderOrder=3;
  const cw=new THREE.Group();cw.add(cono);G.add(cw);G.add(o);return Object.assign({},g,{o,cw,cono,RG,AN,i:0,x:0,z:0,a:0,p:0,al:0})});
 // el protagonista
 C.fig=figNav(REP.spec||{t:'sleigh',col:[0xc4161f]});C.fig.scale.setScalar(.8);G.add(C.fig);
 scene.add(G);C.G=G}
function casaReset(){const C=CASM;C.px=CASA_PUERTA[0];C.pz=CASA_PUERTA[1]+.1;C.pa=Math.PI/2;C.regalo=false;C.dejando=0;C.pillado=0;C.alerta=0;if(C.caja){C.G.remove(C.caja);C.caja=null}C.salida.visible=false;C.hueco.visible=true;
 for(const g of C.gente){g.i=0;g.p=0;g.al=0;if(g.ruta){g.x=g.ruta[0][0];g.z=g.ruta[0][1];g.a=Math.atan2(-(g.ruta[1][1]-g.z),g.ruta[1][0]-g.x)}else{g.x=g.fijo[0];g.z=g.fijo[1];g.a=g.mira}}}
function casaEntra(){const C=CASM;C.car=[P.x,P.y,P.a];C.ox=C.d[1]-CASA_W/2;C.oz=C.d[2]-CASA_D/2;C.base=groundY(C.d[1],C.d[2])+24;if(!C.G)casaConstruye();casaReset();
 cambiarModo('casa');C.fase='dentro';camInit=false;window.__BAJO=true;try{sonCaja()}catch(e){}
 REP.dest=['🎄 Árbol del salón',C.ox+CASA_ARBOL[0],C.oz+CASA_ARBOL[1]];gpsParar();repHud();
 aviso('🤫 ¡Que no te vean!',2,'cuenta');setTimeout(()=>{if(CASM.fase==='dentro')mostrar('Flechas / ◀ ▶ ▲ ▼ para moverte · evita los conos amarillos · deja el regalo bajo el árbol y sal por la puerta')},2200)}
// choque con paredes y muebles (círculo contra rectángulos)
function casaLibre(x,z,r_){if(x<-.6||x>CASA_W+.6||z<-.6||z>CASA_D+.6)return false;for(const w of CASA_MUROS.concat(CASA_MUEB))if(x>w[0]-r_&&x<w[0]+w[2]+r_&&z>w[1]-r_&&z<w[1]+w[3]+r_)return false;
 if(Math.hypot(x-CASA_ARBOL[0],z-CASA_ARBOL[1])<.07+r_)return false;return true}
// ¿algo tapa la línea de vista? (paredes y muebles altos)
function casaVista(x0,z0,x1,z1){const T=CASA_MUROS.concat(CASA_MUEB.filter(m=>m[6]));const n=Math.ceil(Math.hypot(x1-x0,z1-z0)/.012);for(let i=1;i<n;i++){const x=x0+(x1-x0)*i/n,z=z0+(z1-z0)*i/n;for(const w of T)if(x>w[0]&&x<w[0]+w[2]&&z>w[1]&&z<w[1]+w[3])return false}return true}
function updateCasa(dt){const C=CASM;if(!REP.on||!C.on){casaSale(false);return}const tn=performance.now()/1000;
 // movimiento según la pantalla (cámara fija desde el sur)
 let mx=(keys.right?1:0)-(keys.left?1:0),mz=(keys.down?1:0)-(keys.up?1:0);
 const L=Math.hypot(mx,mz);let anda=false;if(L>0&&!C.pillado&&!(C.dejando>0)){mx/=L;mz/=L;const v=.17*dt,nx=C.px+mx*v,nz=C.pz+mz*v;if(casaLibre(nx,C.pz,.02))C.px=nx;if(casaLibre(C.px,nz,.02))C.pz=nz;C.pa=Math.atan2(-mz,mx);anda=true}
 if(C.dejando>0&&L>0){C.dejando=0;mostrar('Te has movido: vuelve a dejar el regalo')}
 // dejar el regalo
 if(C.dejando>0){C.dejando+=dt;const pc=Math.min(100,Math.round(C.dejando/1.3*100));aviso('🎁 Dejando el regalo… '+pc+'%',.3,'peq');if(C.dejando>=1.3){C.dejando=0;C.regalo=true;C.hueco.visible=false;C.salida.visible=true;REP.pts+=150;repPop('🎁 ¡Regalo bajo el árbol! +150','gran');try{sonCaja();setTimeout(sonJoJo,200)}catch(e){}
  const cj=new THREE.Mesh(new THREE.BoxGeometry(.03,.03,.03),new THREE.MeshStandardMaterial({color:0xc23fd0,emissive:0xc23fd0,emissiveIntensity:.4}));cj.position.set(C.ox+CASA_ARBOL[0]-.07,C.base+.015,C.oz+CASA_ARBOL[1]+.05);C.G.add(cj);C.caja=cj;
  REP.dest=['🚪 Salida',C.ox+CASA_PUERTA[0],C.oz+CASA_PUERTA[1]];repHud();setTimeout(()=>{if(CASM.fase==='dentro')mostrar('¡Ahora sal por la puerta sin que te vean!')},800)}}
 // salir por la puerta con el regalo dejado
 if(C.regalo&&C.pz>CASA_PUERTA[1]+.05&&Math.abs(C.px-CASA_PUERTA[0])<.12){casaSale(true);return}
 // los de la casa: rutas, pausas mirando y el niño que mira la tele y a veces alrededor
 let visto=0;for(const g of C.gente){if(g.ruta){if(g.p>0){g.p-=dt;g.a+=Math.sin(tn*2.2+g.v*40)*dt*1.4}else{const t=g.ruta[(g.i+1)%g.ruta.length],dx=t[0]-g.x,dz=t[1]-g.z,d=Math.hypot(dx,dz),st=g.v*dt;g.a=Math.atan2(-dz,dx);if(d<=st){g.x=t[0];g.z=t[1];g.i=(g.i+1)%g.ruta.length;g.p=g.esp}else{g.x+=dx/d*st;g.z+=dz/d*st}}}
  else{const f=(tn%g.per)/g.per;g.a=g.mira+(f>.6?Math.sin((f-.6)/.4*Math.PI*2)*g.barre:0)}
  // ¿te ve?
  const dx=C.px-g.x,dz=C.pz-g.z,d=Math.hypot(dx,dz);let ve=false;if(d<g.RG&&C.pz<CASA_D+.05){let da=Math.atan2(-dz,dx)-g.a;da=Math.atan2(Math.sin(da),Math.cos(da));if(Math.abs(da)<g.AN&&casaVista(g.x,g.z,C.px,C.pz))ve=true}
  g.al=Math.max(0,Math.min(1,g.al+(ve?dt*(d<.15?4:2.4):-dt*.8)));visto=Math.max(visto,g.al);
  g.o.position.set(C.ox+g.x,C.base+(g.ruta&&g.p<=0?Math.abs(Math.sin(tn*10))*.004:0),C.oz+g.z);g.o.rotation.y=g.a;g.cw.position.set(C.ox+g.x,C.base,C.oz+g.z);g.cw.rotation.y=g.a;
  g.cono.material.color.setRGB(1,.88-.7*g.al,.4-.3*g.al);g.cono.material.opacity=.2+.25*g.al}
 if(visto>=1&&!C.pillado){C.pillado=1.6;try{bip(220,.35,.12);setTimeout(()=>bip(160,.4,.12),180)}catch(e){}aviso('😱 ¡Te han visto! Vuelve a empezar',1.6,'cuenta');padVibra(.6,.8,300)}
 else if(visto>.35&&!C.pillado&&(!C.avV||tn-C.avV>2.5)){C.avV=tn;repPop('❓ ¿Qué ha sido eso?','aviso')}
 if(C.pillado){C.pillado-=dt;if(C.pillado<=0){casaReset()}}
 // figura y cámara de casa de muñecas
 const F=C.fig;F.position.set(C.ox+C.px,C.base,C.oz+C.pz);F.rotation.y=C.pa;const k=anda?Math.sin(tn*12)*.6:0;F.userData.pi[0].rotation.z=k;F.userData.pi[1].rotation.z=-k;F.userData.br[0].rotation.z=-k*.6;F.userData.br[1].rotation.z=k*.6;
 P.x=C.ox+C.px;P.y=C.oz+C.pz;P.v=0;
 const want=new THREE.Vector3(C.ox+C.px,C.base+1.05,C.oz+C.pz+.62);if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*4));look.set(C.ox+C.px,C.base,C.oz+C.pz+.05);pcam.lookAt(look);pcam.fov=55;pcam.updateProjectionMatrix();
 FOG.color.setRGB(.05,.06,.12);FOG.near=1.4;FOG.far=3.2;
 const v=document.getElementById('vel');v.firstChild.nodeValue=Math.round(visto*100);v.querySelector('small').textContent='% te han visto · sigilo';hudAccion(dt)}
function casaSale(ok){const C=CASM;window.__BAJO=false;FOG.near=5;FOG.far=20;if(C.G){scene.remove(C.G);C.G.traverse(o=>{if(o.geometry)o.geometry.dispose()});C.G=null}C.on=false;C.fase='fin';
 if(C.car){P.x=C.car[0];P.y=C.car[1];P.a=C.car[2]}P.v=0;cambiarModo('coche');camInit=false;if(!ok)return;
 const pts=300;REP.pts+=pts;REP.ent++;REP.nEnt=(REP.nEnt||0)+1;try{sonJoJo();setTimeout(()=>sonPublico(1.2),400)}catch(e){}repPop('🤫 ¡Misión de sigilo superada! +'+pts+' ⭐','gran');
 const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;repSigue(ab,1600)}
function repCocheCalle(){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok casa')
