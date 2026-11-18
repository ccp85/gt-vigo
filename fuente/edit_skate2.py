import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= SKATE 2: TEJADOS EN LIBERTAD, AL ATARDECER =================
# Control libre: ◀ ▶ giran, ▲ impulsa, ▼ frena; E / Ⓐ / espacio salta. En el aire ◀ ▶ hacen giros y ▼ un flip.
# Las chimeneas (10, a lo largo de la avenida y a ambos lados) están marcadas con un haz dorado, una flecha sobre el
# patinador y la línea del GPS en el minimapa; se reparten en el orden que quieras. Si caes a la calle vuelves al
# último tejado seguro. Al acabar, un gran salto te devuelve a la carroza. La prueba es al atardecer.
a=s.index("function skateSube(){");b=s.index("function repCocheCalle(){")
s=s[:a]+r"""function skAlt(x,y){const g=groundY(x,y),ms=repMallas(x,y);const h=ms.length?repAltura(x,y,ms):-1;return h>g+.05?[h,true,g]:[g,false,g]}
// punto de tejado abierto: tejado alrededor y nada mucho más alto (evita patios de luces)
function skBueno(x,y){const h=skAlt(x,y);if(!h[1])return null;for(let k=0;k<8;k++){const a=k/8*6.283,q=skAlt(x+Math.cos(a)*.055,y+Math.sin(a)*.055);if(!q[1]||q[0]>h[0]+.035)return null}return h[0]}
function skateSube(){const S=SKT,cu=S.cu;S.car=[P.x,P.y,P.a];
 // primer tejado: el más cercano a la carroza
 let st=null;for(let r_=.06;r_<.6&&!st;r_+=.03)for(let k=0;k<16&&!st;k++){const an=k/16*6.283,x=P.x+Math.cos(an)*r_,y=P.y+Math.sin(an)*r_,h=skBueno(x,y);if(h!=null)st=[x,y,h]}
 if(!st){mostrar('Aquí no hay tejados cargados: prueba otra vez en un momento');return}
 // chimeneas a lo largo de la avenida, a los dos lados, separadas
 const C=cu.C,cand=[];for(let i=1;i<C.length;i++){const a0=C[i-1],b0=C[i],L=Math.hypot(b0[0]-a0[0],b0[1]-a0[1]),ux=(b0[0]-a0[0])/L,uy=(b0[1]-a0[1])/L;
  for(let t=0;t<=L;t+=.07)for(const ld of[1,-1])for(const off of[.13,.2,.28,.36]){const x=a0[0]+ux*t-uy*off*ld,y=a0[1]+uy*t+ux*off*ld,h=skBueno(x,y);if(h!=null)cand.push({x,y,h,o:(i-1)*100+t,ld})}}
 let LT=0;for(let i=1;i<C.length;i++)LT+=Math.hypot(C[i][0]-C[i-1][0],C[i][1]-C[i-1][1]);const SEP=Math.max(.33,Math.min(.6,LT/11));
 cand.sort((p,q)=>p.o-q.o);const sel=[];let lado=1;for(const c of cand){if(sel.length>=10)break;if(Math.hypot(c.x-st[0],c.y-st[1])<.25)continue;if(sel.some(q=>Math.hypot(q.x-c.x,q.y-c.y)<SEP))continue;sel.push(c);lado=-c.ld}
 const G=new THREE.Group();G.name='skateCurso';const LAD=new THREE.MeshStandardMaterial({color:0x9a3b2b,roughness:.9}),NIE=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9}),HAZ=new THREE.MeshBasicMaterial({color:0xffd24a,transparent:true,opacity:.4,depthWrite:false,blending:THREE.AdditiveBlending,fog:false}),ARO=new THREE.MeshBasicMaterial({color:0xffe08a,transparent:true,opacity:.75,depthWrite:false,fog:false});
 S.chim=[];for(const c of sel){const g=new THREE.Group();g.position.set(c.x,c.h,c.y);const b=new THREE.Mesh(new THREE.BoxGeometry(.03,.05,.03),LAD);b.position.y=.025;g.add(b);const t=new THREE.Mesh(new THREE.BoxGeometry(.037,.008,.037),NIE);t.position.y=.052;g.add(t);
  const hz=new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,1.2,10,1,true),HAZ);hz.position.y=.65;g.add(hz);const ar=new THREE.Mesh(new THREE.TorusGeometry(.06,.004,6,28),ARO);ar.rotation.x=Math.PI/2;ar.position.y=.01;g.add(ar);G.add(g);S.chim.push({x:c.x,y:c.y,h:c.h,g,hz,ar,ok:false})}
 // flecha sobre el patinador hacia la chimenea más cercana
 const fl=new THREE.Mesh(new THREE.ConeGeometry(.013,.034,4),new THREE.MeshBasicMaterial({color:0xffd24a,fog:false,depthTest:false,transparent:true}));fl.geometry.rotateZ(-Math.PI/2);fl.renderOrder=9;G.add(fl);S.fl=fl;
 scene.add(G);S.G=G;S.sk=mkSkate();scene.add(S.sk);S.hPrev=CIELO.h;S.mPrev=CIELO.modo;CIELO.modo='tarde';CIELO.h=19.1;
 const a0=Math.atan2(-(cu.C[1][1]-cu.C[0][1]),cu.C[1][0]-cu.C[0][0]);
 Object.assign(S,{fase:'patina',x:st[0],y:st[1],a:a0,v:.45,z:st[2],vz:0,air:false,spin:0,flip:0,safe:[st[0],st[1],a0,st[2]],safeT:0,regalos:0,combo:0,t:0,cae:0,gpsT:0,par:0});
 cambiarModo('skate');car.visible=true;camInit=false;REP.dest=null;gpsParar();skObjetivo();repHud();
 try{sonCaja()}catch(e){}aviso('🛹 ¡A patinar por los tejados de Vigo!',1.8,'cuenta');setTimeout(()=>{if(SKT.fase==='patina')mostrar('◀ ▶ gira · ▲ impulso · ▼ frena · '+(document.body.classList.contains('pad')?'Ⓐ':'E / espacio')+' salta · sigue los haces dorados: '+S.chim.length+' chimeneas')},1800)}
function skObjetivo(){const S=SKT;let b=null,bd=1e9;for(const c of S.chim)if(!c.ok){const d=Math.hypot(c.x-S.x,c.y-S.y);if(d<bd){bd=d;b=c}}S.obj=b;if(b){REP.dest=['🏠 Chimenea '+(S.regalos+1)+'/'+S.chim.length,b.x,b.y];gpsSet(REP.dest,linea([[S.x,S.y],[b.x,b.y]]))}else{REP.dest=null;gpsParar()}}
function skateSalta(){const S=SKT;if(S.fase!=='patina'||S.air||S.cae>0)return;S.air=true;S.vz=1.0;S.spin=0;S.flip=0;try{bip(520,.06,.05)}catch(e){}}
function updateSkate(dt){const S=SKT;if(!REP.on||!S.on){skateSale(false);return}const tn=performance.now()/1000;dt=Math.min(dt,.05);
 if(S.fase==='vuelta'){skVuelta(dt);return}
 if(S.cae>0){S.cae-=dt;if(S.cae<=0){[S.x,S.y,S.a,S.z]=S.safe;S.v=.3;S.vz=0;S.air=false;camInit=false}}
 else{
  // dirección y velocidad (control libre)
  const tr=S.air?.9:2.7;if(!S.air){if(keys.left)S.a+=tr*dt;if(keys.right)S.a-=tr*dt}else{if(keys.left){S.spin+=dt*11;S.a+=tr*dt}if(keys.right){S.spin-=dt*11;S.a-=tr*dt}if(keys.down)S.flip+=dt*10}
  if(!S.air){const obj=keys.up?1.05:keys.down?0:.6;S.v+=(obj-S.v)*Math.min(1,dt*(keys.down?3.5:1.6))}
  const dx=Math.cos(S.a),dy=-Math.sin(S.a),nx=S.x+dx*S.v*dt,ny=S.y+dy*S.v*dt,hn=skAlt(nx+dx*.015,ny+dy*.015);
  if(hn[0]>S.z+.05){ // pared delante: si es poco más alta se sube de un salto, si no, rebota
   if(!S.air&&hn[0]-S.z<.2){S.air=true;S.vz=Math.sqrt(2*2.3*(hn[0]-S.z+.04));S.spin=0;S.flip=0;S.x=nx;S.y=ny}
   else{S.v=Math.max(.15,S.v*.3);S.a+=Math.PI*.9;REP.shake=.15;if(!S.avP||tn-S.avP>1){S.avP=tn;aviso('🧱 ¡Pared! Busca otro camino',.8,'peq')}}}
  else{S.x=nx;S.y=ny}
  const h=skAlt(S.x,S.y);
  if(!S.air){if(h[0]<S.z-.03){S.air=true;S.vz=0}else S.z+=(h[0]-S.z)*Math.min(1,dt*18);
   if(h[1]){S.safeT+=dt;if(S.safeT>.4){let ok=true;for(const[a,b]of[[.05,0],[-.05,0],[0,.05],[0,-.05]])if(!skAlt(S.x+a,S.y+b)[1]){ok=false;break}if(ok){S.safe=[S.x,S.y,S.a,S.z];S.safeT=0}}}
   // aviso de borde
   const e=skAlt(S.x+dx*.12,S.y+dy*.12);if(!e[1]&&h[1]&&S.v>.3&&(!S.avS||tn-S.avS>1.4)){S.avS=tn;aviso('⤒ ¡SALTA!',.6,'peq')}}
  else{S.vz-=2.3*dt;S.z+=S.vz*dt;
   if(S.vz<0&&S.z<=h[0]){if(h[1]){S.air=false;S.z=h[0];const g=Math.floor(Math.abs(S.spin)/5.6),fl=Math.floor(S.flip/5.6);if(g||fl){const pts=(g*50+fl*80)*(1+S.combo*.5);S.combo++;REP.pts+=Math.round(pts);repPop((fl?'🛹 Kickflip ':'')+(g?g*360+'° ':'')+'+'+Math.round(pts)+(S.combo>1?' · combo x'+S.combo:''),'aviso');try{bip(880,.08,.05)}catch(e){}}else S.combo=0;S.spin=0;S.flip=0;REP.shake=.1}
    else{S.cae=1.1;S.combo=0;S.v=0;aviso('😵 ¡A la calle! Vuelves al último tejado',1.3,'peq');REP.shake=.35;try{bip(200,.25,.08)}catch(e){}}}}
  // chimeneas
  for(const c of S.chim){c.ar.rotation.z=tn*2;if(!c.ok&&Math.hypot(c.x-S.x,c.y-S.y)<.085&&S.z<c.h+.2&&S.z>c.h-.06){c.ok=true;c.hz.visible=false;c.ar.visible=false;S.regalos++;REP.pts+=100;repPop('🎁 ¡Regalo por la chimenea! '+S.regalos+'/'+S.chim.length+' · +100','gran');try{sonCaja();setTimeout(sonJoJo,150)}catch(e){}
    const gb=new THREE.Mesh(new THREE.BoxGeometry(.016,.016,.016),new THREE.MeshStandardMaterial({color:[0xd51f1f,0x1fae4a,0xf2c230,0x1f6fd0][S.regalos%4],emissive:0x333333}));gb.position.set(S.x,S.z+.08,S.y);scene.add(gb);const tg=c.g.position.clone();let k=0;const an=()=>{k+=.06;gb.position.lerp(tg.clone().setY(tg.y+.05+(1-k)*.08),.25);gb.rotation.y+=.3;if(k<1)requestAnimationFrame(an);else scene.remove(gb)};an();
    skObjetivo();if(S.regalos>=S.chim.length){skVueltaInicio();return}}}
  S.gpsT+=dt;if(S.gpsT>.5){S.gpsT=0;skObjetivo()}}
 skColoca(dt,tn)}
function skColoca(dt,tn){const S=SKT,sk=S.sk;P.x=S.x;P.y=S.y;P.a=S.a;P.v=0;sk.visible=S.cae<=0||S.cae>.6;sk.position.set(S.x,S.z,S.y);sk.rotation.set(0,S.a+S.spin,0);sk.userData.tb.rotation.x=S.flip;sk.userData.f.position.y=.0125+(S.air?0:Math.abs(Math.sin(tn*14))*.002*S.v);
 if(S.fl){const o=S.obj;S.fl.visible=!!o&&S.fase==='patina';if(o){S.fl.position.set(S.x,S.z+.13+Math.sin(tn*4)*.006,S.y);S.fl.rotation.set(0,Math.atan2(-(o.y-S.y),o.x-S.x),0)}}
 const dx=Math.cos(S.a),dz=-Math.sin(S.a),want=new THREE.Vector3(S.x-dx*.34,S.z+.2,S.y-dz*.34);{const hc=skAlt(want.x,want.z)[0];if(hc>want.y-.04)want.y=hc+.06}if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*5));look.set(S.x+dx*.22,S.z+.035,S.y+dz*.22);pcam.lookAt(look);pcam.fov=68+S.v*8;pcam.updateProjectionMatrix();
 FOG.near=5;FOG.far=20;const vv=document.getElementById('vel');vv.firstChild.nodeValue=S.regalos+'/'+S.chim.length;vv.querySelector('small').textContent='🎁 chimeneas · 🛹 skate';hudAccion(dt)}
// vuelta a la carroza: gran salto desde el tejado hasta ella
function skVueltaInicio(){const S=SKT;S.fase='vuelta';REP.dest=null;gpsParar();aviso('🎅 ¡Todas las chimeneas! De vuelta a la carroza',2.2,'cuenta');try{confeti()}catch(e){}
 const c=S.car,zc=groundY(c[0],c[1]);S.vu={t:0,x0:S.x,y0:S.y,z0:S.z,x1:c[0],y1:c[1],z1:zc+.02,a0:S.a,D:Math.max(1.6,Math.min(3,Math.hypot(c[0]-S.x,c[1]-S.y)*1.2))}}
function skVuelta(dt){const S=SKT,V=S.vu,tn=performance.now()/1000;V.t+=dt;const k=Math.min(1,V.t/V.D),e=k*k*(3-2*k);
 S.x=V.x0+(V.x1-V.x0)*e;S.y=V.y0+(V.y1-V.y0)*e;S.z=V.z0+(V.z1-V.z0)*e+Math.sin(Math.PI*k)*.45;S.a=Math.atan2(-(V.y1-V.y0),V.x1-V.x0)||S.a;S.spin=k*Math.PI*4;S.flip=0;S.air=true;skColoca(dt,tn);
 if(k>=1)skateSale(true)}
function skateSale(ok){const S=SKT;if(S.G){scene.remove(S.G);S.G=null}if(S.sk){scene.remove(S.sk);S.sk=null}if(S.hPrev!=null){CIELO.h=S.hPrev;CIELO.modo=S.mPrev||'auto';S.hPrev=null}S.on=false;S.fase='fin';S.fl=null;
 if(MODO==='skate'){cambiarModo('coche');if(S.car){P.x=S.car[0];P.y=S.car[1];P.a=S.car[2]}else repCocheCalle()}P.v=0;camInit=false;if(!ok)return;
 const pts=200+S.regalos*60;REP.pts+=pts;REP.ent++;REP.nEnt=(REP.nEnt||0)+1;try{sonJoJo();setTimeout(()=>sonPublico(1.3),400)}catch(e){}repPop('🛹 ¡Tejados completados! '+S.regalos+'/'+S.chim.length+' chimeneas · +'+pts+' ⭐','gran');
 const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;repSigue(ab,1600)}
"""+s[b:]
r("addEventListener('keydown',e=>{if(SKT.on&&MODO==='skate'&&e.code==='Space'){e.preventDefault();if(!e.repeat)skateSalta()}});",
  "addEventListener('keydown',e=>{if(SKT.on&&MODO==='skate'&&e.code==='Space'){e.preventDefault();if(!e.repeat)skateSalta()}});")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok skate2')
