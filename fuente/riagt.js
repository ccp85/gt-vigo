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
