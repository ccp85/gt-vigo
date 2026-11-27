// ---------- granos de arena de verdad (gpu_arena.js, solo gpu.html y solo con WebGPU) ----------
// Miles de granos simulados en la tarjeta gráfica con compute shaders. Las ruedas en la arena seca y las pisadas los lanzan
// (los mismos sitios donde huellas.js soltaba unos pocos granos, ahora muchos más), vuelan con gravedad y aire, botan un
// poco y se posan. Al posarse se apilan: el suelo se divide en celdas de unos 6 cm y cada celda cuenta (con atómicos) los
// granos que tiene, así que caen unos encima de otros y forman montoncitos. Si un montón queda más empinado que el ángulo
// de reposo de la arena, el grano de arriba rueda hacia la celda vecina más baja: los montones se derrumban solos.
// El coche, la moto o el protagonista empujan los granos posados al pasar por encima (salen despedidos o se apartan).
// Pasados unos segundos se hunden en la arena y su hueco queda libre. Sin WebGPU (motor WebGL2) no se activa y queda lo de
// siempre. Con window.__GRANOS_OFF=true (antes de jugar) no se crea.
const GRA={ini:0,on:false};window.__GRA=GRA;
function granoIni(){if(GRA.ini)return GRA.on;GRA.ini=1;
 try{const b=R.backend;if(!b||!b.isWebGPUBackend||window.__GRANOS_OFF)return false;
 const T=TSL,{Fn,If,Return,instancedArray,instanceIndex,uniform,float,uint,vec2,vec3,vec4,hash,clamp,max,min,mix,length,floor,smoothstep,atomicAdd,atomicSub,atomicLoad,uv,normalize,sqrt,abs}=T;
 const LT=!!window.LITE||matchMedia('(pointer:coarse)').matches;
 const N=LT?12288:49152,M=1024,G=LT?1<<14:1<<16,C=.0012,DH=.00032;     // granos, huecos de salida por fotograma, celdas, lado de celda, altura por grano
 GRA.N=N;GRA.M=M;GRA.LT=LT;GRA.mult=LT?3:8;GRA.head=0;GRA.cnt=0;GRA.seed=1;
 const pos=instancedArray(N,'vec4'),vel=instancedArray(N,'vec4'),ext=instancedArray(N,'vec4');   // pos: xyz + vida · vel: xyz + posado · ext: suelo, tamaño, tono, celda+1
 const pila=instancedArray(G,'uint').toAtomic();
 const sp=instancedArray(M,'vec4'),sv=instancedArray(M,'vec4');GRA.sp=sp;GRA.sv=sv;                // salidas: xyz + vida · vel + suelo
 const uDt=uniform(0),uCnt=uniform(0,'uint'),uHead=uniform(0,'uint'),uSeed=uniform(0,'uint'),uPl=uniform(new THREE.Vector4(0,0,-99,0)),uPv=uniform(new THREE.Vector2()),uWind=uniform(1);
 GRA.u={uDt,uCnt,uHead,uSeed,uPl,uPv,uWind};
 const celda=Fn(([x,z])=>{const ix=uint(T.int(floor(x.div(C)))),iz=uint(T.int(floor(z.div(C))));return ix.mul(uint(73856093)).bitXor(iz.mul(uint(19349663))).bitAnd(uint(G-1))});
 const rnd=k=>hash(instanceIndex.mul(uint(7)).add(uint(k)).add(uSeed.mul(uint(977))));
 // salida de granos nuevos (anillo: el más viejo deja su sitio)
 GRA.cSal=Fn(()=>{const i=instanceIndex;If(i.greaterThanEqual(uCnt),()=>{Return()});
  const j=uHead.add(i).mod(uint(N)),e=ext.element(j),cw=e.w;
  If(cw.greaterThan(.5),()=>{atomicSub(pila.element(uint(cw).sub(uint(1))),uint(1))});
  pos.element(j).assign(sp.element(i));const s=sv.element(i);
  vel.element(j).assign(vec4(s.xyz,0));
  ext.element(j).assign(vec4(s.w,rnd(1).mul(.00045).add(.00045),rnd(2),0))})().compute(M);
 // física de cada grano
 GRA.cUpd=Fn(()=>{const i=instanceIndex,P=pos.element(i),V=vel.element(i),E=ext.element(i);
  const p=P.toVar(),v=V.toVar(),e=E.toVar();
  If(p.w.lessThanEqual(0),()=>{Return()});
  p.w.subAssign(uDt);
  If(p.w.lessThanEqual(0),()=>{If(e.w.greaterThan(.5),()=>{atomicSub(pila.element(uint(e.w).sub(uint(1))),uint(1))});P.assign(vec4(0,-99,0,0));E.w.assign(0);Return()});
  const dPl=p.xz.sub(uPl.xy),lPl=length(dPl);
  If(v.w.lessThan(.5),()=>{   // en el aire
   v.y.subAssign(uDt.mul(.28));
   const aire=vec2(.82,.57).mul(.02).mul(uWind);
   v.xz.assign(mix(v.xz,aire,min(1,uDt.mul(.6))));
   p.xyz.addAssign(v.xyz.mul(uDt));
   const c=celda(p.x,p.z),hc=float(atomicLoad(pila.element(c))),suelo=e.x.add(hc.mul(DH));
   If(p.y.lessThanEqual(suelo),()=>{p.y.assign(suelo);
    If(v.y.lessThan(-.035).and(rnd(3).greaterThan(.35)),()=>{v.y.assign(v.y.negate().mul(.22));v.xz.mulAssign(.45)})   // bote
    .Else(()=>{v.assign(vec4(0,0,0,1));atomicAdd(pila.element(c),uint(1));e.w.assign(float(c).add(1));p.y.assign(suelo.add(DH*.5))})})})
  .Else(()=>{                  // posado: empujones y derrumbes
   const c=uint(e.w).sub(uint(1)),h=float(atomicLoad(pila.element(c)));
   const empuja=lPl.lessThan(uPl.w).and(uPl.z.greaterThan(.02));
   If(empuja,()=>{atomicSub(pila.element(c),uint(1));e.w.assign(0);
    const dir=dPl.div(max(lPl,1e-5)),f=uPl.z;
    v.assign(vec4(dir.x.mul(f.mul(.12).add(.02)).add(uPv.x.mul(rnd(4).mul(.5).add(.3))),f.mul(rnd(5).mul(.08).add(.02)).add(.01),dir.y.mul(f.mul(.12).add(.02)).add(uPv.y.mul(rnd(4).mul(.5).add(.3))),0));
    p.y.addAssign(DH)})
   .Else(()=>{
    // ángulo de reposo: mira una vecina al azar; si está 3 granos o más por debajo (unos 35°), rueda hacia ella
    const a=rnd(6).mul(6.2832),d=vec2(T.cos(a),T.sin(a)),qn=p.xz.add(d.mul(C)),cn=celda(qn.x,qn.y),hn=float(atomicLoad(pila.element(cn)));
    If(h.sub(hn).greaterThanEqual(3).and(cn.notEqual(c)),()=>{atomicSub(pila.element(c),uint(1));e.w.assign(0);v.assign(vec4(d.mul(.025),.004,0).xzyw)})
    .Else(()=>{p.y.assign(mix(p.y,e.x.add(h.sub(.5).mul(DH)),min(1,uDt.mul(8))))});
    p.y.subAssign(smoothstep(1.2,0,p.w).mul(e.y).mul(uDt).mul(1.2))})});   // al final se hunde
  P.assign(p);V.assign(v);E.assign(e)})().compute(N);
 // dibujo: granos redondos con luz como bolitas, cada uno con su tono (alguno oscuro y alguna concha clara)
 const m=new THREE.SpriteNodeMaterial({transparent:false,depthWrite:true});
 const pa=pos.toAttribute(),ea=ext.toAttribute();
 m.positionNode=pa.xyz;m.scaleNode=ea.y.mul(smoothstep(0,.25,pa.w));
 const q=uv().sub(.5).mul(2),r2=q.dot(q);
 m.maskNode=r2.lessThan(1);
 const nz=sqrt(max(0,float(1).sub(r2))),luz=clamp(q.x.mul(-.35).add(q.y.mul(.45)).add(nz.mul(.75)),0,1).mul(.55).add(.5);
 const t=ea.z,base=mix(vec3(.86,.76,.58),vec3(.95,.89,.76),t);
 const tono=mix(mix(base,vec3(.42,.36,.3),smoothstep(.9,.96,t)),vec3(.98,.96,.92),smoothstep(.985,1,t));
 GRA.uL=uniform(1);const uWet=GT.U(UMO.uWet);
 m.colorNode=tono.mul(mix(float(1),float(.62),uWet)).mul(luz).mul(GRA.uL);
 const s=new THREE.Sprite(m);s.count=N;s.frustumCulled=false;s.name='granos_arena';s.renderOrder=2;s.visible=false;scene.add(s);GRA.spr=s;
 // vaciar al empezar (todos muertos)
 GRA.cIni=Fn(()=>{pos.element(instanceIndex).assign(vec4(0,-99,0,0));ext.element(instanceIndex).w.assign(0)})().compute(N);
 GRA.cIniP=Fn(()=>{T.atomicStore(pila.element(instanceIndex),uint(0))})().compute(G);
 R.compute(GRA.cIni);R.compute(GRA.cIniP);
 GRA.on=true;return true}catch(e){console.warn('granos de arena',e);GRA.on=false;return false}}
// los granos que soltaba huellas.js pasan aquí, multiplicados y con un poco de dispersión
function granoEmite(x,y,z,vx,vy,vz,suelo){if(!GRA.on)return false;const A=GRA.sp.value.array,B=GRA.sv.value.array,k=GRA.mult;
 for(let n=0;n<k&&GRA.cnt<GRA.M;n++){const o=GRA.cnt*4,s=.75+Math.random()*.5;
  A[o]=x+(Math.random()-.5)*.002;A[o+1]=y;A[o+2]=z+(Math.random()-.5)*.002;A[o+3]=8+Math.random()*7;
  B[o]=vx*s+(Math.random()-.5)*.02;B[o+1]=vy*(.7+Math.random()*.6);B[o+2]=vz*s+(Math.random()-.5)*.02;B[o+3]=suelo;GRA.cnt++}
 return true}
function granoTick(dt){if(!GRA.ini&&driving)granoIni();if(!GRA.on)return;
 const vis=driving&&!RACE.on;GRA.spr.visible=vis;if(!vis||!dt){GRA.cnt=0;return}
 const u=GRA.u,M=MODO,sp=Math.abs(P.v||0),fx=Math.cos(P.a),fz=-Math.sin(P.a);
 u.uDt.value=Math.min(dt,1/20);u.uSeed.value=(GRA.seed=(GRA.seed*1103515245+12345)>>>0)&0xffffff;
 const rad=M==='pie'?.0035:(M==='coche'?(car.userData&&car.userData.tipo==='moto'?.008:.02):(M==='motoc'?.008:0));
 u.uPl.value.set(P.x,P.y,rad?Math.min(1,sp/.5):0,rad);u.uPv.value.set(fx*(P.v||0)*.25,fz*(P.v||0)*.25);
 u.uWind.value=1+UMO.uWet.value;GRA.uL.value=window.__HU?__HU.mU.uL.value:1;
 if(GRA.cnt){u.uCnt.value=GRA.cnt;u.uHead.value=GRA.head;GRA.sp.value.needsUpdate=true;GRA.sv.value.needsUpdate=true;R.compute(GRA.cSal);GRA.head=(GRA.head+GRA.cnt)%GRA.N;GRA.cnt=0}
 R.compute(GRA.cUpd)}
// ---------- fin de gpu_arena.js
