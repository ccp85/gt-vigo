# Nigrán, zona 1: Patos, Prado y Monteferro con detalle (nigran.js + nigran_detalle.json), en las siete páginas; va al final de la cadena.
# Suelo de monte y costa de granito con bolos en Monteferro, Monumento a la Marina Universal, batería J-3, Mirador de las
# Estelas y rosa de los vientos; muro, farolas, pasarelas y socorristas en el paseo de Patos; la ola de Prado.
# El pinar y eucaliptal de Monteferro van en baiona_inst.json. Datos: herramientas/nigran_hornear.py.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gpu.html','webgl.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'nigran.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- Nigrán: Patos, Prado y Monteferro (nigran.js)'
FIN='// ---------- fin de nigran.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado nigran',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("try{bzChk()}catch(e){console.warn('bouzas',e)}","try{bzChk()}catch(e){console.warn('bouzas',e)}try{nigChk()}catch(e){console.warn('nigran',e)}")
    r("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok nigran',f)
