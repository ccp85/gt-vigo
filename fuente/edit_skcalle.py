f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= SKATE 4: BAJADA DEL CASTRO AL PUERTO =================
# Circuito cerrado y vallado por grandes avenidas (Castro → Praza de España → Gran Vía → Urzaiz → Colón → Praza de
# Compostela → Estación Marítima), al atardecer. El skate siempre avanza (aunque choques con la valla); ◀ ▶ cambian de
# carril, ▲ empuja, ▼ frena un poco. Monedas y regalos por el camino, rampas de salto (en el aire: ◀ ▶ giros, ▼ flip)
# y placas de turbo. Sin tráfico ni peatones en la ruta. Al llegar a la meta, tu carroza te espera en el puerto.
r("if(esSkaK(k))return{v:'coche',skate:true,txt:'🛹 Skate por los tejados'}","if(esSkaK(k))return{v:'coche',skate:true,txt:'🛹 Bajada en skate: Castro → Puerto'}")
r("if(m.skate&&skateInicio(m,k))return;","if(m.skate&&skCalleInicio(m,k))return;")
r("if(m.skate&&SKT.on){skateTick(dt||.016);return}","if(m.skate&&SKC.on){skCalleTick(dt||.016);return}if(m.skate&&SKT.on){skateTick(dt||.016);return}")
r("if(MODO==='skate'){updateSkate(dt);return}","if(MODO==='skate'){if(SKC.on)skCalleUpdate(dt);else updateSkate(dt);return}")
r("if(SKT.on&&skateAccion())return;","if(SKC.on&&MODO==='skate'){skCalleSalta();return}if(SKT.on&&skateAccion())return;")
r("function buscarObjetivo(){objetivo=null;if(SKT.on){","function buscarObjetivo(){objetivo=null;if(SKC.on&&MODO==='skate')return null;if(SKT.on){")
r("DENS.p=dInterp(DTAB_P,h)}","DENS.p=dInterp(DTAB_P,h);if(SKC.on&&SKC.fase!=='ir'){DENS.t=0;DENS.p=0}}")
r("const nAct=Math.max(6,Math.round(TRAF.length*DENS.t))","const nAct=Math.max(SKC.on&&SKC.fase!=='ir'?0:6,Math.round(TRAF.length*DENS.t))")
r("function repCocheCalle(){",r"""const SKC={on:false};window.__SKC=SKC;
const SKC_W=[[86.0,27.4],[85.9,29.9],[88.5,30.24],[91.25,30.31],[93.72,30.14],[95.04,27.1],[97.2,22.5],[95.67,21.14],[93.9,20.5],[93.15,18.6],[91.47,14.91],[89.78,13.63]],SKC_AN=.075;
// ruta por las calles sin sentidos únicos, prefiriendo avenidas grandes
function skcRuta(){const G=gpsGrafo();if(!G)return null;const N=G.X.length;if(!G.UND){const U=[];for(let i=0;i<N;i++)U.push([]);for(let u=0;u<N;u++){const A=G.ADJ[u];for(let k=0;k<A.length;k+=2){const v=A[k],w=A[k+1];U[u].push(v,w);U[v].push(u,w)}}G.UND=U}
 const near=(x,y)=>{let b=-1,bd=1e9;for(let i=0;i<N;i++){const d=Math.hypot(G.X[i]-x,G.Y[i]-y);if(d<bd){bd=d;b=i}}return b};
 const cf=i=>{const c=G.CLS[i]||'m';return c==='T'||c==='P'?1:c==='S'?1.5:3};
 const camino=(a,b)=>{const dist=new Float64Array(N).fill(1e18),prev=new Int32Array(N).fill(-1),H=[[0,a]];dist[a]=0;
  const pop=()=>{const t=H[0],l=H.pop();if(H.length){H[0]=l;let i=0;for(;;){const c1=2*i+1,c2=c1+1;let m=i;if(c1<H.length&&H[c1][0]<H[m][0])m=c1;if(c2<H.length&&H[c2][0]<H[m][0])m=c2;if(m===i)break;[H[i],H[m]]=[H[m],H[i]];i=m}}return t};
  const push=(d,k)=>{H.push([d,k]);let i=H.length-1;while(i>0){const j=(i-1)>>1;if(H[j][0]<=H[i][0])break;[H[i],H[j]]=[H[j],H[i]];i=j}};
  while(H.length){const[d,u]=pop();if(u===b)break;if(d>dist[u])continue;const A=G.UND[u];
   for(let k=0;k<A.length;k+=2){const v=A[k],nd=d+A[k+1]*cf(v);if(nd<dist[v]){dist[v]=nd;prev[v]=u;push(nd,v)}}}
  const o=[];for(let u=b;u>=0;u=prev[u]){o.push([G.X[u],G.Y[u]]);if(u===a)break}return o.reverse()};
 let pts=[];for(let i=1;i<SKC_W.length;i++){const a=near(...SKC_W[i-1]),b=near(...SKC_W[i]);const c=camino(a,b);if(c.length<2)return null;if(pts.length)c.shift();pts.push(...c)}
 // sin idas y vueltas: si el camino vuelve sobre sí mismo se recorta el lazo
 for(let i=0;i<pts.length;i++)for(let j=Math.min(pts.length-1,i+40);j>i+2;j--)if(Math.hypot(pts[i][0]-pts[j][0],pts[i][1]-pts[j][1])<.04){pts.splice(i+1,j-i-1);break}
 for(let it=0;it<3;it++){const q=[pts[0]];for(let i=0;i<pts.length-1;i++){const a=pts[i],b=pts[i+1];q.push([a[0]*.75+b[0]*.25,a[1]*.75+b[1]*.25],[a[0]*.25+b[0]*.75,a[1]*.25+b[1]*.75])}q.push(pts[pts.length-1]);pts=q}
 const R=[pts[0]];let acc=0;for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i],l=Math.hypot(b[0]-a[0],b[1]-a[1]);let t=.02-acc;while(t<=l){R.push([a[0]+(b[0]-a[0])*t/l,a[1]+(b[1]-a[1])*t/l]);t+=.02}acc=l-(t-.02)}
 return R}
function skCalleInicio(m,k){const pts=skcRuta();if(!pts||pts.length<200)return false;REP.mis=m;if(MODO!=='coche')repCocheCalle();
 Object.assign(SKC,{on:true,fase:'ir',pts,L:(pts.length-1)*.02,ac:0});REP.fase='skate';const p0=pts[0];campDestino(['🛹 Salida de la bajada · Monte do Castro',p0[0],p0[1]]);
 aviso('🛹 Misión '+(k+1)+' · ¡Bajada en skate del Castro al Puerto!',2.4,'cuenta');setTimeout(()=>{if(SKC.on&&SKC.fase==='ir')mostrar('Ve a la salida en lo alto del Castro: allí empieza la bajada en skate')},2600);return true}
function skCalleTick(dt){const S=SKC;if(S.fase!=='ir'||MODO!=='coche')return;const p0=S.pts[0];if(Math.hypot(p0[0]-P.x,p0[1]-P.y)<.35){S.ac+=dt;if(S.ac>.2)skCalleEmpieza()}else S.ac=0}
function skcEn(s){const S=SKC,n=S.pts.length,f=Math.max(0,Math.min(n-1.001,s/.02)),i=Math.floor(f),u=f-i,a=S.pts[i],b=S.pts[i+1],c=S.pts[Math.min(n-1,i+3)],d=S.pts[Math.max(0,i-2)];
 const tx=c[0]-d[0],ty=c[1]-d[1],l=Math.hypot(tx,ty)||1;return{x:a[0]+(b[0]-a[0])*u,y:a[1]+(b[1]-a[1])*u,tx:tx/l,ty:ty/l,i}}
function skcPos(s,lat){const e=skcEn(s);return[e.x-e.ty*lat,e.y+e.tx*lat,e]}
function skCalleEmpieza(){const S=SKC,n=S.pts.length,L=S.L;S.car=[P.x,P.y,P.a];REP.dest=null;gpsParar();REP.marca.visible=false;
 S.gy=S.pts.map(p=>groundY(p[0],p[1]));for(let i=2;i<n-2;i++)S.gy[i]=(S.gy[i-2]+S.gy[i-1]+S.gy[i]+S.gy[i+1]+S.gy[i+2])/5;
 const G=new THREE.Group();G.name='skCalle';const W=SKC_AN;
 // vallas: postes y paneles rojos y blancos a los dos lados
 {const tc=document.createElement('canvas');tc.width=128;tc.height=16;const x=tc.getContext('2d');for(let k=0;k<4;k++){x.fillStyle=k%2?'#ffffff':'#d81f26';x.fillRect(k*32,0,32,16)}x.fillStyle='rgba(0,0,0,.25)';x.fillRect(0,14,128,2);
  const T=new THREE.CanvasTexture(tc);T.wrapS=THREE.RepeatWrapping;T.colorSpace=THREE.SRGBColorSpace;const mat=new THREE.MeshStandardMaterial({map:T,roughness:.6,side:THREE.DoubleSide});
  for(const sd of[1,-1]){const pos=[],uv=[],idx=[];for(let i=0;i<n;i++){const[x0,y0]=skcPos(i*.02,sd*W),g=S.gy[i];pos.push(x0,g+.008,y0,x0,g+.026,y0);uv.push(i*.02/.12,0,i*.02/.12,1);if(i<n-1){const a=i*2;idx.push(a,a+1,a+2,a+1,a+3,a+2)}}
   const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();G.add(new THREE.Mesh(g,mat))}
  const NP=Math.floor(n/3)*2,im=new THREE.InstancedMesh(new THREE.BoxGeometry(.004,.03,.004),new THREE.MeshStandardMaterial({color:0xeeeeee,roughness:.5}),NP),du=new THREE.Object3D();let k=0;
  for(let i=0;i<n&&k<NP;i+=3)for(const sd of[1,-1]){const[x0,y0]=skcPos(i*.02,sd*W);du.position.set(x0,S.gy[i]+.015,y0);du.updateMatrix();im.setMatrixAt(k++,du.matrix)}im.count=k;im.frustumCulled=false;G.add(im)}
 // arcos de salida y meta
 const arco=(s0,txt,col)=>{const e=skcEn(s0),g=new THREE.Group(),a=Math.atan2(-e.ty,e.tx);g.position.set(e.x,S.gy[e.i],e.y);g.rotation.y=a;const M=new THREE.MeshStandardMaterial({color:col,roughness:.5});
  for(const sd of[1,-1]){const p=new THREE.Mesh(new THREE.BoxGeometry(.012,.11,.012),M);p.position.set(0,.055,sd*(W+.01));g.add(p)}
  const c=document.createElement('canvas');c.width=512;c.height=96;const x=c.getContext('2d');x.fillStyle='#'+col.toString(16).padStart(6,'0');x.fillRect(0,0,512,96);x.fillStyle='#fff';x.font='bold 64px sans-serif';x.textAlign='center';x.textBaseline='middle';x.fillText(txt,256,52);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;const b=new THREE.Mesh(new THREE.BoxGeometry(.012,.03,2*W+.03),[M,M,M,M,new THREE.MeshBasicMaterial({map:t}),new THREE.MeshBasicMaterial({map:t})]);b.position.y=.11;b.rotation.y=Math.PI/2;b.rotation.y=0;
  const bb=new THREE.Mesh(new THREE.PlaneGeometry(2*W+.03,.03),new THREE.MeshBasicMaterial({map:t,side:THREE.DoubleSide}));bb.position.y=.11;bb.rotation.y=Math.PI/2;g.add(bb);G.add(g)};
 arco(.12,'SALIDA',0x1f8a3a);arco(L-.06,'META',0xc4161f);
 // monedas, regalos, rampas y turbos
 S.mon=[];S.reg=[];S.ram=[];S.tur=[];const lats=[-.045,0,.045];let pat=0;
 for(let s0=.5;s0<L-.4;s0+=.11){if(Math.floor(s0/.9)!==pat)pat=Math.floor(s0/.9);const l=lats[pat%3]+Math.sin(s0*3)*.012;S.mon.push({s:s0,l,ok:false})}
 for(let s0=1.2;s0<L-.6;s0+=1.35)S.reg.push({s:s0,l:lats[(Math.floor(s0*7))%3]*.9,ok:false});
 for(let s0=2.2;s0<L-1;s0+=2.6){const l=lats[Math.floor(s0*3)%3]*.5;S.ram.push({s:s0,l});S.tur.push({s:s0-.32,l})}
 for(let s0=3.4;s0<L-1;s0+=2.6){const l=lats[(Math.floor(s0*5)+1)%3];S.tur.push({s:s0,l})}
 for(const r_ of S.ram)S.mon=S.mon.filter(m=>Math.abs(m.s-r_.s)>.15||Math.abs(m.l-r_.l)>.06);
 const mk=(geo,mat,n)=>{const im=new THREE.InstancedMesh(geo,mat,n);im.frustumCulled=false;G.add(im);return im};
 S.imM=mk(new THREE.CylinderGeometry(.009,.009,.0025,14).rotateX(Math.PI/2),new THREE.MeshStandardMaterial({color:0xffcc33,emissive:0xb07800,emissiveIntensity:.6,metalness:.6,roughness:.3}),S.mon.length);
 S.imR=mk(new THREE.BoxGeometry(.02,.02,.02),new THREE.MeshStandardMaterial({color:0xffffff,emissive:0x222222,roughness:.5}),S.reg.length);
 {const cc=[0xd51f1f,0x1fae4a,0x1f6fd0,0xf2c230,0xb03fd0],C=new THREE.Color();S.reg.forEach((g,i)=>S.imR.setColorAt(i,C.setHex(cc[i%5])))}
 {const ge=new THREE.BoxGeometry(.1,.02,.1);const p=ge.attributes.position;for(let i=0;i<p.count;i++){const x=p.getX(i);if(p.getY(i)>0)p.setY(i,x>0?.025:-.01)}ge.computeVertexNormals();ge.translate(0,.01,0);
  const c=document.createElement('canvas');c.width=64;c.height=64;const x=c.getContext('2d');for(let k=0;k<8;k++){x.fillStyle=k%2?'#111':'#f6c400';x.fillRect(k*8,0,8,64)}const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;
  const M=new THREE.MeshStandardMaterial({map:t,roughness:.6});for(const r_ of S.ram){const[x0,y0,e]=skcPos(r_.s,r_.l),m=new THREE.Mesh(ge,M);m.position.set(x0,S.gy[e.i],y0);m.rotation.y=Math.atan2(-e.ty,e.tx);G.add(m)}}
 {const c=document.createElement('canvas');c.width=64;c.height=64;const x=c.getContext('2d');x.fillStyle='#0a3a5a';x.fillRect(0,0,64,64);x.fillStyle='#35e0ff';for(const yy of[8,30]){x.beginPath();x.moveTo(12,yy+22);x.lineTo(32,yy);x.lineTo(52,yy+22);x.lineTo(44,yy+22);x.lineTo(32,yy+10);x.lineTo(20,yy+22);x.fill()}
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;const M=new THREE.MeshBasicMaterial({map:t,toneMapped:false});
  for(const q of S.tur){const[x0,y0,e]=skcPos(q.s,q.l),m=new THREE.Mesh(new THREE.PlaneGeometry(.045,.06),M);m.rotation.x=-Math.PI/2;m.rotation.z=Math.atan2(-e.ty,e.tx)-Math.PI/2;m.position.set(x0,S.gy[e.i]+.003,y0);G.add(m)}}
 scene.add(G);S.G=G;S.sk=mkSkate();scene.add(S.sk);S.hPrev=CIELO.h;S.mPrev=CIELO.modo;CIELO.modo='tarde';CIELO.h=19.1;
 Object.assign(S,{fase:'cuenta',s:.05,lat:0,rel:0,v:0,z:S.gy[0],vz:0,air:false,spin:0,flip:0,boost:0,t:0,cu:3,monedas:0,regalos:0,combo:0,pts0:REP.pts,avV:0});
 cambiarModo('skate');car.visible=true;camInit=false;repHud();try{densHora()}catch(e){}
 aviso('3',.8,'cuenta');try{bip(440,.12,.06)}catch(e){}}
function skCalleSalta(){const S=SKC;if(S.fase!=='carrera'||S.air)return;S.air=true;S.vz=.75;S.spin=0;S.flip=0;try{bip(520,.06,.05)}catch(e){}}
function skCalleUpdate(dt){const S=SKC;if(!REP.on||!S.on){skCalleSale(false);return}dt=Math.min(dt,.05);const tn=performance.now()/1000;
 if(S.fase==='cuenta'){S.cu-=dt;const c=Math.ceil(S.cu);if(c!==S.cuL&&c>0){S.cuL=c;if(c<3){aviso(String(c),.8,'cuenta');try{bip(440,.12,.06)}catch(e){}}}if(S.cu<=0){S.fase='carrera';aviso('🛹 ¡YA!',1,'cuenta');try{bip(880,.2,.07)}catch(e){};mostrar('◀ ▶ gira · pégate a la valla para hacer grind · ▲ empuja · ▼ frena · turbo + rampa = gran salto: en el aire ◀ ▶ giros y ▼ flip')}}
 else if(S.fase==='carrera'){S.t+=dt;const e=skcEn(S.s),i=e.i,pend=(S.gy[Math.max(0,i-3)]-S.gy[Math.min(S.pts.length-1,i+3)])/.12;
  let obj=.5+Math.max(-.1,Math.min(.35,pend*1.2))+(keys.up?.25:0)-(keys.down?.2:0);if(S.boost>0){S.boost-=dt;obj*=1.7}obj=Math.max(.32,obj);S.v+=(obj-S.v)*Math.min(1,dt*(S.boost>0?4:1.8));
  S.s+=S.v*dt;
  if(!S.air){const st=(keys.left?1:0)-(keys.right?1:0);if(st)S.rel=Math.max(-.7,Math.min(.7,(S.rel||0)+st*3.2*dt));else S.rel=(S.rel||0)*Math.max(0,1-dt*4);S.lat-=Math.sin(S.rel)*Math.max(.35,S.v)*dt}else{if(keys.left)S.spin+=dt*11;if(keys.right)S.spin-=dt*11;if(keys.down)S.flip+=dt*10}
  const lim=SKC_AN-.014;const pulsa=keys.left||keys.right;if(S.grind){S.grT+=dt;S.lat=S.grind*(SKC_AN-.002);S.rel=0;S.grP+=dt*40;if(!pulsa)S.grHeld=false;if(S.grT>.25&&pulsa&&!S.grHeld){const p=Math.round(S.grP);REP.pts+=p;repPop('🛹 Grind '+S.grT.toFixed(1)+' s · +'+p,'aviso');S.lat=S.grind*(lim-.012);S.grind=0;S.air=true;S.vz=.45;try{bip(700,.08,.05)}catch(e){}}else if(Math.random()<.5&&tn-(S.grS||0)>.12){S.grS=tn;try{bip(1400+Math.random()*400,.03,.02)}catch(e){}}}else if(Math.abs(S.lat)>lim){S.lat=Math.sign(S.lat)*lim;S.rel=0;if(!S.air){S.grind=Math.sign(S.lat);S.grT=0;S.grP=0;S.grHeld=pulsa;S.v=Math.max(S.v,.6);aviso('🛹 ¡GRIND! ◀ ▶ para bajar',.9,'peq');try{bip(1200,.1,.05)}catch(e){}}}
  const gy=S.gy[i]+(S.gy[Math.min(S.pts.length-1,i+1)]-S.gy[i])*((S.s/.02)-i);
  // rampas
  let rz=0;for(const r_ of S.ram){const d=S.s-r_.s;if(d>-.05&&d<.05&&Math.abs(S.lat-r_.l)<.05&&!S.grind){rz=(d+.05)/.1*.035;if(d>.042&&!S.air){S.air=true;S.vz=1.2;S.grind=0;S.spin=0;S.flip=0;S.v=Math.max(S.v,.7);try{bip(620,.08,.05)}catch(e){}}}}
  if(!S.air)S.z=gy+rz+(S.grind?.028:0);else{S.vz-=1.8*dt;S.z+=S.vz*dt;if(S.z<=gy){S.z=gy;S.air=false;const g=Math.floor(Math.abs(S.spin)/5.6),fl=Math.floor(S.flip/5.6);if(g||fl){const p=(g*60+fl*90)*(1+S.combo*.5);S.combo++;REP.pts+=Math.round(p);repPop((fl?'🛹 Kickflip ':'')+(g?g*360+'° ':'')+'+'+Math.round(p)+(S.combo>1?' · combo x'+S.combo:''),'aviso');try{bip(880,.08,.05)}catch(e){}}else S.combo=0;S.spin=0;S.flip=0;REP.shake=.1}}
  // turbos
  for(const q of S.tur)if(!q.hit&&Math.abs(S.s-q.s)<.035&&Math.abs(S.lat-q.l)<.03&&!S.air){q.hit=true;S.boost=1.6;aviso('⚡ ¡TURBO!',.7,'peq');try{bip(990,.15,.06)}catch(e){}}
  // monedas y regalos
  for(const m of S.mon)if(!m.ok&&Math.abs(S.s-m.s)<.025&&Math.abs(S.lat-m.l)<.03&&S.z-gy<.06){m.ok=true;S.monedas++;REP.pts+=10;try{sonMoneda()}catch(e){}}
  for(const g of S.reg)if(!g.ok&&Math.abs(S.s-g.s)<.03&&Math.abs(S.lat-g.l)<.035){g.ok=true;S.regalos++;REP.pts+=50;repPop('🎁 ¡Regalo! '+S.regalos+'/'+S.reg.length+' · +50','gran');try{sonCaja()}catch(e){}}
  if(S.s>=S.L-.05){S.fase='meta';S.tm=0;const pts=REP.pts-S.pts0+200;REP.pts+=200;try{confeti()}catch(e){}try{sonJoJo();setTimeout(()=>sonPublico(1.3),300)}catch(e){}
   aviso('🏁 ¡META!',1.6,'cuenta');repPop('🛹 Bajada completada en '+S.t.toFixed(1)+' s · 🪙 '+S.monedas+'/'+S.mon.length+' · 🎁 '+S.regalos+'/'+S.reg.length+' · +'+pts+' ⭐','gran')}}
 else if(S.fase==='meta'){S.tm+=dt;S.v*=Math.max(0,1-dt*1.5);S.s=Math.min(S.L,S.s+S.v*dt);if(S.tm>2.6){skCalleSale(true);return}}
 // mover monedas y regalos (giran) y colocar patinador y cámara
 const du=new THREE.Object3D();S.mon.forEach((m,k)=>{if(m.ok||Math.abs(m.s-S.s)>6){du.scale.setScalar(0)}else{const[x0,y0,e]=skcPos(m.s,m.l);du.position.set(x0,S.gy[e.i]+.022,y0);du.rotation.set(0,tn*3+m.s,0);du.scale.setScalar(1)}du.updateMatrix();S.imM.setMatrixAt(k,du.matrix)});S.imM.instanceMatrix.needsUpdate=true;
 S.reg.forEach((g,k)=>{if(g.ok){du.scale.setScalar(0)}else{const[x0,y0,e]=skcPos(g.s,g.l);du.position.set(x0,S.gy[e.i]+.03+Math.sin(tn*3+g.s)*.006,y0);du.rotation.set(.3,tn*1.5+g.s,0);du.scale.setScalar(1)}du.updateMatrix();S.imR.setMatrixAt(k,du.matrix)});S.imR.instanceMatrix.needsUpdate=true;
 const[x,y,e]=skcPos(S.s,S.lat),a=Math.atan2(-e.ty,e.tx);P.x=x;P.y=y;P.a=a;P.v=0;const sk=S.sk;sk.position.set(x,S.z,y);sk.rotation.set(0,a+S.spin+(S.air?0:(S.rel||0)),0);sk.userData.tb.rotation.x=S.flip;sk.userData.f.position.y=.0125+(S.air?0:Math.abs(Math.sin(tn*14))*.002*S.v);
 const[cx,cy,ce]=skcPos(Math.max(0,S.s-.24),S.lat*.6),want=new THREE.Vector3(cx,Math.max(S.gy[ce.i],S.z)+.19,cy);{const hc=skAlt(cx,cy);if(hc[1]&&hc[0]>want.y-.03)want.y=hc[0]+.05}if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*5));
 const[lx,ly]=skcPos(Math.min(S.L,S.s+.22),S.lat*.8);look.set(lx,S.z+.01,ly);pcam.lookAt(look);pcam.fov=68+S.v*10+(S.boost>0?8:0);pcam.updateProjectionMatrix();FOG.near=5;FOG.far=20;
 const vv=document.getElementById('vel');vv.firstChild.nodeValue='🪙'+S.monedas+' 🎁'+S.regalos;vv.querySelector('small').textContent=S.fase==='carrera'?'⏱ '+S.t.toFixed(1)+' s · 🛹 bajada al puerto':'🛹 bajada al puerto';hudAccion(dt)}
function skCalleSale(ok){const S=SKC;if(S.G){scene.remove(S.G);S.G=null}if(S.sk){scene.remove(S.sk);S.sk=null}if(S.hPrev!=null){CIELO.h=S.hPrev;CIELO.modo=S.mPrev||'auto';S.hPrev=null}S.on=false;const fin=S.fase==='meta';S.fase='fin';
 if(MODO==='skate'){cambiarModo('coche');if(fin&&S.pts){const n=S.pts.length,p=S.pts[n-1],q=S.pts[n-6];P.x=p[0];P.y=p[1];P.a=Math.atan2(-(p[1]-q[1]),p[0]-q[0])}else if(S.car){P.x=S.car[0];P.y=S.car[1];P.a=S.car[2]}}P.v=0;camInit=false;try{densHora()}catch(e){}if(!ok)return;
 REP.ent++;REP.nEnt=(REP.nEnt||0)+1;setTimeout(()=>{if(REP.on)mostrar('🎅 ¡Tu carroza te esperaba en el puerto!')},300);
 const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;repSigue(ab,1800)}
function repCocheCalle(){""")
# el recorte de edificios que tapan la vista usa la posición del patinador (antes, la de la carroza aparcada)
r("const vh=MODO==='moto'?moto:MODO==='pie'?persona:car;","const vh=MODO==='moto'?moto:MODO==='pie'?persona:MODO==='skate'&&(SKC.sk||SKT.sk)?(SKC.sk||SKT.sk):car;")
open(f,'w').write(s)
print('ok skcalle')
