# Dos puntos negros de ojos en todos los personajes (las cinco páginas; va al final, después de playasol y palas).
#  - Gente de la calle y de la playa (crearGente): los ojos van en la propia geometría de la cabeza (color en los vértices),
#    sin dibujos de más.
#  - Papá Noel y los Reyes de las carrozas, y Papá, Mamá y el Niño de la misión de la casa (antes una franja).
#  (El protagonista ya los tenía; la chica de las palas y los bañistas los traen en palas.js y playasol.js.)
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '// ojos: dos puntos negros (edit_ojos)' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("const cabeza=mergeGeometries([cab.toNonIndexed(),cue.toNonIndexed()]);",
      "const ojos=[-1,1].map(k=>{const o=new THREE.SphereGeometry(.0012,6,4);o.scale(.55,1.2,1);o.translate(.0063,.0548,k*.0025);return vc(o,0x000000)});   // ojos: dos puntos negros (edit_ojos)\n const cabeza=mergeGeometries([vc(cab,0xffffff),vc(cue,0xffffff),...ojos]);")
    r("ca:mk(GEO_G.cabeza,false)","ca:mk(GEO_G.cabeza,true)")
    r("esf(.0064,MV(piel,.75),x,.0635,0);",
      "esf(.0064,MV(piel,.75),x,.0635,0);for(const z of[-.0024,.0024])esf(.0011,NEGRO,x+.0058,.0655,z,.55,1.2,1);")
    r("const ojo=new THREE.Mesh(new THREE.BoxGeometry(.004,.003,.014*s_),M(0x111111,.5));ojo.position.set(.01*s_,.07*s_,0);o.add(ojo);",
      "for(const k of[-1,1]){const ojo=new THREE.Mesh(new THREE.SphereGeometry(.0019*s_,8,6),M(0x111111,.4));ojo.scale.set(.55,1.2,1);ojo.position.set(.0102*s_,.07*s_,k*.0042*s_);o.add(ojo)}")
    open(f,'w',encoding='utf8').write(s);print('ok ojos',f)
