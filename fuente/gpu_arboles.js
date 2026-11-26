// ---------- árboles con viento (gpu_arboles.js, solo gpu.html) ----------
// Los árboles (frondosas, pinos y el bosque) se mecen en la tarjeta gráfica: el tronco casi quieto y la copa cada vez más
// cuanto más alta, con las mismas ráfagas que recorren la hierba (misma dirección y mismo ruido), un vaivén lento propio de
// cada árbol y las hojas temblando. Con lluvia sopla más. Al pasar cerca el protagonista o el vehículo las ramas se apartan
// y, si vas rápido, la copa se sacude. También vuelve el ruido de hojas y el tronco pardo (hojas() era GLSL y aquí no
// se aplicaba). Solo se mueven jugando (en la maqueta quedan quietos). Con window.__ARBOLES_OFF=true se paran.
function gpuArbol(m){try{if(!m||m.userData.g_arbol)return;m.userData.g_arbol=1;GT.ini();
 const{vec2,vec3,float,sin,mix,smoothstep,max,clamp,length,dot,select,attribute,positionLocal,positionGeometry,positionWorld,instanceIndex,uniform,fwidth}=TSL;
 const AV=window.__AV||(window.__AV={uT:uniform(0),uPl:uniform(new THREE.Vector3(0,0,-99)),uOn:uniform(0),on:0,n:0});
 const uT=AV.uT,uPl=AV.uPl,uOn=AV.uOn,uWet=GT.U(UMO.uWet),LT=!!window.LITE;
 const hoja=attribute('hoja','float'),v=clamp(positionGeometry.y,0,1.3).div(1.1),curva=v.mul(v);
 const p=positionLocal,q=p.xz,wd=vec2(.82,.57),wp=vec2(-.57,.82),fuerza=uWet.mul(.8).add(1);
 // ráfagas como en la hierba + vaivén propio de cada árbol (fase al azar por instancia)
 const ph=GT.h21(vec2(float(instanceIndex).mul(.137),3.1)).mul(6.283);
 const gust=GT.vn(q.mul(3.5).sub(wd.mul(uT.mul(.9))));
 const sway=sin(uT.mul(1.3).add(ph)).mul(.3).add(sin(uT.mul(2.7).add(ph.mul(1.7))).mul(.12)).add(gust.mul(1.25)).add(.15);
 const lado=sin(uT.mul(1.7).add(ph.mul(2.3))).mul(.22).add(gust.sub(.5).mul(.3));
 const amp=float(.0026).mul(fuerza).mul(curva);
 // temblor de las hojas (solo copa, más con ráfaga)
 const fl=LT?float(0):sin(uT.mul(11).add(dot(q,vec2(900,700))).add(ph)).mul(.0003).mul(hoja).mul(gust.add(.35)).mul(fuerza).mul(v);
 // se aparta al pasar el protagonista o el vehículo; rápido = sacudida
 const dp=q.sub(uPl.xz),dl=length(dp),dirP=dp.div(max(dl,1e-5));
 const cerca=smoothstep(.065,.018,dl).mul(v).mul(hoja.mul(.7).add(.3));
 const empuje=cerca.mul(float(.0055).add(sin(uT.mul(17).add(ph)).mul(uPl.y).mul(.004)));
 const off=vec3(
  wd.x.mul(sway).add(wp.x.mul(lado)).mul(amp).add(dirP.x.mul(empuje)).add(fl),
  sway.mul(amp).mul(-.18).sub(empuje.mul(.25)).add(fl.mul(.6)),
  wd.y.mul(sway).add(wp.y.mul(lado)).mul(amp).add(dirP.y.mul(empuje)).add(fl.mul(-.8)));
 m.positionNode=p.add(off.mul(uOn));
 // color (lo que hacía hojas() en GLSL): ruido de hojas a dos escalas en coordenadas de mundo y tronco pardo
 const W=positionWorld,fw=length(fwidth(W)),n1=GT.vn3(W.mul(160)),n2=GT.vn3(W.mul(48).add(7));
 const leaf=mix(.5,n1,smoothstep(.002,.01,fw).oneMinus());
 // el tronco no lleva el tinte verde de cada árbol (el motor multiplica el color de la instancia después: se descuenta)
 const tronco=TSL.Fn(bd=>{const t=vec3(.3,.22,.17).mul(n1.mul(.4).add(.8));return bd.object&&bd.object.instanceColor?t.div(max(TSL.instanceColor,vec3(.05))):t})();
 GT.cadena(m,b=>{const c=b.mul(leaf.mul(.55).add(.7)).mul(n2.mul(.28).add(.86));
  return select(hoja.lessThan(.5),tronco,mix(c,c.mul(vec3(1.05,1.08,.86)),smoothstep(.55,.8,n2)))});
 AV.n++}catch(e){console.warn('árboles TSL',e)}}
function arbolesTick(dt){const AV=window.__AV;if(!AV)return;
 const on=driving&&!window.__ARBOLES_OFF&&!(MODO==='heli'&&pcam.position.y>.6)?1:0;
 AV.on+=(on-AV.on)*Math.min(1,dt*2);AV.uOn.value=AV.on;if(AV.on<.001)return;
 AV.uT.value+=dt;const sp=Math.abs(P.v||0);AV.uPl.value.set(P.x,Math.min(1,Math.max(0,(sp-.05)/.6)),P.y)}
// ---------- fin de gpu_arboles.js
