// ---------- coches del tráfico más ligeros (gpu_coches.js, solo gpu.html) ----------
// Cada coche del tráfico se construye con muchas piezas (carrocería, cristales, ruedas, llantas, faros, pilotos, retrovisores...):
// entre 17 y 58 mallas que el motor dibujaba una a una, y otra vez para las sombras. Al crearlo se juntan todas las piezas que
// comparten material en una sola malla (una por material: pintura, cristal, goma, cromo, faros...), así que cada coche pasa
// a dibujarse de 6 a 15 veces en vez de 17 a 58. Se ve igual: los faros y pilotos siguen encendiéndose de noche y las sirenas
// destellando porque el material es el mismo. El haz de los faros y la sombra quedan aparte. Al subirte a un coche del
// tráfico se le devuelven sus piezas de siempre. Con window.__COCHES_PIEZAS=true (antes de jugar) no se juntan.
const AVH={n:0,antes:0,despues:0};window.__AVH=AVH;
function aplanaVeh(g){try{if(!g||window.__COCHES_PIEZAS||g.userData.piezas)return g;
 g.updateMatrixWorld(true);const inv=g.matrixWorld.clone().invert(),grupos=new Map(),fuera=[];let n=0;
 g.traverse(o=>{if(!o.isMesh||o===g)return;n++;
  if(o.isInstancedMesh||o.isSkinnedMesh||Array.isArray(o.material)||o.name==='haz'||o.name==='sombra'||!o.visible||o.morphTargetInfluences||o.children.length){fuera.push(o);return}
  const k=o.material.uuid;let q=grupos.get(k);if(!q)grupos.set(k,q={mat:o.material,ms:[],nom:''});q.ms.push(o);if(o.name==='carroceria')q.nom='carroceria'});
 if(n<6)return g;
 const nuevas=[];
 for(const q of grupos.values()){if(q.ms.length<2){continue}
  const gs=q.ms.map(o=>{let ge=o.geometry.clone();const M=inv.clone().multiply(o.matrixWorld);ge.applyMatrix4(M);
   if(M.determinant()<0){ge=ge.index?ge.toNonIndexed():ge;for(const a of Object.values(ge.attributes)){const s=a.itemSize,A=a.array;for(let t=0;t<a.count;t+=3)for(let c=0;c<s;c++){const x=A[(t+1)*s+c];A[(t+1)*s+c]=A[(t+2)*s+c];A[(t+2)*s+c]=x}}}
   return ge});
  const comunes=Object.keys(gs[0].attributes).filter(k=>gs.every(ge=>ge.attributes[k]&&ge.attributes[k].itemSize===gs[0].attributes[k].itemSize));
  const todosIdx=gs.every(ge=>ge.index);
  const listos=gs.map(ge=>{let x=todosIdx?ge:(ge.index?ge.toNonIndexed():ge);for(const k of Object.keys(x.attributes))if(!comunes.includes(k))x.deleteAttribute(k);x.morphAttributes={};return x});
  const mg=mergeGeometries(listos,false);listos.forEach(x=>x.dispose());if(!mg)continue;
  const m=new THREE.Mesh(mg,q.mat);m.name=q.nom||'pieza';m.castShadow=q.ms.some(o=>o.castShadow);m.receiveShadow=q.ms.some(o=>o.receiveShadow);m.userData.junta=1;
  nuevas.push({m,ms:q.ms})}
 if(!nuevas.length)return g;
 const sacadas=[];for(const x of nuevas)for(const o of x.ms){sacadas.push([o,o.parent]);o.parent.remove(o)}
 for(const x of nuevas)g.add(x.m);
 g.userData.piezas={sacadas,juntas:nuevas.map(x=>x.m)};
 AVH.n++;AVH.antes+=n;let d=0;g.traverse(o=>{if(o.isMesh)d++});AVH.despues+=d;
 return g}catch(e){console.warn('aplanaVeh',e);return g}}
// devuelve las piezas originales (para subirse al coche: vestirCoche copia las piezas de una en una)
function desaplanaVeh(g){const P_=g&&g.userData.piezas;if(!P_)return g;
 for(const m of P_.juntas){g.remove(m);m.geometry.dispose()}
 for(const[o,p]of P_.sacadas)p.add(o);
 delete g.userData.piezas;return g}
// ---------- fin de gpu_coches.js
