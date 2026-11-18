import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= CASA DAS ARTES (Policarpo Sanz) =================
# Planta tomada del Catastro (las 4 parcelas del edificio). Google Earth solo como referencia de estilo:
# granito gris, chaflán con gran puerta y ventanal de dos plantas, remate sobre la cornisa, balaustrada,
# buhardillas en el tejado de teja y lucernario de cristal sobre el patio. Modelo procedural propio.
r("function subePaso(){",r"""const CASA={P:[[89.952,17.565],[90.124,17.548],[90.13,17.609],[90.469,17.543],[90.47,17.79],[90.555,17.765],[90.56,17.919],[90.139,17.979],[89.965,17.842]],
 T:['p','p','p','p','p','p','f','c','f'],CAD:[6,7,8,0],LUZ:[90.29,17.70],hecho:0};
function pipC(x,z,P){let c=false;for(let i=0,j=P.length-1;i<P.length;j=i++){const a=P[i],b=P[j];if((a[1]>z)!=(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])c=!c}return c}
function dSegC(x,z,P){let m=1e9;for(let i=0;i<P.length;i++){const a=P[i],b=P[(i+1)%P.length],dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));m=Math.min(m,Math.hypot(x-a[0]-t*dx,z-a[1]-t*dz))}return m}
const enCasa=(x,z,m)=>pipC(x,z,CASA.P)||dSegC(x,z,CASA.P)<m;
function casaOculta(rt){const P=CASA.P,a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();const st={k:0,minY:1e9,maxY:-1e9};
 rt.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||o.userData.casa||GROUND.includes(o))return;const g=o.geometry,ix=g.index,pos=g.attributes.position;if(!ix||!pos)return;
  if(!g.boundingBox)g.computeBoundingBox();o.updateMatrixWorld(true);const bb=g.boundingBox.clone().applyMatrix4(o.matrixWorld);if(bb.max.x<89.9||bb.min.x>90.62||bb.max.z<17.5||bb.min.z>18.03)return;
  const mw=o.matrixWorld;let ch=0;
  for(let t=0;t<ix.count;t+=3){a.fromBufferAttribute(pos,ix.getX(t)).applyMatrix4(mw);b.fromBufferAttribute(pos,ix.getX(t+1)).applyMatrix4(mw);c.fromBufferAttribute(pos,ix.getX(t+2)).applyMatrix4(mw);
   const mx=(a.x+b.x+c.x)/3,mz=(a.z+b.z+c.z)/3;
   if(pipC(mx,mz,P)&&dSegC(mx,mz,P)>.01){const i0=ix.getX(t);ix.setX(t+1,i0);ix.setX(t+2,i0);ch++;st.minY=Math.min(st.minY,a.y,b.y,c.y);st.maxY=Math.max(st.maxY,a.y,b.y,c.y)}}
  if(ch){ix.needsUpdate=true;st.k+=ch}});
 return st}
function casaCanvas(tipo){const W=tipo==='c'?256:128,HH=1024,cv=document.createElement('canvas');cv.width=W;cv.height=HH;const x=cv.getContext('2d');
 let sd=tipo.charCodeAt(0)*977+13;const rn=()=>(sd=(sd*16807)%2147483647)/2147483647;const Y=f=>Math.round(f*HH);
 const base=tipo==='p'?150:166;x.fillStyle='#8a877f';x.fillRect(0,0,W,HH);
 for(let y=0;y<HH;y+=16){const o=((y/16)&1)*23;for(let xx=-o;xx<W;xx+=46){const v=base+(rn()*20|0);x.fillStyle=`rgb(${v},${v-1},${v-8})`;x.fillRect(xx+1,y+1,44,14)}}
 if(tipo==='p')return cv;
 const pie='#c9c5b9',vid='#252b32',mar='#e2dfd7';
 const win=(cx,y0,y1,w,ped,balc,arco)=>{x.fillStyle=pie;x.fillRect(cx-w/2-6,y0-6-(arco?w/2:0),w+12,y1-y0+12+(arco?w/2:0));
  x.fillStyle=vid;x.beginPath();if(arco){x.moveTo(cx-w/2,y1);x.lineTo(cx-w/2,y0);x.arc(cx,y0,w/2,Math.PI,0);x.lineTo(cx+w/2,y1)}else x.rect(cx-w/2,y0,w,y1-y0);x.fill();
  x.fillStyle=mar;x.fillRect(cx-1.5,y0-(arco?w/2:0),3,y1-y0+(arco?w/2:0));x.fillRect(cx-w/2,y0+(y1-y0)*.32,w,3);x.fillRect(cx-w/2,y1-3,w,3);x.fillRect(cx-w/2,y0,3,y1-y0);x.fillRect(cx+w/2-3,y0,3,y1-y0);
  if(ped){x.fillStyle=pie;x.beginPath();x.moveTo(cx-w/2-11,y0-7);x.lineTo(cx+w/2+11,y0-7);x.lineTo(cx,y0-28);x.closePath();x.fill();x.fillStyle='rgba(60,58,52,.55)';x.fillRect(cx-w/2-11,y0-7,w+22,3)}
  if(balc){x.fillStyle='rgba(50,48,44,.6)';x.fillRect(cx-w/2-12,y1+12,w+24,5);x.fillStyle='#bdb9ae';x.fillRect(cx-w/2-12,y1+5,w+24,7);x.fillStyle='#24262a';x.fillRect(cx-w/2-10,y1-16,w+20,2);for(let k=cx-w/2-10;k<=cx+w/2+10;k+=5)x.fillRect(k,y1-16,1.5,21)}};
 const banda=(y,h,c)=>{x.fillStyle=c||'#c3bfb4';x.fillRect(0,y,W,h);x.fillStyle='rgba(55,53,48,.45)';x.fillRect(0,y+h,W,3)};
 x.fillStyle='#bfbbb0';x.fillRect(0,0,W,Y(.065));
 banda(Y(.27),8);banda(Y(.49),8);
 // planta baja almohadillada
 x.fillStyle='#a19e95';x.fillRect(0,Y(.765),W,HH-Y(.765));for(let y=Y(.765);y<HH;y+=22){x.fillStyle='#625f58';x.fillRect(0,y,W,3);x.fillStyle='#b4b1a7';x.fillRect(0,y+3,W,2)}
 banda(Y(.74),Y(.025),'#c7c3b8');
 const pil=(x0,w)=>{x.fillStyle='#bab6ab';x.fillRect(x0,Y(.065),w,Y(.74)-Y(.065));x.fillStyle='rgba(60,58,52,.35)';x.fillRect(x0+w-3,Y(.065),3,Y(.74)-Y(.065));x.fillStyle='#cfcbc0';x.fillRect(x0,Y(.065),w,10)};
 if(tipo==='f'){pil(0,9);pil(W-9,9);
  win(64,Y(.10),Y(.22),40,false,false);win(64,Y(.31),Y(.455),42,false,false);win(64,Y(.53),Y(.69),44,true,true);
  win(64,Y(.83),Y(.975),56,false,false,true);x.fillStyle='#d1cdc1';x.fillRect(60,Y(.83)-40,8,12)}
 else{pil(0,34);pil(W-34,34);for(const c0 of [8,W-26]){x.fillStyle='#d3cfc4';x.fillRect(c0,Y(.08),16,Y(.73)-Y(.08));x.fillStyle='rgba(60,58,52,.4)';x.fillRect(c0+12,Y(.08),4,Y(.73)-Y(.08))}
  for(const cx of [92,128,164])win(cx,Y(.10),Y(.22),22,false,false);
  win(128,Y(.33),Y(.69),68,false,true,true);x.fillStyle=mar;x.fillRect(106,Y(.33),3,Y(.69)-Y(.33));x.fillRect(147,Y(.33),3,Y(.69)-Y(.33));x.fillRect(94,Y(.5),68,4);
  x.fillStyle=pie;x.fillRect(80,Y(.79)-50,96,Y(.985)-Y(.79)+50);x.fillStyle='#3a2a1f';x.beginPath();x.moveTo(86,Y(.985));x.lineTo(86,Y(.79));x.arc(128,Y(.79),42,Math.PI,0);x.lineTo(170,Y(.985));x.fill();
  x.fillStyle='#2a1e16';for(const px of [92,130])for(const py of [Y(.81),Y(.9)])x.fillRect(px,py,34,Y(.07));x.fillStyle='#d9d5ca';x.fillRect(122,Y(.79)-50,12,16)}
 x.fillStyle='#7d7a71';x.fillRect(0,Y(.985),W,HH-Y(.985));return cv}
function casaTex(t){const T=new THREE.CanvasTexture(casaCanvas(t));T.colorSpace=THREE.SRGBColorSpace;T.wrapS=THREE.RepeatWrapping;T.wrapT=t==='p'?THREE.RepeatWrapping:THREE.ClampToEdgeWrapping;T.anisotropy=4;return T}
function casaArtes(rt){const st=casaOculta(rt);CASA.oc=(CASA.oc||0)+st.k;let en=CASA.G;while(en&&en.parent)en=en.parent;if(!st.k||en===scene)return;const P=CASA.P,N=P.length;
 const g0=(x,z)=>{const v=sueloRap(x,z);return v==null?(st.minY<1e8?st.minY:0):v};
 const E=[];for(let i=0;i<N;i++){const a=P[i],b=P[(i+1)%N];const dx=b[0]-a[0],dz=b[1]-a[1],L=Math.hypot(dx,dz);let nx=dz/L,nz=-dx/L;if(pipC((a[0]+b[0])/2+nx*.01,(a[1]+b[1])/2+nz*.01,P)){nx=-nx;nz=-nz}
  E.push({a,b,dx:dx/L,dz:dz/L,L,nx,nz,ga:g0(a[0]+nx*.03,a[1]+nz*.03),gb:g0(b[0]+nx*.03,b[1]+nz*.03),t:CASA.T[i],ang:Math.atan2(-dz,dx)})}
 let gmin=1e9,gmax=-1e9;for(const e of E)if(e.t!=='p'){gmin=Math.min(gmin,e.ga,e.gb);gmax=Math.max(gmax,e.ga,e.gb)}
 const T=gmax+.29;
 const OUT=.004,BL=()=>({p:[],n:[],u:[]});
 const tri=(B,p,q,r_,up,uq,ur,h)=>{const ux=q[0]-p[0],uy=q[1]-p[1],uz=q[2]-p[2],vx=r_[0]-p[0],vy=r_[1]-p[1],vz=r_[2]-p[2];let cx=uy*vz-uz*vy,cy=uz*vx-ux*vz,cz=ux*vy-uy*vx;
  if(cx*h[0]+cy*h[1]+cz*h[2]<0){[q,r_]=[r_,q];[uq,ur]=[ur,uq];cx=-cx;cy=-cy;cz=-cz}const l=Math.hypot(cx,cy,cz)||1;B.p.push(...p,...q,...r_);for(let k=0;k<3;k++)B.n.push(cx/l,cy/l,cz/l);B.u.push(...up,...uq,...ur)};
 const quad=(B,a,b,c,d,ua,ub,uc,ud,h)=>{tri(B,a,b,c,ua,ub,uc,h);tri(B,a,c,d,ua,uc,ud,h)};
 const geo=B=>{const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(B.p,3));g.setAttribute('normal',new THREE.Float32BufferAttribute(B.n,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(B.u,2));return g};
 const W={f:BL(),c:BL(),p:BL()};
 for(const e of E){const A=[e.a[0]+e.nx*OUT,e.a[1]+e.nz*OUT],Bp=[e.b[0]+e.nx*OUT,e.b[1]+e.nz*OUT],ya=e.ga-.08,yb=e.gb-.08,H=e.H=T-Math.min(e.ga,e.gb);
  const U=e.t==='c'?1:e.t==='f'?(e.nb=Math.max(1,Math.round(e.L/.052))):e.L/.09,va=1-(T-ya)/H,vb=1-(T-yb)/H;
  quad(W[e.t],[A[0],T,A[1]],[Bp[0],T,Bp[1]],[Bp[0],yb,Bp[1]],[A[0],ya,A[1]],[0,1],[U,1],[U,vb],[0,va],[e.nx,0,e.nz])}
 const ORN=[],IRON=[],BLAN=[],VENT=[],TEJ=BL();
 const bx=(L,cx,cy,cz,w,h,d,ang)=>{const g=new THREE.BoxGeometry(w,h,d);g.rotateY(ang);g.translate(cx,cy,cz);L.push(g.toNonIndexed())};
 const cil=(L,cx,cy,cz,r1,h,sg)=>{const g=new THREE.CylinderGeometry(r1,r1,h,sg||8);g.translate(cx,cy,cz);L.push(g.toNonIndexed())};
 for(const e of E){if(e.t==='p')continue;const at=(s,o)=>[e.a[0]+e.dx*s+e.nx*o,e.a[1]+e.dz*s+e.nz*o],m=at(e.L/2,0),H=e.H,gy=s=>e.ga+(e.gb-e.ga)*s/e.L;
  let q=at(e.L/2,OUT+.009);bx(ORN,q[0],T-.008,q[1],e.L+.02,.016,.018,e.ang);q=at(e.L/2,OUT+.005);bx(ORN,q[0],T-.022,q[1],e.L,.006,.01,e.ang);
  q=at(e.L/2,OUT+.004);bx(ORN,q[0],T-.74*H,q[1],e.L,.008,.008,e.ang);
  // balaustrada
  q=at(e.L/2,OUT-.002);bx(ORN,q[0],T+.003,q[1],e.L,.006,.012,e.ang);bx(ORN,q[0],T+.023,q[1],e.L,.005,.013,e.ang);
  const nbal=Math.floor(e.L/.008);for(let k=1;k<nbal;k++){const p=at(k*e.L/nbal,OUT-.002);cil(ORN,p[0],T+.013,p[1],.0026,.015,6)}
  if(e.t==='f'){const nb=e.nb,w=e.L/nb;for(let k=0;k<=nb;k++){const p=at(k*w,OUT-.002);bx(ORN,p[0],T+.014,p[1],.009,.026,.014,e.ang)}
   for(let k=0;k<nb;k++){let p=at((k+.5)*w,OUT+.007);bx(ORN,p[0],T-.70*H-.001,p[1],.032,.004,.014,e.ang);p=at((k+.5)*w,OUT+.0135);bx(IRON,p[0],T-.70*H+.007,p[1],.032,.012,.0012,e.ang);
    if(k%2===1){const d=at((k+.5)*w,-.05);bx(BLAN,d[0],T+.045,d[1],.024,.034,.03,e.ang);const v=at((k+.5)*w,-.034);bx(VENT,v[0],T+.044,v[1],.013,.02,.002,e.ang);
     const pr=new THREE.CylinderGeometry(.019,.019,.034,3);pr.rotateX(-Math.PI/2);pr.scale(1,.55,1);pr.rotateY(e.ang);pr.translate(d[0],T+.069,d[1]);const nz=pr.toNonIndexed();nz.deleteAttribute('uv');nz.setAttribute('uv',new THREE.Float32BufferAttribute(new Float32Array(nz.attributes.position.count*2),2));ORN.push.call(TEJ.ex||(TEJ.ex=[]),nz)}}}
  else{// chaflán: remate, frontón curvo, columnas de la puerta
   let p=at(e.L/2,OUT-.012);bx(ORN,p[0],T+.04,p[1],e.L*.62,.08,.03,e.ang);
   const fr=new THREE.CylinderGeometry(e.L*.28,e.L*.28,.03,28);fr.rotateX(Math.PI/2);fr.scale(1,.32,1);fr.rotateY(e.ang);fr.translate(p[0],T+.08,p[1]);ORN.push(fr.toNonIndexed());
   p=at(e.L/2,OUT+.004);bx(ORN,p[0],T+.083,p[1],e.L*.66,.008,.04,e.ang);const s0=new THREE.SphereGeometry(.009,10,8);s0.translate(p[0],T+.08+e.L*.28*.32+.006,p[1]);ORN.push(s0.toNonIndexed());
   for(const fs of [.17,.83]){const s=fs*e.L,c=at(s,OUT+.012),g1=gy(s)-.02,y1=T-.74*H;cil(ORN,c[0],(g1+y1)/2,c[1],.0075,y1-g1,12);bx(ORN,c[0],y1-.004,c[1],.022,.008,.022,e.ang);bx(ORN,c[0],g1+.02,c[1],.02,.012,.02,e.ang)}
   // balcón del gran ventanal
   p=at(e.L/2,OUT+.009);bx(ORN,p[0],T-.70*H-.001,p[1],e.L*.4,.005,.018,e.ang);p=at(e.L/2,OUT+.017);bx(IRON,p[0],T-.70*H+.008,p[1],e.L*.4,.014,.0012,e.ang)}}
 // falsa mansarda de teja tras la balaustrada, sobre las fachadas a la calle
 const CH=CASA.CAD,ed=[];for(let k=0;k<CH.length-1;k++)ed.push(E[CH[k]]);
 const off=(k,d)=>{const v=P[CH[k]];let mx,mz;if(k===0){mx=-ed[0].nx;mz=-ed[0].nz}else if(k===CH.length-1){mx=-ed[k-1].nx;mz=-ed[k-1].nz}else{const m1=[-ed[k-1].nx,-ed[k-1].nz],m2=[-ed[k].nx,-ed[k].nz],dt=1+m1[0]*m2[0]+m1[1]*m2[1];mx=(m1[0]+m2[0])/dt;mz=(m1[1]+m2[1])/dt}return[v[0]+mx*d,v[1]+mz*d]};
 const y1=T+.003,y2=T+.075,ORNB=BL();
 for(let k=0;k<ed.length;k++){const a1=off(k,.022),b1=off(k+1,.022),a2=off(k,.09),b2=off(k+1,.09),e=ed[k],L=e.L*30;
  quad(TEJ,[a1[0],y1,a1[1]],[b1[0],y1,b1[1]],[b2[0],y2,b2[1]],[a2[0],y2,a2[1]],[0,0],[L,0],[L,2],[0,2],[e.nx,1.2,e.nz]);
  quad(ORNB,[a2[0],y2,a2[1]],[b2[0],y2,b2[1]],[b2[0],T,b2[1]],[a2[0],T,a2[1]],[0,0],[1,0],[1,1],[0,1],[-e.nx,0,-e.nz])}
 {const k0=0,kn=CH.length-1,e0=ed[0],en=ed[ed.length-1];let a=off(k0,.022),b=off(k0,.09);tri(ORNB,[a[0],y1,a[1]],[b[0],y2,b[1]],[b[0],T,b[1]],[0,0],[1,0],[1,1],[-e0.dx,0,-e0.dz]);
  a=off(kn,.022);b=off(kn,.09);tri(ORNB,[a[0],y1,a[1]],[b[0],y2,b[1]],[b[0],T,b[1]],[0,0],[1,0],[1,1],[en.dx,0,en.dz])}
 // cubierta plana (teja) y lucernario de cristal sobre el patio
 const sh=new THREE.Shape(P.map(p=>new THREE.Vector2(p[0],p[1])));const rg=new THREE.ShapeGeometry(sh);rg.rotateX(Math.PI/2);rg.translate(0,T+.001,0);
 const ang=E[6].ang,[lx,lz]=CASA.LUZ,VID=[];bx(ORN,lx,T+.007,lz,.135,.012,.105,ang);
 const vg=new THREE.CylinderGeometry(.35,.7,1,4,1);vg.rotateY(Math.PI/4);vg.scale(.12/.99,.05,.09/.99);vg.rotateY(ang);vg.translate(lx,T+.038,lz);
 const M=k=>new THREE.MeshStandardMaterial(k),mats={f:M({map:casaTex('f'),roughness:.88}),c:M({map:casaTex('c'),roughness:.88}),p:M({map:casaTex('p'),roughness:.92}),
  orn:M({color:0xbab7ae,roughness:.85}),iron:M({color:0x232528,roughness:.5,metalness:.5}),tej:M({color:0xa4513b,roughness:.82,side:THREE.DoubleSide}),blan:M({color:0xe6e2d8,roughness:.8}),
  vent:M({color:0x2a3036,roughness:.3,metalness:.3}),vid:M({color:0x9fb6c0,roughness:.12,metalness:.6,transparent:true,opacity:.82})};
 const G=new THREE.Group();G.name='casa_das_artes';rt.updateMatrixWorld(true);G.matrixAutoUpdate=false;G.matrix.copy(rt.matrixWorld).invert();
 const add=(g,m)=>{if(!g)return;const o=new THREE.Mesh(g,m);o.castShadow=o.receiveShadow=true;o.userData.casa=1;G.add(o)};
 for(const t of ['f','c','p'])if(W[t].p.length)add(geo(W[t]),mats[t]);
 const mg=L=>L.length?mergeGeometries(L.map(g=>{for(const k of Object.keys(g.attributes))if(!['position','normal','uv'].includes(k))g.deleteAttribute(k);if(!g.attributes.uv)g.setAttribute('uv',new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count*2),2));return g})):null;
 add(mg([...ORN,geo(ORNB)]),mats.orn);add(mg(IRON),mats.iron);add(mg([geo(TEJ),rg.toNonIndexed(),...(TEJ.ex||[])]),mats.tej);add(mg(BLAN),mats.blan);add(mg(VENT),mats.vent);
 const vgn=vg.toNonIndexed();add(vgn,mats.vid);const ln=new THREE.LineSegments(new THREE.EdgesGeometry(vg),new THREE.LineBasicMaterial({color:0x30363c}));G.add(ln);
 rt.add(G);CASA.G=G;window.__CASA={oculto:CASA.oc,T,gmin,gmax,piezas:G.children.length}}
function subePaso(){""")
r("function subeZonas(){for(const z of ZROOTS){const rt=z.root;","function subeZonas(){for(const z of ZROOTS){const rt=z.root;if(rt.parent&&!rt.userData.casaV){rt.userData.casaV=1;setTimeout(()=>{try{casaArtes(rt)}catch(e){console.warn('casaArtes',e)}},150)}")
r("const mx=(ax+bx)/2,my=(ay+by)/2;","const mx=(ax+bx)/2,my=(ay+by)/2;if(enCasa(mx,my,.03))continue;")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok casa')
