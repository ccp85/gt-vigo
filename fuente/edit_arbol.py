import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= ENCENDIDO DE LUCES: 2 ARCOS → MUÑECOS DE NIEVE → REGALO GIGANTE → ÁRBOL DE PORTA DO SOL =================
# Al empezar la misión todo está apagado. El último paso es el árbol gigante: destello azul, cientos de LED que suben
# en espiral con una cinemática de cámara alrededor del árbol, y al final la estrella brilla e ilumina toda la ciudad.
# --- referencias a los adornos que se encienden
r("ptA.frustumCulled=false;ptA.renderOrder=5;pon(ptA)}","ptA.frustumCulled=false;ptA.renderOrder=5;NAV.arbolPts=pon(ptA)}")
r("const ORO=brillo(0xffd24a,.7);for(const[a,b,c]of[[S*1.01,S*1.01,S*.14],[S*.14,S*1.01,S*1.01]]){const m=new THREE.Mesh(new THREE.BoxGeometry(a,b,c),ORO);m.position.y=S/2;g.add(m)}\n  for(const s of[1,-1]){const l=new THREE.Mesh(new THREE.TorusGeometry(S*.2,S*.045,8,16),ORO);l.position.set(s*S*.17,S*1.12,0);l.rotation.y=Math.PI/2;l.rotation.z=s*.5;g.add(l)}\n  pon(g);const c_=Math.cos(g.rotation.y),s_=Math.sin(g.rotation.y);const W=(lx,ly,lz)=>[gx+lx*c_+lz*s_,z0+ly,gy-lx*s_+lz*c_];\n  for(let e=0;e<12;e++){for(let k=0;k<=16;k++){const t=(k/16-.5)*S;let p;const h=S/2;if(e<4)p=[t,[0,S][e%2],[h,-h][e>>1]];else if(e<8)p=[[h,-h][e%2],[0,S][(e>>1)%2],t];else p=[[h,-h][e%2],t+h,[h,-h][(e>>1)%2]];const w=W(p[0]*1.02,p[1],p[2]*1.02);luz(w[0],w[1]+.004,w[2],k%2?0xffffff:0xffd98a,e+k*.6,3,.013)}}\n  const bx_=gx-s_*S*.95,by_=gy-c_*S*.95,RB=.085;for(let k=0;k<120","const RLp=[],RLc=[],_rc=new THREE.Color();const ORO=brillo(0xffd24a,.7);for(const[a,b,c]of[[S*1.01,S*1.01,S*.14],[S*.14,S*1.01,S*1.01]]){const m=new THREE.Mesh(new THREE.BoxGeometry(a,b,c),ORO);m.position.y=S/2;g.add(m)}\n  for(const s of[1,-1]){const l=new THREE.Mesh(new THREE.TorusGeometry(S*.2,S*.045,8,16),ORO);l.position.set(s*S*.17,S*1.12,0);l.rotation.y=Math.PI/2;l.rotation.z=s*.5;g.add(l)}\n  pon(g);const c_=Math.cos(g.rotation.y),s_=Math.sin(g.rotation.y);const W=(lx,ly,lz)=>[gx+lx*c_+lz*s_,z0+ly,gy-lx*s_+lz*c_];\n  for(let e=0;e<12;e++){for(let k=0;k<=16;k++){const t=(k/16-.5)*S;let p;const h=S/2;if(e<4)p=[t,[0,S][e%2],[h,-h][e>>1]];else if(e<8)p=[[h,-h][e%2],[0,S][(e>>1)%2],t];else p=[[h,-h][e%2],t+h,[h,-h][(e>>1)%2]];const w=W(p[0]*1.02,p[1],p[2]*1.02);RLp.push(w[0],w[1]+.004,w[2]);_rc.set(k%2?0xffffff:0xffd98a);RLc.push(_rc.r,_rc.g,_rc.b)}}\n  {const ge=new THREE.BufferGeometry();ge.setAttribute('position',new THREE.Float32BufferAttribute(RLp,3));ge.setAttribute('color',new THREE.Float32BufferAttribute(RLc,3));const pt=new THREE.Points(ge,new THREE.PointsMaterial({size:.028,map:ledTex(),vertexColors:true,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,toneMapped:false}));pt.frustumCulled=false;pon(pt);NAV.regaloG={x:gx,y:gy,caja,oro:ORO,leds:pt}}\n  const bx_=gx-s_*S*.95,by_=gy-c_*S*.95,RB=.085;for(let k=0;k<120")
r("const cil=(r1,r2,h,sg=10)=>new THREE.CylinderGeometry(r1,r2,h,sg),esf=","NAV.nieMat=NIE;const cil=(r1,r2,h,sg=10)=>new THREE.CylinderGeometry(r1,r2,h,sg),esf=")
r("{const OCU=[],ocu=","{NAV.munP=[];const OCU=[],ocu=")
r("const muneco=(p,rot)=>{const g=G(p,rot);","const muneco=(p,rot)=>{NAV.munP.push(p);const g=G(p,rot);")
# --- la misión: 2 arcos y después los tres adornos en este orden
r("LUZ.ruta=ord.map(luzArco);","LUZ.ruta=ord.slice(0,2).map(luzArco).concat(lucesEspeciales());")
r("function lucesSiguiente(){const a=LUZ.ruta[LUZ.i];if(!a){lucesFin();return}campDestino([a.nom,a.x,a.y]);REP.marca.visible=false;",
  "function lucesSiguiente(){const a=LUZ.ruta[LUZ.i];if(!a){lucesFin();return}campDestino([a.nom,a.x,a.y]);REP.marca.visible=!!a.tipo;if(a.tipo)setTimeout(()=>{if(LUZ.on&&LUZ.ruta[LUZ.i]===a)mostrar({munecos:'Ahora enciende los muñecos de nieve de Príncipe',regalo:'¡A por el regalo gigante de Gran Vía!',arbol:'Lo último: ¡el árbol gigante de Porta do Sol!'}[a.tipo])},500);")
r("function lucesEnciende(a){","function lucesEnciende(a){if(a.on)a.on(a);")
r("LUZ.i++;if(LUZ.i<n)setTimeout(()=>{if(REP.on&&!REP.fin&&LUZ.on)lucesSiguiente()},350);else setTimeout(lucesFin,600)}",
  "LUZ.i++;if(LUZ.i<n)setTimeout(()=>{if(REP.on&&!REP.fin&&LUZ.on)lucesSiguiente()},350);else if(a.tipo==='arbol')arbolCine(lucesFin);else setTimeout(lucesFin,600)}")
r("const enc=LUZ.arcos.filter(a=>a.lit)","const enc=LUZ.arcos.concat(LUZ.esp||[]).filter(a=>a.lit)")
r("LUZ.pl.forEach((l,i)=>{const a=enc[i];","LUZ.pl.forEach((l,i)=>{if(CINE.on&&i===3)return;const a=enc[i];")
r("else{LUZ.noche=false;","else{LUZ.noche=false;lucesEspRestore();")
r("function lucesTick(dt){if(!LUZ.arcos.length)return;LUZ.t+=dt;","function lucesTick(dt){if(CINE.on)cineTick(dt);for(const e of LUZ.esp||[])if(e.lit)e.t+=dt;if(!LUZ.arcos.length)return;LUZ.t+=dt;")
r("function lucesInicio(m){",r"""let _ledT=null;function ledTex(){if(_ledT)return _ledT;const c=document.createElement('canvas');c.width=c.height=64;const x=c.getContext('2d'),g=x.createRadialGradient(32,32,0,32,32,32);g.addColorStop(0,'rgba(255,255,255,1)');g.addColorStop(.25,'rgba(255,255,255,.85)');g.addColorStop(.6,'rgba(255,255,255,.18)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(0,0,64,64);_ledT=new THREE.CanvasTexture(c);return _ledT}
const ARB={x:87.45,y:18.0,H:2.2,RB:.25};const CINE={on:false};window.__CINE=CINE;
// muñecos, regalo y árbol: apagados al empezar; cada uno es un paso de la misión
function lucesEspeciales(){const L=[],N=NAV;
 if(N.nieMat){N.nieMat.emissiveIntensity=.02;N.nieMat.color.setHex(0xb8bcc8)}
 if(N.munP&&N.munP.length){const q=N.munP.slice().sort((a,b)=>a[0]-b[0])[Math.floor(N.munP.length/2)];L.push({tipo:'munecos',nom:'⛄ Muñecos de nieve · Príncipe',x:q[0],y:q[1],w:.26,lit:false,t:0,on(){if(N.nieMat){N.nieMat.color.setHex(0xffffff);N.nieMat.emissiveIntensity=.45}}})}
 if(N.regaloG){const R_=N.regaloG;R_.caja.material.emissiveIntensity=.03;R_.oro.emissiveIntensity=.05;R_.leds.visible=false;
  L.push({tipo:'regalo',nom:'🎁 Regalo gigante · Gran Vía',x:R_.x,y:R_.y,w:.32,lit:false,t:0,on(){R_.caja.material.emissiveIntensity=.6;R_.oro.emissiveIntensity=1.1;R_.leds.visible=true}})}
 if(N.arbolPts)N.arbolPts.visible=false;
 L.push({tipo:'arbol',nom:'🎄 Árbol de Porta do Sol',x:ARB.x,y:ARB.y,w:.5,lit:false,t:0});LUZ.esp=L;return L}
function lucesEspRestore(){const N=NAV;if(N.nieMat){N.nieMat.color.setHex(0xffffff);N.nieMat.emissiveIntensity=.25}if(N.regaloG){N.regaloG.caja.material.emissiveIntensity=.35;N.regaloG.oro.emissiveIntensity=.7;N.regaloG.leds.visible=true}
 if(N.arbolPts)N.arbolPts.visible=true;if(CINE.objs){for(const o of CINE.objs)scene.remove(o);CINE.objs=null}LUZ.esp=[]}
// cinemática del árbol: destello azul, LED en espiral de abajo arriba, la cámara gira y sube, y la estrella ilumina Vigo
function arbolCine(fin){const z0=groundMap(ARB.x,ARB.y),H=ARB.H,RB=ARB.RB,NL=1700,pos=new Float32Array(NL*3),rv=new Float32Array(NL),col=new Float32Array(NL*3),cc=new THREE.Color();
 const PAL=[0xffffff,0xbfe4ff,0x6fb8ff,0xffe39a,0xffffff,0xff7ad0];for(let k=0;k<NL;k++){const sp=k%8,t=Math.pow(((k>>3)+Math.random()*.6)/(NL/8),.9),a=t*34+sp*.785+Math.random()*.08,r_=RB*(1-t)*1.03+.006;
  pos.set([ARB.x+Math.cos(a)*r_,z0+.02+t*H,ARB.y+Math.sin(a)*r_],k*3);rv[k]=t*.94+Math.random()*.04;cc.setHex(PAL[k%PAL.length]);col.set([cc.r,cc.g,cc.b],k*3)}
 const ord=[...Array(NL).keys()].sort((a,b)=>rv[a]-rv[b]),P2=new Float32Array(NL*3),C2=new Float32Array(NL*3);ord.forEach((k,i)=>{P2.set(pos.subarray(k*3,k*3+3),i*3);C2.set(col.subarray(k*3,k*3+3),i*3)});
 const ge=new THREE.BufferGeometry();ge.setAttribute('position',new THREE.BufferAttribute(P2,3));ge.setAttribute('color',new THREE.BufferAttribute(C2,3));ge.setDrawRange(0,0);
 const U={uP:{value:0}};const pm=new THREE.PointsMaterial({size:.045,map:ledTex(),vertexColors:true,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,toneMapped:false,fog:false});
 const leds=new THREE.Points(ge,pm);leds.frustumCulled=false;leds.renderOrder=6;scene.add(leds);
 const sp=(c,s)=>{const m=new THREE.Sprite(new THREE.SpriteMaterial({map:ledTex(),color:c,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,fog:false,toneMapped:false}));m.scale.setScalar(s);scene.add(m);return m};
 const azul=sp(0x3f8cff,.1);azul.position.set(ARB.x,z0+H*.45,ARB.y);const est=sp(0xffe08a,.01);est.position.set(ARB.x,z0+H+.13,ARB.y);
 const estM=new THREE.Mesh(new THREE.OctahedronGeometry(.07,0),new THREE.MeshBasicMaterial({color:0xfff0b0,toneMapped:false}));estM.scale.set(.6,1,.25);estM.position.copy(est.position);estM.visible=false;scene.add(estM);
 if(!R.userData)R.userData={};if(!R.userData.cine){R.userData.cine=1;const r0=R.render.bind(R);R.render=(sc,c)=>{if(CINE.on&&c===pcam&&CINE.cp){c.up.set(0,1,0);c.position.copy(CINE.cp);c.lookAt(CINE.cl);c.fov=55;c.updateProjectionMatrix();c.updateMatrixWorld()}return r0(sc,c)}}
 if(!document.getElementById('cineCss')){const st=document.createElement('style');st.id='cineCss';st.textContent='body.cine #nHud,body.cine .bar,body.cine #pad,body.cine #aviso,body.cine #nPop,body.cine #minimapa,body.cine #vel,body.cine #bAcc{opacity:0!important;transition:opacity .4s}';document.head.appendChild(st)}
 document.body.classList.add('cine');LUZ.obj=.72;REP.marca.visible=false;CINE.ocu=scene.children.filter(o=>o.visible&&o.isMesh&&o.geometry&&o.geometry.parameters&&o.geometry.parameters.radialSegments===160);for(const o of CINE.ocu)o.visible=false;
 Object.assign(CINE,{on:true,t:0,z0,U,leds,azul,est,estM,fin,a0:Math.atan2(P.y-ARB.y,P.x-ARB.x),cp:new THREE.Vector3(),cl:new THREE.Vector3(),objs:[leds,azul,est,estM],star:false});
 try{bip(880,.3,.08);setTimeout(()=>bip(1320,.4,.06),150)}catch(e){}aviso('🎄 ¡Se enciende el árbol de Porta do Sol!',3,'cuenta')}
function cineTick(dt){const C=CINE;C.t+=dt;const t=C.t,z0=C.z0,H=ARB.H;P.v=0;
 // destello azul
 const fa=Math.min(1,t/1.1);C.azul.scale.setScalar(.2+4.5*fa);C.azul.material.opacity=t<1.4?1-Math.max(0,(t-.5)/.9):0;
 const l3=LUZ.pl&&LUZ.pl[3];if(l3){if(t<1.5){l3.color.setHex(0x3f8cff);l3.position.set(ARB.x,z0+H*.4,ARB.y);l3.distance=4;l3.intensity=12*(1-t/1.5)}else if(C.star){l3.color.setHex(0xffd690);l3.position.set(ARB.x,z0+H+.2,ARB.y);l3.intensity=6+2*Math.sin(t*4)}else l3.intensity=0}
 // los LED suben en espiral
 const up=Math.min(1,Math.max(0,(t-.6)/4.2));C.U.uP.value=up;C.leds.geometry.setDrawRange(0,Math.floor(C.leds.geometry.attributes.position.count*up));C.leds.material.opacity=.8+.2*Math.sin(t*9);if(up>0&&Math.floor(up*14)!==C.bq){C.bq=Math.floor(up*14);try{bip(600+C.bq*70,.06,.03)}catch(e){}}
 // la estrella
 if(t>4.9&&!C.star){C.star=true;C.estM.visible=true;LUZ.obj=1;LUZ.flash=.8;try{sonJoJo();setTimeout(()=>sonPublico(1.4),300);sonCampana(1,.5)}catch(e){}aviso('⭐ ¡Vigo ya brilla!',2.6,'cuenta')}
 if(C.star){const k=Math.min(1,(t-4.9)/.8);C.est.scale.setScalar(.05+.55*k+.06*Math.sin(t*5));C.estM.rotation.y+=dt*1.5;C.estM.scale.set(.6+.2*k,1+.3*k,.25)}
 // cámara: gira alrededor del árbol y sube con las luces; al final mira la estrella
 const an=C.a0+t*.38,rad=1.75-.25*Math.min(1,t/6),hy=z0+.95+Math.min(1,t/5)*(H*.75)+(C.star?.15:0);C.cp.set(ARB.x+Math.cos(an)*rad,hy,ARB.y+Math.sin(an)*rad);
 const lk=C.star?z0+H+.05:z0+.5+H*.8*Math.min(1,up+.05);C.cl.set(ARB.x,C.cl.y?C.cl.y+(lk-C.cl.y)*Math.min(1,dt*3):lk,ARB.y);
 if(t>8.2){C.on=false;document.body.classList.remove('cine');for(const o of C.ocu||[])o.visible=true;camInit=false;if(l3)l3.color.setHex(0xffd690);const f=C.fin;C.fin=null;if(f)f()}}
function lucesInicio(m){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok arbol')
