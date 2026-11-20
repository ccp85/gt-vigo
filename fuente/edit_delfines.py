# Delfines en mar abierto (delfines.js) en las cinco páginas.
#  - se mueven y animan en cada fotograma, junto a las gaviotas
#  - bajo el agua no se esconden con el resto del mundo de superficie (userData.submarino)
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'delfines.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function delfinesTick(' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("gaviotasTick(dt);","gaviotasTick(dt);try{delfinesTick(dt)}catch(e){if(!window.__delErr){window.__delErr=1;console.error(e)}}")
    if '!o.userData.submarino' not in s:r("o!==B.W&&o!==B.nad&&!(B.reg&&o===B.reg.g)","o!==B.W&&o!==B.nad&&!o.userData.submarino&&!(B.reg&&o===B.reg.g)")
    a=s.find('setInterval(sagTick,40);')
    assert a>0,f
    a+=len('setInterval(sagTick,40);')
    s=s[:a]+'\n'+JS+s[a:]
    open(f,'w',encoding='utf8').write(s);print('ok delfines',f)
