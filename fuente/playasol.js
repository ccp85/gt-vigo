// ---- playas con vida: bañistas en bañador y bikini, sombrillas a rayas y toallas ----
// Solo con sol y de día. Si llueve o se hace de noche la gente recoge y se va (sombrillas y toallas incluidas);
// cuando vuelve el sol van llegando poco a poco. Con nubes o néboa hay menos gente.
const PLY={f:null,L:[],SAM:null};window.PLY=PLY;
const BANO_C=['#e0303a','#1d4fa8','#f2c230','#14a3a3','#ff7aa8','#1c1c22','#ffffff','#ff8a1f','#7b3fb8','#2e9e4f','#00b4e6','#d8256f'].map(c=>new THREE.Color(c));
const TOA_C=['#e0553a','#f6c945','#3b47a6','#ef9a8f','#4f8a5b','#8fa6ea','#25a6c9','#f08a24','#c03a7a','#3fb58a'].map(c=>new THREE.Color(c));
const SOM_C=['#e0303a','#1d4fa8','#f2c230','#2e9e4f','#ff8a1f','#14a3a3','#d8256f'].map(c=>new THREE.Color(c));
const GPL=(()=>{const U=THREE,ni=g=>{g=g.index?g.toNonIndexed():g;if(g.attributes.uv)g.deleteAttribute('uv');return g},mg=a=>mergeGeometries(a);
 const cilX=(r,x0,x1,y,z,sy=1,sz=1,seg=8)=>{const g=new U.CylinderGeometry(r,r,Math.abs(x1-x0),seg);g.rotateZ(Math.PI/2);g.scale(1,sy,sz);g.translate((x0+x1)/2,y,z);return ni(g)};
 const cil2=(r,a,b,seg=6)=>{const A=new U.Vector3(...a),d=new U.Vector3(...b).sub(A),L=d.length();const g=new U.CylinderGeometry(r,r*.9,L,seg);g.translate(0,L/2,0);g.applyQuaternion(new U.Quaternion().setFromUnitVectors(new U.Vector3(0,1,0),d.normalize()));g.translate(A.x,A.y,A.z);return ni(g)};
 const esf=(r,x,y,z,sx=1,sy=1,sz=1)=>{const g=new U.SphereGeometry(r,8,6);g.scale(sx,sy,sz);g.translate(x,y,z);return ni(g)};
 const caja=(w,h,d,x,y,z)=>{const g=new U.BoxGeometry(w,h,d);g.translate(x,y,z);return ni(g)};
 const par=f=>[f(1),f(-1)];
 // tumbado boca arriba, cabeza hacia +x
 const pielT=mg([cilX(.0075,-.003,.019,.0045,0,.55,1),esf(.0078,.017,.0045,0,.7,.55,1),esf(.0072,-.003,.0042,0,.9,.55,1),cilX(.0024,.019,.023,.0045,0),
  ...par(s=>cil2(.003,[-.004,.003,s*.0036],[-.031,.0026,s*.0042])),...par(s=>esf(.0022,-.032,.0042,s*.0042,.6,1.4,1)),
  ...par(s=>cil2(.0022,[.016,.0035,s*.0098],[-.004,.0026,s*.0106])),...par(s=>esf(.0021,-.006,.0026,s*.0106))]);
 const shortT=cilX(.0083,-.013,.0015,.0043,0,.6,1.02);
 // sentado con las piernas estiradas, mirando hacia +x y apoyado en los brazos
 const tor=new U.CylinderGeometry(.0078,.0072,.021,9);tor.scale(.62,1,1);tor.rotateZ(.18);tor.translate(-.002,.0165,0);
 const pielS=mg([ni(tor),esf(.0078,-.0037,.026,0,.62,.45,1),esf(.0075,0,.0055,0,.8,.6,1),cil2(.0024,[-.0045,.027,0],[-.005,.031,0]),
  ...par(s=>cil2(.003,[.002,.004,s*.0038],[.03,.003,s*.0044])),...par(s=>esf(.0022,.031,.0045,s*.0044,.6,1.4,1)),
  ...par(s=>cil2(.0022,[-.004,.0245,s*.0098],[-.011,.003,s*.0115])),...par(s=>esf(.0021,-.0115,.0022,s*.0115))]);
 const shortS=cilX(.0083,-.005,.01,.0055,0,.75,1.02);
 // ellas: cintura estrecha, cadera ancha, piernas y brazos finos; bikini de copas con banda
 const pielTf=mg([esf(.007,.0155,.0045,0,.75,.55,1),cilX(.0056,.003,.0125,.0042,0,.55,1),esf(.0078,-.002,.0042,0,.95,.58,1.05),cilX(.0021,.019,.023,.0045,0),
  ...par(s=>cil2(.0031,[-.004,.0032,s*.0035],[-.017,.0027,s*.0034])),...par(s=>cil2(.0024,[-.017,.0027,s*.0034],[-.03,.0024,s*.0036])),...par(s=>esf(.0018,-.031,.004,s*.0036,.6,1.5,1)),
  ...par(s=>cil2(.0019,[.0145,.0034,s*.0085],[-.004,.0025,s*.0098])),...par(s=>esf(.0019,-.006,.0025,s*.0098))]);
 const bikiniTf=mg([esf(.0081,-.003,.0042,0,.62,.6,1.07),cilX(.0064,.012,.0135,.0045,0,.58,1),...par(s=>esf(.0031,.0128,.0076,s*.0034,.95,.6,.95))]);
 const cin=new U.CylinderGeometry(.0059,.0063,.008,9);cin.scale(.62,1,1);cin.rotateZ(.18);cin.translate(-.0012,.0112,0);
 const pielSf=mg([esf(.0078,0,.0055,0,.8,.6,1.05),ni(cin),esf(.0072,-.0032,.0192,0,.62,.8,1),esf(.0066,-.0045,.025,0,.6,.42,1),cil2(.0021,[-.0048,.026,0],[-.0052,.031,0]),
  ...par(s=>cil2(.0031,[.002,.004,s*.0035],[.016,.0034,s*.0037])),...par(s=>cil2(.0024,[.016,.0034,s*.0037],[.03,.003,s*.004])),...par(s=>esf(.0018,.031,.0045,s*.004,.6,1.5,1)),
  ...par(s=>cil2(.0019,[-.0045,.0242,s*.0088],[-.011,.003,s*.0105])),...par(s=>esf(.0019,-.0115,.0022,s*.0105))]);
 const ban=new U.CylinderGeometry(.0072,.0072,.0011,12);ban.scale(.64,1,1);ban.rotateZ(.18);ban.translate(-.0026,.0168,0);
 const bikiniSf=mg([esf(.008,.0004,.0049,0,.8,.5,1.06),ni(ban),...par(s=>esf(.0031,.0010,.0192,s*.0034,.6,.95,.95))]);
 const cabeza=ni(new U.SphereGeometry(.0066,10,8)),pelo=ni(new U.SphereGeometry(.0071,10,5,0,Math.PI*2,0,Math.PI*.55));
 // melena larga: tumbada, abierta sobre la toalla por encima de la cabeza; sentada, cayendo por la espalda
 const cas=(rz)=>{const g=ni(new U.SphereGeometry(.0072,10,6,0,Math.PI*2,0,Math.PI*.58));g.rotateZ(rz);return g};
 const peloLT=mg([cas(-Math.PI/2-.5),esf(.0075,.0075,-.0048,0,1.25,.22,1.15)]);
 const peloLS=mg([cas(.4),esf(.0052,-.0058,-.0085,0,.5,1.35,1.12)]);
 // sombrilla a rayas (gajos pares de color; los impares, blancos, van con el palo) y toalla con dos franjas más oscuras
 const cono=ni(new U.ConeGeometry(.04,.013,12,1,true)),P=cono.attributes.position.array,N=cono.attributes.normal.array,A=[[],[]],B=[[],[]];
 for(let t=0;t<P.length/9;t++){const k=(t>>1)&1;for(let j=0;j<9;j++){A[k].push(P[t*9+j]);B[k].push(N[t*9+j])}}
 const gajos=k=>{const g=new U.BufferGeometry();g.setAttribute('position',new U.Float32BufferAttribute(A[k],3));g.setAttribute('normal',new U.Float32BufferAttribute(B[k],3));g.translate(0,.066,0);return g};
 const somB=mg([cil2(.0009,[0,0,0],[0,.073,0],5),esf(.0016,0,.0735,0),gajos(1)]);
 const vc=(g,v)=>{const n=g.attributes.position.count;g.setAttribute('color',new U.Float32BufferAttribute(new Float32Array(n*3).fill(v),3));return g};
 const toalla=mg([vc(caja(.054,.0012,.025,0,.0006,0),1),...par(s=>vc(caja(.006,.0012,.025,s*.03,.0006,0),.62))]);
 return {pielT,shortT,pielS,shortS,pielTf,bikiniTf,pielSf,bikiniSf,cabeza,pelo,peloLT,peloLS,somB,telaA:gajos(0),toalla}})();
const TIPOS_P=Object.keys(GPL);let MAT_P=null;
function matPlaya(){if(MAT_P)return MAT_P;MAT_P={};const sh=new THREE.MeshStandardMaterial({roughness:.6}),ro=new THREE.MeshStandardMaterial({roughness:.75});
 for(const t of TIPOS_P)MAT_P[t]=/^piel|cabeza/.test(t)?sh:ro;MAT_P.telaA=new THREE.MeshStandardMaterial({roughness:.8,side:THREE.DoubleSide});
 MAT_P.somB=new THREE.MeshStandardMaterial({color:0xfbf7f2,roughness:.7,side:THREE.DoubleSide});MAT_P.toalla=new THREE.MeshStandardMaterial({roughness:.9,vertexColors:true});return MAT_P}
// ropa de playa para la gente de crearGente: ellos con bañador y el pecho al aire, ellas con bañador entero
function trajeBano(G,sem=0){const C=new THREE.Color();for(let i=0;i<G.N;i++){const h=(i*7+sem*13)%97,ella=h%2===0,piel=new THREE.Color(PIEL_C[(i*3+sem)%PIEL_C.length]),ba=BANO_C[(h*5+i)%BANO_C.length];
  for(const m of [G.pi,G.pd,G.bi,G.bd,G.ca])m.setColorAt(i,piel);G.cad.setColorAt(i,ba);G.to.setColorAt(i,ella?ba:piel)}
 for(const m of G.all){if(m.instanceColor)m.instanceColor.needsUpdate=true;m.userData.juntaLite=1}}
function vidaPlaya(root){root.updateMatrixWorld(true);const tris=[];let tot=0;const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();
 root.traverse(o=>{if(!o.isMesh||!/^(playa|playita)/.test(o.name))return;const p=o.geometry.attributes.position,ix=o.geometry.index;const n=ix?ix.count:p.count;
  for(let i=0;i<n;i+=3){const i0=ix?ix.getX(i):i,i1=ix?ix.getX(i+1):i+1,i2=ix?ix.getX(i+2):i+2;a.fromBufferAttribute(p,i0).applyMatrix4(o.matrixWorld);b.fromBufferAttribute(p,i1).applyMatrix4(o.matrixWorld);c.fromBufferAttribute(p,i2).applyMatrix4(o.matrixWorld);
   const ar=new THREE.Vector3().subVectors(b,a).cross(new THREE.Vector3().subVectors(c,a)).length()/2;if(ar<1e-6)continue;tot+=ar;tris.push([a.clone(),b.clone(),c.clone(),tot])}});
 if(!tris.length)return;const LT=!!window.LITE,N=Math.min(700,Math.round(tot*55));if(N<3)return;
 const pick=()=>{const r=Math.random()*tot;let lo=0,hi=tris.length-1;while(lo<hi){const m=(lo+hi)>>1;if(tris[m][3]<r)lo=m+1;else hi=m}const[t0,t1,t2]=tris[lo];let u=Math.random(),v=Math.random();if(u+v>1){u=1-u;v=1-v}return new THREE.Vector3().copy(t0).addScaledVector(new THREE.Vector3().subVectors(t1,t0),u).addScaledVector(new THREE.Vector3().subVectors(t2,t0),v)};
 const agua=(x,z)=>!!MAPA&&cell(x,z).t===0,orilla=(x,z,d)=>agua(x+d,z)||agua(x-d,z)||agua(x,z+d)||agua(x,z-d);
 const malo=(x,z)=>{if(!MAPA)return false;const t=cell(x,z).t;return t>=2&&t<=5},calle=(x,z,d)=>malo(x,z)||malo(x+d,z)||malo(x-d,z)||malo(x,z+d)||malo(x,z-d);   // ni calzada ni aparcamientos
 // sitios para grupos: separados entre sí y sin pisar la arena mojada (por ahí pasean)
 const NS=Math.min(LT?150:430,Math.round(tot*30)),R2=.06*.06,HG=new Map(),S=[];
 for(let t=0;t<NS*10&&S.length<NS;t++){const p=pick(),gx=Math.floor(p.x/.06),gz=Math.floor(p.z/.06);let ok=!orilla(p.x,p.z,.05)&&!calle(p.x,p.z,.035);
  for(let dx=-1;dx<=1&&ok;dx++)for(let dz=-1;dz<=1&&ok;dz++){const L=HG.get((gx+dx)+','+(gz+dz));if(L)for(const q of L)if((q.x-p.x)**2+(q.z-p.z)**2<R2){ok=false;break}}
  if(!ok)continue;const k=gx+','+gz;(HG.get(k)||HG.set(k,[]).get(k)).push(p);S.push(p)}
 root.userData.pickPlaya=pick;root.userData.sitiosPlaya=S;   // para la chica de las palas
 // trozos de 8 de lado (en juego se dibuja lo cercano); en el móvil, uno por zona (menos dibujos por imagen)
 const CH=new Map(),M4=new THREE.Matrix4(),Q=new THREE.Quaternion(),V=new THREE.Vector3(),S1=new THREE.Vector3(1,1,1),Yv=new THREE.Vector3(0,1,0);
 const RT=new THREE.Matrix4().makeRotationZ(-Math.PI/2-.5),RS=new THREE.Matrix4().makeRotationZ(.4);
 const TZ=LT?1e9:8,DP=[];const trozo=p=>{const k=Math.floor(p.x/TZ)+','+Math.floor(p.z/TZ);let ch=CH.get(k);if(!ch){ch={L:{},cum:{},n:0,sx:0,sz:0};for(const t of TIPOS_P){ch.L[t]=[];ch.cum[t]=[0]}CH.set(k,ch)}return ch};
 const pon=(ch,tipo,p,a,lx,ly,lz,ang,col,ex)=>{const cs=Math.cos(a),sn=Math.sin(a);V.set(p.x+lx*cs+lz*sn,p.y+ly,p.z-lx*sn+lz*cs);Q.setFromAxisAngle(Yv,a+ang);M4.compose(V,Q,S1);if(ex)M4.multiply(ex);ch.L[tipo].push([M4.clone(),col])};
 const rnd=L=>L[(Math.random()*L.length)|0];
 const persona=(ch,p,a,lx,lz,ang,sent)=>{const ella=Math.random()<.5,piel=new THREE.Color(rnd(PIEL_C)),ba=rnd(BANO_C),pe=new THREE.Color(rnd(PELO_C)),cs=Math.cos(ang),sn=Math.sin(ang);
  const rot=(x,z)=>[lx+x*cs+z*sn,lz-x*sn+z*cs];
  if(sent){const [hx,hz]=rot(-.0055,0);pon(ch,ella?'pielSf':'pielS',p,a,lx,.0013,lz,ang,piel);pon(ch,ella?'bikiniSf':'shortS',p,a,lx,.0013,lz,ang,ba);
   pon(ch,'cabeza',p,a,hx,.0368,hz,ang,piel);if(ella&&Math.random()<.75)pon(ch,'peloLS',p,a,hx,.0368,hz,ang,pe);else pon(ch,'pelo',p,a,hx,.0368,hz,ang,pe,RS)}
  else{const [hx,hz]=rot(.025,0);pon(ch,ella?'pielTf':'pielT',p,a,lx,.0013,lz,ang,piel);pon(ch,ella?'bikiniTf':'shortT',p,a,lx,.0013,lz,ang,ba);
   pon(ch,'cabeza',p,a,hx,.0068,hz,ang,piel);if(ella&&Math.random()<.75)pon(ch,'peloLT',p,a,hx,.0068,hz,ang,pe);else pon(ch,'pelo',p,a,hx,.0068,hz,ang,pe,RT)}};
 const toalla=(ch,p,a,lx,lz,ang)=>pon(ch,'toalla',p,a,lx,0,lz,ang,rnd(TOA_C));
 const dePie=(ch,p,a,lx,lz,ang)=>{const cs=Math.cos(a),sn=Math.sin(a);DP.push([p.x+lx*cs+lz*sn,p.y,p.z-lx*sn+lz*cs,a+ang,.93+Math.random()*.12])};
 for(const p of S){const ch=trozo(p),a=Math.random()*6.2832,r=Math.random();
  if(r<.5){// sombrilla con una o dos toallas a su sombra
   const ex=new THREE.Matrix4().makeRotationAxis(new THREE.Vector3(1,0,0),(Math.random()-.5)*.25);pon(ch,'somB',p,a,0,0,0,0,null,ex);pon(ch,'telaA',p,a,0,0,0,0,rnd(SOM_C),ex);
   const n=Math.random()<.6?2:1;for(let k=0;k<n;k++){const lz=n===2?(k?.016:-.016):.012;toalla(ch,p,a,.006,lz,0);const u=Math.random();
    if(u<.55)persona(ch,p,a,.006,lz,0,false);else if(u<.88)persona(ch,p,a,-.01,lz,0,true)}  // alguna toalla vacía: su dueño está en el agua
   if(Math.random()<.18)dePie(ch,p,a,-.03,.03,Math.PI*.75)}
  else if(r<.85){// tomando el sol sin sombrilla
   const n=Math.random()<.45?2:1;for(let k=0;k<n;k++){const lz=n===2?(k?.015:-.015):0;toalla(ch,p,a,0,lz,0);if(Math.random()<.8)persona(ch,p,a,0,lz,0,Math.random()<.25)}}
  else{// corrillo de pie charlando
   const n=2+(Math.random()<.4?1:0);for(let k=0;k<n;k++){const an=k/n*6.2832;dePie(ch,p,a,Math.cos(an)*.014,Math.sin(an)*.014,Math.PI-an)}
   if(Math.random()<.5)toalla(ch,p,a,.04,0,Math.PI/2)}
  for(const t of TIPOS_P)ch.cum[t].push(ch.L[t].length);ch.n++;ch.sx+=p.x;ch.sz+=p.z}
 const MAT=matPlaya();
 for(const ch of CH.values()){const reg={root,n:ch.n,k:-1,ms:[]},cx=ch.sx/ch.n,cz=ch.sz/ch.n;
  for(const t of TIPOS_P){const L=ch.L[t];if(!L.length)continue;const im=new THREE.InstancedMesh(GPL[t],MAT[t],L.length);im.name='vida_playa';im.userData.juntaLite=1;im.castShadow=true;
   L.forEach(([m,col],i)=>{im.setMatrixAt(i,m);if(col)im.setColorAt(i,col)});im.computeBoundingSphere();root.add(im);TROZOS.push({m:im,x:cx,y:cz});reg.ms.push([im,ch.cum[t]])}
  PLY.L.push(reg)}
 // los que están de pie, juntos para toda la zona (se van en orden al azar)
 if(DP.length){for(let i=DP.length-1;i>0;i--){const j=(Math.random()*(i+1))|0;[DP[i],DP[j]]=[DP[j],DP[i]]}
  const G=crearGente(DP.length,'vida_playa');trajeBano(G,DP.length);DP.forEach(([x,y,z,ang,e],i)=>G.set(i,x,y,z,ang,0,e));G.done();
  const cum=Array.from({length:DP.length+1},(_,i)=>i);for(const m of G.all)root.add(m);PLY.L.push({root,n:DP.length,k:-1,ms:G.all.map(m=>[m,cum])})}
 root.userData.playaN=N*.12;paseantesPlaya(root,pick);
 // nadadores con flotador en el agua cerca de la orilla (también salen del agua con lluvia o de noche)
 if(MAPA){const ns=Math.round(N*.12),mk=(g,n)=>{const im=new THREE.InstancedMesh(g,new THREE.MeshStandardMaterial({roughness:.75}),n);im.name='vida_playa';im.userData.juntaLite=1;im.castShadow=true;return im};const sw=mk(GP.cabeza,ns),fl=mk(GP.flot,ns);let k=0;
  for(let t=0;t<ns*12&&k<ns;t++){const p=pick();const ang=Math.random()*6.28;for(let d=.06;d<.4;d+=.04){const x=p.x+Math.cos(ang)*d,y=p.z+Math.sin(ang)*d;if(cell(x,y).t===0){M4.compose(V.set(x,-.026,y),Q.identity(),S1);sw.setMatrixAt(k,M4);sw.setColorAt(k,PIEL[k%3]);fl.setMatrixAt(k,M4);fl.setColorAt(k,PAL_S[k%PAL_S.length]);k++;break}}}
  sw.count=fl.count=k;if(k){const cum=Array.from({length:k+1},(_,i)=>i);for(const im of [sw,fl]){im.computeBoundingSphere();root.add(im);TROZOS.push({m:im,x:im.boundingSphere.center.x,y:im.boundingSphere.center.z})}PLY.L.push({root,n:k,k:-1,ms:[[sw,cum],[fl,cum]]})}}}
// cada imagen: cuánta gente hay en la playa según la hora y el tiempo
function playaSolTick(dt){const W=(window.TIEMPO&&TIEMPO.W)||{rain:0,cov:0,fog:0},noche=Math.max(CIELO.nf||0,(typeof NAV!=='undefined'&&NAV&&NAV.on)?1:0);
 const dia=1-THREE.MathUtils.smoothstep(noche,.22,.6),seco=1-THREE.MathUtils.smoothstep(W.rain||0,.04,.35);
 const obj=dia*seco*(1-.35*(W.cov||0))*(1-.45*(W.fog||0));
 if(PLY.f==null)PLY.f=obj;else{const d=obj-PLY.f,v=d<0?.2:.07;PLY.f+=Math.sign(d)*Math.min(Math.abs(d),Math.min(dt,.1)*v)}
 const f=PLY.f;
 for(let i=PLY.L.length-1;i>=0;i--){const c=PLY.L[i];if(c.root.parent)c.visto=1;else if(c.visto){PLY.L.splice(i,1);continue}
  const k=Math.round(c.n*f);if(k===c.k)continue;c.k=k;for(const [m,cum] of c.ms)m.count=cum[k]}
 for(const g of PASEO){const k=Math.round(g.L.length*f);if(g.k!==k){g.k=k;g.G.count(k)}}
 if(PLY.SAM)PLY.SAM.visible=f>.5}
