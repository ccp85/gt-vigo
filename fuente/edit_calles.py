# Cantos de calles (las cinco páginas): calzadas, aceras y jardines dejan de parecer láminas flotando sobre el suelo.
# Cada zona trae calzada, aceras y verde como láminas planas a distinta altura sobre la tierra y sin lados; calles.js les
# pone, al cargar la zona y en segundo plano, un lado vertical (bordillo, canto del asfalto, talud de tierra) que baja hasta
# lo que hay al lado. Va al final de la cadena.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'calles.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'const FALDON=' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("function cargaZona(id,NP,k,N){",JS+"\nfunction cargaZona(id,NP,k,N){")
    r("mk('shaders');scene.add(root);","mk('shaders');scene.add(root);try{FALDON(root)}catch(e){console.warn('faldones',e)}")
    open(f,'w',encoding='utf8').write(s);print('ok calles',f)
