# Huellas, surcos y polvo en la arena (huellas.js), en las cinco páginas; va después de edit_orilla.py.
# Al caminar por la playa quedan pisadas y en coche o moto cada rueda abre un surco con el dibujo del neumático; se ven en la
# arena seca y en la mojada, la resaca las borra y se alisan solas. Las ruedas levantan polvo y granos en la arena seca, cada
# pisada suelta un poco de arena y el viento arrastra arena a ras de suelo. La arena (orilla.js) dibuja las huellas.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'huellas.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- huellas, surcos y polvo en la arena (huellas.js'
FIN='// ---------- fin de huellas.js\n'
ANCLA='// ---------- fin de orilla.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado huellas',f);continue
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r(ANCLA,ANCLA+JS)
    r("gaviotasTick(dt);","gaviotasTick(dt);try{huellasTick(dt)}catch(e){if(!window.__huE){window.__huE=1;console.warn('huellas',e)}}")
    open(f,'w',encoding='utf8').write(s);print('ok huellas',f)
