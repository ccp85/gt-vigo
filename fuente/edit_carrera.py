import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------- menú: modo Reparto o Carrera ----------
r('<div class="opt nveh"><span>Vehículo</span>','<div class="opt nveh"><span>Modo</span><button data-modo="0">🎁 Reparto</button><button data-modo="1">🏁 Carrera</button></div>\n<div class="opt nveh nvr"><span>Vehículo</span>')
r("sel:{c:0,col:0,vueltas:1,dif:1,hora:1,traz:1,veh:0}","sel:{c:0,col:0,vueltas:1,dif:1,hora:1,traz:1,veh:0,modo:0}")
r("el.querySelectorAll('[data-veh]').forEach(b=>b.onclick=()=>{RACE.sel.veh=+b.dataset.veh;pintarSel()});","el.querySelectorAll('[data-veh]').forEach(b=>b.onclick=()=>{RACE.sel.veh=+b.dataset.veh;pintarSel()});el.querySelectorAll('[data-modo]').forEach(b=>b.onclick=()=>{RACE.sel.modo=+b.dataset.modo;pintarSel()});")
r("el.querySelector('.go').textContent=RACE.nav?'🎁 ¡A repartir!':'🏁 ¡A correr!';",
  "el.querySelector('.go').textContent=RACE.nav?'🎁 ¡A repartir!':'🏁 ¡A correr!';{const NC=RACE.nav&&s.modo===1;el.querySelector('.nvr').style.display=NC?'none':'';if(NC){el.querySelector('[data-v]').parentNode.style.display=el.querySelector('[data-d]').parentNode.style.display='';el.querySelector('.go').textContent='🏁 ¡A correr!';el.querySelector('h3').textContent='🏁 Carrera de Navidad · Vigo 2026';el.querySelector('.sub').textContent='Vialia · García Barbón · Alameda · Policarpo Sanz · Porta do Sol · Príncipe · Urzáiz'}}el.querySelectorAll('[data-modo]').forEach(b=>b.classList.toggle('on',+b.dataset.modo===(s.modo||0)));")
r("fd.querySelector('span').textContent=RACE.nav?'Tiempo':'Rivales';fd.querySelectorAll('[data-d]').forEach((b,i)=>b.textContent=RACE.nav?","fd.querySelector('span').textContent=RACE.nav&&s.modo!==1?'Tiempo':'Rivales';fd.querySelectorAll('[data-d]').forEach((b,i)=>b.textContent=RACE.nav&&s.modo!==1?")
r(" if(RACE.nav){const r_=repRecords(!!s.veh)[0];"," if(RACE.nav&&s.modo!==1){const r_=repRecords(!!s.veh)[0];")
r("if(RACE.nav)empezarReparto();else empezarCarrera()}","if(RACE.nav&&RACE.sel.modo!==1)empezarReparto();else empezarCarrera()}")
# la carrera de Navidad usa la misma decoración que el reparto (árbol gigante, noria en la estación, mercadillo, angelitos, pancartas, figuras)
r("if(RACE.nav)navDecorado(objs)","if(RACE.nav)navMundo(objs)")
# ---------- figuras de la Navidad de Vigo según las referencias ----------
i=s.index("function navMundo(");j=s.index("function repMarca(")
pre,seg,post=s[:i],s[i:j],s[j:]
def rs(a,b):
    global seg
    assert seg.count(a)==1,(seg.count(a),a[:80]); seg=seg.replace(a,b)
rs(" // halos de luz (pocos) alrededor de las luces principales"," "+r"""// 11. figuras de la Navidad de Vigo: bosque de luz en Porta do Sol, renos y trineos de luz en Príncipe, bola de nieve con oso polar,
 //     globo con Papá Noel, Casa de Papá Noel en Policarpo Sanz, muñeco de nieve gigante y Estrella Polar en García Barbón, bola gigante de Urzáiz, mercado de la Alameda
 {const sitio=(x,y,r=.04)=>{for(let k=0;k<60;k++){const a=k*2.4,d=k*.01,px=x+Math.cos(a)*d,py=y+Math.sin(a)*d,t=cell(px,py).t;if((t===1||t===5)&&libre(px,py,r))return[px,py]}return[x,y]};
  const LZ=c=>new THREE.MeshBasicMaterial({color:c,toneMapped:false}),ST=(c,e=0,r=.6,m=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r,metalness:m,emissive:c,emissiveIntensity:e});
  const G=(p,rot=0,dz=0)=>{const g=new THREE.Group();g.position.set(p[0],groundMap(p[0],p[1])+dz,p[1]);g.rotation.y=rot;pon(g);return g};
  const add=(g,geo,mat,x,y,z,rx=0,ry=0,rz=0)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.rotation.set(rx,ry,rz);g.add(m);return m};
  const ORO=LZ(0xffe6a0),BL=LZ(0xf4f8ff);
  // bosque de luz: 10 árboles luminosos alrededor del árbol gigante
  for(let k=0;k<10;k++){const a=k/10*6.283+.3,p=sitio(87.45+Math.cos(a)*.62,18+Math.sin(a)*.62,.03),z0=groundMap(p[0],p[1]);for(let q=0;q<46;q++){const t=q/46,r=.035*(1-t)+.002,b=t*22;luz(p[0]+Math.cos(b)*r,z0+.01+t*.14,p[1]+Math.sin(b)*r,k%2?0xbfe4ff:0xffffff,q*.3+k,3,.011)}luz(p[0],z0+.16,p[1],0xffe9a0,k,2,.022);halo(p[0],z0+.15,p[1],k%2?0x9fd0ff:0xfff2c0,.12)}
  // renos de luz (blanco y dorado)
  const reno=(p,rot,M_)=>{const g=G(p,rot),cil=(l,r_=.0035)=>new THREE.CylinderGeometry(r_,r_,l,6);add(g,cil(.05,.009),M_,0,.045,0,0,0,Math.PI/2);for(const[x,z]of[[.02,.008],[.02,-.008],[-.02,.008],[-.02,-.008]])add(g,cil(.04),M_,x,.02,z);add(g,cil(.03,.004),M_,.03,.065,0,0,0,-.6);add(g,new THREE.SphereGeometry(.008,8,6),M_,.042,.078,0);add(g,cil(.012,.003),M_,.05,.074,0,0,0,Math.PI/2);for(const z of[.006,-.006]){add(g,cil(.025,.0015),M_,.038,.095,z,0,0,.3);add(g,cil(.012,.0015),M_,.032,.1,z*1.6,.5,0,.9);add(g,cil(.012,.0015),M_,.045,.104,z*1.6,-.5,0,-.4)}};
  const trineo=(p,rot)=>{const g=G(p,rot);for(const z of[.018,-.018]){add(g,new THREE.TorusGeometry(.03,.0025,6,16,Math.PI*.6),ORO,0,.015,z,0,0,Math.PI*1.2);add(g,new THREE.CylinderGeometry(.0025,.0025,.06,6),ORO,0,.004,z,0,0,Math.PI/2)}add(g,new THREE.BoxGeometry(.05,.022,.04),ST(0xc4161f,.5,.4),-.004,.03,0);add(g,new THREE.BoxGeometry(.012,.03,.04),ST(0xc4161f,.5,.4),-.025,.045,0)};
  let kr=0;recorre(['Rúa do Príncipe'],.9,(x,y,tx,ty,k)=>{const nx=-ty,ny=tx,sg=k%2?1:-1,p=sitio(x+nx*.12*sg,y+ny*.12*sg,.025),rot=Math.atan2(-ty,tx)+(sg>0?0:Math.PI);if(kr%3===2)trineo(p,rot);else reno(p,rot,kr%2?ORO:BL);kr++});
  // bola de cristal con un oso polar dentro (Príncipe)
  {const p=sitio(90.62,19.5,.05),g=G(p);add(g,new THREE.CylinderGeometry(.05,.058,.025,24),ST(0x7a1f2a,.2,.4,.3),0,.0125,0);add(g,new THREE.CylinderGeometry(.05,.05,.004,24),ST(0xffffff,.2,.9),0,.027,0);
   const os=ST(0xf8f8f4,.25,.8);add(g,new THREE.SphereGeometry(.018,12,10),os,0,.045,0).scale.set(1.3,1,1);add(g,new THREE.SphereGeometry(.011,10,8),os,.022,.06,0);for(const z of[.007,-.007])add(g,new THREE.SphereGeometry(.004,6,5),os,.02,.071,z);add(g,new THREE.SphereGeometry(.0025,6,5),LZ(0x111111),.033,.06,0);
   const v=add(g,new THREE.SphereGeometry(.07,28,20),new THREE.MeshStandardMaterial({color:0xddeeff,transparent:true,opacity:.18,roughness:.05,metalness:.1,depthWrite:false}),0,.085,0);v.renderOrder=3;for(let q=0;q<40;q++)luz(p[0]+(Math.random()-.5)*.09,groundMap(p[0],p[1])+.04+Math.random()*.09,p[1]+(Math.random()-.5)*.09,0xffffff,q,2,.007);halo(p[0],groundMap(p[0],p[1])+.09,p[1],0xcfe6ff,.25)}
  // globo aerostático con Papá Noel sobre Príncipe
  {const x=92.15,y=19.86,z0=groundMap(x,y)+.42,g=new THREE.Group();g.position.set(x,z0,y);pon(g);const ge=new THREE.SphereGeometry(.07,24,18);const cs=[];const P_=ge.attributes.position;for(let q=0;q<P_.count;q++){const a=Math.atan2(P_.getZ(q),P_.getX(q));cc.set(Math.floor((a+Math.PI)/(Math.PI/6))%2?0xd51f1f:0xf6f4ee);cs.push(cc.r,cc.g,cc.b)}ge.setAttribute('color',new THREE.Float32BufferAttribute(cs,3));
   add(g,ge,new THREE.MeshStandardMaterial({vertexColors:true,roughness:.6,emissive:0x331010,emissiveIntensity:.5}),0,0,0).scale.set(1,1.2,1);add(g,new THREE.CylinderGeometry(.018,.014,.02,10),ST(0x8a5a2b,.2,.8),0,-.115,0);for(const[a,b]of[[.012,.012],[-.012,.012],[.012,-.012],[-.012,-.012]])add(g,new THREE.CylinderGeometry(.0008,.0008,.05,4),LZ(0x553311),a*1.6,-.085,b*1.6);
   add(g,new THREE.SphereGeometry(.008,8,6),ST(0xc21f2a,.4),0,-.098,0);add(g,new THREE.SphereGeometry(.005,8,6),ST(0xf0c8a8,.2),0,-.088,0);add(g,new THREE.ConeGeometry(.005,.01,8),ST(0xc21f2a,.4),0,-.08,0);halo(x,z0-.02,y,0xffb0a0,.3);NAV.globo=g}
  // Casa de Papá Noel (Policarpo Sanz)
  {const p=sitio(90.1,17.55,.06),g=G(p,0),MAD=ST(0x7a4a24,.15,.85);add(g,new THREE.BoxGeometry(.11,.07,.08),MAD,0,.035,0);add(g,new THREE.CylinderGeometry(.001,.075,.05,4,1),ST(0xb01d1d,.25,.7),0,.095,0,0,Math.PI/4,0).scale.set(1.05,1,.8);add(g,new THREE.CylinderGeometry(.001,.08,.012,4,1),ST(0xffffff,.3,.9),0,.118,0,0,Math.PI/4,0).scale.set(1,1,.78);
   for(const[x,z]of[[-.03,.0405],[.03,.0405]])add(g,new THREE.PlaneGeometry(.022,.022),LZ(0xffc070),x,.04,z);add(g,new THREE.PlaneGeometry(.022,.04),ST(0x4a2a12,.1,.8),0,.02,.0406);const z0=groundMap(p[0],p[1]);for(let q=0;q<=24;q++){const t=q/24;luz(p[0]-.055+t*.11,z0+.072,p[1]+.042,q%2?0xff4a3a:0x5aff7a,q,2,.009);luz(p[0]-.055+t*.11,z0+.072,p[1]-.042,q%2?0xffd24a:0x5ab0ff,q,2,.009)}halo(p[0],z0+.06,p[1]+.05,0xffc070,.2)}
  // muñeco de nieve gigante (García Barbón)
  {const p=sitio(97.0,18.32,.07),g=G(p,Math.PI/2),N_=ST(0xf6f8ff,.35,.7);add(g,new THREE.SphereGeometry(.065,20,16),N_,0,.06,0);add(g,new THREE.SphereGeometry(.048,20,16),N_,0,.16,0);add(g,new THREE.SphereGeometry(.034,18,14),N_,0,.235,0);
   add(g,new THREE.TorusGeometry(.036,.008,8,24),ST(0xd51f1f,.3),0,.205,0,Math.PI/2,0,0);add(g,new THREE.ConeGeometry(.007,.04,10),ST(0xff7a1a,.4),0,.235,.05,Math.PI/2,0,0);add(g,new THREE.CylinderGeometry(.032,.032,.006,16),ST(0x1a1a1a,.1),0,.265,0);add(g,new THREE.CylinderGeometry(.022,.022,.04,16),ST(0x1a1a1a,.1),0,.288,0);
   for(const x of[.012,-.012])add(g,new THREE.SphereGeometry(.004,8,6),LZ(0x111111),x,.245,.03);for(const y of[.13,.16,.19])add(g,new THREE.SphereGeometry(.005,8,6),LZ(0x111111),0,y,.047);halo(p[0],groundMap(p[0],p[1])+.15,p[1],0xdfefff,.5)}
  // Estrella Polar de 13 m (García Barbón)
  {const p=sitio(95.0,18.3,.04),g=G(p),sh=new THREE.Shape();for(let q=0;q<10;q++){const a=q/10*6.283+Math.PI/2,r=q%2?.042:.1;q?sh.lineTo(Math.cos(a)*r,Math.sin(a)*r):sh.moveTo(Math.cos(a)*r,Math.sin(a)*r)}
   const eg=new THREE.ExtrudeGeometry(sh,{depth:.012,bevelEnabled:false});eg.translate(0,0,-.006);add(g,eg,LZ(0xffd24a),0,.3,0);add(g,new THREE.CylinderGeometry(.004,.005,.2,8),ST(0x3a3a40,.1,.4,.6),0,.1,0);const z0=groundMap(p[0],p[1]);for(let q=0;q<60;q++){const a=q/60*6.283+Math.PI/2,k=(q/6)%1,r=.1+(.042-.1)*Math.abs(((q%6)/3)-1);luz(p[0]+Math.cos(a)*r*1.05,z0+.3+Math.sin(a)*r*1.05,p[1],0xffffff,q,3,.012)}halo(p[0],z0+.3,p[1],0xffd98a,.9)}
  // bola gigante de Urzáiz
  {const p=sitio(97.55,21.25,.08),g=G(p);add(g,new THREE.SphereGeometry(.085,28,20),ST(0xc4161f,.35,.25,.5),0,.1,0);add(g,new THREE.CylinderGeometry(.022,.022,.03,14),ST(0xd8b040,.4,.3,.8),0,.195,0);add(g,new THREE.TorusGeometry(.012,.003,6,14),ST(0xd8b040,.4,.3,.8),0,.215,0);
   const z0=groundMap(p[0],p[1]);for(let q=0;q<260;q++){const u=(q+.5)/260,ph=Math.acos(1-2*u),th=q*2.4;luz(p[0]+Math.sin(ph)*Math.cos(th)*.088,z0+.1+Math.cos(ph)*.088,p[1]+Math.sin(ph)*Math.sin(th)*.088,q%3?0xfff2c0:0xffffff,q,3,.008)}halo(p[0],z0+.1,p[1],0xff8a7a,.5)}
  // mercado de la Alameda (Praza de Compostela)
  {let n_=0;for(let x=90.2;x<93&&n_<10;x+=.22)for(const y of[15.0,15.55]){const p=[x,y];if(cell(x,y).t===3||!libre(x,y,.05)||n_>=10)continue;n_++;const g=G(p,y>15.2?Math.PI:0);add(g,new THREE.BoxGeometry(.1,.06,.07),ST(0x8a5a2b,.1,.85),0,.03,0);add(g,new THREE.CylinderGeometry(.001,.065,.032,4,1),ST(n_%2?0xc4161f:0x1f8a3c,.25,.7),0,.076,0,0,Math.PI/4,0).scale.set(1.2,1,.9);add(g,new THREE.PlaneGeometry(.08,.03),LZ(0xffc878),0,.035,.0355);const z0=groundMap(x,y);for(let q=0;q<=6;q++)luz(x-.05+q*.0167,z0+.062,y+(y>15.2?-.037:.037),q%2?0xffd98a:0xff5a4a,q+n_,2,.009)}}
 }
 // halos de luz (pocos) alrededor de las luces principales""")
s=pre+seg+post
r('function navTick(dt){','function navTick(dt){if(RACE.nav&&RACE.on&&RACE.pistaMat&&RACE.pistaMat.mA.visible){RACE.pistaMat.mA.visible=false;RACE.pistaMat.mL.visible=false}')
r("if(REP.on&&REP.red&&MODO==='coche'){let dd=.36;","if(((REP.on&&REP.red)||(RACE.on&&RACE.nav))&&MODO==='coche'){let dd=.36;")
r("camC||(REP.on&&REP.red&&MODO==='coche')?14:6","camC||(((REP.on&&REP.red)||(RACE.on&&RACE.nav))&&MODO==='coche')?14:6")
r('window.__G={repRuta,','window.__G={get CIR(){return CIR},repRuta,')
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok carrera')
