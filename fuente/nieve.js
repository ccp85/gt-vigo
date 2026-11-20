// ---------- nevada de Navidad (nieve.js, lo mete edit_nieve.py)
// Durante el reparto de Navidad (y la carrera de Navidad) nieva sobre Vigo y la nieve va cuajando poco a poco:
//  - copos grandes y pequeños que caen alrededor de la cámara, con rachas de viento; la nevada arrecia con el tiempo
//  - todo lo que mira hacia arriba (calles, aceras, plazas, tejados, copas de árboles, techos de coches) se va
//    cubriendo de blanco: primero manchas sueltas, luego casi todo; con brillos de escarcha
//  - escarcha en los bordes de la pantalla que crece con la nevada
// Al salir del modo Navidad la nieve desaparece (el mundo abierto queda como estaba).
const NVE={u:{value:0},t:0,on:false,a:0,pend:[],tScan:0,pts:null,uT:{value:0},uK:{value:0},uC:{value:new THREE.Vector3()},uSc:{value:800},uWd:{value:new THREE.Vector2()},wd:new THREE.Vector2(),racha:0,div:null};
window.__NVE=NVE;
const NVE_TAU=95; // segundos: a los ~1,5 min media ciudad blanca, a los 3 min casi toda
// ---- acumulación: parche a los materiales del mundo
function nveSalta(o,m){if(!m||m.userData.nv)return true;
 if(!(m.isMeshStandardMaterial||m.isMeshLambertMaterial||m.isMeshPhongMaterial))return true;
 if(m.transparent||m.depthWrite===false||m.userData.noNieve)return true;
 if(typeof WATERS!=='undefined'&&WATERS.includes(m))return true;
 if(/agua|mar_|cielo|nube|halo|luz|led/i.test((o.name||'')+' '+(m.name||'')))return true;
 return false}
function nvePatch(m){m.userData.nv=1;const prev=m.onBeforeCompile;
 const own=Object.prototype.hasOwnProperty.call(m,'customProgramCacheKey'),pk=own?m.customProgramCacheKey.bind(m):null,k0=own?'':String(prev);
 m.onBeforeCompile=function(sh,r){if(prev)prev.call(this,sh,r);
  if(!sh.vertexShader.includes('#include <worldpos_vertex>')||!sh.fragmentShader.includes('#include <normal_fragment_maps>')||!sh.fragmentShader.includes('#include <opaque_fragment>'))return;
  sh.uniforms.uNvA=NVE.u;
  sh.vertexShader='varying vec3 vNvW;\n'+sh.vertexShader.replace('#include <worldpos_vertex>',`#include <worldpos_vertex>
{vec4 nvP=vec4(transformed,1.);
#ifdef USE_BATCHING
nvP=batchingMatrix*nvP;
#endif
#ifdef USE_INSTANCING
nvP=instanceMatrix*nvP;
#endif
vNvW=(modelMatrix*nvP).xyz;}`);
  sh.fragmentShader='uniform float uNvA;varying vec3 vNvW;\nfloat hNv(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}\nfloat nNv(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hNv(i),hNv(i+vec2(1,0)),f.x),mix(hNv(i+vec2(0,1)),hNv(i+vec2(1,1)),f.x),f.y);}\n'+sh.fragmentShader
   .replace('#include <normal_fragment_maps>',`#include <normal_fragment_maps>
 float nvM=0.;
 if(uNvA>.001){vec3 upV=normalize((viewMatrix*vec4(0.,1.,0.,0.)).xyz);float up=dot(normal,upV);
  float n=nNv(vNvW.xz*14.)*.5+nNv(vNvW.xz*47.)*.32+nNv(vNvW.xz*150.)*.18;
  float c=uNvA*1.25-.12+(up-.9)*.6;
  nvM=smoothstep(n-.07,n+.05,c)*smoothstep(.5,.82,up);
  vec3 sn=vec3(.9,.93,.98)*(.93+.07*nNv(vNvW.xz*260.));
  diffuseColor.rgb=mix(diffuseColor.rgb,sn,nvM);
#ifdef STANDARD
  roughnessFactor=mix(roughnessFactor,.78,nvM);metalnessFactor=mix(metalnessFactor,0.,nvM);
#endif
 }`)
   .replace('#include <opaque_fragment>',`if(nvM>.001){outgoingLight+=nvM*vec3(.05,.06,.1);
  float gl=step(.993,hNv(floor(vNvW.xz*1300.)));outgoingLight+=nvM*gl*vec3(.7,.8,1.)*(.5+.5*uNvA);}
 #include <opaque_fragment>`)};
 // nitido.js (móvil) mira el código de onBeforeCompile para no pasar a mate el asfalto mojado: que siga viéndolo
 const ob=m.onBeforeCompile;ob.toString=()=>String(prev)+'/*nieve*/';
 m.customProgramCacheKey=()=>(own?pk():k0)+'|nieve';m.needsUpdate=true}
function nveEscanea(){scene.traverse(o=>{if(!o.isMesh||o.isPoints)return;for(const m of [].concat(o.material)){if(!nveSalta(o,m)){m.userData.nv=2;NVE.pend.push(m)}}})}
// ---- copos que caen alrededor de la cámara
function nveCopos(){const LT=!!window.LITE,N=LT?1500:3600,p=new Float32Array(N*3),s=new Float32Array(N*2);
 for(let k=0;k<N;k++){p[k*3]=Math.random();p[k*3+1]=Math.random();p[k*3+2]=Math.random();s[k*2]=Math.random();s[k*2+1]=Math.random()}
 const ge=new THREE.BufferGeometry();ge.setAttribute('position',new THREE.BufferAttribute(p,3));ge.setAttribute('aS',new THREE.BufferAttribute(s,2));
 const m=new THREE.ShaderMaterial({uniforms:{uT:NVE.uT,uK:NVE.uK,uC:NVE.uC,uSc:NVE.uSc,uWd:NVE.uWd},transparent:true,depthWrite:false,
  vertexShader:`#include <common>
#include <logdepthbuf_pars_vertex>
attribute vec2 aS;uniform float uT,uK,uSc;uniform vec3 uC;uniform vec2 uWd;varying float vA,vB;const vec3 B=vec3(4.4,2.6,4.4);
void main(){float sz=.35+.65*aS.x*aS.x;vec3 w=position*B;w.y-=uT*(.1+.13*sz);w.x+=uWd.x*(.7+.6*sz)+sin(uT*(.7+aS.y)+position.z*40.)*.06;w.z+=uWd.y*(.7+.6*sz)+cos(uT*(.6+aS.y)+position.x*40.)*.06;
 vec3 q=mod(w-uC,B)-B*.5+uC;q.y+=.5;vec4 mv=viewMatrix*vec4(q,1.);gl_Position=projectionMatrix*mv;float d=-mv.z;
 float vis=step(aS.y,uK);gl_PointSize=vis*clamp(.02*sz*uSc/d,1.,LTMAX);vB=sz;
 vA=vis*smoothstep(2.8,1.4,d)*smoothstep(.04,.18,d)*(.55+.4*sz);
#include <logdepthbuf_vertex>
}`.replace('LTMAX',LT?'10.':'16.'),
  fragmentShader:`#include <logdepthbuf_pars_fragment>
varying float vA,vB;void main(){
#include <logdepthbuf_fragment>
vec2 q=gl_PointCoord-.5;float r=length(q)*2.;float a=smoothstep(1.,.25,r);
float st=pow(abs(cos(atan(q.y,q.x)*3.)),10.)*smoothstep(1.,.2,r)*step(.6,vB);a=max(a*.85,st*.7);
if(a<.02)discard;gl_FragColor=vec4(.95,.97,1.,a*vA);}`});
 const pt=new THREE.Points(ge,m);pt.frustumCulled=false;pt.renderOrder=7;pt.visible=false;pt.name='nieve_copos';scene.add(pt);NVE.pts=pt}
// ---- escarcha en los bordes de la pantalla
function nveEscarcha(){const d=document.createElement('div');d.id='nvEsc';d.style.cssText='position:fixed;inset:0;pointer-events:none;z-index:4;opacity:0;transition:opacity .6s;background:radial-gradient(ellipse 75% 70% at 50% 50%,rgba(230,240,255,0) 62%,rgba(230,240,255,.35) 85%,rgba(245,250,255,.75) 100%)';document.body.appendChild(d);NVE.div=d}
function nieveActiva(){return (typeof REP!=='undefined'&&REP.on)||(typeof NAV!=='undefined'&&NAV.on)}
function nieveTick(dt){const on=nieveActiva();
 if(on&&!NVE.on){NVE.t=0;NVE.tScan=0;if(!NVE.pts)nveCopos();if(!NVE.div)nveEscarcha()}
 NVE.on=on;
 if(!on){if(NVE.u.value>0)NVE.u.value=Math.max(0,NVE.u.value-dt*2);if(NVE.pts)NVE.pts.visible=false;if(NVE.div)NVE.div.style.opacity=0;return}
 NVE.t+=dt;const a=1-.86*Math.exp(-NVE.t/NVE_TAU);NVE.a=a;NVE.u.value=a;
 // materiales nuevos (zonas que se cargan al moverse) se van cubriendo también; unos pocos por fotograma para no dar tirones
 NVE.tScan-=dt;if(NVE.tScan<=0){NVE.tScan=1.2;nveEscanea()}
 for(let k=window.LITE?10:30;k>0&&NVE.pend.length;k--)nvePatch(NVE.pend.pop());
 // viento a rachas
 NVE.racha-=dt;if(NVE.racha<=0){NVE.racha=3+Math.random()*5;NVE.vw=new THREE.Vector2((Math.random()-.5)*.16,(Math.random()-.5)*.16)}
 if(NVE.vw){NVE.wd.lerp(NVE.vw,Math.min(1,dt*.5))}NVE.uWd.value.addScaledVector(NVE.wd,dt);
 NVE.uT.value+=dt;NVE.uK.value=.3+.7*Math.min(1,NVE.t/120);
 const vis=driving&&!(MODO==='pie'&&typeof BUC!=='undefined'&&BUC.W);NVE.pts.visible=vis;
 if(vis){NVE.uC.value.copy(pcam.position);NVE.uSc.value=R.domElement.height/(2*Math.tan(pcam.fov*Math.PI/360))}
 NVE.div.style.opacity=(vis?.15+.55*a:0).toFixed(3)}
