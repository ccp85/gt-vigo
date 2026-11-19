f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= SAMIL (segunda pasada, con Google Earth de referencia) =================
# 1) Más sombrillas y hamacas en la arena (antes muy pocas).
r("if(i%3===0&&ancho>.12)for(let k=0;k<2;k++){if(rn()<.35)continue;","if(ancho>.12)for(let k=0;k<3;k++){if(rn()<.3)continue;")
# 1b) ocultar recorre todas las instancias (el LOD del bosque baja count al conducir y se saltaba las demás)
r("o.count>5000)return;let ch=false;inv.copy(o.matrixWorld).invert();for(let k=0;k<o.count;k++)","o.count>5000)return;let ch=false;inv.copy(o.matrixWorld).invert();for(let k=0;k<o.instanceMatrix.count;k++)")
# 2) Entre el paseo y la avenida no hay pinar sino aparcamientos grandes y jardines con palmeras: se aclara el pinar
#    (queda ~1 de cada 6 árboles) y se ponen aparcamientos con coches y céspedes con palmeras.
r(" scene.add(G);SAM.G=G;SAM.n=n}",r""" try{samTrasPaseo(G,C,n,ocultar,gy,t)}catch(e){console.warn('samil2',e);SAM.err2=String(e)}
 scene.add(G);SAM.G=G;SAM.n=n}
function samTrasPaseo(G,C,n,ocultar,gy,t){const LT=!!window.LITE;let rs=91;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 // franja de cada fila: desde detrás del paseo hasta la primera calzada de la avenida
 const F=[];for(let i=0;i<n;i++){const[xc,y,xe]=C[i],x0=xe+.11;let x1=null;for(let x=x0;x<x0+1.1;x+=.02){const c=t(x,y);if(c===2||c===3){x1=x-.03;break}}F.push(x1!=null&&x1-x0>.12?[x0,x1,y]:null)}
 const enF=(x,y)=>{const i=Math.round((y-C[0][1])/.08);if(i<0||i>=n)return false;const f=F[i];return !!f&&x>f[0]-.02&&x<f[1]+.02};
 const P=SAM.pisc;const cercaPisc=(x,y)=>P&&x>P[0]-.08&&x<P[0]+.55&&Math.abs(y-P[1])<.25;
 const aclarar=()=>{const o0=SAM.oc;ocultar((x,y)=>enF(x,y)&&!cercaPisc(x,y)&&(((Math.sin(x*91.7+y*47.3)*43758.5)%1+1)%1)>.16);SAM.aclara=(SAM.aclara||0)+SAM.oc-o0};aclarar();
 // el pinar (extras) puede llegar después: se repasa cuando aparecen trozos nuevos
 {let nT=TROZOS.length,veces=0;const iv=setInterval(()=>{if(TROZOS.length!==nT){nT=TROZOS.length;aclarar()}if(++veces>90)clearInterval(iv)},2000)}
 const parts=new Map(),add=(geo,mat,x,y,z,ry=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();if(g.attributes.uv)g.deleteAttribute('uv');g.rotateY(ry);g.translate(x,y,z);if(!parts.has(mat))parts.set(mat,[]);parts.get(mat).push(g)};
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.85},o));
 const ASF=M(0x50535c,{roughness:.95,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}),RAY=M(0xf2f2ee,{polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3}),
  CES=M(0x7cb35a,{roughness:1,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}),PAL=M(0x7a5a3a),HOJ=M(0x3f8a3a),VID=M(0x1b2233,{roughness:.2}),SETO=M(0x2f6b2c);
 const COL=[0xf4f4f2,0x2b2f3a,0x9aa3b0,0xb8423a,0x3a4a6a,0x5d7fb0,0xd8d4ca,0x2f4f3a];const CAR=new Map();
 // tramos alternos: aparcamiento (más largo) y jardín con palmeras
 let i=0,k=0;while(i<n){const L=k%2===0?9:6;const tipo=k%2===0?'ap':'ja';k++;
  for(let j=i;j<Math.min(n,i+L);j++){const f=F[j];if(!f)continue;const[x0,x1,y]=f;if(cercaPisc((x0+x1)/2,y))continue;const yb=y-.04,yt=y+.04;
   const z0=gy(x0,y),z1=gy(x1,y);if(z0==null||z1==null)continue;
   const quad=(m,xa,xb,za,zb)=>{const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute([xa,za+.004,yb,xa,za+.004,yt,xb,zb+.004,yt,xa,za+.004,yb,xb,zb+.004,yt,xb,zb+.004,yb],3));g.computeVertexNormals();if(!parts.has(m))parts.set(m,[]);parts.get(m).push(g)};
   if(tipo==='ap'){quad(ASF,x0,x1,z0,z1);
    // filas de plazas perpendiculares al paseo: cada fila .11 de fondo, pasillo .07
    let x=x0+.01;let fila=0;while(x+.11<=x1){const zz=gy(x+.055,y)??z0;for(const yy of[y-.02,y+.02]){add(new THREE.BoxGeometry(.11,.001,.002),RAY,x+.055,zz+.0055,yy)}
      // coches aparcados (algunos huecos libres)
      for(const yy of[y-.02+.0,y+.02]){const sp=yy;if(rn()<.72){const c=COL[(rn()*COL.length)|0];const cm=CAR.get(c)||CAR.set(c,M(c,{roughness:.4,metalness:.2})).get(c);const cx=x+.055,ry=fila%2?Math.PI:0;
        add(new THREE.BoxGeometry(.075,.016,.03),cm,cx,zz+.014,sp-.0,ry);add(new THREE.BoxGeometry(.04,.013,.027),VID,cx-.004,zz+.027,sp,ry);add(new THREE.BoxGeometry(.038,.003,.028),cm,cx-.004,zz+.035,sp,ry)}}
      x+=fila%2?.18:.11;fila++}}
   else{quad(CES,x0,x1,z0,z1);
    // palmeras en hilera y setos bajos
    for(let px=x0+.05;px<x1-.03;px+=.14){if(j%2)continue;const pz=gy(px,y);if(pz==null)continue;const h=.06+rn()*.025;add(new THREE.CylinderGeometry(.0018,.0026,h,6),PAL,px,pz+h/2,y);
     for(let q=0;q<7;q++){const a=q/7*6.283+rn()*.3;const hg=new THREE.BoxGeometry(.03,.0012,.007);hg.translate(.015,0,0);hg.rotateZ(-.45);add(hg,HOJ,px,pz+h,y,a)}}
    if(j%3===0)add(new THREE.BoxGeometry(Math.max(.02,x1-x0-.06),.008,.012),SETO,(x0+x1)/2,(z0+z1)/2+.006,y+.03)}}
  i+=L}
 for(const[m,gs]of parts){const me=new THREE.Mesh(mergeGeometries(gs),m);me.castShadow=!LT&&m!==ASF&&m!==RAY&&m!==CES;me.receiveShadow=true;G.add(me)}
 SAM.tras=F.filter(Boolean).length}""")
open(f,'w').write(s)
print('ok samil2')
