// ---------- gpu.html: cielo y agua en TSL (gpu_tsl.js) ----------
// Mismo dibujo que los shaders GLSL de index.html (cielo con sol, luna, estrellas y nubes; mar con oleaje, color según la
// profundidad, espuma de orilla, borreguillos, reflejo del cielo y destellos del sol), escrito en TSL para que funcione
// con WebGPU (y con WebGL2 si no hay WebGPU). Los bucles se desenrollan en JavaScript.
const GT={};
GT.U=o=>TSL.uniform(o.value).onRenderUpdate(()=>o.value);
GT.ini=()=>{if(GT.h21)return;const{Fn,vec2,float,floor,fract,sin,dot,mix}=TSL;
 // funciones de verdad en el shader (setLayout): menos código y sin mezclar nudos entre materiales
 GT.h21=Fn(([p])=>fract(sin(dot(p,vec2(127.1,311.7))).mul(43758.5453))).setLayout({name:'gtH21',type:'float',inputs:[{name:'p',type:'vec2'}]});
 GT.vn=Fn(([p])=>{const i=floor(p).toVar(),f0=fract(p).toVar(),f=f0.mul(f0).mul(float(3).sub(f0.mul(2))).toVar();
  return mix(mix(GT.h21(i),GT.h21(i.add(vec2(1,0))),f.x),mix(GT.h21(i.add(vec2(0,1))),GT.h21(i.add(vec2(1,1))),f.x),f.y)}).setLayout({name:'gtVn',type:'float',inputs:[{name:'p',type:'vec2'}]});
 GT.fbm=Fn(([p0])=>{const p=vec2(p0).toVar(),s=float(0).toVar();let a=.5;for(let i=0;i<5;i++){s.addAssign(GT.vn(p).mul(a));p.assign(p.mul(2.03).add(vec2(1.7,9.2)));a*=.5}return s}).setLayout({name:'gtFbm',type:'float',inputs:[{name:'p0',type:'vec2'}]})};
GT.ini2=()=>{if(GT.surf)return;const{Fn,vec2,vec3,vec4,float,floor,fract,sin,mix,smoothstep,max,min,clamp,length,texture,If,select}=TSL;
 if(!ARF.rt){ARF.rt=new THREE.RenderTarget(16,16,{type:THREE.HalfFloatType});ARF.rt.texture.generateMipmaps=false;URF.uRf.value=ARF.rt.texture}
 const uCoR=GT.U(UCO.uCoR),tCos=UCO.uCos.value;
 GT.surfCos=w=>{const uv=w.sub(uCoR.xy).div(uCoR.zw),den=uv.x.greaterThanEqual(0).and(uv.y.greaterThanEqual(0)).and(uv.x.lessThanEqual(1)).and(uv.y.lessThanEqual(1));return select(den,texture(tCos,uv).a,float(0))};
 GT.surfK=p=>{let m=float(0);for(const[x,z,r,w]of SURF.spots)m=max(m,smoothstep(r*.55,r,length(p.sub(vec2(x,z)))).oneMinus().mul(w));return m};
 // x = altura (0..1), y = espuma, z = cara empinada de la ola (antes de romper)
 GT.surf=Fn(([p,cs,t])=>{const n=GT.vn(p.mul(.55)),n2=GT.vn(p.mul(1.7).add(3));
  const q=cs.div(.15).sub(t.div(9)).add(n.mul(1.6)),f=fract(q);
  const set=sin(q.mul(.83).add(n2.mul(2))).mul(.45).add(.55);
  const br=smoothstep(.58,.72,cs.add(n2.sub(.5).mul(.14)));
  const env=smoothstep(.16,.6,cs).mul(br.mul(.55).oneMinus()).mul(smoothstep(.88,.975,cs).oneMinus()).mul(set);
  const fr=smoothstep(0,.07,f).oneMinus(),h=max(f.mul(f).mul(f),fr).mul(env);
  const lip=smoothstep(.48,.64,cs.add(n.sub(.5).mul(.1))).mul(smoothstep(.9,1,f).add(smoothstep(0,.035,f).oneMinus())).mul(min(env.mul(1.6),1));
  const ww=br.mul(smoothstep(.35,.97,f).mul(.85).add(fr)).mul(smoothstep(.93,.985,cs).oneMinus()).mul(set.mul(.5).add(.5));
  return vec3(h,clamp(lip.mul(1.4).add(ww),0,1),clamp(fr.mul(br.oneMinus()).mul(env).mul(1.5),0,1).sub(h.oneMinus().mul(.35).mul(env).mul(br.oneMinus())))}).setLayout({name:'gtSurf',type:'vec3',inputs:[{name:'p',type:'vec2'},{name:'cs',type:'float'},{name:'t',type:'float'}]});
 // (gx, gz, espuma, cara) de la rompiente; fuera de Patos no se calcula
 GT.surfF=(p,cs,aw,t)=>Fn(()=>{const r=vec4(0).toVar(),sm=GT.surfK(p).mul(aw).mul(smoothstep(.97,.995,cs).oneMinus());
  If(sm.greaterThan(.002),()=>{const e=.025,S0=GT.surf(p,GT.surfCos(p),t),px=p.add(vec2(e,0)),pz=p.add(vec2(0,e));
   const hx=GT.surf(px,GT.surfCos(px),t).x,hz=GT.surf(pz,GT.surfCos(pz),t).x,A=GT.U(USURF.uSurfA);
   r.assign(vec4(vec2(hx.sub(S0.x),hz.sub(S0.x)).div(e).mul(A).mul(sm),S0.y.mul(sm),S0.z.mul(sm)))});return r})()};   // sin setLayout: usa uniforms y la textura de la costa, que en una función aparte no se declaran
function gpuCielo(){GT.ini();const{vec2,vec3,float,normalize,max,mix,pow,dot,smoothstep,step,sin,floor,select,positionLocal}=TSL;
 const uSun=GT.U(SKYU.uSun),uZen=GT.U(SKYU.uZen),uHor=GT.U(SKYU.uHor),uT=GT.U(SKYU.uT),uNight=GT.U(SKYU.uNight),uDusk=GT.U(SKYU.uDusk),uCov=GT.U(SKYU.uCov);
 const d=normalize(positionLocal),y=max(d.y,0),sd=normalize(uSun),dia=uNight.oneMinus();
 let col=mix(uHor,uZen,pow(y,.5));
 const cs=max(dot(d,sd),0);
 col=col.add(vec3(1,.62,.32).mul(pow(cs,6)).mul(uDusk.mul(.6).add(.25)).mul(dia));                  // halo del sol
 col=col.add(vec3(1,.96,.86).mul(smoothstep(.999,.9996,cs)).mul(dia));                                // disco del sol
 const cm=max(dot(d,sd.negate()),0);col=col.add(vec3(.85,.88,1).mul(smoothstep(.9993,.9997,cm)).mul(uNight));   // luna
 const sp=floor(d.xz.div(d.y.add(.25)).mul(70));const st=step(.9965,GT.h21(sp)).mul(sin(uT.mul(2).add(GT.h21(sp.add(3)).mul(40))).mul(.5).add(.5));
 col=col.add(vec3(st).mul(uNight).mul(smoothstep(.02,.25,y)));                                         // estrellas
 const cp=d.xz.div(d.y.add(.12)).mul(1.4).add(vec2(uT.mul(.01),uT.mul(.004)));
 const c=smoothstep(float(.5).sub(uCov.mul(.42)),float(.8).sub(uCov.mul(.3)),GT.fbm(cp)).mul(smoothstep(0,.1,y));
 let cl=mix(vec3(1,.99,.97),vec3(1,.66,.52),uDusk);cl=mix(cl,vec3(.16,.18,.28),uNight);
 cl=cl.mul(GT.fbm(cp.mul(2.3).add(3)).mul(.3).add(.78));cl=mix(cl,cl.mul(vec3(.62,.64,.70)),uCov.mul(.8));
 col=mix(col,cl,c.mul(.92));
 const m=new THREE.MeshBasicNodeMaterial({side:THREE.BackSide,depthWrite:false,depthTest:false,fog:false});
 m.colorNode=select(d.y.lessThan(0),uHor,col);return m}
function gpuAgua(glob,surfM){GT.ini();const{vec2,vec3,float,normalize,max,min,mix,pow,dot,smoothstep,sin,cos,exp,abs,clamp,select,length,fwidth,texture,reflect,positionWorld,cameraPosition,transformNormalToView}=TSL;
 const LT=!!window.LITE,uT=GT.U(UW.uT),uN=GT.U(UW.uN),uSun=GT.U(SKYU.uSun),uZen=GT.U(SKYU.uZen),uHor=GT.U(SKYU.uHor),uCoR=GT.U(UCO.uCoR);
 const p=positionWorld.xz,uq=p.sub(uCoR.xy).div(uCoR.zw);
 const dentro=uq.x.greaterThanEqual(0).and(uq.y.greaterThanEqual(0)).and(uq.x.lessThanEqual(1)).and(uq.y.lessThanEqual(1));
 const C=texture(UCO.uCos.value,uq);GT.ini2();const cs=select(dentro,C.r,float(0)),aw=select(dentro,C.g,float(1)).mul(smoothstep(.985,.999,cs).oneMinus());
 const fw=max(length(fwidth(p)),1e-5);
 const calma=smoothstep(.3,.75,GT.vn(p.mul(.35).add(vec2(uT.mul(.012),uT.mul(-.008)))));
 // oleaje: trenes de olas con la velocidad real de cada longitud de onda (1 unidad ≈ 100 m)
 const wp=GT.vn(p.mul(.45).add(uT.mul(.01))).mul(2).sub(1);let rx=float(0),gr=vec2(0,0),sa=float(0),ang=.22,L=1.15;
 for(let i=0;i<(LT?5:8);i++){const dx=Math.cos(ang),dz=Math.sin(ang),k=6.2832/L,w=Math.sqrt(.098*k)*1.15;
  let A=float(.075/k).mul(smoothstep(2,6,float(L).div(fw))).mul(mix(.35,1,aw));if(i>2)A=A.mul(mix(.3,1,calma));
  A=A.mul(GT.vn(p.mul(.6+i*.4).add(i*3.1)).mul(.9).add(.55));
  const ph=p.x.mul(dx).add(p.y.mul(dz)).mul(k).sub(uT.mul(w)).add(i*1.7).add(wp.mul(1.2+i*.35)),e=exp(sin(ph).sub(1));
  rx=rx.add(A.mul(e));const g=A.mul(e).mul(cos(ph)).mul(k);gr=gr.add(vec2(g.mul(dx),g.mul(dz)));sa=sa.add(A);ang+=2.39996;L*=.66}
 const Ox=select(sa.greaterThan(0),rx.div(max(sa,1e-6)),float(0));
 if(!LT){const rz=mix(.25,1,calma).mul(smoothstep(1.5,5,float(.045).div(fw))),q=p.mul(45).add(vec2(uT.mul(.9),uT.mul(-.6))),n0=GT.vn(q),nx=GT.vn(q.add(vec2(.35,0))),nz=GT.vn(q.add(vec2(0,.35)));
  gr=gr.add(vec2(nx.sub(n0),nz.sub(n0)).div(.35).mul(45*.0016).mul(rz))}               // rizos de viento
 // rompiente de Patos (edit_olas.py): pendiente, espuma y cara de la ola
 const SV=GT.surfF(p,cs,aw,uT);gr=gr.add(SV.xy);const aS0=SV.z,sFace=SV.w;
 const aN=normalize(vec3(gr.x.negate(),1,gr.y.negate()));
 // color: ría honda, media, poco hondo turquesa y arena bajo el agua junto a la playa
 const prof=smoothstep(.12,.8,cs).oneMinus(),big=GT.vn(p.mul(.12).add(uT.mul(.004)));
 let col=mix(vec3(.012,.080,.100),vec3(.008,.042,.072),smoothstep(0,.6,prof).mul(big.mul(.3).add(.7)));
 col=mix(col,vec3(.030,.200,.195),smoothstep(.3,.7,cs));col=mix(col,vec3(.13,.36,.29),smoothstep(.7,.9,cs).mul(aw));
 col=mix(col,vec3(.04,.10,.09),aw.oneMinus().mul(.6));
 // cáusticas en el agua poco honda: la luz que enfocan las olas baila sobre la arena del fondo (se mueven con el oleaje;
 // con nubes, lluvia o de noche se apagan; de lejos se funden para no hacer ruido)
 const cSol=smoothstep(.02,.35,normalize(uSun).y).mul(uN.oneMinus()).mul(GT.U(SKYU.uCov).mul(.85).oneMinus()).mul(GT.U(UMO.uWet).mul(.7).oneMinus());
 const zc=smoothstep(.6,.8,cs).mul(smoothstep(.985,.94,cs)).mul(aw).mul(smoothstep(.004,.0013,fw)).mul(cSol);
 const cq=p.add(gr.mul(.006)).div(.028),cT=uT.mul(.7),ca1=GT.caus(cq,cT);
 const caR=LT?ca1:ca1.mul(.6).add(GT.caus(cq.mul(1.37).add(.41),cT.mul(.83).add(5)).mul(.45)),caB=LT?caR:caR.mul(.85).add(GT.caus(cq.add(.012),cT).mul(.15));   // un poco de arcoíris en los bordes
 col=col.add(vec3(caR.mul(.5),caR.mul(.68),caB.mul(.56)).mul(zc).mul(.8));
 col=col.add(vec3(0,.018,.016).mul(smoothstep(.6,.95,Ox)).mul(uN.oneMinus()));
 // espuma de orilla (franjas que van y vienen) y borreguillos mar adentro
 const fb=sin(cs.mul(34).sub(uT.mul(1.6)).add(GT.vn(p.mul(4)).mul(4)));
 const tx=smoothstep(.15,.6,GT.vn(p.mul(20).add(vec2(uT.mul(.35),uT.mul(-.2)))).mul(.6).add(GT.vn(p.mul(52).sub(uT.mul(.3))).mul(.4)).add(.1));
 const foam=smoothstep(.86,.975,cs).add(smoothstep(.74,.94,cs).mul(smoothstep(.65,.97,fb)).mul(.7)).mul(tx).mul(aw);
 const whc=smoothstep(.9,.99,Ox).mul(smoothstep(.72,.9,GT.vn(p.mul(1.3).add(vec2(uT.mul(.1),uT.mul(.04)))))).mul(smoothstep(.5,.8,GT.vn(p.mul(7).add(uT.mul(.2))))).mul(calma.oneMinus()).mul(prof).mul(.45);
 col=mix(col,vec3(.03,.27,.24),max(sFace,0).mul(.75).mul(uN.mul(.7).oneMinus()));col=col.mul(min(sFace,0).mul(.9).add(1));
 const aS=clamp(aS0.mul(tx.mul(.8).add(.45)),0,1);col=mix(col,vec3(.88,.91,.93),aS.mul(uN.mul(.6).oneMinus()));
 const aF=clamp(foam.add(whc.mul(tx)),0,1);col=mix(col,vec3(.78,.82,.84),aF.mul(uN.mul(.6).oneMinus()));const aFS=max(aF,aS);
 // reflejo del cielo (Fresnel) y destellos del sol
 const N=normalize(mix(aN,vec3(0,1,0),aF)),V=normalize(cameraPosition.sub(positionWorld)),nv=max(dot(N,V),0);
 const R0=reflect(V.negate(),N),Rf=vec3(R0.x,abs(R0.y),R0.z);
 const sky=mix(uHor,uZen,smoothstep(0,.5,Rf.y).mul(.65).add(.35)).mul(.82);
 // reflejo de la ciudad, los barcos y los montes: foto desde la cámara reflejada bajo el agua (aguaReflejo)
 const uRfOn=GT.U(URF.uRfOn),uRfM=GT.U(URF.uRfM),rcp=uRfM.mul(TSL.vec4(positionWorld,1)),ru=clamp(rcp.xy.div(rcp.w).add(N.xz.mul(.06)),.001,.999),rc=texture(ARF.rt.texture,ru);
 const rfl=select(uRfOn.greaterThan(.5),mix(sky,rc.rgb.mul(.92),clamp(rc.a,0,1)),sky);
 const F=min(pow(nv.oneMinus(),5).mul(.98).add(.02).mul(1.2).add(.07).add(calma.mul(.06)),mix(.58,.74,uRfOn)).mul(aFS.oneMinus());
 const Ls=normalize(uSun),sd=max(dot(Rf,Ls),0),up=smoothstep(-.02,.12,Ls.y).mul(uN.oneMinus());
 const sc=mix(vec3(1,.5,.25),vec3(1,.95,.86),smoothstep(.05,.4,Ls.y));
 const glint=sc.mul(pow(sd,700).mul(10).add(pow(sd,60).mul(.35))).mul(up).mul(aFS.oneMinus());
 const m=new THREE.MeshStandardNodeMaterial({roughness:.6,metalness:0});
 m.colorNode=col.mul(F.oneMinus());m.normalNode=transformNormalToView(normalize(mix(aN,vec3(0,1,0),aF.mul(.8))));m.emissiveNode=rfl.mul(F).add(glint);
 if(glob){m.alphaTest=.5;m.opacityNode=select(cs.greaterThan(.97).or(C.b.greaterThan(.5).and(dentro)),float(0),float(1))}   // la lámina global no tapa la tierra
 if(surfM){m.alphaTest=.5;m.opacityNode=select(cs.greaterThan(.985),float(0),float(1));m.polygonOffset=true;m.polygonOffsetFactor=-2;m.polygonOffsetUnits=-2;
  const{positionLocal,modelWorldMatrix,vec4}=TSL,wp=modelWorldMatrix.mul(vec4(positionLocal,1)).xz,sc2=GT.surfCos(wp),k2=GT.surfK(wp);   // la malla fina de Patos sube y baja con cada ola
  m.positionNode=positionLocal.add(vec3(0,GT.surf(wp,sc2,uT).x.mul(GT.U(USURF.uSurfA)).mul(k2).mul(smoothstep(.97,.995,sc2).oneMinus()),0))}
 return m}
// ---------- materiales GLSL sueltos → TSL (cielo de los reflejos, haz de los faros, montes y mar lejanos, bajo el agua) ----------
// window.GPUMAT (en la cabecera) pregunta aquí antes de poner el sustituto invisible; se reconoce cada shader por un trozo suyo.
GT.pxW=null;   // tamaño en el mundo de un píxel a 1 u de distancia (para pasar gl_PointSize a sprites)
function gpuShaderTSL(p){try{GT.ini();const T=TSL,{vec2,vec3,vec4,float,normalize,max,min,mix,pow,dot,smoothstep,step,sin,cos,abs,clamp,select,length,positionLocal,positionWorld,normalWorld,cameraPosition,uv,refract,mod,exp,atan}=T;
 const fs=p.fragmentShader||'',vs=p.vertexShader||'',u=p.uniforms||{},U=k=>GT.U(u[k]);
 const basic=(o)=>{const m=new THREE.MeshBasicNodeMaterial(Object.assign({side:p.side??THREE.FrontSide,transparent:!!p.transparent,depthWrite:p.depthWrite!==false,depthTest:p.depthTest!==false,blending:p.blending??THREE.NormalBlending,fog:false},o||{}));m.uniforms=u;return m};
 if(fs.includes('uSuelo')){                       // cielo para el reflejo de los coches (envCoches)
  const d=normalize(positionLocal),uZen=U('uZen'),uHor=U('uHor'),uSun=U('uSun'),uSunC=U('uSunC'),uSuelo=U('uSuelo');
  let c=select(d.y.greaterThan(0),mix(uHor,uZen,pow(max(d.y,0),.6)),mix(uHor.mul(.6),uSuelo,smoothstep(0,.25,d.y.negate())));
  const s_=max(dot(d,normalize(uSun)),0);c=c.add(uSunC.mul(pow(s_,600).mul(30).add(pow(s_,12).mul(.5))).mul(step(0,uSun.y.add(.05))));
  c=c.mul(smoothstep(.35,0,abs(d.y.sub(.08))).mul(.35).oneMinus());const m=basic();m.colorNode=c;return m}
 if(vs.includes('vL=abs(position.x)/3.')){        // haz giratorio de los faros
  const a=pow(clamp(abs(positionLocal.x).div(3).oneMinus(),0,1),1.6).mul(U('uO'));const m=basic();m.colorNode=vec3(1,.93,.72).mul(a);m.opacityNode=a;return m}
 if(fs.includes('neblina(')){                      // montes del fondo y mar lejano (vigo_fondo.json)
  const uCam=U('uCam'),uNear=U('uNear'),uCorte=U('uCorte'),uHor=U('uHor'),uZen=U('uZen'),uNight=U('uNight'),uSun=U('uSun'),W=positionWorld,d=W.xz.sub(uCam.xz).length();
  const neb=c=>{const h=smoothstep(uNear,uNear.add(160),d),aire=mix(uHor,uZen,.35).mul(vec3(.82,.88,1)).mul(uNight.mul(.7).oneMinus());return mix(c,aire,clamp(h.mul(.5).add(.12),0,.65))};
  let c;if(fs.includes('vec3(.30,.40,.26)')){const y=W.y,n=normalize(normalWorld);c=mix(vec3(.30,.40,.26),vec3(.40,.44,.34),smoothstep(1.2,3.5,y));c=mix(c,vec3(.52,.5,.47),smoothstep(3.6,5,y).mul(smoothstep(.6,.3,n.y)));
   c=c.mul(max(dot(n,normalize(uSun.add(vec3(0,.2,0)))),0).mul(.5).add(.55)).mul(uNight.mul(.75).oneMinus())}
  else c=mix(vec3(.16,.33,.45),vec3(.25,.45,.55),.5).mul(uNight.mul(.8).oneMinus());
  const m=basic();m.colorNode=neb(c);m.alphaTest=.5;m.opacityNode=select(d.lessThan(uNear).or(W.y.lessThan(uCorte)),float(0),float(1));return m}
 if(fs.includes('refract(V,-N,1.333)')){           // la superficie vista desde abajo (ventana de Snell)
  const uT=U('uT'),uNf=U('uNf'),uZen=U('uZen'),uHor=U('uHor'),uSun=U('uSun'),uFog=U('uFog'),W=positionWorld,V=normalize(W.sub(cameraPosition)),q=W.xz;
  const wv=pp=>{const p2=mod(pp,10);return GT.vn(p2.mul(40).add(vec2(uT.mul(.7),uT.mul(.3)))).mul(.6).add(GT.vn(p2.mul(95).sub(vec2(uT.mul(.9),uT.mul(-.5)))).mul(.4))};
  const e=.002,h0=wv(q),g=vec2(wv(q.add(vec2(e,0))).sub(h0),wv(q.add(vec2(0,e))).sub(h0)).div(e).mul(.004),N=normalize(vec3(g.x.negate(),1,g.y.negate())),Tr=refract(V,N.negate(),1.333),dd=W.sub(cameraPosition).length(),day=uNf.mul(.9).oneMinus();
  const tot=uFog.mul(h0.mul(.25).add(.55)).add(vec3(0,.03,.03).mul(smoothstep(.6,.9,h0)).mul(day));
  const sk=mix(uHor,uZen,smoothstep(0,.7,Tr.y)),sd=max(dot(Tr,normalize(uSun)),0),sun=pow(sd,300).mul(12).add(pow(sd,12).mul(.4)),edge=pow(clamp(Tr.y,0,1).oneMinus(),6);
  let win=sk.mul(edge.mul(.5).oneMinus().add(.15)).mul(day).add(vec3(1,.97,.9).mul(sun).mul(day).mul(step(0,uSun.y)));win=mix(win,uFog.mul(1.6),edge.mul(.6));
  const col=mix(select(dot(Tr,Tr).lessThan(.01),tot,win),uFog,smoothstep(.15,1.3,dd));const m=basic({transparent:true,depthWrite:false});m.colorNode=col;m.opacityNode=float(.97);return m}
 if(fs.includes('vec3(.7,1.,.92)')){               // rayos de luz bajo el agua
  const uT=U('uT'),uNf=U('uNf'),x=uv().x,y=uv().y,ed=smoothstep(0,.4,x).mul(smoothstep(1,.6,x)),o=T.modelWorldMatrix.element(3).xyz,W=positionWorld;
  const st=sin(x.mul(21).add(uT.mul(.5)).add(o.x.mul(40))).mul(.5).add(.5).mul(sin(x.mul(8.3).sub(uT.mul(.33)).add(o.z.mul(31))).mul(.5).add(.5)).mul(.65).add(.35),dd=W.sub(cameraPosition).length();
  const a=ed.mul(st).mul(pow(y,1.8)).mul(smoothstep(.04,.18,dd)).mul(smoothstep(.5,1.3,dd).oneMinus()).mul(sin(uT.mul(.6).add(o.x.mul(17))).mul(.5).add(.5)).mul(.2).mul(uNf.mul(.95).oneMinus());
  const m=basic();m.colorNode=vec3(.7,1,.92).mul(a);m.opacityNode=float(1);return m}
 // nubes de puntos (gl_PointSize): se devuelven como sprites; gpuPoints los monta al crear THREE.Points
 const pts=GT.ptsKind(fs,vs);if(pts){const m=new THREE.SpriteNodeMaterial({transparent:true,depthWrite:false,blending:p.blending??THREE.NormalBlending,fog:false});m.uniforms=u;m.gpuPts=pts;return m}
 }catch(e){console.warn('shader TSL',e)}return null}
window.GPU_TSLMAT=gpuShaderTSL;
GT.ptsKind=(fs,vs)=>{const T=TSL,{vec2,vec3,vec4,float,max,min,mix,pow,dot,smoothstep,step,sin,cos,abs,clamp,select,length,fract,exp,mod,atan,uv,cameraPosition,cameraViewMatrix,modelViewMatrix}=T;
 // A(nombre): atributo por instancia; ctx: {u(k), pxW}. Devuelve {pos (local), px (tamaño en píxeles), col, a}
 const r2=()=>uv().sub(.5).length().mul(2);
 if(vs.includes('attribute vec3 aP;attribute float aH'))return(A,U)=>{const aP=A('aP','vec3'),aH=A('aH','float'),uT=U('uT'),uSc=U('uSc');   // árbol de luces de colores
  const h=fract(aH.sub(uT.mul(.12))),hs=clamp(abs(fract(vec3(h).add(vec3(0,.6667,.3333))).mul(6).sub(3)).sub(1),0,1),vC=mix(vec3(1),hs,.85).mul(sin(uT.mul(aP.y).add(aP.x)).mul(.45).add(.55));
  const a=smoothstep(1,.1,r2());return{pos:A('position','vec3'),px:(d)=>clamp(aP.z.mul(uSc).div(d),1.8,16),col:vC.mul(a).mul(1.7),a}};
 if(vs.includes('attribute vec3 color;attribute vec3 aP'))return(A,U)=>{const aP=A('aP','vec3'),c=A('color','vec3'),uT=U('uT'),uSc=U('uSc');   // bombillas LED
  const tw=select(aP.z.greaterThan(0),sin(uT.mul(aP.y).add(aP.x)).mul(.45).add(.55),float(1)),a=smoothstep(1,.15,r2());
  return{pos:A('position','vec3'),px:(d)=>clamp(abs(aP.z).mul(uSc).div(d),1.8,11),col:(d)=>c.mul(tw).mul(a.mul(1.6)).mul(exp(d.mul(-.045))),a}};
 if(vs.includes('attribute vec3 color;attribute vec2 aH'))return(A,U)=>{const aH=A('aH','vec2'),c=A('color','vec3'),uT=U('uT'),uSc=U('uSc');   // halos
  const a=pow(max(r2().oneMinus(),0),2.4);return{pos:A('position','vec3'),px:(d)=>clamp(aH.y.mul(uSc).div(d),2,120),col:c.mul(sin(uT.mul(1.6).add(aH.x)).mul(.2).add(.8)).mul(a).mul(.5),a}};
 if(vs.includes('uniform vec2 uWd'))return(A,U)=>{const p=A('position','vec3'),aS=A('aS','vec2'),uT=U('uT'),uK=U('uK'),uC=U('uC'),uSc=U('uSc'),uWd=U('uWd'),B=vec3(4.4,2.6,4.4);   // nevadas
  const sz=aS.x.mul(aS.x).mul(.65).add(.35);let w=p.mul(B);w=vec3(w.x.add(uWd.x.mul(sz.mul(.6).add(.7))).add(sin(uT.mul(aS.y.add(.7)).add(p.z.mul(40))).mul(.06)),w.y.sub(uT.mul(sz.mul(.13).add(.1))),w.z.add(uWd.y.mul(sz.mul(.6).add(.7))).add(cos(uT.mul(aS.y.add(.6)).add(p.x.mul(40))).mul(.06)));
  const q=mod(w.sub(uC),B).sub(B.mul(.5)).add(uC).add(vec3(0,.5,0)),vis=step(aS.y,uK);
  const qq=uv().sub(.5),r=qq.length().mul(2),st=pow(abs(cos(atan(qq.y,qq.x).mul(3))),10).mul(smoothstep(1,.2,r)).mul(step(.6,sz)),a0=max(smoothstep(1,.25,r).mul(.85),st.mul(.7));
  return{world:true,pos:q,px:(d)=>vis.mul(clamp(sz.mul(.02).mul(uSc).div(d),1,window.LITE?10:16)),col:vec3(.95,.97,1),a:(d)=>a0.mul(vis).mul(smoothstep(2.8,1.4,d)).mul(smoothstep(.04,.18,d)).mul(sz.mul(.4).add(.55))}};
 if(vs.includes('const vec3 B=vec3(3.2,1.5,3.2)'))return(A,U)=>{const p=A('position','vec3'),aS=A('aS','float'),uT=U('uT'),uC=U('uC'),uSc=U('uSc'),B=vec3(3.2,1.5,3.2);   // nieve del reparto
  const w=vec3(p.x.mul(3.2).add(sin(uT.mul(.6).add(p.z.mul(30))).mul(.05)).add(uT.mul(.03)),p.y.mul(1.5).sub(uT.mul(aS.mul(.07).add(.11))),p.z.mul(3.2).add(cos(uT.mul(.5).add(p.x.mul(30))).mul(.05)));
  const q=mod(w.sub(uC),B).sub(B.mul(.5)).add(uC).add(vec3(0,.45,0)),a0=smoothstep(.5,.1,uv().sub(.5).length());
  return{world:true,pos:q,px:(d)=>clamp(aS.mul(.006).mul(uSc).div(d),1,4.5),col:vec3(1),a:(d)=>a0.mul(smoothstep(1.7,1.1,d)).mul(smoothstep(.05,.2,d)).mul(.65)}};
 if(vs.includes('attribute vec4 aPolvo'))return(A,U)=>{const a=A('aPolvo','vec4'),uSc=U('uSc'),uL=U('uL'),r=r2(),g=step(.5,a.z);   // polvo y granos de arena
  const al=mix(smoothstep(1,.1,r).mul(sin(a.w.mul(40).add(r.mul(5))).mul(.25).add(.75)),smoothstep(1,.6,r),g).mul(a.y).mul(step(r,1));
  return{pos:A('position','vec3'),px:(d)=>select(a.y.greaterThan(.001),clamp(a.x.mul(uSc).div(d),1.2,90),float(0)),col:mix(vec3(.93,.87,.76),vec3(.5,.42,.3),g).mul(uL),a:al}};
 if(vs.includes('uniform float uT,uWY,uPS'))return(A,U)=>{const p=A('position','vec3'),aS=A('aS','float'),uT=U('uT'),uWY=U('uWY'),uPS=U('uPS'),uNf=U('uNf'),bx=.7,c=cameraPosition;   // partículas bajo el agua
  let q=p.mul(bx).add(vec3(sin(uT.mul(.2).add(p.y.mul(20))).mul(.01).add(uT.mul(.006)),uT.mul(-.003),cos(uT.mul(.15).add(p.x.mul(17))).mul(.01)));q=mod(q.sub(c).add(bx*.5),bx).add(c).sub(bx*.5);
  const vis=step(q.y,uWY.sub(.004)),r=uv().sub(.5).length();
  return{world:true,pos:q,px:(d)=>vis.mul(max(aS.mul(uPS).div(max(d,.01)),1)),col:vec3(.78,.92,.86).mul(uNf.mul(.8).oneMinus()),a:(d)=>smoothstep(.5,.15,r).mul(smoothstep(.015,.05,d)).mul(smoothstep(.12,.5,d).oneMinus()).mul(.4)}};
 return null};
// THREE.Points → sprites por instancia (WebGPU solo dibuja puntos de 1 píxel). Se devuelve un grupo que se comporta como el Points original:
// .geometry y .material son los de siempre (el juego sigue moviendo posiciones y cambiando la opacidad) y dentro va el sprite.
function gpuPoints(geo,mat){const T=TSL,{vec2,vec3,vec4,float,uniform,clamp,select,texture,uv,instancedDynamicBufferAttribute,modelViewMatrix,cameraViewMatrix,cameraProjectionMatrix}=T;
 const g=new THREE.Group();g.geometry=geo;g.material=mat;g.isPoints=true;
 try{GT.ini();const n=geo.attributes.position.count;const IA={};
  for(const k of Object.keys(geo.attributes)){const a=geo.attributes[k];const ia=new THREE.InstancedBufferAttribute(a.array,a.itemSize);ia.setUsage(THREE.DynamicDrawUsage);geo.setAttribute(k,ia);IA[k]=ia}
  const A=(k,t)=>IA[k]?instancedDynamicBufferAttribute(IA[k],t):(t==='vec3'?vec3(0):t==='vec2'?vec2(0):float(0));
  if(!GT.pxW)GT.pxW=uniform(0).onRenderUpdate(()=>{const c=window.__G&&__G.pcam,h=(R.domElement&&R.domElement.height)||800;return 2*Math.tan(((c&&c.fov)||55)*Math.PI/360)/h});
  let sm;
  if(mat.gpuPts){const d0=mat.gpuPts(A,k=>GT.U(mat.uniforms[k]));sm=mat;
   const vpos=d0.world?cameraViewMatrix.mul(vec4(d0.pos,1)):modelViewMatrix.mul(vec4(d0.pos,1)),d=vpos.z.negate().max(1e-4),ev=x=>typeof x==='function'?x(d):x;
   const px=ev(d0.px);sm.positionNode=d0.world?d0.pos:d0.pos;if(d0.world){sm.vertexNode=null}
   sm.scaleNode=vec2(px.mul(d).mul(GT.pxW));sm.colorNode=ev(d0.col);sm.opacityNode=ev(d0.a);sm.sizeAttenuation=true;
   if(d0.world){g.userData.gpuWorld=true}}
  else{// PointsMaterial: tamaño en el mundo, textura, colores por punto y opacidad viva
   sm=new THREE.SpriteNodeMaterial({transparent:mat.transparent,depthWrite:mat.depthWrite,blending:mat.blending,fog:false,toneMapped:mat.toneMapped});
   const op=uniform(1).onRenderUpdate(()=>mat.opacity),cl=uniform(new THREE.Color()).onRenderUpdate(()=>mat.color);
   let col=cl,al=op;if(mat.map){const t=texture(mat.map,uv());col=col.mul(t.rgb);al=al.mul(t.a)}if(mat.vertexColors&&IA.color)col=col.mul(A('color','vec3'));
   sm.positionNode=A('position','vec3');sm.colorNode=col;sm.opacityNode=al;const s=mat.size*.55;sm.scaleNode=vec2(s,s);if(mat.alphaTest)sm.alphaTest=mat.alphaTest}
  const sp=new THREE.Sprite(sm);sp.count=n;sp.frustumCulled=false;g.add(sp);g.userData.sprite=sp;
  // si el juego vuelve a poner la geometría o el material, se reconstruye el sprite
 }catch(e){console.warn('gpuPoints',e)}
 Object.defineProperty(g,'renderOrder',{get(){return this._ro||0},set(v){this._ro=v;if(this.userData&&this.userData.sprite)this.userData.sprite.renderOrder=v}});
 return g}
// ---------- fondo marino (fondomar.js) en TSL: arena con ondulaciones, rocas con coralina y algas, algas que se mecen, peces que
// nadan, pulpos que mueven los brazos; cáusticas del sol y pérdida de color con la distancia (el rojo primero)
GT.h31=p=>TSL.fract(TSL.sin(TSL.dot(p,TSL.vec3(127.1,311.7,74.7))).mul(43758.5453));
GT.vn3=p=>{const{floor,fract,mix,vec3,float}=TSL;const i=floor(p),f0=fract(p),f=f0.mul(f0).mul(float(3).sub(f0.mul(2))),h=o=>GT.h31(i.add(vec3(...o)));
 return mix(mix(mix(h([0,0,0]),h([1,0,0]),f.x),mix(h([0,1,0]),h([1,1,0]),f.x),f.y),mix(mix(h([0,0,1]),h([1,0,1]),f.x),mix(h([0,1,1]),h([1,1,1]),f.x),f.y),f.z)};
GT.caus=(uv0,t)=>{const{vec2,float,mod,sin,cos,length,pow,abs,clamp}=TSL;const p=mod(uv0.mul(6.2832),6.2832).sub(250);let i=p,c=float(1);const inten=.005;
 for(let n=0;n<(window.LITE?2:4);n++){const tt=t.mul(1-3.5/(n+1));i=p.add(vec2(cos(tt.sub(i.x)).add(sin(tt.add(i.y))),sin(tt.sub(i.y)).add(cos(tt.add(i.x)))));
  c=c.add(float(1).div(length(vec2(p.x.div(sin(i.x.add(tt)).div(inten)),p.y.div(cos(i.y.add(tt)).div(inten))))))}
 c=c.div(window.LITE?2:4);c=float(1.17).sub(pow(c,1.4));return clamp(pow(abs(c),8),0,2.5)};
function gpuFondo(B,kind,m){try{if(m.userData.gfm)return;m.userData.gfm=1;GT.ini();
 const T=TSL,{vec2,vec3,vec4,float,normalize,max,min,mix,pow,dot,smoothstep,step,sin,cos,abs,clamp,select,length,fwidth,exp,fract,floor,positionWorld,positionGeometry,positionLocal,normalWorld,cameraPosition,instanceIndex,output,transformNormalToView}=T;
 const LT=!!window.LITE,vn2=GT.vn,h21=GT.h21,vn3=GT.vn3,uT=GT.U(B.FU.uT),uWY=GT.U(B.FU.uWY),uNf=GT.U(B.FU.uNf),uSun=GT.U(B.FU.uSun),uO=GT.U(B.FU.uO);
 const vWB=positionWorld.sub(uO),vNB=normalize(normalWorld),vLY=positionGeometry.y,vLX=positionGeometry.x,fcz=uWY.sub(vWB.y);
 const iph=float(instanceIndex).mul(1.37);   // fase propia de cada instancia (algas y peces)
 // movimiento en el vértice
 if(kind==='alga'&&typeof gpuAlga==='function')gpuAlga(m,uT,uWY,iph);   // mar de fondo en todo el campo de algas (gpu_algas.js)
 else if(kind==='alga'){const hh=max(positionGeometry.y,0),s2=hh.mul(hh),ph=uT.mul(1.05).add(iph);
  m.positionNode=positionLocal.add(vec3(sin(ph.add(hh.mul(2.2))).mul(.3).add(.22).mul(s2).mul(.35).add(sin(uT.mul(4).add(hh.mul(9)).add(iph.mul(3))).mul(.012).mul(s2)),0,cos(ph.mul(.8).add(hh.mul(3.1))).mul(.22).mul(s2).mul(.35)))}
 if(kind==='pez'){const ph=uT.mul(13).add(iph.mul(2.3));m.positionNode=positionLocal.add(vec3(0,0,sin(ph.add(positionGeometry.x.mul(2.6))).mul(.2).mul(smoothstep(.4,-1.5,positionGeometry.x))))}
 const PU=kind==='pulpo';let pk;
 if(PU){const uSw=T.uniform(0).onRenderUpdate(()=>m.userData.U&&m.userData.U.uSw?m.userData.U.uSw.value:0),A=(n,t)=>T.attribute(n,t);
  const aK=A('aK','float'),aT=A('aT','float'),aA=A('aA','float'),aC=A('aC','vec3'),o=T.modelWorldMatrix.element(3).xyz,ph=o.x.mul(370).add(o.z.mul(230)),P=positionGeometry;
  const an=aA.mul(.785398).add(.39),off=P.sub(aC),b=vec3(cos(an).mul(.35),.3,sin(an).mul(.35)),rr0=aC.sub(b),w=sin(uT.mul(.9).add(aA.mul(1.7)).add(ph)).mul(.4).mul(aT),cw=cos(w),sw2=sin(w);
  const rr=vec3(rr0.x.mul(cw).sub(rr0.z.mul(sw2)),rr0.y,rr0.x.mul(sw2).add(rr0.z.mul(cw))),lift=sin(uT.mul(1.4).add(aA.mul(2.3)).sub(aT.mul(5)).add(ph)).mul(.5).add(.5).mul(aT).mul(aT).mul(.8);
  const cr=b.add(rr).add(vec3(0,lift,0)),ct=vec3(aT.mul(2.8).add(.2),sin(an).mul(.25).mul(aT.mul(.6).oneMinus()).add(.8).add(sin(uT.mul(9).sub(aT.mul(7)).add(aA)).mul(.12).mul(aT)),cos(an).mul(.25).mul(aT.mul(.6).oneMinus()).add(cos(uT.mul(8).sub(aT.mul(6)).add(aA)).mul(.1).mul(aT)));
  const brazo=mix(cr,ct,uSw).add(off.mul(uSw.mul(.3).oneMinus())),mc=vec3(-.55,1,0),pu=sin(uT.mul(uSw.mul(11).add(1.6))).mul(uSw.mul(.13).add(.03)).mul(smoothstep(-.1,-.6,P.x)).add(1),manto=mc.add(P.sub(mc).mul(pu));
  m.positionNode=select(aK.greaterThan(.5).and(aK.lessThan(1.5)),brazo,select(aK.lessThan(.5),manto,P));
  const fq=P.mul(7).add(o.mul(500)),fmo=vn3(fq.mul(.45)).mul(.6).add(vn3(fq.mul(1.3)).mul(.4));let fc=mix(vec3(.30,.10,.055),vec3(.52,.28,.17),smoothstep(.3,.75,fmo));
  fc=fc.mul(smoothstep(.7,.8,vn3(fq.mul(3.2))).mul(.3).oneMinus());fc=mix(fc,vec3(.7,.56,.45),smoothstep(.8,.9,vn3(fq.mul(4.5).add(7))).mul(.4));
  const fcam=sin(uT.mul(.35).add(o.x.mul(300)).add(o.z.mul(170))).mul(.5).add(.5);fc=mix(fc,mix(vec3(.36,.31,.22),vec3(.28,.25,.2),fmo),fcam.mul(.38));
  const fsk=smoothstep(.35,.7,A('aU','float')).mul(step(.5,fract(aT.mul(34)))).mul(step(.5,aK)).mul(step(aK,1.5));fc=mix(fc,vec3(.7,.55,.48),fsk.mul(.8));
  fc=select(aK.greaterThan(2.5),vec3(.02),select(aK.greaterThan(1.5),vec3(.62,.52,.28),fc));m.colorNode=fc}
 let ext=null;
 if(kind==='arena'){const q=vWB.xz,fm1=vn2(q.mul(9)),fm2=vn2(q.mul(31).add(7)),fm3=vn2(q.mul(140)),fdeep=smoothstep(.15,.3,fcz);
  let fc=mix(mix(vec3(.30,.27,.20),vec3(.41,.37,.28),fm1),vec3(.12,.12,.09),fdeep.mul(fm2.mul(.45).add(.55)));
  const fdir=normalize(vec2(.8,.6).add(vec2(vn2(q.mul(4)),vn2(q.mul(4).add(9))).sub(.5).mul(.9))),fph=dot(q,fdir).mul(260).add(vn2(q.mul(12)).mul(7));
  const ffw=length(fwidth(q)),frip=fdeep.mul(.75).oneMinus().mul(smoothstep(.0025,.008,ffw).oneMinus());
  fc=fc.mul(sin(fph).mul(.2).mul(frip).add(1));fc=mix(fc,vec3(.11,.10,.07),smoothstep(.5,.95,sin(fph).negate()).mul(.35).mul(frip));
  fc=mix(fc,vec3(.58,.55,.48),step(.985,h21(floor(q.mul(900)))).mul(smoothstep(.45,.2,length(fract(q.mul(900)).sub(.5)))).mul(smoothstep(.0008,.003,ffw).oneMinus()).mul(.45));
  fc=mix(fc,vec3(.16,.15,.13),smoothstep(.62,.8,vn2(q.mul(2.3).add(4))).mul(.35));m.colorNode=fc.mul(fm3.mul(.3).add(.85));
  if(!LT){const fs=cos(fph).add(cos(fph.mul(2)).mul(.35));let fg=fdir.mul(fs).mul(.5).mul(frip);const e=.004,n0=vn2(q.mul(90));fg=fg.add(vec2(vn2(q.add(vec2(e,0)).mul(90)).sub(n0),vn2(q.add(vec2(0,e)).mul(90)).sub(n0)).div(e).mul(.0011));
   m.normalNode=transformNormalToView(normalize(vNB.add(vec3(fg.x.negate(),0,fg.y.negate()).mul(max(vNB.y,.2)))))}}
 else if(kind==='roca'){const q=vWB,fg1=vn3(q.mul(45)),fg2=vn3(q.mul(160)),fg3=vn3(q.mul(520));
  let fc=mix(vec3(.23,.22,.21),vec3(.37,.34,.31),fg1);fc=mix(fc,vec3(.05),step(.76,fg3).mul(.85));fc=mix(fc,vec3(.55,.51,.47),step(.8,fg3.oneMinus()).mul(.5));
  const ftop=smoothstep(.1,.75,vNB.y),fc1=vn3(q.mul(22).add(3)),fc2=vn3(q.mul(55).add(9));
  fc=mix(fc,vec3(.34,.12,.14).mul(fg2.mul(.5).add(.75)),smoothstep(.48,.6,fc2).mul(ftop.oneMinus().mul(.65).add(.35)).mul(.9));      // coralina rosa
  fc=mix(fc,mix(vec3(.06,.10,.03),vec3(.15,.11,.04),fc1).mul(fg2.mul(.7).add(.65)),smoothstep(.32,.58,fc1).mul(ftop));                // algas encima
  fc=mix(fc,vec3(.62,.62,.57),step(.93,vn3(q.mul(900))).mul(smoothstep(.06,.15,fcz).oneMinus()).mul(.85));m.colorNode=fc;
  if(!LT){const fp=q.mul(70),e=.18,n0=vn3(fp);let fg=vec3(vn3(fp.add(vec3(e,0,0))).sub(n0),vn3(fp.add(vec3(0,e,0))).sub(n0),vn3(fp.add(vec3(0,0,e))).sub(n0)).div(e).mul(.55);
   m.normalNode=transformNormalToView(normalize(vNB.sub(fg.sub(vNB.mul(dot(fg,vNB))))))}}
 else if(kind==='alga'){m.colorNode=T.materialColor.mul(mix(.75,1.25,smoothstep(0,1,vLY))).mul(vn2(vWB.xz.mul(300).add(vLY.mul(20))).mul(.3).add(.85));
  ext=T.materialColor.mul(.55).mul(uNf.oneMinus()).mul(exp(fcz.mul(-4))).mul(vLY.mul(.4).add(.6))}
 else if(kind==='pez'){const fb=smoothstep(-.04,.16,vLY),side=mix(vec3(.78,.8,.82),vec3(.55,.6,.64),smoothstep(-.22,.02,vLY));
  m.colorNode=mix(side,T.materialColor,fb).mul(smoothstep(-1,-1.4,vLX).mul(.35).oneMinus());
  const V=normalize(cameraPosition.sub(positionWorld)),fr=pow(abs(dot(vNB,V)).oneMinus(),2.5);
  ext=vec3(.55,.72,.78).mul(fr.mul(.35).add(pow(max(0,sin(uT.mul(2).add(vWB.x.mul(90)).add(vWB.z.mul(70)))),12).mul(.25))).mul(fb.oneMinus()).mul(uNf.mul(.7).oneMinus())}
 // cáusticas del sol y absorción del color con la distancia y la profundidad
 const fcz2=max(fcz,0),fcf=exp(fcz2.mul(-2.6)).mul(smoothstep(-.35,.75,vNB.y)).mul(uNf.mul(.92).oneMinus());
 const fcp=vWB.xz.add(uSun.xz.div(max(uSun.y,.25)).mul(fcz2).mul(.6)).div(.085),fca=GT.caus(fcp,uT.mul(.55).add(11)).mul(.7).add(LT?float(0):GT.caus(fcp.mul(1.31).add(.37),uT.mul(.47).add(3)).mul(.45));
 const dif=m.colorNode||T.materialColor;let L=output.rgb.add(vec3(dif).mul(fca).mul(vec3(.85,1,.95)).mul(7).mul(fcf));if(ext)L=L.add(ext);
 const fdd=length(vWB.sub(cameraPosition.sub(uO)));m.outputNode=vec4(L.mul(exp(vec3(2.6,.62,.5).negate().mul(fdd.mul(1.05).add(fcz2.mul(1.5))))).mul(.8),output.a);
 m.needsUpdate=true}catch(e){console.warn('gpuFondo',kind,e)}}
// ---------- suelos y fachadas (edit_asfalto, edit_charcos, edit_cesped, fachadas del centro, tejados y escaparates) ----------
// Cada efecto añade su paso a la cadena de color del material (colorNode); el motor nuevo copia los nudos al convertirlo.
GT.hF=p=>TSL.fract(TSL.sin(TSL.dot(p,TSL.vec3(12.9898,78.233,37.719))).mul(43758.5453));
GT.cadena=(m,f)=>{const prev=m.userData.gpuCol||(b=>b);m.userData.gpuCol=b=>f(prev(b));m.colorNode=m.userData.gpuCol(TSL.materialColor)};
GT.em=(m,n)=>{m.emissiveNode=m.emissiveNode?m.emissiveNode.add(n):n};
function gpuFx(tipo,m,k){try{if(!m||m.userData['g_'+tipo])return;m.userData['g_'+tipo]=1;GT.ini();
 const{vec2,vec3,float,floor,fract,mix,smoothstep,step,max,min,clamp,length,pow,abs,dot,normalize,sin,cos,select,fwidth,dFdx,dFdy,texture,uniform,uv,attribute,positionWorld,cameraPosition,normalWorld,materialRoughness}=TSL;
 const LT=!!window.LITE,W=positionWorld,q=W.xz,fw=max(length(fwidth(q)),1e-6),vn=GT.vn,h21=GT.h21;
 if(tipo==='asf'){const tn=vn(q.mul(.8)).mul(.6).add(vn(q.mul(3.1)).mul(.4)).sub(.5);let oil=float(0);
  if(!LT){const oc=floor(q.mul(26)),od=fract(q.mul(26)).sub(.5).add(vec2(h21(oc.add(5)),h21(oc.add(9))).sub(.5).mul(.3));
   oil=step(.92,h21(oc)).mul(smoothstep(.10,.30,length(od.mul(vec2(1,2.2))).add(vn(q.mul(300)).sub(.5).mul(.12))).oneMinus()).mul(smoothstep(.008,.035,fw).oneMinus())}
  GT.cadena(m,b=>b.mul(vec3(.06,.035,-.05).mul(tn).mul(2).add(1)).mul(oil.mul(.38).oneMinus()))}
 else if(tipo==='mv'){const asf=vec3(.088,.093,.104),cerca=smoothstep(.004,.02,fw).oneMinus(),lejos=smoothstep(.012,.07,fw);
  let gas=smoothstep(.5,.85,vn(q.mul(45)).mul(.6).add(vn(q.mul(130)).mul(.4))).mul(.8);if(!LT)gas=max(gas,smoothstep(.6,.8,vn(q.mul(380))).mul(.6).mul(cerca));
  GT.cadena(m,b=>mix(b,asf,clamp(gas.mul(cerca.mul(.65).add(.35)).add(lejos.mul(.28)),0,.85)))}
 else if(tipo==='mo'){const uWet=GT.U(UMO.uWet),uTm=GT.U(UMO.uTm),uLz=GT.U(UMO.uLz),wW=uWet.mul(k);
  if(k>.95){const man=vn(q.mul(7)).mul(.55).add(vn(q.mul(23)).mul(.45)),par=smoothstep(.70,.74,vn(q.mul(5.3).add(17)));
   const grano=LT?float(0):vn(q.mul(420)).sub(.5).mul(1.3).mul(smoothstep(.003,.012,fw).oneMinus()).add(vn(q.mul(150)).sub(.5).mul(1.4).mul(smoothstep(.006,.025,fw).oneMinus()));
   const gri=LT?float(0):smoothstep(.985,1,vn(q.mul(90).add(3))).mul(smoothstep(.002,.008,fw).oneMinus());
   GT.cadena(m,b=>b.mul(man.mul(.36).add(.78)).mul(grano.mul(.3).add(1)).mul(par.mul(.2).oneMinus()).mul(gri.mul(.4).oneMinus()));
   m.userData.gpuRough=clamp(materialRoughness.mul(.86).sub(man.mul(.08)).add(grano.mul(.06)),.42,.95)}
  const n=vn(q.mul(23)).mul(.6).add(vn(q.mul(67)).mul(.4)),pud=smoothstep(.56,.71,n.add(uWet.sub(.5).mul(.08))).mul(smoothstep(.15,.6,uWet));
  GT.cadena(m,b=>b.mul(mix(1,mix(.66,.5,pud),wW)));
  m.roughnessNode=mix(m.userData.gpuRough||materialRoughness,mix(.34,.05,pud),wW);
  // reflejo del cielo en lo mojado, ondas de las gotas y luces de noche en los charcos
  const V=normalize(cameraPosition.sub(W)),frs=pow(clamp(V.y,0,1).oneMinus(),5).mul(.96).add(.04),skyc=mix(GT.U(SKYU.uHor),GT.U(SKYU.uZen),clamp(V.y.mul(1.3),0,1));
  const cel=floor(q.mul(60)),ph=fract(uTm.mul(.9).add(h21(cel).mul(7))),rip=smoothstep(0,.07,abs(length(fract(q.mul(60)).sub(.5)).sub(ph.mul(.45)))).oneMinus().mul(ph.oneMinus()).mul(step(.7,h21(cel.add(3)))).mul(pud);
  let skyR=skyc,tope=float(.6);
  {if(!RCUBO.rt)RCUBO.rt=new THREE.CubeRenderTarget(128,{type:THREE.HalfFloatType,generateMipmaps:false});const uEnvOn=GT.U(UENV.uEnvOn),uEnvP=GT.U(UENV.uEnvP);
   const rd=vec3(V.x.negate(),abs(V.y),V.z.negate()).add(vec3(vn(q.mul(70).add(uTm.mul(2))).sub(.5),0,vn(q.mul(70).sub(uTm.mul(2)).add(9)).sub(.5)).mul(.09).mul(pud)),rp=W.sub(uEnvP).div(1.6);
   const env=TSL.cubeTexture(RCUBO.rt.texture,normalize(rd.add(rp))).rgb;skyR=select(uEnvOn.greaterThan(.5),mix(skyc,env,.92),skyc);tope=select(uEnvOn.greaterThan(.5),float(.82),float(.6))}
  const ref=clamp(wW.mul(pud.mul(.62).add(.10)).mul(frs.mul(2.6).add(.18)),0,tope);
  GT.em(m,skyR.mul(rip.mul(.6).add(1)).mul(ref).add(vec3(1,.72,.38).mul(uLz).mul(wW).mul(pud).mul(.12).mul(smoothstep(.55,.9,vn(q.mul(9))))))}
 else if(tipo==='ces'){const uGWet=GT.U(UMO.uWet),gc=smoothstep(.0025,.012,fw).oneMinus(),gm=smoothstep(.015,.07,fw).oneMinus();
  const gL=vn(q.mul(2.2)).mul(.45).add(vn(q.mul(8)).mul(.35)).add(vn(q.mul(19)).mul(.2)),gD=smoothstep(.64,.88,vn(q.mul(2.3).add(7))).mul(vn(q.mul(11)).mul(.4).add(.6));
  const gK=vn(q.mul(38)).mul(.6).add(vn(q.mul(95)).mul(.4)),gS=smoothstep(.5,.6,vn(q.mul(.6).add(3)));
  GT.cadena(m,b=>{const gb=b.mul(vec3(.40,.43,.27));let gcol=mix(gb.mul(vec3(.62,.74,.62)),gb.mul(vec3(1.22,1.14,.92)),smoothstep(.2,.8,gL));
   gcol=mix(gcol,gcol.mul(vec3(1.7,1.32,.7)).add(vec3(.025,.018,0)),gD.mul(.6));gcol=gcol.mul(mix(1,gK.mul(.56).add(.72),gm));
   gcol=gcol.mul(gS.mul(gm).mul(.075).mul(smoothstep(-.35,.35,sin(q.x.mul(50).add(vn(q.mul(.4)).mul(2))))).mul(2).add(1).sub(gS.mul(gm).mul(.075)));
   if(!LT){gcol=gcol.mul(mix(1,h21(floor(q.mul(430))).mul(.32).add(.84),gc));const fcl=floor(q.mul(160)),ffr=fract(q.mul(160)).sub(.5),fh=h21(fcl.add(11));
    const fl=step(.968,fh).mul(smoothstep(.10,.19,length(ffr)).oneMinus()).mul(gc).mul(step(.45,vn(q.mul(3).add(21))));gcol=mix(gcol,select(fh.greaterThan(.988),vec3(.85,.62,.06),vec3(.86,.86,.80)),fl)}
   return gcol.mul(uGWet.mul(.25).oneMinus())});
  m.roughnessNode=mix(.92,.62,uGWet)}
 else if(tipo==='fv'||tipo==='fr'){const uLuz=GT.U(UF.uLuz),map=m.map;if(!map)return;map.updateMatrix();const um=uniform(map.matrix),uvF=um.mul(vec3(uv(map.channel||0),1)).xy;
  if(tipo==='fv'){const sm=texture(map),vb=uvF.y.mul(18),ao=mix(.62,1,smoothstep(0,.55,vb)),win=smoothstep(.30,.42,dot(sm.rgb,vec3(.333))).oneMinus();
   const cel=vec3(floor(uvF.x.mul(2)),floor(vb),0).add(floor(W.mul(3)).mul(vec3(1.7,0,2.3)));
   GT.cadena(m,b=>b.mul(ao));m.emissiveNode=vec3(1,.77,.47).mul(step(.5,GT.hF(cel))).mul(win).mul(uLuz).mul(GT.hF(cel.add(5)).add(1.2));return}
  // fachadas del centro: planta y vano eligen ventana del atlas (balcones en columna, persianas, galerías), sillería y cristal
  const fsh=attribute('fsh','float'),fcol=attribute('fcol','vec4'),pl=max(uvF.y.oneMinus().mul(18).sub(fsh),0),fl=floor(pl),bay=floor(uvF.x),sd=floor(W.mul(1.6)).mul(vec3(1.7,0,2.3));
  const hb=GT.hF(vec3(bay,0,0).add(sd)),hp=GT.hF(vec3(bay,fl,1).add(sd));
  const var_=select(fl.lessThan(.5),floor(GT.hF(vec3(bay,9,0).add(sd)).mul(4)),select(hb.lessThan(.28),float(1),select(hp.lessThan(.12),float(3),select(hp.lessThan(.55),float(0),float(2)))));
  const fila=select(fl.lessThan(.5),float(0),float(1)),cu=vec2(fract(uvF.x),fract(pl)),at=vec2(var_.add(cu.x).div(4),fila.add(cu.y).div(2));
  const dx=vec2(dFdx(uvF.x).div(4),dFdx(pl).div(2)),dy=vec2(dFdy(uvF.x).div(4),dFdy(pl).div(2));let smp=texture(map,at).grad(dx,dy);
  if(!LT){const Rw=select(var_.greaterThan(.5).and(var_.lessThan(1.5)),TSL.vec4(.234,.156,.766,.885),TSL.vec4(.203,.24,.797,.823));
   const dentro=fl.greaterThan(.5).and(k==='b'?var_.lessThan(2.5):float(1).greaterThan(0)).and(cu.x.greaterThan(Rw.x)).and(cu.x.lessThan(Rw.z)).and(cu.y.greaterThan(Rw.y)).and(cu.y.lessThan(Rw.w));
   const dpx=dFdx(W),dpy=dFdy(W),d1=vec2(dFdx(uvF.x),dFdx(pl)),d2=vec2(dFdy(uvF.x),dFdy(pl));let Nn=normalize(TSL.cross(dpx,dpy));const Vw=normalize(W.sub(cameraPosition));Nn=select(dot(Nn,Vw).greaterThan(0),Nn.negate(),Nn);
   const q2=TSL.cross(dpy,Nn),q1=TSL.cross(Nn,dpx),Tt=normalize(q2.mul(d1.x).add(q1.mul(d2.x)).add(vec3(1e-9))),Bt=normalize(q2.mul(d1.y).add(q1.mul(d2.y)).add(vec3(1e-9))),vz=max(dot(Vw,Nn).negate(),.12);
   const c2=cu.add(vec2(dot(Vw,Tt),dot(Vw,Bt)).div(vz).mul(vec2(.0055/.05,.0055/.075)));
   const fondo=texture(map,vec2(var_.add(c2.x).div(4),fila.add(c2.y).div(2))).grad(dx,dy),ed=min(min(c2.x.sub(Rw.x),Rw.z.sub(c2.x)).mul(.05),min(c2.y.sub(Rw.y),Rw.w.sub(c2.y)).mul(.075));
   const fondoS=TSL.vec4(fondo.rgb.mul(mix(.5,1,smoothstep(0,.0035,ed))).mul(mix(.62,1,smoothstep(0,.006,Rw.w.sub(c2.y).mul(.075)))),fondo.a);
   const lado=c2.x.lessThan(Rw.x).or(c2.x.greaterThan(Rw.z)),arriba=c2.y.greaterThan(Rw.w),abajo=c2.y.lessThan(Rw.y);
   const par=select(lado,TSL.vec4(vec3(.58),1),select(arriba,TSL.vec4(vec3(.42),1),select(abajo,TSL.vec4(vec3(.8),1),fondoS)));
   smp=select(dentro,par,smp)}
  const gla=smoothstep(.82,.9,smp.a).oneMinus(),uCol=uniform(m.color);
  const ry=W.y.mul(115),row=floor(ry),uu=W.x.add(W.z).mul(58).add(fract(row.mul(.5)).mul(.5).mul(2));
  const jh=smoothstep(0,.07,fract(ry)).mul(smoothstep(1,.93,fract(ry))),jv=smoothstep(0,.05,fract(uu)).mul(smoothstep(1,.95,fract(uu)));
  const sill=GT.hF(vec3(floor(uu),row,7)).mul(.13).add(.9).mul(mix(.78,1,jh.mul(jv))),liso=GT.hF(floor(W.mul(240))).mul(.05).add(.97);
  const base=fcol.rgb.mul(select(fcol.a.greaterThan(2.5),sill,liso)),conF=base.mul(mix(vec3(1),smp.rgb.mul(1.12),.85)),sinF=uCol.mul(smp.rgb);
  const ao=mix(.7,1,smoothstep(0,.5,pl)),celF=vec3(bay,fl,0).add(sd),on=step(.5,GT.hF(celF)).mul(uLuz);
  const V=normalize(cameraPosition.sub(W)),frg=pow(abs(V.y).oneMinus(),3).mul(.6).add(.08),skyc=mix(GT.U(SKYU.uHor),GT.U(SKYU.uZen),.35).mul(GT.U(SKYU.uNight).mul(.75).oneMinus());
  const kf=gla.mul(frg).mul(on.mul(.85).oneMinus());
  m.colorNode=select(fcol.a.greaterThan(1.5),conF,sinF).mul(ao).mul(kf.oneMinus());
  m.roughnessNode=mix(.82,.12,gla);
  m.emissiveNode=vec3(1,.77,.47).mul(on).mul(gla).mul(GT.hF(celF.add(5)).add(1.2)).add(skyc.mul(kf))}
 else if(tipo==='tj'){const up=abs(normalWorld.y),rtip=attribute('rtip','float');
  GT.cadena(m,c=>{const roj=smoothstep(.04,.14,c.x.sub(c.z)),fine=smoothstep(.004,.02,fw).oneMinus();
   const dir=normalize(normalWorld.xz.add(vec2(1e-4,0))),fl=up.greaterThan(.97),a=select(fl,q.y,dot(q,dir)),bb=select(fl,q.x,dot(q,vec2(dir.y.negate(),dir.x)));
   const fila=fract(a.mul(130)),col=fract(bb.mul(130).add(floor(a.mul(130)).mul(.5)));
   const teja=smoothstep(0,.7,fila).mul(.3).add(.78).mul(smoothstep(0,.5,abs(col.sub(.5)).mul(2)).mul(.16).add(.92)).mul(GT.hF(floor(vec3(a.mul(130),bb.mul(130),0))).mul(.2).add(.9));
   const grava=GT.hF(floor(vec3(q.mul(500),0))).mul(.2).add(.9).mul(fract(sin(dot(floor(q.mul(12)),vec2(7.1,3.3))).mul(91.7)).mul(.3).add(.85));
   const junta=step(.96,fract(q.x.mul(35))).add(step(.96,fract(q.y.mul(35)))).mul(.18).oneMinus();
   const sb=fract(bb.mul(60)),pizarra=vec3(.31,.34,.39).mul(GT.hF(vec3(floor(bb.mul(60)),floor(a.mul(9)),1)).mul(.18).add(.86)).mul(smoothstep(.86,.95,sb).mul(.3).oneMinus()).mul(smoothstep(0,.6,fila).mul(.12).add(1));
   const nor=c.mul(mix(1,mix(grava.mul(junta),teja,roj),fine.mul(.9).add(.1)));
   return select(up.greaterThan(.45),select(rtip.greaterThan(.5).and(roj.greaterThan(.3)),pizarra,nor),c)})}
 else if(tipo==='vit'){const uLuz=GT.U(UF.uLuz),nV=normalWorld,tg=normalize(vec2(nV.z.negate(),nV.x).add(vec2(1e-4,0))),u=dot(q,tg).mul(62),yy=W.y.mul(62);
  const fr=max(smoothstep(.84,.9,abs(fract(u).sub(.5)).mul(2)),step(.82,fract(yy.mul(.22)))),suelo=abs(nV.y).greaterThan(.6),vGl=select(suelo,float(0),fr.oneMinus());
  m.colorNode=select(suelo,vec3(.74,.72,.68).mul(GT.h21(floor(q.mul(300))).mul(.1).add(.9)),mix(vec3(.09,.12,.16),vec3(.78,.78,.76),fr));
  m.roughnessNode=mix(.75,.08,vGl);const V=normalize(cameraPosition.sub(W)),frg=pow(abs(V.y).oneMinus(),3).mul(.7).add(.12),skyc=mix(GT.U(SKYU.uHor),GT.U(SKYU.uZen),.4).mul(GT.U(SKYU.uNight).mul(.75).oneMinus());
  m.emissiveNode=vec3(1,.79,.54).mul(vGl).mul(uLuz).mul(.9).mul(step(.35,GT.h21(floor(q.mul(40))))).add(skyc.mul(.55).mul(vGl).mul(frg).mul(.28))}
 else if(tipo==='arena'){const T=TSL,{exp,cross,transformNormalToView}=T;   // arena de las playas (orilla.js) con huellas y surcos (huellas.js)
  const uT=GT.U(UW.uT),uWet=GT.U(UMO.uWet),uZen=GT.U(SKYU.uZen),uHor=GT.U(SKYU.uHor),hw=W.y.sub(ORI.WY);
  const m1=vn(q.mul(1.7)),m2=vn(q.mul(6.3).add(3.1)),m3=vn(q.mul(23).add(9.7));
  let col=mix(vec3(.70,.57,.38),vec3(.85,.74,.54),smoothstep(.22,.78,m1.mul(.55).add(m2.mul(.45)))).mul(m3.mul(.12).add(.93));
  const c1=smoothstep(.004,.02,fw).oneMinus(),c2=LT?float(0):smoothstep(.00015,.0008,fw).oneMinus();
  col=col.mul(vn(q.mul(700)).sub(.5).mul(c2).add(vn(q.mul(190).add(4)).sub(.5).mul(.6).mul(c1)).mul(.24).add(1));
  col=col.mul(smoothstep(.72,.95,vn(q.mul(420).add(11))).mul(c2).mul(.18).oneMinus());
  const sec=smoothstep(.009,.02,hw),wd=vec2(.825,.565),ph=dot(q,wd).mul(950).add(vn(q.mul(6)).mul(2).add(vn(q.mul(31)).mul(.7)).mul(6.2832));
  const ra=smoothstep(.35,.8,vn(q.mul(6).add(2))).mul(smoothstep(.001,.004,fw).oneMinus()).mul(sec);col=col.mul(sin(ph).mul(.045).mul(ra).add(1));
  let gx=LT?vec2(0,0):wd.mul(cos(ph)).mul(.13).mul(ra);
  const wr=exp(pow(hw.sub(.021).sub(vn(q.mul(3)).sub(.5).mul(.005)).div(.0022),2).negate()).mul(smoothstep(.45,.8,vn(q.mul(85)))).mul(c1);col=col.mul(wr.mul(.28).oneMinus());
  const wetH=vn(q.mul(4)).sub(.5).mul(.004).add(.012),aWet=smoothstep(wetH.mul(.55),wetH,hw).oneMinus();
  const sw=sin(uT.mul(.7).add(vn(q.mul(3)).mul(6.2832))).mul(.5).add(.5).mul(.003).add(.0035).add(vn(q.mul(40).add(uT.mul(.3))).sub(.5).mul(.0008));
  const aFilm=smoothstep(sw.sub(.0008),sw.add(.0002),hw).oneMinus();
  let fo=smoothstep(sw.sub(.0017),sw.sub(.0004),hw).mul(smoothstep(sw.sub(.0001),sw.add(.0007),hw).oneMinus());
  fo=fo.mul(smoothstep(.3,.7,vn(q.mul(260).add(vec2(uT.mul(.05),0))).mul(.6).add(vn(q.mul(60)).mul(.4))).mul(.7).add(.3));
  fo=fo.add(aFilm.mul(smoothstep(.62,.8,vn(q.mul(180).add(vec2(0,uT.mul(.08)))))).mul(.45).mul(smoothstep(-.003,.002,sw.sub(hw).sub(.002)).oneMinus()));
  const wc=col.mul(vec3(.52,.48,.42));col=mix(col,wc,aWet);col=mix(col,wc.mul(vec3(.78,.9,.92)),aFilm);
  {const uSn=GT.U(SKYU.uSun),uNn=GT.U(UW.uN),cs_=smoothstep(.02,.35,normalize(uSn).y).mul(uNn.oneMinus()).mul(GT.U(SKYU.uCov).mul(.85).oneMinus()).mul(uWet.mul(.7).oneMinus());   // cáusticas en la lámina de agua que sube y baja por la arena
   const cq=q.div(.022).add(vec2(sw.mul(9),0)),ca=GT.caus(cq,uT.mul(.8)).mul(LT?1:.65).add(LT?float(0):GT.caus(cq.mul(1.41).add(.3),uT.mul(.71).add(4)).mul(.4));
   col=col.add(vec3(.95,1,.9).mul(ca).mul(aFilm).mul(smoothstep(.0028,.0009,fw)).mul(cs_).mul(.14))}col=mix(col,vec3(.9,.93,.92),clamp(fo,0,1).mul(.9));
  col=mix(col,col.mul(.62),uWet.mul(aWet.oneMinus()));gx=gx.mul(aWet.oneMinus());
  if(window.__HU){const H=window.__HU,uHC=GT.U(H.U.uHC),dq=q.sub(uHC.xy);   // huellas y surcos
   const hin=smoothstep(uHC.z.mul(.40),uHC.z.mul(.47),max(abs(dq.x),abs(dq.y))).oneMinus().mul(aFilm.oneMinus()).mul(step(.5,uHC.w));
   const hu=fract(q.div(uHC.z)),t0=texture(H.tex,hu),dep=t0.r.mul(hin),rim=t0.g.mul(hin);
   col=col.mul(rim.mul(.08).oneMinus()).mul(dep.mul(.24).oneMinus());col=mix(col,col.mul(vec3(.62,.66,.7)),dep.mul(aWet));
   if(!LT){const e=1/H.N,tx=texture(H.tex,hu.add(vec2(e,0))),tz=texture(H.tex,hu.add(vec2(0,e))),h0=t0.g.mul(.35).sub(t0.r),h1=tx.g.mul(.35).sub(tx.r),h2=tz.g.mul(.35).sub(tz.r);
    gx=gx.add(vec2(h0.sub(h1),h0.sub(h2)).mul(.7).mul(hin))}}
  m.colorNode=col;m.roughnessNode=mix(mix(mix(.93,.32,aWet),.07,aFilm),.4,uWet.mul(aWet.oneMinus()).mul(aFilm.oneMinus()).mul(.6));m.metalnessNode=float(0);
  const Ng=normalize(cross(dFdx(W),dFdy(W))),Nu=select(Ng.y.lessThan(0),Ng.negate(),Ng);
  m.normalNode=transformNormalToView(normalize(Nu.add(vec3(gx.x,0,gx.y))));
  const V=normalize(cameraPosition.sub(W)),frs=pow(clamp(V.y,0,1).oneMinus(),5).mul(.98).add(.02);
  GT.em(m,mix(uHor,uZen,.35).mul(frs).mul(aWet.mul(.1).add(aFilm.mul(.28))))}
 else if(tipo==='oriT'){const uR=GT.U(k.uOriR),uq=q.sub(uR.xy).div(uR.zw);   // franja nueva de la orilla: lo viejo no se dibuja
  const den=uq.x.greaterThan(0).and(uq.y.greaterThan(0)).and(uq.x.lessThan(1)).and(uq.y.lessThan(1));
  m.maskNode=den.and(texture(k.uOriM.value,clamp(uq,0,1)).r.greaterThan(.5)).not()}
 m.needsUpdate=true}catch(e){console.warn('gpuFx',tipo,e)}}
// ---------- fin de gpu_tsl.js
