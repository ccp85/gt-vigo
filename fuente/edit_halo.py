# Halo (ascensor urbano con el anillo de 90 m) y la plaza de la cubierta de Vialia con pistas y skatepark (halo.js).
# Siete páginas; va al final de la cadena.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','webgl.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'halo.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- Halo y cubierta de Vialia (halo.js)'
FIN='// ---------- fin de halo.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado halo',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("function subeZonas(){","function subeZonas(){try{halChk()}catch(e){console.warn('halo',e)}")
    r("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok halo',f)
