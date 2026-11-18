import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
def rx(pat,b):
    global s
    m=list(re.finditer(pat,s,re.S));assert len(m)==1,(len(m),pat[:60]);s=s[:m[0].start()]+b+s[m[0].end():]
C="(REP.red&&!REP.heli)"
# ---------- noria y mercado en el punto marcado (explanada junto al final de la autopista, en Vialia) ----------
i=s.index("function navMundo(");j=s.index("function repMarca(")
pre,seg,post=s[:i],s[i:j],s[j:]
def rs(a,b):
    global seg
    assert seg.count(a)==1,(seg.count(a),a[:80]); seg=seg.replace(a,b)
rs("{const nx=100.8,ny=18.95,","{const nx=108.3,ny=16.6,")
rs("{const NX=100.8,NY=18.95,X0=98.8,X1=103,Y0=18.05,Y1=20,pu=[];","{const NX=108.3,NY=16.6,X0=106.1,X1=110.5,Y0=14.8,Y1=18.5,pu=[];")
# puestos de comida y de regalos (cosas sobre el mostrador)
rs("for(const m of[cuerpo,techo,frente]){m.castShadow=true;pon(m)}","""for(const m of[cuerpo,techo,frente]){m.castShadow=true;pon(m)}
  {const nR=pu.filter((_,k)=>k%2===0).length*3,nC=pu.filter((_,k)=>k%2===1).length;const caj=new THREE.InstancedMesh(new THREE.BoxGeometry(.016,.016,.016),new THREE.MeshStandardMaterial({roughness:.5,emissive:0x222222}),Math.max(1,nR)),
   olla=new THREE.InstancedMesh(new THREE.CylinderGeometry(.014,.012,.012,10),new THREE.MeshStandardMaterial({color:0x3a3a40,metalness:.6,roughness:.4}),Math.max(1,nC)),fue=new THREE.InstancedMesh(new THREE.SphereGeometry(.009,8,6),new THREE.MeshBasicMaterial({color:0xff8a2a,toneMapped:false}),Math.max(1,nC)),cartel=new THREE.InstancedMesh(new THREE.PlaneGeometry(.07,.016),new THREE.MeshBasicMaterial({toneMapped:false,side:THREE.DoubleSide}),pu.length);
   let a_=0,b_=0;const CR=[0xd51f1f,0x1fae4a,0xf2c230,0x1f6fd0,0xc23fd0];pu.forEach(([x,y,a],k)=>{const z0=groundMap(x,y),c_=Math.cos(a),s_=Math.sin(a),L=(lx,ly,lz)=>[x+lx*c_+lz*s_,z0+ly,y-lx*s_+lz*c_];
    const pc=L(0,.112,-.036);du.position.set(pc[0],pc[1],pc[2]);du.rotation.set(0,a,0);du.scale.set(1,1,1);du.updateMatrix();cartel.setMatrixAt(k,du.matrix);cartel.setColorAt(k,cc2.set(k%2?0xff9a3a:0x3fd07a));
    if(k%2===0){for(let q=0;q<3;q++){const p=L(-.025+q*.025,.078,-.03);du.position.set(p[0],p[1],p[2]);du.rotation.set(0,a+q,0);du.updateMatrix();caj.setMatrixAt(a_,du.matrix);caj.setColorAt(a_,cc2.set(CR[(k+q)%5]));a_++}}
    else{const p=L(0,.078,-.03);du.position.set(p[0],p[1],p[2]);du.rotation.set(0,0,0);du.updateMatrix();olla.setMatrixAt(b_,du.matrix);du.position.y+=.012;du.updateMatrix();fue.setMatrixAt(b_,du.matrix);b_++}});
   caj.count=a_;olla.count=fue.count=b_;for(const m of[caj,olla,fue,cartel])pon(m)}""")
# gente paseando por el mercado
rs("if(G.length>650)G.length=650;","""if(G.length>650)G.length=650;
  {const GW=G.splice(0,Math.min(330,Math.floor(G.length*.6))),M_=GW.length,ROP=[0xc4161f,0x1f3f8a,0x2a2b30,0x1f8a3c,0xf2c230,0x7a2a8a,0xe8e2d4,0x8a4a22,0x3a8ac4,0xd9622b],PI_=[0xf0c8a8,0xe0b090,0xc68e6a,0x8a5a3a];
   const wb=new THREE.InstancedMesh(new THREE.CylinderGeometry(.0062,.0085,.026,6).translate(0,.013,0),new THREE.MeshStandardMaterial({roughness:.8}),M_),wc=new THREE.InstancedMesh(new THREE.SphereGeometry(.0056,8,6).translate(0,.0315,0),new THREE.MeshStandardMaterial({roughness:.7}),M_);
   const W_=GW.map(([x,y],k)=>{wb.setColorAt(k,cc2.set(ROP[k%ROP.length]));wc.setColorAt(k,cc2.set(PI_[k%PI_.length]));return{x,y,tx:x,ty:y,sp:.012+Math.random()*.012,ph:Math.random()*6.28,a:0}});
   for(const m of[wb,wc]){m.frustumCulled=false;pon(m)}NAV.paseo={W:W_,P:GW.concat(G.slice(0,200)),wb,wc,du:new THREE.Object3D()}}""")
s=pre+seg+post
r("function navTick(dt){","""function navPaseo(dt){const Q=NAV.paseo;if(!Q)return;const du=Q.du,t=NAV.uT.value;Q.W.forEach((w,k)=>{const dx=w.tx-w.x,dy=w.ty-w.y,d=Math.hypot(dx,dy);if(d<.01){const p=Q.P[Math.floor(Math.random()*Q.P.length)];if(Math.hypot(p[0]-w.x,p[1]-w.y)<.5){w.tx=p[0];w.ty=p[1]}}else{const st=Math.min(d,w.sp*dt);w.x+=dx/d*st;w.y+=dy/d*st;w.a=Math.atan2(dx,dy)}
 du.position.set(w.x,groundMap(w.x,w.y)+Math.abs(Math.sin(t*9+w.ph))*.003,w.y);du.rotation.set(0,w.a,0);du.updateMatrix();Q.wb.setMatrixAt(k,du.matrix);Q.wc.setMatrixAt(k,du.matrix)});Q.wb.instanceMatrix.needsUpdate=Q.wc.instanceMatrix.needsUpdate=true}
function navTick(dt){navPaseo(dt);""")
r("function navQuitar(){NAV.angeles=null;","function navQuitar(){NAV.angeles=null;NAV.paseo=null;")
# ---------- helicóptero con sonido de rotor bien fuerte ----------
r("function navSonidos(dt,zonaGente){","""function sonRotor(on,v){if(!AC)return;if(!SFX.r){if(!soundOn||!on)return;const s_=AC.createBufferSource();s_.buffer=NB;s_.loop=true;const fl=AC.createBiquadFilter();fl.type='lowpass';fl.frequency.value=480;const am=AC.createGain();am.gain.value=.5;const lfo=AC.createOscillator();lfo.frequency.value=11;const lg=AC.createGain();lg.gain.value=.5;lfo.connect(lg);lg.connect(am.gain);
 const o=AC.createOscillator();o.type='triangle';o.frequency.value=52;const og=AC.createGain();og.gain.value=.4;const g=AC.createGain();g.gain.value=0;s_.connect(fl);fl.connect(am);o.connect(og);og.connect(am);am.connect(g);g.connect(master);s_.start();lfo.start();o.start();SFX.r={g,lfo,o}}
 const t=AC.currentTime,act=on&&soundOn,a=Math.min(1,Math.abs(v||0));SFX.r.lfo.frequency.setTargetAtTime(10+a*5,t,.2);SFX.r.o.frequency.setTargetAtTime(50+a*14,t,.2);SFX.r.g.gain.setTargetAtTime(act?.7:0,t,.15)}
function navSonidos(dt,zonaGente){""")
r("if(!REP.heli&&!REP.fin)navSonidos(dt,repEnZona(P.x,P.y));else sonMotor(0,false);","if(!REP.heli&&!REP.fin)navSonidos(dt,repEnZona(P.x,P.y));else sonMotor(0,false);sonRotor(REP.heli&&!REP.fin,P.v);")
r("function salirReparto(menu=true){sonMotor(0,false);","function salirReparto(menu=true){sonMotor(0,false);sonRotor(false);")
# ---------- misión de la carroza: un solo regalo; se recoge en Policarpo Sanz, se entrega lejos y se vuelve a por otro ----------
r("function repPila(){","""const REP_DEP=['Policarpo Sanz · almacén de regalos',90.6,17.86];
function repTiempo(){const L=GPS.on&&GPS.acc?GPS.acc[GPS.acc.length-1]:Math.hypot(REP.dest[1]-P.x,REP.dest[2]-P.y)*1.4;return Math.round(10+L*1.5)}
function repMarcaColor(c){REP.marca.traverse(o=>{if(o.isMesh&&(o.geometry.type==='CylinderGeometry'||o.geometry.type==='RingGeometry')&&o.material&&o.material.transparent)o.material.color.setHex(c)})}
function repMisionNueva(ini){REP.fase='entregar';REP.carga=1;repPila();const d=repElegir();REP.dest=d;REP.ult.push([d[1],d[2]]);if(REP.ult.length>5)REP.ult.shift();REP.marca.position.set(d[1],groundY(d[1],d[2]),d[2]);REP.marca.visible=true;repMarcaColor(0xffd24a);
 gpsIniciar(d);REP.t=repTiempo();if(!ini)repPop('🎁 ¡Regalo cargado! ⏱ '+REP.t+' s','aviso');repHud()}
function repVolver(){REP.fase='recoger';REP.dest=REP_DEP;REP.marca.position.set(REP_DEP[1],groundY(REP_DEP[1],REP_DEP[2]),REP_DEP[2]);repMarcaColor(0x3fe07a);gpsParar();gpsIniciar(REP_DEP);REP.t=repTiempo();repHud()}
function repMision(){const d=REP.dest;if(!d||REP.fin||Math.hypot(d[1]-P.x,d[2]-P.y)>.28)return;
 if(REP.fase==='entregar'){const bon=Math.max(0,Math.round(REP.t)),pts=100+bon*10;REP.pts+=pts;REP.ent++;REP.nEnt=(REP.nEnt||0)+1;REP.carga=0;repPila();try{sonCaja();setTimeout(sonJoJo,260);setTimeout(()=>sonPublico(1),700);confeti()}catch(e){}REP.shake=.5;repPop('+'+pts+' ⭐','gran');repVolver();setTimeout(()=>aviso('↩️ Vuelve a Policarpo Sanz a por otro regalo',1.6,'peq'),1300)}
 else{try{sonCaja()}catch(e){}repMisionNueva(false)}}
function repPila(){""")
rx(r"function repElegir\(\)\{if\(REP\.red&&!REP\.heli\)\{.*?return repElegir0\(\)\}","""function repElegir(){if(REP.red&&!REP.heli){const pool=repPool(),k=REP.nEnt||0,mn=Math.min(9,5+.3*k),mx=Math.min(13,7+.5*k),dd=d=>Math.hypot(d[1]-REP_DEP[1],d[2]-REP_DEP[2]);
  let L=pool.filter(d=>{const e=dd(d);return e>mn&&e<mx&&!REP.ult.some(u=>Math.hypot(u[0]-d[1],u[1]-d[2])<.8)});if(!L.length)L=pool.filter(d=>dd(d)>3);if(!L.length)L=pool;return L[Math.floor(Math.random()*L.length)]}
 return repElegir0()}""")
r(" else if(d&&Math.hypot(d[1]-P.x,d[2]-P.y)<.28)repEntrega();"," else if(REP.red)repMision();\n else if(d&&Math.hypot(d[1]-P.x,d[2]-P.y)<.28)repEntrega();")
r("repSiguiente();aviso('🎄 ¡A repartir!',1.4,'cuenta');","if("+C+")repMisionNueva(true);else repSiguiente();aviso('🎄 ¡A repartir!',1.4,'cuenta');")
r("REP.on=true;REP.pool=null;REP.red=null;GPSF=null;REP.nEnt=0;if(!REP.heli){P.x=90.6;P.y=17.86;P.a=0;P.v=0;","REP.on=true;REP.pool=null;REP.red=null;GPSF=null;REP.nEnt=0;REP.fase='entregar';if(!REP.heli){P.x=90.6;P.y=17.86;P.a=0;P.v=0;")
r("const R=[];for(let k=0;k<90&&pool.length&&R.length<36;k++){","const R=[];for(let k=0;k<90&&pool.length&&R.length<0;k++){")
# GPS de verdad por las calles de Vigo (grafo de calles con sus sentidos), no la rejilla del centro
r("function gpsCalcular(x,y,tx,ty){if(REP.on&&REP.red&&!REP.heli){","function gpsCalcular(x,y,tx,ty){if(REP.on&&REP.red&&!REP.heli&&REP.cerrado){")
r("mostrar('▲ acelera · ◀ ▶ gira · recoge regalos y llévalos a la marca')","mostrar('▲ acelera · ◀ ▶ gira · sigue el GPS y lleva el regalo a la marca dorada')")
# HUD de la misión
rx(r"if\(\(REP\.red&&!REP\.heli\)\)\{el\.querySelector\('\.cnt'\)\.innerHTML=.*?;return\}","""if((REP.red&&!REP.heli)){el.querySelector('.cnt').innerHTML=`<span class="t ${REP.t<15?'poco':''}">⏱ ${fmtS(Math.max(0,REP.t))}</span><span class="t">⭐ ${REP.pts}</span><span class="r">🎁 ${REP.ent}</span><span class="r ${REP.fase==='recoger'?'ok':''}">${REP.fase==='recoger'?'↩️ Policarpo Sanz':'📍'} ${d?fmtD(dd):'—'}</span>`;return}""")
r("el.querySelector('h3').textContent=acabado?'🕛 ¡Medianoche!'","el.querySelector('h3').textContent=acabado?'⏱ ¡Se acabó el tiempo!'")
r("if(acabado)sonCampana(12,.55)","if(acabado)sonCampana(3,.7)")
r("'Recoge regalos y repártelos antes de medianoche'","'Recoge el regalo en Policarpo Sanz y llévalo antes de que se acabe el tiempo'")
r("Object.assign(REP,{cap:ra.cap,turD:ra.tur,cmb:ra.cmb,giro:ra.giro,t:REP_T0,pts:0,carga:0,mul:1,ct:0,ultMin:false,shake:0});","Object.assign(REP,{cap:1,turD:ra.tur,cmb:ra.cmb,giro:ra.giro,t:REP_T0,pts:0,carga:0,mul:1,ct:0,ultMin:true,shake:0});")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok mision')
