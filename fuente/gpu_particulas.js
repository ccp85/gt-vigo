// ---------- partículas masivas en la tarjeta gráfica (gpu_particulas.js, solo gpu.html y solo con WebGPU) ----------
// Tres sistemas que se calculan enteros en la GPU con compute shaders (la CPU solo pasa unos pocos números por fotograma):
//  · Lluvia: hasta 200.000 gotas (50.000 en el móvil) en una caja que acompaña a la cámara. Caen en trazos finos e
//    inclinados por el viento (más viento cuanto más llueve) y, cerca del jugador, al llegar al suelo se convierten en
//    una salpicadura: un anillo que se abre y se apaga. Sustituye a los 3.500 trazos que movía la CPU (en la vista de
//    maqueta sigue la lluvia de antes).
//  · Chispas: en cada golpe del coche o la moto saltan chispas naranjas que botan en el suelo y se apagan.
//  · Hojas de otoño: caen de los árboles que tienes cerca, revoloteando y girando, el viento las arrastra y se quedan en
//    el suelo; al pasar con el coche, la moto o andando salen volando otra vez. Con lluvia o viento caen más.
// Sin WebGPU (motor WebGL2) no se activa nada y todo queda como antes. Con window.__PARTICULAS_OFF=true antes de jugar
// no se crean.
const GPP={ini:0,on:false};window.__GPP=GPP;
function gppIni(){if(GPP.ini)return GPP.on;GPP.ini=1;
 try{const b=R.backend;if(!b||!b.isWebGPUBackend||window.__PARTICULAS_OFF)return false;
 const T=TSL,{Fn,If,Return,instancedArray,instanceIndex,uniform,float,uint,vec2,vec3,vec4,hash,mix,smoothstep,clamp,max,min,length,normalize,cross,sin,cos,mod,uv,cameraPosition,positionGeometry,select,abs,pow}=T;
 const LT=!!window.LITE||matchMedia('(pointer:coarse)').matches;GPP.LT=LT;
 const uDt=uniform(0),uT=uniform(0),uSeed=uniform(0,'uint'),uC=uniform(new THREE.Vector3()),uPl=uniform(new THREE.Vector4(0,0,-99,0)),uPv=uniform(new THREE.Vector2()),uGy=uniform(0),uWind=uniform(new THREE.Vector2()),uRain=uniform(0),uSplR=uniform(.35),uNoche=GT.U(UW.uN);
 GPP.u={uDt,uT,uSeed,uC,uPl,uPv,uGy,uWind,uRain,uSplR};
 const rnd=k=>hash(instanceIndex.mul(uint(7)).add(uint(k)).add(uSeed.mul(uint(977))));
 const quad=()=>new THREE.PlaneGeometry(1,1);
 // ===== lluvia =====
 const NR=LT?50000:200000,S=.7,H=.8;GPP.NR=NR;
 const rp=instancedArray(NR,'vec4');      // xyz + edad de la salpicadura (0 = cayendo)
 const vel=i=>hash(i.mul(uint(13)).add(uint(5))).mul(.5).add(.8).mul(3.2);
 GPP.cRini=Fn(()=>{const i=instanceIndex;rp.element(i).assign(vec4(uC.x.add(rnd(1).sub(.5).mul(2*S)),uC.y.add(rnd(2).sub(.5).mul(H)),uC.z.add(rnd(3).sub(.5).mul(2*S)),0))})().compute(NR);
 GPP.cR=Fn(()=>{const i=instanceIndex,P=rp.element(i),p=P.toVar();
  If(p.w.greaterThan(0),()=>{p.w.addAssign(uDt);If(p.w.greaterThan(.28),()=>{p.y.assign(uC.y.add(H*.5).sub(rnd(4).mul(.12)));p.w.assign(0)})})
  .Else(()=>{p.y.subAssign(vel(i).mul(uDt));p.x.addAssign(uWind.x.mul(uDt));p.z.addAssign(uWind.y.mul(uDt));
   const cerca=length(p.xz.sub(uPl.xy)).lessThan(uSplR);
   If(p.y.lessThan(uGy).and(cerca).and(rnd(6).lessThan(.18)),()=>{p.y.assign(uGy.add(.0005));p.w.assign(1e-4)})
   .ElseIf(p.y.lessThan(uC.y.sub(H*.5)),()=>{p.y.addAssign(H)});
   If(p.y.greaterThan(uC.y.add(H*.5)),()=>{p.y.subAssign(H)})});
  p.x.assign(uC.x.add(mod(p.x.sub(uC.x).add(S),2*S)).sub(S));p.z.assign(uC.z.add(mod(p.z.sub(uC.z).add(S),2*S)).sub(S));
  P.assign(p)})().compute(NR);
 {const m=new THREE.MeshBasicNodeMaterial({transparent:true,depthWrite:false,side:THREE.DoubleSide,fog:true});
  const pa=rp.toAttribute(),c=pa.xyz,ed=pa.w,sp=hash(instanceIndex.mul(uint(13)).add(uint(5))).mul(.5).add(.8).mul(3.2);
  const g=positionGeometry,ax=normalize(vec3(uWind.x,sp.negate(),uWind.y)),vw=normalize(c.sub(cameraPosition)),lado=normalize(cross(ax,vw));
  const largo=sp.mul(.006),cae=c.add(lado.mul(g.x.mul(.00035))).add(ax.mul(g.y.negate().mul(largo)));
  const rr=ed.mul(.014).add(.001),salp=c.add(vec3(g.x.mul(rr),0,g.y.mul(rr)));
  m.positionNode=select(ed.greaterThan(0),salp,cae);
  const q=uv(),d=length(q.sub(.5)).mul(2),dist=length(c.sub(cameraPosition));
  const aCae=smoothstep(0,.5,q.y).mul(smoothstep(1,.6,q.y)).mul(.26),aSal=smoothstep(.62,.86,d).mul(smoothstep(1,.88,d)).mul(ed.div(.28).oneMinus()).mul(.32);
  m.colorNode=mix(vec3(.74,.8,.88),vec3(.86,.9,.95),select(ed.greaterThan(0),float(1),float(0))).mul(uNoche.mul(.55).oneMinus());
  m.opacityNode=select(ed.greaterThan(0),aSal,aCae).mul(uRain).mul(smoothstep(S*1.05,S*.5,dist)).mul(smoothstep(.012,.04,dist));
  const me=new THREE.Mesh(quad(),m);me.count=NR;me.frustumCulled=false;me.renderOrder=6;me.visible=false;me.name='lluvia_gpu';scene.add(me);GPP.mR=me}
 // ===== chispas =====
 const NC=LT?2048:8192,MC=256;GPP.NC=NC;GPP.MC=MC;GPP.headC=0;GPP.cntC=0;
 const cp=instancedArray(NC,'vec4'),cv=instancedArray(NC,'vec4'),csp=instancedArray(MC,'vec4'),csv=instancedArray(MC,'vec4');GPP.csp=csp;GPP.csv=csv;
 const uCntC=uniform(0,'uint'),uHeadC=uniform(0,'uint');GPP.u.uCntC=uCntC;GPP.u.uHeadC=uHeadC;
 GPP.cCsal=Fn(()=>{const i=instanceIndex;If(i.greaterThanEqual(uCntC),()=>{Return()});const j=uHeadC.add(i).mod(uint(NC));cp.element(j).assign(csp.element(i));cv.element(j).assign(csv.element(i))})().compute(MC);
 GPP.cC=Fn(()=>{const i=instanceIndex,P=cp.element(i),V=cv.element(i),p=P.toVar(),v=V.toVar();If(p.w.lessThanEqual(0),()=>{Return()});
  p.w.subAssign(uDt);v.y.subAssign(uDt.mul(.9));v.xz.mulAssign(float(1).sub(uDt.mul(.8)));p.xyz.addAssign(v.xyz.mul(uDt));
  If(p.y.lessThan(v.w),()=>{p.y.assign(v.w);v.y.assign(v.y.abs().mul(.35));v.xz.mulAssign(.6)});
  P.assign(p);V.assign(v)})().compute(NC);
 {const m=new THREE.MeshBasicNodeMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide});
  const pa=cp.toAttribute(),va=cv.toAttribute(),c=pa.xyz,g=positionGeometry,vv=va.xyz,spd=length(vv),ax=vv.div(max(spd,1e-4));
  const lado=normalize(cross(ax,normalize(c.sub(cameraPosition)))),viva=smoothstep(0,.15,pa.w);
  m.positionNode=c.add(lado.mul(g.x.mul(.0007))).add(ax.mul(g.y.mul(spd.mul(.03).add(.0015)))).mul(select(pa.w.greaterThan(0),float(1),float(0)));
  const q=uv();m.colorNode=mix(vec3(1,.32,.06),vec3(1,.9,.55),smoothstep(.2,.8,pa.w)).mul(2.2);
  m.opacityNode=smoothstep(0,.5,q.y).mul(viva);
  const me=new THREE.Mesh(quad(),m);me.count=NC;me.frustumCulled=false;me.renderOrder=7;me.visible=false;me.name='chispas_gpu';scene.add(me);GPP.mC=me}
 // ===== hojas =====
 const NH=LT?4096:16384,MH=512;GPP.NH=NH;GPP.MH=MH;GPP.headH=0;GPP.cntH=0;
 const hp=instancedArray(NH,'vec4'),hv=instancedArray(NH,'vec4'),he=instancedArray(NH,'vec4'),hsp=instancedArray(MH,'vec4'),hsv=instancedArray(MH,'vec4');GPP.hsp=hsp;GPP.hsv=hsv;
 const uCntH=uniform(0,'uint'),uHeadH=uniform(0,'uint');GPP.u.uCntH=uCntH;GPP.u.uHeadH=uHeadH;
 GPP.cHsal=Fn(()=>{const i=instanceIndex;If(i.greaterThanEqual(uCntH),()=>{Return()});const j=uHeadH.add(i).mod(uint(NH)),s=hsv.element(i);
  hp.element(j).assign(hsp.element(i));hv.element(j).assign(vec4(0,0,0,0));he.element(j).assign(vec4(s.x,rnd(1).mul(6.28),rnd(2).mul(6).sub(3),rnd(3)))})().compute(MH);
 GPP.cH=Fn(()=>{const i=instanceIndex,P=hp.element(i),V=hv.element(i),E=he.element(i),p=P.toVar(),v=V.toVar(),e=E.toVar();If(p.w.lessThanEqual(0),()=>{Return()});
  p.w.subAssign(uDt);
  const dPl=p.xz.sub(uPl.xy),lPl=length(dPl);
  If(v.w.lessThan(.5),()=>{   // en el aire: cae despacio, revolotea y gira
   const ph=e.w.mul(40).add(uT.mul(e.z.abs().add(1.5)));
   v.y.assign(mix(v.y,float(-.028).add(sin(ph).mul(.012)),min(1,uDt.mul(2))));
   v.xz.assign(mix(v.xz,uWind.mul(.9).add(vec2(cos(ph),sin(ph.mul(.7))).mul(.02)),min(1,uDt.mul(1.5))));
   p.xyz.addAssign(v.xyz.mul(uDt));e.y.addAssign(e.z.mul(uDt));
   If(p.y.lessThanEqual(e.x),()=>{p.y.assign(e.x.add(.0004));v.assign(vec4(0,0,0,1))})})
  .Else(()=>{If(lPl.lessThan(uPl.w).and(uPl.z.greaterThan(.05)),()=>{const dir=dPl.div(max(lPl,1e-5));
    v.assign(vec4(dir.x.mul(uPl.z.mul(.1)).add(uPv.x.mul(.5)),uPl.z.mul(.07).add(.02).mul(rnd(8).add(.5)),dir.y.mul(uPl.z.mul(.1)).add(uPv.y.mul(.5)),0));p.y.addAssign(.001)})});
  P.assign(p);V.assign(v);E.assign(e)})().compute(NH);
 {const m=new THREE.MeshBasicNodeMaterial({side:THREE.DoubleSide});
  const pa=hp.toAttribute(),va=hv.toAttribute(),ea=he.toAttribute(),c=pa.xyz,g=positionGeometry,a=ea.y,tam=ea.w.mul(.002).add(.0035);
  const enAire=va.w.lessThan(.5),inc=select(enAire,sin(a.mul(1.3)).mul(1.1),float(0));
  const n=normalize(vec3(sin(inc).mul(cos(a)),cos(inc),sin(inc).mul(sin(a)))),uu=normalize(cross(n,vec3(sin(a).negate(),.0001,cos(a)))),vv=cross(uu,n);
  m.positionNode=c.add(uu.mul(g.x.mul(tam))).add(vv.mul(g.y.mul(tam))).mul(select(pa.w.greaterThan(0),float(1),float(0)));
  const q=uv().sub(.5).mul(2),forma=abs(q.x).lessThan(pow(max(float(1).sub(q.y.mul(q.y)),0),.8).mul(.55));
  m.maskNode=forma.and(pa.w.greaterThan(0));
  const t=ea.w,col=select(t.lessThan(.35),mix(vec3(.85,.62,.14),vec3(.82,.4,.1),t.div(.35)),select(t.lessThan(.75),mix(vec3(.62,.3,.1),vec3(.42,.26,.12),t.sub(.35).div(.4)),mix(vec3(.4,.48,.14),vec3(.55,.5,.16),t.sub(.75).div(.25))));
  const vena=smoothstep(.06,0,abs(q.x)).mul(.25);
  m.colorNode=col.mul(float(1).sub(vena)).mul(abs(n.y).mul(.25).add(.6)).mul(uNoche.mul(.75).oneMinus()).mul(smoothstep(0,2,pa.w).mul(.3).add(.7));
  const me=new THREE.Mesh(quad(),m);me.count=NH;me.frustumCulled=false;me.visible=false;me.name='hojas_gpu';scene.add(me);GPP.mH=me}
 // todo vacío al empezar
 R.compute(Fn(()=>{cp.element(instanceIndex).w.assign(0)})().compute(NC));R.compute(Fn(()=>{hp.element(instanceIndex).w.assign(0)})().compute(NH));
 GPP.rIni=0;GPP.tArb=-9;GPP.arb=[];GPP.accH=0;GPP.on=true;return true}catch(e){console.warn('partículas GPU',e);GPP.on=false;return false}}
// chispas de un golpe (se llama desde golpe())
function gppChispas(){if(!GPP.on||!driving||MODO==='pie'||MODO==='nado')return;const A=GPP.csp.value.array,B=GPP.csv.value.array,n=GPP.LT?60:160;
 const fx=Math.cos(P.a),fz=-Math.sin(P.a),v=Math.abs(P.v||0),y=UCUT.uCar.value.y-.03,x0=P.x+fx*.035,z0=P.y+fz*.035;
 for(let k=0;k<n&&GPP.cntC<GPP.MC;k++){const o=GPP.cntC*4,a=Math.random()*6.283,s=.15+Math.random()*.45+v*.3;
  A[o]=x0+(Math.random()-.5)*.02;A[o+1]=y+.004+Math.random()*.01;A[o+2]=z0+(Math.random()-.5)*.02;A[o+3]=.35+Math.random()*.7;
  B[o]=Math.cos(a)*s*.6-fx*v*.4;B[o+1]=.12+Math.random()*.35;B[o+2]=Math.sin(a)*s*.6-fz*v*.4;B[o+3]=y;GPP.cntC++}}
// árboles cercanos (de las mallas de árboles ya cargadas) para soltar hojas
function gppArboles(){const L=[],px=P.x,pz=P.y,R2=.9*.9;
 scene.traverse(o=>{if(!o.isInstancedMesh||!o.visible||!o.material||!o.material.userData||!o.material.userData.hj)return;const a=o.instanceMatrix.array;
  for(let i=0;i<o.count;i++){const k=i*16,x=a[k+12],z=a[k+14],dx=x-px,dz=z-pz;if(dx*dx+dz*dz>R2)continue;
   const h=Math.hypot(a[k+4],a[k+5],a[k+6]),r=Math.hypot(a[k],a[k+1],a[k+2]);L.push([x,a[k+13],z,h,r])}});GPP.arb=L}
function gppTick(dt){if(!GPP.ini&&driving)gppIni();if(!GPP.on)return;const rain=GPP.rain||0;
 const u=GPP.u,vis=driving&&!RACE.on;GPP.mC.visible=GPP.mH.visible=vis;
 if(!vis||!dt){GPP.mR.visible=false;GPP.cntC=GPP.cntH=0;return}
 dt=Math.min(dt,1/20);u.uDt.value=dt;u.uT.value+=dt;u.uSeed.value=(Math.random()*16777215)|0;
 const cp=pcam.position;u.uC.value.copy(cp);const gy=UCUT.uCar.value.y-.03;u.uGy.value=gy;u.uSplR.value=cp.y-gy<.6?.35:0;
 const sp=Math.abs(P.v||0),fx=Math.cos(P.a),fz=-Math.sin(P.a),M=MODO;
 const rad=M==='pie'?.006:(M==='coche'?.025:(M==='moto'||M==='motoc'?.012:0));
 u.uPl.value.set(P.x,P.y,rad?Math.min(1,sp/.5):0,rad);u.uPv.value.set(fx*(P.v||0)*.3,fz*(P.v||0)*.3);
 const vto=.08+.5*rain;u.uWind.value.set(.82*vto,.57*vto);
 // lluvia
 u.uRain.value=Math.min(1,rain)*(1-.4*(CIELO.nf||0));const llueve=rain>.02;GPP.mR.visible=llueve;
 if(llueve){GPP.mR.count=Math.max(1000,Math.floor(GPP.NR*Math.min(1,rain)));if(!GPP.rIni){R.compute(GPP.cRini);GPP.rIni=1}R.compute(GPP.cR)}else GPP.rIni=0;
 // chispas
 if(GPP.cntC){u.uCntC.value=GPP.cntC;u.uHeadC.value=GPP.headC;GPP.csp.value.needsUpdate=GPP.csv.value.needsUpdate=true;R.compute(GPP.cCsal);GPP.headC=(GPP.headC+GPP.cntC)%GPP.NC;GPP.cntC=0}
 R.compute(GPP.cC);
 // hojas: caen de los árboles cercanos (más con viento y lluvia)
 if(u.uT.value-GPP.tArb>2.5){GPP.tArb=u.uT.value;try{gppArboles()}catch(e){GPP.arb=[]}}
 const A=GPP.arb;if(A.length){GPP.accH+=dt*(GPP.LT?14:40)*(1+rain*1.5)*Math.min(1,A.length/12);
  const HA=GPP.hsp.value.array,HB=GPP.hsv.value.array;
  while(GPP.accH>=1&&GPP.cntH<GPP.MH){GPP.accH--;const t=A[(Math.random()*A.length)|0],o=GPP.cntH*4,an=Math.random()*6.283,rr=t[4]*(.3+Math.random()*.8);
   HA[o]=t[0]+Math.cos(an)*rr;HA[o+1]=t[1]+t[3]*(.75+Math.random()*.45);HA[o+2]=t[2]+Math.sin(an)*rr;HA[o+3]=25+Math.random()*20;HB[o]=t[1]+.0004;GPP.cntH++}
  GPP.accH=Math.min(GPP.accH,4)}
 if(GPP.cntH){u.uCntH.value=GPP.cntH;u.uHeadH.value=GPP.headH;GPP.hsp.value.needsUpdate=GPP.hsv.value.needsUpdate=true;R.compute(GPP.cHsal);GPP.headH=(GPP.headH+GPP.cntH)%GPP.NH;GPP.cntH=0}
 R.compute(GPP.cH)}
// ---------- fin de gpu_particulas.js
