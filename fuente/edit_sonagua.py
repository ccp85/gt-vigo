# Sonido del agua (sonagua.js) y radio solo en vehículos, en las cinco páginas.
#  - la radio se calla andando, nadando o buceando y vuelve al subir a un vehículo
#  - bajo el agua todo se apaga con un filtro y suena el fondo de la ría (ver sonagua.js)
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'sonagua.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function sagTick(' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("play=RADIO.on&&driving&&(!RACE.on||!!window.SOLO_NAVIDAD)&&soundOn;",
      "play=RADIO.on&&driving&&MODO!=='pie'&&MODO!=='nado'&&(!RACE.on||!!window.SOLO_NAVIDAD)&&soundOn;")
    r("setInterval(radioTick,40);","setInterval(radioTick,40);\n"+JS)
    open(f,'w',encoding='utf8').write(s);print('ok sonagua',f)
