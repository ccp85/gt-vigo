f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= CENTRO DE VIGO (Príncipe, Porta do Sol, Casco Vello y avenidas) =================
# Zona de Príncipe, Porta do Sol, Colón, Policarpo Sanz, Velázquez Moreno y el arranque de Urzáiz. Antes las calles peatonales eran suelo beige liso y vacío. Ahora:
#  - enlosado de granito en las peatonales (Príncipe, Porta do Sol, Velázquez Moreno, Casco Vello...)
#  - farolas de fundición, bancos, jardineras con flores y terrazas de bar con sombrillas
#  - plátanos de sombra con alcorque en las aceras de las avenidas que no tenían árboles
# El ancho libre de cada calle se mide con rayos contra los edificios reales (no con el mapa de celdas, que es más grueso).
r("function subeZonas(){psolChk();","function subeZonas(){psolChk();ctrChk();")
r("function subePaso(){",r"""const CTR={hecha:0,X0:85.8,X1:100,Y0:13.8,Y1:25};window.__CTR=CTR;
setInterval(()=>{if(!CTR.hecha)ctrChk()},3000);
function ctrChk(){if(CTR.hecha||!MAPA||!CALLES)return;for(const[x,y]of[[90,19.13],[87,19],[92.5,17.8],[95,18.1]])if(sueloRap(x,y)==null)return;
 // los edificios del centro tienen que estar ya en escena
 if(repAltura(90.08,19.6,repMallas(90.08,19.6))<0)return;CTR.hecha=1;setTimeout(()=>{try{ctrCrea()}catch(e){console.warn('centro',e);CTR.err=String(e)}},1500)}
function ctrCrea(){const LT=!!window.LITE,G=new THREE.Group();G.name='centro_calles';
 let rs=29;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const t=(x,y)=>cell(x,y).t,gy=(x,y)=>sueloRap(x,y);
 const ocup=(x,y)=>{const g=gy(x,y);if(g==null)return true;return repAltura(x,y,repMallas(x,y))>g+.012};
 const libre=(x,y)=>{const c=t(x,y);return c!==2&&c!==0&&!ocup(x,y)};
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.85},o));
 // enlosado de granito: losas grandes con juntas, en coordenadas de mundo
 const losa=(()=>{const cv=document.createElement('canvas');cv.width=cv.height=128;const x=cv.getContext('2d');x.fillStyle='#7d7972';x.fillRect(0,0,128,128);
  let r2=5;const rr=()=>(r2=(r2*16807)%2147483647)/2147483647;
  // granito gris claro en losas de 2 x 1 con juntas marcadas y una franja de granito oscuro atravesada
  for(let j=0;j<8;j++)for(let i=0;i<4;i++){const v=(j===0)?118+((rr()*14)|0):168+((rr()*26)|0),o=(j%2)*16;x.fillStyle=`rgb(${v},${v-3},${v-9})`;
   for(const dx of[0,128]){x.fillRect(i*32+o+1-dx,j*16+1,30,14)}
   for(let k=0;k<26;k++){const g=v-30+((rr()*60)|0);x.fillStyle=`rgba(${g},${g},${g-4},.45)`;x.fillRect((i*32+o+rr()*30)%128,j*16+1+rr()*14,1.2,1.2)}}
  const tx=new THREE.CanvasTexture(cv);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.colorSpace=THREE.SRGBColorSpace;tx.anisotropy=8;return tx})();
 const PAV=new THREE.MeshStandardMaterial({map:losa,roughness:.9,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2});
 const FUN=M(0x1f2a26,{metalness:.55,roughness:.45}),LUZ=M(0xfff3d0,{emissive:0xffd88a,emissiveIntensity:1}),GRA=M(0xb9b2a6,{roughness:.95}),
  MAD=M(0x7a5434),VER=M(0x3f7a35),FLO=[M(0xd8436b),M(0xf2c14e),M(0xe8e4f0)],MES=M(0xe9e6df,{metalness:.3,roughness:.5}),SIL=M(0xa7abae,{metalness:.15,roughness:.5}),
  TOL=[M(0xf3efe4),M(0xb23a3a),M(0x2f6b4f),M(0xe9d9a8),M(0x2c4a7a)],ALC=M(0x34383b,{metalness:.4,roughness:.6}),PAP=M(0x3d5a3a,{metalness:.3,roughness:.6});
 const PARTS=new Map(),add=(geo,mat,x,y,z,ry=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();if(g.attributes.uv)g.deleteAttribute('uv');g.rotateY(ry);g.translate(x,y,z);if(!PARTS.has(mat))PARTS.set(mat,[]);PARTS.get(mat).push(g)};
 const GEO={poste:new THREE.CylinderGeometry(.0008,.0013,.046,6),base:new THREE.CylinderGeometry(.0022,.0026,.006,8),farol:new THREE.CylinderGeometry(.0034,.0018,.007,6),
  tapa:new THREE.ConeGeometry(.0042,.003,6),banco:new THREE.BoxGeometry(.022,.0016,.006),resp:new THREE.BoxGeometry(.022,.005,.0012),pata:new THREE.BoxGeometry(.0012,.004,.005),
  jard:new THREE.BoxGeometry(.03,.007,.012),mata:new THREE.IcosahedronGeometry(1,0),flor:new THREE.BoxGeometry(.026,.0022,.008),
  mesa:new THREE.CylinderGeometry(.0045,.0045,.0007,10),pie:new THREE.CylinderGeometry(.0004,.0004,.0055,4),silla:new THREE.BoxGeometry(.0042,.0055,.0042),
  palo:new THREE.CylinderGeometry(.0004,.0004,.026,4),toldo:new THREE.ConeGeometry(.017,.006,8),alc:new THREE.BoxGeometry(.014,.0012,.014),alto:new THREE.CylinderGeometry(.0009,.0015,.07,6),brazo:new THREE.BoxGeometry(.018,.0012,.0012),foco:new THREE.BoxGeometry(.008,.0018,.0035),pap:new THREE.CylinderGeometry(.0024,.0022,.009,8)};
 // polilíneas densificadas cada d
 const dens=(l,d)=>{const P=[];for(let i=0;i+1<l.length;i+=2)P.push([l[i],l[i+1]]);if(P.length<2)return null;const Q=[P[0]];for(let i=0;i<P.length-1;i++){const a=P[i],b=P[i+1],L_=Math.hypot(b[0]-a[0],b[1]-a[1]),n=Math.max(1,Math.round(L_/d));for(let k=1;k<=n;k++)Q.push([a[0]+(b[0]-a[0])*k/n,a[1]+(b[1]-a[1])*k/n])}return Q};
 const dentro=(x,y)=>x>CTR.X0&&x<CTR.X1&&y>CTR.Y0&&y<CTR.Y1;
 const PEAT=[],AVS=[];
 for(const[nm,c,ls]of CALLES){for(const l of ls){const Q=dens(l,.04);if(!Q||!Q.some(p=>dentro(...p)))continue;
  if((c===4||c===5)&&Q.every(p=>p[0]<95&&p[1]<23))PEAT.push(Q);else if((c===1||c===2||c===3)&&!/Túnel|Autoestrada|Beiramar/.test(nm))AVS.push(Q)}}
 const tareas=[];
 // ---------- 1) peatonales ----------
 const seg=[];// muestras: [x,y,nx,ny,tx,ty,wIzq,wDer]
 for(const Q of PEAT)tareas.push(()=>{let run=[];const fin=()=>{if(run.length>2)seg.push(run);run=[]};
  for(let i=0;i<Q.length;i++){const a=Q[Math.max(0,i-1)],b=Q[Math.min(Q.length-1,i+1)],L_=Math.hypot(b[0]-a[0],b[1]-a[1])||1,tx=(b[0]-a[0])/L_,ty=(b[1]-a[1])/L_,nx=-ty,ny=tx,[x,y]=Q[i];
   if(!dentro(x,y)||!libre(x,y)){fin();continue}
   const w=[0,0];for(const[k,sd]of[[0,1],[1,-1]]){let d=.01;for(;d<=.13;d+=.01)if(!libre(x+nx*sd*d,y+ny*sd*d))break;w[k]=d-.012}
   if(w[0]+w[1]<.035){fin();continue}run.push([x,y,nx,ny,tx,ty,w[0],w[1]])}fin()});
 tareas.push(()=>{const pos=[],uv=[],idx=[];let nL=0,nB=0,nJ=0,nT=0,acum=0;
  for(const run of seg){let base=pos.length/3,u=0;
   for(let k=0;k<run.length;k++){const[x,y,nx,ny,tx,ty,wa,wb]=run[k];if(k)u+=Math.hypot(x-run[k-1][0],y-run[k-1][1]);
    const ax=x+nx*wa,ay=y+ny*wa,bx=x-nx*wb,by=y-ny*wb,za=gy(ax,ay)??gy(x,y),zb=gy(bx,by)??gy(x,y);
    pos.push(ax,za+.0025,ay,bx,zb+.0025,by);uv.push(u/.11,wa/.055,u/.11,-wb/.055);
    if(k<run.length-1){const q=base+k*2;idx.push(q,q+1,q+2,q+1,q+3,q+2)}
    // mobiliario a lo largo de la calle
    acum+=.04;const z=gy(x,y)??0,ang=-Math.atan2(ty,tx),W=wa+wb;
    if(k%7===3){const sd=(nL%2)?1:-1,w_=sd>0?wa:wb,lx=x+nx*sd*(w_-.012),ly=y+ny*sd*(w_-.012),lz=gy(lx,ly);
     if(lz!=null&&w_>.025){add(GEO.base,FUN,lx,lz+.003,ly);add(GEO.poste,FUN,lx,lz+.029,ly);add(GEO.farol,LUZ,lx,lz+.0555,ly);add(GEO.tapa,FUN,lx,lz+.0605,ly);nL++}}
    if(k%11===6&&W>.07){const sd=(nB%2)?-1:1,w_=sd>0?wa:wb,bx_=x+nx*sd*(w_-.026),by_=y+ny*sd*(w_-.026),bz=gy(bx_,by_);
     if(bz!=null&&w_>.04&&libre(bx_,by_)){add(GEO.banco,MAD,bx_,bz+.0045,by_,ang);add(GEO.resp,MAD,bx_+nx*sd*.003,bz+.007,by_+ny*sd*.003,ang);
      for(const s_ of[-.009,.009])add(GEO.pata,FUN,bx_+tx*s_,bz+.002,by_+ty*s_,ang);nB++}}
    if(k%13===0&&W>.1){const cx=x+nx*(wa-wb)/2,cy=y+ny*(wa-wb)/2,cz=gy(cx,cy);
     if(cz!=null){add(GEO.jard,GRA,cx,cz+.0035,cy,ang);add(GEO.flor,FLO[nJ%3],cx,cz+.008,cy,ang);
      const mg=GEO.mata.clone().scale(.006,.008,.006);add(mg,VER,cx+tx*.008,cz+.012,cy+ty*.008);add(mg,VER,cx-tx*.008,cz+.011,cy-ty*.008);nJ++}}
    // terrazas de bar: mesas con cuatro sillas y sombrilla, pegadas a una fachada
    if(k%9===4&&W>(LT?.11:.085)&&rn()<.75){const sd=(nT%2)?1:-1,w_=sd>0?wa:wb;if(w_>.045){const n_=LT?1:2+((rn()*2)|0);
     for(let m=0;m<n_;m++){const off=(m-(n_-1)/2)*.022,mx=x+nx*sd*(w_-.022)+tx*off,my=y+ny*sd*(w_-.022)+ty*off,mz=gy(mx,my);if(mz==null||!libre(mx,my))continue;
      add(GEO.pie,SIL,mx,mz+.0028,my);add(GEO.mesa,MES,mx,mz+.0058,my);
      for(let c=0;c<4;c++){const a=c*Math.PI/2+.4;add(GEO.silla,SIL,mx+Math.cos(a)*.0068,mz+.0028,my+Math.sin(a)*.0068,a)}
      add(GEO.palo,MES,mx,mz+.013,my);add(GEO.toldo,TOL[(nT+m)%TOL.length],mx,mz+.0265,my)}nT++}}}
  }
  if(pos.length){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();
   const m=new THREE.Mesh(g,PAV);m.receiveShadow=true;m.name='enlosado';G.add(m)}
  CTR.peat=seg.length;CTR.muestras=seg.reduce((a,b)=>a+b.length,0);CTR.farolas=nL;CTR.bancos=nB;CTR.jardineras=nJ;CTR.terrazas=nT});
 // ---------- 2) plátanos en las aceras de las avenidas ----------
 const TR=[],FAR=[];const yaHay=[];
 tareas.push(()=>{scene.traverse(o=>{if(!o.isInstancedMesh||!/arbol|bosque/.test(o.name))return;const mm=new THREE.Matrix4(),p=new THREE.Vector3();
  for(let k=0;k<o.instanceMatrix.count;k++){o.getMatrixAt(k,mm);p.setFromMatrixPosition(mm).applyMatrix4(o.matrixWorld);if(dentro(p.x,p.z))yaHay.push([p.x,p.z])}})});
 const cerca=(x,y,L,r)=>L.some(p=>Math.abs(p[0]-x)<r&&Math.abs(p[1]-y)<r&&Math.hypot(p[0]-x,p[1]-y)<r);
 for(const Q of AVS)tareas.push(()=>{for(let i=2;i<Q.length-2;i+=5){const a=Q[i-1],b=Q[i+1],L_=Math.hypot(b[0]-a[0],b[1]-a[1])||1,tx=(b[0]-a[0])/L_,ty=(b[1]-a[1])/L_,nx=-ty,ny=tx,[x,y]=Q[i];if(!dentro(x,y))continue;
  for(const sd of[1,-1]){let d=.02;for(;d<.2;d+=.01)if(t(x+nx*sd*d,y+ny*sd*d)!==2)break;if(d>=.2)continue;
   const px=x+nx*sd*(d+.018),py=y+ny*sd*(d+.018);
   // la acera tiene que ser lo bastante ancha: sitio libre a 1,5 m alrededor del árbol y fachada a más de 3 m
   if(t(px,py)===2||!libre(px,py)||!libre(px+nx*sd*.022,py+ny*sd*.022)||!libre(px+tx*.03,py+ty*.03)||!libre(px-tx*.03,py-ty*.03))continue;
   if(t(px+tx*.06,py+ty*.06)===2||t(px-tx*.06,py-ty*.06)===2)continue;// no en las esquinas
   if(cerca(px,py,yaHay,.06)||cerca(px,py,TR,.11))continue;TR.push([px,py,.85+rn()*.35])}}
  // farolas altas de brazo junto al bordillo y alguna papelera
  for(let i=4;i<Q.length-4;i+=8){const a=Q[i-1],b=Q[i+1],L_=Math.hypot(b[0]-a[0],b[1]-a[1])||1,tx=(b[0]-a[0])/L_,ty=(b[1]-a[1])/L_,nx=-ty,ny=tx,[x,y]=Q[i];if(!dentro(x,y))continue;
   const sd=(i/8|0)%2?1:-1;let d=.02;for(;d<.2;d+=.01)if(t(x+nx*sd*d,y+ny*sd*d)!==2)break;if(d>=.2)continue;const px=x+nx*sd*(d+.006),py=y+ny*sd*(d+.006),pz=gy(px,py);
   if(pz==null||t(px,py)===2||!libre(px,py)||cerca(px,py,TR,.04)||cerca(px,py,FAR,.2))continue;FAR.push([px,py]);
   const ang=Math.atan2(-ny*sd,-nx*sd);add(GEO.alto,FUN,px,pz+.035,py);add(GEO.brazo,FUN,px-nx*sd*.009,pz+.069,py-ny*sd*.009,-ang);add(GEO.foco,LUZ,px-nx*sd*.018,pz+.067,py-ny*sd*.018,-ang);
   if(rn()<.45){const bx_=px+tx*.03,by_=py+ty*.03;if(libre(bx_,by_))add(GEO.pap,PAP,bx_,(gy(bx_,by_)??pz)+.0045,by_)}}});
 tareas.push(()=>{if(!TR.length)return;const trG=new THREE.CylinderGeometry(.0018,.0026,1,5).translate(0,.5,0),cpG=new THREE.IcosahedronGeometry(1,1);
  const trM=new THREE.MeshStandardMaterial({color:0x8a7a62,roughness:1}),cpM=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9,flatShading:true});
  const it=new THREE.InstancedMesh(trG,trM,TR.length),ic=new THREE.InstancedMesh(cpG,cpM,TR.length),mm=new THREE.Matrix4(),q=new THREE.Quaternion(),e=new THREE.Euler(),co=new THREE.Color(),cols=[0x5c8f3e,0x679a46,0x52833a,0x6fa04c];
  TR.forEach(([x,y,s_],i)=>{const z=(gy(x,y)??0)-.001,h=.042*s_,r_=.019*s_;e.set(0,rn()*6.28,0);q.setFromEuler(e);
   mm.compose(new THREE.Vector3(x,z,y),q,new THREE.Vector3(1,h,1));it.setMatrixAt(i,mm);
   mm.compose(new THREE.Vector3(x,z+h*.98,y),q,new THREE.Vector3(r_,r_*1.15,r_));ic.setMatrixAt(i,mm);co.setHex(cols[(rn()*cols.length)|0]).offsetHSL(0,0,(rn()-.5)*.05);ic.setColorAt(i,co);
   add(GEO.alc,ALC,x,z+.0016,y)});
  it.castShadow=ic.castShadow=!LT;ic.receiveShadow=true;it.name=ic.name='platanos_centro';G.add(it,ic);CTR.arboles=TR.length});
 tareas.push(()=>{for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=!LT&&mat!==LUZ&&mat!==ALC;m.receiveShadow=true;G.add(m)}
  scene.add(G);CTR.G=G;CTR.lista=1});
 // se reparte en pasos para no congelar la imagen
 const paso=()=>{const t0=performance.now();CTR.quedan=tareas.length;while(tareas.length&&performance.now()-t0<12){const f_=tareas.shift();try{f_()}catch(e){console.warn('centro',e);CTR.err=String(e)}}if(tareas.length)setTimeout(paso,30)};paso()}
function subePaso(){""")
open(f,'w').write(s)
print('ok centro')
