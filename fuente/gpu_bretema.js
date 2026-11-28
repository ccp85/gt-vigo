// ---------- brétema y perspectiva aérea (gpu_bretema.js) ----------
// Sustituye la niebla lineal de three.js (scene.fog) por una niebla en TSL con tres capas, en todos los materiales:
//  1) Perspectiva aérea: lo lejano se va azulando (el aire entre tú y Cangas o Rande dispersa el azul del cielo) y a
//     contraluz se calienta con el color del sol. Empieza antes que la niebla de siempre y no la sustituye.
//  2) La niebla de siempre (FOG al conducir, FOGM de calima en la maqueta) con las mismas distancias, así sigue tapando
//     lo que aún no ha cargado; a contraluz toma el tono del sol, como el cielo físico que tiene detrás.
//  3) Brétema: niebla baja que se pega al mar y a lo hondo (la densidad cae con la altura, unos 35 m de capa), a jirones
//     que se mueven con el viento. Sale con néboa, un poco por las mañanas de días tranquilos y, muy fina, siempre sobre
//     la ría. El Castro, A Guía o el puente de Rande asoman por encima. Con néboa la niebla de siempre se abre un poco
//     para que se vea la capa baja en vez de un muro gris.
// En túneles y bajo el agua solo queda la niebla de siempre (con su color). Se calcula para cada cámara: la de la maqueta
// (ortográfica), la del coche, la del reflejo del mar y la del cubo de reflejos.
// Con window.__BRETEMA_OFF=true vuelve la niebla de antes. window.BRT.forzar=0..1 fuerza la cantidad de brétema (pruebas).
const BRT={U:null,nodo:null,ini:false,b:0,forzar:null,_v:null};window.BRT=BRT;
// uniforms de la niebla: en el grupo de dibujo (render). Dentro de scene.fogNode, los del grupo por objeto no se actualizan.
GT.RU=o=>GT.U(o).setGroup(TSL.renderGroup);
function brtU(){if(!BRT.U){cfisU();const V=n=>({value:n});BRT.V={uOn:V(0),uCol:V(new THREE.Color()),uNear:V(5),uFar:V(20),uAer:V(1),uOrt:V(0),uFwd:V(new THREE.Vector3(0,-1,0)),uB:V(0),uT:V(0),uAm:V(.5),uBrC:V(new THREE.Color(.8,.82,.85))};
 BRT.U={};for(const k in BRT.V)BRT.U[k]=GT.RU(BRT.V[k])}return BRT.U}   // los valores van en BRT.V (los uniforms leen de ahí en cada dibujo)
// brétema integrada a lo largo del rayo desde el punto p hasta la cámara c (v: dirección de la mirada; ort: sin fin, cámara de maqueta)
GT.bretema=(p,c,v,ort)=>{const T=TSL,{vec2,float,max,abs,exp,select,smoothstep,length}=T,U=brtU(),b=1/.35,yp=max(p.y.add(.04),0);
 const jir=GT.vn(p.xz.mul(.06).add(vec2(U.uT.mul(.006),U.uT.mul(.0025)))).mul(.6).add(GT.vn(p.xz.mul(.21).sub(vec2(U.uT.mul(.004),0))).mul(.4));
 const a=U.uB.mul(smoothstep(.15,.75,jir).mul(.85).add(.3)).mul(U.uAer);
 const L=ort?select(ort,float(60),max(length(p.sub(c)),1e-4)):max(length(p.sub(c)),1e-4);
 const k=float(b).mul(v.y.negate()).mul(L).clamp(-20,400);
 const ik=select(abs(k).lessThan(1e-3),float(1),exp(k.negate()).oneMinus().div(k));
 return exp(a.mul(exp(yp.mul(-b))).mul(L).mul(ik).negate()).oneMinus().clamp(0,.97)};
// color del aire lejano (azul del cielo, cálido hacia el sol) y de la brétema
GT.aire=v=>{const T=TSL,{vec3,mix,max,dot,pow,normalize,smoothstep,luminance}=T,U=brtU();
 const sd=normalize(GT.RU(SKYU.uSun)),uZen=GT.RU(SKYU.uZen),uHor=GT.RU(SKYU.uHor),uSunC=GT.RU(SKYU.uSunC),uN=GT.RU(SKYU.uNight);
 const glow=pow(max(dot(v,sd),0),6).mul(uN.oneMinus()).mul(smoothstep(-.05,.06,sd.y)).mul(U.uAer),lh=luminance(uHor);
 return{glow,aer:mix(mix(uHor,uZen,.42),uSunC.mul(lh).mul(1.25),glow.mul(.55)),bre:U.uBrC.mul(mix(vec3(1),uSunC,glow.mul(.6))).mul(glow.mul(.5).add(1)),sunC:uSunC}};
// montes y mar del fondo (más allá de la niebla): azulados por el aire y con la brétema pegada al agua
GT.fondoNeb=(c,d,W,uNear,uCam)=>{const T=TSL,{mix,clamp,smoothstep,normalize}=T,U=brtU(),v=normalize(W.sub(uCam)),A=GT.aire(v);
 const h=smoothstep(uNear,uNear.add(160),d);let o=mix(c,A.aer,clamp(h.mul(.5).add(.3),0,.8).mul(U.uAer).mul(U.uAm.mul(1.6)));
 return mix(o,A.bre,GT.bretema(W,uCam,v,null))};
function bretemaNodo(){GT.ini();cfisU();const T=TSL,{Fn,vec2,vec3,vec4,float,max,min,mix,exp,abs,dot,normalize,smoothstep,pow,select,clamp,length,luminance,positionWorld,positionView,cameraPosition,output}=T;
 const U=brtU();
 return Fn(()=>{const viewZ=positionView.z.negate(),p=positionWorld,ort=U.uOrt.greaterThan(.5);
  const v=select(ort,U.uFwd,normalize(p.sub(cameraPosition)));                                   // hacia dónde mira el rayo
  const A=GT.aire(v),glow=A.glow;
  // 1) perspectiva aérea: azul del cielo entre medias, más cálida mirando hacia el sol
  const a0=select(ort,U.uNear,U.uNear.mul(.4)),sp=select(ort,U.uFar.sub(U.uNear).mul(.25),U.uFar.sub(a0)),ar=clamp(viewZ.sub(a0).div(sp.max(1e-3)),0,1);   // en la maqueta, desde el centro de la vista
  const aer=ar.mul(ar.mul(-.5).add(1.5)).mul(U.uAm).mul(U.uAer).mul(U.uOn),aerCol=A.aer;
  // 2) la niebla de siempre (mismas distancias), con el tono del sol a contraluz
  const rf=smoothstep(U.uNear,U.uFar,viewZ).mul(U.uOn);
  const fogCol=U.uCol.mul(mix(vec3(1),A.sunC.mul(1.3),glow.mul(.5)));
  // 3) brétema: densidad a·e^(−b·y) integrada a lo largo del rayo hasta la cámara (en la maqueta, hasta el cielo)
  const hf=GT.bretema(p,cameraPosition,v,ort).mul(U.uOn),brCol=A.bre;
  let c=mix(output.rgb,aerCol,aer);c=mix(c,fogCol,rf);c=mix(c,brCol,hf);
  return vec4(c,output.a)})()}
// cada vez que se dibuja la escena (con cualquier cámara): la niebla que toque y cómo mira la cámara
const _brF=new THREE.Vector3();
function bretemaAntes(r,sc,camR){const U=BRT.V;if(!U)return;const f=sc.fog;U.uOn.value=f?1:0;if(!f)return;
 U.uCol.value.copy(f.color);U.uOrt.value=camR&&camR.isOrthographicCamera?1:0;if(camR)U.uFwd.value.copy(camR.getWorldDirection(_brF));
 // en túneles y bajo el agua, solo la niebla de siempre
 const raro=f===FOG&&(window.__BAJO||(typeof P!=='undefined'&&P.tun));U.uAer.value=raro?0:1;
 // con néboa la niebla de siempre se abre (hasta el doble) y manda la capa baja
 const W=TIEMPO.W,R=raro?1:1+.6*W.fog;U.uNear.value=f.near*(raro?1:1+.4*W.fog);U.uFar.value=f.near+(f.far-f.near)*R;U.uFar.value=Math.max(U.uFar.value,U.uNear.value+1e-3)}
// cada imagen (desde cielo()): cuánta brétema hay
function bretemaTick(dt){if(window.__BRETEMA_OFF){if(BRT.ini){scene.fogNode=null;scene.onBeforeRender=BRT.prevOBR||(()=>{});BRT.ini=false}return}
 if(!BRT.ini){if(!BRT.nodo)BRT.nodo=bretemaNodo();BRT.prevOBR=scene.onBeforeRender;const prev=BRT.prevOBR;
  scene.onBeforeRender=function(r,sc,c,rt){try{prev&&prev.call(this,r,sc,c,rt)}catch(e){}bretemaAntes(r,sc,c)};scene.fogNode=BRT.nodo;BRT.ini=true}
 const U=BRT.V,W=TIEMPO.W,h=CIELO.h;U.uT.value+=dt;
 try{bretemaAntes(R,scene,driving?pcam:cam)}catch(e){}   // la cámara principal, ya para esta imagen
 // mañanas tranquilas: brétema sobre la ría que se levanta hacia media mañana
 const man=THREE.MathUtils.smoothstep(h,6.3,7.8)*(1-THREE.MathUtils.smoothstep(h,9.6,11.6))*(1-W.rain)*(1-.6*W.cov);
 const obj=BRT.forzar!=null?BRT.forzar*1.7:Math.max(1.7*W.fog,1.7*(W.bre||0),.42*man,.02+.06*W.cov);
 BRT.b+=(obj-BRT.b)*Math.min(1,dt*.5);U.uB.value=BRT.b;
 U.uAm.value=.5-.15*CIELO.nf;
 // color de la brétema: lo que vería una pared blanca iluminada por el sol (desde arriba) y el cielo, como una nube baja
 const sy=Math.max(0,SKYU.uSun.value.y),c=U.uBrC.value,sc=sun.intensity*(.35+.65*sy)*(CIELO.nf>.55?.5:1),hc=hemi.intensity;
 c.setRGB((sun.color.r*sc+hemi.color.r*hc*.85+hemi.groundColor.r*hc*.15)/Math.PI*.9,(sun.color.g*sc+hemi.color.g*hc*.85+hemi.groundColor.g*hc*.15)/Math.PI*.9,
  (sun.color.b*sc+hemi.color.b*hc*.85+hemi.groundColor.b*hc*.15)/Math.PI*.9,THREE.LinearSRGBColorSpace);
 {const l=.2126*c.r+.7152*c.g+.0722*c.b,k=1+.35*(1-CIELO.nf);c.setRGB((c.r+(l-c.r)*.35)*k,(c.g+(l-c.g)*.35)*k,(c.b+(l-c.b)*.35)*k,THREE.LinearSRGBColorSpace)}}   // más blanca: gotitas que esparcen toda la luz
// ---------- fin de gpu_bretema.js
