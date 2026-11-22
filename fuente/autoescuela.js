// ================= Misión: clase práctica de autoescuela (edit_autoescuela.py) =================
// Desde el GPS (🎯 Misiones › 🚗 Autoescuela) eliges la clase: normal, solo aparcamiento, con más tráfico o de noche
// (las dos últimas se desbloquean dando clases) y cómo es el profesor (hablador, normal o callado; con voz o sin ella).
// 1) La línea azul te lleva a la autoescuela; el profesor sube y el coche pasa a ser el de la autoescuela (cartel L).
// 2) Circulación: calles tranquilas, Urzáiz y Gran Vía, la rotonda de Praza de España y la de Beiramar (te dice qué
//    salida tomar). Vigila bordillos, choques y roces, velocidad, carril, intermitentes (Z / X o ⬅ ➡) y suavidad.
// 3) Zona de prácticas en el muelle (explanada al este del Areal): aparcamiento en línea, en batería (de frente),
//    en oblicuo y salida del aparcamiento. Cada uno se puntúa por lo centrado y recto que quede el coche.
// 4) Vuelta a la autoescuela, nota del 0 al 10 con los comentarios del profesor, monedas 🪙 y habilidades guardadas
//    en el navegador (gtvigo_ae); con más clases se desbloquean las variantes.
const AE={on:false,fase:'',var:'normal',legs:[],li:0,man:null,mi:0,st:null,park:{},t:0,dT:9,prev:null,objs:[],slots:{},BL:0,blA:0,blT:0,mk:null,p:null,anim:null,ped:[],charla:1,voz:true,cie:null,lastPts:null,turnosVistos:new Set(),fin:null};
window.aeActivo=()=>AE.on;
let AED={clases:0,mejor:0,hab:{linea:0,bateria:0,oblicuo:0,control:0,intermitentes:0},charla:1,voz:true};
try{const j=JSON.parse(localStorage.getItem('gtvigo_ae')||'null');if(j)AED=Object.assign(AED,j,{hab:Object.assign(AED.hab,j.hab||{})})}catch(e){}
function aeGuardar(){try{localStorage.setItem('gtvigo_ae',JSON.stringify(AED))}catch(e){}}
const AE_VAR={normal:{n:'Clase normal',d:'Circulación, rotondas y aparcamiento',ico:'🚗',req:0},
 aparca:{n:'Solo aparcamiento',d:'Directo a la zona de prácticas',ico:'🅿️',req:0},
 trafico:{n:'Con más tráfico',d:'Hora punta en el centro',ico:'🚦',req:1},
 noche:{n:'Clase de noche',d:'Luces, farolas y poca visibilidad',ico:'🌙',req:2}};
const AE_NOM={linea:'en línea',bateria:'en batería',oblicuo:'en oblicuo',salida:'salida del aparcamiento'};
MISIONES.push({id:'autoescuela',ico:'🚗',n:'Autoescuela · clase práctica',d:'El profesor te guía: rotondas y aparcamientos · nota y 🪙',ir:()=>aeElegir(),on:()=>AE.on,fin:()=>aeFin('abandono'),enTxt:' · en clase',da:'Toca para terminar la clase'});
// ---------- estilos y paneles
{const st=document.createElement('style');st.textContent=`
#aeHud{position:fixed;left:50%;transform:translateX(-50%);top:calc(84px + env(safe-area-inset-top,0px));z-index:6;display:flex;align-items:center;gap:8px;background:#163a7a;color:#fff;border:2px solid #fff;border-radius:14px;padding:5px 6px 5px 10px;font:600 12px var(--body);box-shadow:0 4px 14px rgba(0,0,0,.3);max-width:min(96vw,560px)}
#aeHud[hidden],#aeDice[hidden],#aeFinP[hidden]{display:none!important}#aeHud .L{flex:none;width:26px;height:26px;border-radius:6px;background:#fff;color:#163a7a;font:900 19px/26px Arial Black,Arial,sans-serif;text-align:center}
#aeHud .t{flex:1;min-width:0;line-height:1.25}#aeHud .t b{font-weight:800}#aeHud .t small{display:block;opacity:.85;font-weight:500}
#aeHud button{flex:none;border:0;border-radius:10px;cursor:pointer;font:800 15px var(--body);height:34px;min-width:40px;background:rgba(255,255,255,.16);color:#fff}
#aeHud button.on{background:#ffb020;color:#2a1a00;animation:aeBl .5s steps(2) infinite}#aeHud button.x{min-width:28px;height:28px;border-radius:999px;font-size:12px;background:#fff;color:#163a7a}
@keyframes aeBl{50%{filter:brightness(.6)}}
#aeDice{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(96px + env(safe-area-inset-bottom,0px));z-index:7;display:flex;gap:10px;align-items:flex-start;background:rgba(255,255,255,.96);color:#1a1d2b;border-radius:16px;padding:10px 14px;font:600 14px/1.35 var(--body);box-shadow:0 6px 20px rgba(0,0,0,.3);max-width:min(92vw,540px);pointer-events:none}
#aeDice .a{font:400 26px/1 system-ui;flex:none}#aeDice small{display:block;font:700 10px var(--body);letter-spacing:.06em;text-transform:uppercase;color:#163a7a;margin-bottom:2px}
#aeFinP{position:fixed;inset:0;z-index:40;background:rgba(10,14,30,.6);display:flex;align-items:center;justify-content:center;padding:16px}
#aeFinP .c{background:var(--panel,#fff);color:var(--ink,#1a1d2b);border-radius:20px;padding:18px 18px 14px;max-width:440px;width:100%;max-height:88vh;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.45)}
#aeFinP h3{margin:0;font:800 18px var(--display,var(--body))}#aeFinP .nota{display:flex;align-items:center;gap:14px;margin:10px 0}
#aeFinP .n{font:900 46px/1 var(--body);color:#163a7a}#aeFinP .es{font-size:20px;letter-spacing:2px}
#aeFinP .fil{display:flex;justify-content:space-between;font:600 13px var(--body);padding:4px 0;border-bottom:1px solid var(--rule,#ddd)}
#aeFinP blockquote{margin:10px 0;padding:10px 12px;background:#eef3ff;border-left:4px solid #163a7a;border-radius:8px;font:500 14px/1.45 var(--body);color:#1a1d2b}
#aeFinP .rec{margin:10px 0;font:700 14px var(--body)}#aeFinP button{width:100%;margin-top:6px;border:0;border-radius:12px;padding:11px;font:800 15px var(--body);background:#163a7a;color:#fff;cursor:pointer}
#gpsMenu .aeSel .fil{display:flex;justify-content:space-between;font:600 12px var(--body);margin:3px 2px}#gpsMenu .aeSel .bar{height:6px;border-radius:3px;background:var(--rule,#ddd);margin:2px 2px 6px;overflow:hidden}#gpsMenu .aeSel .bar i{display:block;height:100%;background:#163a7a}
#gpsMenu .aeSel .op{display:flex;gap:6px;margin:4px 0 8px}#gpsMenu .aeSel .op button{flex:1;text-align:center;margin:0;padding:8px 4px;font:700 12px var(--body)}#gpsMenu .aeSel .op button.sel{background:#163a7a;color:#fff;border-color:#163a7a}
#gpsMenu button.aeCl{display:flex;align-items:center;gap:10px}#gpsMenu button.aeCl .i{font:400 22px/1 system-ui}#gpsMenu button.aeCl b{display:block}#gpsMenu button.aeCl small{display:block;opacity:.7;font-weight:500}
#gpsMenu button.aeCl[disabled]{opacity:.45;cursor:default}#gpsMenu button.aeCl[disabled]:hover{background:var(--panel);color:var(--ink)}
body.carrera #aeHud,body.rep #aeHud,body.carrera #aeDice,body.rep #aeDice{display:none!important}
@media (max-width:700px){#aeHud{top:calc(96px + env(safe-area-inset-top,0px))}#aeDice{bottom:calc(150px + env(safe-area-inset-bottom,0px));font-size:13px}}`;document.head.appendChild(st)}
const AEH=document.createElement('div');AEH.id='aeHud';AEH.hidden=true;
AEH.innerHTML='<span class="L">L</span><div class="t"></div><button class="bi" title="Intermitente izquierdo (Z)" aria-label="Intermitente izquierdo">⬅</button><button class="bd" title="Intermitente derecho (X)" aria-label="Intermitente derecho">➡</button><button class="x" title="Terminar la clase" aria-label="Terminar la clase">✕</button>';
document.body.appendChild(AEH);
const AEDI=document.createElement('div');AEDI.id='aeDice';AEDI.hidden=true;AEDI.innerHTML='<span class="a">👨‍🏫</span><div><small>Ramón · tu profesor</small><span class="tx"></span></div>';document.body.appendChild(AEDI);
const AEF=document.createElement('div');AEF.id='aeFinP';AEF.hidden=true;document.body.appendChild(AEF);
AEH.querySelector('.bi').onclick=()=>aeIntermitente(-1);AEH.querySelector('.bd').onclick=()=>aeIntermitente(1);AEH.querySelector('.x').onclick=()=>aeFin('abandono');
addEventListener('keydown',e=>{if(!AE.on||e.repeat)return;if(e.code==='KeyZ'||e.code==='Comma')aeIntermitente(-1);else if(e.code==='KeyX'||e.code==='Period')aeIntermitente(1)});
// ---------- el profesor habla (texto y, si quieres, voz)
let AE_VOZ=null;
function aeVoz(t){try{if(!AE.voz||!soundOn||!window.speechSynthesis)return;const S=speechSynthesis;if(!AE_VOZ){const v=S.getVoices();AE_VOZ=v.find(v=>/^es[-_]ES/i.test(v.lang))||v.find(v=>/^es/i.test(v.lang))||null}
 S.cancel();const u=new SpeechSynthesisUtterance(t.replace(/[«»]/g,''));u.lang='es-ES';if(AE_VOZ)u.voice=AE_VOZ;u.rate=1.05;u.pitch=.95;S.speak(u)}catch(e){}}
function aeDice(t,lvl=1,forzar=false){if(lvl>AE.charla)return false;if(!forzar&&AE.dT<2.4)return false;AE.dT=0;AEDI.querySelector('.tx').textContent=t;AEDI.hidden=false;clearTimeout(aeDice.t);aeDice.t=setTimeout(()=>AEDI.hidden=true,Math.max(3500,t.length*70));aeVoz(t);return true}
const AE_CHARLA=['Tranquilo, que no es un examen: hoy venimos a practicar.','Las cuestas de Vigo son la mejor escuela. Si aparcas aquí, aparcas en cualquier sitio.','Mira lejos, no al capó. Y suelta un poco los hombros.','Con este tiempo de Vigo, el paraguas siempre en el coche.','Mi primer coche fue un Seat Panda. Ese sí que no perdonaba.','Mira qué luces de Navidad. Este año Vigo se ha superado.','Las manos a las diez y diez, como te enseñé.','Anticípate: mira lo que hacen los de delante.'];
// ---------- intermitentes
function aeIntermitente(s){if(!AE.on)return;AE.BL=AE.BL===s?0:s;AE.blA=P.a;AE.blT=0;AE.blVisto=AE.BL?AE.BL:AE.blVisto;aeLucesInt();if(AE.BL)AE.blUlt={s:AE.BL,t:performance.now()/1000}}
function aeLucesInt(){const on=AE.BL&&((performance.now()/1000*3)|0)%2===0;for(const m of AE.luces||[])m.material.color.set(AE.BL&&Math.sign(m.userData.lado)===AE.BL&&on?0xffb020:0x5a4a2a);
 AEH.querySelector('.bi').classList.toggle('on',AE.BL===-1);AEH.querySelector('.bd').classList.toggle('on',AE.BL===1)}
function aeClic(){try{if(!AC||!soundOn)return;const t0=AC.currentTime,o=AC.createOscillator(),g=AC.createGain();o.type='square';o.frequency.value=1800;g.gain.setValueAtTime(.05,t0);g.gain.exponentialRampToValueAtTime(.0001,t0+.03);o.connect(g);g.connect(master);o.start(t0);o.stop(t0+.04)}catch(e){}}
// ---------- coche de la autoescuela (cartel L) y vuelta al coche de antes
function aeTex(txt,w,h,fs,bg,fg){const c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d');x.fillStyle=bg;x.fillRect(0,0,w,h);x.fillStyle=fg;x.font='900 '+fs+'px Arial Black,Arial,sans-serif';x.textAlign='center';x.textBaseline='middle';x.fillText(txt,w/2,h/2+2);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
let AE_TX=null;
function aeVestir(){const prev={ch:[...car.children],body:car.userData.body,tipo:car.userData.tipo,moto:P.vestidoMoto};
 vestirCoche(mkVehiculo('turismo',0xf4f4f2),'autoescuela');P.vestidoMoto=false;const k=1/.6;
 if(!AE_TX)AE_TX={L:new THREE.MeshBasicMaterial({map:aeTex('L',64,64,52,'#1f4fb0','#ffffff')}),A:new THREE.MeshBasicMaterial({map:aeTex('AUTOESCUELA',256,64,34,'#1f4fb0','#ffffff')})};
 const g=new THREE.Group();const W=.024,H=.011,D=.016,x0=-.004,y0=.0575;
 const caja=new THREE.Mesh(new THREE.BoxGeometry(W,H,D),new THREE.MeshStandardMaterial({color:0x1f4fb0,roughness:.45}));caja.position.set(x0,y0,0);g.add(caja);
 for(const s of[-1,1]){const pl=new THREE.Mesh(new THREE.PlaneGeometry(W*.94,H*.78),AE_TX.A);pl.position.set(x0,y0,s*(D/2+.0002));if(s<0)pl.rotation.y=Math.PI;g.add(pl);
  const pf=new THREE.Mesh(new THREE.PlaneGeometry(D*.7,H*.85),AE_TX.L);pf.position.set(x0+s*(W/2+.0002),y0,0);pf.rotation.y=s*Math.PI/2;g.add(pf)}
 // intermitentes en las cuatro esquinas (z>0: lado derecho)
 AE.luces=[];for(const fx of[.046,-.046])for(const z of[.0205,-.0205]){const m=new THREE.Mesh(new THREE.BoxGeometry(.006,.005,.005),new THREE.MeshBasicMaterial({color:0x5a4a2a}));m.position.set(fx+(fx>0?.0012:-.0012),.026,z);m.userData.lado=z;g.add(m);AE.luces.push(m)}
 g.position.multiplyScalar(k);g.scale.setScalar(k);car.add(g);AE.prev=prev}
function aeDesvestir(){const pv=AE.prev;AE.prev=null;AE.luces=[];if(!pv||car.userData.tipo!=='autoescuela')return;for(const c of [...car.children])car.remove(c);for(const c of pv.ch)car.add(c);car.userData.body=pv.body;car.userData.tipo=pv.tipo;P.vestidoMoto=pv.moto}
// ---------- geometría: cajas orientadas (choques, bordillos, plazas)
function aeObb(cx,cy,a,hl,hw){const fx=Math.cos(a),fy=-Math.sin(a);return{cx,cy,ax:[[fx,fy],[-fy,fx]],h:[hl,hw]}}
function aeChoca(A,B){for(const O of[A,B])for(let k=0;k<2;k++){const[ux,uy]=O.ax[k];
  const pa=A.h[0]*Math.abs(A.ax[0][0]*ux+A.ax[0][1]*uy)+A.h[1]*Math.abs(A.ax[1][0]*ux+A.ax[1][1]*uy),pb=B.h[0]*Math.abs(B.ax[0][0]*ux+B.ax[0][1]*uy)+B.h[1]*Math.abs(B.ax[1][0]*ux+B.ax[1][1]*uy);
  if(Math.abs((B.cx-A.cx)*ux+(B.cy-A.cy)*uy)>pa+pb)return false}return true}
const AE_CL=.047,AE_CW=.0225;   // medio largo y medio ancho del coche
function aeEsquinas(x,y,a){const fx=Math.cos(a),fy=-Math.sin(a),rx=-fy,ry=fx,o=[];for(const s of[1,-1])for(const t of[1,-1])o.push([x+fx*AE_CL*s+rx*AE_CW*t,y+fy*AE_CL*s+ry*AE_CW*t]);return o}
function aeEnPlaza(S,x,y,a,tol=.008){const fx=Math.cos(S.a),fy=-Math.sin(S.a),rx=-fy,ry=fx;let n=0;for(const[px,py]of aeEsquinas(x,y,a)){const u=(px-S.cx)*fx+(py-S.cy)*fy,v=(px-S.cx)*rx+(py-S.cy)*ry;if(Math.abs(u)<=S.hl+tol&&Math.abs(v)<=S.hw+tol)n++}return n}
const angD=(a,b)=>{let d=a-b;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;return d};
// ---------- zona de prácticas en el muelle (explanada al este del Areal)
const AEZ={x0:100.35,x1:101.85,y0:10.85,y1:11.85,gate:[100.5,11.45],entrada:[99.25,13.72]};
function aeZona(){aeZonaQuitar();aeCampa(true);const O=AE.objs,gy0=groundY((AEZ.x0+AEZ.x1)/2,(AEZ.y0+AEZ.y1)/2);AE.obst=[];AE.bord=[];
 const add=o=>{scene.add(o);O.push(o);return o};
 const Wm=(c,op=1)=>new THREE.MeshBasicMaterial({color:c,transparent:op<1,opacity:op,depthWrite:op>=1,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3});
 // asfalto de la explanada
 const NX=31,NY=21,pg=new THREE.PlaneGeometry(AEZ.x1-AEZ.x0,AEZ.y1-AEZ.y0,NX-1,NY-1);pg.rotateX(-Math.PI/2);const pp=pg.attributes.position,cx0=(AEZ.x0+AEZ.x1)/2,cy0=(AEZ.y0+AEZ.y1)/2;
 for(let i=0;i<pp.count;i++){const x=pp.getX(i)+cx0,y=pp.getZ(i)+cy0;pp.setY(i,groundY(x,y)+.0025)}pg.computeVertexNormals();
 const pad=new THREE.Mesh(pg,new THREE.MeshStandardMaterial({color:0x4a4e57,roughness:.95,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}));pad.position.set(cx0,0,cy0);pad.receiveShadow=true;add(pad);
 const alto=(x,y)=>groundY(x,y)+.0045;
 const linea=(ax,ay,bx,by,w=.004,col=0xf2f2ee,op=1)=>{const L=Math.hypot(bx-ax,by-ay),n=Math.max(1,Math.ceil(L/.05)),out=[];for(let q=0;q<n;q++){const x0=ax+(bx-ax)*q/n,y0=ay+(by-ay)*q/n,x1=ax+(bx-ax)*(q+1)/n,y1=ay+(by-ay)*(q+1)/n;
   const m=new THREE.Mesh(new THREE.PlaneGeometry(L/n+.0005,w),Wm(col,op));m.rotation.x=-Math.PI/2;m.rotation.z=Math.atan2(-(by-ay),bx-ax);m.position.set((x0+x1)/2,Math.max(alto(x0,y0),alto(x1,y1)),(y0+y1)/2);out.push(add(m))}return out[0]};
 const rect=(S,col=0xf2f2ee)=>{const fx=Math.cos(S.a),fy=-Math.sin(S.a),rx=-fy,ry=fx,c=[];for(const[s,t]of[[1,1],[1,-1],[-1,-1],[-1,1]])c.push([S.cx+fx*S.hl*s+rx*S.hw*t,S.cy+fy*S.hl*s+ry*S.hw*t]);for(let i=0;i<4;i++)linea(c[i][0],c[i][1],c[(i+1)%4][0],c[(i+1)%4][1],.0035,col)};
 const bordillo=(ax,ay,bx,by)=>{const L=Math.hypot(bx-ax,by-ay),a=Math.atan2(-(by-ay),bx-ax),m=new THREE.Mesh(new THREE.BoxGeometry(L,.012,.007),new THREE.MeshStandardMaterial({color:0xcfccc4,roughness:.8}));m.position.set((ax+bx)/2,Math.max(alto(ax,ay),alto(bx,by),alto((ax+bx)/2,(ay+by)/2))+.001,(ay+by)/2);m.rotation.y=a;m.castShadow=true;add(m);AE.bord.push(aeObb((ax+bx)/2,(ay+by)/2,a,L/2,.0035))};
 const aparcado=(x,y,a)=>{const T=['turismo','familiar','deportivo','turismo'],t=T[(Math.random()*T.length)|0],cs=VTIPOS[t].col,g=mkVehiculo(t,cs[(Math.random()*cs.length)|0]);g.position.set(x,groundY(x,y),y);g.rotation.y=a;
  for(const c of g.children)if(c.name==='haz')c.visible=false;add(g);const L={turismo:.094,familiar:.106,deportivo:.1}[t],W={turismo:.045,familiar:.046,deportivo:.05}[t];AE.obst.push(aeObb(x,y,a,L/2,W/2))};
 // contorno pintado y conos
 linea(AEZ.x0+.03,AEZ.y0+.03,AEZ.x1-.03,AEZ.y0+.03,.005,0xffc21a);linea(AEZ.x0+.03,AEZ.y1-.02,AEZ.x1-.03,AEZ.y1-.02,.005,0xffc21a);linea(AEZ.x1-.03,AEZ.y0+.03,AEZ.x1-.03,AEZ.y1-.02,.005,0xffc21a);
 const conoG=new THREE.ConeGeometry(.007,.022,10),conoM=new THREE.MeshStandardMaterial({color:0xff6a1a,roughness:.6});
 for(const[x,y]of[[AEZ.x0+.03,AEZ.y0+.03],[AEZ.x1-.03,AEZ.y0+.03],[AEZ.x1-.03,AEZ.y1-.02],[AEZ.x0+.03,AEZ.y1-.02],[AEZ.x0+.03,11.25],[AEZ.x0+.03,11.65]]){const c=new THREE.Mesh(conoG,conoM);c.position.set(x,alto(x,y)+.009,y);c.castShadow=true;add(c)}
 // cartel de la autoescuela a la entrada
 {const tx=aeTex('AUTOESCUELA · ZONA DE PRÁCTICAS',512,96,40,'#1f4fb0','#ffffff'),b=new THREE.Mesh(new THREE.BoxGeometry(.004,.035,.18),[MV(0x1f4fb0),MV(0x1f4fb0),MV(0x1f4fb0),MV(0x1f4fb0),new THREE.MeshBasicMaterial({map:tx}),new THREE.MeshBasicMaterial({map:tx})]);
  b.rotation.y=Math.PI/2;b.position.set(AEZ.x0+.12,alto(AEZ.x0+.12,AEZ.y1-.035)+.07,AEZ.y1-.035);add(b);b.castShadow=true;for(const s of[-1,1]){const p=new THREE.Mesh(new THREE.CylinderGeometry(.002,.002,.06,8),MV(0x8a8f99,.4,.6));p.position.set(AEZ.x0+.12+s*.08,alto(AEZ.x0+.12,AEZ.y1-.035)+.028,AEZ.y1-.035);add(p)}}
 // 1) en línea: junto al bordillo norte, entre dos coches (se entra yendo hacia el oeste: plaza a la derecha)
 bordillo(100.45,10.90,101.25,10.90);const SL={tipo:'linea',cx:100.80,cy:10.9375,a:Math.PI,hl:.08,hw:.0325,dos:true};
 for(const x of[100.53,100.66,100.94])aparcado(x,10.9375,Math.PI);for(const x of[101.06,101.16])linea(x-.08,10.97,x+.08,10.97,.0035);
 linea(100.47,10.97,101.0,10.97,.0035);for(const x of[100.595,100.72,100.88,101.0])linea(x,10.905,x,10.97,.0035);
 // 2) en batería: bordillo sur, plazas de 0,07 de ancho; se entra de frente (mirando al sur)
 bordillo(100.45,11.80,101.22,11.80);const SB={tipo:'bateria',cx:100.808,cy:11.7395,a:-Math.PI/2,hl:.0575,hw:.035};
 for(let i=0;i<10;i++){const x=100.52+i*.072;rect({cx:x,cy:11.7395,a:-Math.PI/2,hl:.0575,hw:.035});if([0,1,3,5,7,8].includes(i))aparcado(x,11.7395,Math.random()<.5?-Math.PI/2:Math.PI/2)}
 // 3) en oblicuo: a 60° del bordillo, también de frente
 bordillo(101.28,11.80,101.82,11.80);const ao=-Math.PI/2+.55,SO={tipo:'oblicuo',cx:101.494,cy:11.735,a:ao,hl:.0575,hw:.035};
 for(let i=0;i<6;i++){const x=101.33+i*.082;rect({cx:x,cy:11.735,a:ao,hl:.0575,hw:.035});if([1,3,5].includes(i))aparcado(x,11.735,ao)}
 AE.slots={linea:SL,bateria:SB,oblicuo:SO};
 // plaza objetivo: relleno amarillo que parpadea
 const hl=new THREE.Mesh(new THREE.PlaneGeometry(1,1),Wm(0xffc21a,.35));hl.rotation.x=-Math.PI/2;hl.visible=false;add(hl);AE.hl=hl}
// los coches nuevos de la campa del puerto dejan libre la zona de prácticas mientras dura la clase
function aeCampa(quitar){const m4=new THREE.Matrix4(),p=new THREE.Vector3(),cero=new THREE.Matrix4().makeScale(0,0,0);
 scene.traverse(o=>{if(!o.isInstancedMesh||o.name!=='campa_coches')return;if(quitar){if(o.userData.aeGuard)return;const G=[];
   for(let k=0;k<o.count;k++){o.getMatrixAt(k,m4);p.setFromMatrixPosition(m4);if(p.x>AEZ.x0-.06&&p.x<AEZ.x1+.06&&p.z>AEZ.y0-.06&&p.z<AEZ.y1+.06){G.push([k,m4.clone()]);o.setMatrixAt(k,cero)}}
   o.userData.aeGuard=G;o.instanceMatrix.needsUpdate=true}
  else if(o.userData.aeGuard){for(const[k,m]of o.userData.aeGuard)o.setMatrixAt(k,m);o.userData.aeGuard=null;o.instanceMatrix.needsUpdate=true}})}
function aeZonaQuitar(){aeCampa(false);for(const o of AE.objs){scene.remove(o);o.traverse&&o.traverse(q=>{if(q.isMesh&&q.geometry)q.geometry.dispose()})}AE.objs=[];AE.obst=[];AE.bord=[];AE.hl=null}
function aeMarcaPlaza(S){const h=AE.hl;if(!h)return;if(!S){h.visible=false;return}h.visible=true;h.scale.set(S.hl*2,S.hw*2,1);h.position.set(S.cx,groundY(S.cx,S.cy)+.005,S.cy);h.rotation.z=S.a}
// ---------- autoescuela: una calle tranquila cerca de Urzáiz (se calcula una vez con la red de calles)
let AE_SEDE=null;
function aeSede(){if(AE_SEDE)return AE_SEDE;const G=gpsGrafo();if(!G)return null;let b=-1,bd=1e9;
 for(let i=0;i<G.X.length;i++){if(G.comp[i]!==G.main||G.ADJ[i].length<2)continue;const c=G.CLS[i]||'m';if(c!=='m'&&c!=='E')continue;const d=Math.hypot(G.X[i]-100.6,G.Y[i]-19.3);if(d<bd&&cell(G.X[i],G.Y[i]).t===2){bd=d;b=i}}
 if(b<0)return null;const j=G.ADJ[b][0];let dx=G.X[j]-G.X[b],dy=G.Y[j]-G.Y[b];const l=Math.hypot(dx,dy)||1;dx/=l;dy/=l;
 AE_SEDE={x:G.X[b]-dy*.035,y:G.Y[b]+dx*.035,sx:G.X[b]-dy*.085,sy:G.Y[b]+dx*.085,a:Math.atan2(-dx,-dy),calle:calleEn(G.X[b],G.Y[b])};return AE_SEDE}
function aeSedeCartel(){const S=aeSede();if(!S)return;const g=new THREE.Group(),gy=groundY(S.sx,S.sy);
 const tx=aeTex('AUTOESCUELA',256,64,34,'#1f4fb0','#ffffff'),b=new THREE.Mesh(new THREE.BoxGeometry(.11,.03,.004),[MV(0x1f4fb0),MV(0x1f4fb0),MV(0x1f4fb0),MV(0x1f4fb0),new THREE.MeshBasicMaterial({map:tx}),new THREE.MeshBasicMaterial({map:tx})]);b.position.y=.085;g.add(b);
 const L=new THREE.Mesh(new THREE.BoxGeometry(.03,.03,.005),[MV(0xffffff),MV(0xffffff),MV(0xffffff),MV(0xffffff),AE_TX?AE_TX.L:new THREE.MeshBasicMaterial({map:aeTex('L',64,64,52,'#1f4fb0','#ffffff')}),AE_TX?AE_TX.L:new THREE.MeshBasicMaterial({map:aeTex('L',64,64,52,'#1f4fb0','#ffffff')})]);L.position.set(-.075,.085,0);g.add(L);
 const p=new THREE.Mesh(new THREE.CylinderGeometry(.002,.002,.1,8),MV(0x8a8f99,.4,.6));p.position.set(.05,.05,0);g.add(p);const p2=p.clone();p2.position.x=-.05;g.add(p2);
 g.position.set(S.sx,gy,S.sy);g.rotation.y=S.a+Math.PI/2;g.traverse(o=>{if(o.isMesh)o.castShadow=true});scene.add(g);AE.objs2=(AE.objs2||[]).concat([g])}
// ---------- rotondas: elige una salida y cuenta cuántas hay antes
const AE_ORD=['primera','segunda','tercera','cuarta','quinta','sexta'];
function aeRotonda(cx,cy,meta){const G=gpsGrafo();if(!G)return null;const ring=new Set();
 for(let a=-8;a<=8;a++)for(let b=-8;b<=8;b++){const L=G.cell.get((Math.floor(cx/.1)+a)+','+(Math.floor(cy/.1)+b));if(L)for(const i of L)if(G.CLS[i]==='R'&&G.comp[i]===G.main&&Math.hypot(G.X[i]-cx,G.Y[i]-cy)<.75)ring.add(i)}
 if(ring.size<3)return null;
 const libre=(u,k)=>{const v=G.ADJ[u][k],w=G.ADJ[u][k+1];return w<=Math.hypot(G.X[v]-G.X[u],G.Y[v]-G.Y[u])*1.6+1e-6};
 const cand=[];for(const r of ring)for(let k=0;k<G.ADJ[r].length;k+=2){const v=G.ADJ[r][k];if(ring.has(v)||G.CLS[v]==='R'||!libre(r,k))continue;cand.push([r,v])}
 let best=null,bs=1e9;
 for(const[r,v] of cand){let cur=v,prev=r;for(let s=0;s<8&&Math.hypot(G.X[cur]-cx,G.Y[cur]-cy)<.9;s++){let nx=-1,nd=-1;for(let k=0;k<G.ADJ[cur].length;k+=2){const q=G.ADJ[cur][k];if(q===prev||ring.has(q)||!libre(cur,k))continue;const d=Math.hypot(G.X[q]-cx,G.Y[q]-cy);if(d>nd){nd=d;nx=q}}if(nx<0)break;prev=cur;cur=nx}
  const tx=G.X[cur],ty=G.Y[cur];if(Math.hypot(tx-cx,ty-cy)<.4)continue;
  const pts=gpsCalcular(P.x,P.y,tx,ty);if(!pts||!GPSN)continue;const N=GPSN;let i0=-1;for(let i=0;i<N.length;i++)if(ring.has(N[i])){i0=i;break}if(i0<1)continue;let i1=i0;while(i1+1<N.length&&ring.has(N[i1+1]))i1++;
  if(i1>=N.length-1||N.slice(i1+1).some(u=>ring.has(u)))continue;
  let n=0;for(let k=i0;k<i1;k++){const u=N[k];for(let q=0;q<G.ADJ[u].length;q+=2){const w=G.ADJ[u][q];if(ring.has(w)||G.CLS[w]==='R'||w===N[k-1]||!libre(u,q))continue;n++}}
  const num=n+1;if(num<1||num>6)continue;const sc=(num===2||num===3?0:num===1?1.2:.8)+(meta?Math.hypot(tx-meta[0],ty-meta[1])*.12:0)+Math.random()*.3;if(sc<bs){bs=sc;best={x:tx,y:ty,n:num}}}
 return best}
// ---------- elegir la clase (en el menú del GPS)
function aeElegir(){if(REP.on||RACE.on)return;const L=document.getElementById('gpsLista');L.innerHTML='';const dv=document.createElement('div');dv.className='aeSel';
 const H=AED.hab,bar=(n,v)=>`<div class="fil"><span>${n}</span><span>${Math.round(v)}</span></div><div class="bar"><i style="width:${Math.max(2,Math.min(100,v))}%"></i></div>`;
 dv.innerHTML=`<div class="gpsSec">🚗 Autoescuela · clase práctica</div><div class="fil"><span>Clases hechas: <b>${AED.clases}</b></span><span>Mejor nota: <b>${AED.clases?AED.mejor.toFixed(1):'—'}</b></span></div>
 ${bar('🅿️ En línea',H.linea)}${bar('🅿️ En batería',H.bateria)}${bar('🅿️ En oblicuo',H.oblicuo)}${bar('🎛 Control',H.control)}${bar('↔ Intermitentes',H.intermitentes)}
 <div class="gpsSec">Profesor</div><div class="op ch"><button data-v="2">Hablador</button><button data-v="1">Normal</button><button data-v="0">Callado</button></div>
 <div class="op vz"><button data-v="1">🔊 Con voz</button><button data-v="0">🔇 Solo texto</button></div><div class="gpsSec">Elige la clase</div>`;
 L.appendChild(dv);
 const marca=()=>{dv.querySelectorAll('.ch button').forEach(b=>b.classList.toggle('sel',+b.dataset.v===AED.charla));dv.querySelectorAll('.vz button').forEach(b=>b.classList.toggle('sel',(+b.dataset.v===1)===!!AED.voz))};marca();
 dv.querySelectorAll('.ch button').forEach(b=>b.onclick=()=>{AED.charla=+b.dataset.v;aeGuardar();marca()});dv.querySelectorAll('.vz button').forEach(b=>b.onclick=()=>{AED.voz=b.dataset.v==='1';aeGuardar();marca()});
 for(const[k,v] of Object.entries(AE_VAR)){const b=document.createElement('button');b.className='aeCl';const bloq=AED.clases<v.req;
  b.innerHTML=`<span class="i">${bloq?'🔒':v.ico}</span><span><b>${v.n}</b><small>${bloq?'Se desbloquea con '+v.req+' clase'+(v.req>1?'s':'')+' hecha'+(v.req>1?'s':''):v.d}</small></span>`;b.disabled=bloq;
  b.onclick=()=>{document.getElementById('gpsMenu').hidden=true;aeEmpezar(k)};L.appendChild(b)}
 const v=document.createElement('button');v.textContent='← Volver';v.onclick=()=>document.getElementById('bGPS').click();L.appendChild(v);document.getElementById('gpsMenu').hidden=false}
// ---------- empezar / terminar
function aeEmpezar(v){if(REP.on||RACE.on)return;if(!driving||MODO!=='coche'){mostrar('🚗 Súbete a un coche para ir a la clase');return}
 if(TAXI.on)taxiFin('otro');if(AE.on)return;const S=aeSede();if(!S){mostrar('Cargando las calles… prueba en un momento');return}
 Object.assign(AE,{on:true,fase:'ir',var:v,charla:AED.charla,voz:AED.voz,li:0,mi:0,man:null,legs:[],park:{},t:0,dT:9,BL:0,turnosVistos:new Set(),
  st:{bord:0,roce:0,choque:0,intOk:0,intMal:0,vel:0,carril:0,brusco:0,ruta:0},ev:{},rr:0,cie:null,charT:0});
 try{gtvEv('mision/autoescuela','Misión autoescuela')}catch(e){}
 if(!AE.mk)AE.mk=txMarca();if(!AE.objs2||!AE.objs2.length)aeSedeCartel();
 AE.mk.position.set(S.x,groundY(S.x,S.y),S.y);AE.mk.visible=true;aeRuta(['🚗 Autoescuela'+(S.calle?' · '+S.calle:''),S.x,S.y]);
 AEH.hidden=false;aeHud();mostrar('🚗 Ve a la autoescuela'+(S.calle?' de '+S.calle:'')+': sigue la línea azul y para en la puerta')}
function aeFin(motivo){if(!AE.on)return;AE.on=false;const f=AE.fase;AE.fase='';if(GPS.taxi)gpsParar();GPS.taxi=false;
 if(AE.mk)AE.mk.visible=false;txQuitarP(AE.p);AE.p=null;for(const q of AE.ped)txQuitarP(q.p);AE.ped=[];aeZonaQuitar();AEH.hidden=true;AEDI.hidden=true;try{speechSynthesis.cancel()}catch(e){}
 window.AE_NOSTUCK=false;window.AE_TRAF=false;if(AE.cie){CIELO.modo=AE.cie.modo;CIELO.h=AE.cie.h;AE.cie=null;try{cielo(0)}catch(e){}}
 if(motivo!=='externo')aeDesvestir();else AE.prev=null;AE.BL=0;
 if(motivo==='abandono'||motivo==='otro')mostrar('🚗 Clase terminada antes de tiempo');else if(motivo==='salir')mostrar(f==='ir'?'🚗 Clase cancelada':'👨‍🏫 «¿A dónde vas? Así no se puede dar clase.» · Clase cancelada')}
window.aeSalir=()=>aeFin('salir');window.aeT={empezar:v=>aeEmpezar(v||'normal'),fin:()=>aeFin('abandono'),st:()=>AE,zona:()=>AEZ};
window.aeGolpe=()=>{if(AE.on&&AE.fase!=='ir'&&!aeEnZona())aeEvento('choque')};
function aeRuta(d){gpsIniciar(d);if(GPS.on){GPS.taxi=true;GPS_DEST.visible=false}AE.ruta=d;AE.lastPts=GPS.pts;return GPS.on}
function aeMuelle(){return Math.hypot(P.x-(AEZ.x0+AEZ.x1)/2,P.y-(AEZ.y0+AEZ.y1)/2)<3.4}   // explanada del muelle: allí se va fuera de la calzada
function aeEnZona(x=P.x,y=P.y){return x>AEZ.x0-.15&&x<AEZ.x1+.15&&y>AEZ.y0-.15&&y<AEZ.y1+.15}
// ---------- faltas: cada una con su espera para no contarla dos veces seguidas
const AE_FALTA={bord:['¡Cuidado, el bordillo!','¡Ese bordillo! Abre un poco más.'],roce:['¡Que rozas! Más despacio, que hay sitio.','Ojo con las distancias.'],choque:['¡Uy! Hay que mirar más.','Eso ha sido un golpe. Tranquilo, respira.'],
 vel:['Reduce, que aquí es a 50.','Vas rápido. Levanta el pie.'],carril:['Pégate a tu carril, a la derecha.','Mantén el carril, no te abras.'],brusco:['Más suave con el freno.','Suavidad, que llevas pasajero.'],contra:['¡Que vas en dirección contraria!'],zonavel:['Despacio, que estamos en la zona de prácticas.']};
function aeEvento(k,espera=2.5){const now=performance.now()/1000;if(AE.ev[k]&&now-AE.ev[k]<espera)return;AE.ev[k]=now;
 if(k==='contra'||k==='carril')AE.st.carril++;else if(k==='zonavel')AE.st.vel++;else AE.st[k]++;
 if(AE.man&&(k==='bord'||k==='roce'||k==='choque'))AE.man.contactos++;const L=AE_FALTA[k];aeDice(L[(Math.random()*L.length)|0],0,true)}
// ---------- tramos de la clase
function aePuntoCalle(nombre,x,y){const G=gpsGrafo();let b=-1,bd=1e9;for(let a=-12;a<=12;a++)for(let c=-12;c<=12;c++){const L=G.cell.get((Math.floor(x/.1)+a)+','+(Math.floor(y/.1)+c));if(!L)continue;for(const i of L){if(G.comp[i]!==G.main)continue;const d=Math.hypot(G.X[i]-x,G.Y[i]-y);if(d<bd&&(!nombre||calleEn(G.X[i],G.Y[i])===nombre)){bd=d;b=i}}}return b<0?null:[G.X[b],G.Y[b]]}
function aeTramos(){const T=[];
 if(AE.var!=='aparca'){
  const q=aePuntoCalle(null,103.1,21.0);if(q)T.push({id:'salida',d:['Calles tranquilas',q[0],q[1]],txt:'Venga, salimos. Primero unas calles tranquilas: sigue la línea azul y mira bien en los cruces.'});
  const u=aePuntoCalle('Rúa de Urzáiz',98.6,22.05)||aePuntoCalle(null,98.6,22.05);if(u)T.push({id:'urzaiz',d:['Rúa de Urzáiz',u[0],u[1]],txt:'Ahora salimos a Urzáiz. Avenida con tráfico: mantén tu carril y respeta el 50.'});
  const g=aePuntoCalle('Avenida da Gran Vía',94.35,28.4)||aePuntoCalle(null,94.35,28.4);if(g)T.push({id:'granvia',d:['Gran Vía',g[0],g[1]],txt:'Giramos a la Gran Vía. Carril derecho y sin cambiar de carril sin poner el intermitente.'});
  T.push({id:'rot',rot:[93.75,30.18],meta:[96.9,13.8],nom:'Praza de España'});
  T.push({id:'rot',rot:[96.89,13.78],meta:AEZ.entrada,nom:'Beiramar'})}
 T.push({id:'zona',d:['Zona de prácticas (muelle)',AEZ.entrada[0],AEZ.entrada[1]],txt:'Reduce un poco, que vamos a practicar aparcamiento. Vamos a la explanada del muelle.'});return T}
function aeTramo(){const L=AE.legs[AE.li];if(!L){aePatio();return}AE.fase='tramo';AE.recalc=0;
 if(L.id==='rot'){const r=aeRotonda(L.rot[0],L.rot[1],L.meta);if(!r){AE.li++;aeTramo();return}L.d=['Rotonda de '+L.nom+' · '+AE_ORD[r.n-1]+' salida',r.x,r.y];L.n=r.n;
  aeDice('En la rotonda de '+L.nom+', toma la '+AE_ORD[r.n-1]+' salida. Intermitente a la derecha antes de salir.',0,true)}
 else aeDice(L.txt,0,true);
 aeRuta(L.d);const e=GPS.pts?GPS.pts[GPS.pts.length-1]:[L.d[1],L.d[2]];L.fin=e;if(L.id!=='zona'){AE.mk.position.set(e[0],groundY(e[0],e[1]),e[1]);AE.mk.visible=true}else AE.mk.visible=false}
// ---------- aparcamientos
const AE_MAN=['linea','bateria','oblicuo','salida'];
const AE_INTRO={linea:['Aquí a la derecha, aparca en línea entre esos dos coches.','Pon el intermitente y acércate despacio.'],bateria:['Ahora entra de frente en ese hueco.','Intermitente hacia el hueco y despacito.'],
 oblicuo:['Prueba a aparcar en diagonal en esa zona.','Entra de frente, siguiendo la línea de la plaza.'],salida:['Ahora sal del sitio con cuidado y reincorpórate.','Intermitente, mira por el retrovisor y sal a la entrada de la zona.']};
function aePatio(){AE.fase='patio';if(!AE.objs.length||AE.nG!==GROUND.length){aeZona();AE.nG=GROUND.length}AE.mi=0;window.AE_NOSTUCK=true;if(GPS.taxi)gpsParar();aeManObra()}
function aeManObra(){const k=AE_MAN[AE.mi];if(!k){aeVuelta();return}const S=k==='salida'?null:AE.slots[k];
 AE.man={k,S,t:0,quieto:0,dentro:0,contactos:0,blOk:false,dijo:{},salio:false};aeMarcaPlaza(S);
 if(k==='salida'){const g=AEZ.gate;AE.mk.position.set(g[0],groundY(g[0],g[1]),g[1]);AE.mk.visible=true}else AE.mk.visible=false;
 const I=AE_INTRO[k];aeDice(I[0],0,true);setTimeout(()=>{if(AE.on&&AE.man&&AE.man.k===k)aeDice(I[1],1,true)},3200)}
function aeNotaPlaza(M){const S=M.S,fx=Math.cos(S.a),fy=-Math.sin(S.a),rx=-fy,ry=fx,du=(P.x-S.cx)*fx+(P.y-S.cy)*fy,dv=(P.x-S.cx)*rx+(P.y-S.cy)*ry;
 let da=Math.abs(angD(P.a,S.a)),rev=false;if(da>Math.PI/2){da=Math.PI-da;rev=!S.dos}
 const mv=S.hw-AE_CW,mu=S.hl-AE_CL;let n=10-Math.min(4,Math.abs(dv)/mv*2.6)-Math.min(2,Math.abs(du)/mu*1.2)-Math.min(4,da/.22*2.5)-(rev?1.5:0)-M.contactos*1-(M.blOk?0:.5);
 n=Math.max(1,Math.round(n*2)/2);return{n,rev,da,dv,du}}
function aeManTick(dt){const M=AE.man;if(!M)return;M.t+=dt;const v=Math.abs(P.v);
 if(M.k==='salida'){const S=AE.slots.oblicuo;const n=aeEnPlaza(S,P.x,P.y,P.a,.02);if(!M.salio){if(AE.BL)M.blOk=true;if(n<2&&M.t>.5){M.salio=true;if(!M.blOk){AE.st.intMal++;aeDice('¡El intermitente antes de salir!',0,true)}else{AE.st.intOk++;aeDice('Bien, intermitente puesto. Sal despacio.',2)}}}
  const g=AEZ.gate;if(Math.hypot(g[0]-P.x,g[1]-P.y)<.16){const nota=Math.max(1,10-(M.blOk?0:3)-M.contactos*2-(M.t>60?1:0));AE.park.salida={n:nota};aeDice(nota>=8?'Bien, sales con cuidado. Así se hace.':'Vale, fuera. Más cuidado al salir la próxima vez.',0,true);AE.mi++;AE.man=null;setTimeout(()=>{if(AE.on)aeManObra()},2500)}
  else if(M.t>120){AE.park.salida={n:3};aeDice('Bueno, lo dejamos aquí. Volvemos.',0,true);AE.mi++;AE.man=null;setTimeout(()=>{if(AE.on)aeManObra()},2000)}return}
 const S=M.S,d=Math.hypot(S.cx-P.x,S.cy-P.y),n=aeEnPlaza(S,P.x,P.y,P.a);
 // intermitente hacia la plaza al acercarte
 if(d<.55&&n<4&&AE.BL){const rx=Math.sin(P.a),ry=Math.cos(P.a),lado=Math.sign((S.cx-P.x)*rx+(S.cy-P.y)*ry)||1;if(AE.BL===lado)M.blOk=true}
 if(d<.35&&v>.2&&!M.dijo.lento){M.dijo.lento=1;aeDice('Reduce, despacito, que estamos aparcando.',1)}
 if(v<.012)M.quieto+=dt;else M.quieto=0;
 if(n>=1&&n<4&&M.quieto>.8&&M.t-(M.dijo.pista||0)>6){M.dijo.pista=M.t;const r=aeNotaPlaza(M);aeDice(r.da>.3?'Gira más, todavía te queda sitio.':Math.abs(r.dv)>S.hw-AE_CW+.006?'Te has quedado separado: corrige un poco.':'Un poco más… ya casi está.',1)}
 if(n===4&&v>.03&&!M.dijo.frena){M.dijo.frena=1;aeDice('Recto ahora… así. Frena.',1)}
 if(n===4&&v<.012){M.dentro+=dt;if(M.dentro>1){const r=aeNotaPlaza(M);AE.park[M.k]={n:r.n};if(M.blOk)AE.st.intOk++;else AE.st.intMal++;
   const nm=AE_NOM[M.k];let t=r.n>=8.5?'Bien, has quedado bastante centrado.':r.n>=6.5?'Vale, aparcado. Un poco '+(r.da>.12?'torcido':'descentrado')+', pero bien.':'Aparcado… aunque regular. Habrá que repetir el '+nm+'.';
   if(r.rev)t+=' Te pedí de frente, pero vale.';if(!M.blOk)t+=' Y te ha faltado el intermitente.';aeDice(t,0,true);aviso('🅿️ '+r.n.toFixed(1).replace('.0',''),1.4);
   AE.mi++;AE.man=null;aeMarcaPlaza(null);setTimeout(()=>{if(AE.on&&AE.fase==='patio')aeManObra()},3500)}}else M.dentro=0;
 if(M.t>150){AE.park[M.k]={n:2};aeDice('Bueno, lo dejamos: este habrá que repetirlo.',0,true);AE.mi++;AE.man=null;aeMarcaPlaza(null);setTimeout(()=>{if(AE.on)aeManObra()},2500)}}
// ---------- vuelta y nota final
function aeVuelta(){AE.fase='vuelta';window.AE_NOSTUCK=false;aeMarcaPlaza(null);const S=aeSede();aeDice('Venga, volvemos a la autoescuela.',0,true);AE.mk.position.set(S.x,groundY(S.x,S.y),S.y);AE.mk.visible=true;aeRuta(['🚗 Autoescuela',S.x,S.y]);AE.comT=12;AE.comI=0}
function aeComentarios(){const C=[],pk=AE.park,H=AED.hab,s=AE.st;
 for(const k of['linea','bateria','oblicuo']){const r=pk[k];if(!r)continue;if(r.n>=8.5&&(r.n*10>H[k]+5||!AED.clases))C.push('Muy bien, hoy has mejorado mucho en el aparcamiento '+AE_NOM[k]+'.');else if(r.n<6)C.push('El '+(k==='linea'?'de línea':k==='bateria'?'de batería':'oblicuo')+' te ha costado un poco, habrá que repetirlo.')}
 if(s.bord>=2)C.push(C.length?'Bien en general, pero cuidado con los bordillos.':'Cuidado con los bordillos: ' +s.bord+' veces.');
 if(s.intMal>=2)C.push('Acuérdate del intermitente antes de girar o aparcar.');if(s.vel>=2)C.push('Vas un poco rápido: respeta los límites.');
 if(s.roce+s.choque>=1)C.push('Ojo con las distancias: '+(s.roce+s.choque)+' '+(s.roce+s.choque>1?'roces o golpes':'roce o golpe')+'.');if(s.brusco>=2)C.push('Más suavidad con el freno y el volante.');
 if(s.carril>=2)C.push('Trabaja la posición en el carril.');if(!C.length)C.push('¡Clase de diez! Así da gusto.');return C.slice(0,4)}
function aeNota(){const s=AE.st,pk=AE.park;const cond=Math.max(0,10-s.bord*.6-s.roce*.8-s.choque*1.5-s.intMal*.35-s.vel*.5-s.carril*.5-s.brusco*.3-s.ruta*.3);
 const ps=['linea','bateria','oblicuo','salida'].map(k=>pk[k]?pk[k].n:null).filter(x=>x!=null),apar=ps.length?ps.reduce((a,b)=>a+b,0)/ps.length:5;
 const w=AE.var==='aparca'?.25:.45;return{cond,apar,nota:Math.round((cond*w+apar*(1-w))*10)/10}}
function aeTerminar(){const N=aeNota(),C=aeComentarios(),s=AE.st,pk=AE.park;AE.fase='fin';
 let mon=Math.round(20+N.nota*6+(AE.var==='noche'?10:0)+(AE.var==='trafico'?10:0));taxiMon(mon);
 const antes=AED.clases;AED.clases++;AED.mejor=Math.max(AED.mejor,N.nota);const H=AED.hab,mez=(a,b)=>Math.round(a?(a*.6+b*.4):b);
 for(const k of['linea','bateria','oblicuo'])if(pk[k])H[k]=mez(H[k],pk[k].n*10);H.control=mez(H.control,N.cond*10);const ti=s.intOk+s.intMal;if(ti)H.intermitentes=mez(H.intermitentes,s.intOk/ti*100);aeGuardar();
 const desb=Object.values(AE_VAR).filter(v=>v.req>antes&&v.req<=AED.clases).map(v=>v.ico+' '+v.n);
 const est='★★★★★'.slice(0,Math.round(N.nota/2))+'☆☆☆☆☆'.slice(0,5-Math.round(N.nota/2));
 const fil=(a,b)=>`<div class="fil"><span>${a}</span><span>${b}</span></div>`;
 AEF.innerHTML=`<div class="c"><h3>👨‍🏫 Fin de la clase · ${AE_VAR[AE.var].n}</h3><div class="nota"><span class="n">${N.nota.toFixed(1).replace('.',',')}</span><div><div class="es">${est}</div><small>Conducción ${N.cond.toFixed(1).replace('.',',')} · Aparcamiento ${N.apar.toFixed(1).replace('.',',')}</small></div></div>
 ${['linea','bateria','oblicuo','salida'].filter(k=>pk[k]).map(k=>fil('🅿️ '+AE_NOM[k][0].toUpperCase()+AE_NOM[k].slice(1),pk[k].n.toFixed(1).replace('.',',')+' / 10')).join('')}
 ${fil('Bordillos',s.bord)}${fil('Roces y golpes',s.roce+s.choque)}${fil('Intermitentes',s.intOk+' bien · '+s.intMal+' olvidados')}${fil('Exceso de velocidad',s.vel)}${fil('Carril / dirección',s.carril)}${fil('Brusquedad',s.brusco)}
 <blockquote>«${C.join(' ')}»</blockquote><div class="rec">🪙 +${mon} monedas (tienes ${TAXI.mon}) · ⭐ habilidades actualizadas${desb.length?'<br>🔓 Desbloqueado: '+desb.join(', '):''}</div><button>Cerrar</button></div>`;
 AEF.hidden=false;AEF.querySelector('button').onclick=()=>{AEF.hidden=true};aeDice(C[0],0,true);
 const p=AE.p;AE.p=null;if(p){p.visible=true;const S=aeSede();AE.ped.push({p,t:0,x0:P.x,y0:P.y,x1:S.sx,y1:S.sy})}
 setTimeout(()=>{if(AE.fase==='fin')aeFin('ok')},2600)}
// ---------- HUD
function aeHud(){const t=AEH.querySelector('.t'),s=AE.st;let paso='';
 if(AE.fase==='ir')paso='Ve a la autoescuela';else if(AE.fase==='subir'||AE.fase==='espera')paso='El profesor se sube…';else if(AE.fase==='tramo'){const L=AE.legs[AE.li];paso=L?(L.id==='rot'?'Rotonda de '+L.nom+(L.n?' · '+AE_ORD[L.n-1]+' salida':''):L.id==='zona'?'A la zona de prácticas':L.d[0]):''}
 else if(AE.fase==='patio')paso=AE.man?'Aparcamiento '+AE_NOM[AE.man.k].replace('salida del aparcamiento','· salida'):'Zona de prácticas';else if(AE.fase==='vuelta')paso='Vuelta a la autoescuela';else if(AE.fase==='fin')paso='Clase terminada';
 const sec=AE_VAR[AE.var].n,h=`<b>${paso}</b><small>${sec} · 🚧 ${s.bord} · 💥 ${s.roce+s.choque} · ↔ ${s.intOk}/${s.intOk+s.intMal}</small>`;if(h!==AE.hudH){AE.hudH=h;t.innerHTML=h}}
// ---------- cada fotograma (mientras se conduce)
let AE_PAD=[false,false];
function aeTick(dt){
 for(let i=AE.ped.length-1;i>=0;i--){const q=AE.ped[i];q.t+=dt;const k=Math.min(1,q.t/1.4),x=q.x0+(q.x1-q.x0)*k,y=q.y0+(q.y1-q.y0)*k;q.p.position.set(x,groundY(x,y),y);q.p.rotation.y=Math.atan2(-(q.y1-q.y0),q.x1-q.x0);animPersona(q.p,q.t,1);if(q.t>2.2){txQuitarP(q.p);AE.ped.splice(i,1)}}
 if(!AE.on)return;if(RACE.on||REP.on){aeFin('externo');return}
 if(AE.fase==='fin')return;
 if(MODO!=='coche'||(AE.fase!=='ir'&&AE.fase!=='subir'&&car.userData.tipo!=='autoescuela')){aeFin(MODO==='coche'?'externo':'salir');return}
 const now=performance.now()/1000,v=Math.abs(P.v);AE.dT+=dt;AE.t+=dt;
 if(AE.mk&&AE.mk.visible){AE.mk.userData.f.position.y=.14+Math.sin(now*3)*.02;AE.mk.userData.f.rotation.y=now*2;AE.mk.userData.r.material.opacity=.55+.3*Math.sin(now*4)}
 if(AE.hl&&AE.hl.visible)AE.hl.material.opacity=.22+.15*Math.sin(now*5);
 if(AE.objs.length&&(AE.campaT=(AE.campaT||0)-dt)<=0){AE.campaT=1;aeCampa(true)}
 // mando: cruceta ◀ ▶ = intermitentes
 try{if(PAD.i!=null){const g=navigator.getGamepads()[PAD.i];if(g){for(const[j,b,s]of[[0,14,-1],[1,15,1]]){const p=!!(g.buttons[b]&&g.buttons[b].pressed);if(p&&!AE_PAD[j])aeIntermitente(s);AE_PAD[j]=p}}}}catch(e){}
 // intermitente: parpadeo, tic-tac y se quita solo al acabar el giro
 if(AE.BL){AE.blT+=dt;const f=((now*3)|0)%2;if(f!==AE.blF){AE.blF=f;aeClic()}if((Math.abs(angD(P.a,AE.blA))>1.1&&!keys.left&&!keys.right)||AE.blT>25){AE.BL=0}}aeLucesInt();
 if(AE.fase==='ir'){const S=aeSede(),d=Math.hypot(S.x-P.x,S.y-P.y);if(!GPS.on&&(AE.rr-=dt)<=0)AE.rr=aeRuta(['🚗 Autoescuela',S.x,S.y])?2:8;
  if(d<.24&&v<.06){AE.fase='subir';AE.mk.visible=false;if(GPS.taxi)gpsParar();const p=txPersona();p.position.set(S.sx,groundY(S.sx,S.sy),S.sy);AE.p=p;AE.anim={t:0,x0:S.sx,y0:S.sy};aeDice('¡Buenas! Soy Ramón. Hoy toca práctica, sin nervios: no es un examen.',0,true)}
  else if(d<.5&&v>=.06&&!AE.avP){AE.avP=1;mostrar('Para en la puerta de la autoescuela')}aeHud();return}
 if(AE.fase==='subir'){const a=AE.anim;a.t+=dt;const k=Math.min(1,a.t/1.1),x=a.x0+(P.x-a.x0)*k,y=a.y0+(P.y-a.y0)*k;AE.p.position.set(x,groundY(x,y),y);AE.p.rotation.y=Math.atan2(-(P.y-a.y0),P.x-a.x0);animPersona(AE.p,a.t,1);
  if(k>=1){AE.fase='espera';AE.p.visible=false;aeVestir();if(AE.var==='noche'){AE.cie={modo:CIELO.modo,h:CIELO.h};CIELO.modo='noche';CIELO.h=23.5;try{cielo(0)}catch(e){}}if(AE.var==='trafico')window.AE_TRAF=true;
   AE.legs=aeTramos();AE.li=0;setTimeout(()=>{if(AE.on){aeDice(AE.var==='noche'?'Hoy de noche: luces puestas y más atención, que se ve menos.':AE.var==='trafico'?'Hoy hay mucho tráfico: paciencia y distancia de seguridad.':'Usa los intermitentes con Z y X (o ⬅ ➡). Cuando quieras, arrancamos.',0,true);setTimeout(()=>{if(AE.on&&AE.fase==='espera')aeTramo()},3800)}},1600)}
  aeHud();return}
 if(AE.fase==='espera'){aeHud();return}
 // ---- faltas mientras se conduce
 AE.pv=AE.pv??P.v;const acc=(P.v-AE.pv)/Math.max(dt,1e-3);AE.pv=P.v;if(acc<-1.75&&P.v>.42)aeEvento('brusco',3);
 const enZ=aeEnZona();
 if(enZ){if(v>.22)aeEvento('zonavel',5)}
 else{const kmh=v*125,lim=50*1.12;if(kmh>lim){AE.velT=(AE.velT||0)+dt;if(AE.velT>1.5)aeEvento('vel',6)}else AE.velT=0;
  const t=cell(P.x,P.y).t,lejos=!aeMuelle();
  if(t===1&&v>.04&&lejos){AE.acT=(AE.acT||0)+dt;if(AE.acT>.3)aeEvento('bord',3)}else AE.acT=0;
  const ct=document.getElementById('contra');if(ct&&!ct.hidden&&v>.05)aeEvento('contra',6);
  for(const c of TRAF){if(!c.g.visible)continue;if(Math.abs(c.x-P.x)<.07&&Math.abs(c.y-P.y)<.07&&Math.hypot(c.x-P.x,c.y-P.y)<.058){aeEvento(v>.25?'choque':'roce',2);break}}
  // posición en el carril: lejos de la línea azul durante un rato
  if(GPS.on&&GPS.pts&&v>.1){const Q=GPS.pts;let bd=1e9;for(let i=Math.max(0,GPS.idx-2);i<Math.min(Q.length-1,GPS.idx+4);i++){const[ax,ay]=Q[i],[bx,by]=Q[i+1],vx=bx-ax,vy=by-ay,L2=vx*vx+vy*vy||1e-9;let u=((P.x-ax)*vx+(P.y-ay)*vy)/L2;u=Math.max(0,Math.min(1,u));bd=Math.min(bd,Math.hypot(ax+vx*u-P.x,ay+vy*u-P.y))}
   if(bd>.075&&bd<.4){AE.caT=(AE.caT||0)+dt;if(AE.caT>2)aeEvento('carril',8)}else AE.caT=0}}
 // ---- choques y bordillos en la zona de prácticas: el coche no los atraviesa
 if(enZ&&AE.obst){const A=aeObb(P.x,P.y,P.a,AE_CL,AE_CW);let hit=null;for(const o of AE.obst)if(aeChoca(A,o)){hit='c';break}if(!hit)for(const o of AE.bord)if(aeChoca(A,o)){hit='b';break}
  if(hit&&AE.ult){const B=aeObb(AE.ult[0],AE.ult[1],AE.ult[2],AE_CL,AE_CW);let antes=false;for(const o of AE.obst.concat(AE.bord))if(aeChoca(B,o)){antes=true;break}
   if(!antes){P.x=AE.ult[0];P.y=AE.ult[1];P.a=AE.ult[2];car.position.x=P.x;car.position.z=P.y;car.rotation.y=P.a;aeEvento(hit==='b'?'bord':v>.2?'choque':'roce',1.2);P.v=-P.v*.15}}
  AE.ult=[P.x,P.y,P.a]}else AE.ult=[P.x,P.y,P.a];
 // ---- intermitentes antes de cada giro de la ruta
 if(AE.fase==='tramo'||AE.fase==='vuelta'){if(GPS.on&&GPS.turns&&GPS.acc){const s=GPS.acc[GPS.idx]||0;
   for(const T of GPS.turns){if(Math.abs(T.da)<.75)continue;const p=GPS.pts[T.i],key=Math.round(p[0]*30)+','+Math.round(p[1]*30);if(AE.turnosVistos.has(key))continue;const lado=T.da>0?1:-1,falta=T.s-s;
    if(falta<.55&&falta>-.05){if(AE.BL===lado)T.ok=true;if(falta<.42&&!T.dicho){T.dicho=1;if(!T.ok)aeDice(lado>0?'Ahora a la derecha. Intermitente.':'Ahora a la izquierda. Intermitente.',AE.st.intOk+AE.st.intMal<3?1:2)}}
    if(falta<=-.05&&falta>-.6){AE.turnosVistos.add(key);if(T.ok||(AE.blUlt&&AE.blUlt.s===lado&&now-AE.blUlt.t<6)){AE.st.intOk++;aeDice('Bien señalizado.',2)}else{AE.st.intMal++;aeDice('¡El intermitente! Hay que señalizar antes de girar.',0)}}}}
  // la ruta se ha recalculado: te has salido o equivocado de salida
  if(GPS.on&&GPS.pts!==AE.lastPts&&aeMuelle())AE.lastPts=GPS.pts;
  if(GPS.on&&GPS.pts!==AE.lastPts){AE.lastPts=GPS.pts;AE.st.ruta++;const L=AE.legs[AE.li];aeDice(L&&L.id==='rot'&&AE.fase==='tramo'?'Esa no era la salida. No pasa nada, recalculamos.':'Por ahí no era. Sigue la línea azul.',0,true)}
  if(!GPS.on&&(AE.rr-=dt)<=0){AE.rr=2;if(AE.fase==='vuelta'){const S=aeSede();aeRuta(['🚗 Autoescuela',S.x,S.y])}else{const L=AE.legs[AE.li];if(L)aeRuta(L.d)}}
  AE.charT=(AE.charT||0)+dt;if(AE.charT>28&&AE.charla>=2&&AE.dT>8){AE.charT=0;aeDice(AE_CHARLA[(Math.random()*AE_CHARLA.length)|0],2)}}
 if(AE.fase==='tramo'){const L=AE.legs[AE.li],e=L&&L.fin;if(e&&Math.hypot(e[0]-P.x,e[1]-P.y)<.3){if(L.id==='rot')aeDice('Bien la rotonda.',1,true);AE.li++;AE.mk.visible=false;if(L.id==='zona'){if(GPS.taxi)gpsParar();AE.fase='alpatio';aeZona();AE.nG=GROUND.length;const g=AEZ.gate;AE.mk.position.set(g[0],groundY(g[0],g[1]),g[1]);AE.mk.visible=true;aeDice('Entra en la explanada, a la zona de prácticas. Despacio.',0,true)}else setTimeout(()=>{if(AE.on&&AE.fase==='tramo')aeTramo()},600)}}
 else if(AE.fase==='alpatio'){if(Math.hypot(AEZ.gate[0]-P.x,AEZ.gate[1]-P.y)<.25||(P.x>AEZ.x0&&P.y<AEZ.y1&&P.y>AEZ.y0)){AE.mk.visible=false;aePatio()}}
 else if(AE.fase==='patio')aeManTick(dt);
 else if(AE.fase==='vuelta'){AE.comT-=dt;if(AE.comT<=0&&AE.comI<2){AE.comT=14;const C=aeComentarios();if(C[AE.comI])aeDice(C[AE.comI],1);AE.comI++}
  const S=aeSede();if(Math.hypot(S.x-P.x,S.y-P.y)<.26&&v<.06){if(GPS.taxi)gpsParar();AE.mk.visible=false;aeTerminar()}}
 aeHud()}
