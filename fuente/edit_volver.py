# Al cambiar la calidad con «🎨» se vuelve al mismo sitio (va después de edit_calidad.py; mundo abierto: index, indexm, webgl).
# Cambiar de calidad tiene que recargar la página (Baja/Media son la versión móvil, Alta el motor clásico y Máxima el
# WebGPU: son juegos distintos por dentro), pero ya no se empieza de cero: antes de recargar se guarda dónde estás, hacia
# dónde miras y en qué vas (coche, moto o helicóptero) en sessionStorage (gtvigo_volver, vale 2 minutos) y, al cargar,
# el juego se salta el menú de inicio, carga la zona donde estabas y te pone ahí (si no estabas en una calle, en la más
# cercana). La cámara y los modelos de vehículo ya se guardaban.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','webgl.html'] if os.path.exists(f)]
MOD_OLD="let MODO='coche';window.modo=()=>MODO;"
MOD_NEW=("let MODO='coche';window.modo=()=>MODO;"
 "window.__estadoJuego=()=>({driving:!!driving,x:P.x,y:P.y,a:P.a,modo:MODO});"   # volver al mismo sitio al cambiar la calidad (edit_volver.py)
 "window.__volverEmpezar=(x,y)=>{let b=null,bd=1e9;for(const q of ZMETA.zonas){const d=zonaDist(q,x,y);if(d<bd){bd=d;b=q}}if(b)empezarEn(b,[x,y])};")
SP_OLD="function startPos(){{const c="
SP_NEW="function startPos(){if(window.__VOLVER){const v=window.__VOLVER;window.__VOLVER=null;START=[v.x,v.y];START_A=v.a}{const c="
SAVE_OLD="   try{localStorage.setItem('gtvigo_calidad',v);sessionStorage.removeItem('gtvigo_saltos')}catch(e){}"
SAVE_NEW=("   try{localStorage.setItem('gtvigo_calidad',v);sessionStorage.removeItem('gtvigo_saltos')}catch(e){}\n"
 "   try{const g=window.__estadoJuego&&window.__estadoJuego();if(g&&g.driving&&isFinite(g.x)&&isFinite(g.y)){sessionStorage.setItem('gtvigo_volver',JSON.stringify({x:g.x,y:g.y,a:g.a,t:Date.now()}));if(/^(coche|moto|heli)$/.test(g.modo))localStorage.setItem('gtvigo_veh',g.modo)}}catch(e){}   // volver al mismo sitio")
RES_OLD="addEventListener('DOMContentLoaded',()=>{const b=document.getElementById('bCal');if(!b)return;"
RES_NEW=("/* 🎨 volver al mismo sitio tras cambiar la calidad: sin menú de inicio, en la zona y el punto donde estabas */\n"
 "addEventListener('DOMContentLoaded',()=>{let v=null;try{v=JSON.parse(sessionStorage.getItem('gtvigo_volver')||'null')}catch(e){}\n"
 " if(!v||Date.now()-v.t>120000||window.__SALTO)return;window.__VOLVER=v;const t0=Date.now();\n"
 " const paso=()=>{const j=document.getElementById('selzJugar');if(j&&!j.disabled&&window.__volverEmpezar){try{sessionStorage.removeItem('gtvigo_volver')}catch(e){}const o=j.onclick;j.onclick=()=>window.__volverEmpezar(v.x,v.y);try{j.click()}finally{j.onclick=o}return}\n"
 "  if(Date.now()-t0<60000)setTimeout(paso,200);else window.__VOLVER=null};setTimeout(paso,200)});\n"
 "addEventListener('DOMContentLoaded',()=>{const b=document.getElementById('bCal');if(!b)return;")
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '__volverEmpezar' in s:print('ya estaba',f);continue
    for a,b in [(MOD_OLD,MOD_NEW),(SP_OLD,SP_NEW),(SAVE_OLD,SAVE_NEW),(RES_OLD,RES_NEW)]:
        assert s.count(a)==1,(f,s.count(a),a[:70]);s=s.replace(a,b)
    open(f,'w',encoding='utf8').write(s);print('ok volver',f)
