// ---- palas en la playa (edit_palas.py) ----
// Con sol, al ir a pie por una playa aparece cerca una chica en bikini dando toques con su pala. Acércate y pulsa E / el botón
// para jugar: la bola va y viene; muévete a los lados (◀ ▶) hasta el aro verde y golpea (E / botón) justo cuando llegue.
// Cuantos más toques seguidos, más rápido. Golpe perfecto = bola más rápida. ▼ para dejar de jugar. Con lluvia o de noche se va.
const PAL={on:false,chica:null,gx:0,gz:0,ga:0,sG:0,sP:0,ux:1,uz:0,wx:0,wz:1,bola:null,sombra:null,aro:null,palaJ:null,
 fase:'',t:0,dur:1,h:.06,de:null,sT:0,quien:'',toques:0,rec:+(localStorage.getItem('gtv_palas_rec')||0),swJ:9,swC:9,busca:0,baja:0,hud:null,fallo:0,perf:false,miss:0};
window.PAL=PAL;
function mkPala(){const g=new THREE.Group(),M=(c,r)=>new THREE.MeshStandardMaterial({color:c,roughness:r});
 const mango=new THREE.Mesh(new THREE.CylinderGeometry(.0012,.0012,.008,8),M(0x1d1c22,.6));mango.position.y=-.0155;g.add(mango);
 const hoja=new THREE.Mesh(new THREE.CylinderGeometry(.0078,.0078,.0011,20),M(0xc98b4b,.7));hoja.rotation.z=Math.PI/2;hoja.scale.set(1,1,.86);hoja.position.y=-.0255;g.add(hoja);
 const borde=new THREE.Mesh(new THREE.TorusGeometry(.0078,.0006,6,20),M(0x2b8fd6,.5));borde.rotation.y=Math.PI/2;borde.scale.set(1,.86,1);borde.position.y=-.0255;g.add(borde);
 g.traverse(o=>{if(o.isMesh)o.castShadow=true});return g}
// la chica: muñeca cartoon propia (misma articulación que el protagonista para andar y golpear), figura de reloj de arena,
// bikini de triángulo con tiras, chanclas, pelo largo suelto o coleta, pestañas, labios y colorete; a veces gafas de sol en la cabeza
function mkChica(){const g=new THREE.Group(),R=a=>a[(Math.random()*a.length)|0];
 const piel=new THREE.Color(R(PIEL_C)),bik=R(BANO_C),pc=R([0x2a1d16,0x3a2a20,0x6b4a2a,0xc9a15a,0x8a3a22,0xe0c27a,0x15171c]),pelo=new THREE.Color(pc);
 const MC={},M=(c,r=.55,x={})=>{const k=new THREE.Color(c).getHex()+'|'+r+'|'+JSON.stringify(x);return MC[k]||(MC[k]=new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:r,metalness:0},x)))};
 const mP=M(piel,.5),mB=M(bik,.42),mH=M(pelo,.65),mC=M(R([0xff7aa8,0xf2c230,0x14a3a3,0xffffff,0x1d4fa8]),.6),mN=M(0x1a1412,.4);
 const add=(par,geo,mat,x=0,y=0,z=0,rx=0,ry=0,rz=0,sx=1,sy=1,sz=1)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.rotation.set(rx,ry,rz);m.scale.set(sx,sy,sz);par.add(m);return m};
 const CAP=(r,l,s=12)=>new THREE.CapsuleGeometry(r,l,4,s),ESF=(r,a=16,b=12)=>new THREE.SphereGeometry(r,a,b),CIL=(a,b,h,s=14)=>new THREE.CylinderGeometry(a,b,h,s);
 const palo=(par,a,b,r,mat)=>{const A=new THREE.Vector3(...a),d=new THREE.Vector3(...b).sub(A),L=d.length();const m=add(par,CIL(r,r,L,6),mat);m.position.copy(A).addScaledVector(d,.5);m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());return m};
 // ---- piernas largas: muslo, rodilla, pantorrilla y pie con chancla
 const piernas=new THREE.Group();piernas.position.y=.033;g.add(piernas);
 for(const z of[-.0043,.0043]){const pv=new THREE.Group();pv.position.z=z;piernas.add(pv);
  add(pv,CAP(.0045,.0082),mP,0,-.0068,0,0,0,0,.95,1,1);
  const rod=new THREE.Group();rod.position.y=-.0152;pv.add(rod);pv.userData.rod=rod;
  add(rod,ESF(.0032,12,8),mP,0,0,0);
  add(rod,CAP(.0031,.0092),mP,0,-.0064,0);
  add(rod,ESF(.0031,12,8),mP,-.0007,-.0045,0,0,0,0,.9,1.35,.95);   // gemelo
  const pie=new THREE.Group();pie.position.y=-.0161;rod.add(pie);
  add(pie,CAP(.0017,.0056,10),mP,.0021,-.0006,0,0,0,Math.PI/2,1,1,1.05);
  add(pie,new THREE.BoxGeometry(.0102,.0009,.0045),mC,.0021,-.0019,0);
  palo(pie,[.0042,-.0014,0],[.0006,.0002,z<0?-.0019:.0019],.00045,mC)}
 g.userData.piernas=piernas;
 // ---- tronco: cadera ancha, cintura estrecha, pecho y hombros finos
 const T0=.033,tronco=new THREE.Group();tronco.position.y=T0;g.add(tronco);g.userData.tronco=tronco;
 add(tronco,ESF(.0088,20,14),mP,0,.0012,0,0,0,0,.7,.62,1);
 const perfil=[[.0001,.0006],[.0083,.0006],[.0088,.0035],[.0072,.0085],[.0064,.0115],[.0068,.014],[.0079,.0175],[.0084,.0205],[.0079,.024],[.0058,.0268],[.003,.0284],[.0001,.0288]].map(([r,y])=>new THREE.Vector2(r,y));
 add(tronco,new THREE.LatheGeometry(perfil,24),mP,0,0,0,0,0,0,.64,1,1);
 // braguita de bikini con lazos a los lados
 add(tronco,new THREE.SphereGeometry(.0091,22,10,0,Math.PI*2,Math.PI*.42,Math.PI*.58),mB,.0001,.0012,0,0,0,0,.72,.66,1.03);
 for(const s of[-1,1]){add(tronco,ESF(.0011,8,6),mB,0,.0026,s*.009);palo(tronco,[0,.0026,s*.009],[.0008,-.0004,s*.0096],.0004,mB)}
 // parte de arriba: dos triángulos (copas), banda y tiras al cuello
 for(const s of[-1,1]){add(tronco,ESF(.0036,14,10),mB,.0039,.0182,s*.0037,0,s*.15,0,.72,.92,.98);
  palo(tronco,[.0057,.0203,s*.0037],[.0053,.0241,s*.0032],.00042,mB);palo(tronco,[.0053,.0241,s*.0032],[.0031,.0279,s*.0025],.00042,mB)}
 add(tronco,new THREE.TorusGeometry(.0077,.00055,6,24),mB,0,.0158,0,Math.PI/2,0,0,.66,1,1);
 // ---- brazos finos: hombro, codo, mano
 const brazos=new THREE.Group();tronco.add(brazos);
 for(const z of[-.0104,.0104]){const b=new THREE.Group();b.position.set(-.0004,.0238,z);b.rotation.x=z<0?.1:-.1;brazos.add(b);
  add(b,ESF(.0031,14,10),mP,0,-.0002,0);
  add(b,CAP(.0024,.0068),mP,0,-.0048,0);
  const codo=new THREE.Group();codo.position.y=-.0104;b.add(codo);b.userData.codo=codo;
  add(codo,CAP(.0021,.0064),mP,0,-.0043,0);
  add(codo,ESF(.0024,12,8),mP,.0002,-.0104,0,0,0,0,.8,1.15,.72);
  add(codo,ESF(.001,8,6),mP,.0021,-.0094,z<0?.001:-.001)}
 g.userData.brazos=brazos;
 // ---- cuello y cabeza
 add(tronco,CIL(.0023,.0027,.0055,12),mP,0,.0293,0);
 const cab=new THREE.Group();cab.position.y=.0315;tronco.add(cab);g.userData.cabeza=cab;const H=.0088;
 add(cab,ESF(.0088,24,18),mP,0,H,0,0,0,0,.95,1.04,.92);
 add(cab,ESF(.0052,16,10),mP,.0034,H-.0045,0,0,0,0,.9,.7,1.05);       // barbilla suave
 // cara: ojos grandes (blanco, iris de color, pupila, brillo, párpado con pestañas), cejas, colorete, orejas, nariz y boca sonriente
 const mIr=M(R([0x5a3a22,0x3d6b3a,0x3a6aa8,0x7a5a2a]),.3),mBl=M(0xfbfbf8,.3);
 for(const s of[-1,1]){const z=s*.0033;
  add(cab,ESF(.002,14,10),mBl,.0074,H+.0008,z,0,0,0,.45,1.15,1);                          // blanco del ojo
  add(cab,ESF(.00125,12,8),mIr,.0082,H+.0006,z,0,0,0,.42,1.1,1);                          // iris
  add(cab,ESF(.00065,10,6),mN,.00865,H+.0006,z,0,0,0,.4,1,1);                             // pupila
  add(cab,ESF(.00032,6,4),mBl,.0089,H+.0011,z+s*.0003);                                    // brillo
  add(cab,ESF(.0021,14,8),mP,.0072,H+.0017,z,0,0,0,.5,.55,1.02);                          // párpado
  add(cab,new THREE.BoxGeometry(.0005,.0006,.0036),mN,.0082,H+.0022,z,s*.08,0,0);          // línea de pestañas
  add(cab,new THREE.BoxGeometry(.0004,.0011,.0007),mN,.0079,H+.0026,z+s*.0019,s*.6,0,0);   // pestaña de fuera
  add(cab,CAP(.00035,.0026,6),M(new THREE.Color(pc).multiplyScalar(.8),.7),.0081,H+.0044,z,Math.PI/2+s*.15,0,0);   // ceja
  add(cab,ESF(.0016,10,8),M(0xf08a8a,.6,{transparent:true,opacity:.45}),.0073,H-.0018,s*.0052,0,0,0,.4,.8,1);   // colorete
  add(cab,ESF(.0018,10,8),mP,-.0004,H,s*.0086,0,0,0,.6,.95,.45)}                           // oreja
 add(cab,ESF(.0009,8,6),mP,.0089,H-.0012,0,0,0,0,1,.8,.9);                                  // nariz
 const mL=M(0xc8404f,.35);
 add(cab,ESF(.0014,12,8),mL,.0082,H-.0035,0,0,0,0,.55,.4,1.7);                             // labio de arriba
 add(cab,ESF(.0013,12,8),mL,.0081,H-.0045,0,0,0,0,.6,.5,1.45);                             // labio de abajo
 add(cab,new THREE.TorusGeometry(.0021,.00025,6,14,Math.PI*.8),M(0x5a1a20,.5),.00845,H-.0034,0,0,Math.PI/2,Math.PI*1.1,1,1,.45);   // sonrisa
 for(const s of[-1,1])add(cab,ESF(.0004,6,4),M(0x8a2a30,.5),.0082,H-.0036,s*.0024);         // comisuras
 // pelo: casquete, flequillo y melena suelta o coleta
 add(cab,new THREE.SphereGeometry(.0092,26,14,0,Math.PI*2,0,Math.PI*.62),mH,-.0004,H+.0002,0,0,0,.8,.97,1.05,.97);
 add(cab,ESF(.006,14,10),mH,.0052,H+.0058,.0016,0,0,-.35,.55,.45,1.45);
 if(Math.random()<.55){add(cab,CAP(.0068,.0145,14),mH,-.0058,H-.0105,0,0,0,.1,.55,1,1.2);
  for(const s of[-1,1])add(cab,CAP(.0021,.0115,8),mH,-.0016,H-.0062,s*.0089,s*.1,0,.1)}
 else{add(cab,ESF(.0094,16,10),mH,-.0032,H-.0012,0,0,0,0,.72,.82,1.02);add(cab,CAP(.0034,.0115,10),mH,-.0124,H-.0045,0,0,0,-.35);
  add(cab,new THREE.TorusGeometry(.0029,.0008,6,12),mC,-.0108,H+.0024,0,0,Math.PI/2,-.35+Math.PI/2)}
 if(Math.random()<.4){const mG=M(0x15171c,.2,{metalness:.4});for(const s of[-1,1])add(cab,ESF(.0024,12,8),mG,.0036,H+.0086,s*.0032,0,0,-.5,.4,1,1);add(cab,CAP(.0004,.003,6),mG,.0043,H+.0089,0,Math.PI/2)}
 const pala=mkPala();brazos.children[1].userData.codo.add(pala);g.userData.pala=pala;
 g.traverse(o=>{if(o.isMesh)o.castShadow=true});g.scale.setScalar(.76);g.name='chica_palas';return g}
function palasObjetos(){if(PAL.bola)return;
 PAL.bola=new THREE.Mesh(new THREE.SphereGeometry(.0034,12,8),new THREE.MeshStandardMaterial({color:0xf2e14a,roughness:.4,emissive:0x2a2400}));PAL.bola.castShadow=true;scene.add(PAL.bola);
 PAL.sombra=new THREE.Mesh(new THREE.CircleGeometry(.004,12),new THREE.MeshBasicMaterial({color:0x1d1c33,transparent:true,opacity:.3,depthWrite:false}));PAL.sombra.rotation.x=-Math.PI/2;PAL.sombra.renderOrder=3;scene.add(PAL.sombra);
 PAL.aro=new THREE.Mesh(new THREE.RingGeometry(.013,.017,28),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.8,depthWrite:false,side:THREE.DoubleSide}));PAL.aro.rotation.x=-Math.PI/2;PAL.aro.renderOrder=3;scene.add(PAL.aro);
 PAL.palaJ=mkPala();PAL.palaJ.visible=false;persona.userData.brazos.children[1].userData.codo.add(PAL.palaJ);
 const d=document.createElement('div');d.id='palasHud';d.hidden=true;d.style.cssText='position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 58px);transform:translateX(-50%);z-index:30;background:rgba(20,22,40,.78);color:#fff;font:600 14px/1.35 system-ui,sans-serif;padding:7px 14px;border-radius:14px;text-align:center;pointer-events:none;white-space:nowrap';document.body.appendChild(d);PAL.hud=d}
// sitio en la arena cerca del jugador, con hueco para jugar (sin grupos de bañistas ni agua)
function palasSitio(){let best=null,bd=9;
 const roots=new Set();for(const c of PLY.L)if(c.root.parent&&c.root.userData.pickPlaya)roots.add(c.root);
 for(const r of roots){const pick=r.userData.pickPlaya,S=r.userData.sitiosPlaya||[];
  for(let k=0;k<30;k++){const p=pick(),d=Math.hypot(p.x-P.x,p.z-P.y);if(d<.3||d>1.3||d>bd)continue;
   const ux=P.x-p.x,uz=P.y-p.z,ul=Math.hypot(ux,uz)||1,a=Math.atan2(uz/ul,ux/ul)+(Math.random()-.5)*1.2,qx=p.x+Math.cos(a)*.17,qz=p.z+Math.sin(a)*.17;
   let ok=true;for(let i=0;i<=6&&ok;i++){const x=p.x+(qx-p.x)*i/6,z=p.z+(qz-p.z)*i/6;for(const [ox,oz] of [[0,0],[.04,0],[-.04,0],[0,.04],[0,-.04]]){if(cell(x+ox,z+oz).t!==1){ok=false;break}}}
   if(ok)for(const s of S)if(Math.hypot(s.x-p.x,s.z-p.z)<.09||Math.hypot(s.x-qx,s.z-qz)<.09){ok=false;break}
   if(ok){bd=d;best={x:p.x,z:p.z,a}}}}
 return best}
function palasPonChica(s){if(PAL.chica){PAL.chica.parent&&PAL.chica.parent.remove(PAL.chica)}palasObjetos();const c=mkChica();scene.add(c);PAL.chica=c;PAL.gx=s.x;PAL.gz=s.z;PAL.ga=s.a;PAL.sG=0;PAL.fase='sola';PAL.t=0;PAL.vis=true}
function palasCerca(){return !PAL.on&&!!PAL.chica&&PAL.chica.visible&&driving&&MODO==='pie'&&Math.hypot(PAL.chica.position.x-P.x,PAL.chica.position.z-P.y)<.13}
function palasTxt(){return palasCerca()?'🏓 Jugar a las palas con ella':null}
function palasEje(){const ux=Math.cos(PAL.ga),uz=Math.sin(PAL.ga);PAL.ux=ux;PAL.uz=uz;PAL.wx=-uz;PAL.wz=ux}   // u: de la chica al jugador · w: lateral
function palasEmpieza(){palasEje();PAL.on=true;PAL.sP=0;PAL.sG=0;PAL.toques=0;PAL.palaJ.visible=true;PAL.hud.hidden=false;palasSaca();padVibra&&padVibra(.1,0,60);mostrar('¡Vamos! Muévete al aro verde y golpea cuando llegue la bola')}
function palasFin(msg){PAL.on=false;PAL.palaJ.visible=false;PAL.hud.hidden=true;PAL.aro.visible=false;PAL.fase='sola';PAL.t=0;if(msg)mostrar(msg)}
function palasSaca(){PAL.quien='chica';PAL.fase='vuelo';PAL.t=0;PAL.perf=false;PAL.dur=1.25;palasTiro()}
// lanza la bola del que golpea al otro; elige dónde caerá (a los lados, más cuanto más larga la racha)
function palasTiro(){const amp=.012+Math.min(.032,PAL.toques*.0025),sT=(Math.random()*2-1)*amp;PAL.sT=sT;PAL.h=.035+Math.random()*.03;PAL.t=0;PAL.fase='vuelo';PAL.miss=0}
function palasPos(lado,s,y){const b=lado==='jug'?.17:0;return [PAL.gx+PAL.ux*b+PAL.wx*s,y,PAL.gz+PAL.uz*b+PAL.wz*s]}
function palasSonido(f){try{const a=window.__acPal||(window.__acPal=new (window.AudioContext||window.webkitAudioContext)());if(a.state==='suspended')a.resume();const t=a.currentTime,o=a.createOscillator(),g=a.createGain();o.type='triangle';o.frequency.setValueAtTime(f,t);o.frequency.exponentialRampToValueAtTime(f*.5,t+.08);g.gain.setValueAtTime(.25,t);g.gain.exponentialRampToValueAtTime(.001,t+.12);o.connect(g);g.connect(a.destination);o.start(t);o.stop(t+.13)}catch(e){}}
function palasGolpe(){PAL.swJ=0;if(PAL.fase!=='vuelo'||PAL.quien!=='chica')return;
 const err=(PAL.t-1)*PAL.dur,lat=Math.abs(PAL.sP-PAL.sT);
 if(err<-.17){PAL.miss=1;return}                                   // demasiado pronto (aún puedes volver a darle)
 if(Math.abs(err)<=.17&&lat<.022){PAL.toques++;PAL.perf=Math.abs(err)<.055;palasSonido(PAL.perf?880:660);padVibra&&padVibra(.25,.1,50);
  if(PAL.toques>PAL.rec){PAL.rec=PAL.toques;try{localStorage.setItem('gtv_palas_rec',PAL.rec)}catch(e){}}
  mostrar(PAL.perf?'¡Perfecto! · '+PAL.toques:'¡Toque! · '+PAL.toques);PAL.quien='jug';PAL.dur=Math.max(.5,1.15-PAL.toques*.03)*(PAL.perf?.82:1);palasTiro()}}
function palasTick(dt){const fSol=PLY.f==null?1:PLY.f;
 if(!driving||RACE.on||REP.on||MODO!=='pie'){if(PAL.on)palasFin();if(PAL.chica)PAL.chica.visible=false;if(PAL.bola){PAL.bola.visible=PAL.sombra.visible=PAL.aro.visible=false}return}
 if(PAL.on&&fSol<.3){palasFin(TIEMPO.W.rain>.1?'Empieza a llover: ¡otro día seguís con las palas!':'Se hace de noche: ¡mañana más palas!')}
 // aparece la chica si hace sol y estás cerca de una playa
 PAL.busca-=dt;if(!PAL.on&&PAL.busca<=0){PAL.busca=1;const lejos=!PAL.chica||!PAL.chica.visible||Math.hypot(PAL.chica.position.x-P.x,PAL.chica.position.z-P.y)>2.2;
  if(fSol>=.5&&lejos){const s=palasSitio();if(s)palasPonChica(s);else PAL.vis=false}}
 if(!PAL.chica)return;
 const C=PAL.chica,tn=performance.now()/1000;palasEje();
 if(!PAL.on){// sola: da toquecitos hacia arriba
  C.visible=PAL.vis&&fSol>=.5;if(!C.visible){PAL.bola.visible=PAL.sombra.visible=PAL.aro.visible=false;return}
  const gy=groundY(PAL.gx,PAL.gz);C.position.set(PAL.gx,gy,PAL.gz);C.rotation.y=Math.atan2(-PAL.uz,PAL.ux)+Math.sin(tn*.6)*.6;animPersona(C,tn,0);palasBrazo(C,tn,(tn*1.6)%1<.15?((tn*1.6)%1)/.15:9,1);
  const k=(tn*1.6)%1,hb=gy+.04+4*k*(1-k)*.035;const fx=Math.cos(C.rotation.y),fz=-Math.sin(C.rotation.y);PAL.bola.visible=PAL.sombra.visible=true;PAL.bola.position.set(PAL.gx+fx*.012,hb,PAL.gz+fz*.012);PAL.sombra.position.set(PAL.bola.position.x,gy+.0015,PAL.bola.position.z);PAL.aro.visible=false;return}
 // jugando
 const izq=keys.left,der=keys.right;PAL.sP=Math.max(-.07,Math.min(.07,PAL.sP+((izq?1:0)-(der?1:0))*.16*dt));
 if(keys.down){PAL.baja+=dt;if(PAL.baja>.35){PAL.baja=0;palasFin('Has dejado las palas · récord: '+PAL.rec+' toques');return}}else PAL.baja=0;
 if(keys.up&&!PAL.fallo){PAL.sube=(PAL.sube||0)+dt;if(PAL.sube>.6){PAL.sube=0;palasFin('Has dejado las palas · récord: '+PAL.rec+' toques');return}}else PAL.sube=0;
 const [jx,,jz]=palasPos('jug',PAL.sP,0);P.x=jx;P.y=jz;P.v=0;P.a=Math.atan2(PAL.uz,-PAL.ux);P.vuelta=0;persona.position.x=jx;persona.position.z=jz;persona.rotation.y=P.a;
 const mv=Math.abs((der?1:0)-(izq?1:0));animPersona(persona,tn,mv*.5);PAL.swJ+=dt;palasBrazo(persona,tn,PAL.swJ/.22,0);
 // la chica corre de lado hacia donde va la bola
 if(PAL.fase==='vuelo'&&PAL.quien==='jug'){const d=PAL.sT-PAL.sG;PAL.sG+=Math.sign(d)*Math.min(Math.abs(d),.2*dt)}
 const [cx,,cz]=palasPos('chica',PAL.sG,0),gy=groundY(cx,cz);C.visible=true;C.position.set(cx,gy,cz);C.rotation.y=Math.atan2(-PAL.uz,PAL.ux);animPersona(C,tn,PAL.fase==='vuelo'&&PAL.quien==='jug'?.5:0);PAL.swC+=dt;palasBrazo(C,tn,PAL.swC/.22,0);
 PAL.hud.textContent='🏓 Toques: '+PAL.toques+' · Récord: '+PAL.rec+(matchMedia('(pointer:coarse)').matches?' · ◀ ▶ moverte · Golpe · ▼ dejar':' · ◀ ▶ moverte · E golpear · ▼ dejar');
 if(PAL.fase==='fallo'){PAL.t+=dt;PAL.aro.visible=false;if(PAL.t>1.6){PAL.fallo=0;palasSaca()}else{const b=PAL.bola.position;PAL.sombra.position.set(b.x,groundY(b.x,b.z)+.0015,b.z)}return}
 // vuelo de la bola: del que golpea al que recibe (golpe a la altura de la mano), parábola
 PAL.t+=dt/PAL.dur;const de=PAL.quien==='chica'?palasPos('chica',PAL.sG,0):palasPos('jug',PAL.sP,0),a_=PAL.quien==='chica'?palasPos('jug',PAL.sT,0):palasPos('chica',PAL.sT,0);
 const y0=groundY(de[0],de[2])+.04,y1=groundY(a_[0],a_[2])+.034,u=PAL.t;const x=de[0]+(a_[0]-de[0])*u,z=de[2]+(a_[2]-de[2])*u,y=y0+(y1-y0)*u+4*PAL.h*u*(1-u);
 PAL.bola.visible=PAL.sombra.visible=true;PAL.bola.position.set(x,y,z);const gb=groundY(x,z);PAL.sombra.position.set(x,gb+.0015,z);
 if(PAL.quien==='chica'){PAL.aro.visible=true;PAL.aro.position.set(a_[0],groundY(a_[0],a_[2])+.002,a_[2]);PAL.aro.material.color.set(Math.abs(PAL.sP-PAL.sT)<.022?0x5cff7a:0xffffff);PAL.aro.material.opacity=.55+.35*Math.min(1,u)}
 else{PAL.aro.visible=false;if(u>=1){PAL.swC=0;palasSonido(600);PAL.quien='chica';PAL.dur=Math.max(.55,1.2-PAL.toques*.03);palasTiro()}}
 if(PAL.quien==='chica'&&y<gb+.004){PAL.fase='fallo';PAL.t=0;PAL.fallo=1;palasSonido(180);mostrar('¡Fallo! '+PAL.toques+' toques seguidos · récord: '+PAL.rec);PAL.toques=0;PAL.sP*=.5}}
// brazo derecho con la pala: en guardia y, si k<1, golpeando
function palasBrazo(p,t,k,sola){const B=p.userData.brazos.children[1],c=B.userData.codo;
 if(sola){B.rotation.z=.75+(k<1?Math.sin(k*Math.PI)*.35:0);B.rotation.x=-.25;c.rotation.z=.9;return}
 if(k<1){B.rotation.z=.2+Math.sin(k*Math.PI)*1.6;B.rotation.x=-.45;c.rotation.z=.35}else{B.rotation.z=.55+Math.sin(t*3)*.05;B.rotation.x=-.5;c.rotation.z=.8}}
