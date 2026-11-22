import sys,os
# ================= SIN DESTELLO NEGRO AL BUCEAR =================
# Al meterte bajo el agua (o al subir) la cámara pasaba unos fotogramas justo por la franja de la superficie: ya estaba
# por debajo del agua de la zona (que solo se ve desde arriba) pero el juego aún no la daba por «bajo el agua»
# (sin niebla azul ni fondo tapado). En esos fotogramas se veía el cielo a través del agua y el fondo marino
# en negro, sin niebla: un destello negro. Ahora la cámara nunca se queda en esa franja: salta a un lado u otro
# de la superficie según estés buceando o no. Las cinco páginas.
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
A="else pcam.position.lerp(want,Math.min(1,dt*4));look.set(P.x+dx*.12,"
B="else pcam.position.lerp(want,Math.min(1,dt*4));{const wy=B.WY,yc=pcam.position.y;if(Math.abs(yc-wy)<.007)pcam.position.y=bajo?wy-.007:wy+.007}   // edit_buceoflash.py\n look.set(P.x+dx*.12,"
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'edit_buceoflash.py' in s:print('ya estaba',f);continue
    assert s.count(A)==1,(f,s.count(A))
    s=s.replace(A,B);open(f,'w',encoding='utf8').write(s);print('ok buceoflash',f)
