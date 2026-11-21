import os
# ================= BORDES SUAVES (antialiasing) con calidad alta =================
# Con calidad alta (tecla G) la imagen pasa por el posprocesado (oclusión, resplandor, gradación) y el suavizado de bordes
# del navegador no actúa: solo quedaba un multimuestreo x2 en la imagen base, y tejados, farolas, barandillas y marcas
# viales salían con dientes de sierra. Ahora:
#  - multimuestreo x4 en la imagen base (antes x2);
#  - y al final un pase SMAA (el suavizado «morfológico» que usan muchos juegos), que busca los bordes en la imagen final
#    (ya con resplandor y gradación) y los suaviza, también los de sombras, reflejos y brillos.
# En modo rendimiento sigue el suavizado del navegador y en el móvil (LITE) no cambia nada. Las cinco páginas.
R=[("import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';",
    "import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';\nimport {SMAAPass} from 'three/addons/postprocessing/SMAAPass.js';"),
   ("function postInit(){if(POST.comp)return;const rt=new THREE.WebGLRenderTarget(2,2,{type:THREE.HalfFloatType,samples:2,",
    "function postInit(){if(POST.comp)return;const rt=new THREE.WebGLRenderTarget(2,2,{type:THREE.HalfFloatType,samples:4,"),
   ("c.addPass(g);POST.comp=c;POST.bloom=b;POST.grade=g}",
    "c.addPass(g);try{POST.smaa=new SMAAPass(2,2);c.addPass(POST.smaa)}catch(e){console.warn('smaa',e)}POST.comp=c;POST.bloom=b;POST.grade=g;window.POST=POST}   // edit_suavizado.py: bordes suaves al final")]
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'POST.smaa=' in s:print('ya estaba',f);continue
    for a,b in R:assert s.count(a)==1,(f,a[:50]);s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s);print('ok suavizado',f)
