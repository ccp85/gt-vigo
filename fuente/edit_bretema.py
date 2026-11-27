# Brétema y perspectiva aérea (gpu_bretema.js), solo en las páginas con WebGPU (index.html y gpu.html); va al final de la
# cadena, después de edit_cielofis.py (usa su cielo físico). La niebla de three.js pasa a una niebla en TSL con tres capas:
# perspectiva aérea (lo lejano se azula; a contraluz, más cálido), la niebla de siempre con las mismas distancias (sigue
# tapando lo que no ha cargado) y brétema: niebla baja pegada al mar y a lo hondo, a jirones, con néboa, por las mañanas
# tranquilas y muy fina siempre sobre la ría. Los montes y el mar del fondo (vigo_fondo.json) se azulan igual y la brétema
# se les pega abajo. En la maqueta, la ría se cubre de brétema vista desde arriba. Con window.__BRETEMA_OFF=true, la de antes.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','gpu.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'gpu_bretema.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- brétema y perspectiva aérea (gpu_bretema.js)'
FIN='// ---------- fin de gpu_bretema.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado bretema',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("// ---------- fin de gpu_cielofis.js\n","// ---------- fin de gpu_cielofis.js\n"+JS)
    r("function cielo(dt){","function cielo(dt){try{bretemaTick(dt)}catch(e){if(!window.__brE){window.__brE=1;console.warn('brétema',e)}}")
    # montes y mar del fondo: aire azulado y brétema abajo
    r("const uFog=U('uFog'),neb=c=>{const h=smoothstep(uNear,uNear.add(160),d);return mix(c,uFog,clamp(h.mul(.55).add(.2),0,.75))};",
      "const uFog=U('uFog'),neb=c=>{try{return GT.fondoNeb(c,d,W,uNear,uCam)}catch(e){console.warn('fondo brétema',e);const h=smoothstep(uNear,uNear.add(160),d);return mix(c,uFog,clamp(h.mul(.55).add(.2),0,.75))}};")
    open(f,'w',encoding='utf8').write(s);print('ok bretema',f)
