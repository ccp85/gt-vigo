f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= NÁUTICO DE VIGO (dársena deportiva junto a As Avenidas) =================
# Google Earth solo como referencia: pantalanes llenos de veleros con la vela recogida y lanchas amarradas de popa,
# y un edificio de club náutico genérico (blanco, dos plantas con ventanales, terraza y mástil de señales).
r("function subeZonas(){psolChk();","function subeZonas(){psolChk();nauChk();")
r("function subePaso(){",r"""const NAU={hecha:0,X0:86.3,X1:95.6,Y0:10,Y1:13.2};window.__NAU=NAU;
setInterval(()=>{if(!NAU.hecha)nauChk()},3000);
function nauChk(){if(NAU.hecha||!MAPA||!MI)return;if(sueloRap(90.6,12.9)==null)return;NAU.hecha=1;setTimeout(()=>{try{nauCrea()}catch(e){console.warn('nautico',e);NAU.err=String(e)}},900)}
function nauCrea(){const LT=!!window.LITE,G=new THREE.Group();G.name='nautico';const t=(x,y)=>cell(x,y).t,gy=(x,y)=>sueloRap(x,y);
 let rs=23;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;const WY=-.032;
 // 1) huecos de amarre: borde de pantalán (5) o muelle (1) con agua delante; el barco entra de proa hacia el agua
 const st=.02,SP=[];for(let x=NAU.X0;x<NAU.X1;x+=st)for(let y=NAU.Y0;y<NAU.Y1;y+=st){const c=t(x,y);if(c!==5)continue;
  for(const[dx,dy]of[[1,0],[-1,0],[0,1],[0,-1]]){if(t(x+dx*st,y+dy*st)!==0)continue;let ok=true;for(let k=1;k<=7&&ok;k++)for(const w of[-.022,0,.022]){if(t(x+dx*(.02+k*.02)-dy*w,y+dy*(.02+k*.02)+dx*w)!==0){ok=false;break}}if(ok)SP.push([x+dx*.012,y+dy*.012,dx,dy])}}
 // separación entre barcos ~0.045
 const PL=[];for(const p of SP){if(PL.some(q=>Math.hypot(q[0]-p[0],q[1]-p[1])<.044))continue;PL.push(p)}
 NAU.huecos=PL.length;
 // 2) modelos: velero con la vela recogida y lancha (la del juego, más pequeña), juntados por material para instanciarlos
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.6},o));
 const vel=(()=>{const L=.12,B=.036,P=new Map(),add=(g,m)=>{if(!P.has(m))P.set(m,[]);g=g.index?g.toNonIndexed():g;if(g.attributes.uv)g.deleteAttribute('uv');P.get(m).push(g)};
  const plan=k=>{const sh=new THREE.Shape();sh.moveTo(-L/2*k,-B/2*k);sh.lineTo(L*.2*k,-B/2*k);sh.quadraticCurveTo(L*.42*k,-B*.32*k,L/2*k,0);sh.quadraticCurveTo(L*.42*k,B*.32*k,L*.2*k,B/2*k);sh.lineTo(-L/2*k,B/2*k);sh.lineTo(-L/2*k,-B/2*k);return sh};
  const ex=(k,h,y0)=>{const g=new THREE.ExtrudeGeometry(plan(k),{depth:h,bevelEnabled:false,curveSegments:4});g.rotateX(-Math.PI/2);g.translate(0,y0,0);return g};
  const W=M(0xf6f6f2),Nv=M(0x1f3557),T=M(0xd9c7a2,{roughness:.8}),Gl=M(0x223247,{roughness:.2}),S=M(0xb9bec6,{metalness:.6,roughness:.35}),C=[M(0x1f5fa8),M(0x2a7a4f),M(0x9a2a2a)];
  add(ex(1,.016,-.008),W);add(ex(1.01,.004,-.006),Nv);add(ex(.9,.001,.008),T);
  const cab=new THREE.BoxGeometry(.04,.009,.024);cab.translate(-.008,.0125,0);add(cab,W);const vi=new THREE.BoxGeometry(.041,.004,.025);vi.translate(-.008,.013,0);add(vi,Gl);
  const ms=new THREE.CylinderGeometry(.0009,.0012,.17,5);ms.translate(.012,.093,0);add(ms,S);const bo=new THREE.BoxGeometry(.055,.0016,.0016);bo.translate(-.014,.03,0);add(bo,S);
  const fo=new THREE.BoxGeometry(.05,.005,.005);fo.translate(-.012,.0335,0);
  // tres versiones del toldo de la vela (azul, verde, granate)
  return {P,fo,C}})();
 const lan=(()=>{const g=mkLanchaM(false,false);const P=new Map();g.traverse(o=>{if(!o.isMesh||o.userData.est)return;const q=o.geometry.clone().applyMatrix4(o.matrixWorld);q.scale(.55,.55,.55);if(q.attributes.uv)q.deleteAttribute('uv');if(!P.has(o.material))P.set(o.material,[]);P.get(o.material).push(q.index?q.toNonIndexed():q)});return P})();
 const mm=new THREE.Matrix4(),qq=new THREE.Quaternion(),e=new THREE.Euler(),V=new THREE.Vector3(),S1=new THREE.Vector3(1,1,1);
 const VL=[],LN=[];for(const p of PL){(rn()<.62?VL:LN).push(p)}
 const inst=(geoMap,lista,len)=>{for(const[mat,gs]of geoMap){const g=mergeGeometries(gs);const im=new THREE.InstancedMesh(g,mat,lista.length);lista.forEach(([x,y,dx,dy],i)=>{const cx=x+dx*(len/2),cy=y+dy*(len/2);e.set(0,Math.atan2(-dy,dx)+(rn()-.5)*.05,0);qq.setFromEuler(e);V.set(cx,WY,cy);im.setMatrixAt(i,mm.compose(V,qq,S1))});im.castShadow=!LT;im.receiveShadow=true;G.add(im)}};
 if(VL.length){inst(vel.P,VL,.12);// toldos de colores
  const grp=[[],[],[]];VL.forEach((p,i)=>grp[i%3].push(p));grp.forEach((L_,k)=>{if(!L_.length)return;const im=new THREE.InstancedMesh(vel.fo,vel.C[k],L_.length);L_.forEach(([x,y,dx,dy],i)=>{e.set(0,Math.atan2(-dy,dx),0);qq.setFromEuler(e);V.set(x+dx*.06,WY,y+dy*.06);im.setMatrixAt(i,mm.compose(V,qq,S1))});G.add(im)})}
 if(LN.length)inst(lan,LN,.11);
 NAU.veleros=VL.length;NAU.lanchas=LN.length;
 // 3) club náutico: edificio blanco de dos plantas en el muelle, cerca de la dársena
 // (el edificio del club ya existe en el mapa, el del catastro con fachada curva: no se duplica)
 if(false){const libreR=(cx,cy,w,d)=>{for(let a=-w/2;a<=w/2;a+=.03)for(let b=-d/2;b<=d/2;b+=.03){const c=t(cx+a,cy+b);if(c!==1&&c!==5)return false;const ms=repMallas(cx+a,cy+b);if(ms.length&&repAltura(cx+a,cy+b,ms)>(gy(cx+a,cy+b)??0)+.02)return false}return true};
  let best=null;for(let r=0;r<1.2&&!best;r+=.04)for(let a=0;a<6.283;a+=.35){const x=90.6+Math.cos(a)*r,y=12.75+Math.sin(a)*r;if(libreR(x,y,.32,.16)){best=[x,y];break}}
  if(best){NAU.club=best;const[x,y]=best,z=gy(x,y)??0,W=.28,D=.12,H1=.032,H2=.028;const B=M(0xf7f7f3,{roughness:.55}),GL=M(0x1d3a5f,{roughness:.15,metalness:.2}),AZ=M(0x1f4fa3),BAR=M(0xdfe3e8,{metalness:.5,roughness:.3});
   const g=new THREE.Group();g.position.set(x,z,y);const bx=(w,h,d,m,px,py,pz)=>{const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(px,py,pz);o.castShadow=!LT;o.receiveShadow=true;g.add(o);return o};
   const cy_=(r_,h,m,px,py,pz)=>{const o=new THREE.Mesh(new THREE.CylinderGeometry(r_,r_,h,24,1,false,0,Math.PI),m);o.position.set(px,py,pz);o.rotation.y=Math.PI/2;o.castShadow=!LT;g.add(o);return o};
   // planta baja y primera, con la proa redondeada hacia el mar (este)
   bx(W,H1,D,B,0,H1/2,0);cy_(D/2,H1,B,W/2,H1/2,0);bx(W-.01,H1*.5,D+.002,GL,0,H1*.55,0);bx(W+.002,H1*.5,D-.01,GL,0,H1*.55,0);cy_(D/2+.001,H1*.5,GL,W/2,H1*.55,0);
   bx(W*.82,H2,D*.85,B,-.02,H1+H2/2,0);cy_(D*.425,H2,B,W*.41-.02,H1+H2/2,0);bx(W*.82-.01,H2*.5,D*.85+.002,GL,-.02,H1+H2*.55,0);cy_(D*.425+.001,H2*.5,GL,W*.41-.02,H1+H2*.55,0);
   bx(W*.86,.004,D*.9,B,-.02,H1+H2+.002,0);bx(W+.004,.005,D+.004,AZ,0,H1+.0025,0);
   // terraza en la cubierta de la planta baja (la parte que no tapa la primera planta) con barandilla
   for(const sd of[-1,1])bx(W,.0012,.0012,BAR,0,H1+.012,sd*(D/2-.002));bx(.0012,.0012,D,BAR,-W/2+.002,H1+.012,0);
   // mástil de señales con verga y banderas
   const mx=W/2+.02,mast=new THREE.Mesh(new THREE.CylinderGeometry(.0012,.0016,.16,6),BAR);mast.position.set(mx,H1+.08,0);g.add(mast);bx(.0012,.0012,.07,BAR,mx,H1+.13,0);
   const fl=[0xd8402e,0xf2c230,0x1f4fa3,0xf6f6f2,0x2a7a4f];fl.forEach((c,i)=>{const sd=i%2?1:-1,k=Math.floor(i/2);const f_=new THREE.Mesh(new THREE.PlaneGeometry(.014,.009),new THREE.MeshStandardMaterial({color:c,side:THREE.DoubleSide}));f_.position.set(mx,H1+.124-k*.016,sd*(.012+k*.008));f_.rotation.y=Math.PI/2;g.add(f_)});
   // rótulo
   const cv=document.createElement('canvas');cv.width=512;cv.height=96;const k=cv.getContext('2d');k.fillStyle='#f7f7f3';k.fillRect(0,0,512,96);k.fillStyle='#1f4fa3';k.font='bold 62px "Russo One",Arial,sans-serif';k.textAlign='center';k.textBaseline='middle';k.fillText('NÁUTICO',256,52);
   const tx=new THREE.CanvasTexture(cv);tx.colorSpace=THREE.SRGBColorSpace;for(const sd of[-1,1]){const p=new THREE.Mesh(new THREE.PlaneGeometry(.12,.022),new THREE.MeshStandardMaterial({map:tx,roughness:.6}));p.position.set(-.02,H1+H2+.016,sd*(D*.45+.0015));p.rotation.y=sd>0?0:Math.PI;g.add(p);const sp=new THREE.Mesh(new THREE.BoxGeometry(.12,.024,.002),B);sp.position.set(-.02,H1+H2+.016,sd*D*.45);g.add(sp)}
   G.add(g)}}
 scene.add(G);NAU.G=G}
function subePaso(){""")
open(f,'w').write(s)
print('ok nautico')
