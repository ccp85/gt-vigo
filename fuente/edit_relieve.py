f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= VENTANAS CON PROFUNDIDAD (adiós al "papel pintado") =================
# Las ventanas de las fachadas eran un dibujo plano. Ahora cada hueco está hundido en el muro unos 35 cm:
# al mirar en ángulo se ve el derrame de piedra (jambas, dintel y alféizar) y el cristal se desplaza hacia dentro
# con su sombra en los bordes, como en un edificio de verdad. Se calcula en el sombreado de la fachada
# (relieve por paralaje), así que no añade piezas. En móvil (LITE) no se aplica.
# Huecos de la textura de fachada (celda de 128 x 192): ventana con su marco x 26..102, y 34..146 (desde arriba);
# balcón x 30..98, y 22..162; las galerías ('b', variante 3) ya sobresalen y no se hunden.
r("vec4 sampledDiffuseColor=textureGrad(map,at,dx,dy);\n    bool tej=false;",
  "vec4 sampledDiffuseColor=textureGrad(map,at,dx,dy);\n    ${window.LITE?'':`"
  "if(fl>.5&&!(var_>2.5&&"+"${k==='b'?'true':'false'}"+")){vec4 Rw=var_>.5&&var_<1.5?vec4(.234,.156,.766,.885):vec4(.203,.24,.797,.823);"
  "if(cu.x>Rw.x&&cu.x<Rw.z&&cu.y>Rw.y&&cu.y<Rw.w){vec3 dpx=dFdx(vWF),dpy=dFdy(vWF);vec2 d1=vec2(dFdx(uvF.x),dFdx(pl)),d2=vec2(dFdy(uvF.x),dFdy(pl));"
  "vec3 Nn=normalize(cross(dpx,dpy));vec3 Vw=normalize(vWF-cameraPosition);if(dot(Nn,Vw)>0.)Nn=-Nn;"
  "vec3 q2=cross(dpy,Nn),q1=cross(Nn,dpx);vec3 Tt=q2*d1.x+q1*d2.x,Bt=q2*d1.y+q1*d2.y;"
  "if(dot(Tt,Tt)>1e-20&&dot(Bt,Bt)>1e-20){Tt=normalize(Tt);Bt=normalize(Bt);float vz=max(-dot(Vw,Nn),.12);"
  "vec2 c2=cu+vec2(dot(Vw,Tt),dot(Vw,Bt))/vz*vec2(.0055/.05,.0055/.075);"
  "if(c2.x<Rw.x||c2.x>Rw.z)sampledDiffuseColor=vec4(vec3(.58),1.);else if(c2.y>Rw.w)sampledDiffuseColor=vec4(vec3(.42),1.);else if(c2.y<Rw.y)sampledDiffuseColor=vec4(vec3(.8),1.);"
  "else{sampledDiffuseColor=textureGrad(map,vec2((var_+c2.x)/4.,(fila+c2.y)/2.),dx,dy);float ed=min(min(c2.x-Rw.x,Rw.z-c2.x)*.05,min(c2.y-Rw.y,Rw.w-c2.y)*.075);"
  "sampledDiffuseColor.rgb*=mix(.5,1.,smoothstep(0.,.0035,ed))*mix(.62,1.,smoothstep(0.,.006,(Rw.w-c2.y)*.075));}}}}"
  "`}\n    bool tej=false;")
# El resto de fachadas (bloques de ventanas corridas, etc.) usan otra textura sin huecos fijos: ahí el hueco se detecta por el color
# (cristal oscuro o azulado) y se hace lo mismo: se mira la textura desplazada hacia dentro del muro y, si cae en pared, se pinta el derrame en sombra.
r("float win=1.-smoothstep(.30,.42,dot(sampledDiffuseColor.rgb,vec3(.333)));",
  "float win=1.-smoothstep(.30,.42,dot(sampledDiffuseColor.rgb,vec3(.333)));\n    ${window.LITE?'':`"
  "float wr=max(win,step(dot(sampledDiffuseColor.rgb,vec3(.333)),.74)*step(.04,sampledDiffuseColor.b-sampledDiffuseColor.r));if(wr>.5){vec3 dpx=dFdx(vWF),dpy=dFdy(vWF);vec2 u1=dFdx(vMapUv),u2=dFdy(vMapUv);vec3 Nn=normalize(cross(dpx,dpy));vec3 Vw=normalize(vWF-cameraPosition);if(dot(Nn,Vw)>0.)Nn=-Nn;"
  "float vz=max(-dot(Vw,Nn),.12);vec3 sv=(Vw+Nn*vz)/vz*.0045;float g11=dot(dpx,dpx),g12=dot(dpx,dpy),g22=dot(dpy,dpy),det=g11*g22-g12*g12;"
  "if(abs(det)>1e-24){float r1=dot(dpx,sv),r2=dot(dpy,sv);float ca=(r1*g22-r2*g12)/det,cb=(r2*g11-r1*g12)/det;vec2 duv=ca*u1+cb*u2;"
  "vec4 s2=texture2D(map,vMapUv+duv);float w2=max(1.-smoothstep(.30,.42,dot(s2.rgb,vec3(.333))),step(dot(s2.rgb,vec3(.333)),.74)*step(.04,s2.b-s2.r));vec3 bas=diffuseColor.rgb/max(sampledDiffuseColor.rgb,vec3(.03));"
  "diffuseColor.rgb=w2<.5?bas*s2.rgb*.5:bas*s2.rgb*.9;}}"
  "`}")
open(f,'w').write(s)
print('ok relieve')
