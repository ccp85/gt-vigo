# Colegio Compañía de María con su iglesia (colegio.js + colegio_compania_maria.glb), en las siete páginas; va al final de la cadena.
# Modelo propio hecho en Blender (fuente/herramientas/colegio_compania_maria.py, modo GAME) con la vista aérea, Street View
# y fotos como referencia. Al cargar la zona "centro" oculta los bloques genéricos del Catastro del recinto y pone el modelo.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','webgl.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'colegio.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- Colegio Compañía de María (colegio.js)'
FIN='// ---------- fin de colegio.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado colegio',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("try{casaArtes(rt)}catch(e){console.warn('casaArtes',e)}","try{casaArtes(rt)}catch(e){console.warn('casaArtes',e)}try{cdmOculta(rt)}catch(e){console.warn('colegio',e)}")
    r("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok colegio',f)
