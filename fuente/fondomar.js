// ---------- el mundo bajo el agua: fondo atlántico de la Ría de Vigo (fondomar.js, lo mete edit_fondomar.py)
// arena con ripples y restos de conchas, fango en lo hondo, bolos de granito con coralina rosa y algas, bosques de laminarias,
// praderas de zostera, batea de mejillones, vieiras, erizos, estrellas de mar y anémonas; bancos de sardinas, sargos y maragotas;
// cáusticas del sol en todo el fondo, absorción del color con la distancia (el rojo se pierde antes), rayos de luz,
// ventana de Snell en la superficie vista desde abajo y nieve marina alrededor de la cámara
const FM_GLSL=`
float h21(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float vn2(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h21(i),h21(i+vec2(1,0)),f.x),mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),f.x),f.y);}
float h31(vec3 p){return fract(sin(dot(p,vec3(127.1,311.7,74.7)))*43758.5453);}
float vn3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
 return mix(mix(mix(h31(i),h31(i+vec3(1,0,0)),f.x),mix(h31(i+vec3(0,1,0)),h31(i+vec3(1,1,0)),f.x),f.y),
            mix(mix(h31(i+vec3(0,0,1)),h31(i+vec3(1,0,1)),f.x),mix(h31(i+vec3(0,1,1)),h31(i+vec3(1,1,1)),f.x),f.y),f.z);}
float caus(vec2 uv,float t){vec2 p=mod(uv*6.2832,6.2832)-250.;vec2 i=p;float c=1.,inten=.005;
 for(int n=0;n<4;n++){float tt=t*(1.-(3.5/float(n+1)));i=p+vec2(cos(tt-i.x)+sin(tt+i.y),sin(tt-i.y)+cos(tt+i.x));
  c+=1./length(vec2(p.x/(sin(i.x+tt)/inten),p.y/(cos(i.y+tt)/inten)));}
 c/=4.;c=1.17-pow(c,1.4);return clamp(pow(abs(c),8.),0.,2.5);}
`;
function fmMat(B,kind,op){const m=new THREE.MeshStandardMaterial(Object.assign({roughness:.95,metalness:0},op||{}));
 m.onBeforeCompile=sh=>{Object.assign(sh.uniforms,B.FU,m.userData.U||{});const PU=kind==='pulpo';
  const sway=kind==='alga'?`{vec3 ip=vec3(0.);
#ifdef USE_INSTANCING
   ip=instanceMatrix[3].xyz;
#endif
   float hh=max(position.y,0.),s=hh*hh,ph=uT*1.05+ip.x*37.+ip.z*23.;
   transformed.x+=(sin(ph+hh*2.2)*.3+.22)*s*.35;transformed.z+=cos(ph*.8+hh*3.1)*.22*s*.35;
   transformed.x+=sin(uT*4.+hh*9.+ip.z*50.)*.012*s;}`:
   kind==='pez'?`{vec3 ip=vec3(0.);
#ifdef USE_INSTANCING
   ip=instanceMatrix[3].xyz;
#endif
   float ph=uT*13.+ip.x*53.+ip.z*31.+ip.y*17.;transformed.z+=sin(ph+position.x*2.6)*.2*smoothstep(.4,-1.5,position.x);}`:
   PU?`{float sw=uSw;vec3 o=vec3(modelMatrix[3]);float ph=o.x*370.+o.z*230.;vK=aK;vAT=aT;vU=aU;vO=o;vLP=position;
   if(aK>.5&&aK<1.5){float an=aA*.785398+.39;vec3 off=position-aC;vec3 b=vec3(cos(an)*.35,.3,sin(an)*.35);vec3 rr=aC-b;
    float w=sin(uT*.9+aA*1.7+ph)*.4*aT;float cw=cos(w),sw2=sin(w);rr=vec3(rr.x*cw-rr.z*sw2,rr.y,rr.x*sw2+rr.z*cw);
    float lift=(sin(uT*1.4+aA*2.3-aT*5.+ph)*.5+.5)*aT*aT*.8;vec3 cr=b+rr+vec3(0.,lift,0.);
    vec3 ct=vec3(.2+aT*2.8,.8+sin(an)*.25*(1.-aT*.6)+sin(uT*9.-aT*7.+aA)*.12*aT,cos(an)*.25*(1.-aT*.6)+cos(uT*8.-aT*6.+aA)*.1*aT);
    transformed=mix(cr,ct,sw)+off*(1.-.3*sw);}
   else if(aK<.5){vec3 mc=vec3(-.55,1.,0.);float pu=1.+sin(uT*(1.6+sw*11.))*(.03+.13*sw)*smoothstep(-.1,-.6,position.x);transformed=mc+(position-mc)*pu;}}`:'';
  sh.vertexShader='uniform float uT;uniform vec3 uO;varying vec3 vWB;varying vec3 vNB;varying float vLY;varying float vLX;\n'+(PU?'uniform float uSw;attribute float aK,aT,aA,aU;attribute vec3 aC;varying float vK,vAT,vU;varying vec3 vO;varying vec3 vLP;\n':'')+sh.vertexShader
   .replace('#include <begin_vertex>','#include <begin_vertex>\n'+sway)
   .replace('#include <project_vertex>',`#include <project_vertex>
   {vec4 wq=vec4(transformed,1.);
#ifdef USE_INSTANCING
   wq=instanceMatrix*wq;
#endif
   wq=modelMatrix*wq;vWB=wq.xyz-uO;vec3 nq=objectNormal;
#ifdef USE_INSTANCING
   nq=mat3(instanceMatrix)*nq;
#endif
   vNB=normalize(mat3(modelMatrix)*nq);vLY=position.y;vLX=position.x;}`);
  let col='',nor='',ext='';
  if(kind==='arena'){
   col=`vec3 fq=vWB;float fcz=uWY-fq.y;
    float fm1=vn2(fq.xz*9.),fm2=vn2(fq.xz*31.+7.),fm3=vn2(fq.xz*140.);
    vec3 fsand=mix(vec3(.30,.27,.20),vec3(.41,.37,.28),fm1);
    float fdeep=smoothstep(.15,.3,fcz);
    vec3 fcol=mix(fsand,vec3(.12,.12,.09),fdeep*(.55+.45*fm2));
    vec2 fdir=normalize(vec2(.8,.6)+(vec2(vn2(fq.xz*4.),vn2(fq.xz*4.+9.))-.5)*.9);
    float fph=dot(fq.xz,fdir)*260.+vn2(fq.xz*12.)*7.;
    float ffw=length(fwidth(fq.xz));float frip=(1.-fdeep*.75)*(1.-smoothstep(.0025,.008,ffw));
    fcol*=1.+.2*sin(fph)*frip;
    fcol=mix(fcol,vec3(.11,.10,.07),smoothstep(.5,.95,-sin(fph))*.35*frip);
    fcol=mix(fcol,vec3(.58,.55,.48),step(.985,h21(floor(fq.xz*900.)))*smoothstep(.45,.2,length(fract(fq.xz*900.)-.5))*(1.-smoothstep(.0008,.003,ffw))*.45);
    fcol=mix(fcol,vec3(.16,.15,.13),smoothstep(.62,.8,vn2(fq.xz*2.3+4.))*.35);
    diffuseColor.rgb=fcol*(.85+.3*fm3);`;
   nor=`{float fs=cos(fph)+.35*cos(2.*fph);vec2 fg=fdir*fs*.5*frip;
    float fe=.004,fn0=vn2(fq.xz*90.),fnx=vn2((fq.xz+vec2(fe,0.))*90.),fnz=vn2((fq.xz+vec2(0.,fe))*90.);fg+=vec2(fnx-fn0,fnz-fn0)/fe*.0011;
    vec3 fnW=normalize(vNB+vec3(-fg.x,0.,-fg.y)*max(vNB.y,.2));normal=normalize((viewMatrix*vec4(fnW,0.)).xyz);}`}
  else if(kind==='roca'){
   col=`vec3 fq=vWB;float fcz=uWY-fq.y;
    float fg1=vn3(fq*45.),fg2=vn3(fq*160.),fg3=vn3(fq*520.);
    vec3 fcol=mix(vec3(.23,.22,.21),vec3(.37,.34,.31),fg1);
    fcol=mix(fcol,vec3(.05,.05,.05),step(.76,fg3)*.85);
    fcol=mix(fcol,vec3(.55,.51,.47),step(.8,1.-fg3)*.5);
    float ftop=smoothstep(.1,.75,vNB.y),fc1=vn3(fq*22.+3.),fc2=vn3(fq*55.+9.);
    fcol=mix(fcol,vec3(.34,.12,.14)*(.75+.5*fg2),smoothstep(.48,.6,fc2)*(.35+.65*(1.-ftop))*.9);
    fcol=mix(fcol,mix(vec3(.06,.10,.03),vec3(.15,.11,.04),fc1)*(.65+.7*fg2),smoothstep(.32,.58,fc1)*ftop);
    fcol=mix(fcol,vec3(.62,.62,.57),step(.93,vn3(fq*900.))*(1.-smoothstep(.06,.15,fcz))*.85);
    diffuseColor.rgb=fcol;`;
   nor=`{vec3 fp=vWB*70.;float fe=.18,fn0=vn3(fp),fnx=vn3(fp+vec3(fe,0.,0.)),fny=vn3(fp+vec3(0.,fe,0.)),fnz=vn3(fp+vec3(0.,0.,fe));
    vec3 fg=vec3(fnx-fn0,fny-fn0,fnz-fn0)/fe*.55;vec3 fp2=vWB*330.;float fm0=vn3(fp2);fg+=vec3(vn3(fp2+vec3(fe,0.,0.))-fm0,vn3(fp2+vec3(0.,fe,0.))-fm0,vn3(fp2+vec3(0.,0.,fe))-fm0)/fe*.18;
    vec3 fnW=normalize(vNB-(fg-dot(fg,vNB)*vNB));normal=normalize((viewMatrix*vec4(fnW,0.)).xyz);if(!gl_FrontFacing)normal=-normal;}`}
  else if(kind==='alga'){
   col=`float fcz=uWY-vWB.y;diffuseColor.rgb*=mix(.75,1.25,smoothstep(0.,1.,vLY))*(.85+.3*vn2(vWB.xz*300.+vLY*20.));`;
   ext=`outgoingLight+=diffuseColor.rgb*.55*(1.-uNf)*exp(-fcz*4.)*(.6+.4*vLY);`}
  else if(kind==='pez'){
   col=`{float fb=smoothstep(-.04,.16,vLY);vec3 fback=diffuseColor.rgb;vec3 fside=mix(vec3(.78,.8,.82),vec3(.55,.6,.64),smoothstep(-.22,.02,vLY));
    diffuseColor.rgb=mix(fside,fback,fb);diffuseColor.rgb*=1.-.35*smoothstep(-1.,-1.4,vLX);}`;
   ext=`{float fr=pow(1.-abs(dot(normal,normalize(vViewPosition))),2.5);float fb2=1.-smoothstep(-.04,.16,vLY);
    outgoingLight+=vec3(.55,.72,.78)*(fr*.35+.25*pow(max(0.,sin(uT*2.+vWB.x*90.+vWB.z*70.)),12.))*fb2*(1.-uNf*.7);}`}
  else if(PU){
   col=`{vec3 fq=vLP*7.+vO*500.;float fmo=vn3(fq*.45)*.6+vn3(fq*1.3)*.4;
    vec3 fcol=mix(vec3(.30,.10,.055),vec3(.52,.28,.17),smoothstep(.3,.75,fmo));
    fcol*=1.-.3*smoothstep(.7,.8,vn3(fq*3.2));fcol=mix(fcol,vec3(.7,.56,.45),smoothstep(.8,.9,vn3(fq*4.5+7.))*.4);
    float fcam=.5+.5*sin(uT*.35+vO.x*300.+vO.z*170.);fcol=mix(fcol,mix(vec3(.36,.31,.22),vec3(.28,.25,.2),fmo),fcam*.38);
    float fsk=smoothstep(.35,.7,vU)*step(.5,fract(vAT*34.))*step(.5,vK)*step(vK,1.5);fcol=mix(fcol,vec3(.7,.55,.48),fsk*.8);
    if(vK>1.5){fcol=vec3(.62,.52,.28);if(vK>2.5)fcol=vec3(.02);}
    diffuseColor.rgb=fcol;}`}
  sh.fragmentShader='uniform float uT,uWY,uNf;uniform vec3 uSun,uO;varying vec3 vWB;varying vec3 vNB;varying float vLY;varying float vLX;\n'+(PU?'varying float vK,vAT,vU;varying vec3 vO;varying vec3 vLP;\n':'')+FM_GLSL+sh.fragmentShader
   .replace('#include <color_fragment>','#include <color_fragment>\n'+col)
   .replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+nor)
   .replace('#include <opaque_fragment>',`{float fcz2=max(uWY-vWB.y,0.);
    float fcf=exp(-fcz2*2.6)*smoothstep(-.35,.75,normalize(vNB).y)*(1.-uNf*.92);
    vec2 fcp=(vWB.xz+uSun.xz/max(uSun.y,.25)*fcz2*.6)/.085;
    float fca=caus(fcp,uT*.55+11.)*.7+caus(fcp*1.31+.37,uT*.47+3.)*.45;
    outgoingLight+=diffuseColor.rgb*fca*vec3(.85,1.,.95)*7.*fcf;
    ${ext}
    float fdd=length(vWB-(cameraPosition-uO));
    outgoingLight*=exp(-vec3(2.6,.62,.5)*(fdd*1.05+fcz2*1.5))*.8;}
   #include <opaque_fragment>`)};
 m.customProgramCacheKey=()=>'fm_'+kind;return m}
// pulpo (Octopus vulgaris): manto, cabeza con ojos y 8 brazos en tubo con ventosas; atributos para animarlo en el shader
function pulpoGeo(LT){const P=[],K=[],T=[],A=[],U=[],C=[],I=[];
 const parte=(g,k)=>{const b=P.length/3,p=g.attributes.position;for(let q=0;q<p.count;q++){P.push(p.getX(q),p.getY(q),p.getZ(q));C.push(p.getX(q),p.getY(q),p.getZ(q));K.push(k);T.push(0);A.push(0);U.push(0)}const ix=g.index.array;for(let q=0;q<ix.length;q++)I.push(ix[q]+b)};
 const ma=new THREE.SphereGeometry(1,LT?14:22,LT?10:16);ma.scale(.95,.6,.6);ma.rotateZ(-.65);ma.translate(-.62,1.05,0);parte(ma,0);
 const he=new THREE.SphereGeometry(.5,LT?12:18,LT?8:12);he.scale(1,.8,1.05);he.translate(.02,.52,0);parte(he,0);
 for(const s of[-1,1]){const e=new THREE.SphereGeometry(.13,10,8);e.translate(.18,.78,s*.36);parte(e,2);const pu=new THREE.SphereGeometry(.06,8,6);pu.scale(.6,1.2,1);pu.translate(.27,.8,s*.44);parte(pu,3)}
 const S=LT?18:30,RS=LT?5:7;
 for(let a=0;a<8;a++){const an=a*.785398+.39,d=[Math.cos(an),0,Math.sin(an)],sd=[-d[2],0,d[0]],L=2.3+.5*Math.abs(Math.sin(a*12.9)),cu=(a%2?1:-1),cl=[];
  for(let i=0;i<=S;i++){const t=i/S;let x=Math.cos(an)*.35+d[0]*t*L,z=Math.sin(an)*.35+d[2]*t*L,y=.3*(1-t)*(1-t)+.1;
   if(t>.6){const ph=(t-.6)/.4*3.4,k=Math.sin(ph)*.32*(t-.6)/.4;x+=sd[0]*cu*k-d[0]*(1-Math.cos(ph))*.15;z+=sd[2]*cu*k-d[2]*(1-Math.cos(ph))*.15;y+=(1-Math.cos(ph))*.08}cl.push([x,y,z])}
  const b=P.length/3;for(let i=0;i<=S;i++){const t=i/S,c=cl[i],n=cl[Math.min(S,i+1)],p=cl[Math.max(0,i-1)];const tg=new THREE.Vector3(n[0]-p[0],n[1]-p[1],n[2]-p[2]).normalize();
   const up=new THREE.Vector3(0,1,0),bn=new THREE.Vector3().crossVectors(tg,up).normalize(),nn=new THREE.Vector3().crossVectors(bn,tg).normalize(),rr=.16*Math.pow(1-t,.9)+.012;
   for(let k=0;k<RS;k++){const g=k/RS*6.2832,o=nn.clone().multiplyScalar(Math.cos(g)*rr).addScaledVector(bn,Math.sin(g)*rr);
    P.push(c[0]+o.x,c[1]+o.y,c[2]+o.z);C.push(c[0],c[1],c[2]);K.push(1);T.push(t);A.push(a);U.push(Math.max(0,-Math.cos(g)))}}
  for(let i=0;i<S;i++)for(let k=0;k<RS;k++){const q=b+i*RS+k,q2=b+i*RS+(k+1)%RS;I.push(q,q2,q+RS,q2,q2+RS,q+RS)}}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(P,3));g.setAttribute('aC',new THREE.Float32BufferAttribute(C,3));
 for(const[n,v]of[['aK',K],['aT',T],['aA',A],['aU',U]])g.setAttribute(n,new THREE.Float32BufferAttribute(v,1));g.setIndex(I);g.computeVertexNormals();return g}
function burbujaTex(){if(burbujaTex.t)return burbujaTex.t;const c=document.createElement('canvas');c.width=c.height=32;const x=c.getContext('2d'),g=x.createRadialGradient(16,16,1,16,16,15);g.addColorStop(0,'rgba(255,255,255,.15)');g.addColorStop(.65,'rgba(255,255,255,.3)');g.addColorStop(.85,'rgba(255,255,255,1)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(0,0,32,32);return burbujaTex.t=new THREE.CanvasTexture(c)}
// ruido determinista en JS (mismo resultado en cada sitio, para que los cuadrados del fondo encajen y no cambien al volver)
const FMN=(()=>{const hs=(x,y)=>{const s=Math.sin(x*127.1+y*311.7)*43758.5453;return s-Math.floor(s)};
 const vn=(x,y)=>{const i=Math.floor(x),j=Math.floor(y),u=x-i,v=y-j,a=hs(i,j),b=hs(i+1,j),c=hs(i,j+1),d=hs(i+1,j+1),uu=u*u*(3-2*u),vv=v*v*(3-2*v);return a+(b-a)*uu+(c-a)*vv+(a-b-c+d)*uu*vv};
 const fbm=(x,y,o=4)=>{let s=0,a=.5,f=1,n=0;for(let k=0;k<o;k++){s+=a*vn(x*f+k*13.1,y*f-k*7.7);n+=a;f*=2.03;a*=.5}return s/n};
 const h3=(x,y,z)=>{const s=Math.sin(x*127.1+y*311.7+z*74.7)*43758.5453;return s-Math.floor(s)};
 const vn3=(x,y,z)=>{const i=Math.floor(x),j=Math.floor(y),k=Math.floor(z);let u=x-i,v=y-j,w=z-k;u=u*u*(3-2*u);v=v*v*(3-2*v);w=w*w*(3-2*w);const L=(a,b,t)=>a+(b-a)*t;
  return L(L(L(h3(i,j,k),h3(i+1,j,k),u),L(h3(i,j+1,k),h3(i+1,j+1,k),u),v),L(L(h3(i,j,k+1),h3(i+1,j,k+1),u),L(h3(i,j+1,k+1),h3(i+1,j+1,k+1),u),v),w)};
 const ss=(x,a,b)=>{const t=Math.min(1,Math.max(0,(x-a)/(b-a)));return t*t*(3-2*t)};
 return{hs,vn,fbm,vn3,ss}})();
// profundidad del mar según la distancia a la costa (1 unidad ≈ 100 m): baja rápido junto a la orilla y se estabiliza mar adentro (≈45-50 m),
// con canales y bajos suaves. Se calcula una vez para todo el mapa con un chamfer sobre la cuadrícula tierra/agua.
function fmProfBase(d,x,y){if(d<=0)return -.02;const b=.025+.46*(1-Math.exp(-d/1.4));const v=(FMN.fbm(x*.35+3.1,y*.35-7.3,3)-.5)*.7*FMN.ss(d,.1,.9);return Math.max(.02,b*(1+v))}
function fmProfundidad(B){if(B.PF)return B.PF;
 if(typeof MAPA!=='undefined'&&MAPA&&typeof MI!=='undefined'&&MI){const k=4,w=Math.floor(MAPA.w/k),h=Math.floor(MAPA.h/k),cs=k/MAPA.res,D=new Float32Array(w*h);
  for(let j=0;j<h;j++)for(let i=0;i<w;i++)D[j*w+i]=Math.round(MI[((j*k)*MAPA.w+i*k)*4]/40)===0?1e4:0;
  for(let j=0;j<h;j++)for(let i=0;i<w;i++){const n=j*w+i;if(i>0)D[n]=Math.min(D[n],D[n-1]+1);if(j>0)D[n]=Math.min(D[n],D[n-w]+1);if(i>0&&j>0)D[n]=Math.min(D[n],D[n-w-1]+1.41);if(i<w-1&&j>0)D[n]=Math.min(D[n],D[n-w+1]+1.41)}
  for(let j=h-1;j>=0;j--)for(let i=w-1;i>=0;i--){const n=j*w+i;if(i<w-1)D[n]=Math.min(D[n],D[n+1]+1);if(j<h-1)D[n]=Math.min(D[n],D[n+w]+1);if(i<w-1&&j<h-1)D[n]=Math.min(D[n],D[n+w+1]+1.41);if(i>0&&j<h-1)D[n]=Math.min(D[n],D[n+w-1]+1.41)}
  let Pd=new Float32Array(w*h);for(let n=0;n<w*h;n++){const i=n%w,j=(n-i)/w;Pd[n]=fmProfBase(Math.min(D[n],1e3)*cs,MAPA.ox+i*cs,MAPA.oy+j*cs)}
  // suavizado (dos pasadas de caja) para que los taludes no tengan escalones
  for(let p=0;p<2;p++){const T=new Float32Array(w*h);for(let j=0;j<h;j++)for(let i=0;i<w;i++){let s=0,c=0;for(let d=-2;d<=2;d++){const ii=i+d;if(ii>=0&&ii<w){s+=Pd[j*w+ii];c++}}T[j*w+i]=s/c}
   for(let j=0;j<h;j++)for(let i=0;i<w;i++){let s=0,c=0;for(let d=-2;d<=2;d++){const jj=j+d;if(jj>=0&&jj<h){s+=T[jj*w+i];c++}}Pd[j*w+i]=s/c}}
  B.PF={w,h,cs,ox:MAPA.ox,oy:MAPA.oy,P:Pd}}
 else B.PF={fn:true};return B.PF}
function fmProfAt(B,x,y){const F=fmProfundidad(B);
 if(F.fn){let d=3;for(let r_=.03;r_<=3&&d===3;r_+=.04)for(let q=0;q<12;q++){const a=q*.5236;if(cell(x+Math.cos(a)*r_,y+Math.sin(a)*r_).t!==0){d=r_;break}}return cell(x,y).t!==0?-.02:fmProfBase(d,x,y)}
 const fi=(x-F.ox)/F.cs,fj=(y-F.oy)/F.cs;if(fi<0||fj<0||fi>=F.w-1||fj>=F.h-1)return .48;const i=Math.floor(fi),j=Math.floor(fj),u=fi-i,v=fj-j,P_=F.P,w=F.w;
 return P_[j*w+i]*(1-u)*(1-v)+P_[j*w+i+1]*u*(1-v)+P_[(j+1)*w+i]*(1-u)*v+P_[(j+1)*w+i+1]*u*v}
// normales suaves en una malla sin índices (las rocas no se ven facetadas): se promedian las de los vértices que coinciden
function fmSuaviza(ge){const p=ge.attributes.position,n=ge.attributes.normal,M=new Map(),k=i=>Math.round(p.getX(i)*1e4)+'_'+Math.round(p.getY(i)*1e4)+'_'+Math.round(p.getZ(i)*1e4);
 for(let i=0;i<p.count;i++){const q=k(i);let a=M.get(q);if(!a)M.set(q,a=[0,0,0]);a[0]+=n.getX(i);a[1]+=n.getY(i);a[2]+=n.getZ(i)}
 for(let i=0;i<p.count;i++){const a=M.get(k(i)),l=Math.hypot(a[0],a[1],a[2])||1;n.setXYZ(i,a[0]/l,a[1]/l,a[2]/l)}}
function buceoMundo(D,WY){const B=BUC,G=new THREE.Group();G.name='fondoMar';B.uT=B.uT||{value:0};const LT=!!window.LITE,RZ=1.35,TS=.6;B.LT=LT;B.TS=TS;
 B.FU={uT:B.uT,uWY:{value:WY},uNf:SKYU.uNight,uSun:SKYU.uSun,uO:{value:new THREE.Vector3(Math.round(D[0]/10)*10,0,Math.round(D[1]/10)*10)}};
 const{fbm,vn3,ss}=FMN;let sd=7;const rn=()=>(sd=(sd*16807)%2147483647)/2147483647;
 const roc=(x,y)=>ss(fbm(x*2.6+11,y*2.6-4,3),.56,.74);B.roc=roc;
 // fondo continuo: profundidad según la costa + dunas + lomos de roca que afloran
 B.hB=(x,y)=>{const pr=fmProfAt(B,x,y);if(pr<=0)return WY+.01;const k=Math.min(1,pr/.45);
  const dun=(fbm(x*5,y*5)-.5)*.045+Math.sin((x*.8+y*.6)*38+fbm(x*3,y*3)*5)*.004,rr=roc(x,y)*(fbm(x*14,y*14,3)*.07+.02)*(.5+.5*k);
  return Math.min(WY-.012,WY-pr+dun*(.4+.6*k)+rr)};
 // ---- geometrías y materiales que comparten todos los cuadrados
 const K={};B.K=K;
 K.arena=fmMat(B,'arena');K.roca=fmMat(B,'roca',{roughness:.92});K.alga2=fmMat(B,'alga',{color:0xffffff,roughness:.7,side:THREE.DoubleSide});K.anem=fmMat(B,'alga',{color:0xffffff,roughness:.5});
 K.viei=fmMat(B,'vida',{color:0xffffff,roughness:.7,side:THREE.DoubleSide});K.vida=fmMat(B,'vida',{color:0xffffff,roughness:.85});K.eriz=fmMat(B,'vida',{color:0xffffff,roughness:.55});
 K.mej=fmMat(B,'vida',{color:0xffffff,roughness:.45,metalness:.1});K.mad=fmMat(B,'vida',{color:0x3b2b1d,roughness:.85});K.flo=fmMat(B,'vida',{color:0x6b7176,roughness:.85});K.cu=fmMat(B,'vida',{color:0x2d2a1e,roughness:.85});
 K.RG=[];for(let g=0;g<(LT?6:10);g++){const ge=new THREE.IcosahedronGeometry(1,LT?2:3),pa=ge.attributes.position,sx=g*3.7;
  for(let q=0;q<pa.count;q++){const x=pa.getX(q),y=pa.getY(q),z=pa.getZ(q);let f=.78+.45*vn3(x*1.3+sx,y*1.3,z*1.3)+.14*vn3(x*3.2,y*3.2+sx,z*3.2)+.05*vn3(x*7,y*7,z*7+sx);
   const ny=y*f;pa.setXYZ(q,x*f,ny<-.25?-.25+(ny+.25)*.3:ny,z*f)}ge.deleteAttribute('uv');ge.computeVertexNormals();fmSuaviza(ge);K.RG.push(ge)}
 K.canto=new THREE.IcosahedronGeometry(1,1);
 {const SEG=14,pos=[],idx=[];for(let i=0;i<=SEG;i++){const t=i/SEG,y=t,w=t<.22?.012:.075*Math.sin(Math.PI*Math.min(1,(t-.12)/.88))**.7+.01,ru=t<.22?0:Math.sin(t*31)*.02*t;
   pos.push(-w/2,y,ru,0,y,0,w/2,y,-ru);if(i<SEG){const a=i*3;idx.push(a,a+3,a+1,a+1,a+3,a+4,a+1,a+4,a+2,a+2,a+4,a+5)}}
  const kg=new THREE.BufferGeometry();kg.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));kg.setIndex(idx);kg.computeVertexNormals();
  const k2=kg.clone();k2.rotateY(1.2);k2.translate(.006,0,.004);const k3=kg.clone();k3.rotateY(-1.4);k3.translate(-.005,0,-.003);k2.scale(1,.85,1);k3.scale(1,.75,1);K.kelp=mergeGeometries([kg,k2,k3])}
 {const bg=new THREE.PlaneGeometry(.06,1,1,4);bg.translate(0,.5,0);const pa=bg.attributes.position;for(let q=0;q<pa.count;q++){const y=pa.getY(q);pa.setX(q,pa.getX(q)*(1-y*.6));pa.setZ(q,y*y*.08)}bg.computeVertexNormals();K.zost=bg}
 {const vg=new THREE.CircleGeometry(1,24,Math.PI*.18,Math.PI*.64);vg.rotateX(-Math.PI/2);const pa=vg.attributes.position;for(let q=0;q<pa.count;q++){const x=pa.getX(q),z=pa.getZ(q),a=Math.atan2(z,x),r=Math.hypot(x,z);pa.setY(q,(.18*(1-r*r)+.035*Math.abs(Math.sin(a*30)))*Math.min(1,r*4))}vg.computeVertexNormals();K.vieira=vg}
 {const sh=new THREE.Shape();for(let q=0;q<=60;q++){const a=q/60*6.283,r_=.32+.68*Math.pow(.5+.5*Math.cos(a*5),2.2);q?sh.lineTo(Math.cos(a)*r_,Math.sin(a)*r_):sh.moveTo(r_,0)}
  const eg=new THREE.ExtrudeGeometry(sh,{depth:.12,bevelEnabled:true,bevelThickness:.12,bevelSize:.1,bevelSegments:2,curveSegments:4});eg.rotateX(-Math.PI/2);K.estrella=eg}
 {const parts=[new THREE.SphereGeometry(1,12,8)];const sp=new THREE.ConeGeometry(.07,1.15,4);sp.translate(0,.57+.6,0);const NSp=LT?40:90;for(let q=0;q<NSp;q++){const s=sp.clone(),y=1-2*(q+.5)/NSp,a=q*2.3999;if(y<-.4)continue;const r=Math.sqrt(1-y*y);
   s.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),new THREE.Vector3(Math.cos(a)*r,y,Math.sin(a)*r)));parts.push(s)}
  const ug=mergeGeometries(parts.map(g=>g.index?g.toNonIndexed():g));ug.scale(1,.75,1);K.erizo=ug}
 {const parts=[new THREE.CylinderGeometry(.5,.6,.5,12)];parts[0].translate(0,.25,0);const tg=new THREE.ConeGeometry(.07,1,4,3);tg.translate(0,.5,0);
  for(let q=0;q<(LT?18:36);q++){const t=tg.clone(),a=q*2.3999,r=.15+.3*Math.sqrt((q+.5)/36);t.rotateZ(.25+r*1.2);t.rotateY(-a);t.translate(Math.cos(a)*r,.5,Math.sin(a)*r);parts.push(t)}
  K.anemona=mergeGeometries(parts.map(g=>g.index?g.toNonIndexed():g))}
 K.mejillon=new THREE.SphereGeometry(1,7,5);K.mejillon.scale(1,.42,.48);K.pulpo=pulpoGeo(LT);
 // ---- cuadrados del fondo (TS × TS), cargados alrededor del nadador
 const enAgua=(x,y)=>cell(x,y).t===0;
 function cuadro(ix,iy){let sd2=(((Math.abs(ix*73856093)^Math.abs(iy*19349663))>>>0)%2147483646)+1;const r=()=>(sd2=(sd2*16807)%2147483647)/2147483647;
  const g=new THREE.Group(),x0=ix*TS,y0=iy*TS,T={g,own:[],pulpos:[],ix,iy};
  let agua=0;for(let q=0;q<25;q++)if(enAgua(x0+(q%5+.5)*TS/5,y0+(Math.floor(q/5)+.5)*TS/5))agua++;
  if(!agua){T.vacio=true;return T}
  const prof=(x,y)=>WY-B.hB(x,y),sitio=f=>{for(let t=0;t<12;t++){const x=x0+r()*TS,y=y0+r()*TS;if(enAgua(x,y)&&prof(x,y)>.03&&(!f||f(x,y)))return[x,y]}return null};
  const own=ge=>{T.own.push(ge);return ge},inst=(ge,m,n)=>{const im=new THREE.InstancedMesh(ge,m,n);im.count=0;return im},du=new THREE.Object3D(),cc=new THREE.Color();
  // relieve: normales analíticas a partir de la altura (sin costuras entre cuadrados)
  {const N=LT?14:22,pg=new THREE.PlaneGeometry(TS,TS,N,N);pg.rotateX(-Math.PI/2);pg.translate(x0+TS/2,0,y0+TS/2);const pa=pg.attributes.position,no=pg.attributes.normal,e=.012;
   for(let q=0;q<pa.count;q++){const x=pa.getX(q),y=pa.getZ(q);pa.setY(q,B.hB(x,y));const nx=B.hB(x-e,y)-B.hB(x+e,y),nz=B.hB(x,y-e)-B.hB(x,y+e),l=Math.hypot(nx,2*e,nz);no.setXYZ(q,nx/l,2*e/l,nz/l)}
   pg.deleteAttribute('uv');const m=new THREE.Mesh(own(pg),K.arena);m.receiveShadow=true;g.add(m)}
  // bolos de granito (todos los del cuadrado en una sola malla)
  const ROC=[];{const L=[];for(let k=0;k<(LT?6:10);k++){const p=sitio((x,y)=>r()<.15+roc(x,y)*.9+(prof(x,y)<.12?.25:0));if(!p)continue;const s=.02+Math.pow(r(),2.2)*.11;
    du.position.set(p[0],B.hB(p[0],p[1])+s*.12,p[1]);du.rotation.set((r()-.5)*.4,r()*6.28,(r()-.5)*.4);du.scale.set(s*(.8+r()*.6),s*(.55+r()*.4),s*(.8+r()*.6));du.updateMatrix();
    L.push(K.RG[Math.floor(r()*K.RG.length)].clone().applyMatrix4(du.matrix));ROC.push({x:p[0],y:p[1],z:du.position.y+du.scale.y*.75,r:s})}
   if(L.length){const m=new THREE.Mesh(own(mergeGeometries(L)),K.roca);m.castShadow=m.receiveShadow=true;g.add(m);L.forEach(x=>x.dispose())}}
  {const n0=LT?10:26,im=inst(K.canto,K.roca,n0);for(let k=0;k<n0;k++){const rr=ROC.length&&r()<.6?ROC[Math.floor(r()*ROC.length)]:null;let x,y;if(rr){const a=r()*6.28,d=rr.r*(1+r()*2.5);x=rr.x+Math.cos(a)*d;y=rr.y+Math.sin(a)*d}else{const p=sitio();if(!p)continue;[x,y]=p}if(!enAgua(x,y))continue;
    const s=.003+Math.pow(r(),2)*.012;du.position.set(x,B.hB(x,y)+s*.2,y);du.rotation.set(r()*3,r()*3,r()*3);du.scale.set(s*(1+r()*.5),s*.6,s);du.updateMatrix();im.setMatrixAt(im.count++,du.matrix)}im.receiveShadow=true;if(im.count)g.add(im)}
  // laminarias sobre las rocas poco hondas
  {const base=ROC.filter(o=>WY-o.z>.06&&WY-o.z<.3),n0=LT?7:16,im=inst(K.kelp,K.alga2,n0);for(let c=0;c<n0*2&&im.count<n0&&base.length;c++){const o=base[Math.floor(r()*base.length)],a=r()*6.28,d=r()*o.r*.7,x=o.x+Math.cos(a)*d,y=o.y+Math.sin(a)*d,z=Math.max(B.hB(x,y),o.z-o.r*.3*r());
    const h=Math.min(WY-.03-z,.06+r()*.1);if(h<.03)continue;du.position.set(x,z,y);du.rotation.set((r()-.5)*.3,r()*6.28,(r()-.5)*.3);du.scale.setScalar(h);du.updateMatrix();const i=im.count++;im.setMatrixAt(i,du.matrix);im.setColorAt(i,cc.setRGB(.17+r()*.06,.13+r()*.04,.035+r()*.02))}
   im.castShadow=true;if(im.count)g.add(im)}
  // pradera de zostera en la arena poco honda
  {const n0=LT?70:180,im=inst(K.zost,K.alga2,n0);for(let c=0;c<2;c++){const p=sitio((x,y)=>prof(x,y)<.16&&roc(x,y)<.35);if(!p||r()<.35)continue;const R=.05+r()*.1;
    for(let q=0;q<n0/2&&im.count<n0;q++){const a=r()*6.28,d=Math.sqrt(r())*R,x=p[0]+Math.cos(a)*d,y=p[1]+Math.sin(a)*d;if(!enAgua(x,y)||r()>1-d/R*.7)continue;
     const h=.018+r()*.03;du.position.set(x,B.hB(x,y)-.001,y);du.rotation.set((r()-.5)*.3,r()*6.28,(r()-.5)*.3);du.scale.setScalar(h);du.updateMatrix();const i=im.count++;im.setMatrixAt(i,du.matrix);im.setColorAt(i,cc.setRGB(.06+r()*.05,.15+r()*.07,.04+r()*.03))}}if(im.count)g.add(im)}
  // vieiras, estrellas, erizos y anémonas
  {const im=inst(K.vieira,K.viei,3);for(let k=0;k<(LT?1:3);k++){const p=sitio((x,y)=>roc(x,y)<.3);if(!p)continue;du.position.set(p[0],B.hB(p[0],p[1])+.001,p[1]);du.rotation.set((r()-.5)*.3,r()*6.28,(r()-.5)*.3);du.scale.setScalar(.008+r()*.004);du.updateMatrix();const i=im.count++;im.setMatrixAt(i,du.matrix);im.setColorAt(i,cc.setRGB(.42+r()*.1,.3+r()*.06,.22))}if(im.count)g.add(im)}
  {const im=inst(K.estrella,K.vida,2);for(let k=0;k<(LT?1:2);k++){let x,y,z;const o=ROC.length&&r()<.6?ROC[Math.floor(r()*ROC.length)]:null;if(o){x=o.x+(r()-.5)*o.r;y=o.y+(r()-.5)*o.r;z=o.z-o.r*.15}else{const p=sitio();if(!p)continue;[x,y]=p;z=B.hB(x,y)}
    du.position.set(x,z+.002,y);du.rotation.set((r()-.5)*.5,r()*6.28,(r()-.5)*.5);du.scale.setScalar(.008+r()*.008);du.updateMatrix();const i=im.count++;im.setMatrixAt(i,du.matrix);im.setColorAt(i,cc.setRGB(.45+r()*.2,.16+r()*.08,.08+r()*.05))}if(im.count)g.add(im)}
  {const im=inst(K.erizo,K.eriz,4);for(let k=0;k<(LT?2:4)&&ROC.length;k++){const o=ROC[Math.floor(r()*ROC.length)],a=r()*6.28,d=o.r*(.5+r()*.6),x=o.x+Math.cos(a)*d,y=o.y+Math.sin(a)*d;if(!enAgua(x,y))continue;
    du.position.set(x,Math.max(B.hB(x,y),o.z-o.r*(.3+r()*.5))+.003,y);du.rotation.set((r()-.5)*.6,r()*6,(r()-.5)*.6);du.scale.setScalar(.004+r()*.003);du.updateMatrix();const i=im.count++;im.setMatrixAt(i,du.matrix);im.setColorAt(i,cc.setRGB(.12+r()*.05,.03,.12+r()*.06))}if(im.count)g.add(im)}
  {const im=inst(K.anemona,K.anem,3);for(let k=0;k<(LT?1:3)&&ROC.length;k++){const o=ROC[Math.floor(r()*ROC.length)];if(WY-o.z<.04)continue;du.position.set(o.x+(r()-.5)*o.r*.6,o.z-o.r*.1,o.y+(r()-.5)*o.r*.6);du.rotation.set((r()-.5)*.4,r()*6,(r()-.5)*.4);du.scale.setScalar(.008+r()*.008);du.updateMatrix();const i=im.count++;im.setMatrixAt(i,du.matrix);
    im.setColorAt(i,r()<.7?cc.setRGB(.16,.26,.08):cc.setRGB(.3,.08,.16))}if(im.count)g.add(im)}
  // pulpo junto a una roca (no en todos los cuadrados)
  if(ROC.length&&r()<(LT?.18:.3)){const o=ROC[Math.floor(r()*ROC.length)],a=r()*6.28,x=o.x+Math.cos(a)*(o.r+.02),y=o.y+Math.sin(a)*(o.r+.02);
   if(enAgua(x,y)){const U={uSw:{value:0}},mt=fmMat(B,'pulpo',{color:0xffffff,roughness:.55});mt.userData.U=U;T.own.push(mt);const m=new THREE.Mesh(K.pulpo,mt);m.scale.setScalar(.0085+r()*.003);m.castShadow=true;m.frustumCulled=false;
    const p={m,U,x,y,z:B.hB(x,y),a:r()*6.28,huye:0,sw:0,ph:r()*6};m.position.set(x,p.z,y);m.rotation.y=p.a;g.add(m);T.pulpos.push(p)}}
  // batea de mejilloneiro (algunos cuadrados de profundidad media)
  {const cx=x0+TS/2,cy=y0+TS/2,pc=prof(cx,cy);if(r()<(LT?.07:.1)&&pc>.15&&pc<.4){const W=.24,L=.2;let ok=true;for(const[ox,oy]of[[-.15,-.13],[.15,-.13],[-.15,.13],[.15,.13]])if(!enAgua(cx+ox,cy+oy)||prof(cx+ox,cy+oy)<.14)ok=false;
   if(ok){const bg=new THREE.Group(),ry=r()*3;bg.position.set(cx,0,cy);bg.rotation.y=ry;
    for(let i=0;i<=6;i++){const b=new THREE.Mesh(own(new THREE.BoxGeometry(W,.004,.004)),K.mad);b.position.set(0,WY+.004,-L/2+i*L/6);bg.add(b)}
    for(let i=0;i<=2;i++){const b=new THREE.Mesh(own(new THREE.BoxGeometry(.006,.006,L+.02)),K.mad);b.position.set(-W/2+i*W/2,WY+.008,0);bg.add(b)}
    const fg=own(new THREE.CylinderGeometry(.018,.018,.05,16));for(const[fx,fz]of[[-.08,-.06],[.08,-.06],[-.08,.06],[.08,.06]]){const c=new THREE.Mesh(fg,K.flo);c.rotation.x=Math.PI/2;c.position.set(fx,WY-.006,fz);bg.add(c)}
    const NX=LT?4:6,NZ=LT?5:8,PM=LT?45:80,im=new THREE.InstancedMesh(K.mejillon,K.mej,NX*NZ*PM);let n=0;const cuL=[];
    for(let i=0;i<NX;i++)for(let k=0;k<NZ;k++){const x=-W/2+.02+i*(W-.04)/(NX-1),z=-L/2+.015+k*(L-.03)/(NZ-1),wx=cx+x*Math.cos(ry)+z*Math.sin(ry),wz=cy-x*Math.sin(ry)+z*Math.cos(ry);
     const len=Math.min(.13,prof(wx,wz)-.035);const cg=new THREE.CylinderGeometry(.0012,.0012,len,5);cg.translate(x,WY-len/2,z);cuL.push(cg);
     for(let q=0;q<PM;q++){const yy=WY-.01-r()*(len-.012),a=r()*6.28,rr=.0035+r()*.002;du.position.set(x+Math.cos(a)*rr,yy,z+Math.sin(a)*rr);du.rotation.set(r()*.8-.4,-a,-1.1+r()*.6);
      du.scale.setScalar(.0035+r()*.0022);du.updateMatrix();im.setMatrixAt(n,du.matrix);im.setColorAt(n,cc.setRGB(.03+r()*.03,.035+r()*.03,.06+r()*.04));n++}}
    im.count=n;bg.add(im);const cm=new THREE.Mesh(own(mergeGeometries(cuL)),K.cu);bg.add(cm);cuL.forEach(x=>x.dispose());g.add(bg)}}}
  return T}
 function stream(B_,max){const R=LT?1.05:1.35,px=P.x,py=P.y;let hechos=0;const want=[];
  for(let ix=Math.floor((px-R)/TS);ix<=Math.floor((px+R)/TS);ix++)for(let iy=Math.floor((py-R)/TS);iy<=Math.floor((py+R)/TS);iy++){const d=Math.hypot((ix+.5)*TS-px,(iy+.5)*TS-py);if(d<R+TS*.71&&!B.tiles.has(ix+','+iy))want.push([d,ix,iy])}
  want.sort((a,b)=>a[0]-b[0]);for(const[d,ix,iy]of want){if(hechos>=max)break;const T=cuadro(ix,iy);B.tiles.set(ix+','+iy,T);if(!T.vacio){G.add(T.g);B.pulpos.push(...T.pulpos)}hechos++}
  for(const[k,T]of B.tiles){const d=Math.hypot((T.ix+.5)*TS-px,(T.iy+.5)*TS-py);if(d>R+TS*1.6){B.tiles.delete(k);if(T.vacio)continue;G.remove(T.g);T.own.forEach(x=>x.dispose());T.g.traverse(o=>{if(o.isInstancedMesh)o.dispose()});B.pulpos=B.pulpos.filter(p=>!T.pulpos.includes(p))}}}
 B.tiles=new Map();B.pulpos=[];B.stream=stream;
 {const sx=P.x,sy=P.y;P.x=D[0];P.y=D[1];stream(B,99);P.x=sx;P.y=sy}
 // peces: banco de sardinas (plata con lomo azul verdoso), sargos y maragotas sueltos; siempre alrededor del nadador
 {const b1=new THREE.SphereGeometry(1,14,8);b1.scale(1,.26,.17);const ta=new THREE.BufferGeometry();ta.setAttribute('position',new THREE.Float32BufferAttribute([-.85,0,0,-1.45,.32,0,-1.3,0,0,-.85,0,0,-1.3,0,0,-1.45,-.32,0],3));
  const dor=new THREE.BufferGeometry();dor.setAttribute('position',new THREE.Float32BufferAttribute([.15,.2,0,-.25,.2,0,-.05,.42,0],3));
  const fg=mergeGeometries([b1.toNonIndexed(),ta,dor].map(g=>{g.deleteAttribute('uv');g.deleteAttribute('normal');return g}));fg.computeVertexNormals();
  const fm=fmMat(B,'pez',{color:0xffffff,roughness:.3,metalness:.25,side:THREE.DoubleSide}),NS=LT?90:220,NI=LT?10:18,NP=NS+NI,im=new THREE.InstancedMesh(fg,fm,NP);
  const BAN=[{tipo:'banco',x:D[0]+.3,y:D[1]+.2,z:WY-.08,ph:rn()*6,R:.35+rn()*.25}];for(let k=0;k<NI;k++){const a=rn()*6.28,d=.15+rn()*.6;BAN.push({tipo:'suelto',x:D[0]+Math.cos(a)*d,y:D[1]+Math.sin(a)*d,z:WY-.05-rn()*.15,ph:rn()*6,R:.04+rn()*.1,w:(rn()<.5?1:-1)*(.25+rn()*.3)})}
  const PZ=[];for(let i=0;i<NP;i++){if(i<NS){PZ.push({b:BAN[0],o:[(rn()-.5)*.22,(rn()-.5)*.05,(rn()-.5)*.1].map(c=>c*(.5+.5*Math.cbrt(rn()))),ph:rn()*6.28,s:.0075+rn()*.002});im.setColorAt(i,new THREE.Color().setRGB(.05+rn()*.02,.14+rn()*.03,.2+rn()*.04))}
   else{const b=BAN[1+i-NS],sarg=rn()<.6;PZ.push({b,o:[0,0,0],ph:rn()*6.28,s:sarg?.016+rn()*.006:.02+rn()*.008});im.setColorAt(i,sarg?new THREE.Color(.32,.33,.32):new THREE.Color(.24,.2,.08))}}
  im.frustumCulled=false;im.castShadow=true;G.add(im);B.peces={im,PZ,BAN,du:new THREE.Object3D()}}
 // superficie vista desde abajo: ventana de Snell (el cielo en un cono de 97°), fuera de ella reflexión total; sigue a la cámara
 {const sm=new THREE.ShaderMaterial({uniforms:{uT:B.uT,uZen:SKYU.uZen,uHor:SKYU.uHor,uSun:SKYU.uSun,uNf:SKYU.uNight,uFog:{value:FOG.color}},transparent:true,depthWrite:false,side:THREE.DoubleSide,
   vertexShader:'varying vec3 vW;void main(){vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}',
   fragmentShader:`uniform float uT,uNf;uniform vec3 uZen,uHor,uSun,uFog;varying vec3 vW;
    float hh(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
    float nn(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hh(i),hh(i+vec2(1,0)),f.x),mix(hh(i+vec2(0,1)),hh(i+vec2(1,1)),f.x),f.y);}
    float wv(vec2 p){p=mod(p,10.);return nn(p*40.+vec2(uT*.7,uT*.3))*.6+nn(p*95.-vec2(uT*.9,-uT*.5))*.4;}
    void main(){vec3 V=normalize(vW-cameraPosition);vec2 q=vW.xz;float e=.002,h0=wv(q);vec2 g=vec2(wv(q+vec2(e,0.))-h0,wv(q+vec2(0.,e))-h0)/e*.004;
     vec3 N=normalize(vec3(-g.x,1.,-g.y));vec3 T=refract(V,-N,1.333);float d=length(vW-cameraPosition);vec3 col;float day=1.-uNf*.9;
     if(dot(T,T)<.01){col=uFog*(.55+.25*h0)+vec3(.0,.03,.03)*smoothstep(.6,.9,h0)*day;}
     else{vec3 sky=mix(uHor,uZen,smoothstep(0.,.7,T.y));float sun=pow(max(dot(T,normalize(uSun)),0.),300.)*12.+pow(max(dot(T,normalize(uSun)),0.),12.)*.4;
      float edge=pow(1.-clamp(T.y,0.,1.),6.);col=sky*(1.15-.5*edge)*day+vec3(1.,.97,.9)*sun*day*step(0.,uSun.y);col=mix(col,uFog*1.6,edge*.6);}
     col=mix(col,uFog,smoothstep(.15,1.3,d));gl_FragColor=vec4(col,.97);
     #include <tonemapping_fragment>
     #include <colorspace_fragment>
    }`});
  const sp=new THREE.Mesh(new THREE.CircleGeometry(RZ*1.4,64),sm);sp.rotation.x=Math.PI/2;sp.position.set(D[0],WY-.004,D[1]);sp.renderOrder=2;sp.frustumCulled=false;G.add(sp);B.sup=sp}
 // rayos de luz que bajan de la superficie (se recolocan alrededor del nadador)
 {const rm=new THREE.ShaderMaterial({uniforms:{uT:B.uT,uNf:SKYU.uNight},transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,fog:false,
   vertexShader:'varying vec2 vU;varying vec3 vW;varying vec3 vO;void main(){vU=uv;vO=modelMatrix[3].xyz;vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}',
   fragmentShader:`uniform float uT,uNf;varying vec2 vU;varying vec3 vW;varying vec3 vO;void main(){float x=vU.x,ed=smoothstep(0.,.4,x)*smoothstep(1.,.6,x);vec3 o=vO;
    float st=.35+.65*(.5+.5*sin(x*21.+uT*.5+o.x*40.))*(.5+.5*sin(x*8.3-uT*.33+o.z*31.));float v=pow(vU.y,1.8);float d=length(vW-cameraPosition);
    float a=ed*st*v*smoothstep(.04,.18,d)*(1.-smoothstep(.5,1.3,d))*(.5+.5*sin(uT*.6+o.x*17.))*.2*(1.-uNf*.95);gl_FragColor=vec4(vec3(.7,1.,.92)*a,1.);}`});
  B.rayos=[];for(let k=0;k<(LT?8:16);k++){const a=rn()*6.28,d=rn()*.7;const m=new THREE.Mesh(new THREE.PlaneGeometry(.05+rn()*.1,.5),rm);m.position.set(D[0]+Math.cos(a)*d,WY-.25,D[1]+Math.sin(a)*d);m.userData.ph=rn()*6;m.userData.tl=(rn()-.5)*.15;G.add(m);B.rayos.push(m)}}
 // nieve marina: partículas que siempre rodean a la cámara y derivan con la corriente
 {const NPa=LT?700:1800,ge=new THREE.BufferGeometry(),ps=new Float32Array(NPa*3),sz=new Float32Array(NPa);for(let k=0;k<NPa;k++){ps.set([rn(),rn(),rn()],k*3);sz[k]=.0005+Math.pow(rn(),4)*.0025}
  ge.setAttribute('position',new THREE.BufferAttribute(ps,3));ge.setAttribute('aS',new THREE.BufferAttribute(sz,1));
  const pm=new THREE.ShaderMaterial({uniforms:{uT:B.uT,uWY:B.FU.uWY,uPS:{value:600},uNf:SKYU.uNight},transparent:true,depthWrite:false,
   vertexShader:`uniform float uT,uWY,uPS;attribute float aS;varying float vD;void main(){float bx=.7;vec3 c=cameraPosition;
    vec3 p=position*bx+vec3(sin(uT*.2+position.y*20.)*.01+uT*.006,-uT*.003,cos(uT*.15+position.x*17.)*.01);p=mod(p-c+bx*.5,bx)+c-bx*.5;
    vec4 mv=viewMatrix*vec4(p,1.);vD=-mv.z;gl_Position=projectionMatrix*mv;if(p.y>uWY-.004)gl_Position=vec4(2.,2.,2.,1.);gl_PointSize=max(1.,aS*uPS/max(vD,.01));}`,
   fragmentShader:`uniform float uNf;varying float vD;void main(){float r=length(gl_PointCoord-.5);float a=smoothstep(.5,.15,r)*smoothstep(.015,.05,vD)*(1.-smoothstep(.12,.5,vD))*.4;gl_FragColor=vec4(vec3(.78,.92,.86)*(1.-uNf*.8),a);}`});
  const pt=new THREE.Points(ge,pm);pt.frustumCulled=false;G.add(pt);B.part=pt;
  const NB=60,bg=new THREE.BufferGeometry(),bp=new Float32Array(NB*3);for(let k=0;k<NB;k++)bp[k*3+1]=-99;bg.setAttribute('position',new THREE.BufferAttribute(bp,3));const bu=new THREE.Points(bg,new THREE.PointsMaterial({color:0xeaffff,size:.008,transparent:true,opacity:.85,depthWrite:false,map:burbujaTex()}));bu.frustumCulled=false;G.add(bu);B.burb={bu,bp,NB,k:0,v:new Float32Array(NB)}}
 B.tinta=[];{const tm=new THREE.SphereGeometry(1,10,8);for(let k=0;k<10;k++){const m=new THREE.Mesh(tm,new THREE.MeshBasicMaterial({color:0x0b0806,transparent:true,opacity:0,depthWrite:false}));m.visible=false;G.add(m);B.tinta.push({m,v:0,dx:0,dy:0})}}
 // esfera de niebla (tapa el cielo cuando la cámara está bajo el agua)
 {const fm=new THREE.MeshBasicMaterial({color:0x0b3f44,side:THREE.BackSide,depthWrite:false,fog:false});const fs=new THREE.Mesh(new THREE.SphereGeometry(1.6,24,16),fm);fs.renderOrder=-5;fs.visible=false;G.add(fs);B.esf=fs}
 scene.add(G);B.W=G;B.RZ=RZ;B.D0=D}
function buceoMundoTick(dt){const B=BUC;B.uT.value+=dt;const t=B.uT.value;
 if(B.stream)B.stream(B,1);
 // lo que acompaña al nadador: superficie, rayos, banco de peces y peces sueltos
 if(B.sup){B.sup.position.x=pcam.position.x;B.sup.position.z=pcam.position.z}
 for(const m of B.rayos)if(Math.hypot(m.position.x-P.x,m.position.z-P.y)>.85){const a=Math.random()*6.28,d=.3+Math.random()*.5;m.position.x=P.x+Math.cos(a)*d;m.position.z=P.y+Math.sin(a)*d}
 if(B.peces){const{im,PZ,BAN,du}=B.peces;
  const lejos=(x,y)=>Math.hypot(x-P.x,y-P.y)>1.1,reubica=(b,dmin,dmax)=>{for(let q=0;q<12;q++){const a=Math.random()*6.28,d=dmin+Math.random()*(dmax-dmin),x=P.x+Math.cos(a)*d,y=P.y+Math.sin(a)*d;if(cell(x,y).t===0&&B.WY-B.hB(x,y)>.08){b.x=x;b.y=y;b.z=Math.max(B.hB(x,y)+.04,Math.min(B.WY-.03,B.WY-.04-Math.random()*.12));return}}};
  for(const b of BAN){const cx_=b.cx??b.x,cy_=b.cy??b.y;if(lejos(cx_,cy_))reubica(b,b.tipo==='banco'?.6:.3,b.tipo==='banco'?.9:.8)}
  const b0=BAN[0],tt=t*.06+b0.ph,cx=b0.x+Math.sin(tt)*b0.R,cy=b0.y+Math.sin(tt*2)*b0.R*.45,vx=Math.cos(tt)*b0.R,vy=Math.cos(tt*2)*b0.R*.9,hd=Math.atan2(vy,vx);b0.cx=cx;b0.cy=cy;
  const cz=Math.max(B.hB(cx,cy)+.05,Math.min(B.WY-.03,b0.z+Math.sin(t*.21)*.025)),ch=Math.cos(hd),sh=Math.sin(hd);
  for(const b of BAN)if(b.tipo==='suelto'){const a=t*b.w*.6+b.ph;b.cx=b.x+Math.cos(a)*b.R;b.cy=b.y+Math.sin(a)*b.R*.7;b.vx=-Math.sin(a)*Math.sign(b.w);b.vy=Math.cos(a)*.7*Math.sign(b.w)}
  PZ.forEach((f,i)=>{const b=f.b;let x,y,z,a;
   if(b.tipo==='banco'){const r=f.o,rot=t*.25,ox=r[0]*Math.cos(rot*.3)-r[2]*Math.sin(rot*.3)*.4,oz=r[2]*Math.cos(rot*.3)+r[0]*Math.sin(rot*.3)*.4;
    x=cx+ox*ch-oz*sh+Math.sin(t*1.3+f.ph)*.004;y=cy+ox*sh+oz*ch+Math.cos(t*1.1+f.ph)*.004;z=cz+r[1]+Math.sin(t*1.7+f.ph)*.003;a=hd+Math.sin(t*2.3+f.ph)*.12}
   else{x=b.cx;y=b.cy;z=b.z+Math.sin(t*.7+f.ph)*.006;a=Math.atan2(b.vy,b.vx)}
   const dP=Math.hypot(x-P.x,y-P.y,z-(P.z||0));if(MODO==='nado'&&dP<.12){const k=(.12-dP)/.12*.09/Math.max(dP,.01);x+=(x-P.x)*k;y+=(y-P.y)*k;z+=(z-P.z)*k*.5}
   z=Math.max(B.hB(x,y)+.012,Math.min(B.WY-.015,z));du.position.set(x,z,y);du.rotation.set(0,-a,Math.sin(t*.9+f.ph)*.08);du.scale.setScalar(f.s);du.updateMatrix();im.setMatrixAt(i,du.matrix)});im.instanceMatrix.needsUpdate=true}
 if(B.pulpos)for(const o of B.pulpos){const m=o.m;
  if(o.huye>0){o.huye-=dt;const k=Math.min(1,o.huye/1.6);o.x+=o.dx*o.v*k*dt;o.y+=o.dy*o.v*k*dt;
   if(cell(o.x,o.y).t!==0){o.x-=o.dx*o.v*k*dt*2;o.y-=o.dy*o.v*k*dt*2;o.dx=-o.dx;o.dy=-o.dy}
   o.z=Math.max(B.hB(o.x,o.y),Math.min(B.WY-.03,o.z+(o.huye>1.3?.05:-.035)*dt));o.sw=o.huye>.5?Math.min(1,o.sw+dt*5):Math.max(0,o.sw-dt*2);
   const ta=Math.atan2(o.dy,-o.dx);let da=ta-m.rotation.y;da=Math.atan2(Math.sin(da),Math.cos(da));m.rotation.y+=da*Math.min(1,dt*6);o.a=m.rotation.y}
  else{o.sw=Math.max(0,o.sw-dt*1.5);o.z=Math.max(B.hB(o.x,o.y),o.z-.03*dt);o.a+=Math.sin(t*.25+o.ph)*.08*dt;m.rotation.y=o.a;
   if(MODO==='nado'&&Math.hypot(o.x-P.x,o.y-P.y,o.z-(P.z||0))<.09){const d=Math.hypot(o.x-P.x,o.y-P.y)||1;o.dx=(o.x-P.x)/d;o.dy=(o.y-P.y)/d;o.v=.2+Math.random()*.06;o.huye=2.4;
    for(let q=0;q<5;q++){const n=B.tinta.find(s=>!s.m.visible)||B.tinta[q];n.m.visible=true;n.v=0;n.m.position.set(o.x+(Math.random()-.5)*.01,o.z+.008+Math.random()*.008,o.y+(Math.random()-.5)*.01);n.dx=-o.dx*.02+(Math.random()-.5)*.015;n.dy=-o.dy*.02+(Math.random()-.5)*.015}}}
  m.position.set(o.x,o.z,o.y);o.U.uSw.value=o.sw}
 if(B.tinta)for(const n of B.tinta)if(n.m.visible){n.v+=dt;const k=n.v/4;n.m.scale.setScalar(.006+k*.045);n.m.material.opacity=.75*Math.max(0,1-k)*Math.min(1,n.v*4);n.m.position.x+=n.dx*dt;n.m.position.z+=n.dy*dt;n.m.position.y+=.002*dt;if(k>=1)n.m.visible=false}
 for(const m of B.rayos){m.lookAt(pcam.position.x,m.position.y,pcam.position.z);m.rotateZ(m.userData.tl)}
 if(B.part&&typeof R!=='undefined')B.part.material.uniforms.uPS.value=R.domElement.height/(2*Math.tan(pcam.fov*Math.PI/360));
 if(B.burb){const u=B.burb;if(MODO==='nado'&&P.z<B.WY-.025&&Math.random()<.35){u.k=(u.k+1)%u.NB;u.bp.set([P.x+(Math.random()-.5)*.01,P.z+.03,P.y+(Math.random()-.5)*.01],u.k*3);u.v[u.k]=.06+Math.random()*.05}
  if(B.reg&&!B.tiene&&Math.random()<.15){u.k=(u.k+1)%u.NB;u.bp.set([B.reg.x+(Math.random()-.5)*.02,B.reg.z+.02,B.reg.y],u.k*3);u.v[u.k]=.05}
  for(let k=0;k<u.NB;k++){if(u.bp[k*3+1]<B.WY-.005){u.bp[k*3+1]+=u.v[k]*dt;u.bp[k*3]+=Math.sin(t*6+k)*.0004}else u.bp[k*3+1]=-99}u.bu.geometry.attributes.position.needsUpdate=true}}
