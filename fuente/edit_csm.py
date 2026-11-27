# Sombras en cascada con WebGPU (gpu_csm.js + gpu_csm_three.js), solo en index.html y gpu.html; va al final de la cadena,
# después de edit_bretema.py. Al conducir con sombra del sol: CSMShadowNode de three.js (copiado en gpu_csm_three.js con las
# importaciones del juego) con tres cascadas atadas a la cámara del coche (nítida cerca, barata lejos). En la maqueta: el
# mapa de sombras del sol ajustado a lo que se ve. Se quita la cascada lejana del motor viejo (con WebGPU no hacía nada).
# Con window.__CSM_OFF=true se vuelve a las sombras de antes.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','gpu.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'gpu_csm_three.js'),encoding='utf8').read().strip('\n')+'\n'+open(os.path.join(D,'gpu_csm.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- sombras en cascada de three.js 0.187'
FIN='// ---------- fin de gpu_csm.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado csm',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("// ---------- fin de gpu_bretema.js\n","// ---------- fin de gpu_bretema.js\n"+JS)
    r("sombrasTick();if(COMIC.on)","sombrasTick();try{csmTick()}catch(e){if(!window.__csmE){window.__csmE=1;console.warn('sombras en cascada',e)}}if(COMIC.on)")
    # la cascada lejana del motor viejo: fuera de la escena (con WebGPU cada luz solo sombrea su propia luz, y esta no alumbra)
    r("window.__SUNF=sunF;","window.__SUNF=sunF;if(sunF.parent){scene.remove(sunF);scene.remove(sunF.target)}")
    r("function sombrasRecv(){window.__SUNF.parent.traverse(","function sombrasRecv(){scene.traverse(")
    open(f,'w',encoding='utf8').write(s);print('ok csm',f)
