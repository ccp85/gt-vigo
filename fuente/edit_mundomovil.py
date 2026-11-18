import os,re
f='index.html';s=open(f,encoding='utf8').read()
D=os.path.dirname(os.path.abspath(__file__))
leer=lambda n:open(os.path.join(D,n),encoding='utf8').read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MUNDO ABIERTO MÓVIL (indexm.html, window.LITE sin SOLO_*) =================
# Se aplica al final de la cadena, solo sobre index.html (nav, navm y gp no cambian). Todo lo nuevo va con window.LITE,
# así index.html en el ordenador se queda igual; indexm.html es index.html con window.LITE=1.
# 1) Maqueta en el móvil (mundomovil.js): árboles y farolas de cada zona juntados, menos alejamiento
r("window.CIRT=()=>CIR;","window.CIRT=()=>CIR;\n"+leer('mundomovil.js'))
# 1b) zonas cargadas a la vez en el móvil: en la maqueta como mucho 16 de radio (antes 30) y se sueltan antes las lejanas
r("Math.min(30,6+14/Math.max(.5,cam.zoom))","Math.min(window.LITE?16:30,6+14/Math.max(.5,cam.zoom))")
r("const lejos=cerca+(matchMedia('(pointer:coarse)').matches?8:16);","const lejos=cerca+(window.LITE?5:matchMedia('(pointer:coarse)').matches?8:16);")
# 2) En el móvil, index.html salta solo a indexm.html (con ?pc=1 se queda en la de gráficos completos)
# (va justo antes del módulo del juego; edit_inicio.py añade antes otro módulo, el del menú)
r('<script type="module">\nconst ZONA=',leer('mundomovil_salto.html')+'<script type="module">\nconst ZONA=')
# 3) Botones y paneles del mundo abierto en el móvil (mundomovil.css)
s=s.replace('</style>',leer('mundomovil.css')+'</style>',1)
open(f,'w',encoding='utf8').write(s)
# 4) indexm.html: el mismo juego con window.LITE=1 (antes de que arranque el código del juego)
L=s.split('\n');i=[k for k,l in enumerate(L) if l.startswith('<script>addEventListener("error"')]
assert len(i)==1,i
L.insert(i[0],'<script>window.LITE=1;window.MUNDO_MOVIL=1;document.body.classList.add("lite","mundom")</script>')
t='\n'.join(L)
t=re.sub(r'<title>[^<]*</title>','<title>GT Vigo · Móvil</title>',t,count=1)
open('indexm.html','w',encoding='utf8').write(t)
print('ok mundomovil')
