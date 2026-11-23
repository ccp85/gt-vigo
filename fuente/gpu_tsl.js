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
function gpuAgua(glob){GT.ini();const{vec2,vec3,float,normalize,max,min,mix,pow,dot,smoothstep,sin,cos,exp,abs,clamp,select,length,fwidth,texture,reflect,positionWorld,cameraPosition,transformNormalToView}=TSL;
 const LT=!!window.LITE,uT=GT.U(UW.uT),uN=GT.U(UW.uN),uSun=GT.U(SKYU.uSun),uZen=GT.U(SKYU.uZen),uHor=GT.U(SKYU.uHor),uCoR=GT.U(UCO.uCoR);
 const p=positionWorld.xz,uq=p.sub(uCoR.xy).div(uCoR.zw);
 const dentro=uq.x.greaterThanEqual(0).and(uq.y.greaterThanEqual(0)).and(uq.x.lessThanEqual(1)).and(uq.y.lessThanEqual(1));
 const C=texture(UCO.uCos.value,uq);const cs=select(dentro,C.r,float(0)),aw=select(dentro,C.g,float(1)).mul(smoothstep(.985,.999,cs).oneMinus());
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
 const aF=clamp(foam.add(whc.mul(tx)),0,1);col=mix(col,vec3(.78,.82,.84),aF.mul(uN.mul(.6).oneMinus()));
 // reflejo del cielo (Fresnel) y destellos del sol
 const N=normalize(mix(aN,vec3(0,1,0),aF)),V=normalize(cameraPosition.sub(positionWorld)),nv=max(dot(N,V),0);
 const R0=reflect(V.negate(),N),Rf=vec3(R0.x,abs(R0.y),R0.z);
 const sky=mix(uHor,uZen,smoothstep(0,.5,Rf.y).mul(.65).add(.35)).mul(.82);
 const F=min(pow(nv.oneMinus(),5).mul(.98).add(.02).mul(1.2).add(.07).add(calma.mul(.06)),.58).mul(aF.oneMinus());
 const Ls=normalize(uSun),sd=max(dot(Rf,Ls),0),up=smoothstep(-.02,.12,Ls.y).mul(uN.oneMinus());
 const sc=mix(vec3(1,.5,.25),vec3(1,.95,.86),smoothstep(.05,.4,Ls.y));
 const glint=sc.mul(pow(sd,700).mul(10).add(pow(sd,60).mul(.35))).mul(up).mul(aF.oneMinus());
 const m=new THREE.MeshStandardNodeMaterial({roughness:.6,metalness:0});
 m.colorNode=col.mul(F.oneMinus());m.normalNode=transformNormalToView(normalize(mix(aN,vec3(0,1,0),aF.mul(.8))));m.emissiveNode=sky.mul(F).add(glint);
 if(glob){m.alphaTest=.5;m.opacityNode=select(cs.greaterThan(.97).or(C.b.greaterThan(.5).and(dentro)),float(0),float(1))}   // la lámina global no tapa la tierra
 return m}
// ---------- fin de gpu_tsl.js
