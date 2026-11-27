// ---------- barcas con forma de barco y gamelas de pescadores (barcas.js)
// Antes las lanchas eran una caja con una punta de prisma y los veleros una silueta extruida plana: parecían bloques.
// Ahora todos los cascos se hacen por cuadernas, como un barco de verdad: proa afilada con el arrufo que sube hacia
// delante, popa de espejo, fondo en V (lancha), redondeado con quilla de aleta y timón (velero) o plano (gamela), y la
// pintura por zonas (obra viva oscura bajo el agua, color del casco y franja junto a la borda). Regalas redondas,
// cubiertas que siguen la forma del casco, parabrisas, consola, fueraborda y velas con bolsa.
// Gamelas de pescadores: la barca de remos gallega (fondo plano, proa alta, popa de espejo, colores vivos) cerca de la
// costa por toda la ría. En unas el pescador rema de espaldas a proa con los dos remos (las palas entran en el agua,
// tiran y salen; el cuerpo acompaña) y va de un sitio a otro sin alejarse de la orilla; otras están fondeadas con su boya,
// el pescador con la caña y los remos recogidos dentro.
const BARC={};window.__BARC=BARC;
BARC.mat=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.6},o));
// casco por cuadernas: o={L,B,H,D(calado),popa(ancho del espejo/manga),arrufo,proaAlta,fondo:'v'|'plano'|'redondo',col,banda,obra,franja}
BARC.casco=o=>{const{L,B,H}=o,D=o.D??H*.5,NS=o.NS??18;let NU=o.NU??7;const popa=o.popa??.7,arr=o.arrufo??H*.35,ar0=o.arrufoPopa??H*.08;
 const plano=o.fondo==='plano',vee=o.fondo==='v';
 const sec=t=>{   // t 0 = espejo de popa, 1 = roda
  const tm=.42,w=t<tm?B/2*(popa+(1-popa)*Math.sin(t/tm*Math.PI/2)):B/2*Math.pow(Math.max(0,1-Math.pow((t-tm)/(1-tm),2)),.62);
  const top=H+ar0*Math.pow(1-t,2)*(t<.2?1:1)+arr*Math.pow(t,2.6);
  const kq=-D*(1-Math.pow(Math.max(0,(t-.55)/.45),1.8)*.92)*(t<.08?.85+t*1.9:1);   // la quilla sube hacia la proa
  return{w,top,kq}};
 const C1=new THREE.Color(o.col??0xf2f2ee),CB=new THREE.Color(o.banda??0x1f3557),CO=new THREE.Color(o.obra??0x5a2a26),CF=o.franja!=null?new THREE.Color(o.franja):null;
 const pos=[],col=[],idx=[],x=t=>-L/2+t*L,AB=o.anchoBanda??H*.22,FL=o.flot??0;
 const curva=(S,a)=>{if(plano){const ch=.32;return a<ch?[S.w*.62*a/ch,S.kq]:[S.w*(.62+.38*Math.pow((a-ch)/(1-ch),.7)),S.kq+(S.top-S.kq)*Math.pow((a-ch)/(1-ch),1.25)]}
  if(vee)return[S.w*Math.pow(Math.sin(a*Math.PI/2),.75),S.kq+(S.top-S.kq)*Math.pow(a,1.35)];return[S.w*Math.sin(a*Math.PI/2),S.kq+(S.top-S.kq)*(1-Math.cos(a*Math.PI/2))]};
 const zona=(S,y)=>y<FL?CO:(S.top-y<AB?CB:(CF&&Math.abs(y-(S.top-AB*1.9))<H*.05?CF:C1));
 // en cada cuaderna, además de los puntos repartidos, se duplican los puntos donde cambia la pintura: líneas de color limpias
 const us=S=>{const lim=[FL,S.top-AB];if(CF)lim.push(S.top-AB*1.9-H*.05,S.top-AB*1.9+H*.05);const L_=[];for(let k=0;k<=NU;k++)L_.push([k/NU,0]);
  for(const yl of lim){let lo=0,hi=1;if(curva(S,0)[1]>=yl){L_.push([0,yl],[0,yl]);continue}if(curva(S,1)[1]<=yl){L_.push([1,yl],[1,yl]);continue}
   for(let it=0;it<22;it++){const m=(lo+hi)/2;if(curva(S,m)[1]<yl)lo=m;else hi=m}L_.push([(lo+hi)/2,yl,-1],[(lo+hi)/2,yl,1])}
  return L_.sort((p,q)=>p[0]-q[0]||(p[2]||0)-(q[2]||0))};
 let NV=0;
 for(let i=0;i<=NS;i++){const t=i/NS,S=sec(t),U=us(S),half=[];
  for(const[a,yl,sd]of U){const[px,py]=curva(S,a);const c=sd?zona(S,yl+sd*1e-5):zona(S,py);half.push([px,py,c])}
  const fila=[...half.slice().reverse().map(([px,py,c])=>[-px,py,c]),...half.slice(1)];NV=fila.length;
  for(const[pz,py,c]of fila){pos.push(x(t),py,pz);col.push(c.r,c.g,c.b)}}
 NU=(NV-1)/2;
 const R=NU*2+1;for(let i=0;i<NS;i++)for(let j=0;j<NU*2;j++){const a=i*R+j,b=a+1,c=a+R,d=c+1;idx.push(a,b,c,b,d,c)}
 // espejo de popa
 const c0=pos.length/3,S0=sec(0);pos.push(x(0),(S0.top+S0.kq)/2,0);col.push(C1.r,C1.g,C1.b);for(let j=0;j<NU*2;j++)idx.push(c0,j+1,j);
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(col,3));g.setIndex(idx);g.computeVertexNormals();
 g.userData.sec=sec;g.userData.L=L;return g};
// curva de la borda (para regalas y cubiertas)
BARC.borda=(g,lado,t0=0,t1=1,n=16,dent=1)=>{const sec=g.userData.sec,L=g.userData.L,P=[];for(let i=0;i<=n;i++){const t=t0+(t1-t0)*i/n,S=sec(t);P.push(new THREE.Vector3(-L/2+t*L,S.top,S.w*lado*dent))}return P};
BARC.regala=(g,r,m,t1=.995)=>{const out=[];for(const l of[-1,1]){const cu=new THREE.CatmullRomCurve3(BARC.borda(g,l,0,t1,20));out.push(new THREE.Mesh(new THREE.TubeGeometry(cu,24,r,5,false),m))}return out};
// cubierta entre las dos bordas (de t0 a t1), un poco por debajo de la regala
BARC.cubierta=(g,t0,t1,baja,m,n=12)=>{const a=BARC.borda(g,1,t0,t1,n,.97),b=BARC.borda(g,-1,t0,t1,n,.97),pos=[],idx=[];
 for(let i=0;i<=n;i++){pos.push(a[i].x,a[i].y-baja,a[i].z,b[i].x,b[i].y-baja,b[i].z)}for(let i=0;i<n;i++){const k=i*2;idx.push(k,k+2,k+1,k+1,k+2,k+3)}
 const q=new THREE.BufferGeometry();q.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));q.setIndex(idx);q.computeVertexNormals();
 const nn=q.attributes.normal;for(let i=0;i<nn.count;i++)if(nn.getY(i)<0)nn.setXYZ(i,-nn.getX(i),-nn.getY(i),-nn.getZ(i));
 return new THREE.Mesh(q,m)};
BARC.cil=(a,b,r,m,n=6)=>{const A=new THREE.Vector3(...a),Bv=new THREE.Vector3(...b),d=Bv.clone().sub(A),c=new THREE.Mesh(new THREE.CylinderGeometry(r,r,d.length(),n),m);
 c.position.copy(A).add(Bv).multiplyScalar(.5);c.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());return c};
// ---- lancha de las bateas (mejilloneras): casco en V, consola, parabrisas, fueraborda
function mkLancha(col){const g=new THREE.Group(),M=BARC.mat,L=.2,B=.072,H=.016;
 const cg=BARC.casco({L,B,H,D:.016,fondo:'v',popa:.82,arrufo:.01,col,banda:0xf2f2ee,obra:0x3a2b2b,flot:-.004,anchoBanda:.006});
 const casco=new THREE.Mesh(cg,new THREE.MeshStandardMaterial({vertexColors:true,roughness:.5,side:THREE.DoubleSide}));g.add(casco);
 const piso=BARC.cubierta(cg,.02,.97,.009,M(0x9aa0a6,{roughness:.85}));g.add(piso);
 const proa=BARC.cubierta(cg,.68,.985,.0015,M(0xf2f2ee,{roughness:.5}));g.add(proa);
 for(const m of BARC.regala(cg,.0016,M(0xe6e8ea,{roughness:.35,metalness:.4})))g.add(m);
 // consola con parabrisas, asiento y caja de mejillón a popa
 const con=new THREE.Mesh(new THREE.BoxGeometry(.03,.02,.032),M(0xf4f3ee));con.position.set(.025,.02,0);g.add(con);
 const vi=new THREE.Mesh(new THREE.PlaneGeometry(.034,.016),M(0x9fb6c8,{transparent:true,opacity:.45,roughness:.1,side:THREE.DoubleSide}));vi.rotation.order='YXZ';vi.rotation.set(-.45,Math.PI/2,0);vi.position.set(.042,.036,0);g.add(vi);
 const vol=new THREE.Mesh(new THREE.TorusGeometry(.005,.0011,5,10),M(0x222222));vol.position.set(.012,.032,0);vol.rotation.y=Math.PI/2;vol.rotation.x=.4;g.add(vol);
 const as=new THREE.Mesh(new THREE.BoxGeometry(.016,.008,.026),M(0x2b3a55));as.position.set(-.005,.016,0);g.add(as);
 const cj=new THREE.Mesh(new THREE.BoxGeometry(.045,.012,.04),M(0x3a5fa8));cj.position.set(-.055,.017,0);g.add(cj);
 const gr=BARC.cil([-.02,.012,.02],[-.012,.075,.014],.0022,M(0xe8c02a));g.add(gr);   // pluma de la grúa
 // motor fueraborda
 const mo=new THREE.Mesh(new THREE.BoxGeometry(.014,.016,.012),M(0x1d1f24,{roughness:.4}));mo.position.set(-.105,.024,0);g.add(mo);
 const pi=new THREE.Mesh(new THREE.BoxGeometry(.005,.03,.004),M(0x55595f,{metalness:.5}));pi.position.set(-.107,.003,0);g.add(pi);
 const est=new THREE.Mesh(new THREE.PlaneGeometry(.3,.12),new THREE.MeshBasicMaterial({map:ESTELA_TEX,transparent:true,depthWrite:false,opacity:.7}));est.rotation.x=-Math.PI/2;est.position.set(-.24,-.016,0);g.add(est);g.userData.est=est;
 g.traverse(o=>{if(o.isMesh&&o!==est)o.castShadow=true});return g}
// ---- velero: casco redondo con quilla de aleta y timón, cubierta de teca, camarote y velas con bolsa
function mkVelero(col,vela){const g=new THREE.Group(),M=BARC.mat,L=.17,B=.052,H=.012;
 const cg=BARC.casco({L,B,H,D:.012,fondo:'redondo',popa:.62,arrufo:.004,col,banda:col===0xf4f3ee?0x23324f:0xf4f3ee,obra:0x2a2f3a,flot:-.006,anchoBanda:.003});
 g.add(new THREE.Mesh(cg,new THREE.MeshStandardMaterial({vertexColors:true,roughness:.4,side:THREE.DoubleSide})));
 g.add(BARC.cubierta(cg,0,.99,.001,M(0xd9c7a2,{roughness:.8})));
 for(const m of BARC.regala(cg,.0009,M(0xdfe3e8,{roughness:.3,metalness:.6})))g.add(m);
 const qu=new THREE.Mesh(new THREE.BoxGeometry(.04,.03,.004),M(0x23262c));qu.position.set(.005,-.026,0);qu.geometry.translate(0,0,0);g.add(qu);   // quilla de aleta con bulbo
 const bu=new THREE.Mesh(new THREE.CapsuleGeometry(.004,.03,4,8),M(0x23262c));bu.rotation.z=Math.PI/2;bu.position.set(.002,-.041,0);g.add(bu);
 const ti=new THREE.Mesh(new THREE.BoxGeometry(.012,.02,.002),M(0x23262c));ti.position.set(-.07,-.016,0);g.add(ti);
 // camarote con portillos
 const ca=new THREE.Mesh(new THREE.BoxGeometry(.055,.008,.03,1,1,1),M(0xf4f3ee,{roughness:.4}));ca.position.set(-.002,.016,0);g.add(ca);
 const ct=new THREE.Mesh(new THREE.BoxGeometry(.05,.002,.026),M(0xf4f3ee,{roughness:.4}));ct.position.set(-.002,.021,0);g.add(ct);
 for(const z of[-.0151,.0151])for(let k=0;k<3;k++){const p=new THREE.Mesh(new THREE.PlaneGeometry(.007,.003),M(0x1b2230,{roughness:.15}));p.position.set(-.018+k*.014,.016,z);p.rotation.y=z>0?0:Math.PI;g.add(p)}
 const mastil=new THREE.Mesh(new THREE.CylinderGeometry(.0018,.0022,.2,6),M(0xc9ccd2,{roughness:.3,metalness:.6}));mastil.position.set(.02,.11,0);g.add(mastil);
 const botavara=new THREE.Mesh(new THREE.CylinderGeometry(.0015,.0015,.085,5),M(0xc9ccd2,{roughness:.3,metalness:.6}));botavara.rotation.z=Math.PI/2;botavara.position.set(-.022,.03,0);g.add(botavara);
 for(const z of[-1,1])g.add(BARC.cil([.02,.2,0],[.02,.012,z*.024],.0003,M(0x9aa0a8)));   // obenques
 g.add(BARC.cil([.022,.19,0],[.083,.014,0],.0003,M(0x9aa0a8)));
 // velas con bolsa (triángulos subdivididos que se curvan hacia sotavento)
 const vela3=(A,Bp,Cp,bolsa,n=8)=>{const pos=[],idx=[];const P=(u,v)=>{const w=1-u-v;const x=A[0]*w+Bp[0]*u+Cp[0]*v,y=A[1]*w+Bp[1]*u+Cp[1]*v,sc=Math.min(1,v/Math.max(1-u,1e-6));return[x,y,bolsa*Math.sin(Math.PI*sc)*(1-u)]};
  const id=(i,j)=>i*(n+1)-i*(i-1)/2+j;for(let i=0;i<=n;i++)for(let j=0;j<=n-i;j++)pos.push(...P(i/n,j/n));
  for(let i=0;i<n;i++)for(let j=0;j<n-i;j++){idx.push(id(i,j),id(i+1,j),id(i,j+1));if(j<n-i-1)idx.push(id(i+1,j),id(i+1,j+1),id(i,j+1))}
  const q=new THREE.BufferGeometry();q.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));q.setIndex(idx);q.computeVertexNormals();return q};
 const SM=new THREE.MeshStandardMaterial({color:vela,roughness:.75,side:THREE.DoubleSide});
 const mayor=new THREE.Mesh(vela3([.019,.03,0],[.019,.205,0],[-.063,.03,0],.012),SM);g.add(mayor);
 const foque=new THREE.Mesh(vela3([.022,.03,0],[.022,.19,0],[.083,.02,0],.009),SM);g.add(foque);
 g.userData.velas=[mayor,foque];g.traverse(o=>{if(o.isMesh)o.castShadow=true});return g}
// ---- gamela gallega con pescador y remos
BARC.figura=(M,camisa)=>{const f=new THREE.Group(),PI_=M(0xd9a67e,{roughness:.7}),CA=M(camisa,{roughness:.8}),PA=M(0x2a3346,{roughness:.85}),GO=M(0x1c1c22,{roughness:.8});
 const tor=new THREE.Group();f.add(tor);f.userData.tor=tor;
 const t=new THREE.Mesh(new THREE.CapsuleGeometry(.0042,.008,3,8),CA);t.position.y=.009;tor.add(t);
 const ca=new THREE.Mesh(new THREE.SphereGeometry(.0034,10,8),PI_);ca.position.y=.0185;tor.add(ca);
 const go=new THREE.Mesh(new THREE.CylinderGeometry(.0032,.0036,.0022,10),GO);go.position.y=.021;tor.add(go);
 const vi=new THREE.Mesh(new THREE.CylinderGeometry(.0046,.0046,.0005,12),GO);vi.position.set(0,.0199,0);tor.add(vi);
 for(const z of[-.0028,.0028]){const pi=BARC.cil([0,.001,z],[.012,.0035,z*1.2],.0017,PA);f.add(pi);const pb=BARC.cil([.012,.0035,z*1.2],[.013,-.005,z*1.3],.0015,PA);f.add(pb)}
 const bra=[];for(let k=0;k<2;k++){const b=new THREE.Mesh(new THREE.CylinderGeometry(.0013,.0013,1,6),CA);b.castShadow=true;f.add(b);bra.push(b)}f.userData.bra=bra;f.userData.piel=PI_;
 const ma=[];for(let k=0;k<2;k++){const h=new THREE.Mesh(new THREE.SphereGeometry(.0016,6,5),PI_);f.add(h);ma.push(h)}f.userData.ma=ma;return f};
function mkGamela(c,banda,camisa,rema){const g=new THREE.Group(),M=BARC.mat,L=.1,B=.034,H=.014;
 const cg=BARC.casco({L,B,H,D:.006,NS:20,fondo:'plano',popa:.58,arrufo:.009,arrufoPopa:.002,col:c,banda,obra:0x2f3b2e,flot:-.002,anchoBanda:.0032,franja:0xf2efe6});
 g.add(new THREE.Mesh(cg,new THREE.MeshStandardMaterial({vertexColors:true,roughness:.55,side:THREE.DoubleSide})));
 const MA=M(0x9b7653,{roughness:.85}),MO=M(0x6b4a2e,{roughness:.8});
 g.add(BARC.cubierta(cg,.03,.93,.0105,MA));                       // tablazón del fondo
 for(const m of BARC.regala(cg,.0011,MO,.985))g.add(m);
 const ro=BARC.cil([L/2-.004,.002,0],[L/2+.002,.03,0],.0013,MO);g.add(ro);   // roda alta
 const sec=cg.userData.sec,xb=t=>-L/2+t*L;
 for(const t of[.22,.5,.74]){const S=sec(t),w=S.w*.94,y=S.top-.0045,ba=new THREE.Mesh(new THREE.BoxGeometry(.0085,.0016,w*2),MA);ba.position.set(xb(t),y,0);g.add(ba)}   // bancadas
 const tR=.5,SR=sec(tR),xr=xb(tR)-.004,yr=SR.top+.001,zr=SR.w;
 for(const l of[-1,1]){const to=new THREE.Mesh(new THREE.CylinderGeometry(.0006,.0006,.005,5),MO);to.position.set(xr,yr+.002,zr*l);g.add(to)}   // toletes
 // remos: palo con puño y pala; giran sobre el tolete
 const RM=M(0xc9a06c,{roughness:.7}),remos=[];
 for(const l of[-1,1]){const piv=new THREE.Group();piv.position.set(xr,yr+.002,zr*l);g.add(piv);const r=new THREE.Group();piv.add(r);
  const LI=.022,LO=.06;const pa=new THREE.Mesh(new THREE.CylinderGeometry(.0009,.0009,LI+LO,6),RM);pa.rotation.x=Math.PI/2;pa.position.z=l*(LO-LI)/2;r.add(pa);
  const pl=new THREE.Mesh(new THREE.BoxGeometry(.006,.0007,.018),RM);pl.position.z=l*(LO-.006);r.add(pl);
  const pu=new THREE.Mesh(new THREE.CylinderGeometry(.0012,.0012,.005,6),MO);pu.rotation.x=Math.PI/2;pu.position.z=-l*(LI-.002);r.add(pu);
  remos.push({piv,r,l,LI})}
 const fig=BARC.figura(M,camisa);g.add(fig);
 if(rema){fig.position.set(xr+.008,yr-.0035,0);fig.rotation.y=Math.PI}   // sentado en la bancada central, mirando a popa
 else{fig.position.set(xb(.24),sec(.24).top-.0035,0);fig.rotation.y=.5;   // a popa, mirando a proa, con la caña
  const ca=BARC.cil([.007,.008,0],[.03,.045,.03],.0006,M(0x3a3a3a));fig.add(ca);fig.userData.cana=ca;BARC.brazos(fig,[.007,.008,.0015],[.007,.008,-.0015]);
  for(const R of remos){R.piv.position.set(.02,yr-.004,zr*R.l*.45);R.piv.rotation.y=-R.l*Math.PI/2;R.r.rotation.x=0}}
 if(rema)BARC.brazos(fig,[-.008,.012,.008],[-.008,.012,-.008]);
 g.userData.gam={remos,fig,xr,yr,zr,rema};g.traverse(o=>{if(o.isMesh)o.castShadow=true});return g}
// fase de remada: los remos barren, la pala entra en el agua al tirar y sale al volver; el cuerpo se inclina
BARC.rema=(g,ph,fuerza)=>{const G=g.userData.gam;if(!G)return;const s=Math.sin(ph),c=Math.cos(ph),f=fuerza;
 for(const R of G.remos){const yaw=s*.55*f,pitch=c>0?.4*f:-.05*f;R.piv.rotation.set(0,-R.l*yaw,0);R.r.rotation.x=R.l*pitch}
 const fig=G.fig,tor=fig.userData.tor;tor.rotation.z=-s*.35*f;   // se echa atrás al tirar
 if(!G.rema)return;
 // brazos: del hombro al puño de cada remo
 fig.updateMatrixWorld(true);const inv=new THREE.Matrix4().copy(fig.matrixWorld).invert(),hom=new THREE.Vector3(),pu=new THREE.Vector3();
 G.remos.forEach((R,i)=>{R.r.updateMatrixWorld(true);pu.set(0,0,-R.l*(R.LI-.002)).applyMatrix4(R.r.matrixWorld).applyMatrix4(inv);
  hom.set(0,.014,-R.l*.004);hom.applyAxisAngle(new THREE.Vector3(0,0,1),tor.rotation.z);
  const b=fig.userData.bra[i],d=pu.clone().sub(hom),len=d.length();b.position.copy(hom).add(pu).multiplyScalar(.5);b.scale.set(1,len,1);b.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());fig.userData.ma[i].position.copy(pu)})};
BARC.brazos=(fig,a,b)=>{const hs=[[0,.014,.004],[0,.014,-.004]],ps=[a,b];fig.userData.bra.forEach((br,i)=>{const h=new THREE.Vector3(...hs[i]),p=new THREE.Vector3(...ps[i]),d=p.clone().sub(h),l=d.length();br.position.copy(h).add(p).multiplyScalar(.5);br.scale.set(1,l,1);br.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());fig.userData.ma[i].position.copy(p)})};
BARC.camisas=[0x2b4f7a,0x7a2b24,0x3c5a3a,0xc98a2a,0x4a4a52,0x1f3a5f];
BARC.colores=[[0x2b6cb0,0xf2c230],[0xf4f1e8,0x2b6cb0],[0x2f8a4e,0xf4f1e8],[0xc8382e,0xf4f1e8],[0xf4f1e8,0xc8382e],[0x1f3a5f,0xe8c02a],[0xe8c02a,0x2b6cb0],[0x2aa0a0,0xf4f1e8]];
// ---- gamelas por la ría: cerca de la costa, unas remando y otras fondeadas
const GAM={lista:[],ok:false};window.GAM=GAM;
function gamelasInit(){if(GAM.ok||!MAPA)return;GAM.ok=true;
 const zonas=[[60,-5,22],[30,0,18],[-10,10,16],[100,-25,12],[120,-35,8],[-40,20,15],[75,-20,12]];
 const N=window.LITE?6:16;let rs=4242;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 for(let i=0,tries=0;GAM.lista.length<N&&tries<6000;tries++){const z=zonas[tries%zonas.length],x=z[0]+(rn()*2-1)*z[2],y=z[1]+(rn()*2-1)*z[2];
  if(!aguaLibre(x,y,.07)||aguaLibre(x,y,.4))continue;if(GAM.lista.some(b=>Math.hypot(b.x-x,b.y-y)<.6))continue;
  const rema=rn()<.6,C=BARC.colores[(rn()*BARC.colores.length)|0],g=mkGamela(C[0],C[1],BARC.camisas[(rn()*BARC.camisas.length)|0],rema);
  g.rotation.order='YXZ';g.visible=false;scene.add(g);
  let boya=null;if(!rema){boya=new THREE.Mesh(new THREE.SphereGeometry(.004,8,6),BARC.mat(0xe8572e));boya.visible=false;scene.add(boya)}
  GAM.lista.push({g,boya,rema,x,y,cx:x,cy:y,a:rn()*6.28,tx:x,ty:y,v:.03+rn()*.012,ph:rn()*6.28,fase:rn()*6.28,espera:rn()*4});i++}}
function gamelaDestino(b){for(let k=0;k<30;k++){const a=Math.random()*6.28,d=.15+Math.random()*.45,x=b.cx+Math.cos(a)*d,y=b.cy+Math.sin(a)*d;if(aguaLibre(x,y,.06)&&tramoLibre(b.x,b.y,x,y,.04)){b.tx=x;b.ty=y;return true}}return false}
function gamelasTick(dt,t){if(!GAM.ok){gamelasInit();return}
 for(const b of GAM.lista){const vis=cercaFoco(b.x,b.y,14);b.g.visible=vis;if(b.boya)b.boya.visible=vis;
  let f=0;
  if(b.rema){if(b.espera>0){b.espera-=dt;f=.0}else{const dx=b.tx-b.x,dy=b.ty-b.y,d=Math.hypot(dx,dy);
    if(d<.05){b.espera=2+Math.random()*6;gamelaDestino(b)}
    else{const want=Math.atan2(dy,dx);let da=want-b.a;da=Math.atan2(Math.sin(da),Math.cos(da));b.a+=Math.max(-.6*dt,Math.min(.6*dt,da));
     b.fase+=dt*2.4;f=1;const emp=.55+.45*Math.max(0,Math.cos(b.fase)),sp=b.v*emp*(1-Math.min(.6,Math.abs(da)*.4));
     const nx=b.x+Math.cos(b.a)*sp*dt,ny=b.y+Math.sin(b.a)*sp*dt;if(aguaLibre(nx,ny,.05)){b.x=nx;b.y=ny}else{b.espera=1;gamelaDestino(b)}}}}
  if(!vis)continue;
  const bob=Math.sin(t*1.5+b.ph)*.0016;b.g.position.set(b.x,-.03+bob,b.y);b.g.rotation.y=-b.a;b.g.rotation.x=Math.sin(t*1.2+b.ph)*.05;b.g.rotation.z=Math.sin(t*.9+b.ph*1.3)*.03+(b.rema&&f?Math.cos(b.fase)*.012:0);
  if(b.rema)BARC.rema(b.g,f?b.fase:Math.PI/2+Math.sin(t*.5+b.ph)*.1,f?1:.15);
  else{const ca=b.g.userData.gam.fig.userData.cana;if(ca)ca.rotation.x=Math.sin(t*.7+b.ph)*.05;
   if(b.boya){b.a+=Math.sin(t*.05+b.ph)*.02*dt;b.boya.position.set(b.x+Math.cos(b.a)*.09,-.03+Math.sin(t*1.7+b.ph)*.0015,b.y+Math.sin(b.a)*.09)}}}}
// ---------- fin de barcas.js
