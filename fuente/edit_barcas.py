# Barcas con forma de barco y gamelas de pescadores con sus remos (barcas.js), en las seis páginas; va al final de la cadena.
# Cascos por cuadernas para las lanchas de las bateas, los veleros de la ría y los veleros amarrados del Náutico (antes
# cajas y siluetas extruidas), y gamelas gallegas cerca de la costa: unas remando y otras fondeadas con el pescador y la caña.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'barcas.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- barcas con forma de barco y gamelas de pescadores (barcas.js)'
FIN='// ---------- fin de barcas.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado barcas',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("function mkLancha(col){","function mkLanchaVieja(col){")
    r("function mkVelero(col,vela){","function mkVeleroViejo(col,vela){")
    r("function velasTick(dt,t){if(!VELAS.ok){velasInit();return}","function velasTick(dt,t){try{gamelasTick(dt,t)}catch(e){if(!window.__gamE){window.__gamE=1;console.warn('gamelas',e)}}if(!VELAS.ok){velasInit();return}")
    # veleros del Náutico: el casco extruido plano pasa a casco por cuadernas
    r("add(ex(1,.016,-.008),W);add(ex(1.01,.004,-.006),Nv);","add((()=>{const q=BARC.casco({L:.12,B:.036,H:.008,D:.009,fondo:'redondo',popa:.62,arrufo:.003,NS:14,NU:5});q.deleteAttribute('color');return q})(),W);")
    r("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok barcas',f)
