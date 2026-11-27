# Peatones solo por donde se puede andar (las seis páginas; va al final de la cadena).
#  - Nunca por el agua, ni por la calzada (salvo cruzando por el paso de cebra), ni por edificios o fuera del mapa:
#    toda posición final se comprueba con peaPisa (acera, zona peatonal o paso de cebra); si no vale, se deshace
#    el esquive y, si sigue sin valer, el peatón desaparece y se recoloca en otra acera.
#  - Al caer atropellados tampoco salen despedidos al agua o a la calzada.
#  - Recién recolocados no se quedan "colgados" en el sitio viejo: si su primera posición no vale, se ocultan.
#  - Altura: bajo puentes y pasos elevados se elige la superficie más cercana a la del mapa (antes cogían el tablero
#    de arriba y quedaban flotando en el aire).
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '(edit_peatones)' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("function peaEsquiva(",
      "// dónde puede pisar un peatón: acera, zona peatonal o paso de cebra (edit_peatones)\n"
      "const peaPisa=(x,y)=>{const c=cell(x,y);return c.t===1||c.t===5||(c.t===2&&c.c)};\n"
      "// suelo del peatón: con puentes encima elige la superficie más cercana a la del mapa, no el tablero\n"
      "const RCpea=new THREE.Raycaster();\n"
      "function sueloPea(x,y){if(!GROUND.length)return groundY(x,y);_o.set(x,9,y);RCpea.set(_o,_dn);RCpea.far=12;const h=RCpea.intersectObjects(GROUND,false);"
      "if(h.length<2)return groundY(x,y);const m=groundMap(x,y);let b=null,bd=1e9;for(const k of h){const z=oriSuelo(k,x,y),d=Math.abs(z-m);if(d<bd){bd=d;b=z}}return b}\n"
      "function peaEsquiva(")
    r("if(q.caido>0){q.caido-=dt;const dm=Math.exp(-dt*4);q.ex+=q.kvx*dt;q.ey+=q.kvy*dt;",
      "if(q.caido>0){q.caido-=dt;const dm=Math.exp(-dt*4);{const nx=q.ex+q.kvx*dt,ny=q.ey+q.kvy*dt;if(peaPisa(q.x+nx,q.y+ny)){q.ex=nx;q.ey=ny}else{q.kvx=q.kvy=0}}")
    r("q.ex=q.ey=0;q.caido=0;q.esq=0;q.tilt=0}",
      "q.ex=q.ey=0;q.caido=0;q.esq=0;q.tilt=0;q.nuevo=true}")
    r("q.mal=(q.mal||0)+.25;if(q.mal<=1.5)continue}}",
      "q.mal=(q.mal||0)+.25;if(q.mal<=1.5){if(q.nuevo)PEA_G.hide(i);continue}}}")
    r("if(!q.cruza&&!(q.caido>0)){const cf=cell(q.x,q.y);if(cf.t===2&&!cf.c){if(q.ex||q.ey){q.x-=q.ex||0;q.y-=q.ey||0;q.ex=q.ey=0;q.esq=0}const cb=cell(q.x,q.y);if(cb.t===2&&!cb.c){q.r=null;q.x=1e5;PEA_G.hide(i);continue}}}",
      "if(!peaPisa(q.x,q.y)){if(q.ex||q.ey){q.x-=q.ex||0;q.y-=q.ey||0;q.ex=q.ey=0;q.esq=0}if(!peaPisa(q.x,q.y)&&!(q.cruza&&cell(q.x,q.y).t===2)){q.r=null;q.x=1e5;PEA_G.hide(i);continue}}   // nunca por agua ni calzada (solo cruzando por el paso de cebra) (edit_peatones)\n  q.nuevo=false;")
    r("if(q.z===null||(i+frameN)%4===0)q.z=groundY(q.x,q.y);",
      "if(q.z===null||(i+frameN)%4===0)q.z=sueloPea(q.x,q.y);")
    open(f,'w',encoding='utf8').write(s);print('ok peatones',f)
