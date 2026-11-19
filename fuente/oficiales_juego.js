// ---------- vehículos oficiales en el juego: los mismos modelos de la pantalla de inicio (oficiales.js), a la escala del juego
// El modelo elegido en el menú (0, 1 o 2 de cada tipo) se guarda en localStorage 'gtvigo_modelos'; el menú avisa con GTV_ponModelo(tipo,i)
const OFJ=(()=>{
 const std=(o)=>new THREE.MeshStandardMaterial(o);
 const T=(rol,c,o={})=>{switch(rol){
  case 'pintura':return pintura(c);
  case 'cristal':{const m=std({color:0x1b2233,roughness:.06,metalness:.3,envMapIntensity:1.3});REFLEJAN.add(m);return m}
  case 'cromo':{const m=std({color:0xd8dbe0,roughness:.18,metalness:.9});REFLEJAN.add(m);return m}
  case 'negro':return std({color:0x1a1a22,roughness:o.roughness>.5?.85:.45,metalness:o.roughness>.5?0:.3});
  case 'faro':{const m=std({color:0xfff6dc,roughness:.2,emissive:0xfff2c0,emissiveIntensity:.4});m.userData.faro='f';FAROMATS.add(m);return m}
  case 'piloto':{const m=std({color:0xc83a2a,roughness:.3,emissive:0xff2a1a,emissiveIntensity:.2});m.userData.faro='p';FAROMATS.add(m);return m}
  case 'luz':return std({color:c,emissive:o.emissive,emissiveIntensity:1.6});
  default:return std({color:c,roughness:o.roughness??.45,metalness:Math.min(.6,o.metalness??.2),transparent:!!o.transparent,opacity:o.opacity??1})}};
 const F=window.GTV_OF(THREE,T);
 // coche y moto: piezas sueltas (vestirCoche solo copia mallas) con la escala ya aplicada; el grupo va a .6 como el coche del juego
 const plano=(g,f,dy,sombra,haz)=>{g.updateMatrixWorld(true);const out=new THREE.Group(),S=new THREE.Matrix4().makeScale(f,f,f).premultiply(new THREE.Matrix4().makeTranslation(0,dy,0));
  g.traverse(o=>{if(!o.isMesh)return;const geo=o.geometry.clone().applyMatrix4(new THREE.Matrix4().multiplyMatrices(S,o.matrixWorld));
   const m=new THREE.Mesh(geo,o.material);m.name=o.name;m.castShadow=true;out.add(m)});
  out.add(manchaSombra(...sombra));if(haz)out.add(haz);out.scale.setScalar(.6);return out};
 const coche=(i=0)=>{const h=hazFaros(.085);h.scale.set(1.6,1,1.6);const g=plano(F.coche(i),.038,0,[i===1?.1:.09,.18],h);g.userData.tipo='oficial'+i;return g};
 const moto=(i=0)=>{const h=hazFaros(.08);h.scale.set(1.3,1,.9);const g=plano(F.moto(i,{piloto:true}),.07,.0007,[.045,.16],h);g.userData.tipo='moto';return g};
 // helicóptero: misma escala que el del juego (rotor de unas .28), patines en el suelo y el rotor en el centro de giro
 const heli=(i=0)=>{const b=F.heli(i),f=.06,g=new THREE.Group(),dx=-.35*f,dy=-.23*f;
  for(const o of [...b.children]){o.position.multiplyScalar(f);o.position.x+=dx;o.position.y+=dy;o.scale.multiplyScalar(f);o.traverse(q=>{if(q.isMesh)q.castShadow=true});g.add(o)}
  g.userData={rotor:b.userData.rot,rcola:b.userData.tr,oficial:true};return g};
 return{coche,moto,heli,nHeli:0}})();
const OF_SEL={coche:0,moto:0,heli:0};
try{const v=JSON.parse(localStorage.getItem('gtvigo_modelos')||'{}');for(const k in OF_SEL)if([0,1,2].includes(v[k]))OF_SEL[k]=v[k]}catch(e){}
let CAR_OF=OFJ.coche(OF_SEL.coche),MOTO_OF=OFJ.moto(OF_SEL.moto);
// el menú cambia de modelo: el próximo coche/moto sale con él y el helicóptero se rehace ya (en el menú no se está volando)
window.GTV_ponModelo=(k,i)=>{if(OF_SEL[k]===i)return;OF_SEL[k]=i;
 if(k==='coche')CAR_OF=OFJ.coche(i);
 else if(k==='moto')MOTO_OF=OFJ.moto(i);
 else if(k==='heli'){const n=OFJ.heli(i),u=heli.userData;heli.clear();for(const o of [...n.children])heli.add(o);u.rotor=n.userData.rotor;u.rcola=n.userData.rcola;u.oficial=true}};
// fin vehiculos oficiales
