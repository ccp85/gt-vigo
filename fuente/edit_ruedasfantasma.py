import sys,os
# ================= SIN SEMICÍRCULOS NARANJAS BAJO LAS RUEDAS =================
# La silueta naranja que deja ver el coche cuando un edificio lo tapa («fantasma», se dibuja solo donde algo está delante)
# también salía en la parte de las ruedas que queda por debajo del asfalto: medio círculo naranja bajo cada rueda.
# Ahora las ruedas (cilindros: neumático, llanta y tapacubos) no forman parte de la silueta; la carrocería sigue viéndose
# a través de los edificios igual que antes. Toca las cinco páginas (coche inicial y vestirCoche).
A1="car.children.filter(m=>m.name!=='haz').forEach(m=>{const c=new THREE.Mesh(m.geometry,ghost);"
B1="car.children.filter(m=>m.name!=='haz'&&!(m.geometry&&m.geometry.type==='CylinderGeometry')).forEach(m=>{const c=new THREE.Mesh(m.geometry,ghost);"
A2="car.children.forEach(m=>{if(m.isMesh&&m.name!=='sombra'&&m.name!=='haz'){const c=new THREE.Mesh(m.geometry,ghost);"
B2="car.children.forEach(m=>{if(m.isMesh&&m.name!=='sombra'&&m.name!=='haz')m.renderOrder=2;if(m.isMesh&&m.name!=='sombra'&&m.name!=='haz'&&m.geometry.type!=='CylinderGeometry'){const c=new THREE.Mesh(m.geometry,ghost);"
for f in (sys.argv[1:] or [x for x in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(x)]):
    s=open(f,encoding='utf-8').read()
    if B2 in s: print('ya estaba',f); continue
    for a in (A1,A2): assert s.count(a)==1,(f,a[:50])
    s=s.replace(A1,B1).replace(A2,B2); open(f,'w',encoding='utf-8').write(s); print('ok ruedas',f)
