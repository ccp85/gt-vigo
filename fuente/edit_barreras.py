# Barreras invisibles fuera (las seis páginas; va al final de la cadena, después de peatones).
# En el mapa de celdas hay "edificios" (tipo 3) que en 3D no tienen nada encima: muros, vallas y trozos de OSM
# que no se dibujan (p. ej. la línea que cruza la playa do Vao, en Coruxo, junto al puente de Toralla).
# Andando y en coche bloqueaban el paso sin que se viera nada.
# Ahora una celda de edificio solo bloquea si de verdad hay un edificio o pieza encima: se lanza un rayo
# vertical contra las mallas de edificios/piezas (OBST, con BVH) en el centro de la celda y cuatro puntos
# alrededor; el resultado se guarda por celda. Mientras las colisiones de la zona se están preparando, se
# sigue bloqueando como antes (así no se atraviesan edificios reales al cargar).
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '(edit_barreras)' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("function updateCar(dt){",
      "// celdas de edificio sin nada encima (muros y vallas del mapa que no se ven) no bloquean (edit_barreras)\n"
      "const EDR=new Map(),RCe=new THREE.Raycaster(),_oE=new THREE.Vector3(),_dE=new THREE.Vector3(0,-1,0);RCe.firstHitOnly=true;\n"
      "function edifReal(x,y){const OB=window.OBST;if(!MAPA||!OB||!OB.length)return true;const i=Math.round((x-MAPA.ox)*MAPA.res),j=Math.round((y-MAPA.oy)*MAPA.res),k=j*MAPA.w+i;\n"
      " const e=EDR.get(k);if(e&&(e.s||e.n===OB.length))return e.s;\n"
      " if(BVHQ.some(o=>!o.userData.suelo))return true;   // colisiones de la zona aún preparándose: como antes\n"
      " const cx=MAPA.ox+i/MAPA.res,cy=MAPA.oy+j/MAPA.res,g=groundY(cx,cy);let sol=false;\n"
      " for(const[a,b]of[[0,0],[.018,0],[-.018,0],[0,.018],[0,-.018]]){_oE.set(cx+a,9,cy+b);RCe.set(_oE,_dE);RCe.far=12;const h=RCe.intersectObjects(OB,false)[0];if(h&&h.point.y>g+.008){sol=true;break}}\n"
      " if(EDR.size>300000)EDR.clear();EDR.set(k,{s:sol,n:OB.length});return sol}\n"
      "window.edifReal=edifReal;\n"
      "function updateCar(dt){")
    r("return t===0||t===3||t===-1||t===6||(RR&&REP.cerrado&&!repLibre(x,y))});",
      "return t===0||(t===3&&edifReal(x,y))||t===-1||t===6||(RR&&REP.cerrado&&!repLibre(x,y))});")
    open(f,'w',encoding='utf8').write(s);print('ok barreras',f)
