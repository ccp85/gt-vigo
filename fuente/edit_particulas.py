# Partículas masivas en la GPU (gpu_particulas.js), solo en las páginas con WebGPU (index.html y gpu.html); va al final de
# la cadena. Lluvia de hasta 200.000 gotas con salpicaduras en el suelo (sustituye a la lluvia de la CPU jugando), chispas en
# los golpes y hojas de otoño que caen de los árboles cercanos y salen volando al pasar. Con window.__PARTICULAS_OFF=true,
# lo de antes.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','gpu.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'gpu_particulas.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- partículas masivas en la tarjeta gráfica (gpu_particulas.js'
FIN='// ---------- fin de gpu_particulas.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado particulas',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("// ---------- fin de gpu_coches.js\n","// ---------- fin de gpu_coches.js\n"+JS)
    r("try{algasTick()}catch(e){if(!window.__alE){window.__alE=1;console.warn('algas',e)}}","try{algasTick()}catch(e){if(!window.__alE){window.__alE=1;console.warn('algas',e)}}try{gppTick(dt)}catch(e){if(!window.__gpE){window.__gpE=1;console.warn('partículas',e)}}")
    r("function lluviaTick(dt,on){LLUVIA.visible=on>.02;","function lluviaTick(dt,on){GPP.rain=on;if(GPP.on&&driving&&!RACE.on){LLUVIA.visible=false;return}LLUVIA.visible=on>.02;")
    r("function golpe(){","function golpe(){try{gppChispas()}catch(e){}")
    open(f,'w',encoding='utf8').write(s);print('ok particulas',f)
