// ---------- marcas viales rectas (edit_lineasrectas.py + lineasrectas.js)
// Las marcas viales horneadas de cada zona («lineas») venían troceadas: trazos sesgados, cuñas sueltas, líneas de borde que
// cruzaban las plazas y los cruces, pasos de cebra torcidos... parecían un collage. Al cargar cada zona se rehacen desde el
// eje de las calles (el mismo grafo del tráfico) y la propia calzada:
//  - se mide el ancho real de asfalto a cada lado del eje y se usa un ancho fijo por calle (mediana), así las líneas van
//    rectas y paralelas al bordillo, con carriles de ~3,2 m;
//  - línea central (continua en avenidas, discontinua en calles), separación de carriles discontinua (3 m de trazo y 5 de
//    hueco), líneas de borde en avenidas, todas de 15-20 cm de ancho;
//  - en los cruces las líneas se cortan donde empieza la otra calle y en las entradas hay línea de detención (continua si
//    cruza una avenida, de ceda el paso discontinua si no);
//  - los pasos de cebra se rehacen donde estaban: perpendiculares a la calle, de bordillo a bordillo, bandas de 50 cm;
//  - las marcas que no son de calle (aparcamientos, explanadas, muelles...) se conservan tal cual.
// Todo va en la misma malla y material que antes (desgaste, mojado, versión WebGPU y móvil siguen igual).
// window.__LINEAS_VIEJAS=true antes de cargar deja las marcas de antes.
(function(){
const U=1/55;                                       // 1 metro en unidades del mapa (aprox.)
const RANK={m:0,E:1,S:2,P:3,T:4};
const LW=.15*U*1.3, LWB=.2*U*1.2, LST=.4*U, DASH=3*U, GAP=5*U, LANE=3.2*U, ALT=.0065;
const ZEB_W=.5*U, ZEB_G=.5*U, ZEB_L=3*U;
const pausa=()=>Promise.resolve();

// rejilla de triángulos de la calzada (en coordenadas del mundo): dentro/fuera y altura
function Rejilla(tris,CS){this.CS=CS;this.t=tris;let x0=1e9,z0=1e9,x1=-1e9,z1=-1e9;
 for(let i=0;i<tris.length;i+=3){const x=tris[i],z=tris[i+2];if(x<x0)x0=x;if(x>x1)x1=x;if(z<z0)z0=z;if(z>z1)z1=z}
 this.x0=x0;this.z0=z0;this.nx=Math.max(1,Math.ceil((x1-x0)/CS)+1);this.nz=Math.max(1,Math.ceil((z1-z0)/CS)+1);
 const cnt=new Uint32Array(this.nx*this.nz+1);const nt=tris.length/9;
 const each=(t,f)=>{const o=t*9;const a=Math.min(tris[o],tris[o+3],tris[o+6]),b=Math.max(tris[o],tris[o+3],tris[o+6]),c=Math.min(tris[o+2],tris[o+5],tris[o+8]),d=Math.max(tris[o+2],tris[o+5],tris[o+8]);
  const i0=Math.floor((a-x0)/CS),i1=Math.floor((b-x0)/CS),j0=Math.floor((c-z0)/CS),j1=Math.floor((d-z0)/CS);
  if((i1-i0+1)*(j1-j0+1)>4000)return;for(let j=j0;j<=j1;j++)for(let i=i0;i<=i1;i++)f(j*this.nx+i)};
 for(let t=0;t<nt;t++)each(t,c=>cnt[c+1]++);
 for(let i=1;i<cnt.length;i++)cnt[i]+=cnt[i-1];
 const fill=cnt.slice(0,this.nx*this.nz),lst=new Uint32Array(cnt[cnt.length-1]);
 for(let t=0;t<nt;t++)each(t,c=>{lst[fill[c]++]=t});this.st=cnt;this.l=lst}
// alturas de la calzada en (x,z); devuelve la más cercana a yRef (o la más baja), o NaN si no hay asfalto
Rejilla.prototype.alt=function(x,z,yRef){const i=Math.floor((x-this.x0)/this.CS),j=Math.floor((z-this.z0)/this.CS);
 if(i<0||j<0||i>=this.nx||j>=this.nz)return NaN;const c=j*this.nx+i,T=this.t;let best=NaN,bd=1e9;
 for(let k=this.st[c];k<this.st[c+1];k++){const o=this.l[k]*9;
  const ax=T[o],az=T[o+2],bx=T[o+3]-ax,bz=T[o+5]-az,cx=T[o+6]-ax,cz=T[o+8]-az,px=x-ax,pz=z-az;
  const den=bx*cz-cx*bz;if(Math.abs(den)<1e-14)continue;const u=(px*cz-cx*pz)/den,v=(bx*pz-px*bz)/den;
  if(u<-1e-5||v<-1e-5||u+v>1+1e-5)continue;const y=T[o+1]+u*(T[o+4]-T[o+1])+v*(T[o+7]-T[o+1]);
  const d=yRef==null||isNaN(yRef)?y:Math.abs(y-yRef);if(d<bd){bd=d;best=y}}
 return best};

// rejilla de segmentos de los ejes (para «¿estoy más cerca de otra calle?»)
function RejSeg(ways,CS){this.CS=CS;this.m=new Map();this.w=ways;
 ways.forEach((w,wi)=>{const p=w.p;for(let i=1;i<p.length;i++){const a=p[i-1],b=p[i];
  const i0=Math.floor(Math.min(a[0],b[0])/CS),i1=Math.floor(Math.max(a[0],b[0])/CS),j0=Math.floor(Math.min(a[1],b[1])/CS),j1=Math.floor(Math.max(a[1],b[1])/CS);
  for(let j=j0;j<=j1;j++)for(let k=i0;k<=i1;k++){const key=k+','+j;let L=this.m.get(key);if(!L)this.m.set(key,L=[]);L.push(wi,i)}}})}
function dSeg(px,pz,a,b){const dx=b[0]-a[0],dz=b[1]-a[1],L2=dx*dx+dz*dz;let t=L2?((px-a[0])*dx+(pz-a[1])*dz)/L2:0;t=t<0?0:t>1?1:t;const x=a[0]+dx*t-px,z=a[1]+dz*t-pz;return Math.sqrt(x*x+z*z)}
RejSeg.prototype.mas=function(x,z){const CS=this.CS,i=Math.floor(x/CS),j=Math.floor(z/CS);let bd=1e9,b=null;
 for(let jj=j-2;jj<=j+2;jj++)for(let ii=i-2;ii<=i+2;ii++){const L=this.m.get(ii+','+jj);if(!L)continue;
  for(let k=0;k<L.length;k+=2){const p=this.w[L[k]].p,d=dSeg(x,z,p[L[k+1]-1],p[L[k+1]]);if(d<bd&&this.ok(L[k])){bd=d;b=[L[k],L[k+1]]}}}
 return {d:bd,b}};
RejSeg.prototype.ok=function(){return true};
RejSeg.prototype.cerca=function(x,z,skip){const CS=this.CS,i=Math.floor(x/CS),j=Math.floor(z/CS);let bd=1e9;
 for(let jj=j-1;jj<=j+1;jj++)for(let ii=i-1;ii<=i+1;ii++){const L=this.m.get(ii+','+jj);if(!L)continue;
  for(let k=0;k<L.length;k+=2){if(L[k]===skip)continue;const p=this.w[L[k]].p,d=dSeg(x,z,p[L[k+1]-1],p[L[k+1]]);if(d<bd)bd=d}}
 return bd};

const med=a=>{if(!a.length)return NaN;const b=a.slice().sort((x,y)=>x-y);return b[b.length>>1]};
const kp=p=>p[0].toFixed(3)+','+p[1].toFixed(3);

// polilínea con longitudes acumuladas y punto/normal a una distancia s
function Poli(p){this.p=p;const a=[0];for(let i=1;i<p.length;i++)a.push(a[i-1]+Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]));this.a=a;this.L=a[a.length-1]}
Poli.prototype.en=function(s){const a=this.a,p=this.p;let i=1;while(i<a.length-1&&a[i]<s)i++;const L=a[i]-a[i-1]||1e-9,t=Math.max(0,Math.min(1,(s-a[i-1])/L));
 const dx=(p[i][0]-p[i-1][0])/L,dz=(p[i][1]-p[i-1][1])/L;return [p[i-1][0]+(p[i][0]-p[i-1][0])*t,p[i-1][1]+(p[i][1]-p[i-1][1])*t,dx,dz,i]};
// normal suavizada en los vértices (para que las líneas paralelas no se quiebren en cada vértice)
Poli.prototype.nrm=function(s){const a=this.a,p=this.p;const q=this.en(s);let dx=q[2],dz=q[3];const i=q[4];
 const near=(k)=>{if(k<=0||k>=p.length-1)return null;const L1=a[k]-a[k-1],L2=a[k+1]-a[k];if(!L1||!L2)return null;return[(p[k][0]-p[k-1][0])/L1+(p[k+1][0]-p[k][0])/L2,(p[k][1]-p[k-1][1])/L1+(p[k+1][1]-p[k][1])/L2]};
 const R=1.5*U;
 if(i-1>0&&s-a[i-1]<R){const m=near(i-1);if(m){const f=.5*(1-(s-a[i-1])/R);const l=Math.hypot(m[0],m[1])||1;dx=dx*(1-f)+m[0]/l*f;dz=dz*(1-f)+m[1]/l*f}}
 if(i<p.length-1&&a[i]-s<R){const m=near(i);if(m){const f=.5*(1-(a[i]-s)/R);const l=Math.hypot(m[0],m[1])||1;dx=dx*(1-f)+m[0]/l*f;dz=dz*(1-f)+m[1]/l*f}}
 const l=Math.hypot(dx,dz)||1;return [q[0],q[1],dx/l,dz/l]};

function simplifica(p,tol,fijo){if(p.length<3)return p;const keep=new Uint8Array(p.length);keep[0]=keep[p.length-1]=1;for(let i=1;i<p.length-1;i++)if(fijo(p[i]))keep[i]=1;const st=[[0,p.length-1]];
 while(st.length){const[a,b]=st.pop();let md=0,mi=-1;for(let i=a+1;i<b;i++){const d=dSeg(p[i][0],p[i][1],p[a],p[b]);if(d>md){md=d;mi=i}}if(md>tol){keep[mi]=1;st.push([a,mi],[mi,b])}}
 return p.filter((_,i)=>keep[i])}
async function construir(tris,ways,viejas){
 const cuenta=new Map();for(const w of ways)for(const q of w.p){const k=kp(q);cuenta.set(k,(cuenta.get(k)||0)+1)}
 const fijo=q=>cuenta.get(kp(q))>1;
 ways=ways.map(w=>Object.assign({},w,{p:simplifica(w.p,.6*U,fijo)}));
 const R=new Rejilla(tris,.04);await pausa();
 const RS=new RejSeg(ways,.15);
 // ---- nudos: grado de cada punto del grafo
 const nud=new Map();
 ways.forEach((w,wi)=>{const p=w.p;p.forEach((q,i)=>{const k=kp(q);let n=nud.get(k);if(!n)nud.set(k,n={g:0,w:[]});const ext=i===0||i===p.length-1;n.g+=ext?1:2;n.w.push([wi,i])})});
 // ---- ancho de cada calle (mediana a cada lado)
 const info=[];let t0=performance.now();
 for(let wi=0;wi<ways.length;wi++){const w=ways[wi],P=new Poli(w.p);const I={P,w,ok:false};info.push(I);if(P.L<.02)continue;
  const n=Math.max(3,Math.min(400,Math.round(P.L/(1.2*U))));const izq=[],der=[],ms=[];let yr=NaN;
  for(let k=0;k<n;k++){const s=P.L*(k+.5)/n;const[x,z,dx,dz]=P.nrm(s);const y=R.alt(x,z,yr);if(isNaN(y))continue;yr=y;
   let abierto=false;
   for(const sg of [1,-1]){let d=0;const st=.25*U;let vor=false;for(;d<14*U;d+=st){const qx=x-dz*sg*(d+st),qz=z+dx*sg*(d+st);const yy=R.alt(qx,qz,y);if(isNaN(yy)||Math.abs(yy-y)>.02)break;if(d>3*U&&RS.cerca(qx,qz,wi)<d+st){vor=true;break}}
    if(!vor&&d>=14*U-st)abierto=true;
    if(vor){let e=d,ok=true;for(;e<d+24*U;e+=1*U){const yy=R.alt(x-dz*sg*e,z+dx*sg*e,y);if(isNaN(yy)||Math.abs(yy-y)>.02){ok=false;break}}if(ok)abierto=true}
    (sg>0?izq:der).push(d)}
   if(abierto)ms.push([s,1e9,1e9]);else
   ms.push([s,izq[izq.length-1],der[der.length-1]])}
  if(izq.length<Math.max(2,n*.4))continue;
  let wl=med(izq),wr=med(der);if(!(wl>1.5*U&&wr>1.5*U))continue;
  const rk=RANK[w.c]||0,maxC=(w.u?[2,2,3,4,4]:[2,4,4,6,6])[rk]*LANE*1.12;   // más ancho que esto: explanada o plaza, no calle
  const disp=Math.abs(med(izq.map((v,i)=>v+(der[i]||0)))-(wl+wr));
  I.abierta=wl+wr>maxC*2;if(!I.abierta&&wl+wr>maxC){if(wl>wr)wl=Math.max(maxC-wr,maxC/2);else wr=Math.max(maxC-wl,maxC/2)}
  I.regular=!I.abierta&&disp<1.5*U;
  // tramos donde la calzada se ensancha mucho (bocas de cruce, plazas, explanadas): sin líneas a lo largo
  const lim=(wl+wr)*1.35+2*U;const fl=[];for(const[s,a,b]of ms){if(a+b>lim||a>wl*1.6+1.5*U||b>wr*1.6+1.5*U)fl.push(s)}
  const paso=P.L/n;I.flare=fl.map(s=>[s-paso*.6-1*U,s+paso*.6+1*U]);
  if(I.abierta)I.flare=[[-1,P.L+1]];
  I.wl=wl;I.wr=wr;I.W=wl+wr;I.off=(wl-wr)/2;I.ok=true;   // off: centro de la calzada respecto al eje (positivo = izquierda)
  if(performance.now()-t0>8){await pausa();t0=performance.now()}}
 // ---- recorte en cada extremo (cruces)
 const ang=(a,b)=>Math.abs(a[0]*b[0]+a[1]*b[1]);
 const dirEn=(I,ext)=>{const P=I.P;const q=ext?P.en(Math.max(0,P.L-2*U)):P.en(Math.min(P.L,2*U));const r=ext?P.en(P.L):P.en(0);const dx=r[0]-q[0],dz=r[1]-q[1],l=Math.hypot(dx,dz)||1;return[dx/l,dz/l]}; // hacia el nudo
 for(const I of info){if(!I.ok)continue;I.cut=[0,0];I.stop=[0,0];
  for(const ext of [0,1]){const q=ext?I.w.p[I.w.p.length-1]:I.w.p[0];const N=nud.get(kp(q));if(!N||N.g<3)continue;
   const d0=dirEn(I,ext);let r=0,mayor=false,sigue=false;
   for(const[wj,ij]of N.w){const J=info[wj];if(J===I)continue;if(!J.ok&&!J.w)continue;const p=J.w.p;
    const outs=[];if(ij>0)outs.push(p[ij-1]);if(ij<p.length-1)outs.push(p[ij+1]);
    for(const o of outs){const dx=o[0]-q[0],dz=o[1]-q[1],l=Math.hypot(dx,dz)||1;const v=[dx/l,dz/l];
     const col=(d0[0]*v[0]+d0[1]*v[1])>.85;                     // continuación recta de esta calle
     if(col&&(RANK[J.w.c]||0)>=(RANK[I.w.c]||0)){sigue=true;continue}
     if(col)continue;const hw=J.ok?Math.max(J.wl,J.wr):3*U;
     const s=Math.sqrt(Math.max(.05,1-ang(d0,v)**2));            // calles en diagonal: hace falta más distancia
     r=Math.max(r,hw/s+1*U);if((RANK[J.w.c]||0)>=3)mayor=true}}
   if(sigue&&r>0&&(RANK[I.w.c]||0)>=3&&!mayor){r=0}               // la avenida sigue recta y la otra es menor: no se corta
   I.cut[ext]=Math.min(r,I.P.L*.45);I.stop[ext]=r>0?(mayor||(RANK[I.w.c]||0)>=3?2:1):0}}
 await pausa();
 // ---- pasos de cebra (donde estaban): bandas anchas de las marcas viejas agrupadas
 const cebras=[];
 if(viejas&&viejas.comps){const cand=viejas.comps.filter(c=>c.nt===2&&c.W>.006&&c.W<.022&&c.L>.018&&c.L<.09&&c.fill>.6);
  const usados=new Set(),CG=.04,G=new Map();cand.forEach((c,i)=>{const k=Math.floor(c.cx/CG)+','+Math.floor(c.cz/CG);let L=G.get(k);if(!L)G.set(k,L=[]);L.push(i)});
  for(let a=0;a<cand.length;a++){if(usados.has(a))continue;const g=[a];usados.add(a);
   for(let gi=0;gi<g.length;gi++){const A=cand[g[gi]];const i0=Math.floor(A.cx/CG),j0=Math.floor(A.cz/CG);
    for(let jj=j0-1;jj<=j0+1;jj++)for(let ii=i0-1;ii<=i0+1;ii++){const L=G.get(ii+','+jj);if(!L)continue;for(const b of L){if(usados.has(b))continue;const B=cand[b];
    if(Math.abs(A.ux*B.ux+A.uz*B.uz)<.9)continue;const dx=B.cx-A.cx,dz=B.cz-A.cz;const lat=Math.abs(dx*A.uz-dz*A.ux),lon=Math.abs(dx*A.ux+dz*A.uz);
    if(lat<.035&&lon<.012){g.push(b);usados.add(b)}}}}
   if(g.length<3)continue;let cx=0,cz=0;for(const k of g){cx+=cand[k].cx;cz+=cand[k].cz}cx/=g.length;cz/=g.length;
   cebras.push({cx,cz,n:g.length,ids:g.map(k=>cand[k].id),pts:g.map(k=>[cand[k].cx,cand[k].cz])})}}
 // calle de cada paso de cebra
 const ceb=[];
 RS.ok=wi=>info[wi].ok;
 for(const C of cebras){const bb=RS.mas(C.cx,C.cz);const best=bb.b,bd=bb.d;
  if(!best||bd>.25)continue;const I=info[best[0]],p=I.w.p,a=p[best[1]-1],b=p[best[1]];
  const dx=b[0]-a[0],dz=b[1]-a[1],l=Math.hypot(dx,dz)||1,ux=dx/l,uz=dz/l;
  let t=((C.cx-a[0])*ux+(C.cz-a[1])*uz);const s=I.P.a[best[1]-1]+Math.max(0,Math.min(l,t));
  const y=R.alt(C.cx,C.cz,NaN);if(isNaN(y))continue;
  // de bordillo a bordillo a lo largo de la normal, sin pasar de donde estaban las bandas viejas (+1 m)
  const nx=-uz,nz=ux;let p0=-1e9,p1=1e9;for(const q of C.pts){const o=(q[0]-C.cx)*nx+(q[1]-C.cz)*nz;p0=Math.max(p0,o);p1=Math.min(p1,o)}
  const lim0=p0+ZEB_W/2+1*U,lim1=-p1+ZEB_W/2+1*U;let e0=0,e1=0;const st=.25*U;
  for(;e0<lim0;e0+=st){const yy=R.alt(C.cx+nx*(e0+st),C.cz+nz*(e0+st),y);if(isNaN(yy)||Math.abs(yy-y)>.02)break}
  for(;e1<lim1;e1+=st){const yy=R.alt(C.cx-nx*(e1+st),C.cz-nz*(e1+st),y);if(isNaN(yy)||Math.abs(yy-y)>.02)break}
  e0=Math.min(e0,lim0-.8*U);e1=Math.min(e1,lim1-.8*U);
  if(e0+e1<3*U)continue;
  ceb.push({wi:best[0],s,cx:C.cx,cz:C.cz,ux,uz,e0,e1,y,ids:C.ids})}
 // pasos de cebra repetidos (dos grupos de bandas del mismo paso): se juntan
 for(let i=0;i<ceb.length;i++){const A=ceb[i];if(!A)continue;for(let j=i+1;j<ceb.length;j++){const B=ceb[j];if(!B||Math.abs(A.ux*B.ux+A.uz*B.uz)<.95)continue;
  const nx=-A.uz,nz=A.ux;const ob=(B.cx-A.cx)*nx+(B.cz-A.cz)*nz,lon=(B.cx-A.cx)*A.ux+(B.cz-A.cz)*A.uz;if(Math.abs(lon)>ZEB_L*.9)continue;
  if(ob-B.e1>A.e0+1*U||ob+B.e0<-A.e1-1*U)continue;const a0=Math.max(A.e0,ob+B.e0),a1=Math.max(A.e1,-ob+B.e1);
  A.e0=a0;A.e1=a1;A.ids=A.ids.concat(B.ids);ceb[j]=null}}
 for(let i=ceb.length-1;i>=0;i--)if(!ceb[i])ceb.splice(i,1);
 // las cebras de cada calle: tramos sin líneas longitudinales y la detención antes de la cebra
 // cebras cerca de cada calle (s: posición a lo largo de esa calle)
 const cebW=new Map();
 for(const c of ceb){const r=Math.max(c.e0,c.e1)+.1;
  for(let wi=0;wi<info.length;wi++){const I=info[wi];if(!I.ok)continue;const bb=I.w.bb;if(c.cx<bb[0]-r||c.cx>bb[2]+r||c.cz<bb[1]-r||c.cz>bb[3]+r)continue;
   const p=I.w.p;let bd=1e9,bs=0;for(let i=1;i<p.length;i++){const a=p[i-1],b=p[i];const dx=b[0]-a[0],dz=b[1]-a[1],l=Math.hypot(dx,dz)||1e-9;let t=((c.cx-a[0])*dx+(c.cz-a[1])*dz)/(l*l);t=Math.max(0,Math.min(1,t));
    const d=Math.hypot(a[0]+dx*t-c.cx,a[1]+dz*t-c.cz);if(d<bd){bd=d;bs=I.P.a[i-1]+t*l}}
   // la calle pasa por el paso: su eje cae dentro del ancho de la cebra y va más o menos en su dirección
   const q=I.P.en(bs);if(Math.abs(q[2]*c.ux+q[3]*c.uz)<.8)continue;const lat=(q[0]-c.cx)*(-c.uz)+(q[1]-c.cz)*c.ux;
   if(lat>c.e0+1*U||lat<-c.e1-1*U||bd>Math.max(c.e0,c.e1)+1*U)continue;
   let L=cebW.get(wi);if(!L)cebW.set(wi,L=[]);L.push({s:bs})}}
 await pausa();

 // ---- geometría
 const rects=[];let yr=NaN;
 const alt=(x,z)=>{const y=R.alt(x,z,yr);if(!isNaN(y))yr=y;return y};
 // rectángulo de a a b (eje) con ancho w: [ax,ay,az,bx,by,bz,w]
 const rect=(ax,az,bx,bz,w)=>{const ya=alt(ax,az),yb=alt(bx,bz);if(isNaN(ya)||isNaN(yb))return false;
  // que no se hunda en el asfalto si hay un cambio de pendiente a medio camino
  const ym=alt((ax+bx)/2,(az+bz)/2);let up=0;if(!isNaN(ym))up=Math.max(0,ym-(ya+yb)/2);
  rects.push(ax,ya+up,az,bx,yb+up,bz,w);return true};
 // tira a lo largo del eje, desplazada «o» a la izquierda, de s0 a s1, ancho w: tramos rectos entre los vértices del eje
 const tira=(P,o,s0,s1,w)=>{if(s1-s0<.2*U)return;const ss=[s0];for(const a of P.a)if(a>s0+.3*U&&a<s1-.3*U)ss.push(a);ss.push(s1);
  const S=[ss[0]];for(let i=1;i<ss.length;i++){const d=ss[i]-ss[i-1],n=Math.ceil(d/(6*U));for(let k=1;k<=n;k++)S.push(ss[i-1]+d*k/n)}
  let prev=null;for(const s of S){const[x,z,dx,dz]=P.nrm(s);const q=[x-dz*o,z+dx*o];if(prev)rect(prev[0],prev[1],q[0],q[1],w);prev=q}};
 const libre=(I,wi,s)=>{for(const f of I.flare)if(s>f[0]&&s<f[1])return false;const L=cebW.get(wi);if(!L)return true;for(const c of L)if(Math.abs(s-c.s)<ZEB_L/2+1.2*U)return false;return true};
 const linea=(I,wi,o,s0,s1,w,disc)=>{ // continua o discontinua, saltando los pasos de cebra
  if(disc){const per=DASH+GAP;let s=s0+((Math.floor(s0/per)+1)*per-s0)%per;            // trazos fijos al eje, iguales en todas las líneas
   for(;s<s1;s+=per){const a=Math.max(s0,s),b=Math.min(s1,s+DASH);if(b-a<DASH*.5)continue;if(libre(I,wi,a)&&libre(I,wi,b))tira(I.P,o,a,b,w)}}
  else{let a=s0;const st=.5*U;for(let s=s0;s<=s1;s+=st){if(!libre(I,wi,s)){if(s-a>1*U)tira(I.P,o,a,s-st,w);a=s+st}}if(s1-a>1*U)tira(I.P,o,a,s1,w)}};
 t0=performance.now();
 for(let wi=0;wi<info.length;wi++){const I=info[wi];if(!I.ok)continue;const w=I.w,P=I.P,rk=RANK[w.c]||0;yr=NaN;
  const s0=I.cut[0],s1=P.L-I.cut[1];if(s1-s0<2*U)continue;
  const W=I.W,c=I.off,doble=!w.u;const sentido=w.u?(w.u<0?-1:1):1;
  if(doble){const porLado=Math.max(1,Math.round(W/2/LANE));
   if(W>=5.6*U){linea(I,wi,c,s0,s1,LW,rk<2);                                 // eje central
    for(let k=1;k<porLado;k++){const o=W/2*k/porLado;linea(I,wi,c+o,s0,s1,LW,true);linea(I,wi,c-o,s0,s1,LW,true)}}}
  else{const n=Math.max(1,Math.min(5,Math.round(W/LANE)));
   for(let k=1;k<n;k++)linea(I,wi,c-W/2+W*k/n,s0,s1,LW,true)}
  // detención en las entradas a los cruces (carril de entrada: a la derecha según se llega)
  for(const ext of [0,1]){if(!I.stop[ext])continue;const llega=ext===1?sentido>0:sentido<0;if(w.u&&!llega)continue;
   let s=ext?s1-LST/2:s0+LST/2;const L=cebW.get(wi);
   if(L)for(const cz of L){const d=ext?(P.L-cz.s):cz.s;const cut=ext?I.cut[1]:I.cut[0];if(d>cut-1*U&&d<cut+12*U)s=ext?cz.s-ZEB_L/2-1.2*U:cz.s+ZEB_L/2+1.2*U}
   if(!libre(I,wi,s)&&!(L&&L.some(q=>Math.abs(q.s-s)<ZEB_L)))continue;
   const[x,z,dx,dz]=P.nrm(s);const nx=-dz,nz=dx;
   let a,b;if(doble){const der=ext?-1:1;a=c;b=c+der*(W/2-.3*U)}else{a=c-W/2+.3*U;b=c+W/2-.3*U}
   if(a>b){const t=a;a=b;b=t}
   if(I.stop[ext]===2)rect(x+nx*a,z+nz*a,x+nx*b,z+nz*b,LST);
   else{const D=.6*U;for(let o=a;o<b;o+=2*D){const o2=Math.min(b,o+D);rect(x+nx*o,z+nz*o,x+nx*o2,z+nz*o2,LST)}}}
  if(performance.now()-t0>8){await pausa();t0=performance.now()}}
 // pasos de cebra nuevos
 for(const c of ceb){yr=c.y;const nx=-c.uz,nz=c.ux;const tot=c.e0+c.e1;const n=Math.max(2,Math.floor((tot+ZEB_G)/(ZEB_W+ZEB_G)));
  const marg=(tot-(n*ZEB_W+(n-1)*ZEB_G))/2;const hx=c.ux*ZEB_L/2,hz=c.uz*ZEB_L/2;
  for(let k=0;k<n;k++){const o=c.e0-marg-k*(ZEB_W+ZEB_G)-ZEB_W/2;const x=c.cx+nx*o,z=c.cz+nz*o;rect(x-hx,z-hz,x+hx,z+hz,ZEB_W)}}
 // ---- marcas viejas que no son de calle: se quedan (lejos de cualquier eje o fuera de la calzada)
 const quitar=new Set();for(const c of ceb)for(const id of c.ids)quitar.add(id);
 const keep=[];
 if(viejas&&viejas.comps)for(const c of viejas.comps){if(quitar.has(c.id))continue;
  const m=RS.mas(c.cx,c.cz);if(m.d>.3){keep.push(c.id);continue}              // lejos de las calles: aparcamientos, muelles...
  if(!isNaN(R.alt(c.cx,c.cz,NaN)))continue;                                   // sobre el asfalto de una calle: la rehacemos nosotros
  const I=info[m.b[0]];if(I&&I.ok&&m.d<Math.max(I.wl,I.wr)+1*U)continue;      // fuera de la calzada pero pegada al eje: sobra
  keep.push(c.id)}
 return {rects:new Float32Array(rects),keep,n:{calles:info.filter(i=>i.ok).length,cebras:ceb.length,viejas:keep.length}}}

// componentes conexas de la malla vieja de marcas (en coordenadas del mundo)
function compsViejas(P,I){const n=P.length/3,par=new Int32Array(n);for(let i=0;i<n;i++)par[i]=i;
 const f=x=>{while(par[x]!==x){par[x]=par[par[x]];x=par[x]}return x};
 for(let t=0;t<I.length;t+=3){const a=f(I[t]),b=f(I[t+1]),c=f(I[t+2]);par[b]=a;par[f(c)]=a}
 const M=new Map();for(let t=0;t<I.length;t+=3){const r=f(I[t]);let L=M.get(r);if(!L)M.set(r,L=[]);L.push(t)}
 const comps=[];let id=0;
 for(const[,ts]of M){const vs=new Set();for(const t of ts){vs.add(I[t]);vs.add(I[t+1]);vs.add(I[t+2])}
  let cx=0,cz=0;for(const v of vs){cx+=P[v*3];cz+=P[v*3+2]}cx/=vs.size;cz/=vs.size;
  let sxx=0,szz=0,sxz=0;for(const v of vs){const x=P[v*3]-cx,z=P[v*3+2]-cz;sxx+=x*x;szz+=z*z;sxz+=x*z}
  const th=.5*Math.atan2(2*sxz,sxx-szz),ux=Math.cos(th),uz=Math.sin(th);let a0=1e9,a1=-1e9,b0=1e9,b1=-1e9;
  for(const v of vs){const x=P[v*3]-cx,z=P[v*3+2]-cz,a=x*ux+z*uz,b=-x*uz+z*ux;a0=Math.min(a0,a);a1=Math.max(a1,a);b0=Math.min(b0,b);b1=Math.max(b1,b)}
  let A=0;for(const t of ts){const o=I[t]*3,p=I[t+1]*3,q=I[t+2]*3;A+=Math.abs((P[p]-P[o])*(P[q+2]-P[o+2])-(P[q]-P[o])*(P[p+2]-P[o+2]))/2}
  let L=a1-a0,W=b1-b0,uxx=ux,uzz=uz;if(W>L){const t=L;L=W;W=t;uxx=-uz;uzz=ux}
  comps.push({id:id++,ts,cx,cz,L,W,ux:uxx,uz:uzz,nt:ts.length,fill:A/Math.max(L*W,1e-12)})}
 return comps}

// ---- archivo horneado <zona>_lineas.bin (herramientas/lineas_hornear.mjs)
// cabecera: 'LSR1', nº de rectángulos, nº de triángulos conservados, origen x,y,z (float32)
// rectángulo (18 bytes): ax,az int32 (1e-5 u) · ay int16 (1e-4 u) · dx,dz int16 (1e-5 u) · by int16 (1e-4 u) · ancho uint16 (1e-6 u)
// conservados: 9 float32 por triángulo (respecto al origen)
const MAGIA=0x3152534C,VER='1';
function codifica(rects,keep){let rr=[];for(let i=0;i<rects.length;i+=7){const ax=rects[i],ay=rects[i+1],az=rects[i+2],bx=rects[i+3],by=rects[i+4],bz=rects[i+5],w=rects[i+6];
  const n=Math.max(1,Math.ceil(Math.max(Math.abs(bx-ax),Math.abs(bz-az))/.3));for(let k=0;k<n;k++){const t0=k/n,t1=(k+1)/n;rr.push(ax+(bx-ax)*t0,ay+(by-ay)*t0,az+(bz-az)*t0,ax+(bx-ax)*t1,ay+(by-ay)*t1,az+(bz-az)*t1,w)}}
 let ox=1e9,oy=1e9,oz=1e9,y1=-1e9;for(let i=0;i<rr.length;i+=7){ox=Math.min(ox,rr[i],rr[i+3]);oz=Math.min(oz,rr[i+2],rr[i+5]);oy=Math.min(oy,rr[i+1],rr[i+4]);y1=Math.max(y1,rr[i+1],rr[i+4])}
 for(let i=0;i<keep.length;i+=3){ox=Math.min(ox,keep[i]);oy=Math.min(oy,keep[i+1]);oz=Math.min(oz,keep[i+2])}
 if(ox>1e8){ox=oy=oz=0}const oym=oy+(y1>-1e8?Math.min(3,(y1-oy)/2):0);
 const nR=rr.length/7,nK=keep.length/9,buf=new ArrayBuffer(24+nR*18+nK*36),dv=new DataView(buf);
 dv.setUint32(0,MAGIA,true);dv.setUint32(4,nR,true);dv.setUint32(8,nK,true);dv.setFloat32(12,ox,true);dv.setFloat32(16,oym,true);dv.setFloat32(20,oz,true);
 const fx=dv.getFloat32(12,true),fy=dv.getFloat32(16,true),fz=dv.getFloat32(20,true);let o=24;const cl=v=>Math.max(-32768,Math.min(32767,Math.round(v)));
 for(let i=0;i<rr.length;i+=7){const ax=Math.round((rr[i]-fx)*1e5),az=Math.round((rr[i+2]-fz)*1e5);dv.setInt32(o,ax,true);dv.setInt32(o+4,az,true);dv.setInt16(o+8,cl((rr[i+1]-fy)*1e4),true);
  dv.setInt16(o+10,cl((rr[i+3]-fx)*1e5-ax),true);dv.setInt16(o+12,cl((rr[i+5]-fz)*1e5-az),true);dv.setInt16(o+14,cl((rr[i+4]-fy)*1e4),true);dv.setUint16(o+16,Math.min(65535,Math.round(rr[i+6]*1e6)),true);o+=18}
 for(let i=0;i<keep.length;i+=3){dv.setFloat32(o,keep[i]-fx,true);dv.setFloat32(o+4,keep[i+1]-fy,true);dv.setFloat32(o+8,keep[i+2]-fz,true);o+=12}
 return buf}
// devuelve posiciones (mundo) e índices de la malla nueva
function decodifica(buf){const dv=new DataView(buf);if(dv.getUint32(0,true)!==MAGIA)return null;const nR=dv.getUint32(4,true),nK=dv.getUint32(8,true);
 const ox=dv.getFloat32(12,true),oy=dv.getFloat32(16,true),oz=dv.getFloat32(20,true);
 const pos=new Float32Array(nR*12+nK*9),idx=new Uint32Array(nR*6+nK*3);let o=24,p=0,q=0;
 for(let r=0;r<nR;r++){const ax=dv.getInt32(o,true)*1e-5,az=dv.getInt32(o+4,true)*1e-5,ay=dv.getInt16(o+8,true)*1e-4,dx=dv.getInt16(o+10,true)*1e-5,dz=dv.getInt16(o+12,true)*1e-5,by=dv.getInt16(o+14,true)*1e-4,w=dv.getUint16(o+16,true)*1e-6;o+=18;
  const l=Math.hypot(dx,dz)||1e-9,nx=-dz/l*w/2,nz=dx/l*w/2,v=p/3;
  pos[p++]=ox+ax+nx;pos[p++]=oy+ay;pos[p++]=oz+az+nz; pos[p++]=ox+ax+dx+nx;pos[p++]=oy+by;pos[p++]=oz+az+dz+nz;
  pos[p++]=ox+ax+dx-nx;pos[p++]=oy+by;pos[p++]=oz+az+dz-nz; pos[p++]=ox+ax-nx;pos[p++]=oy+ay;pos[p++]=oz+az-nz;
  // con la cara hacia arriba (sentido antihorario visto desde arriba)
  if(nx*dz-nz*dx<0){idx[q++]=v;idx[q++]=v+1;idx[q++]=v+2;idx[q++]=v;idx[q++]=v+2;idx[q++]=v+3}else{idx[q++]=v;idx[q++]=v+2;idx[q++]=v+1;idx[q++]=v;idx[q++]=v+3;idx[q++]=v+2}}
 for(let k=0;k<nK;k++){const v=p/3;for(let j=0;j<3;j++){pos[p++]=ox+dv.getFloat32(o,true);pos[p++]=oy+dv.getFloat32(o+4,true);pos[p++]=oz+dv.getFloat32(o+8,true);o+=12}
  const ax=pos[v*3],az=pos[v*3+2],bx=pos[v*3+3],bz=pos[v*3+5],cx=pos[v*3+6],cz=pos[v*3+8];
  if((bz-az)*(cx-ax)-(bx-ax)*(cz-az)>0){idx[q++]=v;idx[q++]=v+1;idx[q++]=v+2}else{idx[q++]=v;idx[q++]=v+2;idx[q++]=v+1}}
 return {pos,idx}}
const PREL={};
function lineasPre(id){if(window.__LINEAS_VIEJAS||PREL[id])return;PREL[id]=fetch(id+'_lineas.bin?v='+VER).then(r=>r.ok?r.arrayBuffer():null).catch(()=>null)}
// cambia la malla «lineas» de una zona recién cargada (antes de que la vean el móvil, los lotes o las sombras)
async function lineasRectas(root,id){if(window.__LINEAS_VIEJAS)return;
 try{lineasPre(id);const buf=await PREL[id];delete PREL[id];if(!buf)return;const d=decodifica(buf);if(!d)return;
  let lin=null;root.traverse(o=>{if(!lin&&o.isMesh&&/^lineas/.test(o.name))lin=o});if(!lin)return;
  root.updateMatrixWorld(true);const inv=lin.matrixWorld.clone().invert(),e=inv.elements,P=d.pos;
  for(let i=0;i<P.length;i+=3){const x=P[i],y=P[i+1],z=P[i+2];P[i]=e[0]*x+e[4]*y+e[8]*z+e[12];P[i+1]=e[1]*x+e[5]*y+e[9]*z+e[13];P[i+2]=e[2]*x+e[6]*y+e[10]*z+e[14]}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(P,3));g.setIndex(new THREE.BufferAttribute(d.idx,1));
  const old=lin.geometry;if(old.attributes.normal){const N=new Float32Array(P.length);for(let i=1;i<N.length;i+=3)N[i]=1;g.setAttribute('normal',new THREE.BufferAttribute(N,3))}
  g.computeBoundingSphere();g.computeBoundingBox();lin.geometry=g;try{old.dispose()}catch(e){}lin.userData.lineasRectas=1}
 catch(e){console.warn('lineasRectas',e)}}
window.lineasPre=lineasPre;
window.lineasRectas=lineasRectas;
window.__lineasConstruir=construir;window.__lineasComps=compsViejas;window.__lineasCodifica=codifica;window.__lineasDecodifica=decodifica;
})();
