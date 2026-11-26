// ---------- huellas, surcos y polvo en la arena (huellas.js, lo mete edit_huellas.py) ----------
// Alrededor del protagonista hay un mapa de huellas de 80 m (en el móvil 60 m) que se va moviendo con él: al
// caminar por la arena deja pisadas (izquierda y derecha, con punta y talón) y en coche, moto o quad cada rueda abre un
// surco con el dibujo del neumático y la arena apartada a los lados. Las huellas se ven en la arena seca y en la mojada
// (allí más oscuras, con agua), la resaca las borra y se van alisando solas en un par de minutos. La arena (orilla.js)
// las dibuja con sombra y relieve.
// Partículas: polvo que levantan las ruedas en la arena seca (más cuanto más rápido), granos que salen despedidos,
// un poco de polvo y arena en cada pisada, y arena que arrastra el viento a ras de suelo alrededor del protagonista.
// Con lluvia la arena no levanta polvo. De noche el polvo se ve oscuro.
const HU={N:window.LITE?512:1024,S:window.LITE?.6:.8,on:false,n:window.LITE?350:1500};window.__HU=HU;
HU.D=new Uint8Array(HU.N*HU.N*2);
HU.tex=new THREE.DataTexture(HU.D,HU.N,HU.N,THREE.RGFormat,THREE.UnsignedByteType);
HU.tex.wrapS=HU.tex.wrapT=THREE.RepeatWrapping;HU.tex.magFilter=HU.tex.minFilter=THREE.LinearFilter;HU.tex.generateMipmaps=false;HU.tex.needsUpdate=true;
HU.U={uHT:{value:HU.tex},uHC:{value:new THREE.Vector4(0,0,HU.S,0)}};
// bloques de 32×32 texeles: cada uno guarda a qué trozo del mundo pertenece; al moverse, los que pasan a otro trozo se borran
HU.nb=HU.N/32;HU.bw=HU.S/HU.nb;HU.bk=new Float64Array(HU.nb*HU.nb*2).fill(NaN);HU.sucio=false;HU.tSub=0;HU.dec=0;
function huVentana(cx,cz){const nb=HU.nb,bw=HU.bw,N=HU.N,D=HU.D,bx0=Math.floor((cx-HU.S/2)/bw),bz0=Math.floor((cz-HU.S/2)/bw);
 for(let jb=0;jb<nb;jb++){const bz=bz0+(((jb-bz0)%nb)+nb)%nb;for(let ib=0;ib<nb;ib++){const bx=bx0+(((ib-bx0)%nb)+nb)%nb,k=(jb*nb+ib)*2;
  if(HU.bk[k]===bx&&HU.bk[k+1]===bz)continue;HU.bk[k]=bx;HU.bk[k+1]=bz;
  for(let j=0;j<32;j++){const o=((jb*32+j)*N+ib*32)*2;D.fill(0,o,o+64)}HU.sucio=true}}
 HU.U.uHC.value.set(cx,cz,HU.S,1)}
// sello: perfil f(u,v) → [hondo, arena apartada] en una caja orientada (centro, dirección, medio largo, medio ancho)
function huSello(x,z,dx,dz,hl,hw,f){const N=HU.N,S=HU.S,D=HU.D,px=S/N,r=Math.hypot(hl,hw)+px;
 const i0=Math.floor((x-r)/px),i1=Math.ceil((x+r)/px),j0=Math.floor((z-r)/px),j1=Math.ceil((z+r)/px);
 for(let j=j0;j<=j1;j++){const wz=(j+.5)*px-z,jj=((j%N)+N)%N;for(let i=i0;i<=i1;i++){const wx=(i+.5)*px-x,u=wx*dx+wz*dz,v=-wx*dz+wz*dx;
  if(Math.abs(u)>hl+px||Math.abs(v)>hw+px)continue;const q=f(u,v);if(!q)continue;const o=(jj*N+(((i%N)+N)%N))*2;
  const a=Math.min(255,q[0]*255|0),b=Math.min(255,q[1]*255|0);if(a>D[o])D[o]=a;if(b>D[o+1])D[o+1]=b}}HU.sucio=true}
const huSS=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t)};
function huPisada(x,z,dx,dz,izq,k){const L=.0025,W=.001;      // a la escala del protagonista (el doble de una persona real)
 huSello(x,z,dx,dz,L*1.5,W*2,(u,v)=>{const un=u/L,ar=1-.32*Math.exp(-un*un*6)*(izq?(v>0?1:.4):(v<0?1:.4)),vn=v/(W*ar),r=Math.hypot(un,vn);
  const dep=huSS(1.05,.55,r)*(.85+.15*huSS(.2,.9,Math.abs(un)))*k;return[dep,huSS(1.55,.95,r)*.9]})}
function huSurco(x0,z0,x1,z1,w,k,s0){const dx=x1-x0,dz=z1-z0,l=Math.hypot(dx,dz);if(l<1e-6)return;const ux=dx/l,uz=dz/l,hw=w/2;
 huSello((x0+x1)/2,(z0+z1)/2,ux,uz,l/2+hw*.4,hw*2.1,(u,v)=>{const a=Math.abs(v)/hw;if(a>2.1)return null;const t=s0+u+l/2;
  const cor=.78+.22*Math.abs(Math.sin(t*1300+(v>0?0:1.57)));   // dibujo del neumático
  return[huSS(1.05,.5,a)*cor*k,huSS(2.1,1.15,a)*.95]})}
// suelo: altura y si es arena (lámina de playa o franja nueva de la orilla)
const HU_RC=new THREE.Raycaster();HU_RC.firstHitOnly=true;const _huO=new THREE.Vector3(),_huD=new THREE.Vector3(0,-1,0);
function huSuelo(x,z){let y=null,ar=false;
 if(GROUND.length){_huO.set(x,9,z);HU_RC.set(_huO,_huD);HU_RC.far=12;const h=HU_RC.intersectObjects(GROUND,false);
  if(h.length){const n=h[0].object.name;y=oriSuelo(h[0],x,z);ar=/^(playa|playita)/.test(n)||(ORI_RE.test(n)&&ORI.Z.length>0&&ORI.h(x,z)!==null)}}
 if(y===null&&ORI.Z.length){const v=ORI.h(x,z);if(v!==null){y=v;ar=true}}
 return{y:y===null?0:y,ar:ar&&y!==null&&y>ORI.WY+.0004,hw:(y===null?1:y-ORI.WY)}}
// ---- partículas ----
function huIniPart(){const n=HU.n,g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(new Float32Array(n*3),3));
 g.setAttribute('aPolvo',new THREE.BufferAttribute(new Float32Array(n*4),4));g.boundingSphere=new THREE.Sphere(new THREE.Vector3(),1e6);
 HU.mU={uSc:{value:800},uL:{value:1}};
 const m=new THREE.ShaderMaterial({uniforms:HU.mU,transparent:true,depthWrite:false,
  vertexShader:'#include <common>\n#include <logdepthbuf_pars_vertex>\nattribute vec4 aPolvo;uniform float uSc;varying vec4 vPo;\nvoid main(){vPo=aPolvo;vec4 mv=modelViewMatrix*vec4(position,1.);gl_Position=projectionMatrix*mv;\n#include <logdepthbuf_vertex>\nfloat d=max(-mv.z,1e-4);gl_PointSize=aPolvo.y>.001?clamp(aPolvo.x*uSc/d,1.2,90.):0.;}',
  fragmentShader:'#include <logdepthbuf_pars_fragment>\nuniform float uL;varying vec4 vPo;\nvoid main(){\n#include <logdepthbuf_fragment>\nfloat r=length(gl_PointCoord-.5)*2.;if(r>1.)discard;float g=step(.5,vPo.z);float a=mix(smoothstep(1.,.1,r)*(.75+.25*sin(vPo.w*40.+r*5.)),smoothstep(1.,.6,r),g)*vPo.y;vec3 c=mix(vec3(.93,.87,.76),vec3(.50,.42,.30),g)*uL;gl_FragColor=vec4(c,a);}'});
 const p=new THREE.Points(g,m);p.name='polvo_arena';p.frustumCulled=false;p.renderOrder=3;scene.add(p);HU.pts=p;
 HU.v=new Float32Array(n*3);HU.vida=new Float32Array(n);HU.edad=new Float32Array(n);HU.t0=new Float32Array(n);HU.t1=new Float32Array(n);HU.a0=new Float32Array(n);HU.k=new Uint8Array(n);HU.suelo=new Float32Array(n);HU.sig=0;HU.vivas=0}
// tipo 0 polvo (crece y se desvanece), 1 grano (cae con gravedad), 2 arena del viento
function huEmite(k,x,y,z,vx,vy,vz,vida,t0,t1,a0,suelo){const n=HU.n;let i=HU.sig;HU.sig=(HU.sig+1)%n;
 const P_=HU.pts.geometry.attributes.position.array;P_[i*3]=x;P_[i*3+1]=y;P_[i*3+2]=z;HU.v[i*3]=vx;HU.v[i*3+1]=vy;HU.v[i*3+2]=vz;
 HU.vida[i]=vida;HU.edad[i]=0;HU.t0[i]=t0;HU.t1[i]=t1;HU.a0[i]=a0;HU.k[i]=k;HU.suelo[i]=suelo}
function huPartTick(dt){const n=HU.n,g=HU.pts.geometry,Pa=g.attributes.position,Aa=g.attributes.aPolvo,P_=Pa.array,A_=Aa.array;let viv=0;
 const wx=.82,wz=.57,ra=Math.sin(performance.now()*.0007)*.5+1;
 for(let i=0;i<n;i++){const o=i*4;if(HU.edad[i]>=HU.vida[i]){if(A_[o+1]!==0){A_[o+1]=0;A_[o]=0}continue}viv++;
  const e=(HU.edad[i]+=dt),t=e/HU.vida[i],k=HU.k[i],p=i*3,v=HU.v;
  if(k===0){v[p]+=(wx*.012*ra-v[p])*Math.min(1,dt*1.6);v[p+2]+=(wz*.012*ra-v[p+2])*Math.min(1,dt*1.6);v[p+1]*=1-Math.min(1,dt*1.2)}
  else{v[p+1]-=.28*dt;if(k===2){v[p]+=(wx*.05*ra-v[p])*Math.min(1,dt*3);v[p+2]+=(wz*.05*ra-v[p+2])*Math.min(1,dt*3);v[p+1]=Math.max(v[p+1],-.004)}}
  P_[p]+=v[p]*dt;P_[p+1]+=v[p+1]*dt;P_[p+2]+=v[p+2]*dt;
  if(k!==0&&P_[p+1]<HU.suelo[i]){P_[p+1]=HU.suelo[i];if(k===1){HU.edad[i]=HU.vida[i];A_[o+1]=0;continue}v[p+1]=Math.abs(v[p+1])*.3}
  A_[o]=HU.t0[i]+(HU.t1[i]-HU.t0[i])*(k===0?1-Math.pow(1-t,2.2):t);
  A_[o+1]=HU.a0[i]*(k===0?huSS(0,.12,t)*(1-huSS(.35,1,t)):(1-huSS(.7,1,t)));A_[o+2]=k===0?0:1;A_[o+3]=(i*.618)%1}
 Pa.needsUpdate=true;Aa.needsUpdate=true;HU.vivas=viv}
const rnd=(a,b)=>a+Math.random()*(b-a);
// ---- cada fotograma ----
HU.ruedas=null;HU.pie=0;HU.izq=false;HU.amb=0;HU.s=0;
function huellasTick(dt){if(!dt)return;if(!HU.pts)huIniPart();
 const c=window.__G&&__G.pcam;if(c&&R.domElement)HU.mU.uSc.value=R.domElement.height/(2*Math.tan(((c.fov||55)*Math.PI/360)));
 HU.mU.uL.value=(1-.8*UW.uN.value)*(1-.25*UMO.uWet.value);
 const vis=driving&&!RACE.on;HU.pts.visible=vis;
 if(vis){huVentana(P.x,P.y);
  const lluvia=UMO.uWet.value>.3,LT=!!window.LITE,M=MODO,fx=Math.cos(P.a),fz=-Math.sin(P.a),sx=-fz,sz=fx,sp=Math.abs(P.v);
  if(M==='pie'&&!BUC.on){if(sp<.01)HU.pie=Math.max(HU.pie,.008);
   HU.pie+=sp*dt;if(HU.pie>.009){HU.pie=0;HU.izq=!HU.izq;const sd=HU.izq?.0018:-.0018,x=P.x+sx*sd,z=P.y+sz*sd,S=huSuelo(x,z);
    if(S.ar&&S.hw>.0015){huPisada(x,z,fx,fz,HU.izq,S.hw<.012?1:.85);
     if(S.hw>.012&&!lluvia){huEmite(0,x,S.y+.001,z,-fx*.012,.005,-fz*.012,rnd(.5,.8),.002,.008,.16,S.y);
      for(let q=0;q<(LT?1:4);q++)huEmite(1,x,S.y+.0006,z,-fx*rnd(.015,.04)+sx*rnd(-.01,.01),rnd(.015,.035),-fz*rnd(.015,.04)+sz*rnd(-.01,.01),2,.0007,.0007,.85,S.y)}}}}
  else HU.pie=0;
  const RUE=M==='coche'||M==='motoc';
  if(RUE&&!P.tun&&!P.ferry){const moto=car.userData&&car.userData.tipo==='moto',W=moto?[[.022,0],[-.022,0]]:[[.025,.015],[.025,-.015],[-.025,.015],[-.025,-.015]];   // ruedas (el coche mide unos 8 × 4 cm del juego)
   if(!HU.ruedas||HU.ruedas.length!==W.length)HU.ruedas=W.map(()=>null);HU.s+=sp*dt;
   W.forEach((w,i)=>{const x=P.x+fx*w[0]+sx*w[1],z=P.y+fz*w[0]+sz*w[1],S=huSuelo(x,z),pr=HU.ruedas[i];
    if(S.ar&&S.hw>.0015){if(pr&&Math.hypot(x-pr[0],z-pr[1])<.05)huSurco(pr[0],pr[1],x,z,moto?.003:.0055,S.hw<.012?.85:1,HU.s);
     const tras=w[0]<0;
     if(tras&&S.hw>.012&&!lluvia&&sp>.03){const f=Math.min(1,sp/.6),np=f*dt*(LT?16:55)+(Math.random()<(f*dt*(LT?16:55))%1?1:0);
      for(let q=0;q<Math.floor(np);q++)huEmite(0,x+rnd(-.004,.004),S.y+.002,z+rnd(-.004,.004),-fx*P.v*.12+rnd(-.008,.008),rnd(.006,.016),-fz*P.v*.12+rnd(-.008,.008),rnd(1.2,2.4),.006,rnd(.03,.06),rnd(.24,.4)*(.5+.5*f),S.y);
      if(sp>.12){const ng=f*dt*(LT?25:90);for(let q=0;q<Math.floor(ng)+(Math.random()<ng%1?1:0);q++)huEmite(1,x,S.y+.0015,z,-fx*P.v*rnd(.2,.45)+sx*rnd(-.05,.05)*f,rnd(.03,.08)*f+.012,-fz*P.v*rnd(.2,.45)+sz*rnd(-.05,.05)*f,2,.0009,.0009,.9,S.y)}}
     HU.ruedas[i]=[x,z]}else HU.ruedas[i]=null})}
  else HU.ruedas=null;
  // arena que arrastra el viento alrededor del protagonista (solo en el ordenador y con la arena seca)
  if(!LT&&!lluvia&&UW.uN.value<.7&&(M==='pie'||sp<.2)){HU.amb+=dt*34;while(HU.amb>=1){HU.amb--;const an=Math.random()*6.2832,r=rnd(.006,.09),x=P.x+Math.cos(an)*r,z=P.y+Math.sin(an)*r,S=huSuelo(x,z);
    if(S.ar&&S.hw>.015)huEmite(2,x,S.y+rnd(.0002,.0015),z,.05,rnd(0,.004),.035,rnd(.8,1.6),.0007,.0007,rnd(.25,.45),S.y)}}else HU.amb=0}
 huPartTick(dt);
 // las huellas se alisan solas (en ≈ 2 min) y la textura se sube a la tarjeta como mucho 12 veces por segundo
 {const D=HU.D,L=D.length;let c=Math.min(L,Math.ceil(L*dt/.45)),i=HU.dec,any=false;while(c-->0){if(D[i]){D[i]--;any=true}if(++i>=L)i=0}HU.dec=i;if(any)HU.sucio=true}
 HU.tSub+=dt;if(HU.sucio&&HU.tSub>.08){HU.tSub=0;HU.sucio=false;HU.tex.needsUpdate=true}}
// ---------- fin de huellas.js
