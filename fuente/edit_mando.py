import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------------- mando de Xbox (Gamepad API estándar)
s=s.replace('</style>','body.pad button:focus,body.pad input:focus{outline:3px solid #ffd34d!important;outline-offset:2px}#padAyuda{display:none;margin:6px 0 0;font-size:12px;color:var(--ink2)}body.pad #padAyuda{display:block}\n</style>',1)
r('function golpe(){','function golpe(){padVibra(.7,.35,160);')
r('function sonTurbo(){','function sonTurbo(){padVibra(.5,.8,350);')
r('function sonCaja(){','function sonCaja(){padVibra(.2,.6,180);')
r("'⤒ / Q para despegar'","(document.body.classList.contains('pad')?'RB / ⤒ para despegar':'⤒ / Q para despegar')")
r("const camOff=new THREE.Vector3();",r"""// ---------- mando de Xbox: RT acelera · LT frena/marcha atrás · stick izq. dirige · A acción/turbo · X cámara · B reaparecer · RB/LB subir/bajar (helicóptero) · Menú = salir
var PAD={i:null,prev:[],act:false,md:0,mt:0};
function padVibra(w,st,ms){try{if(PAD.i==null)return;const g=navigator.getGamepads()[PAD.i];const v=g&&g.vibrationActuator;if(v&&v.playEffect)v.playEffect('dual-rumble',{duration:ms,weakMagnitude:w,strongMagnitude:st}).catch(()=>{})}catch(_){}}
const padK=code=>{for(const t of ['keydown','keyup'])dispatchEvent(new KeyboardEvent(t,{code,key:code==='Enter'?'Enter':code==='Escape'?'Escape':code,bubbles:true,cancelable:true}))};
const padAviso=t=>{try{if(RACE.on)aviso(t,1.8,'peq');else mostrar(t)}catch(_){}};
function padSuelta(){if(!PAD.act)return;PAD.act=false;keys.up=keys.down=keys.left=keys.right=keys.alt_up=keys.alt_dn=false;JOY.act=false;JOY.k=1}
function padConecta(g){if(PAD.i!=null)return;PAD.i=g.index;PAD.prev=g.buttons.map(b=>b.pressed);document.body.classList.add('pad');padAviso('🎮 Mando conectado · RT acelera · LT frena · Ⓐ acción · Ⓧ cámara');padVibra(.4,.4,120)}
addEventListener('gamepadconnected',e=>padConecta(e.gamepad));
addEventListener('gamepaddisconnected',e=>{if(e.gamepad.index===PAD.i){PAD.i=null;padSuelta();document.body.classList.remove('pad');padAviso('🎮 Mando desconectado')}});
function padMenuVis(){for(const id of ['nFin','rFin','selCar','selz']){const el=document.getElementById(id);if(el&&!el.hidden&&el.getClientRects().length)return el}return null}
function padTick(){requestAnimationFrame(padTick);let gs;try{gs=navigator.getGamepads?navigator.getGamepads():[]}catch(_){return}
 if(PAD.i==null){for(const g of gs)if(g&&g.connected&&g.buttons.some(b=>b.pressed)){padConecta(g);break}return}
 const g=gs[PAD.i];if(!g||!g.connected){padSuelta();return}
 const b=g.buttons,ax=g.axes,pr=PAD.prev,P_=k=>!!(b[k]&&b[k].pressed),dn=k=>P_(k)&&!pr[k];PAD.prev=b.map(x=>x.pressed);
 const dz=v=>Math.abs(v||0)<.18?0:v,lx=dz(ax[0]),ly=dz(ax[1]),ry=dz(ax[3]);
 const ov=padMenuVis();
 if(ov||!driving){padSuelta();if(!ov){if(dn(0)){const bc=document.getElementById('bCoche');if(bc&&bc.getClientRects().length)bc.click()}return}
  // menús: cruceta o stick para moverse, A para elegir
  const bs=[...ov.querySelectorAll('button,input')].filter(x=>!x.disabled&&x.getClientRects().length&&getComputedStyle(x).visibility!=='hidden');
  let d=0;const sd=ly<-.6?-1:ly>.6?1:lx<-.6?-2:lx>.6?2:0,now=performance.now();if(sd&&(sd!==PAD.md||now-PAD.mt>380)){d=sd;PAD.mt=now}PAD.md=sd;
  if(dn(12))d=-1;if(dn(13))d=1;if(dn(14))d=-2;if(dn(15))d=2;
  if(Math.abs(d)===2&&ov.id==='selCar'){padK(d<0?'ArrowLeft':'ArrowRight');d=0}else if(d)d=Math.sign(d);
  if(d&&bs.length){let i=bs.indexOf(document.activeElement);i=i<0?(d>0?0:bs.length-1):(i+d+bs.length)%bs.length;bs[i].focus({preventScroll:false})}
  if(dn(0)){const a=document.activeElement;if(a&&bs.includes(a)&&a.tagName==='BUTTON')a.click();else if(ov.id==='selCar')padK('Enter');else{const x=bs.find(x=>x.tagName==='BUTTON');x&&x.click()}}
  if(dn(1)&&ov.id!=='selCar'){const m=ov.querySelector('.menu');m&&m.click()}
  return}
 // conducción
 const val=k=>b[k]?(b[k].value||(b[k].pressed?1:0)):0,rt=val(7),lt=val(6),heli=MODO==='heli';
 const dl=P_(14),dr=P_(15);
 const up=rt>.15||ly<-.55||P_(12),down=lt>.15||ly>.55||P_(13),L=lx<0||dl,R_=lx>0||dr;
 const aU=heli&&(P_(5)||ry<-.5),aD=heli&&(P_(4)||ry>.5);
 if(up||down||L||R_||aU||aD){PAD.act=true;keys.up=up;keys.down=down;keys.left=L;keys.right=R_;keys.alt_up=aU;keys.alt_dn=aD;
  if(dl||dr){JOY.act=false;JOY.k=1}else{JOY.act=true;JOY.k=Math.min(1,Math.max(.3,(Math.abs(lx)-.18)/.62))}}else padSuelta();
 if(dn(0))padK('KeyE');if(dn(1))padK('KeyR');if(dn(2))padK('KeyC');if(dn(3))padK('KeyM');if(dn(8))padK('KeyG');if(dn(9))padK('Escape');
 if(dn(5)&&!heli&&RACE.on)usarTurbo()}
requestAnimationFrame(padTick);
const camOff=new THREE.Vector3();""")
r('<button class="go">🏁 ¡A correr!</button></div>','<button class="go">🏁 ¡A correr!</button></div><p id="padAyuda">🎮 Cruceta ◀ ▶ cambia · Ⓐ elegir · RT acelera · LT frena</p>')
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok mando')
