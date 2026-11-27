# Bouzas y Alcabre con detalle (bouzas.js + bouzas_jardin.json), en las seis páginas; va al final de la cadena.
# Jardines en las parcelas (césped, patios, prado y monte; solado de granito en el casco vello y las manzanas cerradas),
# muros de cierre gallegos con portales, sebes y lindes, árboles de jardín, pinos, palmeras y arbustos con flor, y el
# dique del Museo do Mar rehecho (muelle, escollera, acuario y faro rojo). Datos: herramientas/bouzas_hornear.py.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'bouzas.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- Bouzas y Alcabre (bouzas.js)'
FIN='// ---------- fin de bouzas.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado bouzas',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("try{calChk()}catch(e){console.warn('calzoa',e)}","try{calChk()}catch(e){console.warn('calzoa',e)}try{bzChk()}catch(e){console.warn('bouzas',e)}")
    r("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok bouzas',f)
