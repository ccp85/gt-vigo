import sys,os
# ================= Minijuego de surf en la playa de Patos (surf.js) =================
# Nueva misión en el GPS: «🏄 Surf en Patos». La línea azul lleva a la playa; en la arena hay una tabla clavada con su aro
# y al llegar sale la ficha de la playa (foto real, dónde está, cómo llegar desde Vigo, tipo de ola, nivel, mejor época)
# y empieza una sesión de 3 minutos. Ver surf.js.
# Solo el mundo abierto (index.html e indexm.html). Va después de edit_taxi.py y de edit_olas.py.
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'surf.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function surfUpdate(' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # misiones del GPS: texto propio cuando la misión está en marcha
    r("${act?'Toca para terminar el turno · 🪙 '+TAXI.mon:","${act?(m.da||'Toca para terminar el turno')+' · 🪙 '+TAXI.mon:")
    # mientras surfeas, el minijuego lleva la cámara y el surfista (el vehículo se queda aparcado)
    r("function updateCar(dt){if(MODO==='heli')","function updateCar(dt){if(SG.on){surfUpdate(dt);return}if(MODO==='heli')")
    # se ven las Cíes al fondo (más distancia de dibujo durante el minijuego)
    r("pcam.far=/*fondoheli*/FONDO.m&&!window.LITE?260:FOG.far+4","pcam.far=SG.on?230:/*fondoheli*/FONDO.m&&!window.LITE?260:FOG.far+4")
    # salir del modo conducción termina la sesión
    r("function setDrive(on,modo='coche'){if(!on&&window.taxiSalir)window.taxiSalir();","function setDrive(on,modo='coche'){if(!on&&window.taxiSalir)window.taxiSalir();if(!on&&window.surfgSalir)window.surfgSalir();")
    # cada fotograma: tabla de la playa y llegada
    r("try{taxiTick(dt)}catch(e){console.error(e)}","try{taxiTick(dt)}catch(e){console.error(e)}try{surfgTick(dt)}catch(e){if(!window.__sgErr){window.__sgErr=1;console.error(e)}}")
    # mando: la ficha se maneja como los menús; en el agua manda el minijuego
    r("for(const id of ['radioPanel','nFin','rFin','selCar','selz'])","for(const id of ['sgFicha','radioPanel','nFin','rFin','selCar','selz'])")
    r(" // conducción\n const val="," // conducción\n if(SG.on){sgPad(b,ax,dn);return}\n const val=")
    # el código, después del taxi
    r("// ---------- minimapa ----------\n","\n"+JS+"\n// ---------- minimapa ----------\n")
    open(f,'w',encoding='utf8').write(s);print('ok surf',f)
