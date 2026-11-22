import sys,os
# ================= Misión del GPS: 🎄 Reparto de Navidad (navmision.js) =================
# El minijuego de Navidad 2026 entra en «🎯 Misiones» del GPS: la línea azul lleva al centro, al llegar se elige personaje
# (solo reparto, sin carrera) y al terminar vuelves al mundo abierto en tu coche, no a la pantalla de inicio. Ver navmision.js.
# Solo el mundo abierto (index.html e indexm.html). Va al final, después de edit_basket.py.
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'navmision.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function navmisTick(' in s:print('ya estaba',f);continue
    assert 'function basketTick(' in s,(f,'falta edit_basket.py')
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # cada botón de misión lleva su id (para el estilo navideño del botón)
    r("for(const m of MISIONES){const act=m.on(),b=document.createElement('button');b.className='mis'+(act?' act':'');","for(const m of MISIONES){const act=m.on(),b=document.createElement('button');b.className='mis'+(act?' act':'');b.dataset.m=m.id;")
    # cada fotograma: marcador y llegada
    r("try{basketTick(dt)}catch(e){if(!window.__bkErr){window.__bkErr=1;console.error(e)}}","try{basketTick(dt)}catch(e){if(!window.__bkErr){window.__bkErr=1;console.error(e)}}try{navmisTick(dt)}catch(e){if(!window.__nvmErr){window.__nvmErr=1;console.error(e)}}")
    # el código, al final del de basket (antes del minimapa)
    r("// ---------- minimapa ----------\n","\n"+JS+"\n// ---------- minimapa ----------\n")
    open(f,'w',encoding='utf8').write(s);print('ok navmision',f)
