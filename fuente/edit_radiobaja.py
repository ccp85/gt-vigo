# Calidad Baja (modo gama baja del móvil): la radio empieza apagada. Las emisoras que no son mp3 se tocan en directo con
# instrumentos sintetizados y gastan procesador. Se puede encender con 📻 o la tecla M; no se guarda como apagada, así que
# en las otras calidades sigue como la tuvieras. Va al final de todo.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','webgl.html','gpu.html'] if os.path.exists(f)]
A="try{const v=localStorage.getItem(window.SOLO_NAVIDAD?'gtvigo_nav_radio':'gtvigo_radio');if(v==='off')RADIO.on=false;else if(v!==null)RADIO.i=(+v||0)%10}catch(e){}"
B=A+"\nif(window.LITE&&window.GAMA_BAJA&&!window.SOLO_NAVIDAD){RADIO.on=false;addEventListener('DOMContentLoaded',()=>{const b=document.getElementById('bRadio');if(b)b.classList.add('off')})}   // calidad Baja: radio apagada al empezar (edit_radiobaja.py)"
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'edit_radiobaja.py' in s:print('ya estaba',f);continue
    c=s.count(A)
    if c!=1:print('sin ancla',f,c);continue
    s=s.replace(A,B);open(f,'w',encoding='utf8').write(s);print('ok radiobaja',f)
