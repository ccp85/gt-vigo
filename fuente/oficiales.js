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

// ---- Ría GT 300: deportivo de dos puertas, el coche rojo de siempre. Carrocería modelada por secciones (como un torno a lo largo del coche),
// paso de rueda, faros afilados, luz trasera de lado a lado, difusor con cuatro escapes, alerón, retrovisores, llantas de cinco radios con
// pinzas de freno y, detrás de cristales tintados, el interior: salpicadero, volante, asientos tipo baquet y (con o.piloto) el conductor.
function coche(o={}){
 const {chrome,black}=base(),g=new THREE.Group(),paint=T('pintura',COL.coche,{metalness:.7,roughness:.22,envMapIntensity:1.4});
 const glass=T('cristal',0x0b1020,{metalness:.9,roughness:.06,transparent:true,opacity:.42});
 const goma=T('negro',0x111114,{metalness:.1,roughness:.8}),plastico=T('negro',0x16171b,{metalness:.3,roughness:.45});
 const grafito=T('otro',0x2b2e35,{metalness:.8,roughness:.3}),naranja=T('otro',0xff5a36,{emissive:0x5a1000}),blanco=T('otro',0xf2f2ee,{roughness:.5}),plata=T('otro',0xc4c8cf,{metalness:.6,roughness:.28});
 const interior=T('otro',0x1b1b1f,{roughness:.8,metalness:.05}),cuero=T('otro',0xd2451e,{roughness:.55,metalness:.05});
 // curva suave por puntos (Catmull-Rom) para el perfil, el ancho y el suelo
 const curva=K=>x=>{if(x>=K[0][0])return K[0][1];const n=K.length;if(x<=K[n-1][0])return K[n-1][1];let i=0;while(K[i+1][0]>x)i++;
  const p0=K[Math.max(0,i-1)][1],p1=K[i][1],p2=K[i+1][1],p3=K[Math.min(n-1,i+2)][1],t=(K[i][0]-x)/(K[i][0]-K[i+1][0]);
  return .5*(2*p1+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)};
 const top=curva([[2.24,.6],[2.12,.75],[1.9,.85],[1.35,.95],[.9,.97],[.5,.99],[-.5,1.0],[-1.38,1.03],[-1.9,1.02],[-2.12,.97],[-2.24,.86]]);
 const bot=curva([[2.24,.42],[2.0,.33],[1.0,.3],[-1.0,.3],[-2.0,.34],[-2.24,.44]]);
 const anc=curva([[2.24,.58],[2.12,.74],[1.8,.85],[1.35,.89],[.8,.85],[0,.84],[-.8,.86],[-1.38,.91],[-1.9,.87],[-2.12,.79],[-2.24,.62]]);
 const gTop=curva([[.94,.97],[.62,1.18],[.25,1.4],[0,1.44],[-.5,1.455],[-.92,1.42],[-1.22,1.3],[-1.64,1.0]]);
 const se=(v,e)=>Math.sign(v)*Math.pow(Math.abs(v),e);
 // punto de una sección: th=0 lado derecho (+z), PI/2 arriba; tumble = cuánto se estrecha hacia arriba (la cabina)
 const P=(x,th,yb,yt,w,n,tumble,s=1)=>{const cy=(yb+yt)/2,h=(yt-yb)/2,c=Math.cos(th),sn=Math.sin(th),yy=se(sn,2/n),zz=se(c,2/n)*w*(1-tumble*Math.max(0,yy));
  return [x,cy+h*yy*s,zz*s]};
 // superficie: x de x0 a x1 (nx tramos), ángulo de a0 a a1 (na tramos); con tapas cierra los extremos
 const sup=(fn,x0,x1,nx,a0,a1,na,mat,tapas,name)=>{const pos=[],idx=[];
  for(let i=0;i<=nx;i++){const x=x0+(x1-x0)*i/nx;for(let j=0;j<=na;j++)pos.push(...fn(x,a0+(a1-a0)*j/na))}
  for(let i=0;i<nx;i++)for(let j=0;j<na;j++){const a=i*(na+1)+j,b=a+na+1;idx.push(a,a+1,b,b,a+1,b+1)}
  if(tapas)for(const i of [0,nx]){const c=pos.length/3;let sx=0,sy=0,sz=0;for(let j=0;j<=na;j++){const k=(i*(na+1)+j)*3;sx+=pos[k];sy+=pos[k+1];sz+=pos[k+2]}
   pos.push(sx/(na+1),sy/(na+1),sz/(na+1));for(let j=0;j<na;j++){const a=i*(na+1)+j;i?idx.push(c,a,a+1):idx.push(c,a+1,a)}}
  const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));geo.setIndex(idx);geo.computeVertexNormals();
  const m=new THREE.Mesh(geo,mat);if(name)m.name=name;g.add(m);return m};
 const cuerpo=(x,th,s=1)=>P(x,th,bot(x),top(x),anc(x),5,0,s);
 const cabina=(x,th,s=1)=>{const yb=top(x)-.04,yt=Math.max(yb+.01,gTop(x));return P(x,th,yb-(yt-yb)*.15,yt,anc(x)*.8,3,.28,s)};
 // la carrocería va de delante (+x) hacia atrás: las caras miran hacia fuera
 sup(cuerpo,2.24,-2.24,64,0,Math.PI*2,40,paint,true,'carroceria');
 // cabina: cristal tintado entero y, encima, las piezas de chapa (techo, pilares, aletas traseras)
 sup(cabina,.94,-1.64,40,-.9,Math.PI+.9,36,glass,false);
 const chapa=(x0,x1,a0,a1)=>sup((x,th)=>cabina(x,th,1.012),x0,x1,Math.max(2,Math.round(Math.abs(x1-x0)*14)),a0,a1,8,paint,false,'carroceria');
 chapa(.3,-1.0,.62,Math.PI-.62);                       // techo
 chapa(.94,-1.64,.46,.62);chapa(.94,-1.64,Math.PI-.62,Math.PI-.46);   // pilares A y canaletas del techo
 chapa(-.98,-1.64,-.9,.46);chapa(-.98,-1.64,Math.PI-.46,Math.PI+.9); // pilares traseros (fastback)
 const ad=(geo,mat,x,y,z,rx=0,ry=0,rz=0,name)=>{const m=mesh(geo,mat,x,y,z,name);m.rotation.set(rx,ry,rz);g.add(m);return m};
 const caja=(w,h,d,mat,x,y,z,rx,ry,rz,name)=>ad(new THREE.BoxGeometry(w,h,d),mat,x,y,z,rx,ry,rz,name);
 // ruedas: neumático, llanta de cinco radios, disco y pinza naranja; pasos de rueda negros con su ceja de chapa
 const wheels=[];
 [[1.35,1],[1.35,-1],[-1.38,1],[-1.38,-1]].forEach(([x,s])=>{const z=.8*s,w=new THREE.Group();w.position.set(x,.44,z);
  const cil=(r,l,m,zz,seg=28)=>{const c=mesh(new THREE.CylinderGeometry(r,r,l,seg),m,0,0,zz);c.rotation.x=Math.PI/2;w.add(c);return c};
  const banda=mesh(new THREE.CylinderGeometry(.44,.44,.3,32,1,true),goma);banda.rotation.x=Math.PI/2;w.add(banda);
  const flanco=mesh(new THREE.RingGeometry(.3,.44,32),goma,0,0,.15*s);if(s<0)flanco.rotation.y=Math.PI;w.add(flanco);
  const barril=mesh(new THREE.CylinderGeometry(.3,.3,.28,24,1,true),grafito);barril.rotation.x=Math.PI/2;w.add(barril);
  const fondo=mesh(new THREE.CircleGeometry(.3,24),goma,0,0,-.1*s);if(s<0)fondo.rotation.y=Math.PI;w.add(fondo);
  cil(.25,.02,T('otro',0x8a8d93,{metalness:.9,roughness:.4}),-.03*s,24);
  const pz=mesh(new THREE.BoxGeometry(.13,.2,.07),naranja,x-.13,.6,z+.02*s);pz.rotation.z=.55;g.add(pz);
  for(let k=0;k<5;k++){const a=k*Math.PI*2/5,sp=mesh(new THREE.BoxGeometry(.25,.055,.04),plata,Math.cos(a)*.15,Math.sin(a)*.15,.155*s);sp.rotation.z=a;w.add(sp)}
  cil(.075,.33,naranja,.01*s,14);w.add(mesh(new THREE.TorusGeometry(.295,.018,6,28),plata,0,0,.14*s));
  g.add(w);wheels.push(w);
  const zc=(anc(x)+.004)*s,arco=new THREE.CircleGeometry(.48,24,0,Math.PI);
  ad(arco,goma,x,.42,zc,0,s>0?0:Math.PI,0);
  ad(new THREE.TorusGeometry(.48,.028,6,24,Math.PI),paint,x,.42,zc-.022*s,0,0,0,'carroceria')});
 // morro: parrilla, tomas de aire, faldón y faros afilados con luz de día
 caja(.03,.12,.9,plastico,2.245,.5,0);for(let k=-4;k<=4;k++)caja(.02,.11,.012,chrome,2.258,.5,k*.1);
 [-1,1].forEach(s=>{caja(.06,.1,.26,plastico,2.2,.45,.5*s,0,.35*s,0);
  const f=ad(new THREE.SphereGeometry(1,18,10),faro(),2.01,.79,.58*s,0,-.35*s,-.12);f.scale.set(.19,.04,.12);
  caja(.24,.018,.05,plastico,1.98,.825,.5*s,0,-.35*s,-.12);
  caja(.03,.015,.3,T('luz',0xffffff,{emissive:0xeaf4ff}),2.08,.72,.52*s,0,-.45*s,0);
  // espejos, tiradores, línea de puerta, faldón y toma lateral
  const zl=x=>(anc(x)+.003)*s;
  const esp=ad(new THREE.SphereGeometry(1,14,10),paint,.7,1.07,(anc(.7)+.1)*s,0,0,0,'carroceria');esp.scale.set(.12,.065,.09);
  caja(.06,.03,.1,plastico,.72,1.02,(anc(.7)+.03)*s);ad(new THREE.PlaneGeometry(.13,.08),T('cromo',0xdfe3ea,{metalness:1,roughness:.05}),.59,1.07,(anc(.7)+.1)*s,0,-Math.PI/2,0);
  caja(.012,.5,.012,plastico,.86,.68,zl(.86));caja(.012,.5,.012,plastico,-.72,.7,zl(-.72));
  caja(.14,.035,.03,chrome,-.48,.88,zl(-.48)+.01*s);
  caja(1.95,.09,.06,plastico,0,.35,(anc(0)-.02)*s);
  caja(.34,.13,.04,plastico,-.82,.63,zl(-.82));for(let k=0;k<3;k++)caja(.3,.012,.05,goma,-.82,.59+k*.04,zl(-.82)+.006*s);
  // pilotos traseros grandes
  caja(.05,.09,.28,piloto(),-2.24,.78,.48*s)});
 caja(.04,.035,.7,piloto(),-2.245,.8,0);
 caja(.15,.025,1.3,plastico,2.17,.33,0);
 // capó: dos rejillas
 [-.26,.26].forEach(z=>{caja(.36,.02,.12,plastico,1.52,top(1.52)+.004,z,0,0,-.17);for(let k=0;k<3;k++)caja(.34,.024,.012,goma,1.52,top(1.52)+.006,z-.04+k*.04,0,0,-.17)});
 // trasera: difusor con aletas, cuatro escapes y matrícula
 caja(.18,.12,1.3,plastico,-2.16,.39,0);for(let k=-2;k<=2;k++)caja(.16,.11,.02,goma,-2.18,.38,k*.25);
 [-.37,-.25,.25,.37].forEach(z=>{const e=ad(new THREE.CylinderGeometry(.05,.05,.16,14),chrome,-2.2,.42,z,0,0,Math.PI/2);ad(new THREE.CircleGeometry(.036,12),goma,-2.282,.42,z,0,-Math.PI/2,0)});
 caja(.02,.11,.5,blanco,-2.25,.6,0);caja(.022,.11,.05,T('otro',0x2a4fb8,{roughness:.5}),-2.252,.6,-.225);
 // alerón con perfil de ala, patas y placas laterales
 {const s=new THREE.Shape();s.moveTo(.2,0);s.quadraticCurveTo(0,.07,-.22,.025);s.lineTo(-.22,.0);s.quadraticCurveTo(0,.02,.2,0);
  const geo=new THREE.ExtrudeGeometry(s,{depth:1.76,bevelEnabled:false});geo.translate(0,0,-.88);ad(geo,plastico,-1.98,1.27,0,0,0,.08);
  [-.55,.55].forEach(z=>caja(.1,.26,.04,plastico,-1.96,1.15,z));[-.89,.89].forEach(z=>caja(.34,.14,.02,plastico,-1.98,1.3,z))}
 // antena de aleta en el techo
 ad(new THREE.ConeGeometry(.05,.14,4),plastico,-.82,1.48,0,0,0,.6).scale.set(1,1,.35);
 // interior, visto a través de los cristales: suelo, salpicadero, volante, consola y asientos baquet
 caja(2.0,.02,1.0,interior,-.3,1.005,0);
 caja(.36,.1,1.04,interior,.48,1.05,0);caja(.02,.03,1.04,cuero,.3,1.07,0);caja(.14,.05,.2,plastico,.4,1.11,-.38);
 caja(.7,.08,.2,interior,0,1.04,0);caja(.08,.06,.04,chrome,.1,1.09,0);
 const vol=ad(new THREE.TorusGeometry(.14,.022,8,24),plastico,.24,1.15,-.38);vol.rotation.order='YXZ';vol.rotation.set(.35,Math.PI/2,0);
 ad(new THREE.CylinderGeometry(.035,.035,.12,10),plastico,.24,1.15,-.38,0,Math.PI/2,0).rotation.set(0,0,Math.PI/2-.35);
 [-.32,.32].forEach(z=>{const r=new THREE.Group();r.position.set(-.5,.52,z);r.rotation.z=.2;g.add(r);
  r.add(mesh(new THREE.BoxGeometry(.5,.12,.42),interior,.14,.06,0));
  r.add(mesh(new THREE.BoxGeometry(.1,.78,.38),interior,-.1,.41,0));r.add(mesh(new THREE.BoxGeometry(.106,.56,.13),cuero,-.1,.45,0));
  [-1,1].forEach(q=>r.add(mesh(new THREE.BoxGeometry(.16,.5,.05),interior,-.06,.42,q*.2)))});
 caja(.3,.04,.9,interior,-1.2,1.04,0);
 // el conductor (sudadera roja como en la moto), con las manos en el volante
 if(o.piloto){const piel=T('otro',0xe0a98a,{roughness:.7}),sud=T('otro',0xc0262b,{roughness:.8}),pelo=T('otro',0x2a1c14,{roughness:.9});
  const z=-.38,tr=mesh(new THREE.CapsuleGeometry(.15,.3,6,12),sud,-.44,.86,z);tr.rotation.z=.2;tr.scale.set(.75,1,1);g.add(tr);
  ad(new THREE.CylinderGeometry(.045,.055,.08,10),piel,-.34,1.19,z);
  ad(new THREE.SphereGeometry(.1,16,12),piel,-.32,1.3,z).scale.set(1,1.1,.92);
  const pe=ad(new THREE.SphereGeometry(.105,16,10,0,Math.PI*2,0,Math.PI*.55),pelo,-.335,1.315,z,0,0,.35);pe.scale.set(1.04,1.08,.96);
  [-1,1].forEach(q=>{const hom=new THREE.Vector3(-.38,1.1,z+q*.17),man=new THREE.Vector3(.22,1.15,z+q*.14),d=man.clone().sub(hom);
   const b=ad(new THREE.CapsuleGeometry(.045,d.length(),4,8),sud,0,0,0);b.position.copy(hom).add(man).multiplyScalar(.5);b.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());
   ad(new THREE.SphereGeometry(.042,10,8),piel,man.x+.01,man.y,man.z)})}
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
return{coche:(i=0,o)=>C3[i](o),moto:(i=0,o)=>M3[i](o),heli:(i=0)=>H3[i](),COL}};
window.GTV_OF_INFO={
 coche:[{n:'Ría GT 300',k:'Deportivo',s:[82,70,76]},{n:'Bouzas 4x4',k:'Todoterreno',s:[62,58,72]},{n:'Samil Spider',k:'Descapotable',s:[76,66,86]}],
 moto:[{n:'Castro 600',k:'Naked',s:[74,92,88]},{n:'Toralla RR',k:'Superdeportiva',s:[96,94,70]},{n:'Arenal 125',k:'Scooter',s:[46,58,96]}],
 heli:[{n:'Cíes H-1',k:'Vuelo libre',s:[95,100,60]},{n:'Rande SR',k:'Rescate',s:[80,92,70]},{n:'Ons Vortex',k:'Acrobático',s:[100,84,94]}]};
