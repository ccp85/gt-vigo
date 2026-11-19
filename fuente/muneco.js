function mkPersona(){const g=new THREE.Group();   // protagonista (edit_muneco.py): cartoon pulido · camiseta blanca, vaqueros, zapatillas, ojos de punto y pelo rapado castaño
 // mira hacia +x · pies en y=0 · userData.piernas/brazos con dos hijos cada uno (los usan andar, nadar y la moto)
 const C={PIEL:0xf0bf94,PIEL2:0xe2a47c,ROPA:0xf6f5f1,ROPA2:0xdcdad4,PANT:0x2f5596,PANT2:0x4a74b8,ZAP:0xf4f3ee,SUELA:0x2a2c33,FRANJA:0x2b8fd6,PELO:0x6a4c38,PELO2:0x7a4e2c,OJO:0x3b2414,BLANCO:0xffffff,CORDON:0xf2efe8};
 const MC={};const M=(c,r=.62,x={})=>{const k=c+'|'+r+'|'+JSON.stringify(x);return MC[k]||(MC[k]=new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:r,metalness:0},x)))};
 const add=(par,geo,mat,x=0,y=0,z=0,rx=0,ry=0,rz=0,sx=1,sy=1,sz=1)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.rotation.set(rx,ry,rz);m.scale.set(sx,sy,sz);par.add(m);return m};
 const CAP=(r,l,s=10)=>new THREE.CapsuleGeometry(r,l,4,s),ESF=(r,a=14,b=10)=>new THREE.SphereGeometry(r,a,b),CIL=(a,b,h,s=14)=>new THREE.CylinderGeometry(a,b,h,s);
 // ---- piernas: cadera → rodilla → tobillo, con dobladillo y zapatilla redondeada
 const piernas=new THREE.Group();piernas.position.y=.03;g.add(piernas);
 for(const z of[-.0049,.0049]){const pv=new THREE.Group();pv.position.z=z;piernas.add(pv);
  add(pv,CAP(.0044,.0085),M(C.PANT,.8),0,-.0068,0);                         // muslo
  const rod=new THREE.Group();rod.position.y=-.0136;pv.add(rod);pv.userData.rod=rod;
  add(rod,CAP(.0039,.0075),M(C.PANT,.8),0,-.0052,0);                        // espinilla
  add(rod,CIL(.0043,.0042,.0026),M(C.PANT2,.8),0,-.0092,0);                 // dobladillo vuelto
  const pie=new THREE.Group();pie.position.y=-.0136;rod.add(pie);            // zapatilla (suelo en y=-.03 respecto a la cadera)
  add(pie,CAP(.0034,.0068,12),M(C.ZAP,.45),.0022,-.0007,0,0,0,Math.PI/2,1,.86,1.08);
  add(pie,CAP(.0036,.0072,12),M(C.SUELA,.7),.0022,-.0034,0,0,0,Math.PI/2,.62,.98,1.12);
  add(pie,CAP(.0035,.0066,12),M(C.FRANJA,.45),.0021,-.0019,0,0,0,Math.PI/2,.28,1.01,1.1);
  add(pie,ESF(.0016,8,6),M(C.CORDON,.5),.0045,.0017,0,0,0,0,1.3,.6,1.3)}   // lengüeta/cordones
 g.userData.piernas=piernas;
 // ---- tronco (pivota en la cadera para inclinarse y girar al andar)
 const T0=.031,tronco=new THREE.Group();tronco.position.y=T0;g.add(tronco);g.userData.tronco=tronco;
 add(tronco,CAP(.0058,.0098),M(C.PANT,.8),0,.0004,0,Math.PI/2,0,0,.82,1,1);  // cadera
 const perfil=[[.0001,.0012],[.0099,.0012],[.0109,.0045],[.0115,.011],[.0117,.017],[.0114,.0225],[.0101,.0258],[.0076,.0281],[.0045,.0293],[.0001,.0296]].map(([r,y])=>new THREE.Vector2(r,y));
 add(tronco,new THREE.LatheGeometry(perfil,20),M(C.ROPA,.75),0,0,0,0,0,0,.68,1,1);                 // camiseta
 add(tronco,CIL(.0104,.0101,.003,20),M(C.ROPA2,.8),0,.0026,0,0,0,0,.7,1,1);                       // bajo de la camiseta
 add(tronco,new THREE.TorusGeometry(.0042,.0009,8,20),M(C.ROPA2,.8),0,.0287,0,Math.PI/2,0,0,.95,1.15,1);   // cuello redondo
 // ---- brazos: hombro → codo → puño con mano redonda y pulgar
 const brazos=new THREE.Group();tronco.add(brazos);
 for(const z of[-.0128,.0128]){const b=new THREE.Group();b.position.set(0,.0247,z);b.rotation.x=z<0?.13:-.13;brazos.add(b);
  add(b,ESF(.0041,18,12),M(C.ROPA,.75),0,-.0004,0);                          // hombro
  add(b,CAP(.0039,.0036),M(C.ROPA,.75),0,-.0036,0);                         // manga corta
  add(b,CIL(.004,.0041,.0016),M(C.ROPA2,.8),0,-.0072,0);                    // borde de la manga
  add(b,CAP(.0029,.0072),M(C.PIEL,.55),0,-.0068,0);                         // brazo
  const codo=new THREE.Group();codo.position.y=-.0108;b.add(codo);b.userData.codo=codo;
  add(codo,CAP(.0027,.0062),M(C.PIEL,.55),0,-.0046,0);                      // antebrazo
  add(codo,ESF(.0031,12,8),M(C.PIEL,.55),.0002,-.0125,0,0,0,0,.92,1.08,.88);   // mano
  add(codo,ESF(.0012,8,6),M(C.PIEL,.55),.0024,-.0113,z<0?.0011:-.0011)}     // pulgar
 g.userData.brazos=brazos;
 // ---- cabeza (pivota en el cuello): grande y redonda, dos puntos negros de ojos, nariz, boca y pelo rapado
 add(tronco,CIL(.0031,.0034,.005,12),M(C.PIEL,.55),0,.03,0);                 // cuello
 const cab=new THREE.Group();cab.position.y=.0315;tronco.add(cab);g.userData.cabeza=cab;const H=.0094;   // centro de la cara en y=H (relativo al cuello)
 add(cab,ESF(.0098,22,16),M(C.PIEL,.55),0,H,0,0,0,0,.96,1,1);
 for(const s of[-1,1]){const z=s*.0034;
  add(cab,ESF(.00125,10,8),M(0x14110f,.3),.0088,H+.0012,z,0,0,0,.6,1.15,1);   // ojo: punto negro
  add(cab,ESF(.0022,10,8),M(C.PIEL,.55),-.0004,H,s*.0094,0,0,0,.65,1,.5);    // oreja
  add(cab,ESF(.0011,8,6),M(C.PIEL2,.6),.0001,H,s*.0101,0,0,0,.5,.8,.4)}
 add(cab,ESF(.0016,10,8),M(C.PIEL,.55),.0099,H-.001,0,0,0,0,1,.9,1);                              // nariz
 // pelo rapado: capa finísima con textura de pelo cortito (puntitos) y el borde difuminado, frente bien despejada
 if(!mkPersona.texPelo){const cv=document.createElement('canvas');cv.width=128;cv.height=64;const x=cv.getContext('2d');
  x.fillStyle='#5a3e2c';x.fillRect(0,0,128,64);
  for(let k=0;k<900;k++){const v=Math.random();x.fillStyle=v<.5?'rgba(52,34,22,.55)':'rgba(150,112,84,.35)';x.fillRect(Math.random()*128,Math.random()*64,1,1)}
  const gr=x.createLinearGradient(0,0,0,64);gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(.86,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(0,0,0,1)');
  x.globalCompositeOperation='destination-out';x.fillStyle=gr;x.fillRect(0,0,128,64);
  mkPersona.texPelo=new THREE.CanvasTexture(cv);mkPersona.texPelo.colorSpace=THREE.SRGBColorSpace}
 add(cab,new THREE.SphereGeometry(.01003,32,16,0,Math.PI*2,0,Math.PI*.53),new THREE.MeshStandardMaterial({map:mkPersona.texPelo,transparent:true,roughness:1,depthWrite:false}),-.0002,H,0,0,0,.47);
 // boca: sonrisa fina y oscura, pegada a la cara
 add(cab,new THREE.TorusGeometry(.0019,.00038,6,16,Math.PI*.8),M(0x3a2018,.6),.0084,H-.0034,0,0,Math.PI/2,Math.PI*1.1,1,1,.5);
 g.traverse(o=>{if(o.isMesh)o.castShadow=true});return g}
// animación al andar (o quieto, respirando): piernas con rodilla, brazos con codo, tronco y cabeza
function animPersona(p,t,amp){const ud=p.userData,ph=t*14,s=Math.sin(ph),c=Math.cos(ph);
 const pl=ud.piernas.children;for(let i=0;i<2;i++){const sg=i?-1:1,L=pl[i];L.rotation.z=sg*s*.62*amp;if(L.userData.rod)L.userData.rod.rotation.z=-Math.max(0,sg*c)*1.0*amp-.05*amp}
 if(ud.brazos){const ba=ud.brazos.children;for(let i=0;i<2;i++){const sg=i?1:-1,B=ba[i];B.rotation.z=sg*s*.55*amp;if(B.userData.codo)B.userData.codo.rotation.z=.25+.35*amp+Math.max(0,sg*s)*.3*amp}}
 const res=Math.sin(t*2.2);
 if(ud.tronco){ud.tronco.rotation.y=s*.13*amp;ud.tronco.rotation.z=-.07*amp;ud.tronco.scale.y=1+res*.012*(1-amp)}
 if(ud.cabeza){ud.cabeza.rotation.y=-s*.1*amp+Math.sin(t*.7)*.18*(1-amp);ud.cabeza.rotation.z=.05*amp+res*.02*(1-amp)}}
