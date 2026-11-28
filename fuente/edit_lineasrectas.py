# Calzada con líneas rectas (las siete páginas; va al final de todo, después de edit_bajamenos.py).
# 1) Marcas viales nuevas (lineasrectas.js): al cargar cada zona, su malla «lineas» se cambia por la de <zona>_lineas.bin,
#    horneada con herramientas/lineas_hornear.mjs a partir del eje de las calles y del asfalto real: líneas rectas y paralelas
#    al bordillo, carriles de 3,2 m, trazos de 3 m con huecos de 5 m, cortadas en los cruces, líneas de detención y de ceda el
#    paso, y pasos de cebra rectos de bordillo a bordillo. Si falta el .bin de una zona se quedan las marcas de antes.
# 2) Asfalto más uniforme: las manchas y parches de reasfaltado eran blobs grandes y torcidos que no seguían la calle y hacían
#    que la calzada pareciera un collage; ahora la variación de tono es mucho más suave (WebGL y WebGPU).
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','webgl.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'lineasrectas.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function lineasRectas(root,id)' in s:print('ya estaba',f);continue
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    def r0(a,b):   # solo si está (los nudos de WebGPU solo existen en index.html y gpu.html)
        global s
        if s.count(a)==1:s=s.replace(a,b)
    r("function cargaZona(id,NP,k,N){",JS+"\nfunction cargaZona(id,NP,k,N){")
    r("const root=g.scene;root.name=id;","const root=g.scene;root.name=id;await lineasRectas(root,id);mk('lineas');")
    r("function precargar(id){","function precargar(id){try{lineasPre(id)}catch(e){}")
    # asfalto: menos manchas y parches (WebGL)
    r("diffuseColor.rgb*=(.78+.36*man)*(1.+.3*grano*gf)*(1.-.2*par)*(1.-.4*gri);","diffuseColor.rgb*=(.93+.12*man)*(1.+.3*grano*gf)*(1.-.06*par)*(1.-.3*gri);")
    r("diffuseColor.rgb*=1.+vec3(.06,.035,-.05)*tn*2.;","diffuseColor.rgb*=1.+vec3(.025,.015,-.02)*tn*2.;")
    # y en el motor WebGPU (TSL)
    r0("b.mul(man.mul(.36).add(.78)).mul(grano.mul(.3).add(1)).mul(par.mul(.2).oneMinus()).mul(gri.mul(.4).oneMinus())",
       "b.mul(man.mul(.12).add(.93)).mul(grano.mul(.3).add(1)).mul(par.mul(.06).oneMinus()).mul(gri.mul(.3).oneMinus())")
    r0("b.mul(vec3(.06,.035,-.05).mul(tn).mul(2).add(1))","b.mul(vec3(.025,.015,-.02).mul(tn).mul(2).add(1))")
    open(f,'w',encoding='utf8').write(s);print('ok lineasrectas',f)
