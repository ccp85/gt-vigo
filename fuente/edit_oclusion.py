# Oclusión ambiental (las cinco páginas; va al final de la cadena).
# En «calidad alta» (posprocesado activo, tecla G), oscurece suavemente rincones, juntas, bajos de coches,
# pies de fachada, bancos y farolas: lo que no recibe la luz del cielo. Así las piezas se «asientan» en el suelo.
#  - Lee la profundidad del mismo dibujo de la escena (no vuelve a dibujarla): al objetivo del posprocesado
#    se le añade una textura de profundidad, y como el buffer es logarítmico se pasa a distancia real igual
#    que en el estilo cómic.
#  - Calcula la oclusión a media resolución con 12 muestras en espiral (radio ≈ 0,08 u, unos 3 m) y la
#    normal sacada de la propia profundidad; luego la suaviza respetando los bordes (4x4 según profundidad).
#  - Se desvanece a lo lejos (desde ~5 u) y no toca las luces (faros, ventanas, neones), que no deben ensuciarse.
#  - Va justo después del dibujo de la escena y antes del brillo (bloom), así que también la respeta el color
#    de cada hora. En el móvil (LITE) no se usa porque el posprocesado está apagado.
import os
D=os.path.dirname(os.path.abspath(__file__))
OLD_RT="const rt=new THREE.WebGLRenderTarget(2,2,{type:THREE.HalfFloatType,samples:2});"
NEW_RT="const rt=new THREE.WebGLRenderTarget(2,2,{type:THREE.HalfFloatType,samples:2,depthTexture:new THREE.DepthTexture(2,2)});"
OLD_RP="const c=new EffectComposer(R,rt);c.addPass(new RenderPass(scene,pcam));"
NEW_RP="const c=new EffectComposer(R,rt);c.addPass(new RenderPass(scene,pcam));try{POST.ao=aoPass();c.addPass(POST.ao)}catch(e){console.error(e)}"
ANCLA="function postInit(){"
AO=r'''// ---------- oclusión ambiental (rincones, juntas y bajos más oscuros) con la profundidad del propio dibujo
function aoPass(){const fq=new THREE.Mesh(new THREE.PlaneGeometry(2,2));fq.frustumCulled=false;const qs=new THREE.Scene();qs.add(fq);const qc=new THREE.OrthographicCamera(-1,1,1,-1,0,1);
 const art=new THREE.WebGLRenderTarget(2,2,{depthBuffer:false});
 const VS='varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}';
 const DEP=`uniform sampler2D tD;uniform float uFar;uniform vec2 uP;
  float W(vec2 uv){return exp2(texture2D(tD,uv).x*log2(uFar+1.))-1.;}                 // distancia real (buffer logarítmico)
  vec3 VP(vec2 uv){float w=W(uv);vec2 n=uv*2.-1.;return vec3(n.x*w/uP.x,n.y*w/uP.y,-w);}`;
 const mA=new THREE.ShaderMaterial({uniforms:{tD:{value:null},uFar:{value:120},uP:{value:new THREE.Vector2(1,1)},uRes:{value:new THREE.Vector2(1,1)},uR:{value:.08},uMax:{value:9}},depthTest:false,depthWrite:false,vertexShader:VS,
  fragmentShader:DEP+`uniform vec2 uRes;uniform float uR,uMax;varying vec2 vUv;
   void main(){if(texture2D(tD,vUv).x>.99995){gl_FragColor=vec4(1.);return;}
    vec3 p=VP(vUv);float w=-p.z;if(w>uMax){gl_FragColor=vec4(1.);return;}
    vec2 px=1./uRes;vec3 a=VP(vUv+vec2(px.x,0.)),b=VP(vUv-vec2(px.x,0.)),c=VP(vUv+vec2(0.,px.y)),e=VP(vUv-vec2(0.,px.y));
    vec3 dx=abs(a.z-p.z)<abs(p.z-b.z)?a-p:p-b,dy=abs(c.z-p.z)<abs(p.z-e.z)?c-p:p-e;vec3 n=normalize(cross(dx,dy));
    float rp=min(uR*uP.y/w*.5*uRes.y,40.);if(rp<1.5){gl_FragColor=vec4(1.);return;}
    float ang=6.2832*fract(52.9829189*fract(dot(gl_FragCoord.xy,vec2(.06711056,.00583715))));
    float o=0.;for(int i=0;i<12;i++){float t=(float(i)+.5)/12.,an=ang+float(i)*2.39996;
     vec3 v=VP(vUv+vec2(cos(an),sin(an))*t*rp*px)-p;float L=length(v);
     o+=max(0.,dot(n,v)/(L+1e-5)-.2)*(1.-smoothstep(uR*.6,uR*1.6,L));}
    o=1.-clamp(o/12.*2.6,0.,1.);gl_FragColor=vec4(vec3(mix(1.,o,1.-smoothstep(uMax*.55,uMax,w))),1.);}`});
 const mC=new THREE.ShaderMaterial({uniforms:{tDiffuse:{value:null},tAO:{value:null},tD:{value:null},uFar:{value:120},uP:{value:new THREE.Vector2(1,1)},uRes:{value:new THREE.Vector2(1,1)},uStr:{value:.9}},depthTest:false,depthWrite:false,vertexShader:VS,
  fragmentShader:DEP+`uniform sampler2D tDiffuse,tAO;uniform vec2 uRes;uniform float uStr;varying vec2 vUv;
   void main(){vec4 c=texture2D(tDiffuse,vUv);float w0=W(vUv),s=0.,ws=0.;vec2 px=1./uRes;
    for(int y=0;y<4;y++)for(int x=0;x<4;x++){vec2 uv=vUv+(vec2(x,y)-1.5)*px;float k=exp(-abs(W(uv)-w0)/max(w0*.03,1e-3));s+=texture2D(tAO,uv).r*k;ws+=k;}
    float ao=ws>1e-4?s/ws:1.,l=dot(c.rgb,vec3(.2126,.7152,.0722));
    c.rgb*=mix(1.,ao,uStr*(1.-smoothstep(.9,2.5,l)));gl_FragColor=c;}`});
 return{enabled:true,needsSwap:true,clear:false,renderToScreen:false,art,mA,mC,
  setSize(w,h){art.setSize(Math.max(1,w>>1),Math.max(1,h>>1))},
  dispose(){art.dispose();mA.dispose();mC.dispose();fq.geometry.dispose()},
  render(r,wb,rb){const dt=rb.depthTexture,pe=pcam.projectionMatrix.elements;
   for(const m of[mA,mC]){const u=m.uniforms;u.tD.value=dt;u.uFar.value=pcam.far;u.uP.value.set(pe[0],pe[5]);u.uRes.value.set(art.width,art.height)}
   if(dt){fq.material=mA;r.setRenderTarget(art);r.render(qs,qc)}
   mC.uniforms.tDiffuse.value=rb.texture;mC.uniforms.tAO.value=art.texture;mC.uniforms.uStr.value=dt?.9:0;
   fq.material=mC;r.setRenderTarget(this.renderToScreen?null:wb);r.render(qs,qc)}}}
'''
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'function aoPass(){' in s:print('ya estaba',f);continue
    for a in (OLD_RT,OLD_RP,ANCLA):assert s.count(a)==1,(f,a[:40])
    s=s.replace(OLD_RT,NEW_RT).replace(OLD_RP,NEW_RP).replace(ANCLA,AO+ANCLA)
    open(f,'w',encoding='utf-8').write(s)
    print('ok oclusion',f)
