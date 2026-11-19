function mkPersona(){const g=new THREE.Group();   // protagonista (edit_muneco.py): cartoon pulido · sudadera roja con capucha, vaqueros, zapatillas, cara expresiva
 // mira hacia +x · pies en y=0 · userData.piernas/brazos con dos hijos cada uno (los usan andar, nadar y la moto)
 const C={PIEL:0xf0bf94,PIEL2:0xe2a47c,ROPA:0xe2483a,ROPA2:0xb8322a,PANT:0x2f5596,PANT2:0x4a74b8,ZAP:0xf4f3ee,SUELA:0x2a2c33,FRANJA:0x2b8fd6,PELO:0x4a3022,PELO2:0x5e3d2b,OJO:0x3b2414,BLANCO:0xffffff,CORDON:0xf2efe8,MEJ:0xf28c8c};
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
 add(tronco,new THREE.LatheGeometry(perfil,20),M(C.ROPA,.75),0,0,0,0,0,0,.68,1,1);                 // sudadera
 add(tronco,CIL(.0104,.0101,.003,20),M(C.ROPA2,.8),0,.0026,0,0,0,0,.7,1,1);                       // puño elástico de la cintura
 add(tronco,CAP(.0034,.0072,10),M(C.ROPA2,.8),.0068,.0085,0,Math.PI/2,0,0,.42,1,1.04);            // bolsillo canguro
 add(tronco,new THREE.TorusGeometry(.0052,.0023,8,18),M(C.ROPA,.75),-.0006,.0282,0,Math.PI/2,0,0,.95,1.12,1);  // capucha alrededor del cuello
 add(tronco,ESF(.0072,14,10),M(C.ROPA,.75),-.0058,.0246,0,0,0,.35,.55,.8,1);                      // capucha caída a la espalda
 add(tronco,ESF(.0052,12,8),M(C.ROPA2,.85),-.0074,.0232,0,0,0,.35,.35,.62,.78);                    // interior de la capucha
 for(const z of[-.0024,.0024]){add(tronco,CIL(.00045,.00045,.0085,6),M(C.CORDON,.5),.0072,.0218,z,0,0,-.12);   // cordones
  add(tronco,CIL(.0007,.0007,.0018,6),M(C.CORDON,.4),.0077,.0168,z,0,0,-.12)}
 // ---- brazos: hombro → codo → puño con mano redonda y pulgar
 const brazos=new THREE.Group();tronco.add(brazos);
 for(const z of[-.0128,.0128]){const b=new THREE.Group();b.position.set(0,.0247,z);b.rotation.x=z<0?.13:-.13;brazos.add(b);
  add(b,ESF(.0041,12,8),M(C.ROPA,.75),0,-.0004,0);                          // hombro
  add(b,CAP(.0035,.0068),M(C.ROPA,.75),0,-.0056,0);                         // brazo
  const codo=new THREE.Group();codo.position.y=-.0108;b.add(codo);b.userData.codo=codo;
  add(codo,CAP(.0031,.0062),M(C.ROPA,.75),0,-.0046,0);                      // antebrazo
  add(codo,CIL(.0031,.0032,.0024),M(C.ROPA2,.8),0,-.0093,0);                // puño elástico
  add(codo,ESF(.0031,12,8),M(C.PIEL,.55),.0002,-.0125,0,0,0,0,.92,1.08,.88);   // mano
  add(codo,ESF(.0012,8,6),M(C.PIEL,.55),.0024,-.0113,z<0?.0011:-.0011)}     // pulgar
 g.userData.brazos=brazos;
 // ---- cabeza (pivota en el cuello): grande y redonda, ojos con brillo, cejas, sonrisa, mofletes y tupé
 add(tronco,CIL(.0031,.0034,.005,12),M(C.PIEL,.55),0,.03,0);                 // cuello
 const cab=new THREE.Group();cab.position.y=.0315;tronco.add(cab);g.userData.cabeza=cab;const H=.0094;   // centro de la cara en y=H (relativo al cuello)
 add(cab,ESF(.0098,22,16),M(C.PIEL,.55),0,H,0,0,0,0,.96,1,1);
 for(const s of[-1,1]){const z=s*.0034;
  add(cab,ESF(.0022,14,10),M(C.BLANCO,.25),.0081,H+.0008,z,0,0,0,.55,1.12,.9);   // ojo
  add(cab,ESF(.00145,12,8),M(C.OJO,.2),.0091,H+.0006,z*.98,0,0,0,.5,1.1,.95);    // iris
  add(cab,ESF(.0008,8,6),M(0x0d0806,.2),.0096,H+.0006,z*.98,0,0,0,.5,1.1,1);    // pupila
  add(cab,ESF(.00042,6,4),M(C.BLANCO,.1,{emissive:0xffffff,emissiveIntensity:.6}),.0098,H+.0013,z*.98-.0004);   // brillo
  add(cab,CAP(.00052,.0026,6),M(C.PELO,.8),.0081,H+.0044,z*1.02,Math.PI/2+s*.18,0,0);   // ceja
  add(cab,ESF(.0016,10,6),M(C.MEJ,.7,{transparent:true,opacity:.55}),.0074,H-.0025,s*.0058,0,0,0,.35,.7,1);   // moflete
  add(cab,ESF(.0022,10,8),M(C.PIEL,.55),-.0004,H,s*.0094,0,0,0,.65,1,.5);    // oreja
  add(cab,ESF(.0011,8,6),M(C.PIEL2,.6),.0001,H,s*.0101,0,0,0,.5,.8,.4)}
 add(cab,ESF(.0016,10,8),M(C.PIEL2,.55),.0099,H-.001,0,0,0,0,1,.9,1);                              // nariz
 add(cab,new THREE.TorusGeometry(.0022,.00048,6,14,Math.PI),M(0x8a3b2c,.5),.0084,H-.0036,0,0,Math.PI/2,Math.PI,.85,.85,.6);   // sonrisa
 // pelo: casquete con raya, tupé y mechones
 add(cab,new THREE.SphereGeometry(.0104,22,12,0,Math.PI*2,0,Math.PI*.56),M(C.PELO,.75),-.0013,H+.0004,0,0,0,.42);
 add(cab,ESF(.0055,14,10),M(C.PELO,.75),-.0064,H-.0012,0,0,0,0,.7,1.1,1.45);           // nuca
 for(const[z,ry]of[[-.0046,.35],[-.0016,.1],[.0014,-.1],[.0044,-.35]])
  add(cab,ESF(.0036,12,8),M(C.PELO2,.7),.0062,H+.0062,z,0,ry,-.75,.55,.75,.95);       // flequillo
 add(cab,ESF(.0048,14,10),M(C.PELO2,.7),.0028,H+.0088,0,0,0,-.45,1.2,.6,1.1);           // tupé
 add(cab,new THREE.ConeGeometry(.0015,.0052,8),M(C.PELO2,.7),-.0018,H+.0112,.0006,0,0,.55);   // remolino
 for(const s of[-1,1])add(cab,ESF(.0034,10,8),M(C.PELO,.75),.0004,H+.0028,s*.0083,0,0,0,.9,1.25,.45);   // patillas sobre las orejas
 g.traverse(o=>{if(o.isMesh)o.castShadow=true});return g}
// animación al andar (o quieto, respirando): piernas con rodilla, brazos con codo, tronco y cabeza
function animPersona(p,t,amp){const ud=p.userData,ph=t*14,s=Math.sin(ph),c=Math.cos(ph);
 const pl=ud.piernas.children;for(let i=0;i<2;i++){const sg=i?-1:1,L=pl[i];L.rotation.z=sg*s*.62*amp;if(L.userData.rod)L.userData.rod.rotation.z=-Math.max(0,sg*c)*1.0*amp-.05*amp}
 if(ud.brazos){const ba=ud.brazos.children;for(let i=0;i<2;i++){const sg=i?1:-1,B=ba[i];B.rotation.z=sg*s*.55*amp;if(B.userData.codo)B.userData.codo.rotation.z=.25+.35*amp+Math.max(0,sg*s)*.3*amp}}
 const res=Math.sin(t*2.2);
 if(ud.tronco){ud.tronco.rotation.y=s*.13*amp;ud.tronco.rotation.z=-.07*amp;ud.tronco.scale.y=1+res*.012*(1-amp)}
 if(ud.cabeza){ud.cabeza.rotation.y=-s*.1*amp+Math.sin(t*.7)*.18*(1-amp);ud.cabeza.rotation.z=.05*amp+res*.02*(1-amp)}}
