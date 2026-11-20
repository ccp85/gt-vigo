// ---------- nevadas de Navidad (nieve.js, lo mete edit_nieve.py)
// Durante el reparto de Navidad (y la carrera de Navidad) nieva sobre Vigo de vez en cuando: ratos de nevada con copos
// grandes y pequeños alrededor de la cámara y rachas de viento, que llegan y se van poco a poco, y ratos sin nieve.
// La nieve no cuaja: calles, aceras y tejados quedan como siempre. Mientras nieva se escarchan un poco los bordes de la pantalla.
const NVE={t:0,on:false,k:0,obj:1,cambio:0,pts:null,uT:{value:0},uK:{value:0},uC:{value:new THREE.Vector3()},uSc:{value:800},uWd:{value:new THREE.Vector2()},wd:new THREE.Vector2(),racha:0,div:null};
window.__NVE=NVE;
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
// ---- escarcha en los bordes de la pantalla (solo mientras nieva)
function nveEscarcha(){const d=document.createElement('div');d.id='nvEsc';d.style.cssText='position:fixed;inset:0;pointer-events:none;z-index:4;opacity:0;background:radial-gradient(ellipse 75% 70% at 50% 50%,rgba(230,240,255,0) 66%,rgba(230,240,255,.3) 88%,rgba(245,250,255,.6) 100%)';document.body.appendChild(d);NVE.div=d}
function nieveActiva(){return (typeof REP!=='undefined'&&REP.on)||(typeof NAV!=='undefined'&&NAV.on)}
function nieveTick(dt){const on=nieveActiva();
 if(on&&!NVE.on){NVE.t=0;NVE.k=0;NVE.obj=1;NVE.cambio=35+Math.random()*25;if(!NVE.pts)nveCopos();if(!NVE.div)nveEscarcha()}   // al empezar, nieva
 NVE.on=on;
 if(!on){if(NVE.pts)NVE.pts.visible=false;if(NVE.div)NVE.div.style.opacity=0;return}
 NVE.t+=dt;
 // a ratos: nevada (35-60 s) y pausa sin nieve (30-55 s); entra y se va poco a poco
 NVE.cambio-=dt;if(NVE.cambio<=0){NVE.obj=NVE.obj?0:.6+Math.random()*.4;NVE.cambio=NVE.obj?35+Math.random()*25:30+Math.random()*25}
 NVE.k+=(NVE.obj-NVE.k)*Math.min(1,dt/6);
 // viento a rachas
 NVE.racha-=dt;if(NVE.racha<=0){NVE.racha=3+Math.random()*5;NVE.vw=new THREE.Vector2((Math.random()-.5)*.16,(Math.random()-.5)*.16)}
 if(NVE.vw){NVE.wd.lerp(NVE.vw,Math.min(1,dt*.5))}NVE.uWd.value.addScaledVector(NVE.wd,dt);
 NVE.uT.value+=dt;NVE.uK.value=NVE.k;
 const vis=NVE.k>.01&&driving&&!(MODO==='pie'&&typeof BUC!=='undefined'&&BUC.W);NVE.pts.visible=vis;
 if(vis){NVE.uC.value.copy(pcam.position);NVE.uSc.value=R.domElement.height/(2*Math.tan(pcam.fov*Math.PI/360))}
 NVE.div.style.opacity=(vis?.5*NVE.k:0).toFixed(3)}
