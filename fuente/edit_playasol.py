# Playas con vida según el tiempo (playasol.js), en las cinco páginas.
#  - vidaPlaya nuevo: bañistas en bañador (ellos) y bikini (ellas) tumbados o sentados en toallas con franjas, sombrillas
#    a rayas más altas que la gente, corrillos de pie charlando y nadadores con flotador. Los paseantes de la orilla
#    también van en bañador.
#  - playaSolTick: con sol y de día la playa está llena; con nubes o néboa hay menos gente; si llueve o se hace de noche
#    se van todos y desaparecen sombrillas y toallas (poco a poco, como recogiendo). Las sombrillas y hamacas fijas de
#    Samil se quitan igual.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'playasol.js'),encoding='utf8').read().strip('\n')+'\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function playaSolTick(' in s:   # ya aplicado: solo se actualiza el bloque
        a=s.index('// ---- playas con vida: bañistas');b=s.index('// en juego solo se dibuja lo cercano')
        s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado playasol',f);continue
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    a=s.index('function vidaPlaya(root){');b=s.index('// en juego solo se dibuja lo cercano')
    s=s[:a]+JS+s[b:]
    r("const G=crearGente(L.length,'vida_playa');for(const m of G.all)root.add(m);PASEO.push({G,L,root})",
      "const G=crearGente(L.length,'vida_playa');trajeBano(G,L.length);for(const m of G.all)root.add(m);PASEO.push({G,L,root})")
    r("semaforosTick(dt);paseoTick(t);","semaforosTick(dt);paseoTick(t);try{playaSolTick(dt)}catch(e){}")
    # Samil: sombrillas y hamacas en un grupo aparte que se puede quitar
    i=s.index('function samCrea(');j=s.index('function samTrasPaseo(')
    seg=s[i:j]
    def rs(a,b):
        global seg
        assert seg.count(a)==1,(f,'samil',seg.count(a),a[:80]);seg=seg.replace(a,b)
    rs("PARTS.get(mat).push(g)};",
       "PARTS.get(mat).push(g)},PARTSP=new Map(),addP=(geo,mat,x,y,z,ry=0,rx=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();g.deleteAttribute('uv');if(rx)g.rotateX(rx);g.rotateY(ry);g.translate(x,y,z);if(!PARTSP.has(mat))PARTSP.set(mat,[]);PARTSP.get(mat).push(g)};")
    k0=seg.index('// sombrillas y hamacas en grupos');k1=seg.index('// complejo de piscinas')
    blk=seg[k0:k1];assert blk.count('add(')==4,blk.count('add(')
    seg=seg[:k0]+blk.replace('add(','addP(')+seg[k1:]
    rs("for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=mat!==LUZ;m.receiveShadow=true;G.add(m)}",
       "for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=mat!==LUZ;m.receiveShadow=true;G.add(m)}\n {const GP_=new THREE.Group();GP_.name='samil_playa';for(const[mat,gs]of PARTSP){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=true;m.receiveShadow=true;m.userData.noLote=1;GP_.add(m)}G.add(GP_);PLY.SAM=GP_}")
    s=s[:i]+seg+s[j:]
    open(f,'w',encoding='utf8').write(s);print('ok playasol',f)
