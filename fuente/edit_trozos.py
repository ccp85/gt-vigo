# Piezas enormes de cada zona por trozos en el móvil (LITE): el código está en trozos.js (ver allí). Páginas: indexm y navm
# (y en las de ordenador no hace nada, solo cuenta con LITE). Va al final de todo. Con ?trozos=0 se desactiva para comparar.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
JS=open(os.path.join(D,'trozos.js'),encoding='utf8').read()
FILES=sys.argv[1:] or [f for f in ['indexm.html','navm.html','index.html','webgl.html','gp.html','nav.html','gpu.html'] if os.path.exists(f)]
A="let MODO='coche';window.modo=()=>MODO;"
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'edit_trozos.py' in s:print('ya estaba',f);continue
    if s.count(A)!=1:print('sin ancla',f);continue
    s=s.replace(A,JS.strip()+'\n'+A);open(f,'w',encoding='utf8').write(s);print('ok trozos',f)
