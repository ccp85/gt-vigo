// ---------- Praza de España y Os Redeiros (espana.js)
// Tramo de Gran Vía entre Urzáiz y Praza de España (las rampas ya están en edit_rampas.py / edit_rampas2.py; aquí no se tocan).
//  · Praza de España: en la isleta de la rotonda, Os Cabalos de Juan José Oliveira (1991): cinco caballos de bronce oscuro que
//    suben en espiral por una roca de casi 20 m, con la cascada de agua bajando en espiral hasta el vaso de la fuente;
//    bordillo de granito, césped con arbustos y los proyectores que la iluminan de noche (el bronce se calienta con CIELO.nf).
//  · Os Redeiros (Monumento ao Traballo, Ramón Conde, 1991): siete figuras de bronce tirando de la red sobre un pedestal
//    de granito, en el bulevar de Gran Vía justo debajo de la primera rampa, casi en el cruce con Urzáiz.
// Isleta medida en vigo_mapa.png (celdas tipo 3): centro [93.717,30.15], radio ~0,155 u. 1 u = 64 m.
const PZE={C:[93.717,30.15],R:.152,RD:[96.845,23.0],plaza:0,red:0,G:null,GR:null};window.__PZE=PZE;
function pzeChk(){if(typeof sueloRap!=='function')return;
 if(!PZE.plaza&&sueloRap(PZE.C[0],PZE.C[1])!=null&&sueloRap(PZE.C[0]+.1,PZE.C[1])!=null){PZE.plaza=1;setTimeout(()=>{try{pzePlaza()}catch(e){console.warn('espana',e);PZE.err=String(e);PZE.plaza=0}},600)}
 if(!PZE.red&&sueloRap(PZE.RD[0],PZE.RD[1])!=null){PZE.red=1;setTimeout(()=>{try{pzeRedeiros()}catch(e){console.warn('redeiros',e);PZE.errR=String(e);PZE.red=0}},700)}}
// material de bronce compartido: de noche lo calientan los proyectores
const PZE_BRONCE=new THREE.MeshStandardMaterial({color:0x5b4633,roughness:.38,metalness:.65,flatShading:true});
const PZE_ROCA=new THREE.MeshStandardMaterial({color:0x3f352c,roughness:.55,metalness:.5,flatShading:true});
function pzeNoche(){let n=0;try{n=CIELO.nf||0}catch(e){}const k=THREE.MathUtils.smoothstep(n,.15,.6);
 PZE_BRONCE.emissive.setRGB(.2*k,.12*k,.05*k);PZE_ROCA.emissive.setRGB(.09*k,.065*k,.04*k);if(PZE.lente)PZE.lente.emissiveIntensity=.2+2.8*k}
// oculta lo que el modelo genérico ponía encima de una zona (triángulos por encima del suelo dentro del radio)
function pzeOculta(cx,cz,r,skip){const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();let k=0;
 scene.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||(typeof GROUND!=='undefined'&&GROUND.includes(o))||o.userData.pze)return;
  let p=o;while(p){if(p===skip||p===PZE.G||p===PZE.GR||(typeof RAMPA!=='undefined'&&p===RAMPA.G))return;p=p.parent}
  const g=o.geometry,ix=g.index,pos=g.attributes&&g.attributes.position;if(!ix||!pos)return;if(!g.boundingBox)g.computeBoundingBox();o.updateMatrixWorld(true);
  const bb=g.boundingBox.clone().applyMatrix4(o.matrixWorld);if(bb.max.x<cx-r||bb.min.x>cx+r||bb.max.z<cz-r||bb.min.z>cz+r)return;const mw=o.matrixWorld;let ch=0;
  for(let t=0;t<ix.count;t+=3){a.fromBufferAttribute(pos,ix.getX(t)).applyMatrix4(mw);b.fromBufferAttribute(pos,ix.getX(t+1)).applyMatrix4(mw);c.fromBufferAttribute(pos,ix.getX(t+2)).applyMatrix4(mw);
   const mx=(a.x+b.x+c.x)/3,mz=(a.z+b.z+c.z)/3,my=Math.max(a.y,b.y,c.y);if(Math.hypot(mx-cx,mz-cz)>r)continue;
   let gy=null;try{gy=sueloRap(mx,mz)}catch(e){}if(gy==null)continue;if(my>gy+.006){const i0=ix.getX(t);ix.setX(t+1,i0);ix.setX(t+2,i0);ch++}}
  if(ch){ix.needsUpdate=true;k+=ch;if(g.boundsTree){try{g.computeBoundsTree()}catch(e){}}}});return k}
// piezas sueltas a geometría sin índice para poder juntarlas
function pzeNI(g){const n=g.index?g.toNonIndexed():g;if(n.attributes.uv)n.deleteAttribute('uv');return n}
// caballo de bronce encabritado (mira a +x, patas traseras en el origen, largo del cuerpo = 1)
function pzeCaballo(var_){const P=[],v=var_||0;
 const esf=(sx,sy,sz,x,y,z,rz)=>{const g=new THREE.SphereGeometry(.5,9,7);g.scale(sx,sy,sz);if(rz)g.rotateZ(rz);g.translate(x,y,z);P.push(pzeNI(g))};
 const cil=(r1,r2,L,x0,y0,z0,x1,y1,z1)=>{const g=new THREE.CylinderGeometry(r2,r1,L,7);const d=new THREE.Vector3(x1-x0,y1-y0,z1-z0),l=d.length();g.scale(1,l/L,1);
  g.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize()));g.translate((x0+x1)/2,(y0+y1)/2,(z0+z1)/2);P.push(pzeNI(g))};
 // cuerpo: tronco, pecho y grupa
 esf(1.0,.44,.38,0,0,0);esf(.46,.52,.4,.33,.05,0);esf(.5,.5,.42,-.33,.04,0);
 // cuello, crin y cabeza (algo girada a un lado según la variante)
 const hz=(v%3-1)*.06;cil(.18,.11,1,.4,.12,0,.72,.5,hz*.5);
 for(let k=0;k<5;k++){const t=k/4;const g=new THREE.BoxGeometry(.09,.06,.035);g.rotateZ(-.85);g.translate(.4+.28*t,.3+.3*t,hz*.5*t);P.push(pzeNI(g))}
 cil(.1,.06,1,.7,.55,hz*.5,.98,.36,hz);esf(.17,.19,.14,.71,.55,hz*.5);
 for(const s of[-1,1]){const g=new THREE.ConeGeometry(.022,.075,4);g.rotateZ(.3);g.translate(.68,.66,hz*.5+s*.04);P.push(pzeNI(g))}
 // patas traseras apoyadas en la roca (muslo, caña y casco)
 for(const s of[-1,1]){const z=s*.12,ad=s<0?.06:-.04;cil(.12,.08,1,-.38,-.05,z,-.32+ad,-.38,z);cil(.06,.05,1,-.32+ad,-.38,z,-.3+ad,-.62,z);esf(.11,.07,.1,-.28+ad,-.64,z)}
 // patas delanteras levantadas y dobladas (una más alta que la otra)
 for(const s of[-1,1]){const z=s*.12,up=s<0?.08:-.02;cil(.1,.07,1,.38,-.06,z,.6,-.2+up,z);cil(.055,.045,1,.6,-.2+up,z,.5,-.42+up,z);esf(.1,.07,.09,.49,-.45+up,z)}
 // cola al viento
 cil(.07,.04,1,-.52,.08,0,-.78,-.1,(v%2?.08:-.08));cil(.045,.02,1,-.78,-.1,(v%2?.08:-.08),-.9,-.36,(v%2?.14:-.12));
 const g=mergeGeometries(P);g.translate(.3,.64,0);g.computeVertexNormals();return g}
// figura de redeiro tirando de la cuerda (mira a +x, se echa hacia atrás; pies en el origen, altura = 1)
function pzeRedeiro(v){const P=[];
 const cil=(r1,r2,x0,y0,z0,x1,y1,z1)=>{const g=new THREE.CylinderGeometry(r2,r1,1,7);const d=new THREE.Vector3(x1-x0,y1-y0,z1-z0),l=d.length();g.scale(1,l,1);
  g.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize()));g.translate((x0+x1)/2,(y0+y1)/2,(z0+z1)/2);P.push(pzeNI(g))};
 const esf=(r,sx,sy,sz,x,y,z)=>{const g=new THREE.SphereGeometry(r,8,6);g.scale(sx,sy,sz);g.translate(x,y,z);P.push(pzeNI(g))};
 const lean=.32+(v%3)*.07,hx=-.06,nx=hx-Math.sin(lean)*.42,ny=.52+Math.cos(lean)*.42;
 // piernas abiertas: la de delante clavada y doblada, la de atrás estirada
 cil(.085,.06,hx,.52,.08,.1,.27,.09);cil(.06,.045,.1,.27,.09,.16,.02,.09);esf(.05,1.5,.6,1,.19,.02,.09);
 cil(.085,.06,hx,.52,-.08,-.14,.27,-.08);cil(.06,.045,-.14,.27,-.08,-.24,.02,-.08);esf(.05,1.5,.6,1,-.21,.02,-.08);
 // tronco ancho y musculoso inclinado hacia atrás, hombros y cabeza gacha
 cil(.16,.2,hx,.5,0,nx,ny,0);esf(.5,.26,.2,.48,nx+.01,ny-.04,0);cil(.05,.05,nx,ny,0,nx+.03,ny+.06,0);esf(.075,1,1.15,.95,nx+.05,ny+.11,0);
 // brazos hacia delante agarrando la cuerda a la altura de la cintura
 for(const s of[-1,1]){const sx=nx+.01,sy=ny-.05,sz=s*.2;cil(.06,.05,sx,sy,sz,(sx+.24)/2,(sy+.45)/2,s*.13);cil(.05,.04,(sx+.24)/2,(sy+.45)/2,s*.13,.24,.45,s*.03);esf(.045,1,1,1,.25,.45,s*.03)}
 const g=mergeGeometries(P);g.computeVertexNormals();return g}
function pzePlaza(){const[cx,cz]=PZE.C,R=PZE.R,G=new THREE.Group();G.name='prazaEspana';PZE.G=G;
 let y0=sueloRap(cx,cz);if(y0==null)y0=groundY(cx,cz);
 const sh=o=>{o.castShadow=!window.LITE;o.receiveShadow=true;o.userData.pze=1;G.add(o);return o};
 const GRAN=new THREE.MeshStandardMaterial({color:0xb7b2a7,roughness:.85}),CES=new THREE.MeshStandardMaterial({color:0x5f9a3e,roughness:1}),
  AGUA=new THREE.MeshStandardMaterial({color:0x2f6f86,roughness:.08,metalness:.15,transparent:true,opacity:.86}),
  ESPU=new THREE.MeshStandardMaterial({color:0xeaf6ff,roughness:.3,transparent:true,opacity:.75,depthWrite:false});
 // bordillo, césped y arbustos de la isleta
 {const g=new THREE.CylinderGeometry(R,R+.002,.007,64,1,true);g.translate(cx,y0+.0025,cz);sh(new THREE.Mesh(g,GRAN));
  const t=new THREE.RingGeometry(R-.004,R,64);t.rotateX(-Math.PI/2);t.translate(cx,y0+.006,cz);sh(new THREE.Mesh(t,GRAN));
  const c=new THREE.RingGeometry(.1,R-.004,64);c.rotateX(-Math.PI/2);c.translate(cx,y0+.0055,cz);sh(new THREE.Mesh(c,CES));
  let rs=29;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647,bola=new THREE.IcosahedronGeometry(.007,0),m=new THREE.Matrix4(),q=new THREE.Quaternion(),V=new THREE.Vector3(),S=new THREE.Vector3(),col=new THREE.Color();
  const N=window.LITE?26:46,im=new THREE.InstancedMesh(bola,new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9,flatShading:true}),N);
  for(let i=0;i<N;i++){const a=i/N*Math.PI*2+rn()*.08,r=.112+rn()*.03,k=.7+rn()*.6;m.compose(V.set(cx+Math.cos(a)*r,y0+.009,cz+Math.sin(a)*r),q,S.set(k,k*.75,k));im.setMatrixAt(i,m);im.setColorAt(i,col.setHex([0x3f7d34,0x4f8f3a,0x2f6b35,0xb03a48][i%7===3?3:i%3]))}
  im.computeBoundingSphere();sh(im)}
 // vaso de la fuente: pretil de granito y lámina de agua
 {const w=new THREE.CylinderGeometry(.098,.1,.014,56,1,true);w.translate(cx,y0+.007,cz);sh(new THREE.Mesh(w,new THREE.MeshStandardMaterial({color:0xb7b2a7,roughness:.85,side:THREE.DoubleSide})));
  const tp=new THREE.RingGeometry(.092,.1,56);tp.rotateX(-Math.PI/2);tp.translate(cx,y0+.014,cz);sh(new THREE.Mesh(tp,GRAN));
  const a=new THREE.CircleGeometry(.093,56);a.rotateX(-Math.PI/2);a.translate(cx,y0+.01,cz);const ag=new THREE.Mesh(a,AGUA);ag.receiveShadow=true;ag.userData.pze=1;G.add(ag);
  const f=new THREE.RingGeometry(.03,.058,40);f.rotateX(-Math.PI/2);f.translate(cx,y0+.0105,cz);const fm=new THREE.Mesh(f,ESPU);fm.renderOrder=2;fm.userData.pze=1;G.add(fm)}
 // la roca en espiral: núcleo y repisa que sube dando vuelta y media
 const H=.27,TH0=.4,VUELTA=5.2,base=y0+.01,hel=s=>({a:TH0+s*VUELTA,h:.015+s*(H-.05)});
 {const P=[];let rs=7;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
  for(let k=0;k<26;k++){const s=k/25,h=s*H,r=.017*(1-.5*s)+.004,g=new THREE.DodecahedronGeometry(r*(1.05+rn()*.3),0);g.rotateY(rn()*6);g.rotateX(rn()*.6);g.translate(cx+(rn()-.5)*.01,base+h,cz+(rn()-.5)*.01);P.push(pzeNI(g))}
  for(let k=0;k<70;k++){const s=k/69,e=hel(s),r=.03-.01*s,sz=.012*(1-.35*s)*(.85+rn()*.4),g=new THREE.DodecahedronGeometry(sz,0);g.scale(1.3,.7,1);g.rotateY(-e.a+rn()*.5);
   g.translate(cx+Math.cos(e.a)*r,base+e.h-.012,cz+Math.sin(e.a)*r);P.push(pzeNI(g))}
  const rg=mergeGeometries(P);rg.computeVertexNormals();sh(new THREE.Mesh(rg,PZE_ROCA))}
 // la cascada: lámina de agua que baja en espiral por el lado contrario a los caballos, con el agua corriendo
 {const cv=document.createElement('canvas');cv.width=32;cv.height=128;const x=cv.getContext('2d');x.fillStyle='#cfe9f5';x.fillRect(0,0,32,128);
  for(let i=0;i<60;i++){x.fillStyle=`rgba(255,255,255,${.3+Math.random()*.6})`;x.fillRect(Math.random()*32,Math.random()*128,1+Math.random()*2,6+Math.random()*18)}
  const tx=new THREE.CanvasTexture(cv);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.colorSpace=THREE.SRGBColorSpace;
  const M=new THREE.MeshStandardMaterial({map:tx,roughness:.2,transparent:true,opacity:.62,depthWrite:false,side:THREE.DoubleSide,emissive:0x0c1a22});
  const n=90,pos=[],uv=[],idx=[];for(let i=0;i<=n;i++){const s=i/n,a=TH0+Math.PI+s*VUELTA,h=.005+s*(H-.03),r0=.016*(1-.4*s)+.006,r1=r0+.02;
   pos.push(cx+Math.cos(a)*r0,base+h+.004,cz+Math.sin(a)*r0,cx+Math.cos(a)*r1,base+h-.01,cz+Math.sin(a)*r1);uv.push(0,s*10,1,s*10)}
  for(let i=0;i<n;i++){const a=i*2;idx.push(a,a+2,a+1,a+1,a+2,a+3)}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();
  const cas=new THREE.Mesh(g,M);cas.renderOrder=2;cas.userData.pze=1;G.add(cas);
  cas.onBeforeRender=()=>{tx.offset.y=(performance.now()/1000*1.1)%1;pzeNoche()}}
 // los cinco caballos subiendo por la espiral, cada uno algo más encabritado que el de abajo
 {const s0=[.05,.27,.49,.7,.9];
  s0.forEach((s,i)=>{const e=hel(s),r=.052-.01*s,g=pzeCaballo(i);const m=new THREE.Mesh(g,PZE_BRONCE);
   const px=cx+Math.cos(e.a)*r,pz=cz+Math.sin(e.a)*r,tx_=-Math.sin(e.a),tz=Math.cos(e.a);
   m.position.set(px,base+e.h-.006,pz);m.rotation.order='YXZ';m.rotation.y=Math.atan2(-tz,tx_);m.rotation.z=.32+.09*i;m.rotation.x=-.18;
   const k=.1-.005*i;m.scale.set(k,k,k);sh(m)})}
 // proyectores LED alrededor del vaso (se encienden de noche)
 {const cuerpo=new THREE.MeshStandardMaterial({color:0x34373c,roughness:.5,metalness:.6}),lente=new THREE.MeshStandardMaterial({color:0xfff1d0,emissive:0xffd28a,emissiveIntensity:.2,roughness:.3});PZE.lente=lente;
  for(let i=0;i<8;i++){const a=i/8*Math.PI*2+.2,p=[cx+Math.cos(a)*.082,cz+Math.sin(a)*.082];
   const b=new THREE.Mesh(new THREE.BoxGeometry(.008,.006,.008),cuerpo);b.position.set(p[0],y0+.013,p[1]);b.rotation.y=-a;sh(b);
   const l=new THREE.Mesh(new THREE.CircleGeometry(.0032,10),lente);l.rotation.x=-Math.PI/2;l.position.set(p[0],y0+.0162,p[1]);l.userData.pze=1;G.add(l)}}
 scene.add(G);G.updateMatrixWorld(true);
 // quita lo que hubiera en la isleta (árbol o pieza genérica) y vuelve a mirar cuando cargan más piezas de la zona
 PZE.oc=pzeOculta(cx,cz,R-.003,G);setTimeout(()=>{PZE.oc+=pzeOculta(cx,cz,R-.003,G)},4000);
 // colisión de la roca y los caballos (el coche no atraviesa el monumento)
 G.traverse(o=>{if(o.isMesh&&o.material===PZE_ROCA){try{colaBVH(o,false)}catch(e){}}});
 PZE.listo=1}
function pzeRedeiros(){const[cx,cz]=PZE.RD,G=new THREE.Group();G.name='osRedeiros';PZE.GR=G;
 // eje del bulevar en este tramo (de Praza de España hacia Urzáiz)
 const dx=.348,dz=-.938,ang=Math.atan2(-dz,dx),at=(u,o)=>[cx+dx*u-dz*o,cz+dz*u+dx*o];
 let y0=sueloRap(cx,cz);if(y0==null)y0=groundY(cx,cz);
 const GRAN=new THREE.MeshStandardMaterial({color:0x9d988e,roughness:.9});
 const ped=new THREE.Mesh(new THREE.BoxGeometry(.075,.012,.028),GRAN);ped.position.set(cx,y0+.006,cz);ped.rotation.y=ang;ped.castShadow=!window.LITE;ped.receiveShadow=true;G.add(ped);
 const ped2=new THREE.Mesh(new THREE.BoxGeometry(.08,.003,.033),GRAN);ped2.position.set(cx,y0+.0015,cz);ped2.rotation.y=ang;ped2.receiveShadow=true;G.add(ped2);
 // siete redeiros en fila, al tresbolillo, echados hacia atrás tirando hacia Praza de España (cuesta arriba)
 const top=y0+.012,figs=[];for(let i=0;i<7;i++){const u=.03-i*.0095,o=(i%2?1:-1)*.0045;figs.push([u,o])}
 figs.forEach(([u,o],i)=>{const m=new THREE.Mesh(pzeRedeiro(i),PZE_BRONCE);const p=at(u,o);m.position.set(p[0],top,p[1]);m.rotation.y=ang+Math.PI+(i%2?.12:-.12);
  const k=.036+(i%3)*.002;m.scale.set(k,k,k);m.castShadow=!window.LITE;m.receiveShadow=true;m.userData.pze=1;G.add(m)});
 // la cuerda que pasa por todas las manos y la red amontonada al final
 {const p0=at(.04,0),p1=at(-.03,0),y=top+.018,v=new THREE.Vector3(p1[0]-p0[0],0,p1[1]-p0[1]),L=v.length();
  const g=new THREE.CylinderGeometry(.0012,.0012,L,6);g.rotateZ(Math.PI/2);const c=new THREE.Mesh(g,PZE_BRONCE);c.position.set((p0[0]+p1[0])/2,y,(p0[1]+p1[1])/2);c.rotation.y=ang;G.add(c);
  const pr=at(-.031,0),red=new THREE.Mesh(new THREE.IcosahedronGeometry(.008,1),PZE_BRONCE);red.scale.set(1.3,.55,1);red.position.set(pr[0],top+.004,pr[1]);red.castShadow=!window.LITE;G.add(red)}
 scene.add(G);G.updateMatrixWorld(true);PZE.ocR=pzeOculta(cx,cz,.04,G);
 try{colaBVH(ped,false)}catch(e){}PZE.listoR=1}
// ---------- fin de espana.js
