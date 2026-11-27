// ---------- cielo físico (gpu_cielofis.js) ----------
// Cielo con dispersión de la luz en el aire (Rayleigh: el azul; Mie: el halo blanco y el rojo del atardecer), con el modelo
// de Preetham (el mismo del Sky / SkyMesh de three.js), y el sol en su sitio de verdad sobre Vigo (42,24° N, 8,72° O):
// sale por el Morrazo y Redondela y se pone por el oeste, hacia las Cíes y Cabo Home. Por defecto, un día de mediados de
// agosto (sale ~7:50 y se pone ~21:30), para que las horas de siempre (tarde 19-20:45, noche 23:30) sigan cuadrando;
// con ?dia=hoy en la dirección se usa la fecha de hoy y con ?dia=N el día N del año.
// - En la CPU, cada imagen: posición del sol, color del sol (lo que deja pasar la atmósfera), y colores del cenit y del
//   horizonte (SKYU.uZen / uHor), que ya usan el mar, las fachadas, la niebla, la luz del entorno y el fondo de la página.
// - En la tarjeta (TSL), GT.cieloCol(d, base): reparte esos colores por el cielo como lo haría la atmósfera (resplandor
//   alrededor del sol, horizonte más claro, lado contrario más apagado y disco del sol). Lo usa el cielo y el mapa de
//   entorno (PMREM) de los reflejos de coches, charcos y cristales. Con nubes, néboa o de noche se va apagando solo.
// - Lo que otros ponen a mano (carrera al atardecer rosa, hora azul de Navidad, tiempo cubierto) sigue mandando en los
//   colores: el cielo físico solo pone la forma de la luz encima.
// Con window.__CIELOFIS_OFF=true en la consola se vuelve al cielo de antes (degradado) sin recargar.
const CFIS={lat:42.2406,lon:-8.7207,dia:227,tur:2.6,ray:1,mie:.005,kZ:.2137,kH:.3273,E:.45,ok:false,
 TR:[5.804542996261093e-6,1.3562911419845635e-5,3.0265902468824876e-5],MC:[1.8399918514433978e14,2.7798023919660528e14,4.0790479543861094e14],
 bR:[0,0,0],bM:[0,0,0],sE:0,z:[0,0,0],h:[0,0,0],t:[0,0,0],s:[0,1,0],F:[1,1,1]};
window.CFIS=CFIS;
(()=>{const q=/[?&]dia=([^&#]+)/.exec(location.search);if(!q)return;
 if(q[1]==='hoy'){const d=new Date();CFIS.dia=Math.floor((d-new Date(d.getFullYear(),0,0))/864e5)}else if(+q[1]>=1&&+q[1]<=366)CFIS.dia=Math.round(+q[1])})();
// uniforms nuevos del cielo (SKYU se crea más abajo en la página: se añaden la primera vez que hacen falta)
function cfisU(){if(SKYU.uBR)return;const V=()=>({value:new THREE.Vector3()});
 Object.assign(SKYU,{uBR:V(),uBM:V(),uSE:{value:0},uPZ:V(),uPH:V(),uSunC:V(),uFis:{value:1}});SKYU.uSunC.value.set(1,.96,.86)}
// posición del sol sobre Vigo a la hora h (hora de reloj): deja en out la dirección (x este, y arriba, z sur) y devuelve el seno de la altura
function solVigo(h,out){const tz=CFIS.dia>=87&&CFIS.dia<=300?2:1,hu=h-tz,g=2*Math.PI/365*(CFIS.dia-1+(hu-12)/24);
 const eq=229.18*(.000075+.001868*Math.cos(g)-.032077*Math.sin(g)-.014615*Math.cos(2*g)-.040849*Math.sin(2*g));
 const de=.006918-.399912*Math.cos(g)+.070257*Math.sin(g)-.006758*Math.cos(2*g)+.000907*Math.sin(2*g)-.002697*Math.cos(3*g)+.00148*Math.sin(3*g);
 const H=(hu*60+eq+4*CFIS.lon)/4*Math.PI/180-Math.PI,f=CFIS.lat*Math.PI/180;
 const se=Math.max(-1,Math.min(1,Math.sin(f)*Math.sin(de)+Math.cos(f)*Math.cos(de)*Math.cos(H))),ce=Math.sqrt(1-se*se);
 const az=Math.atan2(Math.sin(H),Math.cos(H)*Math.sin(f)-Math.tan(de)*Math.cos(f))+Math.PI;   // desde el norte, hacia el este
 out.set(Math.sin(az)*ce,se,-Math.cos(az)*ce);return se}
// luz del cielo en la dirección d (Preetham), en el mismo espacio que el shader: o = [r,g,b]
function cfisP(dx,dy,dz,o){const C=CFIS,s=C.s,cy=Math.max(dy,0),za=Math.acos(cy),inv=1/(cy+.15*Math.pow(93.885-za*57.29578,-1.253));
 const ct=dx*s[0]+dy*s[1]+dz*s[2],rp=.0596831*(1+(ct*.5+.5)**2),mp=.0795775*(1-.64)/Math.pow(1.64-1.6*ct,1.5),bl=Math.min(1,Math.max(0,(1-s[1])**5));
 for(let i=0;i<3;i++){const F=Math.exp(-(C.bR[i]*8400+C.bM[i]*1250)*inv),b=(C.bR[i]*rp+C.bM[i]*mp)/(C.bR[i]+C.bM[i]);
  let L=Math.pow(C.sE*b*(1-F),1.5);L*=1+(Math.sqrt(C.sE*b*F)-1)*bl;o[i]=Math.pow((L+.1*F)*.04+[0,.0003,.00075][i],.9167)}return o}
const _cfL=c=>.2126*c[0]+.7152*c[1]+.0722*c[2];
// colores del juego a partir de la luz física: el tono tal cual, el brillo más suave (que la tarde no quede a oscuras)
function _cfCol(c,k,out){const l=Math.max(_cfL(c),1e-6),m=k*Math.pow(l,CFIS.E)/l;return out.setRGB(c[0]*m,c[1]*m,c[2]*m,THREE.LinearSRGBColorSpace)}
const _cfZ=new THREE.Color(),_cfH=new THREE.Color();
// se llama en cielo() con la dirección del sol ya puesta: calcula la atmósfera y mezcla los colores del cielo (zen, hor)
function cieloFis(sd,el,zen,hor){cfisU();const C=CFIS;C.ok=!window.__CIELOFIS_OFF;SKYU.uFis.value=C.ok?1:0;if(!C.ok)return;
 // aire más turbio con néboa, nubes o lluvia (sol más pálido, horizonte más blanco)
 const W=window.TIEMPO&&TIEMPO.W||{cov:0,fog:0,rain:0},tur=C.tur+3.5*Math.max(W.fog,W.rain*.7)+1.2*W.cov;
 C.s[0]=sd.x;C.s[1]=sd.y;C.s[2]=sd.z;
 C.sE=1000*Math.max(0,1-Math.exp(-((1.6110731556870734-Math.acos(Math.max(-1,Math.min(1,sd.y))))/1.5)));
 const cm=.434*(.2*tur*10e-18);for(let i=0;i<3;i++){C.bR[i]=C.TR[i]*C.ray;C.bM[i]=cm*C.MC[i]*C.mie}
 SKYU.uBR.value.fromArray(C.bR);SKYU.uBM.value.fromArray(C.bM);SKYU.uSE.value=C.sE;
 // cenit y media del horizonte (8 rumbos)
 cfisP(0,1,0,C.z);const h=C.h;h[0]=h[1]=h[2]=0;
 for(let a=0;a<8;a++){const t=a*Math.PI/4;cfisP(Math.cos(t)*.9998,.02,Math.sin(t)*.9998,C.t);h[0]+=C.t[0]/8;h[1]+=C.t[1]/8;h[2]+=C.t[2]/8}
 SKYU.uPZ.value.fromArray(C.z);SKYU.uPH.value.fromArray(h);
 // lo que deja pasar la atmósfera hacia el sol: su color (blanco cálido a mediodía, naranja y rojo al ponerse)
 {const za=Math.acos(Math.max(0,sd.y)),inv=1/(Math.max(sd.y,0)+.15*Math.pow(93.885-za*57.29578,-1.253));
  for(let i=0;i<3;i++)C.F[i]=Math.exp(-(C.bR[i]*8400+C.bM[i]*1250)*inv);const mx=Math.max(C.F[0],1e-4);
  SKYU.uSunC.value.set(C.F[0]/mx,Math.max(C.F[1]/mx,.08),Math.max(C.F[2]/mx,.03))}
 // de día manda el cielo físico; en el crepúsculo se mezcla con los colores de siempre de la hora azul y la noche
 const w=THREE.MathUtils.smoothstep(el,-.06,.1);
 _cfCol(C.z,C.kZ,_cfZ);_cfCol(h,C.kH,_cfH);zen.lerp(_cfZ,w);hor.lerp(_cfH,w)}
// luz: el sol toma el color que deja pasar la atmósfera; la luz del cielo (hemisferio), el tono del cielo de ese momento
function cieloFisLuz(el,day){if(!CFIS.ok)return;const w=THREE.MathUtils.smoothstep(el,-.05,.12);
 if(w>0){const c=SKYU.uSunC.value;_cfZ.setRGB(.15+.85*c.x,.15+.85*c.y,.15+.85*c.z,THREE.LinearSRGBColorSpace);sun.color.lerp(_cfZ,w*.85)}
 const z=SKYU.uZen.value,hz=SKYU.uHor.value,l=Math.max(.2126*(z.r+hz.r)+.7152*(z.g+hz.g)+.0722*(z.b+hz.b),1e-4);
 _cfH.setRGB((z.r+hz.r)/l,(z.g+hz.g)/l,(z.b+hz.b)/l,THREE.LinearSRGBColorSpace);hemi.color.lerp(_cfH,.35*day*w)}
// TSL: el cielo de la dirección d con la forma de la atmósfera, partiendo del degradado base (cenit/horizonte del juego)
GT.cieloCol=(d,base)=>{cfisU();const T=TSL,{vec3,float,max,min,pow,exp,dot,clamp,mix,smoothstep,normalize,acos}=T;
 const uBR=GT.U(SKYU.uBR),uBM=GT.U(SKYU.uBM),uSE=GT.U(SKYU.uSE),uPZ=GT.U(SKYU.uPZ),uPH=GT.U(SKYU.uPH),uSun=GT.U(SKYU.uSun),uN=GT.U(SKYU.uNight),uCov=GT.U(SKYU.uCov),uFis=GT.U(SKYU.uFis);
 const sd=normalize(uSun),cy=max(d.y,0),za=acos(min(cy,1));
 const inv=float(1).div(cy.add(pow(float(93.885).sub(za.mul(57.29578)),-1.253).mul(.15)));
 const Fex=exp(uBR.mul(8400).add(uBM.mul(1250)).mul(inv).negate());
 const ct=clamp(dot(d,sd),-1,1),rp=ct.mul(.5).add(.5),rPh=rp.mul(rp).add(1).mul(.0596831);
 const mPh=float(.0795775*.36).div(pow(float(1.64).sub(ct.mul(1.6)),1.5));
 const bT=uBR.mul(rPh).add(uBM.mul(mPh)).div(uBR.add(uBM)),sb=bT.mul(uSE);
 const Lin=pow(sb.mul(Fex.oneMinus()),vec3(1.5)).mul(mix(vec3(1),pow(sb.mul(Fex),vec3(.5)),clamp(pow(sd.y.oneMinus(),5),0,1)));
 const L0=Fex.mul(.1).add(Fex.mul(uSE.mul(19000)).mul(smoothstep(.99995668,.99997668,ct)));   // disco del sol
 const P=pow(Lin.add(L0).mul(.04).add(vec3(0,.0003,.00075)),vec3(.9167));
 const G=mix(uPH,uPZ,pow(cy,.5));
 const r0=pow(P.div(max(G,vec3(1e-5))),vec3(.5)),rm=max(max(r0.x,r0.y),max(r0.z,1e-5)),r=r0.mul(min(float(4).div(rm),1));   // sin quemar el tono (el rojo del ocaso sigue rojo)
 const k=max(max(smoothstep(.55,.95,uN),uCov.mul(.85)),uFis.oneMinus());
 return base.mul(mix(r,vec3(1),k))};
// el cielo de fondo: como gpuCielo (luna, estrellas y nubes), pero con la luz de la atmósfera y nubes teñidas por el sol
function gpuCieloFis(){GT.ini();cfisU();const{vec2,vec3,float,normalize,max,mix,pow,dot,smoothstep,step,sin,floor,select,positionLocal}=TSL;
 const uSun=GT.U(SKYU.uSun),uZen=GT.U(SKYU.uZen),uHor=GT.U(SKYU.uHor),uT=GT.U(SKYU.uT),uNight=GT.U(SKYU.uNight),uDusk=GT.U(SKYU.uDusk),uCov=GT.U(SKYU.uCov),uSunC=GT.U(SKYU.uSunC),uFis=GT.U(SKYU.uFis);
 const d=normalize(positionLocal),y=max(d.y,0),sd=normalize(uSun),dia=uNight.oneMinus();
 let col=GT.cieloCol(d,mix(uHor,uZen,pow(y,.5)));
 const cs=max(dot(d,sd),0);
 col=col.add(vec3(1,.62,.32).mul(pow(cs,6)).mul(uDusk.mul(.6).add(.25)).mul(dia).mul(uFis.oneMinus()));      // halo del sol (solo el cielo de antes)
 col=col.add(uSunC.mul(smoothstep(.999,.9996,cs)).mul(dia).mul(smoothstep(-.03,.02,sd.y)));                  // disco del sol
 const cm=max(dot(d,sd.negate()),0);col=col.add(vec3(.85,.88,1).mul(smoothstep(.9993,.9997,cm)).mul(uNight));   // luna
 const sp=floor(d.xz.div(d.y.add(.25)).mul(70));const st=step(.9965,GT.h21(sp)).mul(sin(uT.mul(2).add(GT.h21(sp.add(3)).mul(40))).mul(.5).add(.5));
 col=col.add(vec3(st).mul(uNight).mul(smoothstep(.02,.25,y)));                                                // estrellas
 const cp=d.xz.div(d.y.add(.12)).mul(1.4).add(vec2(uT.mul(.01),uT.mul(.004)));
 const c=smoothstep(float(.5).sub(uCov.mul(.42)),float(.8).sub(uCov.mul(.3)),GT.fbm(cp)).mul(smoothstep(0,.1,y));
 let cl=mix(vec3(1,.99,.97),vec3(1,.66,.52),uDusk);cl=mix(cl,vec3(.16,.18,.28),uNight);
 cl=cl.mul(mix(vec3(1),uSunC.mul(.55).add(.45),dia.mul(uFis)));                                              // nubes teñidas por el sol
 cl=cl.mul(pow(cs,8).mul(.35).mul(dia).mul(uFis).add(1));                                                     // y más claras cerca de él
 cl=cl.mul(GT.fbm(cp.mul(2.3).add(3)).mul(.3).add(.78));cl=mix(cl,cl.mul(vec3(.62,.64,.70)),uCov.mul(.8));
 col=mix(col,cl,c.mul(.92));
 const m=new THREE.MeshBasicNodeMaterial({side:THREE.BackSide,depthWrite:false,depthTest:false,fog:false});
 m.colorNode=select(d.y.lessThan(0),uHor,col);return m}
// ---------- fin de gpu_cielofis.js
