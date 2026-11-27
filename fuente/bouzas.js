// ---------- Bouzas y Alcabre (bouzas.js) ----------
// Parcelas con detalle por zonas, con Google Earth, Street View y fotos como referencia (todo propio). Zonas: Bouzas y
// Alcabre, Teis y Chapela. Cada zona trae <zona>_jardin.json y <zona>_suelo.png, horneados de sus mallas.
// · Parcelas de las casas: antes la tierra entre casas era una explanada beige vacía. Ahora la propia tierra de la zona
//   se pinta con una máscara: césped en los jardines, prado y monte con matorral en lo no edificado (en Teis, también
//   huertas con surcos), y losas de granito (Bouzas) u hormigón (Teis) en el casco, las manzanas cerradas, los patios
//   y alrededor de las naves.
// · Muros de cierre a la calle como en Galicia: granito, enlucido blanco con albardilla de granito, granito con sebe
//   encima y bloque bajo con verja; con portales. Entre parcelas, sebes y muros medianeros.
// · Árboles de jardín (frutales, magnolios, cipreses), pinos, frondosas y eucaliptos en el monte, palmeras y arbustos
//   con flor (hortensias y camelias). En Teis, además, parras sobre emparrado y postes de la luz con su tendido.
// · Museo do Mar (Alcabre): el dique ya no es un edificio entero: muelle de hormigón, escollera de bloques de granito
//   por fuera, acuario bajo de cubierta oscura y, en la punta, plataforma redonda con el faro rojo de hierro.
// Herramientas en fuente/herramientas/bouzas_*.{mjs,py}.
const PARC={};for(const id of['bouzas','teis'])PARC[id]={id,root:null,datos:null,carga:null};const BZ=PARC.bouzas;window.__BZ=BZ;window.__PARC=PARC;
function bzChk(){if(!MAPA||!MI)return;for(const id in PARC){const P=PARC[id];const z=ZROOTS.find(q=>q.root&&q.root.name===id&&q.root.parent);if(!z||P.root===z.root)continue;
 const r=z.root;P.root=r;
 (P.carga||(P.carga=fetch(id+'_jardin.json').then(x=>{if(!x.ok)throw new Error('HTTP '+x.status);return x.json()}))).then(d=>{P.datos=d;if(P.root!==r||!r.parent)return;
  setTimeout(()=>{if(!r.parent)return;try{bzCrea(r,d,P)}catch(e){console.warn('parcelas '+id,e);P.err=String(e)+' '+String(e.stack).slice(0,600)}},900)}).catch(e=>{P.carga=null;P.root=null;console.warn('parcelas json '+id,e)})}}
function bzCrea(root,D,PZ){const LT=!!window.LITE,t0=performance.now(),G=new THREE.Group();G.name=PZ.id+'_detalle';
 let rs=11;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.9},o));
 const PO={polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2};
 const malla=(pos,col,mat,nombre,sombra=true)=>{if(!pos.length)return null;const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));if(col)g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.computeVertexNormals();
  const m=new THREE.Mesh(g,mat);m.name=nombre;m.castShadow=sombra&&!LT;m.receiveShadow=true;G.add(m);return m};
 const C3=h=>{const c=new THREE.Color(h);return[c.r,c.g,c.b]};
 // ================= suelo de las parcelas: la propia tierra de la zona se pinta con la máscara (sin mallas encima) =================
 // En el móvil (LITE) la tierra pasa a material mate y el brillo de suelo mojado no compila en él: aquí lleva un mate propio
 root.traverse(o=>{if(!o.isMesh||!/^tierra/.test(o.name))return;
  if(LT&&!Array.isArray(o.material)){const v=o.material,n=new THREE.MeshLambertMaterial({color:v.color.clone(),polygonOffset:v.polygonOffset,polygonOffsetFactor:v.polygonOffsetFactor,polygonOffsetUnits:v.polygonOffsetUnits});n.name=v.name;n.userData.noMate=true;o.material=n}
  for(const m of [].concat(o.material))bzSuelo(m,D,PZ.id)});
 // ================= muros de cierre, sebes y lindes =================
 const PIE=-.006;   // los muros entran un poco en el suelo
 const W=new Map();const wadd=(mat,pos,col)=>{let a=W.get(mat);if(!a)W.set(mat,a={p:[],c:[]});a.p.push(...pos);if(col)for(let i=0;i<pos.length/3;i++)a.c.push(...col)};
 // caja que sigue el terreno: de A a B, grosor e, alto h, desplazada del suelo y0
 const caja=(ax,az,ay,bx,bz,by,e,h,y0,mat,col)=>{const dx=bx-ax,dz=bz-az,l=Math.hypot(dx,dz);if(l<1e-4)return;const nx=-dz/l*e/2,nz=dx/l*e/2;
  const a0=ay+y0,b0=by+y0,a1=ay+y0+h,b1=by+y0+h;
  const P=[[ax+nx,a0,az+nz],[bx+nx,b0,bz+nz],[bx+nx,b1,bz+nz],[ax+nx,a1,az+nz],[ax-nx,a0,az-nz],[bx-nx,b0,bz-nz],[bx-nx,b1,bz-nz],[ax-nx,a1,az-nz]];
  const F=[[0,1,2,3],[5,4,7,6],[3,2,6,7],[4,0,3,7],[1,5,6,2]];const out=[];for(const[a,b,c,d]of F)out.push(...P[a],...P[b],...P[c],...P[a],...P[c],...P[d]);wadd(mat,out,col)};
 const mGra=M(0xffffff,{vertexColors:true,roughness:.95}),mBla=M(0xffffff,{vertexColors:true,roughness:.85}),mSeb=M(0xffffff,{vertexColors:true,roughness:1}),
  mHie=M(0x2c3530,{roughness:.5,metalness:.5}),mPor=M(0xffffff,{vertexColors:true,roughness:.6,metalness:.3});
 const GRC=['#a09a8f','#958f84','#aaa497','#8d887e','#a7a093'].map(C3),BLC=['#efede6','#e8e5dc','#f3efe4','#e4e1d8'].map(C3),SEB=['#3f6b35','#46743a','#38602f','#4d7a3f'].map(C3),
  BLQ=['#d9d5cb','#cfcabf','#d2d0c8'].map(C3),PORC=['#3a2c22','#5b3a26','#2f3d33','#3d3f44','#6a6f72'].map(C3);
 recorteVista(mSeb);hojas(mSeb);
 const tramo=(tipo,ax,az,ay,bx,bz,by)=>{const g=GRC[(rn()*5)|0];
  if(tipo===0)caja(ax,az,ay,bx,bz,by,.007,.026,PIE,mGra,g);
  else if(tipo===1){const b=BLC[(rn()*4)|0];caja(ax,az,ay,bx,bz,by,.007,.024,PIE,mBla,b);caja(ax,az,ay,bx,bz,by,.0095,.0035,.018,mGra,g)}
  else if(tipo===2){caja(ax,az,ay,bx,bz,by,.007,.015,PIE,mGra,g);caja(ax,az,ay,bx,bz,by,.012,.017,.009,mSeb,SEB[(rn()*4)|0])}
  else{caja(ax,az,ay,bx,bz,by,.006,.014,PIE,mBla,BLQ[(rn()*3)|0]);if(!LT){caja(ax,az,ay,bx,bz,by,.002,.0018,.026,mHie);const l=Math.hypot(bx-ax,bz-az),n=Math.max(1,Math.round(l/.022));for(let k=0;k<=n;k++){const f=k/n,x=ax+(bx-ax)*f,z=az+(bz-az)*f,y=ay+(by-ay)*f,dx=(bx-ax)/l*.0009,dz=(bz-az)/l*.0009;caja(x-dx,z-dz,y,x+dx,z+dz,y,.0018,.0125,.008,mHie)}}}};
 const TMU=D.tiposMuro;for(const m of D.muros){const tipo=TMU?TMU[Math.abs(m[1]*13.7+m[2]*7.3|0)%TMU.length]:m[0],P=[];for(let i=1;i<m.length;i+=3)P.push([m[i],m[i+1],m[i+2]]);
  let acc=0,pg=.12+rn()*.25;   // portal cada cierto trecho
  for(let i=1;i<P.length;i++){const[a,b]=[P[i-1],P[i]];const l=Math.hypot(b[0]-a[0],b[1]-a[1]);
   if(l>.05&&acc+l>pg){// portal: hueco de .03 con una puerta metida un poco hacia dentro
    const f0=Math.max(0,Math.min(1,(pg-acc)/l)),fw=Math.min(.45,.03/l),f1=Math.min(1,f0+fw),L=(f)=>[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f,a[2]+(b[2]-a[2])*f];
    const p0=L(f0),p1=L(f1);if(f0>0)tramo(tipo,a[0],a[1],a[2],p0[0],p0[1],p0[2]);if(f1<1)tramo(tipo,p1[0],p1[1],p1[2],b[0],b[1],b[2]);
    {const dx=b[0]-a[0],dz=b[1]-a[1],nx=-dz/l*.004,nz=dx/l*.004;caja(p0[0]+nx,p0[1]+nz,p0[2],p1[0]+nx,p1[1]+nz,p1[2],.003,.022,PIE,mPor,PORC[(rn()*5)|0]);
     for(const p of[p0,p1])caja(p[0]-.002,p[1]-.002,p[2],p[0]+.002,p[1]+.002,p[2],.007,.03,PIE,mGra,GRC[0])}
    acc=0;pg=.15+rn()*.3}else{tramo(tipo,a[0],a[1],a[2],b[0],b[1],b[2]);acc+=l}}}
 for(const[tp,ax,az,ay,bx,bz,by]of D.lindes){if(tp===1)caja(ax,az,ay,bx,bz,by,.011,.02,PIE,mSeb,SEB[(rn()*4)|0]);else caja(ax,az,ay,bx,bz,by,.006,.02,PIE,mGra,GRC[(rn()*5)|0])}
 for(const[mat,a]of W){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(a.p,3));if(a.c.length)g.setAttribute('color',new THREE.Float32BufferAttribute(a.c,3));
  if(mat===mSeb)g.setAttribute('hoja',new THREE.BufferAttribute(new Float32Array(a.p.length/3).fill(1),1));g.computeVertexNormals();const m=new THREE.Mesh(g,mat);m.name='muros_bouzas';m.castShadow=!LT;m.receiveShadow=true;G.add(m)}
 // ================= árboles, palmeras y arbustos =================
 const M4=new THREE.Matrix4(),Q=new THREE.Quaternion(),V=new THREE.Vector3(),S=new THREE.Vector3(),E=new THREE.Euler();
 const trozos=(lista,geo,mat,nombre,pon,sombra=true)=>{const G_=new Map();for(const it of lista){const k=Math.floor(it[0]/3)+','+Math.floor(it[1]/3);if(!G_.has(k))G_.set(k,[]);G_.get(k).push(it)}
  for(const L of G_.values()){const im=new THREE.InstancedMesh(geo,mat,L.length);im.name=nombre;let sx=0,sy=0;L.forEach((it,i)=>{pon(im,it,i);sx+=it[0];sy+=it[1]});
   im.instanceMatrix.needsUpdate=true;if(im.instanceColor)im.instanceColor.needsUpdate=true;im.castShadow=sombra&&!LT;im.receiveShadow=true;im.computeBoundingSphere();G.add(im);TROZOS.push({m:im,x:sx/L.length,y:sy/L.length})}};
 {const ACOL=['#4f8a4b','#3d6e48','#5d8a55','#6a9a5a','#4a7a3c','#5f8f3c','#3f6634','#7b8f45','#6f8a6e','#7d9478'].map(c=>new THREE.Color(c));
  const lista=LT?D.arboles.filter((a,i)=>i%2===0):D.arboles;
  const ponA=(im,[x,z,y,r,h,c],i)=>{Q.setFromAxisAngle(V.set(0,1,0),(x*37.1+z*11.3)%6.283);M4.compose(V.set(x,y-.004,z),Q,S.set(r,h,r));im.setMatrixAt(i,M4);im.setColorAt(i,ACOL[c%10])};
  const aC=lista.filter(a=>a[6]!==1),aR=lista.filter(a=>a[6]===1);
  if(aC.length){const mt=M(0xffffff,{roughness:.85,vertexColors:true});recorteVista(mt);hojas(mt);trozos(aC,TREE_GEO,mt,'arboles',ponA)}
  if(aR.length){const mt=M(0xffffff,{roughness:.9,vertexColors:true});recorteVista(mt);hojas(mt);trozos(aR,TREE_R,mt,'arboles',ponA)}}
 // palmeras (Washingtonia/Phoenix de jardín): tronco con anillos y copa de hojas arqueadas; alto 1
 {const parts=[],tin=(g,c,hj)=>{g=g.index?g.toNonIndexed():g;if(g.attributes.uv)g.deleteAttribute('uv');const n=g.attributes.position.count,a=new Float32Array(n*3);for(let i=0;i<n;i++){a[i*3]=c[0];a[i*3+1]=c[1];a[i*3+2]=c[2]}g.setAttribute('color',new THREE.BufferAttribute(a,3));g.setAttribute('hoja',new THREE.BufferAttribute(new Float32Array(n).fill(hj),1));g.deleteAttribute('normal');parts.push(g)};
  const tr=new THREE.CylinderGeometry(.03,.045,.86,7,4);tr.translate(0,.43,0);{const p=tr.attributes.position;for(let i=0;i<p.count;i++){const y=p.getY(i);p.setX(i,p.getX(i)+Math.sin(y*2.2)*.03)}}tin(tr,[.55,.45,.36],0);
  {const b=new THREE.SphereGeometry(.07,7,5);b.scale(1,.8,1);b.translate(.035,.88,0);tin(b,[.42,.34,.24],0)}
  for(let k=0;k<11;k++){const a=k/11*6.283+(k%2)*.2,cai=.35+(k%3)*.18;const f=new THREE.PlaneGeometry(.42,.07,4,1);f.translate(.21,0,0);const p=f.attributes.position;
   for(let i=0;i<p.count;i++){const x=p.getX(i);p.setY(i,p.getY(i)*(1-x/.5)*1.0);p.setZ(i,-x*x*cai*2.2)}f.rotateX(-Math.PI/2);f.rotateZ(.35);f.rotateY(a);f.translate(.035,.9,0);tin(f,k%4===0?[.44,.56,.3]:[.3,.5,.26],1)}
  const pg=mergeGeometries(parts);pg.computeVertexNormals();
  const mt=M(0xffffff,{vertexColors:true,roughness:.8,side:THREE.DoubleSide});recorteVista(mt);hojas(mt);
  trozos(D.palmeras.map(p=>[p[0],p[1],p[2],p[3]]),pg,mt,'arboles',(im,[x,z,y,h],i)=>{Q.setFromAxisAngle(V.set(0,1,0),(x*53.7+z*19.1)%6.283);M4.compose(V.set(x,y-.003,z),Q,S.set(h,h,h));im.setMatrixAt(i,M4)})}
 // arbustos: verdes y con flor (hortensias azules y rosas, camelias)
 if(!LT){const g0=new THREE.IcosahedronGeometry(1,1);g0.scale(1,.7,1);g0.translate(0,.45,0);{const p=g0.attributes.position;for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),z=p.getZ(i),n=1+.16*Math.sin(x*7.1+z*5.3+y*3.1);p.setXYZ(i,x*n,y*n,z*n)}}
  g0.deleteAttribute('uv');const g=g0.toNonIndexed();g.setAttribute('hoja',new THREE.BufferAttribute(new Float32Array(g.attributes.position.count).fill(1),1));{const n=g.attributes.position.count,a=new Float32Array(n*3).fill(1);g.setAttribute('color',new THREE.BufferAttribute(a,3))}g.computeVertexNormals();
  const BC=['#3f6b35','#4d7a3f','#6c8fc9','#d98fb5','#c2445a','#f2f0ea'].map(c=>new THREE.Color(c));
  const mt=M(0xffffff,{roughness:.95,vertexColors:true});recorteVista(mt);hojas(mt);
  trozos(D.arbustos,g,mt,'arbustos',(im,[x,z,y,r,c],i)=>{M4.compose(V.set(x,y-.004,z),Q.identity(),S.set(r*1.2,r,r*1.2));im.setMatrixAt(i,M4);im.setColorAt(i,BC[c%6])},false)}
 // ================= Museo do Mar: dique, acuario y faro =================
 if(D.dique&&D.dique.length)try{bzDique(root,G,D,M,malla)}catch(e){console.warn('bouzas dique',e);PZ.errD=String(e)}
 // ================= postes de la luz con su tendido (hormigón o madera) =================
 if(D.postes&&D.postes.length){const PH=.13,pos=[],hor=[],mad=[];const geoP=new THREE.CylinderGeometry(.0016,.0026,PH,5);geoP.translate(0,PH/2,0);const cr=new THREE.BoxGeometry(.016,.0015,.0015);cr.translate(0,PH-.008,0);
  const mP=M(0x9d9a92,{roughness:.9}),mM=M(0x5e4a36,{roughness:.95});const lH=[],lM=[];
  for(const[x,z,y,a,c]of D.postes){const g=c?mM:mP,L=c?lM:lH;L.push([x,z,y,a])}
  const pon=(L,mat)=>{if(!L.length)return;const gg=mergeGeometries([geoP.toNonIndexed(),cr.toNonIndexed()]);trozos(L,gg,mat,'postes',(im,[x,z,y,a],i)=>{Q.setFromAxisAngle(V.set(0,1,0),a);M4.compose(V.set(x,y-.004,z),Q,S.set(1,1,1));im.setMatrixAt(i,M4)})};pon(lH,mP);pon(lM,mM);
  // cables: tres hilos entre postes seguidos de la misma línea, con su catenaria
  const W_=[];for(const[i,j]of D.cables){const A=D.postes[i],B=D.postes[j];if(!A||!B)continue;for(const k of[-1,0,1]){const ox=Math.cos(A[3])*.006*k,oz=-Math.sin(A[3])*.006*k,ox2=Math.cos(B[3])*.006*k,oz2=-Math.sin(B[3])*.006*k;
    const a=[A[0]+ox,A[2]+PH-.007,A[1]+oz],b=[B[0]+ox2,B[2]+PH-.007,B[1]+oz2],L=Math.hypot(b[0]-a[0],b[2]-a[2]),sag=Math.min(.012,L*.05);let p=a;
    for(let s=1;s<=6;s++){const f=s/6,q=[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f-4*sag*f*(1-f),a[2]+(b[2]-a[2])*f];W_.push(...p,...q);p=q}}}
  if(W_.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(W_,3));const l=new THREE.LineSegments(g,new THREE.LineBasicMaterial({color:0x2a2a2a,transparent:true,opacity:.75}));l.name='cables_luz';G.add(l)}}
 // ================= parras sobre emparrado: postes de granito, alambres y hoja de vid =================
 if(D.parras&&D.parras.length){const mPo=M(0x9c968a,{roughness:.95}),mV=M(0xffffff,{vertexColors:true,roughness:.95});recorteVista(mV);hojas(mV);const pp=[];const VC=['#5c7f2e','#6b8a34','#577a2b'].map(C3),pc=[];
  for(const[x,z,y,a,w,l]of D.parras){const c=Math.cos(a),sn=Math.sin(a),P=(u,v)=>[x+u*c+v*sn,z-u*sn+v*c];
   for(const[u,v]of[[-w/2,-l/2],[w/2,-l/2],[w/2,l/2],[-w/2,l/2]]){const[px,pz]=P(u,v);caja(px-.0015,pz,y,px+.0015,pz,y,.003,.03,PIE,mPo,GRC[1])}
   const g=new THREE.BoxGeometry(w*1.08,.005,l*1.08,4,1,3);const p=g.attributes.position;for(let i=0;i<p.count;i++)p.setY(i,p.getY(i)+Math.sin(p.getX(i)*170+p.getZ(i)*120)*.0018);g.rotateY(a);g.translate(x,y+.031,z);const q=g.toNonIndexed().attributes.position.array;pp.push(...q);const cc=VC[(x*17|0)%3];for(let i=0;i<q.length/3;i++)pc.push(...cc)}
  for(const[mat,a]of W)if(mat===mPo&&!a.done){a.done=1;const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(a.p,3));g.setAttribute('color',new THREE.Float32BufferAttribute(a.c,3));g.computeVertexNormals();const m=new THREE.Mesh(g,M(0xffffff,{vertexColors:true,roughness:.95}));m.castShadow=!LT;G.add(m)}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pp,3));g.setAttribute('color',new THREE.Float32BufferAttribute(pc,3));g.setAttribute('hoja',new THREE.BufferAttribute(new Float32Array(pp.length/3).fill(1),1));g.computeVertexNormals();const m=new THREE.Mesh(g,mV);m.name='parras';m.castShadow=!LT;m.receiveShadow=true;G.add(m)}
 root.add(G);PZ.G=G;PZ.ms=Math.round(performance.now()-t0)}
// máscara RGB (R césped, G prado y monte, B solado de granito) sobre la tierra de la zona; bordes suaves por filtrado
const BZT={};
function bzSuelo(m,D,id='bouzas'){if(!m||m.userData.bzs)return;m.userData.bzs=1;
 let tx=BZT[id];if(!tx){tx=BZT[id]=new THREE.TextureLoader().load(id+'_suelo.png',t=>{t.needsUpdate=true});tx.flipY=false;tx.colorSpace=THREE.NoColorSpace;tx.minFilter=THREE.LinearMipmapLinearFilter;tx.magFilter=THREE.LinearFilter;tx.generateMipmaps=true}
 const R=D.mascara,U={uBzM:{value:tx},uBzR:{value:new THREE.Vector4(R[0],R[1],R[2],R[3])},uBzP:{value:D.pav||0},uBzH:{value:D.huerta||0}};const LT=!!window.LITE;
 const prev=m.onBeforeCompile;const pk=m.customProgramCacheKey?m.customProgramCacheKey.bind(m):null;
 // si debajo va el brillo de suelo mojado, el móvil no debe pasarlo a material mate (nitido.js lo mira en el texto de la función)
 if(prev&&/pud|wW|lights_physical|clearcoat/.test(prev.toString()))m.userData.noMate=true;
 m.onBeforeCompile=(sh,r)=>{if(prev)prev(sh,r);Object.assign(sh.uniforms,U);
  sh.vertexShader='varying vec3 vWbz;\n'+sh.vertexShader.replace('#include <worldpos_vertex>','#include <worldpos_vertex>\n vWbz=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='uniform sampler2D uBzM;uniform vec4 uBzR;uniform float uBzP,uBzH;varying vec3 vWbz;\nfloat hBz(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}\nfloat nBz(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hBz(i),hBz(i+vec2(1,0)),f.x),mix(hBz(i+vec2(0,1)),hBz(i+vec2(1,1)),f.x),f.y);}\n'+sh.fragmentShader
   .replace('#include <color_fragment>',`#include <color_fragment>
    {vec2 bq=(vWbz.xz-uBzR.xy)/uBzR.zw;
     if(bq.x>0.&&bq.y>0.&&bq.x<1.&&bq.y<1.){vec3 mk=texture2D(uBzM,bq).rgb;
      vec2 q=vWbz.xz;float fw=max(length(fwidth(q)),1e-6),cerca=1.-smoothstep(.004,.03,fw);
      float n=nBz(q*3.1)*.45+nBz(q*11.)*.35+nBz(q*31.)*.2;float pl=hBz(floor(q*6.5+.5));          // manchas y tono de cada parcela
      float wl=smoothstep(.3,.62,mk.r),wp=smoothstep(.3,.62,mk.g),ws=smoothstep(.3,.62,mk.b);
      vec3 ces=mix(vec3(.085,.19,.05),vec3(.17,.31,.08),smoothstep(.15,.85,n))*mix(.85,1.15,pl);       // césped (lineal)
      ces=mix(ces,ces*vec3(1.45,1.2,.62),smoothstep(.62,.9,nBz(q*2.2+9.))*.55);                       // calvas secas
      vec3 pra=mix(vec3(.2,.24,.08),vec3(.33,.34,.13),smoothstep(.2,.8,n));                               // prado y monte
      pra=mix(pra,vec3(.13,.17,.06),smoothstep(.55,.8,nBz(q*5.+3.))*.7);                                // matorral (toxo, xesta)
      if(uBzH>0.){vec2 hc=floor(q*4.2);float hh=hBz(hc+17.);if(hh<uBzH){float an=hBz(hc+3.)*3.1416;vec2 dd=vec2(cos(an),sin(an));   // huertas con surcos
        float su=smoothstep(.25,.5,abs(fract(dot(q,dd)*150.)-.5)*2.);vec3 hu=mix(vec3(.17,.11,.06),vec3(.12,.25,.06)*(.8+.4*n),su*step(.3,hBz(hc+9.)));
        pra=mix(pra,hu,smoothstep(.0,.08,min(min(fract(q.x*4.2),1.-fract(q.x*4.2)),min(fract(q.y*4.2),1.-fract(q.y*4.2)))));}}
      ${LT?'':'float bz=nBz(q*260.)*.6+nBz(q*610.)*.4;ces*=mix(1.,.8+.4*bz,cerca);pra*=mix(1.,.78+.44*bz,cerca);'}
      vec3 gra=uBzP>.5?mix(vec3(.42,.42,.4),vec3(.55,.54,.52),pl)*(.9+.2*n):mix(vec3(.36,.34,.3),vec3(.5,.47,.42),pl)*(.9+.2*n);   // losas de granito u hormigón
      ${LT?'':'if(uBzP<.5){vec2 lq=q*vec2(70.,95.);lq.x+=floor(lq.y)*.5;vec2 jl=abs(fract(lq)-.5);float ju=1.-smoothstep(.40,.47,max(jl.x,jl.y));gra*=mix(1.,.72+.28*ju,cerca);}'}
      diffuseColor.rgb=mix(diffuseColor.rgb,pra,wp);diffuseColor.rgb=mix(diffuseColor.rgb,ces,wl);diffuseColor.rgb=mix(diffuseColor.rgb,gra,ws);}}`)};
 m.customProgramCacheKey=()=>(pk?pk():'')+'|bzs';m.needsUpdate=true;bzSueloGPU(m,D,tx)}
// lo mismo para la prueba con el motor WebGPU (gpu.html), en TSL sobre la cadena de color del material
function bzSueloGPU(m,D,tx){if(typeof gpuFx!=='function'||typeof GT==='undefined'||typeof TSL==='undefined'||m.userData.g_bzs)return;m.userData.g_bzs=1;
 try{GT.ini();const{vec2,vec3,float,floor,mix,smoothstep,max,min,length,fwidth,texture,positionWorld,step}=TSL;const R=D.mascara,vn=GT.vn,h21=GT.h21,LT=!!window.LITE;
  const q=positionWorld.xz,bq=q.sub(vec2(R[0],R[1])).div(vec2(R[2],R[3])),mk=texture(tx,bq);
  const ins=step(0,bq.x).mul(step(0,bq.y)).mul(step(bq.x,1)).mul(step(bq.y,1));
  const fw=max(length(fwidth(q)),1e-6),cerca=smoothstep(.004,.03,fw).oneMinus();
  const n=vn(q.mul(3.1)).mul(.45).add(vn(q.mul(11)).mul(.35)).add(vn(q.mul(31)).mul(.2)),pl=h21(floor(q.mul(6.5).add(.5)));
  const wl=smoothstep(.3,.62,mk.r).mul(ins),wp=smoothstep(.3,.62,mk.g).mul(ins),ws=smoothstep(.3,.62,mk.b).mul(ins);
  let ces=mix(vec3(.085,.19,.05),vec3(.17,.31,.08),smoothstep(.15,.85,n)).mul(mix(.85,1.15,pl));ces=mix(ces,ces.mul(vec3(1.45,1.2,.62)),smoothstep(.62,.9,vn(q.mul(2.2).add(9))).mul(.55));
  let pra=mix(vec3(.2,.24,.08),vec3(.33,.34,.13),smoothstep(.2,.8,n));pra=mix(pra,vec3(.13,.17,.06),smoothstep(.55,.8,vn(q.mul(5).add(3))).mul(.7));
  if(!LT){const bz=vn(q.mul(260)).mul(.6).add(vn(q.mul(610)).mul(.4));ces=ces.mul(mix(1,bz.mul(.4).add(.8),cerca));pra=pra.mul(mix(1,bz.mul(.44).add(.78),cerca))}
  const gra=(D.pav?mix(vec3(.42,.42,.4),vec3(.55,.54,.52),pl):mix(vec3(.36,.34,.3),vec3(.5,.47,.42),pl)).mul(n.mul(.2).add(.9));
  GT.cadena(m,b=>mix(mix(mix(b,pra,wp),ces,wl),gra,ws));m.needsUpdate=true}catch(e){console.warn('bouzas gpu',e)}}
function bzDique(root,G,D,M,malla){const LT=!!window.LITE,P=[];for(let i=0;i<D.dique.length;i+=2)P.push([D.dique[i],D.dique[i+1]]);
 const dentro=(x,z)=>{let c=false;for(let i=0,j=P.length-1;i<P.length;j=i++){const[xi,zi]=P[i],[xj,zj]=P[j];if((zi>z)!==(zj>z)&&x<(xj-xi)*(z-zi)/(zj-zi)+xi)c=!c}return c};
 // eje del dique: de la raíz (tierra) a la punta
 const R0=[34.43,41.36],T0=[35.92,39.87],LL=Math.hypot(T0[0]-R0[0],T0[1]-R0[1]),TX=(T0[0]-R0[0])/LL,TZ=(T0[1]-R0[1])/LL,NX=-TZ,NZ=TX; // N: hacia el SE (dársena)
 const W=(u,v)=>[R0[0]+TX*u+NX*v,R0[1]+TZ*u+NZ*v],ANG=Math.atan2(-TZ,TX);
 const cerca=(x,z)=>dentro(x,z)||Math.hypot(x-T0[0],z-T0[1])<.2;
 // fuera el "edificio" que ocupaba todo el dique y el faro genérico de la punta
 const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();let k=0;root.updateMatrixWorld(true);
 root.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||o.parent===G||!/^(edificios|piezas|tejados|cubiertas)/.test(o.name))return;const g=o.geometry,ix=g.index,pos=g.attributes.position;if(!pos)return;if(!g.boundingBox)g.computeBoundingBox();
  const bb=g.boundingBox.clone().applyMatrix4(o.matrixWorld);if(bb.max.x<33.9||bb.min.x>36.4||bb.max.z<39.4||bb.min.z>41.9)return;const mw=o.matrixWorld;let ch=0;const I=j=>ix?ix.getX(j):j,cnt=ix?ix.count:pos.count;
  for(let i=0;i+2<cnt;i+=3){a.fromBufferAttribute(pos,I(i)).applyMatrix4(mw);b.fromBufferAttribute(pos,I(i+1)).applyMatrix4(mw);c.fromBufferAttribute(pos,I(i+2)).applyMatrix4(mw);
   const mx=(a.x+b.x+c.x)/3,mz=(a.z+b.z+c.z)/3;if(cerca(mx,mz)&&Math.max(a.y,b.y,c.y)>.012){if(ix){const i0=ix.getX(i);ix.setX(i+1,i0);ix.setX(i+2,i0)}else for(const j of[i+1,i+2])pos.setXYZ(j,pos.getX(i),pos.getY(i),pos.getZ(i));ch++}}
  if(ch){if(ix)ix.needsUpdate=true;else pos.needsUpdate=true;k+=ch;if(g.boundsTree)try{g.computeBoundsTree()}catch(e){}}});BZ.dique=k;
 const PARTS=new Map(),add=(geo,mat,x,y,z,ry=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();if(g.attributes.uv)g.deleteAttribute('uv');g.rotateY(ry);g.translate(x,y,z);if(!PARTS.has(mat))PARTS.set(mat,[]);PARTS.get(mat).push(g)};
 const HOR=M(0xc4c0b8,{roughness:.9}),GRA=M(0xa39d92,{roughness:.95}),GRC=M(0xb9b2a5,{roughness:.95}),ESC=M(0xffffff,{vertexColors:true,roughness:1}),
  ACW=M(0xdedcd5,{roughness:.8}),ACT=M(0x4b5056,{roughness:.7}),VID=M(0x3b4a57,{roughness:.15,metalness:.4}),
  FAR=M(0xb3472a,{roughness:.55,metalness:.35}),FARO=M(0x7a2c1d,{roughness:.5,metalness:.4}),LIN=M(0xfff1c8,{emissive:0xffd27a,emissiveIntensity:.9,roughness:.2}),
  CRI=new THREE.MeshStandardMaterial({color:0x9fb8c0,roughness:.08,metalness:.2,transparent:true,opacity:.55}),HIE=M(0x2e3134,{roughness:.45,metalness:.6}),NEG=M(0x26282b,{roughness:.6});
 const YD=.042;   // altura de la losa del muelle
 // losa del muelle (lado de la dársena) hasta la plataforma de la punta
 const U1=LL-.12;{const sh=new THREE.Shape();sh.moveTo(0,-.07);sh.lineTo(U1,-.07);sh.lineTo(U1,.21);sh.lineTo(.05,.23);sh.lineTo(0,.23);
  const g=new THREE.ExtrudeGeometry(sh,{depth:YD+.06,bevelEnabled:false});g.rotateX(Math.PI/2);g.translate(0,YD,0);// (u,v) -> x local, z local
  const p=g.attributes.position;for(let i=0;i<p.count;i++){const u=p.getX(i),v=p.getZ(i),[x,z]=W(u,v);p.setX(i,x);p.setZ(i,z)}g.computeVertexNormals();const m=new THREE.Mesh(g,HOR);m.name='dique_museo';m.castShadow=!LT;m.receiveShadow=true;G.add(m);GROUND.push(m)}
 // plataforma redonda de la punta
 {const g=new THREE.CylinderGeometry(.14,.15,YD+.07,28);const[x,z]=W(LL-.04,.06);const m=new THREE.Mesh(g,GRC);m.position.set(x,YD-(YD+.07)/2+.002,z);m.castShadow=!LT;m.receiveShadow=true;m.name='dique_museo';G.add(m);m.updateMatrixWorld(true);GROUND.push(m)}
 // pretil de granito por el lado de la escollera y bolardos en el cantil
 for(let u=.02;u<U1;u+=.08){const[x,z]=W(u+.04,-.065);add(new THREE.BoxGeometry(.08,.012,.008),GRA,x,YD+.006,z,ANG)}
 for(let u=.1;u<U1;u+=.12){const[x,z]=W(u,.215);add(new THREE.CylinderGeometry(.0035,.0045,.009,7),NEG,x,YD+.0045,z)}
 // escollera: bloques de granito por fuera (NO) y alrededor de la punta
 {const geo=new THREE.DodecahedronGeometry(1,0),pos=[],col=[];let rs=5;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;const n=LT?260:640;
  const pon=(x,y,z,r)=>{const g=geo.clone();g.scale(r*(1+rn()*.4),r*(.6+rn()*.4),r*(1+rn()*.4));g.rotateY(rn()*6);g.rotateX(rn()*.6);g.translate(x,y,z);const q=g.toNonIndexed().attributes.position.array;pos.push(...q);const t=.36+rn()*.2,cc=[t*1.03,t,t*.92];for(let i=0;i<q.length/3;i++)col.push(...cc)};
  for(let i=0;i<n;i++){const u=rn()*(LL-.05),w=rn();const v=-.07-w*.2;const y=YD-.004-w*.07+rn()*.01;const[x,z]=W(u,v);pon(x,y,z,.012+rn()*.014)}
  for(let i=0;i<(LT?60:140);i++){const a=-Math.PI*.9+rn()*Math.PI*1.25,r=.15+rn()*.08;const[cx,cz]=W(LL-.04,.06);pon(cx+Math.cos(a)*r*1,YD-.01-(r-.15)*.6,cz+Math.sin(a)*r,.012+rn()*.012)}
  malla(pos,col,ESC,'escollera_museo')}
 // acuario: nave baja y alargada de cubierta oscura, a media altura del dique
 {const ua=.72,ub=1.4,va=-.03,vb=.15,h=.055,[x,z]=W((ua+ub)/2,(va+vb)/2);add(new THREE.BoxGeometry(ub-ua,h,vb-va),ACW,x,YD+h/2,z,ANG);add(new THREE.BoxGeometry(ub-ua+.012,.006,vb-va+.012),ACT,x,YD+h+.003,z,ANG);
  for(const s of[-1,1]){const[x2,z2]=W((ua+ub)/2,(s<0?va:vb)+s*.0006);add(new THREE.BoxGeometry(ub-ua-.04,.016,.002),VID,x2,YD+.022,z2,ANG)}
  for(let u=ua+.06;u<ub-.04;u+=.09){const[x3,z3]=W(u,(va+vb)/2);add(new THREE.BoxGeometry(.03,.006,.05),ACT,x3,YD+h+.008,z3,ANG)}}
 // farolas en el muelle
 for(let u=.2;u<U1;u+=.32){const[x,z]=W(u,.17);add(new THREE.CylinderGeometry(.0012,.0016,.06,5),HIE,x,YD+.03,z);add(new THREE.BoxGeometry(.008,.004,.008),LIN,x,YD+.061,z)}
 // faro: torre de hierro roja con anillos, galería con barandilla, linterna de cristal y cúpula
 {const[x,z]=W(LL-.04,.06),y0=YD+.002,Ht=.12;const T=new THREE.Group();T.position.set(x,y0,z);T.name='faro_museo';
  const mk=(g,m,py)=>{const o=new THREE.Mesh(g,m);o.position.y=py;o.castShadow=!LT;o.receiveShadow=true;T.add(o);return o};
  mk(new THREE.CylinderGeometry(.03,.034,.012,20),GRC,.006);
  mk(new THREE.CylinderGeometry(.0145,.0175,Ht,18),FAR,.012+Ht/2);
  for(let k=1;k<5;k++)mk(new THREE.CylinderGeometry(.0175-.003*k/5+.0012,.0175-.003*k/5+.0012,.003,18),FARO,.012+Ht*k/5);
  mk(new THREE.CylinderGeometry(.026,.022,.005,20),FARO,.012+Ht+.0025);
  mk(new THREE.TorusGeometry(.025,.0008,4,24).rotateX(Math.PI/2),HIE,.012+Ht+.014);
  for(let k=0;k<16;k++){const a=k/16*6.283;const o=mk(new THREE.BoxGeometry(.0012,.012,.0012),HIE,.012+Ht+.011);o.position.x=Math.cos(a)*.025;o.position.z=Math.sin(a)*.025}
  mk(new THREE.CylinderGeometry(.013,.013,.026,16),CRI,.012+Ht+.018);
  mk(new THREE.CylinderGeometry(.006,.006,.016,10),LIN,.012+Ht+.018);
  for(let k=0;k<8;k++){const a=k/8*6.283;const o=mk(new THREE.BoxGeometry(.0012,.026,.0012),FARO,.012+Ht+.018);o.position.x=Math.cos(a)*.0132;o.position.z=Math.sin(a)*.0132}
  mk(new THREE.SphereGeometry(.0145,16,8,0,6.283,0,Math.PI/2),FARO,.012+Ht+.031);
  mk(new THREE.CylinderGeometry(.0012,.002,.012,6),HIE,.012+Ht+.05);
  {const o=mk(new THREE.BoxGeometry(.0035,.02,.012),NEG,.022);o.position.x=.016;o.rotation.y=-ANG}
  G.add(T)}
 for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.name='museo_mar';m.castShadow=!LT;m.receiveShadow=true;G.add(m)}}
// ---------- fin de bouzas.js
