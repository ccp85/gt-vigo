# Plaza de las rampas en Nicaragua (rampas3.js): las cintas empiezan en la Rúa Nicaragua y entre Nicaragua y Praza de España
# van el suelo LED que imita el mar, la rampa de paneles que generan energía, bancos y sillas y el Pezseto. Siete páginas;
# va al final de la cadena (después de edit_rampas2.py, que ya está en la base).
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','webgl.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'rampas3.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- Plaza de las rampas en Nicaragua (rampas3.js)'
FIN='// ---------- fin de rampas3.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado rampas3',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("const TR=[];for(let t0=0;t0<L-.1;t0+=.7)TR.push([t0,Math.min(L,t0+.62)]);","const TR=[];for(let t0=RPZ.T0;t0<L-.1;t0+=.7)TR.push([t0,Math.min(L,t0+.62)]);")
    r(" const mv=G.children.find(o=>o.material===BELT);"," try{rampaPlaza(G,{L,EN,at,gy,angT})}catch(e){console.warn('rampaPlaza',e)}\n const mv=G.children.find(o=>o.material===BELT);")
    r("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok rampas3',f)
