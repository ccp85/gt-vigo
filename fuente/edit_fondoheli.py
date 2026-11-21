import sys,os
# ================= Fondo lejano y cielo también volando =================
# En helicóptero (y la carroza voladora de Navidad) la cámara cortaba a la distancia de la niebla (~25 u): no se veían
# las Cíes, Cangas ni los montes de la ría, y la bóveda del cielo, que se escala con ese corte, quedaba metida en la
# niebla blanca. Ahora, como al conducir: en ordenador la cámara llega a 260 u y el fondo lejano se dibuja también en vuelo.
# En el móvil (LITE) sigue como antes. Va al final de build.sh.
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '/*fondoheli*/' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("pcam.far=FONDO.m&&MODO!=='heli'&&!window.LITE?260:FOG.far+4","pcam.far=/*fondoheli*/FONDO.m&&!window.LITE?260:FOG.far+4")
    r("function fondoTick(){if(!FONDO.m)return;const on=driving&&MODO!=='heli';","function fondoTick(){if(!FONDO.m)return;const on=driving;")
    open(f,'w',encoding='utf8').write(s);print('ok fondoheli',f)
