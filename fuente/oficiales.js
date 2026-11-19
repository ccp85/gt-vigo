// ===== Vehículos oficiales de GT Vigo: tres coches, tres motos y tres helicópteros =====
// Coches: Ría GT 300, Bouzas 4x4, Samil Spider · Motos: Castro 600, Toralla RR, Arenal 125 · Helicópteros: Cíes H-1, Rande SR, Ons Vortex
// coche(i), moto(i,o), heli(i) con i=0,1,2 (0 = el de siempre). GTV_OF_INFO tiene nombre, tipo y barras de cada uno.
// Un solo dibujo para la pantalla de inicio y para el juego: lo que eliges en el menú es lo que conduces.
// Medidas en las unidades del menú (el coche mide unos 4,4 de largo; el juego los encoge a su escala).
// T(rol,color,opciones) da cada material: el menú usa su brillo de estudio (opciones) y el juego, los suyos
// (pintura con barniz que refleja el cielo, faros que se encienden de noche...). Roles: pintura, cristal,
// negro, cromo, faro, piloto, luz (luces de posición) y otro.
window.GTV_OF=function(THREE,T){
const COL={coche:0xff4a26,moto:0x16c5e6,heli:0xb8e62a};
const mesh=(g,m,x=0,y=0,z=0,name)=>{const o=new THREE.Mesh(g,m);o.position.set(x,y,z);if(name)o.name=name;return o};
const ext=(pts,depth,m,bev=.06,name)=>{const s=new THREE.Shape(pts.map(p=>new THREE.Vector2(p[0],p[1])));
 const g=new THREE.ExtrudeGeometry(s,{depth,bevelEnabled:bev>0,bevelThickness:bev,bevelSize:bev,bevelSegments:3,curveSegments:12});g.translate(0,0,-depth/2);
 const o=new THREE.Mesh(g,m);if(name)o.name=name;return o};
const base=()=>({glass:T('cristal',0x0b1020,{metalness:.9,roughness:.06}),black:T('negro',0x111114,{metalness:.1,roughness:.75}),chrome:T('cromo',0xdfe3ea,{metalness:1,roughness:.12})});
const faro=()=>T('faro',0xffffff,{emissive:0xfff3d0,emissiveIntensity:2.5}),piloto=()=>T('piloto',0xff0010,{emissive:0xff1020,emissiveIntensity:2.5});

// ---- Ría GT 300: deportivo naranja de dos puertas con alerón
function coche(){
 const {glass,black,chrome}=base(),g=new THREE.Group(),paint=T('pintura',COL.coche,{metalness:.7,roughness:.22,envMapIntensity:1.4});
 g.add(ext([[-2.1,.38],[2.05,.38],[2.18,.62],[2.12,.82],[1.85,.95],[.9,1.02],[.3,1.42],[-.95,1.45],[-1.65,1.06],[-2.15,1.0]],1.62,paint,.09,'carroceria'));
 g.add(ext([[.82,1.05],[.3,1.44],[-.92,1.47],[-1.55,1.08]],1.86,glass,0));
 const st=T('negro',0x111114,{metalness:.4,roughness:.4});
 g.add(mesh(new THREE.BoxGeometry(.34,.05,1.9),st,-1.95,1.32,0));
 [-.6,.6].forEach(z=>g.add(mesh(new THREE.BoxGeometry(.08,.26,.06),st,-1.92,1.18,z)));
 [-.58,.58].forEach(z=>{g.add(mesh(new THREE.BoxGeometry(.06,.12,.42),faro(),2.2,.74,z));g.add(mesh(new THREE.BoxGeometry(.06,.1,.5),piloto(),-2.2,.86,z))});
 g.add(mesh(new THREE.BoxGeometry(.1,.16,1.2),black,2.18,.5,0));
 const wheels=[],hub=T('otro',0xff5a36,{emissive:0x5a1000});
 [[1.35,.82],[1.35,-.82],[-1.38,.82],[-1.38,-.82]].forEach(([x,z])=>{const w=new THREE.Group();w.position.set(x,.44,z);
  const t=mesh(new THREE.CylinderGeometry(.44,.44,.34,28),black);t.rotation.x=Math.PI/2;w.add(t);
  const r=mesh(new THREE.CylinderGeometry(.29,.29,.36,6),chrome);r.rotation.x=Math.PI/2;w.add(r);
  const h=mesh(new THREE.CylinderGeometry(.08,.08,.38,12),hub);h.rotation.x=Math.PI/2;w.add(h);
  g.add(w);wheels.push(w)});
 g.userData.wheels=wheels;return g}

// ---- Castro 600: naked azul. Con {piloto:true} lleva al protagonista (sudadera roja, vaqueros) con casco a juego
function moto(o={}){
 const {black,chrome}=base(),g=new THREE.Group(),paint=T('pintura',COL.moto,{metalness:.7,roughness:.22,envMapIntensity:1.4}),wheels=[];
 [.82,-.82].forEach(x=>{const w=new THREE.Group();w.position.set(x,.46,0);w.add(mesh(new THREE.TorusGeometry(.36,.11,14,32),black));
  const d=mesh(new THREE.CylinderGeometry(.27,.27,.06,7),chrome);d.rotation.x=Math.PI/2;w.add(d);g.add(w);wheels.push(w)});
 g.add(ext([[-.55,.62],[.42,.6],[.82,.98],[.72,1.22],[.42,1.2],[.1,1.08],[-.35,1.08],[-.8,1.2],[-1.0,1.1],[-.72,.78]],.34,paint,.06,'carroceria'));
 g.add(mesh(new THREE.BoxGeometry(.62,.1,.32),black,-.38,1.17,0));
 g.add(mesh(new THREE.BoxGeometry(.5,.36,.3),T('otro',0x2a2d36,{metalness:.8,roughness:.35}),-.05,.58,0));
 const f=mesh(new THREE.CylinderGeometry(.04,.04,1.0,10),chrome,.7,.88,0);f.rotation.z=.42;[-.12,.12].forEach(z=>{const c=f.clone();c.position.z=z;g.add(c)});
 const hb=mesh(new THREE.CylinderGeometry(.03,.03,.8,10),black,.54,1.32,0);hb.rotation.x=Math.PI/2;g.add(hb);
 const ws=mesh(new THREE.BoxGeometry(.04,.26,.3),T('otro',0x3a5a70,{transparent:true,opacity:.6,metalness:.9,roughness:.05}),.72,1.34,0);ws.rotation.z=-.5;g.add(ws);
 g.add(mesh(new THREE.SphereGeometry(.09,16,12),T('faro',0xffffff,{emissive:0xe8fbff,emissiveIntensity:3}),.86,1.1,0));
 const ex=mesh(new THREE.CylinderGeometry(.06,.08,.7,12),chrome,-.7,.62,.2);ex.rotation.z=1.35;g.add(ex);
 g.add(mesh(new THREE.BoxGeometry(.05,.06,.18),piloto(),-1.03,1.1,0));
 if(o.piloto){
  const ROPA=T('otro',0xe0553a,{roughness:.7}),PANT=T('otro',0x2c4a7f,{roughness:.8}),ZAP=T('otro',0xf2f2ee,{roughness:.8}),PIEL=T('otro',0xe8b48a,{roughness:.7});
  const caja=(l,h,w,m,x,y,z,rz=0)=>{const b=mesh(new THREE.BoxGeometry(l,h,w),m,x,y,z);b.rotation.z=rz;g.add(b);return b};
  [-.15,.15].forEach(z=>{caja(.48,.17,.15,PANT,-.2,1.3,z,-.05);caja(.15,.46,.14,PANT,.06,1.06,z*1.25,.35);caja(.24,.1,.13,ZAP,.12,.82,z*1.3)});
  caja(.3,.6,.42,ROPA,-.2,1.62,0,-.62);
  [-.24,.24].forEach(z=>{caja(.66,.11,.11,ROPA,.22,1.62,z*1.1,-.75);g.add(mesh(new THREE.SphereGeometry(.06,10,8),PIEL,.47,1.39,z*1.35))});
  g.add(mesh(new THREE.SphereGeometry(.2,18,14),paint,-.02,2.02,0,'carroceria'));
  const vis=mesh(new THREE.SphereGeometry(.17,16,10,Math.PI-Math.PI/2.6,Math.PI/1.3,Math.PI/3,Math.PI/3.2),T('cristal',0x0b1020,{metalness:.9,roughness:.06}),.0,2.02,0);vis.scale.set(1.12,1,1.12);g.add(vis)}
 g.userData.wheels=wheels;return g}

// ---- Cíes H-1: helicóptero verde lima. Orden fijo de las 4 primeras piezas: cabina, cristal, cola y deriva
// (el reparto de Navidad las repinta por su posición)
function heli(){
 const {glass,chrome}=base(),g=new THREE.Group(),paint=T('pintura',COL.heli,{metalness:.6,roughness:.25,envMapIntensity:1.4}),dk=T('otro',0x1b1e26,{metalness:.6,roughness:.35});
 const b=mesh(new THREE.SphereGeometry(1,36,24),paint,.35,1.35,0,'carroceria');b.scale.set(1.35,.9,.82);g.add(b);
 const c=mesh(new THREE.SphereGeometry(1,36,24),glass,.95,1.48,0);c.scale.set(.82,.66,.7);g.add(c);
 const tb=mesh(new THREE.CylinderGeometry(.11,.3,2.7,16),paint,-1.95,1.55,0,'carroceria');tb.rotation.z=Math.PI/2+.06;g.add(tb);
 const fin=mesh(new THREE.BoxGeometry(.45,.85,.07),paint,-3.2,1.9,0,'carroceria');fin.rotation.z=-.35;g.add(fin);
 g.add(mesh(new THREE.BoxGeometry(.35,.05,1.0),paint,-2.75,1.52,0,'carroceria'));
 [-.62,.62].forEach(z=>{const s=mesh(new THREE.CylinderGeometry(.05,.05,2.7,10),chrome,.3,.28,z);s.rotation.z=Math.PI/2;g.add(s);
  [-.35,.95].forEach(x=>{const p=mesh(new THREE.CylinderGeometry(.04,.04,.6,8),dk,x,.55,z*.85);p.rotation.x=z>0?-.35:.35;g.add(p)})});
 g.add(mesh(new THREE.CylinderGeometry(.1,.14,.4,12),dk,.35,2.3,0));
 g.add(mesh(new THREE.BoxGeometry(.7,.22,.6),dk,.2,2.12,0));
 const rot=new THREE.Group();rot.position.set(.35,2.5,0);
 for(let i=0;i<4;i++){const p=new THREE.Group();p.rotation.y=i*Math.PI/2;p.add(mesh(new THREE.BoxGeometry(2.3,.035,.2),dk,1.15,0,0));rot.add(p)}
 rot.add(mesh(new THREE.CylinderGeometry(.14,.14,.12,12),chrome));g.add(rot);
 const tr=new THREE.Group();tr.position.set(-3.25,2.0,.1);
 for(let i=0;i<2;i++){const p=new THREE.Group();p.rotation.z=i*Math.PI/2;p.add(mesh(new THREE.BoxGeometry(.06,.75,.03),dk));tr.add(p)}g.add(tr);
 g.add(mesh(new THREE.SphereGeometry(.07,10,8),T('luz',0xff0010,{emissive:0xff2020,emissiveIntensity:3}),-.4,.92,.75));
 g.add(mesh(new THREE.SphereGeometry(.07,10,8),T('luz',0x00ff40,{emissive:0x20ff40,emissiveIntensity:3}),-.4,.92,-.75));
 g.userData.rot=rot;g.userData.tr=tr;return g}
// ---- piezas comunes de las variantes
// palo: caja entre dos puntos del perfil (x,y) a la altura z; sirve para brazos, piernas, horquillas...
const palo=(g,a,b,gr,m,z=0,w=gr)=>{const dx=b[0]-a[0],dy=b[1]-a[1],o=mesh(new THREE.BoxGeometry(Math.hypot(dx,dy),gr,w),m,(a[0]+b[0])/2,(a[1]+b[1])/2,z);o.rotation.z=Math.atan2(dy,dx);g.add(o);return o};
const rueda=(g,x,y,z,r,ancho,llanta,buje,radios=6)=>{const w=new THREE.Group();w.position.set(x,y,z);
 const t=mesh(new THREE.CylinderGeometry(r,r,ancho,28),T('negro',0x111114,{metalness:.1,roughness:.75}));t.rotation.x=Math.PI/2;w.add(t);
 const l=mesh(new THREE.CylinderGeometry(r*.66,r*.66,ancho+.02,radios),llanta);l.rotation.x=Math.PI/2;w.add(l);
 if(buje){const h=mesh(new THREE.CylinderGeometry(r*.18,r*.18,ancho+.04,12),buje);h.rotation.x=Math.PI/2;w.add(h)}
 g.add(w);return w};
const ruedaMoto=(g,x,y,r,tubo,llanta)=>{const w=new THREE.Group();w.position.set(x,y,0);w.add(mesh(new THREE.TorusGeometry(r,tubo,14,32),T('negro',0x111114,{metalness:.1,roughness:.75})));
 const d=mesh(new THREE.CylinderGeometry(r*.75,r*.75,.06,7),llanta);d.rotation.x=Math.PI/2;w.add(d);g.add(w);return w};
// el protagonista en moto: cadera, rodilla, pie, puños y cuánto se inclina el tronco hacia delante
function motorista(g,casco,P){
 const ROPA=T('otro',0xe0553a,{roughness:.7}),PANT=T('otro',0x2c4a7f,{roughness:.8}),ZAP=T('otro',0xf2f2ee,{roughness:.8}),PIEL=T('otro',0xe8b48a,{roughness:.7});
 const {hip,knee,peg,grip,lean}=P,sh=[hip[0]+.6*Math.sin(lean),hip[1]+.6*Math.cos(lean)];
 [-.15,.15].forEach(z=>{palo(g,hip,knee,.17,PANT,z,.16);palo(g,knee,peg,.14,PANT,z*1.15,.14);g.add(mesh(new THREE.BoxGeometry(.24,.1,.13),ZAP,peg[0]+.05,peg[1]-.04,z*1.15))});
 palo(g,hip,sh,.3,ROPA,0,.42);
 [-.24,.24].forEach(z=>{palo(g,sh,grip,.11,ROPA,z,.11);g.add(mesh(new THREE.SphereGeometry(.06,10,8),PIEL,grip[0],grip[1],z*1.3))});
 const hx=sh[0]+.19*Math.sin(lean),hy=sh[1]+.19*Math.cos(lean)+.04;
 g.add(mesh(new THREE.SphereGeometry(.2,18,14),casco,hx-.02,hy,0,'carroceria'));
 const v=mesh(new THREE.SphereGeometry(.17,16,10,Math.PI-Math.PI/2.6,Math.PI/1.3,Math.PI/3,Math.PI/3.2),T('cristal',0x0b1020,{metalness:.9,roughness:.06}),hx,hy,0);v.scale.set(1.12,1,1.12);g.add(v)}
const rotorPalas=(n,L,y,x=.35)=>{const dk=T('otro',0x1b1e26,{metalness:.6,roughness:.35}),rot=new THREE.Group();rot.position.set(x,y,0);
 for(let i=0;i<n;i++){const p=new THREE.Group();p.rotation.y=i*Math.PI*2/n;p.add(mesh(new THREE.BoxGeometry(L,.035,.2),dk,L/2,0,0));rot.add(p)}
 rot.add(mesh(new THREE.CylinderGeometry(.14,.14,.12,12),T('cromo',0xdfe3ea,{metalness:1,roughness:.12})));return rot};
const rotorCola=(x,y,z,n=2,L=.75)=>{const tr=new THREE.Group();tr.position.set(x,y,z);const dk=T('otro',0x1b1e26,{metalness:.6,roughness:.35});
 for(let i=0;i<n;i++){const p=new THREE.Group();p.rotation.z=i*Math.PI/n;p.add(mesh(new THREE.BoxGeometry(.06,L,.03),dk));tr.add(p)}return tr};
const patines=(g,largo,x0,xs,zs=.62)=>{const ch=T('cromo',0xdfe3ea,{metalness:1,roughness:.12}),dk=T('otro',0x1b1e26,{metalness:.6,roughness:.35});
 [-zs,zs].forEach(z=>{const s=mesh(new THREE.CylinderGeometry(.05,.05,largo,10),ch,x0,.28,z);s.rotation.z=Math.PI/2;g.add(s);
  xs.forEach(([x,top])=>{const p=mesh(new THREE.CylinderGeometry(.04,.04,top-.28,8),dk,x,(top+.28)/2,z*.85);p.rotation.x=z>0?-.3:.3;g.add(p)})})};
const lucesNav=(g,x,y,z)=>{g.add(mesh(new THREE.SphereGeometry(.07,10,8),T('luz',0xff0010,{emissive:0xff2020,emissiveIntensity:3}),x,y,z));
 g.add(mesh(new THREE.SphereGeometry(.07,10,8),T('luz',0x00ff40,{emissive:0x20ff40,emissiveIntensity:3}),x,y,-z))};

// ---- Bouzas 4x4: todoterreno cuadrado mostaza, ruedas gordas, rueda de repuesto, barra de luces y snorkel
function bouzas(){
 const {glass,black,chrome}=base(),g=new THREE.Group(),paint=T('pintura',0xe0a43a,{metalness:.6,roughness:.3,envMapIntensity:1.3});
 g.add(ext([[-2.0,.62],[2.0,.62],[2.08,.76],[2.05,1.22],[1.12,1.32],[.78,2.0],[-1.86,2.02],[-2.0,1.9]],1.7,paint,.07,'carroceria'));
 g.add(ext([[1.04,1.36],[.74,2.0],[-1.72,2.0],[-1.72,1.42]],1.88,glass,0));
 g.add(mesh(new THREE.BoxGeometry(2.66,.08,1.86),paint,-.5,2.06,0,'carroceria'));
 const pb=mesh(new THREE.BoxGeometry(.04,.7,1.5),glass,.99,1.68,0);pb.rotation.z=.46;g.add(pb);
 g.add(mesh(new THREE.BoxGeometry(.16,.64,1.9),paint,-.42,1.7,0,'carroceria'));
 [2.12,-2.1].forEach(x=>g.add(mesh(new THREE.BoxGeometry(.22,.26,1.94),black,x,.74,0)));
 [[1.35,.93],[-1.35,.93]].forEach(([x,y])=>[-.97,.97].forEach(z=>g.add(mesh(new THREE.BoxGeometry(1.32,.1,.16),black,x,y+.12,z))));
 const rep=mesh(new THREE.CylinderGeometry(.44,.44,.26,24),black,-2.18,1.32,0);rep.rotation.z=Math.PI/2;g.add(rep);
 const rl=mesh(new THREE.CylinderGeometry(.26,.26,.28,6),chrome,-2.18,1.32,0);rl.rotation.z=Math.PI/2;g.add(rl);
 g.add(mesh(new THREE.BoxGeometry(.18,.12,1.5),black,.45,2.15,0));
 [-.5,-.17,.17,.5].forEach(z=>g.add(mesh(new THREE.BoxGeometry(.06,.1,.22),faro(),.55,2.15,z)));
 [-.62,.62].forEach(z=>{const f=mesh(new THREE.CylinderGeometry(.15,.15,.08,20),faro(),2.09,1.02,z);f.rotation.z=Math.PI/2;g.add(f);
  g.add(mesh(new THREE.BoxGeometry(.06,.24,.14),piloto(),-2.03,1.62,z*1.2))});
 g.add(mesh(new THREE.BoxGeometry(.06,.26,.7),T('negro',0x111114,{metalness:.4,roughness:.4}),2.1,1.0,0));
 const sn=mesh(new THREE.CylinderGeometry(.06,.06,1.0,10),black,1.0,1.75,.94);g.add(sn);
 const wheels=[],hub=T('otro',0xff5a36,{emissive:0x5a1000});
 [[1.35,.88],[1.35,-.88],[-1.35,.88],[-1.35,-.88]].forEach(([x,z])=>wheels.push(rueda(g,x,.52,z,.52,.42,T('otro',0x2a2d36,{metalness:.8,roughness:.35}),hub,6)));
 g.userData.wheels=wheels;return g}

// ---- Samil Spider: descapotable retro verde agua, faros redondos, cromados y ruedas de banda blanca
function spider(){
 const {glass,black,chrome}=base(),g=new THREE.Group(),paint=T('pintura',0x4fc9b3,{metalness:.6,roughness:.24,envMapIntensity:1.4});
 g.add(ext([[-2.12,.38],[2.08,.38],[2.24,.56],[2.2,.78],[1.6,.9],[.42,.92],[.25,.84],[-1.25,.84],[-1.6,.96],[-2.16,.92]],1.56,paint,.12,'carroceria'));
 const cuero=T('otro',0x8a4b2a,{roughness:.6});
 [-.38,.38].forEach(z=>{g.add(mesh(new THREE.BoxGeometry(.5,.12,.5),cuero,-.55,.92,z));const r=mesh(new THREE.BoxGeometry(.14,.5,.5),cuero,-.86,1.12,z);r.rotation.z=.18;g.add(r)});
 const vol=mesh(new THREE.TorusGeometry(.17,.025,8,24),black,.08,1.12,.38);vol.rotation.y=Math.PI/2;vol.rotation.x=.4;g.add(vol);
 const ws=mesh(new THREE.BoxGeometry(.04,.36,1.5),glass,.42,1.1,0);ws.rotation.z=.55;g.add(ws);
 const wf=mesh(new THREE.BoxGeometry(.06,.05,1.56),chrome,.33,1.26,0);g.add(wf);
 [-.38,.38].forEach(z=>{const a=mesh(new THREE.TorusGeometry(.26,.035,8,20,Math.PI),chrome,-1.1,.9,z);a.rotation.y=Math.PI/2;g.add(a)});
 [-.58,.58].forEach(z=>{const f=mesh(new THREE.CylinderGeometry(.15,.15,.1,22),faro(),2.12,.72,z);f.rotation.z=Math.PI/2;g.add(f);
  const ar=mesh(new THREE.TorusGeometry(.15,.03,8,22),chrome,2.15,.72,z);ar.rotation.y=Math.PI/2;g.add(ar);
  const p=mesh(new THREE.CylinderGeometry(.09,.09,.08,16),piloto(),-2.2,.78,z);p.rotation.z=Math.PI/2;g.add(p)});
 [2.3,-2.24].forEach(x=>g.add(mesh(new THREE.BoxGeometry(.08,.1,1.66),chrome,x,.46,0)));
 g.add(mesh(new THREE.BoxGeometry(.06,.14,.7),chrome,2.24,.55,0));
 g.add(mesh(new THREE.BoxGeometry(1.3,.012,.2),T('otro',0xfaf6ea,{roughness:.4}),1.15,.925,0));
 const wheels=[],blanco=T('otro',0xfaf6ea,{roughness:.5});
 [[1.38,.8],[1.38,-.8],[-1.4,.8],[-1.4,-.8]].forEach(([x,z])=>{const w=rueda(g,x,.42,z,.42,.3,chrome,null,16);
  const b=mesh(new THREE.TorusGeometry(.34,.035,8,28),blanco,0,0,z>0?.15:-.15);w.add(b);wheels.push(w)});
 g.userData.wheels=wheels;return g}

// ---- Toralla RR: superdeportiva carenada magenta, horquilla dorada y el piloto agachado
function toralla(o={}){
 const {black,chrome}=base(),g=new THREE.Group(),paint=T('pintura',0xe0245e,{metalness:.7,roughness:.2,envMapIntensity:1.4}),wheels=[];
 const oro=T('otro',0xd4a52a,{metalness:.9,roughness:.25});
 [.85,-.82].forEach(x=>wheels.push(ruedaMoto(g,x,.46,.36,.11,T('otro',0x2a2d36,{metalness:.8,roughness:.35}))));
 g.add(ext([[-.15,.55],[.5,.52],[.98,.92],[1.02,1.16],[.78,1.34],[.42,1.26],[.1,1.22],[-.42,1.2],[-.78,1.38],[-1.08,1.44],[-.85,1.2],[-.5,.92]],.4,paint,.05,'carroceria'));
 g.add(mesh(new THREE.BoxGeometry(.5,.07,.28),black,-.32,1.27,0));
 const sc=mesh(new THREE.BoxGeometry(.04,.32,.32),T('otro',0x2a3440,{transparent:true,opacity:.7,metalness:.9,roughness:.05}),.86,1.4,0);sc.rotation.z=-.95;g.add(sc);
 [-.08,.08].forEach(z=>g.add(mesh(new THREE.BoxGeometry(.04,.06,.1),faro(),1.03,1.03,z*1.2)));
 [-.12,.12].forEach(z=>palo(g,[.86,.48],[.62,1.18],.06,oro,z,.06));
 const hb=mesh(new THREE.CylinderGeometry(.03,.03,.62,10),black,.6,1.26,0);hb.rotation.x=Math.PI/2;g.add(hb);
 const ex=mesh(new THREE.CylinderGeometry(.07,.09,.55,12),chrome,-.55,.72,.22);ex.rotation.z=1.1;g.add(ex);
 g.add(mesh(new THREE.BoxGeometry(.05,.05,.16),piloto(),-1.09,1.38,0));
 if(o.piloto)motorista(g,paint,{hip:[-.38,1.32],knee:[.16,1.22],peg:[-.08,.9],grip:[.58,1.3],lean:1.05});
 g.userData.wheels=wheels;return g}

// ---- Arenal 125: scooter retro amarillo, escudo delantero, plataforma para los pies y faro en el manillar
function arenal(o={}){
 const {black,chrome}=base(),g=new THREE.Group(),paint=T('pintura',0xf5cc3a,{metalness:.55,roughness:.28,envMapIntensity:1.3}),wheels=[];
 [.78,-.75].forEach(x=>wheels.push(ruedaMoto(g,x,.35,.26,.09,chrome)));
 g.add(ext([[-1.08,.5],[-.28,.48],[-.16,.72],[-.24,1.0],[-.56,1.12],[-1.02,1.06],[-1.18,.82]],.5,paint,.1,'carroceria'));
 g.add(mesh(new THREE.BoxGeometry(.66,.08,.44),black,.18,.52,0));
 g.add(ext([[.4,.48],[.64,.48],[.8,1.26],[.62,1.3]],.5,paint,.06,'carroceria'));
 palo(g,[.74,.42],[.76,1.42],.1,paint,0,.1);
 const fd=mesh(new THREE.TorusGeometry(.33,.07,8,16,Math.PI),paint,.78,.37,0,'carroceria');g.add(fd);
 g.add(mesh(new THREE.BoxGeometry(.24,.16,.6),paint,.76,1.48,0,'carroceria'));
 const f=mesh(new THREE.CylinderGeometry(.1,.1,.08,18),faro(),.89,1.48,0);f.rotation.z=Math.PI/2;g.add(f);
 [-.34,.34].forEach(z=>{palo(g,[.74,1.54],[.7,1.72],.03,chrome,z,.03);g.add(mesh(new THREE.SphereGeometry(.06,10,8),chrome,.7,1.75,z))});
 g.add(mesh(new THREE.BoxGeometry(.78,.12,.36),T('otro',0x6b3a22,{roughness:.6}),-.6,1.18,0));
 g.add(mesh(new THREE.BoxGeometry(.32,.03,.3),chrome,-1.08,1.14,0));
 g.add(mesh(new THREE.BoxGeometry(.05,.08,.16),piloto(),-1.2,.92,0));
 g.add(mesh(new THREE.BoxGeometry(.6,.06,.52),T('otro',0x9ee8d2,{roughness:.4}),-.62,.74,0));
 if(o.piloto)motorista(g,paint,{hip:[-.42,1.28],knee:[.12,1.14],peg:[.2,.6],grip:[.76,1.56],lean:.22});
 g.userData.wheels=wheels;return g}

// ---- Rande SR: helicóptero de rescate naranja y blanco, largo, con grúa, foco y cinco palas
function rande(){
 const {glass}=base(),g=new THREE.Group(),paint=T('pintura',0xff6a1a,{metalness:.55,roughness:.28,envMapIntensity:1.4}),dk=T('otro',0x1b1e26,{metalness:.6,roughness:.35}),bl=T('otro',0xf4f4f0,{roughness:.4});
 const b=mesh(new THREE.SphereGeometry(1,36,24),paint,.25,1.42,0,'carroceria');b.scale.set(1.9,.95,.86);g.add(b);
 const c=mesh(new THREE.SphereGeometry(1,36,24),glass,1.42,1.56,0);c.scale.set(.78,.62,.74);g.add(c);
 const tb=mesh(new THREE.CylinderGeometry(.12,.32,2.6,16),paint,-2.55,1.62,0,'carroceria');tb.rotation.z=Math.PI/2+.05;g.add(tb);
 const fin=mesh(new THREE.BoxGeometry(.55,1.0,.08),bl,-3.82,2.05,0);fin.rotation.z=-.32;g.add(fin);
 g.add(mesh(new THREE.BoxGeometry(.4,.05,1.1),paint,-3.4,1.64,0,'carroceria'));
 [-1,1].forEach(s=>{g.add(mesh(new THREE.BoxGeometry(1.0,.62,.04),bl,-.05,1.38,s*.84));g.add(mesh(new THREE.BoxGeometry(.42,.3,.03),glass,-.05,1.5,s*.865))});
 g.add(mesh(new THREE.BoxGeometry(1.1,.32,.74),dk,.25,2.28,0));
 g.add(mesh(new THREE.CylinderGeometry(.1,.14,.3,12),dk,.35,2.5,0));
 g.add(mesh(new THREE.BoxGeometry(.5,.08,.08),dk,.55,2.05,.95));g.add(mesh(new THREE.BoxGeometry(.14,.18,.14),dk,.78,1.95,.95));
 g.add(mesh(new THREE.SphereGeometry(.13,14,10),faro(),1.55,.72,0));
 patines(g,3.3,.3,[[-.5,.62],[1.0,.62]],.72);
 const rot=rotorPalas(5,2.55,2.66);g.add(rot);
 const tr=rotorCola(-3.95,2.12,.12,3,.85);g.add(tr);
 lucesNav(g,-.6,.9,.82);
 g.userData.rot=rot;g.userData.tr=tr;return g}

// ---- Ons Vortex: helicóptero acrobático violeta, fino, cabina en tándem, alas cortas y rotor de cola carenado
function vortex(){
 const {glass,chrome}=base(),g=new THREE.Group(),paint=T('pintura',0x7a3cff,{metalness:.65,roughness:.22,envMapIntensity:1.5}),dk=T('otro',0x1b1e26,{metalness:.6,roughness:.35}),am=T('otro',0xffd23a,{roughness:.35});
 const b=mesh(new THREE.SphereGeometry(1,36,24),paint,.35,1.15,0,'carroceria');b.scale.set(1.75,.62,.5);g.add(b);
 const c=mesh(new THREE.SphereGeometry(1,36,24),glass,.75,1.55,0);c.scale.set(1.08,.42,.4);g.add(c);
 const tb=mesh(new THREE.CylinderGeometry(.08,.24,2.6,16),paint,-2.15,1.3,0,'carroceria');tb.rotation.z=Math.PI/2+.03;g.add(tb);
 const fin=mesh(new THREE.BoxGeometry(.62,.8,.06),paint,-3.35,1.75,0,'carroceria');fin.rotation.z=-.62;g.add(fin);
 const fv=mesh(new THREE.BoxGeometry(.4,.45,.06),am,-3.2,1.0,0);fv.rotation.z=.6;g.add(fv);
 g.add(mesh(new THREE.TorusGeometry(.32,.07,10,28),paint,-3.42,1.36,0,'carroceria'));
 g.add(mesh(new THREE.BoxGeometry(.62,.06,2.0),paint,.05,1.0,0,'carroceria'));
 [-1,1].forEach(s=>{const p=mesh(new THREE.CylinderGeometry(.09,.09,.75,12),dk,.05,.95,s*1.02);p.rotation.z=Math.PI/2;g.add(p);
  g.add(mesh(new THREE.SphereGeometry(.09,10,8),am,.43,.95,s*1.02))});
 g.add(mesh(new THREE.BoxGeometry(2.0,.03,.06),am,.2,1.52,.5));g.add(mesh(new THREE.BoxGeometry(2.0,.03,.06),am,.2,1.52,-.5));
 g.add(mesh(new THREE.CylinderGeometry(.09,.13,.3,12),dk,.35,1.86,0));
 patines(g,2.5,.3,[[-.35,.62],[.95,.6]],.5);
 const rot=rotorPalas(3,2.25,2.05);g.add(rot);
 const tr=rotorCola(-3.42,1.36,0,4,.55);g.add(tr);
 lucesNav(g,.05,1.0,1.12);
 g.userData.rot=rot;g.userData.tr=tr;return g}

const C3=[coche,bouzas,spider],M3=[moto,toralla,arenal],H3=[heli,rande,vortex];
return{coche:(i=0)=>C3[i](),moto:(i=0,o)=>M3[i](o),heli:(i=0)=>H3[i](),COL}};
window.GTV_OF_INFO={
 coche:[{n:'Ría GT 300',k:'Deportivo',s:[82,70,76]},{n:'Bouzas 4x4',k:'Todoterreno',s:[62,58,72]},{n:'Samil Spider',k:'Descapotable',s:[76,66,86]}],
 moto:[{n:'Castro 600',k:'Naked',s:[74,92,88]},{n:'Toralla RR',k:'Superdeportiva',s:[96,94,70]},{n:'Arenal 125',k:'Scooter',s:[46,58,96]}],
 heli:[{n:'Cíes H-1',k:'Vuelo libre',s:[95,100,60]},{n:'Rande SR',k:'Rescate',s:[80,92,70]},{n:'Ons Vortex',k:'Acrobático',s:[100,84,94]}]};
