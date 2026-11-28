# Calidad Baja (modo gama baja del móvil): menos tráfico, menos peatones y árboles más cerca. Va al final de todo.
# · Tráfico ×0,5 y peatones ×0,4 sobre la densidad de cada hora (no en las misiones que necesitan el tráfico entero).
# · Calidad automática: empieza en 0,3 (antes 0,35), puede bajar hasta 0,25 y subir como mucho a 0,5 (antes 0,6). Esto
#   acorta la distancia de los árboles, los bosques, las farolas y la niebla.
# La decoración lejana la quita trozos.js (edit_trozos.py).
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','webgl.html','gpu.html'] if os.path.exists(f)]
R=[("DENS.p=dInterp(DTAB_P,h);if(SKC.on","DENS.p=dInterp(DTAB_P,h);if(window.LITE&&window.GAMA_BAJA){DENS.t*=.5;DENS.p*=.4}   // calidad Baja: menos tráfico y gente (edit_bajamenos.py)\n if(SKC.on"),
   ("let QF=window.LITE?(window.GAMA_BAJA?.35:.5):1;","let QF=window.LITE?(window.GAMA_BAJA?.3:.5):1;"),
   ("QMAX=window.LITE?(window.GAMA_BAJA?.6:.8):1,","QMAX=window.LITE?(window.GAMA_BAJA?.5:.8):1,"),
   ("if(QF>.35)QF=Math.max(.35,QF-.1);","if(QF>(window.GAMA_BAJA?.25:.35))QF=Math.max(window.GAMA_BAJA?.25:.35,QF-.1);")]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'edit_bajamenos.py' in s:print('ya estaba',f);continue
    n=0
    for a,b in R:
        c=s.count(a)
        if c==1:s=s.replace(a,b);n+=1
        elif c>1:raise SystemExit((f,a,c))
    open(f,'w',encoding='utf8').write(s);print('ok bajamenos',f,n,'de',len(R))
