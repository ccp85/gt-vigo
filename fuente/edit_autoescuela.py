import sys,os
# ================= Misión: clase práctica de autoescuela (autoescuela.js) =================
# Nueva misión en el GPS (🎯 Misiones › 🚗 Autoescuela): eliges la clase y el profesor, vas a la autoescuela, circulas
# por calles tranquilas, Urzáiz y Gran Vía, haces dos rotondas (te dice qué salida) y practicas en la zona del muelle
# aparcamiento en línea, en batería, en oblicuo y la salida; vuelta a la autoescuela con nota y comentarios.
# Intermitentes con Z / X, ⬅ ➡ en pantalla o la cruceta del mando. Solo el mundo abierto. Va después de edit_taxi.py.
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'autoescuela.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '/*autoescuela*/' in s:print('ya estaba',f);continue
    assert '/*taxi*/' in s,(f,'falta edit_taxi.py')
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # nodos de la última ruta calculada (para contar las salidas de las rotondas)
    r("let GPSF=null;","let GPSF=null,GPSN=null;")
    r("if(prev[b]<0&&a!==b)return null;const nod=[];for(let u=b;u>=0;u=prev[u]){nod.push(u);if(u===a)break}nod.reverse();","if(prev[b]<0&&a!==b)return null;const nod=[];for(let u=b;u>=0;u=prev[u]){nod.push(u);if(u===a)break}nod.reverse();GPSN=nod;")
    # menú del GPS: textos de las misiones activas y la clase también oculta «Quitar ruta» y se termina al elegir otro destino
    r("/*taxi*/if(GPS.on&&!TAXI.on){","/*taxi*//*autoescuela*/if(GPS.on&&!TAXI.on&&!AE.on){")
    r("if(TAXI.on)taxiFin('otro');gpsIniciar(d)};","if(TAXI.on)taxiFin('otro');if(AE.on)aeFin('otro');gpsIniciar(d)};")
    r("<b>${m.n}${act?' · en servicio':''}</b><small>${act?'Toca para terminar el turno · 🪙 '+TAXI.mon:","<b>${m.n}${act?(m.enTxt||' · en servicio'):''}</b><small>${act?(m.actTxt||'Toca para terminar el turno')+' · 🪙 '+TAXI.mon:")
    r("function taxiEmpezar(){if(REP.on||RACE.on)return;","function taxiEmpezar(){if(REP.on||RACE.on)return;if(window.aeActivo&&window.aeActivo())aeFin('otro');")
    # golpes contra paredes, sin «anti-atasco» en la zona de prácticas, más tráfico en la clase de hora punta
    r("function golpe(){","function golpe(){if(window.aeGolpe)window.aeGolpe();")
    r("if(P.stuck>1){","if(P.stuck>1&&!window.AE_NOSTUCK){")
    r("F.vida=true;F.R=5;F.Rp=4.2;return}","F.vida=true;F.R=window.AE_TRAF?3.2:5;F.Rp=4.2;return}")
    r("if(SKC.on&&SKC.fase!=='ir'){DENS.t=0;DENS.p=0}}","if(SKC.on&&SKC.fase!=='ir'){DENS.t=0;DENS.p=0}if(window.AE_TRAF){DENS.t=1;DENS.p=Math.max(DENS.p,.8)}}")
    r("function setDrive(on,modo='coche'){if(!on&&window.taxiSalir)window.taxiSalir();","function setDrive(on,modo='coche'){if(!on&&window.taxiSalir)window.taxiSalir();if(!on&&window.aeSalir)window.aeSalir();")
    r("try{taxiTick(dt)}catch(e){console.error(e)}","try{taxiTick(dt)}catch(e){console.error(e)}try{aeTick(dt)}catch(e){console.error(e)}")
    r("// ---------- minimapa ----------\n","\n"+JS+"\n// ---------- minimapa ----------\n")
    open(f,'w',encoding='utf8').write(s);print('ok autoescuela',f)
