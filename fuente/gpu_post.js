// calidad alta en WebGPU: cadena de posprocesado en TSL (escena con MSAA → bloom → tono y sRGB → gradación de color → SMAA)
// three/webgpu y three/tsl se cargan sin minificar para que el bloom de addons use los mismos nudos que el motor
function postFallo(e){console.error('posprocesado WebGPU',e);POST.fallo=true;POST.on=false;POST.cargando=false;POST.comp=null;
 try{localStorage.setItem('gtvigo_post','0')}catch(_){}const t_='⚡ Calidad alta no disponible en este equipo';try{if(RACE.on)aviso(t_,2,'peq');else mostrar(t_)}catch(_){}}
function postInit(){if(POST.comp||POST.cargando||POST.fallo)return;POST.cargando=true;
 Promise.all([import('three/addons/tsl/display/BloomNode.js'),import('three/addons/tsl/display/SMAANode.js').catch(()=>null)]).then(([{bloom},sm])=>{const T=TSL;
  const sp=T.pass(scene,pcam,{samples:4});const col=sp.getTextureNode('output');
  const b=bloom(col,.32,.55,.92);
  const U={uWarm:T.uniform(new THREE.Vector3(1,1,1)),uCool:T.uniform(new THREE.Vector3(1,1,1)),uSat:T.uniform(1.08),uCon:T.uniform(1.06)};
  const grade=T.Fn(([c])=>{let x=c.rgb;const l=T.luminance(x);
   x=T.mix(T.vec3(l),x,U.uSat);                                              // saturación
   x=T.clamp(x.sub(.5).mul(U.uCon).add(.5),0,1);x=x.mul(x).mul(T.float(3).sub(x.mul(2))).mul(.25).add(x.mul(.75));   // contraste en curva suave
   x=x.mul(T.mix(U.uCool,U.uWarm,T.smoothstep(.15,.75,T.luminance(x))));   // sombras frías, luces cálidas
   return T.vec4(x,c.a)});
  const pp=new THREE.RenderPipeline(R);pp.outputColorTransform=false;const gr=grade(T.renderOutput(col.add(b)));pp.outputNode=sm&&sm.smaa?sm.smaa(gr):gr;   // suavizado de bordes SMAA al final (como edit_suavizado.py)
  POST.comp=pp;POST.bloom=b;POST.U=U;POST.cargando=false;window.POST=POST}).catch(postFallo)}
function postRender(){postInit();if(!POST.comp){R.render(scene,pcam);return}
 // gradación según la hora: día limpio, tarde dorada, noche azulada con luces cálidas
 const nf=CIELO.nf,du=Math.max(0,1-Math.abs(CIELO.h-20)/2.2)*(1-nf),U=POST.U,b=POST.bloom;
 U.uWarm.value.set(1.03+.06*du+.04*nf,1.0+.02*du,.96-.08*du-.02*nf);U.uCool.value.set(.96-.04*nf,.99,1.03+.07*nf);
 U.uSat.value=1.08+.08*du-.12*nf;U.uCon.value=1.06+.04*du;
 b.strength.value=.18+.2*du+.16*nf;b.threshold.value=nf>.5?.88:.93;b.radius.value=.4;
 try{POST.comp.render()}catch(e){postFallo(e);R.render(scene,pcam)}}
