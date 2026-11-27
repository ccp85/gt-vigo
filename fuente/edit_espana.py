# Praza de España (Os Cabalos de Oliveira con su fuente en espiral) y Os Redeiros de Ramón Conde al pie de las rampas de Gran Vía
# (espana.js), en las siete páginas; va al final de la cadena. No toca las rampas (edit_rampas.py / edit_rampas2.py).
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','webgl.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'espana.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- Praza de España y Os Redeiros (espana.js)'
FIN='// ---------- fin de espana.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado espana',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("function subeZonas(){","function subeZonas(){try{pzeChk()}catch(e){console.warn('espana',e)}")
    r("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok espana',f)
