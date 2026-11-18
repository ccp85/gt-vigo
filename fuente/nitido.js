// ---------- MÓVIL NÍTIDO (window.LITE) ----------
// Antes, para ir fluido, el móvil dibujaba a muy poca resolución (1 punto de imagen por cada 3 de pantalla, y si iba justo, la mitad):
// se veía pixelado. Ahora la resolución no baja de 1 (y sube hasta 1,5 si hay margen) con antialias, y el coste se recorta en los
// materiales: las superficies de las zonas pasan de material «físico» (brillos y reflejos calculados en cada punto) a uno mate
// (MeshLambertMaterial), que cuesta mucho menos por punto y en esta maqueta de colores planos se ve casi igual.
// · Solo piezas de las zonas, sus extras y los lotes (no coches ni personajes). No se tocan materiales con su propio sombreado
//   de brillo (asfalto mojado, charcos), ni los que llevan mapa de luz o de reflejo.
// · El material mate comparte con el original color, brillo propio, opacidad, textura…: lo que el juego cambie en el original
//   (luces de noche, parpadeos) se ve igual. Si el original se descarta, el mate también.
// · Texturas muy grandes (más de 1536 px de lado, p. ej. el plano de la maqueta) se reducen a 1536: menos memoria.
if(window.LITE)(()=>{
 const T=THREE,MATE=new WeakMap(),NO=new WeakSet(),TEXOK=new WeakSet();
 // sin comprobar cada sombreado al compilarlo: esa comprobación obliga a esperar a la GPU y da tirones al entrar en zonas nuevas
 R.debug.checkShaderErrors=false;
 const BRILLO=/pud|wW|lights_physical|clearcoat/;
 const COMP=['opacity','transparent','visible','emissiveIntensity','map','alphaMap','aoMap','alphaTest','side','depthWrite','depthTest','vertexColors','flatShading','fog','polygonOffset','polygonOffsetFactor','polygonOffsetUnits','toneMapped','blending','colorWrite','wireframe','name'];
 function apto(m){if(!m||!m.isMeshStandardMaterial||m.isMeshPhysicalMaterial||NO.has(m))return false;
  if(m.lightMap||m.envMap||m.userData&&m.userData.noMate)return false;
  if(Object.prototype.hasOwnProperty.call(m,'onBeforeCompile')&&BRILLO.test(m.onBeforeCompile.toString())){NO.add(m);return false}return true}
 function mate(m){let l=MATE.get(m);if(l)return l;
  l=new T.MeshLambertMaterial();l.color=m.color;l.emissive=m.emissive;l.userData=m.userData;
  if(m.defines){const d={...m.defines};delete d.STANDARD;delete d.PHYSICAL;if(Object.keys(d).length)l.defines=d}
  for(const k of COMP)Object.defineProperty(l,k,{configurable:true,enumerable:true,get(){return m[k]},set(v){m[k]=v}});
  // needsUpdate del original también recompila el mate
  let pv=0;Object.defineProperty(l,'version',{configurable:true,get(){return m.version+pv},set(v){pv=v-m.version}});
  if(Object.prototype.hasOwnProperty.call(m,'onBeforeCompile'))l.onBeforeCompile=m.onBeforeCompile;
  if(Object.prototype.hasOwnProperty.call(m,'customProgramCacheKey'))l.customProgramCacheKey=m.customProgramCacheKey;
  m.addEventListener('dispose',()=>l.dispose());MATE.set(m,l);return l}
 const conv=m=>apto(m)?mate(m):m;
 function tex(t){if(!t||TEXOK.has(t))return;TEXOK.add(t);const im=t.image;if(!im||t.isRenderTargetTexture||t.isDataTexture||t.isCompressedTexture||t.isVideoTexture||t.isCanvasTexture)return;
  const w=im.width,h=im.height;if(!(w>1536||h>1536))return;const k=1536/Math.max(w,h);
  try{const c=document.createElement('canvas');c.width=Math.round(w*k);c.height=Math.round(h*k);c.getContext('2d').drawImage(im,0,0,c.width,c.height);t.image=c;t.needsUpdate=true}catch(e){}}
 function pasa(o){if(!o.material||o.isSprite||o.isPoints||o.isLine)return;
  if(Array.isArray(o.material)){let c=false;const a=o.material.map(m=>{const n=conv(m);if(n!==m)c=true;tex(m.map);return n});if(c)o.material=a}
  else{tex(o.material.map);const n=conv(o.material);if(n!==o.material)o.material=n}}
 function raices(){const L=ZROOTS.map(z=>z.root||z);for(const c of scene.children)if(/_extras$|^lite_lotes$/.test(c.name||''))L.push(c);return L}
 // poco a poco: unas zonas cada vez, sin parones
 let cola=[],ci=0;
 setInterval(()=>{const t0=performance.now();if(ci>=cola.length){cola=[];for(const r of raices())if(r&&r.traverse)r.traverse(o=>{if(o.material)cola.push(o)});ci=0}
  while(ci<cola.length&&performance.now()-t0<4)pasa(cola[ci++])},250);
 window.__NITIDO=()=>({pr:+R.getPixelRatio().toFixed(2),aa:R.getContext().getContextAttributes().antialias});
})();
