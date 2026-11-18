// ---------- MÓVIL (window.LITE): agrupar en lotes lo que no se mueve ----------
// En el móvil lo que más cuesta no son los triángulos sino el número de piezas que se dibujan por separado (más de 1.000 por
// imagen en el centro). Aquí se juntan en una sola malla, por zonas de la ciudad de unos 400 m, todas las piezas quietas que
// comparten el mismo aspecto: edificios de cada color y fachada, decoración navideña, mobiliario. Las piezas originales se
// quedan en la escena para los choques y el suelo; solo dejan de dibujarse. Si una pieza se mueve, cambia de color, se oculta
// o desaparece, su lote se rehace sin ella y vuelve a dibujarse sola.
if(window.LITE)(()=>{
 const HID=1<<30,LT=THREE.Layers.prototype.test;
 // las piezas originales siguen respondiendo a los rayos (choques, suelo), pero la cámara ya no las dibuja
 THREE.Layers.prototype.test=function(l){if(this.mask===HID)return l.__cam!==true;return LT.call(this,l)};
 cam.layers.__cam=true;pcam.layers.__cam=true;
 const RAIZ=new THREE.Group();RAIZ.name='lite_lotes';scene.add(RAIZ);
 const UD_OK=new Set(['fv','real','tj','tej','cut','vit']);   // sombreados de fachada y tejado que aceptan el color por vértice
 const CEL=4,ESPERA=2200,INFO=new WeakMap(),EN=new Map(),LOTES=new Map();
 const noop=()=>{},m4=new THREE.Matrix4(),m3=new THREE.Matrix3(),v3=new THREE.Vector3();
 const propio=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
 const MAPAS=['normalMap','emissiveMap','roughnessMap','metalnessMap','alphaMap','aoMap','lightMap','bumpMap','displacementMap','envMap','specularMap','gradientMap'];
 function enEscena(o){while(o){if(!o.visible)return false;if(o===scene)return true;if(o===RAIZ)return false;o=o.parent}return false}
 const COK=new WeakMap();
 function matOK(m){if(!m||m.wireframe||m.isShaderMaterial||m.isRawShaderMaterial)return false;
  if(m.transparent&&m.blending!==THREE.AdditiveBlending)return false;
  if(!propio(m,'onBeforeCompile'))return true;let c=COK.get(m);
  if(!c||c.f!==m.onBeforeCompile){c={f:m.onBeforeCompile,ok:!/gl_InstanceID|ip=vec3\(instanceMatrix|[^\w.]position\.[xyz]/.test(m.onBeforeCompile.toString())};COK.set(m,c)}
  return c.ok}
 function cand(o){if(!o.isMesh||o.isInstancedMesh||o.isSkinnedMesh||Array.isArray(o.material))return false;
  const g=o.geometry;if(!g||!g.attributes.position||g.morphAttributes.position||g.attributes.tangent||g.attributes.skinIndex)return false;
  if(g.drawRange.start!==0||g.drawRange.count!==Infinity)return false;
  if(o.frustumCulled===false||(o.layers.mask!==1&&o.layers.mask!==HID)||propio(o,'onBeforeRender')||o.userData.noLote)return false;
  return matOK(o.material)}
 const VOL=new WeakSet(),MST=new WeakMap();
 function estMat(m){return (m.color?m.color.getHex():0)*1.3e-7+(m.emissive?m.emissive.getHex():0)*2.9e-7+m.emissiveIntensity*.37+m.opacity*.59+(m.visible?.11:0)+m.version*.013+(m.map?m.map.id*.07+m.map.offset.x*1.9+m.map.offset.y*2.3+m.map.repeat.x*3.1+m.map.repeat.y*3.7+m.map.rotation*4.1:0)}
 // un material que cambia (luces que parpadean, colores que van rotando) no se pliega: se junta tal cual y sigue animándose
 function volatil(m){const e=estMat(m),p=MST.get(m);MST.set(m,e);if(p!==undefined&&p!==e)VOL.add(m);return VOL.has(m)}
 const CPL=new WeakMap();
 function plegable(m){if(VOL.has(m))return false;const ob=propio(m,'onBeforeCompile')?m.onBeforeCompile:null,nu=m.userData?Object.keys(m.userData).length:0;let c=CPL.get(m);
  if(c&&c.ob===ob&&c.nu===nu&&c.map===m.map&&c.vc===m.vertexColors)return c.r;const r=plegable0(m);CPL.set(m,{ob,nu,map:m.map,vc:m.vertexColors,r});return r}
 function plegable0(m){if(!(m.isMeshStandardMaterial||m.isMeshLambertMaterial||m.isMeshPhongMaterial||m.isMeshBasicMaterial)||m.isMeshPhysicalMaterial)return false;
  if(m.vertexColors)return false;for(const k of MAPAS)if(m[k])return false;if(m.map&&(m.map.channel||0)!==0)return false;
  const ud=Object.keys(m.userData||{});if(propio(m,'onBeforeCompile')){if(!ud.length)return false}for(const k of ud)if(!UD_OK.has(k))return false;return true}
 function claveMat(m){if(!plegable(m))return 'M'+m.uuid;
  const t=m.map;return ['F',m.type,t?[t.source.uuid,t.wrapS,t.wrapT,t.magFilter,t.minFilter,t.anisotropy,t.colorSpace,t.flipY].join(','):'',
   m.emissive?m.emissive.getHex():'',m.emissiveIntensity,m.roughness,m.metalness,m.shininess,m.opacity,m.transparent,m.blending,m.side,m.alphaTest,m.depthWrite,m.depthTest,
   m.flatShading,m.fog,m.toneMapped,m.polygonOffset,m.polygonOffsetFactor,m.polygonOffsetUnits,JSON.stringify(m.userData),
   propio(m,'onBeforeCompile')?m.onBeforeCompile.toString().length+':'+m.onBeforeCompile.toString().slice(0,160):'',
   propio(m,'customProgramCacheKey')?m.customProgramCacheKey():''].join('|')}
 function firma(o){const m=o.material,e=o.matrixWorld.elements;let h=o.geometry.id*7.31+m.id*3.17+o.renderOrder*.53;for(let i=0;i<16;i++)h=h*1.0000013+e[i]*(i*.731+1);
  if(!plegable(m))return h;   // con el mismo material compartido, sus cambios (parpadeos, color) se ven igual en el lote
  h+=(m.color?m.color.getHex():0)*1.3e-7+(m.emissive?m.emissive.getHex():0)*2.9e-7+m.emissiveIntensity*.37+m.opacity*.59+(m.visible?.11:0)+m.version*.013;
  if(m.map){const t=m.map;h+=t.id*.07+t.offset.x*1.9+t.offset.y*2.3+t.repeat.x*3.1+t.repeat.y*3.7+t.rotation*4.1}return h}
 const MR=new THREE.Matrix4();
 function relM(o,r){return MR.copy(r.matrixWorld).invert().multiply(o.matrixWorld)}
 function firmaR(o,r){const m=o.material,e=relM(o,r).elements;let h=o.geometry.id*7.31+m.id*3.17+o.renderOrder*.53;for(let i=0;i<16;i++)h=h*1.0000013+Math.round(e[i]*2e4)*(i*.731+1);
  if(!plegable(m))return h;h+=(m.color?m.color.getHex():0)*1.3e-7+(m.emissive?m.emissive.getHex():0)*2.9e-7+m.emissiveIntensity*.37+m.opacity*.59+(m.visible?.11:0)+m.version*.013;return h}
 function raizDe(o){const p=o.parent;return p&&p!==scene&&p!==RAIZ&&!p.isScene?p:null}   // se junta con sus hermanas y viaja con el padre
 function raizEnEscena(o){while(o){if(o===scene)return true;o=o.parent}return false}
 function claveAttr(g,pl){return Object.keys(g.attributes).filter(k=>!(pl&&k==='color')).sort().map(k=>k+g.attributes[k].itemSize).join(',')+(g.index?'':'')}
 function celda(o){const g=o.geometry;if(!g.boundingSphere)g.computeBoundingSphere();v3.copy(g.boundingSphere.center).applyMatrix4(o.matrixWorld);
  return Math.floor(v3.x/CEL)+','+Math.floor(v3.z/CEL)}
 // une las piezas: posiciones y normales al mundo, uv con la transformación de la textura si el material se pliega
 function unir(srcs,pl,mat){let nv=0,ni=0;for(const o of srcs){const g=o.geometry;nv+=g.attributes.position.count;ni+=g.index?g.index.count:g.attributes.position.count}
  const g0=srcs[0].geometry,nombres=Object.keys(g0.attributes).filter(k=>!(pl&&k==='color'));
  const out={};for(const k of nombres)out[k]=new Float32Array(nv*g0.attributes[k].itemSize);
  const col=pl?new Float32Array(nv*3):null,idx=nv>65535?new Uint32Array(ni):new Uint16Array(ni);let ov=0,oi=0;
  for(const o of srcs){const g=o.geometry,P=g.attributes.position,n=P.count,mw=mat(o);m3.getNormalMatrix(mw);const flip=mw.determinant()<0;
   for(const k of nombres){const A=g.attributes[k],it=A.itemSize,D=out[k];
    const rap=!A.isInterleavedBufferAttribute&&!A.normalized&&A.array instanceof Float32Array,S=A.array;
    if(k==='position'){const e=mw.elements;for(let i=0;i<n;i++){let x,y,z;if(rap){x=S[i*3];y=S[i*3+1];z=S[i*3+2]}else{x=A.getX(i);y=A.getY(i);z=A.getZ(i)}const j=(ov+i)*3;
      D[j]=e[0]*x+e[4]*y+e[8]*z+e[12];D[j+1]=e[1]*x+e[5]*y+e[9]*z+e[13];D[j+2]=e[2]*x+e[6]*y+e[10]*z+e[14]}}
    else if(k==='normal'){const e=m3.elements;for(let i=0;i<n;i++){let x,y,z;if(rap){x=S[i*3];y=S[i*3+1];z=S[i*3+2]}else{x=A.getX(i);y=A.getY(i);z=A.getZ(i)}
      const X=e[0]*x+e[3]*y+e[6]*z,Y=e[1]*x+e[4]*y+e[7]*z,Z=e[2]*x+e[5]*y+e[8]*z,l=Math.hypot(X,Y,Z)||1,j=(ov+i)*3;D[j]=X/l;D[j+1]=Y/l;D[j+2]=Z/l}}
    else if(rap&&!(k==='uv'&&pl&&o.material.map))D.set(S.subarray(0,n*it),ov*it);
    else if(k==='uv'&&pl&&o.material.map){const t=o.material.map;if(t.matrixAutoUpdate)t.updateMatrix();const me=t.matrix.elements;
     for(let i=0;i<n;i++){const u=A.getX(i),v=A.getY(i);D[(ov+i)*2]=me[0]*u+me[3]*v+me[6];D[(ov+i)*2+1]=me[1]*u+me[4]*v+me[7]}}
    else for(let i=0;i<n;i++)for(let c=0;c<it;c++)D[(ov+i)*it+c]=A.getComponent(i,c)}
   if(col){const c=o.material.color||{r:1,g:1,b:1},F=g.attributes.fcol;
    for(let i=0;i<n;i++){const bl=F&&F.getW(i)>1.5;col[(ov+i)*3]=bl?1:c.r;col[(ov+i)*3+1]=bl?1:c.g;col[(ov+i)*3+2]=bl?1:c.b}}
   if(g.index){const I=g.index,IA=I.array;for(let i=0;i<I.count;i+=3){const a=IA[i],b=IA[i+1],c=IA[i+2];idx[oi++]=ov+a;idx[oi++]=ov+(flip?c:b);idx[oi++]=ov+(flip?b:c)}}
   else for(let i=0;i<n;i+=3){idx[oi++]=ov+i;idx[oi++]=ov+(flip?i+2:i+1);idx[oi++]=ov+(flip?i+1:i+2)}
   ov+=n}
  const geo=new THREE.BufferGeometry();for(const k of nombres){const A0=g0.attributes[k];geo.setAttribute(k,new THREE.BufferAttribute(out[k],A0.itemSize,false))}
  if(col)geo.setAttribute('color',new THREE.BufferAttribute(col,3));geo.setIndex(new THREE.BufferAttribute(idx,1));geo.computeBoundingSphere();geo.computeBoundingBox();return geo}
 function matPlegado(m){const mm=m.clone();if(propio(m,'onBeforeCompile'))mm.onBeforeCompile=m.onBeforeCompile;
  if(propio(m,'customProgramCacheKey'))mm.customProgramCacheKey=m.customProgramCacheKey;
  if(mm.color)mm.color.setRGB(1,1,1);mm.vertexColors=true;
  if(m.map){const t=m.map.clone();t.offset.set(0,0);t.repeat.set(1,1);t.rotation=0;t.center.set(0,0);t.matrixAutoUpdate=true;t.needsUpdate=true;mm.map=t}
  mm.needsUpdate=true;return mm}
 const LIB=new WeakSet();
 function soltar(o){o.layers.mask=1;EN.delete(o)}
 const fz=L=>L.r?(o=>firmaR(o,L.r)):firma;
 function rehacer(L){if(L.mesh){L.mesh.removeFromParent();L.mesh.geometry.dispose();L.mesh=null}
  L.srcs=L.srcs.filter(o=>EN.get(o)===L);
  if(L.srcs.length){const ks=claveAttr(L.srcs[0].geometry,L.pl);for(const o of L.srcs.slice())if(claveAttr(o.geometry,L.pl)!==ks){soltar(o);const I=INFO.get(o);if(I)I.cambios=9}L.srcs=L.srcs.filter(o=>EN.get(o)===L)}
  if(L.r&&!enEscena(L.r)){for(const o of L.srcs)soltar(o);L.srcs=[]}
  if(L.srcs.length<2){for(const o of L.srcs)soltar(o);L.srcs=[];if(L.mat&&L.pl){if(L.mat.map)L.mat.map.dispose();L.mat.dispose()}LOTES.delete(L.k);return}
  if(!L.mat)L.mat=L.pl?matPlegado(L.srcs[0].material):L.srcs[0].material;
  if(L.r)L.r.updateMatrixWorld(true);
  const me=new THREE.Mesh(unir(L.srcs,L.pl,L.r?(o=>relM(o,L.r)):(o=>o.matrixWorld)),L.mat);me.raycast=noop;me.name='lote';me.receiveShadow=L.srcs[0].receiveShadow;me.castShadow=L.srcs[0].castShadow;me.renderOrder=L.srcs[0].renderOrder;me.userData.noLote=1;
  const F=fz(L);me.userData.firmas=new Map(L.srcs.map(o=>[o,F(o)]));
  if(L.r){L.r.add(me)}else{me.matrixAutoUpdate=false;RAIZ.add(me)}L.mesh=me;for(const o of L.srcs){o.layers.mask=HID;if(!LIB.has(o.geometry)){LIB.add(o.geometry);o.geometry.dispose()}}}   // la copia de la pieza en la tarjeta gráfica ya no hace falta (si vuelve a dibujarse, se sube otra vez)
 // revisión: ¿alguna pieza de un lote se ha movido, ocultado o ya no está? (por turnos, unos pocos lotes cada vez)
 function revisa1(L){if(!L.mesh||LOTES.get(L.k)!==L)return;const FS=L.mesh.userData.firmas,F=fz(L);let mal=false;
  if(L.r&&!enEscena(L.r)){if(L.r.parent&&raizEnEscena(L.r))return;for(const o of L.srcs)soltar(o);rehacer(L);return}   // coche oculto: el lote se queda dentro y se oculta con él
  for(const [o,f0] of FS){if(EN.get(o)!==L)continue;const fuera=L.r?(!o.visible||raizDe(o)!==L.r||!enEscena(o)):!enEscena(o);
   const vo=L.pl&&volatil(o.material);if(fuera||vo||F(o)!==f0){soltar(o);const I=(L.r?INFR:INFO).get(o);if(I){if(!vo)I.cambios++;I.t=performance.now();I.f=F(o)}mal=true}}
  if(mal)COLA.add(L)}
 // búsqueda lenta: piezas quietas desde hace un rato que aún no están en un lote; las que se mueven con su grupo
 // (coches, carrozas, barcos) se juntan dentro del grupo y viajan con él
 const INFR=new WeakMap();
 let BUS=null,BI=0,NUEV=new Map();
 function busca1(o,ahora){if(o.isInstancedMesh){dieta(o);return}if(EN.has(o)||!cand(o)||!enEscena(o))return;let I=INFO.get(o);if(I&&I.no)return;
  const vo0=VOL.has(o.material),vo=volatil(o.material);const f=firma(o);if(vo&&!vo0&&I){I.f=f;I.t=ahora;I.cambios=0;return}
  if(!I){INFO.set(o,{f,t:ahora,cambios:0});return}
  if(I.f!==f){I.f=f;I.t=ahora;I.cambios++}
  if(grande(o)){if(I.cambios===0&&ahora-I.t>=ESPERA)COLAT.add(o);return}
  const mete=(k,pl,r)=>(NUEV.get(k)||NUEV.set(k,{pl,r,l:[]}).get(k)).l.push(o);
  const pl=plegable(o.material),ka=claveMat(o.material)+'#'+claveAttr(o.geometry,pl)+'#'+o.receiveShadow+'#'+o.castShadow+'#'+o.renderOrder;
  if(I.cambios<=2){if(I.f===f&&ahora-I.t>=ESPERA*(1+I.cambios*3))mete(ka+'#'+celda(o),pl,null);return}
  const r=raizDe(o);if(!r){I.no=true;return}const fr=firmaR(o,r);let J=INFR.get(o);
  if(!J||J.r!==r){INFR.set(o,{f:fr,t:ahora,cambios:0,r});return}
  if(J.f!==fr){J.f=fr;J.t=ahora;J.cambios++;if(J.cambios>6)I.no=true;return}
  if(J.cambios>2||ahora-J.t<ESPERA*(1+J.cambios*3))return;
  mete('R'+r.id+'#'+ka,pl,r)}
 // cada lote, como mucho unos 24.000 vértices: montarlo cuesta poco y lo que llega después va a un lote nuevo (no se rehace el grande)
 let SER=0;const TOPE=24000;
 function buscaFin(){for(const [k,{pl,r,l}] of NUEV){if(l.length<2)continue;let L=null,nv=0;
   for(const o of l){const v=o.geometry.attributes.position.count;if(!L||nv+v>TOPE){if(L&&L.srcs.length<2){for(const q of L.srcs)EN.delete(q);LOTES.delete(L.k);COLA.delete(L)}L={k:k+'|'+(SER++),pl,r,srcs:[],mesh:null,mat:null};LOTES.set(L.k,L);COLA.add(L);nv=0}
    L.srcs.push(o);EN.set(o,L);nv+=v}
   if(L&&L.srcs.length<2){for(const q of L.srcs)EN.delete(q);LOTES.delete(L.k);COLA.delete(L)}}NUEV=new Map()}
 // los lotes se montan poco a poco (unos milisegundos cada vez) para que no se note un parón al entrar en una zona

 // ---- suelos enteros de una zona (aceras, calzada, tierra…: hasta 200.000 triángulos en una sola pieza que abarca 4 km)
 // se trocean en cuadros de unos 600 m: así solo se dibuja lo que entra en la cámara y no la zona entera
 let TRZ=null;const TC=9,TROZ=new Map(),COLAT=new Set(),GRA=new WeakMap();
 function grande(o){let r=GRA.get(o.geometry);if(r===undefined){const g=o.geometry,n=(g.index?g.index.count:g.attributes.position.count)/3;if(!g.boundingSphere)g.computeBoundingSphere();
   r=n>12000&&g.boundingSphere.radius*o.matrixWorld.getMaxScaleOnAxis()>8;GRA.set(o.geometry,r)}return r}
 function* trocear(o){const g=o.geometry,P=g.attributes.position,IX=g.index,nt=(IX?IX.count:P.count)/3,mw=o.matrixWorld,e=mw.elements;m3.getNormalMatrix(mw);
  const nombres=Object.keys(g.attributes),vi=k=>IX?IX.getX(k):k,celdas=new Map(),flip=mw.determinant()<0;
  for(let t=0;t<nt;t++){let cx=0,cz=0;for(let j=0;j<3;j++){const v=vi(t*3+j),x=P.getX(v),y=P.getY(v),z=P.getZ(v);cx+=e[0]*x+e[4]*y+e[8]*z+e[12];cz+=e[2]*x+e[6]*y+e[10]*z+e[14]}
   const k=Math.floor(cx/3/TC)+','+Math.floor(cz/3/TC);let a=celdas.get(k);if(!a)celdas.set(k,a=[]);a.push(t);if((t&4095)===4095)yield}
  const G=new THREE.Group();G.name='trozos';G.matrixAutoUpdate=false;
  for(const ts of celdas.values()){const nv=ts.length*3,out={};for(const n of nombres)out[n]=new Float32Array(nv*g.attributes[n].itemSize);let w=0;
   for(const t of ts)for(let j0=0;j0<3;j0++){const v=vi(t*3+(flip?(3-j0)%3:j0));
    for(const n of nombres){const A=g.attributes[n],it=A.itemSize,D=out[n];
     if(n==='position'){const x=A.getX(v),y=A.getY(v),z=A.getZ(v);D[w*3]=e[0]*x+e[4]*y+e[8]*z+e[12];D[w*3+1]=e[1]*x+e[5]*y+e[9]*z+e[13];D[w*3+2]=e[2]*x+e[6]*y+e[10]*z+e[14]}
     else if(n==='normal'){v3.fromBufferAttribute(A,v).applyMatrix3(m3).normalize();D[w*3]=v3.x;D[w*3+1]=v3.y;D[w*3+2]=v3.z}
     else for(let c=0;c<it;c++)D[w*it+c]=A.getComponent(v,c)}
    w++}
   const gg=new THREE.BufferGeometry();for(const n of nombres)gg.setAttribute(n,new THREE.BufferAttribute(out[n],g.attributes[n].itemSize));gg.computeBoundingSphere();
   const me=new THREE.Mesh(gg,o.material);me.matrixAutoUpdate=false;me.raycast=noop;me.userData.noLote=1;me.receiveShadow=o.receiveShadow;me.renderOrder=o.renderOrder;G.add(me);yield}
  if(!enEscena(o)||EN.has(o)){for(const m of G.children)m.geometry.dispose();return}
  RAIZ.add(G);o.layers.mask=HID;EN.set(o,'T');TROZ.set(o,{G,f:firma(o)});if(!LIB.has(g)){LIB.add(g);g.dispose()}}
 function quitaTrozos(o,T){T.G.removeFromParent();for(const m of T.G.children)m.geometry.dispose();TROZ.delete(o);if(EN.get(o)==='T')soltar(o)}
 function revisaT(){for(const [o,T] of TROZ){if(!enEscena(o)){quitaTrozos(o,T);continue}if(firma(o)!==T.f){quitaTrozos(o,T);const I=INFO.get(o);if(I)I.no=true}}}
 // ---- figuras repetidas miles de veces (público, bombillas, aros de luz): la misma forma con menos caras
 const DIET=new WeakSet(),DG=new WeakMap();
 function dieta(o){if(DIET.has(o))return;DIET.add(o);const g=o.geometry,p=g&&g.parameters;if(!p)return;let n=DG.get(g);
  if(n===undefined){n=null;try{
   if(g.type==='SphereGeometry'&&p.widthSegments>6)n=new THREE.SphereGeometry(p.radius,6,Math.min(p.heightSegments,4),p.phiStart,p.phiLength,p.thetaStart,p.thetaLength);
   else if(g.type==='TorusGeometry'&&(p.tubularSegments>10||p.radialSegments>4))n=new THREE.TorusGeometry(p.radius,p.tube,Math.min(4,p.radialSegments),Math.min(10,p.tubularSegments),p.arc);
   else if(g.type==='CylinderGeometry'&&p.radialSegments>6)n=new THREE.CylinderGeometry(p.radiusTop,p.radiusBottom,p.height,6,1,p.openEnded,p.thetaStart,p.thetaLength);
   else if(g.type==='ConeGeometry'&&p.radialSegments>6)n=new THREE.ConeGeometry(p.radius,p.height,6,1,p.openEnded,p.thetaStart,p.thetaLength)}catch(e){n=null}
   if(n)for(const k in g.attributes)if(!n.attributes[k]){n.dispose();n=null;break}   // con atributos propios no se toca
   DG.set(g,n)}
  if(n)o.geometry=n}

 // ---- calidad automática: si el móvil no llega a ~22 imágenes por segundo, se baja un escalón (nunca se vuelve a subir)
 // 1: se ve menos lejos (más niebla) y resolución 0,9 como mucho · 2: aún menos lejos y resolución 0,75 · 3: además se quita el público de las aceras
 // (antes bajaba hasta 0,55 y se veía muy pixelado)
 const NV={n:0,t:performance.now()+12000,f0:R.info.render.frame,malos:0,pr:9,lejos:99};
 {const sp=R.setPixelRatio.bind(R);R.setPixelRatio=v=>sp(Math.min(v,NV.pr))}
 {let fv=pcam.far;Object.defineProperty(pcam,'far',{configurable:true,get(){return Math.min(fv,NV.lejos)},set(v){fv=v}})}
 const nieblaCorta=()=>{for(const F of [scene.fog,typeof FOG!=='undefined'?FOG:null])if(F&&F.isFog&&!F.__nv){F.__nv=1;let fv=F.far,nv=F.near;
   Object.defineProperty(F,'far',{configurable:true,get(){return Math.min(fv,NV.lejos-1.5)},set(v){fv=v}});
   Object.defineProperty(F,'near',{configurable:true,get(){return Math.min(nv,(NV.lejos-1.5)*.35)},set(v){nv=v}})}};
 function escalon(){NV.n++;if(NV.n===1){NV.pr=.9;NV.lejos=14;nieblaCorta();pcam.updateProjectionMatrix()}else if(NV.n===2){NV.pr=.75;NV.lejos=11;pcam.updateProjectionMatrix()}
  else if(NV.n===3){NV.lejos=9.5;pcam.updateProjectionMatrix();scene.traverse(o=>{if(o.isInstancedMesh&&o.count>1500&&o.frustumCulled===false)o.layers.mask=HID})}
  R.setPixelRatio(R.getPixelRatio()>NV.pr?NV.pr:R.getPixelRatio());window.dispatchEvent(new Event('resize'))}
 setInterval(()=>{const a=performance.now(),fr=R.info.render.frame;if(document.hidden||!driving){NV.t=a;NV.f0=fr;return}
  if(a-NV.t<2500)return;const fps=(fr-NV.f0)*1000/(a-NV.t);NV.t=a;NV.f0=fr;NV.fps=fps;
  if(NV.n<3&&fps<22){if(++NV.malos>=2){NV.malos=0;escalon();NV.t=a+3000}}else NV.malos=0},500);
 const COLA=new Set(),T={tick:0,mon:0};
 function montar(t0,lim){for(const L of COLA){COLA.delete(L);if(LOTES.get(L.k)===L){const t=performance.now();rehacer(L);T.mon=Math.max(T.mon,performance.now()-t)}if(performance.now()-t0>lim)break}}
 // cada décima de segundo, unos 4 ms como mucho: revisar lotes por turnos, buscar piezas nuevas por trozos y montar lotes
 let REV=[],RI=0,tB=0;
 setInterval(()=>{try{const t0=performance.now();
   if(RI>=REV.length){REV=[...LOTES.values()];RI=0}
   while(RI<REV.length&&performance.now()-t0<1.5)revisa1(REV[RI++]);
   if(!BUS&&t0-tB>2000){BUS=[];scene.traverse(o=>{if(o.isMesh&&o!==RAIZ&&!EN.has(o))BUS.push(o)});BI=0;tB=t0}
   if(BUS){const ahora=performance.now();while(BI<BUS.length&&performance.now()-t0<3)busca1(BUS[BI++],ahora);if(BI>=BUS.length){BUS=null;buscaFin()}}
   revisaT();if(!TRZ&&COLAT.size){const o=COLAT.values().next().value;COLAT.delete(o);if(!EN.has(o)&&enEscena(o))TRZ=trocear(o)}
   if(TRZ){const t1=performance.now();while(performance.now()-t1<5)if(TRZ.next().done){TRZ=null;break}}   // a trozos de 5 ms, sin parón
   if(typeof FONDO!=='undefined'&&FONDO.m&&FONDO.m.layers.mask!==HID)FONDO.m.layers.mask=HID;   // los montes lejanos: en el móvil quedan fuera de la vista pero se calculaban igual
   if(COLA.size)montar(t0,COLA.size>40?12:5);/* al llegar a una zona hay muchos: se monta más deprisa */T.tick=Math.max(T.tick,performance.now()-t0)}catch(e){console.warn('lotes',e)}},100);
 if(/[?&]fps=1/.test(location.search)){const d=document.createElement('div');d.style.cssText='position:fixed;left:8px;bottom:calc(8px + env(safe-area-inset-bottom,0px));z-index:99;background:rgba(0,0,0,.6);color:#9f9;font:600 12px monospace;padding:3px 6px;border-radius:6px;pointer-events:none';document.body.appendChild(d);
  let n0=R.info.render.frame,t=performance.now();setInterval(()=>{const a=performance.now(),i=R.info.render;d.textContent=Math.round((i.frame-n0)*1000/(a-t))+' fps · calidad -'+NV.n+' · '+i.calls+' dib · '+Math.round(i.triangles/1000)+'k tri';n0=i.frame;t=a},1000)}
 window.__LOTES=()=>({nivel:NV.n,fps:NV.fps&&+NV.fps.toFixed(1),trozos:TROZ.size,lotes:LOTES.size,piezas:EN.size,cola:COLA.size,ms:{tick:+T.tick.toFixed(1),montarLote:+T.mon.toFixed(1)}});
})();

// botones de arriba solo con su icono cuando el móvil está en vertical (el texto no cabía y tapaba el marcador)
if(window.LITE){const ico=b=>{const t=(b.textContent||'').trim();let f='';try{f=[...new Intl.Segmenter().segment(t)][0]?.segment||''}catch(e){f=Array.from(t)[0]||''}if(b.dataset.ico!==f)b.dataset.ico=f};
 const bar=document.querySelector('.bar');if(bar){const run=()=>bar.querySelectorAll('button').forEach(ico);run();new MutationObserver(run).observe(bar,{subtree:true,childList:true,characterData:true})}}
