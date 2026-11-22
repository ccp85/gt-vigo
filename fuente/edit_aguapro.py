# Agua «pro»: el mar refleja de verdad la ciudad, los barcos, el puente de Rande y los montes (las cinco páginas;
# va al final de la cadena, después de edit_olas.py).
# Antes el agua solo reflejaba un degradado de cielo. Ahora, en el ordenador con calidad alta (tecla G):
#  - Reflejo plano de verdad, como un espejo: una segunda cámara, colocada como la imagen de la tuya bajo la
#    superficie, dibuja la escena del revés en una textura a media resolución (coma flotante, así el sol y las luces
#    de la noche conservan su brillo). Sin plano de corte oblicuo: con la vista casi rasante (barco, nadando) ese
#    truco acercaba el plano lejano y desaparecían los edificios del reflejo. Lo que hay bajo el agua casi no se ve
#    desde abajo (se dibuja solo por delante); los montes del fondo se cortan en el nivel del agua en su sombreado.
#  - El oleaje que ya tenía el agua deforma ese reflejo (se rompe con las olas y los rizos) y la espuma lo tapa.
#  - También se refleja el cielo de verdad, con sus nubes y el color de cada hora.
#  - Las láminas de dos caras (suelos, jardines, montes del fondo) se dibujan solo por delante en el reflejo: vistas
#    desde abajo tapaban los edificios con manchas verdes. Los montes del fondo (malla gruesa) empiezan en el
#    reflejo 12 u (1,2 km) más lejos: así no tapan la ciudad vista desde el agua ni enseñan su borde
#    escalonado; se siguen reflejando los montes del otro lado de la ría.
#  - De lado el agua refleja más (Fresnel hasta 0,74 en vez de 0,58), como la ría en un día de calma.
#  - Barato: solo al conducir/navegar/volar/nadar (no en la vista de maqueta), solo si hay agua cerca de lo que
#    miras, sin sombras nuevas y sin el propio mar. Altura del agua medida bajo la cámara cada segundo.
#  - En el móvil (LITE), en modo rendimiento y bajo el agua: el reflejo de cielo de siempre. Si algo falla, se apaga solo.
import os
JS = r'''// ---------- edit_aguapro.py: reflejo de verdad en el agua (espejo plano bajo la cámara)
const URF={uRf:{value:null},uRfOn:{value:0},uRfM:{value:new THREE.Matrix4()}};
const ARF={rt:null,cam:new THREE.PerspectiveCamera(),h:-.036,tH:-1e9,tL:-1e9,tV:-1e9,vis:false,L:[],mal:false,esc:.5,
 ds:[],rm:new THREE.Matrix4(),cw:new THREE.Vector3(),
 vw:new THREE.Vector3(),lk:new THREE.Vector3(),tg:new THREE.Vector3(),n:new THREE.Vector3(0,1,0),o:new THREE.Vector3(),
 rc:new THREE.Raycaster(),dn:new THREE.Vector3(0,-1,0),d:new THREE.Vector3(),cc:new THREE.Color()};window.__ARF=ARF;
// costa en un punto (0 = mar hondo … 255 = tierra), para pruebas desde la consola: __ARF.mar(x,z)
ARF.mar=(x,z)=>{const img=UCO.uCos.value.image,R4=UCO.uCoR.value;if(!img||!img.data)return -1;const u=(x-R4.x)/R4.z,v=(z-R4.y)/R4.w;if(u<0||v<0||u>1||v>1)return 0;return img.data[(Math.min(img.height-1,Math.floor(v*img.height))*img.width+Math.min(img.width-1,Math.floor(u*img.width)))*4]};
function aguaAltura(now){
 if(now-ARF.tL>5000){ARF.tL=now;const L=[],ds=new Set();scene.traverse(o=>{if(!o.isMesh)return;if(WATERS.includes(o.material)){if(o.name!=='olas_patos')L.push(o);return}
  for(const m of [].concat(o.material))if(m&&m.side===THREE.DoubleSide&&!m.isShaderMaterial)ds.add(m)});ARF.L=L;ARF.ds=[...ds]}
 if(now-ARF.tH<1000)return;ARF.tH=now;const d=ARF.d;pcam.getWorldDirection(d);d.y=0;if(d.lengthSq()<1e-6)d.set(0,0,-1);d.normalize();
 for(const k of [1.5,0,4,8]){ARF.o.set(pcam.position.x+d.x*k,6,pcam.position.z+d.z*k);ARF.rc.set(ARF.o,ARF.dn);ARF.rc.far=20;
  const h=ARF.rc.intersectObjects(ARF.L,false)[0];if(h){ARF.h=h.point.y;return}}}
// ¿hay agua cerca de lo que se mira? (textura de la costa: rojo < 0,97 es mar)
function aguaVista(now){if(now-ARF.tV<400)return ARF.vis;ARF.tV=now;
 const img=UCO.uCos.value.image;if(!img||!img.data||img.width<2){ARF.vis=true;return true}
 const W=img.width,H=img.height,D=img.data,R4=UCO.uCoR.value,d=ARF.d;pcam.getWorldDirection(d);d.y=0;if(d.lengthSq()<1e-6)d.set(0,0,-1);d.normalize();
 const cx=pcam.position.x+d.x*5,cz=pcam.position.z+d.z*5;let ok=false;
 for(let j=-4;j<=4&&!ok;j++)for(let i=-4;i<=4;i++){const x=cx+i*1.6,z=cz+j*1.6,u=(x-R4.x)/R4.z,v=(z-R4.y)/R4.w;
  if(u<0||v<0||u>1||v>1){ok=true;break}const k=(Math.min(H-1,Math.floor(v*H))*W+Math.min(W-1,Math.floor(u*W)))*4;if(D[k]<247){ok=true;break}}
 ARF.vis=ok;return ok}
function aguaReflejo(){URF.uRfOn.value=0;
 if(window.LITE||ARF.mal||!driving||!(typeof POST!=='undefined'&&POST.on)||window.__BAJO||!MAPA)return;
 const now=performance.now();pcam.updateMatrixWorld();aguaAltura(now);if(!aguaVista(now))return;
 const h=ARF.h,cam=pcam,vc=ARF.cam;if(cam.position.y<h+.0008)return;
 const cv_=R.domElement,w=Math.max(16,Math.round(cv_.width*ARF.esc)),hh=Math.max(16,Math.round(cv_.height*ARF.esc));
 if(!ARF.rt){ARF.rt=new THREE.WebGLRenderTarget(w,hh,{type:THREE.HalfFloatType});ARF.rt.texture.generateMipmaps=false;URF.uRf.value=ARF.rt.texture}
 else if(ARF.rt.width!==w||ARF.rt.height!==hh)ARF.rt.setSize(w,hh);
 // cámara reflejada (como THREE.Reflector, con plano horizontal a la altura del agua)
 const N=ARF.n,cw=ARF.cw.setFromMatrixPosition(cam.matrixWorld),P0=ARF.o.set(cw.x,h,cw.z);
 const vw=ARF.vw.subVectors(P0,cw).reflect(N).negate().add(P0);
 ARF.rm.extractRotation(cam.matrixWorld);const lk=ARF.lk.set(0,0,-1).applyMatrix4(ARF.rm).add(cw);
 const tg=ARF.tg.subVectors(P0,lk).reflect(N).negate().add(P0);
 vc.position.copy(vw);vc.up.set(0,1,0).applyMatrix4(ARF.rm).reflect(N);vc.lookAt(tg);
 vc.fov=cam.fov;vc.aspect=cam.aspect;vc.zoom=cam.zoom;vc.near=cam.near;vc.far=cam.far;
 vc.updateProjectionMatrix();vc.updateMatrixWorld();
 const M=URF.uRfM.value;M.set(.5,0,0,.5, 0,.5,0,.5, 0,0,.5,.5, 0,0,0,1);M.multiply(vc.projectionMatrix);M.multiply(vc.matrixWorldInverse);
 // dibujar sin el mar, con el cielo centrado en la cámara reflejada, sin sombras nuevas y sin el recorte de árboles;
 // las láminas de dos caras (suelos, jardines, montes del fondo) solo por delante: desde abajo no deben tapar los edificios
 const wv=WATERS.map(m=>m.visible),sv=sky.visible,sp=sky.position.clone(),ss=sky.scale.clone(),sh=R.shadowMap,au=sh.autoUpdate,nu=sh.needsUpdate,cut=UCUT.uCut.value,prev=R.getRenderTarget(),
  ca=R.getClearAlpha(),cc=R.getClearColor(ARF.cc),fm=(typeof FONDO!=='undefined'&&FONDO.mar)?FONDO.mar.visible:null,fu=(typeof FONDO!=='undefined')?FONDO.U.uCam.value.clone():null;
 try{for(const m of WATERS)m.visible=false;for(const m of ARF.ds)m.side=THREE.FrontSide;sky.visible=true;sky.position.copy(vc.position);sky.scale.setScalar(vc.far*.9);sky.updateMatrixWorld();if(fm!==null)FONDO.mar.visible=false;if(fu){FONDO.U.uCam.value.copy(vc.position);FONDO.U.uCorte.value=h;FONDO.U.uNear.value+=12}
  sh.autoUpdate=false;UCUT.uCut.value=0;R.setClearColor(0x000000,0);R.setRenderTarget(ARF.rt);R.clear();R.render(scene,vc)}
 finally{WATERS.forEach((m,i)=>m.visible=wv[i]);for(const m of ARF.ds)m.side=THREE.DoubleSide;sky.visible=sv;sky.position.copy(sp);sky.scale.copy(ss);sky.updateMatrixWorld();if(fm!==null)FONDO.mar.visible=fm;if(fu){FONDO.U.uCam.value.copy(fu);FONDO.U.uCorte.value=-99;FONDO.U.uNear.value-=12}
  sh.autoUpdate=au;sh.needsUpdate=nu;UCUT.uCut.value=cut;R.setClearColor(cc,ca);R.setRenderTarget(prev)}
 URF.uRfOn.value=1}
'''
# (anterior, nuevo) dentro de aguaSamil()
SH = [
    ("Object.assign(sh.uniforms,UW,UCO,USURF,", "Object.assign(sh.uniforms,UW,UCO,USURF,URF,"),
    ("sh.vertexShader='varying vec3 vWp;\\n'", "sh.vertexShader='varying vec3 vWp;uniform mat4 uRfM;varying vec4 vRfUv;\\n'"),
    ("vWp=(modelMatrix*vec4(position,1.0)).xyz;');", "vWp=(modelMatrix*vec4(position,1.0)).xyz;vRfUv=uRfM*vec4(vWp,1.0);');"),
    ("varying vec3 vWp;vec3 aN;float aF;", "varying vec3 vWp;uniform sampler2D uRf;uniform float uRfOn;varying vec4 vRfUv;vec3 aN;float aF;"),
    (",.58)*(1.-max(aF,aS));", ",mix(.58,.74,uRfOn))*(1.-max(aF,aS));"),
    ("outgoingLight=mix(outgoingLight,sky,F);",
     "vec3 rfl=sky;if(uRfOn>.5){vec2 ru=clamp(vRfUv.xy/vRfUv.w+N.xz*.06,.001,.999);vec4 rc=texture2D(uRf,ru);rfl=mix(sky,rc.rgb*.92,clamp(rc.a,0.,1.));}   // edit_aguapro.py: reflejo de verdad\n"
     "   outgoingLight=mix(outgoingLight,rfl,F);"),
]
FONDO_R = [
    ("uNear:{value:20},", "uNear:{value:20},uCorte:{value:-99},", 1),
    ("uniform float uNear,uNight;", "uniform float uNear,uNight,uCorte;", 1),
    ("float d=distance(vW.xz,uCam.xz);if(d<uNear)discard;", "float d=distance(vW.xz,uCam.xz);if(d<uNear||vW.y<uCorte)discard;", 2),
]
LOOP = [
    ("sombrasTick();if(COMIC.on)comicRender();",
     "try{aguaReflejo()}catch(e){ARF.mal=true;URF.uRfOn.value=0;console.warn('reflejo agua',e)}sombrasTick();if(COMIC.on)comicRender();"),
    ("if(!driving){ctl.update();R.render(scene,cam)}", "if(!driving){URF.uRfOn.value=0;ctl.update();R.render(scene,cam)}"),
]
for f in ['index.html', 'indexm.html', 'gp.html', 'nav.html', 'navm.html']:
    if not os.path.exists(f): continue
    s = open(f, encoding='utf-8').read()
    if 'const URF={uRf:' in s: print('ya estaba', f); continue
    a = s.find('function aguaSamil(m){'); b = s.find('\nfunction texturaCosta()', a)
    assert a > 0 and b > a and s.count('function aguaSamil(m){') == 1, (f, a, b)
    fn = s[a:b]
    for x, y in SH:
        assert fn.count(x) == 1, (f, x[:50]); fn = fn.replace(x, y)
    s = s[:a] + JS + fn + s[b:]
    for x, y, n in FONDO_R:
        assert s.count(x) == n, (f, x[:50]); s = s.replace(x, y)
    for x, y in LOOP:
        assert s.count(x) == 1, (f, x[:50]); s = s.replace(x, y)
    open(f, 'w', encoding='utf-8').write(s); print('ok aguapro', f)
