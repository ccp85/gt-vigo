# Baiona, zona 1: Casco Vello y porto con detalle (baiona.js + baiona_detalle.json), en las siete páginas; va al final de la cadena, después de edit_nigran.py.
# Losas de granito en el casco, Colexiata de Santa María, paseo marítimo (muro, farolas, bancos y árboles), réplica de la
# Carabela Pinta atracada, lonxa y norays del muelle pesquero y gamelas fondeadas. Datos: herramientas/baiona_hornear.py.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gpu.html','webgl.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'baiona.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- Baiona: Casco Vello y porto (baiona.js)'
FIN='// ---------- fin de baiona.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado baiona',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("try{nigChk()}catch(e){console.warn('nigran',e)}","try{nigChk()}catch(e){console.warn('nigran',e)}try{bynChk()}catch(e){console.warn('baiona',e)}")
    r("// ---------- fin de nigran.js\n","// ---------- fin de nigran.js\n"+JS)
    open(f,'w',encoding='utf8').write(s);print('ok baiona',f)
