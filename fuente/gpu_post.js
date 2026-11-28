// calidad alta en WebGPU: cadena de posprocesado en TSL (escena con MSAA → oclusión ambiental GTAO → bloom + rayos de sol →
// tono ACES y sRGB → gradación de color según la hora y el clima → SMAA)
// three/webgpu y three/tsl se cargan sin minificar para que el bloom de addons use los mismos nudos que el motor
function postFallo(e){console.error('posprocesado WebGPU',e);POST.fallo=true;POST.on=false;POST.cargando=false;POST.comp=null;
 try{localStorage.setItem('gtvigo_post','0')}catch(_){}const t_='⚡ Calidad alta no disponible en este equipo';try{if(RACE.on)aviso(t_,2,'peq');else mostrar(t_)}catch(_){}}
function postInit(){if(POST.comp||POST.cargando||POST.fallo)return;POST.cargando=true;
 Promise.all([import('three/addons/tsl/display/BloomNode.js'),import('three/addons/tsl/display/SMAANode.js').catch(()=>null),import('three/addons/tsl/display/GTAONode.js').catch(()=>null)]).then(([{bloom},sm,gt])=>{const T=TSL;
  const sp=T.pass(scene,pcam,{samples:4});const col=sp.getTextureNode('output'),dep=sp.getTextureNode('depth');
  const b=bloom(col,.32,.55,.92);
  const U={uWarm:T.uniform(new THREE.Vector3(1,1,1)),uCool:T.uniform(new THREE.Vector3(1,1,1)),uSat:T.uniform(1.08),uCon:T.uniform(1.06),uLift:T.uniform(0),uLiftC:T.uniform(new THREE.Vector3(1,1,1)),
   uAO:T.uniform(0),uFn:T.uniform(5),uFf:T.uniform(20),uGR:T.uniform(0),uSunUV:T.uniform(new THREE.Vector2(.5,.5)),uSunC:T.uniform(new THREE.Vector3(1,.8,.5)),uAsp:T.uniform(1)};
  // distancia de cada píxel (el buffer de profundidad es logarítmico)
  const vz=d=>T.logarithmicDepthToViewZ(d,T.reference('near','float',pcam),T.reference('far','float',pcam)).negate();
  // 1) oclusión ambiental (GTAO, a media resolución): rincones, portales, bajos de coches y pies de fachada más oscuros;
  //    se apaga con la distancia (en la niebla no hay rincones que oscurecer) y no toca el cielo
  let base=col.rgb;
  if(gt&&gt.ao){const A=gt.ao(dep,null,pcam);A.resolutionScale=.75;A.radius.value=.08;A.thickness.value=.25;A.distanceExponent.value=1;A.scale.value=1.8;A.samples.value=10;
   const at=A.getTextureNode(),px=T.vec2(1.3).div(T.vec2(T.textureSize(at))),s0=T.screenUV;   // suavizado en cruz (quita el grano)
   const ao=at.sample(s0).r.mul(2).add(at.sample(s0.add(px)).r).add(at.sample(s0.sub(px)).r).add(at.sample(s0.add(T.vec2(px.x,px.y.negate()))).r).add(at.sample(s0.add(T.vec2(px.x.negate(),px.y))).r).div(6);
   const d=vz(dep.sample(s0).r),lejos=T.smoothstep(U.uFn,U.uFf,d);
   base=base.mul(T.mix(T.float(1),ao,U.uAO.mul(lejos.oneMinus()).mul(T.smoothstep(.12,.5,d))));POST.ao=A}   // ni pegado a la cámara (suelo rasante)
  // 2) rayos de sol (solo con brétema o atardecer dorado): el cielo que se ve cerca del sol se arrastra hacia él;
  //    los edificios, árboles y el puente lo tapan y dejan los haces
  const rayos=T.Fn(()=>{const r=T.float(0).toVar();T.If(U.uGR.greaterThan(.002),()=>{
    const uv0=T.screenUV,dl=U.uSunUV.sub(uv0).div(28),p=uv0.add(dl.mul(T.interleavedGradientNoise(T.screenCoordinate))).toVar(),w=T.float(1).toVar();
    T.Loop(28,()=>{p.addAssign(dl);const q=p.sub(U.uSunUV).mul(T.vec2(U.uAsp,1));
     const cielo=T.step(.99995,dep.sample(p).r),cerca=T.smoothstep(.42,0,T.length(q));
     r.addAssign(cielo.mul(cerca).mul(w));w.mulAssign(.955)});r.mulAssign(U.uGR.div(28))});return r})();
  const sol=U.uSunC.mul(rayos).mul(1.6);
  const grade=T.Fn(([c])=>{let x=c.rgb;const l=T.luminance(x);
   x=T.mix(T.vec3(l),x,U.uSat);                                              // saturación
   x=T.clamp(x.sub(.5).mul(U.uCon).add(.5),0,1);x=x.mul(x).mul(T.float(3).sub(x.mul(2))).mul(.25).add(x.mul(.75));   // contraste en curva suave
   x=x.mul(T.mix(U.uCool,U.uWarm,T.smoothstep(.15,.75,T.luminance(x))));   // sombras frías, luces cálidas
   x=T.mix(x,U.uLiftC,U.uLift.mul(T.float(1).sub(T.luminance(x))));         // negros levantados (aire húmedo, niebla)
   return T.vec4(x,c.a)});
  const pp=new THREE.RenderPipeline(R);pp.outputColorTransform=false;const gr=grade(T.renderOutput(T.vec4(base.add(b.rgb).add(sol),col.a)));pp.outputNode=sm&&sm.smaa?sm.smaa(gr):gr;   // suavizado de bordes SMAA al final (como edit_suavizado.py)
  POST.comp=pp;POST.bloom=b;POST.U=U;POST.cargando=false;window.POST=POST}).catch(postFallo)}
const _poV=new THREE.Vector3(),_poD=new THREE.Vector3();
function postRender(){postInit();if(!POST.comp){R.render(scene,pcam);return}
 // gradación según la hora y el clima: día limpio, tarde dorada, noche azulada con luces cálidas; plateado frío y suave,
 // dorado cálido y saturado, chubasco frío y algo más duro, brétema y néboa con los negros levantados
 const nf=CIELO.nf,dia=1-nf,du=Math.max(0,1-Math.abs(CIELO.h-20)/2.2)*dia,U=POST.U,b=POST.bloom,W=TIEMPO.W,oro=(W.oro||0)*dia,pla=Math.max(0,W.cov-W.rain)*(W.som||0),ch=W.rain,hu=Math.max(W.fog,W.bre||0);
 U.uWarm.value.set(1.03+.06*du+.04*nf+.06*oro-.03*pla,1.0+.02*du+.02*oro,.96-.08*du-.02*nf-.08*oro+.02*pla);
 U.uCool.value.set(.96-.04*nf-.02*pla-.02*ch,.99,1.03+.07*nf+.03*pla+.04*ch);
 U.uSat.value=1.08+.08*du-.12*nf+.1*oro-.1*pla-.12*ch-.1*hu;U.uCon.value=1.06+.04*du-.06*pla+.05*ch-.08*hu;
 U.uLift.value=.06*hu+.03*pla;U.uLiftC.value.set(.62+.1*oro,.66+.05*oro,.72-.04*oro).multiplyScalar(.35+.65*dia);
 b.strength.value=.18+.2*du+.16*nf+.1*oro+.08*hu;b.threshold.value=nf>.5?.88:.93;b.radius.value=.4+.15*hu;
 // oclusión: más marcada con luz difusa (nublado), menos de noche; mismas distancias que la niebla
 U.uAO.value=window.__AO_OFF?0:(.8+.25*pla)*(1-.35*nf);if(scene.fog){U.uFn.value=scene.fog.near*.6;U.uFf.value=scene.fog.far*.85}
 // rayos de sol: solo con brétema o atardecer dorado, con el sol bajo y por delante de la cámara
 {const sd=SKYU.uSun.value,el=sd.y;pcam.getWorldDirection(_poD);const frente=THREE.MathUtils.smoothstep(_poD.dot(sd),-.05,.35),bajo=1-THREE.MathUtils.smoothstep(el,.35,.65),alto=THREE.MathUtils.smoothstep(el,-.02,.04);
  const g=window.__RAYOS_OFF?0:Math.min(1,Math.max(oro*1.1,(W.bre||0)*1.8))*frente*bajo*alto*dia;U.uGR.value=g;
  if(g>0){_poV.copy(pcam.position).addScaledVector(sd,50).project(pcam);U.uSunUV.value.set(_poV.x*.5+.5,.5-_poV.y*.5)}
  const c=SKYU.uSunC?SKYU.uSunC.value:null;if(c)U.uSunC.value.set(c.x,c.y,c.z);U.uAsp.value=pcam.aspect}
 try{POST.comp.render()}catch(e){postFallo(e);R.render(scene,pcam)}}
