// ================= Misiones en el GPS · Misión de taxi (edit_taxi.py) =================
// En el menú del GPS, arriba del todo, la sección «🎯 Misiones» (resaltadas en dorado, con su icono y la etiqueta MISIÓN),
// y debajo «📍 Direcciones frecuentes» como siempre. Para añadir más misiones: otra entrada en MISIONES.
// 🚕 Taxi: el coche se convierte en taxi (cartel TAXI en el techo, luz verde libre / roja ocupado). Un cliente espera en
// una acera cercana haciendo señas; la línea azul del GPS lleva hasta él. Para a su lado (casi parado) y se sube.
// Te dice a dónde va y la línea azul te guía hasta allí. Al parar en el destino se baja y cobras monedas 🪙 (más propina
// si llegas antes de que acabe el tiempo). Luego sale otro cliente, hasta que terminas el turno (GPS o ✕ del cartel).
// Las monedas se guardan en el navegador (gtvigo_monedas).
const TAXI={on:false,fase:'',p:null,dest:null,t:0,lim:0,carr:0,ganado:0,sig:0,rr:0,prev:null,luz:null,ped:[],mk:null,mon:0,anim:null};
try{TAXI.mon=+localStorage.getItem('gtvigo_monedas')||0}catch(e){}
const TX_NOM=['Maruxa','Xurxo','Uxía','Brais','Sabela','Iago','Noa','Antón','Carmiña','Manolo','Lucía','Paco','Rosalía','Breixo','Iria','Fermín','Mari Carmen','Suso'];
const TX_FRASE=[d=>'¡A '+d+', por favor!',d=>'Lléveme a '+d+', que voy con prisa',d=>'¿Me acerca a '+d+'? Gracias',d=>'A '+d+', ¡e rapidiño!',d=>'Buenas. A '+d+', si é tan amable',d=>'¡Corra, que chego tarde! A '+d];
const MISIONES=[{id:'taxi',ico:'🚕',n:'Taxi',d:'Recoge clientes y llévalos a su destino · cobras 🪙',ir:()=>taxiEmpezar(),on:()=>TAXI.on,fin:()=>taxiFin('menu')}];
// ---- estilos: misiones resaltadas en el GPS y cartel del taxi
{const st=document.createElement('style');st.textContent=`
#gpsMenu .gpsSec{margin:12px 2px 4px;font:700 11px var(--body);letter-spacing:.08em;text-transform:uppercase;opacity:.65}
#gpsMenu .gpsSec:first-child{margin-top:0}
#gpsMenu button.mis{position:relative;display:flex;align-items:center;gap:10px;background:linear-gradient(135deg,#ffcf3a,#ff9f1a);color:#2a1a00;border:2px solid #e08a00;box-shadow:0 3px 10px rgba(224,138,0,.35);padding:10px 12px}
#gpsMenu button.mis:hover{background:linear-gradient(135deg,#ffd95e,#ffb03a);color:#2a1a00;filter:brightness(1.05)}
#gpsMenu button.mis .i{font:400 26px/1 system-ui;flex:none}#gpsMenu button.mis .t{flex:1;min-width:0}
#gpsMenu button.mis b{display:block;font:800 15px var(--body)}#gpsMenu button.mis small{display:block;font:500 12px var(--body);opacity:.85}
#gpsMenu button.mis .tag{flex:none;font:800 10px var(--body);letter-spacing:.06em;background:#2a1a00;color:#ffcf3a;border-radius:6px;padding:3px 6px}
#gpsMenu button.mis.act{background:linear-gradient(135deg,#2a1a00,#4a2f00);color:#ffcf3a;border-color:#ffcf3a}
#gpsMenu button.mis.act .tag{background:#ffcf3a;color:#2a1a00}
#taxiHud{position:fixed;left:50%;transform:translateX(-50%);top:calc(84px + env(safe-area-inset-top,0px));z-index:6;display:flex;align-items:center;gap:10px;background:#ffcf3a;color:#2a1a00;border:2px solid #2a1a00;border-radius:14px;padding:6px 8px 6px 12px;font:600 13px var(--body);box-shadow:0 4px 14px rgba(0,0,0,.3);max-width:min(92vw,520px)}
#taxiHud[hidden]{display:none!important}#taxiHud .i{font:400 22px/1 system-ui}#taxiHud .m{font:800 14px var(--body);white-space:nowrap}
#taxiHud .x{border:0;background:#2a1a00;color:#ffcf3a;border-radius:999px;width:26px;height:26px;font:800 13px var(--body);cursor:pointer;flex:none}
#taxiHud .tm.mal{color:#b3261e}
body.carrera #taxiHud,body.rep #taxiHud{display:none!important}
@media (max-width:700px){#taxiHud{top:calc(96px + env(safe-area-inset-top,0px));font-size:12px}}`;document.head.appendChild(st)}
const TXH=document.createElement('div');TXH.id='taxiHud';TXH.hidden=true;TXH.innerHTML='<span class="i">🚕</span><div class="t"></div><span class="m"></span><button class="x" title="Terminar el turno de taxi" aria-label="Terminar el turno de taxi">✕</button>';document.body.appendChild(TXH);
TXH.querySelector('.x').onclick=()=>taxiFin('menu');
function taxiMon(n){TAXI.mon+=n;try{localStorage.setItem('gtvigo_monedas',TAXI.mon)}catch(e){}}
// ---- menú del GPS: misiones arriba
function gpsMisiones(L){if(REP.on||RACE.on)return;const h=document.createElement('div');h.className='gpsSec';h.textContent='🎯 Misiones';L.appendChild(h);
 for(const m of MISIONES){const act=m.on(),b=document.createElement('button');b.className='mis'+(act?' act':'');
  b.innerHTML=`<span class="i">${m.ico}</span><span class="t"><b>${m.n}${act?' · en servicio':''}</b><small>${act?'Toca para terminar el turno · 🪙 '+TAXI.mon:m.d+(TAXI.mon?' · tienes 🪙 '+TAXI.mon:'')}</small></span><span class="tag">${act?'TERMINAR':'MISIÓN'}</span>`;
  b.onclick=()=>{document.getElementById('gpsMenu').hidden=true;act?m.fin():m.ir()};L.appendChild(b)}
 const h2=document.createElement('div');h2.className='gpsSec';h2.textContent='📍 Direcciones frecuentes';L.appendChild(h2)}
// ---- el coche se convierte en taxi (y vuelve a ser el de antes al acabar)
let TX_TEX=null;function txTex(){if(TX_TEX)return TX_TEX;const c=document.createElement('canvas');c.width=128;c.height=48;const x=c.getContext('2d');
 x.fillStyle='#f6f4ea';x.fillRect(0,0,128,48);x.fillStyle='#141414';x.font='900 38px Arial Black,Arial,sans-serif';x.textAlign='center';x.textBaseline='middle';x.fillText('TAXI',64,26);
 TX_TEX=new THREE.CanvasTexture(c);TX_TEX.colorSpace=THREE.SRGBColorSpace;return TX_TEX}
function taxiVestir(){const prev={ch:[...car.children],body:car.userData.body,tipo:car.userData.tipo,moto:P.vestidoMoto};
 vestirCoche(mkVehiculo('taxi',0xf7f7f4),'taxi');P.vestidoMoto=false;const k=1/.6;
 // cartel TAXI algo más grande que el de serie, con el texto a los cuatro lados
 const g=new THREE.Group();g.name='taxiCartel';const W=.021,H=.0095,D=.014,x0=-.004,y0=.0565;
 const caja=new THREE.Mesh(new THREE.BoxGeometry(W,H,D),new THREE.MeshStandardMaterial({color:0xf6f4ea,roughness:.4,emissive:0x504a30,emissiveIntensity:.25}));caja.position.set(x0,y0,0);g.add(caja);
 const mt=new THREE.MeshBasicMaterial({map:txTex()});
 for(const s of[-1,1]){const pl=new THREE.Mesh(new THREE.PlaneGeometry(W*.92,H*.8),mt);pl.position.set(x0,y0,s*(D/2+.0002));if(s<0)pl.rotation.y=Math.PI;g.add(pl);
  const pf=new THREE.Mesh(new THREE.PlaneGeometry(D*.92,H*.8),mt);pf.position.set(x0+s*(W/2+.0002),y0,0);pf.rotation.y=s*Math.PI/2;g.add(pf)}
 const luz=new THREE.Mesh(new THREE.BoxGeometry(.006,.005,.006),new THREE.MeshBasicMaterial({color:0x3fe07a}));luz.position.set(x0+.009,y0+H/2+.0025,0);g.add(luz);
 g.position.multiplyScalar(k);g.scale.setScalar(k);car.add(g);TAXI.luz=luz.material;
 car.traverse(o=>{if(o.isMesh&&o!==luz&&o.material&&o.material.isMeshBasicMaterial&&o.material.color&&o.material.color.getHex()===0x3fe07a)o.material=luz.material});   // la luz de serie hace lo mismo
 TAXI.prev=prev}
function taxiDesvestir(){const pv=TAXI.prev;TAXI.prev=null;if(!pv||car.userData.tipo!=='taxi')return;for(const c of [...car.children])car.remove(c);for(const c of pv.ch)car.add(c);car.userData.body=pv.body;car.userData.tipo=pv.tipo;P.vestidoMoto=pv.moto}
function taxiLuz(ocupado){if(TAXI.luz)TAXI.luz.color.set(ocupado?0xe0352b:0x3fe07a)}
// ---- marcador amarillo (columna de luz + aro en el suelo donde parar)
function txMarca(){const g=new THREE.Group();
 const c=new THREE.Mesh(new THREE.CylinderGeometry(.035,.035,.7,16,1,true),new THREE.MeshBasicMaterial({color:0xffc21a,transparent:true,opacity:.32,side:THREE.DoubleSide,depthWrite:false,fog:false}));c.position.y=.35;g.add(c);
 const r=new THREE.Mesh(new THREE.RingGeometry(.075,.095,32),new THREE.MeshBasicMaterial({color:0xffc21a,transparent:true,opacity:.8,side:THREE.DoubleSide,depthWrite:false,fog:false}));r.rotation.x=-Math.PI/2;r.position.y=.01;g.add(r);
 const f=new THREE.Mesh(new THREE.ConeGeometry(.022,.04,4),new THREE.MeshBasicMaterial({color:0xffc21a,fog:false}));f.rotation.x=Math.PI;f.position.y=.14;g.add(f);g.userData.f=f;g.userData.r=r;
 g.visible=false;scene.add(g);return g}
// ---- cliente: el mismo muñeco que el protagonista con otra ropa y otro pelo
function txPersona(){const p=mkPersona(),R=a=>a[(Math.random()*a.length)|0];p.scale.setScalar(.8);
 const ropa=new THREE.Color(R([0xd23b2c,0x1f6fd0,0x2fa84f,0xf2c230,0x7a3fb0,0xff7aa8,0x15171c,0x14a3a3,0xe07a1a])),pant=new THREE.Color(R([0x2f5596,0x22232a,0x6b5a44,0x3d4a3a,0x8a8f99,0x3a2a4a]));
 const piel=R([0xf0bf94,0xe2a47c,0xc68a5e,0x8a5a3a,0xf6d2b0]);
 const vistos=new Set();p.traverse(o=>{if(!o.isMesh||!o.material||vistos.has(o.material))return;const m=o.material;vistos.add(m);if(!m.color||m.map)return;const h=m.color.getHex();
  if(h===0xf6f5f1)m.color.copy(ropa);else if(h===0xdcdad4)m.color.copy(ropa).multiplyScalar(.82);else if(h===0x2f5596)m.color.copy(pant);else if(h===0x4a74b8)m.color.copy(pant).multiplyScalar(1.2);
  else if(h===0xf0bf94)m.color.set(piel);else if(h===0xe2a47c)m.color.set(piel).multiplyScalar(.9)});
 p.visible=true;scene.add(p);return p}
function txQuitarP(p){if(!p)return;scene.remove(p);const vis=new Set();p.traverse(o=>{if(o.isMesh){o.geometry.dispose();if(o.material&&!o.material.map&&!vis.has(o.material)){vis.add(o.material);o.material.dispose()}}})}
// ---- elegir dónde espera el cliente: un punto de calle (no autovía) a 2,5–7 de distancia con ruta
function taxiSitioRecogida(){const G=gpsGrafo();if(!G)return null;
 for(let n=0;n<160;n++){const i=(Math.random()*G.X.length)|0;if(G.comp[i]!==G.main||!G.ADJ[i].length)continue;const c=G.CLS[i]||'m';if(c==='T'||c==='R')continue;
  const x=G.X[i],y=G.Y[i],d=Math.hypot(x-P.x,y-P.y);if(d<2.5||d>(n<100?7:12))continue;const t=cell(x,y).t;if(t!==2&&t!==4)continue;return[x,y]}
 return null}
function taxiDestino(px,py){const L=DESTINOS.filter(d=>{const k=Math.hypot(d[1]-px,d[2]-py);return k>5&&k<28});const S=L.length?L:DESTINOS.filter(d=>Math.hypot(d[1]-px,d[2]-py)>2);return S[(Math.random()*S.length)|0]}
// el punto de la acera junto al final de la ruta (a la derecha del sentido de la marcha)
function txAcera(pts){const n=pts.length,e=pts[n-1],q=pts[Math.max(0,n-4)];let dx=e[0]-q[0],dy=e[1]-q[1];const l=Math.hypot(dx,dy)||1;dx/=l;dy/=l;return{x:e[0]-dy*.05,y:e[1]+dx*.05,a:Math.atan2(dx,dy)}}   // mirando a la calzada
function txRuta(){const d=TAXI.fase==='ir'?['👋 '+TAXI.nom+(TAXI.calle?' · '+TAXI.calle:''),TAXI.px,TAXI.py]:TAXI.dest;gpsIniciar(d);if(GPS.on){GPS.taxi=true;GPS_DEST.visible=false}return GPS.on}
// ---- empezar / siguiente cliente / terminar
function taxiEmpezar(){if(REP.on||RACE.on)return;if(!driving||MODO!=='coche'){mostrar('🚕 Súbete a un coche para hacer de taxista');return}
 if(TAXI.on)return;Object.assign(TAXI,{on:true,carr:0,ganado:0});if(!TAXI.mk)TAXI.mk=txMarca();taxiVestir();try{gtvEv('mision/taxi','Misión taxi')}catch(e){}
 aviso('🚕 ¡De servicio!',1.4);taxiCliente()}
function taxiCliente(){for(let n=0;n<6;n++)if(taxiCliente1())return;TAXI.fase='buscar';TAXI.sig=1.5}
function taxiCliente1(){const s=taxiSitioRecogida();if(!s)return false;
 const calle=calleEn(s[0],s[1]);TAXI.nom=TX_NOM[(Math.random()*TX_NOM.length)|0];TAXI.calle=calle;
 const pts=gpsCalcular(P.x,P.y,s[0],s[1]);if(!pts||pts.length<2)return false;
 const ac=txAcera(pts);TAXI.px=ac.x;TAXI.py=ac.y;TAXI.fase='ir';TAXI.anim=null;taxiLuz(false);
 txQuitarP(TAXI.p);TAXI.p=txPersona();TAXI.p.position.set(ac.x,groundY(ac.x,ac.y),ac.y);TAXI.p.rotation.y=ac.a;TAXI.pa=ac.a;
 TAXI.mk.position.set(ac.x,groundY(ac.x,ac.y),ac.y);TAXI.mk.visible=true;txRuta();
 mostrar('👋 '+TAXI.nom+' espera un taxi'+(calle?' en '+calle:'')+'. Sigue la línea azul y para a su lado');return true}
function taxiFin(motivo){if(!TAXI.on)return;TAXI.on=false;const ocup=TAXI.fase==='llevar'||TAXI.fase==='sube';TAXI.fase='';
 if(GPS.taxi)gpsParar();GPS.taxi=false;if(TAXI.mk)TAXI.mk.visible=false;txQuitarP(TAXI.p);TAXI.p=null;for(const q of TAXI.ped)txQuitarP(q.p);TAXI.ped=[];TXH.hidden=true;
 if(motivo!=='externo')taxiDesvestir();else TAXI.prev=null;
 const res=TAXI.carr?` · ${TAXI.carr} carrera${TAXI.carr>1?'s':''} · +🪙 ${TAXI.ganado}`:'';
 if(motivo==='menu')mostrar('🚕 Fin del turno'+res);else if(motivo==='salir')mostrar((ocup?'😠 El cliente se baja sin pagar. ':'')+'🚕 Has dejado el taxi'+res);else if(motivo==='otro')mostrar('🚕 Turno de taxi terminado'+res)}
window.taxiSalir=()=>taxiFin('salir');window.taxiT={empezar:()=>taxiEmpezar(),fin:()=>taxiFin('menu'),st:()=>TAXI};
function txS(s){s=Math.max(0,Math.ceil(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function taxiHud(){const t=TXH.querySelector('.t'),m=TXH.querySelector('.m');TXH.hidden=false;
 if(TAXI.fase==='sube')t.innerHTML=`<b>${TAXI.nom}</b> se está subiendo…`;
 else if(TAXI.fase==='llevar'&&TAXI.dest){const r=TAXI.lim-TAXI.t;t.innerHTML=`<b>${TAXI.nom}</b> → ${TAXI.dest[0]}<br><span class="tm${r<0?' mal':''}">⏱ ${r>=0?txS(r)+' para la propina':'sin propina'}</span>`}
 else if(TAXI.fase==='ir')t.innerHTML=`<b>Libre</b> · recoge a ${TAXI.nom}${TAXI.calle?'<br>'+TAXI.calle:''}`;else t.innerHTML='<b>Libre</b> · buscando cliente…';
 m.textContent='🪙 '+TAXI.mon}
// ---- cada fotograma (mientras se conduce)
function taxiTick(dt){
 for(let i=TAXI.ped.length-1;i>=0;i--){const q=TAXI.ped[i];q.t+=dt;const k=Math.min(1,q.t/1.6);q.p.position.set(q.x0+(q.x1-q.x0)*k,groundY(q.x0+(q.x1-q.x0)*k,q.y0+(q.y1-q.y0)*k),q.y0+(q.y1-q.y0)*k);animPersona(q.p,q.t,1);if(q.t>2.4){txQuitarP(q.p);TAXI.ped.splice(i,1)}}
 if(!TAXI.on)return;
 if(RACE.on||REP.on){taxiFin('externo');return}
 if(MODO!=='coche'||car.userData.tipo!=='taxi'){taxiFin(car.userData.tipo!=='taxi'&&MODO==='coche'?'externo':'salir');return}
 const T=TAXI,mk=T.mk,now=performance.now()/1000,v=Math.abs(P.v);
 if(mk&&mk.visible){mk.userData.f.position.y=.14+Math.sin(now*3)*.02;mk.userData.f.rotation.y=now*2;mk.userData.r.material.opacity=.55+.3*Math.sin(now*4)}
 if(T.fase==='buscar'){T.sig-=dt;if(T.sig<=0)taxiCliente();taxiHud();return}
 if(T.fase==='ir'||T.fase==='llevar'){T.rr-=dt;if(!GPS.on&&T.rr<=0)T.rr=txRuta()?2:8}
 if(T.fase==='ir'){const p=T.p,d=Math.hypot(T.px-P.x,T.py-P.y);
  // hace señas al taxi (brazo arriba) y mira hacia él cuando se acerca
  animPersona(p,now,0);const br=p.userData.brazos&&p.userData.brazos.children[1];if(br){br.rotation.z=0;br.rotation.x=-2.5-.35*Math.sin(now*9)}
  if(d<1.2)p.rotation.y=Math.atan2(-(P.y-T.py),P.x-T.px);
  if(d<.22&&v<.07){T.fase='sube';T.anim={t:0,x0:p.position.x,y0:p.position.z};if(br)br.rotation.x=-.13;mostrar('🚕 '+TAXI.nom+' se sube…')}
  else if(d<.5&&v>=.07&&!T.avF){T.avF=1;mostrar('Frena junto a '+T.nom+' para que suba')}taxiHud();return}
 if(T.fase==='sube'){const a=T.anim;a.t+=dt;const k=Math.min(1,a.t/.9),x=a.x0+(P.x-a.x0)*k,y=a.y0+(P.y-a.y0)*k;T.p.position.set(x,groundY(x,y),y);T.p.rotation.y=Math.atan2(-(P.y-a.y0),P.x-a.x0);animPersona(T.p,a.t,1);
  if(v>.12){T.fase='ir';T.p.position.set(T.px,groundY(T.px,T.py),T.py);T.p.rotation.y=T.pa;mostrar('¡Espera! '+T.nom+' aún no ha subido');return}
  if(k>=1){T.p.visible=false;T.mk.visible=false;taxiLuz(true);T.avF=0;
   const d=taxiDestino(P.x,P.y);T.dest=d;T.fase='llevar';T.t=0;txRuta();const len=GPS.on?GPS.acc[GPS.acc.length-1]:Math.hypot(d[1]-P.x,d[2]-P.y)*1.3;
   T.len=len;T.lim=Math.round(14+len*2.4);const ac=GPS.on?txAcera(GPS.pts):{x:d[1],y:d[2],a:0};T.dx=ac.x;T.dy=ac.y;T.da=ac.a;
   T.mk.position.set(ac.x,groundY(ac.x,ac.y),ac.y);T.mk.visible=true;
   mostrar('🗣 '+T.nom+': «'+TX_FRASE[(Math.random()*TX_FRASE.length)|0](d[0])+'»')}
  taxiHud();return}
 if(T.fase==='llevar'){T.t+=dt;const d=Math.hypot(T.dx-P.x,T.dy-P.y);
  if(d<.25&&v<.07){T.fase='baja';T.mk.visible=false;if(GPS.taxi)gpsParar();
   const base=8+Math.round(T.len*1.6),prop=T.t<=T.lim?Math.round(base*.5):0;taxiMon(base+prop);T.ganado+=base+prop;T.carr++;taxiLuz(false);
   try{sonMoneda();setTimeout(()=>{try{sonMoneda()}catch(e){}},140)}catch(e){}
   aviso('🪙 +'+(base+prop),1.6);mostrar('🏁 '+T.nom+' ha llegado a '+T.dest[0]+' · carrera 🪙 '+base+(prop?' + propina 🪙 '+prop:' (sin propina)'));
   // se baja y se va andando por la acera
   const p=T.p;T.p=null;p.visible=true;const fx=Math.cos(T.da+Math.PI),fy=-Math.sin(T.da+Math.PI);
   TAXI.ped.push({p,t:0,x0:P.x,y0:P.y,x1:T.dx+fx*.06,y1:T.dy+fy*.06});p.rotation.y=Math.atan2(-(T.dy-P.y),T.dx-P.x);
   T.fase='buscar';T.sig=3.5}
  else if(d<.5&&v>=.07&&!T.avF){T.avF=1;mostrar('Para aquí para que se baje '+T.nom)}
  taxiHud();return}}
