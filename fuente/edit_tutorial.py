import sys,os
# ================= Tutorial al empezar a jugar (tutorial.js) =================
# La primera vez que entras a jugar en el mundo abierto (al terminar la llegada), sale un recorrido por los botones:
# se ilumina cada uno (controles, bajar/subir, claxon, minimapa, calle, velocímetro, límite, GPS, radio, cámara,
# sonido, fps, pantalla completa, salir…) con una caja que explica para qué sirve, y se avanza con «Siguiente ▶»
# (◀ para volver). «Saltar tutorial» lo cierra y vas directo al juego. Los botones que no están en pantalla (p. ej. el
# joystick en el ordenador o el límite en el helicóptero) se saltan solos. Se guarda en gtvigo_tutorial y no vuelve a
# salir; el botón «❓» de la barra del juego lo abre otra vez. Con ?tutorial=1 sale aunque ya se haya visto.
# Mientras está abierto el coche no se mueve: el teclado solo mueve el tutorial (→/Enter siguiente, ← anterior,
# Esc saltar) y con mando se maneja como los demás menús (cruceta y Ⓐ). Cuenta tutorial/completo o tutorial/saltado
# en GoatCounter. Solo el mundo abierto (index, indexm, webgl y gpu); va al final de todo.
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','webgl.html','gpu.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'tutorial.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '/*tutorial*/' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # el mando lo trata como un menú más (se suelta el coche, cruceta para moverse y Ⓐ para elegir)
    r("function padMenuVis(){for(const id of [/*mandogps*/'gpsMenu',","function padMenuVis(){for(const id of [/*mandogps*//*tutorial*/'tutGT','gpsMenu',")
    # al final de la página (las páginas no llevan </body>): la barra y los botones ya existen
    i=s.rfind('</body>')
    tag='<script>'+JS+'</script>\n'
    s=s[:i]+tag+s[i:] if i>0 else s.rstrip('\n')+'\n'+tag
    open(f,'w',encoding='utf8').write(s);print('ok tutorial',f)
