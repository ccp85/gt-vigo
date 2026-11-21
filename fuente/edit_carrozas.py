# Carrozas de serie de la Navidad de Vigo (las cinco páginas; va al final de la cadena).
# Cambia la función carroza() por la de carrozas.js: las cuatro carrozas rehechas con formas curvas
# (perfiles extruidos, tubos y piezas torneadas) en vez de cajas, con más detalle y menos dibujos:
#  - Sleigh GT (Papá Noel): trineo rojo con cuello de cisne, ribete de piel blanca, filigrana dorada,
#    patines con la punta enroscada, faroles, acebo, saco de regalos y escapes cromados.
#  - Aurum (Melchor): carroza real dorada con ruedas de carruaje de radios granates, paneles de terciopelo,
#    medallones, faroles altos, corona en la proa, trono y cofre abierto con monedas y joyas.
#  - Mirra (Gaspar): cápsula plateada en gota con pontones, aletas de cola con filo azul, ruedas de disco
#    con aro LED, parabrisas burbuja, estrella en el morro e incensario colgando de un arco.
#  - Esmeralda (Baltasar): carroza verde con costados ondulados, medallones con esmeraldas, mascarón de
#    camello con bridas doradas y un dosel de columnas con cúpula sobre los regalos iluminados.
# Los personajes también se rehacen (torso torneado, capa, barba con bigote, nariz, brazos al volante,
# gorro de Papá Noel, coronas y el turbante de Baltasar), con los dos puntos de ojos de edit_ojos.py.
# Todas las piezas de cada carroza se juntan en una malla por material (de 45-60 mallas a unas 25,
# luces y sombra incluidas), así que vestirCoche las copia igual y se dibujan menos cosas por imagen.
# Mismas medidas, mismo nombre de función y mismas llamadas: carrera, reparto, menú y móvil no cambian.
import os,re
D=os.path.dirname(os.path.abspath(__file__))
NUEVO=open(os.path.join(D,'carrozas.js'),encoding='utf-8').read().rstrip('\n')
RE=re.compile(r'// ---------- las cuatro carrozas \(mallas sueltas[^\n]*\n\s*function carroza\(g,tipo,pint,bx,ruedas4,luces\)\{.*?(?=\n// ---------- luces LED)',re.S)
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if '// ---------- las cuatro carrozas de serie' in s:print('ya estaba',f);continue
    assert len(RE.findall(s))==1,(f,'carroza')
    s=RE.sub(lambda _:NUEVO,s,count=1)
    open(f,'w',encoding='utf-8').write(s)
    print('ok carrozas',f)
