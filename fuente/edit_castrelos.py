f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= PARQUE DE CASTRELOS =================
# Google Earth solo como referencia (no se copia nada): bosque denso entre el río Lagares y la avenida, paseos de
# tierra, auditorio al aire libre en graderío semicircular con escenario cubierto, plaza con fuente, zona infantil y
# jardín formal de setos junto al pazo. Modelos propios y genéricos.
r("function subeZonas(){psolChk();samChk();","function subeZonas(){psolChk();samChk();casChk();")
r("function subePaso(){",r"""const CAS={hecha:0,t:0,AX:80.62,AZ:54.83,RX:1.08,RZ:.6};window.__CAS=CAS;
function casChk(){if(!MAPA||!MI)return;if(!CAS.hecha){if(sueloRap(82.5,52.4)==null||sueloRap(80.9,54.8)==null)return;CAS.hecha=1;setTimeout(()=>{try{casCrea()}catch(e){console.warn('castrelos',e);CAS.err=String(e)}},1100);return}
 const n=performance.now();if(n-CAS.t>2500){CAS.t=n;try{casLosa()}catch(e){}}}
// la losa gris del catastro donde está el graderío: se aplanan sus triángulos (paredes y techo a la misma cota)
function casLosa(){const v=new THREE.Vector3();for(const m of repMallas(80.93,54.83)){const g=m.geometry;if(g.userData.casL||!g.index)continue;g.userData.casL=1;const pa=g.attributes.position,ix=g.index;let c=0;
 for(let t=0;t<ix.count/3;t++){let ok=true,ym=-9;for(let k=0;k<3;k++){v.fromBufferAttribute(pa,ix.getX(t*3+k)).applyMatrix4(m.matrixWorld);if(v.x<80.11||v.x>81.76||v.z<54.18||v.z>55.48){ok=false;break}ym=Math.max(ym,v.y)}
  if(ok&&ym>.2803&&ym<.2813){const a=ix.getX(t*3);ix.setX(t*3+1,a);ix.setX(t*3+2,a);c++}}
 if(c){ix.needsUpdate=true;CAS.losa=(CAS.losa||0)+c}}}
function casCrea(){const G=new THREE.Group();G.name='castrelos';const t=(x,y)=>cell(x,y).t,gy=(x,z)=>{const v=sueloRap(x,z);return v==null?groundY(x,z):v};const LT=!!window.LITE;
 casLosa();
 let rs=7;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.8},o));
 const PIE=M(0xcfc6b4,{roughness:.9}),PIE2=M(0xb8ae9a,{roughness:.95}),CES=M(0x6fae4a,{roughness:1}),BLA=M(0xf5f3ee,{roughness:.5,side:THREE.DoubleSide}),HIE=M(0x2a2d33,{metalness:.5,roughness:.45}),
  LUZ=M(0xfff2cc,{emissive:0xffd88a,emissiveIntensity:.9}),MAD=M(0x8a5a36),SETO=M(0x2f6b2c,{roughness:1}),ROS=M(0xe0567a),ROS2=M(0xf2a2b8),AGUA=new THREE.MeshStandardMaterial({color:0x5cc9e0,roughness:.15,metalness:.1,emissive:0x0a4d66,emissiveIntensity:.3}),
  ROJ=M(0xd8402e),AMA=M(0xf2c230),AZU=M(0x2f7fd6),TIE=new THREE.MeshStandardMaterial({color:0xcbb084,roughness:1,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2});
 const PARTS=new Map(),add=(geo,mat,x,y,z,ry=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();g.deleteAttribute('uv');g.rotateY(ry);g.translate(x,y,z);if(!PARTS.has(mat))PARTS.set(mat,[]);PARTS.get(mat).push(g)};
 const cil=(a,b,h,s=8)=>new THREE.CylinderGeometry(a,b,h,s),cub=(a,b,c)=>new THREE.BoxGeometry(a,b,c);
 const ocultar=dentro=>{const mm=new THREE.Matrix4(),pp=new THREE.Vector3(),q=new THREE.Quaternion(),sc=new THREE.Vector3();let n=0;
  scene.traverse(o=>{if(!o.isInstancedMesh||o.userData.cas||o.count>5000)return;let ch=false;for(let k=0;k<o.count;k++){o.getMatrixAt(k,mm);mm.decompose(pp,q,sc);if(sc.x<=0)continue;const w=pp.clone().applyMatrix4(o.matrixWorld);if(dentro(w.x,w.z)){sc.setScalar(0);mm.compose(pp,q,sc);o.setMatrixAt(k,mm);ch=true;n++}}if(ch)o.instanceMatrix.needsUpdate=true});return n};
 // 1) superficie del parque: celdas verdes conectadas entre el río y la avenida
 const st=.05,K=(x,y)=>Math.round(x/st)+','+Math.round(y/st),PQ=new Set();{const Q=[[82.5,52.4]];let n=0;while(Q.length&&n<40000){const[x,y]=Q.pop(),k=K(x,y);if(PQ.has(k)||x<77.5||x>88||y<48.5||y>57.5)continue;if(t(x,y)!==1){continue}PQ.add(k);n++;Q.push([x+st,y],[x-st,y],[x,y+st],[x,y-st])}}
 const enP=(x,y)=>PQ.has(K(x,y));CAS.celdas=PQ.size;
 // bordes: río (oeste) y avenida (este) en cada fila
 const FI=[];for(let y=50.7;y<=56.5;y+=.1){let xr=null,xe=null;for(let x=77.5;x<88;x+=.025){if(enP(x,y)){if(xr==null)xr=x;xe=x}else if(xr!=null&&t(x,y)===2&&x-xr>.3)break}if(xr!=null&&xe-xr>.35)FI.push([y,xr,xe])}
 for(let it=0;it<3;it++)for(let i=1;i<FI.length-1;i++){FI[i][1]=(FI[i-1][1]+2*FI[i][1]+FI[i+1][1])/4;FI[i][2]=(FI[i-1][2]+2*FI[i][2]+FI[i+1][2])/4}
 CAS.FI=FI.length;
 const AX=CAS.AX,AZ=CAS.AZ,RX=CAS.RX,RZ=CAS.RZ,enAud=(x,y,m=1)=>{if(x<AX-.16*m)return false;const u=(x-AX)/(RX*m+.04),w=(y-AZ)/(RZ*m+.04);return u*u+w*w<1&&x>AX-.2};
 // 2) caminos de tierra: paseo del río, paseo central (rodea el auditorio por el este) y transversales
 const CAM=[];const cinta=(pts,w)=>{if(pts.length<2)return;CAM.push({pts,w});const pos=[],idx=[];for(let i=0;i<pts.length;i++){const a=pts[Math.max(0,i-1)],b=pts[Math.min(pts.length-1,i+1)];let dx=b[0]-a[0],dy=b[1]-a[1];const l=Math.hypot(dx,dy)||1;dx/=l;dy/=l;const nx=-dy*w/2,ny=dx*w/2,[x,y]=pts[i];
   pos.push(x+nx,gy(x+nx,y+ny)+.004,y+ny,x-nx,gy(x-nx,y-ny)+.004,y-ny);if(i<pts.length-1){const k=i*2;idx.push(k,k+1,k+2,k+1,k+3,k+2)}}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();const m=new THREE.Mesh(g,TIE);m.receiveShadow=true;G.add(m)};
 const suav=(P,it=4)=>{for(let k=0;k<it;k++)for(let i=1;i<P.length-1;i++){P[i]=[(P[i-1][0]+2*P[i][0]+P[i+1][0])/4,(P[i-1][1]+2*P[i][1]+P[i+1][1])/4]}return P};
 const rio=FI.map(([y,xr,xe])=>[xr+.075,y]),cen=suav(FI.map(([y,xr,xe])=>{let x=xr+(xe-xr)*(.55+.08*Math.sin(y*2.1));if(y>53.95&&y<55.7)x=Math.max(x,Math.min(xe-.1,AX+RX+.12));return[x,y]}),6);
 cinta(rio,.04);cinta(cen,.05);
 const cruces=[51.3,52.5,53.5,56.1],PLZ=[];for(const yc of cruces){const f=FI.find(q=>Math.abs(q[0]-yc)<.06);if(!f)continue;const[y,xr,xe]=f;const P=[];for(let k=0;k<=12;k++){const u=k/12;P.push([xr+.07+(xe-xr-.12)*u,y+.06*Math.sin(u*3.1)])}cinta(suav(P,2),.035);
  if(yc===52.5){const c=cen.reduce((b,p)=>Math.abs(p[1]-y)<Math.abs(b[1]-y)?p:b);PLZ.push(c)}}
 const dCam=(x,y)=>{let d=9;for(const c of CAM)for(let i=0;i<c.pts.length;i+=1){const p=c.pts[i];const e=Math.hypot(p[0]-x,p[1]-y)-c.w/2;if(e<d)d=e}return d};
 // 3) plaza con fuente en el cruce central
 for(const[px,py]of PLZ){const z=gy(px,py);add(cil(.1,.1,.008,28),PIE,px,z+.002,py);add(cil(.045,.048,.016,24),PIE2,px,z+.01,py);const ag=new THREE.Mesh(cil(.04,.04,.002,24),AGUA);ag.position.set(px,z+.0175,py);G.add(ag);
  add(cil(.008,.011,.03,10),PIE2,px,z+.03,py);add(cil(.018,.012,.005,14),PIE2,px,z+.045,py);add(cil(.004,.006,.014,8),PIE2,px,z+.054,py);
  for(let k=0;k<8;k++){const a=k/8*6.283,bx=px+Math.cos(a)*.08,bz=py+Math.sin(a)*.08;if(k%2)continue;add(cub(.03,.004,.009),MAD,bx,z+.009,bz,-a+Math.PI/2);add(cub(.03,.008,.002),MAD,bx+Math.cos(a)*.005,z+.014,bz+Math.sin(a)*.005,-a+Math.PI/2)}}
 CAS.plz=PLZ.length;
 // 4) farolas y bancos a lo largo del paseo central y del río
 for(const[c,cada]of[[cen,4],[rio,5]])for(let i=2;i<c.length-2;i+=cada){const[x,y]=c[i],[x2,y2]=c[i+1],a=Math.atan2(y2-y,x2-x),nx=-Math.sin(a),ny=Math.cos(a),lado=(i/cada)%2?1:-1;
  const lx=x+nx*.04*lado,ly=y+ny*.04*lado,lz=gy(lx,ly);add(cil(.0012,.0016,.05,6),HIE,lx,lz+.025,ly);add(new THREE.SphereGeometry(.0045,8,6),LUZ,lx,lz+.053,ly);
  const bx=x-nx*.035*lado,by=y-ny*.035*lado,bz=gy(bx,by);add(cub(.026,.0025,.008),MAD,bx,bz+.007,by,-a);add(cub(.026,.007,.0015),MAD,bx-nx*.004*lado,bz+.011,by-ny*.004*lado,-a);add(cub(.002,.007,.008),HIE,bx+Math.cos(a)*.011,bz+.0035,by+Math.sin(a)*.011,-a);add(cub(.002,.007,.008),HIE,bx-Math.cos(a)*.011,bz+.0035,by-Math.sin(a)*.011,-a)}
 // 5) auditorio al aire libre: graderío semicircular de piedra y césped mirando a un escenario con cubierta blanca
 {const NT=LT?7:10,N=40,TH=[],base=gy(AX+.08,AZ)+.004;let prev=base;
  for(let i=0;i<=NT;i++){const r=.32+.68*i/NT;let gm=-9;for(let k=0;k<=N;k++){const a=-Math.PI/2+Math.PI*k/N;gm=Math.max(gm,gy(AX+RX*r*Math.cos(a),AZ+RZ*r*Math.sin(a)))}const h=Math.max(prev+(i?.006:0),gm+.004);TH.push([r,h]);prev=h}
  const fondo=base-.03,qs={P:[],C:[]},quad=(L,a,b,c,d)=>L.push(...a,...b,...c,...a,...c,...d);
  const pt=(r,a,h)=>[AX+RX*r*Math.cos(a),h,AZ+RZ*r*Math.sin(a)];
  // platea (semicírculo interior) de losas
  for(let k=0;k<N;k++){const a0=-Math.PI/2+Math.PI*k/N,a1=a0+Math.PI/N;qs.P.push(...[AX,base,AZ],...pt(TH[0][0],a1,base),...pt(TH[0][0],a0,base))}
  for(let i=0;i<NT;i++){const[r0,h0]=TH[i],[r1,h1]=TH[i+1],rb=r0+.015/RX*1.2;
   for(let k=0;k<N;k++){const a0=-Math.PI/2+Math.PI*k/N,a1=a0+Math.PI/N,hp=i?TH[i][1]:base;
    quad(qs.P,pt(r0,a0,i?h0:base),pt(r0,a1,i?h0:base),pt(r0,a1,h1),pt(r0,a0,h1));// contrahuella
    quad(qs.P,pt(r0,a0,h1),pt(r0,a1,h1),pt(rb,a1,h1),pt(rb,a0,h1));// borde de piedra
    quad(qs.C,pt(rb,a0,h1),pt(rb,a1,h1),pt(r1,a1,h1),pt(r1,a0,h1))}}// césped
  {const[r,h]=TH[NT];for(let k=0;k<N;k++){const a0=-Math.PI/2+Math.PI*k/N,a1=a0+Math.PI/N;quad(qs.P,pt(r,a0,h),pt(r,a0,fondo),pt(r,a1,fondo),pt(r,a1,h))}
   for(const s_ of[-1,1])for(let i=0;i<NT;i++){const[r0]=TH[i],[r1,h1]=TH[i+1],a=s_*Math.PI/2;quad(qs.P,pt(r0,a,h1),pt(r1,a,h1),pt(r1,a,fondo),pt(r0,a,fondo))}}
  for(const[L,mat]of[[qs.P,PIE],[qs.C,CES]]){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(L,3));g.computeVertexNormals();const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:mat.color,roughness:.9,side:THREE.DoubleSide}));m.receiveShadow=true;m.castShadow=!LT;G.add(m)}
  // pasillos radiales de escaleras
  for(const a of[-Math.PI/4,0,Math.PI/4])for(let i=0;i<NT;i++){const[r0]=TH[i],[r1,h1]=TH[i+1],rm=(r0+r1)/2,[x,,z]=pt(rm,a,h1);add(cub(RX*(r1-r0)*1.02,.002,.022),PIE2,x,h1+.001,z,-Math.atan2(RZ*Math.sin(a),RX*Math.cos(a)))}
  // escenario y concha acústica
  const sx=AX-.07,sz=gy(sx,AZ);add(cub(.16,.024,.36),PIE2,sx,Math.max(sz,base)+.012-.004,AZ);add(cub(.17,.003,.37),MAD,sx,Math.max(sz,base)+.0245,AZ);
  const sh=new THREE.SphereGeometry(.17,20,10,-Math.PI/2,Math.PI,0,Math.PI/2);sh.scale(.75,1,1.25);add(sh,BLA,sx-.01,Math.max(sz,base)+.025,AZ);
  for(const s_ of[-1,1]){const tx=AX+.05,tz=AZ+s_*(RZ+.06),tg=gy(tx,tz);add(cil(.003,.004,.12,6),HIE,tx,tg+.06,tz);add(cub(.014,.012,.022),HIE,tx,tg+.12,tz);add(cub(.002,.009,.018),LUZ,tx-.008,tg+.12,tz)}
  CAS.aud=[base,TH[NT][1]]}
 // 6) zona infantil junto al paseo central
 {const c=cen[Math.max(0,cen.findIndex(p=>p[1]>51.75))];const px=c[0]+.09,py=c[1];if(enP(px,py)){const z=gy(px,py);add(cub(.13,.003,.1),M(0xc77a4e,{roughness:1}),px,z+.002,py);
  for(const s_ of[-1,1])for(const d of[-1,1])add(cub(.002,.04,.002),AZU,px-.03+d*.02,z+.02,py+s_*.03);add(cub(.045,.002,.002),AZU,px-.03,z+.04,py+.03);add(cub(.045,.002,.002),AZU,px-.03,z+.04,py-.03);
  add(cub(.01,.002,.006),ROJ,px-.04,z+.013,py+.03);add(cub(.01,.002,.006),AMA,px-.02,z+.013,py-.03);
  add(cub(.012,.03,.012),AMA,px+.03,z+.015,py-.02);const sl=cub(.01,.002,.045);sl.rotateX(.6);add(sl,ROJ,px+.03,z+.016,py+.005);
  add(new THREE.SphereGeometry(.018,8,5,0,6.283,0,Math.PI/2),AZU,px+.035,z+.002,py+.03);CAS.inf=[px,py]}}
 // 7) jardín formal de setos y rosaleda junto al pazo
 {let J=null;for(const[sx,sy]of[[84.85,55.4],[84.7,55.45],[85,55.3],[84.6,55.55]]){if(t(sx,sy)===1){J=[sx,sy];break}}
  if(J){const lib=(x,y)=>{const ms=repMallas(x,y);if(!ms.length)return true;return repAltura(x,y,ms)<gy(x,y)+.02};const e=.02,seen=new Set(),Q=[J],ok=[];const kk=(x,y)=>Math.round(x/e)+','+Math.round(y/e);
   while(Q.length&&ok.length<2500){const[x,y]=Q.pop(),k=kk(x,y);if(seen.has(k))continue;seen.add(k);if(Math.hypot(x-J[0],y-J[1])>.42||t(x,y)!==1||!lib(x,y))continue;let bien=true;for(const[a,b]of[[.03,0],[-.03,0],[0,.03],[0,-.03]])if(t(x+a,y+b)!==1){bien=false;break}if(!bien)continue;ok.push([x,y]);Q.push([x+e,y],[x-e,y],[x,y+e],[x,y-e])}
   CAS.jardin=ok.length;if(ok.length>60){const T=.16;for(const[x,y]of ok){const z=gy(x,y),u=((x-J[0])/T%1+1.5)%1-.5,w=((y-J[1])/T%1+1.5)%1-.5,rr=Math.hypot(u,w),dj=Math.hypot(x-J[0],y-J[1]);
     add(cub(e,.002,e),PIE,x,z+.002,y);
     if(dj<.05){continue}
     if(Math.abs(u)>.42||Math.abs(w)>.42||Math.abs(rr-.28)<.06)add(cub(e*.95,.012,e*.95),SETO,x,z+.007,y);
     else if(rr<.16&&((Math.round(x/e)+Math.round(y/e))%2===0))add(new THREE.IcosahedronGeometry(.006,0),rn()<.5?ROS:ROS2,x,z+.006,y)}
    const z=gy(J[0],J[1]);add(cil(.035,.037,.012,20),PIE2,J[0],z+.006,J[1]);const ag=new THREE.Mesh(cil(.03,.03,.002,20),AGUA);ag.position.set(J[0],z+.012,J[1]);G.add(ag);add(cil(.004,.006,.03,8),PIE2,J[0],z+.025,J[1]);add(cil(.012,.008,.004,12),PIE2,J[0],z+.04,J[1]);
    ocultar((x,y)=>Math.hypot(x-J[0],y-J[1])<.4&&ok.some(p=>Math.abs(p[0]-x)<.02&&Math.abs(p[1]-y)<.02))}}}
 // 8) bosque denso: robles, castaños, pinos y plátanos, con claros
 const lib2=(x,y)=>{for(const[a,b]of[[0,0],[.03,0],[-.03,0],[0,.03],[0,-.03]])if(t(x+a,y+b)!==1)return false;return true};
 const ruido=(x,y)=>.5+.25*Math.sin(x*3.1+Math.sin(y*2.3)*1.7)+.25*Math.sin(y*2.7+Math.cos(x*1.9)*2.1);
 const TR=[];const paso=LT?.075:.055;for(let y=50.6;y<=56.6;y+=paso)for(let x=77.6;x<=86;x+=paso){const px=x+(rn()-.5)*paso*.9,py=y+(rn()-.5)*paso*.9;if(!enP(px,py)||!lib2(px,py))continue;if(enAud(px,py,1.12)||(px>AX-.22&&px<AX+.05&&Math.abs(py-AZ)<.3))continue;
  if(PLZ.some(([a,b])=>Math.hypot(a-px,b-py)<.14))continue;if(CAS.inf&&Math.hypot(CAS.inf[0]-px,CAS.inf[1]-py)<.1)continue;const n=ruido(px,py);if(n<.3)continue;if(dCam(px,py)<.022)continue;TR.push([px,py,n])}
 CAS.arboles=TR.length;
 {const esp=[// [tronco, copa, materiales]
   {w:.55,tr:cil(.0035,.005,1,5).translate(0,.5,0),cp:new THREE.IcosahedronGeometry(1,0),h:[.05,.09],r:[.022,.034],sy:1,cy:.75,col:[0x3f7d34,0x4c8f3a,0x356b2c,0x5a9440]},
   {w:.22,tr:cil(.003,.0045,1,5).translate(0,.5,0),cp:new THREE.ConeGeometry(1,1.6,7).translate(0,.8,0),h:[.07,.12],r:[.016,.024],sy:1,cy:.25,col:[0x2a5a2e,0x315f34,0x24502a]},
   {w:.23,tr:cil(.003,.0042,1,5).translate(0,.5,0),cp:new THREE.IcosahedronGeometry(1,1),h:[.09,.14],r:[.024,.032],sy:1.45,cy:.72,col:[0x5f9a46,0x6aa24c,0x4f8a3c]}];
  const trM=new THREE.MeshStandardMaterial({color:0x6b4a32,roughness:1}),cpM=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9,flatShading:true});
  const asig=TR.map(()=>{const v=rn();return v<esp[0].w?0:v<esp[0].w+esp[1].w?1:2});
  const mm=new THREE.Matrix4(),q=new THREE.Quaternion(),e=new THREE.Euler(),co=new THREE.Color();
  esp.forEach((E,si)=>{const L=TR.filter((_,i)=>asig[i]===si);if(!L.length)return;const it=new THREE.InstancedMesh(E.tr,trM,L.length),ic=new THREE.InstancedMesh(E.cp,cpM,L.length);it.userData.cas=ic.userData.cas=1;
   L.forEach(([x,y,n],i)=>{const h=E.h[0]+(E.h[1]-E.h[0])*rn()*(.6+.4*n),r=E.r[0]+(E.r[1]-E.r[0])*rn(),z=gy(x,y)-.003;e.set(0,rn()*6.28,0);q.setFromEuler(e);
    mm.compose(new THREE.Vector3(x,z,y),q,new THREE.Vector3(1,h,1));it.setMatrixAt(i,mm);
    mm.compose(new THREE.Vector3(x,z+h*E.cy,y),q,new THREE.Vector3(r,r*E.sy*(si===1?h/.1:1),r));ic.setMatrixAt(i,mm);co.setHex(E.col[(rn()*E.col.length)|0]).offsetHSL(0,0,(rn()-.5)*.06);ic.setColorAt(i,co)});
   it.castShadow=ic.castShadow=!LT;ic.receiveShadow=true;G.add(it,ic)})}
 CAS.oc=ocultar((x,y)=>enAud(x,y,1.12)||PLZ.some(([a,b])=>Math.hypot(a-x,b-y)<.12)||(enP(x,y)&&dCam(x,y)<.02));
 for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=!LT&&mat!==LUZ&&mat!==TIE;m.receiveShadow=true;G.add(m)}
 scene.add(G);CAS.G=G}
function subePaso(){""")
open(f,'w').write(s)
print('ok castrelos')
