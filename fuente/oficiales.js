// ===== Vehículos oficiales de GT Vigo: Ría GT 300 (coche), Castro 600 (moto) y Cíes H-1 (helicóptero) =====
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
return{coche,moto,heli,COL}};
