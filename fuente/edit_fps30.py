# Límite de imágenes por segundo: 30 fps por defecto, con botón «⏱ 30 fps / 60 fps» (y tecla P) para cambiarlo al
# momento sin recargar. Se guarda en el navegador (gtvigo_fps). Con 30 el juego va más estable, gasta menos batería y
# deja margen para meter más detalle; con 60 va tan rápido como dé la pantalla. Las cinco páginas (y gpu.html, que se
# genera a partir de index.html). Va al final de la cadena.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'window.FPSLIM' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # botón junto al de pantalla completa (visible en la maqueta y conduciendo)
    r('<button id="bFull" title="Pantalla completa" aria-label="Pantalla completa">⛶</button>',
      '<button id="bFull" title="Pantalla completa" aria-label="Pantalla completa">⛶</button><button id="bFps" title="Imágenes por segundo: 30 o 60 (tecla P)" aria-label="Imágenes por segundo">⏱ 30 fps</button>')
    r('#bFull{display:inline-block!important}','#bFull{display:inline-block!important}#bFps{display:inline-block!important;font-size:13px}')
    # el bucle de dibujo se salta imágenes hasta llegar a 1/30 s
    r("R.setAnimationLoop(()=>{if(window.LITE){",
      """{let v='30';try{v=localStorage.getItem('gtvigo_fps')||'30'}catch(e){}window.FPSLIM={on:v!=='60',t:0};
 const pinta=()=>{const b=document.getElementById('bFps');if(b){b.textContent='⏱ '+(FPSLIM.on?'30':'60')+' fps';b.setAttribute('aria-pressed',FPSLIM.on)}};
 const cambia=()=>{FPSLIM.on=!FPSLIM.on;try{localStorage.setItem('gtvigo_fps',FPSLIM.on?'30':'60')}catch(e){}pinta();if(typeof mostrar==='function')try{mostrar(FPSLIM.on?'Límite: 30 fps':'Límite: 60 fps (lo que dé la pantalla)')}catch(e){}};
 const b=document.getElementById('bFps');if(b)b.addEventListener('click',e=>{e.stopPropagation();cambia();b.blur()});pinta();
 addEventListener('keydown',e=>{if(e.code==='KeyP'&&!e.repeat&&!/INPUT|TEXTAREA|SELECT/.test((e.target&&e.target.tagName)||''))cambia()})}
R.setAnimationLoop(()=>{if(FPSLIM.on){const n_=performance.now();if(n_-FPSLIM.t<29)return;FPSLIM.t=n_}if(window.LITE){""")
    open(f,'w',encoding='utf8').write(s);print('ok fps30',f)
