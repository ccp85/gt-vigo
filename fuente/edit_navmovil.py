import os
f='index.html';s=open(f,encoding='utf8').read()
D=os.path.dirname(os.path.abspath(__file__))
leer=lambda n:open(os.path.join(D,n),encoding='utf8').read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= NAVIDAD MÓVIL (window.LITE) — segunda tanda =================
# 1) Cabecera (navmovil_cabecera.html): codificación y ancho de pantalla de móvil. En GitHub Pages las páginas no la tenían
#    y el móvil las abría como si fuera un ordenador (todo diminuto). También deja añadir el juego a la pantalla de inicio.
if not s.lower().startswith('<!doctype'):s=leer('navmovil_cabecera.html')+s
# 2) Lotes (navmovil_lotes.js): las piezas quietas con el mismo aspecto se dibujan juntas (de ~1.100 a ~350 dibujos por imagen
#    en el centro). Solo actúa con window.LITE, es decir, en navm.html.
r("window.CIRT=()=>CIR;","window.CIRT=()=>CIR;\n"+leer('navmovil_lotes.js'))
# 3) Menú de elegir carroza con el móvil en horizontal: el diseño apilado (carroza arriba, opciones abajo) no cabía en 390 px
#    de alto; en horizontal se usa el de dos columnas, con el panel de opciones desplazable y el botón de jugar siempre a la vista
r("@media (max-width:860px){","@media (max-width:860px) and (orientation:portrait),(max-width:560px){")
# 4) Botones e indicadores en vertical (navmovil.css)
s=s.replace('</style>',leer('navmovil.css')+'</style>',1)
open(f,'w',encoding='utf8').write(s)
print('ok navmovil')
