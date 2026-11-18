// ---------- MUNDO ABIERTO EN EL MÓVIL (window.LITE) ----------
// En la vista de maqueta cada trozo de arbolado y de farolas de cada zona se dibujaba por separado: en el centro, con el puerto,
// más de 1.000 piezas por imagen solo de árboles y farolas (1.600 en total). Aquí se juntan en una sola pieza por tipo y zona
// (en total, de unas 1.600 a unas 630). Las piezas originales siguen en la escena para los choques; solo deja de dibujarlas la
// cámara, con la misma marca que usan los lotes (capa 1<<30). Al conducir se deshace (allí ya se recortan por distancia), y si una
// pieza original cambia (se mueve, se oculta, cambia de forma) la junta de esa zona se rehace.
// (el suelo de cada zona ya se trocea en navmovil_lotes.js)
if(window.LITE)(()=>{
 const HID=1<<30,noop=()=>{};
 const JUN=new Map(),MIAS=new WeakSet();   // raíz -> {mallas juntas, piezas de origen, n}; MIAS: piezas que ocultamos aquí
 const fIM=l=>l.map(o=>o.uuid+':'+o.count+':'+o.instanceMatrix.version+':'+(o.instanceColor?o.instanceColor.version:'-')+':'+o.visible+':'+o.geometry.uuid+':'+o.layers.mask).join(',');
 function fuentes(r){const L=[];r.traverse(o=>{if(o.isInstancedMesh&&!o.isSkinnedMesh&&o.parent===r&&!Array.isArray(o.material)&&o.count>0&&o.visible&&!o.userData.juntaLite&&!o.material.transparent&&(o.layers.mask===1||(o.layers.mask===HID&&MIAS.has(o))))L.push(o)});return L}
 function deshacer(r){const e=JUN.get(r);if(!e)return;JUN.delete(r);for(const m of e.mallas){m.removeFromParent();m.dispose()}for(const o of e.fuentes)if(MIAS.has(o)){MIAS.delete(o);if(o.layers.mask===HID)o.layers.mask=1}}
 function juntar(r,L){const grupos=new Map();for(const o of L){const k=o.geometry.uuid+'|'+o.material.uuid+'|'+(!!o.instanceColor);let g=grupos.get(k);if(!g)grupos.set(k,g=[]);g.push(o)}
  const mallas=[],fu=[];r.updateMatrixWorld();const inv=new THREE.Matrix4().copy(r.matrixWorld).invert(),M=new THREE.Matrix4(),R=new THREE.Matrix4(),C=new THREE.Color();
  for(const g of grupos.values()){if(g.length<3)continue;const n=g.reduce((a,o)=>a+o.count,0);
   const im=new THREE.InstancedMesh(g[0].geometry,g[0].material,n);im.name='junta_lite';im.userData.juntaLite=1;im.userData.noLote=1;im.raycast=noop;
   im.castShadow=g[0].castShadow;im.receiveShadow=g[0].receiveShadow;let k=0;
   for(const o of g){R.multiplyMatrices(inv,o.matrixWorld);for(let i=0;i<o.count;i++){o.getMatrixAt(i,M);M.premultiply(R);im.setMatrixAt(k,M);if(o.instanceColor){o.getColorAt(i,C);im.setColorAt(k,C)}k++}fu.push(o)}
   im.computeBoundingSphere();r.add(im);mallas.push(im)}
  if(!mallas.length)return;for(const o of fu){o.layers.mask=HID;MIAS.add(o)}JUN.set(r,{mallas,fuentes:fu,n:L.length})}
 function maqueta(){
  for(const [r,e] of [...JUN]){if(!r.parent||driving){deshacer(r);continue}
   const ok=e.fuentes.every(o=>o.parent===r&&o.visible&&o.layers.mask===HID)&&fIM(e.fuentes)===e.firmaH&&fuentes(r).length===e.n;if(!ok)deshacer(r)}
  if(driving)return;
  // raíces de zona y grupos de extras de cada zona (puerto_extras...: arbolado y farolas del paseo)
  const RS=ZROOTS.map(z=>z.root||z);for(const c of scene.children)if(/_extras$/.test(c.name||''))RS.push(c);
  for(const r of RS){if(!r||!r.traverse||JUN.has(r))continue;const L=fuentes(r);if(L.length<6)continue;juntar(r,L);const e=JUN.get(r);if(e)e.firmaH=fIM(e.fuentes)}}
 setInterval(maqueta,1000);
 window.__MUNDOM=()=>({juntas:[...JUN.values()].reduce((a,e)=>a+e.mallas.length,0),fuentes:[...JUN.values()].reduce((a,e)=>a+e.fuentes.length,0)});
 // la maqueta del móvil no se aleja tanto (con todo Vigo en pantalla se cargan demasiadas zonas a la vez)
 ctl.minZoom=1.3;
})();
