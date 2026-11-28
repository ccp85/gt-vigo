/* tutorial: al empezar a jugar por primera vez, recorrido por los botones con «Siguiente» y «Saltar tutorial» */
(()=>{
const $=id=>document.getElementById(id),B=document.body;
const TACTIL=!!window.LITE||matchMedia('(pointer:coarse)').matches;
let visto=false;try{visto=localStorage.getItem('gtvigo_tutorial')==='1'}catch(e){}
if(/[?&]tutorial=1/.test(location.search))visto=false;
const ev=(n,t)=>{try{window.gtvEv&&window.gtvEv(n,t)}catch(e){}};

// pasos: sel = lo que se ilumina (si no se ve en pantalla, el paso se salta solo); sin sel, la caja sale centrada
const PASOS=[
 {t:'👋 ¡Bienvenido a GT Vigo!',x:'Te enseño en un momento para qué sirve cada botón. Pulsa <b>Siguiente</b> para ir viéndolos o <b>Saltar tutorial</b> si ya sabes jugar.'},
 TACTIL?{sel:['#pad .flechas','#joy'],t:'🕹️ Dirección',x:'Con el joystick (o las flechas ◀ ▶) giras a izquierda y derecha. A pie, el joystick te mueve en cualquier dirección.'}
       :{t:'🎮 Conducir',x:'<b>Flechas</b> o <b>W A S D</b> para acelerar, frenar y girar.<br><b>E</b> para bajarte o subirte a un vehículo · <b>H</b> claxon.<br>¿Tienes mando? Conéctalo y pulsa cualquier botón: también se juega con él.'},
 {sel:['#pad .g:last-child'],t:'⏫ Acelerar y frenar',x:'▲ acelera y ▼ frena (si sigues pulsando, marcha atrás).'},
 {sel:['#bAcc'],t:'🚪 Bajar y subir',x:'Bájate para ir a pie, nadar en la playa o subirte a otro coche, moto, lancha o helicóptero. Cuando tienes algo cerca, el botón cambia y te dice qué puedes hacer.'},
 {sel:['#bPita'],t:'📯 Claxon',x:'Pita para avisar a los coches y peatones.'},
 {sel:['#pad .alt [data-k="alt_up"]','#pad .alt [data-k="alt_dn"]'],t:'🚁 Altura',x:'En el helicóptero, ⤒ sube y ⤓ baja.'},
 {sel:['#mini'],t:'🗺️ Minimapa',x:'Te enseña dónde estás y las calles de alrededor. '+(TACTIL?'Tócalo':'Haz clic en él')+' para acercar o alejar el zoom.'},
 {sel:['#calle'],t:'🪧 Calle',x:'El nombre de la calle o el sitio por el que vas.'},
 {sel:['#vel'],t:'⏱️ Velocímetro',x:'Tu velocidad en km/h.'},
 {sel:['#lim'],t:'🚸 Límite de velocidad',x:'El límite de la calle. '+(TACTIL?'Tócalo':'Haz clic o pulsa <b>L</b>')+' para cambiarlo.'},
 {sel:['#bGPS'],t:'🧭 GPS',x:'Elige a dónde ir y una línea azul te guía hasta allí. Arriba del todo están las <b>🎯 Misiones</b>: taxi, autoescuela, surf en Patos, basket en Samil…'},
 {sel:['#bRadio'],t:'📻 Radio',x:'La radio del coche: elige emisora y canción.'+(TACTIL?'':' Teclado: <b>M</b> siguiente canción, <b>N</b> lista de emisoras.')+' Suena cuando vas en un vehículo.'},
 {sel:['#bCam'],t:'🎥 Cámara',x:'Cambia la vista: detrás del coche, más lejos, desde dentro…'+(TACTIL?'':' Teclado: <b>C</b>.')},
 {sel:['#bSnd'],t:'🔊 Sonido',x:'Enciende o apaga el sonido del juego.'},
 {sel:['#bFps'],t:'⏱ 30 / 60 fps',x:'Imágenes por segundo. Si el juego va a tirones, prueba con 30.'+(TACTIL?'':' Teclado: <b>P</b>.')},
 {sel:['#bCal'],t:'🎨 Calidad gráfica',x:'Elige cómo se ven los gráficos: <b>Auto</b> (el juego decide según tu aparato), <b>Baja</b> para móviles antiguos, <b>Media</b>, <b>Alta</b> o <b>Máxima</b> (hierba, árboles con viento y reflejos; necesita un equipo potente). Al cambiarla, el juego se recarga.'},
 {sel:['#bFull'],t:'⛶ Pantalla completa',x:'Juega a pantalla completa, sin las barras del navegador.'},
 {sel:['#bCoche'],t:'✕ Salir',x:'Sales a la maqueta de Vigo. Desde allí, con <b>🗺️ Mapa</b>, eliges otro sitio de la ría o cambias de vehículo.'},
 TACTIL?null:{t:'⌨️ Más teclas',x:'<b>G</b> calidad de los gráficos (alta o rendimiento) · <b>L</b> límite de velocidad · <b>C</b> cámara · <b>M</b> / <b>N</b> radio · <b>P</b> fps.'},
 {sel:['#bTut'],t:'❓ Tutorial',x:'Si quieres repasarlo, aquí lo tienes siempre.'},
 {t:'🚗 ¡A jugar!',x:'Ya lo tienes todo. Recorre Vigo, las playas y la ría, y busca misiones en el GPS. ¡Buen viaje!',fin:true},
].filter(Boolean);

const st=document.createElement('style');st.textContent=`
#tutGT{position:fixed;inset:0;z-index:300;font-family:var(--body,system-ui),system-ui,sans-serif;color:#fff;touch-action:none}
#tutGT[hidden]{display:none}
#tutGT .velo{position:absolute;inset:0;background:rgba(6,8,20,.62)}
#tutGT.foco .velo{background:transparent}
#tutGT .luz{position:absolute;border-radius:14px;box-shadow:0 0 0 3px #ffb03a,0 0 22px 6px rgba(255,140,40,.55),0 0 0 9999px rgba(6,8,20,.62);transition:all .35s cubic-bezier(.2,.8,.2,1);pointer-events:none;animation:tutLate 1.4s ease-in-out infinite}
@keyframes tutLate{50%{box-shadow:0 0 0 3px #ffd24a,0 0 32px 10px rgba(255,160,50,.7),0 0 0 9999px rgba(6,8,20,.62)}}
#tutGT .caja{position:absolute;width:min(360px,calc(100vw - 24px));box-sizing:border-box;padding:16px 16px 14px;border-radius:18px;background:linear-gradient(160deg,rgba(32,30,60,.97),rgba(18,18,38,.97));border:1px solid rgba(255,255,255,.16);box-shadow:0 14px 44px rgba(0,0,0,.55);transition:left .35s cubic-bezier(.2,.8,.2,1),top .35s cubic-bezier(.2,.8,.2,1)}
#tutGT .num{font:700 11px/1 system-ui;letter-spacing:.14em;color:#ff8a4a;text-transform:uppercase}
#tutGT h3{margin:6px 0 6px;font:400 21px/1.15 "Russo One","Arial Black",Impact,system-ui,sans-serif;letter-spacing:.02em}
#tutGT p{margin:0 0 14px;font:500 15px/1.45 system-ui;color:rgba(255,255,255,.88)}
#tutGT p b{color:#ffd24a;font-weight:700}
#tutGT .bar_{display:flex;align-items:center;gap:8px}
#tutGT button{font:700 14px system-ui;border-radius:12px;padding:10px 14px;cursor:pointer;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff}
#tutGT button:focus-visible{outline:2px solid #ffd24a;outline-offset:2px}
#tutGT .sal{background:transparent;border-color:transparent;color:rgba(255,255,255,.65);padding-left:4px;padding-right:4px;margin-right:auto;text-decoration:underline;text-underline-offset:3px}
#tutGT .sig{background:linear-gradient(135deg,#ff6a3d,#e0352b);border:none;box-shadow:0 6px 18px rgba(224,53,43,.45);padding:10px 18px}
#tutGT .ant[disabled]{opacity:.35;cursor:default}
#tutGT .pts{display:flex;gap:4px;margin:0 0 12px}
#tutGT .pts i{flex:1;height:3px;border-radius:2px;background:rgba(255,255,255,.18)}
#tutGT .pts i.on{background:#ff8a4a}
#bTut{display:none}
body.drive .bar #bTut{display:inline-block!important}
@media (max-width:700px){body.drive .bar #bTut{position:fixed;left:max(12px,env(safe-area-inset-left,0px));top:calc(160px + env(safe-area-inset-top,0px));width:34px;min-width:0;height:34px;padding:0!important;border-radius:50%;font-size:15px;line-height:1;z-index:5}}
body.carrera .bar #bTut,body.rep .bar #bTut,body.solo .bar #bTut{display:none!important}`;
document.head.appendChild(st);

const T=document.createElement('div');T.id='tutGT';T.hidden=true;T.setAttribute('role','dialog');T.setAttribute('aria-modal','true');T.setAttribute('aria-label','Tutorial');
T.innerHTML='<div class="velo"></div><div class="luz" hidden></div><div class="caja"><div class="num"></div><h3></h3><p></p><div class="pts"></div><div class="bar_"><button class="sal">Saltar tutorial</button><button class="ant" aria-label="Anterior">◀</button><button class="sig">Siguiente ▶</button></div></div>';
B.appendChild(T);
const luz=T.querySelector('.luz'),caja=T.querySelector('.caja'),bSig=T.querySelector('.sig'),bAnt=T.querySelector('.ant'),bSal=T.querySelector('.sal');

// botón ❓ en la barra del juego para volver a verlo
{const bar=document.querySelector('.bar');if(bar){const b=document.createElement('button');b.id='bTut';b.textContent='❓';b.title='Tutorial: para qué sirve cada botón';b.setAttribute('aria-label','Tutorial');
 const f=$('bFull');f&&f.parentNode===bar?bar.insertBefore(b,f):bar.appendChild(b);b.onclick=e=>{e.stopPropagation();abrir()}}}

const visible=el=>{if(!el||el.closest('#tutGT'))return null;const r=el.getBoundingClientRect();if(r.width<4||r.height<4)return null;const cs=getComputedStyle(el);if(cs.visibility==='hidden'||+cs.opacity<.1)return null;
 if(r.right<0||r.bottom<0||r.left>innerWidth||r.top>innerHeight)return null;return r};
function rectDe(p){if(!p.sel)return null;let u=null;
 for(const s of p.sel)for(const el of document.querySelectorAll(s)){const r=visible(el);if(!r)continue;
  u=u?{l:Math.min(u.l,r.left),t:Math.min(u.t,r.top),r:Math.max(u.r,r.right),b:Math.max(u.b,r.bottom)}:{l:r.left,t:r.top,r:r.right,b:r.bottom}}
 return u}
let lista=[],i=0,abierto=false;
function pinta(){const p=lista[i],r=p.r=rectDe(p)||p.r;
 caja.querySelector('.num').textContent=(i+1)+' / '+lista.length;caja.querySelector('h3').textContent=p.t;caja.querySelector('p').innerHTML=p.x;
 caja.querySelector('.pts').innerHTML=lista.map((_,k)=>'<i'+(k<=i?' class="on"':'')+'></i>').join('');
 bAnt.disabled=i===0;bSig.textContent=p.fin?'¡A jugar! 🚗':'Siguiente ▶';bSal.style.visibility=p.fin?'hidden':'visible';
 T.classList.toggle('foco',!!r);luz.hidden=!r;
 const W=innerWidth,H=innerHeight,cw=caja.offsetWidth,ch=caja.offsetHeight,m=12;
 if(!r){caja.style.left=Math.round((W-cw)/2)+'px';caja.style.top=Math.round((H-ch)/2)+'px';return}
 const pd=6;luz.style.left=(r.l-pd)+'px';luz.style.top=(r.t-pd)+'px';luz.style.width=(r.r-r.l+pd*2)+'px';luz.style.height=(r.b-r.t+pd*2)+'px';
 let x=(r.l+r.r)/2-cw/2,y;
 if(r.b+pd+m+ch<=H-m)y=r.b+pd+m;else if(r.t-pd-m-ch>=m)y=r.t-pd-m-ch;
 else{y=Math.max(m,Math.min(H-ch-m,(r.t+r.b)/2-ch/2));x=r.l-pd-m-cw>=m?r.l-pd-m-cw:r.r+pd+m}
 caja.style.left=Math.round(Math.max(m,Math.min(W-cw-m,x)))+'px';caja.style.top=Math.round(y)+'px'}
function ir(k){if(k<0)return;if(k>=lista.length){cerrar(true);return}i=k;pinta();if(!TACTIL)bSig.focus({preventScroll:true})}
function abrir(){if(abierto)return;
 lista=PASOS.filter(p=>!p.sel||rectDe(p));if(!lista.length)return;
 abierto=true;window.__TUT=true;T.hidden=false;try{document.activeElement&&document.activeElement.blur()}catch(e){}
 i=0;pinta();if(!TACTIL)bSig.focus({preventScroll:true});ev('tutorial/abierto','Tutorial abierto')}
function cerrar(completo){if(!abierto)return;abierto=false;window.__TUT=false;T.hidden=true;
 try{localStorage.setItem('gtvigo_tutorial','1')}catch(e){}visto=true;
 ev(completo?'tutorial/completo':'tutorial/saltado',completo?'Tutorial completo':'Tutorial saltado')}
bSig.onclick=()=>ir(i+1);bAnt.onclick=()=>ir(i-1);bSal.onclick=()=>cerrar(false);
// mientras está abierto, el teclado solo mueve el tutorial (el coche no se mueve)
addEventListener('keydown',e=>{if(!abierto)return;
 if(e.code==='Escape'){cerrar(false)}else if(e.code==='ArrowRight'||e.code==='KeyD'||e.code==='Space'){ir(i+1)}else if(e.code==='ArrowLeft'||e.code==='KeyA'){ir(i-1)}
 else if(e.code==='Enter'){const a=document.activeElement;if(!(a&&T.contains(a)&&a.tagName==='BUTTON'))ir(i+1);else return}
 else if(e.code==='Tab')return;
 e.preventDefault();e.stopImmediatePropagation()},true);
addEventListener('resize',()=>{if(abierto)setTimeout(()=>{lista[i].r=null;pinta()},60)});
// si se sale del juego (o empieza una carrera o el reparto), se cierra sin darlo por visto
function fuera(){return !B.classList.contains('drive')||B.classList.contains('carrera')||B.classList.contains('rep')||B.classList.contains('solo')||B.classList.contains('cine')}
// la primera vez: cuando ya se está jugando (llegada terminada, sin pantallas de carga ni menús encima)
let listoT=0;
setInterval(()=>{if(abierto){if(fuera()){abierto=false;window.__TUT=false;T.hidden=true}return}
 if(visto||fuera()){listoT=0;return}
 const tapa=['load','selz','gpsMenu','radioPanel','nFin','rFin','selCar','iGo'].some(id=>{const e=$(id);return e&&!e.hidden&&e.getClientRects().length})||(()=>{const s=$('bSaltar');return s&&!s.hidden})();
 if(tapa){listoT=0;return}
 if(!listoT)listoT=performance.now();else if(performance.now()-listoT>1500){listoT=0;abrir()}},400);
window.tutorialGT=abrir;
})();
