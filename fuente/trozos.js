// ---------- trozos (edit_trozos.py): en el móvil (LITE) no se manda a la tarjeta el relieve lejano cuando la vista no llega
// hasta él (107 000 triángulos que se recortaban enteros) y las piezas enormes de cada zona (aceras, calzada, líneas, tierra,
// verde, faldón, piezas…) se dibujan por trozos de TROZO u (10 u, unos 640 m; más pequeños dan demasiadas piezas que dibujar), para que la tarjeta solo procese los que se ven.
// La pieza original se queda donde estaba (colisiones, rayos y quien la tenga guardada siguen igual) pero ya no se dibuja:
// su material pasa a uno invisible. Los trozos son hijos suyos, comparten sus vértices (solo tienen su propia lista de
// triángulos: casi no gastan memoria) y heredan su visibilidad. Los rayos no ven los trozos.
// Gama baja (calidad Baja): la decoración (piezas_*) va en trozos de 4 u y solo se dibuja a menos de ~4 u (unos 250 m).
(()=>{if(!window.LITE||/[?&]trozos=0/.test(location.search))return;
 const TROZO=10,MIN_TRI=12000,HECHO=new WeakSet(),INV=new Map();
 // gama baja: la decoración (piezas_*: bancos, jardineras, flores, farolas…) en trozos de 4 u y solo a menos de CERCA u del coche
 const GB=!!window.GAMA_BAJA,DECO=o=>GB&&/^piezas_\d/.test(o.name),TAM=o=>DECO(o)?4:TROZO,MINT=o=>DECO(o)?3000:MIN_TRI,CERCA=4,LEJOS=[];
 const invisible=m=>{if(!INV.has(m))INV.set(m,new THREE.MeshBasicMaterial({visible:false,side:m.side}));return INV.get(m)};
 const nada=()=>{},LISTAS=new Map();
 // si a la original le cambian la geometría o la lista de triángulos, se quitan sus trozos y se vuelven a hacer
 const REH=new WeakMap();
 function rehacer(o){REH.set(o,(REH.get(o)||0)+1);for(const c of [...o.children])if(c.userData.trozo){o.remove(c);c.geometry.index=null;c.geometry.attributes={};c.geometry.dispose()}
  const real=o.userData.materialReal;delete o.material;o.material=real;delete o.userData.__matInv;o.userData.__trozosListos=false;LISTAS.delete(o);HECHO.delete(o);window.__TROZOS_REH=(window.__TROZOS_REH||0)+1}
 function revisar(){for(const [o,e] of LISTAS){if(!o.parent){LISTAS.delete(o);continue}const g=o.geometry;if(g!==e.g||g.index!==e.ix||(g.index&&g.index.version!==e.iv)||g.attributes.position.count!==e.pc)rehacer(o)}}
 function candidato(o){if(!o.isMesh||o.isInstancedMesh||o.isSkinnedMesh||o.userData.trozo||HECHO.has(o)||(REH.get(o)||0)>=2)return false;   // si su geometría cambia a menudo, se deja entera
  if(o.frustumCulled===false||o.morphTargetInfluences||o.layers.mask!==1)return false;   // las que ya van en un lote del móvil (navmovil_lotes) se quedan así
  const g=o.geometry;if(!g||!g.attributes.position||g.morphAttributes&&Object.keys(g.morphAttributes).length)return false;
  if(/agua|mar|ola|cielo|nube|lluvia|nieve/i.test(o.name)||/^calzada/.test(o.name))return false;   // la calzada tiene piezas superpuestas que dependen del orden de dibujo: entera
  const ms=Array.isArray(o.material)?o.material:[o.material];if(ms.some(m=>!m||m.isShaderMaterial||m.isRawShaderMaterial||m.visible===false||m.wireframe))return false;
  const n=(g.index?g.index.count:g.attributes.position.count)/3;if(n<MINT(o))return false;
  if(!g.boundingBox)g.computeBoundingBox();o.updateWorldMatrix(true,false);const b=g.boundingBox.clone().applyMatrix4(o.matrixWorld);return Math.max(b.max.x-b.min.x,b.max.z-b.min.z)>TAM(o)*1.5}
 function partir(o){HECHO.add(o);o.userData.noLote=true;const TS=TAM(o),deco=DECO(o);const g=o.geometry,P=g.attributes.position,N=(g.index?g.index.count:P.count);
  const idx=g.index?g.index.array:null,ix=k=>idx?idx[k]:k;o.updateWorldMatrix(true,false);const E=o.matrixWorld.elements;   // trozos en coordenadas del mundo (la pieza puede estar escalada)
  const dr=g.drawRange,D0=Math.max(0,dr.start||0),D1=Math.min(N,dr.count===Infinity?N:D0+dr.count);   // respetar el trozo de la malla que de verdad se dibuja
  const grupos=(Array.isArray(o.material)&&g.groups.length)?g.groups:[{start:D0,count:D1-D0,materialIndex:0}];
  const T=new Map();   // clave del trozo → [lista de índices por grupo]
  for(let gi=0;gi<grupos.length;gi++){const gr=grupos[gi],fin=Math.min(D1,gr.start+(gr.count===Infinity?N:gr.count));
   for(let k=Math.max(D0,gr.start);k+2<fin;k+=3){const a=ix(k),b=ix(k+1),c=ix(k+2);
    const lx=(P.getX(a)+P.getX(b)+P.getX(c))/3,ly=(P.getY(a)+P.getY(b)+P.getY(c))/3,lz=(P.getZ(a)+P.getZ(b)+P.getZ(c))/3,cx=E[0]*lx+E[4]*ly+E[8]*lz+E[12],cz=E[2]*lx+E[6]*ly+E[10]*lz+E[14];
    const key=Math.floor(cx/TS)+','+Math.floor(cz/TS);let t=T.get(key);if(!t){t=grupos.map(()=>[]);T.set(key,t)}t[gi].push(a,b,c)}}
  if(T.size<2)return;
  const grande=P.count>65535;
  for(const [key,listas] of T){const tg=new THREE.BufferGeometry();tg.attributes=g.attributes;   // el mismo diccionario: si a la original le cambian un atributo (alturas…), los trozos lo ven
   const tot=listas.reduce((s,l)=>s+l.length,0),arr=grande?new Uint32Array(tot):new Uint16Array(tot);let p=0;
   listas.forEach((l,gi)=>{if(!l.length)return;arr.set(l,p);if(grupos.length>1||Array.isArray(o.material))tg.addGroup(p,l.length,grupos[gi].materialIndex);p+=l.length});
   tg.setIndex(new THREE.BufferAttribute(arr,1));
   // caja y esfera solo con los vértices de este trozo
   let x0=1e9,y0=1e9,z0=1e9,x1=-1e9,y1=-1e9,z1=-1e9;for(let i=0;i<arr.length;i++){const v=arr[i],x=P.getX(v),y=P.getY(v),z=P.getZ(v);if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;if(z<z0)z0=z;if(z>z1)z1=z}
   tg.boundingBox=new THREE.Box3(new THREE.Vector3(x0,y0,z0),new THREE.Vector3(x1,y1,z1));tg.boundingSphere=tg.boundingBox.getBoundingSphere(new THREE.Sphere());tg.boundingSphere.radius*=1.05;
   const m=new THREE.Mesh(tg,o.material);m.userData.trozo=true;m.userData.trozoDe=o.name;   // sin nombre: hay código que busca piezas por nombre («calzada»…) y las retoca
   m.raycast=nada;m.renderOrder=o.renderOrder;m.castShadow=o.castShadow;m.receiveShadow=o.receiveShadow;
   m.onBeforeRender=o.onBeforeRender;m.onAfterRender=o.onAfterRender;o.add(m);
   if(deco){const [kx,kz]=key.split(',').map(Number);LEJOS.push([m,(kx+.5)*TS,(kz+.5)*TS])}}
  // la original sigue para colisiones y rayos, pero no se dibuja; los trozos usan su material de verdad
  const real=o.material;o.userData.materialReal=real;
  // si alguien le cambia el material a la original, se lo pasamos a los trozos
  Object.defineProperty(o,'material',{configurable:true,get(){return this.userData.__matInv},set(v){if(this.userData.__matInv===undefined||!this.userData.__trozosListos){this.userData.__matInv=v;return}
   this.userData.materialReal=v;for(const c of this.children)if(c.userData.trozo)c.material=v;this.userData.__matInv=Array.isArray(v)?v.map(invisible):invisible(v)}});
  o.userData.__matInv=Array.isArray(real)?real.map(invisible):invisible(real);o.userData.__trozosListos=true;
  LISTAS.set(o,{g,ix:g.index,iv:g.index?g.index.version:-1,pc:P.count});
  window.__TROZOS=(window.__TROZOS||0)+T.size}
 // una pieza cada 120 ms para no dar tirones al cargar una zona
 // el relieve lejano (montes de la ría) solo se dibuja más allá de uNear; si la vista acaba antes, no se manda a la tarjeta
 const fondo=()=>{try{if(typeof FONDO!=='undefined'&&FONDO.m&&window.pcam){const fuera=!!driving&&pcam.far<FONDO.U.uNear.value-.5;FONDO.m.geometry.setDrawRange(0,fuera?0:Infinity)}}catch(e){}};
 const lejos=()=>{if(!LEJOS.length||!window.pcam)return;const x=pcam.position.x,z=pcam.position.z;for(let i=LEJOS.length-1;i>=0;i--){const [m,cx,cz]=LEJOS[i];if(!m.parent){LEJOS.splice(i,1);continue}m.visible=Math.hypot(cx-x,cz-z)<CERCA+2.9}};
 const cola=[];setInterval(()=>{fondo();revisar();lejos();if(!cola.length){scene.traverse(o=>{if(candidato(o))cola.push(o)});return}
  const t0=performance.now();while(cola.length&&performance.now()-t0<12){const o=cola.shift();if(o.parent&&candidato(o))try{partir(o)}catch(e){HECHO.add(o);console.warn('trozos',o.name,e)}}},120);
})();
