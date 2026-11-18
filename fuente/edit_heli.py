import re
f='index.html';s=open(f).read()
def r(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------- HUD compacto en la esquina (no tapa el centro) ----------
r("#nHud{position:fixed;top:calc(64px + env(safe-area-inset-top,0px));left:50%;transform:translateX(-50%);z-index:12;display:flex;flex-wrap:wrap;gap:6px 12px;justify-content:center;align-items:center;background:rgba(20,14,44,.78);color:#fff;border-radius:18px;padding:8px 16px;font:700 16px var(--body);box-shadow:0 0 0 2px #ffd24a inset,0 6px 20px rgba(0,0,0,.35);max-width:calc(100vw - 32px);pointer-events:none}",
  "#nHud{position:fixed;top:calc(58px + env(safe-area-inset-top,0px));right:12px;z-index:12;display:flex;gap:8px;align-items:center;background:rgba(20,14,44,.7);color:#fff;border-radius:999px;padding:4px 4px 4px 12px;font:700 14px var(--body);box-shadow:0 0 0 1.5px #ffd24a inset,0 4px 12px rgba(0,0,0,.3);pointer-events:none}")
r("#nHud .t{font:800 22px var(--body);color:#ffd98a}","#nHud .t{font:800 16px var(--body);color:#ffd98a}")
r("#nHud .cnt{display:flex;flex-wrap:wrap;gap:4px 12px;justify-content:center;align-items:center;flex:1}#nHud .r{font:600 13px var(--body);opacity:.85}#nHud .fin{pointer-events:auto;border:0;border-radius:999px;background:#c4161f;color:#fff;font:700 13px var(--body);padding:7px 12px;cursor:pointer}",
  "#nHud .cnt{display:flex;gap:10px;align-items:center;white-space:nowrap}#nHud .r{font:600 13px var(--body);opacity:.9}#nHud .r.ok{color:#7dffb0;opacity:1}#nHud .fin{pointer-events:auto;border:0;border-radius:999px;background:#c4161f;color:#fff;font:700 12px var(--body);padding:6px 10px;cursor:pointer}\n#selCar:not(.nav) .nveh{display:none!important}")
r("<button class=\"fin\">🏁 Terminar</button>","<button class=\"fin\" aria-label=\"Terminar\">🏁 Fin</button>")
r("const rec=repRecords()[0];el.querySelector('.cnt').innerHTML=`<div class=\"t\">🎁 ${REP.ent}</div><div class=\"r\">${rec?'Récord '+rec.r:'regalos'}</div>`+(d?`<div class=\"d\">Entrega en <b>${d[0]}</b> · ${fmtD(Math.hypot(d[1]-P.x,d[2]-P.y))}</div>`:'')}",
  "const rec=repRecords()[0],dd=d?Math.hypot(d[1]-P.x,d[2]-P.y):0;el.querySelector('.cnt').innerHTML=`<span class=\"t\">🎁 ${REP.ent}</span>`+(rec?`<span class=\"r\">🏆 ${rec.r}</span>`:'')+(d?`<span class=\"r\">📍 ${fmtD(dd)}</span>`:(REP.heli?'<span class=\"r\">Buscando tejado…</span>':''))+(REP.heli&&d&&dd<.8?'<span class=\"r ok\">⤓ Aterriza</span>':'')}")
r("mostrar('Recalculando…');","if(!REP.on)mostrar('Recalculando…');")
# ---------- selección: carroza o helicóptero ----------
r('<div class="opt"><span>Rivales</span>','<div class="opt nveh"><span>Vehículo</span><button data-veh="0">🛷 Carroza</button><button data-veh="1">🚁 Helicóptero</button></div>\n<div class="opt"><span>Rivales</span>')
r("sel:{c:0,col:0,vueltas:1,dif:1,hora:1,traz:1}","sel:{c:0,col:0,vueltas:1,dif:1,hora:1,traz:1,veh:0}")
r(" el.querySelectorAll('[data-d]').forEach(b=>b.onclick=()=>{RACE.sel.dif=+b.dataset.d;pintarSel()});",
  " el.querySelectorAll('[data-d]').forEach(b=>b.onclick=()=>{RACE.sel.dif=+b.dataset.d;pintarSel()});el.querySelectorAll('[data-veh]').forEach(b=>b.onclick=()=>{RACE.sel.veh=+b.dataset.veh;pintarSel()});")
r("el.querySelectorAll('[data-d]').forEach(b=>b.classList.toggle('on',+b.dataset.d===s.dif));","el.querySelectorAll('[data-d]').forEach(b=>b.classList.toggle('on',+b.dataset.d===s.dif));el.querySelectorAll('[data-veh]').forEach(b=>b.classList.toggle('on',+b.dataset.veh===(s.veh||0)));")
# ---------- no se puede bajar del helicóptero durante el reparto ----------
r("if(MODO==='heli'){if(HELI.posado&&HELI.suelo&&pieOK","if(MODO==='heli'){if(REP.on){objetivo=null;return null}if(HELI.posado&&HELI.suelo&&pieOK")
r("function accion(){if(!driving)return;","function accion(){if(!driving)return;if(REP.on&&MODO==='heli'){mostrar('Aterriza en el tejado junto a la chimenea iluminada');return}")
# ---------- empezar en helicóptero ----------
r("setDrive(true,'coche');gpsParar();document.body.classList.add('rep');","REP.heli=!!sel.veh;setDrive(true,REP.heli?'heli':'coche');gpsParar();document.body.classList.add('rep');")
r("vestirCoche(mkVehiculo(spec.t,spec.col[sel.col%spec.col.length]),spec.t);REP.spec=spec;","vestirCoche(mkVehiculo(spec.t,spec.col[sel.col%spec.col.length]),spec.t);REP.spec=spec;if(REP.heli)heliVestir(spec,sel.col);")
r("vestirCoche(CAR0,'clasico');if(driving)setDrive(false);","heliDesvestir();REP.heli=false;REP.chim=null;vestirCoche(CAR0,'clasico');if(driving)setDrive(false);")
r("if(NAV.tr&&REP.spec)navEstela(P.x,P.y,car.position.y","if(NAV.tr&&REP.spec)navEstela(P.x,P.y,REP.heli?P.z+.05:car.position.y")
# siguiente entrega: en helicóptero, un tejado con chimenea
r("function repSiguiente(){const d=repElegir();","function repSiguiente(){if(REP.heli){repBVH();const d=repTejado();REP.dest=d;if(!d){REP.reint=1;repHud();return}REP.ult.push([d[1],d[2]]);if(REP.ult.length>5)REP.ult.shift();repChimenea(d);REP.marca.position.set(d[1],d[3]+.09,d[2]);REP.marca.visible=true;repHud();return}\n const d=repElegir();")
r(" const d=REP.dest;if(d&&Math.hypot(d[1]-P.x,d[2]-P.y)<.2)repEntrega();\n",
  " const d=REP.dest;if(REP.heli){if(!d){REP.reint=(REP.reint||1)-dt;if(REP.reint<=0)repSiguiente()}else if(HELI.posado&&!HELI.suelo&&Math.hypot(d[1]-P.x,d[2]-P.y)<.32)repEntrega()}\n else if(d&&Math.hypot(d[1]-P.x,d[2]-P.y)<.2)repEntrega();\n")
r("{const g=REP.marca.userData.g.clone();g.position.set(P.x,car.position.y+.05,P.y);scene.add(g);let t=0;const tx=d[1],ty=d[2],z0=car.position.y;const vuela=()=>{t+=.04;g.position.x+=(tx-g.position.x)*.15;g.position.z+=(ty-g.position.z)*.15;g.position.y=z0+.05+Math.sin(Math.min(1,t)*Math.PI)*.12;g.rotation.y+=.3;if(t<1.2)requestAnimationFrame(vuela);else scene.remove(g)};vuela()}",
  "{const g=REP.marca.userData.g.clone();const H=REP.heli,zA=H?P.z+.1:car.position.y+.05,zB=H?d[3]+.1:zA;g.position.set(P.x,zA,P.y);scene.add(g);let t=0;const tx=d[1]+(H?.11:0),ty=d[2];const vuela=()=>{t+=.04;g.position.x+=(tx-g.position.x)*.15;g.position.z+=(ty-g.position.z)*.15;const k=Math.min(1,t);g.position.y=zA+(zB-zA)*k+Math.sin(k*Math.PI)*.12-(H&&t>1?(t-1)*.4:0);if(H&&t>1)g.scale.setScalar(Math.max(.01,1-(t-1)*4));g.rotation.y+=.3;if(t<1.3)requestAnimationFrame(vuela);else scene.remove(g)};vuela()}\n if(REP.heli&&REP.chim){REP.chim.userData.haz.visible=false;REP.chim.userData.humo=1.6}")
# chimenea animada (humo tras la entrega)
r(" const m=REP.marca;if(m&&m.visible){"," if(REP.chim&&REP.chim.userData.humo>0){const u=REP.chim.userData;u.humo-=dt;u.bolas.forEach((b,i)=>{const k=((1.6-u.humo)*1.2+i/5)%1;b.visible=u.humo>0;b.position.y=.08+k*.25;b.scale.setScalar(.6+k*1.6);b.material.opacity=.55*(1-k)})}\n if(REP.chim&&REP.chim.userData.haz.visible)REP.chim.userData.haz.material.opacity=.2+.08*Math.sin(NAV.uT.value*3);\n const m=REP.marca;if(m&&m.visible){")
# funciones nuevas
r("function repSiguiente(){","""// prioriza los árboles de colisión de los edificios del centro (para saber la altura de los tejados)
function repBVH(){const Q=BVHQ,add=[];for(let i=Q.length-1;i>=0;i--){const o=Q[i];if(o.userData.suelo)continue;let rr=o;while(rr.parent)rr=rr.parent;if(rr!==scene)continue;if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();const bb=o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld);const cx=Math.max(bb.min.x,Math.min(REP_C2[0],bb.max.x)),cz=Math.max(bb.min.z,Math.min(REP_C2[1],bb.max.z));if(Math.hypot(cx-REP_C2[0],cz-REP_C2[1])>REP_C2[2]+1)continue;try{o.geometry.computeBoundsTree()}catch(e){}add.push(o);Q.splice(i,1)}if(add.length)window.OBST=(window.OBST||[]).concat(add)}
// ---- reparto en helicóptero: el personaje vuela con su color y deja los regalos en chimeneas de tejados
function heliVestir(spec,ci){const u=heli.userData;if(!u.orig)u.orig=heli.children.slice(0,4).map(o=>o.material);heliDesvestir(true);
 const cab=heli.children[0],cris=heli.children[1],der=heli.children[3],col=spec.col[ci%spec.col.length];
 cab.material=der.material=new THREE.MeshStandardMaterial({color:col,roughness:.35,metalness:.45});
 cris.material=new THREE.MeshStandardMaterial({color:0xbfe4ff,roughness:.05,metalness:.1,transparent:true,opacity:.28,depthWrite:false});
 const g=new THREE.Group();g.name='navPiloto';const MT=(c,r=.7)=>new THREE.MeshStandardMaterial({color:c,roughness:r});
 const P_={sleigh:[0xc21f2a,0xf0c8a8,0xffffff],aurum:[0x8e1a2a,0xf0c8a8,0xf2f2ee],mirra:[0x2a4fa8,0xe8bf9a,0x8a4a22],esmeralda:[0x0f6a3c,0x6b4226,0x1a1a1a]}[spec.t]||[0xc21f2a,0xf0c8a8,0xffffff];
 const add=(geo,mat,x,y,z,sx=1,sy=1,sz=1)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.scale.set(sx,sy,sz);g.add(m);return m};
 add(new THREE.CylinderGeometry(.013,.017,.03,10),MT(P_[0]),.012,.06,0);add(new THREE.SphereGeometry(.011,12,8),MT(P_[1]),.012,.084,0);
 add(new THREE.SphereGeometry(.009,10,8),MT(P_[2],.85),.019,.078,0,1,1.25,1.1);
 if(spec.t==='sleigh'){add(new THREE.ConeGeometry(.011,.026,10),MT(0xc21f2a),.01,.103,0).rotation.z=.4;add(new THREE.CylinderGeometry(.012,.012,.004,10),MT(0xffffff,.9),.012,.093,0);add(new THREE.SphereGeometry(.004,8,6),MT(0xffffff,.9),.0,.113,0)}
 else{const oro=new THREE.MeshStandardMaterial({color:0xf5c84a,roughness:.25,metalness:.9});add(new THREE.CylinderGeometry(.01,.009,.008,10),oro,.012,.097,0);for(let k=0;k<6;k++){const a=k/6*6.283;add(new THREE.ConeGeometry(.0025,.007,5),oro,.012+Math.cos(a)*.009,.104,Math.sin(a)*.009)}}
 // saco de regalos colgando con un cabo
 add(new THREE.CylinderGeometry(.0015,.0015,.05,4),MT(0x6b4a2a),0,-.02,0);add(new THREE.SphereGeometry(.022,12,10),MT(0x7a5a2a,.9),0,-.055,0,1,1.15,1);
 const rg=[0xd51f1f,0x2fa84f,0xf2c230];rg.forEach((c,i)=>add(new THREE.BoxGeometry(.012,.012,.012),new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:.4}),(i-1)*.01,-.033,(i%2?.006:-.006)));
 g.traverse(o=>{if(o.isMesh)o.castShadow=true});heli.add(g)}
function heliDesvestir(soloPiloto){const u=heli.userData;const g=heli.getObjectByName('navPiloto');if(g)heli.remove(g);if(!soloPiloto&&u.orig)u.orig.forEach((m,i)=>{heli.children[i].material=m})}
function repCalleCerca(x,y){let bn='Vigo',bd=1e9;for(const d of repPool()){const e=Math.hypot(d[1]-x,d[2]-y);if(e<bd){bd=e;bn=d[0]}}return bn}
// tejado plano de un edificio a media distancia, dentro de la zona del centro
function repTejado(){if(!window.OBST||!OBST.length)return null;const x0=P.x,y0=P.y;
 for(let t=0;t<500;t++){const c=Math.random()<.6?REP_C1:REP_C2,a=Math.random()*6.283,rr=Math.sqrt(Math.random())*c[2],x=c[0]+Math.cos(a)*rr,y=c[1]+Math.sin(a)*rr,e=Math.hypot(x-x0,y-y0);
  if(e<REP_MIN||e>REP_MAX+1||REP.ult.some(u=>Math.hypot(u[0]-x,u[1]-y)<.6)||cell(x,y).t!==3)continue;const h=sueloHeli(x,y);if(h-groundY(x,y)<.12)continue;
  let ok=true;for(const[dx,dy]of[[.09,0],[-.09,0],[0,.09],[0,-.09],[.06,.06],[-.06,-.06]]){if(Math.abs(sueloHeli(x+dx,y+dy)-h)>.012){ok=false;break}}if(!ok)continue;
  return[repCalleCerca(x,y),+x.toFixed(3),+y.toFixed(3),h]}return null}
// chimenea de ladrillo con nieve, haz de luz dorado para verla desde lejos y humo al entregar
function repChimenea(d){if(REP.chim){scene.remove(REP.chim);const i=REP.objs.indexOf(REP.chim);if(i>=0)REP.objs.splice(i,1)}
 const g=new THREE.Group();g.position.set(d[1]+.11,d[3],d[2]);const LAD=new THREE.MeshStandardMaterial({color:0x9a3b2b,roughness:.9});
 const c=new THREE.Mesh(new THREE.BoxGeometry(.045,.075,.045),LAD);c.position.y=.0375;g.add(c);const cap=new THREE.Mesh(new THREE.BoxGeometry(.055,.012,.055),new THREE.MeshStandardMaterial({color:0xf6f6f2,roughness:.9}));cap.position.y=.08;g.add(cap);
 const hueco=new THREE.Mesh(new THREE.BoxGeometry(.032,.002,.032),new THREE.MeshBasicMaterial({color:0x111111}));hueco.position.y=.0865;g.add(hueco);
 const haz=new THREE.Mesh(new THREE.CylinderGeometry(.05,.05,2.4,16,1,true),new THREE.MeshBasicMaterial({color:0xffd24a,transparent:true,opacity:.25,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,toneMapped:false}));haz.position.set(-.11,1.2,0);g.add(haz);
 const pista=new THREE.Mesh(new THREE.RingGeometry(.1,.125,32),new THREE.MeshBasicMaterial({color:0xffd24a,transparent:true,opacity:.85,toneMapped:false,side:THREE.DoubleSide}));pista.rotation.x=-Math.PI/2;pista.position.set(-.11,.004,0);g.add(pista);
 const bolas=[];for(let i=0;i<5;i++){const b=new THREE.Mesh(new THREE.SphereGeometry(.018,8,6),new THREE.MeshBasicMaterial({color:0xdddddd,transparent:true,opacity:0,depthWrite:false}));b.visible=false;g.add(b);bolas.push(b)}
 g.userData={haz,bolas,humo:0};scene.add(g);REP.objs.push(g);REP.chim=g}
function repSiguiente(){""")
# minimapa: línea directa al tejado en helicóptero
r(" const na=P.a-Math.PI/2,r=W2/2-16;"," if(REP.on&&REP.heli&&REP.dest){const d=REP.dest;g.save();g.translate(W2/2,W2/2);g.rotate(P.a-Math.PI/2);g.scale(k,k);g.translate(-P.x,-P.y);g.lineCap='round';g.setLineDash([W2*.05/k,W2*.04/k]);g.strokeStyle='#ffffff';g.lineWidth=W2*.06/k;g.beginPath();g.moveTo(P.x,P.y);g.lineTo(d[1],d[2]);g.stroke();g.strokeStyle='#1f7bff';g.lineWidth=W2*.04/k;g.stroke();g.setLineDash([]);g.fillStyle='#ffd24a';g.strokeStyle='#c4161f';g.lineWidth=W2*.015/k;g.beginPath();g.arc(d[1],d[2],W2*.04/k,0,7);g.fill();g.stroke();g.restore();\n  const dx=d[1]-P.x,dy=d[2]-P.y,ra=Math.atan2(dy,dx)+(P.a-Math.PI/2);if(Math.hypot(dx,dy)*k>W2/2-10){const rr=W2/2-12;g.save();g.translate(W2/2+Math.cos(ra)*rr,W2/2+Math.sin(ra)*rr);g.rotate(ra);g.fillStyle='#1f7bff';g.strokeStyle='#fff';g.lineWidth=2.5;g.beginPath();g.moveTo(10,0);g.lineTo(-7,-8);g.lineTo(-7,8);g.closePath();g.fill();g.stroke();g.restore()}}\n const na=P.a-Math.PI/2,r=W2/2-16;")
r("if(RACE.nav){let r_=null;try{r_=JSON.parse(localStorage.getItem('gtvigo_reparto_'+s.dif)||'null')}catch(e){}el.querySelector('.rec').textContent=r_?'Tu récord: '+r_+' puntos':'8 regalos · cada entrega suma tiempo';",
  "if(RACE.nav){const r_=repRecords()[0];el.querySelector('.rec').textContent=(r_?'🏆 Récord: '+r_.n+' · '+r_.r+' regalos':'Sin tiempo: reparte todos los que puedas')+(s.veh?' · aterriza en los tejados junto a la chimenea':'');el.querySelector('.ayuda').textContent=s.veh?'▲▼ avanzar/frenar · ◀▶ girar · ⤒ Q subir · ⤓ Z bajar · C: cámara':'▲▼◀▶ o WASD para conducir · C: cámara · G: gráficos';")
r("#nHud .cnt{display:flex;","#nHud[hidden]{display:none}#nHud .cnt{display:flex;")
r("opacity:.25,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,toneMapped:false}));haz","opacity:.45,depthWrite:false,side:THREE.DoubleSide,toneMapped:false}));haz")
r("REP.chim.userData.haz.material.opacity=.2+.08*Math.sin","REP.chim.userData.haz.material.opacity=.4+.12*Math.sin")
r("function pintarSel(){const s=RACE.sel,spec=LISTA()[s.c];const el=document.getElementById('selCar');","function pintarSel(){const s=RACE.sel,spec=LISTA()[s.c];const el=document.getElementById('selCar');{const ay=el.querySelector('.ayuda');ay.dataset.o=ay.dataset.o||ay.textContent;ay.textContent=ay.dataset.o}")
r("window.__G={P,RACE,","window.__G={P,RACE,cell,sueloHeli,groundY,HELI,BVHQ,")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok heli')
