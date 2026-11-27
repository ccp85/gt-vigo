# Imágenes por segundo según el aparato y modo «gama baja» para móviles antiguos. Toca las siete páginas
# (index, indexm, gp, nav, navm, webgl y gpu); va al final de todo, después de edit_fps30.py y de edit_webgpu.py.
# · Por defecto 60 fps en el ordenador y 30 en el móvil (pantalla táctil de 820 px o menos, o cualquier página LITE).
#   Lo que elija el jugador con «⏱ 30/60 fps» (o la tecla P) sigue guardado en gtvigo_fps y manda sobre lo de por defecto.
# · En el móvil ya se puede elegir 60 de verdad: antes la versión LITE se quedaba siempre en 30 aunque el botón dijera 60.
# · La resolución automática se ajusta a la meta de fps: con el límite de 30 en el ordenador ya no baja la calidad
#   creyendo que el equipo va justo (antes medía 30 fps, lo tomaba por lento y bajaba resolución y distancia).
# · Gama baja (window.GAMA_BAJA, solo cuenta en el móvil LITE): poca memoria (≤3 GB), 4 núcleos o menos (no en iPhone),
#   tarjeta gráfica antigua (Adreno 1xx-5xx, Mali-4xx/T, Mali-G31/G51/G52/G57/G71/G72, PowerVR) o iOS anterior al 15.
#   Ahí empieza en resolución 0,75 (máx. 1, mín. 0,65), con menos distancia de dibujado y menos árboles y gente
#   (QF 0,35, máx. 0,6) y con el primer escalón de la calidad automática ya puesto (más niebla, se ve menos lejos).
#   Con ?gama=baja o ?gama=alta en la dirección se fuerza para probar.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','webgl.html','gpu.html'] if os.path.exists(f)]
GAMA='''<script>/* gama baja: móviles antiguos o con poca memoria (solo se usa en la versión móvil LITE). ?gama=baja / ?gama=alta lo fuerzan */
(()=>{let b=false;const q=/[?&]gama=(baja|alta)/.exec(location.search);
 if(q)b=q[1]==='baja';else try{if(matchMedia('(pointer:coarse)').matches){const n=navigator,ios=/iPhone|iPad|iPod/.test(n.userAgent)||n.platform==='MacIntel'&&n.maxTouchPoints>1;
  if(n.deviceMemory&&n.deviceMemory<=3)b=true;
  if(!ios&&n.hardwareConcurrency&&n.hardwareConcurrency<=4)b=true;
  if(ios){const v=/OS (\\d+)_/.exec(n.userAgent);if(v&&+v[1]<15)b=true}
  if(!b){const c=document.createElement('canvas'),g=c.getContext('webgl');if(g){const e=g.getExtension('WEBGL_debug_renderer_info'),r=String(e?g.getParameter(e.UNMASKED_RENDERER_WEBGL):g.getParameter(g.RENDERER));
   if(/Adreno[^0-9]*[1-5]\\d\\d\\b|Mali-(4\\d|T\\d)|Mali-G(31|51|52|57|71|72)\\b|PowerVR|SGX/i.test(r))b=true;
   const l=g.getExtension('WEBGL_lose_context');if(l)l.loseContext()}}}}catch(e){}
 window.GAMA_BAJA=b})();</script>
<script type="module">'''
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'window.GAMA_BAJA=' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # detección de gama baja antes que nada del juego
    s=s.replace('<script type="module">',GAMA,1)
    # 60 fps por defecto en el ordenador y 30 en el móvil
    r("{let v='30';try{v=localStorage.getItem('gtvigo_fps')||'30'}catch(e){}window.FPSLIM={on:v!=='60',t:0};",
      "{const mov_=!!window.LITE||matchMedia('(pointer:coarse)').matches&&Math.min(screen.width,screen.height)<=820;let v=mov_?'30':'60';try{v=localStorage.getItem('gtvigo_fps')||v}catch(e){}window.FPSLIM={on:v!=='60',t:0,movil:mov_};")
    # en el móvil LITE el tope de 30 depende ya del botón
    r("if(window.LITE){const n_=performance.now();if(n_-(window.__LT||0)<28)return;window.__LT=n_}",
      "if(window.LITE&&FPSLIM.on){const n_=performance.now();if(n_-(window.__LT||0)<28)return;window.__LT=n_}")
    # gama baja: resolución y distancia de partida
    r("R.setPixelRatio(window.LITE?Math.min(1,devicePixelRatio):Math.min(1.5,devicePixelRatio));",
      "R.setPixelRatio(window.LITE?Math.min(window.GAMA_BAJA?.75:1,devicePixelRatio):Math.min(1.5,devicePixelRatio));")
    r("const PRmax=window.LITE?Math.min(1.5,devicePixelRatio):","const PRmax=window.LITE?Math.min(window.GAMA_BAJA?1:1.5,devicePixelRatio):")
    r("let prAct=window.LITE?Math.min(1,PRmax)","let prAct=window.LITE?Math.min(window.GAMA_BAJA?.75:1,PRmax)")
    r("let QF=window.LITE?.5:1;","let QF=window.LITE?(window.GAMA_BAJA?.35:.5):1;")
    r("const PRmin=window.LITE?Math.min(.75,devicePixelRatio)","const PRmin=window.LITE?Math.min(window.GAMA_BAJA?.65:.75,devicePixelRatio)")
    r("QMAX=window.LITE?.8:1;","QMAX=window.LITE?(window.GAMA_BAJA?.6:.8):1,a30=!window.FPSLIM||FPSLIM.on;")
    # la resolución automática mide contra la meta (30 o 60), no siempre contra 60 en el ordenador ni contra 30 en el móvil
    r("if(window.NOADAPT){}else if(window.LITE){if(ft>1/27){","if(window.NOADAPT){}else if(window.LITE){if(ft>(a30?1/27:1/45)){")
    r("else if(ft<1/29){if(prAct<PRmax)","else if(ft<(a30?1/28.5:1/55)){if(prAct<PRmax)")
    r("}else if(ft>1/34){if(prAct>PRmin)","}else if(ft>(a30?1/27:1/34)){if(prAct>PRmin)")
    r("else if(ft<1/52){if(QF<1)","else if(ft<(a30?1/28.5:1/52)){if(QF<1)")
    # gama baja: el primer escalón de la calidad automática (más niebla, se ve menos lejos) ya desde el principio
    r(" setInterval(()=>{const a=performance.now(),fr=R.info.render.frame;if(document.hidden||!driving){NV.t=a;NV.f0=fr;return}",
      " if(window.GAMA_BAJA)try{escalon()}catch(e){}\n setInterval(()=>{const a=performance.now(),fr=R.info.render.frame;if(document.hidden||!driving){NV.t=a;NV.f0=fr;return}")
    open(f,'w',encoding='utf8').write(s);print('ok fpsmovil',f)
