f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= PLAYA DE SAMIL =================
# Google Earth solo como referencia (no se copia nada): paseo marítimo con barandilla blanca, farolas y palmeras;
# complejo de piscinas detrás del paseo; en la arena sombrillas de colores, hamacas, torres de socorrista, redes de
# voley, duchas y pasarelas de madera hasta el agua; rocas en el islote frente a la playa. Todo se coloca siguiendo
# la línea de costa del mapa del juego. Modelos propios y genéricos.
r("function subeZonas(){psolChk();","function subeZonas(){psolChk();samChk();")
r("function subePaso(){",r"""const SAM={hecha:0,Y0:55.6,Y1:72.6};window.__SAM=SAM;
function samChk(){if(SAM.hecha||!MAPA||!MI)return;if(sueloRap(26.8,64)==null)return;SAM.hecha=1;setTimeout(()=>{try{samCrea()}catch(e){console.warn('samil',e);SAM.err=String(e)}},900)}
function samCrea(){const G=new THREE.Group();G.name='samil';const t=(x,y)=>cell(x,y).t,gy=(x,z)=>{const v=sueloRap(x,z);return v==null?groundY(x,z):v};
 // línea de costa (agua → tierra hacia el este) y borde de la arena
 const C=[];for(let y=SAM.Y0;y<=SAM.Y1;y+=.08){let xc=null;for(let x=12;x<34;x+=.02){if(t(x,y)!==0){xc=x;break}}if(xc==null)continue;C.push([xc,y,xc+.24])}
 for(let it=0;it<4;it++)for(let i=1;i<C.length-1;i++){C[i][0]=(C[i-1][0]+2*C[i][0]+C[i+1][0])/4;C[i][2]=(C[i-1][2]+2*C[i][2]+C[i+1][2])/4}
 SAM.C=C;const n=C.length;if(n<20)return;
 SAM.oc=0;const ocultar=dentro=>{const mm=new THREE.Matrix4(),pp=new THREE.Vector3(),q=new THREE.Quaternion(),sc=new THREE.Vector3(),inv=new THREE.Matrix4();
  scene.traverse(o=>{if(!o.isInstancedMesh||o.parent===G||o.count>5000)return;let ch=false;inv.copy(o.matrixWorld).invert();for(let k=0;k<o.count;k++){o.getMatrixAt(k,mm);mm.decompose(pp,q,sc);if(sc.x<=0)continue;const w=pp.clone().applyMatrix4(o.matrixWorld);if(dentro(w.x,w.z)){sc.setScalar(0);mm.compose(pp,q,sc);o.setMatrixAt(k,mm);ch=true;SAM.oc++}}if(ch)o.instanceMatrix.needsUpdate=true})};
 const yi=y=>Math.max(0,Math.min(n-1,Math.round((y-C[0][1])/.08)));
 ocultar((x,y)=>y>C[0][1]&&y<C[n-1][1]&&x>C[yi(y)][2]-.03&&x<C[yi(y)][2]+.11);
 const PA=[],du=new THREE.Object3D(),PARTS=new Map(),add=(geo,mat,x,y,z,ry=0,rx=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();g.deleteAttribute('uv');if(rx)g.rotateX(rx);g.rotateY(ry);g.translate(x,y,z);if(!PARTS.has(mat))PARTS.set(mat,[]);PARTS.get(mat).push(g)};
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.7},o));
 const BLA=M(0xf4f2ec),PIE=M(0xd9cfb8,{roughness:.9}),MAD=M(0x9a6b42,{roughness:.85}),HIE=M(0x2a2d33,{metalness:.5,roughness:.45}),LUZ=M(0xfff2cc,{emissive:0xffd88a,emissiveIntensity:.8}),
  PAL=M(0x7a5a3a),HOJ=M(0x3f8a3a),ROJ=M(0xd83a2e),AMA=M(0xf2c230),AZU=M(0x2f7fd6),VER=M(0x2fae6a),NAR=M(0xf28a2e),AGUA=new THREE.MeshStandardMaterial({color:0x37c6e6,roughness:.15,metalness:.1,emissive:0x0a4d66,emissiveIntensity:.35}),
  BAL=M(0xd8f0ff,{roughness:.3}),ROCA=M(0x8a8478,{roughness:.95}),RED=M(0xeeeeee,{roughness:.6});
 const cil=(a,b,h,s=8)=>new THREE.CylinderGeometry(a,b,h,s),cub=(a,b,c)=>new THREE.BoxGeometry(a,b,c);
 const tang=i=>{const a=C[Math.max(0,i-3)],b=C[Math.min(n-1,i+3)];const dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy)||1;return[dx/l,dy/l]};
 // paseo marítimo: franja de losas claras, bordillo, barandilla blanca hacia la arena, farolas y palmeras
 {const W=.085,pos=[],idx=[];for(let i=0;i<n;i++){const[xc,y,xe]=C[i],[tx,ty]=tang(i),nx=ty,ny=-tx;const s_=nx<0?-1:1;const ix=xe-.015,ox=ix+W;
   const a=[ix,y],b=[ox,y];pos.push(a[0],gy(a[0],a[1])+.006,a[1],b[0],gy(b[0],b[1])+.006,b[1]);if(i<n-1){const k=i*2;idx.push(k,k+2,k+1,k+1,k+2,k+3)}}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:0xe8e0cf,roughness:.85,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2}));m.receiveShadow=true;G.add(m);
  for(let i=0;i<n;i+=1){const[xc,y,xe]=C[i],x=xe-.015,z=gy(x,y);if(i%2===0)add(cil(.0012,.0012,.012,6),BLA,x,z+.006,y);if(i<n-1){const[x2,y2,xe2]=C[i+1];const xx=xe2-.015,dl=Math.hypot(xx-x,y2-y),a_=Math.atan2(-(y2-y),xx-x);add(cub(dl,.0018,.0022),BLA,(x+xx)/2,z+.012,(y+y2)/2,a_);add(cub(dl,.003,.0035),PIE,(x+xx)/2,z+.0015,(y+y2)/2,a_)}
   if(i%5===0){const lx=xe+W*.55;const lz=gy(lx,y);add(cil(.001,.0014,.05,6),HIE,lx,lz+.025,y);add(cub(.006,.008,.006),LUZ,lx,lz+.054,y);add(new THREE.ConeGeometry(.005,.004,4),HIE,lx,lz+.06,y,Math.PI/4)}
   if(i%5===2){const px=xe+W*.7,pz=gy(px,y),h=.07+.015*Math.sin(i);add(cil(.0018,.0026,h,6),PAL,px,pz+h/2,y);for(let k=0;k<7;k++){const a=k/7*6.283;const hg=new THREE.BoxGeometry(.03,.0012,.007);hg.translate(.015,0,0);hg.rotateZ(-.45);add(hg,HOJ,px,pz+h,y,a)}}}}
 // arena: sombrillas, hamacas, torres de socorrista, voley, duchas, pasarelas
 const COL=[ROJ,AMA,AZU,VER,NAR];let rs=11;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 for(let i=2;i<n-2;i++){const[xc,y,xe]=C[i],ancho=xe-xc;
  if(i%13===6){// pasarela de madera hasta el agua
   for(let x=xe-.02;x>xc+.03;x-=.012)add(cub(.011,.0015,.022),MAD,x,gy(x,y)+.0018,y)}
  if(i%40===20){// torre de socorrista
   const x=xc+ancho*.45,z=gy(x,y);for(const[a,b]of[[-1,-1],[1,-1],[1,1],[-1,1]])add(cil(.0009,.0009,.045,5),BLA,x+a*.007,z+.0225,y+b*.007);add(cub(.018,.002,.018),MAD,x,z+.045,y);add(cub(.016,.012,.0015),ROJ,x+.008,z+.052,y);add(cub(.0015,.012,.016),ROJ,x,z+.052,y-.008);add(cub(.022,.002,.022),ROJ,x,z+.066,y);add(cil(.0006,.0006,.018,4),BLA,x,z+.056,y);
   for(let k=0;k<6;k++)add(cub(.0035,.001,.012),BLA,x+.012+k*.005,z+.0045+k*.0075*.95,y,0,0)}
  if(i%55===30){// red de voley
   const x=xc+ancho*.62,z=gy(x,y);add(cil(.0008,.0008,.03,5),BLA,x,z+.015,y-.045);add(cil(.0008,.0008,.03,5),BLA,x,z+.015,y+.045);add(cub(.0008,.01,.09),RED,x,z+.024,y)}
  if(i%26===10){// ducha
   const x=xe-.03,z=gy(x,y);add(cil(.0009,.0009,.035,5),HIE,x,z+.0175,y);add(cub(.008,.0012,.002),HIE,x+.003,z+.035,y);add(cub(.012,.0008,.012),PIE,x,z+.0006,y)}
  // sombrillas y hamacas en grupos
  if(i%3===0&&ancho>.12)for(let k=0;k<2;k++){if(rn()<.35)continue;const x=xc+.05+rn()*(ancho-.1),yy=y+(rn()-.5)*.06,z=gy(x,yy),cm=COL[(rn()*5)|0];
   add(cil(.0006,.0006,.028,4),BLA,x,z+.014,yy);const cono=new THREE.ConeGeometry(.02,.008,8,1,true);add(cono,cm,x,z+.03,yy);
   if(rn()<.7){add(cub(.008,.0015,.02),rn()<.5?BLA:AZU,x+.014,z+.003,yy);add(cub(.008,.0015,.02),rn()<.5?BLA:AMA,x-.014,z+.003,yy)}}}
 // complejo de piscinas detrás del paseo (zona central de la playa)
 {const i0=Math.round(n*.38),[xc,y0,xe]=C[i0],X=xe+.13,Y=y0;const z=gy(X+.2,Y);SAM.pisc=[X,Y];
  add(cub(.46,.012,.3),BLA,X+.23,z+.003,Y);
  const pis=(px,py,w,l)=>{add(cub(w+.012,.008,l+.012),PIE,px,z+.012,py);const m=new THREE.Mesh(new THREE.BoxGeometry(w,.002,l),AGUA);m.position.set(px,z+.0165,py);G.add(m)};
  pis(X+.12,Y-.07,.16,.09);pis(X+.32,Y-.06,.14,.1);pis(X+.2,Y+.08,.24,.08);
  // tobogán y caseta
  add(cub(.05,.03,.04),BLA,X+.41,z+.024,Y+.1);add(cub(.052,.004,.042),AZU,X+.41,z+.04,Y+.1);
  for(let k=0;k<10;k++){const a=k/10*Math.PI*1.4;add(cub(.012,.003,.008),AMA,X+.37+Math.cos(a)*.02,z+.045-k*.0028,Y+.1+Math.sin(a)*.02,-a)}
  for(let k=0;k<8;k++){const x=X+.06+k*.05;add(cub(.008,.0015,.02),k%2?BLA:AZU,x,z+.011,Y+.135)}
  ocultar((x,y)=>x>X-.03&&x<X+.5&&y>Y-.18&&y<Y+.18)}
 // islote de rocas frente a la playa
 {const[xc,y]=C[Math.round(n*.55)];const X=xc-.55;for(let k=0;k<9;k++){const r_=.03+rn()*.05,g=new THREE.DodecahedronGeometry(r_,0);g.scale(1,.55,1);add(g,ROCA,X+(rn()-.5)*.18,.005+r_*.2,y+(rn()-.5)*.14,rn()*6)}}
 for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=mat!==LUZ;m.receiveShadow=true;G.add(m)}
 scene.add(G);SAM.G=G;SAM.n=n}
function subePaso(){""")
open(f,'w').write(s)
print('ok samil')
