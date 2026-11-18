import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------------- pantalla completa: botón ⛶ y entrada automática al empezar a jugar
s=s.replace('</style>','body.drive .bar #bFull{display:inline-block!important}#bFull{font-size:17px;line-height:1;padding-left:12px;padding-right:12px}\n</style>',1)
r('<button id="bSnd" aria-pressed="false" aria-label="Sonido">🔈 Sonido</button>','<button id="bSnd" aria-pressed="false" aria-label="Sonido">🔈 Sonido</button>\n  <button id="bFull" title="Pantalla completa" aria-label="Pantalla completa">⛶</button>')
r("const camOff=new THREE.Vector3();",r"""// ---------- pantalla completa
var FS={pref:true};
const fsOn=()=>!!(document.fullscreenElement||document.webkitFullscreenElement);
function fsPon(on,avisa){const el=document.documentElement;try{
 if(on&&!fsOn()){const fn=el.requestFullscreen||el.webkitRequestFullscreen;const ok=fn&&(document.fullscreenEnabled||document.webkitFullscreenEnabled);
  if(!ok){if(avisa)mostrar('⛶ Para verlo a pantalla completa, abre el juego en su propia pestaña del navegador');return}
  const p=fn.call(el,{navigationUI:'hide'});if(p&&p.catch)p.catch(()=>{if(avisa)mostrar('⛶ Para verlo a pantalla completa, abre el juego en su propia pestaña del navegador')})}
 else if(!on&&fsOn())(document.exitFullscreen||document.webkitExitFullscreen).call(document)}catch(_){}}
{const bF=document.getElementById('bFull');bF.onclick=()=>{const on=!fsOn();FS.pref=on;fsPon(on,true)};
 const upd=()=>{const on=fsOn();bF.setAttribute('aria-pressed',on);bF.title=on?'Salir de pantalla completa':'Pantalla completa';bF.textContent=on?'🗗':'⛶';setTimeout(()=>dispatchEvent(new Event('resize')),60)};
 document.addEventListener('fullscreenchange',upd);document.addEventListener('webkitfullscreenchange',upd);
 const auto=()=>{if(FS.pref)fsPon(true,false)};
 for(const q of ['#selzJugar','#selzCarrera','#selzNavidad','#selCar .go','#bCoche','#bMotoC','#bMoto','#bHeli','#rFin .otra','#nFin .otra']){const e=document.querySelector(q);e&&e.addEventListener('click',auto)}}
const camOff=new THREE.Vector3();""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok full')
