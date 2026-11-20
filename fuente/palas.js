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
// la chica: el mismo muñeco que el protagonista, en bikini, chanclas y coleta
function mkChica(){const g=mkPersona(),R=a=>a[(Math.random()*a.length)|0];const piel=new THREE.Color(R(PIEL_C)),bik=R(BANO_C).clone(),pelo=new THREE.Color(R([0x2a1d16,0x3a2a20,0x6b4a2a,0xc9a15a,0x8a3a22,0xd8b878]));
 const CAMB={0x2f5596:'piel',0x4a74b8:'piel',0xf6f5f1:'piel',0xdcdad4:'piel',0xf4f3ee:'piel',0x2b8fd6:'piel',0xf2efe8:'piel',0x2a2c33:'chancla'};
 const ch=new THREE.Color(R([0xff7aa8,0xf2c230,0x14a3a3,0xffffff]));const quitar=[];
 g.traverse(o=>{if(!o.isMesh)return;const m=o.material;if(m.map){quitar.push(o);return}const k=CAMB[m.color.getHex()];if(!k)return;o.material=m.clone();o.material.color.copy(k==='piel'?piel:ch);
  if(o.geometry.type==='TorusGeometry'&&o.parent===g.userData.tronco)quitar.push(o)});
 for(const o of quitar)o.parent.remove(o);
 const T=g.userData.tronco,mb=new THREE.MeshStandardMaterial({color:bik,roughness:.6}),mp=new THREE.MeshStandardMaterial({color:pelo,roughness:.85});
 for(const o of T.children)if(o.isMesh&&o.geometry.type==='CapsuleGeometry'&&Math.abs(o.position.y-.0004)<1e-5)o.material=mb;    // cadera → braguita
 const banda=new THREE.Mesh(new THREE.CylinderGeometry(.0121,.0121,.0042,20),mb);banda.scale.set(.7,1,1);banda.position.y=.0185;T.add(banda);
 for(const s of[-1,1]){const c=new THREE.Mesh(new THREE.SphereGeometry(.0036,12,8),mb);c.scale.set(.62,.95,1);c.position.set(.0068,.0182,s*.0042);T.add(c)}
 const cab=g.userData.cabeza,H=.0094;
 const cas=new THREE.Mesh(new THREE.SphereGeometry(.0104,24,14,0,Math.PI*2,0,Math.PI*.6),mp);cas.position.set(-.0006,H,0);cas.rotation.z=.34;cab.add(cas);
 const nuca=new THREE.Mesh(new THREE.SphereGeometry(.0098,16,10),mp);nuca.scale.set(.75,.8,1.02);nuca.position.set(-.0035,H-.0015,0);cab.add(nuca);
 const col=new THREE.Mesh(new THREE.CapsuleGeometry(.0034,.011,4,10),mp);col.position.set(-.0118,H-.004,0);col.rotation.z=-.35;cab.add(col);
 const gom=new THREE.Mesh(new THREE.TorusGeometry(.0029,.0008,6,12),new THREE.MeshStandardMaterial({color:ch,roughness:.5}));gom.position.set(-.0105,H+.0022,0);gom.rotation.set(0,Math.PI/2,-.35+Math.PI/2);cab.add(gom);
 for(const o of cab.children)if(o.geometry&&o.geometry.type==='TorusGeometry'&&o!==gom)o.material=new THREE.MeshStandardMaterial({color:0xb03a3a,roughness:.5});   // labios
 const pala=mkPala();g.userData.brazos.children[1].userData.codo.add(pala);g.userData.pala=pala;
 g.traverse(o=>{if(o.isMesh)o.castShadow=true});g.scale.setScalar(.74);g.name='chica_palas';return g}
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
