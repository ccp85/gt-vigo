import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MISIÓN AL ATARDECER: «EL APAGÓN», EL VILLANO QUE QUIERE APAGAR LA NAVIDAD DE VIGO =================
# Personaje original: un villano gruñón con abrigo morado y capucha, que roba bombillas y huye en su furgoneta oscura.
# 1) Persecución por las avenidas (la furgoneta deja humo oscuro y bombillas robadas). 2) Al alcanzarlo, pelea arcade:
#    pulsa E / Ⓐ muy rápido para reducirlo y esquiva sus golpes con ◀ / ▶ cuando avise. 3) Llévalo al puerto, donde
#    espera la policía. Toda la misión transcurre al atardecer.
r("const esCasaK=k=>k===2||(k>12&&(k-13)%6===0);","const esCasaK=k=>k===2||(k>12&&(k-13)%6===0),esApaK=k=>false;")
r("function campMision(k){if(esCasaK(k))return{v:'coche',casa:true,txt:'🏠 Misión sigilo · el regalo bajo el árbol'};let c=0;for(let i=0;i<k;i++)if(esCasaK(i))c++;return campMisionB(k-c)}",
  "function campMision(k){if(esCasaK(k))return{v:'coche',casa:true,txt:'🏠 Misión sigilo · el regalo bajo el árbol'};if(esApaK(k))return{v:'coche',apagon:true,txt:'😈 Persigue al Apagón'};let c=0;for(let i=0;i<k;i++)if(esCasaK(i)||esApaK(i))c++;return campMisionB(k-c)}")
r("function buscarObjetivo(){objetivo=null;","function buscarObjetivo(){objetivo=null;if(APG.on&&APG.fase==='lucha'){objetivo={k:'apagon'};return '🥊 ¡Forcejea!'}")
r("function accion(){if(!driving)return;","function accion(){if(!driving)return;if(APG.on&&APG.fase==='lucha'){apagonGolpe();return}")
r("if(m.casa&&CASM.on){casaTick(dt||.016);return}","if(m.casa&&CASM.on){casaTick(dt||.016);return}if(m.apagon&&APG.on){apagonTick(dt||.016);return}")
r(" if(m.casa&&casaInicio(m,k))return;"," if(m.casa&&casaInicio(m,k))return;if(m.apagon&&apagonInicio(m,k))return;")
r('<button id="bSaltar"','<div id="lucha" hidden style="position:fixed;left:50%;top:22%;transform:translateX(-50%);z-index:40;width:min(340px,86vw);padding:12px 14px;border-radius:16px;background:rgba(20,14,34,.82);color:#fff;font:700 15px system-ui;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,.4)"><div>🥊 ¡Reduce al Apagón!</div><div style="height:12px;border-radius:6px;background:#5a2a3a;margin:10px 0 6px;overflow:hidden"><i style="display:block;height:100%;width:30%;background:linear-gradient(90deg,#3fd0ff,#7dffb0);border-radius:6px;transition:width .08s"></i></div><div class="t" style="font-size:13px;opacity:.9">Pulsa E / Ⓐ / acción muy rápido</div><div class="e" style="font-size:34px;height:40px;margin-top:4px"></div></div><button id="bSaltar"')
r("function repCocheCalle(){",r"""const APG={on:false};window.__APG=APG;
function mkApagon(){const g=new THREE.Group(),M=(c,r_=.7,e=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r_,emissive:e?c:0,emissiveIntensity:e});
 const add=(geo,mat,x,y,z,par=g)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);par.add(m);m.castShadow=true;return m};const AB=M(0x4a2f66),PI=M(0xd9c8e8),NE=M(0x1a1420);
 add(new THREE.CylinderGeometry(.012,.019,.05,12),AB,0,.035,0);add(new THREE.CylinderGeometry(.0195,.0195,.005,12),NE,0,.013,0);
 add(new THREE.SphereGeometry(.011,12,9),PI,.002,.071,0);add(new THREE.ConeGeometry(.004,.012,8),PI,.014,.07,0).rotation.z=-Math.PI/2;
 const ca=add(new THREE.SphereGeometry(.014,12,9,0,Math.PI*2,0,Math.PI*.6),AB,-.002,.072,0);ca.rotation.z=.5;add(new THREE.ConeGeometry(.007,.02,8),AB,-.014,.086,0).rotation.z=.9;
 for(const z of[.004,-.004]){add(new THREE.SphereGeometry(.0022,6,5),M(0xffe066,.3,1.5),.0105,.075,z);const ce=add(new THREE.BoxGeometry(.006,.0012,.002),NE,.011,.0795,z);ce.rotation.x=z>0?.5:-.5}
 const br=[];for(const z of[.017,-.017]){const pv=new THREE.Group();pv.position.set(0,.055,z);g.add(pv);add(new THREE.CylinderGeometry(.0035,.003,.03,8),AB,0,-.015,0,pv);add(new THREE.SphereGeometry(.0045,8,6),M(0x2a1a30),0,-.031,0,pv);br.push(pv)}
 const pi=[];for(const z of[.006,-.006]){const pv=new THREE.Group();pv.position.set(0,.02,z);g.add(pv);add(new THREE.CylinderGeometry(.0038,.0034,.02,8),NE,0,-.01,0,pv);add(new THREE.BoxGeometry(.012,.005,.007),NE,.003,-.02,0,pv);pi.push(pv)}
 const sa=add(new THREE.SphereGeometry(.017,10,8),M(0x6b5a44,.9),-.02,.06,0);sa.scale.set(1,1.15,1);for(let k=0;k<5;k++)add(new THREE.SphereGeometry(.004,6,5),M([0xff4040,0xffd24a,0x4aa8ff,0x3fe07a,0xff4fb0][k],.4,1.4),-.02+Math.cos(k)*.009,.08,Math.sin(k*2)*.009);
 g.userData={br,pi};return g}
function mkFurgoApagon(){const g=new THREE.Group(),M=(c,r_=.5,mt=.2,e=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r_,metalness:mt,emissive:e?c:0,emissiveIntensity:e});
 const bx=(w,h,d,x,y,z,m)=>{const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(x,y,z);o.castShadow=true;g.add(o);return o};
 bx(.12,.05,.058,-.01,.04,0,M(0x2a1838));bx(.04,.035,.056,.055,.032,0,M(0x2a1838));bx(.006,.022,.05,.075,.04,0,M(0x0a0a12,.1,.6));bx(.1,.004,.06,-.01,.067,0,M(0x3d2650));
 for(const[x,z]of[[.045,.03],[.045,-.03],[-.045,.03],[-.045,-.03]]){const w=new THREE.Mesh(new THREE.CylinderGeometry(.013,.013,.01,12),M(0x101014,.8,0));w.rotation.x=Math.PI/2;w.position.set(x,.013,z);g.add(w)}
 for(const z of[.02,-.02])bx(.003,.006,.01,.079,.03,z,M(0xff3040,.4,0,2));
 const sa=new THREE.Mesh(new THREE.SphereGeometry(.024,10,8),M(0x6b5a44,.9,0));sa.position.set(-.02,.085,0);sa.scale.set(1.3,.8,1);g.add(sa);for(let k=0;k<7;k++){const b=new THREE.Mesh(new THREE.SphereGeometry(.005,6,5),M([0xff4040,0xffd24a,0x4aa8ff,0x3fe07a][k%4],.4,0,1.6));b.position.set(-.02+Math.cos(k*.9)*.02,.098,Math.sin(k*.9)*.015);g.add(b)}
 return g}
function mkPolicia(){const g=new THREE.Group(),M=(c,r_=.4,e=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r_,emissive:e?c:0,emissiveIntensity:e});const bx=(w,h,d,x,y,z,m)=>{const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(x,y,z);g.add(o);return o};
 bx(.11,.03,.05,0,.025,0,M(0xf4f6fa));bx(.06,.025,.046,-.005,.05,0,M(0x1d2a6e));bx(.112,.008,.052,0,.03,0,M(0x1f4fd0));
 for(const[x,z]of[[.035,.026],[.035,-.026],[-.035,.026],[-.035,-.026]]){const w=new THREE.Mesh(new THREE.CylinderGeometry(.011,.011,.008,12),M(0x111111));w.rotation.x=Math.PI/2;w.position.set(x,.011,z);g.add(w)}
 const az=bx(.012,.006,.018,-.005,.066,.01,M(0x2a6bff,.3,2)),ro=bx(.012,.006,.018,-.005,.066,-.01,M(0xff2a2a,.3,2));g.userData={az,ro};return g}
// cima del Monte do Castro: el punto transitable más alto de la zona del parque
function apagonCima(){let best=null,bh=-1e9;for(let x=83.6;x<=87.2;x+=.05)for(let y=24.4;y<=28.2;y+=.05){const t=cell(x,y).t;if(!(t===1||t===2||t===4||t===5))continue;let ok=true;for(const[a,b]of[[.04,0],[-.04,0],[0,.04],[0,-.04]]){const q=cell(x+a,y+b).t;if(q===3||q===0||q===-1||q===6)ok=false}if(!ok)continue;const h=groundY(x,y);if(h>bh){bh=h;best=[x,y]}}return best||[85.6,26.3]}
function apagonInicio(m,k){const S=apagonCima();REP.mis=m;if(MODO!=='coche')repCocheCalle();
 Object.assign(APG,{on:true,fase:'espera',x:S[0],y:S[1],a:Math.atan2(-(P.y-S[1]),P.x-S[0]),path:null,pi:0,t:0,gt:0,hPrev:CIELO.h,humo:[],p:.3,ataque:0,prox:2.2,ok:0});REP.rad=Math.max(REP.rad||0,Math.hypot(S[0]-REP_DEP[1],S[1]-REP_DEP[2])+1.5);
 const gy=groundY(S[0],S[1]);APG.furgo=mkFurgoApagon();APG.furgo.position.set(S[0]-.09,gy,S[1]+.03);APG.furgo.rotation.y=APG.a;scene.add(APG.furgo);REP.objs.push(APG.furgo);
 const ap=mkApagon();ap.position.set(S[0],gy,S[1]);ap.rotation.y=APG.a;ap.scale.setScalar(1.4);scene.add(ap);REP.objs.push(ap);APG.esp=ap;
 const haz=new THREE.Mesh(new THREE.CylinderGeometry(.03,.06,2.4,12,1,true),new THREE.MeshBasicMaterial({color:0x9a4aff,transparent:true,opacity:.35,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,toneMapped:false}));haz.position.set(S[0],gy+1.2,S[1]);scene.add(haz);REP.objs.push(haz);APG.haz=haz;
 REP.fase='apagon';REP.dest=['😈 El Apagón · Monte do Castro',S[0],S[1]];REP.marca.visible=false;gpsIniciar(REP.dest);repHud();
 aviso('😈 Misión '+(k+1)+' · ¡El Apagón te reta!',2.4,'cuenta');setTimeout(()=>{if(APG.on&&APG.fase==='espera')mostrar('El Apagón te espera en lo alto del Monte do Castro, junto a su furgoneta morada: ¡sube a por él!')},2600);return true}
function apagonRuta(){const A=APG,pool=repPool().filter(d=>AV_MED.test(d[0])&&Math.hypot(d[1]-REP_DEP[1],d[2]-REP_DEP[2])<(REP.rad||12)-1);for(let q=0;q<8;q++){const d=pool[Math.floor(Math.random()*pool.length)];if(!d)break;const e=Math.hypot(d[1]-A.x,d[2]-A.y);if(e<2||e>7)continue;const pp=gpsCalcular(A.x,A.y,d[1],d[2]);if(pp&&pp.length>3){A.path=pp;A.pi=0;return}}A.path=null}
function apagonTick(dt){const A=APG;A.t+=dt;CIELO.h=19.15;const tn=performance.now()/1000;apagonRegTick(dt);
 if(A.fase==='regalos'){A.t2+=dt;P.v=0;const ap=A.ap;if(ap){const k=Math.min(1,A.t2/1.4);ap.rotation.y+=dt*(4+10*k);ap.scale.setScalar(Math.max(.01,1-k*.9));ap.position.y=A.gy+Math.sin(k*Math.PI)*.05}
  if(window.__CAMAP){const c=window.__CAMAP;c.p[1]+=dt*.05}if(A.t2>3)apagonLleva();return}
 if(A.fase==='espera'){const dP=Math.hypot(A.x-P.x,A.y-P.y),e=A.esp;if(e){e.rotation.y=Math.atan2(-(P.y-A.y),P.x-A.x);const k=Math.sin(tn*5);e.userData.br[0].rotation.z=-2.4+k*.4;e.userData.br[1].rotation.z=-2.4-k*.4;e.position.y=groundY(A.x,A.y)+Math.abs(Math.sin(tn*4))*.008}
  if(A.haz)A.haz.material.opacity=.25+.15*Math.sin(tn*3);A.gt-=dt;if(A.gt<=0){A.gt=2;gpsIniciar(REP.dest)}repHud();
  if(dP<.6&&!A.risa){A.risa=1;aviso('😈 «¡Ja, ja, ja! ¡Vigo se quedará a oscuras!»',2.2,'cuenta');try{bip(140,.5,.1)}catch(e){}}
  if(dP<.2){if(A.esp){scene.remove(A.esp);A.esp=null}if(A.haz){scene.remove(A.haz);A.haz=null}apagonLucha()}return}
 if(A.fase==='persigue'){const dP=Math.hypot(A.x-P.x,A.y-P.y);if(!A.path||A.pi>=A.path.length-1)apagonRuta();
  if(A.path){let v=(.55+.42*Math.min(1,dP/1.6))*dt;while(v>0&&A.pi<A.path.length-1){const q=A.path[A.pi+1],dx=q[0]-A.x,dy=q[1]-A.y,dd=Math.hypot(dx,dy);if(dd<=v){A.x=q[0];A.y=q[1];A.pi++;v-=dd}else{A.x+=dx/dd*v;A.y+=dy/dd*v;const an=Math.atan2(-dy,dx);let da=an-A.a;da=Math.atan2(Math.sin(da),Math.cos(da));A.a+=da*Math.min(1,dt*8);v=0}}}
  A.furgo.position.set(A.x,groundY(A.x,A.y),A.y);A.furgo.rotation.y=A.a;REP.dest=['😈 El Apagón',A.x,A.y];A.gt-=dt;if(A.gt<=0){A.gt=1.4;gpsIniciar(REP.dest)}repHud();
  // humo oscuro detrás de la furgoneta
  if(Math.random()<.5){const h=new THREE.Mesh(new THREE.SphereGeometry(.018,6,5),new THREE.MeshBasicMaterial({color:0x2a2030,transparent:true,opacity:.5,depthWrite:false}));h.position.set(A.x-Math.cos(A.a)*.07,groundY(A.x,A.y)+.03,A.y+Math.sin(A.a)*.07);scene.add(h);A.humo.push({h,t:0})}
  for(let i=A.humo.length-1;i>=0;i--){const q=A.humo[i];q.t+=dt;q.h.scale.setScalar(1+q.t*2.5);q.h.position.y+=dt*.03;q.h.material.opacity=.5*(1-q.t/1.4);if(q.t>1.4){scene.remove(q.h);A.humo.splice(i,1)}}
  if(dP<.14)apagonLucha();else if(dP>6&&(!A.avL||tn-A.avL>6)){A.avL=tn;mostrar('¡Que se escapa! Sigue el GPS hasta la furgoneta morada')}return}
 if(A.fase==='lucha'){P.v=0;const U=document.getElementById('lucha');if(A.p>=1){apagonGana();return}A.p=Math.max(0,A.p-dt*.11);
  // golpes del Apagón: avisa con una flecha y hay que esquivar hacia ese lado
  if(!A.ataque){A.prox-=dt;if(A.prox<=0){A.ataque=Math.random()<.5?'izq':'der';A.ventana=.95;A.ok=0;U.querySelector('.e').textContent=A.ataque==='izq'?'⬅️ ¡Esquiva!':'¡Esquiva! ➡️';try{bip(500,.08,.06)}catch(e){}}}
  else{A.ventana-=dt;const bien=A.ataque==='izq'?keys.left:keys.right,mal=A.ataque==='izq'?keys.right:keys.left;
   if(bien){A.p=Math.min(1,A.p+.12);if(A.p>=1){apagonGana();return}A.ataque=0;A.prox=1.6+Math.random()*1.4;U.querySelector('.e').textContent='👌';repPop('¡Esquivado!','aviso')}
   else if(mal||A.ventana<=0){A.p=Math.max(0,A.p-.22);A.ataque=0;A.prox=1.8+Math.random()*1.4;U.querySelector('.e').textContent='💥';REP.shake=.4;try{bip(180,.2,.1)}catch(e){}padVibra(.6,.6,200)}}
  U.querySelector('i').style.width=(A.p*100).toFixed(0)+'%';
  // animación de la pelea
  const yo=A.yo,ap=A.ap,k=Math.sin(tn*14);ap.userData.br[0].rotation.z=A.ataque?-1.6+Math.sin(tn*20)*.3:k*.5;ap.userData.br[1].rotation.z=A.ataque?-.4:-k*.5;yo.userData.br[0].rotation.z=1.2+Math.max(0,Math.sin(tn*18))*.8;yo.userData.br[1].rotation.z=1.2+Math.max(0,-Math.sin(tn*18))*.8;
  ap.position.y=A.gy+Math.abs(Math.sin(tn*9))*.006;yo.position.y=A.gy+Math.abs(Math.sin(tn*9+1))*.006;
  const mx=(yo.position.x+ap.position.x)/2,mz=(yo.position.z+ap.position.z)/2,nx=-Math.sin(A.fa),nz=-Math.cos(A.fa);window.__CAMAP={p:[mx+nx*.26,A.gy+.12,mz+nz*.26],l:[mx,A.gy+.05,mz]};
  if(A.p>=1)apagonGana();return}
 if(A.fase==='lleva'){const dd=Math.hypot(A.pol[0]-P.x,A.pol[1]-P.y);const pc=A.poli;pc.userData.az.material.emissiveIntensity=Math.sin(tn*12)>0?3:.2;pc.userData.ro.material.emissiveIntensity=Math.sin(tn*12)>0?.2:3;
  if(dd<.3){A.fase='entrega';A.t=0;P.v=0;const ap=mkApagon();ap.position.set(A.pol[0]+.06,groundY(A.pol[0],A.pol[1]),A.pol[1]+.05);ap.rotation.y=Math.PI;scene.add(ap);REP.objs.push(ap);A.ap2=ap;aviso('🚓 ¡La policía se lleva al Apagón!',2.6,'cuenta');try{sonPublico(1.2);sonJoJo()}catch(e){}}return}
 if(A.fase==='entrega'){P.v=0;const pc=A.poli;pc.userData.az.material.emissiveIntensity=Math.sin(tn*12)>0?3:.2;pc.userData.ro.material.emissiveIntensity=Math.sin(tn*12)>0?.2:3;if(A.ap2&&A.t>1){A.ap2.position.lerp(pc.position,dt*1.5)}if(A.t>1.6&&A.ap2){scene.remove(A.ap2);A.ap2=null}
  if(A.t>2.6){pc.position.x+=Math.cos(pc.rotation.y)*dt*.6;pc.position.z-=Math.sin(pc.rotation.y)*dt*.6}if(A.t>4)apagonFin()}}
function apagonLucha(){const A=APG;A.fase='lucha';P.v=0;gpsParar();REP.dest=null;A.gy=groundY(P.x,P.y);A.fa=P.a;
 const yo=figNav(REP.spec||{t:'sleigh',col:[0xc4161f]}),ap=mkApagon();const fx=Math.cos(P.a),fz=-Math.sin(P.a),sx=-fz,sz=fx;
 yo.position.set(P.x+sx*.07+fx*.02,A.gy,P.y+sz*.07+fz*.02);ap.position.set(P.x+sx*.07+fx*.1,A.gy,P.y+sz*.07+fz*.1);yo.rotation.y=P.a;ap.rotation.y=P.a+Math.PI;scene.add(yo);scene.add(ap);A.yo=yo;A.ap=ap;

 if(!R.userData)R.userData={};if(!R.userData.camo){R.userData.camo=1;const r0=R.render.bind(R);R.render=(sc,c)=>{const O=window.__CAMAP;if(O&&c===pcam){c.up.set(0,1,0);c.position.set(...O.p);c.lookAt(...O.l);c.fov=55;c.updateProjectionMatrix();c.updateMatrixWorld()}return r0(sc,c)}}
 A.p=.3;A.prox=2;A.ataque=0;const U=document.getElementById('lucha');U.hidden=false;U.querySelector('.e').textContent='';try{bip(300,.2,.1);setTimeout(()=>bip(450,.2,.1),150)}catch(e){}aviso('🥊 ¡Lo tienes! ¡A por él!',1.6,'cuenta')}
function apagonGolpe(){const A=APG;if(A.fase!=='lucha')return;A.p=Math.min(1,A.p+.055);if(A.p>=1){apagonGana();return}try{bip(700+Math.random()*200,.04,.03)}catch(e){}}
// al derrotarlo, del saco del Apagón salen disparados todos los regalos que había robado
function apagonGana(){const A=APG;if(A.fase!=='lucha')return;A.fase='regalos';A.t2=0;document.getElementById('lucha').hidden=true;
 const o=A.ap.position,CR=[0xd51f1f,0x1fae4a,0xf2c230,0x1f6fd0,0xc23fd0,0xff7a1a,0xf6f6f2,0x35e0ff],MT=CR.map(c=>new THREE.MeshStandardMaterial({color:c,roughness:.5,emissive:c,emissiveIntensity:.25})),OR=new THREE.MeshStandardMaterial({color:0xffd24a,roughness:.35,emissive:0x8a6000,emissiveIntensity:.5});
 A.reg=[];for(let k=0;k<42;k++){const sz=.012+Math.random()*.014,g=new THREE.Group(),b=new THREE.Mesh(new THREE.BoxGeometry(sz,sz,sz),MT[k%MT.length]);g.add(b);const c1=new THREE.Mesh(new THREE.BoxGeometry(sz*1.04,sz*1.04,sz*.22),OR),c2=new THREE.Mesh(new THREE.BoxGeometry(sz*.22,sz*1.04,sz*1.04),OR);g.add(c1,c2);
  g.position.set(o.x,o.y+.07,o.z);scene.add(g);const an=Math.random()*6.283,sp=.15+Math.random()*.35;A.reg.push({g,vx:Math.cos(an)*sp,vz:Math.sin(an)*sp,vy:.45+Math.random()*.55,rx:(Math.random()-.5)*12,ry:(Math.random()-.5)*12,t:0,h:sz/2})}
 try{sonCaja();setTimeout(sonJoJo,200);setTimeout(()=>sonPublico(1.3),500);bip(880,.15,.07);setTimeout(()=>bip(1320,.2,.06),120)}catch(e){}REP.shake=.5;padVibra(.8,.8,350);aviso('🎁 ¡Los regalos robados vuelven a Vigo!',2.6,'cuenta');REP.pts+=150;repPop('🎁 42 regalos recuperados · +150 ⭐','gran')}
function apagonRegTick(dt){const A=APG;if(!A.reg)return;for(let i=A.reg.length-1;i>=0;i--){const q=A.reg[i];q.t+=dt;const p=q.g.position;q.vy-=1.6*dt;p.x+=q.vx*dt;p.z+=q.vz*dt;p.y+=q.vy*dt;const gy=groundY(p.x,p.z)+q.h;
  if(p.y<gy){p.y=gy;if(Math.abs(q.vy)>.08){q.vy*=-.38;q.vx*=.6;q.vz*=.6}else{q.vy=0;q.vx*=.85;q.vz*=.85;q.rx*=.8;q.ry*=.8}}q.g.rotation.x+=q.rx*dt;q.g.rotation.y+=q.ry*dt;
  if(q.t>9){q.g.scale.multiplyScalar(.9);if(q.t>9.6){scene.remove(q.g);A.reg.splice(i,1)}}}}
function apagonLleva(){const A=APG;A.fase='lleva';window.__CAMAP=null;camInit=false;scene.remove(A.yo);scene.remove(A.ap);A.yo=A.ap=null;scene.remove(A.furgo);
 REP.pts+=200;repPop('🪢 ¡Atrapado! +200 ⭐','gran');try{sonCaja();setTimeout(sonJoJo,200)}catch(e){}
 const pu=aguaCerca(89.5,10.83)||[89.5,10.83];let b=null,bd=1e9;for(const q of repPool()){const e=Math.hypot(q[1]-pu[0],q[2]-pu[1]);if(e<bd){bd=e;b=q}}A.pol=b?[b[1],b[2]]:[REP_DEP[1],REP_DEP[2]];
 const pc=mkPolicia();pc.position.set(A.pol[0],groundY(A.pol[0],A.pol[1]),A.pol[1]);pc.rotation.y=b?Math.atan2(-b[4],b[3]):0;scene.add(pc);REP.objs.push(pc);A.poli=pc;
 campDestino(['🚓 Policía · Puerto de Vigo',A.pol[0],A.pol[1]]);REP.fase='apagon';setTimeout(()=>{if(APG.on)mostrar('Llévalo al Puerto de Vigo: allí espera la policía')},900)}
function apagonFin(){const A=APG;A.on=false;for(const q of A.reg||[])scene.remove(q.g);A.reg=null;CIELO.h=A.hPrev;for(const q of A.humo||[])scene.remove(q.h);A.humo=[];if(A.poli){scene.remove(A.poli);A.poli=null}window.__CAMAP=null;
 const pts=350;REP.pts+=pts;REP.ent++;REP.nEnt=(REP.nEnt||0)+1;repPop('😈 ¡La Navidad de Vigo está a salvo! +'+pts+' ⭐','gran');const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;repSigue(ab,1400)}
function repCocheCalle(){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok apagon')
