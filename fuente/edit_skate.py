import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MISIÓN: SKATE POR LOS TEJADOS DE VIGO =================
# Papá Noel (o el Rey Mago elegido) sube a los tejados de una fila de edificios junto a una avenida y la recorre en
# skate a toda velocidad. Va solo hacia delante: E / Ⓐ / espacio salta de un edificio a otro por encima de las calles;
# en el aire, ◀ ▶ hacen giros (360, 720…) y ▼ un flip, que suman puntos al aterrizar. Cada chimenea por la que pasa
# recibe un regalo. Si cae a la calle, vuelve al último tejado. Sencillo y rápido.
r("const esCasaK=k=>k===2||(k>12&&(k-13)%6===0),esApaK=k=>false;",
  "const esCasaK=k=>k===2||(k>12&&(k-13)%6===0),esApaK=k=>false,esSkaK=k=>k===7||(k>14&&(k-15)%6===0);")
r("if(esApaK(k))return{v:'coche',apagon:true,txt:'😈 Persigue al Apagón'};let c=0;for(let i=0;i<k;i++)if(esCasaK(i)||esApaK(i))c++;",
  "if(esApaK(k))return{v:'coche',apagon:true,txt:'😈 Persigue al Apagón'};if(esSkaK(k))return{v:'coche',skate:true,txt:'🛹 Skate por los tejados'};let c=0;for(let i=0;i<k;i++)if(esCasaK(i)||esApaK(i)||esSkaK(i))c++;")
r("if(MODO==='casa'){updateCasa(dt);return}","if(MODO==='casa'){updateCasa(dt);return}if(MODO==='skate'){updateSkate(dt);return}")
r("function accion(){if(!driving)return;","function accion(){if(!driving)return;if(SKT.on&&skateAccion())return;")
r("function buscarObjetivo(){objetivo=null;","function buscarObjetivo(){objetivo=null;if(SKT.on){if(SKT.fase==='ir'&&MODO==='coche'&&SKT.cerca){objetivo={k:'skate'};return '🛹 Subir al tejado'}if(MODO==='skate'){objetivo={k:'skate'};return '⤒ Saltar'}}")
r("if(m.apagon&&APG.on){apagonTick(dt||.016);return}","if(m.apagon&&APG.on){apagonTick(dt||.016);return}if(m.skate&&SKT.on){skateTick(dt||.016);return}")
r(" if(m.casa&&casaInicio(m,k))return;"," if(m.casa&&casaInicio(m,k))return;if(m.skate&&skateInicio(m,k))return;")
r("MODO!=='nado'&&MODO!=='casa')navEstela(","MODO!=='nado'&&MODO!=='casa'&&MODO!=='skate')navEstela(")
r("function repCocheCalle(){",r"""const SKT={on:false};window.__SKT=SKT;
addEventListener('keydown',e=>{if(SKT.on&&MODO==='skate'&&e.code==='Space'){e.preventDefault();if(!e.repeat)skateSalta()}});
// recorrido: una avenida desplazada hacia la fila de edificios de uno de sus lados
const SKT_CALLES=[[[93.64,20.41],[94.57,20.76],[96.49,21.43],[97.0,21.58]],[[93.08,17.62],[90.06,18.17],[89.1,18.11]],[[97.57,21.9],[99.31,22.46],[100.5,22.84],[102.22,23.37]]];
function skateCurso(){let best=null;for(const C of SKT_CALLES){if(Math.hypot(C[0][0]-P.x,C[0][1]-P.y)>12)continue;for(const lado of[1,-1])for(const off of[.14,.18,.22,.27,.32]){const pts=[];let acc=0;
   for(let i=1;i<C.length;i++){const a=C[i-1],b=C[i],L=Math.hypot(b[0]-a[0],b[1]-a[1]),ux=(b[0]-a[0])/L,uy=(b[1]-a[1])/L;for(let t=(i>1?.03:0);t<=L;t+=.03)pts.push([a[0]+ux*t-uy*off*lado,a[1]+uy*t+ux*off*lado,ux,uy])}
   const ed=pts.filter(p=>cell(p[0],p[1]).t===3).length/pts.length;if(ed>.45&&(!best||ed>best.ed))best={pts,ed,C,lado,off}}}return best}
function skateInicio(m,k){const cu=skateCurso();if(!cu)return false;REP.mis=m;if(MODO!=='coche')repCocheCalle();Object.assign(SKT,{on:true,fase:'ir',cu,t:0,av:0,cerca:false});REP.fase='skate';
 const c0=cu.C[0];campDestino(['🛹 Inicio del recorrido por los tejados',c0[0],c0[1]]);aviso('🛹 Misión '+(k+1)+' · ¡Skate por los tejados!',2.4,'cuenta');
 setTimeout(()=>{if(SKT.on&&SKT.fase==='ir')mostrar('Ve al inicio del recorrido: desde allí subirás a los tejados con el skate')},2600);return true}
function skateAccion(){if(SKT.fase==='ir'&&MODO==='coche'&&SKT.cerca){skateSube();return true}if(MODO==='skate'){skateSalta();return true}return false}
function skateTick(dt){const S=SKT;S.t+=dt;if(S.fase==='ir'&&MODO==='coche'){const c0=S.cu.C[0];S.cerca=Math.hypot(c0[0]-P.x,c0[1]-P.y)<.3;if(S.cerca){S.av-=dt;if(S.av<=0){S.av=3;mostrar(document.body.classList.contains('pad')?'Ⓐ para subir al tejado con el skate':'E (o el botón de acción) para subir al tejado con el skate')}}}}
// la tabla y el patinador
function mkSkate(){const g=new THREE.Group(),M=(c,r_=.5,mt=0,e=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r_,metalness:mt,emissive:e?c:0,emissiveIntensity:e});
 const tb=new THREE.Group();g.add(tb);const de=new THREE.Mesh(new THREE.BoxGeometry(.075,.0045,.022),M(0x2a2a30,.6));de.position.y=.012;tb.add(de);const gr=new THREE.Mesh(new THREE.BoxGeometry(.06,.001,.02),M(0xc4161f,.7));gr.position.y=.0148;tb.add(gr);
 for(const x of[.026,-.026]){const ej=new THREE.Mesh(new THREE.BoxGeometry(.006,.003,.022),M(0xb9bec6,.3,.8));ej.position.set(x,.008,0);tb.add(ej);for(const z of[.009,-.009]){const w=new THREE.Mesh(new THREE.CylinderGeometry(.0045,.0045,.005,10),M(0xffe066,.4,0,.4));w.rotation.x=Math.PI/2;w.position.set(x,.0045,z);tb.add(w)}}
 const f=figNav(REP.spec||{t:'sleigh',col:[0xc4161f]});f.scale.setScalar(.85);f.position.y=.0125;f.rotation.y=-Math.PI/2*.6;f.userData.pi[0].rotation.z=.35;f.userData.pi[1].rotation.z=-.35;f.userData.br[0].rotation.x=.9;f.userData.br[1].rotation.x=-.9;g.add(f);
 const sa=new THREE.Mesh(new THREE.SphereGeometry(.013,10,8),M(0x8a5a2b,.9));sa.position.set(-.012,.075,.006);g.add(sa);g.userData={tb,f};return g}
function skateSube(){const S=SKT,cu=S.cu,n=cu.pts.length;S.car=[P.x,P.y,P.a];
 // alturas de los tejados a lo largo del recorrido (se suavizan un poco)
 const H=[],T=[];for(const p of cu.pts){const ed=cell(p[0],p[1]).t===3,ms=ed?repMallas(p[0],p[1]):[],h=ed&&ms.length?repAltura(p[0],p[1],ms):-1,g=groundY(p[0],p[1]);T.push(ed&&h>g+.08);H.push(T[T.length-1]?h:g)}
 for(let i=1;i<n-1;i++)if(T[i-1]&&T[i]&&T[i+1])H[i]=(H[i-1]+H[i]*2+H[i+1])/4;S.H=H;S.T=T;
 let i0=T.indexOf(true);if(i0<0){mostrar('Aquí no hay tejados cargados: prueba otra vez en un momento');return}
 // chimeneas a lo largo de los tejados
 const G=new THREE.Group();G.name='skateCurso';const LAD=new THREE.MeshStandardMaterial({color:0x9a3b2b,roughness:.9}),NIE=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9}),HAZ=new THREE.MeshBasicMaterial({color:0xffd24a,transparent:true,opacity:.35,depthWrite:false,blending:THREE.AdditiveBlending});
 S.chim=[];for(let i=i0+12;i<n-4;i+=Math.round(.42/.03)){let j=i;while(j<n-4&&!(T[j]&&T[j+1]&&T[j-1]))j++;if(j>=n-4)break;const p=cu.pts[j],ox=-p[3]*.035,oy=p[2]*.035;const c=new THREE.Group();c.position.set(p[0]+ox,H[j],p[1]+oy);
  const b=new THREE.Mesh(new THREE.BoxGeometry(.028,.045,.028),LAD);b.position.y=.022;c.add(b);const t=new THREE.Mesh(new THREE.BoxGeometry(.034,.007,.034),NIE);t.position.y=.047;c.add(t);const hz=new THREE.Mesh(new THREE.CylinderGeometry(.01,.01,.5,8,1,true),HAZ);hz.position.y=.3;c.add(hz);G.add(c);S.chim.push({i:j,g:c,hz,ok:false});i=j}
 scene.add(G);S.G=G;S.sk=mkSkate();scene.add(S.sk);
 Object.assign(S,{fase:'patina',s:i0,z:H[i0],vz:0,air:false,spin:0,flip:0,check:i0,pts:0,regalos:0,combo:0,t:0,cae:0});cambiarModo('skate');camInit=false;REP.dest=null;gpsParar();repHud();
 try{sonCaja()}catch(e){}aviso('🛹 ¡A patinar por los tejados!',1.8,'cuenta');setTimeout(()=>{if(SKT.fase==='patina')mostrar((document.body.classList.contains('pad')?'Ⓐ salta':'E / espacio salta')+' · en el aire ◀ ▶ giros y ▼ flip · pasa por las chimeneas para dejar regalos')},1800)}
function skateSalta(){const S=SKT;if(S.fase!=='patina'||S.air)return;S.air=true;S.vz=1.05;S.spin=0;S.flip=0;try{bip(520,.06,.05)}catch(e){}}
function updateSkate(dt){const S=SKT;if(!REP.on||!S.on){skateSale(false);return}const cu=S.cu,n=cu.pts.length,tn=performance.now()/1000;
 if(S.cae>0){S.cae-=dt;if(S.cae<=0){S.s=S.check;S.z=S.H[S.check];S.vz=0;S.air=false;camInit=false}}
 else{const v=(1.15+(keys.up?.35:0)-(keys.down?.35:0))*(S.air?1.05:1);S.s+=v*dt/.03;
  if(S.s>=n-1){skateSale(true);return}
  const i=Math.floor(S.s),u=S.s-i,hr=S.H[i]*(1-u)+S.H[Math.min(n-1,i+1)]*u,techo=S.T[i]||S.T[Math.min(n-1,i+1)];
  if(!S.air){if(hr<S.z-.02){S.air=true;S.vz=0}else if(hr>S.z+.07){S.air=true;S.vz=Math.sqrt(2*2.3*(hr-S.z+.05));S.spin=0;S.flip=0}else S.z+=(hr-S.z)*Math.min(1,dt*18);
   {let gap=false;for(let q=2;q<9;q++){const j=Math.min(n-1,i+q);if(!S.T[j]){gap=true;break}}if(gap&&!S.air&&S.T[i]&&(!S.avS||tn-S.avS>1.2)){S.avS=tn;aviso('⤒ ¡SALTA!',.6,'peq')}}}
  else{S.vz-=2.3*dt;S.z+=S.vz*dt;if(keys.left)S.spin+=dt*11;if(keys.right)S.spin-=dt*11;if(keys.down)S.flip+=dt*10;
   if(S.vz<0&&S.z<=hr){if(techo){S.air=false;S.z=hr;S.check=i;const g=Math.floor(Math.abs(S.spin)/5.6),fl=Math.floor(S.flip/5.6);if(g||fl){const pts=(g*50+fl*80)*(1+S.combo*.5);S.combo++;REP.pts+=Math.round(pts);repPop((fl?'🛹 Kickflip ':'')+(g?g*360+'° ':'')+'+'+Math.round(pts)+(S.combo>1?' · combo x'+S.combo:''),'aviso');try{bip(880,.08,.05)}catch(e){}}else S.combo=0;S.spin=0;S.flip=0;REP.shake=.12}
    else if(S.z<groundY(cu.pts[i][0],cu.pts[i][1])+.02){S.cae=1.1;S.combo=0;aviso('😵 ¡A la calle! Vuelves al último tejado',1.3,'peq');REP.shake=.35;try{bip(200,.25,.08)}catch(e){}}}}
  // chimeneas: se deja el regalo al pasar
  for(const c of S.chim)if(!c.ok&&S.s>=c.i-.5&&S.s<=c.i+2.5&&Math.abs(S.z-S.H[c.i])<.25){c.ok=true;c.hz.visible=false;S.regalos++;REP.pts+=100;repPop('🎁 ¡Regalo por la chimenea! '+S.regalos+'/'+S.chim.length+' · +100','gran');try{sonCaja();setTimeout(sonJoJo,150)}catch(e){}
   const gb=new THREE.Mesh(new THREE.BoxGeometry(.016,.016,.016),new THREE.MeshStandardMaterial({color:[0xd51f1f,0x1fae4a,0xf2c230,0x1f6fd0][S.regalos%4],emissive:0x333333}));gb.position.copy(S.sk.position);gb.position.y+=.08;scene.add(gb);const tg=c.g.position.clone();let k=0;const an=()=>{k+=.06;gb.position.lerp(tg.clone().setY(tg.y+.05+(1-k)*.08),.25);gb.rotation.y+=.3;if(k<1)requestAnimationFrame(an);else scene.remove(gb)};an()}}
 // colocar patinador y cámara
 const i=Math.min(n-2,Math.floor(S.s)),u=S.s-i,p=cu.pts[i],q=cu.pts[i+1],x=p[0]+(q[0]-p[0])*u,y=p[1]+(q[1]-p[1])*u,a=Math.atan2(-p[3],p[2]);P.x=x;P.y=y;P.a=a;P.v=0;
 const sk=S.sk;sk.visible=S.cae<=0||S.cae>.6;sk.position.set(x,S.z,y);sk.rotation.set(0,a+S.spin,0);sk.userData.tb.rotation.x=S.flip;sk.userData.f.position.y=.0125+(S.air?0:Math.abs(Math.sin(tn*14))*.002);
 const dx=Math.cos(a),dz=-Math.sin(a),want=new THREE.Vector3(x-dx*.42,S.z+.2,y-dz*.42);if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*6));look.set(x+dx*.35,S.z+.02,y+dz*.35);pcam.lookAt(look);pcam.fov=72+(keys.up?6:0);pcam.updateProjectionMatrix();
 FOG.near=5;FOG.far=20;const vv=document.getElementById('vel');vv.firstChild.nodeValue=S.regalos+'/'+S.chim.length;vv.querySelector('small').textContent='🎁 chimeneas · 🛹 skate';hudAccion(dt)}
function skateSale(ok){const S=SKT;if(S.G){scene.remove(S.G);S.G=null}if(S.sk){scene.remove(S.sk);S.sk=null}S.on=false;S.fase='fin';if(MODO==='skate'){cambiarModo('coche');repCocheCalle()}P.v=0;camInit=false;if(!ok)return;
 const pts=150+S.regalos*50;REP.pts+=pts;REP.ent++;REP.nEnt=(REP.nEnt||0)+1;try{sonJoJo();setTimeout(()=>sonPublico(1.3),400)}catch(e){}repPop('🛹 ¡Recorrido completado! '+S.regalos+'/'+S.chim.length+' chimeneas · +'+pts+' ⭐','gran');
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
print('ok skate')
