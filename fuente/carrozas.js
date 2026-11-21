// ---------- las cuatro carrozas de serie (edit_carrozas.py): Sleigh GT (Papá Noel), Aurum (Melchor), Mirra (Gaspar) y Esmeralda (Baltasar)
// Mismas medidas y misma llamada que las de antes (eje x hacia delante, y arriba). Todas las piezas se juntan en una malla por material
// (unas 15 por carroza en vez de 60-90 sueltas), así que siguen siendo mallas sueltas sin grupos anidados y vestirCoche las copia igual.
// La pintura (pint) va en las mallas 'carroceria'.
const _CZ={};const czMat=(k,f)=>_CZ[k]||(_CZ[k]=f());
function carroza(g,tipo,pint,bx,ruedas4,luces){
 const V2=THREE.Vector2,V3=THREE.Vector3,PI=Math.PI;
 const ORO=MV(0xf5c84a,.22,.95),ORO2=MV(0xc9952a,.3,.85),NEGRO=MV(0x16171c,.6),BLANCO=MV(0xf6f4ee,.9),GOMA=MV(0x141418,.9),CROMO=MV(0xd8dbe0,.18,.9);
 const led=c=>czMat('led'+c,()=>new THREE.MeshBasicMaterial({color:c,toneMapped:false}));
 const brillo=(c,k=.9)=>czMat('br'+c+'_'+k,()=>new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:k,roughness:.4}));
 const tela=c=>czMat('tela'+c,()=>new THREE.MeshStandardMaterial({color:c,roughness:.9,side:THREE.DoubleSide}));
 const CRISTAL=czMat('cristal',()=>new THREE.MeshStandardMaterial({color:0x8fd0ff,roughness:.05,metalness:.3,transparent:true,opacity:.38,side:THREE.DoubleSide,depthWrite:false}));
 // ---- todas las piezas van a un cubo por material y al final se juntan
 const B=new Map(),put=(geo,m)=>{if(!B.has(m))B.set(m,[]);B.get(m).push(geo);return geo};
 const O=new THREE.Object3D();
 const P=(geo,m,x=0,y=0,z=0,rx=0,ry=0,rz=0,sx=1,sy=1,sz=1)=>{O.position.set(x,y,z);O.rotation.set(rx,ry,rz);O.scale.set(sx,sy,sz);O.updateMatrix();geo.applyMatrix4(O.matrix);return put(geo,m)};
 const caja=(l,h,w,m,x,y,z,rx=0,ry=0,rz=0)=>P(new THREE.BoxGeometry(l,h,w),m,x,y,z,rx,ry,rz);
 const cil=(r1,r2,h,m,x,y,z,rx=0,ry=0,rz=0,seg=12)=>P(new THREE.CylinderGeometry(r1,r2,h,seg),m,x,y,z,rx,ry,rz);
 const esf=(r,m,x,y,z,sx=1,sy=1,sz=1,seg=10)=>P(new THREE.SphereGeometry(r,seg,Math.max(5,seg*2/3|0)),m,x,y,z,0,0,0,sx,sy,sz);
 const cono=(r,h,m,x,y,z,rx=0,ry=0,rz=0,seg=10)=>P(new THREE.ConeGeometry(r,h,seg),m,x,y,z,rx,ry,rz);
 const aro=(R,t,m,x,y,z,rx=0,ry=0,rz=0,arc=2*PI,seg=18)=>P(new THREE.TorusGeometry(R,t,6,seg,arc),m,x,y,z,rx,ry,rz);
 const tubo=(pts,r,m,seg=28,rs=6)=>put(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts.map(p=>new V3(p[0],p[1],p[2]))),Math.ceil(seg*.7),r,Math.max(4,rs-1),false),m);
 const torno=(pts,m,x,y,z,seg=16,sx=1,sy=1,sz=1)=>P(new THREE.LatheGeometry(pts.map(p=>new V2(p[0],p[1])),seg),m,x,y,z,0,0,0,sx,sy,sz);
 // perfil lateral: contorno de arriba (de delante a atrás, suavizado) + línea de abajo; se extruye a lo ancho (z)
 const suave=(pts,n=36)=>new THREE.SplineCurve(pts.map(p=>new V2(p[0],p[1]))).getPoints(n);
 const perfil=(arriba,abajo,depth,m,z=0,bev=.0015)=>{const s=new THREE.Shape([...suave(arriba),...abajo.map(p=>new V2(p[0],p[1]))]);
  const ge=new THREE.ExtrudeGeometry(s,{depth,bevelEnabled:bev>0,bevelThickness:bev,bevelSize:bev,bevelSegments:2,curveSegments:8});ge.translate(0,0,z-depth/2);return put(ge,m)};
 const lado=f=>{for(const s of[1,-1])f(s)};
 // rueda: neumático, llanta, radios en la cara de fuera y buje
 const rueda=(x,z,r,a,LL,RAD,nr=0,cubo=ORO)=>{const s=Math.sign(z);
  cil(r,r,a,GOMA,x,r,z,PI/2,0,0,16);cil(r*.7,r*.7,a+.0006,LL,x,r,z,PI/2,0,0,14);
  for(let k=0;k<nr;k++)caja(r*1.36,r*.13,.0009,RAD,x,r,z+s*(a/2+.0003),0,0,k/nr*PI);
  cil(r*.24,r*.24,a+.0018,cubo,x,r,z,PI/2,0,0,10)};
 // espiral dorada (filigrana) en el costado
 const espiral=(cx,cy,z,r0,r1,v,d=1)=>{const p=[];for(let k=0;k<=20;k++){const t=k/20,a=d*t*v*2*PI,r=r0+(r1-r0)*t;p.push([cx+Math.cos(a)*r,cy+Math.sin(a)*r,z])}tubo(p,.0007,ORO,40,4)};
 // farol de latón: poste, jaula con luz cálida y sombrerete
 const farol=(x,y,z,h=.01,c=0xffd27a)=>{cil(.0009,.0009,h,ORO2,x,y+h/2,z,0,0,0,6);caja(.0052,.006,.0052,brillo(c,1.4),x,y+h+.003,z);
  for(const[a,b]of[[1,1],[1,-1],[-1,1],[-1,-1]])caja(.0008,.0068,.0008,ORO,x+a*.0027,y+h+.003,z+b*.0027);cono(.0042,.004,ORO,x,y+h+.0081,z,0,PI/4,0,4);esf(.0011,ORO,x,y+h+.0105,z)};
 // personaje sentado: túnica, capa, cabeza con ojos, nariz y barba, brazos al volante y gorro, corona o turbante
 const figura=(x,o)=>{const T=MV(o.tun,.75),PIEL=MV(o.piel,.7),BAR=o.barba!=null?MV(o.barba,.95):null;
  torno([[0,0],[.0102,0],[.0116,.007],[.011,.015],[.009,.021],[.0062,.0255],[.002,.027],[0,.027]],T,x,.034,0,14,1,1,.9);                 // torso
  if(o.capa!=null)P(new THREE.CylinderGeometry(.0094,.0124,.025,14,1,true,PI*1.08,PI*.84),tela(o.capa),x-.0006,.0465,0);                   // capa por detrás
  if(o.ribete!=null){cil(.0118,.0118,.0026,MV(o.ribete,.95),x,.035,0,0,0,0,14);caja(.0016,.024,.0034,MV(o.ribete,.95),x+.0108,.047,0,0,0,.08)}
  if(o.cinto){cil(.0114,.0114,.0024,NEGRO,x,.0425,0,0,0,0,14);caja(.0012,.0036,.0046,ORO,x+.0114,.0425,0)}
  if(o.pechera!=null)caja(.0012,.012,.006,MV(o.pechera,.5,.6),x+.0098,.049,0,0,0,.12);
  esf(.0066,PIEL,x+.001,.0655,0);                                                                                                         // cabeza
  for(const z of[-.0024,.0024])esf(.0011,NEGRO,x+.0068,.0672,z,.55,1.2,1,8);                                                               // ojos
  esf(.0015,MV(o.nariz??0xe39a7c,.7),x+.0076,.065,0,1,1,1,8);
  if(BAR){esf(.0058,BAR,x+.0044,.0598,0,1,1.25,1.08);esf(.0036,BAR,x+.0058,.0535,0,1,1.45,1);if(o.barbaL)esf(.0026,BAR,x+.0062,.0485,0,1,1.5,1);
   for(const z of[-.0022,.0022])esf(.0021,BAR,x+.0072,.0628,z,.7,.55,1.25,8)}                                                             // bigote
  if(o.pelo!=null)esf(.0067,MV(o.pelo,.95),x-.0012,.0662,0,.95,1,1.02);
  // brazos al volante
  lado(s=>{tubo([[x+.001,.0565,s*.0095],[x+.008,.0505,s*.0102],[x+.016,.0492,s*.0068]],.0027,T,10,6);esf(.0026,o.guante!=null?MV(o.guante,.7):PIEL,x+.0172,.0492,s*.006,1,1,1,8);
   if(o.ribete!=null)aro(.0029,.0012,MV(o.ribete,.95),x+.0142,.0495,s*.0074,0,PI/2-.4,0,2*PI,10)});
  // volante con su columna
  aro(.0052,.001,NEGRO,x+.0195,.0492,0,0,PI/2,.5,2*PI,16);cil(.0008,.0008,.008,NEGRO,x+.0228,.046,0,0,0,.8,6);caja(.006,.005,.02,pint,x+.0272,.0335,0,0,0,.3);   // volante, columna y consola
  // cabeza: gorro de Papá Noel, corona o turbante
  const hy=.0705;
  if(o.gorro==='noel'){tubo([[x-.0004,hy+.001,0],[x-.003,hy+.0085,0],[x-.0085,hy+.0125,0],[x-.0125,hy+.009,0]],.0045,MV(0xc21f2a,.75),14,10);
   cono(.0068,.012,MV(0xc21f2a,.75),x-.0004,hy+.0035,0,0,0,.25,14);cil(.0071,.0071,.0032,BLANCO,x+.0002,hy-.0003,0,0,0,0,16);esf(.0027,BLANCO,x-.0135,hy+.0075,0)}
  else{if(o.gorro==='turbante'){esf(.0072,MV(o.turb??0xf3efe4,.9),x-.0004,hy+.0015,0,1,.72,1.02);for(let k=0;k<3;k++)aro(.0068-.0008*k,.0012,MV(o.turb??0xf3efe4,.9),x-.0004,hy+.0008+k*.0022,0,PI/2,0,0,2*PI,14)}
   const cy=hy+(o.gorro==='turbante'?.0055:.0012),cr=o.gorro==='turbante'?.0048:.0061;
   cil(cr,cr*.92,.0046,ORO,x,cy,0,0,0,0,14);for(let k=0;k<7;k++){const a=k/7*2*PI;cono(.0013,.0042,ORO,x+Math.cos(a)*cr*.96,cy+.0042,Math.sin(a)*cr*.96,0,0,0,5);esf(.0008,ORO,x+Math.cos(a)*cr*.96,cy+.0066,Math.sin(a)*cr*.96,1,1,1,6)}
   esf(.0016,brillo(o.gema,1.3),x+cr,cy,0,.6,1,1,8);if(o.gorro==='corona')esf(.0052,tela(o.forro??0x8e1a2a),x,cy+.0012,0,1,.7,1,10)}};
 // asiento de terciopelo con botones
 const asiento=(x,col,ancho=.044,alto=.02)=>{const T=MV(col,.95);caja(.022,.0055,ancho,T,x+.009,.0312,0);
  P(new THREE.CapsuleGeometry(.0034,ancho-.006,4,8),T,x-.004,.0336,0,PI/2,0,0);caja(.006,alto,ancho,T,x-.006,.031+alto/2,0,0,0,.22);
  for(let k=0;k<5;k++)esf(.0008,ORO,x-.0025,.036+(k%2)*.006,(k-2)*ancho*.17,1,1,1,6)};
 // regalo con lazo dorado
 const regalo=(s,c,x,y,z,ry=0)=>{caja(s,s,s,brillo(c,.6),x,y+s/2,z,0,ry,0);caja(s*1.04,s*1.04,s*.2,ORO,x,y+s/2,z,0,ry,0);caja(s*.2,s*1.04,s*1.04,ORO,x,y+s/2,z,0,ry,0);
  aro(s*.18,s*.06,ORO,x-s*.15,y+s+.0004,z,0,ry,0,2*PI,8);aro(s*.18,s*.06,ORO,x+s*.15,y+s+.0004,z,0,ry,0,2*PI,8)};

 if(tipo==='sleigh'){const L=.124,W=.06,TER=0x7a0f16;
  // núcleo y costados altos con el cuello de cisne delante
  perfil([[.046,.012],[.058,.02],[.063,.031],[.06,.04],[.052,.042],[.045,.035],[.034,.0305],[.0,.029],[-.03,.03],[-.06,.031]],[[-.062,.012]],.046,pint);
  lado(s=>{perfil([[.05,.01],[.063,.024],[.069,.04],[.065,.052],[.057,.054],[.051,.047],[.044,.04],[.03,.0365],[.01,.04],[-.02,.042],[-.04,.046],[-.054,.056],[-.063,.062],[-.069,.056],[-.068,.04],[-.064,.01]],[],.003,pint,s*.0275,.0012);
   tubo([[.046,.0415,s*.0275],[.03,.0378,s*.0275],[.01,.0415,s*.0275],[-.02,.0435,s*.0275],[-.04,.0475,s*.0275],[-.054,.0575,s*.0275],[-.0635,.0635,s*.0275]],.0022,BLANCO,30,7);   // ribete de piel blanca
   tubo([[.045,.041,s*.029],[.052,.048,s*.029],[.058,.0545,s*.029],[.066,.0525,s*.029],[.0695,.042,s*.029],[.065,.026,s*.029],[.053,.0115,s*.029]],.0015,ORO,30,5);               // filo dorado del cisne
   espiral(-.018,.026,s*.0306,.0105,.002,1.6,s);espiral(.02,.024,s*.0306,.008,.0018,1.4,-s);espiral(-.052,.03,s*.0306,.008,.0018,1.3,s);
   caja(.1,.0018,.0012,led(0xffffff),-.006,.0122,s*.0308);                                                                                   // tira LED
   // patines con la punta enroscada y sus soportes
   tubo([[-.064,.006,s*.033],[-.03,.0032,s*.033],[.02,.0032,s*.033],[.05,.0048,s*.033],[.066,.013,s*.033],[.071,.026,s*.033],[.066,.034,s*.033],[.059,.031,s*.033],[.059,.025,s*.033],[.063,.023,s*.033]],.0017,ORO,48,6);
   for(const x of[-.046,-.008,.032])cil(.0011,.0011,.0085,ORO,x,.0078,s*.0325,0,0,0,6)});
  for(const x of[.034,-.034])lado(s=>rueda(x,s*.0235,.0092,.0062,MV(0x8e0f1a,.4,.3),ORO,3));
  // capó: acebo y faroles; detrás, asiento de terciopelo y saco de regalos
  for(const[dx,dz]of[[0,0],[.0028,.0022],[.0022,-.0024]])esf(.0018,brillo(0xe0141e,.6),.055+dx,.0438,dz,1,1,1,8);
  lado(s=>esf(.0042,MV(0x1f7a35,.6),.0525,.0432,s*.0045,1.3,.35,.75,8));
  lado(s=>farol(.038,.032,s*.019,.008));
  asiento(-.03,TER,.046,.022);
  figura(-.018,{tun:0xc21f2a,piel:0xf0c8a8,barba:0xffffff,barbaL:1,ribete:0xffffff,cinto:1,guante:0x1a1a1a,nariz:0xe8907a,gorro:'noel'});
  torno([[0,0],[.009,.001],[.012,.008],[.0115,.018],[.008,.025],[.0036,.028],[.0042,.032],[.0048,.034],[0,.034]],MV(0x8a5a2b,.95),-.052,.0305,0,14);
  aro(.0042,.0011,ORO,-.052,.0585,0,PI/2);
  regalo(.0085,0x2fa84f,-.0535,.0588,.004,.4);regalo(.007,0x1f6fd0,-.0485,.0592,-.0045,-.3);regalo(.006,0xf2c230,-.0565,.0598,-.006,.9);
  lado(s=>cil(.0028,.0034,.012,CROMO,-.066,.014,s*.012,0,0,PI/2,10));                                                                      // escapes
  luces(L,.022,W);g.add(manchaSombra(.07,.142))}

 else if(tipo==='aurum'){const L=.126,W=.058,VEL=MV(0x8e1a2a,.85),MAD=MV(0x6b3d1a,.8);
  // casco de carroza real (barquilla) con costados ondulados
  perfil([[.06,.032],[.05,.0345],[.035,.0315],[.015,.03],[-.005,.031],[-.03,.032],[-.045,.037],[-.058,.04],[-.062,.034]],[[-.06,.026],[-.052,.018],[-.035,.0145],[.03,.0145],[.05,.019],[.058,.025]],.044,pint);
  lado(s=>{perfil([[.061,.034],[.05,.0405],[.036,.0385],[.02,.039],[.005,.036],[-.015,.037],[-.032,.042],[-.046,.049],[-.057,.052],[-.064,.047],[-.064,.034]],[[-.061,.025],[-.053,.0165],[-.035,.0125],[.03,.0125],[.051,.017],[.059,.024]],.003,pint,s*.0245,.0012);
   // panel de terciopelo con marco dorado y medallón con corona
   const z=s*.0268;caja(.05,.0125,.0012,VEL,-.012,.0255,z);
   tubo([[-.037,.019,z+s*.0006],[.013,.019,z+s*.0006]],.0009,ORO,4,4);tubo([[-.037,.032,z+s*.0006],[.013,.032,z+s*.0006]],.0009,ORO,4,4);
   for(const x of[-.037,.013])cil(.0009,.0009,.0138,ORO,x,.0255,z+s*.0006,0,0,0,5);
   cil(.0052,.0052,.0014,ORO,-.012,.0258,z+s*.0007,PI/2,0,0,14);esf(.0017,brillo(0xd51f1f,1.1),-.012,.0258,z+s*.0016,1,1,.6,8);
   tubo([[.061,.0352,s*.0262],[.05,.0418,s*.0262],[.036,.0398,s*.0262],[.02,.0402,s*.0262],[.005,.0373,s*.0262],[-.015,.0383,s*.0262],[-.032,.0433,s*.0262],[-.046,.0503,s*.0262],[-.057,.0533,s*.0262],[-.0645,.048,s*.0262]],.0013,ORO,36,5);
   tubo([[-.061,.0245,s*.0262],[-.053,.0157,s*.0262],[-.035,.0117,s*.0262],[.03,.0117,s*.0262],[.051,.0162,s*.0262],[.059,.0235,s*.0262]],.0012,ORO,30,5);
   espiral(.042,.026,s*.027,.0075,.0016,1.5,-s);espiral(-.051,.033,s*.027,.0072,.0016,1.5,s);
   caja(.09,.0016,.0012,led(0xffe9a0),-.002,.0145,s*.028);
   // aletas sobre las ruedas (como guardabarros de carruaje)
   aro(.0146,.0013,ORO2,-.036,.0128,s*.0305,0,0,0,PI,16);aro(.0124,.0013,ORO2,.041,.0106,s*.0305,0,0,0,PI,16)});
  // ruedas de carruaje: grandes detrás, radios granate
  lado(s=>{rueda(-.036,s*.0305,.0128,.005,ORO,VEL,4);rueda(.041,s*.0305,.0106,.005,ORO,VEL,4)});
  // corona en la proa y faroles altos
  {const x=.058,y=.039;cil(.0048,.0042,.004,ORO,x,y,0,0,0,0,12);for(let k=0;k<6;k++){const a=k/6*2*PI;cono(.0012,.0036,ORO,x+Math.cos(a)*.0046,y+.0036,Math.sin(a)*.0046,0,0,0,5)}esf(.0016,brillo(0xd51f1f,1.2),x+.0046,y,0,.6,1,1,8);esf(.003,VEL,x,y+.001,0,1,.7,1,8)}
  lado(s=>farol(.034,.034,s*.0215,.013,0xffe6a0));
  // trono de terciopelo
  asiento(-.028,0x8e1a2a,.04,.026);aro(.012,.0011,ORO,-.0352,.058,0,0,PI/2,0,PI,14);
  figura(-.015,{tun:0x8e1a2a,capa:0xd9a32a,piel:0xf0c8a8,barba:0xf2f2ee,barbaL:1,pelo:0xf2f2ee,pechera:0xf5c84a,gorro:'corona',gema:0xd51f1f});
  // cofre del tesoro abierto con monedas y joyas
  {const x=-.05,y=.04;caja(.02,.012,.028,MAD,x,y+.006,0);for(const dx of[-.0065,.0065])caja(.0018,.0124,.0284,ORO,x+dx,y+.006,0);caja(.0204,.0018,.0284,ORO,x,y+.0005,0);
   caja(.0024,.014,.028,MAD,x-.0118,y+.019,0,0,0,.28);caja(.0028,.0026,.0284,ORO,x-.0135,y+.0255,0,0,0,.28);   // tapa abierta hacia atrás
   torno([[0,0],[.0095,0],[.0085,.0025],[.006,.0045],[.003,.0056],[0,.006]],brillo(0xffc21f,.75),x,y+.0115,0,12,1,1,1.35);
   for(let k=0;k<6;k++)cil(.0028,.0028,.0008,brillo(0xffc21f,.8),x-.006+(k%3)*.006,y+.014+(k>2?.0012:0),(k%2?-1:1)*(.004+k*.0012),.3*k,0,.4,10);
   esf(.0018,brillo(0x2fe07a,1.2),x+.004,y+.0165,.006,1,1,1,8);esf(.0016,brillo(0x3f7fff,1.2),x-.003,y+.017,-.008,1,1,1,8);esf(.0015,brillo(0xd51f1f,1.2),x+.001,y+.0175,-.002,1,1,1,8)}
  luces(L,.024,W);g.add(manchaSombra(.07,.14))}

 else if(tipo==='mirra'){const L=.128,W=.052,AZ=led(0x4aa8ff);
  // cápsula plateada en gota, con morro bajo y popa alta
  perfil([[.064,.016],[.058,.0235],[.042,.0295],[.022,.031],[.0,.0295],[-.025,.032],[-.048,.0355],[-.062,.033],[-.066,.024]],[[-.063,.011],[.05,.01],[.062,.012]],.038,pint,0,.0045);
  // pontones laterales sobre las ruedas
  lado(s=>{perfil([[.056,.0135],[.05,.021],[.034,.0255],[.0,.023],[-.034,.0255],[-.052,.0225],[-.06,.016]],[[-.058,.009],[.052,.009]],.006,pint,s*.0235,.002);
   tubo([[.055,.0175,s*.0272],[.034,.0215,s*.0272],[.0,.019,s*.0272],[-.034,.0215,s*.0272],[-.056,.018,s*.0272]],.0008,AZ,24,4);
   caja(.06,.0028,.0012,MV(0x2a4fa8,.35,.6),-.004,.0128,s*.0272);
   // aletas de cola con filo azul
   P(new THREE.ExtrudeGeometry(new THREE.Shape([new V2(-.04,.03),new V2(-.059,.05),new V2(-.068,.052),new V2(-.066,.031)]),{depth:.002,bevelEnabled:true,bevelThickness:.0006,bevelSize:.0006,bevelSegments:1}),pint,0,0,s*.014-.001,s*.22,0,0);
   tubo([[-.0395,.031,s*(.014+.0066)],[-.059,.0505,s*(.014+.011)],[-.068,.0525,s*(.014+.0115)]],.0008,AZ,10,4)});
  lado(s=>{for(const x of[.038,-.038]){rueda(x,s*.0245,.0102,.0068,CROMO,MV(0x2a3242,.4,.6),0,MV(0x2a3242,.4,.6));aro(.0062,.0007,AZ,x,.0102,s*.0283,0,0,0,2*PI,18)}});
  // parabrisas burbuja, faro LED corrido y estrella en el morro
  P(new THREE.SphereGeometry(.024,18,8,PI*.62,PI*.76,PI*.2,PI*.3),CRISTAL,-.012,.025,0);
  caja(.0016,.0024,.03,AZ,.0638,.017,0);
  {const st=[];for(let k=0;k<10;k++){const a=PI/2+k/10*2*PI,r=k%2?.0026:.0062;st.push(new V2(Math.cos(a)*r,Math.sin(a)*r))}
   P(new THREE.ExtrudeGeometry(new THREE.Shape(st),{depth:.0014,bevelEnabled:true,bevelThickness:.0004,bevelSize:.0004,bevelSegments:1}),brillo(0xffd24a,1.1),.052,.0292,-.0007,0,PI/2,-.35)}
  asiento(-.03,0x1b2a4a,.036,.018);
  figura(-.016,{tun:0x2a4fa8,capa:0x9fb6e8,piel:0xe8bf9a,barba:0x8a4a22,pelo:0x8a4a22,pechera:0xdfe3ea,gorro:'corona',gema:0x3f7fff,forro:0x1b2a4a});
  // arco con el incensario colgando y su humo azul
  aro(.0175,.0012,CROMO,-.05,.033,0,0,PI/2,0,PI,20);
  for(const dz of[-.0028,.0028])cil(.0003,.0003,.012,ORO,-.05,.0445,dz,dz*30,0,0,4);
  torno([[0,0],[.0038,.0006],[.0056,.004],[.0054,.0072],[.0046,.0088],[.0028,.0104],[.0012,.0118],[.001,.013],[0,.013]],ORO,-.05,.0268,0,12);
  aro(.0055,.0006,ORO,-.05,.0335,0,PI/2,0,0,2*PI,14);
  esf(.0045,czMat('humoAz',()=>new THREE.MeshBasicMaterial({color:0x7fc4ff,transparent:true,opacity:.6,toneMapped:false,depthWrite:false})),-.05,.0412,0,1,.8,1,10);
  luces(L*.95,.017,W);g.add(manchaSombra(.064,.144))}

 else{const L=.124,W=.06,CAM=MV(0xc8955a,.9),VERD=MV(0x0a4a2a,.5,.3);
  // casco verde con proa alta
  perfil([[.05,.013],[.06,.022],[.062,.03],[.053,.0345],[.03,.0305],[.0,.0305],[-.03,.033],[-.05,.0355],[-.06,.033]],[[-.062,.013]],.048,pint);
  lado(s=>{perfil([[.063,.032],[.054,.0385],[.04,.0355],[.026,.039],[.012,.0375],[-.004,.04],[-.02,.038],[-.036,.042],[-.05,.044],[-.062,.0425],[-.067,.036]],[[-.064,.011],[.052,.011]],.003,pint,s*.0275,.0012);
   const z=s*.0293;
   tubo([[.063,.0332,z],[.054,.0397,z],[.04,.0367,z],[.026,.0402,z],[.012,.0387,z],[-.004,.0412,z],[-.02,.0392,z],[-.036,.0432,z],[-.05,.0452,z],[-.062,.0437,z],[-.0675,.037,z]],.0013,ORO,40,5);
   tubo([[-.064,.0128,z],[.052,.0128,z],[.061,.022,z]],.0012,ORO,16,5);
   for(const x of[-.044,-.012,.02]){cil(.0044,.0044,.0012,ORO,x,.025,z,PI/2,0,0,8);esf(.0018,brillo(0x2fe07a,1.3),x,.025,z+s*.0008,1,1,.7,8)}
   for(const x of[-.028,.004,.036])espiral(x,.0255,z,.0055,.0014,1.2,(x>0?-1:1)*s);
   caja(.1,.0016,.0012,led(0x7dffb0),-.006,.0145,z+s*.0004)});
  lado(s=>{for(const x of[.036,-.036])rueda(x,s*.0255,.011,.0062,ORO,VERD,4)});
  // mascarón de proa: un camello con bridas doradas y borlas rojas
  tubo([[.05,.03,0],[.061,.036,0],[.0665,.047,0],[.067,.057,0],[.0705,.0635,0]],.0042,CAM,20,8);
  esf(.0055,CAM,.0755,.0655,0,1.55,.85,.85);esf(.0034,CAM,.0835,.0632,0,1.2,.9,.9);esf(.0016,MV(0x3a2416,.8),.0866,.0635,0,.5,1,1.6,8);
  lado(s=>{esf(.001,NEGRO,.0788,.0682,s*.0036,.6,1.1,1,6);esf(.0017,CAM,.0725,.0715,s*.0034,.6,1,.5,6);cil(.0004,.0004,.005,ORO,.0775,.0595,s*.0042,0,0,0,4);esf(.0013,brillo(0xd51f1f,.5),.0775,.0565,s*.0042,1,1.4,1,6)});
  aro(.0051,.0011,ORO,.0675,.0535,0,PI/2,0,.25,2*PI,14);aro(.0046,.0009,ORO,.0782,.0652,0,0,PI/2,0,2*PI,12);
  // dosel con cúpula verde y dorada sobre los regalos iluminados
  for(const[x,z]of[[-.034,.019],[-.034,-.019],[-.058,.019],[-.058,-.019]]){cil(.0014,.0014,.03,ORO,x,.0485,z,0,0,0,8);esf(.0021,ORO,x,.035,z,1,1,1,8)}
  caja(.03,.0028,.044,ORO2,-.046,.0645,0);caja(.026,.0034,.04,pint,-.046,.0668,0);
  torno([[0,0],[.0135,0],[.0145,.003],[.013,.0085],[.0095,.0135],[.0055,.0175],[.0022,.021],[.0012,.024],[0,.025]],pint,-.046,.0685,0,16);
  aro(.0138,.0011,ORO,-.046,.0698,0,PI/2,0,0,2*PI,18);esf(.0018,ORO,-.046,.0942,0,1,1,1,8);cono(.0012,.005,ORO,-.046,.0975,0,0,0,0,6);
  [[0xd51f1f,.011,-.045,.008],[0x1f6fd0,.0095,-.047,-.009],[0xf2c230,.008,-.035,-.006],[0xc23fd0,.0075,-.056,-.003],[0xf4f4f2,.0065,-.046,0,.011]].forEach(([c,s_,x,z,y=0])=>regalo(s_,c,x,.0345+y,z,(x*97)%1));
  asiento(-.018,0x0f5a33,.044,.018);
  figura(-.008,{tun:0x6a2a8a,capa:0x0f8a4f,piel:0x5a3a28,barba:0x1a1a1a,nariz:0x4a2e20,pechera:0xf5c84a,gorro:'turbante',turb:0xf3efe4,gema:0x2fe07a});
  luces(L,.02,W);g.add(manchaSombra(.072,.14))}

 // juntar: una malla por material (la pintura se queda con el nombre 'carroceria')
 for(const[m,L]of B){const gs=L.map(q=>{const r=q.index?q.toNonIndexed():q;for(const k of Object.keys(r.attributes))if(k!=='position'&&k!=='normal'&&k!=='uv')r.deleteAttribute(k);return r});
  const geo=mergeGeometries(gs);if(!geo)continue;const o=new THREE.Mesh(geo,m);if(m===pint)o.name='carroceria';o.castShadow=true;g.add(o)}}
