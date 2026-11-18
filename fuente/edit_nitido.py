import os
f='index.html';s=open(f,encoding='utf8').read()
D=os.path.dirname(os.path.abspath(__file__))
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MÓVIL NÍTIDO (window.LITE: navm.html e indexm.html) =================
# Va antes de edit_skatetest.py para que lo hereden nav/navm; todo con window.LITE (en el ordenador no cambia nada).
# 1) antialias también en el móvil (en las gráficas de móvil, que pintan por baldosas, cuesta poco y quita los dientes de sierra)
r("antialias:!window.LITE,","antialias:true,")
# 2) resolución: empieza en 1,25 (o la de la pantalla si es menor), sube hasta 1,5 si sobra y nunca baja de 1 (antes: 1, hasta 1,1, mínimo 0,9)
r("R.setPixelRatio(window.LITE?Math.min(1,devicePixelRatio):","R.setPixelRatio(window.LITE?Math.min(1.25,devicePixelRatio):")
r("const PRmax=window.LITE?Math.min(1.1,devicePixelRatio):","const PRmax=window.LITE?Math.min(1.5,devicePixelRatio):")
r("let prAct=window.LITE?Math.min(1,PRmax):","let prAct=window.LITE?Math.min(1.25,PRmax):")
r("const PRmin=window.LITE?Math.min(.9,devicePixelRatio):","const PRmin=window.LITE?Math.min(1,devicePixelRatio):")
# 3) materiales mates y texturas grandes reducidas (nitido.js)
r("window.CIRT=()=>CIR;","window.CIRT=()=>CIR;\n"+open(os.path.join(D,'nitido.js'),encoding='utf8').read())
open(f,'w',encoding='utf8').write(s)
print('ok nitido')
