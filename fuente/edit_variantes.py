# ================= VARIANTES DE LOS VEHÍCULOS OFICIALES =================
# Tres modelos de cada vehículo (oficiales.js): coches Ría GT 300 / Bouzas 4x4 / Samil Spider,
# motos Castro 600 / Toralla RR / Arenal 125, helicópteros Cíes H-1 / Rande SR / Ons Vortex.
#  - menú: ‹ › en la tarjeta elegida (▲ ▼ con teclado) cambian el modelo, con su nombre, tipo y barras (variantes_menu.js);
#    el dibujo 3D cambia con GTV_MODELO3D.
#  - juego (index/indexm): conduces el modelo elegido; los helicópteros aparcados salen de los tres modelos al azar.
# Va DESPUÉS de edit_oficiales.py (pone al día lo que ese insertó) y antes de edit_mundomovil.py.
import os,re
D=os.path.dirname(os.path.abspath(__file__))
rd=lambda n:open(os.path.join(D,n),encoding='utf-8').read()
FACT='<script id="gtvOficiales">\n'+rd('oficiales.js')+'</script>\n'
UI='<script id="gtvVariantes">\n'+rd('variantes_menu.js')+'</script>\n'
FACT_RE=re.compile(r'<script id="gtvOficiales">\n.*?</script>\n',re.S)
JUEGO_RE=re.compile(r"// ---------- vehículos oficiales en el juego.*?(?:// fin vehiculos oficiales|const MOTO_OF=OFJ\.moto\(\);MOTO_OF\.userData\.tipo='moto';)\n",re.S)
MENU_RE=re.compile(r'const OF=window\.GTV_OF\(THREE,.*?(?=function glowTex)',re.S)
MENU=("const OF=window.GTV_OF(THREE,(r,c,o={})=>M(c,o));\n"
 "const OFSEL=k=>{try{const v=JSON.parse(localStorage.getItem('gtvigo_modelos')||'{}')[k];return [0,1,2].includes(v)?v:0}catch(e){return 0}};\n"
 "function coche(i=OFSEL('coche')){const g=OF.coche(i),wheels=g.userData.wheels;g.userData.mi=i;\n"
 " g.userData.tick=(t,dt,on)=>{wheels.forEach(w=>w.rotation.z-=dt*(on?9:2.5));g.position.y=on?Math.sin(t*14)*.008:0};return g}\n"
 "function moto(i=OFSEL('moto')){const g=OF.moto(i),wheels=g.userData.wheels;g.userData.mi=i;g.scale.setScalar(i===2?1.95:1.85);\n"
 " g.userData.tick=(t,dt,on)=>{wheels.forEach(w=>w.rotation.z-=dt*(on?12:3));g.rotation.x=on?Math.sin(t*1.6)*.14:0};return g}\n"
 "function heli(i=OFSEL('heli')){const g=OF.heli(i),{rot,tr}=g.userData;g.userData.mi=i;g.scale.setScalar(i===1?.85:.95);g.position.x=i===1?.5:.35;\n"
 " g.userData.tick=(t,dt,on)=>{rot.rotation.y+=dt*(on?28:6);tr.rotation.z+=dt*(on?40:9);g.position.y=Math.sin(t*(on?2.2:1.2))*(on?.18:.06)+(on?.25:0);g.rotation.z=on?Math.sin(t*1.3)*.05:0};return g}\n"
 "window.GTV_MODELO3D=(k,i)=>{if(!views)return;const v=views.find(v=>v.card.dataset.v===k);if(!v||v.model.userData.mi===i)return;\n"
 " v.piv.remove(v.model);v.model=({coche,moto,heli})[k](i);v.piv.add(v.model)};\n")
JUEGO=[
 ("car.userData.tipo!=='oficial'","car.userData.tipo!==CAR_OF.userData.tipo"),
 ("function mkHeli(){return OFJ.heli()}","function mkHeli(){return OFJ.heli(OFJ.nHeli++?Math.random()*3|0:OF_SEL.heli)}"),
]
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'id="gtvVariantes"' in s:print('ya estaba',f);continue
    assert len(FACT_RE.findall(s))==1,(f,'fact');s=FACT_RE.sub(lambda _:FACT,s,count=1)
    assert len(MENU_RE.findall(s))==1,(f,'menu');s=MENU_RE.sub(lambda _:MENU,s,count=1)
    i=s.find('// ===== Pantalla de inicio v2 (interfaz)');j=s.find('</script>\n',i)+10
    assert i>0 and j>i and s.find('<script id="gtvOficiales">')<i,(f,'ui');s=s[:j]+UI+s[j:]
    if f in ('index.html','indexm.html'):
        assert len(JUEGO_RE.findall(s))==1,(f,'juego');s=JUEGO_RE.sub(lambda _:rd('oficiales_juego.js'),s,count=1)
        for a,b in JUEGO:
            assert s.count(a)==1,(f,a);s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s)
    print('ok variantes',f)
