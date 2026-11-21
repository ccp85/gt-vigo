import sys,os
# ================= Misiones en el GPS + misión de taxi (taxi.js) =================
# El menú del GPS lleva arriba «🎯 Misiones» (botones dorados con icono y etiqueta MISIÓN) y debajo «📍 Direcciones
# frecuentes». Primera misión: 🚕 Taxi (el coche se convierte en taxi, recoges clientes guiado por la línea azul, los
# llevas a su destino y cobras monedas 🪙, con propina si llegas a tiempo). Ver taxi.js.
# Solo el mundo abierto (index.html e indexm.html). Va al final de build.sh.
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'taxi.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '/*taxi*/' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # menú del GPS: misiones arriba; «Quitar ruta» no sale durante el taxi; elegir otro destino termina el turno
    r("if(GPS.on){const b=document.createElement('button');b.textContent='✕ Quitar ruta';","/*taxi*/if(GPS.on&&!TAXI.on){const b=document.createElement('button');b.textContent='✕ Quitar ruta';")
    r(" const orden=DESTINOS.map(d=>[d,Math.hypot(d[1]-P.x,d[2]-P.y)])"," gpsMisiones(L);const orden=DESTINOS.map(d=>[d,Math.hypot(d[1]-P.x,d[2]-P.y)])")
    r("b.onclick=()=>{document.getElementById('gpsMenu').hidden=true;gpsIniciar(d)};L.appendChild(b)}","b.onclick=()=>{document.getElementById('gpsMenu').hidden=true;if(TAXI.on)taxiFin('otro');gpsIniciar(d)};L.appendChild(b)}")
    # la ruta del taxi no se da por terminada al llegar (la cierra la misión) y no lleva el marcador azul
    r("const e=P_[P_.length-1];if(Math.hypot(e[0]-P.x,e[1]-P.y)<.18){mostrar('🏁 Has llegado a '","const e=P_[P_.length-1];if(!GPS.taxi&&Math.hypot(e[0]-P.x,e[1]-P.y)<.18){mostrar('🏁 Has llegado a '")
    r("GPS_DEST.visible=!REP.on;document.getElementById('gps').hidden=false;gpsPanel()}","GPS_DEST.visible=!REP.on&&!GPS.taxi;document.getElementById('gps').hidden=false;gpsPanel()}")
    r("function gpsParar(){GPS.on=false;","function gpsParar(){GPS.on=false;GPS.taxi=false;")
    # salir del modo conducción termina el turno
    r("function setDrive(on,modo='coche'){","function setDrive(on,modo='coche'){if(!on&&window.taxiSalir)window.taxiSalir();")
    # cada fotograma
    r("if(driving){recortar(dt);nombreCalle(dt);gpsTick(dt);","if(driving){recortar(dt);nombreCalle(dt);gpsTick(dt);try{taxiTick(dt)}catch(e){console.error(e)}")
    # el código de la misión, junto al GPS
    r("// ---------- minimapa ----------\n","\n"+JS+"\n// ---------- minimapa ----------\n")
    open(f,'w',encoding='utf8').write(s);print('ok taxi',f)
