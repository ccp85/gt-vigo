f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MONTE DO CASTRO =================
# Fotos y Google Earth solo como referencia (no se copia nada): fortaleza abaluartada de granito en lo alto del monte
# (recinto alto en estrella y recinto bajo), garitas en las puntas de los baluartes, cañones, jardines de setos y caminos
# de tierra por dentro, mirador norte con anclas antiguas, estanque de patos, poblado castreño de casas redondas con
# techo de paja y pinar en las laderas. Modelos propios y genéricos. Deja huecos (puertas) donde pasa la bajada en skate.
r("function subeZonas(){psolChk();samChk();casChk();","function subeZonas(){psolChk();samChk();casChk();cstChk();")
r("function subePaso(){",r"""const CST={hecha:0,
 U:[[86.18,25.97],[86.4,26.17],[86.37,26.36],[86.37,27.1],[86.45,27.2],[86.6,27.5],[86.86,27.71],[86.68,27.84],[86.52,27.87],[86.28,28.26],[86.15,28.54],[86.0,28.41],[85.77,28.38],[85.53,27.84],[85.7,27.32],[85.86,27.15],[85.92,26.95],[85.86,26.82],[85.95,26.6],[85.97,26.3],[86.03,26.18]],
 L:[[85.53,27.84],[85.0,28.63],[85.2,28.68],[85.74,29.58],[85.97,29.57],[86.25,28.97],[86.88,28.92],[87.28,28.72],[86.68,27.84]]};window.__CST=CST;
function cstChk(){if(CST.G&&performance.now()-(CST.t||0)>2500){CST.t=performance.now();try{cstViejos();cstPiezas()}catch(e){}}if(CST.hecha||!MAPA||!MI)return;if(sueloRap(86.2,27.6)==null||sueloRap(85.4,28.8)==null||sueloRap(86.9,26.6)==null)return;CST.hecha=1;setTimeout(()=>{try{cstCrea()}catch(e){console.warn('castro',e);CST.err=String(e)}},1300)}
// murallas finas del catastro: se aplanan para poner encima las de granito
function cstViejos(){const v=new THREE.Vector3(),W=[];const Pu=CST.U,Pl=CST.L;for(let i=0;i<Pu.length;i++)W.push([Pu[i],Pu[(i+1)%Pu.length]]);for(let i=0;i<Pl.length-1;i++)W.push([Pl[i],Pl[i+1]]);
 const dW=(x,y)=>{let d=9;for(const[a,b]of W){const dx=b[0]-a[0],dy=b[1]-a[1],l=dx*dx+dy*dy;let u=((x-a[0])*dx+(y-a[1])*dy)/l;u=Math.max(0,Math.min(1,u));d=Math.min(d,Math.hypot(a[0]+dx*u-x,a[1]+dy*u-y))}return d};
 const ms=new Map();for(const[a,b]of W){const L=Math.hypot(b[0]-a[0],b[1]-a[1]);for(let u=0;u<=1;u+=.1/L)for(const m of repMallas(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u))ms.set(m.uuid,m)}
 for(const m of ms.values()){const g=m.geometry;if(g.userData.cstV||!g.index)continue;g.userData.cstV=1;const pa=g.attributes.position,ix=g.index;let c=0;
  for(let t=0;t<ix.count/3;t++){let ok=true;for(let k=0;k<3;k++){v.fromBufferAttribute(pa,ix.getX(t*3+k)).applyMatrix4(m.matrixWorld);if(v.x<84.8||v.x>87.5||v.z<25.8||v.z>29.8||dW(v.x,v.z)>.034){ok=false;break}}
   if(ok){const a=ix.getX(t*3);ix.setX(t*3+1,a);ix.setX(t*3+2,a);c++}}
  if(c){ix.needsUpdate=true;CST.viejos=(CST.viejos||0)+c}}}
function cstPiezas(){const H={piezas_89:1,piezas_90:1,piezas_91:1,piezas_92:1,piezas_93:1,piezas_94:1,piezas_101:1,piezas_102:1,piezas_103:1,piezas_104:1};let n=0;
 for(const r of scene.children){if(r.name!=='centro')continue;r.traverse(o=>{if(!o.isMesh||!H[o.name]||!o.visible)return;if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();const b=o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld);
  if(b.min.x>84.9&&b.max.x<87.4&&b.min.z>25.9&&b.max.z<29.7){o.visible=false;n++}})}if(n)CST.piezas=(CST.piezas||0)+n}
function cstCrea(){const G=new THREE.Group();G.name='monteCastro';const t=(x,y)=>cell(x,y).t,gy=(x,z)=>{const v=sueloRap(x,z);return v==null?groundY(x,z):v};const LT=!!window.LITE;
 let rs=29;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.85},o));
 const SILL=(()=>{const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');x.fillStyle='#8f877a';x.fillRect(0,0,256,256);let s_=5;const r_=()=>(s_=(s_*16807)%2147483647)/2147483647;
  for(let j=0;j<8;j++){let i=-r_()*40;while(i<256){const w=34+r_()*30,l=150+r_()*55|0;x.fillStyle=`rgb(${l+8},${l+2},${l-8})`;x.fillRect(i+1.5,j*32+1.5,w-3,29);for(let k=0;k<14;k++){const g=l-20+r_()*40|0;x.fillStyle=`rgba(${g},${g},${g-6},.35)`;x.fillRect(i+2+r_()*(w-6),j*32+2+r_()*26,2+r_()*4,2+r_()*3)}i+=w}}
  const t_=new THREE.CanvasTexture(c);t_.wrapS=t_.wrapT=THREE.RepeatWrapping;t_.colorSpace=THREE.SRGBColorSpace;t_.anisotropy=4;return t_})();
 const GRA=M(0xffffff,{roughness:.95,map:SILL}),GRA2=M(0xd8d2c6,{roughness:1,map:SILL}),GRAC=M(0xbdb5a5,{roughness:.9}),HIE=M(0x2a2d33,{metalness:.55,roughness:.4}),HIEV=M(0x3b3f45,{metalness:.6,roughness:.5}),
  LUZ=M(0xfff2cc,{emissive:0xffd88a,emissiveIntensity:.9}),MAD=M(0x7a5232),SETO=M(0x2f6b2c,{roughness:1}),FLO=M(0xe2577e),FLO2=M(0xf4c542),PAJA=M(0xb89a5a,{roughness:1,flatShading:true}),
  PIEC=M(0x9a8f7c,{roughness:1,flatShading:true}),AGUA=new THREE.MeshStandardMaterial({color:0x4fb8c9,roughness:.12,metalness:.1,emissive:0x0a4050,emissiveIntensity:.3}),BLA=M(0xf3f1ea),NAR=M(0xf0a030),
  TIE=new THREE.MeshStandardMaterial({color:0xcdb689,roughness:1,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2});
 const PARTS=new Map(),add=(geo,mat,x,y,z,ry=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();if(g.attributes.uv)g.deleteAttribute('uv');g.rotateY(ry);g.translate(x,y,z);if(!PARTS.has(mat))PARTS.set(mat,[]);PARTS.get(mat).push(g)};
 const RAW=new Map(),UVS=new Map(),quad=(mat,a,b,c,d,uv)=>{if(!RAW.has(mat)){RAW.set(mat,[]);UVS.set(mat,[])}RAW.get(mat).push(...a,...b,...c,...a,...c,...d);const U=uv||[0,0,1,0,1,1,0,1];UVS.get(mat).push(U[0],U[1],U[2],U[3],U[4],U[5],U[0],U[1],U[4],U[5],U[6],U[7])};
 const cil=(a,b,h,s=8)=>new THREE.CylinderGeometry(a,b,h,s),cub=(a,b,c)=>new THREE.BoxGeometry(a,b,c);
 const dentroP=(P,x,y)=>{let c=false;for(let i=0,j=P.length-1;i<P.length;j=i++){const[xi,yi]=P[i],[xj,yj]=P[j];if((yi>y)!==(yj>y)&&x<(xj-xi)*(y-yi)/(yj-yi)+xi)c=!c}return c};
 const dSeg=(x,y,a,b)=>{const dx=b[0]-a[0],dy=b[1]-a[1],l=dx*dx+dy*dy||1;let u=((x-a[0])*dx+(y-a[1])*dy)/l;u=Math.max(0,Math.min(1,u));return Math.hypot(a[0]+dx*u-x,a[1]+dy*u-y)};
 const dPol=(P,x,y)=>{let d=9;for(let i=0;i<P.length;i++)d=Math.min(d,dSeg(x,y,P[i],P[(i+1)%P.length]));return d};
 const enFuerte=(x,y)=>dentroP(CST.U,x,y)||dentroP(CST.L,x,y),dMuro=(x,y)=>Math.min(dPol(CST.U,x,y),dPol(CST.L,x,y));
 const libre=(x,y,r=.03)=>{for(const[a,b]of[[0,0],[r,0],[-r,0],[0,r],[0,-r]]){const q=t(x+a,y+b);if(q!==1)return false}return true};
 // ruta de la bajada en skate: por ahí no se pone nada y las murallas tienen puerta
 let RU=[];try{const R=skcRuta();if(R)RU=R.filter(p=>p[0]>84.4&&p[0]<88&&p[1]>25.4&&p[1]<30)}catch(e){}
 CST.ru=RU.length;const dRu=(x,y)=>{let d=9;for(let i=0;i<RU.length-1;i++)d=Math.min(d,dSeg(x,y,RU[i],RU[i+1]));if(RU.length===1)d=Math.hypot(RU[0][0]-x,RU[0][1]-y);return d};
 const ocultar=dentro=>{const mm=new THREE.Matrix4(),pp=new THREE.Vector3(),q=new THREE.Quaternion(),sc=new THREE.Vector3();let n=0;
  scene.traverse(o=>{if(!o.isInstancedMesh||o.userData.cst||o.userData.cas||o.count>5000)return;let ch=false;for(let k=0;k<o.count;k++){o.getMatrixAt(k,mm);mm.decompose(pp,q,sc);if(sc.x<=0)continue;const w=pp.clone().applyMatrix4(o.matrixWorld);if(dentro(w.x,w.z)){sc.setScalar(0);mm.compose(pp,q,sc);o.setMatrixAt(k,mm);ch=true;n++}}if(ch)o.instanceMatrix.needsUpdate=true});return n};
 // 1) murallas de granito con talud, adarve y pretil; puertas donde cruza la bajada
 let LAC=0;const muro=(P,cerrado,skip)=>{const n=P.length;let cx=0,cy=0;for(const p of P){cx+=p[0];cy+=p[1]}cx/=n;cy/=n;
  for(let i=0;i<(cerrado?n:n-1);i++){if(skip&&skip(i))continue;const a=P[i],b=P[(i+1)%n],L=Math.hypot(b[0]-a[0],b[1]-a[1]),ns=Math.max(2,Math.ceil(L/.025));let tx=(b[0]-a[0])/L,ty=(b[1]-a[1])/L;let nx=ty,ny=-tx;
   if(dentroP(P,(a[0]+b[0])/2+nx*.02,(a[1]+b[1])/2+ny*.02)){nx=-nx;ny=-ny}// normal hacia fuera
   const S=[];for(let k=0;k<=ns;k++){const u=k/ns,x=a[0]+(b[0]-a[0])*u,y=a[1]+(b[1]-a[1])*u;const pu=dRu(x,y)<.1;const ul=(LAC+u*L)*14;
    const go=gy(x+nx*.03,y+ny*.03),gi=gy(x-nx*.03,y-ny*.03),top=Math.max(gi+.036,go+.1);S.push({x,y,go,gi,top,pu,ul})}LAC+=L;
   for(let k=0;k<ns;k++){const A=S[k],B=S[k+1];if(A.pu||B.pu)continue;const T=.026,TL=.014;
    const o=(p,d,h)=>[p.x+nx*d,h,p.y+ny*d];
    const V=h=>h*14;quad(GRA,o(A,TL,A.go-.02),o(B,TL,B.go-.02),o(B,0,B.top),o(A,0,A.top),[A.ul,V(A.go-.02),B.ul,V(B.go-.02),B.ul,V(B.top),A.ul,V(A.top)]);// cara exterior en talud
    quad(GRAC,o(A,0,A.top),o(B,0,B.top),o(B,-T,B.top),o(A,-T,A.top));// adarve
    quad(GRA2,o(A,-T,A.top),o(B,-T,B.top),o(B,-T,B.gi-.02),o(A,-T,A.gi-.02),[A.ul,V(A.top),B.ul,V(B.top),B.ul,V(B.gi-.02),A.ul,V(A.gi-.02)]);// cara interior
    quad(GRA,o(A,.002,A.top),o(B,.002,B.top),o(B,.002,B.top+.012),o(A,.002,A.top+.012),[A.ul,V(A.top),B.ul,V(B.top),B.ul,V(B.top+.012),A.ul,V(A.top+.012)]);quad(GRA,o(A,-.004,A.top+.012),o(B,-.004,B.top+.012),o(B,-.004,B.top),o(A,-.004,A.top),[A.ul,V(A.top+.012),B.ul,V(B.top+.012),B.ul,V(B.top),A.ul,V(A.top)]);quad(GRAC,o(A,.002,A.top+.012),o(B,.002,B.top+.012),o(B,-.004,B.top+.012),o(A,-.004,A.top+.012));// pretil
    if(k===0||k===ns-1){}
   }
   // remate en las puertas: pilastras
   for(let k=1;k<S.length;k++){if(S[k].pu!==S[k-1].pu){const p=S[k].pu?S[k-1]:S[k];add(cub(.03,p.top-p.go+.05,.03),GRA2,p.x-nx*.012,(p.top+p.go)/2+.01,p.y-ny*.012);add(new THREE.SphereGeometry(.009,8,6),GRAC,p.x-nx*.012,p.top+.045,p.y-ny*.012);CST.puertas=(CST.puertas||0)+1}}}
  return[cx,cy]};
 cstViejos();cstPiezas();muro(CST.U,true);muro(CST.L,false);
 // 2) garitas en las puntas de los baluartes
 const garita=(x,y,ang)=>{const z=gy(x,y);let top=-9;for(const[a,b]of[[0,0],[.02,0],[-.02,0],[0,.02],[0,-.02]])top=Math.max(top,gy(x+a,y+b));top=Math.max(top+.036,z+.1);
  add(cil(.016,.012,.02,10),GRA,x,top-.004,y);add(cil(.013,.013,.03,10),GRAC,x,top+.02,y);add(new THREE.SphereGeometry(.0145,10,6,0,6.283,0,Math.PI/2),GRA,x,top+.035,y);add(new THREE.ConeGeometry(.004,.012,6),GRA2,x,top+.05,y);
  add(cub(.006,.012,.004),HIE,x+Math.cos(ang)*.013,top+.022,y+Math.sin(ang)*.013,-ang+Math.PI/2)};
 for(const P of[CST.U,CST.L]){for(let i=0;i<P.length;i++){const p=P[i],a=P[(i+P.length-1)%P.length],b=P[(i+1)%P.length];const v1=[a[0]-p[0],a[1]-p[1]],v2=[b[0]-p[0],b[1]-p[1]];const cr=v1[0]*v2[1]-v1[1]*v2[0],dt=v1[0]*v2[0]+v1[1]*v2[1];const ang=Math.abs(Math.atan2(cr,dt));
   if(ang<1.75&&!dentroP(P,p[0]-(v1[0]+v2[0])*.1,p[1]-(v1[1]+v2[1])*.1)&&dRu(p[0],p[1])>.12){const ox=-(v1[0]/Math.hypot(...v1)+v2[0]/Math.hypot(...v2)),oy=-(v1[1]/Math.hypot(...v1)+v2[1]/Math.hypot(...v2)),l=Math.hypot(ox,oy)||1;
    garita(p[0]+ox/l*.004,p[1]+oy/l*.004,Math.atan2(oy,ox));CST.garitas=(CST.garitas||0)+1}}}
 // 3) caminos de tierra por dentro: los senderos reales del mapa (RUTAS peatonales) dentro del recinto
 let nCam=0;const tramo=(pts,w)=>{if(pts.length<2)return;const pos=[],idx=[];for(let i=0;i<pts.length;i++){const a=pts[Math.max(0,i-1)],b=pts[Math.min(pts.length-1,i+1)];let dx=b[0]-a[0],dy=b[1]-a[1];const l=Math.hypot(dx,dy)||1;const nx=-dy/l*w/2,ny=dx/l*w/2,[x,y]=pts[i];
   pos.push(x+nx,gy(x+nx,y+ny)+.004,y+ny,x-nx,gy(x-nx,y-ny)+.004,y-ny);if(i<pts.length-1){const k=i*2;idx.push(k,k+1,k+2,k+1,k+3,k+2)}}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();const m=new THREE.Mesh(g,TIE);m.receiveShadow=true;G.add(m);nCam++};
 const CAMS=[];if(typeof RUTAS!=='undefined'&&RUTAS)for(const ru of RUTAS){if(!ru.p||ru.p.length<2)continue;if(!(ru.c==='P'||ru.c==='T'||ru.c==='S'))continue;
  let cur=[];const den=[];for(let i=0;i<ru.p.length-1;i++){const a=ru.p[i],b=ru.p[i+1],L=Math.hypot(b[0]-a[0],b[1]-a[1]),ns=Math.max(1,Math.ceil(L/.03));for(let k=0;k<ns;k++){const u=k/ns;den.push([a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u])}}den.push(ru.p[ru.p.length-1]);
  for(const p of den){const ok=p[0]>84.5&&p[0]<87.8&&p[1]>25.5&&p[1]<29.5&&(enFuerte(p[0],p[1])||dMuro(p[0],p[1])<.35)&&t(p[0],p[1])!==2;if(ok)cur.push(p);else{if(cur.length>1){CAMS.push(cur)}cur=[]}}if(cur.length>1)CAMS.push(cur)}
 {const Lc=CST.L.concat([[86.52,27.87],[86.28,28.26],[86.15,28.54],[86.0,28.41],[85.77,28.38]]);for(const P of[CST.U,Lc]){for(let i=0;i<P.length;i++){const a=P[i],b=P[(i+1)%P.length],L=Math.hypot(b[0]-a[0],b[1]-a[1]);if(L<.12)continue;let nx=(b[1]-a[1])/L,ny=-(b[0]-a[0])/L;const mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2;if(!dentroP(P,mx+nx*.05,my+ny*.05)){nx=-nx;ny=-ny}
   const pts=[];for(let u=.07;u<=L-.07;u+=.03){const x=a[0]+(b[0]-a[0])*u/L+nx*.06,y=a[1]+(b[1]-a[1])*u/L+ny*.06;if(dentroP(P,x,y)&&dRu(x,y)>.06&&t(x,y)!==3)pts.push([x,y]);else{if(pts.length>2)CAMS.push(pts.splice(0));pts.length=0}}if(pts.length>2)CAMS.push(pts)}}
  const eje=[[86.19,26.43],[86.17,26.8],[86.18,27.2],[86.2,27.48],[86.2,27.92],[86.14,28.36]],E=[];for(let i=0;i<eje.length-1;i++){const a=eje[i],b=eje[i+1];for(let u=0;u<1;u+=.1)E.push([a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u])}E.push(eje[eje.length-1]);
  let cur=[];for(const p of E){if(t(p[0],p[1])!==3&&Math.hypot(p[0]-86.2,p[1]-27.7)>.05)cur.push(p);else{if(cur.length>1)CAMS.push(cur);cur=[]}}if(cur.length>1)CAMS.push(cur)}
 for(const c of CAMS)tramo(c,.035);CST.cams=nCam;
 const dCam=(x,y)=>{let d=9;for(const c of CAMS)for(const p of c){const e=Math.hypot(p[0]-x,p[1]-y);if(e<d)d=e}return d};
 // 4) mirador norte con anclas antiguas y barandilla
 {const mx=86.19,my=26.32,z=gy(mx,my);add(cil(.1,.1,.01,28),GRAC,mx,z+.002,my);add(cil(.102,.102,.004,28),GRA2,mx,z-.002,my);
  for(let k=0;k<=14;k++){const a=Math.PI*1.05+k/14*Math.PI*.9,x=mx+Math.cos(a)*.095,y=my+Math.sin(a)*.095;add(cil(.0012,.0012,.018,5),HIE,x,z+.012,y);if(k<14){const a2=Math.PI*1.05+(k+1)/14*Math.PI*.9,x2=mx+Math.cos(a2)*.095,y2=my+Math.sin(a2)*.095,dl=Math.hypot(x2-x,y2-y);add(cub(dl,.0018,.0018),HIE,(x+x2)/2,z+.021,(y+y2)/2,-Math.atan2(y2-y,x2-x))}}
  const ancla=(x,y,s,ry)=>{const zz=gy(x,y);add(cub(.03*s,.008,.03*s),GRA2,x,zz+.006,y,ry);const h=.075*s;add(cub(.006*s,h,.006*s),HIEV,x,zz+.01+h/2,y,ry);add(cub(.04*s,.005*s,.006*s),HIEV,x,zz+.01+h*.86,y,ry);add(new THREE.TorusGeometry(.007*s,.0018*s,6,12),HIEV,x,zz+.01+h+.006*s,y,ry);
   const ar=new THREE.TorusGeometry(.024*s,.0035*s,6,16,Math.PI);ar.rotateZ(Math.PI);add(ar,HIEV,x,zz+.01+.026*s,y,ry);for(const sd of[-1,1]){const pu=new THREE.ConeGeometry(.0055*s,.012*s,4);pu.rotateZ(sd*.6);add(pu,HIEV,x+Math.cos(-ry)*sd*.024*s,zz+.01+.03*s,y+Math.sin(-ry)*sd*.024*s,ry)}};
  ancla(mx-.05,my+.02,1,.3);ancla(mx,my-.03,1.15,0);ancla(mx+.05,my+.02,1,-.3);
  for(const[a,b]of[[-.07,.06],[.07,.06]]){add(cub(.03,.0025,.008),MAD,mx+a,z+.009,my+b);add(cub(.03,.007,.0015),MAD,mx+a,z+.013,my+b+.004)}
  CST.mirador=[mx,my]}
 // 5) jardín de setos con parterres y flores en el recinto alto
 {const J=[86.2,27.7];const pts=[];let nj=0;for(let x=J[0]-.24;x<=J[0]+.24;x+=.02)for(let y=J[1]-.2;y<=J[1]+.2;y+=.02){if(!dentroP(CST.U,x,y)||dMuro(x,y)<.07||t(x,y)!==1||dRu(x,y)<.09||dCam(x,y)<.025)continue;const z=gy(x,y),u=(x-J[0])/.24,w=(y-J[1])/.2;
   const borde=Math.abs(Math.abs(u)-.95)<.06||Math.abs(Math.abs(w)-.95)<.07,diag=Math.abs(Math.abs(u)-Math.abs(w))<.08,circ=Math.abs(Math.hypot(u,w)-.45)<.06;
   if(Math.hypot(u,w)<.12){continue}
   if(borde||circ)add(cub(.019,.011,.019),SETO,x,z+.006,y);else if(diag)add(cub(.02,.002,.02),GRAC,x,z+.002,y);else if((Math.round(x/.02)+Math.round(y/.02))%3===0)add(new THREE.IcosahedronGeometry(.005,0),rn()<.5?FLO:FLO2,x,z+.006,y);nj++}
  const z=gy(J[0],J[1]);add(cil(.035,.038,.012,20),GRA2,J[0],z+.006,J[1]);const ag=new THREE.Mesh(cil(.03,.03,.002,20),AGUA);ag.position.set(J[0],z+.012,J[1]);G.add(ag);add(cil(.005,.007,.03,8),GRAC,J[0],z+.025,J[1]);add(cil(.013,.009,.004,12),GRAC,J[0],z+.04,J[1]);CST.jardin=nj}
 // 6) cañones sobre el adarve mirando a la ría
 {let nc=0;const P=CST.U;for(let i=0;i<P.length&&nc<8;i++){const a=P[i],b=P[(i+1)%P.length];for(const u of[.35,.7]){const x=a[0]+(b[0]-a[0])*u,y=a[1]+(b[1]-a[1])*u;if(dRu(x,y)<.15)continue;const L=Math.hypot(b[0]-a[0],b[1]-a[1]);let nx=(b[1]-a[1])/L,ny=-(b[0]-a[0])/L;if(dentroP(P,x+nx*.03,y+ny*.03)){nx=-nx;ny=-ny}
   const ix=x-nx*.04,iy=y-ny*.04,z=gy(ix,iy),ang=Math.atan2(ny,nx);add(cub(.022,.008,.014),MAD,ix,z+.006,iy,-ang);for(const sd of[-1,1])add(cil(.006,.006,.002,10).rotateX(Math.PI/2),HIE,ix+Math.cos(ang+Math.PI/2)*sd*.009,z+.006,iy+Math.sin(ang+Math.PI/2)*sd*.009,-ang+Math.PI/2);
   const c=cil(.0035,.005,.04,8);c.rotateZ(-Math.PI/2+.15);add(c,HIE,ix+nx*.012,z+.015,iy+ny*.012,-ang);nc++}}CST.canones=nc}
 // 7) recinto bajo: pradera redonda con parterre de flores y farolas
 {const c=[85.68,28.95];if(t(...c)===1){const z=gy(...c);for(let k=0;k<36;k++){const a=k/36*6.283;add(new THREE.IcosahedronGeometry(.007,0),k%2?FLO:FLO2,c[0]+Math.cos(a)*.1,gy(c[0]+Math.cos(a)*.1,c[1]+Math.sin(a)*.1)+.006,c[1]+Math.sin(a)*.1)}
  add(cil(.02,.025,.012,12),GRAC,c[0],z+.006,c[1]);add(new THREE.SphereGeometry(.014,10,8),SETO,c[0],z+.022,c[1]);CST.pradera=c}}
 // farolas a lo largo de los caminos interiores
 {let nf=0;const LP=[];{const P=CST.U;for(let i=0;i<P.length;i++){const a=P[i],b=P[(i+1)%P.length],L=Math.hypot(b[0]-a[0],b[1]-a[1]);for(let u=.12;u<L-.05;u+=.28){const x=a[0]+(b[0]-a[0])*u/L,y=a[1]+(b[1]-a[1])*u/L;let nx=(b[1]-a[1])/L,ny=-(b[0]-a[0])/L;if(!dentroP(P,x+nx*.05,y+ny*.05)){nx=-nx;ny=-ny}LP.push([[x+nx*.07,y+ny*.07],[x+nx*.07+(b[0]-a[0])/L*.01,y+ny*.07+(b[1]-a[1])/L*.01]])}}}for(const cm of CAMS)for(let i=(cm.length>2?3:0);i<cm.length-(cm.length>2?0:1);i+=(cm.length>2?7:9)){const[x,y]=cm[i],[x2,y2]=cm[Math.min(cm.length-1,i+1)];const a=Math.atan2(y2-y,x2-x),lx=x-Math.sin(a)*.03,ly=y+Math.cos(a)*.03;if(!libre(lx,ly,.01)||dMuro(lx,ly)<.04)continue;const lz=gy(lx,ly);add(cil(.0012,.0016,.05,6),HIE,lx,lz+.025,ly);add(new THREE.SphereGeometry(.0045,8,6),LUZ,lx,lz+.053,ly);nf++}CST.farolas=nf}
 // 8) estanque de patos al este, junto al recinto
 const hueco=(cx,cy,R,need)=>{let best=null;for(let r=0;r<=R;r+=.04)for(let k=0;k<Math.max(1,Math.round(r*60));k++){const a=k/Math.max(1,Math.round(r*60))*6.283,x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r;let ok=true;for(let b=0;b<12&&ok;b++){const aa=b/12*6.283;for(const rr of[0,need*.5,need]){const px=x+Math.cos(aa)*rr,py=y+Math.sin(aa)*rr;if(t(px,py)!==1||enFuerte(px,py)||dMuro(px,py)<.05||dRu(px,py)<.1){ok=false;break}}}if(ok)return[x,y]}return best};
 {const E=hueco(87.05,28.1,.35,.13);if(E){const[x,y]=E,z=gy(x,y);const g=new THREE.CircleGeometry(.12,28);g.rotateX(-Math.PI/2);g.scale(1,1,.75);const m=new THREE.Mesh(g,AGUA);m.position.set(x,z+.006,y);G.add(m);
  for(let k=0;k<30;k++){const a=k/30*6.283;add(new THREE.DodecahedronGeometry(.008+rn()*.006,0),PIEC,x+Math.cos(a)*.122,z+.004,y+Math.sin(a)*.092)}
  for(let k=0;k<6;k++){const a=rn()*6.283,r=rn()*.07,px=x+Math.cos(a)*r,py=y+Math.sin(a)*r*.75;add(new THREE.SphereGeometry(.004,6,4),BLA,px,z+.009,py);add(new THREE.SphereGeometry(.0025,6,4),BLA,px+.004,z+.013,py);add(new THREE.ConeGeometry(.0012,.003,4).rotateZ(-Math.PI/2),NAR,px+.0068,z+.013,py)}
  for(let k=0;k<0;k++){const a=k/4*6.283+.4,bx=x+Math.cos(a)*.15,by=y+Math.sin(a)*.12;if(t(bx,by)!==1)continue;const bz=gy(bx,by);add(cub(.026,.0025,.008),MAD,bx,bz+.007,by,-a+Math.PI/2);add(cub(.026,.007,.0015),MAD,bx+Math.cos(a)*.004,bz+.011,by+Math.sin(a)*.004,-a+Math.PI/2)}
  CST.estanque=E}}
 // 9) poblado castreño: casas redondas de piedra con techo cónico de paja y muralla baja
 {const C=hueco(85.7,26.55,.6,.17)||hueco(85.3,28.2,.5,.17);if(C){const[x,y]=C;let nh=0;for(let k=0;k<5;k++){const a=k/5*6.283+.3,r=.085+rn()*.03,hx=x+Math.cos(a)*r,hy=y+Math.sin(a)*r;if(t(hx,hy)!==1)continue;const z=gy(hx,hy),R=.026+rn()*.008;
    add(cil(R,R*1.03,.024,12),PIEC,hx,z+.01,hy);add(new THREE.ConeGeometry(R*1.25,.03,12),PAJA,hx,z+.036,hy);add(cub(.008,.016,.004),MAD,hx+Math.cos(a+3.14)*R*.98,z+.008,hy+Math.sin(a+3.14)*R*.98,-(a+3.14)+Math.PI/2);nh++}
   for(let k=0;k<44;k++){const a=k/44*6.283;if(k%11===0)continue;const px=x+Math.cos(a)*.16,py=y+Math.sin(a)*.16;if(t(px,py)!==1)continue;add(cub(.024,.012,.01),PIEC,px,gy(px,py)+.005,py,-a+Math.PI/2)}
   CST.poblado=[x,y,nh]}}
 // 10) pinar y robledal en las laderas, fuera de las murallas; dentro solo algunos cipreses junto a los caminos
 const TR=[],paso=LT?.075:.055;for(let y=25.5;y<=29.8;y+=paso)for(let x=84.5;x<=88.2;x+=paso){const px=x+(rn()-.5)*paso*.9,py=y+(rn()-.5)*paso*.9;if(!libre(px,py))continue;if(dRu(px,py)<.1)continue;
  const dm=dMuro(px,py);if(dm<.07)continue;if(CST.estanque&&Math.hypot(px-CST.estanque[0],py-CST.estanque[1])<.2)continue;if(CST.poblado&&Math.hypot(px-CST.poblado[0],py-CST.poblado[1])<.2)continue;if(Math.hypot(px-86.2,py-26.3)<.16)continue;
  if(enFuerte(px,py)){if(dCam(px,py)>.035&&dCam(px,py)<.06&&rn()<.25&&Math.hypot(px-86.2,py-27.7)>.28)TR.push([px,py,2]);continue}
  const n=.5+.25*Math.sin(px*3.3+Math.sin(py*2.1)*1.6)+.25*Math.sin(py*2.9+Math.cos(px*1.7)*2.3);if(n<.28)continue;if(dCam(px,py)<.025)continue;TR.push([px,py,rn()<.55?0:1])}
 CST.arboles=TR.length;
 {const esp=[{tr:cil(.003,.0045,1,5).translate(0,.5,0),cp:new THREE.IcosahedronGeometry(1,0),h:[.08,.13],r:[.022,.03],sy:.55,cy:.92,col:[0x2f5f2c,0x356b30,0x2a5528]},// pino piñonero (copa ancha arriba)
   {tr:cil(.0035,.005,1,5).translate(0,.5,0),cp:new THREE.IcosahedronGeometry(1,0),h:[.05,.085],r:[.022,.032],sy:1,cy:.75,col:[0x4c8f3a,0x3f7d34,0x5a9440]},// roble
   {tr:cil(.002,.003,1,5).translate(0,.5,0),cp:new THREE.ConeGeometry(1,1,7).translate(0,.5,0),h:[.06,.08],r:[.008,.011],sy:1,cy:.12,col:[0x23502a,0x2a5a2e]}];// ciprés
  const trM=new THREE.MeshStandardMaterial({color:0x6b4a32,roughness:1}),cpM=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9,flatShading:true});
  const mm=new THREE.Matrix4(),q=new THREE.Quaternion(),e=new THREE.Euler(),co=new THREE.Color();
  esp.forEach((E,si)=>{const L=TR.filter(p=>p[2]===si);if(!L.length)return;const it=new THREE.InstancedMesh(E.tr,trM,L.length),ic=new THREE.InstancedMesh(E.cp,cpM,L.length);it.userData.cst=ic.userData.cst=1;
   L.forEach(([x,y],i)=>{const h=E.h[0]+(E.h[1]-E.h[0])*rn(),r=E.r[0]+(E.r[1]-E.r[0])*rn(),z=gy(x,y)-.003;e.set(0,rn()*6.28,0);q.setFromEuler(e);
    mm.compose(new THREE.Vector3(x,z,y),q,new THREE.Vector3(1,h,1));it.setMatrixAt(i,mm);
    mm.compose(new THREE.Vector3(x,z+h*E.cy,y),q,new THREE.Vector3(r,si===2?h*.95:r*E.sy,r));ic.setMatrixAt(i,mm);co.setHex(E.col[(rn()*E.col.length)|0]).offsetHSL(0,0,(rn()-.5)*.06);ic.setColorAt(i,co)});
   it.castShadow=ic.castShadow=!LT;ic.receiveShadow=true;G.add(it,ic)})}
 CST.oc=ocultar((x,y)=>(x>84.4&&x<88.2&&y>25.4&&y<29.8)&&(enFuerte(x,y)||dMuro(x,y)<.06||(CST.estanque&&Math.hypot(x-CST.estanque[0],y-CST.estanque[1])<.17)||(CST.poblado&&Math.hypot(x-CST.poblado[0],y-CST.poblado[1])<.19)));
 for(const[mat,L]of RAW){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(L,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(UVS.get(mat),2));g.computeVertexNormals();const m=new THREE.Mesh(g,mat);mat.side=THREE.DoubleSide;m.castShadow=!LT;m.receiveShadow=true;G.add(m)}
 for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=!LT&&mat!==LUZ;m.receiveShadow=true;G.add(m)}
 scene.add(G);CST.G=G}
function subePaso(){""")
open(f,'w').write(s)
print('ok castro')
