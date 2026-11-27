# Fachadas reales del tramo bajo de Gran Vía (granvia.js): color y material de cada edificio sacados de Street View, y paleta del
# centro para el resto del corredor. Siete páginas; va al final de la cadena. Toca solo el reparto de colores de subeMalla.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','webgl.html','indexm.html','gpu.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'granvia.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- Fachadas reales de Gran Vía (granvia.js)'
FIN='// ---------- fin de granvia.js\n'
A="{const zc=new Map();for(const[c,e] of C){V.fromBufferAttribute(pos,e.v[0]).applyMatrix4(mw);if(!enZonaC(V.x,V.z))continue;"
B=("{const zc=new Map(),_gc=new THREE.Vector3();for(const[c,e] of C){V.fromBufferAttribute(pos,e.v[0]).applyMatrix4(mw);"
   "{let sx=0,sz=0;for(const i of e.v){_gc.fromBufferAttribute(pos,i).applyMatrix4(mw);sx+=_gc.x;sz+=_gc.z}const gx=sx/e.v.length,gz=sz/e.v.length;"
   "if(gvCorr(gx,gz)){const rv=gvColor(gx,gz);if(rv){zc.set(c,rv);continue}}else if(!enZonaC(V.x,V.z))continue}")
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado granvia',f);continue
    assert s.count(A)==1,(f,s.count(A))
    s=s.replace(A,B)
    assert s.count("function subePaso(){")==1
    s=s.replace("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok granvia',f)
