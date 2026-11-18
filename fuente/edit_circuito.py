import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------- GPS: solo por las calles del circuito ----------
r("function gpsCalcular(x,y,tx,ty){","let GPSF=null;\nfunction gpsCalcular(x,y,tx,ty){")
r("const A=G.ADJ[u];for(let k=0;k<A.length;k+=2){const v=A[k],nd=dist[u]+A[k+1];","const A=G.ADJ[u];for(let k=0;k<A.length;k+=2){const v=A[k];if(GPSF&&!GPSF(G.X[v],G.Y[v]))continue;const nd=dist[u]+A[k+1];")
# ---------- coche: el circuito cerrado bloquea y da media vuelta en los finales ----------
r("const blocked=MOTO?((x,y)=>{const t=cell(x,y).t;return t!==0&&t!==4}):((x,y)=>{const t=cell(x,y).t;return t===0||t===3||t===-1||t===6});",
  "const RR=REP.on&&REP.red&&MODO==='coche';const blocked=MOTO?((x,y)=>{const t=cell(x,y).t;return t!==0&&t!==4}):((x,y)=>{const t=cell(x,y).t;return t===0||t===3||t===-1||t===6||(RR&&!repLibre(x,y))});")
r("if(MOTO?(t===0||t===4):(t!==0&&t!==3&&t!==6&&t!==-1))free++","if(MOTO?(t===0||t===4):(t!==0&&t!==3&&t!==6&&t!==-1&&!(REP.on&&REP.red&&!repLibre(x,y))))free++")
# ---------- decoración común (coche y helicóptero): halos, guirnaldas, angelitos y pancartas ----------
i=s.index("function navMundo(");j=s.index("function repMarca(")
pre,seg,post=s[:i],s[i:j],s[j:]
def rs(a,b):
    global seg
    assert seg.count(a)==1,(seg.count(a),a[:80]); seg=seg.replace(a,b)
rs("function navMundo(objs){NAV.on=true;NAV.refl=[];const P_=[],C_=[],A_=[],cc=new THREE.Color();",
   "function navMundo(objs){NAV.on=true;NAV.refl=[];const P_=[],C_=[],A_=[],cc=new THREE.Color();const H_=[],HC_=[],HA_=[];const halo=(x,y,z,col,sz)=>{H_.push(x,y,z);cc.set(col);HC_.push(cc.r,cc.g,cc.b);HA_.push(Math.random()*6.28,sz)};")
rs("recorre(['Rúa de Urzáiz','Rúa de Urzaiz','Avenida da Gran Vía','Rúa Colón'],.7,","recorre(['Rúa de Urzáiz','Rúa de Urzaiz','Avenida da Gran Vía','Rúa Colón','Rúa García Barbón','Rúa Rosalía de Castro','Vía Norte','Rúa Areal'],.55,")
rs("R0=.028,estr=k%4===0;","R0=.028,estr=k%4===0;if(k%4===0)halo(cx,z0+.195,cy,estr?0xffe9a0:0xbfe4ff,.16);")
rs("luz(ax,z0+H+.05,ay,0xffffff,0,1.5,-.09);","luz(ax,z0+H+.05,ay,0xffffff,0,1.5,-.09);halo(ax,z0+H+.05,ay,0xfff2b0,.55);")
rs("if(k%5===0)NAV.refl.push({x,z:z0,y,col:0x9fd0ff,lx:.25,a:.55})});","if(k%3===0)halo(x,z0+.16,y,0x9fd0ff,.13);if(k%5===0)NAV.refl.push({x,z:z0,y,col:0x9fd0ff,lx:.25,a:.55})});")
rs(" // 9. mercadillo grande"," "+r"""// 10. angelitos colgando sobre las calles principales y pancartas «Navidad Vigo 2026»
 {const CAL=['Rúa de Urzáiz','Rúa de Urzaiz','Avenida da Gran Vía','Rúa Colón','Rúa García Barbón','Rúa Policarpo Sanz','Rúa Rosalía de Castro','Vía Norte'];const AN=[];
  recorre(CAL,.8,(x,y,tx,ty,k)=>{if(!repEnZona(x,y)||!esCalzada(x,y)||k%2)return;const nx=-ty,ny=tx,wl=Math.min(.25,borde(x,y,nx,ny,1)),wr=Math.min(.25,borde(x,y,nx,ny,-1));
   for(const o of[-.45,.45])if(wl+wr>.1)AN.push([x+nx*o*(wl-wr)*.5+nx*(o<0?-wr*.5:wl*.5),groundMap(x,y)+.33,y+ny*o*(wl-wr)*.5+ny*(o<0?-wr*.5:wl*.5),Math.atan2(-ty,tx),Math.random()*6.28])});
  if(AN.length>60)AN.length=60;const n=AN.length;
  const B=new THREE.MeshStandardMaterial({color:0xf8f6ff,roughness:.5,emissive:0x8a8aa0,emissiveIntensity:.35}),ORO=new THREE.MeshStandardMaterial({color:0xffd24a,emissive:0xffb800,emissiveIntensity:1.1,metalness:.6,roughness:.3});
  const D=-.104,ala=(sx)=>new THREE.SphereGeometry(.012,10,8).scale(.3,1,.75).rotateZ(sx*.5).translate(sx*.011,D+.006,-.005);
  const geos=[[new THREE.ConeGeometry(.013,.032,10).translate(0,D,0),B],[new THREE.SphereGeometry(.0075,10,8).translate(0,D+.022,0),new THREE.MeshStandardMaterial({color:0xf0c8a8,roughness:.7})],
   [new THREE.TorusGeometry(.008,.0016,6,18).rotateX(Math.PI/2).translate(0,D+.034,0),ORO],[mergeGeometries([ala(1),ala(-1)]),B],[new THREE.CylinderGeometry(.0007,.0007,.07,4).translate(0,D+.069,0),new THREE.MeshBasicMaterial({color:0x8a8a8a})]];
  const ms=geos.map(([g,m])=>{const im=new THREE.InstancedMesh(g,m,n);im.frustumCulled=false;pon(im);return im});NAV.angeles={ms,AN,du:new THREE.Object3D()};
  for(const a of AN)halo(a[0],a[1]-.104+.034,a[2],0xffe9a0,.08);
  const cv=document.createElement('canvas');cv.width=1024;cv.height=192;const q=cv.getContext('2d');const gr=q.createLinearGradient(0,0,0,192);gr.addColorStop(0,'#c4161f');gr.addColorStop(1,'#7a0c14');q.fillStyle=gr;q.fillRect(0,0,1024,192);
  q.strokeStyle='#ffd24a';q.lineWidth=10;q.strokeRect(10,10,1004,172);q.fillStyle='#fff6dc';q.font='900 88px system-ui,sans-serif';q.textAlign='center';q.textBaseline='middle';q.fillText('★ NAVIDAD VIGO 2026 ★',512,100);
  const tx_=new THREE.CanvasTexture(cv);tx_.colorSpace=THREE.SRGBColorSpace;tx_.anisotropy=4;NAV.texPancarta=tx_;const mP=new THREE.MeshBasicMaterial({map:tx_,side:THREE.DoubleSide,toneMapped:false}),mPo=M(0x2a2b30,.5,.5);
  let np=0;recorre(CAL,1.9,(x,y,tx,ty,k)=>{if(np>=22||k%2===1||!repEnZona(x,y)||!esCalzada(x,y))return;const nx=-ty,ny=tx,wl=Math.min(.3,borde(x,y,nx,ny,1)),wr=Math.min(.3,borde(x,y,nx,ny,-1)),W=wl+wr;if(W<.12)return;np++;
   const z0=groundMap(x,y),cx=x+nx*(wl-wr)/2,cy=y+ny*(wl-wr)/2,pl=new THREE.Mesh(new THREE.PlaneGeometry(W,W*.19),mP);pl.position.set(cx,z0+.24,cy);pl.rotation.y=Math.atan2(-ny,nx);pon(pl);
   for(const sg of[1,-1]){const po=new THREE.Mesh(new THREE.CylinderGeometry(.004,.004,.28,6),mPo);po.position.set(cx+nx*sg*W/2,z0+.14,cy+ny*sg*W/2);pon(po);halo(cx+nx*sg*W/2,z0+.285,cy+ny*sg*W/2,0xffd98a,.09);luz(cx+nx*sg*W/2,z0+.285,cy+ny*sg*W/2,0xffe9a0,k,2,.02)}})}
 // 9. mercadillo grande""")
rs(" // nube con todas las bombillas"," // halos de luz (pocos) alrededor de las luces principales\n {const ge=new THREE.BufferGeometry();ge.setAttribute('position',new THREE.Float32BufferAttribute(H_,3));ge.setAttribute('color',new THREE.Float32BufferAttribute(HC_,3));ge.setAttribute('aH',new THREE.Float32BufferAttribute(HA_,2));const pt=new THREE.Points(ge,haloMat());pt.frustumCulled=false;pt.renderOrder=4;pon(pt);NAV.nHalo=H_.length/3}\n // nube con todas las bombillas")
s=pre+seg+post
r("function navQuitar(){","""function haloMat(){return new THREE.ShaderMaterial({uniforms:{uT:NAV.uT,uSc:NAV.uSc},transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
 vertexShader:`#include <common>
#include <logdepthbuf_pars_vertex>
attribute vec3 color;attribute vec2 aH;uniform float uT,uSc;varying vec3 vC;
void main(){vec4 mv=modelViewMatrix*vec4(position,1.);gl_Position=projectionMatrix*mv;float d=-mv.z;vC=color*(.8+.2*sin(uT*1.6+aH.x));gl_PointSize=clamp(aH.y*uSc/d,2.,120.);
#include <logdepthbuf_vertex>
}`,
 fragmentShader:`#include <logdepthbuf_pars_fragment>
varying vec3 vC;void main(){
#include <logdepthbuf_fragment>
float r=length(gl_PointCoord-.5)*2.;float a=pow(max(0.,1.-r),2.4);gl_FragColor=vec4(vC*a*.5,a);}`})}
function navQuitar(){NAV.angeles=null;""")
# ---------- circuito cerrado (solo coche): máscara de calles, vallas, público animando y turbos ----------
r("function repArcade(){","""const RED_CORR=['Rúa de Urzáiz','Rúa de Urzaiz','Avenida da Gran Vía','Vía Norte'];
const urzY=x=>x<93.5?20.3:x<97.5?20.3+(x-93.5)*.325:21.6+(x-97.5)*.386;
const redZona=(x,y)=>x>88&&x<104.6&&y>14.6&&y<(x<93.1?18.65:urzY(x)-.05);
function repLibre(x,y){const R=REP.red;if(!R)return true;const i=Math.floor((x-R.x0)/R.res),j=Math.floor((y-R.y0)/R.res);return i>=0&&j>=0&&i<R.w&&j<R.h&&R.m[j*R.w+i]===1}
// le pone el público animando un salto (cada uno a su ritmo)
function animaMat(m,amp){m.onBeforeCompile=sh=>{sh.uniforms.uT=NAV.uT;sh.vertexShader='uniform float uT;\\n'+sh.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\\n#ifdef USE_INSTANCING\\ntransformed.y+=abs(sin(uT*7.+float(gl_InstanceID)*1.37))*'+amp.toFixed(4)+';\\n#endif')};return m}
function repCircuito(){const res=.025,x0=87.8,y0=14.4,w=Math.ceil((105-x0)/res),h=Math.ceil((25-y0)/res),m=new Uint8Array(w*h);
 const sg=[];if(CALLES)for(const[n,c,ls]of CALLES)if(RED_CORR.includes(n))for(const l of ls)for(let i=0;i+3<l.length;i+=2)sg.push([l[i],l[i+1],l[i+2],l[i+3]]);
 const cerca=(x,y)=>{for(const[ax,ay,bx,by]of sg){if(x<Math.min(ax,bx)-.25||x>Math.max(ax,bx)+.25||y<Math.min(ay,by)-.25||y>Math.max(ay,by)+.25)continue;const vx=bx-ax,vy=by-ay,L2=vx*vx+vy*vy||1e-9;let t=((x-ax)*vx+(y-ay)*vy)/L2;t=Math.max(0,Math.min(1,t));if(Math.hypot(ax+vx*t-x,ay+vy*t-y)<.2)return true}return false};
 for(let j=0;j<h;j++)for(let i=0;i<w;i++){const x=x0+(i+.5)*res,y=y0+(j+.5)*res;if(x>104.6||y>24.6)continue;const t=cell(x,y).t;if(t!==2&&t!==4)continue;if(redZona(x,y)||cerca(x,y))m[j*w+i]=2}
 // quita los pasos demasiado estrechos para la carroza (apertura morfológica, radio 5 cm de juego)
 {const K=[];for(let b=-3;b<=3;b++)for(let a=-3;a<=3;a++)if(a*a+b*b<=10)K.push(b*w+a);const E=new Uint8Array(w*h);for(let j=3;j<h-3;j++)for(let i=3;i<w-3;i++){const k=j*w+i;if(!m[k])continue;let ok=1;for(const o of K)if(!m[k+o]){ok=0;break}E[k]=ok}
  const O=new Uint8Array(w*h);for(let k=0;k<E.length;k++)if(E[k])for(const o of K)O[k+o]=1;for(let k=0;k<m.length;k++)if(m[k]&&!O[k])m[k]=0}
 // solo la parte conectada con la salida
 let si=Math.floor((P.x-x0)/res),sj=Math.floor((P.y-y0)/res);if(!(m[sj*w+si]>0)){let bd=1e9;for(let j=0;j<h;j+=2)for(let i=0;i<w;i+=2)if(m[j*w+i]){const d=Math.hypot(i-si,j-sj);if(d<bd){bd=d;var bi=i,bj=j}}si=bi;sj=bj;P.x=x0+(si+.5)*res;P.y=y0+(sj+.5)*res}
 const Q=[sj*w+si];m[Q[0]]=1;while(Q.length){const k=Q.pop(),i=k%w,j=(k-i)/w;for(const[di,dj]of[[1,0],[-1,0],[0,1],[0,-1]]){const a=i+di,b=j+dj;if(a<0||b<0||a>=w||b>=h)continue;const q=b*w+a;if(m[q]===2){m[q]=1;Q.push(q)}}}
 for(let k=0;k<m.length;k++)if(m[k]===2)m[k]=0;REP.red={x0,y0,res,w,h,m};GPSF=repLibre;
 // vallas en todo el borde del circuito (rojas y blancas, alguna con pancarta)
 const V=[];for(let j=4;j<h-4;j++)for(let i=4;i<w-4;i++){if(m[j*w+i]!==1||(i+j)%3)continue;if(m[j*w+i+1]&&m[j*w+i-1]&&m[(j+1)*w+i]&&m[(j-1)*w+i])continue;let nx=0,ny=0;for(let b=-4;b<=4;b++)for(let a=-4;a<=4;a++)if(!m[(j+b)*w+i+a]&&a*a+b*b<=17){nx+=a;ny+=b}const l=Math.hypot(nx,ny);if(l<1e-6)continue;nx/=l;ny/=l;V.push([x0+(i+.5)*res+nx*.012,y0+(j+.5)*res+ny*.012,nx,ny])}
 const du=new THREE.Object3D(),cc=new THREE.Color(),N=V.length;const pan=new THREE.InstancedMesh(new THREE.BoxGeometry(.078,.034,.005).translate(0,.028,0),new THREE.MeshStandardMaterial({roughness:.6}),N),pie=new THREE.InstancedMesh(new THREE.BoxGeometry(.004,.011,.018).translate(0,.0055,0),new THREE.MeshStandardMaterial({color:0x9aa0aa,roughness:.5,metalness:.6}),N);
 const cv=document.createElement('canvas');cv.width=512;cv.height=96;const q=cv.getContext('2d');q.fillStyle='#0f6a3c';q.fillRect(0,0,512,96);q.fillStyle='#ffd24a';q.font='900 54px system-ui,sans-serif';q.textAlign='center';q.textBaseline='middle';q.fillText('NAVIDAD VIGO',256,52);
 const tx=new THREE.CanvasTexture(cv);tx.colorSpace=THREE.SRGBColorSpace;const nb=Math.ceil(N/14),ban=new THREE.InstancedMesh(new THREE.BoxGeometry(.13,.03,.005).translate(0,.026,0),[0,0,0,0,new THREE.MeshBasicMaterial({map:tx,toneMapped:false}),new THREE.MeshBasicMaterial({map:tx,toneMapped:false})].map(x=>x||new THREE.MeshStandardMaterial({color:0x0f6a3c})),nb);let kb=0;
 V.forEach(([x,y,nx,ny],k)=>{const z=groundY(x,y);du.position.set(x,z,y);du.rotation.set(0,Math.atan2(-nx,-ny),0);du.scale.set(1,1,1);du.updateMatrix();
  if(k%14===7&&kb<nb){ban.setMatrixAt(kb++,du.matrix);du.scale.set(0,0,0);du.updateMatrix()}pan.setMatrixAt(k,du.matrix);pan.setColorAt(k,cc.set(Math.floor(k/2)%2?0xd51f1f:0x1f9a48));du.scale.set(1,1,1);du.updateMatrix();pie.setMatrixAt(k,du.matrix)});ban.count=kb;
 for(const o of[pan,pie,ban]){o.frustumCulled=false;scene.add(o);REP.objs.push(o)}
 // público detrás de las vallas, saltando y con los brazos en alto viendo la cabalgata
 const G=[];V.forEach(([x,y,nx,ny],k)=>{for(const fila of[.04,.075]){if(fila>.05&&Math.random()<.45)continue;const px=x+nx*(fila+Math.random()*.015)+(Math.random()-.5)*.02,py=y+ny*(fila+Math.random()*.015)+(Math.random()-.5)*.02;if(cell(px,py).t!==1)continue;G.push([px,py,Math.atan2(nx,ny)+Math.PI])}});
 if(G.length>2600)G.length=2600;const n=G.length,ROPA=[0xc4161f,0x1f3f8a,0x2a2b30,0x1f8a3c,0xf2c230,0x7a2a8a,0xe8e2d4,0x8a4a22,0x3a8ac4,0xd9622b],PIEL=[0xf0c8a8,0xe0b090,0xc68e6a,0x8a5a3a,0x5a3a26];
 const brazo=sx=>new THREE.CylinderGeometry(.0017,.0017,.019,4).rotateZ(sx*.45).translate(sx*.0085,.034,0);
 const ab=new THREE.InstancedMesh(new THREE.CylinderGeometry(.0062,.0085,.026,6).translate(0,.013,0),animaMat(new THREE.MeshStandardMaterial({roughness:.8}),.007),n),
  br=new THREE.InstancedMesh(mergeGeometries([brazo(1),brazo(-1)]),animaMat(new THREE.MeshStandardMaterial({roughness:.8}),.007),n),
  ca=new THREE.InstancedMesh(new THREE.SphereGeometry(.0056,8,6).translate(0,.0315,0),animaMat(new THREE.MeshStandardMaterial({roughness:.7}),.007),n),
  go=new THREE.InstancedMesh(new THREE.ConeGeometry(.0058,.013,6).translate(0,.042,0),animaMat(new THREE.MeshStandardMaterial({color:0xd51f1f,roughness:.7}),.007),n);
 G.forEach(([x,y,a],k)=>{const s_=1.2+Math.random()*.35;du.position.set(x,groundY(x,y),y);du.rotation.set(0,a,0);du.scale.set(s_,s_,s_);du.updateMatrix();ab.setMatrixAt(k,du.matrix);ca.setMatrixAt(k,du.matrix);
  const ropa=cc.set(ROPA[Math.floor(Math.random()*ROPA.length)]).clone();ab.setColorAt(k,ropa);ca.setColorAt(k,cc.set(PIEL[Math.floor(Math.random()*PIEL.length)]));
  const anima=Math.random()<.6;du.scale.multiplyScalar(anima?1:0.0001);du.updateMatrix();br.setMatrixAt(k,du.matrix);br.setColorAt(k,ropa);du.scale.set(s_,s_,s_);if(Math.random()>.3)du.scale.set(0,0,0);du.updateMatrix();go.setMatrixAt(k,du.matrix)});
 for(const o of[ab,br,ca,go]){o.frustumCulled=false;scene.add(o);REP.objs.push(o)}REP.publico=n;REP.vallas=N}
function repPop(t){const el=document.getElementById('nPop');el.textContent=t;el.hidden=false;el.classList.remove('on');void el.offsetWidth;el.classList.add('on');clearTimeout(repPop.t);repPop.t=setTimeout(()=>el.hidden=true,700)}
function repArcade(){""")
# monedas: imán, combo y +1 ; turbos en el suelo
r("const C=[];for(let k=0;k<60&&pool.length;k++){","const C=[];for(let k=0;k<90&&pool.length;k++){")
r("if(cell(x,y).t===2||cell(x,y).t===4)C.push({x,y,z:groundY(x,y)+.035,on:true,t:0})}}","if((cell(x,y).t===2||cell(x,y).t===4)&&repLibre(x,y))C.push({x,y,x0:x,y0:y,z:groundY(x,y)+.035,on:true,t:0})}}")
r("A.C.forEach((c,i)=>{if(!c.on){c.t-=dt;if(c.t<=0)c.on=true}if(c.on&&Math.hypot(c.x-P.x,c.y-P.y)<.075){c.on=false;c.t=25;REP.mon++;ch=true;if(!REP.sT||t-REP.sT>.07){REP.sT=t;try{sonMoneda()}catch(e){}}}",
  "A.C.forEach((c,i)=>{if(!c.on){c.t-=dt;if(c.t<=0){c.on=true;c.x=c.x0;c.y=c.y0}}const dd=Math.hypot(c.x-P.x,c.y-P.y);if(c.on&&dd<.17){const k_=Math.min(1,dt*10);c.x+=(P.x-c.x)*k_;c.y+=(P.y-c.y)*k_}\n  if(c.on&&dd<.05){c.on=false;c.t=25;REP.combo=(t-(REP.lc||-9)<1.3)?(REP.combo||0)+1:1;REP.lc=t;const b=REP.combo>=10&&REP.combo%10===0?5:0;REP.mon+=1+b;ch=true;repPop(b?'🔥 COMBO x'+REP.combo+' +'+(1+b):REP.combo>=3?'+1 · x'+REP.combo:'+1');if(!REP.sT||t-REP.sT>.07){REP.sT=t;try{sonMoneda()}catch(e){}}}")
r("REP.arc={C,R,mc,rc,lz,du};repArcadeTick(0)}","""// turbos: flechas brillantes en el asfalto
 const cvt=document.createElement('canvas');cvt.width=64;cvt.height=128;const qt=cvt.getContext('2d');qt.fillStyle='rgba(0,0,0,0)';qt.clearRect(0,0,64,128);for(const y0 of[8,72]){qt.fillStyle='#35e0ff';qt.beginPath();qt.moveTo(32,y0);qt.lineTo(60,y0+30);qt.lineTo(46,y0+30);qt.lineTo(32,y0+16);qt.lineTo(18,y0+30);qt.lineTo(4,y0+30);qt.closePath();qt.fill()}
 const txt=new THREE.CanvasTexture(cvt);txt.wrapS=txt.wrapT=THREE.RepeatWrapping;txt.repeat.set(1,2);const T=[];for(let k=0;k<40&&pool.length&&T.length<18;k++){const d=pool[Math.floor(Math.random()*pool.length)];if(!repLibre(d[1],d[2])||T.some(c=>Math.hypot(c.x-d[1],c.y-d[2])<1.2)||C.some(c=>Math.hypot(c.x-d[1],c.y-d[2])<.15))continue;T.push({x:d[1],y:d[2],a:Math.atan2(-d[3],-d[4])+(Math.random()<.5?Math.PI:0)})}
 const tm=new THREE.InstancedMesh(new THREE.PlaneGeometry(.09,.2).rotateX(-Math.PI/2),new THREE.MeshBasicMaterial({map:txt,transparent:true,toneMapped:false,depthWrite:false,blending:THREE.AdditiveBlending}),T.length),tb=new THREE.InstancedMesh(new THREE.PlaneGeometry(.1,.21).rotateX(-Math.PI/2),new THREE.MeshBasicMaterial({color:0x0a2a6a,transparent:true,opacity:.8,toneMapped:false}),T.length);
 T.forEach((c,k)=>{du.position.set(c.x,groundY(c.x,c.y)+.004,c.y);du.rotation.set(0,c.a,0);du.scale.set(1,1,1);du.updateMatrix();tb.setMatrixAt(k,du.matrix);du.position.y+=.002;du.updateMatrix();tm.setMatrixAt(k,du.matrix)});
 for(const m of[tb,tm]){m.frustumCulled=false;scene.add(m);REP.objs.push(m)}
 REP.arc={C,R,mc,rc,lz,du,T,txt};repArcadeTick(0)}""")
r(" if(REP.boost>0){REP.boost-=dt;P.v=Math.min(P.v+2.2*dt,1.55)}if(ch)repHud()}",
  " if(A.T){A.txt.offset.y-=dt*2;for(const c of A.T)if(Math.hypot(c.x-P.x,c.y-P.y)<.08&&(!REP.tT||t-REP.tT>.8)){REP.tT=t;REP.boost=Math.max(REP.boost,1.4);aviso('⚡ ¡TURBO!',.7,'peq');try{sonCaja()}catch(e){}}}\n if(REP.boost>0){REP.boost-=dt;P.v=Math.min(P.v+2.2*dt,1.55)}if(ch)repHud()}")
# angelitos balanceándose
r(" if(REP.chim&&REP.chim.userData.humo>0){"," if(NAV.angeles){const A=NAV.angeles,du=A.du,tt=NAV.uT.value;A.AN.forEach((a,k)=>{du.position.set(a[0],a[1],a[2]);du.rotation.set(0,a[3],Math.sin(tt*1.3+a[4])*.2);du.updateMatrix();for(const im of A.ms)im.setMatrixAt(k,du.matrix)});for(const im of A.ms)im.instanceMatrix.needsUpdate=true}\n if(REP.chim&&REP.chim.userData.humo>0){")
# arrancar / salir
r("REP.on=true;if(!REP.heli)repArcade();","REP.on=true;REP.pool=null;REP.red=null;GPSF=null;if(!REP.heli){repCircuito();repArcade()}")
r("heliDesvestir();REP.heli=false;REP.chim=null;REP.arc=null;REP.boost=0;","heliDesvestir();REP.heli=false;REP.chim=null;REP.arc=null;REP.boost=0;REP.red=null;GPSF=null;REP.pool=null;")
# el reparto en coche solo elige puntos dentro del circuito
r("if(repEnZona(x,y)&&esCalzada(x,y))out.push(","if(repEnZona(x,y)&&esCalzada(x,y)&&repLibre(x,y))out.push(")
r("for(const d of REP_PUNTOS)if(repEnZona(d[1],d[2]))out.push(d);","for(const d of REP_PUNTOS)if(repEnZona(d[1],d[2])&&repLibre(d[1],d[2]))out.push(d);")
# popup de monedas
r('<div id="nHud" hidden>','<div id="nPop" hidden></div><div id="nHud" hidden>')
r("#nHud[hidden]{display:none}","#nHud[hidden]{display:none}#nPop{position:fixed;left:50%;bottom:34%;transform:translateX(-50%);z-index:13;pointer-events:none;font:900 26px var(--body);color:#ffd24a;text-shadow:0 2px 0 #7a4a00,0 0 12px rgba(255,190,0,.7)}#nPop[hidden]{display:none}#nPop.on{animation:npop .7s ease-out}@keyframes npop{0%{transform:translate(-50%,10px) scale(.7);opacity:0}25%{transform:translate(-50%,0) scale(1.15);opacity:1}100%{transform:translate(-50%,-30px) scale(1);opacity:0}}")
r("window.__G={P,RACE,","window.__G={repLibre,P,RACE,")
r("if(RACE.nav)navLuz()}else{updateTraffic(d0);","if(RACE.nav)navLuz()}else{if(!REP.on||REP.heli)updateTraffic(d0);else for(const c of TRAF)c.g.visible=false;")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok circuito')
