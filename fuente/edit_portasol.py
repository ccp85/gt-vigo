import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= PORTA DO SOL =================
# hook de cámara de depuración (window.__CAMV) para las pruebas
r("const R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,logarithmicDepthBuffer:true});",
  "const R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,logarithmicDepthBuffer:true});{const r0=R.render.bind(R);R.render=(sc,c)=>{const O=window.__CAMV;if(O&&c===window.pcam){c.up.set(0,1,0);c.position.set(...O.p);c.lookAt(...O.l);c.fov=O.f||55;c.updateProjectionMatrix();c.updateMatrixWorld()}return r0(sc,c)}}window.__dbg={cell:(x,y)=>cell(x,y),g:(x,y)=>groundMap(x,y),s:(x,z)=>sueloRap(x,z),top:(x,z)=>{const rc=new THREE.Raycaster(new THREE.Vector3(x,4,z),new THREE.Vector3(0,-1,0),0,8);const h=rc.intersectObjects(scene.children,true).filter(i=>i.object.isMesh&&!i.object.isInstancedMesh&&i.object.visible&&!(window.__PSOL&&__PSOL.G&&__PSOL.G.children.includes(i.object)));return h.length?[h[0].point.y,h[0].object.name||h[0].object.parent&&h[0].object.parent.name]:null}};")

# ----- mejoras de la plaza (Google Earth solo como referencia de estilo; sin estatuas)
r("function subeZonas(){","function subeZonas(){psolChk();")
r("function subePaso(){",r"""const PSOL={hecha:0,X0:86.3,X1:88.02,Y0:17.55,Y1:18.25,TX:87.45,TY:18.0};window.__PSOL=PSOL;
function psolChk(){if(PSOL.hecha||!MAPA||!MI)return;if(sueloRap(87.45,18.0)==null||sueloRap(86.6,17.75)==null||sueloRap(87.9,17.9)==null)return;if(!repMallas(87.0,17.9).length||!repMallas(87.9,18.1).length||!repMallas(86.6,17.6).length)return;PSOL.hecha=1;setTimeout(()=>{try{psolCrea()}catch(e){console.warn('psol',e);PSOL.err=String(e)}},700)}
function psolGranito(){const c=document.createElement('canvas');c.width=c.height=512;const x=c.getContext('2d');let sd=7;const rn=()=>(sd=(sd*16807)%2147483647)/2147483647;
 x.fillStyle='#6f6c66';x.fillRect(0,0,512,512);const H=64;
 for(let r=0;r<8;r++){const o=(r&1)*48;for(let k=-1;k<6;k++){const w=96,x0=k*w+o,v=150+(rn()*26|0),t=rn()*8;x.fillStyle=`rgb(${v},${v-2+t*.2|0},${v-7})`;x.fillRect(x0+2,r*H+2,w-4,H-4);
  for(let n=0;n<70;n++){const q=v+(rn()*44-22|0);x.fillStyle=`rgba(${q},${q},${q-4},.55)`;x.fillRect(x0+3+rn()*(w-8),r*H+3+rn()*(H-8),1.6,1.6)}
  x.fillStyle='rgba(255,255,255,.07)';x.fillRect(x0+2,r*H+2,w-4,3)}}
 const T=new THREE.CanvasTexture(c);T.wrapS=T.wrapT=THREE.RepeatWrapping;T.colorSpace=THREE.SRGBColorSpace;T.anisotropy=8;return T}
function psolCrea(){const P=PSOL,G=new THREE.Group();G.name='portaDoSol';
 const t=(x,y)=>cell(x,y).t,gy=(x,z)=>{const v=sueloRap(x,z);return v==null?groundY(x,z):v};
 const libre=(x,y)=>{const ms=repMallas(x,y);if(!ms.length)return true;const h=repAltura(x,y,ms);return h<gy(x,y)+.03},near=(x,y,r,tt)=>{for(let a=-r;a<=r+1e-6;a+=.02)for(let b=-r;b<=r+1e-6;b+=.02){if(a*a+b*b>r*r)continue;if(t(x+a,y+b)===tt)return true}return false};
 // 1) pavimento de granito: celdas peatonales conectadas con la plaza
 const res=MAPA.res,i0=Math.floor((P.X0-MAPA.ox)*res),i1=Math.ceil((P.X1-MAPA.ox)*res),j0=Math.floor((P.Y0-MAPA.oy)*res),j1=Math.ceil((P.Y1-MAPA.oy)*res);
 const cx=i=>MAPA.ox+i/res,cy=j=>MAPA.oy+j/res,on=new Set(),Q=[[Math.round((87.3-MAPA.ox)*res),Math.round((17.92-MAPA.oy)*res)]];
 while(Q.length){const[i,j]=Q.pop(),k=i+','+j;if(on.has(k)||i<i0||i>i1||j<j0||j>j1||t(cx(i),cy(j))!==1||!libre(cx(i),cy(j)))continue;on.add(k);Q.push([i+1,j],[i-1,j],[i,j+1],[i,j-1])}
 P.celdas=on.size;const hv=new Map(),HV=(i,j)=>{const k=i+','+j;if(!hv.has(k))hv.set(k,gy(cx(i-.5)+0,cy(j-.5))+.0035);return hv.get(k)};
 const pos=[],uv=[],S=.11;for(const k of on){const[i,j]=k.split(',').map(Number);const xa=cx(i-.5),xb=cx(i+.5),ya=cy(j-.5),yb=cy(j+.5);
  const A=[xa,HV(i,j),ya],B=[xb,HV(i+1,j),ya],C=[xb,HV(i+1,j+1),yb],D=[xa,HV(i,j+1),yb];
  for(const p of[A,D,C,A,C,B]){pos.push(...p);uv.push(p[0]/S,p[2]/S)}}
 {const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.computeVertexNormals();
  const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({map:psolGranito(),roughness:.85,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}));m.receiveShadow=true;m.renderOrder=1;G.add(m)}
 // anillo de granito oscuro alrededor del árbol
 {const z=gy(P.TX,P.TY);const rg=new THREE.Mesh(new THREE.RingGeometry(.135,.165,48),new THREE.MeshStandardMaterial({color:0x56544f,roughness:.8,polygonOffset:true,polygonOffsetFactor:-4,polygonOffsetUnits:-4}));rg.rotation.x=-Math.PI/2;rg.position.set(P.TX,z+.005,P.TY);G.add(rg)}
 // mobiliario: piezas que se funden por material
 const PARTS=new Map(),add=(geo,mat,x,y,z,ry=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();g.deleteAttribute('uv');g.rotateY(ry);g.translate(x,y,z);if(!PARTS.has(mat))PARTS.set(mat,[]);PARTS.get(mat).push(g)};
 const HIE=new THREE.MeshStandardMaterial({color:0x1c1f23,roughness:.45,metalness:.6}),FAR=new THREE.MeshStandardMaterial({color:0xfff1c8,emissive:0xffcf7a,emissiveIntensity:.9,roughness:.3}),
  GRA=new THREE.MeshStandardMaterial({color:0xa9a69e,roughness:.9}),LONA=new THREE.MeshStandardMaterial({color:0xf4f4f0,roughness:.7}),ROJO=new THREE.MeshStandardMaterial({color:0xb3202a,roughness:.6}),
  MAD=new THREE.MeshStandardMaterial({color:0x6b4a2f,roughness:.8}),HOJ=new THREE.MeshStandardMaterial({color:0x3f7a3a,roughness:.8}),BOM=new THREE.MeshStandardMaterial({color:0xffe6a8,emissive:0xffc860,emissiveIntensity:1.2});
 const cil=(r1,r2,h,s=8)=>new THREE.CylinderGeometry(r1,r2,h,s),cub=(a,b,c)=>new THREE.BoxGeometry(a,b,c);
 const farola=(x,y)=>{const z=gy(x,y);add(cil(.0035,.0042,.008),HIE,x,z+.004,y);add(cil(.0011,.0015,.07),HIE,x,z+.043,y);add(cil(.0024,.0018,.004),HIE,x,z+.078,y);
  for(const a of[0,2.094,4.189]){const dx=Math.cos(a)*.009,dy=Math.sin(a)*.009;add(cub(.018,.0012,.0012),HIE,x+dx/2,z+.081,y+dy/2,-a);
   add(cub(.0055,.009,.0055),FAR,x+dx,z+.077,y+dy);add(new THREE.ConeGeometry(.0048,.0045,4),HIE,x+dx,z+.0838,y+dy,Math.PI/4);add(cil(.0016,.0016,.0018),HIE,x+dx,z+.0714,y+dy)}
  add(new THREE.SphereGeometry(.0022,8,6),HIE,x,z+.0835,y)};
 const banco=(x,y,a)=>{const z=gy(x,y);add(cub(.03,.0055,.009),GRA,x,z+.0028,y,a);add(cub(.03,.0012,.0016),MAD,x-Math.sin(a)*0,z+.0062,y,a)};
 const arbol=(x,y)=>{const z=gy(x,y);add(cub(.026,.007,.026),GRA,x,z+.0035,y);add(cil(.0016,.0022,.024),MAD,x,z+.019,y);add(new THREE.IcosahedronGeometry(.016,1),HOJ,x,z+.04,y);add(new THREE.IcosahedronGeometry(.011,1),HOJ,x+.006,z+.05,y-.004)};
 const caseta=(x,y,a)=>{const z=gy(x,y),c=Math.cos(a),s=Math.sin(a),L=(lx,lz)=>[x+lx*c+lz*s,y-lx*s+lz*c];const W=.042,H=.026;
  for(const[lx,lz]of[[-1,-1],[1,-1],[1,1],[-1,1]]){const p=L(lx*W/2,lz*W/2);add(cil(.0009,.0009,H),LONA,p[0],z+H/2,p[1])}
  for(const lz of[-1,1]){const p=L(0,lz*W/2);add(cub(W,.008,.0012),LONA,p[0],z+H-.004,p[1],a)}{const p=L(0,W/2);add(cub(W,.0012,.001),LONA,p[0],z+H-.004,p[1],a)}
  {const p=L(-W/2,0);add(cub(.0012,H*.85,W),LONA,p[0],z+H*.43,p[1],a);const q=L(W/2,0);add(cub(.0012,H*.85,W),LONA,q[0],z+H*.43,q[1],a)}
  {const p=L(0,-W/2+.002);add(cub(W*.98,H*.85,.0012),LONA,p[0],z+H*.43,p[1],a)}
  {const p=L(0,W/2-.006);add(cub(W*.92,.011,.008),ROJO,p[0],z+.0055,p[1],a);add(cub(W*.95,.0012,.01),MAD,p[0],z+.0115,p[1],a)}
  {const r=new THREE.ConeGeometry(W*.74,.02,4,1);add(r,LONA,x,z+H+.01,y,a+Math.PI/4);add(cil(.0006,.0006,.012),LONA,x,z+H+.025,y)}
  for(let k=0;k<=8;k++){const f=k/8-.5;for(const lz of[-1,1]){const p=L(f*W,lz*W/2+lz*.001);add(new THREE.SphereGeometry(.0011,5,4),BOM,p[0],z+H-.0005-Math.sin((k/8)*Math.PI)*.003,p[1])}}};
 // colocación: banda junto a las fachadas para farolas, bancos y árboles; casetas en el ancho de la plaza
 const ptsB=[],ptsC=[];for(let x=P.X0+.02;x<P.X1;x+=.025)for(let y=P.Y0+.02;y<P.Y1;y+=.025){if(t(x,y)!==1)continue;const ci=Math.round((x-MAPA.ox)*res),cj=Math.round((y-MAPA.oy)*res);if(!on.has(ci+','+cj))continue;
  const dT=Math.hypot(x-P.TX,y-P.TY);if(dT<.2)continue;if(near(x,y,.09,2)||near(x,y,.03,0)||near(x,y,.03,-1))continue;if(!libre(x,y)||!libre(x+.03,y)||!libre(x-.03,y)||!libre(x,y+.03)||!libre(x,y-.03))continue;
  if(near(x,y,.055,3)&&!near(x,y,.03,3))ptsB.push([x,y]);else if(!near(x,y,.085,3)&&dT>.24)ptsC.push([x,y])}
 const pick=(L,sp,max,ya)=>{const o=[];for(const p of L){if(o.length>=max)break;if(ya.some(q=>Math.hypot(q[0]-p[0],q[1]-p[1])<sp))continue;o.push(p);ya.push(p)}return o};
 const used=[];const dirP=(x,y)=>{let bx=0,by=0;for(let a=0;a<6.28;a+=.393){const dx=Math.cos(a)*.05,dy=Math.sin(a)*.05;if(t(x+dx,y+dy)===3){bx+=dx;by+=dy}}return Math.atan2(-by,bx)};
 ptsB.sort((a,b)=>Math.hypot(a[0]-P.TX,a[1]-P.TY)-Math.hypot(b[0]-P.TX,b[1]-P.TY));
 const fa=pick(ptsB,.15,14,used);for(const p of fa)farola(p[0],p[1]);
 const ba=pick(ptsB,.09,10,used);for(const p of ba)banco(p[0],p[1],dirP(p[0],p[1])+Math.PI/2);
 const ar=pick(ptsB,.12,5,used);for(const p of ar)arbol(p[0],p[1]);
 ptsC.sort((a,b)=>Math.abs(a[1]-17.86)-Math.abs(b[1]-17.86));
 const ca=pick(ptsC.filter(p=>p[0]<P.TX-.05),.075,5,used);for(const p of ca)caseta(p[0],p[1],0);
 P.n={farolas:fa.length,bancos:ba.length,arboles:ar.length,casetas:ca.length,ca:ca.map(p=>p.map(v=>+v.toFixed(3))),fa:fa.map(p=>p.map(v=>+v.toFixed(3)))};
 for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=mat!==BOM&&mat!==FAR;m.receiveShadow=true;G.add(m)}
 scene.add(G);P.G=G}
function subePaso(){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok portasol')
