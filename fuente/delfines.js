// ---------- delfines en mar abierto (delfines.js, lo mete edit_delfines.py)
// Grupos de arroaces (delfín mular, habitual en las Rías Baixas) que nadan en formación, asoman el lomo y la aleta para
// respirar (con su resoplido) y de vez en cuando saltan fuera del agua, con salpicadura y aro de espuma.
// Solo en mar abierto (donde el fondo pasa de unos 30 m); aparecen cerca del jugador y se van al alejarse.
// Buceando también se ven por debajo de la superficie: se acercan a curiosear y se les oye silbar.
const DEL={G:null,grupos:[],t:0,spawn:6,WY:-.033,sil:2};
function delfinGeo(){const P_=[],I=[],S=16;
 // cuerpo: perfil a lo largo de x (rostro en +x, cola en -x), sección algo aplastada por la tripa
 const pf=[[1.0,0],[.98,.035],[.93,.05],[.86,.06],[.8,.12],[.72,.18],[.58,.225],[.4,.25],[.18,.25],[-.05,.23],[-.3,.185],[-.55,.12],[-.76,.065],[-.9,.04],[-.95,.022],[-.97,0]];
 pf.forEach(([x,r],i)=>{for(let k=0;k<S;k++){const a=k/S*6.2832,c=Math.cos(a),s=Math.sin(a);P_.push(x,r*s*(s<0?.85:1),r*c*.88)}
  if(i<pf.length-1)for(let k=0;k<S;k++){const a=i*S+k,b=i*S+(k+1)%S;I.push(a,a+S,b,b,a+S,b+S)}});
 const cu=new THREE.BufferGeometry();cu.setAttribute('position',new THREE.Float32BufferAttribute(P_,3));cu.setIndex(I);
 const parts=[cu.toNonIndexed()];
 const ext=(pts,dep,fn)=>{const sh=new THREE.Shape();pts.forEach(([x,y],i)=>i?sh.lineTo(x,y):sh.moveTo(x,y));const g=new THREE.ExtrudeGeometry(sh,{depth:dep,bevelEnabled:true,bevelThickness:dep*.25,bevelSize:dep*.15,bevelSegments:1,curveSegments:6});g.translate(0,0,-dep/2);if(fn)fn(g);g.deleteAttribute('uv');return g.toNonIndexed()};
 // aleta dorsal falcada
 parts.push(ext([[.12,.2],[-.02,.3],[-.2,.44],[-.18,.37],[-.26,.19]],.025));
 // aletas pectorales
 for(const s of[-1,1])parts.push(ext([[.06,0],[-.02,.03],[-.16,-.02],[-.2,-.06],[-.08,-.04]],.02,g=>{g.rotateX(Math.PI/2);g.rotateX(s*.55);g.translate(.45,-.13,s*.19)}));
 // aleta caudal horizontal (con la escotadura del centro)
 parts.push(ext([[-.88,0],[-1.04,.23],[-1.13,.24],[-1.07,.07],[-1.1,0],[-1.07,-.07],[-1.13,-.24],[-1.04,-.23]],.02,g=>g.rotateX(Math.PI/2)));
 parts.forEach(g=>{for(const k of Object.keys(g.attributes))if(k!=='position')g.deleteAttribute(k)});
 const g=mergeGeometries(parts);g.computeVertexNormals();return g}
function delfinMat(){const m=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.32,metalness:0});
 m.onBeforeCompile=sh=>{sh.uniforms.uT=DEL.uT;
  sh.vertexShader='uniform float uT;varying vec3 vLP;\n'+sh.vertexShader.replace('#include <begin_vertex>',`#include <begin_vertex>
   vLP=position;{vec3 ip=vec3(0.);
#ifdef USE_INSTANCING
   ip=instanceMatrix[3].xyz;
#endif
   float ph=uT*6.5+ip.x*41.+ip.z*29.,k=smoothstep(-.25,-1.15,position.x);transformed.y+=sin(ph+position.x*1.6)*.14*k*k;}`);
  sh.fragmentShader='varying vec3 vLP;\n'+sh.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
   {float lom=smoothstep(-.02,.12,vLP.y),tri=smoothstep(-.04,-.14,vLP.y);vec3 c=mix(vec3(.2,.22,.25),vec3(.075,.085,.1),lom);c=mix(c,vec3(.62,.62,.64),tri);
    c=mix(c,vec3(.1,.11,.13),smoothstep(.85,.97,vLP.x)*(1.-tri));c=mix(c,vec3(.12,.13,.15),step(.2,abs(vLP.z))*step(vLP.x,.5)*step(.2,vLP.x)*step(vLP.y,-.05));c=mix(c,vec3(.1,.11,.13),step(vLP.x,-.98));diffuseColor.rgb=c;}`).replace('#include <opaque_fragment>',`{float fr=pow(1.-abs(dot(normal,normalize(vViewPosition))),3.);outgoingLight+=vec3(.5,.6,.7)*fr*.18;}
   #include <opaque_fragment>`)};m.customProgramCacheKey=()=>'delfin';return m}
function delfinesInit(){const LT=!!window.LITE,G=new THREE.Group();G.name='delfines';G.userData.submarino=true;DEL.G=G;DEL.uT={value:0};DEL.MAX=LT?14:24;
 DEL.im=new THREE.InstancedMesh(delfinGeo(),delfinMat(),DEL.MAX);DEL.im.count=0;DEL.im.frustumCulled=false;DEL.im.castShadow=true;G.add(DEL.im);DEL.du=new THREE.Object3D();DEL.du.rotation.order='YZX';
 // salpicaduras y soplos: gotas que saltan y caen (o suben en el soplo) con gravedad
 const c=document.createElement('canvas');c.width=c.height=32;const x=c.getContext('2d'),gr=x.createRadialGradient(16,16,0,16,16,15);gr.addColorStop(0,'rgba(255,255,255,1)');gr.addColorStop(.5,'rgba(255,255,255,.55)');gr.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=gr;x.fillRect(0,0,32,32);
 const NP=LT?220:520,pg=new THREE.BufferGeometry(),pp=new Float32Array(NP*3);for(let k=0;k<NP;k++)pp[k*3+1]=-99;pg.setAttribute('position',new THREE.BufferAttribute(pp,3));
 const pt=new THREE.Points(pg,new THREE.PointsMaterial({color:0xf2f8fa,size:.012,map:new THREE.CanvasTexture(c),transparent:true,opacity:.9,depthWrite:false}));pt.frustumCulled=false;G.add(pt);
 DEL.go={pt,pp,v:new Float32Array(NP*3),vida:new Float32Array(NP),gr:new Float32Array(NP),NP,k:0};
 // aros de espuma donde entran y salen del agua
 DEL.aros=[];const rg=new THREE.RingGeometry(.55,1,28);rg.rotateX(-Math.PI/2);for(let k=0;k<(LT?6:12);k++){const m=new THREE.Mesh(rg,new THREE.MeshBasicMaterial({color:0xf4fafc,transparent:true,opacity:0,depthWrite:false}));m.visible=false;G.add(m);DEL.aros.push({m,t:9,d:1})}
 scene.add(G)}
function delGotas(x,y,z,n,f,soplo){const g=DEL.go;for(let q=0;q<n;q++){const k=g.k=(g.k+1)%g.NP,a=Math.random()*6.2832,r=Math.random();
 g.pp.set([x+(Math.random()-.5)*.006,y,z+(Math.random()-.5)*.006],k*3);
 if(soplo)g.v.set([Math.cos(a)*r*.03,.16+Math.random()*.12,Math.sin(a)*r*.03],k*3);else g.v.set([Math.cos(a)*(.04+r*.12)*f,(.15+Math.random()*.3)*f,Math.sin(a)*(.04+r*.12)*f],k*3);
 g.vida[k]=soplo?.5+Math.random()*.4:.6+Math.random()*.6;g.gr[k]=soplo?.35:1.1}}
function delAro(x,z,d){const a=DEL.aros.find(o=>o.t>=o.d)||DEL.aros[0];a.t=0;a.d=d;a.m.position.set(x,DEL.WY+.002,z);a.m.visible=true}
function delSon(tipo,x,y,z){if(typeof AC==='undefined'||!AC||!soundOn||!driving||!master)return;const d=Math.hypot(x-pcam.position.x,y-pcam.position.y,z-pcam.position.z),v=Math.max(0,1-d/2.2);if(v<=.02)return;
 const t=AC.currentTime,s=AC.createBufferSource(),f=AC.createBiquadFilter(),g=AC.createGain();s.buffer=NB;f.type='bandpass';
 const[fq,q,a,du,vol]=tipo==='sopla'?[950,1.3,.02,.5,.16]:tipo==='entra'?[900,.7,.005,.55,.3]:[1700,.6,.005,.4,.22];f.frequency.value=fq;f.Q.value=q;
 g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(vol*v,t+a);g.gain.exponentialRampToValueAtTime(.0005,t+du);s.connect(f);f.connect(g);g.connect(master);s.start(t,Math.random()*1.5);s.stop(t+du+.05)}
// silbidos y chasquidos bajo el agua (cuando buceas cerca)
function delSilbido(v){if(typeof AC==='undefined'||!AC||!soundOn||typeof SAG==='undefined'||!SAG.g)return;const t=AC.currentTime+.02;
 if(Math.random()<.65){const o=AC.createOscillator(),g=AC.createGain(),f0=4500+Math.random()*2500,du=.25+Math.random()*.45;o.frequency.setValueAtTime(f0,t);o.frequency.linearRampToValueAtTime(f0*(1.3+Math.random()*.5),t+du*.55);o.frequency.linearRampToValueAtTime(f0*(.85+Math.random()*.3),t+du);
  g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.035*v,t+.03);g.gain.setValueAtTime(.035*v,t+du-.05);g.gain.linearRampToValueAtTime(0,t+du);o.connect(g);g.connect(SAG.g);o.start(t);o.stop(t+du+.02)}
 else{const n=8+Math.floor(Math.random()*14),gap=.012+Math.random()*.02;for(let k=0;k<n;k++){const s=AC.createBufferSource(),f=AC.createBiquadFilter(),g=AC.createGain(),tk=t+k*gap;s.buffer=NB;f.type='highpass';f.frequency.value=3000;
  g.gain.setValueAtTime(.05*v,tk);g.gain.exponentialRampToValueAtTime(.0005,tk+.006);s.connect(f);f.connect(g);g.connect(SAG.g);s.start(tk,Math.random()*1.5);s.stop(tk+.01)}}}
function delfinesTick(dt){if(!MAPA||typeof fmProfAt!=='function'||typeof BUC==='undefined')return;DEL.t+=dt;if(DEL.t<4)return;if(!DEL.G)delfinesInit();DEL.uT.value+=dt;
 const WY=DEL.WY,prof=(x,y)=>cell(x,y).t===0?fmProfAt(BUC,x,y):-1,bucea=driving&&MODO==='nado'&&!!window.__BAJO;
 const fx=driving?P.x:(typeof ctl!=='undefined'?ctl.target.x:P.x),fy=driving?P.y:(typeof ctl!=='undefined'?ctl.target.z:P.y);
 // aparecen grupos en mar abierto alrededor del jugador (si buceas, más cerca: vienen a curiosear)
 DEL.spawn-=dt;if(DEL.spawn<=0){DEL.spawn=2.5;const nmax=window.LITE?2:3,used=DEL.grupos.reduce((s,g)=>s+g.d.length,0);
  if(DEL.grupos.length<nmax&&used<DEL.MAX-3)for(let q=0;q<25;q++){const a=Math.random()*6.2832,d=bucea?1.2+Math.random()*1.3:2+Math.random()*7,x=fx+Math.cos(a)*d,y=fy+Math.sin(a)*d;
   if(prof(x,y)<.3)continue;const n=Math.min(DEL.MAX-used,3+Math.floor(Math.random()*5)),gr={x,y,h:Math.random()*6.2832,v:.11+Math.random()*.06,ph:Math.random()*9,d:[],sz:.9+Math.random()*.2};
   for(let k=0;k<n;k++)gr.d.push({ox:-k*.06+(Math.random()-.5)*.05,oz:(k%2?1:-1)*(.03+Math.random()*.07),est:'nada',t:Math.random()*2.5,espera:1+Math.random()*2,dur:1,H:0,y:WY-.03,py:WY-.03,s:.036+Math.random()*.01,rol:0,gira:false});
   DEL.grupos.push(gr);break}}
 const du=DEL.du,im=DEL.im;let n=0;
 DEL.grupos=DEL.grupos.filter(gr=>Math.hypot(gr.x-fx,gr.y-fy)<(bucea?6:14));
 for(const gr of DEL.grupos){
  // rumbo: evitan lo poco hondo (miran por delante, a izquierda y derecha) y deambulan; buceando se acercan al nadador
  const L=.7,pa=prof(gr.x+Math.cos(gr.h)*L,gr.y+Math.sin(gr.h)*L);
  if(pa<.28){const pl=prof(gr.x+Math.cos(gr.h+.7)*L,gr.y+Math.sin(gr.h+.7)*L),pr=prof(gr.x+Math.cos(gr.h-.7)*L,gr.y+Math.sin(gr.h-.7)*L);gr.h+=(pl>pr?1:-1)*1.4*dt}
  else if(bucea&&Math.hypot(P.x-gr.x,P.y-gr.y)>.35){let da=Math.atan2(P.y-gr.y,P.x-gr.x)-gr.h;da=Math.atan2(Math.sin(da),Math.cos(da));gr.h+=da*.5*dt}
  else gr.h+=Math.sin(DEL.uT.value*.23+gr.ph)*.18*dt;
  gr.x+=Math.cos(gr.h)*gr.v*dt;gr.y+=Math.sin(gr.h)*gr.v*dt;const ch=Math.cos(gr.h),sh=Math.sin(gr.h);
  for(const d of gr.d){d.t+=dt;
   if(d.est==='nada'){d.y=WY-.03+Math.sin(DEL.uT.value*1.3+d.ox*40)*.003;if(d.t>d.espera){d.t=0;d.espera=1.3+Math.random()*2.2;if(Math.random()<.3){d.est='salta';d.dur=.9+Math.random()*.4;d.H=.05+Math.random()*.06;d.gira=Math.random()<.15}else{d.est='respira';d.dur=1+Math.random()*.4;d.sop=false}}}
   else{const s=Math.min(1,d.t/d.dur);if(d.est==='respira')d.y=WY-.03+.045*Math.sin(Math.PI*s);else d.y=WY-.03+(d.H+.03)*4*s*(1-s);d.rol=d.gira?s*6.2832:0;if(s>=1){d.est='nada';d.t=0}}
   const wx=gr.x+ch*d.ox-sh*d.oz,wz=gr.y+sh*d.ox+ch*d.oz,vy=(d.y-d.py)/Math.max(dt,1e-3),vh=Math.max(gr.v,.2)*(d.est==='salta'?2.2:1.4);
   // salidas y entradas en el agua: salpicadura, aro de espuma y sonido; soplo al respirar
   if(d.py<WY&&d.y>=WY){const fz=d.est==='salta'?1:.35;delGotas(wx,WY,wz,d.est==='salta'?26:6,fz);if(d.est==='salta'){delAro(wx,wz,1.4);delSon('sale',wx,WY,wz)}}
   if(d.py>=WY&&d.y<WY&&d.est!=='nada'){const fz=d.est==='salta'?1.2:.3;delGotas(wx,WY,wz,d.est==='salta'?34:5,fz);delAro(wx,wz,d.est==='salta'?1.8:1);if(d.est==='salta')delSon('entra',wx,WY,wz)}
   if(d.est==='respira'&&!d.sop&&d.t>d.dur*.4){d.sop=true;delGotas(wx+ch*d.s*.4,WY+.012,wz+sh*d.s*.4,9,1,true);delSon('sopla',wx,WY,wz)}
   d.py=d.y;if(n>=DEL.MAX)continue;
   du.position.set(wx,d.y,wz);du.rotation.set(d.rol,-gr.h,Math.max(-.85,Math.min(.85,Math.atan2(vy,vh))));du.scale.setScalar(d.s*gr.sz);du.updateMatrix();im.setMatrixAt(n++,du.matrix)}}
 im.count=n;im.instanceMatrix.needsUpdate=true;
 // gotas y aros
 const g=DEL.go;for(let k=0;k<g.NP;k++){if(g.vida[k]<=0)continue;g.vida[k]-=dt;const i=k*3;g.v[i+1]-=g.gr[k]*dt;g.pp[i]+=g.v[i]*dt;g.pp[i+1]+=g.v[i+1]*dt;g.pp[i+2]+=g.v[i+2]*dt;if(g.vida[k]<=0||g.pp[i+1]<WY-.004){g.vida[k]=0;g.pp[i+1]=-99}}g.pt.geometry.attributes.position.needsUpdate=true;
 for(const a of DEL.aros){if(a.t>=a.d){a.m.visible=false;continue}a.t+=dt;const s=a.t/a.d;a.m.scale.setScalar(.012+s*.05);a.m.material.opacity=.55*(1-s)*Math.min(1,s*8)}
 // buceando cerca: silbidos y chasquidos
 if(bucea){let dm=9;for(const gr of DEL.grupos)dm=Math.min(dm,Math.hypot(gr.x-P.x,gr.y-P.y));if(dm<1.3){DEL.sil-=dt;if(DEL.sil<=0){DEL.sil=.6+Math.random()*1.6;delSilbido(1-dm/1.3)}}}}
