import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MENÚS PRINCIPALES: SALA DE EXPOSICIÓN =================
# El vehículo (coche, carroza, helicóptero) ocupa la mayor parte de la pantalla sobre una plataforma giratoria con
# luces; las opciones van en un panel lateral oscuro (abajo en el móvil). Tema navideño (noche, oro y nieve) o de
# carrera (asfalto y neón). Se puede girar el vehículo arrastrando.
r("family=Fraunces:opsz,wght@9..144,700&","family=Fraunces:opsz,wght@9..144,700&family=Russo+One&")
CSS=r"""<style id="menuV2">
:root{--mv-a:#ff5a36;--mv-a2:#ffb03a;--mv-on:#fff;--mv-bg:radial-gradient(ellipse 80% 70% at 32% 45%,#3a2340 0%,#1a1424 45%,#08070d 100%);--mv-glow:255,90,54}
html body #selCar{padding:0;display:block;background:var(--mv-bg);overflow:hidden;color:#fff}
html body #selCar.nav{--mv-a:#ffd24a;--mv-a2:#ff8a3a;--mv-on:#1b1530;--mv-bg:radial-gradient(ellipse 80% 70% at 32% 45%,#2f3a8f 0%,#161a4a 42%,#060716 100%);--mv-glow:255,210,74}
html body #selCar .c{box-sizing:border-box;position:absolute;top:0;right:0;bottom:0;width:min(470px,40vw);max-width:none;margin:0;border-radius:0;padding:26px 28px 18px;overflow-y:auto;overflow-x:hidden;text-align:left;color:#fff;
 background:linear-gradient(180deg,rgba(9,10,26,.55),rgba(9,10,26,.88) 30%,rgba(9,10,26,.94));border-left:1px solid rgba(255,255,255,.09);box-shadow:-30px 0 60px rgba(0,0,0,.35);display:flex;flex-direction:column;gap:2px;z-index:2;scrollbar-width:thin}
html body #selCar h3{font:400 clamp(22px,2.3vw,30px)/1.05 "Russo One","Arial Black",Impact,system-ui,sans-serif;letter-spacing:.01em;color:#fff;margin:0}
html body #selCar .sub{color:rgba(255,255,255,.62);font:500 12.5px/1.4 var(--body);margin:6px 0 14px}
html body #selCar .car{position:fixed;left:0;top:0;bottom:0;right:min(470px,40vw);display:block;z-index:1;
 background:radial-gradient(ellipse 46% 13% at 50% 74%,rgba(var(--mv-glow),.28),transparent 70%),radial-gradient(ellipse 30% 60% at 50% 20%,rgba(255,255,255,.07),transparent 70%)}
html body #selCar #carPrev{position:absolute;inset:0;width:100%;height:100%;border-radius:0;background:none;z-index:2;cursor:grab;touch-action:none}
html body #selCar #carPrev:active{cursor:grabbing}
html body #selCar .car>button{position:absolute;top:50%;transform:translateY(-50%);z-index:4;width:62px;height:62px;border-radius:50%;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.08);color:#fff;font:700 22px var(--body);
 box-shadow:0 8px 30px rgba(0,0,0,.35);transition:background .2s,transform .2s;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
html body #selCar .car>button:hover{background:rgba(var(--mv-glow),.35);transform:translateY(-50%) scale(1.08)}
html body #selCar .car>.prev{left:clamp(14px,3vw,40px)}html body #selCar .car>.next{right:clamp(14px,3vw,40px)}
#selCar .mvBig{position:absolute;left:0;right:0;top:50%;transform:translateY(-62%);text-align:center;z-index:1;pointer-events:none;white-space:nowrap;overflow:hidden;
 font:400 clamp(70px,13vw,230px)/1 "Russo One","Arial Black",Impact,system-ui,sans-serif;letter-spacing:.04em;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.16);background:linear-gradient(180deg,rgba(255,255,255,.15),rgba(255,255,255,0) 80%);-webkit-background-clip:text;background-clip:text}
#selCar .mvMarca{position:absolute;left:clamp(16px,3vw,40px);top:clamp(14px,2.6vw,30px);z-index:3;pointer-events:none;font:400 clamp(20px,2.2vw,30px)/1 "Russo One","Arial Black",Impact,system-ui,sans-serif;letter-spacing:.06em;color:#fff;text-shadow:0 2px 18px rgba(0,0,0,.5)}
#selCar .mvMarca span{color:var(--mv-a)}
#selCar .mvNom{position:absolute;left:0;right:0;bottom:clamp(18px,6vh,64px);z-index:3;text-align:center;pointer-events:none}
#selCar .mvNom b{display:block;font:400 clamp(26px,3.6vw,52px)/1 "Russo One","Arial Black",Impact,system-ui,sans-serif;letter-spacing:.03em;color:#fff;text-shadow:0 4px 30px rgba(var(--mv-glow),.45),0 2px 0 rgba(0,0,0,.3)}
#selCar .mvNom small{display:inline-block;margin-top:10px;font:600 12px var(--body);letter-spacing:.22em;text-transform:uppercase;color:var(--mv-a);padding:5px 12px;border:1px solid rgba(var(--mv-glow),.45);border-radius:999px;background:rgba(0,0,0,.25)}
#selCar .mvNieve{position:absolute;inset:0;z-index:3;pointer-events:none;display:none;
 background-image:radial-gradient(2px 2px at 20px 30px,#fff 50%,transparent 51%),radial-gradient(2.5px 2.5px at 140px 80px,#fff 50%,transparent 51%),radial-gradient(1.5px 1.5px at 90px 150px,#fff 50%,transparent 51%),radial-gradient(2px 2px at 200px 200px,#fff 50%,transparent 51%),radial-gradient(1.5px 1.5px at 60px 230px,#fff 50%,transparent 51%),radial-gradient(3px 3px at 170px 10px,rgba(255,255,255,.8) 50%,transparent 51%);
 background-size:240px 260px;opacity:.55;animation:mvNieve 14s linear infinite}
#selCar.nav .mvNieve{display:block}
@keyframes mvNieve{from{background-position:0 0,0 0,0 0,0 0,0 0,0 0}to{background-position:40px 520px,-30px 520px,20px 520px,-10px 520px,30px 520px,0 520px}}
@media (prefers-reduced-motion:reduce){#selCar .mvNieve{animation:none}}
html body #selCar .nom{display:none}
html body #selCar .cols{justify-content:flex-start;gap:10px;margin:2px 0 16px;flex-wrap:wrap}
html body #selCar .cols button{width:32px;height:32px;border:2px solid rgba(255,255,255,.25);box-shadow:inset 0 -6px 10px rgba(0,0,0,.25),0 2px 8px rgba(0,0,0,.3);transition:transform .15s}
html body #selCar .cols button:hover{transform:scale(1.12)}
html body #selCar .cols button.on{outline:2px solid var(--mv-a);outline-offset:3px;transform:scale(1.12)}
html body #selCar .stats{gap:10px 18px;color:rgba(255,255,255,.7);font:600 11px var(--body);letter-spacing:.06em;text-transform:uppercase;margin:0 0 16px;padding:14px 16px;border-radius:14px;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.07)}
html body #selCar .stats div{flex-direction:column;align-items:flex-start;gap:6px}
html body #selCar .bar5{gap:3px;width:100%}
html body #selCar .bar5 i{flex:1;width:auto;height:6px;border-radius:3px;background:rgba(255,255,255,.12)}
html body #selCar .bar5 i.on{background:linear-gradient(90deg,var(--mv-a2),var(--mv-a));box-shadow:0 0 10px rgba(var(--mv-glow),.45)}
html body #selCar .opt{justify-content:flex-start;flex-wrap:wrap;gap:6px;margin:0 0 10px}
html body #selCar .opt span{width:100%;text-align:left;margin:0 0 1px;font:600 10.5px var(--body);letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.5)}
html body #selCar .opt button{background:rgba(255,255,255,.06);color:#fff;border:1px solid rgba(255,255,255,.13);padding:8px 14px;font:600 13px var(--body);transition:background .15s,border-color .15s}
html body #selCar .opt button:hover{background:rgba(255,255,255,.13)}
html body #selCar .opt button.on{background:var(--mv-a);color:var(--mv-on);border-color:var(--mv-a);box-shadow:0 4px 18px rgba(var(--mv-glow),.35)}
html body #selCar .rec{color:rgba(255,255,255,.72);font:500 12.5px/1.45 var(--body);margin:6px 0 4px}
html body #selCar .acc{position:sticky;bottom:-18px;margin:auto -28px -18px;padding:16px 28px 18px;justify-content:stretch;background:linear-gradient(180deg,rgba(9,10,26,0),rgba(9,10,26,.97) 30%)}
html body #selCar .acc .go{flex:1;padding:17px 22px;font:400 20px/1 "Russo One","Arial Black",Impact,system-ui,sans-serif;letter-spacing:.05em;border-radius:14px;color:#fff;background:linear-gradient(135deg,#ff6a3d,#e0352b 55%,#b51b2a);box-shadow:0 10px 34px rgba(224,53,43,.5),inset 0 1px 0 rgba(255,255,255,.3);animation:mvLate 2.4s ease-in-out infinite}
html body #selCar.nav .acc .go{background:linear-gradient(135deg,#ff4b3a,#c4161f 60%,#8e0f1a);box-shadow:0 10px 34px rgba(196,22,31,.55),0 0 0 2px rgba(255,210,74,.75) inset}
html body #selCar .acc .go:hover{filter:brightness(1.1)}
html body #selCar .acc .volver{background:rgba(255,255,255,.07);color:#fff;border:1px solid rgba(255,255,255,.15);border-radius:14px}
@keyframes mvLate{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}
@media (prefers-reduced-motion:reduce){html body #selCar .acc .go{animation:none}}
html body #selCar .ayuda,html body #selCar #padAyuda{color:rgba(255,255,255,.42);font:500 11px/1.4 var(--body);text-align:center;margin:8px 0 0}
html body #selCar button:focus-visible{outline:2px solid var(--mv-a);outline-offset:2px}
/* móvil y pantallas estrechas: el vehículo arriba a lo grande, las opciones debajo */
@media (max-width:860px){
 html body #selCar .c{left:0;width:auto;top:0;padding:calc(50vh + 6px) 16px 16px;background:linear-gradient(180deg,transparent 0,transparent 49vh,rgba(9,10,26,.9) 52vh,rgba(9,10,26,.96));border-left:none;box-shadow:none}
 html body #selCar .car{right:0;bottom:auto;height:50vh}
 html body #selCar .car>button{width:48px;height:48px;font-size:18px;top:46%}
 #selCar .mvBig{font-size:clamp(60px,22vw,140px)}
 #selCar .mvNom{bottom:10px}#selCar .mvNom b{font-size:clamp(24px,7vw,34px)}#selCar .mvNom small{margin-top:6px;font-size:10.5px}
 html body #selCar .acc{bottom:-16px;margin:auto -16px -16px;padding:14px 16px 16px}
 html body #selCar .ayuda{display:none}
}
/* pantalla de inicio */
html body #selz{background:radial-gradient(ellipse 90% 70% at 50% 35%,#2a2f6a 0%,#14163a 50%,#07081a 100%);gap:16px}
html body #selz h2.gt{font:400 clamp(60px,15vw,132px)/.9 "Russo One","Arial Black",Impact,system-ui,sans-serif;letter-spacing:.06em;color:#fff;text-shadow:0 6px 40px rgba(255,90,54,.35),0 3px 0 rgba(0,0,0,.35)}
html body #selz h2.gt span{color:transparent;background:linear-gradient(180deg,#ffb03a,#ff5a36 60%,#e0352b);-webkit-background-clip:text;background-clip:text;text-shadow:none;filter:drop-shadow(0 6px 24px rgba(255,90,54,.45))}
html body #selz p{color:rgba(255,255,255,.65)}
html body #selzMap{border:1px solid rgba(255,255,255,.14);box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 0 6px rgba(255,255,255,.03)}
html body #selzBtns{gap:12px}
html body #selzBtns button{padding:16px 28px;font:400 18px/1 "Russo One","Arial Black",Impact,system-ui,sans-serif;letter-spacing:.04em;border-radius:14px;transition:transform .15s,filter .15s}
html body #selzBtns button:hover{transform:translateY(-2px);filter:brightness(1.1)}
html body #selzJugar{background:linear-gradient(135deg,#ff6a3d,#e0352b);box-shadow:0 10px 30px rgba(224,53,43,.45)}
html body #selzCarrera{background:rgba(255,255,255,.1);color:#fff;border:1px solid rgba(255,255,255,.2)}
html body #selzNavidad{background:linear-gradient(135deg,#c4161f,#8e0f1a);box-shadow:0 0 0 2px #ffd24a inset,0 10px 30px rgba(196,22,31,.45)}
html body #selzList button{background:rgba(255,255,255,.07);color:#fff;border-color:rgba(255,255,255,.16)}
</style>"""
i=s.rfind('</style>');s=s[:i+8]+'\n'+CSS+s[i+8:]
# --- sala de exposición 3D: plataforma con anillo de luz, sombra de contacto, luces de contorno, arrastrar para girar
r("const base=new THREE.Mesh(new THREE.CylinderGeometry(.11,.11,.006,48),new THREE.MeshStandardMaterial({color:0x3a3b64,roughness:.6}));base.position.y=-.003;sc.add(base);\n const cm=new THREE.PerspectiveCamera(32,cv3.width/cv3.height,.01,10);cm.position.set(.2,.13,.24);cm.lookAt(0,.025,0);",
  r"""const nv=!!RACE.nav,ACC=nv?0xffd24a:0xff5a36;
 const base=new THREE.Mesh(new THREE.CylinderGeometry(.105,.11,.012,72),new THREE.MeshStandardMaterial({color:0x14152c,roughness:.45,metalness:.35}));base.position.y=-.006;sc.add(base);
 const tapa=new THREE.Mesh(new THREE.CircleGeometry(.1,72),new THREE.MeshStandardMaterial({color:0x0e0f22,roughness:.62,metalness:.12}));tapa.rotation.x=-Math.PI/2;tapa.position.y=.0002;sc.add(tapa);
 const aro=new THREE.Mesh(new THREE.TorusGeometry(.107,.0016,8,120),new THREE.MeshBasicMaterial({color:ACC,toneMapped:false}));aro.rotation.x=Math.PI/2;aro.position.y=.0002;sc.add(aro);
 const aro2=new THREE.Mesh(new THREE.RingGeometry(.078,.0792,96),new THREE.MeshBasicMaterial({color:ACC,transparent:true,opacity:.35,toneMapped:false}));aro2.rotation.x=-Math.PI/2;aro2.position.y=.0005;sc.add(aro2);
 {const c=document.createElement('canvas');c.width=c.height=128;const x=c.getContext('2d'),g=x.createRadialGradient(64,64,0,64,64,64);g.addColorStop(0,'rgba(0,0,0,.75)');g.addColorStop(.55,'rgba(0,0,0,.35)');g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(0,0,128,128);
  const sh=new THREE.Mesh(new THREE.PlaneGeometry(.2,.13),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c),transparent:true,depthWrite:false}));sh.rotation.x=-Math.PI/2;sh.position.y=.0008;sc.add(sh);PREVSH=sh}
 for(const[c,x,y,z,k]of[[ACC,-.2,.07,-.3,1.3],[nv?0x7fa8ff:0x46d6ff,.22,.06,-.3,1.1],[0xffffff,0,.3,.05,.6]]){const l=new THREE.DirectionalLight(c,k);l.position.set(x,y,z);sc.add(l)}
 const cm=new THREE.PerspectiveCamera(30,cv3.width/cv3.height,.01,10);const CB=new THREE.Vector3(.15,.078,.172);cm.position.copy(CB);cm.lookAt(0,.024,0);
 {let dr=null;cv3.onpointerdown=e=>{dr=e.clientX;PREVPAUSA=performance.now()+2500;try{cv3.setPointerCapture(e.pointerId)}catch(_){}};cv3.onpointermove=e=>{if(dr==null||!PREV||!PREV.obj)return;PREV.obj.rotation.y+=(e.clientX-dr)*.012;dr=e.clientX;PREVPAUSA=performance.now()+2500};cv3.onpointerup=cv3.onpointercancel=()=>{dr=null}}""")
r("PREV={r,sc,cm,obj:null,raf:0};const loop=()=>{PREV.raf=requestAnimationFrame(loop);if(PREV.obj)PREV.obj.rotation.y+=.012;const w=cv3.clientWidth,h=cv3.clientHeight;if(w&&(cv3.width!==Math.round(w*r.getPixelRatio()))){r.setSize(w,h,false);cm.aspect=w/h;cm.updateProjectionMatrix()}r.render(sc,cm)};loop();previa()}",
  "PREV={r,sc,cm,obj:null,raf:0,aro,aro2};const loop=()=>{PREV.raf=requestAnimationFrame(loop);if(PREV.obj&&performance.now()>PREVPAUSA)PREV.obj.rotation.y+=.006;aro2.rotation.z+=.004;const w=cv3.clientWidth,h=cv3.clientHeight;if(w&&(cv3.width!==Math.round(w*r.getPixelRatio())||cv3.height!==Math.round(h*r.getPixelRatio()))){r.setSize(w,h,false);cm.aspect=w/h;const f=Math.max(1,1.05/cm.aspect);cm.position.copy(CB).multiplyScalar(f);cm.lookAt(0,.024+(cm.aspect<1?-.006:0),0);cm.updateProjectionMatrix()}r.render(sc,cm)};loop();previa()}\nlet PREVPAUSA=0,PREVSH=null;")
r("sc.add(new THREE.HemisphereLight(0xffffff,0x6b6a8a,2.2));","sc.add(new THREE.HemisphereLight(0xffffff,0x6b6a8a,1.6));")
# el vehículo un poco más grande sobre la plataforma
r("const k=.15/Math.max(sz.x,sz.z);g.scale.multiplyScalar(k);g.position.y=0;PREV.sc.add(g);PREV.obj=g;g.rotation.y=-.6}",
  "const k=.17/Math.max(sz.x,sz.z);g.scale.multiplyScalar(k);g.position.y=0;PREV.sc.add(g);PREV.obj=g;g.rotation.y=-.6;mvDeco(spec)}")
# decoración de la sala (marca, rótulo gigante, nombre del vehículo, nieve)
r("function barras(v,a,b){",r"""function mvDeco(spec){const el=document.getElementById('selCar'),car=el.querySelector('.car');if(!car)return;const q=(c,t)=>{let e=car.querySelector('.'+c);if(!e){e=document.createElement(t||'div');e.className=c;car.insertBefore(e,car.firstChild)}return e};
 const nv=!!RACE.nav,carrera=!nv||RACE.sel.modo===1;q('mvBig').textContent=nv?'NAVIDAD':'GT VIGO';q('mvMarca').innerHTML='GT <span>VIGO</span>';q('mvNieve');
 const n=q('mvNom'),nom=el.querySelector('.nom').textContent||spec.nom||'';n.innerHTML='<b></b><small></small>';n.querySelector('b').textContent=nom;n.querySelector('small').textContent=nv?(RACE.sel.veh&&!carrera?'🚁 Helicóptero':carrera?'🏁 Carrera de Navidad':'🛷 Carroza de reparto'):'🏁 Gran Premio';
 if(PREV&&PREV.aro){const c=nv?0xffd24a:0xff5a36;PREV.aro.material.color.setHex(c);PREV.aro2.material.color.setHex(c)}}
function barras(v,a,b){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok menus')
