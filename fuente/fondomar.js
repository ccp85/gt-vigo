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
function buceoMundo(D,WY){const B=BUC,G=new THREE.Group();G.name='fondoMar';B.uT=B.uT||{value:0};const LT=!!window.LITE,RZ=1.35,DEP=.32;let sd=7;const rn=()=>(sd=(sd*16807)%2147483647)/2147483647;
 B.FU={uT:B.uT,uWY:{value:WY},uNf:SKYU.uNight,uSun:SKYU.uSun,uO:{value:new THREE.Vector3(D[0],0,D[1])}};
 const hs=(x,y)=>{const s=Math.sin(x*127.1+y*311.7)*43758.5453;return s-Math.floor(s)};
 const vn=(x,y)=>{const i=Math.floor(x),j=Math.floor(y),u=x-i,v=y-j,a=hs(i,j),b=hs(i+1,j),c=hs(i,j+1),d=hs(i+1,j+1),uu=u*u*(3-2*u),vv=v*v*(3-2*v);return a+(b-a)*uu+(c-a)*vv+(a-b-c+d)*uu*vv};
 const fbm=(x,y,o=4)=>{let s=0,a=.5,f=1,n=0;for(let k=0;k<o;k++){s+=a*vn(x*f+k*13.1,y*f-k*7.7);n+=a;f*=2.03;a*=.5}return s/n};
 const h3=(x,y,z)=>{const s=Math.sin(x*127.1+y*311.7+z*74.7)*43758.5453;return s-Math.floor(s)};
 const vn3=(x,y,z)=>{const i=Math.floor(x),j=Math.floor(y),k=Math.floor(z);let u=x-i,v=y-j,w=z-k;u=u*u*(3-2*u);v=v*v*(3-2*v);w=w*w*(3-2*w);const L=(a,b,t)=>a+(b-a)*t;
  return L(L(L(h3(i,j,k),h3(i+1,j,k),u),L(h3(i,j+1,k),h3(i+1,j+1,k),u),v),L(L(h3(i,j,k+1),h3(i+1,j,k+1),u),L(h3(i,j+1,k+1),h3(i+1,j+1,k+1),u),v),w)};
 const dTierra=(x,y)=>{for(let r_=.03;r_<=.5;r_+=.05)for(let q=0;q<8;q++){const a=q*.785;if(cell(x+Math.cos(a)*r_,y+Math.sin(a)*r_).t!==0)return r_}return .5};
 // relieve: talud desde la costa, dunas de arena y lomos de roca que afloran
 const roc=(x,y)=>THREE.MathUtils.smoothstep(fbm(x*2.6+11,y*2.6-4,3),.56,.74);
 const N=LT?64:110,S=RZ*2/N,H=new Float32Array((N+1)*(N+1));
 for(let j=0;j<=N;j++)for(let i=0;i<=N;i++){const x=D[0]-RZ+i*S,y=D[1]-RZ+j*S,dl=dTierra(x,y),k=THREE.MathUtils.smoothstep(dl,.02,.48);
  const dun=(fbm(x*5,y*5)-.5)*.045+Math.sin((x*.8+y*.6)*38+fbm(x*3,y*3)*5)*.004,rr=roc(x,y)*(fbm(x*14,y*14,3)*.07+.02);
  H[j*(N+1)+i]=WY-.035-DEP*k+dun*(.4+.6*k)+rr}
 B.hB=(x,y)=>{const fi=(x-(D[0]-RZ))/S,fj=(y-(D[1]-RZ))/S;if(fi<0||fj<0||fi>=N||fj>=N)return WY-DEP;const i=Math.floor(fi),j=Math.floor(fj),u=fi-i,v=fj-j,a=H[j*(N+1)+i],b=H[j*(N+1)+i+1],c=H[(j+1)*(N+1)+i],d=H[(j+1)*(N+1)+i+1];return a*(1-u)*(1-v)+b*u*(1-v)+c*(1-u)*v+d*u*v};
 const pg=new THREE.PlaneGeometry(RZ*2,RZ*2,N,N);pg.rotateX(-Math.PI/2);const pp=pg.attributes.position;for(let k=0;k<pp.count;k++){const x=pp.getX(k)+D[0],y=pp.getZ(k)+D[1];pp.setY(k,B.hB(x,y))}pg.translate(D[0],0,D[1]);pg.computeVertexNormals();
 const fondo=new THREE.Mesh(pg,fmMat(B,'arena'));fondo.receiveShadow=true;G.add(fondo);
 const enAgua=(x,y)=>cell(x,y).t===0;const sitio=(f)=>{for(let t=0;t<40;t++){const a=rn()*6.283,r_=Math.sqrt(rn())*(RZ-.08),x=D[0]+Math.cos(a)*r_,y=D[1]+Math.sin(a)*r_;if(enAgua(x,y)&&(!f||f(x,y)))return[x,y]}return null};
 const prof=(x,y)=>WY-B.hB(x,y);
 // bolos de granito (rocas de Vigo): icosaedros deformados con ruido, medio enterrados
 const ROCAM=fmMat(B,'roca',{roughness:.92}),RG=[];for(let g=0;g<(LT?6:10);g++){const ge=new THREE.IcosahedronGeometry(1,LT?2:3),pa=ge.attributes.position,sx=g*3.7;
  for(let q=0;q<pa.count;q++){const x=pa.getX(q),y=pa.getY(q),z=pa.getZ(q);let f=.78+.45*vn3(x*1.3+sx,y*1.3,z*1.3)+.14*vn3(x*3.2,y*3.2+sx,z*3.2)+.05*vn3(x*7,y*7,z*7+sx);
   const ny=y*f;pa.setXYZ(q,x*f,ny<-.25?-.25+(ny+.25)*.3:ny,z*f)}ge.computeVertexNormals();RG.push(ge)}
 const ROCAS=[];for(let k=0;k<(LT?40:85);k++){const p=sitio((x,y)=>rn()<.25+roc(x,y)*.9+(prof(x,y)<.12?.3:0));if(!p)continue;const sz=.02+Math.pow(rn(),2.2)*.11;
  const m=new THREE.Mesh(RG[k%RG.length],ROCAM);m.scale.set(sz*(.8+rn()*.6),sz*(.55+rn()*.4),sz*(.8+rn()*.6));m.rotation.set((rn()-.5)*.4,rn()*6.28,(rn()-.5)*.4);m.position.set(p[0],B.hB(p[0],p[1])+sz*.12,p[1]);m.castShadow=m.receiveShadow=true;G.add(m);ROCAS.push({x:p[0],y:p[1],z:m.position.y+m.scale.y*.75,r:sz})}
 // cantos rodados pequeños
 {const ge=new THREE.IcosahedronGeometry(1,1),NC=LT?160:420,im=new THREE.InstancedMesh(ge,ROCAM,NC),du=new THREE.Object3D();let n=0;
  for(let k=0;k<NC;k++){const r=ROCAS.length&&rn()<.6?ROCAS[Math.floor(rn()*ROCAS.length)]:null;let x,y;if(r){const a=rn()*6.28,d=r.r*(1+rn()*2.5);x=r.x+Math.cos(a)*d;y=r.y+Math.sin(a)*d}else{const p=sitio();if(!p)continue;[x,y]=p}if(!enAgua(x,y))continue;
   const s=.003+Math.pow(rn(),2)*.012;du.position.set(x,B.hB(x,y)+s*.2,y);du.rotation.set(rn()*3,rn()*3,rn()*3);du.scale.set(s*(1+rn()*.5),s*.6,s);du.updateMatrix();im.setMatrixAt(n++,du.matrix)}im.count=n;im.receiveShadow=true;G.add(im)}
 // laminarias: cinta ondulada con estipe, crecen sobre las rocas; se mecen con la corriente
 {const SEG=14,pos=[],idx=[];for(let i=0;i<=SEG;i++){const t=i/SEG,y=t,w=t<.22?.012:.075*Math.sin(Math.PI*Math.min(1,(t-.12)/.88))**.7+.01,ru=t<.22?0:Math.sin(t*31)*.02*t;
   pos.push(-w/2,y,ru,0,y,0,w/2,y,-ru);if(i<SEG){const a=i*3;idx.push(a,a+3,a+1,a+1,a+3,a+4,a+1,a+4,a+2,a+2,a+4,a+5)}}
  const kg=new THREE.BufferGeometry();kg.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));kg.setIndex(idx);kg.computeVertexNormals();
  const k2=kg.clone();k2.rotateY(1.2);k2.translate(.006,0,.004);const k3=kg.clone();k3.rotateY(-1.4);k3.translate(-.005,0,-.003);k2.scale(1,.85,1);k3.scale(1,.75,1);const KG=mergeGeometries([kg,k2,k3]);
  const km=fmMat(B,'alga',{color:0xffffff,roughness:.7,side:THREE.DoubleSide}),NK=LT?110:260,im=new THREE.InstancedMesh(KG,km,NK),du=new THREE.Object3D(),cc=new THREE.Color();let n=0;
  const base=ROCAS.filter(r=>WY-r.z>.06);for(let c=0;c<NK*2&&n<NK&&base.length;c++){const r=base[Math.floor(rn()*base.length)],a=rn()*6.28,d=rn()*r.r*.7,x=r.x+Math.cos(a)*d,y=r.y+Math.sin(a)*d,z=Math.max(B.hB(x,y),r.z-r.r*.3*rn());
   const h=Math.min(WY-.03-z,.06+rn()*.1);if(h<.03)continue;du.position.set(x,z,y);du.rotation.set((rn()-.5)*.3,rn()*6.28,(rn()-.5)*.3);du.scale.setScalar(h);du.updateMatrix();im.setMatrixAt(n,du.matrix);
   im.setColorAt(n,cc.setRGB(.17+rn()*.06,.13+rn()*.04,.035+rn()*.02));n++}im.count=n;im.castShadow=true;G.add(im)}
 // pradera de zostera en la arena poco honda
 {const bg=new THREE.PlaneGeometry(.06,1,1,4);bg.translate(0,.5,0);const pa=bg.attributes.position;for(let q=0;q<pa.count;q++){const y=pa.getY(q);pa.setX(q,pa.getX(q)*(1-y*.6));pa.setZ(q,y*y*.08)}bg.computeVertexNormals();
  const zm=fmMat(B,'alga',{color:0xffffff,roughness:.75,side:THREE.DoubleSide}),NZ=LT?1400:4200,im=new THREE.InstancedMesh(bg,zm,NZ),du=new THREE.Object3D(),cc=new THREE.Color();let n=0;
  for(let c=0;c<(LT?30:60)&&n<NZ;c++){const p=sitio((x,y)=>prof(x,y)<.26&&roc(x,y)<.35);if(!p)continue;const R=.06+rn()*.12;
   for(let q=0;q<NZ/(LT?18:32)&&n<NZ;q++){const a=rn()*6.28,d=Math.sqrt(rn())*R,x=p[0]+Math.cos(a)*d,y=p[1]+Math.sin(a)*d;if(!enAgua(x,y)||rn()>1-d/R*.7)continue;
    const h=.018+rn()*.03;du.position.set(x,B.hB(x,y)-.001,y);du.rotation.set((rn()-.5)*.3,rn()*6.28,(rn()-.5)*.3);du.scale.setScalar(h);du.updateMatrix();im.setMatrixAt(n,du.matrix);
    im.setColorAt(n,cc.setRGB(.06+rn()*.05,.15+rn()*.07,.04+rn()*.03));n++}}im.count=n;G.add(im)}
 // batea de mejilloneiro: emparrillado de madera con flotadores y cuerdas cubiertas de mejillón
 {const VIDA=c=>fmMat(B,'vida',{color:c,roughness:.85});let bx=null;for(let t=0;t<30&&!bx;t++){const a=rn()*6.28,d=.3+rn()*.5,x=D[0]+Math.cos(a)*d,y=D[1]+Math.sin(a)*d;let ok=true;for(const[ox,oy]of[[-.14,-.12],[.14,-.12],[-.14,.12],[.14,.12],[0,0]])if(!enAgua(x+ox,y+oy)||prof(x+ox,y+oy)<.14)ok=false;if(ok)bx=[x,y]}
  if(bx){const g=new THREE.Group(),mad=VIDA(0x3b2b1d),W=.24,L=.2;g.position.set(bx[0],0,bx[1]);g.rotation.y=rn()*3;
   for(let i=0;i<=6;i++){const b=new THREE.Mesh(new THREE.BoxGeometry(W,.004,.004),mad);b.position.set(0,WY+.004,-L/2+i*L/6);g.add(b)}
   for(let i=0;i<=2;i++){const b=new THREE.Mesh(new THREE.BoxGeometry(.006,.006,L+.02),mad);b.position.set(-W/2+i*W/2,WY+.008,0);g.add(b)}
   const fl=VIDA(0x6b7176);for(const[fx,fz]of[[-.08,-.06],[.08,-.06],[-.08,.06],[.08,.06]]){const c=new THREE.Mesh(new THREE.CylinderGeometry(.018,.018,.05,16),fl);c.rotation.x=Math.PI/2;c.position.set(fx,WY-.006,fz);g.add(c)}
   const NX=LT?4:6,NZb=LT?5:8,cu=VIDA(0x2d2a1e),PM=LT?45:80,mg=new THREE.SphereGeometry(1,7,5);mg.scale(1,.42,.48);const mm=fmMat(B,'vida',{color:0xffffff,roughness:.45,metalness:.1}),
    im=new THREE.InstancedMesh(mg,mm,NX*NZb*PM),du=new THREE.Object3D(),cc=new THREE.Color();let n=0;
   for(let i=0;i<NX;i++)for(let k=0;k<NZb;k++){const x=-W/2+.02+i*(W-.04)/(NX-1),z=-L/2+.015+k*(L-.03)/(NZb-1),wx=bx[0]+x*Math.cos(g.rotation.y)+z*Math.sin(g.rotation.y),wz=bx[1]-x*Math.sin(g.rotation.y)+z*Math.cos(g.rotation.y);
    const len=Math.min(.13,prof(wx,wz)-.035);const c=new THREE.Mesh(new THREE.CylinderGeometry(.0012,.0012,len,5),cu);c.position.set(x,WY-len/2,z);g.add(c);
    for(let q=0;q<PM;q++){const yy=WY-.01-rn()*(len-.012),a=rn()*6.28,r=.0035+rn()*.002;du.position.set(x+Math.cos(a)*r,yy,z+Math.sin(a)*r);du.rotation.set(rn()*.8-.4+Math.PI*.5*(rn()<.5?1:-1)*.4,-a,-1.1+rn()*.6);
     du.scale.setScalar(.0035+rn()*.0022);du.updateMatrix();im.setMatrixAt(n,du.matrix);im.setColorAt(n,cc.setRGB(.03+rn()*.03,.035+rn()*.03,.06+rn()*.04));n++}}
   im.count=n;g.add(im);G.add(g);B.batea=bx}}
 // vieiras sobre la arena, estrellas de mar (Marthasterias) y erizos (Paracentrotus) sobre las rocas, anémonas
 {const vg=new THREE.CircleGeometry(1,24,Math.PI*.18,Math.PI*.64);vg.rotateX(-Math.PI/2);const pa=vg.attributes.position;for(let q=0;q<pa.count;q++){const x=pa.getX(q),z=pa.getZ(q),a=Math.atan2(z,x),r=Math.hypot(x,z);pa.setY(q,(.18*(1-r*r)+.035*Math.abs(Math.sin(a*30)))*Math.min(1,r*4))}vg.computeVertexNormals();
  const NV=LT?14:30,im=new THREE.InstancedMesh(vg,fmMat(B,'vida',{color:0xffffff,roughness:.7,side:THREE.DoubleSide}),NV),du=new THREE.Object3D(),cc=new THREE.Color();let n=0;
  for(let k=0;k<NV;k++){const p=sitio((x,y)=>roc(x,y)<.3);if(!p)continue;du.position.set(p[0],B.hB(p[0],p[1])+.001,p[1]);du.rotation.set((rn()-.5)*.3,rn()*6.28,(rn()-.5)*.3);du.scale.setScalar(.008+rn()*.004);du.updateMatrix();im.setMatrixAt(n,du.matrix);im.setColorAt(n,cc.setRGB(.42+rn()*.1,.3+rn()*.06,.22));n++}im.count=n;G.add(im)}
 {const sh=new THREE.Shape();for(let q=0;q<=60;q++){const a=q/60*6.283,r_=.32+.68*Math.pow(.5+.5*Math.cos(a*5),2.2);q?sh.lineTo(Math.cos(a)*r_,Math.sin(a)*r_):sh.moveTo(r_,0)}
  const eg=new THREE.ExtrudeGeometry(sh,{depth:.12,bevelEnabled:true,bevelThickness:.12,bevelSize:.1,bevelSegments:2,curveSegments:4});eg.rotateX(-Math.PI/2);
  const NE=LT?10:22,im=new THREE.InstancedMesh(eg,fmMat(B,'vida',{color:0xffffff,roughness:.85}),NE),du=new THREE.Object3D(),cc=new THREE.Color();let n=0;
  for(let k=0;k<NE;k++){let x,y,z;const r=ROCAS.length&&rn()<.6?ROCAS[Math.floor(rn()*ROCAS.length)]:null;if(r){x=r.x+(rn()-.5)*r.r;y=r.y+(rn()-.5)*r.r;z=r.z-r.r*.15}else{const p=sitio();if(!p)continue;[x,y]=p;z=B.hB(x,y)}
   du.position.set(x,z+.002,y);du.rotation.set((rn()-.5)*.5,rn()*6.28,(rn()-.5)*.5);du.scale.setScalar(.008+rn()*.008);du.updateMatrix();im.setMatrixAt(n,du.matrix);im.setColorAt(n,cc.setRGB(.45+rn()*.2,.16+rn()*.08,.08+rn()*.05));n++}im.count=n;G.add(im)}
 {const parts=[new THREE.SphereGeometry(1,12,8)];const sp=new THREE.ConeGeometry(.07,1.15,4);sp.translate(0,.57+.6,0);for(let q=0;q<(LT?40:90);q++){const s=sp.clone(),y=1-2*(q+.5)/(LT?40:90),a=q*2.3999;if(y<-.4)continue;const r=Math.sqrt(1-y*y);
   const d=new THREE.Vector3(Math.cos(a)*r,y,Math.sin(a)*r);s.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),d));parts.push(s)}
  const ug=mergeGeometries(parts.map(g=>g.index?g.toNonIndexed():g));ug.scale(1,.75,1);const NU=LT?18:45,im=new THREE.InstancedMesh(ug,fmMat(B,'vida',{color:0xffffff,roughness:.55}),NU),du=new THREE.Object3D(),cc=new THREE.Color();let n=0;
  for(let k=0;k<NU&&ROCAS.length;k++){const r=ROCAS[Math.floor(rn()*ROCAS.length)],a=rn()*6.28,d=r.r*(.5+rn()*.6),x=r.x+Math.cos(a)*d,y=r.y+Math.sin(a)*d;if(!enAgua(x,y))continue;
   du.position.set(x,Math.max(B.hB(x,y),r.z-r.r*(.3+rn()*.5))+.003,y);du.rotation.set((rn()-.5)*.6,rn()*6,(rn()-.5)*.6);du.scale.setScalar(.004+rn()*.003);du.updateMatrix();im.setMatrixAt(n,du.matrix);im.setColorAt(n,cc.setRGB(.12+rn()*.05,.03,.12+rn()*.06));n++}im.count=n;G.add(im)}
 {const parts=[new THREE.CylinderGeometry(.5,.6,.5,12)];parts[0].translate(0,.25,0);const tg=new THREE.ConeGeometry(.07,1,4,3);tg.translate(0,.5,0);
  for(let q=0;q<(LT?18:36);q++){const t=tg.clone(),a=q*2.3999,r=.15+.3*Math.sqrt((q+.5)/36);t.rotateZ(.25+r*1.2);t.rotateY(-a);t.translate(Math.cos(a)*r,.5,Math.sin(a)*r);parts.push(t)}
  const ag=mergeGeometries(parts.map(g=>g.index?g.toNonIndexed():g));const NA=LT?14:32,im=new THREE.InstancedMesh(ag,fmMat(B,'alga',{color:0xffffff,roughness:.5}),NA),du=new THREE.Object3D(),cc=new THREE.Color();let n=0;
  for(let k=0;k<NA&&ROCAS.length;k++){const r=ROCAS[Math.floor(rn()*ROCAS.length)];if(WY-r.z<.04)continue;du.position.set(r.x+(rn()-.5)*r.r*.6,r.z-r.r*.1,r.y+(rn()-.5)*r.r*.6);du.rotation.set((rn()-.5)*.4,rn()*6,(rn()-.5)*.4);du.scale.setScalar(.008+rn()*.008);du.updateMatrix();im.setMatrixAt(n,du.matrix);
   im.setColorAt(n,rn()<.7?cc.setRGB(.16,.26,.08):cc.setRGB(.3,.08,.16));n++}im.count=n;G.add(im)}
 // pulpos: junto a las rocas, sobre el fondo
 {const pg=pulpoGeo(LT);B.pulpos=[];for(let k=0;k<(LT?2:4);k++){const r=ROCAS.length?ROCAS[Math.floor(rn()*ROCAS.length)]:null;let x,y;
   if(r){const a=rn()*6.28;x=r.x+Math.cos(a)*(r.r+.02);y=r.y+Math.sin(a)*(r.r+.02)}else{const p=sitio();if(!p)continue;[x,y]=p}if(!enAgua(x,y))continue;
   const U={uSw:{value:0}},m=new THREE.Mesh(pg,fmMat(B,'pulpo',{color:0xffffff,roughness:.55}));m.material.userData.U=U;m.scale.setScalar(.0085+rn()*.003);m.castShadow=true;m.frustumCulled=false;
   const o={m,U,x,y,z:B.hB(x,y),a:rn()*6.28,huye:0,sw:0,ph:rn()*6};m.position.set(x,o.z,y);m.rotation.y=o.a;G.add(m);B.pulpos.push(o)}
  B.tinta=[];const tm=new THREE.SphereGeometry(1,10,8);for(let k=0;k<10;k++){const m=new THREE.Mesh(tm,new THREE.MeshBasicMaterial({color:0x0b0806,transparent:true,opacity:0,depthWrite:false}));m.visible=false;G.add(m);B.tinta.push({m,v:0,dx:0,dy:0})}}
 // peces: banco de sardinas (plata con lomo azul verdoso), sargos y maragotas sueltos
 {const b1=new THREE.SphereGeometry(1,14,8);b1.scale(1,.26,.17);const ta=new THREE.BufferGeometry();ta.setAttribute('position',new THREE.Float32BufferAttribute([-.85,0,0,-1.45,.32,0,-1.3,0,0,-.85,0,0,-1.3,0,0,-1.45,-.32,0],3));
  const dor=new THREE.BufferGeometry();dor.setAttribute('position',new THREE.Float32BufferAttribute([.15,.2,0,-.25,.2,0,-.05,.42,0],3));
  const fg=mergeGeometries([b1.toNonIndexed(),ta,dor].map(g=>{g.deleteAttribute('uv');g.deleteAttribute('normal');return g}));fg.computeVertexNormals();
  const fm=fmMat(B,'pez',{color:0xffffff,roughness:.3,metalness:.25,side:THREE.DoubleSide}),NS=LT?90:220,NI=LT?10:18,NP=NS+NI,im=new THREE.InstancedMesh(fg,fm,NP),cc=new THREE.Color();
  const BAN=[];{const p=sitio((x,y)=>prof(x,y)>.12)||[D[0],D[1]];BAN.push({tipo:'banco',x:p[0],y:p[1],z:WY-.05-rn()*.08,ph:rn()*6,R:.35+rn()*.25})}
  for(let k=0;k<NI;k++){const r=ROCAS.length?ROCAS[Math.floor(rn()*ROCAS.length)]:{x:D[0],y:D[1],z:WY-.2};BAN.push({tipo:'suelto',x:r.x,y:r.y,z:Math.min(WY-.03,r.z+.01+rn()*.04),ph:rn()*6,R:.04+rn()*.1,w:(rn()<.5?1:-1)*(.25+rn()*.3)})}
  const PZ=[];for(let i=0;i<NP;i++){if(i<NS){const u=rn(),v=rn(),w=rn();PZ.push({b:BAN[0],o:[(u-.5)*.22,(v-.5)*.05,(w-.5)*.1].map((c,q)=>c*(.5+.5*Math.cbrt(rn()))),ph:rn()*6.28,s:.0075+rn()*.002});im.setColorAt(i,cc.setRGB(.05+rn()*.02,.14+rn()*.03,.2+rn()*.04))}
   else{const b=BAN[1+i-NS],sarg=rn()<.6;PZ.push({b,o:[0,0,0],ph:rn()*6.28,s:sarg?.016+rn()*.006:.02+rn()*.008});im.setColorAt(i,sarg?cc.setRGB(.32,.33,.32):cc.setRGB(.24,.2,.08))}}
  im.frustumCulled=false;im.castShadow=true;G.add(im);B.peces={im,PZ,BAN,du:new THREE.Object3D()}}
 // superficie vista desde abajo: ventana de Snell (el cielo en un cono de 97°), fuera de ella reflexión total del fondo
 {const sm=new THREE.ShaderMaterial({uniforms:{uT:B.uT,uZen:SKYU.uZen,uHor:SKYU.uHor,uSun:SKYU.uSun,uNf:SKYU.uNight,uFog:{value:FOG.color}},transparent:true,depthWrite:false,side:THREE.DoubleSide,
   vertexShader:'varying vec3 vW;void main(){vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}',
   fragmentShader:`uniform float uT,uNf;uniform vec3 uZen,uHor,uSun,uFog;varying vec3 vW;
    float hh(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
    float nn(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hh(i),hh(i+vec2(1,0)),f.x),mix(hh(i+vec2(0,1)),hh(i+vec2(1,1)),f.x),f.y);}
    float wv(vec2 p){return nn(p*40.+vec2(uT*.7,uT*.3))*.6+nn(p*95.-vec2(uT*.9,-uT*.5))*.4;}
    void main(){vec3 V=normalize(vW-cameraPosition);vec2 q=vW.xz;float e=.002,h0=wv(q);vec2 g=vec2(wv(q+vec2(e,0.))-h0,wv(q+vec2(0.,e))-h0)/e*.004;
     vec3 N=normalize(vec3(-g.x,1.,-g.y));vec3 T=refract(V,-N,1.333);float d=length(vW-cameraPosition);vec3 col;float day=1.-uNf*.9;
     if(dot(T,T)<.01){vec3 Rr=reflect(V,-N);col=uFog*(.55+.25*h0)+vec3(.0,.03,.03)*smoothstep(.6,.9,h0)*day;}
     else{vec3 sky=mix(uHor,uZen,smoothstep(0.,.7,T.y));float sun=pow(max(dot(T,normalize(uSun)),0.),300.)*12.+pow(max(dot(T,normalize(uSun)),0.),12.)*.4;
      float edge=pow(1.-clamp(T.y,0.,1.),6.);col=sky*(1.15-.5*edge)*day+vec3(1.,.97,.9)*sun*day*step(0.,uSun.y);col=mix(col,uFog*1.6,edge*.6);}
     col=mix(col,uFog,smoothstep(.15,1.3,d));gl_FragColor=vec4(col,.97);
     #include <tonemapping_fragment>
     #include <colorspace_fragment>
    }`});
  const sp=new THREE.Mesh(new THREE.CircleGeometry(RZ*1.4,64),sm);sp.rotation.x=Math.PI/2;sp.position.set(D[0],WY-.004,D[1]);sp.renderOrder=2;G.add(sp);B.sup=sp}
 // rayos de luz que bajan de la superficie: planos que miran a la cámara con estrías que se mueven
 {const rm=new THREE.ShaderMaterial({uniforms:{uT:B.uT,uNf:SKYU.uNight},transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,fog:false,
   vertexShader:'varying vec2 vU;varying vec3 vW;varying vec3 vO;void main(){vU=uv;vO=modelMatrix[3].xyz;vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}',
   fragmentShader:`uniform float uT,uNf;varying vec2 vU;varying vec3 vW;varying vec3 vO;void main(){float x=vU.x,ed=smoothstep(0.,.4,x)*smoothstep(1.,.6,x);vec3 o=vO;
    float st=.35+.65*(.5+.5*sin(x*21.+uT*.5+o.x*40.))*(.5+.5*sin(x*8.3-uT*.33+o.z*31.));float v=pow(vU.y,1.8);float d=length(vW-cameraPosition);
    float a=ed*st*v*smoothstep(.04,.18,d)*(1.-smoothstep(.5,1.3,d))*(.5+.5*sin(uT*.6+o.x*17.))*.2*(1.-uNf*.95);gl_FragColor=vec4(vec3(.7,1.,.92)*a,1.);}`});
  B.rayos=[];for(let k=0;k<(LT?8:16);k++){const p=sitio();if(!p)continue;const m=new THREE.Mesh(new THREE.PlaneGeometry(.05+rn()*.1,.5),rm);m.position.set(p[0],WY-.25,p[1]);m.userData.ph=rn()*6;m.userData.tl=(rn()-.5)*.15;G.add(m);B.rayos.push(m)}}
 // nieve marina: partículas que siempre rodean a la cámara (se repiten en una caja) y derivan con la corriente
 {const NPa=LT?700:1800,ge=new THREE.BufferGeometry(),ps=new Float32Array(NPa*3),sz=new Float32Array(NPa);for(let k=0;k<NPa;k++){ps.set([rn(),rn(),rn()],k*3);sz[k]=.0005+Math.pow(rn(),4)*.0025}
  ge.setAttribute('position',new THREE.BufferAttribute(ps,3));ge.setAttribute('aS',new THREE.BufferAttribute(sz,1));
  const pm=new THREE.ShaderMaterial({uniforms:{uT:B.uT,uWY:B.FU.uWY,uPS:{value:600},uNf:SKYU.uNight},transparent:true,depthWrite:false,
   vertexShader:`uniform float uT,uWY,uPS;attribute float aS;varying float vD;void main(){float bx=.7;vec3 c=cameraPosition;
    vec3 p=position*bx+vec3(sin(uT*.2+position.y*20.)*.01+uT*.006,-uT*.003,cos(uT*.15+position.x*17.)*.01);p=mod(p-c+bx*.5,bx)+c-bx*.5;
    vec4 mv=viewMatrix*vec4(p,1.);vD=-mv.z;gl_Position=projectionMatrix*mv;if(p.y>uWY-.004)gl_Position=vec4(2.,2.,2.,1.);gl_PointSize=max(1.,aS*uPS/max(vD,.01));}`,
   fragmentShader:`uniform float uNf;varying float vD;void main(){float r=length(gl_PointCoord-.5);float a=smoothstep(.5,.15,r)*smoothstep(.015,.05,vD)*(1.-smoothstep(.12,.5,vD))*.4;gl_FragColor=vec4(vec3(.78,.92,.86)*(1.-uNf*.8),a);}`});
  const pt=new THREE.Points(ge,pm);pt.frustumCulled=false;G.add(pt);B.part=pt;
  const NB=60,bg=new THREE.BufferGeometry(),bp=new Float32Array(NB*3);for(let k=0;k<NB;k++)bp[k*3+1]=-99;bg.setAttribute('position',new THREE.BufferAttribute(bp,3));const bu=new THREE.Points(bg,new THREE.PointsMaterial({color:0xeaffff,size:.008,transparent:true,opacity:.75,depthWrite:false}));bu.frustumCulled=false;G.add(bu);B.burb={bu,bp,NB,k:0,v:new Float32Array(NB)}}
 // esfera de niebla (tapa el cielo cuando la cámara está bajo el agua)
 {const fm=new THREE.MeshBasicMaterial({color:0x0b3f44,side:THREE.BackSide,depthWrite:false,fog:false});const fs=new THREE.Mesh(new THREE.SphereGeometry(1.6,24,16),fm);fs.renderOrder=-5;fs.visible=false;G.add(fs);B.esf=fs}
 scene.add(G);B.W=G;B.RZ=RZ;B.D0=D}
function buceoMundoTick(dt){const B=BUC;B.uT.value+=dt;const t=B.uT.value;
 if(B.peces){const{im,PZ,BAN,du}=B.peces;
  // el banco recorre la zona en un ocho lento; sus peces van todos en la misma dirección y se abren al paso del nadador
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
   if(cell(o.x,o.y).t!==0||Math.hypot(o.x-B.D0[0],o.y-B.D0[1])>B.RZ-.08){o.x-=o.dx*o.v*k*dt*2;o.y-=o.dy*o.v*k*dt*2;o.dx=-o.dx;o.dy=-o.dy}
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
