f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= LANCHA CON MOTOR FUERABORDA (modelo aportado por el usuario: lancha_con_motor.js) =================
# Se construye a escala real (4.5 m a lo largo de +Z), se gira para que la proa mire a +X, se escala a ~0.2 de largo
# (como la moto de agua) y se hunde un poco para que flote. Se hornea en mallas sueltas.
r("const moto=mkMoto(true);moto.visible=false;scene.add(moto);",r"""function mkLanchaM(piloto,estela){const g=new THREE.Group(),R=new THREE.Group();
 const mat=(c,x={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.82,metalness:.04,flatShading:true},x));
 const M={casco:mat(0xe8e9e8,{side:THREE.DoubleSide}),cubierta:mat(0xf3f3f0),sombra:mat(0xbfc4c8),navy:mat(0x172b4d),navyClaro:mat(0x263e63),cristal:mat(0x687681,{transparent:true,opacity:.48,roughness:.22,side:THREE.DoubleSide}),
  borde:mat(0x252d38),asiento:mat(0x858d94),asientoLuz:mat(0xaab0b4),metal:mat(0x555d66,{metalness:.55}),motor:mat(0x1d3155),negro:mat(0x15191f),blanco:mat(0xffffff)};
 const LARGO=4.5,O=new THREE.Group();O.position.z=.135;R.add(O);
 const mesh=(geo,m,x,y,z,rx=0,ry=0,rz=0,par=O)=>{const q=new THREE.Mesh(geo,m);q.position.set(x,y,z);q.rotation.set(rx,ry,rz);par.add(q);return q},B=(w,h,d)=>new THREE.BoxGeometry(w,h,d),Cy=(a,b,h,n)=>new THREE.CylinderGeometry(a,b,h,n);
 // casco en V por estaciones [z, semiancho, borda, pantoque, quilla]
 {const E=[[-2.18,.48,.78,.37,.13],[-1.72,.77,.82,.32,.10],[-.95,.84,.83,.25,.08],[0,.82,.85,.24,.08],[.92,.68,.91,.34,.11],[1.62,.43,1,.48,.19],[2.18,.08,1.08,.76,.55]];
  const V=[],I=[];for(const[z,w,top,ch,k]of E)V.push(-w,top,z,-w*.78,ch,z,0,k,z,w*.78,ch,z,w,top,z);
  for(let i=0;i<E.length-1;i++)for(let j=0;j<4;j++){const a_=i*5+j,b_=a_+1,c_=(i+1)*5+j,d_=c_+1;I.push(a_,c_,b_,b_,c_,d_)}
  I.push(0,1,2,0,2,4,2,3,4);// espejo de popa
  const g_=new THREE.BufferGeometry();g_.setAttribute('position',new THREE.Float32BufferAttribute(V,3));g_.setIndex(I);g_.computeVertexNormals();O.add(new THREE.Mesh(g_,M.casco));
  mesh(B(1.48,.16,3.35),M.navy,0,.105,-.35)}
 // cubierta
 mesh(B(1.48,.1,3.62),M.cubierta,0,.79,-.12);
 for(const l of[-1,1]){mesh(B(.105,.16,3.48),M.cubierta,l*.75,.84,-.18,0,0,l*-.035);mesh(B(.035,.055,3.3),M.navy,l*.79,.735,-.2);mesh(B(.1,.12,.34),M.sombra,l*.69,.91,-1.45)}
 mesh(B(.72,.055,.82),M.cubierta,0,.85,1.53);mesh(B(.54,.045,.32),M.navy,0,.89,1.55);mesh(B(1.1,.045,1.05),M.navy,0,.87,-.63);
 // asientos
 for(const[x,z,ry]of[[-.28,-.72,0],[.3,-.13,Math.PI]]){const S_=new THREE.Group();S_.position.set(x,0,z);S_.rotation.y=ry;O.add(S_);mesh(B(.53,.13,.48),M.asiento,0,.98,0,0,0,0,S_);mesh(B(.53,.52,.14),M.asientoLuz,0,1.27,-.17,-.1,0,0,S_);mesh(B(.12,.22,.12),M.metal,0,.84,0,0,0,0,S_)}
 // consola
 mesh(B(.58,.24,.3),M.navyClaro,-.38,1,.28,-.12);mesh(B(.25,.12,.025),M.negro,-.38,1.13,.31);mesh(new THREE.TorusGeometry(.105,.018,5,8),M.metal,-.38,1.12,.08,Math.PI/2);
 // parabrisas de tres paneles
 for(const p of[{x:-.43,w:.43,z:.69},{x:0,w:.43,z:.73},{x:.43,w:.43,z:.69}]){mesh(B(p.w,.48,.018),M.cristal,p.x,1.34,p.z+.02,-.5);mesh(B(p.w+.035,.055,.075),M.borde,p.x,1.13,p.z,-.5)}
 for(const x of[-.66,-.22,.22,.66])mesh(B(.035,.5,.045),M.borde,x,1.34,.72,-.5);
 // motor fueraborda
 mesh(B(.48,.25,.18),M.negro,0,.78,-2.17);mesh(B(.13,.56,.13),M.metal,0,.49,-2.28);mesh(Cy(.24,.3,.57,6),M.motor,0,1.02,-2.31);mesh(B(.4,.1,.35),M.navyClaro,0,1.32,-2.31);
 mesh(Cy(.055,.055,.18,6),M.metal,0,.2,-2.36,Math.PI/2);mesh(B(.06,.34,.035),M.metal,0,.2,-2.45,0,0,.45);mesh(B(.06,.34,.035),M.metal,0,.2,-2.45,0,0,-.45);
 // antena
 mesh(Cy(.07,.09,.1,6),M.blanco,.48,.94,-1.48);mesh(Cy(.012,.018,1.02,5),M.metal,.48,1.49,-1.48,0,0,-.06);mesh(Cy(.018,.018,.09,5),M.negro,.42,2.03,-1.48);
 if(piloto){// patrón sentado en el puesto de mando, con las manos al volante
  const PI_=new THREE.MeshStandardMaterial({color:0xe0b38f,roughness:.7}),CA=new THREE.MeshStandardMaterial({color:0xd8402e,roughness:.7}),PA=new THREE.MeshStandardMaterial({color:0x2b3142,roughness:.8});
  mesh(B(.36,.5,.24),CA,-.28,1.3,-.72);mesh(B(.32,.14,.46),PA,-.28,1.1,-.5);mesh(new THREE.SphereGeometry(.12,10,8),PI_,-.28,1.68,-.7);
  for(const dx of[-.1,.1])mesh(B(.08,.08,.5),CA,-.28+dx,1.32,-.42,-.3)}
 R.scale.setScalar(.2/LARGO);R.rotation.y=Math.PI/2;R.position.y=-.021;R.updateMatrixWorld(true);
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
