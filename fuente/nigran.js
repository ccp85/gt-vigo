// ---------- Nigrán: Patos, Prado y Monteferro (nigran.js) ----------
// Zona 2, Panxón: el Templo Votivo do Mar en la ladera sobre la playa (en lugar del bloque del catastro), el dique del
// puerto con pretil, norays, farolas y la baliza verde de la punta, la rampa de varada y unas 45 barcas fondeadas
// (gamelas, planeadoras y veleros pequeños con su boya) que se mecen en la dársena.
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
 // ================= ZONA 2: PANXÓN — Templo Votivo do Mar, puerto y barcas =================
 if(D.panxon){const PX=D.panxon,m=MT;
  // ---------- Templo Votivo do Mar (Antonio Palacios, 1932-1937): fuera el bloque del catastro y el templo de granito ----------
  {const T_=PX.templo,Q=[];for(let i=0;i<T_.quita.length;i+=2)Q.push([T_.quita[i],T_.quita[i+1]]);
   const dentro=(x,z)=>{let c=false;for(let i=0,j=Q.length-1;i<Q.length;j=i++){const[xi,zi]=Q[i],[xj,zj]=Q[j];if((zi>z)!==(zj>z)&&x<(xj-xi)*(z-zi)/(zj-zi)+xi)c=!c}return c};
   const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();let k=0;root.updateMatrixWorld(true);
   root.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||o.parent===G||!/^(edificios|piezas|tejados|cubiertas)/.test(o.name))return;const g=o.geometry,ix=g.index,pos=g.attributes.position;if(!pos)return;if(!g.boundingBox)g.computeBoundingBox();
    const bb=g.boundingBox.clone().applyMatrix4(o.matrixWorld);if(bb.max.x<T_.x-.5||bb.min.x>T_.x+.5||bb.max.z<T_.z-.5||bb.min.z>T_.z+.5)return;const mw=o.matrixWorld;let ch=0;const I=j=>ix?ix.getX(j):j,cnt=ix?ix.count:pos.count;
    for(let i=0;i+2<cnt;i+=3){a.fromBufferAttribute(pos,I(i)).applyMatrix4(mw);b.fromBufferAttribute(pos,I(i+1)).applyMatrix4(mw);c.fromBufferAttribute(pos,I(i+2)).applyMatrix4(mw);
     const mx=(a.x+b.x+c.x)/3,mz=(a.z+b.z+c.z)/3;if(dentro(mx,mz)&&Math.max(a.y,b.y,c.y)>T_.y+.01){if(ix){const i0=ix.getX(i);ix.setX(i+1,i0);ix.setX(i+2,i0)}else for(const j of[i+1,i+2])pos.setXYZ(j,pos.getX(i),pos.getY(i),pos.getZ(i));ch++}}
    if(ch){if(ix)ix.needsUpdate=true;else pos.needsUpdate=true;k+=ch;if(g.boundsTree)try{g.computeBoundsTree()}catch(e){}}});NIG.temploQuitados=k;
   const ang=T_.a,ca=Math.cos(ang),sa=Math.sin(ang),y0=T_.y-.002;
   const TG=M(0xb3ab9c,{roughness:.95}),TG2=M(0x9c9486,{roughness:.95}),TOS=M(0x2b2926,{roughness:1}),TCU=M(0x6d6a64,{roughness:.9}),TCR=M(0x4a4740,{roughness:.6,metalness:.4});
   // L(u,v): u hacia la fachada, v a la derecha; medidas en metros
   const L=(u,v)=>[T_.x+(u*ca-v*sa)*m,T_.z+(u*sa+v*ca)*m];
   const B=(w,h,l,mat,u,v,y,sol=true)=>{const[x,z]=L(u,v);caja(w*m,h*m,l*m,mat,x,y0+y*m,z,ang,sol)};
   const almenas=(u0,u1,v0,v1,y,paso=2.2)=>{   // merlones en el borde de un rectángulo (u0..u1, v0..v1) a la altura y
    for(let u=u0+.6;u<=u1-.5;u+=paso){B(1,1.1,.8,TG2,u,v0+.4,y,false);B(1,1.1,.8,TG2,u,v1-.4,y,false)}
    for(let v=v0+.6;v<=v1-.5;v+=paso){B(.8,1.1,1,TG2,u0+.4,v,y,false);B(.8,1.1,1,TG2,u1-.4,v,y,false)}};
   // terraza y escalinata hacia la playa
   B(36,1.2,26,TG2,0,0,-.6);for(let s=0;s<4;s++)B(1.4,.45,10,TG2,18.7+s*1.4,0,.15-s*.45);
   for(const v of[-12.7,12.7])B(34,1.1,.5,TG,0,v,.6,false);   // pretil de la terraza
   // nave con almenas, naves bajas a los lados y cubierta oscura
   B(26,13,14,TG,1,0,.6);almenas(-12,14,-7,7,13.6);B(25,.8,13,TCU,1,0,12.8,false);
   for(const s of[-1,1]){B(20,8,5,TG2,0,s*9.5,.6);almenas(-10,10,s>0?7:-12,s>0?12:-7,8.6);
    for(let u=-7;u<=7;u+=3.5)B(1.2,3.2,.3,TOS,u,s*12.05,3.2,false)}   // ventanas de las capillas
   for(const s of[-1,1])for(let u=-8;u<=10;u+=4.5)B(1,4,.3,TOS,u,s*7.05,9,false);   // ventanales altos de la nave
   // ábside semicircular detrás, con el arco visigótico
   {const[x,z]=L(-12,0);const g=new THREE.CylinderGeometry(7*m,7*m,10*m,20,1,false,Math.PI,Math.PI);pon(g,TG,x,y0+5.6*m,z,ang,true);
    const[xa,za]=L(-19.05,0);const ar=new THREE.CylinderGeometry(1.1*m,1.1*m,.3*m,14);ar.rotateZ(Math.PI/2);pon(ar,TOS,xa,y0+4.2*m,za,ang,false);B(.3,2.4,2.2,TOS,-19.05,0,1.8,false)}
   // fachada: muro alto con almenas, gran arco de entrada y rosetón
   B(1.6,17,16,TG,14.6,0,.6);almenas(13.8,15.4,-8,8,17.6,2);
   B(.4,7,5,TOS,15.45,0,.6,false);{const[x,z]=L(15.45,0);const g=new THREE.CylinderGeometry(2.5*m,2.5*m,.4*m,18);g.rotateZ(Math.PI/2);pon(g,TOS,x,y0+7.6*m,z,ang,false)}
   {const[x,z]=L(15.5,0);const g=new THREE.TorusGeometry(3.1*m,.35*m,6,24,Math.PI);g.rotateY(Math.PI/2);pon(g,TG2,x,y0+7.6*m,z,ang,false)}
   {const[x,z]=L(15.45,0);const g=new THREE.CylinderGeometry(2.1*m,2.1*m,.4*m,20);g.rotateZ(Math.PI/2);pon(g,TOS,x,y0+12.6*m,z,ang,false);const r=new THREE.TorusGeometry(2.2*m,.3*m,6,24);r.rotateY(Math.PI/2);pon(r,TG2,x+ca*.1*m,y0+12.6*m,z+sa*.1*m,ang,false)}
   {const[x,z]=L(15,0);pon(new THREE.BoxGeometry(.4*m,2.4*m,.4*m),TCR,x,y0+19.6*m,z);pon(new THREE.BoxGeometry(.4*m,.4*m,1.6*m),TCR,x,y0+20.2*m,z,ang)}
   // torre cuadrada con campanario y almenas, a la derecha de la fachada
   B(7.5,28,7.5,TG,10.5,10.5,.6);almenas(6.75,14.25,6.75,14.25,28.6,1.9);
   for(const[du,dv,w,l]of[[3.8,0,.3,2],[-3.8,0,.3,2],[0,3.8,2,.3],[0,-3.8,2,.3]])B(w,4.5,l,TOS,10.5+du,10.5+dv,21,false);   // huecos de las campanas
   for(const[du,dv]of[[-3.4,-3.4],[3.4,-3.4],[-3.4,3.4],[3.4,3.4]])B(1.3,2.2,1.3,TG2,10.5+du,10.5+dv,28.6,false);       // garitas de las esquinas
   // torrecilla redonda y esbelta con la aguja y la cruz
   {const[x,z]=L(9.5,5.4);pon(new THREE.CylinderGeometry(1.5*m,1.7*m,33*m,14),TG,x,y0+17.1*m,z,0,true);pon(new THREE.CylinderGeometry(2*m,1.6*m,1*m,14),TG2,x,y0+33.8*m,z);
    pon(new THREE.ConeGeometry(1.1*m,6*m,10),TG2,x,y0+37.3*m,z);pon(new THREE.CylinderGeometry(.08*m,.08*m,3*m,5),TCR,x,y0+41.5*m,z);pon(new THREE.BoxGeometry(.15*m,.15*m,1.4*m),TCR,x,y0+42.3*m,z,ang);
    for(let k=0;k<4;k++)B(.3,1.4,.6,TOS,9.5+Math.cos(k*1.57)*1.6,5.4+Math.sin(k*1.57)*1.6,26,false)}}
  // ---------- dique del puerto: pretil por fuera, norays por dentro, farolas y la baliza verde de la punta ----------
  {const E=PX.dique.eje,[nx,nz]=PX.dique.n;
   for(let i=1;i<E.length;i++){const[a1,b1,c1,wl1]=E[i-1],[a2,b2,c2,wl2]=E[i];
    const ox1=-nx*Math.max(.01,wl1-.008),oz1=-nz*Math.max(.01,wl1-.008),ox2=-nx*Math.max(.01,wl2-.008),oz2=-nz*Math.max(.01,wl2-.008);
    const x1=a1+ox1,z1=b1+oz1,x2=a2+ox2,z2=b2+oz2,l=Math.hypot(x2-x1,z2-z1);if(l<1e-4)continue;
    caja(l+.002,.014,.008,i%2?GRA:GRA2,(x1+x2)/2,(Math.max(c1,c2))-.003,(z1+z2)/2,Math.atan2(z2-z1,x2-x1),true)}
   for(let i=1;i<E.length-1;i+=2){const[x,z,y,wl,wr]=E[i];pon(new THREE.CylinderGeometry(.0025,.003,.007,8),NEG,x+nx*Math.max(.008,wr-.008),y+.0035,z+nz*Math.max(.008,wr-.008))}
   for(let i=3;i<E.length-1;i+=6){const[x,z,y,wl]=E[i],fx=x-nx*Math.max(.012,wl-.02),fz=z-nz*Math.max(.012,wl-.02);
    pon(new THREE.CylinderGeometry(.0011,.0015,.042,6),NEG,fx,y+.021,fz);pon(new THREE.CylinderGeometry(.0034,.0024,.0075,4,1),LUZF,fx,y+.046,fz,Math.PI/4);pon(new THREE.ConeGeometry(.0052,.004,4),NEG,fx,y+.052,fz,Math.PI/4)}
   const[x,z,y]=E[E.length-1];const VERD=M(0x2f8f4a,{roughness:.6});
   pon(new THREE.CylinderGeometry(.012,.014,.012,14),BLA,x,y+.006,z,0,true);pon(new THREE.CylinderGeometry(.006,.008,.045,12),VERD,x,y+.0345,z,0,true);
   pon(new THREE.CylinderGeometry(.0085,.0085,.0025,12),NEG,x,y+.058,z);pon(new THREE.CylinderGeometry(.004,.004,.008,10),M(0xb7f5c4,{emissive:0x33ff66,emissiveIntensity:.8,roughness:.2}),x,y+.0632,z);pon(new THREE.ConeGeometry(.005,.005,10),VERD,x,y+.0697,z)}
  // ---------- rampa de varada ----------
  {const[x,z,y,a]=PX.rampa,ca=Math.cos(a),sa=Math.sin(a),l=.11,c=-.05,g=new THREE.BoxGeometry(l,.004,.05);
   const p=g.attributes.position;for(let i=0;i<p.count;i++){const u=(p.getX(i)+l/2)/l;p.setY(i,p.getY(i)+(y-.002)+(c-y)*u)}g.computeVertexNormals();pon(g,HOR,x+ca*(l/2-.01),0,z+sa*(l/2-.01),a)}
  // ---------- barcas fondeadas: gamelas, planeadoras y veleros pequeños, con su boya; se mecen ----------
  if(typeof BARC!=='undefined'&&BARC.casco){const PAL=[[0x2f6fb0,0xf2efe6],[0x2e8b57,0xf2efe6],[0xc8352b,0xf2efe6],[0xf2efe6,0x2f6fb0],[0xe9c234,0x2f6fb0],[0x1f4f8f,0xc8352b],[0xf2efe6,0x2e8b57],[0x7a3e9d,0xf2efe6]];
   const tmp=new THREE.Color();
   // aplana un grupo a triángulos con color por vértice (color propio × color del material)
   const aplana=(g,out)=>{g.updateMatrixWorld(true);g.traverse(o=>{if(!o.isMesh||(o.material&&(o.material.transparent||o.material.isMeshBasicMaterial)))return;let geo=o.geometry.index?o.geometry.toNonIndexed():o.geometry.clone();geo.applyMatrix4(o.matrixWorld);
    const p=geo.attributes.position,cc=geo.attributes.color,mc=o.material.color||tmp.set(0xffffff);for(let i=0;i<p.count;i++){out.p.push(p.getX(i),p.getY(i),p.getZ(i));if(cc)out.c.push(cc.getX(i)*mc.r,cc.getY(i)*mc.g,cc.getZ(i)*mc.b);else out.c.push(mc.r,mc.g,mc.b)}})};
   const barca=(tipo,ci)=>{const g=new THREE.Group(),[c1,c2]=PAL[ci%PAL.length],MM=BARC.mat;
    if(tipo===0){const cg=BARC.casco({L:.07,B:.026,H:.011,D:.005,NS:14,NU:5,fondo:'plano',popa:.58,arrufo:.008,arrufoPopa:.002,col:c1,banda:c2,obra:0x2f3b2e,flot:-.002,anchoBanda:.0028,franja:0xf2efe6});
     g.add(new THREE.Mesh(cg,MM(0xffffff,{vertexColors:true})));g.add(BARC.cubierta(cg,.03,.93,.0085,MM(0x9b7653)));for(const r of BARC.regala(cg,.0009,MM(0x6b4a2e),.985))g.add(r);
     const sec=cg.userData.sec;for(const t of[.3,.62]){const S=sec(t),b=new THREE.Mesh(new THREE.BoxGeometry(.007,.0014,S.w*1.85),MM(0x9b7653));b.position.set(-.035+t*.07,S.top-.004,0);g.add(b)}}
    else if(tipo===1){const cg=BARC.casco({L:.075,B:.028,H:.012,D:.007,NS:14,NU:5,fondo:'v',popa:.82,arrufo:.006,col:0xf2f2ee,banda:c1,obra:0x3a2b2b,flot:-.003,anchoBanda:.004});
     g.add(new THREE.Mesh(cg,MM(0xffffff,{vertexColors:true})));g.add(BARC.cubierta(cg,.04,.97,.007,MM(0xd9d6cf)));
     const co=new THREE.Mesh(new THREE.BoxGeometry(.014,.01,.014),MM(0xf4f3ee));co.position.set(.008,.014,0);g.add(co);const mo=new THREE.Mesh(new THREE.BoxGeometry(.008,.011,.007),MM(0x1d1f24));mo.position.set(-.04,.012,0);g.add(mo);
     const lo=new THREE.Mesh(new THREE.BoxGeometry(.016,.0012,.022),MM(c2===0xf2efe6?0x2b3a55:c2));lo.position.set(.024,.0125,0);g.add(lo)}
    else{const cg=BARC.casco({L:.09,B:.03,H:.011,D:.012,NS:16,NU:5,fondo:'redondo',popa:.75,arrufo:.004,col:0xf4f4f0,banda:c1,obra:0x223355,flot:-.002,anchoBanda:.003});
     g.add(new THREE.Mesh(cg,MM(0xffffff,{vertexColors:true})));g.add(BARC.cubierta(cg,.02,.97,.0015,MM(0xb08a5c)));
     const ca_=new THREE.Mesh(new THREE.BoxGeometry(.03,.007,.018),MM(0xf2f2ee));ca_.position.set(-.004,.014,0);g.add(ca_);
     const ma=new THREE.Mesh(new THREE.CylinderGeometry(.0008,.001,.13,5),MM(0xd8dadc,{metalness:.5}));ma.position.set(.012,.075,0);g.add(ma);
     const bo=new THREE.Mesh(new THREE.CylinderGeometry(.0006,.0006,.04,5),MM(0xd8dadc,{metalness:.5}));bo.rotation.z=Math.PI/2;bo.position.set(-.008,.022,0);g.add(bo)}
    return g};
   const MAR_Y=-.03,lista=LT?PX.barcas.filter((b,i)=>i%2===0):PX.barcas,TRES=[{p:[],c:[]},{p:[],c:[]},{p:[],c:[]}],BOY=[];
   for(const[x,z,tipo,ci,a,s]of lista){const g=barca(tipo,ci);g.rotation.y=-a;g.position.set(x,0,z);const k=Math.floor(s*3)%3;aplana(g,TRES[k]);BOY.push([x+Math.cos(a)*.055,z+Math.sin(a)*.055,ci])}
   const mB=M(0xffffff,{vertexColors:true,roughness:.55,side:THREE.DoubleSide}),mallas=[];
   TRES.forEach((T,k)=>{if(!T.p.length)return;const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(T.p,3));g.setAttribute('color',new THREE.Float32BufferAttribute(T.c,3));g.computeVertexNormals();
    const mm=new THREE.Mesh(g,mB);mm.name='barcas_panxon';mm.position.y=MAR_Y;mm.castShadow=!LT;mm.receiveShadow=true;mm.userData.fase=k*2.1;G.add(mm);mallas.push(mm)});
   for(const[x,z,ci]of BOY)pon(new THREE.SphereGeometry(.0045,10,8),ci%2?ROJ:M(0xff8a1e,{roughness:.6}),x,MAR_Y+.001,z);
   // vaivén suave: cada tercio de la flota con su fase
   const t0=performance.now();const meces=()=>{if(!mallas.length||!mallas[0].parent)return;const t=(performance.now()-t0)/1000;
    for(const mm of mallas){const f=mm.userData.fase;mm.position.y=MAR_Y+Math.sin(t*1.3+f)*.0012;mm.rotation.z=Math.sin(t*.9+f)*.006;mm.rotation.x=Math.sin(t*1.1+f*1.7)*.005}
    requestAnimationFrame(meces)};requestAnimationFrame(meces);NIG.barcas=lista.length}}
 // ---------- juntar por material ----------
 const junta=(P_,nombre,solido)=>{for(const[mat,gs]of P_){if(!gs.length)continue;const mm=new THREE.Mesh(mergeGeometries(gs),mat);mm.name=nombre;mm.castShadow=!LT&&mat!==LUZF;mm.receiveShadow=true;G.add(mm);if(solido)try{colaBVH(mm)}catch(e){}}};
 junta(PARTS,'piezas_nigran',false);
 root.add(G);junta(SOLID,'piezas_nigran_solidas',true);
 NIG.G=G;NIG.ms=Math.round(performance.now()-t0)}
// ---------- fin de nigran.js
