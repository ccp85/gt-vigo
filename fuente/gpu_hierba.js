// ---------- hierba de verdad (gpu_hierba.js, solo gpu.html) ----------
// Matas de 3 briznas sobre todos los céspedes (parques, jardines, medianas, taludes, dunas con hierba) alrededor de la
// cámara. Todo se calcula en la tarjeta gráfica: cada mata sale de una rejilla pegada al mundo (no "nada" al moverte),
// toma la altura y si hay césped debajo de una textura que se rehace al alejarte, se mece con el viento (ráfagas que
// recorren el parque) y se aparta al pasar el protagonista o el vehículo. Más alta y seca en las calvas, más corta en las
// franjas de corte; de lejos se desvanece. En el móvil (LITE) menos matas y más cerca.
const HB={on:false,tex:null,data:null,res:384,size:1.0,cx:1e9,cz:1e9,mesh:null,t:0,nT:-1,err:null};window.__HB=HB;
function hierbaMallas(x0,z0,x1,z1){const out=[];scene.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||!o.visible)return;const ms=[].concat(o.material);if(!ms.some(m=>m&&m.userData&&m.userData.ces))return;
  const g=o.geometry;if(!g||!g.attributes.position)return;if(!g.boundingBox)g.computeBoundingBox();o.updateMatrixWorld();const b=g.boundingBox.clone().applyMatrix4(o.matrixWorld);
  if(b.max.x<x0||b.min.x>x1||b.max.z<z0||b.min.z>z1)return;let p=o.parent,vis=true;while(p){if(!p.visible){vis=false;break}p=p.parent}if(vis)out.push(o)});return out}
// textura de la zona: r = altura del césped, g = hay césped (1) o no (0)
function hierbaTextura(cx,cz){const N=HB.res,S=HB.size,x0=cx-S/2,z0=cz-S/2,px=S/N;
 if(!HB.data){HB.data=new Uint16Array(N*N*4);HB.tex=new THREE.DataTexture(HB.data,N,N,THREE.RGBAFormat,THREE.HalfFloatType);HB.tex.magFilter=HB.tex.minFilter=THREE.LinearFilter;HB.tex.generateMipmaps=false}
 const H=new Float32Array(N*N).fill(-99),D=HB.data,h2=THREE.DataUtils.toHalfFloat,a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();let nt=0;
 for(const o of hierbaMallas(x0,z0,x0+S,z0+S)){const g=o.geometry,p=g.attributes.position,ix=g.index,cnt=ix?ix.count:p.count,mw=o.matrixWorld;
  for(let t=0;t+2<cnt;t+=3){a.fromBufferAttribute(p,ix?ix.getX(t):t).applyMatrix4(mw);b.fromBufferAttribute(p,ix?ix.getX(t+1):t+1).applyMatrix4(mw);c.fromBufferAttribute(p,ix?ix.getX(t+2):t+2).applyMatrix4(mw);
   const mnx=Math.min(a.x,b.x,c.x),mxx=Math.max(a.x,b.x,c.x),mnz=Math.min(a.z,b.z,c.z),mxz=Math.max(a.z,b.z,c.z);if(mxx<x0||mnx>x0+S||mxz<z0||mnz>z0+S)continue;
   const den=(b.z-c.z)*(a.x-c.x)+(c.x-b.x)*(a.z-c.z);if(Math.abs(den)<1e-14)continue;nt++;   // triángulos verticales (taludes de lado) no cuentan
   const i0=Math.max(0,Math.floor((mnx-x0)/px)),i1=Math.min(N-1,Math.ceil((mxx-x0)/px)),j0=Math.max(0,Math.floor((mnz-z0)/px)),j1=Math.min(N-1,Math.ceil((mxz-z0)/px));
   for(let j=j0;j<=j1;j++){const z=z0+(j+.5)*px;for(let i=i0;i<=i1;i++){const x=x0+(i+.5)*px;
     const l1=((b.z-c.z)*(x-c.x)+(c.x-b.x)*(z-c.z))/den,l2=((c.z-a.z)*(x-c.x)+(a.x-c.x)*(z-c.z))/den,l3=1-l1-l2;if(l1<-.02||l2<-.02||l3<-.02)continue;
     const y=l1*a.y+l2*b.y+l3*c.y,k=j*N+i;if(y>H[k])H[k]=y}}}}
 for(let k=0;k<N*N;k++){const ok=H[k]>-90;D[k*4]=h2(ok?H[k]:0);D[k*4+1]=h2(ok?1:0);D[k*4+2]=0;D[k*4+3]=h2(1)}
 HB.tex.needsUpdate=true;HB.cx=cx;HB.cz=cz;HB.uC.value.set(x0,z0,S,S);HB.nt=nt}
// una mata: 3 briznas curvas y afiladas, giradas 120°; x = ancho, y = altura (0..1), z = profundidad
function hierbaGeo(){const P=[],I=[],U=[],seg=4;
 for(let b=0;b<3;b++){const an=b*2.094+.3,ca=Math.cos(an),sa=Math.sin(an),ox=Math.cos(an+1.3)*.35,oz=Math.sin(an+1.3)*.35,inc=.18+.12*b,base=P.length/3;
  for(let s=0;s<=seg;s++){const v=s/seg,w=.5*(1-v)*(1-v*.15),lean=inc*v*v;
   for(const sg of[-1,1]){const lx=sg*w,lz=lean;P.push(ox+lx*ca-lz*sa,v*(1-.12*b),oz+lx*sa+lz*ca);U.push(sg*.5+.5,v)}}
  for(let s=0;s<seg;s++){const k=base+s*2;I.push(k,k+1,k+2,k+1,k+3,k+2)}}
 const g=new THREE.InstancedBufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(P,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(U,2));
 g.setAttribute('normal',new THREE.Float32BufferAttribute(new Float32Array(P.length).map((_,i)=>i%3===1?1:0),3));g.setIndex(I);return g}
function hierbaInit(){if(HB.mesh||HB.err)return;try{GT.ini();
 const LT=!!window.LITE,G=window.__HBG||(LT?150:300),R_=LT?.15:.26,T=TSL,{vec2,vec3,vec4,float,floor,fract,sin,cos,mix,smoothstep,max,min,clamp,length,normalize,dot,texture,uniform,instanceIndex,positionGeometry,uv,transformNormalToView,select}=T;
 HB.uC=uniform(new THREE.Vector4(0,0,1,1));hierbaTextura(P.x,P.y);
 const uCam=uniform(new THREE.Vector3()),uPush=uniform(new THREE.Vector3(0,-99,0)),uT=uniform(0),uWet=GT.U(UMO.uWet),cell=R_*2/G;HB.uCam=uCam;HB.uPush=uPush;HB.uT=uT;
 // posición de la mata en la rejilla pegada al mundo, con desplazamiento al azar
 const ii=float(instanceIndex),gx=ii.mod(G),gz=floor(ii.div(G)),snap=vec2(floor(uCam.x.div(cell)),floor(uCam.z.div(cell)));
 const cellId=snap.add(vec2(gx,gz)).sub(G/2),rnd=vec2(GT.h21(cellId),GT.h21(cellId.add(17.3))),base=cellId.add(rnd).mul(cell);
 const tuv=base.sub(HB.uC.xy).div(HB.uC.zw),tx=texture(HB.tex,tuv).level(0),dentro=tuv.x.greaterThan(0).and(tuv.y.greaterThan(0)).and(tuv.x.lessThan(1)).and(tuv.y.lessThan(1));
 const mask=select(dentro,smoothstep(.55,.9,tx.g),float(0)),hy=tx.r;
 const dist=length(base.sub(uCam.xz)),fade=smoothstep(R_,R_*.6,dist);
 // altura: más corta en las franjas de corte, más larga y seca en las calvas; algo de ruido por matas
 const q=base,gD=smoothstep(.64,.88,GT.vn(q.mul(2.3).add(7))),gS=smoothstep(.5,.6,GT.vn(q.mul(.6).add(3))),corte=gS.mul(smoothstep(-.35,.35,sin(q.x.mul(50).add(GT.vn(q.mul(.4)).mul(2)))));
 const alto=mix(.0011,.0024,GT.vn(q.mul(38))).mul(gD.mul(.5).add(1)).mul(corte.mul(.4).oneMinus()).mul(GT.h21(cellId.add(5)).mul(.5).add(.75));
 const esc=alto.mul(mask).mul(fade);
 const ang=GT.h21(cellId.add(9)).mul(6.283),ca=cos(ang),sa=sin(ang),L=positionGeometry,v=L.y;
 const hs=esc.mul(.35),lx=L.x.mul(ca).sub(L.z.mul(sa)).mul(hs),lz=L.x.mul(sa).add(L.z.mul(ca)).mul(hs);
 // viento: ráfagas que recorren el césped en la dirección del viento + temblor de cada brizna
 const wd=vec2(.82,.57),gust=GT.vn(q.mul(3.5).sub(wd.mul(uT.mul(.9)))),sway=sin(uT.mul(2.3).add(dot(q,wd).mul(160)).add(GT.h21(cellId).mul(6))).mul(.25).add(gust.mul(1.1)).add(.15);
 const bend=v.mul(v).mul(esc).mul(sway).mul(.55);
 // se aparta al pasar el protagonista o el vehículo
 const dp=base.sub(uPush.xz),dl=length(dp),empuje=smoothstep(.012,.003,dl).mul(v).mul(esc).mul(1.4),dirP=dp.div(max(dl,1e-5));
 const off=vec3(lx.add(wd.x.mul(bend)).add(dirP.x.mul(empuje)),v.mul(esc).mul(empuje.mul(-120).add(1).max(.35)),lz.add(wd.y.mul(bend)).add(dirP.y.mul(empuje)));
 const m=new THREE.MeshStandardNodeMaterial({side:THREE.DoubleSide,roughness:.85,metalness:0});
 m.positionNode=vec3(base.x,hy.add(.0004),base.y).add(off).add(vec3(0,select(esc.greaterThan(1e-6),float(0),float(-9)),0));
 // color: raíz oscura, punta clara; calvas pajizas; matas más verdes o más amarillas; mojado más oscuro
 const raiz=vec3(.09,.15,.045),punta=mix(vec3(.28,.40,.11),vec3(.38,.47,.14),GT.vn(q.mul(9))),paja=vec3(.55,.47,.20);
 let col=mix(raiz,mix(punta,paja,gD.mul(.7)),smoothstep(0,.85,v)).mul(GT.h21(cellId.add(3)).mul(.35).add(.8));
 m.colorNode=col.mul(uWet.mul(.3).oneMinus());
 m.normalNode=transformNormalToView(normalize(vec3(lx.mul(-30),1,lz.mul(-30))));   // casi hacia arriba: la hierba recibe la luz del cielo como el césped
 m.roughnessNode=mix(.85,.45,uWet);
 const geo=hierbaGeo();geo.instanceCount=G*G;const me=new THREE.Mesh(geo,m);me.frustumCulled=false;me.receiveShadow=true;me.castShadow=false;me.name='hierba';me.renderOrder=1;scene.add(me);HB.mesh=me;HB.R=R_;HB.on=true}
 catch(e){HB.err=String(e);console.warn('hierba',e)}}
function hierbaTick(dt){if(window.__HIERBA_OFF){if(HB.mesh)HB.mesh.visible=false;return}
 const cerca=driving&&!(MODO==='heli'&&pcam.position.y>.6);if(!cerca){if(HB.mesh)HB.mesh.visible=false;return}
 if(!HB.mesh){hierbaInit();if(!HB.mesh)return}HB.mesh.visible=true;HB.uT.value+=dt;
 const cx=pcam.position.x*.3+P.x*.7,cz=pcam.position.z*.3+P.y*.7;HB.uCam.value.set(cx,0,cz);HB.uPush.value.set(P.x,0,P.y);
 // la textura se rehace al acercarse a su borde o cuando entran zonas nuevas
 HB.t+=dt;const lejos=Math.max(Math.abs(cx-HB.cx),Math.abs(cz-HB.cz))>HB.size/2-HB.R-.05;
 const nz=ZROOTS.length+TROZOS.length;if(lejos||(HB.t>2&&(nz!==HB.nT||!HB.nt))){HB.t=0;HB.nT=nz;try{hierbaTextura(cx,cz)}catch(e){console.warn('hierba tex',e)}}}
// ---------- fin de gpu_hierba.js
