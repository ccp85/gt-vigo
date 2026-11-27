// ---------- Colegio Compañía de María (colegio.js)
// Rúa Ecuador 35 / Colmeiro Laforet: el colegio con su iglesia, modelado en Blender a partir de la vista aérea,
// Street View y fotos (colegio_compania_maria.glb, generado con fuente/herramientas/colegio_compania_maria.py en modo GAME).
// Iglesia de granito con frontón, rosetón, hornacina con la Virgen y espadaña con campana; ala clásica del claustro
// (revoco crema y recercados de granito), ala moderna con arcos en la planta baja, pabellón de chapa roja,
// edificio de granito de Ecuador, muro alto con el mural del tucán, escalera, verja, jardines y árboles.
// Al cargar la zona "centro" se ocultan los bloques genéricos del Catastro que ocupa y se coloca el modelo encima,
// con colisión. Ejes del modelo: x a lo largo de la fachada (NO→SE), z hacia Ecuador; 1 unidad del juego = CDM.S m.
const CDM={O:[93.017,22.36],TH:21.8*Math.PI/180,S:64,
 OC:[[-1.5,-2,57,36],[56,-7,82,32],[17,33,60,61],[2,60,62,77]],root:null,carga:null,G:null,oc:0};window.__CDM=CDM;
function cdmG(x,y){const c=Math.cos(CDM.TH),s=Math.sin(CDM.TH);return[CDM.O[0]+(x*c-y*s)/CDM.S,CDM.O[1]+(x*s+y*c)/CDM.S]}
function cdmLoc(gx,gz){const c=Math.cos(CDM.TH),s=Math.sin(CDM.TH),dx=(gx-CDM.O[0])*CDM.S,dz=(gz-CDM.O[1])*CDM.S;return[dx*c+dz*s,-dx*s+dz*c]}
function cdmDentro(gx,gz){const[x,y]=cdmLoc(gx,gz);for(const r of CDM.OC)if(x>r[0]&&x<r[2]&&y>r[1]&&y<r[3])return true;return false}
// bloques del Catastro dentro del recinto: sus triángulos se anulan (y se rehace su árbol de colisión si ya lo tenían)
function cdmOculta(rt){if(!rt||rt.name!=='centro')return;const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();let k=0;
 rt.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||o.userData.cdm||!/^edificios/.test(o.name)||(typeof GROUND!=='undefined'&&GROUND.includes(o)))return;
  const g=o.geometry,ix=g.index,pos=g.attributes.position;if(!ix||!pos)return;o.updateMatrixWorld(true);const mw=o.matrixWorld;let ch=0;
  for(let t=0;t<ix.count;t+=3){a.fromBufferAttribute(pos,ix.getX(t)).applyMatrix4(mw);b.fromBufferAttribute(pos,ix.getX(t+1)).applyMatrix4(mw);c.fromBufferAttribute(pos,ix.getX(t+2)).applyMatrix4(mw);
   if(cdmDentro((a.x+b.x+c.x)/3,(a.z+b.z+c.z)/3)){const i0=ix.getX(t);ix.setX(t+1,i0);ix.setX(t+2,i0);ch++}}
  if(ch){ix.needsUpdate=true;k+=ch;if(g.boundsTree){try{g.computeBoundsTree()}catch(e){}}}});
 CDM.oc+=k;cdmCarga(rt)}
function cdmSuelo(){const v=[];for(const[x,y]of[[8,16],[22,10],[40,16],[30,45],[30,68],[70,0]]){const[gx,gz]=cdmG(x,y);let h=null;try{h=sueloRap(gx,gz)}catch(e){}if(h!=null)v.push(h)}
 if(v.length<3)return null;v.sort((p,q)=>p-q);return v[v.length>>1]}
function cdmCarga(rt){if(CDM.root===rt&&CDM.G&&CDM.G.parent===rt)return;CDM.root=rt;
 (CDM.carga||(CDM.carga=new Promise((ok,ko)=>{const ld=new GLTFLoader();ld.setMeshoptDecoder(MeshoptDecoder);ld.load('colegio_compania_maria.glb',g=>ok(g.scene),undefined,ko)})))
 .then(sc=>{let n=0;const pon=()=>{if(CDM.root!==rt||!rt.parent)return;const y=cdmSuelo();if(y==null&&++n<40){setTimeout(pon,500);return}
   const G=CDM.G||(CDM.G=sc);G.name='colegioCompaniaMaria';
   if(!G.userData.prep){G.userData.prep=1;G.traverse(o=>{if(!o.isMesh)return;o.userData.cdm=1;o.castShadow=!window.LITE;o.receiveShadow=true;
     for(const m of [].concat(o.material)){if(m&&m.map){m.map.anisotropy=4;m.map.needsUpdate=true}}})}
   const[gx,gz]=[CDM.O[0],CDM.O[1]];G.position.set(gx,(y==null?groundY(cdmG(22,16)[0],cdmG(22,16)[1]):y)+.0005,gz);
   G.rotation.set(0,-CDM.TH,0);G.scale.setScalar(1/CDM.S);rt.add(G);G.updateMatrixWorld(true);CDM.y=G.position.y;
   // colisión: edificios, tejados, muro y pabellón (los árboles y barandillas no)
   G.traverse(o=>{if(!o.isMesh||!/granito|revoco|teja|hormigon|chapa|vidrio|madera/.test(o.name))return;delete o.userData.bbw;
    if(!(window.OBST||[]).includes(o)&&!(typeof BVHQ!=='undefined'&&BVHQ.includes(o))){try{colaBVH(o,false)}catch(e){}}});
   CDM.listo=1};pon()})
 .catch(e=>{console.warn('colegio',e);CDM.carga=null;CDM.err=String(e)})}
// ---------- fin de colegio.js
