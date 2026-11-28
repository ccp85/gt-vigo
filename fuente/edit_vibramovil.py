# El móvil vibra al chocar: en golpe() (choques con paredes, tráfico, peatones, rivales y obstáculos) se llama también
# a navigator.vibrate en pantallas táctiles, con un toque corto y como mucho uno cada 0,35 s para que no zumbe sin parar
# al rozar una pared. Con mando conectado vibra el mando, no el móvil. iPhone (Safari) no deja vibrar desde la web.
# Va al final de todo, en las siete páginas.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','webgl.html','gpu.html'] if os.path.exists(f)]
A="padVibra(.7,.35,160);if(!AC||!soundOn)return;"
B="padVibra(.7,.35,160);movilVibra(70);if(!AC||!soundOn)return;"
F=("let _movVibT=0;   // el móvil vibra al chocar (edit_vibramovil.py)\n"
   "function movilVibra(ms){try{if(PAD.i!=null||!navigator.vibrate||!matchMedia('(pointer:coarse)').matches)return;"
   "const t=performance.now();if(t-_movVibT<350)return;_movVibT=t;navigator.vibrate(ms)}catch(_){}}\n")
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'edit_vibramovil.py' in s:print('ya estaba',f);continue
    i=s.find('function golpe(){')
    if i<0 or s.count(A)!=1 or s.find(A)<i:print('sin ancla',f);continue
    s=s.replace(A,B)
    s=s[:i]+F+s[i:]
    open(f,'w',encoding='utf8').write(s);print('ok vibramovil',f)
