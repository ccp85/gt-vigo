// ===== Pantalla de inicio v2: coche, moto y helicóptero en 3D (renderer propio, solo mientras se ve el menú) =====
(async()=>{const SZ=document.getElementById('selz');
if(SZ&&SZ.classList.contains('v2')&&!window.SOLO_CARRERA){
const emojis=()=>{const E={coche:'🚗',moto:'🏍️',heli:'🚁'};SZ.querySelectorAll('.iCard').forEach(c=>{c.querySelector('.stage').textContent=E[c.dataset.v]})};
let THREE,RoomEnvironment;
try{THREE=await import('three');({RoomEnvironment}=await import('three/addons/environments/RoomEnvironment.js'))}catch(e){emojis();THREE=null}
if(THREE){
const visible=()=>!SZ.hidden&&SZ.getClientRects().length>0;
let rd=null,views=null,env=null,last=0,parado=true;
const cv=document.getElementById('iGl');
const M=(c,o={})=>new THREE.MeshStandardMaterial({color:c,metalness:.55,roughness:.3,...o});
const mesh=(g,m,x=0,y=0,z=0)=>{const o=new THREE.Mesh(g,m);o.position.set(x,y,z);return o};
const ext=(pts,depth,m,bev=.06)=>{const s=new THREE.Shape(pts.map(p=>new THREE.Vector2(p[0],p[1])));
 const g=new THREE.ExtrudeGeometry(s,{depth,bevelEnabled:bev>0,bevelThickness:bev,bevelSize:bev,bevelSegments:3,curveSegments:12});g.translate(0,0,-depth/2);return new THREE.Mesh(g,m)};
function mats(){return{glass:M(0x0b1020,{metalness:.9,roughness:.06}),black:M(0x111114,{metalness:.1,roughness:.75}),chrome:M(0xdfe3ea,{metalness:1,roughness:.12})}}
function coche(){
 const {glass,black,chrome}=mats(),g=new THREE.Group(),paint=M(0xff4a26,{metalness:.7,roughness:.22,envMapIntensity:1.4});
 g.add(ext([[-2.1,.38],[2.05,.38],[2.18,.62],[2.12,.82],[1.85,.95],[.9,1.02],[.3,1.42],[-.95,1.45],[-1.65,1.06],[-2.15,1.0]],1.62,paint,.09));
 g.add(ext([[.82,1.05],[.3,1.44],[-.92,1.47],[-1.55,1.08]],1.86,glass,0));
 const st=M(0x111114,{metalness:.4,roughness:.4});
 g.add(mesh(new THREE.BoxGeometry(.34,.05,1.9),st,-1.95,1.32,0));
 [-.6,.6].forEach(z=>g.add(mesh(new THREE.BoxGeometry(.08,.26,.06),st,-1.92,1.18,z)));
 [-.58,.58].forEach(z=>{g.add(mesh(new THREE.BoxGeometry(.06,.12,.42),M(0xffffff,{emissive:0xfff3d0,emissiveIntensity:2.5}),2.2,.74,z));
  g.add(mesh(new THREE.BoxGeometry(.06,.1,.5),M(0xff0010,{emissive:0xff1020,emissiveIntensity:2.5}),-2.2,.86,z))});
 g.add(mesh(new THREE.BoxGeometry(.1,.16,1.2),black,2.18,.5,0));
 const wheels=[];
 [[1.35,.82],[1.35,-.82],[-1.38,.82],[-1.38,-.82]].forEach(([x,z])=>{const w=new THREE.Group();w.position.set(x,.44,z);
  const t=mesh(new THREE.CylinderGeometry(.44,.44,.34,28),black);t.rotation.x=Math.PI/2;w.add(t);
  const r=mesh(new THREE.CylinderGeometry(.29,.29,.36,6),chrome);r.rotation.x=Math.PI/2;w.add(r);
  const h=mesh(new THREE.CylinderGeometry(.08,.08,.38,12),M(0xff5a36,{emissive:0x5a1000}));h.rotation.x=Math.PI/2;w.add(h);
  g.add(w);wheels.push(w)});
 g.userData.tick=(t,dt,on)=>{wheels.forEach(w=>w.rotation.z-=dt*(on?9:2.5));g.position.y=on?Math.sin(t*14)*.008:0};
 return g}
function moto(){
 const {black,chrome}=mats(),g=new THREE.Group(),paint=M(0x16c5e6,{metalness:.7,roughness:.22,envMapIntensity:1.4}),wheels=[];
 [.82,-.82].forEach(x=>{const w=new THREE.Group();w.position.set(x,.46,0);w.add(mesh(new THREE.TorusGeometry(.36,.11,14,32),black));
  const d=mesh(new THREE.CylinderGeometry(.27,.27,.06,7),chrome);d.rotation.x=Math.PI/2;w.add(d);g.add(w);wheels.push(w)});
 g.add(ext([[-.55,.62],[.42,.6],[.82,.98],[.72,1.22],[.42,1.2],[.1,1.08],[-.35,1.08],[-.8,1.2],[-1.0,1.1],[-.72,.78]],.34,paint,.06));
 g.add(mesh(new THREE.BoxGeometry(.62,.1,.32),black,-.38,1.17,0));
 g.add(mesh(new THREE.BoxGeometry(.5,.36,.3),M(0x2a2d36,{metalness:.8,roughness:.35}),-.05,.58,0));
 const f=mesh(new THREE.CylinderGeometry(.04,.04,1.0,10),chrome,.7,.88,0);f.rotation.z=.42;[-.12,.12].forEach(z=>{const c=f.clone();c.position.z=z;g.add(c)});
 const hb=mesh(new THREE.CylinderGeometry(.03,.03,.8,10),black,.54,1.32,0);hb.rotation.x=Math.PI/2;g.add(hb);
 const ws=mesh(new THREE.BoxGeometry(.04,.26,.3),M(0x3a5a70,{transparent:true,opacity:.6,metalness:.9,roughness:.05}),.72,1.34,0);ws.rotation.z=-.5;g.add(ws);
 g.add(mesh(new THREE.SphereGeometry(.09,16,12),M(0xffffff,{emissive:0xe8fbff,emissiveIntensity:3}),.86,1.1,0));
 const ex=mesh(new THREE.CylinderGeometry(.06,.08,.7,12),chrome,-.7,.62,.2);ex.rotation.z=1.35;g.add(ex);
 g.add(mesh(new THREE.BoxGeometry(.05,.06,.18),M(0xff0010,{emissive:0xff1020,emissiveIntensity:2.5}),-1.03,1.1,0));
 g.scale.setScalar(1.85);
 g.userData.tick=(t,dt,on)=>{wheels.forEach(w=>w.rotation.z-=dt*(on?12:3));g.rotation.x=on?Math.sin(t*1.6)*.14:0};
 return g}
function heli(){
 const {glass,chrome}=mats(),g=new THREE.Group(),paint=M(0xb8e62a,{metalness:.6,roughness:.25,envMapIntensity:1.4}),dk=M(0x1b1e26,{metalness:.6,roughness:.35});
 const b=mesh(new THREE.SphereGeometry(1,36,24),paint,.35,1.35,0);b.scale.set(1.35,.9,.82);g.add(b);
 const c=mesh(new THREE.SphereGeometry(1,36,24),glass,.95,1.48,0);c.scale.set(.82,.66,.7);g.add(c);
 const tb=mesh(new THREE.CylinderGeometry(.11,.3,2.7,16),paint,-1.95,1.55,0);tb.rotation.z=Math.PI/2+.06;g.add(tb);
 const fin=mesh(new THREE.BoxGeometry(.45,.85,.07),paint,-3.2,1.9,0);fin.rotation.z=-.35;g.add(fin);
 g.add(mesh(new THREE.BoxGeometry(.35,.05,1.0),paint,-2.75,1.52,0));
 [-.62,.62].forEach(z=>{const s=mesh(new THREE.CylinderGeometry(.05,.05,2.7,10),chrome,.3,.28,z);s.rotation.z=Math.PI/2;g.add(s);
  [-.35,.95].forEach(x=>{const p=mesh(new THREE.CylinderGeometry(.04,.04,.6,8),dk,x,.55,z*.85);p.rotation.x=z>0?-.35:.35;g.add(p)})});
 g.add(mesh(new THREE.CylinderGeometry(.1,.14,.4,12),dk,.35,2.3,0));
 g.add(mesh(new THREE.BoxGeometry(.7,.22,.6),dk,.2,2.12,0));
 const rot=new THREE.Group();rot.position.set(.35,2.5,0);
 for(let i=0;i<4;i++){const p=new THREE.Group();p.rotation.y=i*Math.PI/2;p.add(mesh(new THREE.BoxGeometry(2.3,.035,.2),dk,1.15,0,0));rot.add(p)}
 rot.add(mesh(new THREE.CylinderGeometry(.14,.14,.12,12),chrome));g.add(rot);
 const tr=new THREE.Group();tr.position.set(-3.25,2.0,.1);
 for(let i=0;i<2;i++){const p=new THREE.Group();p.rotation.z=i*Math.PI/2;p.add(mesh(new THREE.BoxGeometry(.06,.75,.03),dk));tr.add(p)}g.add(tr);
 g.add(mesh(new THREE.SphereGeometry(.07,10,8),M(0xff0010,{emissive:0xff2020,emissiveIntensity:3}),-.4,.92,.75));
 g.add(mesh(new THREE.SphereGeometry(.07,10,8),M(0x00ff40,{emissive:0x20ff40,emissiveIntensity:3}),-.4,.92,-.75));
 g.scale.setScalar(.95);g.position.x=.35;
 g.userData.tick=(t,dt,on)=>{rot.rotation.y+=dt*(on?28:6);tr.rotation.z+=dt*(on?40:9);g.position.y=Math.sin(t*(on?2.2:1.2))*(on?.18:.06)+(on?.25:0);g.rotation.z=on?Math.sin(t*1.3)*.05:0};
 return g}
function glowTex(hex){const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');
 const gr=x.createRadialGradient(128,128,0,128,128,128);gr.addColorStop(0,hex+'cc');gr.addColorStop(.45,hex+'44');gr.addColorStop(1,hex+'00');
 x.fillStyle=gr;x.fillRect(0,0,256,256);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
function crear(){
 try{rd=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,powerPreference:'low-power'})}catch(e){emojis();return false}
 rd.setPixelRatio(Math.min(devicePixelRatio,matchMedia('(pointer:coarse)').matches?1.5:2));
 rd.toneMapping=THREE.ACESFilmicToneMapping;rd.toneMappingExposure=1.05;rd.outputColorSpace=THREE.SRGBColorSpace;rd.setClearColor(0,0);rd.autoClear=false;
 env=new THREE.PMREMGenerator(rd).fromScene(new RoomEnvironment(),.04).texture;
 const B={coche,moto,heli},C={coche:'#ff5a36',moto:'#22d3ee',heli:'#c6f432'};
 views=[...SZ.querySelectorAll('.iCard')].map(card=>{
  const k=card.dataset.v,sc=new THREE.Scene();sc.environment=env;
  sc.add(new THREE.HemisphereLight(0xbfc8ff,0x201028,.6));
  const key=new THREE.DirectionalLight(0xffffff,2.2);key.position.set(4,6,5);sc.add(key);
  const rim=new THREE.DirectionalLight(new THREE.Color(C[k]),3.5);rim.position.set(-5,2,-4);sc.add(rim);
  const piv=new THREE.Group();sc.add(piv);const model=B[k]();piv.add(model);
  const gm=new THREE.Mesh(new THREE.PlaneGeometry(7,7),new THREE.MeshBasicMaterial({map:glowTex(C[k]),transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}));gm.rotation.x=-Math.PI/2;gm.position.y=.01;sc.add(gm);
  const ring=new THREE.Mesh(new THREE.RingGeometry(2.75,2.82,96),new THREE.MeshBasicMaterial({color:C[k],transparent:true,opacity:.6,side:THREE.DoubleSide}));ring.rotation.x=-Math.PI/2;ring.position.y=.02;sc.add(ring);
  const sh=new THREE.Mesh(new THREE.CircleGeometry(2.2,48),new THREE.MeshBasicMaterial({color:0,transparent:true,opacity:.45,depthWrite:false}));sh.rotation.x=-Math.PI/2;sh.scale.set(1,.55,1);sh.position.y=.015;sc.add(sh);
  return{card,stage:card.querySelector('.stage'),sc,cam:new THREE.PerspectiveCamera(30,1,.1,100),piv,model,ring,gm,s:.85,a:Math.random()*6}});
 return true}
function frame(now){
 if(!visible()){parado=true;return}
 requestAnimationFrame(frame);
 const dt=Math.min(.05,(now-last)/1000||0),t=now/1000;last=now;
 const R=SZ.getBoundingClientRect(),W=Math.round(R.width),H=Math.round(R.height);
 const sz=rd.getSize(new THREE.Vector2());if(sz.x!==W||sz.y!==H)rd.setSize(W,H,false);
 rd.setScissorTest(false);rd.clear();rd.setScissorTest(true);
 const mapaAbierto=!document.getElementById('iMapa').hidden;
 for(const v of views){
  const r=v.stage.getBoundingClientRect();if(mapaAbierto||r.width<4||r.height<4)continue;
  const on=v.card.classList.contains('on');
  v.s+=((on?1:.82)-v.s)*Math.min(1,dt*6);v.piv.scale.setScalar(v.s);
  v.a+=dt*(on?.7:.25);v.piv.rotation.y=v.a;v.model.userData.tick(t,dt,on);
  v.ring.material.opacity=on?.55+Math.sin(t*4)*.3:.18;v.ring.scale.setScalar(on?1+Math.sin(t*2)*.03:1);v.gm.material.opacity=on?1:.45;
  const asp=r.width/r.height,d=10.5*Math.max(1,1.55/asp);
  v.cam.aspect=asp;v.cam.position.set(0,d*.32,d);v.cam.lookAt(0,1.05,0);v.cam.updateProjectionMatrix();
  const x=r.left-R.left,y=R.bottom-r.bottom;rd.setViewport(x,y,r.width,r.height);rd.setScissor(x,y,r.width,r.height);rd.render(v.sc,v.cam);
 }
}
function despierta(){if(!visible()||!parado)return;if(!rd&&!crear())return;parado=false;last=performance.now();requestAnimationFrame(frame)}
new MutationObserver(despierta).observe(SZ,{attributes:true,attributeFilter:['hidden','class','style']});
addEventListener('resize',despierta);setInterval(despierta,1000);despierta();
}}})();
