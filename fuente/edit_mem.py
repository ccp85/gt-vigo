import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------------- cola de colisiones (BVH): sin piezas de zonas ya descargadas, más rápida y empezando por lo cercano
r("function pasoBVH(){const o=BVHQ.shift();if(!o){bvhOn=false;subeZonas();return}let rr=o;while(rr.parent)rr=rr.parent;if(rr===scene){try{o.geometry.computeBoundsTree()}catch(e){};if(o.userData.suelo)GROUND.push(o);else window.OBST=(window.OBST||[]).concat(o)}setTimeout(pasoBVH,o.userData.suelo?16:60)}",
r"""function pasoBVH(){const t0=performance.now();
 for(;;){if(!BVHQ.length){bvhOn=false;subeZonas();return}
  // primero el suelo; después, el edificio o pieza más cercano a donde estás
  let i=BVHQ.findIndex(o=>o.userData.suelo);
  if(i<0){const fx=driving?P.x:ctl.target.x,fy=driving?P.y:ctl.target.z;let bd=1e18;i=0;
   for(let k=0;k<BVHQ.length;k++){const o=BVHQ[k];let c=o.userData.bc;if(!c){const g=o.geometry;if(!g.boundingSphere)g.computeBoundingSphere();o.updateMatrixWorld(true);c=o.userData.bc=g.boundingSphere.center.clone().applyMatrix4(o.matrixWorld)}const d=(c.x-fx)**2+(c.z-fy)**2;if(d<bd){bd=d;i=k}}}
  const o=BVHQ.splice(i,1)[0];let rr=o;while(rr.parent)rr=rr.parent;if(rr!==scene)continue;          // de una zona ya descargada: fuera, sin esperar
  try{o.geometry.computeBoundsTree()}catch(e){}if(o.userData.suelo)GROUND.push(o);else(window.OBST=window.OBST||[]).push(o);
  if(performance.now()-t0>8)break}
 setTimeout(pasoBVH,16)}""")
# al descargar una zona, quitar sus piezas de las colas (si no, seguían ocupando memoria y retrasando la zona nueva)
r("for(let i=GROUND.length-1;i>=0;i--)if(fuera.has(GROUND[i]))GROUND.splice(i,1);",
  "for(let i=GROUND.length-1;i>=0;i--)if(fuera.has(GROUND[i]))GROUND.splice(i,1);\n for(let i=BVHQ.length-1;i>=0;i--)if(fuera.has(BVHQ[i]))BVHQ.splice(i,1);SUBE.cola=SUBE.cola.filter(o=>!fuera.has(o));")
# zona que falla 3 veces (p. ej. se corta la conexión del móvil): antes quedaba perdida hasta recargar; ahora se reintenta a los 20 s
r("ZEST[id]=ZFALLOS[id]<3?null:'fallo';","ZEST[id]=ZFALLOS[id]<3?null:'fallo';if(ZEST[id]==='fallo')setTimeout(()=>{if(ZEST[id]==='fallo'){ZEST[id]=null;ZFALLOS[id]=0}},20000);")
# al descargar una zona, liberar también los búferes de las mallas instanciadas (árboles, farolas, toldos…) en la tarjeta gráfica
r("const fuera=new Set();root.traverse(o=>{if(o.isMesh){fuera.add(o);o.geometry?.disposeBoundsTree?.();o.geometry?.dispose();",
  "const fuera=new Set();root.traverse(o=>{if(o.isMesh){fuera.add(o);if(o.isInstancedMesh)o.dispose();o.geometry?.disposeBoundsTree?.();o.geometry?.dispose();")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok mem')
