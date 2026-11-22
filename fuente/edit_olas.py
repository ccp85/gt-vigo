import os
# ================= OLAS EN LA PLAYA DE PATOS (rompientes) =================
# Patos (Nigrán) es playa abierta al océano: ahora entran series de olas hacia la arena.
#  - Cada ola sigue la forma de la costa (las crestas van paralelas a la orilla) y avanza hacia la arena:
#    crece al acercarse, se empina con la cara verde transparente hacia la playa, rompe con el labio blanco
#    y sigue como espuma (la «escuma») hasta morir en la orilla. Vienen en series (unas más grandes que otras)
#    y no rompen todas a la vez a lo largo de la playa.
#  - En el ordenador las olas tienen relieve de verdad: una malla fina solo sobre la franja de rompiente de Patos
#    (unas 66.000 celdas) que sube y baja con la misma fórmula que el sombreado del agua. Solo se dibuja cerca.
#  - Las crestas siguen una distancia a la costa suavizada (canal alfa de la textura de la costa, antes sin usar),
#    para que no salgan escalones ni zigzags por los píxeles del mapa.
#  - En el móvil (LITE) no hay malla: las olas se ven por el brillo/sombreado y la espuma (sin coste de geometría).
#  - Sitios con olas en SURF.spots ([x, z, radio, fuerza]); hay hueco para 3. Para poner olas en otra playa
#    abierta basta con añadir su punto (las coordenadas son las del mapa del juego).
# Las cinco páginas.
SURF_JS = r"""// edit_olas.py: rompientes en playas abiertas al océano (Patos). Sitios: [x, z, radio, fuerza]
const SURF={spots:[[-25,127,12,1]],m:null,pt:null,yOk:false,t:0};
const USURF={uSurf:{value:[0,1,2].map(i=>{const s=SURF.spots[i];return s?new THREE.Vector4(s[0],s[1],s[2],s[3]):new THREE.Vector4(0,0,1,0)})},uSurfA:{value:.028}};
const SURF_GLSL=`uniform vec4 uSurf[3];uniform float uSurfA;
float sh21(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float svn(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(sh21(i),sh21(i+vec2(1,0)),f.x),mix(sh21(i+vec2(0,1)),sh21(i+vec2(1,1)),f.x),f.y);}
float surfMask(vec2 p){float m=0.;for(int i=0;i<3;i++){vec4 s=uSurf[i];if(s.w>0.)m=max(m,s.w*(1.-smoothstep(s.z*.55,s.z,length(p-s.xy))));}return m;}
float surfCos(vec2 w){vec2 uv=(w-uCoR.xy)/uCoR.zw;if(uv.x<0.||uv.y<0.||uv.x>1.||uv.y>1.)return 0.;return texture2D(uCos,uv).a;}
// x = altura (0..1), y = espuma, z = cara empinada de la ola (antes de romper)
vec3 surf(vec2 p,float cs,float t){
 float n=svn(p*.55),n2=svn(p*1.7+3.);
 float q=cs/.15-t/9.+n*1.6;float f=fract(q);                       // f: 0 = cresta, sube mar adentro
 float set=.55+.45*sin(q*.83+n2*2.);                                 // series: unas olas más grandes que otras
 float br=smoothstep(.58,.72,cs+(n2-.5)*.14);                         // ya rompió
 float env=smoothstep(.16,.6,cs)*(1.-.55*br)*(1.-smoothstep(.88,.975,cs))*set;
 float fr=1.-smoothstep(0.,.07,f);                                  // cara hacia la playa
 float h=max(f*f*f,fr)*env;
 float lip=smoothstep(.48,.64,cs+(n-.5)*.1)*(smoothstep(.9,1.,f)+1.-smoothstep(0.,.035,f))*min(env*1.6,1.);
 float ww=br*(smoothstep(.35,.97,f)*.85+fr)*(1.-smoothstep(.93,.985,cs))*(.5+.5*set);
 return vec3(h,clamp(lip*1.4+ww,0.,1.),clamp(fr*(1.-br)*env*1.5,0.,1.)-.35*(1.-h)*env*(1.-br));}
`;
function surfMesh(){if(SURF.m||window.LITE||!MAPA)return;const img=UCO.uCos.value.image;if(!img||img.width<2||!img.data)return;
 const W=img.width,H=img.height,d=img.data,R4=UCO.uCoR.value;
 const csAt=(x,z)=>{const i=Math.max(0,Math.min(W-1,Math.round((x-R4.x)/R4.z*W-.5))),j=Math.max(0,Math.min(H-1,Math.round((z-R4.y)/R4.w*H-.5)));return d[(j*W+i)*4]/255};
 const st=.035,pos=[],idx=[],csR=(x,z)=>{const i=Math.max(0,Math.min(W-1,Math.round((x-R4.x)/R4.z*W-.5))),j=Math.max(0,Math.min(H-1,Math.round((z-R4.y)/R4.w*H-.5))),k=(j*W+i)*4;return d[k]>=250?1:d[k+3]/255};
 SURF.spots.forEach(([cx,cz,R],si)=>{const n=Math.ceil(2*R/st),map=new Map();
  const id=(i,j)=>{const k=i*100000+j;let v=map.get(k);if(v===undefined){v=pos.length/3;pos.push(cx-R+i*st,0,cz-R+j*st);map.set(k,v)}return v};
  for(let j=0;j<n;j++)for(let i=0;i<n;i++){const x=cx-R+(i+.5)*st,z=cz-R+(j+.5)*st;if((x-cx)**2+(z-cz)**2>R*R)continue;const c=csR(x,z);if(c<.12||c>.99)continue;
   if(!SURF.pt&&c>.3&&c<.4)SURF.pt=[x,z];const a=id(i,j),b=id(i+1,j),c2=id(i+1,j+1),e=id(i,j+1);idx.push(a,e,b,b,e,c2)}});
 if(!idx.length)return;
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(new Float32Array(pos),3));g.setIndex(new THREE.BufferAttribute(new Uint32Array(idx),1));{const nr=new Float32Array(pos.length);for(let i=1;i<nr.length;i+=3)nr[i]=1;g.setAttribute('normal',new THREE.BufferAttribute(nr,3))}g.computeBoundingSphere();g.boundingSphere.radius+=.05;
 const m=new THREE.MeshStandardMaterial({color:0x2a3f9a});aguaSamil(m);const prev=m.onBeforeCompile;
 m.onBeforeCompile=(sh,r)=>{prev(sh,r);
  sh.vertexShader='uniform sampler2D uCos;uniform vec4 uCoR;uniform float uT;\n'+SURF_GLSL+sh.vertexShader.replace('vWp=(modelMatrix*vec4(position,1.0)).xyz;',
   'vWp=(modelMatrix*vec4(position,1.0)).xyz;{float sc=surfCos(vWp.xz);transformed.y+=surf(vWp.xz,sc,uT).x*uSurfA*surfMask(vWp.xz)*(1.-smoothstep(.97,.995,sc));}');
  sh.fragmentShader=sh.fragmentShader.replace('vec2 p=vWp.xz;float cs=costa();','vec2 p=vWp.xz;float cs=costa();if(cs>.985)discard;')};
 m.customProgramCacheKey=()=>'surfolas';m.polygonOffset=true;m.polygonOffsetFactor=-2;m.polygonOffsetUnits=-2;WATERS.push(m);
 const me=new THREE.Mesh(g,m);me.name='olas_patos';me.frustumCulled=true;me.receiveShadow=false;me.castShadow=false;me.position.y=(MARG?MARG.position.y:-.036)+.0015;me.visible=false;scene.add(me);SURF.m=me}
function surfTick(){if(window.LITE||!MAPA)return;const now=performance.now();if(now-SURF.t<1000)return;SURF.t=now;if(!SURF.m){surfMesh();if(!SURF.m)return}
 const fx=driving?P.x:(typeof ctl!=='undefined'?ctl.target.x:P.x),fz=driving?P.y:(typeof ctl!=='undefined'?ctl.target.z:P.y);
 const[cx,cz,R]=SURF.spots[0];const cerca=Math.hypot(fx-cx,fz-cz)<R+40;SURF.m.visible=cerca&&!window.__BAJO;
 if(cerca&&!SURF.yOk&&SURF.pt){const L=[];scene.traverse(o=>{if(o.isMesh&&o!==SURF.m&&o!==MARG&&WATERS.includes(o.material))L.push(o)});
  const rc=new THREE.Raycaster(new THREE.Vector3(SURF.pt[0],3,SURF.pt[1]),new THREE.Vector3(0,-1,0),0,10);const h=L.length?rc.intersectObjects(L,false)[0]:null;
  if(h){SURF.m.position.y=Math.max(h.point.y,MARG?MARG.position.y:-9)+.0015;SURF.yOk=true}}}
"""
R = [
    # distancia a la costa suavizada en el canal alfa (para las crestas de las olas)
    ("px[n*4+1]=Math.round(255*a);px[n*4+3]=255}",
     "px[n*4+1]=Math.round(255*a);px[n*4+3]=255}\n"
     " {const S=new Float32Array(w*h),T=new Float32Array(w*h),r=2;for(let n=0;n<w*h;n++)S[n]=land[n]?0:Math.min(D[n],16);   // edit_olas.py: costa suave (alfa)\n"
     "  for(let it=0;it<3;it++){for(let j=0;j<h;j++)for(let i=0;i<w;i++){let m=0,c=0;for(let d=-r;d<=r;d++){const ii=i+d;if(ii>=0&&ii<w){m+=S[j*w+ii];c++}}T[j*w+i]=m/c}\n"
     "   for(let j=0;j<h;j++)for(let i=0;i<w;i++){let m=0,c=0;for(let d=-r;d<=r;d++){const jj=j+d;if(jj>=0&&jj<h){m+=T[jj*w+i];c++}}S[j*w+i]=m/c}}\n"
     "  for(let n=0;n<w*h;n++)px[n*4+3]=land[n]?255:Math.round(Math.max(0,255*(1-S[n]/14)))}"),
    # datos de las olas antes del agua
    ("function aguaSamil(m){", SURF_JS + "function aguaSamil(m){"),
    # uniformes
    ("Object.assign(sh.uniforms,UW,UCO,{uSun:SKYU.uSun,uZen:SKYU.uZen,uHor:SKYU.uHor});",
     "Object.assign(sh.uniforms,UW,UCO,USURF,{uSun:SKYU.uSun,uZen:SKYU.uZen,uHor:SKYU.uHor});"),
    # funciones en el sombreado del agua
    ("varying vec3 vWp;vec3 aN;float aF;\\n'+",
     "varying vec3 vWp;vec3 aN;float aF;float aS;\\n'+SURF_GLSL+"),
    # relieve (normales) y espuma de la rompiente
    ("vec3 O=olas(p,uT,fw,calma,aw);vec2 gr=O.yz;",
     "vec3 O=olas(p,uT,fw,calma,aw);vec2 gr=O.yz;\n"
     "  aS=0.;float sFace=0.;{float sm=surfMask(p)*aw*(1.-smoothstep(.97,.995,cs));if(sm>.002){float e=.025;vec3 S0=surf(p,surfCos(p),uT);   // edit_olas.py: rompiente\n"
     "   float hx=surf(p+vec2(e,0.),surfCos(p+vec2(e,0.)),uT).x,hz=surf(p+vec2(0.,e),surfCos(p+vec2(0.,e)),uT).x;\n"
     "   gr+=vec2(hx-S0.x,hz-S0.x)/e*uSurfA*sm;aS=S0.y*sm;sFace=S0.z*sm;}}"),
    ("col+=vec3(.0,.018,.016)*smoothstep(.6,.95,O.x)*(1.-uN);",
     "col+=vec3(.0,.018,.016)*smoothstep(.6,.95,O.x)*(1.-uN);\n  col=mix(col,vec3(.03,.27,.24),max(sFace,0.)*.75*(1.-uN*.7));col*=1.+min(sFace,0.)*.9;   // la luz atraviesa la cara de la ola; valles más oscuros"),
    ("aF=clamp(foam+whc*tx,0.,1.);",
     "aF=clamp(foam+whc*tx,0.,1.);aS=clamp(aS*(.45+.8*tx),0.,1.);col=mix(col,vec3(.88,.91,.93),aS*(1.0-uN*.6));"),
    (".58)*(1.-aF);", ".58)*(1.-max(aF,aS));"),
    ("*up*(1.-aF);}", "*up*(1.-max(aF,aS));}"),
    # se crea y se coloca sola cerca de Patos
    ("const t=clock.elapsedTime;UW.uT.value=t;",
     "const t=clock.elapsedTime;UW.uT.value=t;try{surfTick()}catch(e){if(!window.__surfErr){window.__surfErr=1;console.error(e)}}"),
]
for f in ['index.html', 'indexm.html', 'gp.html', 'nav.html', 'navm.html']:
    if not os.path.exists(f): continue
    s = open(f, encoding='utf-8').read()
    if 'function surfTick(' in s: print('ya estaba', f); continue
    for a, b in R:
        assert s.count(a) == 1, (f, s.count(a), a[:60])
        s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print('ok olas', f)
