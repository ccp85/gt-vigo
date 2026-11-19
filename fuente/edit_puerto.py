import json
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= PUERTO DE VIGO: MÁS BARCOS =================
# Modelos propios y genéricos (sin logos ni nombres de navieras):
#  - arrastreros con caseta, mástil y pórtico de popa en el Berbés
#  - remolcadores, graneleros con grúas, buques de carga rodada (car carriers) y portacontenedores atracados en los muelles
#  - mercantes fondeados en la ría y pesqueros y remolcadores navegando
#  - campas con coches nuevos esperando embarque en las explanadas vacías del puerto
# Los barcos se colocan solos: se busca agua pegada a un muelle recto y el barco se pone de costado, sin pisar a otros.
ex=json.load(open('/home/claude/work/vigo/visor/vigo_extras.json'))
CAS=json.dumps([[round(c[0],2),round(c[1],2),c[3],c[4],round(c[6],3)] for c in ex['cascos']])
r("function subeZonas(){psolChk();","function subeZonas(){psolChk();ptoChk();")
r("function subePaso(){",r"""const PTO={hecha:0};window.__PTO=PTO;
setInterval(()=>{if(!PTO.hecha)ptoChk()},3000);
function ptoChk(){if(PTO.hecha||!MAPA)return;for(const[x,y]of[[78,17],[100,11],[95,18]])if(sueloRap(x,y)==null)return;PTO.hecha=1;setTimeout(()=>{try{ptoCrea()}catch(e){console.warn('puerto',e);PTO.err=String(e)}},1500)}
function ptoCrea(){const LT=!!window.LITE,G=new THREE.Group();G.name='puerto_barcos';
 let rs=41;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const t=(x,y)=>cell(x,y).t,gy=(x,y)=>sueloRap(x,y),W0=-.032;
 // ---------- modelos ----------
 const sh=new THREE.Shape();sh.moveTo(-.5,-.5);sh.lineTo(.3,-.5);sh.quadraticCurveTo(.47,-.36,.5,0);sh.quadraticCurveTo(.47,.36,.3,.5);sh.lineTo(-.5,.5);sh.lineTo(-.5,-.5);
 const HULLG=new THREE.ExtrudeGeometry(sh,{depth:1,bevelEnabled:false,curveSegments:5});HULLG.rotateX(-Math.PI/2);HULLG.deleteAttribute('uv');
 // cada tipo: piezas fijas con su color (fijo) y casco que cambia de color por barco
 const C=new THREE.Color();
 const tipo=(L,B,fun)=>{const fx=[],hu=[];const caja=(w,h,d,x,y,z,col,ry=0)=>{const g=new THREE.BoxGeometry(w,h,d).toNonIndexed();g.deleteAttribute('uv');if(ry)g.rotateY(ry);g.translate(x,y,z);pinta(g,col);fx.push(g)};
  const cil=(r1,r2,h,x,y,z,col,rx=0,rz=0,n=8)=>{const g=new THREE.CylinderGeometry(r1,r2,h,n).toNonIndexed();g.deleteAttribute('uv');if(rx)g.rotateX(rx);if(rz)g.rotateZ(rz);g.translate(x,y,z);pinta(g,col);fx.push(g)};
  const casco=(l,b,h,x,y,z,col)=>{const g=HULLG.index?HULLG.toNonIndexed():HULLG.clone();g.scale(l,h,b);g.translate(x,y,z);if(col!=null){pinta(g,col);fx.push(g)}else hu.push(g)};
  fun({caja,cil,casco,L,B});const m=a=>a.length?mergeGeometries(a):null;return{L,B,fx:m(fx),hu:m(hu)}};
 const pinta=(g,col)=>{C.setHex(col);const n=g.attributes.position.count,a=new Float32Array(n*3);for(let i=0;i<n;i++){a[i*3]=C.r;a[i*3+1]=C.g;a[i*3+2]=C.b}g.setAttribute('color',new THREE.BufferAttribute(a,3))};
 const BL=0xf2f1ec,VD=0x24323d,GR=0x7c8288,NA=0xe0782f,AM=0xe2b23a,NE=0x26292c,RO=0xb8322c;
 const T={};
 T.arr=tipo(.42,.1,({caja,cil,casco,L,B})=>{casco(L,B,.058,0,-.022,0);casco(L*.99,B*1.01,.007,0,.03,0,BL);
  caja(.095,.042,.072,.05,.057,0,BL);caja(.097,.011,.074,.05,.072,0,VD);caja(.1,.004,.078,.05,.08,0,BL);
  cil(.0018,.0018,.1,.03,.12,0,BL);caja(.002,.002,.06,.03,.15,0,BL);cil(.0016,.0016,.07,.15,.07,0,BL);
  for(const z of[-.034,.034])caja(.005,.07,.005,-.185,.07,z,NA);caja(.006,.006,.074,-.185,.105,0,NA);
  cil(.017,.017,.06,-.115,.052,0,0x3f6f4a,Math.PI/2);cil(.007,.008,.03,-.01,.08,0,NE);caja(.06,.01,.09,-.06,.04,0,GR)});
 T.rem=tipo(.36,.12,({caja,cil,casco,L,B})=>{casco(L,B,.06,0,-.025,0);casco(L*1.02,B*1.08,.012,0,.008,0,NE);casco(L*.99,B*1.01,.006,0,.03,0,BL);
  caja(.13,.035,.09,.03,.05,0,BL);caja(.07,.035,.075,.05,.085,0,BL);caja(.072,.012,.077,.05,.096,0,VD);caja(.075,.004,.08,.05,.104,0,BL);
  cil(.0018,.0018,.07,.04,.14,0,AM);cil(.008,.009,.03,-.03,.08,0,RO);caja(.03,.012,.03,-.13,.04,0,NE)});
 T.ro=tipo(2.6,.42,({caja,cil,casco,L,B})=>{casco(L,B,.16,0,-.06,0);casco(L*.985,B*.99,.36,0,.1,0,BL);
  for(let k=0;k<5;k++)caja(L*.9,.003,B*1.002,-.02,.16+k*.06,0,0xd8d8d2);
  caja(.06,.05,B*1.02,L*.42,.47,0,BL);caja(.062,.012,B*1.03,L*.42,.485,0,VD);caja(.06,.06,.08,-L*.42,.49,0,0x3a5f8f);caja(.18,.015,.2,-L*.5+.06,.02,0,GR)});
 T.gra=tipo(2.2,.34,({caja,cil,casco,L,B})=>{casco(L,B,.16,0,-.06,0);casco(L*.99,B*1.01,.01,0,.1,0,0x8a2f2a);
  for(let k=0;k<5;k++)caja(.24,.035,B*.62,L*.34-k*.3,.117,0,GR);
  for(let k=0;k<4;k++){const x=L*.19-k*.3;cil(.012,.014,.11,x,.155,0,AM);caja(.32,.012,.012,x+.12,.2,0,AM,0);}
  caja(.2,.2,B*.9,-L*.4,.2,0,BL);caja(.21,.014,B*.95,-L*.4,.28,0,VD);caja(.22,.006,B*1.05,-L*.4,.302,0,BL);cil(.025,.03,.09,-L*.47,.33,0,NE)});
 T.con=tipo(3,.44,({caja,cil,casco,L,B})=>{casco(L,B,.17,0,-.06,0);casco(L*.99,B*1.01,.01,0,.11,0,0xb8322c);
  const CC=[0xc8473a,0x2f5fa8,0x3f8a5a,0xd9a441,0x8c939c,0xe0782f,0x1f3f6f,0x7a2f2f,0xf2f0ea];let k=0;
  for(let x=-L*.18;x<L*.4;x+=.19){if(Math.abs(x+L*.2)<.12)continue;const hh=2+((x*13.7|0)%3+3)%3;for(let j=0;j<6;j++)for(let h=0;h<hh;h++)caja(.17,.036,.058,x,.13+h*.037,(j-2.5)*.062,CC[(k++*7+h*3+j)%CC.length])}
  caja(.16,.3,B*.95,-L*.24,.27,0,BL);caja(.17,.016,B*1.1,-L*.24,.4,0,VD);caja(.17,.006,B*1.15,-L*.24,.415,0,BL);cil(.03,.035,.1,-L*.42,.25,0,NE);
  for(let x=-L*.45;x<-L*.3;x+=.19)for(let j=0;j<6;j++)caja(.17,.036,.058,x,.13,(j-2.5)*.062,CC[(j*5+3)%CC.length])});
 T.pla=tipo(.22,.065,({caja,cil,casco,L,B})=>{casco(L,B,.045,0,-.02,0);caja(.05,.032,.045,.03,.04,0,BL);caja(.052,.008,.047,.03,.05,0,VD);cil(.0012,.0012,.06,.02,.08,0,BL);caja(.04,.012,.05,-.07,.03,0,0x3f6f4a)});
 const HC={arr:[0xb8322c,0x2f5fa8,0x3f8a5a,0x1f3f6f,0xe9e6de,0xc84a2a,0x2a6f7a,0x7a2f2f],rem:[0xc8473a,0xb8322c,0x1f3f6f],ro:[0x1f3f6f,0x7a2f2f,0x2f4f2f,0x3c3c3c],gra:[0x2a2f38,0x7a2f2f,0x1f3f6f,0x2f4f2f],con:[0x1f3f6f,0x2f4f4f,0x3c3c3c,0x7a2f2f],pla:[0x2f5fa8,0xe9e6de,0xb8322c,0x3f8a5a]};
 // ---------- ocupación: barcos que ya había, náutico y atraque de los ferris ----------
 const OC=new Set(),ck=(x,y)=>Math.floor(x/.03)+','+Math.floor(y/.03);
 const pie=(x,y,a,L,B,mg,fn)=>{const ux=Math.cos(a),uy=Math.sin(a),vx=-uy,vy=ux;for(let s_=-L/2-mg;s_<=L/2+mg;s_+=.025)for(let w=-B/2-mg;w<=B/2+mg;w+=.025)if(fn(x+ux*s_+vx*w,y+uy*s_+vy*w)===false)return false;return true};
 const marca=(x,y,a,L,B,mg=.02)=>pie(x,y,a,L,B,mg,(px,py)=>{OC.add(ck(px,py))});
 for(const[x,y,L,B,a]of """+CAS+r""")marca(x,y,a,L,B,.03);
 const vedado=(x,y)=>(x>NAU.X0-.3&&x<NAU.X1+.3&&y>NAU.Y0-.3&&y<NAU.Y1+.3)||Math.hypot(x-89.5,y-10.83)<.8;
 const cabe=(x,y,a,L,B)=>pie(x,y,a,L,B,.015,(px,py)=>t(px,py)===0&&!OC.has(ck(px,py))&&!vedado(px,py));
 const ships={};const pon=(k,x,y,a)=>{(ships[k]||(ships[k]=[])).push([x,y,a,HC[k][(rn()*HC[k].length)|0]]);marca(x,y,a,T[k].L,T[k].B)};
 // atraque: agua junto a un muelle recto
 const atraca=(k,X0,X1,Y0,Y1,n,intentos)=>{const{L,B}=T[k];let hechos=0;
  for(let it=0;it<intentos&&hechos<n;it++){const px=X0+rn()*(X1-X0),py=Y0+rn()*(Y1-Y0);if(t(px,py)!==0||vedado(px,py))continue;
   let bd=9,bn=null;for(let d=0;d<16;d++){const an=d/16*6.2832,nx=Math.cos(an),ny=Math.sin(an);for(let r_=.015;r_<.3;r_+=.015)if(t(px+nx*r_,py+ny*r_)!==0){if(r_<bd){bd=r_;bn=[nx,ny]}break}}
   if(!bn)continue;const[nx,ny]=bn,cx=px+nx*(bd-B/2-.02),cy=py+ny*(bd-B/2-.02),a=Math.atan2(nx,-ny)+(rn()<.5?Math.PI:0),ux=Math.cos(a),uy=Math.sin(a);
   // muelle a lo largo de casi toda la eslora
   let nOk=0;for(const f_ of[-.42,-.2,0,.2,.42]){const qx=cx+ux*L*f_,qy=cy+uy*L*f_;for(let r_=B/2;r_<B/2+.14;r_+=.012)if(t(qx+nx*r_,qy+ny*r_)!==0){nOk++;break}}
   if(nOk<3||!cabe(cx,cy,a,L,B))continue;pon(k,cx,cy,a);hechos++;
   // abarloados: pesqueros y remolcadores se amarran unos al costado de otros
   if(k==='arr'||k==='pla'||k==='rem')for(let m=1;m<3&&hechos<n;m++){if(rn()<.35)break;const ox=cx-nx*m*(B+.014),oy=cy-ny*m*(B+.014),dl=(rn()-.5)*L*.3;const x2=ox+ux*dl,y2=oy+uy*dl;if(!cabe(x2,y2,a,L,B))break;pon(k,x2,y2,a);hechos++}}return hechos};
 // pesqueros de proa al muelle, en fila unos junto a otros (como en el Berbés)
 const proa=(k,X0,X1,Y0,Y1,n,intentos)=>{const{L,B}=T[k];let h=0;
  for(let it=0;it<intentos&&h<n;it++){const px=X0+rn()*(X1-X0),py=Y0+rn()*(Y1-Y0);if(t(px,py)!==0||vedado(px,py))continue;
   let bd=9,bn=null;for(let d=0;d<16;d++){const an=d/16*6.2832,nx=Math.cos(an),ny=Math.sin(an);for(let r_=.015;r_<.5;r_+=.015)if(t(px+nx*r_,py+ny*r_)!==0){if(r_<bd){bd=r_;bn=[nx,ny]}break}}
   if(!bn)continue;const[nx,ny]=bn,a=Math.atan2(ny,nx),ux=-ny,uy=nx;
   for(const sd of[1,-1])for(let m=(sd>0?0:1);m<8&&h<n;m++){const lx=px+ux*sd*m*(B+.012),ly=py+uy*sd*m*(B+.012);
    let q_=null;for(let r_=0;r_<.6;r_+=.012)if(t(lx+nx*r_,ly+ny*r_)!==0){q_=r_;break}if(q_==null)break;
    const cx=lx+nx*(q_-L/2-.035),cy=ly+ny*(q_-L/2-.035);if(!cabe(cx,cy,a,L,B))break;pon(k,cx,cy,a);h++}}return h};
 const fondea=(k,X0,X1,Y0,Y1,n)=>{const{L,B}=T[k];let h=0;for(let it=0;it<300&&h<n;it++){const x=X0+rn()*(X1-X0),y=Y0+rn()*(Y1-Y0),a=.55+rn()*.25;
  if(!pie(x,y,a,L*1.6,B*3,0,(px,py)=>t(px,py)===0&&!OC.has(ck(px,py))))continue;pon(k,x,y,a);h++}return h};
 const tareas=[];const Q=LT?.6:1;
 tareas.push(()=>{PTO.n1=atraca('arr',73.5,85,13.5,23.5,Math.round(14*Q),2000)+proa('arr',73.5,85,13.5,23.5,Math.round(30*Q),1500)+proa('pla',73.5,85,13.5,23.5,Math.round(16*Q),1200)+atraca('rem',73.5,85,13.5,23.5,3,600)+proa('pla',96,121,-9,13,Math.round(10*Q),800)});
 tareas.push(()=>{PTO.n2=atraca('ro',95.8,109,4,13,2,1500)+atraca('gra',95.8,109,4,13,2,1500)+atraca('rem',95.8,109,4,13,3,800)});
 tareas.push(()=>{PTO.n3=atraca('con',103,120,-9,6,2,1800)+atraca('gra',103,120,-9,6,1,900)+atraca('rem',103,120,-9,6,2,800)});
 tareas.push(()=>{PTO.n4=atraca('ro',56,75,12,27,2,1800)+atraca('gra',56,75,12,27,1,900)+atraca('arr',56,75,12,27,Math.round(8*Q),1500)+atraca('rem',56,75,12,27,2,600)});
 tareas.push(()=>{PTO.n5=fondea('con',72,112,-22,-9,2)+fondea('gra',72,112,-22,-9,2)+fondea('ro',72,112,-22,-9,1)});
 // ---------- instancias ----------
 const MF=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.7,metalness:.1}),MH=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.6,metalness:.1});
 const mm=new THREE.Matrix4(),q=new THREE.Quaternion(),Y=new THREE.Vector3(0,1,0),V=new THREE.Vector3(),S1=new THREE.Vector3(1,1,1);
 tareas.push(()=>{let tot=0;for(const k in ships){const Ls=ships[k],Tk=T[k];tot+=Ls.length;
  for(const[geo,mat,col]of[[Tk.fx,MF,0],[Tk.hu,MH,1]]){if(!geo)continue;const im=new THREE.InstancedMesh(geo,mat,Ls.length);
   Ls.forEach(([x,y,a,c],i)=>{q.setFromAxisAngle(Y,-a);mm.compose(V.set(x,W0,y),q,S1);im.setMatrixAt(i,mm);if(col)im.setColorAt(i,C.setHex(c))});
   im.castShadow=!LT;im.receiveShadow=true;im.computeBoundingSphere();im.name='barcos_'+k;G.add(im)}}PTO.barcos=tot;PTO.tipos=Object.fromEntries(Object.entries(ships).map(([k,v])=>[k,v.length]))});
 // ---------- barcos navegando: vueltas lentas por aguas abiertas ----------
 const MOV=[];const ESTELA=(()=>{const cv=document.createElement('canvas');cv.width=64;cv.height=16;const x=cv.getContext('2d'),g=x.createLinearGradient(64,0,0,0);g.addColorStop(0,'rgba(255,255,255,.9)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;
  x.beginPath();x.moveTo(64,6);x.lineTo(0,0);x.lineTo(0,16);x.lineTo(64,10);x.fill();return new THREE.CanvasTexture(cv)})();
 tareas.push(()=>{const tipos=LT?['arr','rem','arr']:['arr','rem','arr','pla','rem','arr'];let it=0;
  for(const k of tipos){for(;it<400;it++){const cx=68+rn()*48,cy=-16+rn()*16,rx=.8+rn()*1.6,ry=.5+rn()*1.1;let ok=true;
    for(let a=0;a<6.283&&ok;a+=.25)if(!aguaOK(cx+Math.cos(a)*rx,cy+Math.sin(a)*ry))ok=false;if(!ok)continue;
    const g=new THREE.Group(),Tk=T[k];g.add(new THREE.Mesh(Tk.fx,MF));const mh=new THREE.Mesh(Tk.hu,MH.clone());mh.material.color.setHex(HC[k][(rn()*HC[k].length)|0]);g.add(mh);
    // estela
    const es=new THREE.Mesh(new THREE.PlaneGeometry(Tk.L*1.1,Tk.B*1.6).rotateX(-Math.PI/2),new THREE.MeshBasicMaterial({map:ESTELA,color:0xffffff,transparent:true,opacity:.5,depthWrite:false}));es.position.set(-Tk.L*.95,.034,0);g.add(es);
    g.children.forEach(o=>o.castShadow=!LT);G.add(g);MOV.push({g,cx,cy,rx,ry,f:rn()*6.28,w:(rn()<.5?-1:1)*(.045+rn()*.03)/Math.max(rx,ry)});it++;break}}PTO.navegan=MOV.length});
 // ---------- campas de coches nuevos esperando embarque ----------
 const CAR=[];
 tareas.push(()=>{const arb=[];scene.traverse(o=>{if(!o.isInstancedMesh||!/arbol|bosque|puerto/.test(o.name))return;const m4=new THREE.Matrix4(),p=new THREE.Vector3();
   for(let k=0;k<o.instanceMatrix.count;k++){o.getMatrixAt(k,m4);p.setFromMatrixPosition(m4).applyMatrix4(o.matrixWorld);if(p.x>93&&p.x<121&&p.z>-10&&p.z<15)arb.push([p.x,p.z])}});
  const AG=new Set(arb.map(([x,y])=>Math.floor(x/.06)+','+Math.floor(y/.06)));const cercaArb=(x,y)=>{const i=Math.floor(x/.06),j=Math.floor(y/.06);for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++)if(AG.has((i+a)+','+(j+b)))return true;return false};
  const lib=(x,y)=>{if(t(x,y)!==1)return false;for(const[a,b]of[[.09,0],[-.09,0],[0,.09],[0,-.09],[.06,.06],[-.06,.06],[.06,-.06],[-.06,-.06]]){const c=t(x+a,y+b);if(c===2||c===3)return false}
   const g=gy(x,y);if(g==null||g>.15)return false;return repAltura(x,y,repMallas(x,y))<g+.01&&!cercaArb(x,y)};
  const max=LT?900:2600;
  for(const[X0,X1,Y0,Y1]of[[95.5,111,4,13.5],[103,120,-9,5],[56,75,12,27]]){for(let bx=X0;bx<X1&&CAR.length<max;bx+=.5)for(let by=Y0;by<Y1&&CAR.length<max;by+=.32){
    if(!lib(bx+.25,by+.16)||!lib(bx,by)||!lib(bx+.5,by+.32)||!lib(bx+.5,by)||!lib(bx,by+.32))continue;
    for(let i=0;i<7;i++)for(let j=0;j<7;j++){const x=bx+.03+i*.068,y=by+.025+j*.04;if(rn()<.08)continue;CAR.push([x,y,gy(x,y)])}}}
  if(!CAR.length)return;const body=new THREE.BoxGeometry(.06,.013,.026).translate(0,.0085,0),cab=new THREE.BoxGeometry(.032,.011,.0235).translate(-.004,.019,0);
  const bm=new THREE.InstancedMesh(body,new THREE.MeshStandardMaterial({color:0xffffff,roughness:.35,metalness:.5}),CAR.length),cm=new THREE.InstancedMesh(cab,new THREE.MeshStandardMaterial({color:0x2a3038,roughness:.2,metalness:.6}),CAR.length);
  const CC=[0xf4f4f2,0xf4f4f2,0xc9ccd0,0x2a2c30,0x8c939c,0xb8322c,0x2f5fa8,0xd9d6cf];q.identity();
  CAR.forEach(([x,y,z],i)=>{mm.compose(V.set(x,z,y),q,S1);bm.setMatrixAt(i,mm);cm.setMatrixAt(i,mm);bm.setColorAt(i,C.setHex(CC[(rn()*CC.length)|0]))});
  for(const m of[bm,cm]){m.receiveShadow=true;m.castShadow=false;m.computeBoundingSphere();m.name='campa_coches';G.add(m)}PTO.coches=CAR.length});
 tareas.push(()=>{scene.add(G);PTO.G=G;PTO.lista=1;
  let tA=performance.now();const anima=()=>{requestAnimationFrame(anima);const now=performance.now(),dt=Math.min(.1,(now-tA)/1000);tA=now;if(!G.visible)return;const tt=now/1000;
   for(const b of MOV){b.f+=b.w*dt;const x=b.cx+Math.cos(b.f)*b.rx,y=b.cy+Math.sin(b.f)*b.ry,dx=-Math.sin(b.f)*b.rx*Math.sign(b.w),dy=Math.cos(b.f)*b.ry*Math.sign(b.w);
    b.g.position.set(x,W0+Math.sin(tt*1.3+b.cx)*.003,y);b.g.rotation.set(Math.sin(tt*1.1+b.cy)*.02,-Math.atan2(dy,dx),0)}};anima()});
 const paso=()=>{const t0=performance.now();while(tareas.length&&performance.now()-t0<14){const f_=tareas.shift();try{f_()}catch(e){console.warn('puerto',e);PTO.err=String(e)}}if(tareas.length)setTimeout(paso,30)};paso()}
function subePaso(){""")
open(f,'w').write(s)
print('ok puerto')
