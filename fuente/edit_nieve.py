# Nevada de Navidad (nieve.js) en las cinco páginas: nieva durante el reparto y la carrera de Navidad
# y la nieve va cuajando en calles, aceras, tejados y árboles. Va al final de build.sh (después de edit_trafico.py).
#  - nieveTick va en el bucle principal, junto a gaviotas y delfines, para poder quitar la nieve al salir del modo
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'nieve.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function nieveTick(' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("gaviotasTick(dt);","gaviotasTick(dt);try{nieveTick(dt)}catch(e){if(!window.__nvErr){window.__nvErr=1;console.error(e)}}")
    a=s.find('setInterval(sagTick,40);')
    assert a>0,f
    a+=len('setInterval(sagTick,40);')
    s=s[:a]+'\n'+JS+s[a:]
    open(f,'w',encoding='utf8').write(s);print('ok nieve',f)
