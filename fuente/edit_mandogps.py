import sys,os
# ================= Mando de Xbox: Ⓑ abre el GPS =================
# Conduciendo (mundo abierto y Navidad), Ⓑ abre el menú «¿A dónde vamos?» del GPS.
# Con el menú abierto se maneja como los demás menús: cruceta/stick para moverse, Ⓐ elige, Ⓑ cierra.
# En carreras (donde no hay GPS) Ⓑ sigue siendo «reaparecer».
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','nav.html','navm.html','gp.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '/*mandogps*/' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # el menú del GPS cuenta como menú para el mando
    r("function padMenuVis(){for(const id of [","function padMenuVis(){for(const id of [/*mandogps*/'gpsMenu',")
    # Ⓑ en el menú del GPS: cerrarlo
    r("if(dn(1)&&ov.id!=='selCar'){","if(dn(1)&&ov.id==='gpsMenu'){ov.hidden=true}else if(dn(1)&&ov.id!=='selCar'){")
    # Ⓑ conduciendo: abre el GPS si está disponible; si no (carreras), reaparecer
    r("if(dn(1))padK('KeyR');","if(dn(1)){const bg=document.getElementById('bGPS');if(bg&&bg.getClientRects().length){bg.click();padVibra(.2,0,60)}else padK('KeyR')}")
    # aviso al conectar el mando
    r("Ⓐ acción · Ⓧ cámara')","Ⓐ acción · Ⓑ GPS · Ⓧ cámara')")
    open(f,'w',encoding='utf8').write(s);print('ok',f)
