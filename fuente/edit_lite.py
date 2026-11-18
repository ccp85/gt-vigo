import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= VERSIÓN MÓVIL (window.LITE) =================
# Gráficos simples para que vaya fluido en el móvil: sin sombras, sin antialias ni buffer de profundidad logarítmico,
# sin posprocesado, resolución interna más baja, menos distancia de dibujado y menos tráfico y gente.
# La versión de PC sube la resolución hasta 2x en ordenador (la resolución adaptativa la baja si hace falta).
r("const R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,logarithmicDepthBuffer:true});",
  "const R=new THREE.WebGLRenderer({canvas:cv,antialias:!window.LITE,alpha:true,logarithmicDepthBuffer:!window.LITE,powerPreference:'high-performance'});")
r("R.setPixelRatio(Math.min(1.5,devicePixelRatio));R.shadowMap.enabled=true;",
  "R.setPixelRatio(window.LITE?Math.min(1,devicePixelRatio):Math.min(1.5,devicePixelRatio));R.shadowMap.enabled=!window.LITE;")
r("sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);","sun.castShadow=!window.LITE;sun.shadow.mapSize.set(2048,2048);")
r("const PRmax=Math.min(1.5,devicePixelRatio);let prAct=PRmax,",
  "const PRmax=window.LITE?Math.min(1.1,devicePixelRatio):matchMedia('(pointer:coarse)').matches?Math.min(1.5,devicePixelRatio):Math.min(2,devicePixelRatio);let prAct=window.LITE?Math.min(1,PRmax):Math.min(1.5,PRmax),")
r("let QF=1;window.QF=()=>QF;","let QF=window.LITE?.5:1;window.QF=()=>QF;")
r("const PRmin=matchMedia('(pointer:coarse)').matches?.6:.7;","const PRmin=window.LITE?Math.min(.9,devicePixelRatio):matchMedia('(pointer:coarse)').matches?.6:.7,QMAX=window.LITE?.8:1;")
r("if(ft>1/34){if(prAct>PRmin)nv=Math.max(PRmin,prAct-.2);else QF=Math.max(.5,QF-.15)}else if(ft<1/52){if(QF<1)QF=Math.min(1,QF+.1);else if(prAct<PRmax)nv=Math.min(PRmax,prAct+.2)}",
  "if(window.LITE){if(ft>1/27){if(QF>.35)QF=Math.max(.35,QF-.1);else if(prAct>PRmin)nv=Math.max(PRmin,prAct-.125)}else if(ft<1/31){if(prAct<PRmax)nv=Math.min(PRmax,prAct+.125);else if(QF<QMAX)QF=Math.min(QMAX,QF+.05)}}else if(ft>1/34){if(prAct>PRmin)nv=Math.max(PRmin,prAct-.2);else QF=Math.max(.5,QF-.15)}else if(ft<1/52){if(QF<1)QF=Math.min(1,QF+.1);else if(prAct<PRmax)nv=Math.min(PRmax,prAct+.2)}")
r("try{const v=localStorage.getItem('gtvigo_post');if(v!==null)POST.on=v==='1'}catch(e){}","try{const v=localStorage.getItem('gtvigo_post');if(v!==null)POST.on=v==='1'}catch(e){}if(window.LITE)POST.on=false;")
r(".matches?40:56;for(let k=0;k<NT;k++)",".matches?(window.LITE?7:40):(window.LITE?8:56);for(let k=0;k<NT;k++)")
r("const N=matchMedia('(pointer:coarse)').matches?60:96;","const N=window.LITE?14:matchMedia('(pointer:coarse)').matches?60:96;")
# luces puntuales de las misiones: se apagan del todo (fuera de la escena) al acabar; si se quedan, cada píxel de la
# ciudad las sigue calculando y el juego va más lento el resto de la partida (en el móvil se nota mucho)
r("if(!LUZ.pl){LUZ.pl=[];for(let k=0;k<4;k++){const l=new THREE.PointLight(0xffd690,0,1.6,1.4);l.position.set(0,-50,0);scene.add(l);LUZ.pl.push(l)}}}",
  "if(!LUZ.pl){LUZ.pl=[];for(let k=0;k<4;k++){const l=new THREE.PointLight(0xffd690,0,1.6,1.4);l.position.set(0,-50,0);scene.add(l);LUZ.pl.push(l)}}for(const l of LUZ.pl)l.visible=true}")
r("if(LUZ.pl)for(const l of LUZ.pl){l.intensity=0;l.position.y=-50}}}","if(LUZ.pl)for(const l of LUZ.pl){l.intensity=0;l.position.y=-50;l.visible=false}}}")
r("for(const l of CASM.luces)scene.add(l)}","for(const l of CASM.luces)scene.add(l)}for(const l of CASM.luces)l.visible=true;")
r("function casaSale(ok){const C=CASM;if(C.luces)for(const l of C.luces)l.intensity=0;","function casaSale(ok){const C=CASM;if(C.luces)for(const l of C.luces){l.intensity=0;l.visible=false}")
# móvil: 30 imágenes por segundo estables (menos calor y menos tirones que ir saltando entre 40 y 60) y sin los montes lejanos
r("R.setAnimationLoop(()=>{let dt=Math.min(.25,clock.getDelta());","R.setAnimationLoop(()=>{if(window.LITE){const n_=performance.now();if(n_-(window.__LT||0)<28)return;window.__LT=n_}let dt=Math.min(.25,clock.getDelta());")
r("pcam.far=FONDO.m&&MODO!=='heli'?260:FOG.far+4","pcam.far=FONDO.m&&MODO!=='heli'&&!window.LITE?260:FOG.far+4")
open(f,'w').write(s)
def var(tit,scr,out,ref=None):
    g=open(ref or out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
var('GT Vigo · Navidad Móvil','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;window.LITE=1;document.body.classList.add("solo","lite")</script>','navm.html','nav.html')
print('ok lite')
