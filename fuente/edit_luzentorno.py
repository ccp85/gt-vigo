import os
# ================= LUZ DEL ENTORNO EN TODO EL MUNDO (iluminación basada en imagen) =================
# Hasta ahora edificios, suelo, árboles y personajes se iluminaban con el sol y una luz ambiente plana (hemisferio: un color
# arriba y otro abajo). Ahora, en el ordenador, todo el mundo se ilumina también con la foto de 6 caras que se hace alrededor
# de tu vehículo (edit_reflejos.py, ya suavizada con PMREM): cada superficie recibe la luz del cielo y de lo que tiene al lado,
# así las fachadas se tiñen de azul de día, de naranja al atardecer, de las ventanas y farolas encendidas de noche, del verde
# del césped por abajo, y los materiales brillantes (cristales, metales, agua) reflejan algo de la ciudad.
#  - Para no quemar ni teñir de azul la imagen, la foto entra a media fuerza (envMapIntensity .5 en los materiales sin reflejo
#    propio) y la luz de hemisferio baja al 60 % mientras está puesta (entra y sale suave en ~1 s).
#  - Solo jugando (coche, moto, a pie, helicóptero…); en la vista de maqueta vuelve la luz de siempre.
#  - Como la foto se rehace también al iluminar, la luz rebota un poco de una superficie a otra (un «rebote» barato).
#  - Los coches siguen con sus reflejos propios. En el móvil (LITE) no cambia nada.
# Va después de edit_reflejos.py y edit_charcos.py; toca las cinco páginas.
A="cielo(dt);nubesTick(dt,t);tiempoTick(dt,t);"
B="cielo(dt);nubesTick(dt,t);tiempoTick(dt,t);luzEntorno(dt);"
ANCLA="function reflejosCoches(){"
FN=r'''// ---------- luz del entorno en todo el mundo (edit_luzentorno.py): la foto de 6 caras ilumina edificios, suelo y árboles
const LUZE={k:0,i:.5,t:0};window.LUZE=LUZE;
function luzEntorno(dt){const ok=!window.LITE&&!RCUBO.mal&&RCUBO.out&&driving&&!LUZE.off;
 LUZE.k=THREE.MathUtils.clamp(LUZE.k+(ok?1:-1)*Math.min(dt,.1)*1.2,0,1);
 const tex=LUZE.k>0&&RCUBO.out?RCUBO.out.texture:null;if(scene.environment!==tex)scene.environment=tex;
 if(LUZE.k>0){hemi.intensity*=1-.4*LUZE.k;
  // la foto entra a media fuerza en los materiales que no tienen reflejo propio (repasa la escena cada 2 s por las zonas que van cargando)
  const t=performance.now();if(t-LUZE.t>2000){LUZE.t=t;scene.traverse(o=>{if(!o.isMesh)return;for(const m of Array.isArray(o.material)?o.material:[o.material])
   if(m&&m.isMeshStandardMaterial&&!m.envMap&&!m.userData.luze){m.userData.luze=1;m.envMapIntensity=LUZE.i}})}}}
'''
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'function luzEntorno(' in s:print('ya estaba',f);continue
    for a in (A,ANCLA):assert s.count(a)==1,(f,a)
    s=s.replace(A,B).replace(ANCLA,FN+ANCLA);open(f,'w',encoding='utf-8').write(s);print('ok luzentorno',f)
