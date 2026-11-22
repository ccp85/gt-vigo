import sys,os
# ================= Minijuego de basket en las canchas de Samil (basket.js) =================
# Nueva misión en el GPS: «🏀 Basket en Samil». La cancha (mural propio con los colores de las pistas reales) queda siempre
# en el mundo, en la franja entre el paseo y la avenida de Samil: allí no se ponen aparcamientos ni palmeras y se quitan
# los árboles que caigan dentro. Al llegar sale la ficha (dónde está, cómo llegar) y eliges 1x1, 3x3, 5x5 o entrenamiento.
# Cámara de tele desde la banda. Ver basket.js.
# Solo el mundo abierto (index.html e indexm.html). Va después de edit_surf.py y de edit_mandogps.py.
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'basket.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function bkUpdate(' in s:print('ya estaba',f);continue
    assert 'function surfUpdate(' in s,(f,'falta edit_surf.py')
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # Samil: sitio de la cancha en la franja tras el paseo; esa parte pasa a ser una explanada y se quitan los árboles
    r(" const enF=(x,y)=>{const i=Math.round((y-C[0][1])/.08);"," try{SAM.bk=bkSitio(F)}catch(e){SAM.bk=null}\n const enF=(x,y)=>{const i=Math.round((y-C[0][1])/.08);")
    r("const aclarar=()=>{const o0=SAM.oc;ocultar((x,y)=>enF(x,y)","const aclarar=()=>{const o0=SAM.oc;ocultar((x,y)=>SAM.bk&&bkDentroM(x,y,.03)||enF(x,y)")
    r("SETO=M(0x2f6b2c);","SETO=M(0x2f6b2c),PLZ=M(0xcfc8ba,{roughness:.95,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2});")
    r("   if(tipo==='ap'){quad(ASF,x0,x1,z0,z1);","   if(SAM.bk&&bkFilaToca(x0,x1,y)){quad(PLZ,x0,x1,z0,z1);continue}\n   if(tipo==='ap'){quad(ASF,x0,x1,z0,z1);")
    # mientras juegas, el minijuego lleva la cámara y los jugadores (el vehículo se queda aparcado)
    r("function updateCar(dt){if(SG.on){surfUpdate(dt);return}","function updateCar(dt){if(BK.on){bkUpdate(dt);return}if(SG.on){surfUpdate(dt);return}")
    r("pcam.far=SG.on?230:","pcam.far=BK.on?200:SG.on?230:")
    r("UCUT.uCut.value=MODO==='heli'||window.__CAM?0:1;","UCUT.uCut.value=MODO==='heli'||window.__CAM||BK.on?0:1;")
    # salir del modo conducción termina el partido
    r("if(!on&&window.surfgSalir)window.surfgSalir();","if(!on&&window.surfgSalir)window.surfgSalir();if(!on&&window.basketSalir)window.basketSalir();")
    # cada fotograma: la cancha, el marcador de la misión y la llegada
    r("try{surfgTick(dt)}catch(e){if(!window.__sgErr){window.__sgErr=1;console.error(e)}}","try{surfgTick(dt)}catch(e){if(!window.__sgErr){window.__sgErr=1;console.error(e)}}try{basketTick(dt)}catch(e){if(!window.__bkErr){window.__bkErr=1;console.error(e)}}")
    # mando: la ficha se maneja como los menús; en la cancha manda el minijuego
    r("/*mandogps*/'gpsMenu','sgFicha',","/*mandogps*/'gpsMenu','sgFicha','bkFicha',")
    r(" // conducción\n if(SG.on){sgPad(b,ax,dn);return}"," // conducción\n if(BK.on){bkPad(b,ax,dn);return}\n if(SG.on){sgPad(b,ax,dn);return}")
    # el código, después del surf
    r("// ---------- minimapa ----------\n","\n"+JS+"\n// ---------- minimapa ----------\n")
    open(f,'w',encoding='utf8').write(s);print('ok basket',f)
