import re
f='index.html';s=open(f).read()
def r(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:90]); s=s.replace(a,b)
def rx(pat,b):
    global s
    m=list(re.finditer(pat,s,re.S));assert len(m)==1,(len(m),pat[:60]);s=s[:m[0].start()]+b+s[m[0].end():]
CAR="(REP.red&&!REP.heli)"
# ---------- récords: uno para la carroza (puntos) y otro para el helicóptero (regalos) ----------
r("function repRecords(){try{const a=JSON.parse(localStorage.getItem(REP_KREC)||'[]');",
  "const repModoC=h=>h===undefined?!REP.heli:!h;const repScore=()=>"+CAR+"?REP.pts:REP.ent;\nfunction repRecords(h){try{const a=JSON.parse(localStorage.getItem(repModoC(h)?'gtvigo_reparto_puntos':REP_KREC)||'[]');")
r("function repGuardar(nombre,n,m=0){const a=repRecords();a.push({n:nombre.slice(0,18),r:n,m,f:Date.now()});",
  "function repGuardar(nombre,n,m=0,g=0){const a=repRecords();a.push({n:nombre.slice(0,18),r:n,m,g,f:Date.now()});")
r("try{localStorage.setItem(REP_KREC,JSON.stringify(top));","try{localStorage.setItem(repModoC()?'gtvigo_reparto_puntos':REP_KREC,JSON.stringify(top));")
r("<b>🎁 ${e.r}${e.m?' · 🪙 '+e.m:''}</b></li>","<b>${e.g!==undefined?'⭐ '+e.r+' · 🎁 '+e.g:'🎁 '+e.r+(e.m?' · 🪙 '+e.m:'')}</b></li>")
rx(r"function repFin\(\)\{if\(REP\.fin\)return;.*?\n(?=function repGuardarClick)",r"""function repFin(){if(REP.fin)return;REP.fin=true;gpsParar();REP.marca.visible=false;const el=document.getElementById('nFin'),C=REP.red&&!REP.heli,sc=repScore();
 const top=repRecords(),entra=!REP.guardado&&sc>0&&(top.length<10||sc>top[top.length-1].r);const acabado=C&&REP.t<=0;
 el.querySelector('h3').textContent=acabado?'🕛 ¡Medianoche!':REP.ent?'🎄 ¡Buen reparto!':'🎄 Reparto de Navidad';
 el.querySelector('p').innerHTML=C?(REP.ent?`Has repartido <b>${REP.ent}</b> ${REP.ent===1?'regalo':'regalos'} · <b>⭐ ${REP.pts}</b> puntos`+(REP.mon?` · 🪙 ${REP.mon}`:'')+'.'+(top[0]&&sc>top[0].r?' ¡Nuevo récord!':''):'No has entregado ningún regalo.'):
  (REP.ent?`Has repartido <b>${REP.ent}</b> ${REP.ent===1?'regalo':'regalos'}`+(REP.mon?` y recogido <b>${REP.mon}</b> 🪙`:'')+'.'+(top[0]&&sc>top[0].r?' ¡Nuevo récord!':''):'Aún no has entregado ningún regalo.');
 const g=el.querySelector('.guarda');g.hidden=!entra;if(entra){let nm='';try{nm=localStorage.getItem('gtvigo_nombre')||''}catch(e){}g.querySelector('input').value=nm}
 el.querySelector('.seguir').hidden=acabado;el.querySelector('.otra').textContent=acabado?'↻ Otra partida':'↻ Empezar de cero';
 el.querySelector('.pts').innerHTML='<h4>🏆 Récords</h4>'+repLista(top);el.hidden=false;if(entra&&(!top[0]||sc>top[0].r))try{confeti()}catch(e){}}
""")
r("const nm=(inp.value||'').trim()||'Anónimo';if(REP.guardado||!REP.ent)return;REP.guardado=true;\n const top=repGuardar(nm,REP.ent,REP.mon||0);const yo=top.find(e=>e.n===nm.slice(0,18)&&e.r===REP.ent&&Date.now()-e.f<5000);",
  "const nm=(inp.value||'').trim()||'Anónimo';const sc=repScore();if(REP.guardado||!sc)return;REP.guardado=true;\n const top=repGuardar(nm,sc,REP.mon||0,"+CAR+"?REP.ent:undefined);const yo=top.find(e=>e.n===nm.slice(0,18)&&e.r===sc&&Date.now()-e.f<5000);")
r("if(REP.guardado){REP.ent=0;REP.mon=0;REP.guardado=false}repSiguiente()}","if(REP.guardado&&!"+CAR+"){REP.ent=0;REP.mon=0;REP.guardado=false}repSiguiente()}")
r("if(RACE.nav){const r_=repRecords()[0];el.querySelector('.rec').textContent=(r_?'🏆 Récord: '+r_.n+' · '+r_.r+' regalos':'Sin tiempo: reparte todos los que puedas')",
  "if(RACE.nav){const r_=repRecords(!!s.veh)[0];el.querySelector('.rec').textContent=(r_?'🏆 Récord: '+r_.n+' · '+(s.veh?r_.r+' regalos':'⭐ '+r_.r):(s.veh?'Sin tiempo: reparte todos los que puedas':'Recoge regalos y repártelos antes de medianoche'))+(s.veh?'':' · '+['Papá Noel: el saco más grande (8)','Melchor: turbo más largo','Gaspar: el más ágil en los giros','Baltasar: su combo dura más'][s.c]||'')")
# ---------- partida contra el reloj, saco de regalos, combo y obstáculos (solo carroza) ----------
r("const repEnZona=(x,y)=>","""const REP_RASGO=[{cap:8,tur:1.4,cmb:14,giro:1},{cap:5,tur:2.6,cmb:14,giro:1},{cap:5,tur:1.4,cmb:14,giro:1.5},{cap:5,tur:1.4,cmb:22,giro:1}],REP_T0=180,REP_TBONO=6;
const repEnZona=(x,y)=>""")
r("REP.on=true;REP.pool=null;REP.red=null;GPSF=null;if(!REP.heli){repCircuito();repArcade()}",
  "REP.on=true;REP.pool=null;REP.red=null;GPSF=null;if(!REP.heli){const ra=REP_RASGO[sel.c]||REP_RASGO[0];Object.assign(REP,{cap:ra.cap,turD:ra.tur,cmb:ra.cmb,giro:ra.giro,t:REP_T0,pts:0,carga:0,mul:1,ct:0,ultMin:false,shake:0});CIELO.h=20.8;repCircuito();repArcade();repPila()}")
# entrega: solo con regalos en el saco; puntos según cuántos llevas, combo y último minuto
r("function repEntrega(){const d=REP.dest;REP.dest=null;REP.ent++;","function repEntrega(){if("+CAR+"&&!repPuntua())return;const d=REP.dest;REP.dest=null;if(!"+CAR+")REP.ent++;")
r("const rec=repRecords()[0];aviso(rec&&REP.ent===rec.r+1?'🏆 ¡Nuevo récord! '+REP.ent:'🎁 ¡Entregado! · '+REP.ent,1.1,'peq');","if(!"+CAR+"){const rec=repRecords()[0];aviso(rec&&REP.ent===rec.r+1?'🏆 ¡Nuevo récord! '+REP.ent:'🎁 ¡Entregado! · '+REP.ent,1.1,'peq')}")
r("function repPop(t){","""function repPuntua(){const t=NAV.uT.value;if(REP.carga<=0){if(!REP.avT||t-REP.avT>2.5){REP.avT=t;repPop('🎁 ¡Recoge regalos primero!','aviso')}return false}
 const n=REP.carga,x2=REP.t<=60?2:1,pts=n*100*REP.mul*x2;REP.pts+=pts;REP.ent+=n;REP.carga=0;repPila();REP.t+=REP_TBONO;
 repPop('+'+pts+(REP.mul>1?'  ×'+REP.mul:'')+(x2>1?'  ×2':''),'gran');REP.mul=Math.min(5,REP.mul+1);REP.ct=REP.cmb;REP.shake=.5;try{confeti()}catch(e){}repHud();return true}
// saco visible: los regalos que llevas se apilan en la carroza
function repPila(){if(!REP.pilaG||REP.pilaG.parent!==car){const g=new THREE.Group(),C=[0xd51f1f,0x1fae4a,0xf2c230,0x1f6fd0,0xc23fd0,0xf6f6f2,0xff7a1a,0x35e0ff];REP.pilaB=[];
  for(let k=0;k<8;k++){const b=new THREE.Mesh(new THREE.BoxGeometry(.017,.017,.017),new THREE.MeshStandardMaterial({color:C[k],emissive:C[k],emissiveIntensity:.35,roughness:.5}));b.position.set(-.04+(k%2)*.012,.045+Math.floor(k/2)*.016,(k%4<2?-.008:.008));b.rotation.y=k*.6;g.add(b);REP.pilaB.push(b)}
  car.add(g);REP.pilaG=g}REP.pilaB.forEach((b,k)=>b.visible=k<(REP.carga||0))}
function repPop(t){""")
r("function repPop(t){const el=document.getElementById('nPop');el.textContent=t;el.hidden=false;el.classList.remove('on');void el.offsetWidth;el.classList.add('on');clearTimeout(repPop.t);repPop.t=setTimeout(()=>el.hidden=true,700)}",
  "function repPop(t,c=''){const el=document.getElementById('nPop');el.textContent=t;el.hidden=false;el.className='';void el.offsetWidth;el.className='on '+c;clearTimeout(repPop.t);repPop.t=setTimeout(()=>el.hidden=true,c?1200:700)}")
# regalos sueltos por la calle: se recogen al saco (en vez de dar monedas)
r("const R=[];for(let k=0;k<22&&pool.length;k++){const d=pool[Math.floor(Math.random()*pool.length)];if(R.some(c=>Math.hypot(c.x-d[1],c.y-d[2])<.8)",
  "const R=[];for(let k=0;k<90&&pool.length&&R.length<36;k++){const d=pool[Math.floor(Math.random()*pool.length)];if(R.some(c=>Math.hypot(c.x-d[1],c.y-d[2])<.55)")
r("if(c.on&&Math.hypot(c.x-P.x,c.y-P.y)<.1){c.on=false;c.t=40;REP.mon+=5;REP.boost=1.8;ch=true;try{sonCaja()}catch(e){}aviso('🎁 ¡Turbo navideño! +5 🪙',1,'peq')}",
  "if(c.on&&Math.hypot(c.x-P.x,c.y-P.y)<.1){if((REP.carga||0)<REP.cap){c.on=false;c.t=18;REP.carga++;repPila();ch=true;try{sonCaja()}catch(e){}repPop(REP.carga>=REP.cap?'🎒 ¡Saco lleno!':'🎁 '+REP.carga+'/'+REP.cap)}else if(!REP.llT||t-REP.llT>2){REP.llT=t;repPop('🎒 ¡Saco lleno! Entrégalos','aviso')}}")
r("REP.combo=(t-(REP.lc||-9)<1.3)?(REP.combo||0)+1:1;REP.lc=t;const b=REP.combo>=10&&REP.combo%10===0?5:0;REP.mon+=1+b;ch=true;repPop(b?'🔥 COMBO x'+REP.combo+' +'+(1+b):REP.combo>=3?'+1 · x'+REP.combo:'+1');",
  "REP.combo=(t-(REP.lc||-9)<1.3)?(REP.combo||0)+1:1;REP.lc=t;const b=REP.combo>=10&&REP.combo%10===0?5:0;REP.mon+=1+b;REP.pts=(REP.pts||0)+10*(1+b);ch=true;if(b)repPop('🔥 RACHA x'+REP.combo+' +'+(1+b)+' 🪙');")
r("REP.tT=t;REP.boost=Math.max(REP.boost,1.4);","REP.tT=t;REP.boost=Math.max(REP.boost,REP.turD||1.4);")
# obstáculos suaves: puestos de castañas en la calzada (la ruta los esquiva; si los tocas pierdes un regalo y el combo)
r("REP.arc={C,R,mc,rc,lz,du,T,txt};repArcadeTick(0)}","""const O=[];for(let k=0;k<80&&pool.length&&O.length<14;k++){const d=pool[Math.floor(Math.random()*pool.length)],sg=Math.random()<.5?1:-1,x=d[1]-d[4]*.05*sg,y=d[2]+d[3]*.05*sg;if(!repLibre(x,y)||Math.hypot(x-P.x,y-P.y)<1||O.some(c=>Math.hypot(c.x-x,c.y-y)<1)||R.some(c=>Math.hypot(c.x-x,c.y-y)<.2))continue;O.push({x,y,a:Math.atan2(-d[3],d[4])})}
 const MAD=new THREE.MeshStandardMaterial({color:0x6b3d1a,roughness:.85}),TOL=new THREE.MeshStandardMaterial({color:0xc4161f,roughness:.7}),BR=new THREE.MeshBasicMaterial({color:0xff7a1a,toneMapped:false});
 for(const o of O){const g=new THREE.Group();g.position.set(o.x,groundY(o.x,o.y),o.y);g.rotation.y=o.a;const c_=new THREE.Mesh(new THREE.BoxGeometry(.05,.03,.035),MAD);c_.position.y=.024;g.add(c_);for(const z of[-.02,.02]){const w=new THREE.Mesh(new THREE.CylinderGeometry(.011,.011,.004,10),new THREE.MeshStandardMaterial({color:0x222222}));w.rotation.x=Math.PI/2;w.position.set(-.012,.011,z);g.add(w)}
  const t_=new THREE.Mesh(new THREE.ConeGeometry(.04,.02,4),TOL);t_.rotation.y=Math.PI/4;t_.position.y=.068;g.add(t_);const p_=new THREE.Mesh(new THREE.CylinderGeometry(.002,.002,.03,4),MAD);p_.position.y=.05;g.add(p_);const f_=new THREE.Mesh(new THREE.SphereGeometry(.008,8,6),BR);f_.position.set(.012,.043,0);g.add(f_);scene.add(g);REP.objs.push(g)}
 REP.obst=O;REP.arc={C,R,mc,rc,lz,du,T,txt};repArcadeTick(0)}""")
r(" if(REP.boost>0){REP.boost-=dt;P.v=Math.min(P.v+2.2*dt,1.55)}if(ch)repHud()}",
  """ if(REP.obst)for(const o of REP.obst)if(Math.hypot(o.x-P.x,o.y-P.y)<.07&&(!REP.oT||t-REP.oT>1.2)){REP.oT=t;P.v*=.3;REP.boost=0;REP.mul=1;REP.ct=0;REP.shake=.7;try{golpe()}catch(e){}if(REP.carga>0){REP.carga--;repPila();repPop('💥 -1 🎁','aviso')}else repPop('💥 ¡Cuidado!','aviso');ch=true}
 if(REP.boost>0){REP.boost-=dt;P.v=Math.min(P.v+2.2*dt,1.55)}if(ch)repHud()}""")
# reloj, combo y último minuto
r("if(!REP.heli&&!REP.fin)repArcadeTick(dt);","""if(!REP.heli&&!REP.fin&&REP.red){repArcadeTick(dt);REP.t-=dt;if(REP.ct>0){REP.ct-=dt;if(REP.ct<=0&&REP.mul>1){REP.mul=1;repPop('Combo perdido','aviso')}}
  if(!REP.ultMin&&REP.t<=60){REP.ultMin=true;aviso('🔔 ¡Último minuto! Puntos ×2',1.8,'cuenta')}if(REP.t<=0){REP.t=0;repHud();repFin();return}}""")
# HUD de la carroza: tiempo, puntos, saco y combo
r("const rec=repRecords()[0],dd=d?Math.hypot(d[1]-P.x,d[2]-P.y):0;el.querySelector('.cnt').innerHTML=",
  "const rec=repRecords()[0],dd=d?Math.hypot(d[1]-P.x,d[2]-P.y):0;if("+CAR+"){el.querySelector('.cnt').innerHTML=`<span class=\"t ${REP.t<20?'poco':''}\">⏱ ${fmtS(REP.t)}</span><span class=\"t\">⭐ ${REP.pts}</span><span class=\"r ${REP.carga>=REP.cap?'ok':''}\">🎁 ${REP.carga}/${REP.cap}</span>`+(REP.mul>1?`<span class=\"cmb\">×${REP.mul}<i style=\"width:${Math.max(0,REP.ct/REP.cmb*100)}%\"></i></span>`:'')+`<span class=\"r\">📍 ${d?fmtD(dd):'—'}</span>`;return}\n el.querySelector('.cnt').innerHTML=")
r("REP.hT=(REP.hT||0)-dt;if(REP.hT<=0){REP.hT=.2;repHud()}","REP.hT=(REP.hT||0)-dt;if(REP.hT<=0){REP.hT=.1;repHud()}")
# CSS: combo, popup grande, menos ruido arriba
r("#nPop.on{animation:npop .7s ease-out}","#nPop.on{animation:npop .7s ease-out}#nPop.gran{font-size:44px;color:#fff3b0;text-shadow:0 3px 0 #c4161f,0 0 18px rgba(255,200,0,.9);animation:npopg 1.2s ease-out}#nPop.aviso{font-size:20px;color:#fff;text-shadow:0 2px 0 #000,0 0 10px rgba(0,0,0,.6)}@keyframes npopg{0%{transform:translate(-50%,20px) scale(.5);opacity:0}20%{transform:translate(-50%,0) scale(1.25);opacity:1}70%{transform:translate(-50%,-10px) scale(1);opacity:1}100%{transform:translate(-50%,-40px) scale(.9);opacity:0}}\n#nHud .cmb{position:relative;font:900 16px var(--body);color:#ff7a1a;padding-bottom:3px}#nHud .cmb i{position:absolute;left:0;bottom:0;height:3px;background:#ff7a1a;border-radius:2px}#nHud .t.poco{color:#ff6a5a}\nbody.rep #vel small,body.rep header h1{display:none!important}@media (max-width:700px){#nHud{max-width:calc(100vw - 150px);border-radius:16px;padding:4px 4px 4px 10px}#nHud .cnt{flex-wrap:wrap;justify-content:flex-end;gap:2px 8px}}")
# la carroza también gira según el personaje
r("const des=Math.atan2(-(ty-P.y),tx-P.x),df=Math.atan2(Math.sin(des-P.a),Math.cos(des-P.a)),mx=3.4*dt;","const des=Math.atan2(-(ty-P.y),tx-P.x),df=Math.atan2(Math.sin(des-P.a),Math.cos(des-P.a)),mx=3.4*(REP.giro||1)*dt;")
# la cámara tiembla al entregar o chocar
r("if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*(camC||(REP.on&&REP.red&&MODO==='coche')?14:6)));",
  "if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*(camC||(REP.on&&REP.red&&MODO==='coche')?14:6)));if(REP.on&&REP.shake>0){REP.shake-=dt;const k_=REP.shake*.03;pcam.position.x+=(Math.random()-.5)*k_;pcam.position.y+=(Math.random()-.5)*k_;pcam.position.z+=(Math.random()-.5)*k_}")
# la ruta, más fina
r("const P_=GPS.pts,i0=Math.max(0,GPS.idx-1),i1=Math.min(P_.length,i0+260);const pos=[],w=.022;","const P_=GPS.pts,i0=Math.max(0,GPS.idx-1),i1=Math.min(P_.length,i0+260);const pos=[],w=REP.on&&REP.red?.011:.022;")
# pancartas legibles por los dos lados
r("mP=new THREE.MeshBasicMaterial({map:tx_,side:THREE.DoubleSide,toneMapped:false})","mP=new THREE.MeshBasicMaterial({map:tx_,toneMapped:false})")
r("pl.rotation.y=Math.atan2(-ny,nx);pon(pl);","pl.rotation.y=Math.atan2(-ny,nx);pon(pl);const pl2=pl.clone();pl2.rotation.y+=Math.PI;pon(pl2);")
# obstáculos: la ruta los rodea
r("const co=new Float32Array(cw*ch);for(let k=0;k<cm.length;k++)co[k]=1+6*Math.exp(-(D[k]-1)/1.3);","const co=new Float32Array(cw*ch);for(let k=0;k<cm.length;k++)co[k]=1+6*Math.exp(-(D[k]-1)/1.3);for(const o of REP.obst||[]){const oi=Math.floor((o.x-R.x0)/(R.res*2)),oj=Math.floor((o.y-R.y0)/(R.res*2));for(let b=-3;b<=3;b++)for(let a=-3;a<=3;a++){const q=(oj+b)*cw+oi+a;if(q>=0&&q<co.length&&a*a+b*b<=9)co[q]+=40}}")
r("heliDesvestir();REP.heli=false;","heliDesvestir();REP.heli=false;REP.obst=null;REP.pilaG=null;")
r("REP.marca.visible=true;gpsIniciar(d);repHud()}","REP.marca.visible=true;gpsIniciar(d);repSembrar();repHud()}")
r("function repPila(){","""// pone unos regalos sueltos en el camino hacia la próxima entrega (el piloto automático los recoge al pasar)
function repSembrar(){if(!(REP.red&&!REP.heli)||!REP.arc||!GPS.pts)return;const A=GPS.acc,L=A[A.length-1],R=REP.arc.R;const lib=R.filter(c=>!c.on).concat(R.filter(c=>c.on).sort((a,b)=>Math.hypot(b.x-P.x,b.y-P.y)-Math.hypot(a.x-P.x,a.y-P.y)));
 const nq=Math.max(1,Math.min(REP.cap-(REP.carga||0),2+Math.floor(Math.random()*3)));for(let q=0;q<nq&&lib.length;q++){const s_=L*(.2+.6*(q+.5)/nq);let j=0;while(j<A.length-1&&A[j]<s_)j++;const c=lib.shift();c.x=GPS.pts[j][0];c.y=GPS.pts[j][1];c.z=groundY(c.x,c.y)+.04;c.on=true;c.t=0}}
function repPila(){""")
r("if(REP.on&&REP.red&&MODO==='coche'&&!P.turn&&P.v>.02){const man=","if(REP.auto&&REP.on&&REP.red&&MODO==='coche'&&!P.turn&&P.v>.02){const man=")
r("mostrar('▲ Solo acelera: la carroza va sola · ◀ ▶ para desviarte')","mostrar('▲ acelera · ◀ ▶ gira · recoge regalos y llévalos a la marca')")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok juego')
