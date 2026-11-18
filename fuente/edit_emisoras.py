import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= EMISORAS DE RADIO: botón 📻 abre el panel, eliges emisora y dentro la canción =================
# Mundo abierto: 📻 Radio Vigo (las 3 de siempre) y 🌴 Vigo Reggae. Navidad: 🎄 Radio Navidad y 🌴 Vigo Reggae.
# M / Ⓨ siguen pasando a la siguiente canción de la emisora; N abre el panel; en el mando se maneja con la cruceta y Ⓐ, Ⓑ cierra.
r("// villancicos con arreglo arcade","const VIGO3=CANCIONES.slice(0,3);\n// villancicos con arreglo arcade")
r("function radioAviso(){",r"""const EMISORAS=window.SOLO_NAVIDAD?[{nom:'🎄 Radio Navidad',c:VILLANCICOS},{nom:'🌴 Vigo Reggae',c:REGGAE}]:[{nom:'📻 Radio Vigo',c:VIGO3},{nom:'🌴 Vigo Reggae',c:REGGAE}];
function emisoraPon(e,i,callado){RADIO.e=Math.max(0,Math.min(EMISORAS.length-1,e|0));CANCIONES.length=0;CANCIONES.push(...EMISORAS[RADIO.e].c);RADIO.i=Math.max(0,(i|0)%CANCIONES.length);RADIO.on=true;RADIO.run=false;
 try{localStorage.setItem('gtvigo_emisora',String(RADIO.e))}catch(_){}radioGuarda();if(!callado)radioAviso();radioPanelPinta()}
{let e=0;try{e=+localStorage.getItem('gtvigo_emisora')||0}catch(_){}const on=RADIO.on;emisoraPon(e,RADIO.i,true);RADIO.on=on}
function radioPanelPinta(){const P_=document.getElementById('radioPanel');if(!P_||P_.hidden)return;const E=EMISORAS[RADIO.e];
 P_.querySelector('.em').innerHTML=EMISORAS.map((x,k)=>`<button data-e="${k}" class="${k===RADIO.e?'sel':''}">${x.nom}</button>`).join('');
 P_.querySelector('.ca').innerHTML=E.c.map((x,k)=>`<button data-i="${k}" class="${RADIO.on&&k===RADIO.i?'sel':''}">${RADIO.on&&k===RADIO.i?'🔊':'▶'} ${x.nom}</button>`).join('')+`<button data-off="1" class="${RADIO.on?'':'sel'}">⏻ Apagar la radio</button>`;
 P_.querySelectorAll('.em button').forEach(b=>b.onclick=ev=>{ev.stopPropagation();emisoraPon(+b.dataset.e,0)});
 P_.querySelectorAll('.ca button').forEach(b=>b.onclick=ev=>{ev.stopPropagation();if(b.dataset.off){RADIO.on=false;RADIO.run=false;if(RADIO.g)RADIO.g.gain.setTargetAtTime(0,AC.currentTime,.1);radioGuarda();radioAviso();radioPanelPinta()}else emisoraPon(RADIO.e,+b.dataset.i)});
 const f=P_.querySelector('.ca button.sel')||P_.querySelector('.ca button');if(f&&document.body.classList.contains('pad'))f.focus({preventScroll:true})}
// cartelito de la emisora al cambiar de canción (Ⓨ / M): icono grande, emisora y título
function radioOSD(){let el=document.getElementById('radioOSD');if(!el){el=document.createElement('div');el.id='radioOSD';el.style.cssText='position:fixed;right:14px;top:calc(110px + env(safe-area-inset-top));z-index:80;display:flex;align-items:center;gap:10px;padding:8px 14px 8px 8px;border-radius:16px;background:rgba(18,20,38,.88);color:#fff;font:600 13px system-ui;box-shadow:0 6px 24px rgba(0,0,0,.4);transition:opacity .4s,transform .4s;pointer-events:none';document.body.appendChild(el)}
 const E=EMISORAS[RADIO.e||0],ico=RADIO.on?E.nom.split(' ')[0]:'🔇',nm=E.nom.replace(/^\S+\s/,'');
 el.innerHTML=`<div style="width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:30px;background:${RADIO.on?'linear-gradient(135deg,#2f7bff,#7a4dff)':'#444'}">${ico}</div><div><div style="opacity:.75;font-size:11px">${RADIO.on?nm:'Radio'}</div><div style="font-size:14px">${RADIO.on?'«'+CANCIONES[RADIO.i].nom+'»':'Apagada'}</div></div>`;
 el.style.opacity='1';el.style.transform='translateX(0)';clearTimeout(radioOSD.t);radioOSD.t=setTimeout(()=>{el.style.opacity='0';el.style.transform='translateX(20px)'},3500)}
function radioPanel(abre){const P_=document.getElementById('radioPanel');if(!P_)return;P_.hidden=abre===undefined?!P_.hidden:!abre;radioPanelPinta()}
function radioAviso(){""")
r("mostrar(RADIO.on?(window.SOLO_NAVIDAD?'🎄 Radio Navidad · ':'📻 Radio Vigo · ')","mostrar(RADIO.on?(EMISORAS[RADIO.e||0].nom+' · ')")
r("{const b=document.getElementById('bRadio');if(b){b.onclick=e=>{e.stopPropagation();radioSig()};b.classList.toggle('off',!RADIO.on)}}",
  "{const b=document.getElementById('bRadio');if(b){b.title='Radio: elegir emisora y canción (N) · siguiente canción (M)';b.onclick=e=>{e.stopPropagation();radioPanel()};b.classList.toggle('off',!RADIO.on)}}\naddEventListener('keydown',e=>{if(driving&&!RACE.on&&e.code==='KeyN'&&!e.repeat)radioPanel()});")
r("function radioSig(){","function radioSig(){setTimeout(radioPanelPinta,0);if(RADIO.on&&RADIO.i>=CANCIONES.length-1){emisoraPon(((RADIO.e||0)+1)%EMISORAS.length,0);return}")
r("function radioAviso(){try{","function radioAviso(){radioOSD();try{")
r("function padMenuVis(){for(const id of ['nFin','rFin','selCar','selz']){","function padMenuVis(){for(const id of ['radioPanel','nFin','rFin','selCar','selz']){")
r('<button id="bSaltar"','<div id="radioPanel" hidden style="position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);z-index:70;width:min(360px,92vw);max-height:80vh;overflow:auto;padding:14px;border-radius:18px;background:rgba(18,20,38,.94);color:#fff;font:600 14px system-ui;box-shadow:0 12px 40px rgba(0,0,0,.5)"><style>#radioPanel button{display:block!important;visibility:visible!important;opacity:1!important;position:static!important;width:100%;margin:5px 0;padding:10px 12px;border-radius:12px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.08);color:#fff;font:600 14px system-ui;text-align:left;cursor:pointer}#radioPanel button.sel{background:linear-gradient(90deg,#2f7bff,#7a4dff);border-color:transparent}#radioPanel button:focus{outline:2px solid #ffd24a}#radioPanel .em{display:flex;gap:6px}#radioPanel .em button{text-align:center}#radioPanel h4{margin:2px 0 8px;display:flex;justify-content:space-between;align-items:center;font-size:16px}#radioPanel h4 .menu{width:auto;display:inline-block;margin:0;padding:4px 10px}#radioPanel .t{opacity:.7;font-size:12px;margin:8px 0 2px}</style><h4>📻 Radio <button class="menu" onclick="this.closest(\'#radioPanel\').hidden=true">✕</button></h4><div class="t">Emisora</div><div class="em"></div><div class="t">Canciones</div><div class="ca"></div></div><button id="bSaltar"')
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok emisoras')
