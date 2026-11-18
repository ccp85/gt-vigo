import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------- circuito: hasta el final de Vialia por Vía Norte, la calle del Príncipe y la vuelta al árbol de Porta do Sol ----------
r("const repEnZona=(x,y)=>x>87.3&&x<104.6&&y>14.6&&y<24.6;","const repEnZona=(x,y)=>x>86.6&&x<109.6&&y>14.6&&y<24.6;")
r("const res=.025,x0=87.8,y0=14.4,w=Math.ceil((105-x0)/res)","const res=.025,x0=86.4,y0=14.4,w=Math.ceil((110-x0)/res)")
r("if(x>104.6||y>24.6)continue;const t=cell(x,y).t;if(t!==2&&t!==4)continue;if(redZona(x,y)||cerca(x,y))m[j*w+i]=2}",
  "if(x>109.6||y>24.6)continue;const t=cell(x,y).t,dA=Math.hypot(x-87.45,y-18);if(dA<.29)continue;if(((t===2||t===4)&&(redZona(x,y)||cerca(x,y)))||(t!==3&&t!==0&&t!==-1&&(cercaP(x,y)||dA<.78)))m[j*w+i]=2}")
r("const cerca=(x,y)=>{","const sgP=[];if(CALLES)for(const[n,c,ls]of CALLES)if(n==='Rúa do Príncipe')for(const l of ls)for(let i=0;i+3<l.length;i+=2)sgP.push([l[i],l[i+1],l[i+2],l[i+3]]);\n const cercaP=(x,y)=>{for(const[ax,ay,bx,by]of sgP){const vx=bx-ax,vy=by-ay,L2=vx*vx+vy*vy||1e-9;let t=((x-ax)*vx+(y-ay)*vy)/L2;t=Math.max(0,Math.min(1,t));if(Math.hypot(ax+vx*t-x,ay+vy*t-y)<.085)return true}return false};\n const cerca=(x,y)=>{")
r("for(const[n,c,ls]of CALLES){if(c===4||","for(const[n,c,ls]of CALLES){if((c===4&&n!=='Rúa do Príncipe')||")
r("if(repEnZona(x,y)&&esCalzada(x,y)&&repLibre(x,y)&&","if(repEnZona(x,y)&&(esCalzada(x,y)||n==='Rúa do Príncipe')&&repLibre(x,y)&&")
i=s.index("function navMundo(");j=s.index("function repMarca(")
pre,seg,post=s[:i],s[i:j],s[j:]
def rs(a,b):
    global seg
    assert seg.count(a)==1,(seg.count(a),a[:80]); seg=seg.replace(a,b)
# gente de Príncipe a los lados (el centro queda libre para la carroza)
rs("for(let s=0;s<L;s+=.022)for(let q=0;q<3;q++){const lat=(Math.random()*2-1)*.085,","for(let s=0;s<L;s+=.022)for(let q=0;q<3;q++){const lat=(Math.random()<.5?-1:1)*(.095+Math.random()*.05),")
# noria gigante y mercadillo en el parking del final de Vialia (Vía Norte)
rs("{const nx=100.8,ny=18.95,","{const nx=109.2,ny=20.45,")
rs("{const NX=100.8,NY=18.95,X0=98.6,X1=103.6,Y0=17.6,Y1=22.8,pu=[];","{const NX=109.2,NY=20.45,X0=107.3,X1=110.6,Y0=18.1,Y1=21.6,pu=[];")
# árbol de Porta do Sol gigante (más alto que los edificios) con LEDs que cambian de color
rs("{const ax=87.45,ay=18.0,z0=groundMap(ax,ay),H=.8,RB=.1;","{const ax=87.45,ay=18.0,z0=groundMap(ax,ay),H=2.2,RB=.25;")
rs("for(let k=0;k<700;k++){const t=k/700,h=t*H,r=RB*(1-t)+.002,a=t*60+(k%3)*2.094;const banda=Math.floor(t*14)%2;luz(ax+Math.cos(a)*r,z0+.018+h,ay+Math.sin(a)*r,banda?0xffffff:(k%5===0?0xff4fb0:0xffd98a),t*40,3+(k%4),.012)}",
   "{const TP=[],TA=[],TH=[];const pt_=(x,y,z,ph,sz,hu)=>{TP.push(x,y,z);TA.push(ph,2+Math.random()*3,sz);TH.push(hu)};for(let s_=0;s_<5;s_++)for(let k=0;k<520;k++){const t=k/520,r=RB*(1-t)+.006,a=t*34+s_*1.2566;pt_(ax+Math.cos(a)*r,z0+.02+t*H,ay+Math.sin(a)*r,k*.3,.03,t*.9+s_*.2)}\n   for(let k=0;k<1400;k++){const t=Math.pow(Math.random(),.75),a=Math.random()*6.283,r=(RB*(1-t))*1.01+.004;pt_(ax+Math.cos(a)*r,z0+.02+t*H,ay+Math.sin(a)*r,Math.random()*6.28,.024,Math.random())}\n   const ge=new THREE.BufferGeometry();ge.setAttribute('position',new THREE.Float32BufferAttribute(TP,3));ge.setAttribute('aP',new THREE.Float32BufferAttribute(TA,3));ge.setAttribute('aH',new THREE.Float32BufferAttribute(TH,1));const ptA=new THREE.Points(ge,arbolMat());ptA.frustumCulled=false;ptA.renderOrder=5;pon(ptA)}")
rs("for(let k=0;k<10;k++){const a=k/10*6.283,r=k%2?.018:.045;luz(ax+Math.cos(a)*r,z0+H+.05+Math.sin(a)*r,ay,0xfff2b0,k,2,.028)}","for(let k=0;k<10;k++){const a=k/10*6.283,r=k%2?.05:.13;for(let q=0;q<5;q++){const f=q/5;luz(ax+Math.cos(a)*r*(1-f)+Math.cos(a+.6)*r*f*.4,z0+H+.12+Math.sin(a)*r*(1-f)+Math.sin(a+.6)*r*f*.4,ay,0xfff2b0,k,2,.05)}}")
rs("halo(ax,z0+H+.05,ay,0xfff2b0,.55);","halo(ax,z0+H+.12,ay,0xfff2b0,1.6);halo(ax,z0+H*.5,ay,0xff9ad0,1.4);")
s=pre+seg+post
r("function haloMat(){","""function arbolMat(){return new THREE.ShaderMaterial({uniforms:{uT:NAV.uT,uSc:NAV.uSc},transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
 vertexShader:`#include <common>
#include <logdepthbuf_pars_vertex>
attribute vec3 aP;attribute float aH;uniform float uT,uSc;varying vec3 vC;
vec3 hsv(float h){vec3 p=abs(fract(h+vec3(0.,.6667,.3333))*6.-3.);return clamp(p-1.,0.,1.);}
void main(){vec4 mv=modelViewMatrix*vec4(position,1.);gl_Position=projectionMatrix*mv;float d=-mv.z;vC=mix(vec3(1.),hsv(fract(aH-uT*.12)),.85)*(.55+.45*sin(uT*aP.y+aP.x));gl_PointSize=clamp(aP.z*uSc/d,1.8,16.);
#include <logdepthbuf_vertex>
}`,
 fragmentShader:`#include <logdepthbuf_pars_fragment>
varying vec3 vC;void main(){
#include <logdepthbuf_fragment>
float r=length(gl_PointCoord-.5)*2.;float a=smoothstep(1.,.1,r);gl_FragColor=vec4(vC*a*1.7,a);}`})}
function haloMat(){""")
# ---------- se ve mejor: luz de anochecer clara (no oscuro), sin suelo mojado; menos confeti y menos cosas en la calle ----------
r("function navQuitar(){","""function repLuz(){SKYU.uZen.value.setRGB(.16,.2,.48);SKYU.uHor.value.setRGB(.95,.6,.7);SKYU.uNight.value=.35;SKYU.uDusk.value=.8;FOG.color.setRGB(.52,.44,.66);NUBE_MAT.color.setRGB(.8,.7,.95);
 hemi.color.setRGB(.95,.92,1.1);hemi.groundColor.setRGB(.6,.5,.6);hemi.intensity=1.5;sun.color.setRGB(1,.85,.75);sun.intensity=.75;if(sun.castShadow)sun.castShadow=false;R.toneMappingExposure=1.3;UMO.uWet.value=0;TIEMPO.moj=0}
function navQuitar(){""")
r("if(!REP.heli&&!REP.fin&&REP.red){repArcadeTick(dt);","if(!REP.heli&&REP.red)repLuz();\n if(!REP.heli&&!REP.fin&&REP.red){repArcadeTick(dt);")
r("REP.mul=Math.min(5,REP.mul+1);REP.ct=REP.cmb;REP.shake=.5;try{confeti()}catch(e){}repHud();return true}","REP.mul=Math.min(5,REP.mul+1);REP.ct=REP.cmb;REP.shake=.5;if(n>=5)try{confeti()}catch(e){}repHud();return true}")
r("const C=[];for(let k=0;k<90&&pool.length;k++){","const C=[];for(let k=0;k<55&&pool.length;k++){")
r("O.length<14;k++){","O.length<8;k++){")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok vialia')
