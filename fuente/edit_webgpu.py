# GT Vigo con WebGPU (fase 1, de prueba): genera gpu.html a partir de index.html ya compilado (va al final de la cadena).
# index.html no se toca. gpu.html usa three.js 0.187 con WebGPURenderer: en navegadores con WebGPU dibuja con WebGPU
# y si no lo hay, el propio three.js vuelve solo a WebGL2. Arriba a la izquierda sale qué motor está usando y los fps.
# Lo que aún no está pasado al sistema nuevo de shaders (TSL) se apaga en esta página:
#  - los efectos hechos con onBeforeCompile (agua realista, asfalto, césped, arena...) no se aplican: se ve el material base;
#  - los ShaderMaterial (GLSL) pasan a un material básico invisible;
#  - fase 2: el cielo y el mar están pasados a TSL (gpu_tsl.js);
#  - fase 3: reflejo de la ciudad en el mar, olas de Patos, asfalto, marcas, charcos, césped, fachadas, tejados y escaparates;
#  - sin posprocesado (bloom, color, suavizado SMAA) ni reflejo de la ciudad en coches y charcos (los charcos reflejan el cielo).
# Con ?webgl=1 se fuerza el motor nuevo sobre WebGL2 (para comparar en el mismo aparato).
# Sirve para medir el rendimiento en cada dispositivo antes de ir pasando efectos uno a uno.
import sys,os,re
D=os.path.dirname(os.path.abspath(__file__))
SRC=sys.argv[1] if len(sys.argv)>1 else 'index.html'
DST=sys.argv[2] if len(sys.argv)>2 else 'gpu.html'
s=open(SRC,encoding='utf8').read()
def r(a,b,n=None):
    global s
    c=s.count(a)
    assert c>=1 and (n is None or c==n),(c,a[:90]); s=s.replace(a,b)
V='0.187.0'
# 1) three.js nuevo con WebGPU (el mismo módulo para el juego y los addons)
s=re.sub(r'<script type="importmap">.*?</script>',
  '<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@%s/build/three.webgpu.min.js","three/webgpu":"https://cdn.jsdelivr.net/npm/three@%s/build/three.webgpu.min.js","three/tsl":"https://cdn.jsdelivr.net/npm/three@%s/build/three.tsl.min.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@%s/examples/jsm/","three-mesh-bvh":"https://cdn.jsdelivr.net/npm/three-mesh-bvh@0.9.18/build/index.module.js","fflate":"https://cdn.jsdelivr.net/npm/fflate@0.8.2/esm/browser.js"}}</script>'%(V,V,V,V),s,count=1,flags=re.S)
# 1b) el posprocesado viejo (WebGL) no carga con el módulo de WebGPU: clases vacías (está apagado en esta página)
for n in ['EffectComposer','RenderPass','UnrealBloomPass','ShaderPass','OutputPass','SMAAPass']:
    a="import {%s} from 'three/addons/postprocessing/%s.js';"%(n,n)
    assert s.count(a)==1,n
    s=s.replace(a,"class %s{constructor(){throw new Error('sin posprocesado en WebGPU (fase 1)')}}"%n)
# 1c) los trozos de shader GLSL de three.js no existen en WebGPU (solo los usa el reparto de sombras en cascada)
r("{const CH=THREE.ShaderChunk,","{const CH={lights_fragment_begin:''},",1)
# 2) motor de dibujo
r('new THREE.WebGLRenderer(','new THREE.WebGPURenderer(')
r("powerPreference:'high-performance'});","powerPreference:'high-performance',forceWebGL:/[?&]webgl=1/.test(location.search)});await R.init();",1)
# la pantalla de inicio tiene su propio motor 3D: en la prueba se usan los dibujos planos de reserva
r("try{rd=new THREE.WebGPURenderer({canvas:cv,antialias:true,alpha:true,powerPreference:'low-power'})}catch(e){emojis();return false}","emojis();return false;",1)
r('THREE.WebGLCubeRenderTarget','THREE.CubeRenderTarget')
# 3) materiales GLSL → sustituto (se conservan los uniforms para que el código que los actualiza siga funcionando)
r('new THREE.ShaderMaterial(','window.GPUMAT(THREE,')
s=s.replace('new THREE.RawShaderMaterial(','window.GPUMAT(THREE,')
SHIM=r"""<script>
// gpu.html: sustituto de los ShaderMaterial (GLSL) mientras no estén pasados a TSL
window.GPUMAT=(T,p={})=>{const u=p.uniforms||{},cielo=/topColor|uTop|uZenit|cielo|sky/i.test(Object.keys(u).join(' '));
 const m=new T.MeshBasicMaterial({color:cielo?0x9cc8ec:0xffffff,transparent:true,opacity:cielo?1:0,depthWrite:false,side:p.side??T.FrontSide,fog:false});
 if(!cielo){m.colorWrite=false}m.uniforms=u;m.defines=p.defines||{};m.isGpuSustituto=true;m.vertexShader=p.vertexShader||'';m.fragmentShader=p.fragmentShader||'';return m};
window.GPU_INFO={motor:'…',fps:0};
</script>
"""
r('<script type="importmap">',SHIM+'<script type="importmap">',1)
# 4) sin posprocesado ni reflejos por ahora
r("if(window.LITE)POST.on=false;","POST.on=false;",1)
r("const RCUBO={cc:null,rt:null,pm:null,out:null,face:0,t:-99,mal:false,","const RCUBO={cc:null,rt:null,pm:null,out:null,face:0,t:-99,mal:true,",1)
# 5) cosas del motor viejo que no existen en el nuevo
r("aa:R.getContext().getContextAttributes().antialias","aa:true",1)
s=s.replace("R.info.render.calls","(R.info.render.drawCalls??R.info.render.calls)")
# 6) marcador: motor en uso y fps (arriba a la izquierda)
r("R.setAnimationLoop(()=>{",r"""{const d=document.createElement('div');d.id='gpuInfo';d.style.cssText='position:fixed;left:8px;top:calc(56px + env(safe-area-inset-top,0px));z-index:99;background:rgba(10,12,30,.72);color:#9fe;font:600 12px monospace;padding:4px 7px;border-radius:6px;pointer-events:none';document.body.appendChild(d);
 let n=0,t0=performance.now();const tic=()=>{n++;const t=performance.now();if(t-t0>1000){GPU_INFO.fps=Math.round(n*1000/(t-t0));n=0;t0=t;const b=R.backend;GPU_INFO.motor=b&&b.isWebGPUBackend?'WebGPU':'WebGL2 (sin WebGPU en este navegador)';d.textContent='Motor: '+GPU_INFO.motor+' · '+GPU_INFO.fps+' fps'}requestAnimationFrame(tic)};requestAnimationFrame(tic)}
R.setAnimationLoop(()=>{""",1)
# 7) en el móvil no salta a indexm.html: esta página es la prueba también en móvil
s=s.replace("location.replace('indexm.html'+location.search+location.hash)","void 0")
# 8) fase 2: cielo y agua en TSL (gpu_tsl.js)
TSLJS=open(os.path.join(D,'gpu_tsl.js'),encoding='utf8').read().strip('\n')+'\n'
r("import * as THREE from 'three';","import * as THREE from 'three';\nconst TSL=THREE.TSL;   // TSL del mismo módulo que el motor (three/tsl trae otra copia de los nudos)",1)
r("function aguaSamil(m){",TSLJS+"function aguaSamil(m){",1)
r("window.CIELO=CIELO;sky.renderOrder=-10;","window.CIELO=CIELO;try{sky.material=gpuCielo()}catch(e){console.warn('cielo TSL',e)}sky.renderOrder=-10;",1)
r("aguaSamil(m);WATERS.push(m);water=m;","aguaSamil(m);WATERS.push(m);water=m;try{o.material=gpuAgua(false);WATERS.push(o.material)}catch(e){console.warn('agua TSL',e)}",1)
r("MARG=new THREE.Mesh(g,m);MARG.name='mar_global';","let mg=m;try{mg=gpuAgua(true);WATERS.push(mg)}catch(e){console.warn('mar TSL',e)}MARG=new THREE.Mesh(g,mg);MARG.name='mar_global';",1)
r("const me=new THREE.Mesh(g,m);me.name='olas_patos';","let ms=m;try{ms=gpuAgua(false,true);WATERS.push(ms)}catch(e){console.warn('olas TSL',e);m.visible=false}const me=new THREE.Mesh(g,ms);me.name='olas_patos';",1)
# fase 3: reflejo de la ciudad en el mar (aguaReflejo dibuja con la cámara reflejada; aquí no depende del posprocesado)
r("if(window.LITE||ARF.mal||!driving||!(typeof POST!=='undefined'&&POST.on)||","if(window.LITE||ARF.mal||!driving||",1)
# fase 3: suelos, fachadas, tejados y escaparates (cada función añade su versión TSL al material)
for a,b in [("'|asf';m.needsUpdate=true;return m}","'|asf';m.needsUpdate=true;gpuFx('asf',m);return m}"),
            ("'|mv';m.needsUpdate=true;return m}","'|mv';m.needsUpdate=true;gpuFx('mv',m);return m}"),
            ("'|ces';m.needsUpdate=true;return m}","'|ces';m.needsUpdate=true;gpuFx('ces',m);return m}"),
            ("'|mo';m.needsUpdate=true}","'|mo';m.needsUpdate=true;gpuFx('mo',m,k)}"),
            ("m.customProgramCacheKey=()=>'fr'+k;m.needsUpdate=true}","m.customProgramCacheKey=()=>'fr'+k;m.needsUpdate=true;gpuFx('fr',m,k)}"),
            ("'|tj';m.needsUpdate=true}","'|tj';m.needsUpdate=true;gpuFx('tj',m)}"),
            ("m.customProgramCacheKey=()=>'vit';m.needsUpdate=true}","m.customProgramCacheKey=()=>'vit';m.needsUpdate=true;gpuFx('vit',m)}"),
            ("m.needsUpdate=true}\n// edit_olas.py","m.needsUpdate=true;gpuFx('fv',m)}\n// edit_olas.py")]:
    r(a,b,1)
s=s.replace('<title>GT Vigo','<title>GT Vigo · WebGPU (prueba)',1)
open(DST,'w',encoding='utf8').write(s);print('ok webgpu',DST)
