import os
f='index.html';s=open(f,encoding='utf8').read()
D=os.path.dirname(os.path.abspath(__file__))
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MÓVIL NÍTIDO (window.LITE: navm.html e indexm.html) =================
# Va antes de edit_skatetest.py para que lo hereden nav/navm; todo con window.LITE (en el ordenador no cambia nada).
# 1) (quitado) el antialias en el móvil: con él y más resolución, algún móvil se quedaba en negro al cargar el mapa y se reiniciaba
# 2) resolución: empieza como siempre (1) para no forzar la gráfica al cargar; si el móvil va sobrado (llega al tope de 30 imágenes
#    por segundo) sube poco a poco hasta 1,5; si va justo baja hasta 0,75 como mucho (antes podía llegar a 0,55: muy pixelado)
r("const PRmax=window.LITE?Math.min(1.1,devicePixelRatio):","const PRmax=window.LITE?Math.min(1.5,devicePixelRatio):")
r("const PRmin=window.LITE?Math.min(.9,devicePixelRatio):","const PRmin=window.LITE?Math.min(.75,devicePixelRatio):")
# con el tope de 30 imágenes por segundo del móvil nunca se cumplía «más de 31» y la resolución no subía nunca
r("else if(ft<1/31){if(prAct<PRmax)","else if(ft<1/29){if(prAct<PRmax)")
# 3) materiales mates y texturas grandes reducidas (nitido.js)
r("window.CIRT=()=>CIR;","window.CIRT=()=>CIR;\n"+open(os.path.join(D,'nitido.js'),encoding='utf8').read())
# 4) asfalto: en el móvil sin el grano fino ni las grietas (de lejos ya se difuminaban; a la resolución del móvil solo eran ruido),
#    se quedan las manchas y los parches: 3 cálculos de ruido menos por cada punto de calzada
a="float grano=(hM(floor(q*420.))-.5)*(1.-smoothstep(.003,.012,fw))+(nM(q*150.)-.5)*1.4*(1.-smoothstep(.006,.025,fw));float gf=1.;"
r(a,"${window.LITE?'float grano=0.;float gf=0.;':'"+a+"'}")
a="float gri=smoothstep(.985,1.,nM(q*90.+3.))*(1.-smoothstep(.002,.008,fw));"
r(a,"${window.LITE?'float gri=0.;':'"+a+"'}")
# 5) reflejo del cielo en los coches: en el ordenador se rehace cada 4 s; en el móvil cada 60 s (cada vez son decenas de pasadas de GPU: tirón)
r("if(t-ENVC.t<4)return;","if(t-ENVC.t<(window.LITE?60:4))return;")
# 6) detalles de fachada (balcones, marcos) al conducir: en el móvil hasta 4 de distancia en vez de 6 (con la niebla del móvil apenas se veían más allá)
r("R_=driving?6:(cam.zoom>6?7:0);","R_=driving?(window.LITE?4:6):(cam.zoom>6?7:0);")
open(f,'w',encoding='utf8').write(s)
print('ok nitido')
