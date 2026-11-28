// ---------- vista interior del coche (edit_cabina.py): cámara en el asiento del conductor con salpicadero, volante, cuadro y retrovisores
// La cabina se modela en metros alrededor del ojo del conductor y se dibuja ampliada (CAB.K) para no chocar con el plano cercano de la cámara;
// va sin prueba de profundidad y en orden de pintor (renderOrder), así la ciudad nunca la tapa. Los retrovisores muestran la calle de atrás
// (una cámara pequeña que mira hacia atrás, cada 3 imágenes; en el móvil LITE un degradado quieto). Con window.__CAB_ESPEJO_OFF=true se apagan.
const CAB={g:null,on:false,K:3,UPM:.02,q:new THREE.Quaternion(),qi:false,st:0,ocultos:new Set(),cl:null,pa:null,tc:0,tp:0,col:-1,
 rt:null,mcam:null,mf:0,rueda:null,capo:null,espejos:[],bob:0};window.__CAB=CAB;
function cabOK(){return MODO==='coche'&&car.userData.tipo!=='moto'&&!(REP&&REP.on)&&!(RACE&&RACE.on&&RACE.nav)&&!window.__CAB_OFF}
function cabCanvas(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=4;return{c,g:c.getContext('2d'),t}}
function cabCrear(){
 const g=new THREE.Group();g.name='cabina';let ord=1000;
 const M=(c,r=.85,m=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r,metalness:m,depthTest:false,depthWrite:true});
 const add=(geo,mat,ro,p,par=g)=>{const m=new THREE.Mesh(geo,mat);m.renderOrder=ro;m.frustumCulled=false;m.castShadow=m.receiveShadow=false;if(p)m.position.set(...p);par.add(m);return m};
 const caja=(w,h,d,mat,ro,p)=>add(new THREE.BoxGeometry(w,h,d),mat,ro,p);
 // pieza recta entre dos puntos (pilares)
 const barra=(a,b,w,d,mat,ro)=>{const A=new THREE.Vector3(...a),B=new THREE.Vector3(...b),L=A.distanceTo(B);const m=caja(w,L,d,mat,ro);m.position.copy(A).add(B).multiplyScalar(.5);m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),B.clone().sub(A).normalize());return m};
 const NEG=M(0x2a2421),NEG2=M(0x141211,.7),CUERO=M(0x6a3a24,.65),PESP=M(0xc9a27a,.6),CROMO=M(0xb9bcc2,.25,.9),TECHO=M(0x3b3734,.95),GOMA=M(0x0d0c0c,.9);
 // capó (pintura del coche, se cambia sola si cambia el color)
 {const geo=new THREE.PlaneGeometry(1.46,1.6,16,10);geo.rotateX(-Math.PI/2);const p=geo.attributes.position;
  for(let i=0;i<p.count;i++){const x=p.getX(i),z=p.getZ(i),t=(.8-z)/1.6,xn=x/.73;p.setX(i,.37+x*(1-.16*t));p.setZ(i,-1.05-(.8-z)+0*t);p.setY(i,-.315-.1*t-.07*xn*xn*(1-.3*t)+.02*Math.sin(Math.PI*Math.min(1,t*1.2)))}
  geo.computeVertexNormals();CAB.capo=add(geo,M(0x6e1423,.3,.5),ord++)}
 // salpicadero: cuerpo, borde de cuero con pespunte, parte baja y rejilla del parabrisas
 caja(1.5,.36,.58,NEG,ord++,[.37,-.47,-.84]);
 caja(1.5,.03,.09,NEG2,ord++,[.37,-.282,-1.09]);
 caja(1.5,.07,.03,CUERO,ord++,[.37,-.335,-.548]);
 caja(1.5,.008,.032,PESP,ord++,[.37,-.317,-.546]);
 caja(1.5,.45,.32,NEG2,ord++,[.37,-.86,-.74]);
 // aireadores
 for(const x of [.24,.62]){caja(.13,.055,.02,CROMO,ord++,[x,-.385,-.545]);caja(.115,.042,.02,GOMA,ord++,[x,-.385,-.538])}
 // pilares A, techo y puertas
 barra([-.62,-.29,-1.06],[-.47,.29,-.55],.1,.07,TECHO,ord++);
 barra([1.36,-.29,-1.06],[1.21,.29,-.55],.1,.07,TECHO,ord++);
 caja(1.95,.06,.6,TECHO,ord++,[.37,.34,-.25]);
 caja(1.95,.07,.07,NEG,ord++,[.37,.295,-.56]);
 for(const [x,s] of [[-.68,1],[1.42,-1]]){caja(.06,.75,1.35,NEG,ord++,[x,-.68,-.35]);caja(.07,.035,1.35,NEG2,ord++,[x+.005*s,-.3,-.35]);caja(.02,.03,1.2,CUERO,ord++,[x+.035*s,-.36,-.35]);caja(.04,.12,.5,NEG2,ord++,[x+.03*s,-.5,-.2])}
 // cuadro de instrumentos bajo una visera
 CAB.cl=cabCanvas(512,192);
 {const vis=add(new THREE.CylinderGeometry(.22,.22,.16,20,1,true,-Math.PI/2,Math.PI),M(0x191715,.9),0,[0,-.32,-.72]);vis.rotation.x=-Math.PI/2;vis.scale.set(1,1,.42);
  const pan=add(new THREE.PlaneGeometry(.4,.15),new THREE.MeshBasicMaterial({map:CAB.cl.t,depthTest:false,depthWrite:true}),ord++,[0,-.345,-.71]);pan.lookAt(0,0,0);
  vis.renderOrder=ord++}
 // pantalla central (mapa y radio)
 CAB.pa=cabCanvas(512,320);
 {const b=caja(.33,.215,.02,GOMA,ord++,[.43,-.33,-.735]);b.lookAt(0,0,0);
  const pan=add(new THREE.PlaneGeometry(.31,.194),new THREE.MeshBasicMaterial({map:CAB.pa.t,depthTest:false,depthWrite:true}),ord++,[.428,-.329,-.728]);pan.lookAt(0,0,0)}
 // retrovisores: interior y exterior izquierdo (cristal con la imagen de atrás, espejada)
 const vy=!!R.isWebGPURenderer;   // en el motor nuevo la imagen de un render target llega boca abajo
 const vidrio=()=>{const geo=new THREE.PlaneGeometry(1,1);const uv=geo.attributes.uv;for(let i=0;i<uv.count;i++){uv.setX(i,1-uv.getX(i));if(vy)uv.setY(i,1-uv.getY(i))}return geo};
 CAB.espMat=new THREE.MeshBasicMaterial({color:0xdde3ea,depthTest:false,depthWrite:true});
 {barra([.34,.32,-.56],[.34,.2,-.6],.025,.025,NEG2,ord++);
  const f=caja(.25,.075,.03,NEG2,ord++,[.34,.17,-.62]);f.lookAt(0,0,0);
  const v=add(vidrio(),CAB.espMat,ord++,[.34,.17,-.605]);v.scale.set(.232,.06,1);v.lookAt(0,0,0)}
 {CAB.carcasa=M(0x6e1423,.35,.4);const c=add(new THREE.SphereGeometry(.12,14,10),CAB.carcasa,ord++,[-.96,-.15,-1.0]);c.scale.set(1,.62,.5);c.lookAt(0,0,0);
  const v=add(vidrio(),CAB.espMat,ord++,[-.95,-.15,-.96]);v.scale.set(.17,.095,1);v.lookAt(0,0,0)}
 // volante (gira con la dirección)
 {const col=add(new THREE.CylinderGeometry(.045,.06,.3,12),NEG2,ord++,[0,-.56,-.64]);col.rotation.x=-1.1;
  const w=new THREE.Group();w.position.set(0,-.45,-.5);w.rotation.x=-.42;g.add(w);const r=new THREE.Group();w.add(r);CAB.rueda=r;
  add(new THREE.TorusGeometry(.19,.024,10,40),M(0x1b1918,.6),ord++,null,r);
  add(new THREE.TorusGeometry(.19,.026,6,8,.32),M(0xb02a22,.5),ord++,null,r).rotation.z=Math.PI/2-.16;
  for(const a of [0,Math.PI,-Math.PI/2]){const s=add(new THREE.BoxGeometry(.17,.035,.02),M(0x262321,.55,.3),ord++,null,r);s.rotation.z=a;s.position.set(Math.cos(a)*.085,Math.sin(a)*.085,0)}
  add(new THREE.CylinderGeometry(.065,.07,.04,20),M(0x232120,.5,.3),ord++,[0,0,.005],r).rotation.x=Math.PI/2;
  add(new THREE.CylinderGeometry(.022,.022,.01,16),CROMO,ord++,[0,0,.03],r).rotation.x=Math.PI/2}
 // brazos y manos del conductor: las manos van agarradas al aro (giran con él); los antebrazos se recolocan en cada imagen
 {const PIEL=M(0xd9a184,.6),MANGA=M(0xb8222a,.85),PUNO=M(0x8e1a20,.85);CAB.brazos=[];
  for(const lado of [-1,1]){const piel=add(new THREE.CylinderGeometry(.026,.03,1,10),PIEL,ord++),manga=add(new THREE.CylinderGeometry(.046,.052,1,12),MANGA,ord++),puno=add(new THREE.CylinderGeometry(.05,.05,.03,12),PUNO,ord++);
   CAB.brazos.push({lado,piel,manga,puno,codo:new THREE.Vector3(.34*lado,-.82,-.16)})}
  // mano en ejes del aro: x hacia fuera del volante, y a lo largo del aro, z hacia el conductor; los dedos rodean el aro
  const dedo=(R,ang)=>{const q=new THREE.TorusGeometry(R,.0115,6,12,ang);q.rotateZ(-Math.PI/5);q.rotateX(Math.PI/2);return q};
  for(const b of CAB.brazos){const lado=b.lado,an=lado>0?Math.PI/5:Math.PI-Math.PI/5,h=new THREE.Group();h.position.set(.19*Math.cos(an),.19*Math.sin(an),0);h.rotation.z=an;CAB.rueda.add(h);b.mano=h;
   b.dorso=add(new THREE.BoxGeometry(.082,.09,.028),PIEL,ord++);
   [.03,.01,-.01,-.029].forEach((y,k)=>add(dedo(k===3?.033:.036,Math.PI*1.3),PIEL,ord++,[0,y,0],h));
   const pu=add(new THREE.CapsuleGeometry(.012,.035,3,8),PIEL,ord++,[-.028,.04*lado,.03],h);pu.rotation.z=.4*lado;
   b.nud=new THREE.Vector3(0,0,.03)}}
 CAB.mCuero=CUERO;CAB.mPesp=PESP;CAB.cueroBase=CUERO.color.getHex();CAB.pespBase=PESP.color.getHex();
 g.traverse(o=>{if(o.isMesh)o.layers.set(5)});g.visible=false;scene.add(g);pcam.layers.enable(5);CAB.g=g}
// color del coche para el capó y la carcasa del retrovisor
function cabColor(){const ria=car.children.some(c=>c.userData&&c.userData.oficial==='coche0');CAB.mCuero.color.setHex(ria?0xc93d18:CAB.cueroBase);CAB.mPesp.color.setHex(ria?0xff8a5a:CAB.pespBase);
 let c=null,best=0;const bx=new THREE.Box3(),v=new THREE.Vector3();car.traverse(o=>{if(o.isMesh&&o.material&&o.material.userData&&o.material.userData.pintura){if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();bx.copy(o.geometry.boundingBox).getSize(v);const a=v.x*v.y+v.y*v.z+v.x*v.z;if(a>best){best=a;c=o.material}}});
 if(!c&&car.userData.body)c=car.userData.body;if(!c)return;const h=c.color.getHex();if(h===CAB.col)return;CAB.col=h;
 CAB.carcasa.color.setHex(h);const m=c.clone();m.depthTest=false;m.depthWrite=true;m.userData={pintura:1};try{REFLEJAN.add(m)}catch(e){}const old=CAB.capo.material;CAB.capo.material=m;if(old&&old!==m){try{REFLEJAN.delete(old)}catch(e){}old.dispose()}}
// esconde las piezas opacas del coche (las luces y la mancha de sombra se quedan)
function cabEsconder(){car.traverse(o=>{if(o.isMesh&&o.visible&&o.name!=='haz'&&o.name!=='sombra'){o.visible=false;CAB.ocultos.add(o)}})}
// medidas del coche en sus propios ejes (para sentar al conductor en cualquier modelo): caja de las piezas, sin sombra ni haz
function cabMedidas(){const k=car.children.length+':'+(car.children[0]?car.children[0].uuid:'');if(CAB.mk===k)return CAB.med;
 car.updateMatrixWorld(true);const inv=car.matrixWorld.clone().invert(),b=new THREE.Box3(),t=new THREE.Box3(),m=new THREE.Matrix4();
 for(const c of car.children){if(!c.isMesh||c.name==='sombra'||c.name==='haz')continue;if(!c.geometry.boundingBox)c.geometry.computeBoundingBox();t.copy(c.geometry.boundingBox).applyMatrix4(m.multiplyMatrices(inv,c.matrixWorld));b.union(t)}
 if(b.isEmpty())b.set(new THREE.Vector3(-.08,0,-.04),new THREE.Vector3(.08,.07,.04));CAB.mk=k;CAB.med=b;return b}
function cabOff(){if(!CAB.on)return;CAB.on=false;if(CAB.g)CAB.g.visible=false;for(const o of CAB.ocultos)o.visible=true;CAB.ocultos.clear();camInit=false;window.CD=undefined;CAB.qi=false}
window.cabOff=cabOff;
function cabCuadro(kmh){const {g}=CAB.cl,W=512,H=192;g.clearRect(0,0,W,H);
 const bg=g.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#070a10');bg.addColorStop(1,'#10151e');g.fillStyle=bg;g.fillRect(0,0,W,H);
 const reloj=(cx,v,max,paso,txt)=>{const r=78,a0=Math.PI*.75,a1=Math.PI*2.25;g.lineWidth=3;g.strokeStyle='#2b3850';g.beginPath();g.arc(cx,96,r,a0,a1);g.stroke();
  g.strokeStyle='#5ad0ff';g.lineWidth=4;g.beginPath();g.arc(cx,96,r,a0,a0+(a1-a0)*Math.min(1,v/max));g.stroke();
  g.fillStyle='#9fb3cf';g.font='600 11px system-ui,sans-serif';g.textAlign='center';g.textBaseline='middle';
  for(let k=0;k<=max;k+=paso){const a=a0+(a1-a0)*k/max;g.fillRect(0,0,0,0);g.save();g.translate(cx+Math.cos(a)*(r-6),96+Math.sin(a)*(r-6));g.rotate(a+Math.PI/2);g.fillStyle='#cfe0f5';g.fillRect(-1,-4,2,8);g.restore();
   g.fillText(txt(k),cx+Math.cos(a)*(r-20),96+Math.sin(a)*(r-20))}
  const a=a0+(a1-a0)*Math.min(1,v/max);g.strokeStyle='#ff4030';g.lineWidth=3;g.beginPath();g.moveTo(cx,96);g.lineTo(cx+Math.cos(a)*(r-10),96+Math.sin(a)*(r-10));g.stroke();
  g.fillStyle='#222';g.beginPath();g.arc(cx,96,7,0,7);g.fill()};
 const marcha=kmh<1?1:Math.min(6,1+Math.floor(kmh/32)),rpm=kmh<1?.8:1.4+((kmh%32)/32)*4.2+marcha*.15;
 reloj(100,kmh,240,40,k=>k);reloj(412,rpm,8,1,k=>k);
 g.textAlign='center';g.textBaseline='middle';g.fillStyle='#fff';g.font='700 54px system-ui,sans-serif';g.fillText(Math.round(kmh),256,86);
 g.fillStyle='#8fa3bd';g.font='600 14px system-ui,sans-serif';g.fillText('km/h',256,122);
 g.fillStyle=P.v<-.01?'#ffb020':'#5ad0ff';g.font='700 22px system-ui,sans-serif';g.fillText(P.v<-.01?'R':kmh<1?'N':'D'+marcha,256,30);
 g.fillStyle='#6f819a';g.font='500 12px system-ui,sans-serif';g.fillText('GT VIGO',256,160);CAB.cl.t.needsUpdate=true}
function cabPantalla(){const {g}=CAB.pa,W=512,H=320;g.fillStyle='#0b0f16';g.fillRect(0,0,W,H);
 const mi=document.getElementById('mini');g.save();g.beginPath();g.roundRect?g.roundRect(10,10,300,300,14):g.rect(10,10,300,300);g.clip();g.fillStyle='#2b5a3a';g.fillRect(10,10,300,300);
 try{if(mi&&mi.width)g.drawImage(mi,mi.width*.12,mi.height*.12,mi.width*.76,mi.height*.76,10,10,300,300)}catch(e){}g.restore();
 g.fillStyle='rgba(10,14,20,.78)';g.fillRect(10,10,300,40);g.fillStyle='#fff';g.font='600 17px system-ui,sans-serif';g.textAlign='left';g.textBaseline='middle';
 let calle='';try{calle=calleAct||''}catch(e){}g.fillText(calle?('📍 '+calle).slice(0,30):'📍 Vigo',22,30);
 g.fillStyle='#fff';g.beginPath();g.moveTo(160,148);g.lineTo(148,178);g.lineTo(160,170);g.lineTo(172,178);g.closePath();g.fill();
 // derecha: hora del juego y radio
 let h=12;try{h=CIELO.h}catch(e){}const hh=Math.floor(((h%24)+24)%24),mm=Math.floor((h-Math.floor(h))*60);
 g.fillStyle='#e8eef7';g.font='600 30px system-ui,sans-serif';g.textAlign='center';g.fillText(String(hh).padStart(2,'0')+':'+String(mm).padStart(2,'0'),412,40);
 const gr=g.createLinearGradient(342,80,482,220);gr.addColorStop(0,'#f08a5d');gr.addColorStop(.5,'#b83b5e');gr.addColorStop(1,'#6a2c70');g.fillStyle=gr;g.fillRect(352,72,120,120);
 g.strokeStyle='rgba(255,255,255,.45)';g.lineWidth=2;g.beginPath();for(let x=0;x<=120;x+=4){const y=132+Math.sin(x*.12+performance.now()*.002)*12*Math.sin(x/120*Math.PI);x?g.lineTo(352+x,y):g.moveTo(352,y)}g.stroke();
 let em='📻 Radio',on=true;try{on=RADIO.on;em=(typeof EMISORAS!=='undefined'&&EMISORAS[RADIO.e||0])?EMISORAS[RADIO.e||0].nom:em}catch(e){}
 g.fillStyle='#fff';g.font='600 16px system-ui,sans-serif';g.fillText(on?em:'📻 Radio apagada',412,218);
 g.fillStyle='#8fa3bd';g.font='500 13px system-ui,sans-serif';g.fillText(on?'En directo':'M para encender',412,242);
 g.fillStyle='#cfd8e6';g.font='20px system-ui,sans-serif';g.fillText('⏮   ⏯   ⏭',412,285);CAB.pa.t.needsUpdate=true}
// imagen de los retrovisores: cámara pequeña mirando hacia atrás
function cabEspejo(eye,qCar){if(window.LITE||window.__CAB_ESPEJO_OFF){if(CAB.espMat.map){CAB.espMat.map=null;CAB.espMat.needsUpdate=true}CAB.espMat.color.setHex(0x8a9bb0);return}
 if(++CAB.mf%3)return;
 try{if(!CAB.rt){CAB.rt=new THREE.WebGLRenderTarget(320,96,{type:THREE.HalfFloatType});CAB.rt.texture.generateMipmaps=false;CAB.mcam=new THREE.PerspectiveCamera(34,320/96,.004,10);CAB.espMat.map=CAB.rt.texture;CAB.espMat.color.setHex(0xffffff);CAB.espMat.needsUpdate=true}
  const mc=CAB.mcam;mc.position.copy(eye).addScaledVector(new THREE.Vector3(0,1,0),.006);mc.quaternion.copy(qCar).multiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0),Math.PI/2)).multiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1,0,0),.02));
  mc.translateZ(-.04);mc.updateMatrixWorld();
  const sh=R.shadowMap,au=sh.autoUpdate,prev=R.getRenderTarget(),cc=R.getClearColor(new THREE.Color()),ca=R.getClearAlpha();
  try{sh.autoUpdate=false;R.setClearColor(FOG.color,1);R.setRenderTarget(CAB.rt);R.clear();R.render(scene,mc)}
  finally{sh.autoUpdate=au;R.setClearColor(cc,ca);R.setRenderTarget(prev)}}
 catch(e){console.warn('retrovisor',e);window.__CAB_ESPEJO_OFF=true}}
// cámara en el asiento: se llama en lugar de la cámara de persecución
function cabCam(dt,gy){if(!CAB.g)cabCrear();
 if(!CAB.on){CAB.on=true;CAB.g.visible=true;CAB.col=-1}
 cabEsconder();if((CAB.tc-=dt)<=0){CAB.tc=1;cabColor()}
 const qCar=car.getWorldQuaternion(new THREE.Quaternion());if(!CAB.qi){CAB.q.copy(qCar);CAB.qi=true}else CAB.q.slerp(qCar,Math.min(1,dt*12));
 const v=Math.abs(P.v);CAB.bob+=dt*(6+v*10);
 const B=cabMedidas(),L=B.max.x-B.min.x,H=B.max.y-B.min.y,cz=(B.min.z+B.max.z)/2,hw=(B.max.z-B.min.z)/2;
 car.updateMatrixWorld(true);const a0=car.localToWorld(new THREE.Vector3(B.min.x,0,0)),a1=car.localToWorld(new THREE.Vector3(B.max.x,0,0));
 const S=a0.distanceTo(a1)/4.4;   // el coche mide unos 4,4 m: de ahí los metros del mundo
 const eye=car.localToWorld(new THREE.Vector3(B.min.x+.43*L,B.min.y+.8*H,cz-.42*hw));eye.y+=Math.sin(CAB.bob)*S*.006*Math.min(1,v*3);
 const cy=car.getWorldPosition(new THREE.Vector3()).y;if(cy<gy)eye.y+=gy-cy;
 // cabina: ejes del coche (−z hacia delante), ampliada K veces alrededor del ojo
 const qG=CAB.q.clone().multiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0),-Math.PI/2));
 CAB.g.position.copy(eye);CAB.g.quaternion.copy(qG);CAB.g.scale.setScalar(S*CAB.K);CAB.g.updateMatrixWorld(true);
 // la cabeza se inclina un poco hacia la curva
 let stIn=0;try{stIn=((keys.left?1:0)-(keys.right?1:0))*(typeof JOY!=='undefined'&&JOY.act?JOY.k:1)}catch(e){}CAB.st+=(stIn-CAB.st)*Math.min(1,dt*6);
 CAB.rueda.rotation.z=CAB.st*1.2;CAB.g.updateMatrixWorld(true);
 // dorso de la mano desde los nudillos hacia el codo, y luego muñeca, puño de la manga y antebrazo
 for(const b of CAB.brazos){const K=CAB.g.worldToLocal(b.mano.localToWorld(b.nud.clone())),Tg=CAB.g.worldToLocal(b.mano.localToWorld(new THREE.Vector3(0,1,.03))).sub(K);
  const d=b.codo.clone().sub(K).normalize(),xA=Tg.addScaledVector(d,-Tg.dot(d)).normalize(),zA=new THREE.Vector3().crossVectors(xA,d);
  b.dorso.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(xA,d,zA));b.dorso.position.copy(K).addScaledVector(d,.042);
  const w=K.clone().addScaledVector(d,.08),l=b.codo.distanceTo(w),q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),d);
  const pon=(m,a,c)=>{m.position.copy(w).addScaledVector(d,(a+c)/2);m.quaternion.copy(q);m.scale.set(1,c-a,1)};pon(b.piel,-.01,.07);pon(b.manga,.06,l);b.puno.position.copy(w).addScaledVector(d,.065);b.puno.quaternion.copy(q)}
 pcam.up.set(0,1,0);pcam.position.copy(eye);pcam.quaternion.copy(qG).multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(-.075,CAB.st*.06*Math.min(1,v*2),0,'YXZ')));
 const asp=cv.clientWidth/Math.max(1,cv.clientHeight);pcam.fov=Math.min(100,(asp<1?2*Math.atan(Math.tan(.68)/asp)*180/Math.PI:66)+5*Math.min(1,v));pcam.updateProjectionMatrix();camInit=false;
 const kmh=v*125;if((CAB.tp-=dt)<=0){CAB.tp=.09;cabCuadro(kmh);if((CAB.tq=(CAB.tq||0)+1)%3===0)cabPantalla()}
 cabEspejo(eye,CAB.q)}
