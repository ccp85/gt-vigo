// ---------- orillas de las playas y arena realista (orilla.js, lo mete edit_orilla.py) ----------
// Las playas venían como una lámina plana unos metros por encima del mar y, en el borde, caían en vertical al agua
// (labio, zócalo y muro de costa): parecían cortadas y biseladas, con un escalón. Ahora, al cargar cada zona:
//  - en una franja de unos 15 m junto al agua, la arena baja poco a poco hasta meterse en el mar (perfil de playa:
//    suave en la orilla, algo más empinada en la cara de la playa y enlazando con la arena de siempre más arriba),
//    con una malla fina propia («orilla_arena») que sigue bajo el agua unos metros;
//  - lo que asomaba por encima en esa franja (la lámina vieja, la tierra, el labio, el zócalo y el muro de costa)
//    deja de dibujarse con una máscara por zona, así que no queda ningún corte ni escalón;
//  - el suelo por el que se camina (groundY, sueloRap, sueloVeh) usa la arena nueva y la gente de la playa se
//    coloca a su altura.
// La arena se pinta en el sombreado, en coordenadas del mundo (sin texturas que cargar): tonos de arena con manchas,
// grano de cerca, ondulaciones del viento con relieve, línea de restos secos de la marea alta, arena mojada más
// oscura y brillante, la lámina de agua que sube y baja por la orilla (resaca) con su encaje de espuma, y con lluvia
// toda la playa se oscurece. Todo es GLSL estándar de three.js (WebGL2), sin extensiones.
const ORI={WY:-.03,Z:[],G:.02};window.__ORI=ORI;
ORI.h=function(x,z){for(const e of ORI.Z){if(x<e.x0||z<e.z0||x>=e.x1||z>=e.z1||!e.root.parent)continue;
  const mi=Math.floor((x-e.x0)/e.mr),mj=Math.floor((z-e.z0)/e.mr);if(!e.M[mj*e.mw+mi])continue;
  for(const c of e.C){const fx=(x-c.x0)/c.g,fz=(z-c.z0)/c.g,i=Math.floor(fx),j=Math.floor(fz);if(i<0||j<0||i>=c.nx-1||j>=c.nz-1)continue;
   const H=c.H,k=j*c.nx+i,a=H[k],b=H[k+1],d=H[k+c.nx],f=H[k+c.nx+1];if(a!==a||b!==b||d!==d||f!==f)continue;
   const u=fx-i,v=fz-j;return (a*(1-u)+b*u)*(1-v)+(d*(1-u)+f*u)*v}}
 return null};
// altura del suelo para un impacto de rayo: si da en la lámina vieja de la playa (o en lo que tenía debajo) dentro de
// la franja nueva, vale la arena nueva
const ORI_RE=/^(playa|playita|tierra|labio|zocalo|muro_costa)/;
function oriSuelo(hit,x,z){if(ORI.Z.length&&hit.object&&ORI_RE.test(hit.object.name)){const v=ORI.h(x,z);if(v!==null)return v}return hit.point.y}
function oriZ(x,z,y){if(ORI.Z.length){const h=ORI.h(x,z);if(h!==null)return Math.max(h,ORI.WY+.001)}return y}
function oriPick(v){if(ORI.Z.length){const h=ORI.h(v.x,v.z);if(h!==null&&h<v.y)v.y=Math.max(h,ORI.WY+.001)}return v}
// arena realista en el sombreado
function arenaReal(m){if(!m||m.userData.arena)return m;m.userData.arena=1;const prev=m.onBeforeCompile;const pk=m.customProgramCacheKey?m.customProgramCacheKey.bind(m):null;const LT=!!window.LITE;
 m.onBeforeCompile=(sh,r)=>{if(prev)prev(sh,r);Object.assign(sh.uniforms,{uAT:UW.uT,uAWet:UMO.uWet,uAZen:SKYU.uZen,uAHor:SKYU.uHor});
  sh.vertexShader='varying vec3 vWa;\n'+sh.vertexShader.replace('#include <worldpos_vertex>','#include <worldpos_vertex>\n vWa=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='uniform float uAT,uAWet;uniform vec3 uAZen,uAHor;varying vec3 vWa;\nfloat hA(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}\nfloat nA(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hA(i),hA(i+vec2(1,0)),f.x),mix(hA(i+vec2(0,1)),hA(i+vec2(1,1)),f.x),f.y);}\nfloat aWet,aFilm;vec2 aGr;\n'+sh.fragmentShader
   .replace('#include <color_fragment>',`#include <color_fragment>
    {vec2 q=vWa.xz;float fw=max(length(fwidth(q)),1e-6);float hw=vWa.y-(${ORI.WY.toFixed(3)});
     float m1=nA(q*1.7),m2=nA(q*6.3+3.1),m3=nA(q*23.+9.7);                          // manchas de 60 a 4 m
     vec3 col=mix(vec3(.70,.57,.38),vec3(.85,.74,.54),smoothstep(.22,.78,m1*.55+m2*.45));
     col*=.93+.12*m3;
     float c1=1.-smoothstep(.004,.02,fw);                                              // detalle medio
     ${LT?'float c2=0.;':'float c2=1.-smoothstep(.0003,.0015,fw);'}                    // detalle de cerca
     float gr=(nA(q*700.)-.5)*c2+(nA(q*190.+4.)-.5)*.6*c1;col*=1.+.24*gr;              // grano
     col*=1.-.18*smoothstep(.72,.95,nA(q*420.+11.))*c2;                                // granitos oscuros
     float sec=smoothstep(.009,.02,hw);                                                // arena seca
     float wa=.6+(nA(q*2.3)-.5)*.9;vec2 wd=vec2(cos(wa),sin(wa));                      // ondulaciones del viento (~60 cm), a parches
     float ph=dot(q,wd)*(950.+300.*nA(q*5.))+nA(q*30.)*6.;
     float ra=smoothstep(.35,.8,nA(q*6.+2.))*(1.-smoothstep(.0015,.006,fw))*sec;col*=1.+.045*sin(ph)*ra;
     aGr=${LT?'vec2(0.)':'wd*cos(ph)*.13*ra'};
     float wr=exp(-pow((hw-.021-.005*(nA(q*3.)-.5))/.0022,2.))*smoothstep(.45,.8,nA(q*85.))*c1;
     col*=1.-.28*wr;                                                                    // restos secos de la pleamar
     float wetH=.012+.004*(nA(q*4.)-.5);aWet=1.-smoothstep(wetH*.55,wetH,hw);          // arena mojada
     float sw=.0035+.003*(.5+.5*sin(uAT*.7+nA(q*3.)*6.2832))+.0008*(nA(q*40.+uAT*.3)-.5); // la resaca sube y baja
     aFilm=1.-smoothstep(sw-.0008,sw+.0002,hw);
     float fo=smoothstep(sw-.0017,sw-.0004,hw)*(1.-smoothstep(sw-.0001,sw+.0007,hw));  // borde de espuma
     fo*=.3+.7*smoothstep(.3,.7,nA(q*260.+vec2(uAT*.05,0.))*.6+nA(q*60.)*.4);
     fo+=aFilm*smoothstep(.62,.8,nA(q*180.+vec2(0.,uAT*.08)))*.45*(1.-smoothstep(-.003,.002,sw-hw-.002)); // encaje que se retira
     vec3 wc=col*vec3(.52,.48,.42);col=mix(col,wc,aWet);
     col=mix(col,wc*vec3(.78,.9,.92),aFilm);
     col=mix(col,vec3(.90,.93,.92),clamp(fo,0.,1.)*.9);
     col=mix(col,col*.62,uAWet*(1.-aWet));                                             // lluvia
     aGr*=1.-aWet;
     diffuseColor.rgb=col;}`)
   .replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\n    roughnessFactor=mix(mix(.93,.32,aWet),.07,aFilm);roughnessFactor=mix(roughnessFactor,.4,uAWet*(1.-aWet)*.6);')
   .replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n    normal=normalize(normal+(viewMatrix*vec4(aGr.x,0.,aGr.y,0.)).xyz);')
   .replace('#include <emissivemap_fragment>',`#include <emissivemap_fragment>
    {vec3 aV=isOrthographic?vec3(0.,.8,0.):normalize(cameraPosition-vWa);float fr=.02+.98*pow(1.-clamp(aV.y,0.,1.),5.);
     totalEmissiveRadiance+=mix(uAHor,uAZen,.35)*fr*(aWet*.1+aFilm*.28);}`)};
 m.customProgramCacheKey=()=>(pk?pk():'')+'|arena'+(LT?'L':'');m.needsUpdate=true;return m}
// lo viejo que queda dentro de la franja nueva no se dibuja (máscara de la zona)
function oriTapa(m,U){if(!m||m.userData.oriT)return;m.userData.oriT=1;const prev=m.onBeforeCompile;const pk=m.customProgramCacheKey?m.customProgramCacheKey.bind(m):null;
 m.onBeforeCompile=(sh,r)=>{if(prev)prev(sh,r);Object.assign(sh.uniforms,U);
  sh.vertexShader='varying vec2 vOriQ;\n'+sh.vertexShader.replace('#include <worldpos_vertex>','#include <worldpos_vertex>\n vOriQ=(modelMatrix*vec4(transformed,1.)).xz;');
  sh.fragmentShader='uniform sampler2D uOriM;uniform vec4 uOriR;varying vec2 vOriQ;\n'+sh.fragmentShader.replace('void main() {','void main() {\n {vec2 uq=(vOriQ-uOriR.xy)/uOriR.zw;if(uq.x>0.&&uq.y>0.&&uq.x<1.&&uq.y<1.&&texture2D(uOriM,uq).r>.5)discard;}')};
 m.customProgramCacheKey=()=>(pk?pk():'')+'|oriT';m.needsUpdate=true}
// distancia (chaflán, dos pasadas) a las celdas marcadas, en unidades
function oriDist(src,nx,nz,g){const n=nx*nz,D=new Float32Array(n),a=g,b=g*1.4142;for(let k=0;k<n;k++)D[k]=src[k]?0:1e9;
 for(let j=0;j<nz;j++)for(let i=0;i<nx;i++){const k=j*nx+i;let d=D[k];if(!d)continue;if(i>0)d=Math.min(d,D[k-1]+a);if(j>0){d=Math.min(d,D[k-nx]+a);if(i>0)d=Math.min(d,D[k-nx-1]+b);if(i<nx-1)d=Math.min(d,D[k-nx+1]+b)}D[k]=d}
 for(let j=nz-1;j>=0;j--)for(let i=nx-1;i>=0;i--){const k=j*nx+i;let d=D[k];if(!d)continue;if(i<nx-1)d=Math.min(d,D[k+1]+a);if(j<nz-1){d=Math.min(d,D[k+nx]+a);if(i<nx-1)d=Math.min(d,D[k+nx+1]+b);if(i>0)d=Math.min(d,D[k+nx-1]+b)}D[k]=d}
 return D}
function oriBlur(A,nx,nz,r,it){const T=new Float32Array(A.length);for(let q=0;q<it;q++){
  for(let j=0;j<nz;j++){const o=j*nx;let s=0,c=0;for(let i=-r;i<=r;i++)if(i>=0&&i<nx){s+=A[o+i];c++}
   for(let i=0;i<nx;i++){T[o+i]=s/c;const ia=i-r,ib=i+r+1;if(ia>=0){s-=A[o+ia];c--}if(ib<nx){s+=A[o+ib];c++}}}
  for(let i=0;i<nx;i++){let s=0,c=0;for(let j=-r;j<=r;j++)if(j>=0&&j<nz){s+=T[j*nx+i];c++}
   for(let j=0;j<nz;j++){A[j*nx+i]=s/c;const ja=j-r,jb=j+r+1;if(ja>=0){s-=T[ja*nx+i];c--}if(jb<nz){s+=T[jb*nx+i];c++}}}}
 return A}
const oriSS=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t)};
// una playa (grupo de triángulos de arena juntos): rejilla fina con la altura nueva
function oriPlaya(T,ids,bb){const WY=ORI.WY;let g=ORI.G;const x0=Math.floor((bb[0]-.25)/g)*g,z0=Math.floor((bb[1]-.25)/g)*g;
 let nx=Math.ceil((bb[2]+.25-x0)/g)+1,nz=Math.ceil((bb[3]+.25-z0)/g)+1;
 if(nx*nz>2.5e6){g*=Math.sqrt(nx*nz/2.5e6);nx=Math.ceil((bb[2]+.25-x0)/g)+1;nz=Math.ceil((bb[3]+.25-z0)/g)+1}
 const n=nx*nz,Hb=new Float32Array(n).fill(NaN);
 // altura de la arena de siempre en cada punto de la rejilla
 for(const t of ids){const o=t*9,ax=T[o],ay=T[o+1],az=T[o+2],bx=T[o+3],by=T[o+4],bz=T[o+5],cx=T[o+6],cy=T[o+7],cz=T[o+8];
  const den=(bz-cz)*(ax-cx)+(cx-bx)*(az-cz);if(Math.abs(den)<1e-12)continue;
  const i0=Math.max(0,Math.ceil((Math.min(ax,bx,cx)-x0)/g)),i1=Math.min(nx-1,Math.floor((Math.max(ax,bx,cx)-x0)/g));
  const j0=Math.max(0,Math.ceil((Math.min(az,bz,cz)-z0)/g)),j1=Math.min(nz-1,Math.floor((Math.max(az,bz,cz)-z0)/g));
  for(let j=j0;j<=j1;j++){const z=z0+j*g;for(let i=i0;i<=i1;i++){const x=x0+i*g;
   const l1=((bz-cz)*(x-cx)+(cx-bx)*(z-cz))/den,l2=((cz-az)*(x-cx)+(ax-cx)*(z-cz))/den,l3=1-l1-l2;if(l1<-2e-3||l2<-2e-3||l3<-2e-3)continue;
   const y=l1*ay+l2*by+l3*cy,k=j*nx+i;if(!(Hb[k]>=y))Hb[k]=y}}}
 const W=new Uint8Array(n),L=new Uint8Array(n),B=new Uint8Array(n),O=new Uint8Array(n);let toca=false;
 const Mw=MAPA.w,Mh=MAPA.h,Mr=MAPA.res;
 for(let j=0;j<nz;j++){const mj=Math.round((z0+j*g-MAPA.oy)*Mr);for(let i=0;i<nx;i++){const k=j*nx+i,mi=Math.round((x0+i*g-MAPA.ox)*Mr),w=mi>=0&&mj>=0&&mi<Mw&&mj<Mh&&Math.round(MI[(mj*Mw+mi)*4]/40)===0;W[k]=w?1:0;L[k]=w?0:1;const b=Hb[k]===Hb[k];B[k]=b?1:0;O[k]=(!w&&!b)?1:0}}
 // rendijas entre el borde de la lámina de arena y el agua del mapa: son playa (se rellenan con la altura de al lado)
 {const dW0=oriDist(W,nx,nz,g),dB0=oriDist(B,nx,nz,g);const F=[];for(let k=0;k<n;k++)if(!W[k]&&!B[k]&&dW0[k]<.08&&dB0[k]<.07)F.push(k);
  for(let it=0;it<6&&F.length;it++){const nf=[];for(const k of F){let s_=0,c_=0;for(const q of [k-1,k+1,k-nx,k+nx])if(q>=0&&q<n&&Hb[q]===Hb[q]){s_+=Hb[q];c_++}if(c_)Hb[k]=s_/c_;else nf.push(k)}
   for(const k of F)if(Hb[k]===Hb[k]){B[k]=1;O[k]=0}F.length=0;F.push(...nf)}}
 for(let j=1;j<nz-1&&!toca;j++)for(let i=1;i<nx-1;i++){const k=j*nx+i;if(B[k]&&(W[k-1]||W[k+1]||W[k-nx]||W[k+nx])){toca=true;break}}
 if(!toca)return null;
 // distancia con signo a la orilla (+ tierra adentro, − mar adentro), suavizada para quitar los dientes del mapa
 const dW=oriDist(W,nx,nz,g),dL=oriDist(L,nx,nz,g),S=new Float32Array(n);
 for(let k=0;k<n;k++)S[k]=W[k]?-Math.min(dL[k]-g*.5,.6):Math.min(dW[k]-g*.5,.6);
 oriBlur(S,nx,nz,Math.max(1,Math.round(.045/g)),2);
 const dO=oriBlur(oriDist(O,nx,nz,g),nx,nz,Math.max(1,Math.round(.02/g)),1),dB=oriDist(B,nx,nz,g);
 const H=new Float32Array(n).fill(NaN);let nin=0;
 for(let k=0;k<n;k++){const s=S[k],tap=oriSS(.05,.13,dO[k]);
  if(B[k]){if(s>.32)continue;const ss=Math.max(s,-.06),p=WY+.25*ss+1.2*ss*Math.max(ss,0),hb=Hb[k];
   const kk=.006,hh=Math.max(kk-Math.abs(hb-p),0)/kk,sm=Math.min(hb,p)-hh*hh*kk*.25;   // mínimo suave (sin arista)
   H[k]=hb+(Math.min(sm,hb)-hb)*tap;nin++}
  else if(W[k]&&dB[k]<.12&&tap>.5&&s>-.2){H[k]=Math.max(WY+.25*s,WY-.05);nin++}}
 if(!nin)return null;
 const c={x0,z0,nx,nz,g,H};if(window.ORIDBG)c.dbg={Hb,S,dO,W};return c}
// malla de la arena nueva (solo los cuadros con sus cuatro esquinas dentro) y núcleo para la máscara
function oriMalla(c,mat){const {nx,nz,g,H,x0,z0}=c,ok=k=>H[k]===H[k];const id=new Int32Array(nx*nz).fill(-1),P=[],N=[],I=[];let nv=0;
 const vid=(i,j)=>{const k=j*nx+i;if(id[k]<0){id[k]=nv++;const h=H[k];P.push(x0+i*g,h,z0+j*g);
   const hl=i>0&&ok(k-1)?H[k-1]:h,hr=i<nx-1&&ok(k+1)?H[k+1]:h,hd=j>0&&ok(k-nx)?H[k-nx]:h,hu=j<nz-1&&ok(k+nx)?H[k+nx]:h;
   const ddx=(hr-hl)/(((i<nx-1&&ok(k+1))?1:0)+((i>0&&ok(k-1))?1:0)||1)/g,ddz=(hu-hd)/(((j<nz-1&&ok(k+nx))?1:0)+((j>0&&ok(k-nx))?1:0)||1)/g;
   const l=Math.hypot(ddx,1,ddz);N.push(-ddx/l,1/l,-ddz/l)}return id[k]};
 for(let j=0;j<nz-1;j++)for(let i=0;i<nx-1;i++){const k=j*nx+i;if(!ok(k)||!ok(k+1)||!ok(k+nx)||!ok(k+nx+1))continue;
  const a=vid(i,j),b=vid(i+1,j),d=vid(i,j+1),e=vid(i+1,j+1);
  if(Math.abs(H[k]-H[k+nx+1])<Math.abs(H[k+1]-H[k+nx]))I.push(a,d,e,a,e,b);else I.push(a,d,b,b,d,e)}
 if(!I.length)return null;
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(P,3));geo.setAttribute('normal',new THREE.Float32BufferAttribute(N,3));
 geo.setIndex(nv>65535?new THREE.Uint32BufferAttribute(I,1):new THREE.Uint16BufferAttribute(I,1));geo.computeBoundingSphere();geo.computeBoundingBox();
 const m=new THREE.Mesh(geo,mat);m.name='orilla_arena';m.receiveShadow=true;m.castShadow=false;m.userData.noLote=1;
 // núcleo: dentro y con sus ocho vecinos dentro (en el borde se sigue viendo lo de siempre, que está a la misma altura)
 const core=new Uint8Array(nx*nz);for(let j=1;j<nz-1;j++)for(let i=1;i<nx-1;i++){const k=j*nx+i;if(ok(k)&&ok(k-1)&&ok(k+1)&&ok(k-nx)&&ok(k+nx)&&ok(k-nx-1)&&ok(k-nx+1)&&ok(k+nx-1)&&ok(k+nx+1))core[k]=1}
 c.core=core;return m}
function orillaZona(root){if(!MAPA||!MI||root.userData.orilla)return;root.userData.orilla=1;const t0=performance.now();root.updateMatrixWorld(true);
 const PL=[];root.traverse(o=>{if(o.isMesh&&/^(playa|playita)/.test(o.name))PL.push(o)});if(!PL.length)return;
 // triángulos de arena en coordenadas del mundo
 let nt=0;for(const o of PL){const g=o.geometry;nt+=(g.index?g.index.count:g.attributes.position.count)/3}
 const T=new Float32Array(nt*9),v=new THREE.Vector3();let t=0;
 for(const o of PL){const g=o.geometry,p=g.attributes.position,ix=g.index,cnt=ix?ix.count:p.count;
  for(let i=0;i<cnt;i++){v.fromBufferAttribute(p,ix?ix.getX(i):i).applyMatrix4(o.matrixWorld);T[t*3]=v.x;T[t*3+1]=v.y;T[t*3+2]=v.z;t++}}
 // playas: triángulos que se tocan (rejilla gruesa de 0,4) → grupos
 const C=.4,cel=new Map(),par=new Int32Array(nt);for(let i=0;i<nt;i++)par[i]=i;const fnd=i=>{while(par[i]!==i){par[i]=par[par[i]];i=par[i]}return i};
 const bbT=new Float32Array(nt*4);
 for(let i=0;i<nt;i++){const o=i*9,ax=Math.min(T[o],T[o+3],T[o+6]),bx=Math.max(T[o],T[o+3],T[o+6]),az=Math.min(T[o+2],T[o+5],T[o+8]),bz=Math.max(T[o+2],T[o+5],T[o+8]);bbT[i*4]=ax;bbT[i*4+1]=az;bbT[i*4+2]=bx;bbT[i*4+3]=bz;
  for(let a=Math.floor(ax/C);a<=Math.floor(bx/C);a++)for(let b=Math.floor(az/C);b<=Math.floor(bz/C);b++){const k=a+','+b,f=cel.get(k);if(f===undefined)cel.set(k,i);else{const r1=fnd(f),r2=fnd(i);if(r1!==r2)par[r1]=r2}}}
 const grp=new Map();for(let i=0;i<nt;i++){const r=fnd(i);let q=grp.get(r);if(!q){q={ids:[],bb:[1e9,1e9,-1e9,-1e9]};grp.set(r,q)}q.ids.push(i);const b=q.bb;b[0]=Math.min(b[0],bbT[i*4]);b[1]=Math.min(b[1],bbT[i*4+1]);b[2]=Math.max(b[2],bbT[i*4+2]);b[3]=Math.max(b[3],bbT[i*4+3])}
 const LT=!!window.LITE,mat=arenaReal(new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9,metalness:0,polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-1}));
 const CL=[];for(const q of grp.values()){const ar=(q.bb[2]-q.bb[0])*(q.bb[3]-q.bb[1]);if(ar<.002)continue;const c=oriPlaya(T,q.ids,q.bb);if(!c)continue;const m=oriMalla(c,mat);if(!m)continue;root.add(m);CL.push(c)}
 for(const o of PL)for(const mm of [].concat(o.material))arenaReal(mm);
 if(!CL.length)return;
 // máscara de la zona (1 = se ve la arena nueva; lo viejo no se dibuja)
 let x0=1e9,z0=1e9,x1=-1e9,z1=-1e9;for(const c of CL){x0=Math.min(x0,c.x0);z0=Math.min(z0,c.z0);x1=Math.max(x1,c.x0+(c.nx-1)*c.g);z1=Math.max(z1,c.z0+(c.nz-1)*c.g)}
 let mr=.02;while(((x1-x0)/mr)*((z1-z0)/mr)>4e6)mr*=1.25;
 const mw=Math.ceil((x1-x0)/mr)+1,mh=Math.ceil((z1-z0)/mr)+1,M=new Uint8Array(mw*mh);
 for(const c of CL){const i0=Math.max(0,Math.floor((c.x0-x0)/mr)),i1=Math.min(mw-1,Math.ceil((c.x0+(c.nx-1)*c.g-x0)/mr)),j0=Math.max(0,Math.floor((c.z0-z0)/mr)),j1=Math.min(mh-1,Math.ceil((c.z0+(c.nz-1)*c.g-z0)/mr));
  for(let j=j0;j<=j1;j++){const z=z0+(j+.5)*mr,cj=Math.round((z-c.z0)/c.g);if(cj<0||cj>=c.nz)continue;
   for(let i=i0;i<=i1;i++){const x=x0+(i+.5)*mr,ci=Math.round((x-c.x0)/c.g);if(ci<0||ci>=c.nx)continue;if(c.core[cj*c.nx+ci])M[j*mw+i]=255}}}
 const tex=new THREE.DataTexture(M,mw,mh,THREE.RedFormat,THREE.UnsignedByteType);tex.magFilter=tex.minFilter=THREE.LinearFilter;tex.generateMipmaps=false;tex.needsUpdate=true;
 const U={uOriM:{value:tex},uOriR:{value:new THREE.Vector4(x0,z0,mw*mr,mh*mr)}};
 root.traverse(o=>{if(o.isMesh&&ORI_RE.test(o.name))for(const mm of [].concat(o.material))oriTapa(mm,U)});
 for(const c of CL)delete c.core;
 ORI.Z=ORI.Z.filter(e=>e.root.parent||performance.now()-e.t<60000);ORI.Z.push({t:performance.now(),root,x0,z0,x1:x0+mw*mr,z1:z0+mh*mr,mr,mw,mh,M,C:CL});
 root.userData.oriMs=Math.round(performance.now()-t0)}
