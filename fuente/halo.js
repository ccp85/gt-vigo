// ---------- Halo y cubierta de Vialia (halo.js)
// Vialia (Morphosis, 2021-2023): la estación intermodal con la plaza pública en la cubierta, con pistas deportivas y skatepark.
// Halo (2024): el ascensor urbano de lo alto de Serafín Avendaño. Torre blanca de base ~6×6 m y, arriba, una pasarela
// colgada en anillo de 90 m de diámetro que se abre en dos arcos y se apoya en el atrio acristalado de la cubierta de Vialia:
// chapa lacada blanca y vidrio serigrafiado; de noche el anillo se ilumina. Posiciones sacadas de la vista aérea de Google
// (torre 42.235826,-8.712245; atrio 42.234976,-8.711848) y pasadas al juego. Las alturas se miden al cargar (rayos contra la
// cubierta y el suelo), así encajan con las piezas del Catastro que ya hay. 1 u = 65 m.
const HAL={T:[101.977,18.595],A:[102.579,20.007],C:[102.275,19.301],R:.69,hecho:0,G:null,
 PISTAS:[[101.97,19.98,'b'],[102.5,20.39,'f'],[101.815,21.43,'s']]};window.__HAL=HAL;
function halChk(){if(HAL.hecho||typeof sueloRap!=='function')return;const[tx,tz]=HAL.T,[ax,az]=HAL.A;
 if(sueloRap(tx,tz)==null||sueloRap(ax,az)==null)return;HAL.hecho=1;setTimeout(()=>{try{halCrea()}catch(e){console.warn('halo',e);HAL.err=String(e);HAL.hecho=0}},1200)}
// lo más alto en un punto: suelo pisable o tejado de un edificio
function halTop(x,z){let h=null;try{h=sueloRap(x,z)}catch(e){}let r=-1;try{if(typeof repMallas==='function')r=repAltura(x,z,repMallas(x,z))}catch(e){}return Math.max(h==null?-1:h,r)}
function halCrea(){const G=new THREE.Group();G.name='haloVialia';HAL.G=G;const[tx,tz]=HAL.T,[cx,cz]=HAL.C,R=HAL.R;
 const BL=new THREE.MeshStandardMaterial({color:0xf2f2ef,roughness:.35,metalness:.25}),
  VID=new THREE.MeshStandardMaterial({color:0xb9ccd6,roughness:.12,metalness:.3,transparent:true,opacity:.72,emissive:0x9fd8ff,emissiveIntensity:0,side:THREE.DoubleSide}),
  SUE=new THREE.MeshStandardMaterial({color:0x8d8e8c,roughness:.8});HAL.vid=VID;
 const yT=sueloRap(tx,tz),yAt=halTop(HAL.A[0],HAL.A[1]);
 // altura del anillo: algo por encima del atrio; si no se puede medir, unos 50 m sobre la calle de la torre
 let yR=(yAt>yT+.2?yAt:yT+.77)+.035;yR=Math.min(yT+1.15,Math.max(yT+.45,yR));HAL.yR=yR;
 const sh=o=>{o.castShadow=!window.LITE;o.receiveShadow=true;G.add(o);return o};
 // torre: núcleo blanco con la cara frontal de vidrio serigrafiado y franjas horizontales
 {const H=yR-yT+.05,b=new THREE.Mesh(new THREE.BoxGeometry(.092,H,.085),BL);b.position.set(tx,yT+H/2,tz);b.rotation.y=Math.atan2(-(cz-tz),cx-tx);sh(b);HAL.torre=b;
  const f=new THREE.Mesh(new THREE.BoxGeometry(.002,H*.94,.07),VID);const dx=Math.cos(b.rotation.y),dz=-Math.sin(b.rotation.y);f.position.set(tx-dx*.047,yT+H*.49,tz-dz*.047);f.rotation.y=b.rotation.y;G.add(f);
  for(let y=.06;y<H-.02;y+=.06){const l=new THREE.Mesh(new THREE.BoxGeometry(.095,.003,.088),BL);l.position.set(tx,yT+y,tz);l.rotation.y=b.rotation.y;G.add(l)}
  // puerta de abajo y remate de arriba
  const p=new THREE.Mesh(new THREE.BoxGeometry(.003,.04,.035),new THREE.MeshStandardMaterial({color:0x2b2f35,roughness:.3,metalness:.4}));p.position.set(tx-dx*.048,yT+.02,tz-dz*.048);p.rotation.y=b.rotation.y;G.add(p);
  try{colaBVH(b,false)}catch(e){}}
 // anillo de 90 m: tablero, pretil blanco por dentro, vidrio por fuera y canto inferior blanco
 {const W=.024,N=window.LITE?72:128;
  const deck=new THREE.RingGeometry(R-W,R+W,N);deck.rotateX(-Math.PI/2);deck.translate(cx,yR,cz);sh(new THREE.Mesh(deck,SUE));
  const bajo=new THREE.RingGeometry(R-W-.004,R+W+.004,N);bajo.rotateX(Math.PI/2);bajo.translate(cx,yR-.012,cz);sh(new THREE.Mesh(bajo,BL));
  const cantoE=new THREE.CylinderGeometry(R+W+.004,R+W+.004,.016,N,1,true);cantoE.translate(cx,yR-.004,cz);sh(new THREE.Mesh(cantoE,BL));
  const cantoI=new THREE.CylinderGeometry(R-W-.004,R-W-.004,.016,N,1,true);cantoI.translate(cx,yR-.004,cz);sh(new THREE.Mesh(cantoI,new THREE.MeshStandardMaterial({color:0xf2f2ef,roughness:.35,metalness:.25,side:THREE.BackSide})));
  // mitad este cerrada por dentro del perfil (vidrio alto) y mitad oeste abierta con barandilla baja, como el de verdad
  const vE=new THREE.CylinderGeometry(R+W,R+W,.04,N,1,true,0,Math.PI);vE.translate(cx,yR+.02,cz);G.add(new THREE.Mesh(vE,VID));
  const tE=new THREE.RingGeometry(R-W,R+W+.004,N,1,0,Math.PI);tE.rotateX(-Math.PI/2);tE.translate(cx,yR+.04,cz);sh(new THREE.Mesh(tE,BL));
  const vO=new THREE.CylinderGeometry(R+W,R+W,.016,N,1,true,Math.PI,Math.PI);vO.translate(cx,yR+.008,cz);G.add(new THREE.Mesh(vO,VID));
  const pi=new THREE.CylinderGeometry(R-W,R-W,.012,N,1,true);pi.translate(cx,yR+.006,cz);G.add(new THREE.Mesh(pi,new THREE.MeshStandardMaterial({color:0xf2f2ef,roughness:.35,side:THREE.DoubleSide})))}
 // pistas deportivas y skatepark en la plaza de la cubierta de Vialia (solo si la cubierta es plana ahí)
 {const ang=Math.atan2(-(20.89-22.43),103.66-100.62),mk=(k)=>{const c=document.createElement('canvas');c.width=128;c.height=72;const x=c.getContext('2d');
   const fondo={b:'#d65b8a',f:'#3f63c9',s:'#3ab3b0'}[k];x.fillStyle=fondo;x.fillRect(0,0,128,72);x.strokeStyle='#ffffff';x.lineWidth=2;
   if(k==='s'){x.fillStyle='rgba(30,40,50,.35)';for(const[a,b,r] of[[30,30,18],[78,42,22],[108,22,12]]){x.beginPath();x.ellipse(a,b,r,r*.7,0,0,6.283);x.fill();x.stroke()}x.strokeRect(4,4,120,64)}
   else{x.strokeRect(6,6,116,60);x.beginPath();x.moveTo(64,6);x.lineTo(64,66);x.stroke();x.beginPath();x.arc(64,36,10,0,6.283);x.stroke();
    if(k==='b'){x.beginPath();x.arc(6,36,22,-1.3,1.3);x.stroke();x.beginPath();x.arc(122,36,22,Math.PI-1.3,Math.PI+1.3);x.stroke()}else{x.strokeRect(6,22,14,28);x.strokeRect(108,22,14,28)}}
   const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=4;return t};
  for(const[x,z,k] of HAL.PISTAS){const w=k==='s'?.3:.34,d=k==='s'?.2:.19,y0=halTop(x,z);if(y0<0)continue;let ok=true;
   for(const[a,b] of[[-1,-1],[1,-1],[-1,1],[1,1]]){const px=x+Math.cos(ang)*a*w/2+Math.sin(ang)*b*d/2,pz=z-Math.sin(ang)*a*w/2+Math.cos(ang)*b*d/2;if(Math.abs(halTop(px,pz)-y0)>.012){ok=false;break}}
   if(!ok)continue;const g=new THREE.PlaneGeometry(w,d);g.rotateX(-Math.PI/2);const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({map:mk(k),roughness:.8,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3}));
   m.position.set(x,y0+.0015,z);m.rotation.y=ang;m.receiveShadow=true;G.add(m);
   if(k==='b')for(const s of[-1,1]){const p=[x+Math.cos(ang)*s*(w/2-.012),z-Math.sin(ang)*s*(w/2-.012)],c=new THREE.Mesh(new THREE.CylinderGeometry(.0012,.0012,.05,5),new THREE.MeshStandardMaterial({color:0x2b2f35}));c.position.set(p[0],y0+.025,p[1]);G.add(c);
    const tb=new THREE.Mesh(new THREE.BoxGeometry(.003,.016,.025),BL);tb.position.set(p[0]-Math.cos(ang)*s*.004,y0+.05,p[1]+Math.sin(ang)*s*.004);tb.rotation.y=ang+Math.PI/2;G.add(tb)}}}
 scene.add(G);G.updateMatrixWorld(true);
 // de noche el anillo se enciende
 HAL.torre.onBeforeRender=()=>{let n=0;try{n=CIELO.nf||0}catch(e){}VID.emissiveIntensity=1.1*THREE.MathUtils.smoothstep(n,.15,.6)};
 HAL.listo=1}
// ---------- fin de halo.js
