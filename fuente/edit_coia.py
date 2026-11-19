f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= AVENIDA DE CASTELAO Y BARRIO DE COIA =================
# Google Earth solo como referencia: hileras de árboles y farolas en las aceras de Castelao, carril bici verde,
# y césped con arbolado en los espacios libres entre los bloques de viviendas de Coia (antes tierra beige).
r("function subeZonas(){psolChk();","function subeZonas(){psolChk();coiaChk();")
r("function subePaso(){",r"""const COIA={hecha:0,X0:56,X1:73.5,Y0:46,Y1:55.6};window.__COIA=COIA;
setInterval(()=>{if(!COIA.hecha)coiaChk()},3000);// subeZonas solo se llama al cargar zonas; las calles pueden llegar después
function coiaChk(){if(COIA.hecha||!MAPA||!MI||!CALLES)return;if(sueloRap(64.6,51.6)==null||sueloRap(60,52.2)==null||sueloRap(68,51.2)==null)return;COIA.hecha=1;setTimeout(()=>{try{coiaCrea()}catch(e){console.warn('coia',e);COIA.err=String(e)}},1200)}
function coiaCrea(){const LT=!!window.LITE,G=new THREE.Group();G.name='coia';const t=(x,y)=>cell(x,y).t,gy=(x,y)=>sueloRap(x,y);
 let rs=17;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.85},o));
 const HIE=M(0x3a3f46,{metalness:.5,roughness:.45}),LUZ=M(0xfff2cc,{emissive:0xffd88a,emissiveIntensity:.9}),TRO=M(0x6b4a32),
  CES=new THREE.MeshStandardMaterial({color:0xffffff,vertexColors:true,roughness:1,polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-1}),
  BICI=new THREE.MeshStandardMaterial({color:0x3f9a63,roughness:.9,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3,side:THREE.DoubleSide}),RAYA=M(0xf4f4f0,{polygonOffset:true,polygonOffsetFactor:-4,polygonOffsetUnits:-4});
 const PARTS=new Map(),add=(geo,mat,x,y,z,ry=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();if(g.attributes.uv)g.deleteAttribute('uv');g.rotateY(ry);g.translate(x,y,z);if(!PARTS.has(mat))PARTS.set(mat,[]);PARTS.get(mat).push(g)};
 const TR=[];// árboles: [x,y,tipo,escala]
 // distancia a calzada (2) y a edificio (3) en el mapa de celdas, muestreando en anillos
 const cerca=(x,y,tt,r)=>{for(let a=0;a<6.283;a+=.785){if(t(x+Math.cos(a)*r,y+Math.sin(a)*r)===tt)return true}return t(x,y)===tt};
 // 1) Avenida de Castelao: árboles y farolas en las aceras, carril bici en el lado norte
 const L=[];for(const[nm,c,ls]of CALLES){if(nm!=='Avenida de Castelao')continue;for(const l of ls){const P=[];for(let i=0;i+1<l.length;i+=2)P.push([l[i],l[i+1]]);if(P.length<2)continue;const Q=[P[0]];for(let i=0;i<P.length-1;i++){const a=P[i],b=P[i+1],d=Math.hypot(b[0]-a[0],b[1]-a[1]),n=Math.max(1,Math.round(d/.05));for(let k=1;k<=n;k++)Q.push([a[0]+(b[0]-a[0])*k/n,a[1]+(b[1]-a[1])*k/n])}if(Q.length>6)L.push(Q)}}
 let nAv=0,nF=0;const bici=[];
 for(const Q of L)for(let i=1;i<Q.length-1;i++){const a=Q[i-1],b=Q[i+1],l=Math.hypot(b[0]-a[0],b[1]-a[1])||1,tx=(b[0]-a[0])/l,ty=(b[1]-a[1])/l,nx=-ty,ny=tx,[x,y]=Q[i];
  for(const sd of[1,-1]){let d=.02;for(;d<.26;d+=.01)if(t(x+nx*sd*d,y+ny*sd*d)!==2)break;if(d>=.26)continue;const ex=x+nx*sd*d,ey=y+ny*sd*d;const tt=t(ex,ey);if(tt===0||tt===3)continue;
   // acera: el árbol a 2 m del bordillo, si no hay otra calle ni edificio pegados
   const px=ex+nx*sd*.028,py=ey+ny*sd*.028;
   if(i%3===0&&t(px,py)!==2&&t(px,py)!==3&&!cerca(px,py,3,.025)&&t(px+tx*.05,py+ty*.05)!==2&&t(px-tx*.05,py-ty*.05)!==2){TR.push([px,py,0,.85+rn()*.3]);nAv++}
   if(i%7===3){const lx=ex+nx*sd*.012,ly=ey+ny*sd*.012,lz=gy(lx,ly);if(lz!=null&&t(lx,ly)!==2){add(new THREE.CylinderGeometry(.0011,.0015,.055,6),HIE,lx,lz+.0275,ly);add(new THREE.BoxGeometry(.016,.0016,.0016),HIE,lx-nx*sd*.007,lz+.055,ly-ny*sd*.007,-Math.atan2(ny,nx));add(new THREE.BoxGeometry(.008,.003,.005),LUZ,lx-nx*sd*.014,lz+.0535,ly-ny*sd*.014,-Math.atan2(ny,nx));nF++}}
   // carril bici sobre la acera del lado norte (normal hacia y menor)
   if(ny*sd<-.3){const bx=ex+nx*sd*.05,by=ey+ny*sd*.05;bici.push([bx,by,nx*sd,ny*sd,t(bx,by)!==2&&t(bx,by)!==3])}}}
 // cinta verde del carril bici (tramos continuos)
 {let cur=[];const flush=()=>{if(cur.length>3){const pos=[],idx=[],W=.011;for(let k=0;k<cur.length;k++){const[x,y,nx,ny]=cur[k];const z1=gy(x+nx*W,y+ny*W),z2=gy(x-nx*W,y-ny*W);if(z1==null||z2==null)return;pos.push(x+nx*W,z1+.003,y+ny*W,x-nx*W,z2+.003,y-ny*W);if(k<cur.length-1){const q=k*2;idx.push(q,q+1,q+2,q+1,q+3,q+2)}}
    const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setIndex(idx);g.computeVertexNormals();const m=new THREE.Mesh(g,BICI);m.receiveShadow=true;G.add(m);COIA.bici=(COIA.bici||0)+cur.length}cur=[]};
  for(const p of bici){if(p[4])cur.push(p);else flush()}flush()}
 COIA.av=nAv;COIA.farolas=nF;
 // 2) Coia: césped y árboles en los espacios libres entre bloques (lejos de calles y fachadas)
 const st=.05,pos=[],col=[],c0=new THREE.Color(0x7fb35a),c1=new THREE.Color(0x6aa64b),cc=new THREE.Color();let nC=0;
 const libre=(x,y)=>t(x,y)===1&&!cerca(x,y,2,.06)&&!cerca(x,y,3,.03)&&!cerca(x,y,0,.05);
 const H=new Map(),hz=(i,j)=>{const k=i+','+j;if(!H.has(k))H.set(k,gy(i*st,j*st));return H.get(k)};
 for(let i=Math.floor(COIA.X0/st);i<COIA.X1/st;i++)for(let j=Math.floor(COIA.Y0/st);j<COIA.Y1/st;j++){const x=(i+.5)*st,y=(j+.5)*st;if(!libre(x,y))continue;
  const za=hz(i,j),zb=hz(i+1,j),zc=hz(i+1,j+1),zd=hz(i,j+1);if(za==null||zb==null||zc==null||zd==null)continue;
  const A=[i*st,za+.004,j*st],B=[(i+1)*st,zb+.004,j*st],C=[(i+1)*st,zc+.004,(j+1)*st],D=[i*st,zd+.004,(j+1)*st];
  pos.push(...A,...D,...C,...A,...C,...B);const n=.5+.5*Math.sin(x*7.3+Math.sin(y*5.1)*2);cc.copy(c0).lerp(c1,n);for(let k=0;k<6;k++)col.push(cc.r,cc.g,cc.b);nC++;
  if(rn()<(LT?.06:.11)){const ox=x+(rn()-.5)*st*.8,oy=y+(rn()-.5)*st*.8;if(libre(ox,oy))TR.push([ox,oy,rn()<.7?1:2,.8+rn()*.5])}}
 if(pos.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.computeVertexNormals();const m=new THREE.Mesh(g,CES);m.receiveShadow=true;G.add(m)}
 COIA.cesped=nC;
 // árboles instanciados: plátanos de sombra (avenida), frondosos y pinos (zonas verdes)
 {const esp=[{tr:new THREE.CylinderGeometry(.0022,.003,1,5).translate(0,.5,0),cp:new THREE.IcosahedronGeometry(1,1),h:.05,r:.02,sy:1.25,cy:.95,col:[0x4f8f3a,0x5a9a44,0x467f35]},
   {tr:new THREE.CylinderGeometry(.0025,.0035,1,5).translate(0,.5,0),cp:new THREE.IcosahedronGeometry(1,0),h:.045,r:.022,sy:.95,cy:.85,col:[0x3f7d34,0x4c8f3a,0x356b2c]},
   {tr:new THREE.CylinderGeometry(.002,.003,1,5).translate(0,.5,0),cp:new THREE.ConeGeometry(1,1.8,7).translate(0,.9,0),h:.03,r:.016,sy:1,cy:.5,col:[0x2a5a2e,0x315f34]}];
  const trM=new THREE.MeshStandardMaterial({color:0x6b4a32,roughness:1}),cpM=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9,flatShading:true});
  const mm=new THREE.Matrix4(),q=new THREE.Quaternion(),e=new THREE.Euler(),co=new THREE.Color();
  esp.forEach((E,si)=>{const Ls=TR.filter(p=>p[2]===si);if(!Ls.length)return;const it=new THREE.InstancedMesh(E.tr,trM,Ls.length),ic=new THREE.InstancedMesh(E.cp,cpM,Ls.length);
   Ls.forEach(([x,y,,s_],i)=>{const z=(gy(x,y)??0)-.002,h=E.h*s_,r_=E.r*s_;e.set(0,rn()*6.28,0);q.setFromEuler(e);
    mm.compose(new THREE.Vector3(x,z,y),q,new THREE.Vector3(1,h,1));it.setMatrixAt(i,mm);
    mm.compose(new THREE.Vector3(x,z+h*E.cy,y),q,new THREE.Vector3(r_,si===2?h*.7:r_*E.sy,r_));ic.setMatrixAt(i,mm);co.setHex(E.col[(rn()*E.col.length)|0]).offsetHSL(0,0,(rn()-.5)*.06);ic.setColorAt(i,co)});
   it.castShadow=ic.castShadow=!LT;ic.receiveShadow=true;G.add(it,ic)})}
 COIA.arboles=TR.length;
 for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=!LT&&mat!==LUZ;m.receiveShadow=true;G.add(m)}
 scene.add(G);COIA.G=G}
function subePaso(){""")
open(f,'w').write(s)
print('ok coia')
