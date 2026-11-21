# Charcos con reflejos de verdad (las cinco páginas; va después de edit_reflejos.py y edit_asfalto.py).
# Con lluvia, la calzada mojada y los charcos (edit de «mojado») reflejaban solo un degradado del cielo. Ahora reflejan
# la ciudad: usan la misma foto de 6 caras que la pintura de los coches (edit_reflejos.py), así que en los charcos se ven
# las fachadas, los árboles, los coches y el cielo, y de noche las farolas, ventanas y luces de la Navidad.
#  - el reflejo se corrige según la distancia al punto de la foto (parallax), para que los edificios cuadren con el suelo;
#  - las luces se estiran en vertical (4 muestras), como las estelas de luz en el asfalto mojado de verdad;
#  - las gotas que caen en los charcos ondulan también el reflejo;
#  - charcos con el borde más suave y más espejo cuanto más rasante se miran; la calzada solo mojada refleja suave, más cuanto más rasante la miras.
#  - mientras llueve o el suelo sigue mojado, la foto se rehace también yendo a pie (antes solo dentro de un vehículo);
#    mientras se hace la foto, el suelo no se usa a sí mismo de espejo (evita el bucle de la tarjeta gráfica).
# En el móvil (LITE) no hay foto de la ciudad: sigue el reflejo del cielo de antes.
import os
R=[
 ("const UMO={uWet:{value:0},uTm:{value:0},uLz:{value:0}};",
  "const UMO={uWet:{value:0},uTm:{value:0},uLz:{value:0}};\nconst UENV={uEnvC:{value:null},uEnvOn:{value:0},uEnvP:{value:new THREE.Vector3()}};   // edit_charcos.py: foto de la ciudad para los charcos"),
 ("Object.assign(sh.uniforms,UMO,{uZen:SKYU.uZen,uHor:SKYU.uHor,uK:{value:k}});",
  "Object.assign(sh.uniforms,UMO,UENV,{uZen:SKYU.uZen,uHor:SKYU.uHor,uK:{value:k}});"),
 ("'uniform float uWet,uTm,uLz,uK;uniform vec3 uZen,uHor;varying vec3 vWm;\\n",
  "'uniform float uWet,uTm,uLz,uK;uniform vec3 uZen,uHor;varying vec3 vWm;uniform samplerCube uEnvC;uniform float uEnvOn;uniform vec3 uEnvP;\\n"),
 ("vec3 sky=mix(uHor,uZen,clamp(Vv.y*1.3,0.,1.));",
  """vec3 sky=mix(uHor,uZen,clamp(Vv.y*1.3,0.,1.));
     if(uEnvOn>.5){vec3 rd=vec3(-Vv.x,abs(Vv.y),-Vv.z);rd.xz+=(vec2(nM(vWm.xz*70.+uTm*2.),nM(vWm.xz*70.-uTm*2.+9.))-.5)*.09*pud;
      vec3 rp=(vWm-uEnvP)/1.6;vec3 env=vec3(0.);for(int i=0;i<4;i++){vec3 d=normalize(rd+rp+vec3(0.,(float(i)-1.5)*.07*(.4+.6*pud),0.));env+=textureCube(uEnvC,d).rgb;}
      env*=.25;sky=mix(sky,env,.92);}"""),
 ("float ref=wW*(.10+.55*pud)*(.35+2.2*fr);outgoingLight=mix(outgoingLight,sky*(1.+.6*rip),clamp(ref,0.,.6));",
  "float ref=wW*(.10+.62*pud)*(.18+2.6*fr);outgoingLight=mix(outgoingLight,sky*(1.+.6*rip),clamp(ref,0.,uEnvOn>.5?.82:.6));"),
 ("pud=smoothstep(.58,.68,n+.08*(uWet-.5))*smoothstep(.15,.6,uWet);",
  "pud=smoothstep(.56,.71,n+.08*(uWet-.5))*smoothstep(.15,.6,uWet);"),
 ("function reflejosCoches(){if(!driving){RCUBO.face=0;return}",
  "function reflejosCoches(){if(!driving&&!(UMO.uWet.value>.02)){RCUBO.face=0;return}"),
 ("sh.autoUpdate=false;UCUT.uCut.value=0;",
  "sh.autoUpdate=false;UCUT.uCut.value=0;UENV.uEnvOn.value=0;UENV.uEnvC.value=null;"),
 ("if(RCUBO.face>=6){RCUBO.face=0;RCUBO.out=",
  "if(RCUBO.face>=6){UENV.uEnvP.value.copy(RCUBO.cc.position)}if(RCUBO.face>0||RCUBO.listo){UENV.uEnvC.value=RCUBO.rt.texture;UENV.uEnvOn.value=RCUBO.listo||RCUBO.face>=6?1:0}if(RCUBO.face>=6){RCUBO.listo=1;RCUBO.face=0;RCUBO.out="),
]
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'const UENV=' in s:print('ya estaba',f);continue
    for a,b in R:
        assert s.count(a)==1,(f,a[:60]);s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s);print('ok charcos',f)
