# Selector de calidad gráfica «🎨» en el mundo abierto y menos zonas cargadas en móviles de gama baja.
# Va al final de todo (después de edit_fpsmovil.py y edit_sinvaiven.py). Toca las siete páginas, pero el botón y los saltos
# entre versiones solo funcionan en las del mundo abierto (index.html, indexm.html y webgl.html).
# · 🎨 Calidad (se guarda en gtvigo_calidad; cambiarla recarga el juego):
#     Auto    → como hasta ahora: el ordenador va a index.html (WebGPU) y el móvil a indexm.html, que detecta la gama baja.
#     Baja    → indexm.html con el modo gama baja siempre puesto (resolución 0,75, menos distancia, árboles, gente y zonas).
#     Media   → indexm.html sin modo gama baja (la versión móvil de siempre).
#     Alta    → webgl.html: gráficos completos con el motor clásico (sombras, más distancia…).
#     Máxima  → index.html: motor WebGPU con todos los efectos (hierba, árboles con viento, reflejos, posprocesado…).
#               Si el navegador no tiene WebGPU, se queda en Alta.
#   Al abrir cualquiera de las tres páginas se salta sola a la que toca. Para no entrar en bucle, como mucho 2 saltos cada
#   15 s. ?gama=baja / ?gama=alta en la dirección siguen mandando para probar.
# · Gama baja (solo móvil LITE): conduciendo carga las zonas a menos de ~4 u (unos 250 m) en vez de 9 (~575 m), las
#   suelta a ~8 u (~500 m) y al empezar carga solo la zona de salida (antes también las que tuviera a menos de 6 u: desde la
#   Praza de España, el Puerto y el Areal). En la maqueta, radio 10 como mucho en vez de 16.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','webgl.html','gpu.html'] if os.path.exists(f)]
MUNDO={'index.html','indexm.html','webgl.html'}
GAMA_OLD="(()=>{let b=false;const q=/[?&]gama=(baja|alta)/.exec(location.search);\n if(q)b=q[1]==='baja';else try{"
GAMA_NEW=("(()=>{let b=false;const q=/[?&]gama=(baja|alta)/.exec(location.search);let cal='auto';try{cal=localStorage.getItem('gtvigo_calidad')||'auto'}catch(e){}\n"
 " if(!/^(auto|baja|media|alta|maxima)$/.test(cal))cal='auto';window.CALIDAD=cal;   // 🎨 calidad elegida (edit_calidad.py)\n"
 " if(q)b=q[1]==='baja';else if(cal==='baja')b=true;else if(cal!=='auto')b=false;else try{")
FIN_OLD="window.GAMA_BAJA=b})();</script>"
ROUTER=r"""window.GAMA_BAJA=b})();
/* 🎨 calidad: salta a la versión del mundo abierto que toca (como mucho 2 saltos cada 15 s, para no entrar en bucle) */
(()=>{const cal=window.CALIDAD;if(!cal||cal==='auto')return;const pg=location.pathname.split('/').pop()||'index.html';if(!/^(index|indexm|webgl)\.html$/.test(pg))return;
 const dest=(cal==='baja'||cal==='media')?'indexm.html':cal==='alta'?'webgl.html':(navigator.gpu?'index.html':'webgl.html');if(dest===pg)return;
 if(cal==='maxima'&&pg==='webgl.html'&&/\/(index\.html)?$/.test((document.referrer||'').split(/[?#]/)[0]))return;   // index.html saltó aquí porque no arrancó WebGPU
 try{const n=JSON.parse(sessionStorage.getItem('gtvigo_saltos')||'[]').filter(t=>Date.now()-t<15000);if(n.length>=2)return;n.push(Date.now());sessionStorage.setItem('gtvigo_saltos',JSON.stringify(n))}catch(e){}
 let q=location.search.replace(/([?&])pc=1(&|$)/,'$1').replace(/[?&]+$/,'');if(dest!=='indexm.html')q+=(q?'&':'?')+'pc=1';
 window.__SALTO=1;location.replace(dest+q+location.hash)})();
/* 🎨 botón y menú de calidad */
addEventListener('DOMContentLoaded',()=>{const b=document.getElementById('bCal');if(!b)return;
 const OP=[['auto','Auto','El juego elige según tu aparato'],['baja','Baja','Móviles antiguos: menos resolución, distancia y zonas'],['media','Media','Versión móvil normal'],['alta','Alta','Gráficos completos (motor clásico)'],['maxima','Máxima','WebGPU: hierba, árboles con viento, reflejos… (necesita un equipo potente)']];
 const nom=c=>(OP.find(o=>o[0]===c)||OP[0])[1];b.textContent='🎨 '+nom(window.CALIDAD);
 const cierra=()=>{const m=document.getElementById('calMenu');if(m)m.remove()};
 b.addEventListener('click',e=>{e.stopPropagation();b.blur();if(document.getElementById('calMenu')){cierra();return}
  const m=document.createElement('div');m.id='calMenu';m.setAttribute('role','dialog');m.setAttribute('aria-label','Calidad gráfica');
  m.innerHTML='<b>🎨 Calidad gráfica</b>'+OP.map(o=>'<button data-c="'+o[0]+'"'+(o[0]===window.CALIDAD?' class="on" aria-pressed="true"':'')+'><span>'+o[1]+'</span><small>'+o[2]+'</small></button>').join('')+'<i>Al cambiarla se recarga el juego</i>';
  m.addEventListener('click',ev=>{ev.stopPropagation();const c=ev.target.closest('[data-c]');if(!c)return;const v=c.dataset.c;if(v===window.CALIDAD){cierra();return}
   try{localStorage.setItem('gtvigo_calidad',v);sessionStorage.removeItem('gtvigo_saltos')}catch(e){}
   const pg=location.pathname.split('/').pop()||'index.html';const q=location.search.replace(/([?&])(gama=\w+|pc=1)(?=&|$)/g,'$1').replace(/[?&]{2,}/g,'&').replace(/[?&]+$/,'').replace(/^&/,'?');
   location.replace((v==='auto'?'index.html':pg)+q+location.hash)});
  document.body.appendChild(m)});
 addEventListener('click',e=>{const m=document.getElementById('calMenu');if(m&&!m.contains(e.target))cierra()});
 addEventListener('keydown',e=>{if(e.key==='Escape')cierra()})});
</script>"""
CSS=("#bFps{display:inline-block!important;font-size:13px}#bCal{display:inline-block!important;font-size:13px}"
 "#calMenu{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);z-index:10000;width:min(340px,calc(100vw - 24px));max-height:calc(100vh - 24px);overflow:auto;box-sizing:border-box;"
 "background:rgba(20,20,40,.96);color:#fff;border-radius:16px;padding:14px;box-shadow:0 10px 40px rgba(0,0,0,.5);font:14px system-ui,sans-serif;display:flex;flex-direction:column;gap:6px}"
 "#calMenu>b{font-size:16px;margin-bottom:4px}#calMenu>i{opacity:.6;font-size:12px;margin-top:4px;font-style:normal}"
 "#calMenu button{display:flex;flex-direction:column;align-items:flex-start;gap:2px;text-align:left;background:rgba(255,255,255,.08);color:#fff;border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:9px 12px;cursor:pointer;font:inherit}"
 "#calMenu button span{font-weight:700}#calMenu button small{opacity:.75;font-size:12px}"
 "#calMenu button.on{background:#ff6a3d;border-color:#ff6a3d}")
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'edit_calidad.py' in s:print('ya estaba',f);continue
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r(GAMA_OLD,GAMA_NEW)
    r(FIN_OLD,ROUTER)
    # el salto automático del ordenador a la versión móvil no debe pisar el de la calidad
    if "(()=>{if(window.LITE||window.SOLO_CARRERA||/[?&]pc=1/.test(location.search))return;" in s:
        r("(()=>{if(window.LITE||window.SOLO_CARRERA||/[?&]pc=1/.test(location.search))return;","(()=>{if(window.__SALTO||window.LITE||window.SOLO_CARRERA||/[?&]pc=1/.test(location.search))return;")
    if f in MUNDO:
        r('<button id="bFps" title="Imágenes por segundo: 30 o 60 (tecla P)" aria-label="Imágenes por segundo">⏱ 30 fps</button>',
          '<button id="bFps" title="Imágenes por segundo: 30 o 60 (tecla P)" aria-label="Imágenes por segundo">⏱ 30 fps</button><button id="bCal" title="Calidad gráfica" aria-label="Calidad gráfica">🎨 Auto</button>')
        r('#bFps{display:inline-block!important;font-size:13px}',CSS)
    # gama baja: menos zonas a la vez
    if "const cerca=driving?(MODO==='heli'?(QF>.8?11:8):9):Math.min(window.LITE?16:30,6+14/Math.max(.5,cam.zoom));" in s:
        r("const cerca=driving?(MODO==='heli'?(QF>.8?11:8):9):Math.min(window.LITE?16:30,6+14/Math.max(.5,cam.zoom));",
          "const GB_=!!(window.LITE&&window.GAMA_BAJA),cerca=driving?(MODO==='heli'?(GB_?6:QF>.8?11:8):(GB_?4:9)):Math.min(window.LITE?(GB_?10:16):30,6+14/Math.max(.5,cam.zoom));   // gama baja: ~250 m (edit_calidad.py)")
        r("const lejos=cerca+(window.LITE?5:matchMedia('(pointer:coarse)').matches?8:16);","const lejos=cerca+(GB_?4:window.LITE?5:matchMedia('(pointer:coarse)').matches?8:16);")
        r("const sig=ds.find(([id,d])=>d<cerca+7&&!ZEST[id]&&!PRE[id]);","const sig=ds.find(([id,d])=>d<cerca+(GB_?3:7)&&!ZEST[id]&&!PRE[id]);")
        r("for(const [id,d] of ds)if(d<6)pedirZona(id)}","for(const [id,d] of ds)if(d<(window.LITE&&window.GAMA_BAJA?3:6))pedirZona(id)}")
    open(f,'w',encoding='utf8').write(s);print('ok calidad',f)
