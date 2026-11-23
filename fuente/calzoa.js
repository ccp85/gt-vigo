// ---------- playa da Calzoa / As Barcas (calzoa.js) ----------
// Coruxo, al final de Samil y separada de él por la desembocadura del Lagares. Modelos propios a partir de fotos
// (satélite, 3D y a pie de calle) como referencia: arenal rectilíneo de arena clara, dunas con matorral, senda de tierra
// con postes, hierba con dornas y chalanas varadas (las barcas que dan nombre a la playa), plaza con árboles, bancos,
// fuente y mesas redondas, rampa de hormigón desde la carretera con barandilla, muro con grafitis, malecón de la
// carretera hacia Canido con rocas al pie, bolos de granito en el agua, el conjunto de apartamentos escalonados con su
// piscina y el muro blanco a la arena, y el Lagares cortando la playa con su banco de arena y la arena mojada.
// Todo se coloca siguiendo la línea de costa del mapa (coordenadas u = a lo largo de la playa, v = tierra adentro).
const CALZ={hecha:0,A:[18.0,77.75],B:[22.35,74.05]};window.__CALZ=CALZ;
function calChk(){if(CALZ.hecha||!MAPA||!MI)return;const z=ZROOTS.find(q=>q.root&&q.root.name==='samil'&&q.root.parent);if(!z)return;
 if(cell(20,75.6).t<0)return;CALZ.hecha=1;CALZ.root=z.root;setTimeout(()=>{try{calCrea()}catch(e){console.warn('calzoa',e);CALZ.err=String(e)+' '+String(e.stack).slice(0,600)}},1500)}
function calCrea(){const LT=!!window.LITE,G=new THREE.Group();G.name='calzoa';
 const t=(x,y)=>cell(x,y).t,gy=(x,z)=>{let v=null;try{v=sueloRap(x,z)}catch(e){}return v==null?groundY(x,z):v};
 const[ax,ay]=CALZ.A,[bx,by]=CALZ.B,L0=Math.hypot(bx-ax,by-ay),TX=(bx-ax)/L0,TY=(by-ay)/L0,NX=-TY,NY=TX; // N: tierra adentro (SE)
 const nS=NX>0?[-NX,-NY]:[NX,NY];const IN=[-nS[0],-nS[1]];
 // ---- línea de costa: para cada u (de -1.8, malecón hacia Canido, a L0) se busca el agua hacia el mar
 const U0=-1.8,DU=.04,S=[];
 for(let u=U0;u<=L0+.001;u+=DU){const px=ax+TX*u,py=ay+TY*u;let hit=null;
  // marcha desde tierra (+1.2 tierra adentro) hacia el mar hasta la primera celda de agua
  for(let d=1.4;d>-1.6;d-=.01){const x=px+IN[0]*d,y=py+IN[1]*d;if(t(x,y)===0){hit=d+.01;break}}
  S.push([u,hit==null?0:hit])}
 for(let it=0;it<5;it++)for(let i=1;i<S.length-1;i++)S[i][1]=(S[i-1][1]+2*S[i][1]+S[i+1][1])/4;
 // distancia de la orilla a la primera calzada (la plaza y la rampa no pueden pisar la carretera)
 for(const q of S){const px=ax+TX*q[0],py=ay+TY*q[0];let rd=2;for(let d=q[1];d<q[1]+2;d+=.01){if(t(px+IN[0]*d,py+IN[1]*d)===2){rd=d-q[1];break}}q.push(rd)}
 for(let it=0;it<3;it++)for(let i=1;i<S.length-1;i++)S[i][2]=(S[i-1][2]+2*S[i][2]+S[i+1][2])/4;
 const shc=(u,c)=>{if(!(u>-1e6&&u<1e6))return 0;const f=(u-U0)/DU,i=Math.max(0,Math.min(S.length-2,Math.floor(f))),k=Math.max(0,Math.min(1,f-i));return S[i][c]*(1-k)+S[i+1][c]*k},sh=u=>shc(u,1),rdv=u=>shc(u,2);
 // de (u,v) a mundo: v = metros/100 tierra adentro desde la orilla
 const W=(u,v)=>{const d=sh(u)+v;return[ax+TX*u+IN[0]*d,ay+TY*u+IN[1]*d]};
 const UV=(x,y)=>{const u=(x-ax)*TX+(y-ay)*TY,d=(x-ax)*IN[0]+(y-ay)*IN[1];return[u,d-sh(u)]};
 const ANG=Math.atan2(-TY,TX); // rotación Y para alinear el eje x local con la playa
 CALZ.W=W;CALZ.UV=UV;
 // ---- materiales y utilidades (todo se junta en una malla por material)
 const PARTS=new Map(),add=(geo,mat,x,y,z,ry=0,rx=0,rz=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();if(g.attributes.uv&&!mat.map)g.deleteAttribute('uv');if(rz)g.rotateZ(rz);if(rx)g.rotateX(rx);if(ry)g.rotateY(ry);g.translate(x,y,z);if(!PARTS.has(mat))PARTS.set(mat,[]);PARTS.get(mat).push(g)};
 const addUV=(u,v,geo,mat,h=0,ry=0)=>{const[x,z]=W(u,v);add(geo,mat,x,gy(x,z)+h,z,ANG+ry)};
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.85},o));
 const PO={polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2};
 let rs=7;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const HOR=M(0xb9b4aa,{roughness:.95}),GRA=M(0x9c968c,{roughness:.95}),GRAO=M(0x6f6a62,{roughness:1}),BLA=M(0xf1efe8),BLA2=M(0xdedbd2),
  TEJ=M(0x5b5450,{roughness:.9}),VID=M(0x4a5866,{roughness:.2,metalness:.3}),JAR=M(0x5f8f3c,{roughness:.9}),HIE=M(0x5f656d,{metalness:.6,roughness:.4}),MAD=M(0x8a6440),MADO=M(0x5e4430),
  TRO=M(0x5a4532),HO1=M(0x3b5a2a,{roughness:.9}),HO2=M(0x4c6e33,{roughness:.9}),PIN=M(0x2f4a2a,{roughness:.9}),OCR=M(0x958459,{roughness:1,...PO}),CES=M(0x7a9858,{roughness:1,...PO}),
  TIE=M(0xc9b38a,{roughness:1,...PO}),DUN=M(0xffffff,{roughness:1,vertexColors:true}),MAT=M(0x6e6a40),MAT2=M(0x9a8656),BARR=M(0xd9cf9a),
  ARM=M(0xd8ccb0,{roughness:1,...PO}),MOJ=M(0xb8ab8c,{roughness:.55,transparent:true,opacity:.55,depthWrite:false,side:THREE.DoubleSide,...PO}),
  AGUAF=new THREE.MeshStandardMaterial({color:0x58b8b0,roughness:.12,metalness:.05,transparent:true,opacity:.82,emissive:0x0d3b3a,emissiveIntensity:.35,depthWrite:false,side:THREE.DoubleSide,...PO}),
  AGUAH=new THREE.MeshStandardMaterial({color:0x2f8a8c,roughness:.1,transparent:true,opacity:.7,emissive:0x082a2c,emissiveIntensity:.3,depthWrite:false,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3}),
  PIS=new THREE.MeshStandardMaterial({color:0x6fd3ef,roughness:.1,emissive:0x0e5a78,emissiveIntensity:.35}),
  ROC=M(0x5e4433,{roughness:1}),RMA=M(0x5e4433,{roughness:1}),RG1=M(0x6a4c37,{roughness:1}),ROR=M(0x8b5b45,{roughness:1}),ALG=M(0x3e4a2a,{roughness:1}),FAR=M(0xfff3cf,{emissive:0xffdc8a,emissiveIntensity:.7});
 const BCOL=[0xf4f4f0,0xf4f4f0,0x2f6fb0,0x3f8f5a,0xd9d2c0,0x7fb7d9,0xb84a3a].map(c=>M(c,{roughness:.6}));
 const cil=(a,b,h,s=8)=>new THREE.CylinderGeometry(a,b,h,s),cub=(a,b,c)=>new THREE.BoxGeometry(a,b,c);
 // grafitis: textura propia (letras y tags inventados) sobre hormigón
 const grafiti=(sd)=>{const c=document.createElement('canvas');c.width=512;c.height=128;const g=c.getContext('2d');let r=sd;const R=()=>(r=(r*16807)%2147483647)/2147483647;
  g.fillStyle='#b4afa5';g.fillRect(0,0,512,128);for(let i=0;i<900;i++){g.fillStyle=`rgba(${70+R()*60|0},${70+R()*55|0},${65+R()*50|0},${.08+R()*.15})`;g.fillRect(R()*512,R()*128,2+R()*6,2+R()*4)}
  for(let i=0;i<12;i++){g.fillStyle=`rgba(60,70,60,${.1+R()*.1})`;g.fillRect(R()*512,90+R()*38,30+R()*80,4+R()*8)}
  const W_=['CORUXO','BARCAS','LAGARES','CALZOA','RÍA','OLA','VIGO','MAR'],C_=['#e2402e','#2f7fd6','#f2c230','#2fae6a','#e85fb0','#f0f0f0','#1d1d24','#f28a2e','#7a4fd0'];
  for(let k=0;k<5;k++){const x=R()*420,y=40+R()*70,s=26+R()*36;g.save();g.translate(x,y);g.rotate((R()-.5)*.25);g.font=`900 ${s|0}px Impact, Arial Black, sans-serif`;
   const w=W_[R()*W_.length|0];g.lineJoin='round';g.lineWidth=s*.22;g.strokeStyle=C_[R()*C_.length|0];g.strokeText(w,0,0);g.fillStyle=C_[R()*C_.length|0];g.fillText(w,0,0);g.lineWidth=2;g.strokeStyle='#111';g.strokeText(w,0,0);g.restore()}
  for(let k=0;k<6;k++){g.strokeStyle=C_[R()*C_.length|0];g.lineWidth=2+R()*3;g.beginPath();let x=R()*512,y=30+R()*90;g.moveTo(x,y);for(let q=0;q<5;q++){x+=10+R()*20;y+=(R()-.5)*30;g.lineTo(x,y)}g.stroke()}
  const tx=new THREE.CanvasTexture(c);tx.colorSpace=THREE.SRGBColorSpace;tx.wrapS=THREE.RepeatWrapping;tx.anisotropy=4;return tx};
 const GRF1=M(0xffffff,{map:grafiti(31),roughness:.95}),GRF2=M(0xffffff,{map:grafiti(977),roughness:.95});
 // muro vertical siguiendo una curva de puntos [x,z] con base en el suelo y altura h (cara con textura)
 const muro=(pts,h0,grosor,mat,top=GRA,base=0,yf=null)=>{let acc=0;for(let i=0;i<pts.length-1;i++){const[x1,z1]=pts[i],[x2,z2]=pts[i+1],dl=Math.hypot(x2-x1,z2-z1);if(dl<1e-4)continue;const a=Math.atan2(-(z2-z1),x2-x1),mx=(x1+x2)/2,mz=(z1+z2)/2;let y0=Math.min(gy(x1,z1),gy(x2,z2))+base,h=h0;if(yf){const q=yf(mx,mz);y0=q[0];h=q[1]-q[0]}
   const g=new THREE.BoxGeometry(dl,h,grosor);if(mat.map){const uv=g.attributes.uv;for(let k=0;k<uv.count;k++)uv.setX(k,(acc+uv.getX(k)*dl)/.35)}acc+=dl;add(g,mat,mx,y0+h/2,mz,a);add(cub(dl+.002,.003,grosor+.004),top,mx,y0+h+.0015,mz,a)}};
 const baranda=(pts,y0f,h=.011)=>{for(let i=0;i<pts.length-1;i++){const[x1,z1]=pts[i],[x2,z2]=pts[i+1],dl=Math.hypot(x2-x1,z2-z1);if(dl<1e-4)continue;const a=Math.atan2(-(z2-z1),x2-x1),y1=y0f(x1,z1),y2=y0f(x2,z2);
   add(cil(.0006,.0006,h,5),HIE,x1,y1+h/2,z1);const g=cub(dl,.0009,.0009);const p=g.attributes.position;for(let k=0;k<p.count;k++){const f=p.getX(k)/dl+.5;p.setY(k,p.getY(k)+(y2-y1)*f)}
   const g2=g.clone();add(g,HIE,(x1+x2)/2,y1+h,(z1+z2)/2,a);add(g2,HIE,(x1+x2)/2,y1+h*.5,(z1+z2)/2,a)}};
 const arbol=(x,z,s=1,tipo=0,yb=null)=>{const y=yb==null?gy(x,z):yb,h=(.045+rn()*.02)*s;add(cil(.0022*s,.0034*s,h,6),TRO,x,y+h/2,z);
  if(tipo===1){for(let k=0;k<3;k++){const r=(.018-.004*k)*s;add(new THREE.ConeGeometry(r,.03*s,7),PIN,x,y+h+.01*s+k*.016*s,z)}return}
  for(let k=0;k<6;k++){const r=(.016+rn()*.012)*s,a=rn()*6.28,d=rn()*.016*s,g=new THREE.DodecahedronGeometry(r,0);g.scale(1,.75,1);add(g,rn()<.5?HO1:HO2,x+Math.cos(a)*d,y+h+.006*s+rn()*.014*s,z+Math.sin(a)*d,rn()*6)}};
 // ---- ocultar lo genérico que había en la zona (árboles, rocas y piezas sueltas de la zona en instancias)
 const ocultar=dentro=>{const mm=new THREE.Matrix4(),pp=new THREE.Vector3(),q=new THREE.Quaternion(),sc=new THREE.Vector3();let n=0;
  scene.traverse(o=>{if(!o.isInstancedMesh||o.parent===G||o.count>5000)return;let ch=false;for(let k=0;k<o.instanceMatrix.count;k++){o.getMatrixAt(k,mm);mm.decompose(pp,q,sc);if(sc.x<=0)continue;const w=pp.clone().applyMatrix4(o.matrixWorld);if(dentro(w.x,w.z)){sc.setScalar(0);mm.compose(pp,q,sc);o.setMatrixAt(k,mm);ch=true;n++}}if(ch)o.instanceMatrix.needsUpdate=true});CALZ.oc=(CALZ.oc||0)+n};
 // ---- piezas fijas de la zona que sobran: edificios del catastro donde va el conjunto escalonado y el verde pegado al agua
 const colapsar=(prueba)=>{const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();let k=0;CALZ.root.updateMatrixWorld(true);
  CALZ.root.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||GROUND.includes(o)||o.userData.suelo||/^(verde|tierra|playa|playita|calzada|aceras|agua)/.test(o.name))return;const g=o.geometry,ix=g.index,pos=g.attributes.position;if(!pos)return;if(!g.boundingBox)g.computeBoundingBox();
   const bb=g.boundingBox.clone().applyMatrix4(o.matrixWorld);if(bb.max.x<17||bb.min.x>23.6||bb.max.z<73.5||bb.min.z>78.6)return;const mw=o.matrixWorld;let ch=0;
   const I=j=>ix?ix.getX(j):j,cnt=ix?ix.count:pos.count;
   for(let i=0;i+2<cnt;i+=3){a.fromBufferAttribute(pos,I(i)).applyMatrix4(mw);b.fromBufferAttribute(pos,I(i+1)).applyMatrix4(mw);c.fromBufferAttribute(pos,I(i+2)).applyMatrix4(mw);
    const mx=(a.x+b.x+c.x)/3,mz=(a.z+b.z+c.z)/3,my=Math.max(a.y,b.y,c.y);if(prueba(o.name,mx,mz,my,o.material&&o.material.color?o.material.color.getHex():null)){if(ix){const i0=ix.getX(i);ix.setX(i+1,i0);ix.setX(i+2,i0)}else{for(const j of[i+1,i+2])pos.setXYZ(j,pos.getX(i),pos.getY(i),pos.getZ(i))}ch++}}
   if(ch){if(ix)ix.needsUpdate=true;else pos.needsUpdate=true;k+=ch;if(o.geometry.boundsTree)try{o.geometry.computeBoundsTree()}catch(e){}}});return k};
 // zonas (en u,v)
 const PARQ=[.35,.85],DORN=[.95,1.65],DUNA=[1.75,3.0],COMP=[3.05,5.3],FIN=L0;
 const enComp=(x,z)=>{const[u,v]=UV(x,z);return u>COMP[0]-.05&&u<COMP[1]+.12&&v>.28&&v<1.2};
 const enPlaya=(x,z)=>{const[u,v]=UV(x,z);return u>-.1&&u<FIN+.1&&v>-.35&&v<.78&&!(u>COMP[0]&&v>.5)};
 const enParque=(x,z)=>{const[u,v]=UV(x,z);return u>PARQ[0]-.05&&u<PARQ[1]+.05&&v>-.05&&v<.75};
 // ---- el Lagares: de debajo del puente hasta el mar, cortando la arena
 const RIO=[[22.66,77.05],[22.72,76.55],[22.7,76.0],[22.62,75.45],[22.5,74.95],[22.36,74.45],[22.18,73.95],[21.98,73.5]],AR=[.07,.08,.1,.12,.15,.19,.24,.3];
 const rioD=(x,z)=>{let m=1e9,w=.1;for(let i=1;i<RIO.length;i++){const p=RIO[i-1],q=RIO[i],dx=q[0]-p[0],dz=q[1]-p[1],l2=dx*dx+dz*dz,f=Math.max(0,Math.min(1,((x-p[0])*dx+(z-p[1])*dz)/l2)),d=Math.hypot(x-p[0]-f*dx,z-p[1]-f*dz);if(d<m){m=d;w=AR[i-1]*(1-f)+AR[i]*f}}return[m,w]};
 CALZ.rioD=rioD;
 ocultar((x,z)=>enComp(x,z)||enPlaya(x,z)&&!(UV(x,z)[0]<PARQ[1]&&UV(x,z)[1]>.6)||rioD(x,z)[0]<rioD(x,z)[1]+.04);
 const ARB=[0x5a4332,0x335f34,0x386b39,0x497935,0x54803d,0x4e7e37,0x5d8b43,0x6a9b4f];
 CALZ.col=colapsar((nm,x,z,y,col)=>{if(/^muro_costa/.test(nm)){const[u,v]=UV(x,z);return u>U0&&u<FIN+.05&&v>-.6&&v<.6}
  if(/^(agua|playa|playita|calzada|aceras|labio|zocalo|lineas|ori|tierra|puentes)/.test(nm))return false;
  if(enComp(x,z)&&y>gy(x,z)+.008)return true;                                   // edificios del catastro del conjunto
  if(/^piezas/.test(nm)&&col!=null&&ARB.includes(col)){const[u,v]=UV(x,z);if(u>PARQ[1]+.05&&u<FIN&&v<.45)return true}
  if(/^faldon/.test(nm)){const[u,v]=UV(x,z);if(u>PARQ[0]&&u<FIN+.1&&v<.42||u>U0&&u<=PARQ[0]&&v<.05)return true}  // franja verde pegada al agua sobre la arena
  const[d,w]=rioD(x,z);if(d<w&&y>gy(x,z)+.006&&!/^(edificios|tejado)/.test(nm))return true;return false});
 {let nT=TROZOS.length,veces=0;const iv=setInterval(()=>{if(TROZOS.length!==nT){nT=TROZOS.length;ocultar((x,z)=>enComp(x,z)||enPlaya(x,z)||rioD(x,z)[0]<rioD(x,z)[1]+.04)}if(++veces>90)clearInterval(iv)},2000)}

 // ---- cauce del río: lámina de agua turquesa, centro más hondo, orillas de arena mojada y banco de arena (tómbolo)
 {const ribbon=(wf,yo,mat)=>{const pos=[],idx=[];let n=0;for(let i=0;i<RIO.length-1;i++){const p=RIO[i],q=RIO[i+1];for(let s=0;s<6;s++){const f=s/6,x=p[0]+(q[0]-p[0])*f,z=p[1]+(q[1]-p[1])*f,dx=q[0]-p[0],dz=q[1]-p[1],l=Math.hypot(dx,dz),w=(AR[i]*(1-f)+AR[i+1]*f)*wf,
    wob=1+.12*Math.sin((i*6+s)*1.3),nx=-dz/l,nz=dx/l;for(const sg of[-1,1]){const xx=x+nx*w*wob*sg,zz=z+nz*w*wob*sg;pos.push(xx,Math.max(.002,gy(xx,zz))+yo,zz)}if(n){const k=(n-1)*2;idx.push(k,k+2,k+1,k+1,k+2,k+3)}n++}}
   const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();const m=new THREE.Mesh(g,mat);m.receiveShadow=true;m.renderOrder=2;G.add(m);return m};
  ribbon(1.35,.0035,MOJ);ribbon(1,.005,AGUAF);ribbon(.45,.0058,AGUAH);
  // banco de arena en la boca, del lado del conjunto (en bajamar se cruza a pie hacia Samil)
  {const c=[22.05,74.35],g=new THREE.CircleGeometry(.2,28);g.rotateX(-Math.PI/2);g.scale(1.5,1,.55);g.rotateY(.75);const p=g.attributes.position;for(let k=0;k<p.count;k++){const x=p.getX(k)+c[0],z=p.getZ(k)+c[1];p.setY(k,Math.max(.002,gy(x,z))+.0066)}g.translate(c[0],0,c[1]);add(g,ARM,0,0,0)}
  CALZ.rio=1}

 // ---- malecón de la carretera hacia Canido (u<0): muro alto de hormigón y granito con grafitis, barandilla y rocas al pie
 {const pts=[];for(let u=U0;u<=PARQ[0]+.02;u+=.05)pts.push(W(u,.02));const top=(x,z)=>{const[u]=UV(x,z);return gy(...W(u,.06))+.009};muro(pts,0,.014,GRF1,GRA,0,(x,z)=>[-.02,top(x,z)]);
  baranda(pts,(x,z)=>top(x,z)+.003);
  for(let u=U0;u<PARQ[0];u+=.025){const[x,z]=W(u,-.02-rn()*.03),r=.008+rn()*.012,g=new THREE.DodecahedronGeometry(r,0);g.scale(1,.7,1);add(g,rn()<.3?ALG:ROC,x,-.004+r*.3,z,rn()*6)}}
 // ---- bolos de granito en el agua frente a la plaza (pardo-rojizos con algas) y alguna roca en la orilla
 for(let k=0;k<(LT?14:24);k++){const u=-1.0+rn()*3.2,v=-.25-rn()*1.1,[x,z]=W(u,v);if(t(x,z)!==0)continue;const r=.008+rn()*.016,g=new THREE.DodecahedronGeometry(r,0);g.scale(1.2+rn()*.5,.4,1+rn()*.4);add(g,rn()<.5?RMA:RG1,x,-.016+rn()*.01,z,rn()*6)}
 for(let k=0;k<10;k++){const u=PARQ[1]+rn()*1.2,v=-.04-rn()*.08,[x,z]=W(u,v),r=.006+rn()*.01,g=new THREE.DodecahedronGeometry(r,0);g.scale(1,.5,1);add(g,ROC,x,gy(x,z)-.001,z,rn()*6)}

 // ---- plaza de As Barcas (u -0.05..0.5): plataforma de hormigón sobre la arena con árboles, fuente, mesas y bancos
 {const H=.022,P=[],VB=u=>Math.max(.3,Math.min(.6,rdv(u)-.05));for(let u=PARQ[0];u<=PARQ[1]+.001;u+=.05)P.push([u,.12+.06*Math.sin((u-PARQ[0])/(PARQ[1]-PARQ[0])*Math.PI)]);
  // muro de contención curvo hacia la playa (con grafitis), y el muro de atrás que la separa de la carretera
  const fr=P.map(([u,v])=>W(u,v));muro(fr,H,.012,GRF2,HOR,-.004);
  muro([W(PARQ[0],.12),W(PARQ[0],VB(PARQ[0]))],H+.004,.012,GRF1,HOR,-.004);{const pts=[];for(let u=PARQ[0];u<=PARQ[1]+.001;u+=.05)pts.push(W(u,VB(u)));muro(pts,H+.012,.01,GRF2,HOR,-.004)}
  // suelo de la plaza (tierra apisonada) y céspedes
  {const pos=[],idx=[];let n=0;for(const[u,v]of P){for(const vv of[v,VB(u)]){const[x,z]=W(u,vv);pos.push(x,Math.max(gy(x,z),gy(...W(u,v)))+H-.004,z)}if(n){const k=(n-1)*2;idx.push(k,k+2,k+1,k+1,k+2,k+3)}n++}
   const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();add(g.toNonIndexed(),TIE,0,0,0);CALZ.plazaY=pos[1]}
  const py=(u,v)=>{const[x,z]=W(u,v);return Math.max(gy(x,z),gy(...W(u,.15)))+H};
  for(const[u0,u1,v0,v1]of[[.0,.14,.3,.5],[.32,.46,.3,.5]].map(q=>[PARQ[0]+q[0],PARQ[0]+q[1],q[2],Math.min(q[3],VB(PARQ[0]+q[1])-.03)])){const pos=[];const q=(u,v)=>{const[x,z]=W(u,v);return[x,py(u,v)+.0005,z]};const a=q(u0,v0),b=q(u1,v0),c=q(u1,v1),d=q(u0,v1);pos.push(...a,...c,...b,...a,...d,...c);const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.computeVertexNormals();add(g,CES,0,0,0)}
  // fuente circular en el centro
  {const[x,z]=W(PARQ[0]+.23,.32),y=py(PARQ[0]+.23,.32);add(new THREE.TorusGeometry(.022,.0045,6,20),GRA,x,y+.003,z,0,Math.PI/2);add(cil(.02,.02,.002,20),new THREE.MeshStandardMaterial({color:0x6fa9b8,roughness:.1,emissive:0x123a44,emissiveIntensity:.3}),x,y+.003,z);add(cil(.003,.004,.012,8),GRA,x,y+.006,z);add(cil(.006,.003,.003,10),GRA,x,y+.013,z)}
  // árboles grandes que dan sombra (y un pino)
  for(const[u_,v,s,tp]of[[.06,.4,1.35,0],[.14,.2,1.2,0],[.27,.44,1.25,0],[.38,.22,1.3,0],[.45,.42,1.1,0],[.02,.26,1,1]]){const u=PARQ[0]+u_;const[x,z]=W(u,v);arbol(x,z,s,tp,py(u,v))}
  // los árboles se apoyan en la plaza, no en la arena: se suben a la altura de la plataforma
  // mesas redondas con taburetes y bancos de piedra
  for(const[u_,v]of[[.1,.44],[.33,.36],[.4,.24]]){const u=PARQ[0]+u_;const[x,z]=W(u,v),y=py(u,v);add(cil(.009,.009,.0018,12),HOR,x,y+.009,z);add(cil(.0018,.0025,.008,6),HOR,x,y+.004,z);for(let k=0;k<4;k++){const a=k*Math.PI/2+.4;add(cil(.0032,.0032,.0045,8),HOR,x+Math.cos(a)*.015,y+.0022,z+Math.sin(a)*.015)}}
  for(const[u_,v,r]of[[.04,.2,0],[.2,.17,0],[.31,.17,0],[.47,.3,Math.PI/2],[.16,.45,0]]){const u=PARQ[0]+u_;const[x,z]=W(u,v),y=py(u,v);add(cub(.03,.0025,.009),GRA,x,y+.0045,z,ANG+r);add(cub(.004,.0045,.008),GRAO,x-.011*Math.cos(ANG+r),y+.0022,z+.011*Math.sin(ANG+r),ANG+r);add(cub(.004,.0045,.008),GRAO,x+.011*Math.cos(ANG+r),y+.0022,z-.011*Math.sin(ANG+r),ANG+r)}
  // farolas
  for(const[u_,v]of[[.02,.45],[.44,.45]]){const u=PARQ[0]+u_;const[x,z]=W(u,v),y=py(u,v);add(cil(.001,.0014,.04,6),HIE,x,y+.02,z);add(cub(.006,.007,.006),FAR,x,y+.043,z)}
  // escaleras de la plaza a la arena
  {const u=PARQ[0]+.25,v=.06+.06;for(let k=0;k<5;k++){const[x,z]=W(u,v-.008-k*.009);add(cub(.05,.0045,.009),HOR,x,gy(x,z)+H-.0045*(k+1)+.002,z,ANG)}}
  CALZ.parque=1}
 // la plaza está a la altura del muro: los árboles, mesas y bancos se dibujan sobre ella (sus piezas ya usan py)
 // ---- rampa de hormigón desde la carretera hasta la arena, con barandilla metálica
 {const u=PARQ[1]+.05,v0=Math.max(.3,rdv(PARQ[1]+.05)),v1=.18,N_=10,pos=[],idx=[],w=.022;const r0=W(u,v0);const yTop=gy(...r0);
  for(let i=0;i<=N_;i++){const v=v0+(v1-v0)*i/N_,[x,z]=W(u,v),yb=gy(x,z),y=Math.max(yb+.003,yTop+(gy(...W(u,v1))-yTop)*i/N_+.003);for(const s of[-1,1]){pos.push(x+TX*w*s,y,z+TY*w*s)}if(i){const k=(i-1)*2;idx.push(k,k+1,k+2,k+1,k+3,k+2)}}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();add(g.toNonIndexed(),HOR,0,0,0);
  const lado=s=>{const pts=[];for(let i=0;i<=N_;i+=2){const v=v0+(v1-v0)*i/N_,[x,z]=W(u,v);pts.push([x+TX*(w+.002)*s,z+TY*(w+.002)*s,pos[(i*2)*3+1]])}return pts};
  for(const s of[-1,1]){const pts=lado(s);baranda(pts.map(p=>[p[0],p[1]]),(x,z)=>{let b=pts[0];for(const p of pts)if(Math.hypot(p[0]-x,p[1]-z)<Math.hypot(b[0]-x,b[1]-z))b=p;return b[2]})}
  // senda de tierra que sale del pie de la rampa y corre tras las dunas hasta el conjunto
  const pos2=[],idx2=[];let n=0;for(let uu=u;uu<=COMP[0]+.15;uu+=.04){const v=.74+.05*Math.sin(uu*1.7)+(uu>COMP[0]-.3?-(uu-(COMP[0]-.3))*.5:0),[x,z]=W(uu,v),ww=.018;for(const s of[-1,1]){const xx=x+IN[0]*ww*s,zz=z+IN[1]*ww*s;pos2.push(xx,gy(xx,zz)+.0045,zz)}if(n){const k=(n-1)*2;idx2.push(k,k+2,k+1,k+1,k+2,k+3)}n++;
   // postes de madera con cuerda al lado de tierra
   if(n%2===0&&uu<COMP[0]-.2){const[px,pz]=W(uu,v+.028);add(cil(.0011,.0013,.012,5),MAD,px,gy(px,pz)+.006,pz)}}
  const g2=new THREE.BufferGeometry();g2.setAttribute('position',new THREE.Float32BufferAttribute(pos2,3));g2.setIndex(idx2);g2.computeVertexNormals();add(g2.toNonIndexed(),TIE,0,0,0)}

 // ---- hierba con dornas y chalanas varadas (las barcas que dan nombre a la playa)
 {const pos=[];const tri=(a,b,c)=>pos.push(...a,...b,...c);const q=(u,v)=>{const[x,z]=W(u,v);return[x,gy(x,z)+.004,z]};
  for(let u=DORN[0];u<DORN[1];u+=.05){const va=.34+.05*Math.sin(u*9),vb=.34+.05*Math.sin((u+.05)*9);tri(q(u,va),q(u,.7),q(u+.05,vb));tri(q(u+.05,vb),q(u,.7),q(u+.05,.7))}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.computeVertexNormals();add(g,OCR,0,0,0);
  const barca=(len,anch,alt)=>{const g=new THREE.BoxGeometry(len,alt,anch,6,1,2);const p=g.attributes.position;for(let k=0;k<p.count;k++){const f=Math.abs(p.getX(k))/(len/2),y=p.getY(k);p.setZ(k,p.getZ(k)*(1-Math.pow(f,2.2)*.85)*(y<0?.75:1));p.setY(k,y+(f>.6?(f-.6)*alt*.9:0))}g.computeVertexNormals();return g};
  for(let k=0;k<(LT?9:15);k++){const u=DORN[0]+.05+rn()*(DORN[1]-DORN[0]-.1),v=.4+rn()*.25,[x,z]=W(u,v),len=.035+rn()*.02,ry=ANG+Math.PI/2+(rn()-.5)*.7,boca=rn()<.45;
   const cm=BCOL[(rn()*BCOL.length)|0];const y=gy(x,z)+.006;const h=barca(len,.014+len*.12,.008);if(boca)h.rotateX(Math.PI);add(h,cm,x,y+(boca?.001:0),z,ry,0,(rn()-.5)*.12);
   if(!boca){add(cub(len*.8,.0012,.003),MADO,x,y+.003,z,ry);add(cub(.003,.0013,.013),MADO,x,y+.0035,z,ry)}else add(cub(len*.9,.0008,.0025),BCOL[2],x,y+.0045,z,ry)}
  // alguna barca también en la arena, junto a la orilla
  for(let k=0;k<3;k++){const[x,z]=W(DORN[0]+rn()*.6,.15+rn()*.1),ry=rn()*3;add(new THREE.BoxGeometry(.04,.006,.014),BCOL[k%BCOL.length],x,gy(x,z)+.004,z,ry)}}

 // ---- dunas con matorral pardo (dos lóbulos separados por un paso de arena)
 {const lob=[[DUNA[0],2.05],[2.15,DUNA[1]]];for(const[u0,u1]of lob){const nu=18,nv=7,pos=[],col=[],idx=[];for(let i=0;i<=nu;i++)for(let j=0;j<=nv;j++){const fu=i/nu,fv=j/nv,ra=1+.18*Math.sin(fu*11+u0*3)+.1*Math.sin(fu*23),u=u0+(u1-u0)*fu,v=.44+.26*(fv-.5)*ra+.13+.02*Math.sin(u*13),e=Math.pow(Math.sin(fu*Math.PI)*Math.sin(fv*Math.PI),.6),[x,z]=W(u,v);
    pos.push(x,gy(x,z)+.0025+e*.012+(rn()-.5)*.0015*e,z);const c=new THREE.Color(rn()<.5?0x9c8a63:0x8a7b57).lerp(new THREE.Color(0x9a9a62),rn()*.35).lerp(new THREE.Color(0xe6d7b4),Math.pow(1-e,3));col.push(c.r,c.g,c.b)}
   for(let i=0;i<nu;i++)for(let j=0;j<nv;j++){const a=i*(nv+1)+j;idx.push(a,a+1,a+nv+1,a+1,a+nv+2,a+nv+1)}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.setIndex(idx);g.computeVertexNormals();
   const m=new THREE.Mesh(g,DUN);m.receiveShadow=true;G.add(m);
   for(let k=0;k<(LT?40:90);k++){const u=u0+.03+rn()*(u1-u0-.06),fv=.15+rn()*.7,v=.42+.3*fv,[x,z]=W(u,v),e=Math.sin(((u-u0)/(u1-u0))*Math.PI)*Math.sin(fv*Math.PI),r=.004+rn()*.006,gg=new THREE.IcosahedronGeometry(r,0);gg.scale(1,.6,1);add(gg,rn()<.6?MAT:MAT2,x,gy(x,z)+.002+e*.012+r*.4,z,rn()*6)}
   for(let k=0;k<(LT?14:30);k++){const u=u0+rn()*(u1-u0),v=.4+rn()*.04,[x,z]=W(u,v);add(new THREE.ConeGeometry(.0025,.01,4),BARR,x,gy(x,z)+.005,z,rn()*3)}}}

 // ---- conjunto de apartamentos escalonados frente a la playa (bloques en zigzag, terrazas, tejados oscuros),
 //      el edificio blanco grande de la punta, el césped, la piscina y el muro blanco con contrafuertes hacia la arena
 {const bloque=(u,v,fondo,pisos,tejado,dsh)=>{for(let p=0;p<pisos;p++){const re=p*.02,hh=.03,[x,z]=W(u,v+re+dsh),y=gy(...W(u,v))+.004+p*hh;const w=.07,d=fondo-re;
    add(cub(w,hh*.18,d),BLA,x+IN[0]*d/2,y+hh*.91,z+IN[1]*d/2,ANG);                          // canto del forjado
    add(cub(w*.96,hh*.74,d*.92),VID,x+IN[0]*(d/2+.008),y+hh*.45,z+IN[1]*(d/2+.008),ANG);       // cristaleras al fondo de la terraza
    for(const s_ of[-1,1])add(cub(.004,hh*.82,d),BLA,x+TX*s_*w/2,y+hh*.41,z+TY*s_*w/2,ANG);   // muros laterales entre viviendas
    add(cub(w,hh*.3,.003),BLA,x-IN[0]*.004,y+hh*.15,z-IN[1]*.004,ANG);                        // antepecho blanco
    add(cub(w+.004,.0018,d+.012),BLA2,x+IN[0]*(d/2-.006),y+.0009,z+IN[1]*(d/2-.006),ANG);    // losa de terraza volada
    add(cub(w*.9,.004,.005),JAR,x-IN[0]*.004,y+hh*.32,z-IN[1]*.004,ANG);for(let q=0;q<3;q++){const gq=new THREE.IcosahedronGeometry(.0035+rn()*.002,0);gq.scale(1.4,.8,1);add(gq,JAR,x-IN[0]*.006+TX*(q-1)*w*.3,y+hh*.36,z-IN[1]*.006+TY*(q-1)*w*.3,rn()*6)}}  // jardinera con plantas
   const re=(pisos-1)*.02,[x,z]=W(u,v+re+dsh),d=fondo-re,y=gy(...W(u,v))+.004+pisos*.03;add(cub(.074,.003,d+.004),tejado,x+IN[0]*d/2,y+.0015,z+IN[1]*d/2,ANG)};
  // fila de delante: tejados oscuros, 3 pisos; cada módulo se desplaza en diagonal (zigzag)
  for(let i=0;i<22;i++){const u=COMP[0]+.08+i*.07;if(u>COMP[1]-.4)break;const z_=(i%4<2?i%2:1-i%2)*.03;bloque(u,.52+z_,.11,i%5===2?2:3,TEJ,0)}
  // fila de atrás: más alta y de tejado claro
  for(let i=0;i<20;i++){const u=COMP[0]+.2+i*.07;if(u>COMP[1]-.35)break;const z_=(i%3)*.025;bloque(u,.7+z_,.13,4,BLA2,0)}
  // edificio blanco grande de la punta (junto al Lagares), con bandas de ventanas
  {const u=COMP[1]-.18,v=.52,[x,z]=W(u,v),y=gy(x,z);const w=.32,d=.16,H=.16;add(cub(w,H,d),BLA,x+IN[0]*d/2,y+H/2,z+IN[1]*d/2,ANG);
   for(let p=0;p<5;p++){add(cub(w+.003,.011,d+.003),VID,x+IN[0]*d/2,y+.018+p*.03,z+IN[1]*d/2,ANG);add(cub(w+.012,.002,.012),BLA2,x-IN[0]*.004,y+.011+p*.03,z-IN[1]*.004,ANG);for(let q=0;q<12;q++){const o_=(q/11-.5)*w*.96;add(cub(.002,.011,.002),BLA,x+TX*o_-IN[0]*.0015,y+.018+p*.03,z+TY*o_-IN[1]*.0015)}}add(cub(w+.006,.003,d+.006),BLA2,x+IN[0]*d/2,y+H+.0015,z+IN[1]*d/2,ANG);
   for(let k=0;k<4;k++){const[cx,cz]=W(u-.12+k*.08,v+.05);add(cub(.03,.012,.03),BLA2,cx,y+H+.006,cz,ANG)}}
  // césped del conjunto entre el muro y los bloques
  {const pos=[];const q=(u,v)=>{const[x,z]=W(u,v);return[x,gy(x,z)+.0045,z]};for(let u=COMP[0];u<COMP[1]-.35;u+=.05){pos.push(...q(u,.42),...q(u,.53),...q(u+.05,.42),...q(u+.05,.42),...q(u,.53),...q(u+.05,.53))}
   const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.computeVertexNormals();add(g,CES,0,0,0)}
  // piscina en forma de cruz escalonada (extremo oeste del conjunto)
  {const u=COMP[0]+.12,v=.47,[x,z]=W(u,v),y=gy(x,z);const P1=[[0,0,.09,.035],[.03,.025,.04,.035],[-.035,-.02,.04,.03]];
   for(const[du,dv,a,b]of P1){const[px,pz]=W(u+du,v+dv);add(cub(a+.012,.009,b+.012),BLA,px,y+.0045,pz,ANG);const m=new THREE.Mesh(new THREE.BoxGeometry(a,.002,b),PIS);m.position.set(px,y+.0095,pz);m.rotation.y=ANG;G.add(m)}}
  // muro blanco hacia la arena con contrafuertes en cuña
  {const pts=[];for(let u=COMP[0]-.02;u<=COMP[1]-.3;u+=.05)pts.push(W(u,.41));muro(pts,.018,.008,BLA,BLA2,-.002);
   for(let u=COMP[0];u<=COMP[1]-.32;u+=.09){const[x,z]=W(u,.395),y=gy(x,z);const g=new THREE.BoxGeometry(.012,.016,.018);const p=g.attributes.position;for(let k=0;k<p.count;k++)if(p.getY(k)>0&&p.getZ(k)<0)p.setZ(k,p.getZ(k)*.1);g.computeVertexNormals();add(g,BLA2,x,y+.008,z,ANG)}}
  // muro de piedra del lado del río, bajo el edificio de la punta
  {const pts=[];for(let u=COMP[1]-.35;u<=COMP[1]+.1;u+=.05)pts.push(W(u,.48));muro(pts,.02,.01,GRAO,GRA,-.006)}
  CALZ.comp=1}


 // ---- (2ª pasada, fotos aéreas) grandes lajas de granito en el agua: plataformas planas y estratificadas, gris pardo,
 //      con la base oscura de algas; una frente al centro de la playa, otra más afuera al oeste y otra pequeña junto a la plaza
 {const RG=[M(0x7a5a42,{roughness:1}),M(0x6a4c37,{roughness:1}),M(0x86664a,{roughness:1})],RGB=M(0x3a2b20,{roughness:1}),GRI=M(0x4a3628,{roughness:1});
  // cada laja es un montón de bloques facetados y aplastados que se solapan: superficie irregular, más alta en el centro,
  // bordes rotos que se meten en el agua y la franja de abajo oscura de algas
  const RF=[0x7a5a42,0x6a4c37,0x86664a,0x735440,0x5f4632].map(c=>M(c,{roughness:1,flatShading:true})),RAL=M(0x3a3424,{roughness:1,flatShading:true});
  const bloqueR=(r)=>{const g=new THREE.IcosahedronGeometry(r,LT?0:1);const p=g.attributes.position,mp=new Map();for(let k=0;k<p.count;k++){const key=p.getX(k).toFixed(4)+p.getY(k).toFixed(4)+p.getZ(k).toFixed(4);let f=mp.get(key);if(f==null){f=.78+rn()*.4;mp.set(key,f)}p.setXYZ(k,p.getX(k)*f,p.getY(k)*f,p.getZ(k)*f)}g.computeVertexNormals();return g};
  const laja=(u,v,R,el,ang,top)=>{const[cx,cz]=W(u,v),a0=rn()*6,ca=Math.cos(ang),sa=Math.sin(ang),n=Math.round(R*R*(LT?900:1700))+6;
   for(let k=0;k<n;k++){const a=rn()*6.283,borde=.7+.3*Math.sin(a*3+a0)+.12*Math.sin(a*7+a0*2),d=Math.sqrt(rn())*borde,lx=Math.cos(a)*d*R*el,lz=Math.sin(a)*d*R,x=cx+lx*ca-lz*sa,z=cz+lx*sa+lz*ca;
    const rr=(.012+rn()*.02)*(1.2-d*.5)*Math.min(1.6,R/.12+.4),g=bloqueR(rr);g.scale(1+rn()*.5,.3+rn()*.25,1+rn()*.4);
    const y=top-d*d*.022-rn()*.005-rr*.25;add(g,d>.85&&rn()<.7?RAL:RF[(rn()*RF.length)|0],x,y,z,rn()*6)}
   // piedras sueltas alrededor, medio hundidas
   for(let k=0;k<Math.round(R*40);k++){const a=rn()*6.283,d=1.05+rn()*.5,lx=Math.cos(a)*d*R*el,lz=Math.sin(a)*d*R,x=cx+lx*ca-lz*sa,z=cz+lx*sa+lz*ca;if(t(x,z)!==0)continue;const g=bloqueR(.005+rn()*.01);g.scale(1.2,.45,1);add(g,rn()<.5?RAL:RF[1],x,-.014+rn()*.008,z,rn()*6)}};
  const fuera=(u,v)=>{const[x,z]=W(u,v);return t(x,z)===0};const LJ=[];
  for(const[u,v,R,el,an,top,cp]of[[1.4,-.78,.28,1.7,.5,.007,5],[.3,-1.2,.32,1.6,.3,.009,5],[-.45,-.8,.2,1.5,.9,.005,4],[2.15,-1.05,.14,1.4,.2,-.002,3],[.85,-.5,.1,1.5,.6,.003,3],[2.6,-.7,.06,1.3,1.1,-.006,2]])if(fuera(u,v)){laja(u,v,R,el,an,top);LJ.push([...W(u,v),R*el])}
  // barcas fondeadas entre las rocas (chalanas y dornas con su boya), y alguna varada en las rocas de la orilla
  {const casco=(len,anch,alt)=>{const g=new THREE.BoxGeometry(len,alt,anch,6,1,2);const p=g.attributes.position;for(let k=0;k<p.count;k++){const f=Math.abs(p.getX(k))/(len/2),y=p.getY(k);p.setZ(k,p.getZ(k)*(1-Math.pow(f,2.2)*.85)*(y<0?.75:1));p.setY(k,y+(f>.6?(f-.6)*alt*.9:0))}g.computeVertexNormals();return g};
   const BOYA=M(0xe8572e,{roughness:.6});let puestas=0;
   for(let k=0;k<120&&puestas<(LT?10:18);k++){const u=-1.1+rn()*3.3,v=-.18-rn()*1.15;if(!fuera(u,v))continue;const[x,z]=W(u,v);if(LJ.some(([lx,lz,R])=>Math.hypot(x-lx,z-lz)<R+.03))continue;
    const len=.045+rn()*.02,ry=rn()*6.28,cm=BCOL[(rn()*BCOL.length)|0],Y=-.004;add(casco(len,.015+len*.12,.009),cm,x,Y,z,ry);add(cub(len*.8,.0012,.003),MADO,x,Y+.005,z,ry);add(cub(.003,.0013,.014),MADO,x,Y+.0055,z,ry);
    if(rn()<.5)add(cub(.006,.005,.006),BLA2,x-Math.cos(ry)*len*.42,Y+.006,z+Math.sin(ry)*len*.42,ry);  // motor fueraborda
    add(new THREE.SphereGeometry(.0035,6,4),BOYA,x+Math.cos(ry)*len*.9,Y-.001,z-Math.sin(ry)*len*.9);puestas++}
   for(let k=0;k<6;k++){const u=-.9+rn()*1.1,[x,z]=W(u,-.05-rn()*.05),ry=ANG+(rn()-.5)*.8,len=.035+rn()*.015;add(casco(len,.014,.008),BCOL[(rn()*BCOL.length)|0],x,Math.max(gy(x,z),-.012)+.006,z,ry,0,(rn()-.5)*.25)}
   CALZ.barcas=puestas}
  // hilera de rocas que sale de la playa hacia el agua (se ve en bajamar)
  for(let k=0;k<26;k++){const f=k/25,u=1.05+f*.06+(rn()-.5)*.02,v=.06-f*.5,[x,z]=W(u,v),r=.004+rn()*.006,g=new THREE.DodecahedronGeometry(r,0);g.scale(1.3,.5,1);add(g,rn()<.5?RMA:ALG,x,Math.max(gy(x,z),-.012)+r*.15,z,rn()*6)}
  // manchas oscuras de algas y roca bajo el agua clara
  const MANCHA=new THREE.MeshStandardMaterial({color:0x1d3a35,roughness:1,transparent:true,opacity:.6,depthWrite:false,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-1});
  for(let k=0;k<(LT?14:26);k++){const u=-.8+rn()*2.8,v=-.2-rn()*1.1;if(!fuera(u,v))continue;const[x,z]=W(u,v),g=new THREE.CircleGeometry(.02+rn()*.05,9);const p=g.attributes.position;for(let i=1;i<p.count;i++){const q=.6+rn()*.6;p.setXY(i,p.getX(i)*q*1.5,p.getY(i)*q)}g.rotateX(-Math.PI/2);g.rotateY(rn()*6);g.translate(x,-.018,z);const m=new THREE.Mesh(g,MANCHA);m.renderOrder=1;G.add(m)}}
 // ---- arena por encima de la franja verde pegada al agua (el suelo no se toca: se tapa)
 {const AR_=M(0xeadcbc,{roughness:1,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3});const pos=[];const D=.03;
  const h=(u,v)=>{const[x,z]=W(u,v);let y=null;try{y=sueloRap(x,z)}catch(e){}return y==null||y<-.005?null:[x,y+.0025,z]};
  for(let u=U0;u<FIN-.3;u+=D)for(let v=-.75;v<.42;v+=D){if(u>PARQ[0]-.05&&u<PARQ[1]+.05&&v>.05)continue;if(u>DORN[0]-.05&&u<DORN[1]+.05&&v>.3)continue;const a=h(u,v),b=h(u+D,v),c=h(u+D,v+D),d=h(u,v+D);if(!a||!b||!c||!d)continue;
   const mx=(a[0]+c[0])/2,mz=(a[2]+c[2])/2;if(rioD(mx,mz)[0]<rioD(mx,mz)[1]*1.4)continue;if(Math.max(a[1],b[1],c[1],d[1])<.009)continue; // solo donde el suelo está alto (la franja), no la arena baja
   pos.push(...a,...c,...b,...a,...d,...c)}
  if(pos.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.computeVertexNormals();const m=new THREE.Mesh(g,AR_);m.receiveShadow=true;G.add(m)}}
 // ---- arena mojada de bajamar delante de la playa (más oscura y brillante)
 {const pos=[],idx=[];let n=0;for(let u=PARQ[0];u<=FIN-.25;u+=.05){for(const v of[-.32+.06*Math.sin(u*4),.05]){const[x,z]=W(u,v);pos.push(x,Math.max(gy(x,z),-.004)+.0025,z)}if(n){const k=(n-1)*2;idx.push(k,k+2,k+1,k+1,k+2,k+3)}n++}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();
  const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:0x9a8c72,roughness:.35,transparent:true,opacity:.45,depthWrite:false,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}));m.renderOrder=1;G.add(m)}
 // ---- coches aparcados en batería sobre el malecón, entre el muro y la carretera
 {const COLC=[0xf4f4f2,0x2b2f3a,0x9aa3b0,0xb8423a,0x3a4a6a,0x5d7fb0,0xd8d4ca,0x7a1f1f],CM=COLC.map(c=>M(c,{roughness:.4,metalness:.25}));
  for(let u=U0+.1;u<PARQ[0]-.05;u+=.03){if(rdv(u)<.09||rn()<.2)continue;const[x,z]=W(u,.06),y=gy(x,z),cm=CM[(rn()*CM.length)|0],ry=ANG+Math.PI/2;
   add(cub(.042,.012,.018),cm,x,y+.009,z,ry);add(cub(.022,.009,.016),VID,x,y+.019,z,ry);add(cub(.021,.002,.017),cm,x,y+.024,z,ry)}}
 for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=!LT&&![CES,OCR,TIE,ARM,MOJ].includes(mat);m.receiveShadow=true;G.add(m)}
 scene.add(G);CALZ.G=G}
// ---------- fin de calzoa.js
