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
  const ref=clamp(wW.mul(pud.mul(.62).add(.10)).mul(frs.mul(2.6).add(.18)),0,.6);
  GT.em(m,skyc.mul(rip.mul(.6).add(1)).mul(ref).add(vec3(1,.72,.38).mul(uLz).mul(wW).mul(pud).mul(.12).mul(smoothstep(.55,.9,vn(q.mul(9))))))}
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
  const dx=vec2(dFdx(uvF.x).div(4),dFdx(pl).div(2)),dy=vec2(dFdy(uvF.x).div(4),dFdy(pl).div(2)),smp=texture(map,at).grad(dx,dy);
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
 m.needsUpdate=true}catch(e){console.warn('gpuFx',tipo,e)}}
// ---------- fin de gpu_tsl.js
