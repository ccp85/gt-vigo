import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
def rx(pat,b):
    global s
    m=list(re.finditer(pat,s,re.S));assert len(m)==1,(len(m),pat[:60]);s=s[:m[0].start()]+b+s[m[0].end():]
# --- zona desbloqueada alrededor de Policarpo Sanz: un muro de luz que solo se abre al entregar el regalo
r("function repMisionNueva(ini){","""const REP_R0=6,REP_RD=2.2,REP_RMAX=24,repMuroR=()=>REP.rad+1.2;
function repMuro(){const m=new THREE.Mesh(new THREE.CylinderGeometry(1,1,1.6,160,1,true),new THREE.MeshBasicMaterial({color:0xff5a3a,transparent:true,opacity:.36,side:THREE.DoubleSide,depthWrite:false,toneMapped:false,fog:false}));
 m.position.set(REP_DEP[1],groundY(REP_DEP[1],REP_DEP[2])+.5,REP_DEP[2]);m.renderOrder=3;const borde=new THREE.Mesh(new THREE.CylinderGeometry(1,1,.035,160,1,true),new THREE.MeshBasicMaterial({color:0xffe066,side:THREE.DoubleSide,toneMapped:false,fog:false}));borde.position.y=-.47;m.add(borde);
 const cnd=new THREE.Mesh(new THREE.CylinderGeometry(1,1,.02,160,1,true),new THREE.MeshBasicMaterial({color:0xff3a3a,side:THREE.DoubleSide,toneMapped:false,fog:false}));cnd.position.y=.25;m.add(cnd);scene.add(m);REP.objs.push(m);REP.muro=m;REP.radV=repMuroR();m.scale.set(REP.radV,1,REP.radV)}
function repLimite(dt){if(!REP.rad)return;const W=repMuroR();if(REP.muro){REP.radV+=(W-REP.radV)*Math.min(1,dt*1.5);REP.muro.scale.set(REP.radV,1,REP.radV);REP.muro.material.opacity=.3+.1*Math.sin(NAV.uT.value*3)}
 if(REP.avL>0)REP.avL-=dt;const dx=P.x-REP_DEP[1],dy=P.y-REP_DEP[2],d=Math.hypot(dx,dy);if(d>REP.radV){const k=(REP.radV-.02)/d;P.x=REP_DEP[1]+dx*k;P.y=REP_DEP[2]+dy*k;P.v*=-.3;REP.shake=.25;
  if(!(REP.avL>0)){REP.avL=3;aviso(REP.fase==='entregar'?'🔒 Zona bloqueada · entrega el regalo para abrir más ciudad':'🔒 Zona bloqueada · vuelve a Policarpo Sanz',1.6,'peq');try{sonCaja()}catch(e){}}}}
function repMisionNueva(ini){if(ini){REP.rad=REP_R0;repMuro()}""")
# el destino y toda la ruta del GPS tienen que caber dentro de la zona abierta
r("REP.fase='entregar';REP.carga=1;repPila();const d=repElegir();","""REP.fase='entregar';REP.carga=1;repPila();const W=repMuroR()-.15;let d=null;for(let k=0;k<12;k++){const c=repElegir(),pp=gpsCalcular(P.x,P.y,c[1],c[2]);d=c;if(pp&&pp.length>1&&pp.every(p=>Math.hypot(p[0]-REP_DEP[1],p[1]-REP_DEP[2])<W))break}""")
rx(r"mn=Math\.min\(9,5\+\.3\*k\),mx=Math\.min\(13,7\+\.5\*k\)","mn=Math.max(2.4,(REP.rad||REP_R0)-3.6),mx=(REP.rad||REP_R0)-.3")
r("if(!L.length)L=pool.filter(d=>dd(d)>3);if(!L.length)L=pool;","if(!L.length)L=pool.filter(d=>dd(d)>2&&dd(d)<(REP.rad||REP_R0));if(!L.length)L=pool;")
# al entregar se abre más ciudad
r("repPop('+'+pts+' ⭐','gran');repVolver();setTimeout(()=>aviso('↩️ Vuelve a Policarpo Sanz a por otro regalo',1.6,'peq'),1300)}",
  "repPop('+'+pts+' ⭐','gran');const ab=REP.rad<REP_RMAX;if(ab)REP.rad=Math.min(REP_RMAX,REP.rad+REP_RD);repVolver();setTimeout(()=>aviso(ab?'🔓 ¡Nueva zona desbloqueada! Vuelve a Policarpo Sanz':'↩️ Vuelve a Policarpo Sanz a por otro regalo',1.8,'peq'),1300)}")
# sin límite de tiempo: el reloj es solo un bonus que llega a 0 y ya
r("if(!REP.ultMin&&REP.t<=60){REP.ultMin=true;aviso('🔔 ¡Último minuto! Puntos ×2',1.8,'cuenta');sonCampana(3,.8)}if(REP.t<=0){REP.t=0;repHud();repFin();return}}",
  "if(REP.t<=0)REP.t=0;repLimite(dt)}")
r("repPop('🎁 ¡Regalo cargado! ⏱ '+REP.t+' s','aviso')","repPop('🎁 ¡Regalo cargado! ⚡ bonus '+REP.t+' s','aviso')")
r("<span class=\"t ${REP.t<15?'poco':''}\">⏱ ${fmtS(Math.max(0,REP.t))}</span>","<span class=\"t\" title=\"bonus por rapidez\">⚡ ${REP.t>0?fmtS(REP.t):'0'}</span>")
r("'Recoge el regalo en Policarpo Sanz y llévalo antes de que se acabe el tiempo'","'Recoge el regalo en Policarpo Sanz, entrégalo y abre más ciudad. Sin límite de tiempo'")
r("function salirReparto(menu=true){sonMotor(0,false);sonRotor(false);","function salirReparto(menu=true){sonMotor(0,false);sonRotor(false);REP.rad=0;REP.muro=null;")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok limite')
