// ================= Minijuego: Surf en la playa de Patos (Nigrán) · surf.js (lo mete edit_surf.py) =================
// En el GPS, «🎯 Misiones» → «🏄 Surf en Patos»: la línea azul lleva a la playa. En la arena hay una tabla clavada con su aro:
// al llegar (en coche, moto, andando o en moto de agua) sale la ficha de la playa y empieza la sesión (3 minutos).
//  - Esperas sentado en la tabla mirando al mar (con las Cíes al fondo en días claros). Viene una ola: ¡rema! (↑ / Espacio / Ⓐ
//    o el botón Remar varias veces) y si llegas a tiempo te pones de pie.
//  - En la ola: ◀ ▶ subes y bajas por la pared (abajo vas más rápido, arriba haces maniobras). La ola rompe detrás de ti:
//    si te pilla la espuma te caes; si te alejas demasiado, se queda sin fuerza.
//    🌀 Giro (C / Ⓧ): cutback, vuelves hacia la rompiente. 🚀 Aéreo (↑ / Espacio / Ⓐ cerca de la cresta y con velocidad).
//    Al subir a la cresta y bajar de golpe: snap. Metido justo bajo el labio: ¡tubo! El equilibrio se pierde si te pasas
//    de la cresta, si te quedas abajo del todo o con el picado del mar.
//  - Siempre de día o al atardecer (se elige en la ficha; nunca de noche). Al terminar vuelve la hora que había.
//  - Cada maniobra seguida sube el multiplicador (hasta x5). Retos: 3 cutbacks, aguantar 20 s en una ola y 5 olas seguidas
//    sin caerte (la racha se guarda entre sesiones). Dan monedas 🪙 y suben el nivel: olas pequeñas → medianas → grandes,
//    y tablas nuevas (Clásica, Cíes, Monteferro). Se guarda en el navegador (gtvigo_surf).
const SG={on:false,ficha:false,ruta:false,cerca:false,sp:null,fase:'',t:0,tt:0,pts:0,mult:1,multT:0,olas:0,caidas:0,cut:0,maxRide:0,
 k:{l:0,r:0,a:0,b:0},padX:0,W:null,S:null,sf:null,cam:{p:new THREE.Vector3(),l:new THREE.Vector3(),ini:false},msgT:0,retoHecho:{},mk:null,cies:null,prevPie:false};
let SGD=null;try{SGD=JSON.parse(localStorage.getItem('gtvigo_surf')||'null')}catch(e){}
SGD=Object.assign({nivel:1,olas:1,mejor:0,retos:{},racha:0,tabla:0,sesiones:0},SGD||{});
function sgGuardar(){try{localStorage.setItem('gtvigo_surf',JSON.stringify(SGD))}catch(e){}}
const SG_NIV=[null,{n:'Pequeñas',H:.085,T:22,vc:.16,chop:.22},{n:'Medianas',H:.105,T:27,vc:.19,chop:.32},{n:'Grandes',H:.13,T:33,vc:.225,chop:.42}];
const SG_TABLAS=[{n:'Clásica',c:0xf4f1e8,f:0x1f6fd0,traje:0x1b1d22,acento:0x1f6fd0,niv:1},{n:'Cíes',c:0x3fd0c9,f:0xffffff,traje:0x0f3f4a,acento:0x3fd0c9,niv:2},{n:'Monteferro',c:0xd8352a,f:0x15171c,traje:0x241414,acento:0xff9f1a,niv:3}];
const SG_RETOS=[{id:'cut3',n:'Haz 3 cutbacks',ico:'🌀'},{id:'t20',n:'Aguanta 20 segundos en una ola',ico:'⏱️'},{id:'seq5',n:'Surfea 5 olas seguidas sin caerte',ico:'🔥'}];
const SG_DUR=180;
MISIONES.push({id:'surf',ico:'🏄',n:'Surf en Patos',d:'Minijuego en la playa de Patos (Nigrán)',da:'Vas camino de Patos · toca para cancelar',ir:()=>surfIr(),on:()=>SG.ruta,fin:()=>surfCancelar()});
// ---- estilos: ficha de la playa, marcador y HUD del minijuego
{const st=document.createElement('style');st.textContent=`
body.surfg #bNoche,body.surfg .bar,body.surfg #pad,body.surfg #mini,body.surfg #vel,body.surfg #calle,body.surfg #gps,body.surfg #bAcc,body.surfg #taxiHud,body.surfg #contra,body.surfg #aviso,body.surfg #rCuenta,body.surfg #joy,body.surfg #radio,body.surfg #radioPanel,body.surfg .hint{display:none!important}
#sgFicha{position:fixed;inset:0;z-index:40;background:rgba(8,30,44,.55);display:flex;align-items:center;justify-content:center;padding:14px}
#sgFicha[hidden],#sgHud[hidden]{display:none!important}
#sgFicha .c{background:#fffdf7;color:#10232e;border-radius:20px;max-width:460px;width:100%;max-height:92vh;overflow:auto;box-shadow:0 10px 40px rgba(0,0,0,.4);font:500 13px var(--body)}
#sgFicha .foto{position:relative;height:170px;background:linear-gradient(180deg,#8fd3e8,#2a8fb0 60%,#e9d7a8 60%);border-radius:20px 20px 0 0;overflow:hidden}
#sgFicha .foto img{width:100%;height:100%;object-fit:cover;display:block}
#sgFicha .foto small{position:absolute;right:8px;bottom:6px;font:500 10px var(--body);color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.8)}#sgFicha .foto small a{color:#fff}
#sgFicha .foto .sello{position:absolute;left:12px;bottom:10px;background:#ffcf3a;color:#2a1a00;font:800 11px var(--body);letter-spacing:.06em;border-radius:6px;padding:3px 7px}
#sgFicha .in{padding:14px 16px 16px}
#sgFicha h2{margin:0;font:800 22px var(--display,var(--body))}#sgFicha .sub{margin:2px 0 10px;opacity:.7}
#sgFicha ul{list-style:none;margin:0 0 10px;padding:0}#sgFicha li{display:flex;gap:8px;padding:5px 0;border-top:1px solid #eee3cc;line-height:1.35}#sgFicha li i{font-style:normal;flex:none;width:22px;text-align:center}
#sgFicha .prog{background:#f2f7f8;border-radius:12px;padding:8px 10px;margin:8px 0}#sgFicha .prog b{font-weight:800}
#sgFicha .reto{display:flex;gap:6px;align-items:center;margin:3px 0}#sgFicha .reto.ok{color:#14804a}#sgFicha .reto.ok::after{content:' ✓';font-weight:800}
#sgFicha .opt{margin:8px 0 2px;font:700 11px var(--body);letter-spacing:.06em;text-transform:uppercase;opacity:.65}
#sgFicha .sel{display:flex;gap:6px;flex-wrap:wrap}#sgFicha .sel button{flex:1;min-width:90px;border:2px solid #d9e6ea;background:#fff;border-radius:10px;padding:7px 6px;font:700 12px var(--body);cursor:pointer;color:#10232e}
#sgFicha .sel button.on{border-color:#1f6fd0;background:#e6f0fc}#sgFicha .sel button:disabled{opacity:.45;cursor:default}
#sgFicha .acc{display:flex;gap:8px;margin:12px -16px -16px;padding:10px 16px 14px;position:sticky;bottom:0;background:linear-gradient(180deg,rgba(255,253,247,.85),#fffdf7 30%)}#sgFicha .acc button{flex:1;border:0;border-radius:12px;padding:11px;font:800 15px var(--body);cursor:pointer}
#sgFicha .acc .go{background:linear-gradient(135deg,#1fb5c9,#1f6fd0);color:#fff}#sgFicha .acc .no{flex:.6;background:#eef1f2;color:#10232e}
#sgFicha .res{text-align:center;padding:6px 0 2px}#sgFicha .res .p{font:900 40px/1 var(--body);color:#1f6fd0}#sgFicha .res small{display:block;opacity:.7}
#sgFicha .gana{background:#fff4cf;border-radius:10px;padding:6px 10px;margin:6px 0;font-weight:700}
#sgHud{position:fixed;inset:0;z-index:20;pointer-events:none;font:600 13px var(--body);color:#fff}
#sgHud .top{position:absolute;top:calc(10px + env(safe-area-inset-top,0px));left:50%;transform:translateX(-50%);display:flex;gap:8px;align-items:center;pointer-events:auto}
#sgHud .top>div{background:rgba(6,30,44,.72);border-radius:12px;padding:5px 10px;text-align:center;min-width:52px}
#sgHud .top b{display:block;font:900 20px/1.05 var(--body)}#sgHud .top small{font:600 10px var(--body);opacity:.8}
#sgHud .top .mul b{color:#ffcf3a}#sgHud .x{border:0;background:rgba(6,30,44,.72);color:#fff;border-radius:999px;width:34px;height:34px;font:800 14px var(--body);cursor:pointer}
#sgHud .bal{position:absolute;top:calc(64px + env(safe-area-inset-top,0px));left:50%;transform:translateX(-50%);width:min(260px,60vw);height:10px;border-radius:6px;background:rgba(6,30,44,.6);overflow:hidden}
#sgHud .bal i{display:block;height:100%;width:0;background:linear-gradient(90deg,#3fe07a,#ffcf3a 60%,#e0352b);transition:width .1s}
#sgHud .bal span{position:absolute;inset:0;font:700 8px/10px var(--body);text-align:center;letter-spacing:.1em;color:#fff;text-shadow:0 1px 2px #000}
#sgHud .retos{position:absolute;top:calc(84px + env(safe-area-inset-top,0px));left:max(10px,env(safe-area-inset-left,0px));display:flex;flex-direction:column;gap:3px}
#sgHud .retos div{background:rgba(6,30,44,.6);border-radius:8px;padding:3px 8px;font:600 11px var(--body)}#sgHud .retos div.ok{background:rgba(20,128,74,.85)}
#sgHud .msg{position:absolute;top:30%;left:50%;transform:translate(-50%,-50%);text-align:center;font:900 30px/1.1 var(--body);text-shadow:0 3px 12px rgba(0,0,0,.55);white-space:nowrap;opacity:0;transition:opacity .2s}
#sgHud .msg small{display:block;font:700 15px var(--body)}#sgHud .msg.on{opacity:1;animation:sgPop .35s}
@keyframes sgPop{0%{transform:translate(-50%,-50%) scale(.6)}70%{transform:translate(-50%,-50%) scale(1.12)}100%{transform:translate(-50%,-50%) scale(1)}}
#sgHud .rema{position:absolute;bottom:calc(150px + env(safe-area-inset-bottom,0px));left:50%;transform:translateX(-50%);width:min(240px,56vw);height:14px;border-radius:8px;background:rgba(6,30,44,.6);overflow:hidden;border:2px solid #fff}
#sgHud .rema i{display:block;height:100%;width:0;background:#1fb5c9}#sgHud .rema[hidden]{display:none}
#sgHud .ctl{position:absolute;left:0;right:0;bottom:calc(14px + env(safe-area-inset-bottom,0px));display:flex;justify-content:space-between;padding:0 max(14px,env(safe-area-inset-left,0px));pointer-events:none}
#sgHud .ctl .g{display:flex;gap:10px;pointer-events:auto}
#sgHud .ctl button{width:74px;height:74px;border-radius:50%;border:3px solid rgba(255,255,255,.85);background:rgba(6,30,44,.55);color:#fff;font:800 13px var(--body);touch-action:none;user-select:none;-webkit-user-select:none;cursor:pointer}
#sgHud .ctl button.on{background:rgba(31,181,201,.8)}#sgHud .ctl button.off{opacity:.35}#sgHud .ctl button span{display:block;font:400 24px/1 system-ui}
#sgHud .tip{position:absolute;bottom:calc(100px + env(safe-area-inset-bottom,0px));left:50%;transform:translateX(-50%);font:600 12px var(--body);background:rgba(6,30,44,.55);padding:4px 10px;border-radius:10px;white-space:nowrap}
@media (pointer:fine){#sgHud .ctl{opacity:.75}#sgHud .ctl button{width:62px;height:62px}}
@media (max-width:700px){#sgHud .msg{font-size:24px}#sgHud .top b{font-size:17px}}`;document.head.appendChild(st)}
// ---- HTML: ficha y HUD
const SGF=document.createElement('div');SGF.id='sgFicha';SGF.hidden=true;document.body.appendChild(SGF);
const SGH=document.createElement('div');SGH.id='sgHud';SGH.hidden=true;SGH.innerHTML=`<div class="top"><div class="pt"><b>0</b><small>puntos</small></div><div class="mul"><b>x1</b><small>combo</small></div><div class="tm"><b>3:00</b><small>tiempo</small></div><div class="ol"><b>0</b><small>olas</small></div><button class="x" title="Salir del surf" aria-label="Salir del surf">✕</button></div>
<div class="bal"><i></i><span>EQUILIBRIO</span></div><div class="retos"></div><div class="msg"></div><div class="rema" hidden><i></i></div><div class="tip"></div>
<div class="ctl"><div class="g"><button data-k="l" aria-label="Izquierda"><span>◀</span></button><button data-k="r" aria-label="Derecha"><span>▶</span></button></div>
<div class="g"><button data-k="b" class="bB" aria-label="Giro"><span>🌀</span>Giro</button><button data-k="a" class="bA" aria-label="Remar"><span>🏊</span>Remar</button></div></div>`;document.body.appendChild(SGH);
SGH.querySelector('.x').onclick=()=>sgTerminar('menu');
SGH.querySelectorAll('.ctl button').forEach(b=>{const k=b.dataset.k;
 const on=e=>{e.preventDefault();e.stopPropagation();if(!SG.k[k]){SG.k[k]=1;if(k==='a')sgBotonA();if(k==='b')sgBotonB()}b.classList.add('on')},off=e=>{SG.k[k]=0;b.classList.remove('on')};
 b.addEventListener('pointerdown',on);b.addEventListener('pointerup',off);b.addEventListener('pointercancel',off);b.addEventListener('pointerleave',off)});
// teclado (antes que el resto del juego: el coche no se mueve mientras surfeas)
addEventListener('keydown',e=>{if(!SG.on&&!SG.ficha)return;const c=e.code;
 if(SG.ficha){if(c==='Escape'){const b=SGF.querySelector('.no');b&&b.click()}else if(c==='Enter'&&!e.repeat){const b=SGF.querySelector('.go');b&&b.click()}if(!/^Tab$/.test(c)){e.stopImmediatePropagation();if(c!=='Enter'||document.activeElement===document.body)e.preventDefault()}return}
 if(c==='ArrowLeft'||c==='KeyA')SG.k.l=1;else if(c==='ArrowRight'||c==='KeyD')SG.k.r=1;
 else if(c==='ArrowUp'||c==='KeyW'||c==='Space'){if(!e.repeat)sgBotonA();SG.k.a=1}
 else if(c==='KeyC'||c==='KeyX'||c==='ShiftLeft'||c==='ShiftRight'||c==='ArrowDown'||c==='KeyS'){if(!e.repeat)sgBotonB();SG.k.b=1}
 else if(c==='Escape'){sgTerminar('menu')}
 else if(c==='KeyM'||c==='KeyN'||c==='KeyR')return;
 e.preventDefault();e.stopImmediatePropagation()},true);
addEventListener('keyup',e=>{if(!SG.on)return;const c=e.code;
 if(c==='ArrowLeft'||c==='KeyA')SG.k.l=0;else if(c==='ArrowRight'||c==='KeyD')SG.k.r=0;else if(c==='ArrowUp'||c==='KeyW'||c==='Space')SG.k.a=0;
 else if(c==='KeyC'||c==='KeyX'||c==='ShiftLeft'||c==='ShiftRight'||c==='ArrowDown'||c==='KeyS')SG.k.b=0;e.stopImmediatePropagation()},true);
// mando: stick/cruceta ◀ ▶, Ⓐ remar/aéreo, Ⓧ o Ⓑ giro, Menú salir (lo llama padTick)
function sgPad(b,ax,dn){const P_=k=>!!(b[k]&&b[k].pressed);let x=Math.abs(ax[0]||0)<.2?0:ax[0];if(P_(14))x=-1;if(P_(15))x=1;SG.padX=x;
 if(dn(0))sgBotonA();SG.padA=P_(0)?1:0;if(dn(2)||dn(1))sgBotonB();if(dn(9))sgTerminar('menu')}
// ---- la playa: orilla, hacia dónde mira y el punto de la arena (se calcula con la textura de la costa)
function sgSpot(){if(SG.sp)return SG.sp;const img=UCO.uCos.value.image;if(!img||!img.data||img.width<2)return null;
 const W=img.width,H=img.height,d=img.data,R4=UCO.uCoR.value;
 const smp=(x,z,ch)=>{const u=(x-R4.x)/R4.z*W-.5,v=(z-R4.y)/R4.w*H-.5,i=Math.floor(u),j=Math.floor(v),fu=u-i,fv=v-j;
  const g=(a,b)=>{a=Math.max(0,Math.min(W-1,a));b=Math.max(0,Math.min(H-1,b));return d[(b*W+a)*4+ch]/255};
  return (g(i,j)*(1-fu)+g(i+1,j)*fu)*(1-fv)+(g(i,j+1)*(1-fu)+g(i+1,j+1)*fu)*fv};
 const cs=(x,z)=>smp(x,z,3),tierra=(x,z)=>smp(x,z,0)>.97;
 let n=[.57,.82],q=[-24.5-n[0]*1.2,130.3-n[1]*1.2];
 for(let it=0;it<4;it++){const e=.3,gx=cs(q[0]+e,q[1])-cs(q[0]-e,q[1]),gz=cs(q[0],q[1]+e)-cs(q[0],q[1]-e),l=Math.hypot(gx,gz);if(l>1e-4)n=[gx/l,gz/l];
  const c=cs(q[0],q[1]);q=[q[0]+n[0]*(.4-c)*2.5,q[1]+n[1]*(.4-c)*2.5]}
 let S=null;for(let k=0;k<120;k++){const x=q[0]+n[0]*k*.04,z=q[1]+n[1]*k*.04;if(tierra(x,z)){S=[x,z];break}}if(!S)return null;
 let B=[S[0]+n[0]*.2,S[1]+n[1]*.2];for(let k=0;k<10;k++){const t=cell(B[0],B[1]).t;if(t>=1&&t<=5)break;B=[B[0]+n[0]*.05,B[1]+n[1]*.05]}
 SG.sp={n,t:[-n[1],n[0]],S,B,cs,tierra,o:S};return SG.sp}
const sgSm=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t)},sgL=(a,b,t)=>a+(b-a)*t;
function sgWY(){return typeof SURF!=='undefined'&&SURF.m&&SURF.yOk?SURF.m.position.y-.0015:-.03}
// ---- marcador en la arena: tabla clavada + aro amarillo
function sgMarca(){const g=new THREE.Group();const tb=new THREE.Mesh(new THREE.SphereGeometry(1,18,10),new THREE.MeshStandardMaterial({color:0x1fb5c9,roughness:.35}));tb.scale.set(.0085,.03,.0022);tb.position.y=.026;g.add(tb);
 const fr=new THREE.Mesh(new THREE.BoxGeometry(.0012,.05,.0046),new THREE.MeshStandardMaterial({color:0xffffff,roughness:.4}));fr.position.y=.026;g.add(fr);
 const r=new THREE.Mesh(new THREE.RingGeometry(.075,.095,32),new THREE.MeshBasicMaterial({color:0xffc21a,transparent:true,opacity:.8,side:THREE.DoubleSide,depthWrite:false,fog:false}));r.rotation.x=-Math.PI/2;r.position.y=.008;g.add(r);g.userData.r=r;
 const c=new THREE.Mesh(new THREE.CylinderGeometry(.035,.035,.6,16,1,true),new THREE.MeshBasicMaterial({color:0x1fb5c9,transparent:true,opacity:.25,side:THREE.DoubleSide,depthWrite:false,fog:false}));c.position.y=.3;g.add(c);
 const f=new THREE.Mesh(new THREE.ConeGeometry(.02,.036,4),new THREE.MeshBasicMaterial({color:0x1fb5c9,fog:false}));f.rotation.x=Math.PI;f.position.y=.12;g.add(f);g.userData.f=f;
 g.visible=false;scene.add(g);return g}
// ---- la ola del minijuego: una malla que se rehace cada fotograma (pared, labio que se enrosca, espuma detrás)
const SGW={NR:64,NC:22,m:null,pos:null,col:null,sec:new Float32Array(22*3)};
function sgOlaInit(){if(SGW.m)return;const NR=SGW.NR,NC=SGW.NC,g=new THREE.BufferGeometry();SGW.pos=new Float32Array(NR*NC*3);SGW.col=new Float32Array(NR*NC*4);
 g.setAttribute('position',new THREE.BufferAttribute(SGW.pos,3));g.setAttribute('color',new THREE.BufferAttribute(SGW.col,4));
 const idx=[];for(let r=0;r<NR-1;r++)for(let c=0;c<NC-1;c++){const a=r*NC+c,b=a+1,d=a+NC,e=d+1;idx.push(a,b,d,b,e,d)}g.setIndex(idx);
 SGW.m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({vertexColors:true,transparent:true,roughness:.22,metalness:0,side:THREE.DoubleSide}));SGW.m.frustumCulled=false;SGW.m.renderOrder=2;SGW.m.visible=false;scene.add(SGW.m)}
// parámetros de cada franja de la ola según su distancia a la rompiente (σ>0 por delante, σ<0 ya rota)
function sgFila(W,sg){let b,k,H;
 if(W.rota){b=1;k=0;H=W.H*.42}
 else{const pk=W.pk;b=(1-sgSm(-.35,-.05,sg))*pk;k=sgSm(-.3,-.08,sg)*(1-.95*sgSm(.05,1.1,sg))*pk;
  H=W.H*(1-.5*b)*(1-.7*sgSm(1.1,3.2,sg))*(pk+(1-pk)*(1-.55*sgSm(.4,3.2,Math.abs(sg))))}
 const ed=sgSm(-2.6,-1.9,sg)*(1-sgSm(2.9,3.6,sg));return{b,k,H:H*ed,ed}}
// sección de la ola: [d (hacia la orilla), y, parte] · parte 0 espalda, 1 labio, 2 pared, 3 llano
function sgSeccion(H,k,out){const Bw=4.2*H+.05,Fw=2.6*H+.03;let i=0;const put=(d,y,p)=>{out[i*3]=d;out[i*3+1]=y;out[i*3+2]=p;i++};
 for(let j=0;j<6;j++){const d=-Bw*(1-j/6);put(d,H*Math.exp(-Math.pow(2*d/Bw,2)),0)}
 put(0,H,1);const R=.55*H*k;for(let j=1;j<=5;j++){const th=j/5*2.5*k;put(R*Math.sin(th),H-R*(1-Math.cos(th))+.12*H*k*Math.sin(th),1)}
 const f0=.22*H*k;for(let j=0;j<8;j++){const u=j/7,d=f0+(Fw-f0)*u;put(d,H*(1-.35*k)*Math.pow(1-u,2),2)}
 put(Fw+.12,0,3);put(Fw+.4,0,3);return{Bw,Fw,f0}}
// altura del agua de la ola en un punto (para flotar esperando)
function sgAltura(H,d){const Bw=4.2*H+.05,Fw=2.6*H+.03;return d<0?H*Math.exp(-Math.pow(2*d/Bw,2)):d<Fw?H*Math.pow(1-d/Fw,2):0}
function sgOlaUpd(){const W=SG.W,sp=SG.sp;if(!W||!SGW.m)return;const NR=SGW.NR,NC=SGW.NC,pos=SGW.pos,col=SGW.col,sec=SGW.sec,n=sp.n,t=sp.t,o=sp.o,WY=sgWY()+.0025,tt=SG.tt;
 for(let r=0;r<NR;r++){const sg=-2.6+6.2*r/(NR-1),F=sgFila(W,sg),L=(W.c+sg)*W.dir;sgSeccion(Math.max(F.H,.0005),F.k,sec);
  for(let c=0;c<NC;c++){const d=sec[c*3],y0=sec[c*3+1],pa=sec[c*3+2],w=W.wc+d,x=o[0]+t[0]*L+n[0]*w,z=o[1]+t[1]*L+n[1]*w,i=r*NC+c;
   const lm=1-sgSm(.82,.95,sp.cs(x,z));let y=y0*lm;pos[i*3]=x;pos[i*3+1]=WY+y;pos[i*3+2]=z;
   const hh=F.H>.001?Math.min(1,y0/F.H):0;let cr,cg,cb;
   if(pa===0){cr=sgL(.025,.07,hh*hh);cg=sgL(.15,.38,hh*hh);cb=sgL(.36,.46,hh*hh)}
   else if(pa===1){cr=sgL(.09,.85,F.k*.75);cg=sgL(.45,.92,F.k*.75);cb=sgL(.48,.94,F.k*.75)}
   else if(pa===2){const q=Math.pow(hh,1.2);cr=sgL(.03,.14,q);cg=sgL(.18,.6,q);cb=sgL(.38,.54,q);if(hh>.8){const lf=(hh-.8)*5*F.k*.6;cr=sgL(cr,.9,lf);cg=sgL(cg,.94,lf);cb=sgL(cb,.95,lf)}}
   else{cr=.03;cg=.16;cb=.4}
   const fo=F.b*(.7+.3*Math.sin(L*23+w*31-tt*3)*Math.sin(L*7-tt*1.3+w*9))*(pa===3?.35:1);if(fo>0){cr=sgL(cr,.93,fo);cg=sgL(cg,.96,fo);cb=sgL(cb,.97,fo)}
   const ae=(c===0||c===NC-1)?0:(c===1||c===NC-2)?.3:c===NC-3?.75:1;col[i*4]=cr;col[i*4+1]=cg;col[i*4+2]=cb;col[i*4+3]=ae*F.ed*lm*W.alfa}}
 const g=SGW.m.geometry;g.attributes.position.needsUpdate=true;g.attributes.color.needsUpdate=true;g.computeVertexNormals();SGW.m.visible=true}
// ---- espuma y salpicaduras (partículas)
const SGP={N:600,i:0,pos:null,vel:null,life:null,pts:null};
function sgPartInit(){if(SGP.pts)return;const N=SGP.N;SGP.pos=new Float32Array(N*3);SGP.vel=new Float32Array(N*3);SGP.life=new Float32Array(N);for(let i=0;i<N;i++)SGP.pos[i*3+1]=-99;
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(SGP.pos,3));
 const c=document.createElement('canvas');c.width=c.height=32;const x=c.getContext('2d'),gr=x.createRadialGradient(16,16,0,16,16,16);gr.addColorStop(0,'rgba(255,255,255,1)');gr.addColorStop(.45,'rgba(255,255,255,.7)');gr.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=gr;x.fillRect(0,0,32,32);
 SGP.pts=new THREE.Points(g,new THREE.PointsMaterial({size:.012,map:new THREE.CanvasTexture(c),transparent:true,depthWrite:false,color:0xf2fbff}));SGP.pts.frustumCulled=false;SGP.pts.renderOrder=3;scene.add(SGP.pts)}
function sgSpray(x,y,z,vx,vy,vz,n,sp){for(let k=0;k<n;k++){const i=SGP.i=(SGP.i+1)%SGP.N;SGP.pos[i*3]=x;SGP.pos[i*3+1]=y;SGP.pos[i*3+2]=z;
 SGP.vel[i*3]=vx+(Math.random()-.5)*sp;SGP.vel[i*3+1]=vy+Math.random()*sp;SGP.vel[i*3+2]=vz+(Math.random()-.5)*sp;SGP.life[i]=.45+Math.random()*.6}}
function sgPartTick(dt){if(!SGP.pts)return;const p=SGP.pos,v=SGP.vel,WY=sgWY();for(let i=0;i<SGP.N;i++){if(SGP.life[i]<=0)continue;SGP.life[i]-=dt;v[i*3+1]-=.32*dt;
 p[i*3]+=v[i*3]*dt;p[i*3+1]+=v[i*3+1]*dt;p[i*3+2]+=v[i*3+2]*dt;if(SGP.life[i]<=0||p[i*3+1]<WY-.01){SGP.life[i]=0;p[i*3+1]=-99}}SGP.pts.geometry.attributes.position.needsUpdate=true}
// ---- las Cíes al fondo (siluetas sacadas del mapa, sin niebla) en días claros
function sgCies(){if(SG.cies||!MAPA)return;const x0=-90,x1=-58,z0=0,z1=92,st=.5,nx=Math.round((x1-x0)/st)+1,nz=Math.round((z1-z0)/st)+1,N=nx*nz;
 const L=new Float32Array(N);for(let j=0;j<nz;j++)for(let i=0;i<nx;i++){const t=cell(x0+i*st,z0+j*st).t;L[j*nx+i]=(t>=1&&t<=5)?1:0}
 let A=L.slice();for(let it=0;it<5;it++){const B=new Float32Array(N);for(let j=0;j<nz;j++)for(let i=0;i<nx;i++){let s=0,c=0;for(let dj=-1;dj<=1;dj++)for(let di=-1;di<=1;di++){const ii=i+di,jj=j+dj;if(ii<0||jj<0||ii>=nx||jj>=nz)continue;s+=A[jj*nx+ii];c++}B[j*nx+i]=s/c}A=B}
 const pos=new Float32Array(N*3),col=new Float32Array(N*3);for(let j=0;j<nz;j++)for(let i=0;i<nx;i++){const k=j*nx+i,h=L[k]?.05+Math.pow(A[k],1.6)*3.2*(.8+.4*Math.sin(i*.7)*Math.sin(j*.45)):-.35;
  pos[k*3]=x0+i*st;pos[k*3+1]=h;pos[k*3+2]=z0+j*st;const q=Math.max(0,Math.min(1,h/3));col[k*3]=sgL(.52,.62,q);col[k*3+1]=sgL(.6,.68,q);col[k*3+2]=sgL(.6,.66,q)}
 const idx=[];for(let j=0;j<nz-1;j++)for(let i=0;i<nx-1;i++){const a=j*nx+i;if(!(L[a]||L[a+1]||L[a+nx]||L[a+nx+1]))continue;idx.push(a,a+nx,a+1,a+1,a+nx,a+nx+1)}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(pos,3));g.setAttribute('color',new THREE.BufferAttribute(col,3));g.setIndex(idx);
 SG.cies=new THREE.Mesh(g,new THREE.MeshBasicMaterial({vertexColors:true,fog:false}));SG.cies.visible=false;SG.cies.renderOrder=-2;scene.add(SG.cies)}
// ---- el surfista: el protagonista con neopreno, descalzo, y su tabla
function sgSurfista(){const g=new THREE.Group(),tabla=new THREE.Group();g.add(tabla);
 const bm=new THREE.MeshStandardMaterial({color:0xf4f1e8,roughness:.3}),fm=new THREE.MeshStandardMaterial({color:0x1f6fd0,roughness:.4});
 const b=new THREE.Mesh(new THREE.SphereGeometry(1,24,10),bm);b.scale.set(.029,.0022,.0088);tabla.add(b);
 const f1=new THREE.Mesh(new THREE.BoxGeometry(.05,.0006,.0016),fm);f1.position.y=.0019;tabla.add(f1);
 const f2=new THREE.Mesh(new THREE.BoxGeometry(.012,.0006,.012),fm);f2.position.set(.02,.0018,0);f2.scale.set(1,1,.9);tabla.add(f2);
 const q=new THREE.Mesh(new THREE.BoxGeometry(.006,.006,.0008),fm);q.position.set(-.024,-.0035,0);tabla.add(q);
 const p=mkPersona();p.scale.setScalar(.8);g.add(p);const mats=new Set();p.traverse(o=>{if(o.isMesh&&o.material)mats.add(o.material)});
 g.visible=false;scene.add(g);return{g,tabla,p,bm,fm,mats:[...mats].map(m=>({m,h:m.color?m.color.getHex():0}))}}
function sgVestir(){const S=SG.sf,T=SG_TABLAS[SGD.tabla]||SG_TABLAS[0];S.bm.color.set(T.c);S.fm.color.set(T.f);
 for(const{m,h}of S.mats){if(m.map)continue;const c=m.color;
  if(h===0xf6f5f1||h===0x2f5596)c.set(T.traje);else if(h===0xdcdad4||h===0x4a74b8)c.set(T.traje).multiplyScalar(1.25);else if(h===0x2b8fd6)c.set(T.acento);
  else if(h===0xf4f3ee||h===0xf2efe8)c.set(0xf0bf94);else if(h===0x2a2c33)c.set(0xe2a47c)}}
function sgPose(p,pose,t,x={}){const ud=p.userData,pl=ud.piernas.children,ba=ud.brazos?ud.brazos.children:[];p.rotation.set(0,0,0);p.position.set(0,0,0);
 for(const L of pl){L.rotation.set(0,0,0);if(L.userData.rod)L.userData.rod.rotation.set(0,0,0)}for(const B of ba){B.rotation.set(0,0,0);if(B.userData.codo)B.userData.codo.rotation.set(0,0,0)}
 if(ud.tronco)ud.tronco.rotation.set(0,0,0);if(ud.cabeza)ud.cabeza.rotation.set(0,0,0);
 if(pose==='sentado'){p.position.set(-.004,.0022-.0215+Math.sin(t*1.7)*.0006,0);for(let i=0;i<2;i++){pl[i].rotation.z=1.45;pl[i].rotation.x=(i?-1:1)*.25;if(pl[i].userData.rod)pl[i].userData.rod.rotation.z=-1.5+Math.sin(t*2+i)*.15}
  for(let i=0;i<ba.length;i++){ba[i].rotation.z=.25;ba[i].rotation.x=(i?-1:1)*.25;if(ba[i].userData.codo)ba[i].userData.codo.rotation.z=.5}if(ud.cabeza)ud.cabeza.rotation.y=Math.sin(t*.6)*.3}
 else if(pose==='rema'){p.rotation.z=-Math.PI/2;p.position.set(-.031,.0022+.0052,0);for(let i=0;i<2;i++){pl[i].rotation.z=Math.sin(t*9+i*3)*.12}
  for(let i=0;i<ba.length;i++){ba[i].rotation.z=Math.PI+(t*(x.v||7)+i*Math.PI);ba[i].rotation.x=(i?-1:1)*.25}if(ud.cabeza)ud.cabeza.rotation.z=.6}
 else if(pose==='pie'||pose==='aire'){const cr=pose==='aire'?1.3:(x.cr||1);p.rotation.y=x.lado||Math.PI/2;p.position.y=.0022-.0045*cr;
  for(let i=0;i<2;i++){pl[i].rotation.x=(i?-1:1)*.42;pl[i].rotation.z=.38*cr;if(pl[i].userData.rod)pl[i].userData.rod.rotation.z=-.75*cr}
  for(let i=0;i<ba.length;i++){ba[i].rotation.x=(i?-1:1)*(pose==='aire'?1.9:1.15+(x.br||0)*(i?1:-1));ba[i].rotation.z=.15;if(ba[i].userData.codo)ba[i].userData.codo.rotation.z=.3}
  if(ud.tronco){ud.tronco.rotation.z=-.28*cr;ud.tronco.rotation.x=x.inc||0}if(ud.cabeza)ud.cabeza.rotation.y=x.mira||0}
 else if(pose==='cae'){const q=Math.min(1,t/1.2);p.rotation.z=-q*3.4;p.rotation.x=q*1.2;p.position.set(.02*q,.03*Math.sin(q*Math.PI)-.03*q*q,.01*q);
  for(let i=0;i<2;i++){pl[i].rotation.z=Math.sin(t*14+i*2)*.9;pl[i].rotation.x=(i?-1:1)*.6}for(let i=0;i<ba.length;i++){ba[i].rotation.z=Math.sin(t*12+i*2.5)*1.6;ba[i].rotation.x=(i?-1:1)*1.4}}}
// ---- sonidos (sintetizados con el ruido del juego)
function sgSnd(tipo){try{if(typeof AC==='undefined'||!AC||!master||!NB||!soundOn)return;const t=AC.currentTime,s=AC.createBufferSource(),f=AC.createBiquadFilter(),g=AC.createGain();s.buffer=NB;
 const P_={salpica:[1500,.6,.32,.9,.006],giro:[2800,1.1,.16,.5,.03],caida:[700,.5,.55,1.4,.01],ola:[450,.6,.22,1.8,.35],remo:[1900,1.4,.07,.22,.01]}[tipo];if(!P_)return;
 f.type='bandpass';f.frequency.value=P_[0];f.Q.value=P_[1];g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(P_[2],t+P_[4]);g.gain.exponentialRampToValueAtTime(.0005,t+P_[3]);
 s.connect(f);f.connect(g);g.connect(master);s.start(t,Math.random()*1.5);s.stop(t+P_[3]+.1)}catch(e){}}
function sgDing(n=3){try{if(typeof AC==='undefined'||!AC||!master||!soundOn)return;const t=AC.currentTime;for(let i=0;i<n;i++){const o=AC.createOscillator(),g=AC.createGain();o.type='triangle';o.frequency.value=660*Math.pow(1.26,i);
 g.gain.setValueAtTime(0,t+i*.09);g.gain.linearRampToValueAtTime(.12,t+i*.09+.01);g.gain.exponentialRampToValueAtTime(.0005,t+i*.09+.3);o.connect(g);g.connect(master);o.start(t+i*.09);o.stop(t+i*.09+.35)}}catch(e){}}
function sgRugido(v){try{if(typeof AC==='undefined'||!AC||!master||!NB)return;if(!SG.rg){const s=AC.createBufferSource();s.buffer=NB;s.loop=true;const f=AC.createBiquadFilter();f.type='lowpass';f.frequency.value=520;SG.rg=AC.createGain();SG.rg.gain.value=0;s.connect(f);f.connect(SG.rg);SG.rg.connect(master);s.start()}
 SG.rg.gain.setTargetAtTime(soundOn?v:0,AC.currentTime,.3)}catch(e){}}
// ---- ficha de la playa (al llegar) y resultados (al terminar)
const SG_FOTO='https://commons.wikimedia.org/wiki/Special:FilePath/Praia_de_Patos,_Nigr%C3%A1n.jpg?width=640',SG_FOTOW='https://commons.wikimedia.org/wiki/File:Praia_de_Patos,_Nigr%C3%A1n.jpg';
const SG_DATOS=[['📍','<b>Dónde:</b> ensenada de Carreira, en Nigrán (Pontevedra). Arenal de unos 1,7 km abierto al océano, con las Islas Cíes enfrente.'],
 ['🚗','<b>Desde Vigo:</b> unos 16 km, de 20 a 30 minutos en coche por la carretera de la costa (PO-325).'],
 ['🚌','<b>En bus:</b> línea Vigo–Baiona, parada en Patos (unos 30 minutos desde Vigo).'],
 ['🌊','<b>La ola:</b> beach break de arena y roca con varios picos. Entra con mar del norte, noroeste y oeste, mejor de media marea a pleamar y con viento del sur o del este.'],
 ['🎯','<b>Nivel:</b> para todos. Es la playa donde aprende a surfear medio Vigo: hay varias escuelas de surf.'],
 ['📅','<b>Mejor época:</b> otoño e invierno, cuando entra más mar; en verano las olas son pequeñas, ideales para aprender (y la playa se llena: llega pronto).'],
 ['🌅','<b>Consejo:</b> quédate al atardecer: el sol se pone detrás de las Cíes.']];
function sgRetosHtml(ses){return SG_RETOS.map(r=>{const ok=ses?!!SG.retoHecho[r.id]:!!SGD.retos[r.id];return `<div class="reto${ok?' ok':''}">${r.ico} ${r.n}${r.id==='seq5'&&!ok?` <small>(racha: ${SGD.racha})</small>`:''}</div>`}).join('')}
function sgSel(){const bo=SG_NIV.slice(1).map((v,i)=>`<button data-o="${i+1}" class="${SGD.olas===i+1?'on':''}" ${i+1>SGD.nivel?'disabled':''}>${i+1>SGD.nivel?'🔒 ':''}${v.n}</button>`).join('');
 const bt=SG_TABLAS.map((v,i)=>`<button data-t="${i}" class="${SGD.tabla===i?'on':''}" ${v.niv>SGD.nivel?'disabled':''}><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:#${v.c.toString(16).padStart(6,'0')};border:1px solid #0003"></span> ${v.niv>SGD.nivel?'🔒 ':''}${v.n}</button>`).join('');
 const bh=[['dia','☀️ De día'],['tarde','🌅 Atardecer']].map(([k,t])=>`<button data-h="${k}" class="${sgHora()===k?'on':''}">${t}</button>`).join('');
 return `<div class="opt">Hora</div><div class="sel sh">${bh}</div><div class="opt">Olas</div><div class="sel so">${bo}</div><div class="opt">Tabla</div><div class="sel st">${bt}</div>`}
// hora de la sesión: siempre de día o al atardecer, nunca de noche (si no la has elegido, la que se parezca a la hora del juego)
function sgHora(){return SGD.hora||(CIELO.h>=18.3&&CIELO.h<22.5?'tarde':'dia')}
function sgFicha(modo){const fin=modo==='fin';SG.ficha=true;
 const cab=`<div class="foto"><span class="sello">PLAYA REAL · RÍAS BAIXAS</span><small>Foto: HombreDHojalata · <a href="${SG_FOTOW}" target="_blank" rel="noopener">Wikimedia Commons</a></small></div>`;
 let cuerpo;
 if(!fin){cuerpo=`<h2>🏄 Playa de Patos</h2><p class="sub">Nigrán · a unos 20–30 min de Vigo</p><ul>${SG_DATOS.map(d=>`<li><i>${d[0]}</i><span>${d[1]}</span></li>`).join('')}</ul>
  <div class="prog">Nivel <b>${SGD.nivel}</b> · récord <b>${SGD.mejor}</b> puntos${typeof TAXI!=='undefined'?' · 🪙 '+TAXI.mon:''}${sgRetosHtml(false)}</div>${sgSel()}
  <div class="acc"><button class="no">Ahora no</button><button class="go">🏄 ¡A surfear!</button></div><p class="sub" style="margin:8px 0 0;font-size:11px">◀ ▶ subir y bajar por la ola · ↑/Espacio remar y aéreo · C giro (cutback)</p>`}
 else{const R=SG.res;cuerpo=`<h2>🏄 ¡Sesión terminada!</h2><p class="sub">Playa de Patos · Nigrán</p><div class="res"><div class="p">${R.pts}</div><small>puntos${R.record?' · 🏆 ¡nuevo récord!':' · récord '+SGD.mejor}</small></div>
  <ul><li><i>🌊</i><span>${R.olas} ola${R.olas===1?'':'s'} surfeada${R.olas===1?'':'s'} · ${R.caidas} revolcón${R.caidas===1?'':'es'}</span></li><li><i>⏱️</i><span>Ola más larga: ${R.maxRide.toFixed(1).replace('.',',')} s</span></li><li><i>🌀</i><span>${R.cut} cutback${R.cut===1?'':'s'}</span></li></ul>
  ${R.gana?`<div class="gana">${R.gana}</div>`:''}<div class="prog">Retos de la sesión${sgRetosHtml(true)}</div>${sgSel()}
  <p class="sub" style="margin:10px 0 0">📍 Playa de Patos (Nigrán): beach break para todos los niveles, frente a las Cíes. Otoño e invierno, más mar; verano, olas para aprender.</p>
  <div class="acc"><button class="no">Salir</button><button class="go">🔁 Otra sesión</button></div>`}
 SGF.innerHTML=`<div class="c">${cab}<div class="in">${cuerpo}</div></div>`;SGF.hidden=false;
 {const im=new Image();im.alt='Playa de Patos, Nigrán';im.decoding='async';im.onload=()=>{const f=SGF.querySelector('.foto');if(f&&!f.querySelector('img'))f.prepend(im)};im.onerror=()=>{};im.src=SG_FOTO}
 SGF.querySelectorAll('.so button').forEach(b=>b.onclick=()=>{SGD.olas=+b.dataset.o;sgGuardar();SGF.querySelectorAll('.so button').forEach(x=>x.classList.toggle('on',x===b))});
 SGF.querySelectorAll('.sh button').forEach(b=>b.onclick=()=>{SGD.hora=b.dataset.h;sgGuardar();SGF.querySelectorAll('.sh button').forEach(x=>x.classList.toggle('on',x===b))});
 SGF.querySelectorAll('.st button').forEach(b=>b.onclick=()=>{SGD.tabla=+b.dataset.t;sgGuardar();SGF.querySelectorAll('.st button').forEach(x=>x.classList.toggle('on',x===b))});
 SGF.querySelector('.go').onclick=()=>{SGF.hidden=true;SG.ficha=false;sgEmpezar()};
 SGF.querySelector('.no').onclick=()=>{SGF.hidden=true;SG.ficha=false};
 setTimeout(()=>{const b=SGF.querySelector('.go');b&&b.focus({preventScroll:true})},50);
 if(!fin)try{gtvEv('minijuego/surf-ficha','Surf Patos · ficha')}catch(e){}}
// ---- GPS: ir a Patos
function surfIr(){if(REP.on||RACE.on)return;const sp=sgSpot();if(!sp){mostrar('⏳ Un momento, cargando la costa…');return}
 if(driving&&Math.hypot(sp.B[0]-P.x,sp.B[1]-P.y)<1.2){SG.cerca=true;sgFicha('intro');return}
 if(typeof TAXI!=='undefined'&&TAXI.on)taxiFin('otro');
 // la misión empieza en coche: si vas a pie, en moto de agua, nadando o en helicóptero, te subes a uno en la calle más cercana
 if(!driving)setDrive(true,'coche');
 if(MODO!=='coche'){const G=gpsGrafo(),i=G?gpsNodo(P.x,P.y):-1;if(i>=0){const A=G.ADJ[i];let a=P.a;if(A&&A.length){const j=A[0];a=Math.atan2(-(G.Y[j]-G.Y[i]),G.X[j]-G.X[i])}Object.assign(P,{x:G.X[i],y:G.Y[i],a,v:0});P.z=groundY(P.x,P.y)}
  cambiarModo('coche');camInit=false;mostrar('🚗 Te subes a un coche para ir a Patos')}
 // ruta hasta el aparcamiento de la playa (el punto de la calle más cerca de la tabla en la arena)
 gpsIniciar(['🏄 Playa de Patos (Nigrán)',sp.B[0],sp.B[1]]);
 if(GPS.on){SG.ruta=true;SG.fin=GPS.pts[GPS.pts.length-1].slice();setTimeout(()=>{if(SG.ruta)mostrar('🏄 Sigue la línea azul hasta la playa de Patos ('+fmtD(GPS.acc[GPS.acc.length-1])+')')},MODO==='coche'?0:1700)}}
function surfCancelar(){if(SG.ruta&&GPS.on&&GPS.dest&&/Patos/.test(GPS.dest[0]))gpsParar();SG.ruta=false;mostrar('🏄 Surf cancelado')}
// ---- cada fotograma conduciendo: marcador, llegada a la playa
function surfgTick(dt){if(SG.on)return;const sp=SG.sp||(MAPA&&Math.hypot(P.x+25,P.y-128)<40?sgSpot():null);if(!sp)return;
 if(!SG.mk)SG.mk=sgMarca();const d=Math.hypot(sp.B[0]-P.x,sp.B[1]-P.y),mk=SG.mk;mk.visible=d<30&&!RACE.on&&!REP.on;
 if(mk.visible){const now=performance.now()/1000;mk.position.set(sp.B[0],groundY(sp.B[0],sp.B[1]),sp.B[1]);mk.rotation.y=Math.atan2(sp.n[0],sp.n[1]);mk.userData.f.position.y=.12+Math.sin(now*3)*.02;mk.userData.f.rotation.y=now*2;mk.userData.r.material.opacity=.55+.3*Math.sin(now*4)}
 // fin de la ruta: al llegar al aparcamiento de la playa empieza la misión (aunque no pares del todo)
 if(SG.ruta&&SG.fin&&!SG.ficha&&MODO==='coche'&&Math.hypot(SG.fin[0]-P.x,SG.fin[1]-P.y)<.32){SG.ruta=false;if(GPS.on)gpsParar();P.v=0;SG.cerca=true;sgFicha('intro');return}
 if(SG.ruta&&(!GPS.on||!GPS.dest||!/Patos/.test(GPS.dest[0])))SG.ruta=false;
 if(d>1.4)SG.cerca=false;
 if(!SG.cerca&&!SG.ficha&&d<.6&&Math.abs(P.v)<.15&&!RACE.on&&!REP.on&&MODO!=='heli'){SG.cerca=true;if(SG.ruta){if(GPS.on)gpsParar();SG.ruta=false}P.v=0;sgFicha('intro')}}
// ---- empezar / terminar la sesión
function sgEmpezar(){const sp=sgSpot();if(!sp||!driving)return;sgOlaInit();sgPartInit();sgCies();if(!SG.sf)SG.sf=sgSurfista();sgVestir();
 Object.assign(SG,{on:true,t:SG_DUR,tt:0,pts:0,mult:1,multT:0,olas:0,caidas:0,cut:0,maxRide:0,retoHecho:{},msgT:0});SG.k={l:0,r:0,a:0,b:0};SG.padX=0;SG.cam.ini=false;
 for(const k in keys)keys[k]=false;P.v=0;SG.prevPie=MODO==='pie'&&persona.visible;if(SG.prevPie)persona.visible=false;if(SG.mk)SG.mk.visible=false;
 if(!SG.prevCielo)SG.prevCielo={modo:CIELO.modo,h:CIELO.h};CIELO.modo='surf';CIELO.h=sgHora()==='tarde'?20.45:(SG.prevCielo.h>=9&&SG.prevCielo.h<=18?SG.prevCielo.h:12.5);CIELO.txt='';try{cielo(0)}catch(e){}
 document.body.classList.add('surfg');SGH.hidden=false;SG.sf.g.visible=true;SGD.sesiones++;sgGuardar();sgRetosHud();sgNuevaOla(true);
 try{gtvEv('minijuego/surf','Surf Patos')}catch(e){}}
function sgTerminar(motivo){if(!SG.on)return;SG.on=false;SG.pts=Math.round(SG.pts);SG.padA=0;document.body.classList.remove('surfg');SGH.hidden=true;if(SGW.m)SGW.m.visible=false;if(SG.sf)SG.sf.g.visible=false;if(SG.cies)SG.cies.visible=false;
 if(SGP.pts){SGP.life.fill(0);for(let i=0;i<SGP.N;i++)SGP.pos[i*3+1]=-99;SGP.pts.geometry.attributes.position.needsUpdate=true}
 if(SG.prevCielo){CIELO.modo=SG.prevCielo.modo;CIELO.h=SG.prevCielo.h;CIELO.txt='';SG.prevCielo=null;try{cielo(0)}catch(e){}}
 if(SG.prevPie)persona.visible=true;SG.prevPie=false;camInit=false;sgRugido(0);SG.cerca=true;SG.W=null;
 const rec=SG.pts>SGD.mejor;if(rec)SGD.mejor=SG.pts;let gana='';const nv0=SGD.nivel,nr=Object.keys(SGD.retos).length;
 if(SGD.nivel<2&&SGD.mejor>=4000&&nr>=2)SGD.nivel=2;if(SGD.nivel===2&&nv0===2&&SGD.mejor>=9000&&nr>=3)SGD.nivel=3;
 if(SGD.nivel>nv0){SGD.olas=SGD.nivel;gana=`⬆️ ¡Nivel ${SGD.nivel}! Desbloqueas olas ${SG_NIV[SGD.nivel].n.toLowerCase()} y la tabla «${SG_TABLAS[SGD.nivel-1].n}»`}
 sgGuardar();SG.res={pts:SG.pts,record:rec&&SG.pts>0,olas:SG.olas,caidas:SG.caidas,maxRide:SG.maxRide,cut:SG.cut,gana};
 if(motivo!=='salir')sgFicha('fin')}
window.surfgSalir=()=>{sgTerminar('salir');SGF.hidden=true;SG.ficha=false};window.surfT={paso:dt=>surfUpdate(dt),a:()=>sgBotonA(),b:()=>sgBotonB(),st:()=>SG,ir:()=>surfIr(),empezar:()=>sgEmpezar(),fin:()=>sgTerminar('menu'),datos:()=>SGD};
// ---- olas: llega una, se coge (o se escapa), se surfea
function sgNuevaOla(primera){const N=SG_NIV[SGD.olas]||SG_NIV[1],sp=SG.sp;
 // la ola rompe hacia el lado con más agua (la playa es curva)
 let dir=Math.random()<.5?1:-1;{const at=s=>{const x=sp.o[0]+sp.t[0]*s*4-sp.n[0]*.6,z=sp.o[1]+sp.t[1]*s*4-sp.n[1]*.6;return sp.cs(x,z)};const a=at(1),b=at(-1);if(Math.abs(a-b)>.12)dir=a<b?1:-1}
 SG.W={wc:-3.7+1.75,H:N.H,va:.34,vw:0,c:0,vc:N.vc,pk:0,rota:false,dir,alfa:0,peel:false,t:0};
 SG.S=Object.assign(SG.S||{},{s:0,h:.5,hv:0,vs:0,inst:0,air:0,cut:0,rem:0,ws:0,yaw:Math.atan2(sp.n[1],-sp.n[0]),rideT:0,tubo:0,topT:0,snapT:0,fallT:0,aireY:0,spin:0,lado:Math.PI/2,popT:0,cutN:0});
 SG.fase='llega';SG.W.wc=-3.7;SG.S.ws=-1.75+(Math.random()-.5)*.1;
 sgMsg(primera?'🌊 Espera la ola':'🌊 ¡Viene otra ola!',primera?'mira al mar: cuando llegue, ¡rema!':'',1.6);sgTip('Espera sentado · cuando se acerque la ola, rema (↑ / Espacio / Remar)')}
function sgMsg(t,s='',d=1.1){const m=SGH.querySelector('.msg');m.innerHTML=t+(s?`<small>${s}</small>`:'');m.classList.remove('on');void m.offsetWidth;m.classList.add('on');SG.msgT=d}
function sgTip(t){SGH.querySelector('.tip').textContent=t}
function sgPuntos(n,txt){const v=Math.round(n*SG.mult);SG.pts+=v;if(txt){sgMsg(txt,'+'+v+(SG.mult>1?' · x'+SG.mult:''),1.1);SG.mult=Math.min(5,SG.mult+1);SG.multT=5}}
function sgReto(id){if(SG.retoHecho[id])return;SG.retoHecho[id]=true;const pr=!SGD.retos[id];SGD.retos[id]=true;sgGuardar();const r=SG_RETOS.find(x=>x.id===id),mon=pr?50:15;
 try{if(typeof taxiMon==='function')taxiMon(mon)}catch(e){}sgMsg('✅ ¡Reto conseguido!',r.n+' · +🪙 '+mon,2);sgDing(4);sgRetosHud()}
function sgRetosHud(){SGH.querySelector('.retos').innerHTML=SG_RETOS.map(r=>{const ok=!!SG.retoHecho[r.id];let p='';if(!ok){if(r.id==='cut3')p=` ${SG.cut}/3`;else if(r.id==='t20')p=` ${Math.min(20,SG.S&&SG.fase==='ola'?SG.S.rideT:SG.maxRide).toFixed(0)}/20 s`;else p=` ${Math.min(5,SGD.racha)}/5`}return `<div class="${ok?'ok':''}">${r.ico} ${r.n}${p}${ok?' ✓':''}</div>`}).join('')}
function sgBotonA(){if(!SG.on)return;const S=SG.S,W=SG.W;if(!S||!W)return;
 if(SG.fase==='llega'){const dd=S.ws-W.wc;if(dd<.75){S.rem=Math.min(1.2,S.rem+.21);sgSnd('remo')}}
 else if(SG.fase==='ola'&&!S.air&&!S.cut&&S.h>.74&&S.vs>W.vc*.7){S.air=.9;S.airD=.9;S.aireH=.045+.025*Math.min(1,S.vs/(W.vc*1.6));S.spin=0;sgSnd('giro');
  const p=SG.sf.g.position;sgSpray(p.x,p.y,p.z,0,.12,0,22,.12)}}
function sgBotonB(){if(!SG.on)return;const S=SG.S,W=SG.W;if(SG.fase!=='ola'||!S||S.air||S.cut)return;const g=S.s-W.c;
 if(g<.25){S.inst=Math.min(1,S.inst+.25);sgMsg('😬 ¡Muy cerca de la espuma!','',.8);return}S.cut=.95;S.cutD=.95;S.vs0=Math.max(S.vs,W.vc*.9);S.h0=S.h;sgSnd('giro');
 const p=SG.sf.g.position,n=SG.sp.n;sgSpray(p.x,p.y+.004,p.z,-n[0]*.05,.1,-n[1]*.05,30,.14)}
function sgCaer(txt){const S=SG.S;SG.fase='caida';S.fallT=0;SG.caidas++;SGD.racha=0;sgGuardar();SG.mult=1;SG.multT=0;sgMsg('🌊 ¡Revolcón!',txt,1.6);sgSnd('caida');sgTip('');
 const p=SG.sf.g.position;sgSpray(p.x,p.y,p.z,0,.16,0,70,.22);sgRetosHud()}
function sgOlaHecha(txt){const S=SG.S;SG.fase='fin';S.fallT=0;SG.olas++;SGD.racha++;sgGuardar();SG.maxRide=Math.max(SG.maxRide,S.rideT);
 sgPuntos(300,txt||'🏄 ¡Ola completada!');if(S.rideT>=20)sgReto('t20');if(SGD.racha>=5)sgReto('seq5');sgRetosHud();sgTip('')}
// ---- cada fotograma del minijuego (sustituye a updateCar)
function surfUpdate(dt){dt=window.__SGPAUSA?0:Math.min(dt,.05);const sp=SG.sp,W=SG.W,S=SG.S,N=SG_NIV[SGD.olas]||SG_NIV[1],n=sp.n,tv=sp.t,o=sp.o,WY=sgWY();SG.tt+=dt;
 if(SG.msgT>0){SG.msgT-=dt;if(SG.msgT<=0)SGH.querySelector('.msg').classList.remove('on')}
 if(SG.multT>0){SG.multT-=dt;if(SG.multT<=0)SG.mult=1}
 SG.t-=dt;const st=Math.max(-1,Math.min(1,(SG.k.r?1:0)-(SG.k.l?1:0)+SG.padX));
 W.alfa=Math.min(1,W.alfa+dt*.8);W.t+=dt;
 const td=[tv[0]*W.dir,tv[1]*W.dir];
 let px,py,pz,pose='sentado',yaw=S.yaw,pitch=0,bank=0,face=null;
 if(SG.fase==='llega'||SG.fase==='pasa'){
  W.wc+=W.va*dt;const dd=S.ws-W.wc;W.H=N.H*Math.min(1,.45+.55*sgSm(-3.7,S.ws-.3,W.wc));
  if(SG.fase==='llega'){
   S.rem=Math.max(0,S.rem-dt*.28+((SG.k.a||SG.padA)&&dd<.75?dt*.75:0));
   const quiere=Math.atan2(-n[1],n[0]);if(dd<.9){let dy=quiere-S.yaw;dy=Math.atan2(Math.sin(dy),Math.cos(dy));S.yaw+=dy*Math.min(1,dt*3)}
   if(dd<.75)sgTip(S.rem>.05?'¡Más! ¡Rema, rema!':'🏊 ¡REMA! (↑ / Espacio / botón Remar varias veces)');
   if(dd<.75&&!S.avisoRema){S.avisoRema=1;sgMsg('🏊 ¡REMA!','',1)}
   if(S.rem>=1&&dd<.28&&dd>-.06){SG.fase='pie';S.popT=0;W.peel=true;W.c=-.12;W.vw=(-.5-S.ws)/N.T;S.s=0;S.h=.55;S.vs=W.vc;S.rideT=0;S.rem=0;S.avisoRema=0;sgSnd('ola');
    S.lado=null;sgMsg('⬆️ ¡De pie!','',.8);sgTip('◀ ▶ sube y baja por la pared · 🌀 giro · 🚀 aéreo en la cresta')}
   else if(dd<-.06){SG.fase='pasa';W.rota=true;S.avisoRema=0;S.rem=0;sgMsg('😅 Se escapó…','¡a por la siguiente!',1.4);S.pasaT=0}}
  else{S.pasaT+=dt;W.alfa=Math.max(0,1-S.pasaT/2.4);if(S.pasaT>2.4){if(SG.t<=0){sgTerminar('fin');return}sgNuevaOla(false)}}
  // flotando: sube y baja con la ola que pasa
  const h=sgAltura(W.H,S.ws-W.wc)*(W.rota?.5:1);px=o[0]+n[0]*S.ws;pz=o[1]+n[1]*S.ws;py=WY+h+.001+Math.sin(SG.tt*1.6)*.001;
  pose=SG.fase==='llega'&&dd<.75?'rema':'sentado';{const e=.03,h2=sgAltura(W.H,S.ws+e-W.wc)*(W.rota?.5:1),fn=Math.cos(yaw)*n[0]-Math.sin(yaw)*n[1];pitch=Math.atan((h2-h)/e*fn)}
  sgRugido(.08+.12*sgSm(1.5,0,Math.abs(dd)))}
 else{
  // la rompiente no avanza siempre igual: a veces cierra una sección rápida
  if(SG.fase==='ola'){W.secT=(W.secT??(6+Math.random()*3))-dt;if(W.secT<=0){W.secT=7+Math.random()*4;W.sec=1.7;sgMsg('⚠️ ¡Sección rápida!','baja para coger velocidad',1.1)}}if(W.sec>0)W.sec-=dt;
  W.c+=W.vc*(W.sec>0?2.1:1)*(1+.15*Math.sin(W.t*.7))*dt;W.wc+=W.vw*dt;W.pk=Math.min(1,W.pk+dt*1.8);
  if(SG.fase==='pie'){S.popT+=dt;if(S.popT>.55)SG.fase='ola'}
  if(SG.fase==='ola'){S.rideT+=dt;
   // arriba / abajo por la pared (el signo depende de dónde queda la cresta en la pantalla)
   const cf=[SG.cam.l.x-SG.cam.p.x,SG.cam.l.z-SG.cam.p.z],ri=[-cf[1],cf[0]],ups=(ri[0]*-n[0]+ri[1]*-n[1])>=0?1:-1;
   if(S.cut>0){S.cut-=dt;const q=1-S.cut/S.cutD;S.vs=S.vs0*(1-1.75*Math.sin(q*Math.PI));S.h=Math.min(1,S.h0+.22*Math.sin(q*Math.PI));S.hv=Math.cos(q*Math.PI)*.4;
    if(S.cut<=0){S.cut=0;SG.cut++;S.cutN++;sgPuntos(250,'🌀 ¡CUTBACK!');if(SG.cut>=3)sgReto('cut3');sgRetosHud()}}
   else if(S.air>0){S.air-=dt;const q=1-S.air/S.airD;S.aireY=4*S.aireH*q*(1-q);S.spin=q*Math.PI*2;S.h=Math.max(S.h,.95);S.inst=Math.min(1.1,S.inst+N.chop*.35*dt+Math.abs(st)*.25*dt);
    if(S.air<=0){S.air=0;S.aireY=0;S.spin=0;S.h=.72;const p=SG.sf.g.position;sgSpray(p.x,p.y,p.z,0,.1,0,40,.18);sgSnd('salpica');
     if(S.inst>.7){sgCaer('aterrizaje fallido');return}S.inst+=.2;sgPuntos(500,'🚀 ¡AÉREO 360!')}}
   else{const hv=st*ups*1.35;S.hv+=(hv-S.hv)*Math.min(1,dt*7);S.h=Math.max(0,Math.min(1.08,S.h+S.hv*dt));
    const vt=W.vc*(.7+.95*(1-S.h));S.vs+=(vt-S.vs)*Math.min(1,dt*1.3)+Math.max(0,-S.hv)*.16*dt}
   const g=S.s-W.c;if(g>1.15)S.vs-=(g-1.15)*.3*dt;S.s+=S.vs*dt;
   // equilibrio
   let pr=N.chop*.22*(.4+Math.abs(Math.sin(SG.tt*2.3+Math.sin(SG.tt*.7)*3)));
   if(S.h>.95&&!S.air)pr+=(S.h-.95)*6;if(S.h<.07)pr+=.5;if(g<0&&g>-.07)pr+=.25;if(S.cut>0)pr+=.1;
   S.inst=Math.max(0,S.inst+pr*dt-(pr<.25?.32*dt:0));
   // snap: tocar la cresta y bajar de golpe
   if(S.h>.92&&!S.air)S.topT=.6;else S.topT=Math.max(0,S.topT-dt);S.snapT=Math.max(0,S.snapT-dt);
   if(S.topT>0&&S.hv<-.9&&S.snapT<=0&&!S.cut&&!S.air){S.snapT=1.4;S.topT=0;sgPuntos(150,'💥 ¡SNAP!');sgSnd('giro');const p=SG.sf.g.position;sgSpray(p.x,p.y+.004,p.z,-n[0]*.06,.12,-n[1]*.06,26,.12)}
   // tubo
   if(g<0&&g>-.07&&S.h>.25&&S.h<.8&&!S.air){if(S.tubo===0)sgMsg('🌀 ¡TUBO!','',1);S.tubo+=dt;SG.pts+=Math.round(60*dt*SG.mult)}else if(S.tubo>0){if(S.tubo>.8&&g>=0)sgPuntos(200+Math.round(S.tubo*150),'🌀 ¡Salida del tubo!');S.tubo=0}
   SG.pts+=10*dt*SG.mult;
   if(S.rideT>=20&&!SG.retoHecho.t20)sgReto('t20');
   if(g<-.07){sgCaer('te pilló la espuma');return}
   if(S.inst>=1){sgCaer(S.h>.95?'te pasaste de la cresta':S.h<.07?'clavaste la punta':'perdiste el equilibrio');return}
   if(g>2.5){sgOlaHecha('🏄 La ola se quedó sin fuerza');return}
   if(S.rideT>=N.T||W.wc>-.52){sgOlaHecha('🏄 ¡Ola completada!');return}
   if(Math.floor(S.rideT*4)!==Math.floor((S.rideT-dt)*4))sgRetosHud()}
  if(SG.fase==='caida'||SG.fase==='fin'){S.fallT+=dt;W.alfa=SG.fase==='fin'?Math.max(.2,1-S.fallT/2):1;if(SG.fase==='fin'){S.h=Math.min(1.25,S.h+dt*.8);S.s+=W.vc*.3*dt}
   if(S.fallT>(SG.fase==='caida'?1.8:1.6)){if(SG.t<=0){sgTerminar('fin');return}sgNuevaOla(false)}}
  // posición en la pared
  const F=sgFila(W,S.s-W.c),sec=sgSeccion(Math.max(F.H,.001),F.k,SGW.sec),hh=Math.min(1,S.h),u=1-hh,d=sec.f0+(sec.Fw-sec.f0)*u*.94+.004,H1=F.H*(1-.35*F.k);
  let y=H1*Math.pow(1-((d-sec.f0)/(sec.Fw-sec.f0)),2);if(S.h>1)y+=(S.h-1)*F.H*.6;const sl=-2*H1*(1-(d-sec.f0)/(sec.Fw-sec.f0))/(sec.Fw-sec.f0);
  const L=(W.c+(S.s-W.c))*W.dir,w=W.wc+d;px=o[0]+tv[0]*L+n[0]*w;pz=o[1]+tv[1]*L+n[1]*w;py=WY+.0025+y+.0012+(S.aireY||0);
  // rumbo: a lo largo de la ola y arriba/abajo
  const fx=S.vs*td[0]-S.hv*sec.Fw*n[0]*.9,fz=S.vs*td[1]-S.hv*sec.Fw*n[1]*.9;yaw=Math.atan2(-fz,fx);
  const hn=(fx*n[0]+fz*n[1])/(Math.hypot(fx,fz)||1);pitch=Math.atan(sl*hn);face={sl,ny:Math.atan(-sl)};
  pose=SG.fase==='pie'?(S.popT<.25?'rema':'pie'):SG.fase==='caida'?'cae':S.air>0?'aire':'pie';
  if(S.lado==null){const fr=[Math.cos(yaw),-Math.sin(yaw)],zr=[-fr[1],fr[0]];S.lado=(zr[0]*-n[0]+zr[1]*-n[1])>0?-Math.PI/2:Math.PI/2}
  // espuma: el labio que rompe y la estela de la tabla
  if(SG.fase!=='caida'){const cL=W.c*W.dir,cw=W.wc+.01;for(let k=0;k<3;k++){const s_=(Math.random()-.6)*.25,x=o[0]+tv[0]*(cL+s_*W.dir)+n[0]*(cw+.03),z=o[1]+tv[1]*(cL+s_*W.dir)+n[1]*(cw+.03);sgSpray(x,WY+W.H*(.75+Math.random()*.3),z,n[0]*.06,.04,n[1]*.06,1,.08)}
   if(SG.fase==='ola'&&!S.air){const sp_=Math.abs(S.hv)*.5+S.vs*.6;if(Math.random()<sp_*dt*60*.5)sgSpray(px-td[0]*.02,py,pz-td[1]*.02,-n[0]*.05*Math.sign(S.hv||1),.07,-n[1]*.05*Math.sign(S.hv||1),1,.06)}}
  sgRugido(.22+.18*W.pk)}
 SG.S.yaw=yaw;
 // la ola y el surfista
 sgOlaUpd();sgPartTick(dt);const sf=SG.sf,G=sf.g;G.position.set(px,py,pz);
 {G.rotation.order='YZX';G.rotation.set(0,yaw+(S.spin||0),pitch);if(face){const sd=Math.sin(yaw)*n[0]+Math.cos(yaw)*n[1];G.rotation.x=-Math.atan(face.sl*sd)+(SG.fase==='ola'?st*.12:0)}}
 if(SG.fase==='caida'){sgPose(sf.p,'cae',S.fallT);sf.tabla.rotation.set(Math.min(1,S.fallT)*2.2,0,S.fallT*4);sf.tabla.position.set(-.02*S.fallT,Math.max(-.004,.04*Math.sin(Math.min(Math.PI,S.fallT*3))),0)}
 else{sf.tabla.rotation.set(0,0,0);sf.tabla.position.set(0,0,0);
  if(pose==='pie'||pose==='aire'){const cr=.85+.5*(1-Math.min(1,S.h))+(S.cut?.3:0);sgPose(sf.p,pose,SG.tt,{lado:S.lado||Math.PI/2,cr,inc:-st*.25,br:Math.sin(SG.tt*2.2)*.15,mira:(S.lado>0?-1:1)*.5})}
  else sgPose(sf.p,pose,SG.tt,{v:pose==='rema'?(SG.k.a||SG.padA||S.rem>.2?11:6):0})}
 // las Cíes al fondo si el día está claro
 if(SG.cies){const Wt=TIEMPO.W;SG.cies.visible=Wt.fog<.35&&Wt.rain<.3&&CIELO.nf<.75;if(SG.cies.visible){SG.cies.material.color.copy(FOG.color).lerp(new THREE.Color(0x8fa4ac),.35).multiplyScalar(1-CIELO.nf*.6);
  // si la cámara no llega tan lejos (móvil), se dibujan más cerca y más pequeñas: se ven igual desde donde estás
  const cp=SG.cam.p,D=Math.hypot(cp.x+76,cp.z-45),k=pcam.far>D+25?1:Math.max(.02,pcam.far*.55/D);SG.cies.scale.setScalar(k);SG.cies.position.set(cp.x*(1-k),cp.y*(1-k),cp.z*(1-k))}}
 // cámara
 {const up=SG.fase==='llega'||SG.fase==='pasa';const tg=new THREE.Vector3(px,py,pz),want=new THREE.Vector3(),lk=new THREE.Vector3();
  if(up){want.set(px+n[0]*.3+td[0]*.04,py+.085,pz+n[1]*.3+td[1]*.04);lk.set(px-n[0]*.9,py+.05,pz-n[1]*.9)}
  else if(SG.fase==='caida'){want.copy(SG.cam.p);lk.copy(tg)}
  else{want.set(px-td[0]*.34+n[0]*.15,py+.12-(S.aireY||0)*.5,pz-td[1]*.34+n[1]*.15);lk.set(px+td[0]*.3-n[0]*.04,py+.015,pz+td[1]*.3-n[1]*.04)}
  want.y=Math.max(want.y,WY+.035);
  if(!SG.cam.ini){SG.cam.p.copy(want);SG.cam.l.copy(lk);SG.cam.ini=true}else{SG.cam.p.lerp(want,Math.min(1,dt*3));SG.cam.l.lerp(lk,Math.min(1,dt*4.5))}
  if(window.__SGCAM){const c=window.__SGCAM;SG.cam.p.set(c[0],c[1],c[2]);SG.cam.l.set(c[3],c[4],c[5])}   // para revisar la ola desde fuera
  pcam.position.copy(SG.cam.p);pcam.lookAt(SG.cam.l);pcam.far=230;pcam.fov=(cv.clientWidth<cv.clientHeight?74:62)+(SG.fase==='ola'?8*Math.min(1,S.vs/(W.vc*1.6)):0);pcam.updateProjectionMatrix()}
 {const Wt=TIEMPO.W;FOG.far=34*(1-.7*Wt.fog)*(1-.3*Wt.rain);FOG.near=7*(1-.85*Wt.fog)}
 // HUD
 const s_=Math.max(0,Math.ceil(SG.t));SGH.querySelector('.pt b').textContent=Math.floor(SG.pts);SGH.querySelector('.mul b').textContent='x'+SG.mult;SGH.querySelector('.tm b').textContent=Math.floor(s_/60)+':'+String(s_%60).padStart(2,'0');
 SGH.querySelector('.ol b').textContent=SG.olas;SGH.querySelector('.bal i').style.width=Math.round(Math.min(1,S.inst)*100)+'%';SGH.querySelector('.bal').style.visibility=SG.fase==='ola'?'visible':'hidden';
 const rm=SGH.querySelector('.rema');rm.hidden=!(SG.fase==='llega'&&S.ws-W.wc<.75);if(!rm.hidden)rm.querySelector('i').style.width=Math.round(Math.min(1,S.rem)*100)+'%';
 const bA=SGH.querySelector('.bA'),bB=SGH.querySelector('.bB');const ride=SG.fase==='ola'||SG.fase==='pie';bA.innerHTML=ride?'<span>🚀</span>Aéreo':'<span>🏊</span>Remar';
 bA.classList.toggle('off',ride?!(S.h>.74&&S.vs>W.vc*.7&&!S.air&&!S.cut):!(SG.fase==='llega'&&S.ws-W.wc<.75));bB.classList.toggle('off',!(SG.fase==='ola'&&!S.air&&!S.cut&&S.s-W.c>=.25));
 if(SG.t<=0&&!SG.finAv&&SG.fase==='ola'){SG.finAv=1;sgMsg('⏱️ ¡Última ola!','',1.2)}if(SG.t>0)SG.finAv=0}
