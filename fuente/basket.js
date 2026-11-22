// ================= Minijuego: Basket en las canchas de Samil · basket.js (lo mete edit_basket.py) =================
// Detrás del paseo de Samil hay una cancha de baloncesto pintada de colores (mural propio con la paleta de las canchas reales:
// morado, azul, rosa, amarillo y turquesa). En el GPS, «🎯 Misiones» → «🏀 Basket en Samil»: la línea azul lleva a la cancha;
// al llegar sale la ficha (dónde está, cómo llegar…) y eliges modo: 1x1, 3x3 (media pista), 5x5 (pista entera) o entrenamiento.
//  - Cámara de tele: desde la banda, alta, siguiendo el balón (como en los juegos de basket de consola).
//  - Ataque: ◀ ▶ ▲ ▼ moverse (Mayús o joystick a tope: correr) · 🏀 Tirar (mantén y suelta en lo alto del salto; cerca del aro,
//    bandeja o mate) · 👉 Pasar (al compañero hacia donde apuntas) · ⚡ Finta (crossover para irte del defensor).
//    Siempre llevas al jugador que tiene el balón.
//  - Defensa: ✋ Tapón (salta) · 🖐️ Robar · 🔄 Cambiar (al defensor más cerca del balón).
//  - 1x1 y 3x3 (reglas de 3x3): dentro 1 punto, fuera de la línea 2; tras rebote defensivo, robo o canasta hay que sacar el balón
//    fuera de la línea antes de tirar. 1x1 a 11 o 3 min; 3x3 a 21 o 5 min (posesión de 12 s). 5x5: 2 y 3 puntos, 4 min, 24 s.
//    Empate al final: canasta de oro.
//  - Entrenamiento: 60 s tirando desde donde quieras; el balón vuelve solo. Racha de 3 = +1.
// Monedas 🪙 al ganar y récords guardados en el navegador (gtvigo_basket). Con window.__BKAUTO=1 tu jugador juega solo (pruebas).
const BKK=.02,BKX=14,BKZ=7.5,BKHX=12.425,BKRY=3.05,BKRR=.225,BKBR=.12,BKBX=12.8,BKG=9.8;
const BKC={G:null,dyn:null,aro:{},red:{},suelo:0,mk:null};
const BK={on:false,ficha:false,ruta:false,cerca:false,modo:'3x3',J:[],T:[[],[]],ball:null,pos:-1,fase:'',muertaT:0,muertaFn:null,
 reloj:0,c24:0,pts:[0,0],tt:0,yo:null,k:{l:0,r:0,u:0,d:0,a:0,b:0,c:0,sh:0},joy:{x:0,y:0,on:false},padX:0,padY:0,padSh:0,limpiar:[false,false],
 msgT:0,cam:{p:new THREE.Vector3(),l:new THREE.Vector3(),ini:false},st:null,oro:false,ent:null,auto:false,spotT:0};
let BKD=null;try{BKD=JSON.parse(localStorage.getItem('gtvigo_basket')||'null')}catch(e){}
BKD=Object.assign({modo:'3x3',dif:1,hora:null,gan:{},jug:{},mejorEnt:0,partidos:0},BKD||{});
function bkGuardar(){try{localStorage.setItem('gtvigo_basket',JSON.stringify(BKD))}catch(e){}}
const BK_MODOS={'1x1':{n:'1 contra 1',ico:'🧍',k:1,full:false,meta:11,dur:180,c24:12,mon:20},'3x3':{n:'3 contra 3',ico:'👥',k:3,full:false,meta:21,dur:300,c24:12,mon:30},
 '5x5':{n:'5 contra 5',ico:'🏟️',k:5,full:true,meta:0,dur:240,c24:24,mon:40},'ent':{n:'Entrenamiento',ico:'🎯',k:1,full:false,meta:0,dur:60,c24:0,mon:0}};
const BK_DIF=[{n:'Fácil',ia:.78,df:.6},{n:'Normal',ia:1,df:1},{n:'Difícil',ia:1.12,df:1.35}];
const BK_EQ=[{n:'SAMIL',cam:0xec4f8f,ribete:0xffffff,pant:0x6a4fe0,acento:0xf5d33a,css:'#ec4f8f'},{n:'RÍA',cam:0xf5c400,ribete:0x1f3fbf,pant:0x1f3fbf,acento:0xffffff,css:'#f5c400'}];
MISIONES.push({id:'basket',ico:'🏀',n:'Basket en Samil',d:'Minijuego en las canchas del paseo de Samil · 1x1, 3x3, 5x5',da:'Vas camino de Samil · toca para cancelar',ir:()=>basketIr(),on:()=>BK.ruta,fin:()=>basketCancelar()});
// ---- dónde va la cancha: en la franja entre el paseo y la avenida de Samil (lo llama samTrasPaseo antes de poner aparcamientos)
function bkSitio(F){const pts=F.filter(f=>f&&f[2]>63.3&&f[2]<65.15).map(f=>[(f[0]+f[1])/2,f[2]]);if(pts.length<8)return null;
 let mx=0,my=0;for(const p of pts){mx+=p[0];my+=p[1]}mx/=pts.length;my/=pts.length;let sxy=0,syy=0;for(const p of pts){sxy+=(p[0]-mx)*(p[1]-my);syy+=(p[1]-my)**2}
 const b=syy>0?sxy/syy:0,l=Math.hypot(b,1),ex=[-b/l,-1/l],ez=[-ex[1],ex[0]];   // ex: a lo largo de la costa (hacia el norte) · ez: hacia la avenida
 return{cx:mx,cy:my,ex,ez,hl:16*BKK,hw:9.5*BKK,rot:Math.atan2(-ex[1],ex[0])}}
function bkDentroM(x,y,m){const B=SAM.bk;if(!B)return false;const dx=x-B.cx,dy=y-B.cy,u=dx*B.ex[0]+dy*B.ex[1],w=dx*B.ez[0]+dy*B.ez[1];return Math.abs(u)<B.hl+m&&Math.abs(w)<B.hw+m}
function bkFilaToca(x0,x1,y){for(let x=x0;x<=x1+1e-6;x+=.02)if(bkDentroM(x,y,.05))return true;return false}
// ---- estilos
{const st=document.createElement('style');st.textContent=`
body.bkg header,body.bkg #lim,body.bkg #stream,body.bkg #radioOSD,body.bkg #bNoche,body.bkg .bar,body.bkg #pad,body.bkg #mini,body.bkg #vel,body.bkg #calle,body.bkg #gps,body.bkg #bAcc,body.bkg #taxiHud,body.bkg #contra,body.bkg #aviso,body.bkg #rCuenta,body.bkg #joy,body.bkg #radio,body.bkg #radioPanel,body.bkg .hint{display:none!important}
#bkFicha{position:fixed;inset:0;z-index:40;background:rgba(30,16,60,.55);display:flex;align-items:center;justify-content:center;padding:14px}
#bkFicha[hidden],#bkHud[hidden]{display:none!important}
#bkFicha .c{background:#fffdf7;color:#1d1640;border-radius:20px;max-width:470px;width:100%;max-height:92vh;overflow:auto;box-shadow:0 10px 40px rgba(0,0,0,.45);font:500 13px var(--body)}
#bkFicha .cab{position:relative;height:120px;border-radius:20px 20px 0 0;overflow:hidden;background:#8f6fe6}
#bkFicha .cab i{position:absolute;display:block}
#bkFicha .cab .sello{position:absolute;left:12px;bottom:10px;background:#fff;color:#1d1640;font:800 11px var(--body);letter-spacing:.06em;border-radius:6px;padding:3px 7px}
#bkFicha .cab .bal{position:absolute;right:16px;top:14px;font:400 58px/1 system-ui;filter:drop-shadow(0 4px 6px rgba(0,0,0,.35))}
#bkFicha .in{padding:14px 16px 16px}
#bkFicha h2{margin:0;font:800 22px var(--display,var(--body))}#bkFicha .sub{margin:2px 0 10px;opacity:.7}
#bkFicha ul{list-style:none;margin:0 0 10px;padding:0}#bkFicha li{display:flex;gap:8px;padding:5px 0;border-top:1px solid #ece4f6;line-height:1.35}#bkFicha li i{font-style:normal;flex:none;width:22px;text-align:center}
#bkFicha .prog{background:#f4f0fc;border-radius:12px;padding:8px 10px;margin:8px 0}#bkFicha .prog b{font-weight:800}
#bkFicha .opt{margin:8px 0 2px;font:700 11px var(--body);letter-spacing:.06em;text-transform:uppercase;opacity:.65}
#bkFicha .sel{display:flex;gap:6px;flex-wrap:wrap}#bkFicha .sel button{flex:1;min-width:84px;border:2px solid #e2daf2;background:#fff;border-radius:10px;padding:7px 6px;font:700 12px var(--body);cursor:pointer;color:#1d1640}
#bkFicha .sel button small{display:block;font:600 10px var(--body);opacity:.65}
#bkFicha .sel button.on{border-color:#7a4fe0;background:#efe8ff}
#bkFicha .acc{display:flex;gap:8px;margin:12px -16px -16px;padding:10px 16px 14px;position:sticky;bottom:0;background:linear-gradient(180deg,rgba(255,253,247,.85),#fffdf7 30%)}#bkFicha .acc button{flex:1;border:0;border-radius:12px;padding:11px;font:800 15px var(--body);cursor:pointer}
#bkFicha .acc .go{background:linear-gradient(135deg,#ec4f8f,#7a4fe0);color:#fff}#bkFicha .acc .no{flex:.6;background:#efecf4;color:#1d1640}
#bkFicha .res{text-align:center;padding:6px 0 2px}#bkFicha .res .p{font:900 38px/1 var(--body)}#bkFicha .res small{display:block;opacity:.7;margin-top:4px}
#bkFicha .gana{background:#fff4cf;border-radius:10px;padding:6px 10px;margin:6px 0;font-weight:700}
#bkHud{position:fixed;inset:0;z-index:20;pointer-events:none;font:600 13px var(--body);color:#fff;user-select:none;-webkit-user-select:none}
#bkHud .mar{position:absolute;top:calc(8px + env(safe-area-inset-top,0px));left:50%;transform:translateX(-50%);display:flex;align-items:stretch;gap:0;background:rgba(16,12,40,.82);border-radius:12px;overflow:hidden;box-shadow:0 3px 12px rgba(0,0,0,.3);pointer-events:auto}
#bkHud .mar .eq{display:flex;align-items:center;gap:6px;padding:4px 10px;font:900 13px var(--body);letter-spacing:.04em}
#bkHud .mar .eq b{font:900 22px/1 var(--body);min-width:26px;text-align:center}
#bkHud .mar .eq i{width:8px;height:22px;border-radius:3px;display:block}
#bkHud .mar .ce{padding:3px 10px;text-align:center;background:rgba(255,255,255,.08)}#bkHud .mar .ce b{display:block;font:900 17px/1.1 var(--body)}#bkHud .mar .ce small{font:800 11px var(--body);color:#ffcf3a}
#bkHud .x{position:absolute;top:calc(10px + env(safe-area-inset-top,0px));right:max(10px,env(safe-area-inset-right,0px));border:0;background:rgba(16,12,40,.72);color:#fff;border-radius:999px;width:36px;height:36px;font:800 14px var(--body);cursor:pointer;pointer-events:auto}
#bkHud .modo{position:absolute;top:calc(12px + env(safe-area-inset-top,0px));left:max(10px,env(safe-area-inset-left,0px));background:rgba(16,12,40,.6);border-radius:10px;padding:4px 9px;font:700 11px var(--body)}
#bkHud .msg{position:absolute;top:30%;left:50%;transform:translate(-50%,-50%);text-align:center;font:900 32px/1.1 var(--body);text-shadow:0 3px 12px rgba(0,0,0,.6);white-space:nowrap;opacity:0;transition:opacity .2s}
#bkHud .msg small{display:block;font:700 15px var(--body)}#bkHud .msg.on{opacity:1;animation:bkPop .35s}
@keyframes bkPop{0%{transform:translate(-50%,-50%) scale(.6)}70%{transform:translate(-50%,-50%) scale(1.12)}100%{transform:translate(-50%,-50%) scale(1)}}
#bkHud .med{position:absolute;bottom:calc(118px + env(safe-area-inset-bottom,0px));left:50%;transform:translateX(-50%);width:min(230px,52vw);height:14px;border-radius:8px;background:rgba(16,12,40,.7);border:2px solid #fff;overflow:hidden}
#bkHud .med[hidden]{display:none}#bkHud .med i{position:absolute;left:0;top:0;bottom:0;width:0;background:#fff}#bkHud .med u{position:absolute;top:0;bottom:0;background:#3fe07a;opacity:.85}
#bkHud .tip{position:absolute;bottom:calc(92px + env(safe-area-inset-bottom,0px));left:50%;transform:translateX(-50%);font:600 12px var(--body);background:rgba(16,12,40,.55);padding:4px 10px;border-radius:10px;white-space:nowrap;max-width:94vw;overflow:hidden;text-overflow:ellipsis}
#bkHud .zj{position:absolute;left:0;bottom:0;width:48%;height:62%;pointer-events:auto;touch-action:none}
#bkHud .jb{position:absolute;width:116px;height:116px;margin:-58px 0 0 -58px;border-radius:50%;border:3px solid rgba(255,255,255,.7);background:rgba(16,12,40,.35);display:none}
#bkHud .jb i{position:absolute;left:50%;top:50%;width:48px;height:48px;margin:-24px 0 0 -24px;border-radius:50%;background:rgba(255,255,255,.85)}
#bkHud .jb.on{display:block}
#bkHud .bt{position:absolute;right:max(12px,env(safe-area-inset-right,0px));bottom:calc(12px + env(safe-area-inset-bottom,0px));width:212px;height:176px;pointer-events:none}
#bkHud .bt button{position:absolute;border-radius:50%;border:3px solid rgba(255,255,255,.85);background:rgba(16,12,40,.55);color:#fff;font:800 11px var(--body);touch-action:none;pointer-events:auto;cursor:pointer;padding:0}
#bkHud .bt button span{display:block;font:400 26px/1 system-ui;margin-bottom:1px}#bkHud .bt button.on{background:rgba(236,79,143,.85)}#bkHud .bt button.off{opacity:.4}
#bkHud .bt .bA{width:92px;height:92px;right:0;bottom:0}#bkHud .bt .bB{width:70px;height:70px;right:100px;bottom:0}#bkHud .bt .bC{width:66px;height:66px;right:26px;bottom:102px}
#bkHud .bt .bA span{font-size:32px}
@media (pointer:fine){#bkHud .bt,#bkHud .zj{opacity:.72}}
@media (max-width:700px){#bkHud .msg{font-size:25px}#bkHud .mar .eq{padding:3px 7px;font-size:11px}#bkHud .mar .eq b{font-size:18px}#bkHud .modo{display:none}}`;document.head.appendChild(st)}
// ---- HTML: ficha y marcador
const BKF=document.createElement('div');BKF.id='bkFicha';BKF.hidden=true;document.body.appendChild(BKF);
const BKH=document.createElement('div');BKH.id='bkHud';BKH.hidden=true;BKH.innerHTML=`<div class="modo"></div>
<div class="mar"><div class="eq e0"><i></i><span>SAMIL</span><b>0</b></div><div class="ce"><b class="rl">3:00</b><small class="c24">12</small></div><div class="eq e1"><b>0</b><span>RÍA</span><i></i></div></div>
<button class="x" title="Salir del basket" aria-label="Salir del basket">✕</button><div class="msg"></div><div class="med" hidden><u></u><i></i></div><div class="tip"></div>
<div class="zj"><div class="jb"><i></i></div></div>
<div class="bt"><button data-k="c" class="bC"><span>⚡</span>Finta</button><button data-k="b" class="bB"><span>👉</span>Pasar</button><button data-k="a" class="bA"><span>🏀</span>Tirar</button></div>`;document.body.appendChild(BKH);
BKH.querySelector('.x').onclick=()=>bkTerminar('menu');
BKH.querySelector('.e0 i').style.background=BK_EQ[0].css;BKH.querySelector('.e1 i').style.background=BK_EQ[1].css;
BKH.querySelectorAll('.bt button').forEach(b=>{const k=b.dataset.k;
 const on=e=>{e.preventDefault();e.stopPropagation();if(!BK.k[k]){BK.k[k]=1;bkBoton(k,true)}b.classList.add('on')},off=e=>{if(BK.k[k]){BK.k[k]=0;bkBoton(k,false)}b.classList.remove('on')};
 b.addEventListener('pointerdown',on);b.addEventListener('pointerup',off);b.addEventListener('pointercancel',off);b.addEventListener('pointerleave',off)});
// joystick: aparece donde pones el dedo en la mitad izquierda
{const zj=BKH.querySelector('.zj'),jb=zj.querySelector('.jb'),kn=jb.querySelector('i');let id=null,ox=0,oy=0;
 zj.addEventListener('pointerdown',e=>{e.preventDefault();id=e.pointerId;zj.setPointerCapture(id);const r=zj.getBoundingClientRect();ox=e.clientX;oy=e.clientY;jb.style.left=(ox-r.left)+'px';jb.style.top=(oy-r.top)+'px';jb.classList.add('on');BK.joy.on=true;BK.joy.x=BK.joy.y=0;kn.style.transform=''});
 zj.addEventListener('pointermove',e=>{if(e.pointerId!==id)return;let dx=e.clientX-ox,dy=e.clientY-oy;const l=Math.hypot(dx,dy),R=50;if(l>R){dx*=R/l;dy*=R/l}BK.joy.x=dx/R;BK.joy.y=-dy/R;kn.style.transform=`translate(${dx}px,${dy}px)`});
 const fin=e=>{if(e.pointerId!==id)return;id=null;jb.classList.remove('on');BK.joy.on=false;BK.joy.x=BK.joy.y=0};zj.addEventListener('pointerup',fin);zj.addEventListener('pointercancel',fin)}
// teclado (antes que el resto del juego)
const BK_TECLA={ArrowLeft:'l',KeyA:'l',ArrowRight:'r',KeyD:'r',ArrowUp:'u',KeyW:'u',ArrowDown:'d',KeyS:'d',Space:'a',KeyJ:'a',KeyK:'b',KeyE:'b',KeyL:'c',KeyQ:'c',ShiftLeft:'sh',ShiftRight:'sh'};
addEventListener('keydown',e=>{if(!BK.on&&!BK.ficha)return;const c=e.code;
 if(BK.ficha){if(c==='Escape'){const b=BKF.querySelector('.no');b&&b.click()}else if(c==='Enter'&&!e.repeat){const b=BKF.querySelector('.go');b&&b.click()}if(!/^Tab$/.test(c)){e.stopImmediatePropagation();if(c!=='Enter'||document.activeElement===document.body)e.preventDefault()}return}
 if(c==='Escape'){bkTerminar('menu')}else if(BK_TECLA[c]){const k=BK_TECLA[c];if(!BK.k[k]&&!e.repeat){BK.k[k]=1;bkBoton(k,true)}}else if(c==='KeyM'||c==='KeyN'||c==='KeyR')return;
 e.preventDefault();e.stopImmediatePropagation()},true);
addEventListener('keyup',e=>{if(!BK.on)return;const k=BK_TECLA[e.code];if(k&&BK.k[k]){BK.k[k]=0;bkBoton(k,false)}e.stopImmediatePropagation()},true);
// mando: stick/cruceta mover · Ⓧ tirar/tapón · Ⓐ pasar/robar · Ⓑ finta/cambiar · RT correr · Menú salir (lo llama padTick)
function bkPad(b,ax,dn){const P_=k=>!!(b[k]&&b[k].pressed);let x=Math.abs(ax[0]||0)<.2?0:ax[0],y=Math.abs(ax[1]||0)<.2?0:-ax[1];if(P_(14))x=-1;if(P_(15))x=1;if(P_(12))y=1;if(P_(13))y=-1;
 BK.padX=x;BK.padY=y;BK.padSh=(b[7]&&b[7].value>.4)||P_(5)?1:0;
 const bt=(i,k)=>{const p=P_(i);if(p&&!BK['pd'+k]){BK['pd'+k]=1;bkBoton(k,true)}else if(!p&&BK['pd'+k]){BK['pd'+k]=0;bkBoton(k,false)}};bt(2,'a');bt(0,'b');bt(1,'c');if(dn(9))bkTerminar('menu')}
// ---- la cancha (siempre en el mundo, aunque no juegues)
const bkSm=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t)};
function bkTexCancha(){const LT=!!window.LITE,W=LT?1024:2048,H=Math.round(W*19/32),ppm=W/32,c=document.createElement('canvas');c.width=W;c.height=H;const g=c.getContext('2d');
 const X=x=>(x+16)*ppm,Z=z=>(z+9.5)*ppm,R=r=>r*ppm;let rs=7;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const poly=(col,pts)=>{g.fillStyle=col;g.beginPath();pts.forEach((p,i)=>i?g.lineTo(X(p[0]),Z(p[1])):g.moveTo(X(p[0]),Z(p[1])));g.closePath();g.fill()};
 const rect=(col,x0,z0,x1,z1)=>{g.fillStyle=col;g.fillRect(X(x0),Z(z0),R(x1-x0),R(z1-z0))};
 const MOR='#8d6ae6',AZU='#2f4fd8',LIL='#b9a2f4',ROS='#ec4f8f',AMA='#f5d33a',TUR='#4fe0d8',MOR2='#6448d8',BLA='#ffffff';
 rect(MOR,-16,-9.5,16,9.5);rect(AZU,-14,-7.5,14,7.5);
 // bandas en diagonal y bloques (composición propia con los colores de las canchas de Samil)
 poly(MOR2,[[-14,-7.5],[-6,-7.5],[2,7.5],[-6,7.5]]);poly(AMA,[[-1.2,-7.5],[1.8,-7.5],[9.6,7.5],[6.6,7.5]]);poly(LIL,[[3,-7.5],[4.2,-7.5],[12,7.5],[10.8,7.5]]);
 for(let i=0;i<14;i++){const x=-14+i,z0=i%2?-7.5:-6.5;rect(i%2?'#ece6ff':LIL,x,z0,x+1,z0+1)}
 for(let i=0;i<10;i++){const x=4+i,z0=i%2?6.5:5.5;rect(i%2?TUR:'#ece6ff',x,z0,x+1,z0+1)}
 // dentro de las líneas de 6,75: zonas de color; la zona (pintura) rosa y el semicírculo amarillo
 for(const s of[-1,1]){const hx=s*BKHX;g.save();g.beginPath();g.moveTo(X(s*14),Z(-6.6));g.lineTo(X(s*11),Z(-6.6));g.arc(X(hx),Z(0),R(6.75),s>0?Math.PI+Math.asin(6.6/6.75):-Math.asin(6.6/6.75),s>0?Math.PI-Math.asin(6.6/6.75):Math.asin(6.6/6.75),s>0);g.lineTo(X(s*14),Z(6.6));g.closePath();g.clip();
  g.fillStyle=s>0?'#7a5cf0':'#d84a9a';g.fillRect(0,0,W,H);poly(s>0?TUR:AMA,[[s*14,-6.6],[s*10,-6.6],[s*6,6.6],[s*9,6.6]]);g.restore();
  rect(ROS,s>0?14-5.8:-14,-2.45,s>0?14:-14+5.8,2.45);g.fillStyle=AMA;g.beginPath();g.arc(X(hx),Z(0),R(1.25),0,Math.PI*2);g.fill();
  g.fillStyle=TUR;g.beginPath();g.arc(X(s*8.2),Z(0),R(1.8),0,Math.PI*2);g.fill()}
 g.fillStyle=TUR;g.beginPath();g.arc(X(0),Z(0),R(1.8),0,Math.PI*2);g.fill();g.fillStyle=ROS;g.beginPath();g.arc(X(0),Z(0),R(.9),0,Math.PI*2);g.fill();
 // grano del pavimento
 for(let i=0;i<(LT?2500:9000);i++){g.fillStyle=`rgba(${rn()<.5?255:0},${rn()<.5?255:0},255,${.03+rn()*.04})`;g.fillRect(rn()*W,rn()*H,1+rn()*2,1+rn()*2)}
 // líneas blancas (FIBA)
 g.strokeStyle=BLA;g.lineWidth=Math.max(2,R(.06));g.strokeRect(X(-14),Z(-7.5),R(28),R(15));g.beginPath();g.moveTo(X(0),Z(-7.5));g.lineTo(X(0),Z(7.5));g.stroke();
 g.beginPath();g.arc(X(0),Z(0),R(1.8),0,Math.PI*2);g.stroke();
 for(const s of[-1,1]){const hx=s*BKHX;g.strokeRect(s>0?X(14-5.8):X(-14),Z(-2.45),R(5.8),R(4.9));g.beginPath();g.arc(X(s*8.2),Z(0),R(1.8),0,Math.PI*2);g.stroke();
  g.beginPath();g.moveTo(X(s*14),Z(-6.6));g.lineTo(X(s*11),Z(-6.6));g.stroke();g.beginPath();g.moveTo(X(s*14),Z(6.6));g.lineTo(X(s*11),Z(6.6));g.stroke();
  const a=Math.asin(6.6/6.75);g.beginPath();if(s>0)g.arc(X(hx),Z(0),R(6.75),Math.PI+a,Math.PI-a,true);else g.arc(X(hx),Z(0),R(6.75),-a,a,false);g.stroke();
  g.beginPath();if(s>0)g.arc(X(hx),Z(0),R(1.25),Math.PI*.5,Math.PI*1.5);else g.arc(X(hx),Z(0),R(1.25),-Math.PI*.5,Math.PI*.5);g.stroke()}
 const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=LT?2:8;return t}
function bkTexBalon(){const c=document.createElement('canvas');c.width=256;c.height=128;const g=c.getContext('2d');g.fillStyle='#e8661f';g.fillRect(0,0,256,128);
 for(let i=0;i<1600;i++){g.fillStyle=`rgba(120,40,0,${Math.random()*.18})`;g.fillRect(Math.random()*256,Math.random()*128,2,2)}
 g.strokeStyle='#1c1208';g.lineWidth=4;g.beginPath();g.moveTo(0,64);g.lineTo(256,64);g.stroke();for(const x of[0,64,128,192,256]){g.beginPath();g.moveTo(x,0);g.lineTo(x,128);g.stroke()}
 for(const x0 of[32,160]){g.beginPath();for(let y=0;y<=128;y+=4){const x=x0+Math.sin(y/128*Math.PI)*26;y?g.lineTo(x,y):g.moveTo(x,y)}g.stroke()}
 const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
function bkTexSombra(){const c=document.createElement('canvas');c.width=c.height=64;const g=c.getContext('2d'),gr=g.createRadialGradient(32,32,0,32,32,32);gr.addColorStop(0,'rgba(0,0,0,.55)');gr.addColorStop(.6,'rgba(0,0,0,.25)');gr.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=gr;g.fillRect(0,0,64,64);return new THREE.CanvasTexture(c)}
function bkAroMontar(G,s){const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.5,metalness:.2},o));const H=new THREE.Group();G.add(H);
 const AZ=M(0x2440c8),BL=M(0xffffff,{metalness:0}),NE=M(0x1c1f26,{roughness:.4,metalness:.5}),NA=M(0xff5a1f,{roughness:.35,metalness:.3});
 const m=(geo,mat,x,y,z)=>{const o=new THREE.Mesh(geo,mat);o.position.set(x,y,z);o.castShadow=true;H.add(o);return o};
 m(new THREE.CylinderGeometry(.1,.12,3.5,10),AZ,s*15.1,1.75,0);m(new THREE.BoxGeometry(.5,.08,.5),AZ,s*15.1,.04,0);
 m(new THREE.BoxGeometry(2.3,.13,.13),AZ,s*13.95,3.35,0);m(new THREE.BoxGeometry(1.2,.1,.1),AZ,s*14.5,2.9,0).rotation.z=s*.6;
 m(new THREE.BoxGeometry(.05,1.05,1.8),NE,s*BKBX,3.425,0);
 const fx=s*(BKBX-.03);for(const[w,h,y,z]of[[.05,.05,3.95,0],[.05,.05,2.9,0]])m(new THREE.BoxGeometry(.02,h,1.8),BL,fx,y-(y>3.4?.025:-.025),z);for(const z of[-.875,.875])m(new THREE.BoxGeometry(.02,1.05,.05),BL,fx,3.425,z);
 for(const[h,w,y,z]of[[.05,.59,3.2,0],[.05,.59,3.6,0]])m(new THREE.BoxGeometry(.02,h,w),BL,fx-s*.005,y,z);for(const z of[-.295,.295])m(new THREE.BoxGeometry(.02,.45,.05),BL,fx-s*.005,3.4,z);
 const aro=m(new THREE.TorusGeometry(BKRR,.018,8,28),NA,s*BKHX,BKRY,0);aro.rotation.x=Math.PI/2;m(new THREE.BoxGeometry(.16,.04,.12),NA,s*(BKBX-.09),BKRY,0);
 // red: hilos blancos
 const v=[],N=12;for(let i=0;i<N;i++){const a=i/N*Math.PI*2,a2=(i+.5)/N*Math.PI*2;const p=(r,y,an)=>[Math.cos(an)*r,y,Math.sin(an)*r];
  const A=p(BKRR,0,a),B=p(.17,-.22,a2),C=p(.14,-.44,a);v.push(...A,...B,...B,...C);const A2=p(BKRR,0,(i+1)/N*Math.PI*2);v.push(...A2,...B);const C2=p(.14,-.44,(i+1)/N*Math.PI*2);v.push(...B,...C2)}
 const gg=new THREE.BufferGeometry();gg.setAttribute('position',new THREE.Float32BufferAttribute(v,3));const red=new THREE.LineSegments(gg,new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:.9}));
 red.position.set(s*BKHX,BKRY,0);H.add(red);BKC.red[s]={o:red,t:9};BKC.aro[s]=H}
function bkCancha(){const B=SAM.bk;if(!B||BKC.G)return;const G=new THREE.Group();G.name='basketSamil';
 let top=-9;for(let i=-4;i<=4;i++)for(let j=-3;j<=3;j++){const x=B.cx+B.ex[0]*B.hl*i/4+B.ez[0]*B.hw*j/3,y=B.cy+B.ex[1]*B.hl*i/4+B.ez[1]*B.hw*j/3;const v=sueloRap(x,y)??groundY(x,y);if(v!=null&&v>top)top=v}
 if(top<-8)return;BKC.suelo=top+.004;G.position.set(B.cx,BKC.suelo,B.cy);G.rotation.y=B.rot;G.scale.setScalar(BKK);
 const fl=new THREE.Mesh(new THREE.PlaneGeometry(32,19),new THREE.MeshStandardMaterial({map:bkTexCancha(),roughness:.82,metalness:0}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;G.add(fl);
 const base=new THREE.Mesh(new THREE.BoxGeometry(32.4,4,19.4),new THREE.MeshStandardMaterial({color:0xbdb6a8,roughness:.95}));base.position.y=-2.01;base.receiveShadow=true;G.add(base);
 for(const s of[-1,1])bkAroMontar(G,s);
 // bancos a lo largo de la banda del paseo
 const BM=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.6});for(const x of[-9,-3,3,9]){const b=new THREE.Mesh(new THREE.BoxGeometry(2.4,.45,.5),BM);b.position.set(x,.225,-8.6);b.castShadow=true;G.add(b)}
 const dyn=new THREE.Group();G.add(dyn);BKC.dyn=dyn;scene.add(G);BKC.G=G;G.updateMatrixWorld(true)}
// ---- jugadores: el muñeco del juego con camiseta de tirantes, pantalón corto y calcetines
const BK_PIEL=[0xf0bf94,0xd9a074,0xb07850,0x8a5a3c,0x6a4230,0xf3c8a5,0xc68b5e],BK_PELO=[0x2a1d14,0x6a4c38,0x111111,0xc79a4a,0x3a2a20];
function bkJugador(eq,i){const p=mkPersona(),E=BK_EQ[eq],h=1.88+Math.random()*.22;p.scale.setScalar(h/.083);
 const piel=BK_PIEL[(Math.random()*BK_PIEL.length)|0],MP=new THREE.MeshStandardMaterial({color:piel,roughness:.55}),MS=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.8});
 p.traverse(o=>{if(!o.isMesh||!o.material||o.material.map)return;const m=o.material,c=m.color&&m.color.getHex();
  if(c===0xf6f5f1)m.color.set(E.cam);else if(c===0xdcdad4)m.color.set(E.ribete);else if(c===0x2f5596)m.color.set(E.pant);else if(c===0x2b8fd6)m.color.set(E.acento);
  else if(c===0xf0bf94)m.color.set(piel);else if(c===0xe2a47c)m.color.set(piel).multiplyScalar(.9);else if(c===0x6a4c38||c===0x7a4e2c)m.color.set(BK_PELO[(Math.random()*BK_PELO.length)|0])});
 for(const L of p.userData.piernas.children){const rod=L.userData.rod;if(rod){rod.children[0].material=MP;rod.children[1].material=MS}}
 for(const b of p.userData.brazos.children){for(let k=0;k<3;k++)if(b.children[k])b.children[k].material=MP}
 p.traverse(o=>{if(o.isMesh)o.castShadow=true});
 const sh=new THREE.Mesh(BKC.shGeo,BKC.shMat);sh.rotation.x=-Math.PI/2;sh.position.y=.02;sh.renderOrder=1;
 const G=new THREE.Group();G.add(p);BKC.dyn.add(G);BKC.dyn.add(sh);
 return{eq,i,G,p,sh,x:0,z:0,vx:0,vz:0,ang:0,h,sk:{tiro:.45+Math.random()*.4,vel:.85+Math.random()*.25,def:.5+Math.random()*.5},
  salto:0,saltoD:0,saltoH:0,tiro:null,cd:0,robCD:0,aturd:0,boost:0,spot:null,corteT:3+Math.random()*4,corte:0,dec:0,holdT:0,tx:0,tz:0,run:0,anim:0,man:null}}
// ---- sonidos
function bkSnd(tipo,v=1){try{if(typeof AC==='undefined'||!AC||!master||!soundOn)return;const t=AC.currentTime;
 if(tipo==='bote'){const o=AC.createOscillator(),g=AC.createGain();o.type='sine';o.frequency.setValueAtTime(120,t);o.frequency.exponentialRampToValueAtTime(55,t+.09);g.gain.setValueAtTime(.18*v,t);g.gain.exponentialRampToValueAtTime(.0005,t+.12);o.connect(g);g.connect(master);o.start(t);o.stop(t+.14);return}
 if(tipo==='aro'){for(const f of[620,1340,2100]){const o=AC.createOscillator(),g=AC.createGain();o.type='triangle';o.frequency.value=f*(.97+Math.random()*.06);g.gain.setValueAtTime(.06*v,t);g.gain.exponentialRampToValueAtTime(.0005,t+.35);o.connect(g);g.connect(master);o.start(t);o.stop(t+.4)}return}
 if(tipo==='silbato'){const o=AC.createOscillator(),g=AC.createGain(),l=AC.createOscillator(),lg=AC.createGain();o.type='square';o.frequency.value=2850;l.frequency.value=32;lg.gain.value=120;l.connect(lg);lg.connect(o.frequency);g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.05,t+.02);g.gain.setValueAtTime(.05,t+.32);g.gain.exponentialRampToValueAtTime(.0005,t+.45);o.connect(g);g.connect(master);o.start(t);l.start(t);o.stop(t+.5);l.stop(t+.5);return}
 if(tipo==='bocina'){const o=AC.createOscillator(),g=AC.createGain();o.type='sawtooth';o.frequency.value=196;g.gain.setValueAtTime(.08,t);g.gain.setValueAtTime(.08,t+.9);g.gain.exponentialRampToValueAtTime(.0005,t+1.1);o.connect(g);g.connect(master);o.start(t);o.stop(t+1.15);return}
 if(!NB)return;const s=AC.createBufferSource(),f=AC.createBiquadFilter(),g=AC.createGain();s.buffer=NB;
 const P_={red:[3200,.9,.22,.35,.01],palmas:[1800,.5,.18,1.6,.05],grito:[900,.7,.14,1.4,.15],zapa:[4200,2,.05,.06,.003]}[tipo];if(!P_)return;
 f.type='bandpass';f.frequency.value=P_[0];f.Q.value=P_[1];g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(P_[2]*v,t+P_[4]);g.gain.exponentialRampToValueAtTime(.0005,t+P_[3]);
 s.connect(f);f.connect(g);g.connect(master);s.start(t,Math.random()*1.5);s.stop(t+P_[3]+.1)}catch(e){}}
// ---- ficha (al llegar) y resultado
const BK_DATOS=[['📍','<b>Dónde:</b> paseo marítimo de Samil (Vigo), junto a la playa y con las Islas Cíes enfrente.'],
 ['🎨','<b>Las canchas:</b> en 2025 se renovaron con un gran mural de colores (morado, azul, rosa, amarillo y turquesa) del artista @dantearcade. En el juego la pista lleva un dibujo propio con esos colores.'],
 ['🏀','<b>Uso:</b> pistas al aire libre, de uso libre y gratis. Buenas para un 3x3 a cualquier hora con luz.'],
 ['🚗','<b>Cómo llegar:</b> por la avenida de Samil, con aparcamientos detrás del paseo. También llegan los buses urbanos de Vitrasa hasta la playa.'],
 ['🌅','<b>Consejo:</b> echa un partido al atardecer: el sol se pone detrás de las Cíes.']];
const bkHora=()=>BKD.hora||(CIELO.h>=18.3&&CIELO.h<22.5?'tarde':'dia');
function bkSel(){const bm=Object.entries(BK_MODOS).map(([k,v])=>`<button data-m="${k}" class="${BKD.modo===k?'on':''}">${v.ico} ${k==='ent'?'Entreno':k}<small>${k==='ent'?'60 s de tiro':v.full?'pista entera · 4 min':'media pista · a '+v.meta}</small></button>`).join('');
 const bd=BK_DIF.map((v,i)=>`<button data-d="${i}" class="${BKD.dif===i?'on':''}">${v.n}</button>`).join('');
 const bh=[['dia','☀️ De día'],['tarde','🌅 Atardecer']].map(([k,t])=>`<button data-h="${k}" class="${bkHora()===k?'on':''}">${t}</button>`).join('');
 return `<div class="opt">Modo</div><div class="sel sm">${bm}</div><div class="opt">Rival</div><div class="sel sd">${bd}</div><div class="opt">Hora</div><div class="sel sh">${bh}</div>`}
function bkProg(){const g=BKD.gan,j=BKD.jug;return `<div class="prog">🏆 Victorias: 1x1 <b>${g['1x1']||0}</b>/${j['1x1']||0} · 3x3 <b>${g['3x3']||0}</b>/${j['3x3']||0} · 5x5 <b>${g['5x5']||0}</b>/${j['5x5']||0} · 🎯 récord entreno <b>${BKD.mejorEnt}</b>${typeof TAXI!=='undefined'?' · 🪙 '+TAXI.mon:''}</div>`}
function bkCab(){return `<div class="cab"><i style="left:0;top:0;width:100%;height:100%;background:#2f4fd8"></i><i style="left:-10%;top:0;width:45%;height:100%;background:#6448d8;transform:skewX(-28deg)"></i>
 <i style="left:44%;top:0;width:13%;height:100%;background:#f5d33a;transform:skewX(-28deg)"></i><i style="left:63%;top:0;width:5%;height:100%;background:#b9a2f4;transform:skewX(-28deg)"></i>
 <i style="left:6%;top:18%;width:70px;height:70px;border-radius:50%;background:#ec4f8f"></i><i style="left:72%;top:58%;width:90px;height:50px;background:#4fe0d8;border-radius:45px 45px 0 0"></i>
 <i style="left:0;top:50%;width:100%;height:3px;background:#fff;opacity:.85"></i><span class="bal">🏀</span><span class="sello">PISTAS REALES · PASEO DE SAMIL</span></div>`}
function bkFicha(modo){const fin=modo==='fin';BK.ficha=true;let cuerpo;
 if(!fin)cuerpo=`<h2>🏀 Canchas de Samil</h2><p class="sub">Vigo · paseo marítimo de Samil</p><ul>${BK_DATOS.map(d=>`<li><i>${d[0]}</i><span>${d[1]}</span></li>`).join('')}</ul>${bkProg()}${bkSel()}
  <div class="acc"><button class="no">Ahora no</button><button class="go">🏀 ¡A jugar!</button></div><p class="sub" style="margin:8px 0 0;font-size:11px">Flechas mover · Espacio tirar (mantén y suelta arriba) · K pasar / robar · L finta / cambiar · Mayús correr</p>`;
 else{const R=BK.res;cuerpo=`<h2>${R.titulo}</h2><p class="sub">Canchas de Samil · ${R.modoN}</p><div class="res">${R.marc}<small>${R.sub}</small></div>
  <ul>${R.lineas.map(l=>`<li><i>${l[0]}</i><span>${l[1]}</span></li>`).join('')}</ul>${R.gana?`<div class="gana">${R.gana}</div>`:''}${bkProg()}${bkSel()}
  <div class="acc"><button class="no">Salir</button><button class="go">🔁 Otro partido</button></div>`}
 BKF.innerHTML=`<div class="c">${bkCab()}<div class="in">${cuerpo}</div></div>`;BKF.hidden=false;
 const grupo=(q,k,fn)=>BKF.querySelectorAll(q+' button').forEach(b=>b.onclick=()=>{fn(b.dataset[k]);bkGuardar();BKF.querySelectorAll(q+' button').forEach(x=>x.classList.toggle('on',x===b))});
 grupo('.sm','m',v=>BKD.modo=v);grupo('.sd','d',v=>BKD.dif=+v);grupo('.sh','h',v=>BKD.hora=v);
 BKF.querySelector('.go').onclick=()=>{BKF.hidden=true;BK.ficha=false;bkEmpezar()};BKF.querySelector('.no').onclick=()=>{BKF.hidden=true;BK.ficha=false};
 setTimeout(()=>{const b=BKF.querySelector('.go');b&&b.focus({preventScroll:true})},50);if(!fin)try{gtvEv('minijuego/basket-ficha','Basket Samil · ficha')}catch(e){}}
// ---- GPS: ir a Samil
function bkDestino(){const B=SAM.bk;if(B){const x=B.cx+B.ez[0]*(B.hw+.12),y=B.cy+B.ez[1]*(B.hw+.12);return[x,y]}return[27.25,64.2]}
function basketIr(){if(REP.on||RACE.on)return;const d=bkDestino();
 if(driving&&Math.hypot(d[0]-P.x,d[1]-P.y)<1.2&&BKC.G){BK.cerca=true;bkFicha('intro');return}
 if(typeof TAXI!=='undefined'&&TAXI.on)taxiFin('otro');
 if(!driving)setDrive(true,'coche');
 if(MODO!=='coche'&&MODO!=='pie'){const G=gpsGrafo(),i=G?gpsNodo(P.x,P.y):-1;if(i>=0){const A=G.ADJ[i];let a=P.a;if(A&&A.length){const j=A[0];a=Math.atan2(-(G.Y[j]-G.Y[i]),G.X[j]-G.X[i])}Object.assign(P,{x:G.X[i],y:G.Y[i],a,v:0});P.z=groundY(P.x,P.y)}
  cambiarModo('coche');camInit=false;mostrar('🚗 Te subes a un coche para ir a Samil')}
 gpsIniciar(['🏀 Canchas de Samil',d[0],d[1]]);
 if(GPS.on){BK.ruta=true;BK.fin=GPS.pts[GPS.pts.length-1].slice();setTimeout(()=>{if(BK.ruta)mostrar('🏀 Sigue la línea azul hasta las canchas de Samil ('+fmtD(GPS.acc[GPS.acc.length-1])+')')},400)}}
function basketCancelar(){if(BK.ruta&&GPS.on&&GPS.dest&&/Samil/.test(GPS.dest[0]))gpsParar();BK.ruta=false;mostrar('🏀 Basket cancelado')}
// marcador de la misión: aro amarillo y balón flotando en el centro de la cancha
function bkMarca(){const g=new THREE.Group();const r=new THREE.Mesh(new THREE.RingGeometry(.075,.095,32),new THREE.MeshBasicMaterial({color:0xffc21a,transparent:true,opacity:.8,side:THREE.DoubleSide,depthWrite:false,fog:false}));r.rotation.x=-Math.PI/2;r.position.y=.006;g.add(r);g.userData.r=r;
 const c=new THREE.Mesh(new THREE.CylinderGeometry(.035,.035,.6,16,1,true),new THREE.MeshBasicMaterial({color:0xff7a1a,transparent:true,opacity:.22,side:THREE.DoubleSide,depthWrite:false,fog:false}));c.position.y=.3;g.add(c);
 const b=new THREE.Mesh(new THREE.SphereGeometry(.022,18,12),new THREE.MeshStandardMaterial({map:bkTexBalon(),roughness:.6}));b.position.y=.12;g.add(b);g.userData.b=b;g.visible=false;scene.add(g);return g}
// ---- cada fotograma jugando en el mundo: construir la cancha, marcador y llegada
function basketTick(dt){if(BK.on)return;if(!BKC.G){if(typeof SAM!=='undefined'&&SAM.bk&&SAM.G)try{bkCancha()}catch(e){console.warn('basket cancha',e);SAM.bk=null}if(!BKC.G)return}
 const B=SAM.bk;if(!BKC.mk)BKC.mk=bkMarca();const d=Math.hypot(B.cx-P.x,B.cy-P.y),mk=BKC.mk;mk.visible=d<30&&!RACE.on&&!REP.on&&!BK.ficha;
 if(mk.visible){const now=performance.now()/1000;mk.position.set(B.cx,BKC.suelo,B.cy);mk.userData.b.position.y=.12+Math.sin(now*3)*.02;mk.userData.b.rotation.y=now*2;mk.userData.r.material.opacity=.55+.3*Math.sin(now*4)}
 if(BK.ruta&&BK.fin&&!BK.ficha&&Math.hypot(BK.fin[0]-P.x,BK.fin[1]-P.y)<.32){BK.ruta=false;if(GPS.on)gpsParar();P.v=0;BK.cerca=true;bkFicha('intro');return}
 if(BK.ruta&&(!GPS.on||!GPS.dest||!/Samil/.test(GPS.dest[0])))BK.ruta=false;
 if(d>1.2)BK.cerca=false;
 if(!BK.cerca&&!BK.ficha&&(d<.3||(MODO==='pie'&&bkDentroM(P.x,P.y,0)))&&Math.abs(P.v)<.15&&!RACE.on&&!REP.on&&MODO!=='heli'&&!(typeof SG!=='undefined'&&SG.on)){BK.cerca=true;if(BK.ruta){if(GPS.on)gpsParar();BK.ruta=false}P.v=0;bkFicha('intro')}}
// ---- empezar / terminar
function bkEmpezar(){if(!BKC.G||!driving)return;const M=BK_MODOS[BKD.modo]||BK_MODOS['3x3'];BK.modo=BKD.modo;BK.M=M;BK.dif=BK_DIF[BKD.dif]||BK_DIF[1];
 if(!BKC.shGeo){BKC.shGeo=new THREE.CircleGeometry(.55,20);BKC.shMat=new THREE.MeshBasicMaterial({map:bkTexSombra(),transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-4,polygonOffsetUnits:-4})}
 bkLimpiarDyn();BK.J=[];BK.T=[[],[]];const nE=BK.modo==='ent'?[1,0]:[M.k,M.k];
 for(let e=0;e<2;e++)for(let i=0;i<nE[e];i++){const j=bkJugador(e,i);BK.T[e].push(j);BK.J.push(j)}
 for(let i=0;i<BK.T[0].length;i++){if(BK.T[1][i]){BK.T[0][i].man=BK.T[1][i];BK.T[1][i].man=BK.T[0][i]}}
 if(!BKC.ballGeo){BKC.ballGeo=new THREE.SphereGeometry(BKBR,20,14);BKC.ballMat=new THREE.MeshStandardMaterial({map:bkTexBalon(),roughness:.6})}
 const bm=new THREE.Mesh(BKC.ballGeo,BKC.ballMat);bm.castShadow=true;BKC.dyn.add(bm);const bs=new THREE.Mesh(BKC.shGeo,BKC.shMat);bs.rotation.x=-Math.PI/2;bs.scale.setScalar(.5);BKC.dyn.add(bs);
 BK.ball={m:bm,sh:bs,x:0,y:1,z:0,vx:0,vy:0,vz:0,st:'mano',hold:null,ult:0,tiro:null,pase:null,ign:null,ignT:0,ph:0,aroT:0,toque:false};
 // indicador del jugador que llevas
 const ind=new THREE.Group();const ar=new THREE.Mesh(new THREE.RingGeometry(.5,.66,28),new THREE.MeshBasicMaterial({color:0x4fe0d8,transparent:true,opacity:.9,side:THREE.DoubleSide,depthWrite:false}));ar.rotation.x=-Math.PI/2;ar.position.y=.03;ind.add(ar);
 const fl=new THREE.Mesh(new THREE.ConeGeometry(.16,.3,4),new THREE.MeshBasicMaterial({color:0x4fe0d8}));fl.rotation.x=Math.PI;fl.position.y=2.75;ind.add(fl);ind.userData.fl=fl;BKC.dyn.add(ind);BK.ind=ind;
 // público en el paseo (detrás de la cancha)
 BK.pub=[];if(BK.modo!=='ent')for(let i=0;i<(window.LITE?3:6);i++){const p=mkPersona();p.scale.setScalar(1.75/.083);const g=new THREE.Group();g.add(p);g.position.set(-10+i*4+Math.random()*1.5,0,-9.6-Math.random()*.6);g.rotation.y=Math.PI/2+(Math.random()-.5)*.6;BKC.dyn.add(g);BK.pub.push({g,p,ph:Math.random()*6,salta:0})}
 Object.assign(BK,{on:true,pts:[0,0],reloj:M.dur,c24:M.c24,fase:'juego',muertaT:0,muertaFn:null,tt:0,limpiar:[false,false],oro:false,msgT:0,pos:0,
  st:{pts:0,tri:0,tap:0,rob:0,reb:0,tiros:0,dentro:0,racha:0,mejorRacha:0,asis:0},auto:!!window.__BKAUTO,ultPase:null,ent:null,dbg:{tiro:[0,0],quiere:[0,0],can:[0,0],tap:[0,0],rob:[0,0],c24:[0,0],fuera:[0,0],inter:[0,0],tipos:{}}});
 BK.k={l:0,r:0,u:0,d:0,a:0,b:0,c:0,sh:0};BK.cam.ini=false;for(const k in keys)keys[k]=false;P.v=0;
 BK.prevPie=MODO==='pie'&&persona.visible;if(BK.prevPie)persona.visible=false;if(BKC.mk)BKC.mk.visible=false;
 if(!BK.prevCielo)BK.prevCielo={modo:CIELO.modo,h:CIELO.h,t:TIEMPO.modo};CIELO.modo='basket';CIELO.h=bkHora()==='tarde'?20.3:(BK.prevCielo.h>=9&&BK.prevCielo.h<=18?BK.prevCielo.h:12.5);CIELO.txt='';TIEMPO.modo='despejado';try{cielo(0)}catch(e){}
 // colocación inicial
 const full=M.full;BK.J.forEach(j=>{j.G.visible=true});
 if(BK.modo==='ent'){const j=BK.T[0][0];bkPon(j,5.5,0,0);bkDar(j);BK.ent={t:0,vuelta:0};BK.reloj=M.dur}
 else{bkFormacion(full?'salto':'arriba',0);for(const j of BK.J){j.x=j.tx;j.z=j.tz}bkDar(full?BK.T[0][0]:BK.T[0][0]);}
 BK.yo=BK.T[0][0];bkCtl();document.body.classList.add('bkg');BKH.hidden=false;BKH.querySelector('.modo').textContent=M.ico+' '+M.n+(BK.modo==='ent'?'':' · '+BK.dif.n);
 BKH.querySelector('.ce small').style.visibility=BK.modo==='ent'?'hidden':'visible';BKH.querySelector('.e1').style.visibility=BK.modo==='ent'?'hidden':'visible';BKH.querySelector('.e0 span').textContent=BK.modo==='ent'?'PUNTOS':'SAMIL';
 BKD.partidos++;bkGuardar();bkSnd('silbato');
 bkMsg(BK.modo==='ent'?'🎯 ¡Entrenamiento!':'🏀 ¡A jugar!',BK.modo==='ent'?'60 s · tira desde donde quieras':M.meta?'gana el primero a '+M.meta:'4 minutos · 24 s de posesión',1.6);
 bkTip();try{gtvEv('minijuego/basket-'+BK.modo,'Basket Samil '+BK.modo)}catch(e){}}
function bkLimpiarDyn(){if(!BKC.dyn)return;for(const o of [...BKC.dyn.children]){BKC.dyn.remove(o);o.traverse(q=>{if(q.geometry&&q.geometry!==BKC.shGeo&&q.geometry!==BKC.ballGeo)q.geometry.dispose();const m=q.material;if(m&&m!==BKC.shMat&&m!==BKC.ballMat&&!Array.isArray(m))m.dispose()})}}
function bkTerminar(motivo){if(!BK.on)return;BK.on=false;document.body.classList.remove('bkg');BKH.hidden=true;bkLimpiarDyn();BK.J=[];BK.T=[[],[]];BK.ball=null;BK.ind=null;
 if(BK.prevCielo){CIELO.modo=BK.prevCielo.modo;CIELO.h=BK.prevCielo.h;TIEMPO.modo=BK.prevCielo.t;CIELO.txt='';BK.prevCielo=null;try{cielo(0)}catch(e){}}
 if(BK.prevPie)persona.visible=true;BK.prevPie=false;camInit=false;BK.cerca=true;
 const M=BK.M,s=BK.st;let gana='';
 if(BK.modo==='ent'){const rec=s.pts>BKD.mejorEnt;if(rec)BKD.mejorEnt=s.pts;const mon=Math.floor(s.pts/5);if(mon&&motivo==='fin'){try{taxiMon(mon)}catch(e){}gana=`🪙 +${mon} monedas`}
  BK.res={titulo:'🎯 ¡Tiempo!',modoN:'Entrenamiento',marc:`<div class="p" style="color:#7a4fe0">${s.pts}</div>`,sub:'puntos'+(rec&&s.pts>0?' · 🏆 ¡nuevo récord!':' · récord '+BKD.mejorEnt),
   lineas:[['🏀',`${s.dentro} de ${s.tiros} tiros (${s.tiros?Math.round(s.dentro/s.tiros*100):0} %)`],['🎯',`${s.tri} triple${s.tri===1?'':'s'}`],['🔥',`Mejor racha: ${s.mejorRacha} seguidas`]],gana}}
 else{const g=BK.pts[0]>BK.pts[1];if(motivo==='fin'){BKD.jug[BK.modo]=(BKD.jug[BK.modo]||0)+1;if(g){BKD.gan[BK.modo]=(BKD.gan[BK.modo]||0)+1;const mon=Math.round(M.mon*(BKD.dif===2?1.5:BKD.dif===0?.6:1));try{taxiMon(mon)}catch(e){}gana=`🪙 +${mon} monedas por la victoria`}}
  BK.res={titulo:motivo!=='fin'?'🏀 Partido abandonado':g?'🏆 ¡Victoria!':'😓 Derrota',modoN:M.n+' · '+BK.dif.n,
   marc:`<div class="p"><span style="color:${BK_EQ[0].css}">${BK.pts[0]}</span> <span style="opacity:.4">–</span> <span style="color:#c9a000">${BK.pts[1]}</span></div>`,sub:'SAMIL – RÍA',
   lineas:[['🏀',`Tus puntos: ${s.pts} · tiros ${s.dentro}/${s.tiros}`],['🎯',BK.M.full?`${s.tri} triple${s.tri===1?'':'s'}`:`${s.tri} canasta${s.tri===1?'':'s'} de 2 (desde fuera de la línea)`],['✋',`${s.tap} tapón${s.tap===1?'':'es'} · ${s.rob} robo${s.rob===1?'':'s'} · ${s.reb} rebote${s.reb===1?'':'s'}`],['👉',`${s.asis} asistencia${s.asis===1?'':'s'}`]],gana}}
 bkGuardar();if(motivo!=='salir')bkFicha('fin')}
window.basketSalir=()=>{bkTerminar('salir');BKF.hidden=true;BK.ficha=false};
window.bkT={paso:dt=>bkUpdate(dt),st:()=>BK,datos:()=>BKD,ir:()=>basketIr(),empezar:m=>{if(m)BKD.modo=m;bkEmpezar()},fin:()=>bkTerminar('menu'),ficha:()=>bkFicha('intro'),boton:(k,v)=>bkBoton(k,v),cancha:()=>BKC};
// ---- utilidades de juego
function bkMsg(t,s='',d=1.1){const m=BKH.querySelector('.msg');m.innerHTML=t+(s?`<small>${s}</small>`:'');m.classList.remove('on');void m.offsetWidth;m.classList.add('on');BK.msgT=d}
function bkTip(){const t=BKH.querySelector('.tip');const tactil=matchMedia('(pointer:coarse)').matches;const y=BK.yo,at=BK.ball&&BK.ball.hold&&BK.ball.hold.eq===0;
 t.textContent=BK.modo==='ent'?(tactil?'Mantén 🏀 y suelta en lo alto del salto · el balón vuelve solo':'Espacio: mantén y suelta en lo alto del salto · el balón vuelve solo'):
  at?(tactil?'🏀 tirar (mantén) · 👉 pasar · ⚡ finta · joystick a tope: correr':'Espacio tirar (mantén) · K pasar · L finta · Mayús correr'):(tactil?'✋ tapón · 🖐️ robar · 🔄 cambiar de jugador':'Espacio tapón · K robar · L cambiar de jugador · Mayús correr')}
function bkAtk(eq){return BK.M.full&&eq===1?-1:1}   // canasta a la que ataca cada equipo (+1 derecha)
function bkPon(j,x,z,a){j.x=x;j.z=z;j.vx=j.vz=0;if(a!=null)j.ang=a}
function bkDar(j){const b=BK.ball;b.hold=j;b.st='mano';b.tiro=null;b.pase=null;b.ult=j.eq;b.toque=false;if(BK.pos!==j.eq){BK.pos=j.eq;BK.c24=BK.M.c24}j.holdT=0;
 if(j.eq===0&&BK.T[0].length){if(BK.yo!==j){BK.yo=j;bkCtl()}}else if(j.eq===1&&BK.T[0].length){const d=j.man||BK.T[0][0];if(BK.yo!==d&&!BK.yoFijo){BK.yo=d;bkCtl()}}bkTip()}
function bkCtl(){const b=BKH.querySelectorAll('.bt button');const ataque=BK.pos===0||BK.modo==='ent';const L=ataque?[['⚡','Finta'],['👉','Pasar'],['🏀','Tirar']]:[['🔄','Cambiar'],['🖐️','Robar'],['✋','Tapón']];
 b.forEach((x,i)=>x.innerHTML=`<span>${L[i][0]}</span>${L[i][1]}`);if(BK.modo==='ent'||BK.M.k===1)b[1].classList.toggle('off',ataque);b[0].classList.toggle('off',!ataque&&BK.M.k===1);bkTip()}
// formaciones: posiciones de cada uno al empezar o tras una canasta
function bkSpot(eq,d,z){const s=bkAtk(eq);return[s*(BKHX-d),z]}
const BK_SP3=[[7.6,0],[5.8,-4.6],[5.8,4.6],[1.2,-6.2],[1.2,6.2],[3.8,-2.6],[3.8,2.6]],BK_SP5=[[7.8,0],[6.2,-5],[6.2,5],[1.2,-6.2],[1.2,6.2],[2.2,-3],[2.2,3],[5.4,0]];
function bkFormacion(tipo,eqBalon){const full=BK.M.full;
 for(const eq of[0,1])BK.T[eq].forEach((j,i)=>{let p;
  if(tipo==='salto'){const s=eq===0?-1:1;p=[[s*.9,0],[s*3.2,-4.5],[s*3.2,4.5],[s*6,-2],[s*6,2]][i]}
  else if(eq===eqBalon){const SP=full?BK_SP5:BK_SP3;p=bkSpot(eq,...SP[i===0?0:i+(full?0:0)])}
  else{const m=j.man;const q=m?[m.tx,m.tz]:bkSpot(eqBalon,5,0);const hx=bkAtk(eqBalon)*BKHX,dx=hx-q[0],dz=-q[1],l=Math.hypot(dx,dz)||1;p=[q[0]+dx/l*1.4,q[1]+dz/l*1.4]}
  j.tx=p[0];j.tz=p[1]})}
// ---- botones
function bkBoton(k,on){if(!BK.on||BK.fase==='fin')return;const y=BK.yo,b=BK.ball;if(!y||!b)return;
 if(k==='sh')return;const ataque=BK.modo==='ent'||(b.hold?b.hold.eq===0:BK.pos===0);
 if(k==='a'){if(b.hold===y){if(on)bkTiroEmpieza(y,false);else if(y.tiro&&y.tiro.carga)bkSuelta(y)}else if(on&&!ataque)bkSaltar(y,.75)}
 else if(k==='b'&&on){if(b.hold===y)bkPasar(y,bkInput());else if(!ataque)bkRobar(y)}
 else if(k==='c'&&on){if(b.hold===y)bkFinta(y,bkInput());else if(!ataque)bkCambiar()}}
function bkInput(){let x=(BK.k.r?1:0)-(BK.k.l?1:0)+BK.padX+BK.joy.x,y=(BK.k.u?1:0)-(BK.k.d?1:0)+BK.padY+BK.joy.y;const l=Math.hypot(x,y);if(l>1){x/=l;y/=l}return{x,z:-y,l:Math.min(1,l)}}
function bkCambiar(){const b=BK.ball,bx=b.x,bz=b.z;let best=null,bd=1e9;for(const j of BK.T[0]){if(j===BK.yo)continue;const d=Math.hypot(j.x-bx,j.z-bz);if(d<bd){bd=d;best=j}}if(best){BK.yo=best;BK.yoFijo=true;setTimeout(()=>BK.yoFijo=false,2500)}}
function bkSaltar(j,dur,h=.55){if(j.salto>0||j.aturd>0)return;j.salto=dur;j.saltoD=dur;j.saltoH=h}
function bkRobar(j){if(j.robCD>0)return;j.robCD=.9;const b=BK.ball,h=b.hold;j.anim=.35;if(!h||h.eq===j.eq){return}const d=Math.hypot(h.x-j.x,h.z-j.z);
 if(d<1.5){const p=(.22+(h.run>.8?.12:0))*(h.tiro?0:1);if(Math.random()<p){bkSuelto(j,'robo')}else if(Math.random()<.12){bkMsg('🟨 Falta','saque de banda',1);bkSnd('silbato');bkMuerta(1,()=>{bkDarEn(h,h.x,h.z)})}}}
function bkSuelto(j,tipo){const b=BK.ball,h=b.hold;b.hold=null;b.st='aire';b.x=h?h.x+(j.x-h.x)*.5:b.x;b.z=h?h.z+(j.z-h.z)*.5:b.z;b.y=.9;b.vx=(j.x-(h?h.x:b.x))*1.2+(Math.random()-.5);b.vz=(j.z-(h?h.z:b.z))*1.2+(Math.random()-.5);b.vy=1.5;b.ign=h;b.ignT=.4;b.tiro=null;
 if(tipo==='robo'){BK.dbg.rob[j.eq]++;bkMsg(j.eq===0?'🖐️ ¡ROBO!':'😱 ¡Te la roban!','',1);if(j.eq===0)BK.st.rob++;bkSnd('palmas',.6)}if(h)h.aturd=.35}
function bkFinta(j,inp){if(j.cd>0||j.tiro)return;j.cd=2.2;let dx=inp.x,dz=inp.z;if(inp.l<.2){const d=bkDefensor(j);if(d){dx=-(d.z-j.z);dz=(d.x-j.x);const l=Math.hypot(dx,dz)||1;dx/=l;dz/=l;if(Math.random()<.5){dx=-dx;dz=-dz}}else{dx=bkAtk(j.eq);dz=0}}
 const l=Math.hypot(dx,dz)||1;j.boost=.5;j.bx=dx/l;j.bz=dz/l;const d=bkDefensor(j);if(d&&Math.hypot(d.x-j.x,d.z-j.z)<2.2&&Math.random()<.55*(1.1-BK.dif.df*.25)){d.aturd=.75;if(j.eq===0)bkMsg('⚡ ¡CROSSOVER!','lo dejas atrás',.9)}else if(j.eq===0)bkMsg('⚡ Finta','',.6);bkSnd('zapa',.8)}
function bkDefensor(j){let best=null,bd=1e9;for(const o of BK.T[1-j.eq]){const d=Math.hypot(o.x-j.x,o.z-j.z);if(d<bd){bd=d;best=o}}return best}
function bkDefDist(j){const d=bkDefensor(j);return d?Math.hypot(d.x-j.x,d.z-j.z):99}
// ---- tiro: el jugador salta; se suelta el balón en lo alto (usuario: al soltar el botón)
function bkTiroEmpieza(j,ia){if(j.tiro||j.salto>0||BK.fase!=='juego')return;const s=bkAtk(j.eq),hx=s*BKHX,dist=Math.hypot(hx-j.x,j.z);
 if(BK.M&&!BK.M.full&&BK.modo!=='ent'&&BK.limpiar[j.eq]){if(j.eq===0)bkMsg('↩️ Saca el balón','fuera de la línea antes de tirar',1.1);return}
 let tipo='salto';if(dist<1.7&&(j.run>.5||dist<1.1))tipo='mate';else if(dist<2.8)tipo='bandeja';
 j.tiro={t:0,tipo,carga:!ia&&tipo==='salto',rel:tipo==='salto'?(ia?.42+(Math.random()-.5)*.16/(.6+j.sk.tiro):.78):tipo==='mate'?.5:.42,hx,s,dist0:dist};
 bkSaltar(j,tipo==='mate'?1.05:.9,tipo==='mate'?.95:tipo==='bandeja'?.7:.55);
 // los defensores cercanos saltan a puntear (con un poco de retraso)
 for(const d of BK.T[1-j.eq]){if(d===BK.yo&&!BK.auto)continue;const dd=Math.hypot(d.x-j.x,d.z-j.z);if(dd<2.2&&Math.random()<.65*BK.dif.df*(d.eq===0?.8:1))d.puntea=.08+Math.random()*.22}}
function bkSuelta(j){const T=j.tiro;if(!T||T.solto)return;T.rel=Math.max(.05,T.t);T.carga=false}
function bkLanza(j){const T=j.tiro,b=BK.ball;T.solto=true;BKH.querySelector('.med').hidden=true;
 const s=T.s,hx=T.hx,dist=Math.hypot(hx-j.x,j.z),tres=bkFuera(j.x,j.z,s),pts=BK.M.full||BK.modo==='ent'?(tres?3:2):(tres?2:1);
 // calidad del momento de soltar (solo tiros en suspensión)
 let q=1,cal='';if(T.tipo==='salto'){const e=Math.abs(T.rel-.42);if(e<.05){q=1.28;cal='perfecto'}else if(e<.12){q=1;cal='bien'}else{q=.5;cal=T.rel<.42?'pronto':'tarde'}}
 let p=T.tipo==='mate'?.93:T.tipo==='bandeja'?.8:dist<4?.64:dist<6.75?.56-(dist-4)*.035:Math.max(.05,.4-(dist-6.75)*.07);
 p*=q*(.82+.36*j.sk.tiro);if(j.eq===1)p*=BK.dif.ia;const dd=bkDefDist(j);p*=dd<.9?.5:dd<1.6?.72:dd<2.4?.9:1;if(j.eq===0&&BK.modo!=='ent'&&BKD.dif===0)p*=1.1;p=Math.min(.97,p);
 const dentro=Math.random()<p;
 // tapón
 let tapon=null;for(const d of BK.T[1-j.eq]){if(d.salto<=0)continue;const k=1-d.salto/d.saltoD;const dh=Math.hypot(d.x-j.x,d.z-j.z);if(dh<1.35&&k>.12&&k<.8){const pb=(T.tipo==='mate'?.18:T.tipo==='bandeja'?.24:.14)*(d.eq===1?BK.dif.df:1)*(.7+.6*d.sk.def);if(Math.random()<pb){tapon=d;break}}}
 b.hold=null;b.st='aire';b.ign=j;b.ignT=.55;b.toque=false;b.aroT=0;b.ult=j.eq;
 const hy=1.95+j.h*.25+bkAlt(j);b.x=j.x+Math.cos(j.ang)*.25;b.z=j.z-Math.sin(j.ang)*.25;b.y=hy;
 if(tapon){BK.dbg.tap[tapon.eq]++;b.vx=(b.x-tapon.x)*3+(Math.random()-.5)*2;b.vz=(b.z-tapon.z)*3+(Math.random()-.5)*2;b.vy=2.5;b.tiro=null;bkMsg(tapon.eq===0?'✋ ¡TAPÓN!':'🚫 ¡Te ponen un tapón!','',1.1);if(tapon.eq===0)BK.st.tap++;bkSnd('palmas');bkSnd('grito',.7);
  if(j.eq===0)BK.st.tiros++;return}
 b.tiro={eq:j.eq,j,pts,s,dentro,tipo:T.tipo,t:0};{const D=BK.dbg;D.tiro[j.eq]++;if(dentro)D.quiere[j.eq]++;D.tipos[T.tipo]=(D.tipos[T.tipo]||0)+1}if(j.eq===0){BK.st.tiros++}if(BK.ent){BK.ent.pend=true;BK.ent.t=0}
 if(T.tipo==='mate'&&dentro){b.x=hx-s*.05;b.z=0;b.y=BKRY+.32;b.vx=0;b.vz=0;b.vy=-4.5;j.colgado=.45;bkMsg(j.eq===0?'💥 ¡MATE!':'💥 Mate de la Ría','',1);bkSnd('aro',1.3);return}
 // objetivo: el centro del aro (dentro) o un punto del hierro (fuera)
 let tx=hx,tz=0;if(dentro){const ux=hx-b.x,uz=-b.z,ul=Math.hypot(ux,uz)||1,r=Math.random()*.04,a=Math.random()*6.28;tx+=ux/ul*.04+Math.cos(a)*r;tz+=uz/ul*.04+Math.sin(a)*r}else{const a=Math.random()*6.28,r=BKRR+.02+Math.random()*.09;tx+=Math.cos(a)*r;tz+=Math.sin(a)*r}
 const ty=BKRY+.02,dx=tx-b.x,dz=tz-b.z,dh=Math.hypot(dx,dz),Tt=T.tipo==='salto'?.75+dh*.075:.55+dh*.08,vy=(ty-b.y+.5*BKG*Tt*Tt)/Tt;b.vx=dx/Tt;b.vz=dz/Tt;b.vy=vy;
 if(j.eq===0&&cal)bkMsg(cal==='perfecto'?'🟢 ¡Perfecto!':cal==='bien'?'Bien soltado':cal==='pronto'?'🟡 Pronto':'🟠 Tarde','',.7)}
function bkFuera(x,z,s){const hx=s*BKHX;if(Math.abs(z)>6.6-.0)return true;return Math.hypot(x-hx,z)>6.75}
function bkAlt(j){return j.salto>0?j.saltoH*4*(1-j.salto/j.saltoD)*(j.salto/j.saltoD):0}
// ---- pase
function bkPasar(j,inp,dest){if(j.tiro||BK.fase!=='juego')return;const tm=BK.T[j.eq].filter(o=>o!==j);if(!tm.length)return;let best=dest||null;
 if(!best){let bs=-1e9;for(const o of tm){const dx=o.x-j.x,dz=o.z-j.z,l=Math.hypot(dx,dz)||1;let sc=inp&&inp.l>.3?(dx*inp.x+dz*inp.z)/l*3-l*.05:bkDefDist(o)-l*.08;if(sc>bs){bs=sc;best=o}}}
 const b=BK.ball;b.hold=null;b.st='aire';b.ign=j;b.ignT=.3;b.tiro=null;b.pase={a:best,de:j};b.toque=false;BK.ultPase={de:j,t:4};
 const px=best.x+best.vx*.12,pz=best.z+best.vz*.12;b.pase.px=px;b.pase.pz=pz;b.pase.x0=j.x;b.pase.z0=j.z;b.x=j.x+Math.cos(j.ang)*.3;b.z=j.z-Math.sin(j.ang)*.3;b.y=1.3;const dx=px-b.x,dz=pz-b.z,dh=Math.hypot(dx,dz),Tt=Math.max(.22,dh/15);
 b.vx=dx/Tt;b.vz=dz/Tt;b.vy=(1.25-b.y+.5*BKG*Tt*Tt)/Tt;best.espera=Tt+.3;j.anim=.3;bkSnd('zapa',.5)}
function bkDarEn(j,x,z){bkPon(j,Math.max(-13.4,Math.min(13.4,x)),Math.max(-7,Math.min(7,z)));bkDar(j)}
function bkMuerta(t,fn){BK.fase='muerta';BK.muertaT=t;BK.muertaFn=fn}
// cambio de posesión tras canasta, fuera o violación: el balón lo coge el equipo eq cerca de la canasta s (o en el punto dado)
function bkSaque(eq,s,punto){if(BK.modo==='ent')return;const T=BK.T[eq];if(!T.length)return;let j=T[0],bd=1e9;const px=punto?punto[0]:s*13,pz=punto?punto[1]:.8;
 for(const o of T){const d=Math.hypot(o.x-px,o.z-pz);if(d<bd){bd=d;j=o}}const x=punto?Math.max(-13.3,Math.min(13.3,px)):s*13.1,z=punto?Math.max(-6.9,Math.min(6.9,pz)):.8;
 j.tx=x;j.tz=z;BK.saqueJ=j;if(!BK.M.full)BK.limpiar[eq]=true;bkMuerta(1.1,()=>{if(Math.hypot(j.x-x,j.z-z)>.4)bkPon(j,x,z);bkDar(j)})}
function bkCanasta(b){const t=b.tiro,eq=t?t.eq:b.ult,pts=t?t.pts:(BK.M.full?2:1),s=b.x>0?1:-1;
 if(BK.modo==='ent'){const S=BK.st;S.dentro++;S.racha++;S.mejorRacha=Math.max(S.mejorRacha,S.racha);let n=pts;if(S.racha>=3)n++;S.pts+=n;if(pts===3)S.tri++;
  bkMsg(pts===3?'🎯 ¡TRIPLE!':t&&t.tipo==='mate'?'💥 ¡MATE!':'🏀 ¡Dentro!','+'+n+(S.racha>=3?' · 🔥 racha de '+S.racha:''),1);bkSnd('red');BK.ent.vuelta=.9;BK.ent.pend=false;BKC.red[s].t=0;return}
 BK.pts[eq]+=pts;BK.dbg.can[eq]++;BKC.red[s].t=0;bkSnd('red');bkSnd(eq===0?'palmas':'grito',eq===0?1:.5);
 if(eq===0&&t){BK.st.pts+=pts;BK.st.dentro++;if(BK.M.full?pts===3:pts===2)BK.st.tri++;
  if(BK.ultPase&&BK.ultPase.de!==t.j&&BK.ultPase.de.eq===0&&BK.ultPase.t>0)BK.st.asis++}
 const nom=BK.M.full?(pts===3?'¡TRIPLE!':'¡Canasta!'):(pts===2?'¡De 2!':'¡Canasta!');for(const p of BK.pub)p.salta=1.2;
 bkMsg((eq===0?'🏀 ':'😬 ')+nom,(eq===0?'SAMIL ':'RÍA ')+'+'+pts,1.1);
 // ¿se acabó?
 const M=BK.M;if((M.meta&&BK.pts[eq]>=M.meta)||BK.oro){BK.fase='fin';setTimeout(()=>bkFinal(),1400);return}
 BK.c24=M.c24;bkSaque(1-eq,s)}
function bkFinal(){bkSnd('bocina');const g=BK.pts[0]>BK.pts[1];bkMsg(g?'🏆 ¡Victoria!':'😓 Derrota',`${BK.pts[0]} – ${BK.pts[1]}`,2);setTimeout(()=>bkTerminar('fin'),1700)}
// ---- IA
function bkIA(j,dt){const b=BK.ball,full=BK.M.full,eqA=b.hold?b.hold.eq:(b.pase&&b.pase.de?b.pase.de.eq:BK.pos);j.dec-=dt;
 if(BK.fase==='muerta'){return}
 // balón suelto o en un tiro: a por el rebote
 if(!b.hold&&!b.pase){const libre=b.st==='suelo'||(b.tiro&&(b.toque||b.vy<0));const cerca=BK.J.filter(o=>!o.tiro).sort((p,q)=>Math.hypot(p.x-b.x,p.z-b.z)-Math.hypot(q.x-b.x,q.z-b.z));
  if(cerca.indexOf(j)<(full?4:3)||b.st==='suelo'){let lx=b.x,lz=b.z;if(b.st==='aire'){const tf=Math.max(0,(b.vy+Math.sqrt(Math.max(0,b.vy*b.vy+2*BKG*(b.y-1.6))))/BKG);lx=b.x+b.vx*Math.min(tf,1.2);lz=b.z+b.vz*Math.min(tf,1.2)}
   if(b.tiro&&!libre){const hx=b.tiro.s*BKHX,dx=j.x-hx,dz=j.z,l=Math.hypot(dx,dz)||1;lx=hx+dx/l*Math.min(l,2.4);lz=dz/l*Math.min(l,2.4)}
   j.tx=lx;j.tz=lz;j.quiereCorrer=true;
   if(b.st==='aire'&&b.y>2.3&&b.vy<0&&Math.hypot(b.x-j.x,b.z-j.z)<1.2&&Math.random()<dt*6)bkSaltar(j,.8,.6)}
  return}
 const ataco=j.eq===eqA;
 if(ataco&&b.hold===j){bkIAbalon(j,dt);return}
 if(ataco){// sin balón: a su sitio y de vez en cuando corta hacia el aro
  if(b.pase&&b.pase.a===j){j.tx=b.pase.px??j.x;j.tz=b.pase.pz??j.z;return}
  if(!j.spot||BK.spotT<=0)bkSpots(eqA);j.corteT-=dt;if(j.corte>0){j.corte-=dt}else if(j.corteT<=0){j.corteT=4+Math.random()*4;if(bkDefDist(j)<1.7&&Math.random()<.6)j.corte=1.4}
  const s=bkAtk(j.eq);if(j.corte>0){j.tx=s*(BKHX-1.3);j.tz=j.spot[1]>0?1.1:-1.1;j.quiereCorrer=true}else{j.tx=j.spot[0];j.tz=j.spot[1];j.quiereCorrer=Math.hypot(j.tx-j.x,j.tz-j.z)>4}
  return}
 // defensa: entre su hombre y el aro
 const m=j.man&&BK.T[eqA].includes(j.man)?j.man:(b.hold||BK.T[eqA][0]);const s=bkAtk(eqA),hx=s*BKHX,dx=hx-m.x,dz=-m.z,l=Math.hypot(dx,dz)||1;
 let gap=m===b.hold?1.05:1.9;if(full&&s*m.x<0)gap=m===b.hold?2.2:4;if(m!==b.hold&&l>8)gap+=1;
 j.tx=m.x+dx/l*Math.min(gap,l*.6);j.tz=m.z+dz/l*Math.min(gap,l*.6);j.quiereCorrer=Math.hypot(j.tx-j.x,j.tz-j.z)>2.5;
 if(m===b.hold&&!m.tiro){const d=Math.hypot(m.x-j.x,m.z-j.z);if(d<1.3&&j.robCD<=0&&Math.random()<dt*(.16*BK.dif.df)*(j.eq===0?.7:1)*(m.run>.8?1.6:1))bkRobar(j)}
 if(j.puntea!=null){j.puntea-=dt;if(j.puntea<=0){j.puntea=null;bkSaltar(j,.8,.6)}}}
function bkSpots(eq){BK.spotT=1.6;const SP=BK.M.full?BK_SP5:BK_SP3,h=BK.ball.hold,us=[];const pts=SP.map(p=>bkSpot(eq,p[0],p[1]));
 for(const j of BK.T[eq]){if(j===h)continue;let best=null,bs=-1;for(const p of pts){if(us.includes(p))continue;let m=99;if(h)m=Math.hypot(p[0]-h.x,p[1]-h.z);for(const u of us)m=Math.min(m,Math.hypot(p[0]-u[0],p[1]-u[1]));const sc=Math.min(m,6)-Math.hypot(p[0]-j.x,p[1]-j.z)*.15;if(sc>bs){bs=sc;best=p}}
  if(best){us.push(best);j.spot=best}}}
function bkIAbalon(j,dt){const s=bkAtk(j.eq),hx=s*BKHX,dist=Math.hypot(hx-j.x,j.z),dd=bkDefDist(j),full=BK.M.full;j.holdT+=dt;
 if(j.tiro)return;
 const limp=!full&&BK.limpiar[j.eq];
 if(limp){const top=bkSpot(j.eq,7.7,Math.max(-3,Math.min(3,j.z)));j.tx=top[0];j.tz=top[1];j.quiereCorrer=false;return}
 if(full&&s*j.x<1.5){j.tx=s*5.5;j.tz=j.z*.6;j.quiereCorrer=dd>2.5;if(j.holdT>4&&j.dec<=0){j.dec=.4;if(Math.random()<.35)bkPasar(j,null)}return}
 if(j.dec>0)return;j.dec=.22+Math.random()*.12;const ia=j.eq===1?BK.dif.ia:1;
 if(BK.c24>0&&BK.c24<2.2&&BK.M.c24){bkTiroEmpieza(j,true);return}
 if(dist<2.4&&dd>.8){bkTiroEmpieza(j,true);return}
 const tres=bkFuera(j.x,j.z,s);
 if(!tres&&dist<6.3&&dd>1.5&&Math.random()<.5*ia){bkTiroEmpieza(j,true);return}
 if(tres&&dist<7.8&&dd>2&&Math.random()<.3*ia*(.6+j.sk.tiro)){bkTiroEmpieza(j,true);return}
 // ¿hay un defensor delante?
 const d=bkDefensor(j);let delante=false;if(d){const ax=hx-j.x,az=-j.z,al=Math.hypot(ax,az)||1,ox=d.x-j.x,oz=d.z-j.z;delante=(ox*ax+oz*az)/al>.2&&Math.abs((ox*az-oz*ax)/al)<1.2&&Math.hypot(ox,oz)<1.7}
 if(!delante||d.aturd>0){j.tx=hx-s*.7;j.tz=j.z*.4+(d?(j.z>d.z?.8:-.8):0);j.quiereCorrer=dist>3;return}
 if(j.cd<=0&&Math.random()<.16*ia){bkFinta(j,{x:0,z:0,l:0});return}
 if(BK.T[j.eq].length>1&&j.holdT>1.3&&Math.random()<.55){let best=null,bo=1.6;for(const o of BK.T[j.eq]){if(o===j)continue;const od=bkDefDist(o);if(od>bo){bo=od;best=o}}if(best||j.holdT>2.6){bkPasar(j,null,best);return}}
 // amagar a un lado
 const lat=(Math.random()<.5?-1:1)*2.2;j.tx=j.x-s*.3;j.tz=Math.max(-6,Math.min(6,j.z+lat));j.quiereCorrer=false}
// ---- cada fotograma del minijuego (sustituye a updateCar)
function bkUpdate(dt){dt=Math.min(dt,.05);BK.tt+=dt;const b=BK.ball,M=BK.M;if(!b)return;
 if(BK.msgT>0){BK.msgT-=dt;if(BK.msgT<=0)BKH.querySelector('.msg').classList.remove('on')}
 if(BK.ultPase)BK.ultPase.t-=dt;BK.spotT-=dt;
 // reloj
 if(BK.fase==='juego'){BK.reloj-=dt;if(M.c24&&b.hold&&BK.modo!=='ent'){BK.c24-=dt;if(BK.c24<=0){BK.dbg.c24[b.hold?b.hold.eq:0]++;bkSnd('silbato');bkMsg('⏱️ ¡Posesión!',M.c24+' segundos',1.1);const h=b.hold;b.hold=null;b.st='muerta';bkSaque(1-h.eq,bkAtk(h.eq),M.full?[h.x,h.z]:null);BK.c24=M.c24}}
  if(BK.reloj<=0&&!b.tiro&&BK.modo!=='ent'){BK.reloj=0;if(BK.pts[0]===BK.pts[1]&&!BK.oro){BK.oro=true;bkMsg('⭐ ¡Canasta de oro!','la siguiente canasta gana',1.8);bkSnd('bocina')}else if(!BK.oro){BK.fase='fin';bkFinal()}}
  if(BK.reloj<=0&&BK.modo==='ent'&&!b.tiro){BK.reloj=0;BK.fase='fin';bkSnd('bocina');bkMsg('⏱️ ¡Tiempo!',BK.st.pts+' puntos',1.5);setTimeout(()=>bkTerminar('fin'),1500)}}
 if(BK.fase==='muerta'){BK.muertaT-=dt;if(BK.muertaT<=0){BK.fase='juego';const f=BK.muertaFn;BK.muertaFn=null;if(f)f();bkFormacionSuelta()}}
 // entrenamiento: el balón vuelve solo
 if(BK.modo==='ent'&&BK.fase==='juego'){const y=BK.T[0][0];if(!b.hold&&!b.pase){BK.ent.t+=dt;if(BK.ent.vuelta>0){BK.ent.vuelta-=dt}
   const parado=b.st==='suelo'&&Math.hypot(b.vx,b.vz)<1.5;if((BK.ent.vuelta<0)||(BK.ent.t>(parado?.6:3.2)&&!(b.tiro&&b.y>2))){BK.ent.vuelta=0;BK.ent.t=0;b.st='aire';b.tiro=null;b.x=13;b.z=(Math.random()-.5)*2;b.y=1.2;b.pase={a:y,de:null};b.ign=null;
    const dx=y.x-b.x,dz=y.z-b.z,dh=Math.hypot(dx,dz),Tt=Math.max(.3,dh/11);b.vx=dx/Tt;b.vz=dz/Tt;b.vy=(1.3-b.y+.5*BKG*Tt*Tt)/Tt;bkEntFallo()}}
  else{BK.ent.t=0}}
 // jugadores
 const inp=bkInput(),sprint=BK.k.sh||BK.padSh||(BK.joy.on&&inp.l>.92);
 for(const j of BK.J){j.cd=Math.max(0,j.cd-dt);j.robCD=Math.max(0,j.robCD-dt);j.aturd=Math.max(0,j.aturd-dt);j.anim=Math.max(0,j.anim-dt);if(j.espera>0)j.espera-=dt;if(j.colgado>0)j.colgado-=dt;
  const yo=j===BK.yo&&!BK.auto;let ax=0,az=0,corre=false,vmax=5.2*j.sk.vel;
  if(yo){ax=inp.x;az=inp.z;corre=sprint;const l=Math.hypot(ax,az);if(l>.05){ax/=l;az/=l;vmax*=Math.min(1,l*1.15)}else{ax=az=0}}
  else{j.quiereCorrer=false;if(j.eq===0&&BK.T[0].length>1||j.eq===1||BK.auto)bkIA(j,dt);if(BK.fase==='muerta'){}const dx=j.tx-j.x,dz=j.tz-j.z,l=Math.hypot(dx,dz);if(l>.12){ax=dx/l;az=dz/l;vmax*=Math.min(1,l/1.2)}corre=j.quiereCorrer}
  if(corre)vmax*=1.3;if(b.hold===j)vmax*=.9;if(j.aturd>0)vmax*=.25;if(j.tiro&&j.tiro.tipo==='salto')vmax*=.08;
  if(j.boost>0){j.boost-=dt;ax=j.bx;az=j.bz;vmax=7.4}
  if(j.tiro&&j.tiro.tipo!=='salto'){const s=j.tiro.s,dx=s*(BKHX-.45)-j.x,dz=-j.z,l=Math.hypot(dx,dz);if(l>.1){ax=dx/l;az=dz/l;vmax=j.tiro.tipo==='mate'?4.5:3.6}}
  if(j.colgado>0){vmax=0}
  const ac=j.salto>0?4:22;j.vx+=(ax*vmax-j.vx)*Math.min(1,ac*dt/Math.max(1,vmax*.4));j.vz+=(az*vmax-j.vz)*Math.min(1,ac*dt/Math.max(1,vmax*.4));
  j.x+=j.vx*dt;j.z+=j.vz*dt;j.run=Math.hypot(j.vx,j.vz)/5.2;
  // salto
  if(j.salto>0){j.salto-=dt;if(j.salto<0)j.salto=0}
  // tiro en marcha
  if(j.tiro){const T=j.tiro;T.t+=dt;if(j===BK.yo&&T.carga&&!BK.auto){const md=BKH.querySelector('.med');md.hidden=false;md.querySelector('i').style.width=Math.min(100,T.t/.78*100)+'%';const u=md.querySelector('u');u.style.left=(.37/.78*100)+'%';u.style.width=(.1/.78*100)+'%';if(T.t>=.78)bkSuelta(j)}
   if(!T.solto&&!T.carga&&T.t>=T.rel&&b.hold===j)bkLanza(j);if(T.t>1.1&&j.salto<=0){j.tiro=null;BKH.querySelector('.med').hidden=true}}}
 // separación entre jugadores y límites
 for(let i=0;i<BK.J.length;i++)for(let k=i+1;k<BK.J.length;k++){const p=BK.J[i],q=BK.J[k],dx=q.x-p.x,dz=q.z-p.z,d=Math.hypot(dx,dz),m=.62;if(d<m&&d>1e-4){const o=(m-d)/2,nx=dx/d,nz=dz/d;
  const wp=b.hold===p?.3:1,wq=b.hold===q?.3:1,ws=wp+wq;p.x-=nx*o*2*wp/ws;p.z-=nz*o*2*wp/ws;q.x+=nx*o*2*wq/ws;q.z+=nz*o*2*wq/ws}}
 for(const j of BK.J){const lx=b.hold===j?13.6:14.6,lz=b.hold===j?7.2:8.1;j.x=Math.max(-lx,Math.min(lx,j.x));j.z=Math.max(-lz,Math.min(lz,j.z));if(!BK.M.full&&BK.modo!=='ent'){j.x=Math.max(-1,j.x)}
  // sacar el balón de la zona (3x3): se cumple al salir de la línea
  if(b.hold===j&&BK.limpiar[j.eq]&&bkFuera(j.x,j.z,bkAtk(j.eq))){BK.limpiar[j.eq]=false;if(j.eq===0)bkMsg('✅ Balón fuera','¡ya puedes tirar!',.7)}}
 // balón
 bkBalon(dt);
 // dibujo
 bkDibujar(dt);bkCamara(dt);bkHud()}
function bkEntFallo(){if(BK.ent.pend){BK.ent.pend=false;if(BK.st.racha>=3)bkMsg('Se acabó la racha','',.7);BK.st.racha=0}}
function bkFormacionSuelta(){for(const j of BK.J){j.tx=j.x;j.tz=j.z}BK.spotT=0}
function bkBalon(dt){const b=BK.ball;if(b.ignT>0){b.ignT-=dt;if(b.ignT<=0)b.ign=null}
 if(b.hold){const j=b.hold,fx=Math.cos(j.ang),fz=-Math.sin(j.ang),rx=-fz,rz=fx;
  if(j.tiro&&!j.tiro.solto){const a=bkAlt(j);b.x=j.x+fx*.2;b.z=j.z+fz*.2;b.y=Math.min(2.4,1.2+j.tiro.t*3)+a}
  else if(BK.fase==='muerta'||j.holdT<.15&&j.run<.1&&j.eq===1&&BK.fase!=='juego'){b.x=j.x+fx*.35;b.z=j.z+fz*.35;b.y=1.05}
  else{const f=j.run>.6?2.6:2.1;const ph0=b.ph;b.ph+=dt*f*Math.PI;if(Math.floor(b.ph/Math.PI)!==Math.floor(ph0/Math.PI))bkSnd('bote',.5);b.x=j.x+fx*.32+rx*.28;b.z=j.z+fz*.32+rz*.28;b.y=BKBR+(.95-BKBR)*Math.abs(Math.cos(b.ph))}
  b.vx=b.vz=b.vy=0;return}
 if(b.st==='muerta')return;
 const N=3,h=dt/N;for(let it=0;it<N;it++){const y0=b.y;b.vy-=BKG*h;b.x+=b.vx*h;b.y+=b.vy*h;b.z+=b.vz*h;
  // suelo
  if(b.y<BKBR){b.y=BKBR;if(b.vy<-.8){bkSnd('bote',Math.min(1,-b.vy/6));b.vy=-b.vy*.72;b.vx*=.9;b.vz*=.9}else{b.vy=0;b.st='suelo';b.vx*=Math.pow(.25,h);b.vz*=Math.pow(.25,h)}}
  else if(b.st==='suelo'&&b.y>BKBR+.01)b.st='aire';
  for(const s of[-1,1]){const cx=s*BKHX;
   // aro (toro): punto más cercano del hierro
   const hx=b.x-cx,hz=b.z,hl=Math.hypot(hx,hz);if(Math.abs(b.y-BKRY)<.3&&hl<BKRR+.3){const qx=cx+(hl>1e-4?hx/hl:1)*BKRR,qz=(hl>1e-4?hz/hl:0)*BKRR,dx=b.x-qx,dy=b.y-BKRY,dz=b.z-qz,d=Math.hypot(dx,dy,dz),m=BKBR+.018;
    if(d<m&&d>1e-5){const nx=dx/d,ny=dy/d,nz=dz/d;b.x=qx+nx*m;b.y=BKRY+ny*m;b.z=qz+nz*m;const vn=b.vx*nx+b.vy*ny+b.vz*nz;if(vn<0){b.vx-=1.55*vn*nx;b.vy-=1.55*vn*ny;b.vz-=1.55*vn*nz;b.vx*=.82;b.vz*=.82;b.vx+=(Math.random()-.5)*.4;b.vz+=(Math.random()-.5)*.4;if(b.aroT<=0){bkSnd('aro',Math.min(1,-vn/3));b.aroT=.12}b.toque=true}}}
   // tablero
   const fx=s*(BKBX-.03);if(Math.abs(b.z)<.9&&b.y>2.9-BKBR&&b.y<3.95+BKBR&&s*(b.x-fx)>-BKBR&&s*(b.x-fx)<.2&&s*b.vx>0){b.x=fx-s*BKBR;b.vx=-b.vx*.55;b.toque=true;bkSnd('aro',.4)}
   // canasta: cruza el aro hacia abajo por dentro
   if(y0>=BKRY&&b.y<BKRY&&b.vy<0&&Math.hypot(b.x-cx,b.z)<BKRR-.035){b.vx*=.35;b.vz*=.35;b.vy*=.6;if(BK.fase==='juego'||BK.oro)bkCanasta(b);b.tiro=null;b.toque=true}
   // poste
   if(s*b.x>14.95&&s*b.x<15.3&&Math.abs(b.z)<.25&&b.y<3.5){b.vx=-b.vx*.5;b.x=s*14.95}}}
 if(b.aroT>0)b.aroT-=dt;
 // fuera de la pista
 if(BK.modo!=='ent'&&BK.fase==='juego'&&(Math.abs(b.x)>14.25||Math.abs(b.z)>7.75)&&b.y<2.2){bkSnd('silbato');bkMsg('🚩 Fuera','',.9);const eq=1-b.ult;BK.dbg.fuera[b.ult]++;b.st='muerta';b.tiro=null;b.pase=null;b.vx=b.vy=b.vz=0;bkSaque(eq,0,[b.x,b.z]);return}
 if(BK.modo==='ent'&&(Math.abs(b.x)>15.5||Math.abs(b.z)>9)){b.x=Math.max(-15,Math.min(15,b.x));b.z=Math.max(-8.8,Math.min(8.8,b.z));b.vx=-b.vx*.3;b.vz=-b.vz*.3}
 if(b.st==='muerta')return;
 // recoger: el más cercano que llegue con la mano
 let quien=null,qd=1e9;if(BK.fase!=='juego')return;for(const j of BK.J){if(j===b.ign||j.aturd>.3||(j.tiro&&!j.tiro.solto))continue;if(b.pase&&b.pase.a!==j&&j.eq===b.pase.a.eq)continue;
  const dh=Math.hypot(b.x-j.x,b.z-j.z),alc=2.45+bkAlt(j)+j.h-1.95;if(dh>.75||b.y>alc)continue;
  if(b.tiro&&!b.toque&&b.y>2)continue;   // no se coge un tiro que sube (salvo tapón)
  if(b.pase&&j.eq!==b.pase.a.eq){if(b.pase.x0==null||Math.hypot(b.x-b.pase.x0,b.z-b.pase.z0)<1.8||Math.hypot(b.x-b.pase.a.x,b.z-b.pase.a.z)<.9)continue;if(j.intercepta===b.pase)continue;j.intercepta=b.pase;if(Math.random()>.2*(j.eq===1?BK.dif.df:.8))continue}
  if(dh<qd){qd=dh;quien=j}}
 if(quien){const eraTiro=b.tiro||b.toque,pase=b.pase;b.tiro=null;b.pase=null;
  if(BK.modo==='ent'){if(!pase)bkEntFallo();bkDar(quien);return}
  if(pase&&quien.eq!==pase.de?.eq&&pase.de){BK.dbg.inter[quien.eq]++;bkMsg(quien.eq===0?'🖐️ ¡Interceptas!':'😱 ¡Interceptado!','',1);if(quien.eq===0)BK.st.rob++;if(!BK.M.full)BK.limpiar[quien.eq]=true}
  else if(eraTiro&&!pase){if(quien.eq===0)BK.st.reb++;if(quien.eq!==b.ult){if(!BK.M.full)BK.limpiar[quien.eq]=true;if(quien.eq===0)bkMsg('💪 Rebote','',.6)}else if(BK.M.c24)BK.c24=Math.max(BK.c24,BK.M.full?14:BK.M.c24)}
  else if(!pase&&quien.eq!==b.ult&&!BK.M.full)BK.limpiar[quien.eq]=true;
  bkDar(quien)}}
// ---- dibujo de jugadores, balón y red
function bkPose(j,dt){const p=j.p,ud=p.userData,pl=ud.piernas.children,ba=ud.brazos.children,b=BK.ball,t=BK.tt;j.ph=(j.ph||0)+dt*(2+j.run*9);
 const amp=Math.min(1,j.run*1.1);animPersona(p,j.ph/14,amp);const def=b&&b.hold&&b.hold.eq!==j.eq&&j.run<.5&&!j.salto&&BK.fase==='juego';
 if(def){for(let i=0;i<2;i++){pl[i].rotation.z+= .45;pl[i].rotation.x=(i?-1:1)*.22;if(pl[i].userData.rod)pl[i].userData.rod.rotation.z=-.85}for(let i=0;i<2;i++){ba[i].rotation.x=(i?-1:1)*1.25;ba[i].rotation.z=.3+Math.sin(t*6+i)*.15;if(ba[i].userData.codo)ba[i].userData.codo.rotation.z=.4}if(ud.tronco)ud.tronco.rotation.z=-.25}
 if(b&&b.hold===j&&!j.tiro){const B=ba[1];B.rotation.z=.6+.35*Math.abs(Math.cos(b.ph))-.25;B.rotation.x=-.35;if(B.userData.codo)B.userData.codo.rotation.z=.3+.3*Math.abs(Math.cos(b.ph))}
 if(j.tiro||j.salto>0&&(j.puntea!==undefined||b.hold!==j)){const k=j.tiro?Math.min(1,j.tiro.t/.35):1;for(let i=0;i<2;i++){ba[i].rotation.z=j.tiro?2.7*k:3.05;ba[i].rotation.x=(i?-1:1)*(j.tiro?.15:.35);if(ba[i].userData.codo)ba[i].userData.codo.rotation.z=j.tiro?(j.tiro.solto?.05:1.2*k):.1}
  for(let i=0;i<2;i++){pl[i].rotation.z=-.15;if(pl[i].userData.rod)pl[i].userData.rod.rotation.z=-.35}}
 if(j.colgado>0){for(let i=0;i<2;i++){ba[i].rotation.z=3.1;if(ba[i].userData.codo)ba[i].userData.codo.rotation.z=0}}
 if(j.anim>0&&!j.tiro){const B=ba[1];B.rotation.z=1.5;if(B.userData.codo)B.userData.codo.rotation.z=.1}}
function bkDibujar(dt){const b=BK.ball;
 for(const j of BK.J){const sp=Math.hypot(j.vx,j.vz);let ang=j.ang;
  if(j.tiro||(b.hold===j&&sp<.4)||(b.hold&&b.hold.eq!==j.eq&&!j.tiro)){const tx=j.tiro?j.tiro.hx:b.hold===j?bkAtk(j.eq)*BKHX:b.hold.x,tz=j.tiro?0:b.hold===j?0:b.hold.z;if(!(b.hold&&b.hold.eq!==j.eq&&!j.tiro)||Math.hypot(tx-j.x,tz-j.z)>.2)ang=Math.atan2(-(tz-j.z),tx-j.x)}
  else if(!b.hold&&sp<.6){ang=Math.atan2(-(b.z-j.z),b.x-j.x)}else if(sp>.3)ang=Math.atan2(-j.vz,j.vx);
  let da=ang-j.ang;da=Math.atan2(Math.sin(da),Math.cos(da));j.ang+=da*Math.min(1,dt*12);
  let y=bkAlt(j);if(j.colgado>0)y=BKRY-1.95;j.G.position.set(j.x,y,j.z);j.G.rotation.y=j.ang;bkPose(j,dt);j.sh.position.set(j.x,.02,j.z);j.sh.scale.setScalar(1-Math.min(.5,y*.4))}
 b.m.position.set(b.x,b.y,b.z);if(b.hold)b.m.rotation.x+=dt*8;else{b.m.rotation.z-=b.vx*dt*4;b.m.rotation.x+=b.vz*dt*4}b.sh.position.set(b.x,.025,b.z);b.sh.scale.setScalar(.45*(1-Math.min(.6,b.y*.12)));
 for(const s of[-1,1]){const r=BKC.red[s];if(!r)continue;r.t+=dt;const w=r.t<1?Math.sin(r.t*22)*Math.exp(-r.t*4):0;r.o.scale.set(1-w*.12,1+w*.25,1-w*.12)}
 const y=BK.yo;if(BK.ind&&y){BK.ind.visible=!BK.auto;BK.ind.position.set(y.x,0,y.z);BK.ind.userData.fl.position.y=2.7+y.h-1.95+bkAlt(y)+Math.sin(BK.tt*5)*.08;BK.ind.userData.fl.rotation.y+=dt*3}
 for(const p of BK.pub){p.ph+=dt;p.salta=Math.max(0,p.salta-dt);p.g.position.y=p.salta>0?Math.abs(Math.sin(p.salta*9))*.35:0;animPersona(p.p,p.ph*.3,0);const ba=p.p.userData.brazos.children;if(p.salta>0)for(const B of ba)B.rotation.z=2.9}}
// cámara de tele: desde la banda de la avenida, alta, siguiendo el balón
function bkCamara(dt){const b=BK.ball,G=BKC.G,full=BK.M.full,ent=BK.modo==='ent';const port=cv.clientWidth<cv.clientHeight;
 let tx=full?(port?Math.max(-10,Math.min(10,b.x)):Math.max(-7.5,Math.min(7.5,b.x*.82))):(port?Math.max(6.5,Math.min(10,6+b.x*.3)):Math.max(3,Math.min(8.2,4.2+b.x*.35))),ty=.6,tz=-.4;
 const D=full?(port?20:15.5):(port?17:12.8),H=full?(port?14:11):(port?12.5:9.6);
 const want=new THREE.Vector3(tx*.96,H,tz+D),lk=new THREE.Vector3(tx,ty,tz);
 if(!BK.cam.ini){BK.cam.p.copy(want);BK.cam.l.copy(lk);BK.cam.ini=true}else{BK.cam.p.lerp(want,Math.min(1,dt*2.6));BK.cam.l.lerp(lk,Math.min(1,dt*3.2))}
 G.updateMatrixWorld();const wp=G.localToWorld(BK.cam.p.clone()),wl=G.localToWorld(BK.cam.l.clone());if(window.__BKCAM){const c=window.__BKCAM;wp.set(c[0],c[1],c[2]);wl.set(c[3],c[4],c[5])}
 pcam.position.copy(wp);pcam.lookAt(wl);pcam.near=.01;pcam.far=200;pcam.fov=port?(full?68:64):(full?44:42);pcam.updateProjectionMatrix();
 {const Wt=TIEMPO.W;FOG.far=34*(1-.7*Wt.fog);FOG.near=6*(1-.85*Wt.fog)}}
function bkHud(){const M=BK.M,s=Math.max(0,Math.ceil(BK.reloj));const q=x=>BKH.querySelector(x);
 if(BK.modo==='ent'){q('.e0 b').textContent=BK.st.pts}else{q('.e0 b').textContent=BK.pts[0];q('.e1 b').textContent=BK.pts[1]}
 q('.rl').textContent=BK.oro?'ORO':Math.floor(s/60)+':'+String(s%60).padStart(2,'0');q('.c24').textContent=M.c24?Math.max(0,Math.ceil(BK.c24)):'';
 const ataque=BK.modo==='ent'||BK.ball.hold?.eq===0||(!BK.ball.hold&&BK.pos===0);if(ataque!==BK.ataqueHud){BK.ataqueHud=ataque;bkCtl()}
 if(BK.ataqueHud&&BK.ball.hold!==BK.yo&&BK.modo!=='ent'&&BK.T[0].length>1){}}
