# Reflejos de verdad en la pintura y los cristales de los coches (las cinco páginas; va al final de la cadena).
# Antes, el barniz de los coches reflejaba solo un cielo dibujado (degradado con una franja oscura de «calle»),
# rehecho cada 4 s. Ahora, en el ordenador, una cámara de 6 caras pegada a tu vehículo fotografía la ciudad de
# verdad a su alrededor (fachadas, árboles, farolas, otros coches, el mar, el cielo de cada hora y, de noche,
# las ventanas y luces encendidas) y eso es lo que se ve en la carrocería, los cristales y los cromados.
#  - Cubo de 128 px en coma flotante (el sol y las luces conservan su brillo), 2 caras por imagen: una vuelta
#    completa cada 3 imágenes y luego se suaviza con PMREM para que el barniz y lo mate reflejen más borroso.
#  - Se repite cada 0,2 s con calidad alta (tecla G) y cada 0,6 s en modo rendimiento.
#  - Solo dibuja hasta ~6 u (unos 240 m) y sin sombras nuevas, para que salga barato; tu propio vehículo no se ve
#    en su reflejo, el recorte de árboles entre cámara y coche se desactiva y el cielo se centra en el cubo.
#  - En el móvil (LITE) sigue el reflejo del cielo cada 60 s de siempre. Si algo falla, vuelve al reflejo de cielo.
#  - Cristales de los vehículos oficiales como vidrio de verdad: oscuros de frente y espejo de lado (barniz, sin metal,
#    reflejo ×2,2), para que se vean las fachadas en el parabrisas (solo index e indexm, que son las que los llevan).
#  - Pintura algo más metálica y lisa (roughness .42→.26, metalness .25→.55, barniz .07→.03, reflejo ×1,3) para que se note.
import os
OLD_FN="function reflejosCoches(){if(!driving)return;const t=performance.now()/1000;if(t-ENVC.t<(window.LITE?60:4))return;ENVC.t=t;try{envCoches()}catch(e){console.warn(e)}}"
OLD_PINT="function pintura(col){const m=new THREE.MeshPhysicalMaterial({color:col,roughness:.42,metalness:.25,clearcoat:1,clearcoatRoughness:.07,envMapIntensity:1});"
NEW_PINT="function pintura(col){const m=new THREE.MeshPhysicalMaterial({color:col,roughness:.26,metalness:.55,clearcoat:1,clearcoatRoughness:.03,envMapIntensity:1.3});"
OLD_CRI="case 'cristal':{const m=std({color:0x1b2233,roughness:.06,metalness:.3,envMapIntensity:1.3})"
NEW_CRI="case 'cristal':{const m=new THREE.MeshPhysicalMaterial({color:0x0e121a,roughness:.03,metalness:0,clearcoat:1,clearcoatRoughness:0,envMapIntensity:2.2})"
NEW_FN=r'''// ---------- reflejos de verdad (edit_reflejos.py): un cubo pegado a tu vehículo fotografía la ciudad y eso refleja la pintura
const RCUBO={cc:null,rt:null,pm:null,out:null,face:0,t:-99,mal:false,far:6};window.__RCUBO=RCUBO;
function reflejoCaras(n){
 if(!RCUBO.cc){RCUBO.rt=new THREE.WebGLCubeRenderTarget(128,{type:THREE.HalfFloatType,generateMipmaps:false});
  RCUBO.cc=new THREE.CubeCamera(.004,RCUBO.far,RCUBO.rt);RCUBO.cc.coordinateSystem=R.coordinateSystem;RCUBO.cc.updateCoordinateSystem();RCUBO.pm=new THREE.PMREMGenerator(R)}
 const ob=n_=>{try{return n_()}catch(e){return null}};
 const vs=[ob(()=>car),ob(()=>moto),ob(()=>persona),ob(()=>heli)].filter(o=>o&&o.isObject3D);
 if(RCUBO.face===0){const vh=MODO==='moto'?vs[1]:MODO==='heli'?vs[3]:MODO==='pie'?vs[2]:car;const p=new THREE.Vector3();(vh&&vh.isObject3D?vh:car).getWorldPosition(p);
  RCUBO.cc.position.set(p.x,p.y+.025,p.z);RCUBO.cc.updateMatrixWorld(true)}
 const sh=R.shadowMap,au=sh.autoUpdate,nu=sh.needsUpdate,prev=R.getRenderTarget(),pf=R.getActiveCubeFace(),pl=R.getActiveMipmapLevel(),cut=UCUT.uCut.value,
  sp=sky.position.clone(),ss=sky.scale.clone(),sv=sky.visible,vis=vs.map(o=>o.visible);
 sh.autoUpdate=false;UCUT.uCut.value=0;sky.visible=true;sky.position.copy(RCUBO.cc.position);sky.scale.setScalar(RCUBO.far*.9);vs.forEach(o=>o.visible=false);
 try{for(let k=0;k<n&&RCUBO.face<6;k++){R.setRenderTarget(RCUBO.rt,RCUBO.face);R.render(scene,RCUBO.cc.children[RCUBO.face]);RCUBO.face++}}
 finally{vs.forEach((o,i)=>o.visible=vis[i]);sky.visible=sv;sky.position.copy(sp);sky.scale.copy(ss);UCUT.uCut.value=cut;sh.autoUpdate=au;sh.needsUpdate=nu;R.setRenderTarget(prev,pf,pl)}
 if(RCUBO.face>=6){RCUBO.face=0;RCUBO.out=RCUBO.pm.fromCubemap(RCUBO.rt.texture,RCUBO.out);const tex=RCUBO.out.texture;ENVC.tex=tex;
  for(const m of REFLEJAN){if(m.envMap!==tex){const nuevo=!m.envMap;m.envMap=tex;if(nuevo)m.needsUpdate=true}}return true}
 return false}
function reflejosCoches(){if(!driving){RCUBO.face=0;return}const t=performance.now()/1000;
 if(window.LITE||RCUBO.mal){if(t-ENVC.t<(window.LITE?60:4))return;ENVC.t=t;try{envCoches()}catch(e){console.warn(e)}return}
 if(!ENVC.tex){ENVC.t=t;try{envCoches()}catch(e){}}   // mientras se llena el primer cubo, el cielo de siempre
 if(RCUBO.face===0&&t-RCUBO.t<((typeof POST!=='undefined'&&POST.on)?.2:.6))return;
 try{if(reflejoCaras(2))RCUBO.t=t}catch(e){console.warn('reflejos',e);RCUBO.mal=true;RCUBO.face=0}}'''
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'const RCUBO={cc:null' in s:print('ya estaba',f);continue
    for a in (OLD_FN,OLD_PINT):assert s.count(a)==1,(f,a[:40])
    s=s.replace(OLD_FN,NEW_FN).replace(OLD_PINT,NEW_PINT)
    if s.count(OLD_CRI)==1:s=s.replace(OLD_CRI,NEW_CRI)
    open(f,'w',encoding='utf-8').write(s)
    print('ok reflejos',f)
