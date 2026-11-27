// ---------- Plaza de las rampas en Nicaragua (rampas3.js)
// Como en la Gran Vía de verdad: las cintas acaban en la Rúa Nicaragua (t≈1,55 desde arriba) y de ahí hasta Praza de España
// el bulevar es una plaza. De arriba abajo: bancos y sillas sueltas, la rampa fija de paneles triangulares que convierten las
// pisadas en energía (con su placa), y al final de las cintas el suelo LED que imita el mar: agua, olas y peces; cada paso
// hace una salpicadura y los peces se apartan del que pasa. Encima, el «Pezseto»: la silueta de un pez enorme hecha de
// costillas de acero con plantas dentro, sobre cuatro postes, por debajo del cual se pasa andando.
// rampaPlaza(G,ctx) la llama rampaGV (edit_rampas3.py) con sus ayudas: ctx={L,EN,at,gy,angT}.
const RPZ={led:null,pasos:[],peces:[],T0:1.55};window.__RPZ=RPZ;
function rampaPlaza(G,{EN,at,gy,angT}){const T0=RPZ.T0;
 const strip=(t0,t1,w,y0,mat,ro)=>{const n=Math.max(2,Math.ceil((t1-t0)/.03)),pos=[],uv=[],idx=[];for(let i=0;i<=n;i++){const t=t0+(t1-t0)*i/n,y=gy(t)+y0;for(const s of[-1,1]){const p=at(t,s*w/2);pos.push(p[0],y,p[1]);uv.push(s>0?1:0,i/n)}}
  for(let i=0;i<n;i++){const a=i*2;idx.push(a,a+1,a+2,a+1,a+3,a+2)}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();
  const m=new THREE.Mesh(g,mat);m.receiveShadow=true;if(ro)m.renderOrder=ro;G.add(m);return m};
 const ACE=new THREE.MeshStandardMaterial({color:0x8d939a,roughness:.4,metalness:.7}),MAD=new THREE.MeshStandardMaterial({color:0x9a6a3e,roughness:.75});
 // 1) suelo LED que imita el mar, al final de las cintas (t de 0,95 a 1,5)
 const LA=.95,LB=1.5,LW=.066;{const cv=document.createElement('canvas');cv.width=96;cv.height=384;const cx=cv.getContext('2d'),tx=new THREE.CanvasTexture(cv);tx.colorSpace=THREE.SRGBColorSpace;
  const M=new THREE.MeshStandardMaterial({map:tx,emissiveMap:tx,emissive:0xffffff,emissiveIntensity:.55,roughness:.25,metalness:.1,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3});
  const m=strip(LA,LB,LW,.0035,M,1);RPZ.led={cv,cx,tx,M,m};
  // marco de acero del panel
  for(const s of[-1,1]){const g=new THREE.BoxGeometry(.003,.002,1);const n=8;for(let k=0;k<n;k++){const t=LA+(LB-LA)*(k+.5)/n,p=at(t,s*(LW/2+.0015)),b=new THREE.Mesh(new THREE.BoxGeometry(.003,.002,(LB-LA)/n*1.02),ACE);b.position.set(p[0],gy(t)+.0045,p[1]);b.rotation.y=angT(t)+Math.PI/2;G.add(b)}}
  let rs=3;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;for(let i=0;i<9;i++)RPZ.peces.push({u:rn(),v:rn(),a:rn()*6.28,s:.6+rn()*.6,c:['#ffb347','#ffe066','#ff7f50','#9fe2ff','#f5f5f5'][i%5],hu:0});
  m.onBeforeRender=()=>rpzLed(EN,at,LA,LB,LW)}
 // 2) rampa fija de paneles triangulares que generan energía con las pisadas (t de 0,4 a 0,9) y su placa
 const EA=.4,EB=.9;{const cv=document.createElement('canvas');cv.width=64;cv.height=256;const x=cv.getContext('2d');x.fillStyle='#55595f';x.fillRect(0,0,64,256);
  for(let j=0;j<16;j++)for(let i=0;i<4;i++){const x0=i*16,y0=j*16,up=(i+j)%2===0;x.fillStyle=['#6b7078','#7a8089','#646971'][(i*3+j)%3];x.beginPath();if(up){x.moveTo(x0+1,y0+15);x.lineTo(x0+8,y0+1);x.lineTo(x0+15,y0+15)}else{x.moveTo(x0+1,y0+1);x.lineTo(x0+15,y0+1);x.lineTo(x0+8,y0+15)}x.closePath();x.fill()}
  x.strokeStyle='#2f3236';x.lineWidth=1;for(let j=0;j<=256;j+=16){x.beginPath();x.moveTo(0,j);x.lineTo(64,j);x.stroke()}
  const tx=new THREE.CanvasTexture(cv);tx.colorSpace=THREE.SRGBColorSpace;tx.wrapT=THREE.RepeatWrapping;tx.repeat.set(1,3);
  const M=new THREE.MeshStandardMaterial({map:tx,roughness:.55,metalness:.35,emissive:0x2bd96b,emissiveIntensity:0,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3});RPZ.ener=M;
  strip(EA,EB,.06,.0035,M,1);
  const p=at(EB+.02,.03),post=new THREE.Mesh(new THREE.CylinderGeometry(.0012,.0012,.012,6),ACE);post.position.set(p[0],gy(EB)+.009,p[1]);G.add(post);
  const pl=new THREE.Mesh(new THREE.BoxGeometry(.012,.008,.001),new THREE.MeshStandardMaterial({color:0x2b4f3a,roughness:.4,metalness:.3,emissive:0x2bd96b,emissiveIntensity:.25}));pl.position.set(p[0],gy(EB)+.017,p[1]);pl.rotation.y=angT(EB);pl.rotation.x=-.4;G.add(pl)}
 // 3) bancos y sillas sueltas a mitad de la plaza (t de 0,15 a 0,35)
 {const S=[[.18,.03,0],[.24,-.03,1],[.3,.032,0],[.2,-.028,2],[.27,.02,2],[.33,-.02,2]];
  for(const[t,o,k] of S){const p=at(t,o),y=gy(t),a=angT(t);
   if(k<2){const b=new THREE.Mesh(new THREE.BoxGeometry(.026,.0025,.008),MAD);b.position.set(p[0],y+.0075,p[1]);b.rotation.y=a;b.castShadow=!window.LITE;G.add(b);
    const r=new THREE.Mesh(new THREE.BoxGeometry(.026,.006,.0015),MAD);const q=at(t,o+Math.sign(o)*.0045);r.position.set(q[0],y+.011,q[1]);r.rotation.y=a;G.add(r);
    for(const e of[-.011,.011]){const c=at(t+e,o),l=new THREE.Mesh(new THREE.BoxGeometry(.002,.006,.007),ACE);l.position.set(c[0],y+.0035,c[1]);l.rotation.y=a;G.add(l)}}
   else{// silla individual de colores, girada un poco
    const col=[0xe23b3b,0xf4c21a,0x1d9fc4][Math.floor(t*100)%3],cm=new THREE.MeshStandardMaterial({color:col,roughness:.5}),gS=new THREE.Group();
    const s=new THREE.Mesh(new THREE.BoxGeometry(.006,.0012,.006),cm);s.position.y=.0062;gS.add(s);const r=new THREE.Mesh(new THREE.BoxGeometry(.0012,.006,.006),cm);r.position.set(-.003,.0095,0);gS.add(r);
    for(const[dx,dz] of[[-.0025,-.0025],[-.0025,.0025],[.0025,-.0025],[.0025,.0025]]){const l=new THREE.Mesh(new THREE.CylinderGeometry(.0004,.0004,.006,4),ACE);l.position.set(dx,.003,dz);gS.add(l)}
    gS.position.set(p[0],y+.0005,p[1]);gS.rotation.y=a+(o>0?-1.2:1.9)+t*7;G.add(gS)}}}
 // 4) el Pezseto: costillas de acero con forma de pez, plantas dentro, sobre cuatro postes; se pasa por debajo (t de 0,95 a 1,45)
 {const PA=.97,PB=1.45,len=PB-PA,base=.034,H0=.024,P=new THREE.Group();P.name='pezseto';
  const perf=u=>{// radio del cuerpo a lo largo del pez (u=0 cabeza, u=1 arranque de la cola)
   return .034*Math.pow(Math.sin(Math.PI*Math.min(1,Math.max(0,u*.92+.04))),.75)};
  const RIB=[],NR=11;for(let i=0;i<NR;i++){const u=i/(NR-1),t=PA+u*len*.82,r=Math.max(.006,perf(u)),p=at(t,0),y=gy(t)+base+H0+.034;
   const g=new THREE.TorusGeometry(r,.0011,5,22);g.rotateY(Math.PI/2);const m=new THREE.Mesh(g,ACE);m.position.set(p[0],y,p[1]);m.rotation.y=angT(t);m.scale.set(1,.85,1);P.add(m);RIB.push([t,r,y])}
  // espina y vientre: dos largueros a lo largo
  for(const s of[1,-1]){const pts=RIB.map(([t,r,y])=>{const p=at(t,0);return new THREE.Vector3(p[0],y+s*r*.85,p[1])});const c=new THREE.CatmullRomCurve3(pts);P.add(new THREE.Mesh(new THREE.TubeGeometry(c,30,.0012,5),ACE))}
  for(const s of[1,-1]){const pts=RIB.map(([t,r,y])=>{const p=at(t,s*r);return new THREE.Vector3(p[0],y,p[1])});P.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts),30,.0011,5),ACE))}
  // cola en abanico al final (hacia la plaza) y aleta dorsal
  {const[tc,,yc]=RIB[RIB.length-1],tE=PA+len*.95,pC=at(tc,0),pE=at(tE,0);for(const s of[1,-1]){const a=new THREE.Vector3(pC[0],yc,pC[1]),b=new THREE.Vector3(pE[0],yc+s*.022,pE[1]);
    const g=new THREE.TubeGeometry(new THREE.LineCurve3(a,b),4,.0011,5);P.add(new THREE.Mesh(g,ACE))}const g=new THREE.TubeGeometry(new THREE.LineCurve3(new THREE.Vector3(pE[0],yc+.022,pE[1]),new THREE.Vector3(pE[0],yc-.022,pE[1])),4,.0011,5);P.add(new THREE.Mesh(g,ACE))}
  // ojo
  {const[t,r,y]=RIB[1];for(const s of[1,-1]){const p=at(t+.01,s*r*.8),o=new THREE.Mesh(new THREE.SphereGeometry(.0035,8,6),new THREE.MeshStandardMaterial({color:0x1b1d20,roughness:.3,metalness:.5}));o.position.set(p[0],y+.004,p[1]);P.add(o)}}
  // plantas dentro: matas verdes y flores sobre la mitad de arriba de cada costilla, y lianas colgando
  {let rs=21;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647,L_=[],geo=new THREE.IcosahedronGeometry(.0055,0),mm=new THREE.Matrix4(),q=new THREE.Quaternion(),V=new THREE.Vector3(),S=new THREE.Vector3(),col=new THREE.Color();
   for(let i=1;i<RIB.length-1;i++){const[t,r,y]=RIB[i];for(let k=0;k<9;k++){const a=(rn()-.5)*Math.PI*1.25,p=at(t+(rn()-.5)*.02,Math.sin(a)*r*.9);L_.push([p[0],y+Math.cos(a)*r*.75,p[1],.7+rn()*.7,rn()])}}
   const im=new THREE.InstancedMesh(geo,new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9,flatShading:true}),L_.length);
   L_.forEach(([x,y,z,k,c],i)=>{mm.compose(V.set(x,y,z),q,S.set(k,k*.8,k));im.setMatrixAt(i,mm);im.setColorAt(i,col.setHex(c<.12?0xd94f6b:c<.2?0xf2c14e:[0x3f7d34,0x4f8f3a,0x2f6b35,0x6a9a3a][i%4]))});im.castShadow=!window.LITE;im.computeBoundingSphere();P.add(im)}
  // cuatro postes
  for(const[u,s] of[[.2,1],[.2,-1],[.7,1],[.7,-1]]){const t=PA+u*len*.82,p=at(t,s*.036),y=gy(t),h=base+H0+.034-.02;const m=new THREE.Mesh(new THREE.CylinderGeometry(.0013,.0016,h,6),ACE);m.position.set(p[0],y+h/2,p[1]);P.add(m)}
  P.traverse(o=>{if(o.isMesh&&!o.isInstancedMesh){o.castShadow=!window.LITE;o.receiveShadow=true}});G.add(P)}}
// animación del suelo LED: agua con olas, peces que nadan y huyen de quien pisa, y salpicaduras en cada paso
function rpzLed(EN,at,LA,LB,LW){const R=RPZ.led;if(!R)return;const now=performance.now()/1000;if(R.t&&now-R.t<1/24)return;const dt=Math.min(.1,now-(R.t||now));R.t=now;
 const{cx,cv}=R,W=cv.width,H=cv.height;
 // posición del protagonista en coordenadas del panel (u a lo ancho, v a lo largo)
 let pu=-9,pv=-9;try{if(window.P&&window.modo&&window.modo()==='pie'){let best=1e9;for(let k=0;k<=24;k++){const t=LA+(LB-LA)*k/24,e=EN(t),d=Math.hypot(P.x-e[0],P.y-e[1]);if(d<best){best=d;pv=k/24;const sd=(P.x-e[0])*(-e[3])+(P.y-e[1])*e[2];pu=.5+sd/LW}}if(best>.06){pu=-9;pv=-9}}}catch(e){}
 if(pu>-1&&(!R.ult||Math.hypot(pu-R.ult[0],(pv-R.ult[1])*8)>.18)){RPZ.pasos.push({u:pu,v:pv,t0:now});R.ult=[pu,pv];if(RPZ.ener)RPZ.ener.emissiveIntensity=.4}
 if(RPZ.ener&&RPZ.ener.emissiveIntensity>0)RPZ.ener.emissiveIntensity=Math.max(0,RPZ.ener.emissiveIntensity-dt*.8);
 let n=0;try{n=CIELO.nf||0}catch(e){}R.M.emissiveIntensity=.45+.9*THREE.MathUtils.smoothstep(n,.15,.6);
 // agua: degradado y franjas de luz que se mueven
 const g=cx.createLinearGradient(0,0,W,0);g.addColorStop(0,'#0b4f7a');g.addColorStop(.5,'#137fb1');g.addColorStop(1,'#0b4f7a');cx.fillStyle=g;cx.fillRect(0,0,W,H);
 cx.strokeStyle='rgba(170,235,255,.35)';cx.lineWidth=2;for(let k=0;k<14;k++){cx.beginPath();const y0=((k*29+now*22)%(H+40))-20;for(let x=0;x<=W;x+=8){const y=y0+Math.sin(x*.12+now*2+k)*4;x?cx.lineTo(x,y):cx.moveTo(x,y)}cx.stroke()}
 // peces: nadan a lo largo y se escapan si el protagonista está cerca
 for(const f of RPZ.peces){let vx=Math.cos(f.a)*.05*f.s,vy=Math.sin(f.a)*.012*f.s;const dx=f.u-pu,dy=(f.v-pv)*6,d=Math.hypot(dx,dy);
  if(d<.45){const k=(.45-d)/.45*2.5;vx+=dx/(d+1e-3)*k*.4;vy+=dy/(d+1e-3)*k*.06;f.a=Math.atan2(vy,vx)}else f.a+=(Math.sin(now*.7+f.s*9)*.6)*dt;
  f.u+=vx*dt*3;f.v+=vy*dt*3;if(f.u<.08){f.u=.08;f.a=Math.PI-f.a}if(f.u>.92){f.u=.92;f.a=Math.PI-f.a}if(f.v<0)f.v+=1;if(f.v>1)f.v-=1;
  const x=f.u*W,y=f.v*H,ang=Math.atan2(vy*H,vx*W);cx.save();cx.translate(x,y);cx.rotate(ang);cx.fillStyle=f.c;cx.beginPath();cx.ellipse(0,0,9*f.s,4*f.s,0,0,6.283);cx.fill();
  cx.beginPath();cx.moveTo(-8*f.s,0);cx.lineTo(-15*f.s,-5*f.s);cx.lineTo(-15*f.s,5*f.s);cx.closePath();cx.fill();cx.fillStyle='#111';cx.fillRect(4*f.s,-1.5*f.s,2,2);cx.restore()}
 // salpicaduras: anillos que se abren desde cada pisada
 RPZ.pasos=RPZ.pasos.filter(p=>now-p.t0<1.4);for(const p of RPZ.pasos){const a=(now-p.t0)/1.4;cx.strokeStyle=`rgba(255,255,255,${(1-a)*.9})`;cx.lineWidth=2.5;
  for(const k of[1,.6]){cx.beginPath();cx.ellipse(p.u*W,p.v*H,6+a*34*k,(6+a*34*k)*.9,0,0,6.283);cx.stroke()}}
 R.tx.needsUpdate=true}
// ---------- fin de rampas3.js
