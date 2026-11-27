# Cielo barato en el móvil y menos brillo de coches en gama baja. Toca las páginas con el motor WebGL
# (indexm, gp, nav, navm y webgl); en las de WebGPU el cielo es otro. Va al final de todo, después de edit_fpsmovil.py.
# · El cielo (degradado, sol, luna, estrellas y nubes con ruido) se dibujaba el primero y sin mirar la profundidad, así que
#   calculaba sus nubes en TODOS los puntos de la pantalla aunque luego los tapara la ciudad. En la vista desde arriba no se
#   ve nada de cielo y aun así era lo que más costaba (en las pruebas, un tercio de cada imagen). Ahora, en el móvil (LITE),
#   se dibuja el último de lo opaco, pegado al fondo de la vista y respetando la profundidad: la tarjeta solo lo calcula
#   donde de verdad se ve cielo. Se ve igual.
# · Gama baja: las nubes del cielo con 3 capas de ruido en vez de 5, y los coches sin la capa de barniz (clearcoat),
#   que obliga a calcular dos veces el brillo de cada punto de la carrocería.
import sys,os
FILES=sys.argv[1:] or [f for f in ['indexm.html','gp.html','nav.html','navm.html','webgl.html'] if os.path.exists(f)]
A="const sky=new THREE.Mesh(new THREE.SphereGeometry(1,32,16),new THREE.ShaderMaterial({uniforms:SKYU,side:THREE.BackSide,depthWrite:false,depthTest:false,fog:false,"
V="vertexShader:'varying vec3 vD;void main(){vD=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',"
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'cielo al fondo (LITE)' in s:print('ya estaba',f);continue
    assert s.count(A)==1,(f,'A')
    i=s.find(A);fs=s.find('fragmentShader:`',i);fe=s.find('`',fs+17)
    blk=s[i:fe]
    assert blk.count(V)==1 and blk.count('for(int i=0;i<5;i++)')==1,(f,'blk')
    blk=blk.replace("depthTest:false,fog:false,","depthTest:!!window.LITE,fog:false,",1)
    blk=blk.replace(V,"vertexShader:'varying vec3 vD;void main(){vD=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);'+(window.LITE?'gl_Position.z=gl_Position.w;':'')+'}',",1)
    blk=blk.replace('for(int i=0;i<5;i++)','for(int i=0;i<${window.LITE&&window.GAMA_BAJA?3:5};i++)',1)
    s=s[:i]+blk+s[fe:]
    assert s.count('sky.renderOrder=-10;')==1,(f,'ro')
    s=s.replace('sky.renderOrder=-10;',"sky.renderOrder=window.LITE?1e6:-10;   // cielo al fondo (LITE): el último de lo opaco, solo donde no tapa nada\n"
      " if(window.LITE&&window.GAMA_BAJA)setInterval(()=>{scene.traverse(o=>{const m=o.material;if(!m)return;for(const x of Array.isArray(m)?m:[m])if(x.isMeshPhysicalMaterial&&x.clearcoat>0){x.clearcoat=0;x.needsUpdate=true}})},3000);\n",1)
    open(f,'w',encoding='utf8').write(s);print('ok cielomovil',f)
