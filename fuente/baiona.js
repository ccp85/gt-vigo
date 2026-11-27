// ---------- Baiona: Casco Vello y porto (baiona.js) ----------
// Baiona con detalle, zona 1, con Google Earth, Street View y fotos como referencia (toda la geometría es propia).
// Datos en baiona_detalle.json (fuente/herramientas/baiona_hornear.py).
// · Casco Vello: rúas peatonales, aceras y calles estrechas con losas de granito de tonos distintos.
// · Colexiata de Santa María (s. XIII) en lo alto del casco, en lugar del bloque del catastro: tres naves de granito con
//   tejado de teja, tres ábsides rectangulares, fachada al oeste con contrafuertes, portada de arquivoltas y rosetón,
//   y una torre robusta con almenas que le da el aire de fortaleza.
// · Paseo marítimo: muro de granito con albardilla sobre el mar, farolas clásicas, bancos y árboles.
// · Porto: la réplica de la Carabela Pinta atracada en el peirao central (castillos de popa y proa, tres palos, velas
//   cuadras con la cruz roja, vela latina en la mesana, bauprés, jarcia, banderas y la pasarela al muelle), la lonxa del
//   muelle pesquero con cajas de pescado, norays en los muelles y gamelas fondeadas en la dársena que se mecen.
const BYN={root:null,datos:null,carga:null};window.__BYN=BYN;
function bynChk(){if(!MAPA||!MI)return;const z=ZROOTS.find(q=>q.root&&q.root.name==='baiona'&&q.root.parent);if(!z||BYN.root===z.root)return;
 const r=z.root;BYN.root=r;
 (BYN.carga||(BYN.carga=fetch('baiona_detalle.json').then(x=>{if(!x.ok)throw new Error('HTTP '+x.status);return x.json()}))).then(d=>{BYN.datos=d;if(BYN.root!==r||!r.parent)return;
  setTimeout(()=>{if(!r.parent)return;try{bynCrea(r,d)}catch(e){console.warn('baiona',e);BYN.err=String(e)+' '+String(e.stack).slice(0,600)}},1600)}).catch(e=>{BYN.carga=null;BYN.root=null;console.warn('baiona json',e)})}
function bynCrea(root,D){const LT=!!window.LITE,t0=performance.now(),G=new THREE.Group();G.name='baiona_detalle';
 let rs=71;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.9},o));
 const C3=h=>{const c=new THREE.Color(h);return[c.r,c.g,c.b]};
 const m=1/78;                                      // 1 unidad del mapa ≈ 78 m
 const PARTS=new Map(),SOLID=new Map();
 const prep=g=>{g=g.index?g.toNonIndexed():g;if(g.attributes.uv)g.deleteAttribute('uv');if(g.attributes.uv1)g.deleteAttribute('uv1');if(!g.attributes.normal)g.computeVertexNormals();return g};
 // pone la geometría g (local) girada a ang (dirección cos,sin en x,z) en (x,y,z); solido → choca
 const pon=(g,mat,x,y,z,ang=0,solido=false)=>{g=prep(g);if(ang)g.rotateY(-ang);g.translate(x,y,z);const P_=solido?SOLID:PARTS;if(!P_.has(mat))P_.set(mat,[]);P_.get(mat).push(g)};
 const caja=(w,h,l,mat,x,y,z,ang=0,solido=false)=>pon(new THREE.BoxGeometry(w,h,l),mat,x,y+h/2,z,ang,solido);
 const LOC=(x0,z0,a)=>{const ca=Math.cos(a),sa=Math.sin(a);return(u,v)=>[x0+u*ca-v*sa,z0+u*sa+v*ca]};
 const tejado=(w,l,h)=>{const s=new THREE.Shape();s.moveTo(-w/2,0);s.lineTo(w/2,0);s.lineTo(0,h);s.lineTo(-w/2,0);const g=new THREE.ExtrudeGeometry(s,{depth:l,bevelEnabled:false});g.translate(0,0,-l/2);g.rotateY(Math.PI/2);return g};
 const GRA=M(0xa39d90,{roughness:.95}),GRA2=M(0x8b8579,{roughness:.95}),GRAO=M(0x2c2a27,{roughness:1}),TEJ=M(0xa9512f,{roughness:.85}),TEJ2=M(0x934528,{roughness:.85}),
  NEG=M(0x22252a,{roughness:.5,metalness:.5}),LUZF=M(0xfff1d0,{emissive:0xffd98a,emissiveIntensity:.5,roughness:.3}),MAD=M(0x8a6a48,{roughness:.9}),MAD2=M(0x5e4430,{roughness:.9}),
  BLA=M(0xefece5,{roughness:.8}),ROJ=M(0xb8282a,{roughness:.7}),AZU=M(0x2f62a8,{roughness:.6}),TRO=M(0x6b5a45,{roughness:1}),HOJ=M(0x4f7a35,{roughness:.9}),HOJ2=M(0x3f6a2c,{roughness:.9});
 // ---------- 1) Casco Vello: losas de granito en rúas, aceras y calles estrechas ----------
 // los propios triángulos de la calzada y las aceras del casco (mismo plano, un pelo por encima) con una textura de losas
 // a hiladas en coordenadas del mundo: cada losa de ~1 m × 0,65 m con su tono y sus juntas
 if(D.losas){const S=D.losas,W=S.w,H=S.h;const kv=(x,z)=>{const i=Math.round((x-S.x0)/S.s),j=Math.round((z-S.z0)/S.s);if(i<0||j<0||i>=W||j>=H)return 0;return S.k.charCodeAt(j*W+i)-48};
  const X0=S.x0,X1=S.x0+W*S.s,Z0=S.z0,Z1=S.z0+H*S.s;
  const NX=8,NZ=12,LX=.0125,LZ=.0085,TX=LT?256:512,cv=document.createElement('canvas');cv.width=cv.height=TX;const g2=cv.getContext('2d'),px=TX/NX,pz=TX/NZ;
  const TON=['#9e998f','#a8a397','#958f84','#b0aa9d','#8d887e','#a49c8c','#99948a','#aba596'];
  g2.fillStyle='#5e5a53';g2.fillRect(0,0,TX,TX);
  for(let j=0;j<NZ;j++)for(let i=-1;i<NX;i++){const x=(i+(j%2)*.5)*px,y=j*pz;g2.fillStyle=TON[(rn()*TON.length)|0];g2.fillRect(x+1.5,y+1.5,px-3,pz-3);
   for(let k=0;k<(LT?6:24);k++){g2.fillStyle=`rgba(${rn()<.5?'40,38,34':'230,226,215'},${.05+rn()*.08})`;g2.fillRect(x+2+rn()*(px-6),y+2+rn()*(pz-6),1+rn()*3,1+rn()*3)}}   // grano del granito
  const tex=new THREE.CanvasTexture(cv);tex.wrapS=tex.wrapT=THREE.RepeatWrapping;tex.colorSpace=THREE.SRGBColorSpace;tex.anisotropy=4;
  const pos=[],uv=[],a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3(),ALZA=.0015,UX=1/(NX*LX),UZ=1/(NZ*LZ);
  root.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||o.parent===G||!/^(calzada|aceras)/.test(o.name))return;o.updateMatrixWorld(true);
   const g=o.geometry,p=g.attributes.position;if(!p)return;const ix=g.index,n=ix?ix.count:p.count,mw=o.matrixWorld;
   if(!g.boundingBox)g.computeBoundingBox();const bb=g.boundingBox.clone().applyMatrix4(mw);if(bb.max.x<X0||bb.min.x>X1||bb.max.z<Z0||bb.min.z>Z1)return;
   for(let t=0;t<n;t+=3){const i0=ix?ix.getX(t):t,i1=ix?ix.getX(t+1):t+1,i2=ix?ix.getX(t+2):t+2;
    a.fromBufferAttribute(p,i0).applyMatrix4(mw);if(a.x<X0-.1||a.x>X1+.1||a.z<Z0-.1||a.z>Z1+.1)continue;
    b.fromBufferAttribute(p,i1).applyMatrix4(mw);c.fromBufferAttribute(p,i2).applyMatrix4(mw);
    // dentro del casco si el centro (o la mayoría de los vértices) cae en una celda marcada
    const cx=(a.x+b.x+c.x)/3,cz=(a.z+b.z+c.z)/3;if(!kv(cx,cz)&&kv(a.x,a.z)+kv(b.x,b.z)+kv(c.x,c.z)<2)continue;
    for(const q of[a,b,c]){pos.push(q.x,q.y+ALZA,q.z);uv.push(q.x*UX,q.z*UZ)}}});
  if(pos.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.computeVertexNormals();
   const nn=g.attributes.normal;for(let i=0;i<nn.count;i++)if(nn.getY(i)<0)nn.setXYZ(i,-nn.getX(i),-nn.getY(i),-nn.getZ(i));
   const mm=new THREE.Mesh(g,M(0xffffff,{map:tex,roughness:.85,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3}));mm.name='losas_casco_baiona';mm.receiveShadow=true;mm.castShadow=false;G.add(mm);BYN.losas=pos.length/9}}
 // ---------- 2) Colexiata de Santa María: fuera el bloque del catastro y la iglesia de granito ----------
 if(D.colexiata){const T_=D.colexiata,Q=[];for(let i=0;i<T_.quita.length;i+=2)Q.push([T_.quita[i],T_.quita[i+1]]);
  const dentro=(x,z)=>{let c=false;for(let i=0,j=Q.length-1;i<Q.length;j=i++){const[xi,zi]=Q[i],[xj,zj]=Q[j];if((zi>z)!==(zj>z)&&x<(xj-xi)*(z-zi)/(zj-zi)+xi)c=!c}return c};
  const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();let k=0;root.updateMatrixWorld(true);
  root.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||o.parent===G||!/^(edificios|piezas|tejados|cubiertas)/.test(o.name))return;const g=o.geometry,ix=g.index,pos=g.attributes.position;if(!pos)return;if(!g.boundingBox)g.computeBoundingBox();
   const bb=g.boundingBox.clone().applyMatrix4(o.matrixWorld);if(bb.max.x<T_.x-.6||bb.min.x>T_.x+.6||bb.max.z<T_.z-.6||bb.min.z>T_.z+.6)return;const mw=o.matrixWorld;let ch=0;const I=j=>ix?ix.getX(j):j,cnt=ix?ix.count:pos.count;
   for(let i=0;i+2<cnt;i+=3){a.fromBufferAttribute(pos,I(i)).applyMatrix4(mw);b.fromBufferAttribute(pos,I(i+1)).applyMatrix4(mw);c.fromBufferAttribute(pos,I(i+2)).applyMatrix4(mw);
    const mx=(a.x+b.x+c.x)/3,mz=(a.z+b.z+c.z)/3;if(dentro(mx,mz)&&Math.max(a.y,b.y,c.y)>T_.y+.01){if(ix){const i0=ix.getX(i);ix.setX(i+1,i0);ix.setX(i+2,i0)}else for(const j of[i+1,i+2])pos.setXYZ(j,pos.getX(i),pos.getY(i),pos.getZ(i));ch++}}
   if(ch){if(ix)ix.needsUpdate=true;else pos.needsUpdate=true;k+=ch;if(g.boundsTree)try{g.computeBoundsTree()}catch(e){}}});BYN.colexiataQuitados=k;
  // L(u,v): u hacia la fachada (oeste), v a la derecha; medidas en metros. Cabe en el solar del bloque quitado
  const LL=Math.min(44,T_.l*78-3),WW=Math.min(22,T_.w*78-2),ang=T_.a,L=LOC(T_.x,T_.z,ang),y0=T_.y-.002;
  const B=(w,h,l,mat,u,v,y,sol=true)=>{const[x,z]=L(u*m,v*m);caja(w*m,h*m,l*m,mat,x,y0+y*m,z,ang,sol)};
  const CG=M(0xa8a194,{roughness:.95}),CG2=M(0x938c7f,{roughness:.95});
  const nave=LL-8,uF=LL/2-1,uA=-LL/2+4;           // nave de uF (fachada) a uA (cabecera)
  B(LL+3,3,WW+3,CG2,0,0,-2.6);                     // zócalo que asienta la iglesia en la ladera
  // nave central alta y naves laterales bajas
  B(nave,11,WW*.42,CG,(uF+uA)/2,0,0);{const[x,z]=L((uF+uA)/2*m,0);pon(tejado(WW*.46*m,nave*m+.002,3.4*m),TEJ,x,y0+11*m,z,ang,true)}
  for(const s of[-1,1]){B(nave,7,WW*.29,CG2,(uF+uA)/2,s*WW*.355,0);
   {const g=tejado(WW*.62*m,nave*m,2.2*m);const[x,z]=L((uF+uA)/2*m,s*WW*.355*m);pon(g,TEJ2,x,y0+7*m-1.1*m,z,ang,true)}
   // ventanas románicas (aspilleras) de las naves laterales y de la nave central
   for(let u=uA+4;u<uF-3;u+=5){B(1.2,2.2,.3,GRAO,u,s*(WW/2+.02),3,false);B(1,1.8,.3,GRAO,u,s*(WW*.21+.02),8.2,false)}
   // contrafuertes
   for(let u=uA+1.5;u<uF;u+=5)B(1.4,6,1.2,CG2,u,s*(WW/2+.5),0)}
  // cabecera: tres ábsides rectangulares, el central más alto y profundo
  B(7,9,WW*.38,CG,uA-3.5,0,0);{const[x,z]=L((uA-3.5)*m,0);pon(tejado(WW*.42*m,7*m,2.8*m),TEJ,x,y0+9*m,z,ang,true)}
  for(const s of[-1,1]){B(5,6,WW*.26,CG2,uA-2.5,s*WW*.33,0);const[x,z]=L((uA-2.5)*m,s*WW*.33*m);pon(tejado(WW*.3*m,5*m,1.8*m),TEJ2,x,y0+6*m,z,ang,true);B(.3,2,1,GRAO,uA-5.05,s*WW*.33,2.5,false)}
  B(.3,2.6,1.2,GRAO,uA-7.05,0,4,false);
  // fachada oeste: hastial con piñón, dos contrafuertes, portada de arquivoltas con tímpano liso y rosetón
  {const s=new THREE.Shape(),w=WW*.48;s.moveTo(-w/2,0);s.lineTo(w/2,0);s.lineTo(w/2,11);s.lineTo(0,14.6);s.lineTo(-w/2,11);s.lineTo(-w/2,0);
   const g=new THREE.ExtrudeGeometry(s,{depth:1.4,bevelEnabled:false});g.scale(m,m,m);g.translate(0,0,-.7*m);g.rotateY(Math.PI/2);const[x,z]=L(uF*m,0);pon(g,CG,x,y0,z,ang,true)}
  for(const v of[-WW*.2,WW*.2])B(1.6,9,1.4,CG2,uF+1,v,0);
  for(let k=0;k<3;k++){const r=2.2-k*.45;const[x,z]=L((uF+.75+k*.12)*m,0);const ar=new THREE.TorusGeometry(r*m,.22*m,6,18,Math.PI);ar.rotateY(Math.PI/2);pon(ar,k%2?CG2:CG,x,y0+3.6*m,z,ang)}
  for(const v of[-2.4,-1.9,-1.4,1.4,1.9,2.4])B(.45,3.6,.45,CG2,uF+.8,v,0,false);   // columnas acodilladas
  B(.3,3.6,2.4,GRAO,uF+.72,0,0,false);{const[x,z]=L((uF+.72)*m,0);const ti=new THREE.CylinderGeometry(1.2*m,1.2*m,.3*m,14,1,false,0,Math.PI);ti.rotateZ(Math.PI/2);ti.rotateX(Math.PI/2);pon(ti,CG2,x,y0+3.6*m,z,ang)}
  {const[x,z]=L((uF+.75)*m,0);const g=new THREE.CylinderGeometry(1.5*m,1.5*m,.3*m,16);g.rotateZ(Math.PI/2);pon(g,GRAO,x,y0+8.6*m,z,ang);const r=new THREE.TorusGeometry(1.6*m,.25*m,6,20);r.rotateY(Math.PI/2);pon(r,CG2,x+Math.cos(ang)*.1*m,y0+8.6*m,z+Math.sin(ang)*.1*m,ang)}
  {const[x,z]=L((uF+.4)*m,0);caja(.25*m,1.6*m,.25*m,CG2,x,y0+14.4*m,z,ang);caja(.25*m,.25*m,1*m,CG2,x,y0+15.3*m,z,ang)}   // cruz del piñón
  // torre robusta a la derecha de la fachada, con almenas: el aire de fortaleza
  {const tu=uF-3,tv=WW/2+2.2;B(6.5,18,6.5,CG,tu,tv,0);B(7.1,.5,7.1,CG2,tu,tv,18);
   for(const[du,dv,w,l]of[[3.27,0,.3,1.6],[-3.27,0,.3,1.6],[0,3.27,1.6,.3],[0,-3.27,1.6,.3]])B(w,3,l,GRAO,tu+du,tv+dv,13.5,false);   // huecos de las campanas
   for(let k=0;k<8;k++){const t=k/8*6.283;const du=Math.abs(Math.cos(t))>.7?Math.sign(Math.cos(t))*3.05:Math.cos(t)*4.3,dv=Math.abs(Math.sin(t))>.7?Math.sign(Math.sin(t))*3.05:Math.sin(t)*4.3;B(1.1,1.2,1.1,CG2,tu+du,tv+dv,18.5,false)}
   B(1,2.4,.3,GRAO,tu+3.27,tv,2,false)}
  // almenas sobre las naves laterales, como en la iglesia real
  for(const s of[-1,1])for(let u=uA+1;u<uF-1;u+=2.4)B(1.1,1,.7,CG2,u,s*(WW/2-.35),7,false);
  BYN.colexiata=1}
 // ---------- 3) paseo marítimo: muro de granito, farolas, bancos y árboles ----------
 if(D.paseo){const PS=D.paseo;
  {const pos=[],col=[],cMuro=['#aaa496','#a09a8d','#b3ad9f'].map(C3),cAlb=['#c6c1b5','#bdb8ac','#cfcabd'].map(C3);
   const box=(ax,az,ay,bx,bz,by,e,h,y0,cc)=>{const dx=bx-ax,dz=bz-az,l=Math.hypot(dx,dz);if(l<1e-5)return;const nx=-dz/l*e/2,nz=dx/l*e/2;
    const a0=ay+y0,b0=by+y0,a1=a0+h,b1=b0+h;const P=[[ax+nx,a0,az+nz],[bx+nx,b0,bz+nz],[bx+nx,b1,bz+nz],[ax+nx,a1,az+nz],[ax-nx,a0,az-nz],[bx-nx,b0,bz-nz],[bx-nx,b1,bz-nz],[ax-nx,a1,az-nz]];
    for(const[a,b,c,d]of[[0,1,2,3],[5,4,7,6],[3,2,6,7],[4,0,3,7],[1,5,6,2]]){pos.push(...P[a],...P[b],...P[c],...P[a],...P[c],...P[d]);for(let i=0;i<6;i++)col.push(...cc)}};
   for(const t of PS.muro){for(let i=3;i<t.length;i+=3){const[ax,az,ay,bx,bz,by]=[t[i-3],t[i-2],t[i-1],t[i],t[i+1],t[i+2]];
    box(ax,az,ay,bx,bz,by,.007,.014,-.004,cMuro[(i/3|0)%3]);box(ax,az,ay,bx,bz,by,.0095,.0022,.01,cAlb[(i/3|0)%3])}}
   if(pos.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.computeVertexNormals();
    const mm=new THREE.Mesh(g,M(0xffffff,{vertexColors:true,roughness:.9}));mm.name='muro_paseo_baiona';mm.castShadow=!LT;mm.receiveShadow=true;G.add(mm)}}
  for(const[x,z,y]of PS.farolas){pon(new THREE.CylinderGeometry(.0026,.0032,.006,8),NEG,x,y+.003,z);pon(new THREE.CylinderGeometry(.0011,.0015,.042,6),NEG,x,y+.027,z);
   pon(new THREE.CylinderGeometry(.0042,.0022,.0018,4),NEG,x,y+.049,z,Math.PI/4);pon(new THREE.CylinderGeometry(.0034,.0024,.0075,4,1),LUZF,x,y+.0525,z,Math.PI/4);
   pon(new THREE.ConeGeometry(.0052,.004,4),NEG,x,y+.0584,z,Math.PI/4);pon(new THREE.SphereGeometry(.0011,6,4),NEG,x,y+.0612,z)}
  for(const[x,z,y,a]of PS.bancos){const ca=Math.cos(a),sa=Math.sin(a);   // banco de granito con asiento de madera, mirando al mar
   for(const t of[-1,1])caja(.004,.0055,.0035,GRA2,x-sa*t*.009,y,z+ca*t*.009,a,true);
   caja(.0055,.0012,.024,MAD,x,y+.0055,z,a);caja(.0012,.006,.024,MAD2,x-ca*.0028,y+.0067,z-sa*.0028,a)}
  for(const[x,z,y,s]of(LT?PS.arboles.filter((t,i)=>i%2===0):PS.arboles)){const h=.03+s*.012;   // tamarindos y plátanos del paseo, con alcorque
   caja(.012,.0012,.012,GRA2,x,y,z,0);pon(new THREE.CylinderGeometry(.0013,.0019,h,6),TRO,x,y+h/2,z);
   for(let k=0;k<3;k++){const g=new THREE.IcosahedronGeometry(.009+s*.004-k*.0015,0);g.scale(1.15,.8,1.1);pon(g,k%2?HOJ2:HOJ,x+Math.cos(k*2.1+s*6)*.004,y+h+k*.004,z+Math.sin(k*2.1+s*6)*.004)}}}
 // ---------- 4) norays en los muelles ----------
 if(D.norays)for(const[x,z,y]of(LT?D.norays.filter((n,i)=>i%2===0):D.norays)){pon(new THREE.CylinderGeometry(.0022,.0026,.0045,8),NEG,x,y+.00225,z);pon(new THREE.CylinderGeometry(.003,.003,.0012,8),NEG,x,y+.005,z)}
 // ---------- 5) la lonxa del muelle pesquero: nave baja blanca con portones azules, letrero y cajas de pescado ----------
 if(D.lonxa){const[x0,z0,y0,a,lw,lp]=D.lonxa,L=LOC(x0,z0,a),h=.045,ca=Math.cos(a),sa=Math.sin(a);
  caja(lw,h,lp,BLA,x0,y0-.004,z0,a,true);caja(lw+.006,.003,lp+.006,M(0x7d8792,{roughness:.6,metalness:.3}),x0,y0+h-.004,z0,a,true);
  for(let k=0;k<4;k++){const u=-lw/2+lw*(k+.5)/4;for(const s of[-1,1]){const[x,z]=L(u,s*(lp/2+.0006));caja(lw/4*.6,.028,.001,AZU,x,y0-.004,z,a)}}
  {const[x,z]=L(0,lp/2+.0012);caja(.07,.011,.001,AZU,x,y0+.031,z,a);
   // letras «LONXA» en blanco sobre el cartel
   const F={L:['100','100','100','100','111'],O:['111','101','101','101','111'],N:['1001','1101','1011','1001','1001'],X:['101','101','010','101','101'],A:['010','101','111','101','101']};
   const c=.0016;let u=-.026;for(const ch of'LONXA'){const g=F[ch];for(let r=0;r<5;r++)for(let i=0;i<g[r].length;i++)if(g[r][i]==='1'){const[xx,zz]=L(u+i*c,lp/2+.0019);caja(c,c,.0008,BLA,xx,y0+.0326+(4-r)*c,zz,a)}u+=g[0].length*c+c}}
  // pilas de cajas de pescado (azules y verdes) delante de los portones
  const CAZ=M(0x2d78c8,{roughness:.6}),CVE=M(0x2f9a6a,{roughness:.6});
  for(let k=0;k<(LT?4:9);k++){const u=(rn()-.5)*lw*.9,v=lp/2+.01+rn()*.02,n=1+(rn()*4|0),[x,z]=L(u,v);for(let j=0;j<n;j++)caja(.0075,.0028,.0055,rn()<.6?CAZ:CVE,x,y0+j*.0029,z,a+(rn()-.5)*.2)}}
 // ---------- 6) gamelas fondeadas en la dársena: se mecen por tandas ----------
 if(D.gamelas&&typeof BARC!=='undefined'&&BARC.casco){const PAL=[[0x2f6fb0,0xf2efe6],[0x2e8b57,0xf2efe6],[0xc8352b,0xf2efe6],[0xf2efe6,0x2f6fb0],[0xe9c234,0x2f6fb0],[0x1f4f8f,0xc8352b],[0xf2efe6,0x2e8b57],[0x7a3e9d,0xf2efe6]];
  const tmp=new THREE.Color();
  const aplana=(g,out)=>{g.updateMatrixWorld(true);g.traverse(o=>{if(!o.isMesh||(o.material&&(o.material.transparent||o.material.isMeshBasicMaterial)))return;let geo=o.geometry.index?o.geometry.toNonIndexed():o.geometry.clone();geo.applyMatrix4(o.matrixWorld);
   const p=geo.attributes.position,cc=geo.attributes.color,mc=o.material.color||tmp.set(0xffffff);for(let i=0;i<p.count;i++){out.p.push(p.getX(i),p.getY(i),p.getZ(i));if(cc)out.c.push(cc.getX(i)*mc.r,cc.getY(i)*mc.g,cc.getZ(i)*mc.b);else out.c.push(mc.r,mc.g,mc.b)}})};
  const barca=(tipo,ci)=>{const g=new THREE.Group(),[c1,c2]=PAL[ci%PAL.length],MM=BARC.mat;
   if(tipo===0){const cg=BARC.casco({L:.07,B:.026,H:.011,D:.005,NS:14,NU:5,fondo:'plano',popa:.58,arrufo:.008,arrufoPopa:.002,col:c1,banda:c2,obra:0x2f3b2e,flot:-.002,anchoBanda:.0028,franja:0xf2efe6});
    g.add(new THREE.Mesh(cg,MM(0xffffff,{vertexColors:true})));g.add(BARC.cubierta(cg,.03,.93,.0085,MM(0x9b7653)));for(const r of BARC.regala(cg,.0009,MM(0x6b4a2e),.985))g.add(r);
    const sec=cg.userData.sec;for(const t of[.3,.62]){const S=sec(t),b=new THREE.Mesh(new THREE.BoxGeometry(.007,.0014,S.w*1.85),MM(0x9b7653));b.position.set(-.035+t*.07,S.top-.004,0);g.add(b)}}
   else{const cg=BARC.casco({L:.085,B:.03,H:.013,D:.007,NS:14,NU:5,fondo:'v',popa:.82,arrufo:.008,col:c1,banda:c2,obra:0x3a2b2b,flot:-.003,anchoBanda:.004});
    g.add(new THREE.Mesh(cg,MM(0xffffff,{vertexColors:true})));g.add(BARC.cubierta(cg,.04,.97,.007,MM(0x9b7653)));
    const ca_=new THREE.Mesh(new THREE.BoxGeometry(.016,.012,.016),MM(0xf4f3ee));ca_.position.set(-.012,.017,0);g.add(ca_);   // caseta del pesquero de bajura
    const ma=new THREE.Mesh(new THREE.CylinderGeometry(.0007,.0009,.04,5),MM(0xd8dadc));ma.position.set(.008,.03,0);g.add(ma)}
   return g};
  const MAR_Y=-.03,lista=LT?D.gamelas.filter((b,i)=>i%2===0):D.gamelas,TRES=[{p:[],c:[]},{p:[],c:[]},{p:[],c:[]}],BOY=[];
  for(const[x,z,tipo,ci,a,s]of lista){const g=barca(tipo,ci);g.rotation.y=-a;g.position.set(x,0,z);aplana(g,TRES[Math.floor(s*3)%3]);BOY.push([x+Math.cos(a)*.055,z+Math.sin(a)*.055,ci])}
  const mB=M(0xffffff,{vertexColors:true,roughness:.55,side:THREE.DoubleSide}),mallas=[];
  TRES.forEach((T,k)=>{if(!T.p.length)return;// centradas en su tanda: el vaivén gira alrededor de la propia flota y no del origen del mapa (lejísimos)
   let cx=0,cz=0;for(let i=0;i<T.p.length;i+=3){cx+=T.p[i];cz+=T.p[i+2]}cx/=T.p.length/3;cz/=T.p.length/3;for(let i=0;i<T.p.length;i+=3){T.p[i]-=cx;T.p[i+2]-=cz}
   const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(T.p,3));g.setAttribute('color',new THREE.Float32BufferAttribute(T.c,3));g.computeVertexNormals();
   const mm=new THREE.Mesh(g,mB);mm.name='gamelas_baiona';mm.position.set(cx,MAR_Y,cz);mm.castShadow=!LT;mm.receiveShadow=true;mm.userData.fase=k*2.1;G.add(mm);mallas.push(mm)});
  for(const[x,z,ci]of BOY)pon(new THREE.SphereGeometry(.0045,10,8),ci%2?ROJ:M(0xff8a1e,{roughness:.6}),x,MAR_Y+.001,z);
  const t0_=performance.now();const meces=()=>{if(!mallas.length||!mallas[0].parent)return;const t=(performance.now()-t0_)/1000;
   for(const mm of mallas){const f=mm.userData.fase;mm.position.y=MAR_Y+Math.sin(t*1.3+f)*.0012;mm.rotation.z=Math.sin(t*.9+f)*.003;mm.rotation.x=Math.sin(t*1.1+f*1.7)*.0025}
   requestAnimationFrame(meces)};requestAnimationFrame(meces);BYN.gamelas=lista.length}
 // ---------- 7) la Carabela Pinta (réplica) atracada en el peirao central ----------
 if(D.carabela){const[x0,z0,a,yM,px,pz]=D.carabela,MAR_Y=-.03,Lc=.27,Bc=.08,Hc=.03,ca=Math.cos(a),sa=Math.sin(a);
  const CAR=new THREE.Group(),MAD3=M(0x6b4a2e,{roughness:.85}),MAD4=M(0x4a3220,{roughness:.9}),VEL=M(0xeee4cc,{roughness:.95,side:THREE.DoubleSide}),CRZ=M(0xb5221f,{roughness:.8,side:THREE.DoubleSide}),
   CUE=M(0x2a2420,{roughness:1}),ORO=M(0xc9a043,{roughness:.5,metalness:.5});
  const add=(geo,mat,x,y,z)=>{const o=new THREE.Mesh(geo,mat);o.position.set(x,y,z);CAR.add(o);return o};
  const cil=(A,Bv,r,mat,n=6)=>{const o=BARC&&BARC.cil?BARC.cil(A,Bv,r,mat,n):null;if(o)CAR.add(o)};
  // casco de madera: proa con arrufo alto y popa alta, línea de flotación oscura
  let sec=null;
  if(typeof BARC!=='undefined'&&BARC.casco){const cg=BARC.casco({L:Lc,B:Bc,H:Hc,D:.028,NS:22,NU:8,fondo:'redondo',popa:.78,arrufo:.016,arrufoPopa:.012,col:0x6b4a2e,banda:0x3d2a1b,obra:0x2a2018,flot:-.001,anchoBanda:.006,franja:0xc9a043});
   CAR.add(new THREE.Mesh(cg,M(0xffffff,{vertexColors:true,roughness:.85,side:THREE.DoubleSide})));CAR.add(BARC.cubierta(cg,.02,.96,.004,M(0xa58058,{roughness:.9})));
   for(const r of BARC.regala(cg,.0016,MAD4,.98))CAR.add(r);sec=cg.userData.sec}
  else{add(new THREE.BoxGeometry(Lc,Hc+.02,Bc),MAD3,0,Hc/2-.01,0);sec=()=>({w:Bc/2,top:Hc})}
  const xs=t=>-Lc/2+t*Lc,top=t=>sec(t).top,wd=t=>sec(t).w;
  // castillo de popa con la toldilla encima, barandilla y fanal
  {const u0=xs(0),u1=xs(.27),w=wd(.14)*2*.96,y=top(.14)-.002;add(new THREE.BoxGeometry(u1-u0,.016,w),MAD3,(u0+u1)/2,y+.008,0);add(new THREE.BoxGeometry(u1-u0+.002,.0016,w+.002),MAD4,(u0+u1)/2,y+.0168,0);
   const v0=xs(0),v1=xs(.12);add(new THREE.BoxGeometry(v1-v0,.011,w*.86),MAD3,(v0+v1)/2,y+.0225,0);add(new THREE.BoxGeometry(v1-v0+.002,.0014,w*.88),MAD4,(v0+v1)/2,y+.0287,0);
   for(let k=0;k<6;k++){const u=u1-.004-k*.012;for(const s of[-1,1])add(new THREE.BoxGeometry(.0012,.006,.0012),MAD4,u,y+.0198,s*w*.47)}
   add(new THREE.BoxGeometry(.0016,.0016,w*.94),MAD4,u1-.03,y+.0228,0);
   add(new THREE.CylinderGeometry(.0028,.0022,.007,6),ORO,v0+.004,y+.036,0);add(new THREE.CylinderGeometry(.0006,.0006,.008,4),NEG,v0+.004,y+.0305,0);
   // espejo de popa con ventanas
   for(const s of[-1,0,1])add(new THREE.BoxGeometry(.001,.004,.005),CUE,u0-.0004,y+.008,s*.012)}
  // castillo de proa, pequeño
  {const u0=xs(.8),u1=xs(.93),y=top(.86)-.002,w=wd(.86)*2*.92;add(new THREE.BoxGeometry(u1-u0,.008,w),MAD3,(u0+u1)/2,y+.004,0);add(new THREE.BoxGeometry(u1-u0+.002,.0014,w+.002),MAD4,(u0+u1)/2,y+.0085,0)}
  // portas y cintas a lo largo del casco
  for(let k=0;k<5;k++){const t=.32+k*.1;for(const s of[-1,1])add(new THREE.BoxGeometry(.006,.004,.001),CUE,xs(t),top(t)-.008,s*(wd(t)+.0004))}
  // palos: trinquete, mayor y mesana, con la cofa en el mayor
  const yD=top(.5)-.004,PAL=[[xs(.74),.17,.0018],[xs(.5),.22,.0022],[xs(.26),.15,.0016]];
  for(const[u,h,r]of PAL)add(new THREE.CylinderGeometry(r*.7,r,h,8),MAD4,u,yD+h/2,0);
  add(new THREE.CylinderGeometry(.0065,.005,.006,10),MAD3,xs(.5),yD+.16,0);
  // bauprés
  cil([xs(.96),top(.97)+.002,0],[xs(.96)+.06,top(.97)+.03,0],.0016,MAD4);
  // vergas y velas cuadras con la cruz roja (trinquete y mayor); vela latina en la mesana
  const cuadra=(u,yb,w,h)=>{add(new THREE.CylinderGeometry(.0011,.0011,w*1.1,6),MAD4,u+.002,yb+h,0).rotation.x=Math.PI/2;
   const g=new THREE.PlaneGeometry(w,h,6,4),p=g.attributes.position;for(let i=0;i<p.count;i++){const vx=p.getX(i),vy=p.getY(i);p.setZ(i,.009*(1-Math.pow(vx/(w/2),2))*(1-Math.pow(vy/(h/2),2)*.5))}
   g.computeVertexNormals();const o=add(g,VEL,u+.003,yb+h/2,0);o.rotation.y=Math.PI/2;
   const cz=new THREE.Mesh(new THREE.PlaneGeometry(w*.16,h*.62),CRZ),cx=new THREE.Mesh(new THREE.PlaneGeometry(w*.56,h*.15),CRZ);
   for(const c of[cz,cx]){c.position.set(u+.003+.0105,yb+h/2+(c===cx?h*.08:0),0);c.rotation.y=Math.PI/2;CAR.add(c)}};
  cuadra(PAL[0][0],yD+.07,.075,.06);cuadra(PAL[1][0],yD+.08,.1,.075);
  {const u=PAL[2][0],sh=new THREE.Shape();sh.moveTo(-.055,.03);sh.lineTo(.05,.135);sh.lineTo(.01,.035);sh.lineTo(-.055,.03);
   const g=new THREE.ShapeGeometry(sh);const o=add(g,VEL,u,yD,0);cil([u-.06,yD+.025,0],[u+.055,yD+.142,0],.001,MAD4)}
  // jarcia: obenques a las bordas y estays de proa a popa
  for(const[u,h]of[[PAL[0][0],.17],[PAL[1][0],.22],[PAL[2][0],.15]])for(const s of[-1,1])for(const d of[-.012,0,.012]){const t=(u+d+Lc/2)/Lc;cil([u,yD+h*.92,0],[u+d,top(t)+.001,s*wd(t)],.00035,NEG,3)}
  cil([xs(.96)+.058,top(.97)+.029,0],[PAL[0][0],yD+.168,0],.0004,NEG,3);cil([PAL[0][0],yD+.168,0],[PAL[1][0],yD+.215,0],.0004,NEG,3);cil([PAL[1][0],yD+.215,0],[PAL[2][0],yD+.148,0],.0004,NEG,3);
  // banderas en los topes y gallardete en popa
  for(const[u,h]of PAL){add(new THREE.BoxGeometry(.016,.009,.0006),ROJ,u-.008,yD+h-.004,0)}
  {const o=add(new THREE.PlaneGeometry(.022,.012),M(0xe9c234,{roughness:.8,side:THREE.DoubleSide}),xs(.02)-.012,top(0)+.05,0);cil([xs(.02),top(0)+.02,0],[xs(.02),top(0)+.058,0],.0007,MAD4)}
  // figura: el casco hacia la línea de flotación
  CAR.position.set(x0,MAR_Y,z0);CAR.rotation.y=-a;G.add(CAR);CAR.updateMatrixWorld(true);
  // el casco y los castillos chocan; el resto es decoración
  CAR.traverse(o=>{if(o.isMesh){o.castShadow=!LT;o.receiveShadow=true}});
  BYN.carabela=CAR;
  {const solido=new THREE.Mesh(new THREE.BoxGeometry(Lc*.92,Hc+.018,Bc*.9));solido.position.set(x0,MAR_Y+(Hc+.018)/2-.004,z0);solido.rotation.y=-a;solido.updateMatrixWorld(true);
   const g=solido.geometry.clone();g.applyMatrix4(solido.matrixWorld);const INV=new THREE.MeshBasicMaterial({visible:false});SOLID.set(INV,[g])}
  // pasarela de madera del costado al peirao
  {const yb=MAR_Y+top(.5),ym=Math.max(yM,yb-.03),sd=Math.sign((px-x0)*(-sa)+(pz-z0)*ca)||1,bx=x0+(-sa)*sd*wd(.45),bz=z0+ca*sd*wd(.45);
   const vx=px-bx,vz=pz-bz,l=Math.hypot(vx,vz),an=Math.atan2(vz,vx),g=new THREE.BoxGeometry(l,.0015,.012),p=g.attributes.position;
   for(let i=0;i<p.count;i++){const u=(p.getX(i)+l/2)/l;p.setY(i,p.getY(i)+yb*(1-u)+ym*u)}g.computeVertexNormals();pon(g,MAD,(bx+px)/2,0,(bz+pz)/2,an);
   for(const s of[-1,1]){const g2=new THREE.BoxGeometry(l,.0012,.0012),p2=g2.attributes.position;for(let i=0;i<p2.count;i++){const u=(p2.getX(i)+l/2)/l;p2.setY(i,p2.getY(i)+yb*(1-u)+ym*u+.008)}g2.translate(0,0,s*.0058);pon(g2,MAD4,(bx+px)/2,0,(bz+pz)/2,an)}}
  BYN.carabelaOk=1}
 // ---------- juntar por material ----------
 const junta=(P_,nombre,solido)=>{for(const[mat,gs]of P_){if(!gs.length)continue;const mm=new THREE.Mesh(mergeGeometries(gs),mat);mm.name=nombre;mm.castShadow=!LT&&mat!==LUZF&&mat.visible!==false;mm.receiveShadow=true;G.add(mm);if(solido)try{colaBVH(mm)}catch(e){}}};
 junta(PARTS,'piezas_baiona',false);
 root.add(G);junta(SOLID,'piezas_baiona_solidas',true);
 BYN.G=G;BYN.ms=Math.round(performance.now()-t0)}
// ---------- fin de baiona.js
