f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= ENTRADA DE VIGO POR LA AP-9 (Teis → Vialia) =================
# Google Earth solo como referencia: mediana de hormigón con farolas dobles, barreras New Jersey, pantallas antirruido
# en Teis, taludes de césped con arbustos y árboles, pórticos con carteles azules de destino y un monolito de bienvenida.
r("function subeZonas(){psolChk();samChk();casChk();cstChk();","function subeZonas(){psolChk();samChk();casChk();cstChk();apChk();")
r("function subePaso(){",r"""const AP={L:null,hecho:new Set(),t:0,G:null};window.__AP=AP;
function apChk(){if(!CALLES||!MAPA||!MI)return;const n=performance.now();if(n-AP.t<2000)return;AP.t=n;try{apCrea()}catch(e){console.warn('ap9',e);AP.err=String(e)}}
function apCrea(){const LT=!!window.LITE;
 if(!AP.L){AP.L=[];for(const[nm,c,ls]of CALLES){if(nm!=='Autoestrada do Atlántico')continue;for(const l of ls){const P=[];for(let i=0;i+1<l.length;i+=2)if(l[i]<126&&l[i+1]>-3&&l[i+1]<21)P.push([l[i],l[i+1]]);if(P.length>1)AP.L.push(P)}}
  // remuestreo cada 0.05
  AP.L=AP.L.map(P=>{const Q=[P[0]];for(let i=0;i<P.length-1;i++){const a=P[i],b=P[i+1],L=Math.hypot(b[0]-a[0],b[1]-a[1]),n=Math.max(1,Math.round(L/.05));for(let k=1;k<=n;k++)Q.push([a[0]+(b[0]-a[0])*k/n,a[1]+(b[1]-a[1])*k/n])}return Q}).filter(Q=>Q.length>8);
  const G=new THREE.Group();G.name='ap9';scene.add(G);AP.G=G;
  const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.85},o));
  AP.MAT={HOR:M(0xc9c6bd,{roughness:.95}),HOR2:M(0xa9a59b),CES:new THREE.MeshStandardMaterial({color:0x76a84f,roughness:1,polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-1,side:THREE.DoubleSide}),
   PAN:new THREE.MeshStandardMaterial({color:0x8fc1c9,roughness:.2,metalness:.1,transparent:true,opacity:.55,side:THREE.DoubleSide}),PANM:M(0x6f8f7a),HIE:M(0x5d6670,{metalness:.6,roughness:.4}),LUZ:M(0xfff2cc,{emissive:0xffd88a,emissiveIntensity:1}),
   ARB:M(0x3f7d34,{flatShading:true}),ARB2:M(0x4f8f3a,{flatShading:true}),TRO:M(0x6b4a32),PIE:M(0xd9d4c7,{roughness:.9})};
  AP.cartel=(lineas,ancho)=>{const c=document.createElement('canvas');c.width=512;c.height=Math.round(512*.32);const x=c.getContext('2d');x.fillStyle='#1f4fa3';x.fillRect(0,0,c.width,c.height);x.strokeStyle='#fff';x.lineWidth=6;x.strokeRect(8,8,c.width-16,c.height-16);
   x.fillStyle='#fff';x.textBaseline='middle';const h=c.height/(lineas.length+1);lineas.forEach((t,i)=>{x.font=(i===0?'bold 58px':'44px')+' "Russo One",Arial,sans-serif';x.fillText(t,28,h*(i+1))});const tx=new THREE.CanvasTexture(c);tx.colorSpace=THREE.SRGBColorSpace;tx.anisotropy=4;return new THREE.MeshStandardMaterial({map:tx,roughness:.5,emissive:0x0a1e40,emissiveIntensity:.25})};
 }
 const L=AP.L,MT=AP.MAT,t=(x,y)=>cell(x,y).t,gy=(x,y)=>sueloRap(x,y);
 // anchura de cada calzada a cada lado, medida en el mapa de celdas
 const ancho=(x,y,nx,ny)=>{let d=.02;for(;d<.22;d+=.01)if(t(x+nx*d,y+ny*d)!==2)break;return d};
 let nuevos=0;
 L.forEach((P,li)=>{
  // sentido: hacia Vigo si avanza hacia el oeste
  const entra=(P[P.length-1][0]-P[0][0])<0;
  // trozos de 20 muestras; cada trozo se construye una vez cuando su suelo ya está cargado
  for(let c0=0;c0<P.length-1;c0+=20){const key=li+':'+c0;if(AP.hecho.has(key))continue;const c1=Math.min(P.length-1,c0+20);let ok=true;for(let i=c0;i<=c1;i+=4)if(gy(P[i][0],P[i][1])==null){ok=false;break}if(!ok)continue;AP.hecho.add(key);nuevos++;
   const parts=new Map(),add=(geo,mat,x,y,z,ry=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();if(g.attributes.uv)g.deleteAttribute('uv');g.rotateY(ry);g.translate(x,y,z);if(!parts.has(mat))parts.set(mat,[]);parts.get(mat).push(g)},raw=new Map(),quad=(mat,a,b,c,d)=>{if(!raw.has(mat))raw.set(mat,[]);raw.get(mat).push(...a,...b,...c,...a,...c,...d)};
   const S=[];for(let i=Math.max(0,c0-1);i<=Math.min(P.length-1,c1+1);i++){const a=P[Math.max(0,i-1)],b=P[Math.min(P.length-1,i+1)];const l=Math.hypot(b[0]-a[0],b[1]-a[1])||1;const nx=-(b[1]-a[1])/l,ny=(b[0]-a[0])/l,[x,y]=P[i];S.push({i,x,y,nx,ny,tx:(b[0]-a[0])/l,ty:(b[1]-a[1])/l,wl:ancho(x,y,nx,ny),wr:ancho(x,y,-nx,-ny)})}
   for(let k=1;k<S.length-1;k++){S[k].wl=(S[k-1].wl+2*S[k].wl+S[k+1].wl)/4;S[k].wr=(S[k-1].wr+2*S[k].wr+S[k+1].wr)/4}
   for(let k=0;k<S.length-1;k++){const A=S[k],B=S[k+1];if(A.i<c0||B.i>c1)continue;
    for(const sd of[1,-1]){const wa=(sd>0?A.wl:A.wr)+.006,wb=(sd>0?B.wl:B.wr)+.006;const pa=[A.x+A.nx*sd*wa,A.y+A.ny*sd*wa],pb=[B.x+B.nx*sd*wb,B.y+B.ny*sd*wb];const ga=gy(...pa),gb=gy(...pb);if(ga==null||gb==null)continue;
     // barrera New Jersey de hormigón
     const o=.004;quad(MT.HOR,[pa[0],ga-.002,pa[1]],[pb[0],gb-.002,pb[1]],[pb[0],gb+.012,pb[1]],[pa[0],ga+.012,pa[1]]);
     quad(MT.HOR2,[pa[0],ga+.012,pa[1]],[pb[0],gb+.012,pb[1]],[pb[0]+B.nx*sd*o,gb+.012,pb[1]+B.ny*sd*o],[pa[0]+A.nx*sd*o,ga+.012,pa[1]+A.ny*sd*o]);
     quad(MT.HOR,[pa[0]+A.nx*sd*o,ga+.012,pa[1]+A.ny*sd*o],[pb[0]+B.nx*sd*o,gb+.012,pb[1]+B.ny*sd*o],[pb[0]+B.nx*sd*o,gb-.002,pb[1]+B.ny*sd*o],[pa[0]+A.nx*sd*o,ga-.002,pa[1]+A.ny*sd*o]);
     // por fuera de la barrera: ¿hay más autopista (mediana) o tierra libre?
     const fx=(pa[0]+pb[0])/2+A.nx*sd*.05,fy=(pa[1]+pb[1])/2+A.ny*sd*.05,lado=t(fx,fy);
     if(lado===2){// mediana: farola doble cada 8 muestras
      if(A.i%8===0&&sd>0){const mx=pa[0]+A.nx*.02,my=pa[1]+A.ny*.02,mz=gy(mx,my);if(mz!=null){add(new THREE.CylinderGeometry(.0013,.0018,.075,6),MT.HIE,mx,mz+.0375,my);for(const s2 of[-1,1]){const bx=mx+A.nx*s2*.018,by=my+A.ny*s2*.018;add(new THREE.BoxGeometry(.036,.0018,.0018),MT.HIE,(mx+bx)/2,mz+.074,(my+by)/2,-Math.atan2(A.ny,A.nx));add(new THREE.BoxGeometry(.012,.003,.006),MT.LUZ,bx,mz+.0725,by,-Math.atan2(A.ny,A.nx))}}}
     }else{
      // tramo de Teis: pantalla antirruido sobre la barrera exterior
      if(A.y>7.5&&A.y<16.8&&!LT){const h=.034;quad(MT.PAN,[pa[0],ga+.012,pa[1]],[pb[0],gb+.012,pb[1]],[pb[0],gb+.012+h,pb[1]],[pa[0],ga+.012+h,pa[1]]);if(A.i%3===0)add(new THREE.BoxGeometry(.0025,h+.002,.0025),MT.PANM,pa[0],ga+.012+h/2,pa[1])}
      // talud de césped hasta 0.18 fuera de la barrera, solo sobre terreno libre
      const W=.18,q1=[pa[0]+A.nx*sd*.006,pa[1]+A.ny*sd*.006],q2=[pb[0]+B.nx*sd*.006,pb[1]+B.ny*sd*.006],q3=[pb[0]+B.nx*sd*W,pb[1]+B.ny*sd*W],q4=[pa[0]+A.nx*sd*W,pa[1]+A.ny*sd*W];
      if(t(...q3)===1&&t(...q4)===1&&t((q3[0]+q4[0])/2,(q3[1]+q4[1])/2)===1){const z3=gy(...q3),z4=gy(...q4);if(z3!=null&&z4!=null){quad(MT.CES,[q1[0],ga+.002,q1[1]],[q2[0],gb+.002,q2[1]],[q3[0],z3+.002,q3[1]],[q4[0],z4+.002,q4[1]]);
        if(A.i%3===0){const u=.05+((A.i*37)%11)/11*.11,ax=pa[0]+A.nx*sd*u,ay=pa[1]+A.ny*sd*u,az=gy(ax,ay);if(az!=null&&t(ax,ay)===1){if(A.i%9===0){add(new THREE.CylinderGeometry(.002,.003,.03,5),MT.TRO,ax,az+.015,ay);add(new THREE.IcosahedronGeometry(.019,0),(A.i%2)?MT.ARB:MT.ARB2,ax,az+.04,ay)}else add(new THREE.IcosahedronGeometry(.009,0),(A.i%2)?MT.ARB:MT.ARB2,ax,az+.006,ay)}}}}
     }}
    // pórticos con carteles
    if(A.i>0&&A.i%70===35){const wl=A.wl+.01,wr=A.wr+.01,p1=[A.x+A.nx*wl,A.y+A.ny*wl],p2=[A.x-A.nx*wr,A.y-A.ny*wr],g1=gy(...p1),g2=gy(...p2);if(g1!=null&&g2!=null){const H=.09,top=Math.max(g1,g2)+H,ang=Math.atan2(A.ny,A.nx);
      for(const[p,g]of[[p1,g1],[p2,g2]])add(new THREE.BoxGeometry(.006,top-g+.004,.006),MT.HIE,p[0],(top+g)/2,p[1]);
      const lx=(p1[0]+p2[0])/2,ly=(p1[1]+p2[1])/2,len=wl+wr;add(new THREE.BoxGeometry(len,.006,.006),MT.HIE,lx,top,ly,-ang);add(new THREE.BoxGeometry(len,.004,.004),MT.HIE,lx,top-.022,ly,-ang);
      const n=Math.floor(A.i/70)%3,TX=entra?[['VIGO Centro','Praza de España · Vialia'],['Porto · Bouzas','Areal · Beiramar'],['Estación Vialia','Urzaiz · Centro']][n]:[['AP-9  A Coruña','Santiago · Pontevedra'],['Redondela','Ponte de Rande'],['AP-9  Pontevedra','Aeroporto']][n];
      const mt=AP.cartel(TX),pw=Math.min(len*.8,.16),pl=new THREE.Mesh(new THREE.PlaneGeometry(pw,pw*.32),mt);
      // el cartel mira a los coches que llegan (contra el sentido de la marcha)
      pl.position.set(lx-A.tx*.004,top-.011,ly-A.ty*.004);pl.rotation.y=Math.atan2(-A.tx,-A.ty);AP.G.add(pl);
      const bk=new THREE.Mesh(new THREE.PlaneGeometry(pw,pw*.32),MT.HIE);bk.position.set(lx-A.tx*.0035,top-.011,ly-A.ty*.0035);bk.rotation.y=Math.atan2(A.tx,A.ty);AP.G.add(bk)}}
   }
   for(const[mat,Lr]of raw){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(Lr,3));g.computeVertexNormals();const m=new THREE.Mesh(g,mat);if(mat!==MT.PAN&&mat!==MT.CES)mat.side=THREE.DoubleSide;m.receiveShadow=true;m.castShadow=!LT&&mat!==MT.CES&&mat!==MT.PAN;AP.G.add(m)}
   for(const[mat,gs]of parts){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=!LT&&mat!==MT.LUZ;m.receiveShadow=true;AP.G.add(m)}
  }});
 // monolito de bienvenida junto al final de la autopista
 if(!AP.mono){const c=[102.6,17.75];let best=null;for(let r=0;r<.6&&!best;r+=.04)for(let a=0;a<6.28;a+=.3){const x=c[0]+Math.cos(a)*r,y=c[1]+Math.sin(a)*r;let ok=true;for(const[dx,dy]of[[0,0],[.06,0],[-.06,0],[0,.04],[0,-.04]])if(t(x+dx,y+dy)!==1){ok=false;break}if(ok&&gy(x,y)!=null){best=[x,y];break}}
  if(best){AP.mono=best;const[x,y]=best,z=gy(x,y),mm=AP.MAT;const cv=document.createElement('canvas');cv.width=512;cv.height=160;const k=cv.getContext('2d');k.fillStyle='#e8e3d6';k.fillRect(0,0,512,160);k.fillStyle='#1f4fa3';k.textAlign='center';k.textBaseline='middle';k.font='bold 96px "Russo One",Arial,sans-serif';k.fillText('VIGO',256,70);k.font='30px Arial,sans-serif';k.fillStyle='#55606b';k.fillText('Benvidos · Bienvenidos',256,132);
   const tx=new THREE.CanvasTexture(cv);tx.colorSpace=THREE.SRGBColorSpace;const fr=new THREE.MeshStandardMaterial({map:tx,roughness:.8});const g=new THREE.Group();
   const b=new THREE.Mesh(new THREE.BoxGeometry(.16,.05,.018),[mm.PIE,mm.PIE,mm.PIE,mm.PIE,fr,fr]);b.position.set(0,.03,0);g.add(b);const base=new THREE.Mesh(new THREE.BoxGeometry(.19,.008,.04),mm.HOR2);base.position.y=.004;g.add(base);
   for(let i=0;i<7;i++){const f=new THREE.Mesh(new THREE.IcosahedronGeometry(.008,0),i%2?mm.ARB:mm.ARB2);f.position.set(-.09+i*.03,.006,.022);g.add(f)}
   g.position.set(x,z,y);// de cara a los que llegan por la autopista (desde el noreste)
   g.rotation.y=Math.atan2(1,-.6);g.traverse(o=>{if(o.isMesh){o.castShadow=!LT;o.receiveShadow=true}});AP.G.add(g)}}
 if(nuevos)AP.trozos=(AP.trozos||0)+nuevos}
function subePaso(){""")
open(f,'w').write(s)
print('ok ap9')
