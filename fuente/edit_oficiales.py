# ================= VEHÍCULOS OFICIALES =================
# Los vehículos de la pantalla de inicio pasan a ser los del juego: el Ría GT 300 (coche), la Castro 600 (moto)
# y el Cíes H-1 (helicóptero). Un solo dibujo para los dos sitios, en oficiales.js (window.GTV_OF):
#  - menú: las funciones coche/moto/heli de inicio3d.js ahora salen de GTV_OF (se ven igual que antes).
#  - juego (solo index.html / indexm.html): oficiales_juego.js los pasa a la escala del juego.
#    · Conducir arranca en el Ría GT 300 (CAR_OF). Al robar otro coche y volver a empezar, vuelves al tuyo.
#    · La moto (bMotoC) es la Castro 600 con el protagonista y casco a juego (MOTO_OF).
#    · El helicóptero (el tuyo y los aparcados) es el Cíes H-1: mkHeli lo construye; las 4 primeras piezas
#      siguen siendo cabina, cristal, cola y deriva, así el reparto de Navidad lo repinta igual.
#  - Carrera y reparto no cambian (siguen eligiendo su coche; el «clásico granate» sigue siendo CAR0).
# Va DESPUÉS de edit_inicio.py y ANTES de edit_mundomovil.py en build.sh (así indexm.html lo hereda);
# si ya existe indexm.html también lo parchea.
import os,re
D=os.path.dirname(os.path.abspath(__file__))
rd=lambda n:open(os.path.join(D,n),encoding='utf-8').read()
FACT='<script id="gtvOficiales">\n'+rd('oficiales.js')+'</script>\n'
MENU_RE=re.compile(r'function mats\(\)\{.*?(?=function glowTex)',re.S)
MENU=("const OF=window.GTV_OF(THREE,(r,c,o={})=>M(c,o));\n"
 "function coche(){const g=OF.coche(),wheels=g.userData.wheels;\n"
 " g.userData.tick=(t,dt,on)=>{wheels.forEach(w=>w.rotation.z-=dt*(on?9:2.5));g.position.y=on?Math.sin(t*14)*.008:0};return g}\n"
 "function moto(){const g=OF.moto(),wheels=g.userData.wheels;g.scale.setScalar(1.85);\n"
 " g.userData.tick=(t,dt,on)=>{wheels.forEach(w=>w.rotation.z-=dt*(on?12:3));g.rotation.x=on?Math.sin(t*1.6)*.14:0};return g}\n"
 "function heli(){const g=OF.heli(),{rot,tr}=g.userData;g.scale.setScalar(.95);g.position.x=.35;\n"
 " g.userData.tick=(t,dt,on)=>{rot.rotation.y+=dt*(on?28:6);tr.rotation.z+=dt*(on?40:9);g.position.y=Math.sin(t*(on?2.2:1.2))*(on?.18:.06)+(on?.25:0);g.rotation.z=on?Math.sin(t*1.3)*.05:0};return g}\n")
CAR0="const CAR0=car.clone(true);CAR0.userData={tipo:'clasico'};"
HELI_RE=re.compile(r'function mkHeli\(\)\{.*?g\.userData=\{rotor,rcola\};g\.traverse\(o=>\{if\(o\.isMesh\)o\.castShadow=true\}\);return g\}',re.S)
JUEGO=[
 ("vestirCoche(mkVehiculo('moto',0xd51f1f),'moto')","vestirCoche(MOTO_OF,'moto')"),
 ("else if(modo==='coche'&&P.vestidoMoto){vestirCoche(CAR0,'clasico');P.vestidoMoto=false}",
  "else if(modo==='coche'&&car.userData.tipo!=='oficial'){vestirCoche(CAR_OF,'oficial');P.vestidoMoto=false}"),
 # piloto de Navidad sentado en la cabina del Cíes H-1
 ("g.traverse(o=>{if(o.isMesh)o.castShadow=true});heli.add(g)}\nfunction heliDesvestir",
  "g.traverse(o=>{if(o.isMesh)o.castShadow=true});if(heli.userData.oficial)g.position.set(.018,.012,0);heli.add(g)}\nfunction heliDesvestir"),
]
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'id="gtvOficiales"' in s:print('ya estaba',f);continue
    assert s.count('<div id="selz" class="v2">')==1,(f,'selz')
    s=s.replace('<div id="selz" class="v2">',FACT+'<div id="selz" class="v2">',1)
    assert len(MENU_RE.findall(s))==1,(f,'menu')
    s=MENU_RE.sub(lambda _:MENU,s,count=1)
    if f in ('index.html','indexm.html'):
        assert s.count(CAR0)==1,(f,'car0')
        s=s.replace(CAR0,CAR0+'\n'+rd('oficiales_juego.js'),1)
        assert len(HELI_RE.findall(s))==1,(f,'heli')
        s=HELI_RE.sub(lambda _:'function mkHeli(){return OFJ.heli()}',s,count=1)
        for a,b in JUEGO:
            assert s.count(a)==1,(f,a[:40]);s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s)
    print('ok oficiales',f)
