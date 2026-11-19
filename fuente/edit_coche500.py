f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= COCHE PRINCIPAL NUEVO (modelo aportado por el usuario, Tripo: coche500.glb) =================
# Solo mundo abierto (index.html): se aplica DESPUÉS de edit_skatetest.py, así nav/navm/gp no cambian.
# coche500.glb viene de herramientas/coche2glb.py: reducido a ~30k triángulos, frente a +X, ruedas en y=0, largo .165
# (el mismo que el utilitario granate procedural). Al cargar sustituye la carrocería de CAR0 (el coche "clasico");
# se conservan la mancha de sombra, el haz de los faros y los faros/pilotos (recolocados sobre los del modelo).
# Mientras carga (o si falla) se ve el coche antiguo.
r("const CAR0=car.clone(true);CAR0.userData={tipo:'clasico'};\n",
  "const CAR0=car.clone(true);CAR0.userData={tipo:'clasico'};\n"
  "new GLTFLoader().load('coche500.glb',gl=>{let src=null;gl.scene.traverse(o=>{if(o.isMesh&&!src)src=o});if(!src)return;const q=src.material;\n"
  " const m=new THREE.MeshPhysicalMaterial({map:q.map,normalMap:q.normalMap,normalScale:q.normalScale.clone(),roughnessMap:q.roughnessMap,metalnessMap:q.metalnessMap,roughness:1,metalness:.6,clearcoat:.7,clearcoatRoughness:.12,envMapIntensity:1});\n"
  " m.userData.pintura=1;REFLEJAN.add(m);if(ENVC.tex)m.envMap=ENVC.tex;\n"
  " const mod=new THREE.Mesh(src.geometry,m);mod.name='modelo';mod.castShadow=true;\n"
  " const GF=new THREE.CylinderGeometry(.0055,.0055,.004,14),GP=new THREE.BoxGeometry(.004,.012,.006);\n"
  " for(const c of [...CAR0.children]){const fa=c.isMesh&&c.material&&c.material.userData&&c.material.userData.faro;\n"
  "  if(fa==='f'){const sz=Math.sign(c.position.z);c.geometry=GF;c.position.set(.0705,.032,sz*.0245);c.rotation.set(0,-sz*.3,Math.PI/2,'YXZ')}\n"
  "  else if(fa==='p'){const sz=Math.sign(c.position.z);c.geometry=GP;c.position.set(-.0715,.04,sz*.027);c.rotation.set(0,sz*.45,0)}\n"
  "  else if(!(c.isMesh&&(c.name==='sombra'||c.name==='haz')))CAR0.remove(c)}\n"
  " CAR0.add(mod);CAR0.userData.modelo500=true;\n"
  " try{const sp=COCHES.find(c=>c.t==='clasico');if(sp){sp.col=[0xb3202a];sp.n='Cinquecento'}}catch(e){}\n"
  " if(!P.vestidoMoto&&(car.userData.tipo===undefined||car.userData.tipo==='clasico'))vestirCoche(CAR0,'clasico')},undefined,e=>console.warn('coche500.glb',e));\n")
open(f,'w').write(s)
print('ok coche500')
