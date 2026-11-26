import sys,os
# ================= SIN DESTELLO NI PARPADEO AL BUCEAR =================
# Al meterte bajo el agua (o al subir) la cámara pasaba unos fotogramas justo por la franja de la superficie: ya estaba
# por debajo del agua de la zona (que solo se ve desde arriba) pero el juego aún no la daba por «bajo el agua»
# (sin niebla azul ni fondo tapado): destello negro.
# v2: la primera versión elegía el lado según si el nadador estaba buceando, y nadando justo bajo la superficie la
# cámara saltaba arriba y abajo (parpadeo); además quedaba tan pegada a la «superficie vista desde abajo» que esta
# se cortaba con el plano cercano de la cámara. Ahora la cámara recuerda en qué lado está y solo cambia cuando quiere
# ir claramente al otro (con margen), cruzando de golpe; y se queda a distancia de la superficie por los dos lados.
# Las páginas con buceo (index, indexm, gp, nav, navm, gpu).
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','gpu.html'] if os.path.exists(f)]
A="else pcam.position.lerp(want,Math.min(1,dt*4));look.set(P.x+dx*.12,"
V1="{const wy=B.WY,yc=pcam.position.y;if(Math.abs(yc-wy)<.007)pcam.position.y=bajo?wy-.007:wy+.007}   // edit_buceoflash.py\n "
V2=("{const wy=B.WY,w=want.y;if(B.cs===undefined)B.cs=pcam.position.y<wy;if(B.cs&&w>wy+.016)B.cs=false;else if(!B.cs&&w<wy-.02)B.cs=true;"
    "const yc=pcam.position.y;if(B.cs&&yc>wy-.018)pcam.position.y=wy-.018;else if(!B.cs&&yc<wy+.014)pcam.position.y=wy+.014}   // edit_buceoflash.py v2\n ")
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'edit_buceoflash.py v2' in s:print('ya estaba',f);continue
    if V1 in s: s=s.replace(V1,V2)
    else:
        assert s.count(A)==1,(f,s.count(A))
        s=s.replace(A,A.replace("look.set(","")+V2+"look.set(")
    # al salir del buceo se olvida el lado
    if "function buceoLimpia(sube){const B=BUC;" in s: s=s.replace("function buceoLimpia(sube){const B=BUC;","function buceoLimpia(sube){const B=BUC;B.cs=undefined;",1)
    open(f,'w',encoding='utf8').write(s);print('ok buceoflash v2',f)
