# Ría GT 300 (el coche rojo de siempre) con mucho más detalle por fuera y por dentro, y manos al volante en la vista interior.
#  - oficiales.js: coche() nuevo (riagt.js): carrocería por secciones, cabina de cristal tintado que deja ver el interior
#    (salpicadero, volante, asientos baquet y el conductor con sudadera roja), pasos de rueda, llantas de cinco radios con
#    pinzas, faros, luz trasera de lado a lado, difusor con cuatro escapes, alerón, retrovisores, rejillas y antena.
#  - juego: el cristal respeta la opacidad; las piezas de cada vehículo oficial se juntan por material (muchas menos
#    llamadas de dibujo aunque el coche tenga más piezas) y el coche lleva al conductor.
#  - cabina.js: manos agarradas al volante que giran con él y antebrazos con la manga roja; el ojo del conductor se calcula
#    con las medidas de cada coche; en el Ría GT la tapicería del salpicadero es naranja.
# Toca las siete páginas; va después de edit_cabina.py.
import sys,os,re
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','webgl.html','gpu.html'] if os.path.exists(f)]
OF=open(os.path.join(D,'oficiales.js'),encoding='utf8').read()
CAB=open(os.path.join(D,'cabina.js'),encoding='utf8').read()
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function cabMedidas(' in s:print('ya estaba',f);continue
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    m=re.search(r'(<script id="gtvOficiales">\n)(.*?)(</script>)',s,re.S);assert m,f
    s=s[:m.start(2)]+OF+s[m.end(2):]
    a=s.find('// ---------- vista interior del coche (edit_cabina.py)');b=s.find('\nfunction camCambia(')
    assert 0<a<b,f
    s=s[:a]+CAB.rstrip('\n')+s[b:]
    if 'const OFJ=(()=>{' in s:
        r("case 'cristal':{const m=new THREE.MeshPhysicalMaterial({color:0x0e121a,roughness:.03,metalness:0,clearcoat:1,clearcoatRoughness:0,envMapIntensity:2.2});REFLEJAN.add(m);return m}",
          "case 'cristal':{const m=new THREE.MeshPhysicalMaterial({color:0x0e121a,roughness:.03,metalness:0,clearcoat:1,clearcoatRoughness:0,envMapIntensity:2.2});if(o.opacity<1){m.transparent=true;m.opacity=o.opacity;m.depthWrite=false}REFLEJAN.add(m);return m}")
        r("""  g.traverse(o=>{if(!o.isMesh)return;const geo=o.geometry.clone().applyMatrix4(new THREE.Matrix4().multiplyMatrices(S,o.matrixWorld));
   const m=new THREE.Mesh(geo,o.material);m.name=o.name;m.castShadow=true;out.add(m)});""",
"""  // se juntan las piezas que comparten material: una malla por material
  const L=new Map();g.traverse(o=>{if(!o.isMesh)return;let geo=o.geometry.clone().applyMatrix4(new THREE.Matrix4().multiplyMatrices(S,o.matrixWorld));if(geo.index)geo=geo.toNonIndexed();if(!geo.attributes.normal)geo.computeVertexNormals();
   if(!L.has(o.material))L.set(o.material,{gs:[],n:o.name});const e=L.get(o.material);e.gs.push(geo);if(o.name==='carroceria')e.n='carroceria'});
  for(const [mat,e] of L){let n=0;for(const q of e.gs)n+=q.attributes.position.count;const Pp=new Float32Array(n*3),Nn=new Float32Array(n*3);let k=0;
   for(const q of e.gs){Pp.set(q.attributes.position.array,k*3);Nn.set(q.attributes.normal.array,k*3);k+=q.attributes.position.count}
   const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(Pp,3));geo.setAttribute('normal',new THREE.BufferAttribute(Nn,3));geo.computeBoundingSphere();
   const m=new THREE.Mesh(geo,mat);m.name=e.n;m.castShadow=!mat.transparent;if(mat.transparent)m.renderOrder=3;out.add(m)}""")
        r("const g=plano(F.coche(i),.038,0,[i===1?.1:.09,.18],h);g.userData.tipo='oficial'+i;","const g=plano(F.coche(i,{piloto:true}),.038,0,[i===1?.1:.09,.18],h);g.userData.tipo='oficial'+i;g.children.forEach(m=>m.userData.oficial='coche'+i);")
    open(f,'w',encoding='utf8').write(s);print('ok riagt',f)
