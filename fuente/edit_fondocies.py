import sys,os
# ================= Cíes (y montes) sin doble silueta =================
# Más allá de la niebla se veían dos siluetas superpuestas: la maqueta de verdad, toda tapada por la niebla (clara),
# y encima el relieve del fondo lejano (vigo_fondo.json, alturas x1.6), que asomaba por arriba como una cresta negra,
# sobre todo de noche (su neblina propia oscurecía mucho y no llegaba al color de la niebla del juego).
# Ahora: el fondo lejano se dibuja un pelín "hacia la cámara" (misma imagen en pantalla, pero gana en profundidad a la
# maqueta tapada por la niebla, así que solo se ve una silueta) y su neblina acaba en el color de la niebla del juego.
# Va al final de build.sh.
TSL_NEB_A="const neb=c=>{const h=smoothstep(uNear,uNear.add(160),d),aire=mix(uHor,uZen,.35).mul(vec3(.82,.88,1)).mul(uNight.mul(.7).oneMinus());return mix(c,aire,clamp(h.mul(.5).add(.12),0,.65))};"
TSL_NEB_B="const uFog=U('uFog'),neb=c=>{const h=smoothstep(uNear,uNear.add(160),d);return mix(c,uFog,clamp(h.mul(.55).add(.2),0,.75))};"
TSL_POS_A="const m=basic();m.colorNode=neb(c);"
TSL_POS_B="const m=basic();m.colorNode=neb(c);if(vs.includes('*.96'))m.positionNode=uCam.add(positionLocal.sub(uCam).mul(.96));"
if __name__=='__main__' and sys.argv[1:2]==['--tsl']:   # también el fuente gpu_tsl.js
    f='gpu_tsl.js';s=open(f,encoding='utf8').read()
    if TSL_POS_B not in s:
        for a,b in((TSL_NEB_A,TSL_NEB_B),(TSL_POS_A,TSL_POS_B)):assert s.count(a)==1,a[:60];s=s.replace(a,b)
        open(f,'w',encoding='utf8').write(s)
    print('ok gpu_tsl.js');sys.exit()
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','gpu.html','nav.html','navm.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '/*fondocies*/' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("uNight:SKYU.uNight,uSun:SKYU.uSun}};","uNight:SKYU.uNight,uSun:SKYU.uSun,uFog:{value:FOG.color}}};")
    r("const vs='varying vec3 vW;varying vec3 vN;void main(){vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;vN=normal;gl_Position=projectionMatrix*viewMatrix*w;}';",
      "const vs='varying vec3 vW;varying vec3 vN;void main(){vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;vN=normal;gl_Position=projectionMatrix*viewMatrix*w;}';"
      "/*fondocies*/const vsF='uniform vec3 uCam;varying vec3 vW;varying vec3 vN;void main(){vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;vN=normal;vec3 p=uCam+(w.xyz-uCam)*.96;gl_Position=projectionMatrix*viewMatrix*vec4(p,1.);}';")
    r("const comun=`uniform vec3 uCam,uHor,uZen,uSun;","const comun=`uniform vec3 uCam,uHor,uZen,uSun,uFog;")
    r("vec3 aire=mix(uHor,uZen,.35)*vec3(.82,.88,1.)*(1.-.7*uNight);return mix(c,aire,clamp(.12+.5*h,0.,.65));",
      "vec3 aire=uFog;return mix(c,aire,clamp(.2+.55*h,0.,.75));")
    if 'window.GPU_TSLMAT' in s:   # versión WebGPU: el fondo va en TSL (mismo cambio que en gpu_tsl.js)
        r("const m=window.GPUMAT(THREE,{uniforms:FONDO.U,vertexShader:vs,","const m=window.GPUMAT(THREE,{uniforms:FONDO.U,vertexShader:vsF,")
        r(TSL_NEB_A,TSL_NEB_B);r(TSL_POS_A,TSL_POS_B)
    else:
        r("const m=new THREE.ShaderMaterial({uniforms:FONDO.U,vertexShader:vs,","const m=new THREE.ShaderMaterial({uniforms:FONDO.U,vertexShader:vsF,")
    open(f,'w',encoding='utf8').write(s);print('ok fondocies',f)
