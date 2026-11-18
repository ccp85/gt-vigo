import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MISIÓN DE LA MOTO DE AGUA: EL REGALO PERDIDO BAJO EL MAR =================
# · La moto de agua lleva a Papá Noel (o al Rey Mago elegido) y una pila de regalos.
# · Hay que ir a un punto cerca de la costa (boya), tirarse al agua (E / Ⓐ), nadar y bucear (Z baja, Q sube)
#   buscando el regalo perdido en el fondo, volver a la moto y llevarlo al Puerto de Vigo.
# · Mundo submarino propio alrededor del punto de buceo: fondo de arena que sube hacia la costa con cáusticas,
#   rocas, algas que se mecen, corales, estrellas de mar, bancos de peces, rayos de luz, partículas en suspensión,
#   superficie vista desde abajo, niebla azul, linterna y burbujas. Aire limitado: hay que subir a respirar.

# --- la campaña: todas las misiones de moto son ahora de buceo
r("function campMision(k){","""function campMisionB(k){const m=campMision0(k);if(m.v==='moto'){m.buceo=true;m.txt='🤿 Moto de agua · regalo perdido'}return m}
function campMision(k){return campMisionB(k)}
function campMision0(k){""")
# --- la niebla del cielo no pisa la del fondo del mar
r("if(driving)FOG.color.copy(hor);","if(driving&&!window.__BAJO)FOG.color.copy(hor);")
r("if(driving){FOG.color.copy(SKYU.uHor.value);scene.fog=FOG}","if(driving){if(!window.__BAJO)FOG.color.copy(SKYU.uHor.value);scene.fog=FOG}")
# --- modo nado dentro del bucle del jugador
r("function updateCar(dt){if(MODO==='heli'){updateHeli(dt);return}","function updateCar(dt){if(MODO==='heli'){updateHeli(dt);return}if(MODO==='nado'){updateNado(dt);return}")
r("function buscarObjetivo(){objetivo=null;","function buscarObjetivo(){objetivo=null;if(BUC.on){const t_=buceoObjetivo();if(t_!==undefined)return t_}")
r("function accion(){if(!driving)return;","function accion(){if(!driving)return;if(BUC.on&&buceoAccion())return;")
r("REP.enPuerto=0;campVeh('moto',pu[0],pu[1],Math.atan2(-(tg[1]-pu[1]),tg[0]-pu[0]));","REP.enPuerto=0;if(m.buceo&&buceoInicio(m,pu,k))return;campVeh('moto',pu[0],pu[1],Math.atan2(-(tg[1]-pu[1]),tg[0]-pu[0]));")
r("if(m.v==='moto'){repVolver();","if(m.v==='moto'&&!m.buceo){repVolver();")
r("function repSigue(ab,ms){","function repSigue(ab,ms){motoNavQuita();")
r("if(m.v==='intro'){introTick(dt||.016);return}","if(m.v==='intro'){introTick(dt||.016);return}if(m.buceo&&BUC.on){buceoTick(dt||.016);return}")
# --- interfaz: velo azul bajo el agua y barra de aire
r('<button id="bSaltar"','<div id="bajoAgua" hidden style="position:fixed;inset:0;pointer-events:none;z-index:4;background:radial-gradient(ellipse at 50% -10%,rgba(150,235,255,.22),rgba(0,60,90,.18) 45%,rgba(0,20,40,.55) 100%)"></div><div id="aire" hidden style="position:fixed;left:50%;bottom:calc(150px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:30;width:180px;padding:5px 8px;border-radius:12px;background:rgba(10,30,50,.65);color:#dff6ff;font:600 12px system-ui;text-align:center">🫧 Aire<div style="height:7px;border-radius:4px;background:rgba(255,255,255,.2);margin-top:4px;overflow:hidden"><i style="display:block;height:100%;width:100%;background:linear-gradient(90deg,#3fd0ff,#bff4ff);border-radius:4px"></i></div></div><button id="bSaltar"')
r("function repCocheCalle(){",r"""const BUC={on:false};window.__BUC=BUC;
// figura de Papá Noel o del Rey Mago (mira hacia +x), con brazos y piernas articulados
function figNav(spec){const g=new THREE.Group(),t=spec.t,M=(c,r_=.7)=>new THREE.MeshStandardMaterial({color:c,roughness:r_});
 const C={sleigh:[0xc4161f,0xf0c8a8,0xffffff,0x161414],aurum:[0x8e1a2a,0xf0c8a8,0xf2f2ee,0xf5c84a],mirra:[0x2a4fa8,0xe8bf9a,0x8a4a22,0xf5c84a],esmeralda:[0x0f6a3c,0x6b4226,0x1a1a1a,0xf5c84a]}[t]||[0xc4161f,0xf0c8a8,0xffffff,0x161414];
 const ROPA=M(C[0]),PIEL=M(C[1]),BAR=M(C[2],.9),FAJ=M(C[3],t==='sleigh'?.4:.25),BL=M(0xffffff,.9),BOT=M(0x1a1612,.5),ORO=new THREE.MeshStandardMaterial({color:0xf5c84a,roughness:.25,metalness:.9});
 const add=(geo,mat,x,y,z,par=g)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);par.add(m);return m};
 add(new THREE.CylinderGeometry(.011,.0145,.03,12),ROPA,0,.046,0);add(new THREE.CylinderGeometry(.0148,.0148,.004,12),t==='sleigh'?BL:ORO,0,.032,0);add(new THREE.CylinderGeometry(.0128,.0128,.004,12),FAJ,0,.047,0);
 if(t==='sleigh')add(new THREE.BoxGeometry(.004,.005,.004),ORO,.013,.047,0);else{const ca=add(new THREE.BoxGeometry(.004,.034,.03),M(spec.col[0],.5),-.012,.046,0);ca.rotation.z=-.08}
 add(new THREE.SphereGeometry(.0095,12,9),PIEL,.001,.069,0);add(new THREE.SphereGeometry(.0092,10,8),BAR,.006,.063,0).scale.set(.9,1.2,1.15);
 for(const z of[.0035,-.0035])add(new THREE.SphereGeometry(.0014,6,5),BOT,.0088,.071,z);
 if(t==='sleigh'){const h=add(new THREE.ConeGeometry(.0095,.024,12),ROPA,-.002,.086,0);h.rotation.z=.45;add(new THREE.TorusGeometry(.0088,.0026,6,14),BL,.0,.077,0).rotation.x=Math.PI/2;add(new THREE.SphereGeometry(.0033,8,6),BL,-.009,.093,0)}
 else{add(new THREE.CylinderGeometry(.0092,.0085,.009,12,1,true),ORO,.001,.08,0);for(let k=0;k<6;k++){const a=k/6*6.283;add(new THREE.ConeGeometry(.0018,.006,5),ORO,.001+Math.cos(a)*.009,.087,Math.sin(a)*.009)}add(new THREE.SphereGeometry(.0018,6,5),M(0xc81830,.3),.0098,.081,0)}
 const br=[],pi=[];for(const z of[.0145,-.0145]){const pv=new THREE.Group();pv.position.set(0,.057,z);g.add(pv);add(new THREE.CylinderGeometry(.0042,.0036,.022,8),ROPA,0,-.011,0,pv);add(new THREE.SphereGeometry(.0042,8,6),t==='sleigh'?BOT:PIEL,0,-.023,0,pv);br.push(pv)}
 for(const z of[.0062,-.0062]){const pv=new THREE.Group();pv.position.set(0,.032,z);g.add(pv);add(new THREE.CylinderGeometry(.0048,.0042,.026,8),t==='sleigh'?ROPA:M(0x2a2420),0,-.013,0,pv);add(new THREE.BoxGeometry(.011,.006,.007),BOT,.002,-.028,0,pv);pi.push(pv)}
 g.userData={br,pi};g.traverse(o=>{if(o.isMesh)o.castShadow=true});return g}
// la moto de agua del reparto: piloto navideño sentado y regalos atados detrás
function motoNavPon(extra){motoNavQuita();const sp=REP.spec||{t:'sleigh',col:[0xc4161f]};const pil=moto.children.find(c=>c.userData&&c.userData.piernas);if(pil)pil.visible=false;
 const g=new THREE.Group();g.name='motoNav';const f=figNav(sp);f.position.set(-.02,.01,0);f.userData.pi.forEach(p=>p.rotation.z=1.25);f.userData.br.forEach(p=>p.rotation.z=1.15);g.add(f);
 const CR=[0xd51f1f,0x1fae4a,0xf2c230,0x1f6fd0,0xc23fd0],O=new THREE.MeshStandardMaterial({color:0xffd24a,emissive:0x8a6000,emissiveIntensity:.4,roughness:.4});
 const caja=(x,y,z,sz,c)=>{const b=new THREE.Mesh(new THREE.BoxGeometry(sz,sz,sz),new THREE.MeshStandardMaterial({color:c,roughness:.5}));b.position.set(x,y,z);g.add(b);for(const[a,bb,cc]of[[sz*1.04,sz*1.04,sz*.22],[sz*.22,sz*1.04,sz*1.04]]){const q=new THREE.Mesh(new THREE.BoxGeometry(a,bb,cc),O);q.position.copy(b.position);g.add(q)}};
 caja(-.052,.038,.008,.018,CR[0]);caja(-.052,.038,-.011,.015,CR[1]);caja(-.054,.055,0,.014,CR[2]);caja(-.064,.03,0,.012,CR[3]);if(extra)caja(-.03,.06,0,.02,CR[4]);moto.add(g)}
function motoNavQuita(){const g=moto.getObjectByName('motoNav');if(g)moto.remove(g);const pil=moto.children.find(c=>c.userData&&c.userData.piernas);if(pil)pil.visible=true}
// punto de buceo: agua cerca de la costa, a unos cientos de metros del puerto
function buceoSitio(pu){const L=[];for(let rr=2.5;rr<=9;rr+=.5)for(let k=0;k<48;k++){const a=k/48*6.2832,x=pu[0]+Math.cos(a)*rr,y=pu[1]+Math.sin(a)*rr;if(!aguaOK(x,y))continue;
  let cerca=false,lejos=true;for(let q=0;q<12;q++){const b=q/12*6.2832;if(cell(x+Math.cos(b)*.5,y+Math.sin(b)*.5).t!==0)cerca=true;if(cell(x+Math.cos(b)*.22,y+Math.sin(b)*.22).t!==0)lejos=false}if(cerca&&lejos)L.push([x,y])}
 return L.length?L[Math.floor(Math.random()*L.length)]:null}
function buceoInicio(m,pu,k){const mo=(FERRY_DEST['Moaña']||[[0,0],[76.26,-35.52]])[1],D=aguaCerca(pu[0]+(mo[0]-pu[0])*.5,pu[1]+(mo[1]-pu[1])*.5,4)||buceoSitio(pu);if(!D)return false;REP.rad=Math.max(REP.rad||0,Math.hypot(D[0]-REP_DEP[1],D[1]-REP_DEP[2])+2);REP.puerto=['Puerto de Vigo',pu[0],pu[1]];campVeh('moto',pu[0],pu[1],Math.atan2(-(D[1]-pu[1]),D[0]-pu[0]));REP.mis=m;motoNavPon(false);
 Object.assign(BUC,{on:true,fase:'ir',D,t:0,tiene:false,aire:1,W:null,av:0});REP.fase='bucear';
 // boya roja y blanca con banderín
 const b=new THREE.Group(),Mb=c=>new THREE.MeshStandardMaterial({color:c,roughness:.5,emissive:c,emissiveIntensity:.25});for(let q=0;q<4;q++){const c=new THREE.Mesh(new THREE.CylinderGeometry(.022-q*.003,.024-q*.003,.018,14),Mb(q%2?0xffffff:0xd51f1f));c.position.y=q*.018;b.add(c)}
 const pa=new THREE.Mesh(new THREE.CylinderGeometry(.002,.002,.08,6),Mb(0x333333));pa.position.y=.1;b.add(pa);const fl=new THREE.Mesh(new THREE.PlaneGeometry(.035,.022),new THREE.MeshBasicMaterial({color:0xffd24a,side:THREE.DoubleSide}));fl.position.set(.018,.125,0);b.add(fl);
 b.position.set(D[0]+.12,moto.position.y,D[1]);scene.add(b);REP.objs.push(b);BUC.boya=b;
 campDestino(['🤿 Medio de la Ría',D[0],D[1]]);
 aviso('🌊 Misión '+(k+1)+' · ¡Regalo perdido en el mar!',2.2,'cuenta');setTimeout(()=>{if(REP.on&&!REP.fin)mostrar('Navega hasta la boya en medio de la Ría: allí se cayó un regalo al fondo del mar')},2400);return true}
function buceoObjetivo(){if(BUC.fase==='saltar'&&MODO==='moto'){objetivo={k:'buceo'};return '🤿 Tirarse al agua'}if(MODO==='nado'){const d=BUC.moto?Math.hypot(BUC.moto.position.x-P.x,BUC.moto.position.z-P.y):9;if(d<.16&&P.z>BUC.WY-.05){objetivo={k:'buceo'};return 'Subir a la moto'}objetivo=null;return null}}
function buceoAccion(){if(BUC.fase==='saltar'&&MODO==='moto'){buceoSalta();return true}
 if(MODO==='nado'){const d=Math.hypot(BUC.moto.position.x-P.x,BUC.moto.position.z-P.y);if(d<.16&&P.z>BUC.WY-.05){if(BUC.tiene)buceoSube();else mostrar('Primero encuentra el regalo perdido en el fondo');return true}mostrar(P.z>BUC.WY-.05?'⤓ Z / LB para bucear · busca el brillo dorado en el fondo':'Nada hasta la moto para subir');return true}return false}
function buceoTick(dt){const B=BUC;B.t+=dt;if(B.boya){B.boya.position.y=(B.WY||moto.position.y)+Math.sin(B.t*2.2)*.006;B.boya.rotation.z=Math.sin(B.t*1.7)*.12}
 if(B.W)buceoMundoTick(dt);
 if(B.fase==='ir'||B.fase==='saltar'){if(MODO!=='moto')return;const d=Math.hypot(B.D[0]-P.x,B.D[1]-P.y);if(B.fase==='ir'&&d<.38){B.fase='saltar';B.av=0}else if(B.fase==='saltar'&&d>.65)B.fase='ir';
  if(B.fase==='saltar'){B.av-=dt;if(B.av<=0){B.av=3;mostrar(document.body.classList.contains('pad')?'Ⓐ para tirarte al agua y bucear':'E (o el botón de acción) para tirarte al agua y bucear')}}return}
 if(B.fase==='nado'&&!B.tiene){const R=B.reg;R.g.rotation.y+=dt;const d=Math.hypot(R.x-P.x,R.y-P.y,R.z-P.z);if(d<.075){B.tiene=true;scene.remove(R.g);try{sonMoneda();setTimeout(sonJoJo,200)}catch(e){}repPop('🎁 ¡Regalo encontrado!','gran');REP.pts+=100;
   const c=new THREE.Mesh(new THREE.BoxGeometry(.016,.016,.016),new THREE.MeshStandardMaterial({color:0xc23fd0,emissive:0xc23fd0,emissiveIntensity:.4}));c.position.set(.02,.03,.018);B.nad.add(c);
   REP.dest=['🛥️ Tu moto de agua',B.moto.position.x,B.moto.position.z];gpsSet(REP.dest,linea([[P.x,P.y],[REP.dest[1],REP.dest[2]]]));setTimeout(()=>{if(BUC.on)mostrar('¡Lo tienes! Sube a respirar y nada hasta la moto de agua')},900)}}}
// ---------- el mundo bajo el agua
function buceoMat(c,rg=.95){const m=new THREE.MeshStandardMaterial({color:c,roughness:rg});m.onBeforeCompile=sh=>{sh.uniforms.uT=BUC.uT;
  sh.vertexShader='varying vec3 vWpB;\n'+sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\n vWpB=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='uniform float uT;varying vec3 vWpB;\n'+sh.fragmentShader.replace('#include <dithering_fragment>','#include <dithering_fragment>\n {vec2 q=vWpB.xz*34.;float c=pow(abs(sin(q.x+uT*1.3+sin(q.y*.7+uT))*sin(q.y+uT*1.1+sin(q.x*.8-uT*.7))),5.);gl_FragColor.rgb+=c*vec3(.3,.5,.55)*smoothstep(-.4,.1,vWpB.y-'+('%.3f'%0)+'-uT*0.);}')};
 m.customProgramCacheKey=()=>'cau';return m}
function buceoMundo(D,WY){const B=BUC,G=new THREE.Group();G.name='fondoMar';B.uT=B.uT||{value:0};const RZ=1.35,DEP=.32;let sd=7;const rn=()=>(sd=(sd*16807)%2147483647)/2147483647;
 const dTierra=(x,y)=>{for(let r_=.03;r_<=.5;r_+=.05)for(let q=0;q<8;q++){const a=q*.785;if(cell(x+Math.cos(a)*r_,y+Math.sin(a)*r_).t!==0)return r_}return .5};
 const N=56,S=RZ*2/N,H=new Float32Array((N+1)*(N+1));for(let j=0;j<=N;j++)for(let i=0;i<=N;i++){const x=D[0]-RZ+i*S,y=D[1]-RZ+j*S,dl=dTierra(x,y),k=THREE.MathUtils.smoothstep(dl,.02,.48);
  H[j*(N+1)+i]=WY-.03-DEP*k+Math.sin(x*23)*Math.cos(y*19)*.012+Math.sin(x*61+y*47)*.006}
 B.hB=(x,y)=>{const fi=(x-(D[0]-RZ))/S,fj=(y-(D[1]-RZ))/S;if(fi<0||fj<0||fi>=N||fj>=N)return WY-DEP;const i=Math.floor(fi),j=Math.floor(fj),u=fi-i,v=fj-j,a=H[j*(N+1)+i],b=H[j*(N+1)+i+1],c=H[(j+1)*(N+1)+i],d=H[(j+1)*(N+1)+i+1];return a*(1-u)*(1-v)+b*u*(1-v)+c*(1-u)*v+d*u*v};
 const pg=new THREE.PlaneGeometry(RZ*2,RZ*2,N,N);pg.rotateX(-Math.PI/2);const pp=pg.attributes.position;for(let k=0;k<pp.count;k++){const x=pp.getX(k)+D[0],y=pp.getZ(k)+D[1];pp.setY(k,B.hB(x,y))}pg.translate(D[0],0,D[1]);pg.computeVertexNormals();
 const fondo=new THREE.Mesh(pg,buceoMat(0xc9b48a));fondo.receiveShadow=true;G.add(fondo);
 const enAgua=(x,y)=>cell(x,y).t===0;const sitio=()=>{for(let t=0;t<30;t++){const a=rn()*6.283,r_=Math.sqrt(rn())*(RZ-.08),x=D[0]+Math.cos(a)*r_,y=D[1]+Math.sin(a)*r_;if(enAgua(x,y))return[x,y]}return[D[0],D[1]]};
 // rocas (más cerca de la costa), con corales y anémonas encima
 const ROC=[buceoMat(0x5a6660),buceoMat(0x6d7468),buceoMat(0x4c5550)],COR=[0xff6a5a,0xffa53a,0xc04ad8,0xff4f9a,0xf2e35a,0x3fe0c0].map(c=>new THREE.MeshStandardMaterial({color:c,roughness:.6,emissive:c,emissiveIntensity:.15}));
 for(let k=0;k<46;k++){const p=sitio(),sz=.025+Math.pow(rn(),2)*.11,ge=new THREE.DodecahedronGeometry(1,1),pa=ge.attributes.position;for(let q=0;q<pa.count;q++){const f=.8+.35*Math.sin(pa.getX(q)*5+k)*Math.cos(pa.getZ(q)*4+k*.7);pa.setXYZ(q,pa.getX(q)*f,pa.getY(q)*f*.7,pa.getZ(q)*f)}ge.computeVertexNormals();
  const m=new THREE.Mesh(ge,ROC[k%3]);m.scale.set(sz*(1+rn()*.6),sz,sz*(1+rn()*.5));m.rotation.y=rn()*6;m.position.set(p[0],B.hB(p[0],p[1])+sz*.25,p[1]);m.castShadow=m.receiveShadow=true;G.add(m);
  for(let q=0;q<(sz>.05?4:1);q++){const a=rn()*6.283,rr=sz*.5*rn(),x=p[0]+Math.cos(a)*rr,y=p[1]+Math.sin(a)*rr,z=m.position.y+sz*.5,cm=COR[Math.floor(rn()*COR.length)];
   if(rn()<.5){const c=new THREE.Mesh(new THREE.ConeGeometry(.006,.03+rn()*.03,6),cm);c.position.set(x,z+.012,y);c.rotation.set(rn()-.5,0,rn()-.5);G.add(c)}else{const c=new THREE.Mesh(new THREE.SphereGeometry(.008+rn()*.008,8,6),cm);c.scale.y=.6;c.position.set(x,z,y);G.add(c)}}}
 // estrellas de mar y erizos sobre la arena
 {const sh=new THREE.Shape();for(let q=0;q<10;q++){const a=q/10*6.283,r_=q%2?.4:1;q?sh.lineTo(Math.cos(a)*r_,Math.sin(a)*r_):sh.moveTo(r_,0)}const eg=new THREE.ExtrudeGeometry(sh,{depth:.25,bevelEnabled:true,bevelThickness:.12,bevelSize:.12,bevelSegments:1});eg.rotateX(-Math.PI/2);
  for(let k=0;k<18;k++){const p=sitio(),m=new THREE.Mesh(eg,new THREE.MeshStandardMaterial({color:[0xff6a2a,0xe03a3a,0xffb23a][k%3],roughness:.7}));m.scale.setScalar(.011+rn()*.006);m.position.set(p[0],B.hB(p[0],p[1])+.002,p[1]);m.rotation.y=rn()*6;G.add(m)}
  const er=new THREE.MeshStandardMaterial({color:0x3a1840,roughness:.5});for(let k=0;k<14;k++){const p=sitio(),m=new THREE.Mesh(new THREE.IcosahedronGeometry(.009,1),er);m.scale.y=.7;m.position.set(p[0],B.hB(p[0],p[1])+.005,p[1]);G.add(m)}}
 // algas: dos planos cruzados por alga, se mecen con la corriente en el sombreador
 {const a1=new THREE.PlaneGeometry(.009,1,1,10);a1.translate(0,.5,0);const a2=a1.clone();a2.rotateY(Math.PI/2);const ag=mergeGeometries([a1,a2]);
  const am=new THREE.MeshStandardMaterial({color:0x3f8a3a,roughness:.8,side:THREE.DoubleSide,emissive:0x0d2a10,emissiveIntensity:.5});am.onBeforeCompile=sh=>{sh.uniforms.uT=B.uT;sh.vertexShader='uniform float uT;\n'+sh.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\n {float hh=position.y;vec4 ip=instanceMatrix[3];transformed.x+=sin(uT*1.6+ip.x*37.+ip.z*23.+hh*3.)*hh*hh*.05;transformed.z+=cos(uT*1.25+ip.z*41.+hh*2.)*hh*hh*.04;}')};am.customProgramCacheKey=()=>'alga';
  const NA=170,im=new THREE.InstancedMesh(ag,am,NA),du=new THREE.Object3D(),cc=new THREE.Color();let n=0;for(let c=0;c<16;c++){const p=sitio();for(let q=0;q<11&&n<NA;q++){const x=p[0]+(rn()-.5)*.12,y=p[1]+(rn()-.5)*.12;if(!enAgua(x,y))continue;const fz=B.hB(x,y),hmax=Math.max(.06,WY-.03-fz);
   du.position.set(x,fz,y);du.rotation.set(0,rn()*3,0);du.scale.set(1,Math.min(hmax,.08+rn()*.22),1);du.updateMatrix();im.setMatrixAt(n,du.matrix);im.setColorAt(n,cc.setHSL(.26+rn()*.12,.55,.28+rn()*.18));n++}}im.count=n;im.frustumCulled=false;G.add(im)}
 // bancos de peces de colores y algún pez grande
 {const b1=new THREE.SphereGeometry(1,8,6);b1.scale(1,.45,.32);const t1=new THREE.ConeGeometry(.5,.6,4);t1.rotateZ(Math.PI/2);t1.translate(-1.15,0,0);const fg=mergeGeometries([b1.toNonIndexed(),t1.toNonIndexed()]);
  const fm=new THREE.MeshStandardMaterial({roughness:.35,metalness:.3}),NP=96,im=new THREE.InstancedMesh(fg,fm,NP),cc=new THREE.Color();
  const BAN=[];for(let k=0;k<4;k++){const p=sitio();BAN.push({x:p[0],y:p[1],z:WY-.06-rn()*.18,w:(rn()<.5?1:-1)*(.35+rn()*.4),col:[0xffa21a,0xf2e35a,0x4ab8ff,0xd8e4ea][k],big:k===3})}
  const PZ=[];for(let i=0;i<NP;i++){const b=BAN[i%4];PZ.push({b,ph:rn()*6.283,r:.07+rn()*.16,dy:(rn()-.5)*.06,s:b.big?(i<8?.03:.011):.009+rn()*.006});im.setColorAt(i,cc.setHex(b.col).offsetHSL((rn()-.5)*.05,0,(rn()-.5)*.15))}
  im.frustumCulled=false;G.add(im);B.peces={im,PZ,BAN,du:new THREE.Object3D()}}
 // superficie vista desde abajo
 {const sm=new THREE.ShaderMaterial({uniforms:{uT:B.uT},transparent:true,depthWrite:false,side:THREE.DoubleSide,vertexShader:'varying vec2 vP;void main(){vec4 w=modelMatrix*vec4(position,1.);vP=w.xz;gl_Position=projectionMatrix*viewMatrix*w;}',
   fragmentShader:'uniform float uT;varying vec2 vP;void main(){vec2 q=vP*18.;float w=sin(q.x+uT*1.2+sin(q.y*.8+uT))*.5+.5;w*=sin(q.y*1.3-uT+sin(q.x*.6))*.5+.5;gl_FragColor=vec4(mix(vec3(.25,.6,.75),vec3(.85,1.,1.),pow(w,2.)),.55+.3*w);}'});
  const sp=new THREE.Mesh(new THREE.CircleGeometry(RZ*1.3,48),sm);sp.rotation.x=Math.PI/2;sp.position.set(D[0],WY-.004,D[1]);sp.renderOrder=2;G.add(sp);B.sup=sp}
 // rayos de luz que bajan de la superficie
 {const cv=document.createElement('canvas');cv.width=32;cv.height=128;const c=cv.getContext('2d'),gr=c.createLinearGradient(0,0,0,128);gr.addColorStop(0,'rgba(220,250,255,.55)');gr.addColorStop(1,'rgba(220,250,255,0)');c.fillStyle=gr;c.fillRect(0,0,32,128);const g2=c.createLinearGradient(0,0,32,0);g2.addColorStop(0,'rgba(0,0,0,1)');g2.addColorStop(.5,'rgba(0,0,0,0)');g2.addColorStop(1,'rgba(0,0,0,1)');c.globalCompositeOperation='destination-out';c.fillStyle=g2;c.fillRect(0,0,32,128);
  const rm=new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(cv),transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,fog:false});B.rayos=[];for(let k=0;k<10;k++){const p=sitio(),m=new THREE.Mesh(new THREE.PlaneGeometry(.07+rn()*.08,.42),rm);m.position.set(p[0],WY-.2,p[1]);m.rotation.z=(rn()-.5)*.5;m.userData.ph=rn()*6;G.add(m);B.rayos.push(m)}}
 // partículas en suspensión y burbujas
 {const NPa=420,ge=new THREE.BufferGeometry(),ps=new Float32Array(NPa*3);for(let k=0;k<NPa;k++){const p=sitio();ps.set([p[0],WY-.02-rn()*DEP,p[1]],k*3)}ge.setAttribute('position',new THREE.BufferAttribute(ps,3));
  const pm=new THREE.PointsMaterial({color:0xcff4ff,size:.006,transparent:true,opacity:.6,depthWrite:false});const pt=new THREE.Points(ge,pm);pt.frustumCulled=false;G.add(pt);B.part=pt;
  const NB=60,bg=new THREE.BufferGeometry(),bp=new Float32Array(NB*3);for(let k=0;k<NB;k++)bp[k*3+1]=-99;bg.setAttribute('position',new THREE.BufferAttribute(bp,3));const bu=new THREE.Points(bg,new THREE.PointsMaterial({color:0xeaffff,size:.01,transparent:true,opacity:.8,depthWrite:false}));bu.frustumCulled=false;G.add(bu);B.burb={bu,bp,NB,k:0,v:new Float32Array(NB)}}
 // esfera de niebla (tapa el cielo cuando la cámara está bajo el agua)
 {const fm=new THREE.MeshBasicMaterial({color:0x0b5b7c,side:THREE.BackSide,depthWrite:false,fog:false});const fs=new THREE.Mesh(new THREE.SphereGeometry(1.6,24,16),fm);fs.renderOrder=-5;fs.visible=false;G.add(fs);B.esf=fs}
 scene.add(G);B.W=G;B.RZ=RZ}
function buceoMundoTick(dt){const B=BUC;B.uT.value+=dt;const t=B.uT.value;
 if(B.peces){const{im,PZ,BAN,du}=B.peces;for(const b of BAN){b.cx=b.x+Math.sin(t*.13+b.z*9)*.15;b.cy=b.y+Math.cos(t*.11+b.x)*.15}
  PZ.forEach((f,i)=>{const b=f.b;let r_=f.r;const a=t*b.w*(b.big?.4:1)+f.ph,x0=b.cx+Math.cos(a)*r_,y0=b.cy+Math.sin(a)*r_,dP=Math.hypot(x0-P.x,y0-P.y);if(MODO==='nado'&&dP<.15)r_+=(.15-dP)*2.5;
   const x=b.cx+Math.cos(a)*r_,y=b.cy+Math.sin(a)*r_,z=Math.max(B.hB(x,y)+.02,Math.min(B.WY-.03,b.z+f.dy+Math.sin(t*2+i)*.012));du.position.set(x,z,y);
   const vx=-Math.sin(a)*Math.sign(b.w),vy=Math.cos(a)*Math.sign(b.w);du.rotation.set(0,Math.atan2(-vy,vx)+Math.sin(t*9+i)*.15,0);du.scale.setScalar(f.s);du.updateMatrix();im.setMatrixAt(i,du.matrix)});im.instanceMatrix.needsUpdate=true}
 for(const m of B.rayos){m.material.opacity=.5+.35*Math.sin(t*.8+m.userData.ph);m.lookAt(pcam.position.x,m.position.y,pcam.position.z)}
 if(B.burb){const u=B.burb;if(MODO==='nado'&&P.z<B.WY-.025&&Math.random()<.35){u.k=(u.k+1)%u.NB;u.bp.set([P.x+(Math.random()-.5)*.01,P.z+.03,P.y+(Math.random()-.5)*.01],u.k*3);u.v[u.k]=.06+Math.random()*.05}
  if(B.reg&&!B.tiene&&Math.random()<.15){u.k=(u.k+1)%u.NB;u.bp.set([B.reg.x+(Math.random()-.5)*.02,B.reg.z+.02,B.reg.y],u.k*3);u.v[u.k]=.05}
  for(let k=0;k<u.NB;k++){if(u.bp[k*3+1]<B.WY-.005){u.bp[k*3+1]+=u.v[k]*dt;u.bp[k*3]+=Math.sin(t*6+k)*.0004}else u.bp[k*3+1]=-99}u.bu.geometry.attributes.position.needsUpdate=true}}
function buceoSalta(){const B=BUC;B.WY=moto.position.y;if(!B.W)buceoMundo(B.D,B.WY);
 // la moto se queda flotando con los regalos; Papá Noel se tira al agua
 const mc=moto.clone(true);const fig=mc.getObjectByName('motoNav');if(fig&&fig.children[0])fig.children[0].visible=false;mc.position.copy(moto.position);mc.rotation.copy(moto.rotation);scene.add(mc);REP.objs.push(mc);B.moto=mc;
 const nad=new THREE.Group(),f=figNav(REP.spec||{t:'sleigh',col:[0xc4161f]});f.position.x=-.045;f.rotation.z=-1.25;nad.add(f);nad.userData.f=f;const lz=new THREE.PointLight(0xa8ecff,0,.9,1.5);lz.position.set(.05,.02,0);nad.add(lz);nad.userData.luz=lz;scene.add(nad);B.nad=nad;
 // regalo perdido en el fondo, a cierta distancia de la moto
 let rg=null;for(let t=0;t<40&&!rg;t++){const a=Math.random()*6.283,d=.35+Math.random()*.45,x=P.x+Math.cos(a)*d,y=P.y+Math.sin(a)*d;if(cell(x,y).t===0&&B.hB(x,y)<B.WY-.12&&Math.hypot(x-B.D[0],y-B.D[1])<B.RZ-.15)rg=[x,y]}if(!rg)rg=[P.x+.3,P.y];
 const R=introRegalo(rg[0],rg[1],B.hB(rg[0],rg[1])+.03,0,1);R.haz.visible=true;R.haz.scale.y=.6;R.g.rotation.z=.4;B.reg=R;
 const px=P.x,py=P.y;cambiarModo('nado');document.body.classList.add('heli');P.x=px+Math.sin(P.a)*.06;P.y=py+Math.cos(P.a)*.06;P.z=B.WY-.012;P.v=0;P.vz=0;camInit=false;B.fase='nado';B.aire=1;B.tiene=false;
 document.getElementById('aire').hidden=false;REP.dest=['🎁 Regalo perdido',rg[0],rg[1]];gpsSet(REP.dest,linea([[P.x,P.y],[rg[0],rg[1]]]));try{sonCaja()}catch(e){}
 setTimeout(()=>{if(BUC.on&&BUC.fase==='nado')mostrar(document.body.classList.contains('pad')?'Joystick derecho: ↓ bucea · ↑ sube · joystick izquierdo para nadar · busca el regalo que brilla':'⤓ Z bucea · ⤒ Q sube · ▲ nada · busca el regalo que brilla en el fondo')},700)}
function updateNado(dt){const B=BUC;if(!REP.on||!B.on){buceoLimpia();cambiarModo('coche');return}
 const sup=B.WY-.012,bajo=P.z<sup-.015,tnow=performance.now()/1000;
 const tgt=keys.up?(bajo?.3:.24):keys.down?-.08:0;P.v+=(tgt-P.v)*Math.min(1,dt*3);const steer=(keys.left?1:0)-(keys.right?1:0);P.a+=steer*2.2*dt;
 const vzt=PAD.ry?-PAD.ry*.3:keys.alt_dn?-.22:keys.alt_up?.24:(bajo?.035:0);P.vz=(P.vz||0)+(vzt-(P.vz||0))*Math.min(1,dt*3);
 let nx=P.x+Math.cos(P.a)*P.v*dt,ny=P.y-Math.sin(P.a)*P.v*dt;if(cell(nx,ny).t!==0||Math.hypot(nx-B.D[0],ny-B.D[1])>B.RZ-.06){P.v*=.3;nx=P.x;ny=P.y;if(!B.avB||tnow-B.avB>3){B.avB=tnow;mostrar('Hasta aquí: no te alejes de la zona de buceo')}}P.x=nx;P.y=ny;
 P.z+=P.vz*dt;const fz=B.hB(P.x,P.y)+.022;if(P.z<fz){P.z=fz;if(P.vz<0)P.vz=0}if(P.z>sup){P.z=sup;if(P.vz>0)P.vz=0}
 // aire: se gasta bajo el agua y se recupera en la superficie
 if(bajo){B.aire-=dt/26;if(B.aire<=0){B.aire=0;P.vz=.4;if(!B.avA||tnow-B.avA>2.5){B.avA=tnow;mostrar('¡Sin aire! Sube a la superficie')}}}else B.aire=Math.min(1,B.aire+dt*.5);
 const ai=document.querySelector('#aire i');ai.style.width=(B.aire*100).toFixed(0)+'%';ai.style.background=B.aire<.25?'linear-gradient(90deg,#ff5a3a,#ffb08a)':'linear-gradient(90deg,#3fd0ff,#bff4ff)';
 // nadador: horizontal bajo el agua, más inclinado en la superficie; brazos a crol y patada de piernas
 const N_=B.nad,f=N_.userData.f,inc=bajo?-Math.PI/2+Math.max(-.6,Math.min(.6,P.vz*2.5)):-1.2;f.rotation.z+=(inc-f.rotation.z)*Math.min(1,dt*5);
 const vel=Math.min(1,Math.abs(P.v)*4+.25);f.userData.br[0].rotation.z=Math.PI+tnow*5*vel;f.userData.br[1].rotation.z=tnow*5*vel;f.userData.pi[0].rotation.z=Math.sin(tnow*9)*.45*vel;f.userData.pi[1].rotation.z=-Math.sin(tnow*9)*.45*vel;
 N_.position.set(P.x,P.z+(bajo?0:Math.sin(tnow*3)*.003),P.y);N_.rotation.set(0,P.a,0);N_.userData.luz.intensity=bajo?1.3:0;
 if(B.moto){B.moto.position.y=B.WY+Math.sin(tnow*2)*.003;B.moto.rotation.z=Math.sin(tnow*1.6)*.04}
 // cámara: detrás del nadador
 const dx=Math.cos(P.a),dz=-Math.sin(P.a),dist=bajo?.24:.32,hg=bajo?.05:.12;const want=new THREE.Vector3(P.x-dx*dist,Math.max(P.z+hg,B.hB(P.x-dx*dist,P.y-dz*dist)+.04),P.y-dz*dist);
 if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*4));look.set(P.x+dx*.12,P.z-(bajo?.01:.03),P.y+dz*.12);pcam.lookAt(look);pcam.fov=62;pcam.updateProjectionMatrix();
 // efecto océano: niebla azul, velo, esfera que tapa el cielo
 const camBajo=pcam.position.y<B.WY-.003;window.__BAJO=camBajo;document.getElementById('bajoAgua').hidden=!camBajo;B.esf.visible=camBajo;for(const w of WATERS)w.visible=!camBajo;B.esf.position.copy(pcam.position);B.part.visible=camBajo;for(const m of B.rayos)m.visible=camBajo;B.sup.visible=camBajo;
 if(camBajo){const pr=Math.min(1,(B.WY-pcam.position.y)/.3);FOG.color.setRGB(.03+.03*(1-pr),.3-.12*pr,.43-.12*pr);B.esf.material.color.copy(FOG.color);FOG.near=.02;FOG.far=1.25-.35*pr}else{FOG.near=5;FOG.far=20}
 const v=document.getElementById('vel');v.firstChild.nodeValue=Math.max(0,Math.round((sup-P.z)*70));v.querySelector('small').textContent='m de profundidad · Z bucea · Q sube';hudAccion(dt)}
function buceoSube(){const B=BUC,mc=B.moto;P.x=mc.position.x;P.y=mc.position.z;P.v=0;scene.remove(mc);B.moto=null;scene.remove(B.nad);B.nad=null;buceoLimpia(true);cambiarModo('moto');motoNavPon(true);camInit=false;
 B.on=false;REP.fase='entregar';campDestino(['🎁 Puerto de Vigo',REP.puerto[1],REP.puerto[2]]);aviso('🎁 ¡Rescatado! Llévalo al Puerto de Vigo',2.4,'cuenta')}
function buceoLimpia(sube){const B=BUC;window.__BAJO=false;for(const w of WATERS)w.visible=true;FOG.near=5;FOG.far=20;document.getElementById('bajoAgua').hidden=true;document.getElementById('aire').hidden=true;document.body.classList.remove('heli');
 if(B.W){scene.remove(B.W);B.W.traverse(o=>{if(o.geometry)o.geometry.dispose()});B.W=null}if(B.boya){scene.remove(B.boya);B.boya=null}if(B.reg){scene.remove(B.reg.g);B.reg=null}if(!sube){if(B.moto){scene.remove(B.moto);B.moto=null}if(B.nad){scene.remove(B.nad);B.nad=null}B.on=false}}
function repCocheCalle(){""")
r("const aU=heli&&(P_(5)||ry<-.5),aD=heli&&(P_(4)||ry>.5);","const nad=MODO==='nado';PAD.ry=nad?ry:0;const aU=(heli||nad)&&(P_(5)||ry<-.3),aD=(heli||nad)&&(P_(4)||ry>.3);")
r("if(dn(4)&&!heli)pitar()","if(dn(4)&&!heli&&MODO!=='nado')pitar()")
r("if(NAV.tr&&REP.spec)navEstela(","if(NAV.tr&&REP.spec&&MODO!=='nado')navEstela(")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok buceo')
