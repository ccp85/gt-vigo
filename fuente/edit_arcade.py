import re
f='index.html';S=open(f).read()
i=S.index("function navMundo(");j=S.index("function repMarca(")
pre,seg,post=S[:i],S[i:j],S[j:]
def rs(a,b):
    global seg
    assert seg.count(a)==1,(seg.count(a),a[:80]); seg=seg.replace(a,b)
# noria en la explanada de Vialia
rs("{const nx=100.55,ny=20.7,","{const nx=100.8,ny=18.95,")
# Príncipe más lleno de luz
rs("recorre(['Rúa do Príncipe'],.3,","recorre(['Rúa do Príncipe'],.16,")
# mercadillo grande + gente
rs(" // nube con todas las bombillas"," "+r"""// 9. mercadillo grande alrededor de la noria (explanada de Vialia) y muchísima gente en Vialia y en Príncipe
 {const NX=100.8,NY=18.95,X0=98.6,X1=103.6,Y0=17.6,Y1=22.8,pu=[];
  for(let x=X0;x<X1;x+=.17)for(let y=Y0;y<Y1;y+=.17){const px=x+(Math.random()-.5)*.05,py=y+(Math.random()-.5)*.05;if(cell(px,py).t!==1||!libre(px,py,.07)||Math.hypot(px-NX,py-NY)<.75)continue;if(Math.random()<.75)pu.push([px,py,Math.floor(Math.random()*4)*Math.PI/2])}
  if(pu.length>70)pu.length=70;const n=pu.length,du=new THREE.Object3D();
  const cuerpo=new THREE.InstancedMesh(new THREE.BoxGeometry(.11,.07,.08).translate(0,.035,0),M(0x8a5a2b,.85),n),
   techo=new THREE.InstancedMesh(new THREE.CylinderGeometry(.001,.068,.036,4,1).rotateY(Math.PI/4).translate(0,.088,0).scale(1.25,1,.95),new THREE.MeshStandardMaterial({color:0xffffff,roughness:.8,emissive:0x220808,emissiveIntensity:.4}),n),
   frente=new THREE.InstancedMesh(new THREE.PlaneGeometry(.09,.035).rotateY(Math.PI).translate(0,.042,-.0405),new THREE.MeshBasicMaterial({color:0xffc878,toneMapped:false,side:THREE.DoubleSide}),n),cc2=new THREE.Color();
  pu.forEach(([x,y,a],k)=>{du.position.set(x,groundMap(x,y),y);du.rotation.set(0,a,0);du.updateMatrix();cuerpo.setMatrixAt(k,du.matrix);techo.setMatrixAt(k,du.matrix);frente.setMatrixAt(k,du.matrix);techo.setColorAt(k,cc2.set([0xc4161f,0xf6f4ee,0x1f8a3c,0xc4161f][k%4]));
   const c_=Math.cos(a),s_=Math.sin(a);if(k%2===0)for(let q=0;q<=6;q++){const t=q/6-.5,lx=t*.11,lz=-.046;luz(x+lx*c_+lz*s_,groundMap(x,y)+.072,y-lx*s_+lz*c_,q%2?0xffd98a:0xff5a4a,q+k,2,.009)}});
  for(const m of[cuerpo,techo,frente]){m.castShadow=true;pon(m)}
  // gente: en la explanada, alrededor de los puestos, y llenando la calle del Príncipe
  const G=[];const lejosPuesto=(x,y)=>pu.every(p=>Math.hypot(p[0]-x,p[1]-y)>.075);
  for(let x=X0;x<X1;x+=.05)for(let y=Y0;y<Y1;y+=.05){const px=x+(Math.random()-.5)*.04,py=y+(Math.random()-.5)*.04;if(Math.random()<.45&&cell(px,py).t===1&&libre(px,py,.012)&&Math.hypot(px-NX,py-NY)>.2&&lejosPuesto(px,py))G.push([px,py])}
  if(G.length>650)G.length=650;
  if(CALLES)for(const[nm,c,ls]of CALLES){if(nm!=='Rúa do Príncipe'&&nm!=='Porta do Sol')continue;for(const l of ls){for(let i=0;i+3<l.length;i+=2){const ax=l[i],ay=l[i+1],bx=l[i+2],by=l[i+3],L=Math.hypot(bx-ax,by-ay);if(L<1e-6)continue;const nx=-(by-ay)/L,ny=(bx-ax)/L;
   for(let s=0;s<L;s+=.022)for(let q=0;q<3;q++){const lat=(Math.random()*2-1)*.085,x=ax+(bx-ax)*s/L+nx*lat+(Math.random()-.5)*.01,y=ay+(by-ay)*s/L+ny*lat;const t=cell(x,y).t;if(t!==3&&t!==0&&t!==-1&&Math.random()<.8)G.push([x,y])}}}}
  const N=G.length,ROPA=[0xc4161f,0x1f3f8a,0x2a2b30,0x1f8a3c,0xf2c230,0x7a2a8a,0xe8e2d4,0x8a4a22,0x3a8ac4,0xd9622b],PIEL=[0xf0c8a8,0xe0b090,0xc68e6a,0x8a5a3a,0x5a3a26];
  const ab=new THREE.InstancedMesh(new THREE.CylinderGeometry(.0062,.0085,.026,6).translate(0,.013,0),new THREE.MeshStandardMaterial({roughness:.8}),N),
   ca=new THREE.InstancedMesh(new THREE.SphereGeometry(.0056,8,6).translate(0,.0315,0),new THREE.MeshStandardMaterial({roughness:.7}),N),
   go=new THREE.InstancedMesh(new THREE.ConeGeometry(.0058,.013,6).translate(0,.042,0),new THREE.MeshStandardMaterial({color:0xd51f1f,roughness:.7}),N);let ng=0;
  G.forEach(([x,y],k)=>{const s=.9+Math.random()*.3;du.position.set(x,groundMap(x,y),y);du.rotation.set(0,Math.random()*6.28,0);du.scale.set(s,s,s);du.updateMatrix();ab.setMatrixAt(k,du.matrix);ca.setMatrixAt(k,du.matrix);
   ab.setColorAt(k,cc2.set(ROPA[Math.floor(Math.random()*ROPA.length)]));ca.setColorAt(k,cc2.set(PIEL[Math.floor(Math.random()*PIEL.length)]));if(Math.random()<.3)go.setMatrixAt(ng++,du.matrix)});
  go.count=ng;for(const m of[ab,ca,go])pon(m);NAV.gente=N}
 // nube con todas las bombillas""")
S=pre+seg+post
s=S
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
# zona del reparto en coche: solo el centro (Urzáiz, Príncipe, Policarpo Sanz, Alameda, Gran Vía y Vialia)
r("REP_MIN=2.8,REP_MAX=7,","REP_MIN=1.8,REP_MAX=5,")
r("const REP_C1=[91,18.5,2.8],","const repEnZona=(x,y)=>x>87.3&&x<104.6&&y>14.6&&y<24.6;\nconst REP_C1=[91,18.5,2.8],")
r("if(Math.hypot(x-REP_C2[0],y-REP_C2[1])<REP_C2[2]&&esCalzada(x,y))out.push([n,+x.toFixed(2),+y.toFixed(2)]);","if(repEnZona(x,y)&&esCalzada(x,y))out.push([n,+x.toFixed(2),+y.toFixed(2),(bx-ax)/L,(by-ay)/L]);")
r("for(const d of REP_PUNTOS)if(Math.hypot(d[1]-REP_C2[0],d[2]-REP_C2[1])<REP_C2[2])out.push(d);","for(const d of REP_PUNTOS)if(repEnZona(d[1],d[2]))out.push(d);")
# marca de entrega más visible
r("function repMarca(){const g=new THREE.Group();const S=.05;","function repMarca(){const g=new THREE.Group();const S=.075;")
r("const col=new THREE.Mesh(new THREE.CylinderGeometry(.045,.07,1.6,20,1,true),new THREE.MeshBasicMaterial({color:0xffd24a,transparent:true,opacity:.28,side:THREE.DoubleSide,depthWrite:false,blending:THREE.AdditiveBlending,toneMapped:false}));col.position.y=.8;",
  "const col=new THREE.Mesh(new THREE.CylinderGeometry(.06,.09,3.2,20,1,true),new THREE.MeshBasicMaterial({color:0xffd24a,transparent:true,opacity:.42,side:THREE.DoubleSide,depthWrite:false,toneMapped:false}));col.position.y=1.6;\n const flecha=new THREE.Mesh(new THREE.ConeGeometry(.06,.12,4).rotateX(Math.PI),new THREE.MeshBasicMaterial({color:0x1f7bff,toneMapped:false}));flecha.position.y=.36;const fb=new THREE.Mesh(new THREE.ConeGeometry(.072,.14,4).rotateX(Math.PI),new THREE.MeshBasicMaterial({color:0xffffff,toneMapped:false,side:THREE.BackSide}));flecha.add(fb);")
r("const aro=new THREE.Mesh(new THREE.RingGeometry(.13,.17,40),","const aro=new THREE.Mesh(new THREE.RingGeometry(.17,.23,40),")
r("const G=new THREE.Group();G.add(g,col,aro);G.userData={g,aro};","const G=new THREE.Group();G.add(g,col,aro,flecha);G.userData={g,aro,flecha};")
r(" const m=REP.marca;if(m&&m.visible){"," const m=REP.marca;if(m&&m.visible){m.userData.flecha.position.y=.36+Math.abs(Math.sin(NAV.uT.value*4))*.06;m.userData.flecha.rotation.y+=dt*2;")
# nunca choca: al tocar una pared el coche se endereza a lo largo de la calle sin perder velocidad
r("if(vn<0){if(Math.abs(P.v)>.35&&MODO!=='pie')golpe();","if(vn<0&&REP.on&&MODO==='coche'){const tx=-n[1],ty=n[0],sg=(Math.cos(P.a)*tx-Math.sin(P.a)*ty)>=0?1:-1,ta=Math.atan2(-ty*sg,tx*sg);P.a+=Math.atan2(Math.sin(ta-P.a),Math.cos(ta-P.a))*Math.min(1,dt*12);dx_-=n[0]*vn;dy_-=n[1]*vn;P.v=Math.max(P.v,.25)}\n  else if(vn<0){if(Math.abs(P.v)>.35&&MODO!=='pie')golpe();")
r("if(bl!==br)P.a+=(br>bl?1:-1)*1.3*dt*Math.min(1,P.v*2)}","if(bl!==br)P.a+=(br>bl?1:-1)*(REP.on?4:1.3)*dt*Math.min(1,P.v*2)}")
r("const vmax=PIE?.24:MOTO?.95:Math.min(road?1.05:.6,LIM?LIM/125:9);","const vmax=PIE?.24:MOTO?.95:Math.min(road?1.05:.6,LIM?LIM/125:9)*(REP.on&&REP.boost>0?1.5:1);")
# monedas y regalos sorpresa por las calles (solo en coche)
r("function repSiguiente(){","""// arcade: filas de monedas y regalos sorpresa (turbo) por las calles de la zona; reaparecen al rato
function repArcade(){const pool=repPool().filter(d=>d.length>4),du=new THREE.Object3D();REP.mon=0;REP.boost=0;
 const C=[];for(let k=0;k<60&&pool.length;k++){const d=pool[Math.floor(Math.random()*pool.length)];if(C.some(c=>Math.hypot(c.x-d[1],c.y-d[2])<.4))continue;for(let q=-2;q<=2;q++){const x=d[1]+d[3]*q*.07,y=d[2]+d[4]*q*.07;if(cell(x,y).t===2||cell(x,y).t===4)C.push({x,y,z:groundY(x,y)+.035,on:true,t:0})}}
 const mc=new THREE.InstancedMesh(new THREE.CylinderGeometry(.018,.018,.005,18).rotateX(Math.PI/2),new THREE.MeshStandardMaterial({color:0xffc21f,emissive:0xb07800,emissiveIntensity:.7,metalness:.8,roughness:.25}),C.length);mc.frustumCulled=false;scene.add(mc);REP.objs.push(mc);
 const R=[];for(let k=0;k<22&&pool.length;k++){const d=pool[Math.floor(Math.random()*pool.length)];if(R.some(c=>Math.hypot(c.x-d[1],c.y-d[2])<.8)||C.some(c=>Math.hypot(c.x-d[1],c.y-d[2])<.12))continue;R.push({x:d[1],y:d[2],z:groundY(d[1],d[2])+.04,on:true,t:0})}
 const cajaG=new THREE.BoxGeometry(.04,.04,.04),rc=new THREE.InstancedMesh(cajaG,new THREE.MeshStandardMaterial({color:0x1fae4a,emissive:0x0f6a2a,emissiveIntensity:.8}),R.length),lz=new THREE.InstancedMesh(new THREE.BoxGeometry(.043,.043,.012),new THREE.MeshStandardMaterial({color:0xffd24a,emissive:0xffb800,emissiveIntensity:.9}),R.length*2);
 for(const m of[rc,lz]){m.frustumCulled=false;scene.add(m);REP.objs.push(m)}REP.arc={C,R,mc,rc,lz,du};repArcadeTick(0)}
function repArcadeTick(dt){const A=REP.arc;if(!A)return;const du=A.du,t=NAV.uT.value,cs=Math.cos(P.a),sn=-Math.sin(P.a);let ch=false;
 A.C.forEach((c,i)=>{if(!c.on){c.t-=dt;if(c.t<=0)c.on=true}if(c.on&&Math.hypot(c.x-P.x,c.y-P.y)<.075){c.on=false;c.t=25;REP.mon++;ch=true;if(!REP.sT||t-REP.sT>.07){REP.sT=t;try{sonMoneda()}catch(e){}}}
  if(c.f===undefined||Math.abs(c.x-P.x)+Math.abs(c.y-P.y)<2.5||c.f!==c.on){c.f=c.on;du.position.set(c.x,c.z+Math.sin(t*3+i)*.006,c.y);du.rotation.set(0,t*3+i*.3,0);du.scale.setScalar(c.on?1:0.0001);du.updateMatrix();A.mc.setMatrixAt(i,du.matrix)}});A.mc.instanceMatrix.needsUpdate=true;
 A.R.forEach((c,i)=>{if(!c.on){c.t-=dt;if(c.t<=0)c.on=true}if(c.on&&Math.hypot(c.x-P.x,c.y-P.y)<.1){c.on=false;c.t=40;REP.mon+=5;REP.boost=1.8;ch=true;try{sonCaja()}catch(e){}aviso('🎁 ¡Turbo navideño! +5 🪙',1,'peq')}
  const s=c.on?1:0.0001;du.position.set(c.x,c.z+Math.sin(t*2.5+i)*.012,c.y);du.rotation.set(0,t*1.5+i,0);du.scale.setScalar(s);du.updateMatrix();A.rc.setMatrixAt(i,du.matrix);A.lz.setMatrixAt(i*2,du.matrix);du.rotation.y+=Math.PI/2;du.updateMatrix();A.lz.setMatrixAt(i*2+1,du.matrix)});
 A.rc.instanceMatrix.needsUpdate=A.lz.instanceMatrix.needsUpdate=true;
 if(REP.boost>0){REP.boost-=dt;P.v=Math.min(P.v+2.2*dt,1.55)}if(ch)repHud()}
function repSiguiente(){""")
r(" REP.dest=null;REP.ult=[];REP.ent=0;REP.fin=false;REP.guardado=false;REP.on=true;"," REP.dest=null;REP.ult=[];REP.ent=0;REP.mon=0;REP.boost=0;REP.arc=null;REP.fin=false;REP.guardado=false;REP.on=true;if(!REP.heli)repArcade();")
r("if(NAV.tr&&REP.spec)navEstela(","if(!REP.heli&&!REP.fin)repArcadeTick(dt);\n if(NAV.tr&&REP.spec)navEstela(")
r("+(REP.heli&&d&&dd<.8?'<span class=\"r ok\">⤓ Aterriza</span>':'')}","+(REP.heli&&d&&dd<.8?'<span class=\"r ok\">⤓ Aterriza</span>':'')+(REP.heli?'':`<span class=\"r\">🪙 ${REP.mon||0}</span>`)}")
r("`<span class=\"t\">🎁 ${REP.ent}</span>`+(rec?`<span class=\"r\">🏆 ${rec.r}</span>`:'')","`<span class=\"t\">🎁 ${REP.ent}</span>`+(rec?`<span class=\"r\">🏆 ${rec.r}</span>`:'')")
# récords con monedas
r("function repGuardar(nombre,n){const a=repRecords();a.push({n:nombre.slice(0,18),r:n,f:Date.now()});a.sort((p,q)=>q.r-p.r||p.f-q.f);","function repGuardar(nombre,n,m=0){const a=repRecords();a.push({n:nombre.slice(0,18),r:n,m,f:Date.now()});a.sort((p,q)=>q.r-p.r||(q.m||0)-(p.m||0)||p.f-q.f);")
r("<b>🎁 ${e.r}</b></li>","<b>🎁 ${e.r}${e.m?' · 🪙 '+e.m:''}</b></li>")
r("const top=repGuardar(nm,REP.ent);","const top=repGuardar(nm,REP.ent,REP.mon||0);")
r("`Has repartido <b>${REP.ent}</b> ${REP.ent===1?'regalo':'regalos'}.`","`Has repartido <b>${REP.ent}</b> ${REP.ent===1?'regalo':'regalos'}`+(REP.mon?` y recogido <b>${REP.mon}</b> 🪙`:'')+'.'")
r("if(REP.guardado){REP.ent=0;REP.guardado=false}","if(REP.guardado){REP.ent=0;REP.mon=0;REP.guardado=false}")
r("heliDesvestir();REP.heli=false;REP.chim=null;","heliDesvestir();REP.heli=false;REP.chim=null;REP.arc=null;REP.boost=0;")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok arcade')
