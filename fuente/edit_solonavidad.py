import sys,os
# ================= GT VIGO · EDICIÓN NAVIDEÑA: enlace propio solo para el juego de Navidad =================
# nav.html y navm.html pasan a ser «GT Vigo · Edición Navideña»:
#  - portada a pantalla completa con la ilustración (portada_navidad.jpg) y «GT VIGO · EDICIÓN NAVIDEÑA» en grande
#    mientras carga la página y otra vez al pulsar «¡A repartir!», hasta que empieza el reparto;
#  - fuera la maqueta de Vigo de fondo, el cartel de «Preparando el circuito», el título y las ayudas de la maqueta;
#  - en la elección de personaje no sale «Modo» (sin carrera): siempre reparto (carroza o helicóptero).
# Desde el juego completo en el móvil (botón «🎄 Navidad 2026» → navm.html?desde=gt) todo sigue como antes, con carrera.
# Va al final de build.sh (después de edit_radiosuno.py) y usa solonavidad.html.
AQUI=os.path.dirname(os.path.abspath(__file__))
SNIP=open(os.path.join(AQUI,'solonavidad.html'),encoding='utf-8').read()
for f in (sys.argv[1:] or [x for x in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(x)]):
    s=open(f,encoding='utf-8').read()
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # el salto al reparto móvil desde el juego completo lleva ?desde=gt (así conserva la carrera)
    r("location.replace('navm.html'+location.search+location.hash)",
      "location.replace('navm.html'+(window.SOLO_NAVIDAD?location.search:'?desde=gt')+location.hash)")
    if 'window.SOLO_NAVIDAD=1' in s.split('<canvas id="c"')[0] or os.path.basename(f) in ('nav.html','navm.html'):
        i=s.index('window.SOLO_NAVIDAD=1');i=s.index('</script>',i)+len('</script>')
        s=s[:i]+'\n'+SNIP+s[i:]
        r("el.querySelector('h3').textContent=RACE.nav?'🎄 Reparto de Navidad · Vigo 2026'",
          "el.querySelector('h3').textContent=RACE.nav?(document.body.classList.contains('edn')?'🎄 GT Vigo · Edición Navideña':'🎄 Reparto de Navidad · Vigo 2026')")
    open(f,'w',encoding='utf-8').write(s)
