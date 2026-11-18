f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= LANCHA CON MOTOR FUERABORDA (modelo aportado por el usuario: lancha_con_motor.js) =================
# Se construye a escala real (4.5 m a lo largo de +Z), se gira para que la proa mire a +X, se escala a ~0.2 de largo
# (como la moto de agua) y se hunde un poco para que flote. Se hornea en mallas sueltas.
r("const moto=mkMoto(true);moto.visible=false;scene.add(moto);",r"""function mkLanchaM(piloto,estela){const g=new THREE.Group(),R=new THREE.Group();
 const C=(c,mt,ro)=>new THREE.MeshStandardMaterial({color:c,metalness:mt,roughness:ro,flatShading:true});
 const mB=C(0xf8f8f8,.05,.5),mAO=C(0x1e3a6e,.1,.45),mAM=C(0x2d4a8a,.1,.45),mGC=C(0xb8b8b8,.1,.55),mG=C(0x909090,.15,.5),mGO=C(0x5a5a5a,.2,.45),mN=C(0x2c2c2c,.3,.4),mNM=C(0x1c1c1c,.05,.75),mCr=new THREE.MeshStandardMaterial({color:0xd0e0f0,metalness:.15,roughness:.1,transparent:true,opacity:.6}),mPl=C(0xe0e0e0,.55,.3);
 const LARGO=4.5,ANCHO=1.7,AB=.28;
 const box=(w,h,d,mat,x,y,z,rx=0,ry=0,par=R)=>{const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);m.rotation.set(rx,ry,0);par.add(m);return m};
 // casco azul
 box(ANCHO*.95,.28,LARGO*.65,mAO,0,AB-.02,-.15);box(ANCHO*.5,.32,LARGO*.38,mAO,0,AB+.04,LARGO*.32,-.18);box(ANCHO*.85,.26,LARGO*.22,mAO,0,AB-.01,-LARGO*.38);
 // cubierta blanca
 box(ANCHO*.88,.16,LARGO*.62,mB,0,AB+.22,-.05);box(ANCHO*.48,.14,LARGO*.32,mB,0,AB+.28,LARGO*.28,-.1);
 for(const sx of[-1,1]){box(.07,.12,LARGO*.55,mAO,sx*ANCHO*.44,AB+.18,.05);box(.07,.09,LARGO*.58,mB,sx*ANCHO*.42,AB+.32,0);
  // asientos
  const x=sx*.28;box(.38,.1,.42,mG,x,AB+.28+.05,.05);box(.36,.42,.09,mGC,x,AB+.28+.3,.05-.16,-.08);
  // parabrisas: marco y cristal lateral
  box(.035,.48,.08,mN,sx*.42,AB+.52,LARGO*.16,0,sx*.12);box(.04,.32,.35,mCr,sx*.38,AB+.5,LARGO*.12,0,sx*.2)}
 box(.78,.4,.035,mCr,0,AB+.55,LARGO*.2,-.28);
 {const m=new THREE.Mesh(new THREE.CylinderGeometry(.02,.028,.65,6),mPl);m.position.set(-.32,AB+.55,LARGO*.3);R.add(m)}
 box(.1,.07,.1,mAO,-.32,AB+.25,LARGO*.3);box(.08,.05,.07,mAM,-.12,AB+.26,LARGO*.26);
 // motor fueraborda
 {const M=new THREE.Group();box(.5,.62,.55,mN,0,.35,0,0,0,M);box(.56,.32,.48,mGO,0,.72,0,0,0,M);box(.32,.38,.4,mNM,0,.02,-.04,0,0,M);
  const h=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,.035,5),mG);h.rotation.x=Math.PI/2;h.position.set(0,-.08,-.1);M.add(h);M.position.set(0,AB+.32,-LARGO*.4);R.add(M)}
 box(.18,.1,.22,mGO,0,AB+.22,-LARGO*.32);box(ANCHO*.4,.05,.1,mAO,0,AB+.34,LARGO*.4);box(.22,.1,.15,mGO,0,AB+.3,LARGO*.08);
 const AC=AB+.2;// altura de asiento para el patrón
 if(piloto){// patrón sentado en el asiento de babor
  const PI_=new THREE.MeshStandardMaterial({color:0xe0b38f,roughness:.7}),CA=new THREE.MeshStandardMaterial({color:0xd8402e,roughness:.7}),PA=new THREE.MeshStandardMaterial({color:0x2b3142,roughness:.8});
  box(.34,.5,.24,CA,-.28,AC+.5,0);box(.32,.14,.46,PA,-.28,AC+.22,.2);{const m=new THREE.Mesh(new THREE.SphereGeometry(.12,10,8),PI_);m.position.set(-.28,AC+.88,.02);R.add(m)}
  box(.1,.1,.4,CA,-.16,AC+.56,.28,-.4)}
 R.scale.setScalar(.2/LARGO);R.rotation.y=Math.PI/2;R.position.y=-.0035;R.updateMatrixWorld(true);
 R.traverse(m=>{if(!m.isMesh)return;const q=new THREE.Mesh(m.geometry.clone().applyMatrix4(m.matrixWorld),m.material);q.castShadow=true;g.add(q)});
 if(estela){const est=new THREE.Mesh(new THREE.PlaneGeometry(.3,.12),new THREE.MeshBasicMaterial({map:ESTELA_TEX,transparent:true,depthWrite:false,opacity:.7}));est.rotation.x=-Math.PI/2;est.position.set(-.25,-.016,0);g.add(est);g.userData.est=est}
 g.userData.lancha=1;return g}
const moto=mkMoto(true);moto.visible=false;scene.add(moto);
// la moto de agua del jugador puede vestirse de lancha: se ocultan sus piezas y se enseña la lancha con su patrón
const MOTO_ORIG=[...moto.children],LANCHA_J=mkLanchaM(true,false);LANCHA_J.visible=false;moto.add(LANCHA_J);
function vestirMoto(l){P.lancha=!!l;for(const c of MOTO_ORIG)c.visible=!l;LANCHA_J.visible=!!l}window.__vestirMoto=vestirMoto;""")
# amarres: una de cada dos motos de agua aparcadas es una lancha
r("   const g=mkMoto(false);g.visible=false;scene.add(g);APARC.push({tipo:'moto',g,x:best[0],y:best[1],a})}}",
  "   const ln=(APARC.filter(q=>q.tipo==='moto').length%2)===1;const g=ln?mkLanchaM(false,false):mkMoto(false);g.visible=false;scene.add(g);APARC.push({tipo:'moto',g,x:best[0],y:best[1],a,lancha:ln})}}")
r("txt:v.tipo==='moto'?'Subir a la moto de agua'","txt:v.tipo==='moto'?(v.lancha?'Subir a la lancha':'Subir a la moto de agua')")
r("  Object.assign(P,{x:v.x,y:v.y,a:v.a,v:0});if(v.tipo==='heli'){P.z=v.z;P.vz=0;HELI.posado=true}cambiarModo(v.tipo);return}}",
  "  if(v.tipo==='moto'){vestirMoto(v.lancha);if(v.lancha)mostrar('¡A bordo de la lancha!')}Object.assign(P,{x:v.x,y:v.y,a:v.a,v:0});if(v.tipo==='heli'){P.z=v.z;P.vz=0;HELI.posado=true}cambiarModo(v.tipo);return}}")
r("  const g=mkMoto(false);scene.add(g);g.position.copy(moto.position);g.rotation.y=P.a;APARC.push({tipo:'moto',g,x:P.x,y:P.y,a:P.a});",
  "  const ln=!!P.lancha;const g=ln?mkLanchaM(false,false):mkMoto(false);scene.add(g);g.position.copy(moto.position);g.rotation.y=P.a;APARC.push({tipo:'moto',g,x:P.x,y:P.y,a:P.a,lancha:ln});vestirMoto(false);")
r("   if(v){APARC.splice(APARC.indexOf(v),1);scene.remove(v.g);Object.assign(P,{x:v.x,y:v.y,a:v.a,v:0});cambiarModo('moto')}",
  "   if(v){APARC.splice(APARC.indexOf(v),1);scene.remove(v.g);vestirMoto(v.lancha);Object.assign(P,{x:v.x,y:v.y,a:v.a,v:0});cambiarModo('moto')}")
# el reparto de Navidad en moto de agua siempre con la moto
r("function motoNavPon(extra){motoNavQuita();","function motoNavPon(extra){motoNavQuita();vestirMoto(false);")
# lanchas navegando por la ría (como los veleros, sin velas)
r(" const BT=RIA.bateasL||[];const CL=[0xd8572a,0x2b5fa8,0x2f8a4e,0xe0e0dc];",
  r""" for(let i=0;i<(window.LITE?3:8);i++){const z=zonas[(i*3+1)%zonas.length];let x=0,y=0,ok=false;for(let k=0;k<80&&!ok;k++){x=z[0]+(Math.random()*2-1)*z[2];y=z[1]+(Math.random()*2-1)*z[2];ok=aguaLibre(x,y,.3)}if(!ok)continue;
  const g=mkLanchaM(true,true);g.scale.setScalar(1.3);g.visible=false;scene.add(g);const b={k:'motora',g,x,y,a:Math.random()*6.28,v:.3+Math.random()*.12,marg:.3,cx:z[0],cy:z[1],R:z[2],tx:x,ty:y,ph:Math.random()*6};velaDestino(b,b.cx,b.cy,b.R);VELAS.lista.push(b)}
 const BT=RIA.bateasL||[];const CL=[0xd8572a,0x2b5fa8,0x2f8a4e,0xe0e0dc];""")
r("if(d<.3){if(b.k==='vela'){if(!velaDestino(b,b.cx,b.cy,b.R))velaDestino(b,b.x,b.y,4)}","if(d<.3){if(b.k!=='lancha'){if(!velaDestino(b,b.cx,b.cy,b.R))velaDestino(b,b.x,b.y,4)}")
r("else{b.a+=1.2*dt;if(b.k==='vela')velaDestino(b,b.x,b.y,4)}","else{b.a+=1.2*dt;if(b.k!=='lancha')velaDestino(b,b.x,b.y,4)}")
r("else{b.g.rotation.x=Math.sin(t*1.4+b.ph)*.025;b.g.userData.est.material.opacity=b.espera>0?0:.7}","else{b.g.rotation.x=Math.sin(t*1.4+b.ph)*.025;if(b.k==='motora')b.g.rotation.z=.04;b.g.userData.est.material.opacity=b.espera>0?0:.7}")
open(f,'w').write(s)
print('ok lancha')
