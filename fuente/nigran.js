// ---------- Nigrán: Patos, Prado y Monteferro (nigran.js) ----------
// Zona 1 de Nigrán pulida con Google Earth, Street View y fotos como referencia (toda la geometría es propia).
// Datos en nigran_detalle.json (fuente/herramientas/nigran_hornear.py); el pinar de Monteferro va en baiona_inst.json.
// · Monteferro: suelo de monte (pinocha, musgo, helecho y tojo) en vez de césped, costa de granito con bolos,
//   Monumento a la Marina Universal en la cima (torre de granito escalonada de unos 25 m con la Virgen del Carmen,
//   1924), batería costera J-3 (cañones oxidados con escudo en sus fosos de hormigón y búnkeres con grafitis),
//   Mirador de las Estelas con bancos y la rosa de los vientos.
// · Playa de Patos: muro bajo del paseo con albardilla de granito, farolas negras clásicas, pasarelas de madera a la
//   arena y dos torres de socorrista con bandera.
// · Prado: la escultura blanca con forma de ola junto al acceso a la playa.
const NIG={root:null,datos:null,carga:null};window.__NIG=NIG;
function nigChk(){if(!MAPA||!MI)return;const z=ZROOTS.find(q=>q.root&&q.root.name==='baiona'&&q.root.parent);if(!z||NIG.root===z.root)return;
 const r=z.root;NIG.root=r;
 (NIG.carga||(NIG.carga=fetch('nigran_detalle.json').then(x=>{if(!x.ok)throw new Error('HTTP '+x.status);return x.json()}))).then(d=>{NIG.datos=d;if(NIG.root!==r||!r.parent)return;
  setTimeout(()=>{if(!r.parent)return;try{nigCrea(r,d)}catch(e){console.warn('nigran',e);NIG.err=String(e)+' '+String(e.stack).slice(0,600)}},1100)}).catch(e=>{NIG.carga=null;NIG.root=null;console.warn('nigran json',e)})}
function nigCrea(root,D){const LT=!!window.LITE,t0=performance.now(),G=new THREE.Group();G.name='nigran_detalle';
 let rs=29;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.9},o));
 const C3=h=>{const c=new THREE.Color(h);return[c.r,c.g,c.b]};
 const MT=1/78;                                     // 1 unidad del mapa ≈ 78 m
 // ---------- piezas sueltas: se juntan por material al final ----------
 const PARTS=new Map(),SOLID=new Map();
 const prep=g=>{g=g.index?g.toNonIndexed():g;if(g.attributes.uv)g.deleteAttribute('uv');if(g.attributes.uv1)g.deleteAttribute('uv1');if(!g.attributes.normal)g.computeVertexNormals();return g};
 // pone la geometría g (local) girada a (ang: dirección cos,sin en x,z) en (x,y,z); solido → choca
 const pon=(g,mat,x,y,z,ang=0,solido=false)=>{g=prep(g);if(ang)g.rotateY(-ang);g.translate(x,y,z);const P_=solido?SOLID:PARTS;if(!P_.has(mat))P_.set(mat,[]);P_.get(mat).push(g)};
 const caja=(w,h,l,mat,x,y,z,ang=0,solido=false)=>pon(new THREE.BoxGeometry(w,h,l),mat,x,y+h/2,z,ang,solido);
 // ---------- 1) suelo de Monteferro: se repintan los triángulos de la tierra y el verde de la zona (mismo plano) ----------
 // con pinocha, musgo, helecho y claros de tojo en el monte, granito en la costa (más oscuro y mojado junto al agua)
 // y la explanada del monumento; cada triángulo se subdivide para que el color tenga detalle
 {const S=D.suelo,W=S.w,H=S.h;const kv=(x,z)=>{const i=Math.round((x-S.x0)/S.s),j=Math.round((z-S.z0)/S.s);if(i<0||j<0||i>=W||j>=H)return 0;return S.k.charCodeAt(j*W+i)-48};
  const X0=S.x0,X1=S.x0+W*S.s,Z0=S.z0,Z1=S.z0+H*S.s;
  const ns=(x,z)=>.5+.25*Math.sin(x*23.1+Math.sin(z*17.3)*1.7)+.25*Math.sin(z*19.7+Math.cos(x*13.9)*2.3);
  const MON=[C3('#4a4a2c'),C3('#5b4b33'),C3('#3e4a2a'),C3('#545230'),C3('#6e6b38'),C3('#6a5a3c')],ROC=[C3('#8f897d'),C3('#a19b8e'),C3('#7b766c'),C3('#9a9474'),C3('#6a665e')],EXP=[C3('#b5a57c'),C3('#a99a72'),C3('#c0b089')];
  const color=(x,y,z,k)=>{const n=ns(x,z),n2=ns(x*2.7+5,z*2.7-3);let c;
   if(k===1){c=MON[(n*2.2+n2*3.7|0)%6];if(n2>.78)c=MON[4]}
   else if(k===2){c=ROC[(n*3.1+n2*2.3|0)%5];if(y<.03)c=c.map(v=>v*.72)}
   else c=EXP[(n*5|0)%3];
   const f=.92+n2*.16;return[c[0]*f,c[1]*f,c[2]*f]};
  const pos=[],col=[],a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3(),LADO=LT?.3:.15,ALZA=.002;   // un palmo por encima: sin pelea de profundidad en ningún motor
  root.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||!/^(verde|tierra)/.test(o.name)||/paseo/.test(o.name))return;o.updateMatrixWorld(true);
   const g=o.geometry,p=g.attributes.position,ix=g.index,n=ix?ix.count:p.count,mw=o.matrixWorld;
   for(let t=0;t<n;t+=3){const i0=ix?ix.getX(t):t,i1=ix?ix.getX(t+1):t+1,i2=ix?ix.getX(t+2):t+2;
    a.fromBufferAttribute(p,i0).applyMatrix4(mw);if(a.x<X0-.3||a.x>X1+.3||a.z<Z0-.3||a.z>Z1+.3)continue;
    b.fromBufferAttribute(p,i1).applyMatrix4(mw);c.fromBufferAttribute(p,i2).applyMatrix4(mw);
    const cx=(a.x+b.x+c.x)/3,cz=(a.z+b.z+c.z)/3;if(!kv(cx,cz)&&!kv(a.x,a.z)&&!kv(b.x,b.z)&&!kv(c.x,c.z))continue;
    const L=Math.max(a.distanceTo(b),b.distanceTo(c),c.distanceTo(a)),N=Math.max(1,Math.min(10,Math.ceil(L/LADO)));
    const P=(u,v)=>{const w=1-u-v;return[a.x*w+b.x*u+c.x*v,a.y*w+b.y*u+c.y*v,a.z*w+b.z*u+c.z*v]};
    const V=q=>{let k=kv(q[0],q[2]);if(!k)k=kv(cx,cz)||1;pos.push(q[0],q[1]+ALZA,q[2]);col.push(...color(q[0],q[1],q[2],k))};
    for(let i=0;i<N;i++)for(let j=0;j<N-i;j++){const A=P(i/N,j/N),B=P((i+1)/N,j/N),Cc=P(i/N,(j+1)/N);
     // solo los subtriángulos dentro de Monteferro
     const mx=(A[0]+B[0]+Cc[0])/3,mz=(A[2]+B[2]+Cc[2])/3;if(kv(mx,mz)){V(A);V(B);V(Cc)}
     if(j<N-i-1){const E=P((i+1)/N,(j+1)/N);const mx2=(B[0]+E[0]+Cc[0])/3,mz2=(B[2]+E[2]+Cc[2])/3;if(kv(mx2,mz2)){V(B);V(E);V(Cc)}}}}});
  if(pos.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.computeVertexNormals();
   // normales hacia arriba aunque el triángulo original venga al revés
   const nn=g.attributes.normal;for(let i=0;i<nn.count;i++)if(nn.getY(i)<0){nn.setXYZ(i,-nn.getX(i),-nn.getY(i),-nn.getZ(i))}
   const m=new THREE.Mesh(g,M(0xffffff,{vertexColors:true,roughness:1,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3}));m.name='suelo_monteferro';m.receiveShadow=true;m.castShadow=false;G.add(m);NIG.suelo=pos.length/9}}
 // ---------- 2) bolos de granito en la costa ----------
 {const geo=new THREE.IcosahedronGeometry(1,LT?0:1),pos=[],col=[];const L=LT?D.bolos.filter((b,i)=>i%2===0):D.bolos;
  for(const[x,z,y,r,s]of L){const g=geo.clone(),p=g.attributes.position;const a=s*12.3;
   for(let i=0;i<p.count;i++){const px=p.getX(i),py=p.getY(i),pz=p.getZ(i),n=1+.18*Math.sin(px*3.1+a)*Math.cos(pz*2.7-a)+.1*Math.sin(py*5+a*2);p.setXYZ(i,px*n,py*n,pz*n)}
   g.scale(r*(1+s*.5),r*(.55+s*.35),r*(1.1-s*.3));g.rotateY(s*6.28);g.translate(x,y,z);const q=(g.index?g.toNonIndexed():g).attributes.position.array;pos.push(...q);
   const t=.5+s*.14,cc=[t*1.02,t,t*.93];for(let i=0;i<q.length/3;i++){const k=q[i*3+1]>y+r*.35?1.08:.9;col.push(cc[0]*k,cc[1]*k,cc[2]*k)}}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.computeVertexNormals();
  const m=new THREE.Mesh(g,M(0xffffff,{vertexColors:true,roughness:.95}));m.name='bolos_monteferro';m.castShadow=!LT;m.receiveShadow=true;G.add(m)}
 // materiales
 const GRA=M(0x9d978b,{roughness:.95}),GRA2=M(0x837d72,{roughness:.95}),GRAO=M(0x2e2c29,{roughness:1}),STA=M(0xc2bcae,{roughness:.85}),
  HOR=M(0x8f8b82,{roughness:1}),HOR2=M(0x6f6c66,{roughness:1}),OXI=M(0x6e3d24,{roughness:.8,metalness:.35}),OXI2=M(0x54301f,{roughness:.85,metalness:.3}),
  NEG=M(0x22252a,{roughness:.5,metalness:.5}),LUZF=M(0xfff1d0,{emissive:0xffd98a,emissiveIntensity:.5,roughness:.3}),MAD=M(0x8a6a48,{roughness:.9}),MAD2=M(0x6f5238,{roughness:.9}),
  BLA=M(0xeeebe4,{roughness:.8}),ROJ=M(0xc8352b,{roughness:.7}),AMA=M(0xe9c234,{roughness:.7}),MUR=M(0xd8d3c7,{roughness:.9}),VER=M(0x3f5f2c,{roughness:1}),
  GRF=['#e0418f','#2f7fd6','#f2c230','#3aa655','#151515','#ff7a1a','#9b5de5'].map(c=>M(c,{roughness:.8}));
 // ---------- 3) Monumento a la Marina Universal (cima de Monteferro) ----------
 {const[x0,z0,y0,ang]=D.monumento,m=MT,ca=Math.cos(ang),sa=Math.sin(ang);
  // local: +x es el frente (hacia el mar). L(u,v): u adelante, v a la derecha
  const L=(u,v)=>[x0+u*ca-v*sa,z0+u*sa+v*ca];
  const B=(w,h,l,mat,u,v,y,sol=true)=>{const[x,z]=L(u*m,v*m);caja(w*m,h*m,l*m,mat,x,y0+y*m,z,ang,sol)};
  // escalinata y basamento
  B(17,.5,17,GRA2,0,0,-.3);B(15.6,.45,15.6,GRA,0,0,.2);B(14.2,.45,14.2,GRA2,0,0,.65);B(12.8,.45,12.8,GRA,0,0,1.1);
  // cuerpo bajo con arcos: pilastras en cada lado y el hueco oscuro dentro
  const Y1=1.55,HA=6;B(9,HA,9,GRAO,0,0,Y1);
  for(const s of[-1,1]){for(const t of[-1,-.36,.36,1]){const w=Math.abs(t)===1?2.4:1.3;B(w,HA,w,GRA,s*5.1,t*4.6,Y1);B(w,HA,w,GRA,t*4.6,s*5.1,Y1)}}
  B(12,1.8,12,GRA2,0,0,Y1+HA);B(12.8,.5,12.8,GRA,0,0,Y1+HA+1.8);
  // fuste escalonado con contrafuertes en las esquinas
  let y=Y1+HA+2.3;const T=[[8.6,4.6],[7.2,4],[5.8,3.4],[4.4,2.4]];
  for(const[w,h]of T){B(w,h,w,GRA,0,0,y);for(const s of[-1,1])for(const t of[-1,1])B(1.2,h*.8,1.2,GRA2,s*(w/2+.3),t*(w/2+.3),y);
   // ranuras de ventana en los costados
   for(const s of[-1,1])B(.35,h*.5,.9,GRAO,0,s*(w/2+.02),y+h*.25,false);
   B(w+.6,.35,w+.6,GRA2,0,0,y+h);y+=h+.35}
  // remate: corona con tres pináculos y el escudo al frente
  B(3.2,1.6,3.2,GRA,0,0,y);for(const v of[-1.1,0,1.1])B(.7,v?1.3:1.9,.7,GRA2,.6,v,y+1.6);
  {const[x,z]=L(1.65*m,0);const g=new THREE.CylinderGeometry(.75*m,.75*m,.25*m,18);g.rotateZ(Math.PI/2);pon(g,STA,x,y0+(y+.8)*m,z,ang,true)}
  // hornacina y la Virgen del Carmen con el Niño, de piedra clara, sobre su peana al frente
  const yN=Y1+HA+2.3;B(.6,4.2,3,GRAO,4.32,0,yN+.2,false);B(1.8,.6,3.6,GRA2,4.9,0,yN-.2);
  {const[x,z]=L(5.1*m,0),yb=y0+(yN+.4)*m;
   const manto=new THREE.CylinderGeometry(.5*m,1*m,3*m,14);pon(manto,STA,x,yb+1.5*m,z,ang);
   const hom=new THREE.SphereGeometry(.62*m,12,8);hom.scale(1,.7,1.05);pon(hom,STA,x,yb+3.05*m,z,ang);
   const cab=new THREE.SphereGeometry(.38*m,12,10);pon(cab,STA,x+ca*.05*m,yb+3.55*m,z+sa*.05*m,ang);
   const cor=new THREE.CylinderGeometry(.3*m,.24*m,.35*m,10);pon(cor,STA,x,yb+4.05*m,z,ang);
   const[xn,zn]=L(5.35*m,-.55*m);const nin=new THREE.SphereGeometry(.26*m,10,8);pon(nin,STA,xn,yb+2.75*m,zn,ang);
   const cue=new THREE.CylinderGeometry(.18*m,.24*m,.7*m,8);pon(cue,STA,xn,yb+2.25*m,zn,ang)}
  // bancos de granito en la explanada
  for(const v of[-9,9]){B(1,.45,4,GRA2,-2,v,0,false);B(1,.45,4,GRA2,3,v,0,false)}}
 // ---------- 4) batería J-3: fosos de hormigón, cañones oxidados con escudo y búnkeres con grafitis ----------
 for(const[x,z,y,a]of D.bateria.canones){const m=MT,ca=Math.cos(a),sa=Math.sin(a);
  caja(.09,.004,.09,HOR,x,y-.002,z,0);                                           // solera
  for(let k=0;k<14;k++){const b=k/14*6.283;if(Math.abs(Math.atan2(Math.sin(b-a),Math.cos(b-a)))<.4)continue;   // pretil en anillo, abierto hacia el mar
   caja(.02,.012,.006,k%3?HOR:HOR2,x+Math.cos(b)*.044,y,z+Math.sin(b)*.044,b+Math.PI/2,true)}
  pon(new THREE.CylinderGeometry(.011,.014,.01,14),OXI2,x,y+.005,z);
  {const g=new THREE.CylinderGeometry(.021,.021,.024,16,1,true,-.85,1.7);pon(g,OXI,x,y+.022,z,a-Math.PI/2,true)}   // escudo curvo
  caja(.018,.012,.022,OXI2,x-ca*.004,y+.016,z-sa*.004,a);
  {const g=new THREE.CylinderGeometry(.0026,.0036,.085,10);g.rotateZ(-Math.PI/2+.06);g.translate(.042,.0025,0);pon(g,OXI,x,y+.02,z,a)}
  {const g=new THREE.CylinderGeometry(.0042,.0042,.006,10);g.rotateZ(-Math.PI/2+.06);g.translate(.084,.005,0);pon(g,OXI2,x,y+.02,z,a)}}
 for(const[x,z,y,a,w,l]of D.bateria.bunkers){const h=.034;
  caja(w,h,l,HOR,x,y,z,a,true);caja(w+.008,.005,l+.008,HOR2,x,y+h,z,a,true);
  const ca=Math.cos(a),sa=Math.sin(a);
  caja(.0015,.02,.014,GRAO,x+ca*(w/2+.0004),y+.004,z+sa*(w/2+.0004),a);                    // puerta
  for(const s of[-1,1])caja(.0015,.006,.01,GRAO,x+ca*(w/2+.0004)-sa*s*l*.32,y+.02,z+sa*(w/2+.0004)+ca*s*l*.32,a);   // troneras
  // grafitis: manchas de color en las paredes
  for(let k=0;k<(LT?3:7);k++){const lado=rn()<.5?1:-1,u=(rn()-.5)*l*.8,hh=.006+rn()*.012,ww=.01+rn()*.02;const mat=GRF[(rn()*GRF.length)|0];
   if(rn()<.5)caja(.0012,hh,ww,mat,x+ca*lado*(w/2+.0008)-sa*u,y+.002+rn()*(h-hh-.004),z+sa*lado*(w/2+.0008)+ca*u,a);
   else{const u2=(rn()-.5)*w*.8;caja(ww,hh,.0012,mat,x+ca*u2-sa*lado*(l/2+.0008),y+.002+rn()*(h-hh-.004),z+sa*u2+ca*lado*(l/2+.0008),a)}}
  caja(w*.7,.002,l*.5,VER,x-ca*w*.1,y+h+.005,z-sa*w*.1,a)}                                // musgo en la cubierta
 // ---------- 5) Mirador de las Estelas y rosa de los vientos ----------
 {const[x,z,y,a]=D.mirador,ca=Math.cos(a),sa=Math.sin(a);
  for(const s of[-1,1]){const bx=x-ca*.02-sa*s*.035,bz=z-sa*.02+ca*s*.035;caja(.006,.0035,.026,MAD,bx,y+.0055,bz,a);caja(.002,.008,.026,MAD2,bx-ca*.004,y+.009,bz-sa*.004,a);
   for(const t of[-1,1])caja(.005,.0055,.003,GRA2,bx-sa*t*.01,y,bz+ca*t*.01,a)}
  pon(new THREE.CylinderGeometry(.0012,.0012,.03,6),MAD2,x-ca*.05,y+.015,z-sa*.05);caja(.002,.012,.022,MAD,x-ca*.05,y+.026,z-sa*.05,a)}
 {const[x,z,y]=D.rosa;pon(new THREE.CylinderGeometry(.03,.031,.004,24),GRA,x,y+.001,z,0,false);
  for(let k=0;k<8;k++){const b=k/8*6.283,L_=k%2?.016:.027;const g=new THREE.ConeGeometry(.004,L_,4);g.rotateZ(-Math.PI/2);g.translate(L_/2,0,0);g.scale(1,.25,1);pon(g,k===6?ROJ:GRAO,x,y+.0035,z,b)}}
 // ---------- 6) paseo de Patos: muro bajo con albardilla, farolas clásicas, pasarelas y socorristas ----------
 {const pos=[],col=[],cMuro=['#d9d4c8','#d2ccbf','#ddd8cd'].map(C3),cAlb=['#9d978b','#938d81','#a7a194'].map(C3);
  const box=(ax,az,ay,bx,bz,by,e,h,y0,cc)=>{const dx=bx-ax,dz=bz-az,l=Math.hypot(dx,dz);if(l<1e-5)return;const nx=-dz/l*e/2,nz=dx/l*e/2;
   const a0=ay+y0,b0=by+y0,a1=a0+h,b1=b0+h;const P=[[ax+nx,a0,az+nz],[bx+nx,b0,bz+nz],[bx+nx,b1,bz+nz],[ax+nx,a1,az+nz],[ax-nx,a0,az-nz],[bx-nx,b0,bz-nz],[bx-nx,b1,bz-nz],[ax-nx,a1,az-nz]];
   for(const[a,b,c,d]of[[0,1,2,3],[5,4,7,6],[3,2,6,7],[4,0,3,7],[1,5,6,2]]){pos.push(...P[a],...P[b],...P[c],...P[a],...P[c],...P[d]);for(let i=0;i<6;i++)col.push(...cc)}};
  for(const t of D.muro){for(let i=3;i<t.length;i+=3){const[ax,az,ay,bx,bz,by]=[t[i-3],t[i-2],t[i-1],t[i],t[i+1],t[i+2]];
   box(ax,az,ay,bx,bz,by,.007,.013,-.005,cMuro[(i/3|0)%3]);box(ax,az,ay,bx,bz,by,.0095,.0022,.008,cAlb[(i/3|0)%3])}}
  if(pos.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.computeVertexNormals();
   const mm=new THREE.Mesh(g,M(0xffffff,{vertexColors:true,roughness:.9}));mm.name='muro_paseo_patos';mm.castShadow=!LT;mm.receiveShadow=true;G.add(mm)}}
 for(const[x,z,y]of D.farolas){pon(new THREE.CylinderGeometry(.0026,.0032,.006,8),NEG,x,y+.003,z);pon(new THREE.CylinderGeometry(.0011,.0015,.042,6),NEG,x,y+.027,z);
  pon(new THREE.CylinderGeometry(.0042,.0022,.0018,4),NEG,x,y+.049,z,Math.PI/4);pon(new THREE.CylinderGeometry(.0034,.0024,.0075,4,1),LUZF,x,y+.0525,z,Math.PI/4);
  pon(new THREE.ConeGeometry(.0052,.004,4),NEG,x,y+.0584,z,Math.PI/4);pon(new THREE.SphereGeometry(.0011,6,4),NEG,x,y+.0612,z)}
 for(const[x,z,y,a,l]of D.pasarelas){const ca=Math.cos(a),sa=Math.sin(a),n=Math.max(4,Math.round(l/(LT?.01:.0055)));
  for(let k=0;k<n;k++){const u=(k+.5)/n*l;caja(.0035,.0012,.018,k%4?MAD:MAD2,x+ca*u,y-.0008,z+sa*u,a)}
  for(const s of[-1,1])caja(l,.001,.0018,MAD2,x+ca*l/2-sa*s*.0075,y-.0014,z+sa*l/2+ca*s*.0075,a)}
 for(const[x,z,y,a]of D.socorristas){const ca=Math.cos(a),sa=Math.sin(a);
  for(const s of[-1,1])for(const t of[-1,1])caja(.0018,.028,.0018,BLA,x+ca*s*.007-sa*t*.007,y,z+sa*s*.007+ca*t*.007,a);
  caja(.02,.0025,.02,ROJ,x,y+.028,z,a);caja(.0025,.014,.016,BLA,x-ca*.008,y+.0305,z-sa*.008,a);caja(.008,.002,.012,AMA,x,y+.032,z,a);
  for(let k=0;k<4;k++)caja(.0015,.001,.012,BLA,x+ca*(.012+k*.004),y+.006+k*.0065,z+sa*(.012+k*.004),a);   // escalera
  pon(new THREE.CylinderGeometry(.0007,.0007,.06,5),BLA,x-sa*.016,y+.03,z+ca*.016);caja(.0006,.009,.014,AMA,x-sa*.016+ca*.007,y+.05,z+ca*.016+sa*.007,a+Math.PI/2)}   // bandera amarilla
 // ---------- 7) la ola de Prado: escultura blanca en el acceso a la playa ----------
 {const[x,z,y,a]=D.ola;const s=new THREE.Shape();
  s.moveTo(-.05,0);s.lineTo(.045,0);s.quadraticCurveTo(.05,.022,.034,.04);s.quadraticCurveTo(.018,.054,-.004,.046);s.quadraticCurveTo(-.016,.04,-.012,.03);
  s.quadraticCurveTo(-.004,.024,.006,.03);s.quadraticCurveTo(.014,.036,.02,.03);s.quadraticCurveTo(.028,.018,.018,.01);s.quadraticCurveTo(0,.004,-.05,.006);s.lineTo(-.05,0);
  const g=new THREE.ExtrudeGeometry(s,{depth:.014,bevelEnabled:true,bevelThickness:.0015,bevelSize:.0015,bevelSegments:2,curveSegments:10});g.translate(0,0,-.007);g.scale(1.3,1.3,1.1);
  // el largo de la ola va paralelo a la orilla; mira al mar con su cresta
  pon(g,BLA,x,y-.001,z,a+Math.PI/2,true);caja(.14,.004,.035,GRA2,x,y-.003,z,a+Math.PI/2,true)}
 // ---------- juntar por material ----------
 const junta=(P_,nombre,solido)=>{for(const[mat,gs]of P_){if(!gs.length)continue;const mm=new THREE.Mesh(mergeGeometries(gs),mat);mm.name=nombre;mm.castShadow=!LT&&mat!==LUZF;mm.receiveShadow=true;G.add(mm);if(solido)try{colaBVH(mm)}catch(e){}}};
 junta(PARTS,'piezas_nigran',false);
 root.add(G);junta(SOLID,'piezas_nigran_solidas',true);
 NIG.G=G;NIG.ms=Math.round(performance.now()-t0)}
// ---------- fin de nigran.js
