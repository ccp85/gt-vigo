# Posprocesado ligero con WebGPU (gpu_post.js), solo index.html y gpu.html: rehace el bloque postInit/postRender con la
# versión de gpu_post.js (como edit_webgpu.py) después de los cambios de la cadena. Añade oclusión ambiental GTAO,
# rayos de sol con brétema y atardecer dorado, y gradación de color según la hora y el clima (tono ACES).
# window.__AO_OFF=true quita la oclusión; window.__RAYOS_OFF=true, los rayos.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','gpu.html'] if os.path.exists(f)]
src=open(os.path.join(D,'gpu_post.js'),encoding='utf8').read()
blk=src[src.index('function postInit(){'):].rstrip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    a=s.index('function postInit(){');b=s.index('\n\n// ---------- estilo cómic',a)
    s=s[:a]+blk+s[b:];open(f,'w',encoding='utf8').write(s);print('ok posprocesado',f)
