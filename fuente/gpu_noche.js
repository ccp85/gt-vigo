// ---------- noche (gpu_noche.js) ----------
// Farolas de sodio (naranja cálido) frente al azul de la noche en la ría, ventanas que se encienden y se apagan según la hora
// y con tonos distintos (bombilla cálida, LED, el azul de una tele), el puerto y el puente de Rande iluminados, y las luces
// de Cangas y Moaña al otro lado. Casi todo son luces "pintadas": puntos brillantes (sprites aditivos, que el bloom de
// calidad alta hace resplandecer y el mar refleja); luces de verdad solo cerca del jugador: 4 farolas reales (las más
// cercanas al coche) que alumbran el asfalto, las fachadas y la pintura del coche.
// Con window.__NOCHE_OFF=true se apaga todo lo nuevo (las ventanas siguen como antes).
const NOCHE={V:{uLz:{value:0},uFrac:{value:.55},uOrt:{value:0},uPxO:{value:.01},uPxP:{value:.001},uT:{value:0}},
 spr:{},pl:[],plT:0,rande:0,costa:0,lz:0,cand:[],tex:null};window.NOCHE=NOCHE;
const NOCHE_SODIO=[1,.45,.12];
NOCHE.zona=id=>{try{pedirZona(id)}catch(e){console.warn(e)}};   // para pruebas desde la consola: NOCHE.zona('rande')
// cuántas ventanas hay encendidas según la hora (de las que pueden encenderse): mucho al anochecer, poco de madrugada
function nocheFraccion(h){const k=(a,b,x)=>Math.min(1,Math.max(0,(x-a)/(b-a)));
 if(h>=17&&h<21)return .45+.25*k(17,21,h);if(h>=21)return .7-.2*k(21,24,h);if(h<2)return .5-.22*k(0,2,h);if(h<5)return .28-.1*k(2,5,h);if(h<8)return .18+.27*k(5,8,h);return .45}
// TSL: ventana encendida o no (c = celda de la ventana) y su color
GT.ventanaOn=c=>TSL.step(GT.U(NOCHE.V.uFrac).oneMinus(),GT.hF(c));
GT.ventanaCol=c=>{const T=TSL,{vec3,select,sin}=T,h=GT.hF(c.add(11)),b=GT.hF(c.add(5)).add(1.2);
 const tele=vec3(.45,.62,1).mul(sin(GT.U(NOCHE.V.uT).mul(GT.hF(c.add(3)).mul(3).add(2)).add(h.mul(40))).mul(.25).add(.75));   // el azul de una tele, que parpadea
 return select(h.lessThan(.5),vec3(1,.66,.36),select(h.lessThan(.82),vec3(1,.82,.6),select(h.lessThan(.93),vec3(.95,.96,1),tele))).mul(b)};
function nocheHalo(){if(NOCHE.tex)return NOCHE.tex;const N=64,c=document.createElement('canvas');c.width=c.height=N;const x=c.getContext('2d'),g=x.createRadialGradient(N/2,N/2,0,N/2,N/2,N/2);
 g.addColorStop(0,'rgba(255,255,255,1)');g.addColorStop(.12,'rgba(255,255,255,.85)');g.addColorStop(.35,'rgba(255,255,255,.22)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(0,0,N,N);
 const t=new THREE.CanvasTexture(c);NOCHE.tex=t;return t}
// un grupo de luces pintadas: L = [[x,y,z, r,g,b, tamaño], ...] (y hacia arriba)
function nocheSprites(nombre,L,brillo=1.3){if(!L.length)return null;const T=TSL,n=L.length,P=new Float32Array(n*3),C=new Float32Array(n*3),S=new Float32Array(n);
 L.forEach((l,i)=>{P[i*3]=l[0];P[i*3+1]=l[1];P[i*3+2]=l[2];C[i*3]=l[3];C[i*3+1]=l[4];C[i*3+2]=l[5];S[i]=l[6]});
 const p=T.instancedBufferAttribute(new THREE.InstancedBufferAttribute(P,3)),c=T.instancedBufferAttribute(new THREE.InstancedBufferAttribute(C,3)),s=T.instancedBufferAttribute(new THREE.InstancedBufferAttribute(S,1));
 const V=NOCHE.V,uOrt=GT.U(V.uOrt),uLz=GT.U(V.uLz),d=T.length(p.sub(T.cameraPosition)),ort=uOrt.greaterThan(.5);
 const sz=T.max(s,T.select(ort,GT.U(V.uPxO),d.mul(GT.U(V.uPxP))).mul(3.2));                       // como poco unos 3 píxeles
 const m=new THREE.SpriteNodeMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,fog:false});
 const a=T.texture(nocheHalo(),T.uv()).r,lejos=T.select(ort,T.float(1),T.exp(d.div(-70)));
 m.positionNode=p;m.scaleNode=T.vec2(sz,sz);m.colorNode=c.mul(brillo).mul(lejos);m.opacityNode=a.mul(uLz);
 const sp=new THREE.Sprite(m);sp.count=n;sp.frustumCulled=false;sp.renderOrder=6;sp.name='noche_'+nombre;sp.visible=false;scene.add(sp);NOCHE.spr[nombre]=sp;return sp}
// ---- el puente de Rande: farolas en los dos bordes del tablero, torres iluminadas desde abajo y los tirantes con un hilo de luz
function nocheRande(){if(NOCHE.rande)return;const tor=[];
 scene.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||!/^piezas/.test(o.name||''))return;if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();const b=o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld);
  if(b.max.y-b.min.y>2&&b.min.x>142&&b.max.x<149&&b.min.z>-46&&b.max.z<-28)tor.push({b,o})});
 if(tor.length<2)return;
 // las dos torres (las dos cajas altas más separadas)
 tor.sort((a,b)=>a.b.min.z-b.b.min.z);const A=tor[0].b,B=tor[tor.length-1].b,ca=A.getCenter(new THREE.Vector3()),cb=B.getCenter(new THREE.Vector3());
 const dir=new THREE.Vector3(cb.x-ca.x,0,cb.z-ca.z),vano=dir.length();if(vano<1)return;dir.normalize();const per=new THREE.Vector3(-dir.z,0,dir.x);
 const mallas=tor.map(t=>t.o);scene.traverse(o=>{if(o.isMesh&&!o.isInstancedMesh&&/^piezas/.test(o.name||'')&&!mallas.includes(o)){if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();const b=o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld);
  if(b.max.x>ca.x-vano*2&&b.min.x<cb.x+vano*2&&b.max.z>Math.min(ca.z,cb.z)-vano*2&&b.min.z<Math.max(ca.z,cb.z)+vano*2)mallas.push(o)}});
 const rc=new THREE.Raycaster(),abajo=new THREE.Vector3(0,-1,0),q=new THREE.Vector3();rc.firstHitOnly=true;
 const alto=(x,z)=>{q.set(x,40,z);rc.set(q,abajo);const h=rc.intersectObjects(mallas,false)[0];return h?h.point.y:null};
 // altura del tablero: en el centro del vano; el puente sigue mientras haya tablero a esa altura (más o menos)
 const mid=ca.clone().lerp(cb,.5),hT=A.max.y-A.min.y;let y0=alto(mid.x+per.x*.05,mid.z+per.z*.05);const medido=y0!=null&&y0>.3;if(!medido)y0=A.min.y+hT*.34;   // si no se encuentra el tablero, a un tercio de la torre
 let ancho=medido?.1:.35;if(medido)for(let w=.08;w<1.2;w+=.04){const yy=alto(mid.x+per.x*w,mid.z+per.z*w);if(yy==null||Math.abs(yy-y0)>.08)break;ancho=w}   // medio ancho del tablero
 const L=[],paso=.16,tab=[];
 for(let s=-vano*2.2;s<=vano*3.2;s+=paso){const x=ca.x+dir.x*s,z=ca.z+dir.z*s;let yy=medido?alto(x,z):null;if(yy==null&&s>-vano*1.45&&s<vano*2.45)yy=y0;if(yy==null||yy<y0-.6||yy>y0+.25)continue;tab.push([x,yy,z]);
  for(const sg of[-1,1])L.push([x+per.x*ancho*.95*sg,yy+.07,z+per.z*ancho*.95*sg,1,.7,.42,.03])}
 // torres: luz que sube por las aristas (blanca, algo fría) y un foco arriba
 const T2=[];for(const b of[A,B]){const h=b.max.y-b.min.y;for(const[x,z]of[[b.min.x,b.min.z],[b.max.x,b.max.z],[b.min.x,b.max.z],[b.max.x,b.min.z]])
  for(let k=1;k<=9;k++)T2.push([x,b.min.y+h*k/10,z,.75,.86,1,.035*(1-k/14)])}
 // tirantes: un hilo de luces desde lo alto de cada torre hasta el tablero, a los dos lados
 const H=[];for(const[b,c]of[[A,ca],[B,cb]])for(const sg of[-1,1])for(let j=1;j<=7;j++)for(const lado of[-1,1]){const s0=lado*vano*.42*j/7,top=new THREE.Vector3(c.x,b.max.y-.15,c.z),
   bot=new THREE.Vector3(c.x+dir.x*s0+per.x*ancho*.8*sg,y0+.05,c.z+dir.z*s0+per.z*ancho*.8*sg);for(let t=.12;t<.95;t+=.11){const p=top.clone().lerp(bot,t);H.push([p.x+per.x*ancho*.8*sg*(1-t),p.y,p.z+per.z*ancho*.8*sg*(1-t),.6,.75,1,.012])}}
 nocheSprites('rande',L,1.4);nocheSprites('rande_torres',T2,1.1);nocheSprites('rande_tirantes',H,.8);NOCHE.rande=1;NOCHE.randeInfo={tab:tab.length,y0,ancho,vano}}
// ---- costa: el puerto (muelles con farolas y torres de luz en las explanadas) y las luces de Cangas y Moaña enfrente
function nocheCosta(){if(NOCHE.costa)return;const img=UCO.uCos.value.image;if(!img||!img.data||img.width<8||typeof groundMap!=='function')return;
 const mar=(x,z)=>ARF.mar(x,z),tierra=(x,z)=>mar(x,z)>247,L=[],M=[],O=[],usados=[];
 const lejos=(x,z,r)=>{for(const u of usados)if((u[0]-x)**2+(u[1]-z)**2<r*r)return false;return true};
 const borde=(x0,x1,z0,z1,st,sep,out,f)=>{for(let x=x0;x<=x1;x+=st)for(let z=z0;z<=z1;z+=st){if(!tierra(x,z))continue;
  let sx=0,sz=0,n=0;const e=.3;for(const[dx,dz]of[[e,0],[-e,0],[0,e],[0,-e]])if(mar(x+dx,z+dz)<230){sx+=dx;sz+=dz;n++}
  if(!n||!lejos(x,z,sep))continue;usados.push([x,z]);const l=Math.hypot(sx,sz)||1;f(x,z,-sx/l,-sz/l,out)}};
 const suelo=(x,z)=>{const g=groundMap(x,z);return g>-1?Math.max(g,0):.05};
 // puerto de Vigo (Bouzas → Guixar): farola en el cantil cada ~18 m y, cada pocas, una torre alta de la explanada
 let k=0;borde(58,124,2,34,.15,.45,L,(x,z,ix,iz)=>{const y=suelo(x,z);L.push([x,y+.12,z,...NOCHE_SODIO,.028]);
  if(k++%4===0){const mx=x+ix*.7,mz=z+iz*.7;if(tierra(mx,mz))M.push([mx,suelo(mx,mz)+.5,mz,1,.52,.2,.04])}});
 // enfrente: Cangas, Moaña y Domaio, más pequeñas (casas y paseos)
 borde(-6,132,-42,-4,.2,.55,O,(x,z,ix,iz)=>{for(let j=0;j<2;j++){const ox=x+ix*(.25+j*.5),oz=z+iz*(.25+j*.5);if(tierra(ox,oz))O.push([ox,suelo(ox,oz)+.1,oz,1,.6+.15*Math.random(),.3,.022])}});
 if(L.length+O.length<20)return;nocheSprites('puerto',L,1.3);nocheSprites('puerto_torres',M,1.5);nocheSprites('enfrente',O,1.05);NOCHE.costa=1;NOCHE.costaInfo={muelle:L.length,torres:M.length,enfrente:O.length}}
// ---- farolas de verdad cerca del jugador (las 4 más cercanas de las zonas cargadas)
function nocheFarolasReales(on){if(window.LITE)return;if(!NOCHE.pl.length){for(let i=0;i<4;i++){const l=new THREE.PointLight(new THREE.Color().setRGB(1,.55,.22,THREE.LinearSRGBColorSpace),0,.55,2);l.position.set(0,-50,0);l.castShadow=false;scene.add(l);NOCHE.pl.push(l)}}
 const t=performance.now();if(on&&t-NOCHE.plT>250){NOCHE.plT=t;const px=P.x,py=P.y,c=[];
  for(const z of ZROOTS){const F=z.root&&z.root.userData.farolas;if(!F||!z.root.parent)continue;for(const f of F){const d=(f.x-px)**2+(f.y-py)**2;if(d<1.44)c.push([d,f])}}
  c.sort((a,b)=>a[0]-b[0]);NOCHE.cand=c.slice(0,4)}
 NOCHE.pl.forEach((l,i)=>{const e=on&&NOCHE.cand[i];if(!e){l.intensity=0;return}const f=e[1],d=Math.sqrt((f.x-P.x)**2+(f.y-P.y)**2);
  l.position.set(f.x,f.z+.1,f.y);l.intensity=.017*NOCHE.lz*(1-THREE.MathUtils.smoothstep(d,.7,1.2))})}
// cada imagen (desde cielo())
function nocheTick(dt){const V=NOCHE.V,off=!!window.__NOCHE_OFF;V.uT.value+=dt;
 NOCHE.lz=off?0:THREE.MathUtils.smoothstep(CIELO.nf,.35,.8);V.uLz.value=NOCHE.lz;V.uFrac.value=nocheFraccion(CIELO.h);
 if(!NOCHE.ini){NOCHE.ini=1;try{LAMPARA_MAT.emissive.setRGB(1,.5,.16,THREE.LinearSRGBColorSpace);CHARCO_MAT.color.setRGB(1,.62,.32,THREE.LinearSRGBColorSpace)}catch(e){}}
 V.uOrt.value=driving?0:1;const h=(R.domElement&&R.domElement.height)||800;V.uPxO.value=(cam.top-cam.bottom)/cam.zoom/h;V.uPxP.value=2*Math.tan(pcam.fov*Math.PI/360)/h;
 const t=performance.now();if(!NOCHE.tt||t-NOCHE.tt>3000){NOCHE.tt=t;try{nocheCosta()}catch(e){if(!NOCHE.eC){NOCHE.eC=1;console.warn('noche costa',e)}}try{nocheRande()}catch(e){if(!NOCHE.eR){NOCHE.eR=1;console.warn('noche Rande',e)}}}
 for(const k in NOCHE.spr)NOCHE.spr[k].visible=NOCHE.lz>.01;
 nocheFarolasReales(driving&&NOCHE.lz>.01)}
// ---------- fin de gpu_noche.js
