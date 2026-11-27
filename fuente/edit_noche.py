# Noche (gpu_noche.js), solo en index.html y gpu.html; va al final de la cadena, después de edit_csm.py.
# Farolas de sodio, ventanas encendidas según la hora y con tonos distintos (cálida, LED, tele), puerto, Rande y la otra
# orilla iluminados con luces pintadas (sprites aditivos que el bloom hace brillar y el mar refleja) y 4 farolas de verdad
# (luces puntuales) solo cerca del jugador. Con window.__NOCHE_OFF=true se apaga lo nuevo.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','gpu.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'gpu_noche.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- noche (gpu_noche.js)'
FIN='// ---------- fin de gpu_noche.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado noche',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("// ---------- fin de gpu_csm.js\n","// ---------- fin de gpu_csm.js\n"+JS)
    r("function cielo(dt){try{bretemaTick(dt)}","function cielo(dt){try{nocheTick(dt)}catch(e){if(!window.__nchE){window.__nchE=1;console.warn('noche',e)}}try{bretemaTick(dt)}")
    # ventanas: cuántas encendidas según la hora y de qué color
    r("vec3(1,.77,.47).mul(step(.5,GT.hF(cel))).mul(win).mul(uLuz).mul(GT.hF(cel.add(5)).add(1.2))","GT.ventanaCol(cel).mul(GT.ventanaOn(cel)).mul(win).mul(uLuz)")
    r("on=step(.5,GT.hF(celF)).mul(uLuz)","on=GT.ventanaOn(celF).mul(uLuz)")
    r("m.emissiveNode=vec3(1,.77,.47).mul(on).mul(gla).mul(GT.hF(celF.add(5)).add(1.2))","m.emissiveNode=GT.ventanaCol(celF).mul(on).mul(gla)")
    # las bombillas de las farolas, más fuertes (que el bloom las haga brillar)
    r("LAMPARA_MAT.emissiveIntensity=lz*2.2","LAMPARA_MAT.emissiveIntensity=lz*(window.__NOCHE_OFF?2.2:3.4)")
    open(f,'w',encoding='utf8').write(s);print('ok noche',f)
