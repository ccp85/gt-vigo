# Praza de América con la Porta do Atlántico de Silverio Rivas, la plaza peatonal, fuentes a ras de suelo, bancos, árboles y farolas
# (america.js), en las siete páginas; va al final de la cadena, después de edit_espana.py (usa su pzeOculta).
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','webgl.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'america.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- Praza de América (america.js)'
FIN='// ---------- fin de america.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado america',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("try{pzeChk()}catch(e){console.warn('espana',e)}","try{pzeChk()}catch(e){console.warn('espana',e)}try{pamChk()}catch(e){console.warn('america',e)}")
    r("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok america',f)
