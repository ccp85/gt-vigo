// ---------- Praza de América (america.js)
// Final de Gran Vía: la plaza peatonal de la rotonda con la Porta do Atlántico de Silverio Rivas (1991-92), el gran arco de piedra
// de unos 14 m y más de 400 t, homenaje a la emigración a América. El arco mira a lo largo del eje Gran Vía–Castelao (este-oeste),
// macizo y áspero por fuera, con la abertura de medio punto pulida. Alrededor, la plaza peatonal tras la reforma: enlosado de granito
// claro, fuentes a ras de suelo con chorros que suben y bajan (luminosas de noche), bancos de granito, árboles en alcorques y farolas.
// Isleta medida en vigo_mapa.png (celdas tipo 1, peatonal): centro [77.958,46.065], radio ~0,22 u. 1 u = 64 m.
// Usa pzeOculta de espana.js para quitar lo genérico que hubiera en la isleta. El circuito del Gran Premio rodea la rotonda y no se toca.
const PAM={C:[77.958,46.065],R:.212,hecha:0,G:null};window.__PAM=PAM;
function pamChk(){if(PAM.hecha||typeof sueloRap!=='function')return;const[cx,cz]=PAM.C;
 if(sueloRap(cx,cz)!=null&&sueloRap(cx+.15,cz)!=null&&sueloRap(cx-.15,cz)!=null){PAM.hecha=1;setTimeout(()=>{try{pamCrea()}catch(e){console.warn('america',e);PAM.err=String(e);PAM.hecha=0}},650)}}
function pamTex(base,vetas,seed,n){const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');let sd=seed;const rn=()=>(sd=(sd*16807)%2147483647)/2147483647;
 x.fillStyle=base;x.fillRect(0,0,256,256);for(let i=0;i<(n||2600);i++){const v=rn();x.fillStyle=v<.5?`rgba(0,0,0,${.05+rn()*.12})`:`rgba(255,255,255,${.04+rn()*.1})`;const s=1+rn()*3;x.fillRect(rn()*256,rn()*256,s,s)}
 if(vetas){x.strokeStyle='rgba(40,38,36,.35)';x.lineWidth=1.5;for(let k=0;k<=256;k+=32){x.beginPath();x.moveTo(0,k);x.lineTo(256,k);x.stroke();for(let j=0;j<256;j+=64){const o=(k/32)%2?32:0;x.beginPath();x.moveTo(j+o,k);x.lineTo(j+o,k+32);x.stroke()}}}
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=4;return t}
function pamCrea(){const[cx,cz]=PAM.C,R=PAM.R,G=new THREE.Group();G.name='prazaAmerica';PAM.G=G;
 let y0=sueloRap(cx,cz);if(y0==null)y0=groundY(cx,cz);
 const add=(o,sombra)=>{o.castShadow=!!sombra&&!window.LITE;o.receiveShadow=true;o.userData.pze=1;G.add(o);return o};
 // enlosado de granito claro en anillos y bordillo
 const lt=pamTex('#c9c3b7',true,11);lt.repeat.set(9,9);
 const LOSA=new THREE.MeshStandardMaterial({map:lt,roughness:.85,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}),GRAN=new THREE.MeshStandardMaterial({color:0xb4aea3,roughness:.85});
 {const d=new THREE.CircleGeometry(R,72);d.rotateX(-Math.PI/2);d.translate(cx,y0+.0045,cz);add(new THREE.Mesh(d,LOSA));
  const b=new THREE.CylinderGeometry(R,R+.002,.007,72,1,true);b.translate(cx,y0+.0015,cz);add(new THREE.Mesh(b,GRAN));
  const t=new THREE.RingGeometry(R-.004,R,72);t.rotateX(-Math.PI/2);t.translate(cx,y0+.005,cz);add(new THREE.Mesh(t,GRAN));
  // anillo de losa oscura alrededor del monumento
  const o=new THREE.RingGeometry(.1,.112,64);o.rotateX(-Math.PI/2);o.translate(cx,y0+.0052,cz);add(new THREE.Mesh(o,new THREE.MeshStandardMaterial({color:0x6e6a64,roughness:.7})))}
 // lámina de agua al pie del arco (refleja el cielo)
 {const a=new THREE.CircleGeometry(.1,56);a.rotateX(-Math.PI/2);a.translate(cx,y0+.0058,cz);add(new THREE.Mesh(a,new THREE.MeshStandardMaterial({color:0x35667a,roughness:.06,metalness:.2,transparent:true,opacity:.85})))}
 // la Porta do Atlántico: bloque de piedra con abertura de medio punto, eje este-oeste
 {const W=.19,H=.22,D=.05,aw=.085,ah=.15,sh=new THREE.Shape();sh.moveTo(-W/2,0);sh.lineTo(W/2,0);sh.lineTo(W/2,H*.93);sh.quadraticCurveTo(W/2,H,W/2-.02,H);sh.lineTo(-W/2+.015,H);sh.quadraticCurveTo(-W/2,H,-W/2,H*.95);sh.lineTo(-W/2,0);
  const ho=new THREE.Path();ho.moveTo(-aw/2,0);ho.lineTo(-aw/2,ah-aw/2);ho.absarc(0,ah-aw/2,aw/2,Math.PI,0,true);ho.lineTo(aw/2,0);ho.lineTo(-aw/2,0);sh.holes.push(ho);
  const g=new THREE.ExtrudeGeometry(sh,{depth:D,bevelEnabled:true,bevelThickness:.004,bevelSize:.004,bevelSegments:1,curveSegments:24});g.translate(0,0,-D/2);
  // piel áspera: cada vértice exterior se mueve un poco (la abertura queda lisa)
  {const p=g.attributes.position;let sd=5;const rn=()=>(sd=(sd*16807)%2147483647)/2147483647,cache=new Map();
   for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),z=p.getZ(i);const dentro=Math.abs(x)<aw/2+.006&&y<ah+.006;if(dentro||y<.001||y>H*.86)continue;
    const k=x.toFixed(3)+'_'+y.toFixed(3)+'_'+z.toFixed(3);let d=cache.get(k);if(!d){d=[(rn()-.5)*.006,(rn()-.5)*.004,(rn()-.5)*.006];cache.set(k,d)}
    p.setXYZ(i,x+d[0],y,z+d[2])}g.computeVertexNormals()}
  const pt=pamTex('#6f6c67',false,23,5000);pt.repeat.set(14,14);
  const PIEDRA=new THREE.MeshStandardMaterial({map:pt,roughness:.92,flatShading:true});
  const m=new THREE.Mesh(g,PIEDRA);m.position.set(cx,y0+.004,cz);m.rotation.y=Math.PI/2;add(m,true);PAM.arco=m;
  // intradós pulido de la abertura (piedra más oscura y brillante)
  const L=[];const n=24;for(let i=0;i<=n;i++){const a=Math.PI*i/n,x=-Math.cos(a)*aw/2,y=ah-aw/2+Math.sin(a)*aw/2;L.push(new THREE.Vector2(x,y))}
  const pts=[new THREE.Vector2(-aw/2,0),...L,new THREE.Vector2(aw/2,0)],pos=[],idx=[];
  pts.forEach(v=>{pos.push(v.x*.985,v.y,-D/2-.001,v.x*.985,v.y,D/2+.001)});for(let i=0;i<pts.length-1;i++){const a=i*2;idx.push(a,a+1,a+2,a+1,a+3,a+2)}
  const ig=new THREE.BufferGeometry();ig.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));ig.setIndex(idx);ig.computeVertexNormals();
  const im=new THREE.Mesh(ig,new THREE.MeshStandardMaterial({color:0x4a4845,roughness:.28,metalness:.1,side:THREE.DoubleSide}));im.position.copy(m.position);im.rotation.y=m.rotation.y;add(im);
  // zócalo bajo el arco
  const z=new THREE.Mesh(new THREE.BoxGeometry(.07,.004,.21),GRAN);z.position.set(cx,y0+.006,cz);add(z);
  try{colaBVH(m,false)}catch(e){}}
 // fuentes a ras de suelo: dos arcos de chorros a los lados del monumento que suben y bajan en ola
 {const N=window.LITE?14:24,geo=new THREE.CylinderGeometry(.0014,.0024,1,6,1,true).translate(0,.5,0),
   M=new THREE.MeshStandardMaterial({color:0xe6f6ff,roughness:.2,transparent:true,opacity:.6,depthWrite:false,emissive:0x5aa8ff,emissiveIntensity:0}),
   jm=new THREE.InstancedMesh(geo,M,N),P=[],mm=new THREE.Matrix4(),q=new THREE.Quaternion(),V=new THREE.Vector3(),S=new THREE.Vector3();
  for(let i=0;i<N;i++){const lado=i<N/2?1:-1,k=i%(N/2),a=(lado>0?0:Math.PI)+(-.95+1.9*k/(N/2-1)),r=.135;P.push([cx+Math.cos(a)*r,cz+Math.sin(a)*r,k])}
  const rejilla=new THREE.InstancedMesh(new THREE.CircleGeometry(.004,10).rotateX(-Math.PI/2),new THREE.MeshStandardMaterial({color:0x3a3c40,roughness:.5,metalness:.6,emissive:0x8fc6ff,emissiveIntensity:0}),N);
  P.forEach(([x,z],i)=>{mm.compose(V.set(x,y0+.0058,z),q,S.set(1,1,1));rejilla.setMatrixAt(i,mm)});add(rejilla);
  jm.frustumCulled=false;jm.renderOrder=2;jm.userData.pze=1;G.add(jm);
  jm.onBeforeRender=()=>{const t=performance.now()/1000;for(let i=0;i<N;i++){const[x,z,k]=P[i],h=.012+.03*Math.max(0,Math.sin(t*1.6-k*.55))**2;mm.compose(V.set(x,y0+.005,z),q,S.set(1,h,1));jm.setMatrixAt(i,mm)}jm.instanceMatrix.needsUpdate=true;
   let n=0;try{n=CIELO.nf||0}catch(e){}const kN=THREE.MathUtils.smoothstep(n,.15,.6);M.emissiveIntensity=1.4*kN;rejilla.material.emissiveIntensity=2.2*kN}}
 // bancos de granito, árboles en alcorque y farolas alrededor
 {const banco=new THREE.BoxGeometry(.03,.006,.009),pata=new THREE.BoxGeometry(.004,.004,.008);let rs=17;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
  const BAN=[],PAT=[];for(let i=0;i<10;i++){const a=i/10*Math.PI*2+Math.PI/10;if(Math.abs(Math.cos(a))>.93)continue;const r=.172,x=cx+Math.cos(a)*r,z=cz+Math.sin(a)*r,o=new THREE.Object3D();o.position.set(x,y0+.0085,z);o.rotation.y=-a+Math.PI/2;o.updateMatrix();BAN.push(o.matrix.clone());
   for(const s of[-1,1]){const p2=new THREE.Object3D();p2.position.set(x-Math.sin(a)*s*.011,y0+.0065,z+Math.cos(a)*s*.011);p2.rotation.y=o.rotation.y;p2.updateMatrix();PAT.push(p2.matrix.clone())}}
  const ib=new THREE.InstancedMesh(banco,GRAN,BAN.length);BAN.forEach((m,i)=>ib.setMatrixAt(i,m));add(ib,true);
  const ip=new THREE.InstancedMesh(pata,GRAN,PAT.length);PAT.forEach((m,i)=>ip.setMatrixAt(i,m));add(ip);
  // árboles: tronco y copa redondeada, con alcorque de hierro
  const TR=[],CO=[],AL=[];for(let i=0;i<8;i++){const a=i/8*Math.PI*2,r=.195,x=cx+Math.cos(a)*r,z=cz+Math.sin(a)*r,k=.85+rn()*.3;TR.push([x,z,k]);CO.push([x,z,k]);AL.push([x,z])}
  const mm=new THREE.Matrix4(),q=new THREE.Quaternion(),V=new THREE.Vector3(),S=new THREE.Vector3(),col=new THREE.Color();
  const it=new THREE.InstancedMesh(new THREE.CylinderGeometry(.0018,.0025,.03,6).translate(0,.015,0),new THREE.MeshStandardMaterial({color:0x5a4634,roughness:.9}),TR.length);
  TR.forEach(([x,z,k],i)=>{mm.compose(V.set(x,y0+.005,z),q,S.set(1,k,1));it.setMatrixAt(i,mm)});add(it,true);
  const ic=new THREE.InstancedMesh(new THREE.IcosahedronGeometry(.014,1),new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9,flatShading:true}),CO.length);
  CO.forEach(([x,z,k],i)=>{mm.compose(V.set(x,y0+.005+.03*k+.006,z),q,S.set(k,k*.85,k));ic.setMatrixAt(i,mm);ic.setColorAt(i,col.setHex([0x4e8a3a,0x5c9441,0x467f36][i%3]))});add(ic,true);
  const ia=new THREE.InstancedMesh(new THREE.RingGeometry(.006,.009,12).rotateX(-Math.PI/2),new THREE.MeshStandardMaterial({color:0x2d2f33,roughness:.5,metalness:.7}),AL.length);
  AL.forEach(([x,z],i)=>{mm.compose(V.set(x,y0+.0056,z),q,S.set(1,1,1));ia.setMatrixAt(i,mm)});add(ia);
  // cuatro farolas altas en las diagonales
  const FAR=new THREE.MeshStandardMaterial({color:0x2f3236,roughness:.45,metalness:.7}),BOM=new THREE.MeshStandardMaterial({color:0xfff3d6,emissive:0xffd9a0,emissiveIntensity:.3});PAM.bom=BOM;
  for(let i=0;i<4;i++){const a=Math.PI/4+i*Math.PI/2,x=cx+Math.cos(a)*.15,z=cz+Math.sin(a)*.15;
   const f=new THREE.Mesh(new THREE.CylinderGeometry(.0012,.0018,.075,6),FAR);f.position.set(x,y0+.0045+.0375,z);add(f,true);
   const b=new THREE.Mesh(new THREE.SphereGeometry(.0045,10,8),BOM);b.position.set(x,y0+.083,z);add(b)}}
 scene.add(G);G.updateMatrixWorld(true);
 // farolas más fuertes de noche (se actualiza al dibujar el arco)
 PAM.arco.onBeforeRender=()=>{let n=0;try{n=CIELO.nf||0}catch(e){}PAM.bom.emissiveIntensity=.3+3*THREE.MathUtils.smoothstep(n,.15,.6)};
 // quita lo genérico que hubiera en la isleta (dos pasadas: ahora y cuando acaben de subir las piezas de la zona)
 try{PAM.oc=pzeOculta(cx,cz,R-.004,G);setTimeout(()=>{PAM.oc+=pzeOculta(cx,cz,R-.004,G)},4000)}catch(e){console.warn('america oculta',e)}
 PAM.listo=1}
// ---------- fin de america.js
