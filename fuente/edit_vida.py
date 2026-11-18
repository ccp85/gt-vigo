import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= CIUDAD VIVA: el tráfico y la gente reaccionan =================
# ---- estilos: bocadillos de diálogo y botón de claxon en móvil
s=s.replace('</style>',r""".burb{position:fixed;left:0;top:0;z-index:12;pointer-events:none;transform:translate(-50%,-100%);background:#fff;color:#1b1d2b;font:800 13px/1.15 var(--body);padding:5px 10px;border-radius:12px;box-shadow:0 3px 12px rgba(0,0,0,.28);white-space:nowrap;display:none}
.burb:after{content:'';position:absolute;left:50%;bottom:-6px;margin-left:-6px;border:6px solid transparent;border-top-color:#fff;border-bottom:0}
.burb.enf{background:#ffd9d2;color:#7a1810}.burb.enf:after{border-top-color:#ffd9d2}.burb.sus{background:#fff4c2;color:#5a4300}.burb.sus:after{border-top-color:#fff4c2}
#pad #bPita{width:52px;height:52px;font-size:20px}body.heli #bPita,body.rep #bPita,body.carrera #bPita,body.pie #bPita{display:none!important}@media (pointer:fine){#pad #bPita{display:none}}
</style>""",1)
r('<button id="bAcc" aria-label="Subir o bajar del vehículo">Bajar</button>','<button id="bAcc" aria-label="Subir o bajar del vehículo">Bajar</button><button id="bPita" aria-label="Claxon">📯</button>')

# ---- gente: se puede inclinar (caerse) además de girar
r("const MB=new THREE.Matrix4(),ML=new THREE.Matrix4()","const qT=new THREE.Quaternion(),MB=new THREE.Matrix4(),ML=new THREE.Matrix4()")
r("G.set=(i,x,z,y,ang,sw,esc=1)=>{q.setFromAxisAngle(Y,ang);","G.set=(i,x,z,y,ang,sw,esc=1,tilt=0)=>{q.setFromAxisAngle(Y,ang);if(tilt){qT.setFromAxisAngle(Zx,tilt);q.multiply(qT)}")

# ---- peatones: densidad según la hora, esquivan, se caen si los rozas y protestan
r("q.hu=0;q.z=null;q.ox=undefined;q.oxs=undefined}","q.hu=0;q.z=null;q.ox=undefined;q.oxs=undefined;q.ex=q.ey=0;q.caido=0;q.esq=0;q.tilt=0}")
r("if(i>=PEA.length*QF){","if(i>=PEA.length*QF*DENS.p){")
r("q.s+=q.dir*(huye?0:q.v*(q.cruza?2.5:1))*dt;","q.s+=q.dir*(huye||q.esq>0||q.caido>0?0:q.v*(q.cruza?2.5:1))*dt;")
r("q.x=x+sd*(off+q.oxs);q.y=y+cd*(off+q.oxs);q.a=ang;",r"""q.x=x+sd*(off+q.oxs);q.y=y+cd*(off+q.oxs);q.a=ang;
  {const vr=peaReacciona(q,dt);q.x+=q.ex||0;q.y+=q.ey||0;if(vr!=null)ang=vr}""")
r("const[x,y,a]=posRuta(q.r,q.s);const off=(ANCH[q.r.c]||.07)+(ACW[q.r.c]||.03)*.5+q.hu;const ang=a+(q.dir<0?Math.PI:0);",
  "const[x,y,a]=posRuta(q.r,q.s);const off=(ANCH[q.r.c]||.07)+(ACW[q.r.c]||.03)*.5+q.hu;let ang=a+(q.dir<0?Math.PI:0);")
r("PEA_G.set(i,q.x,q.z+bob*.6,q.y,ang,Math.sin(performance.now()/160+q.ph)*.55*(q.cruza?1.3:1)*(huye?.2:1),q.esc||(q.esc=.92+((i*37)%17)/100))",
  "{const corre=q.esq>0||q.enfT>0;PEA_G.set(i,q.x,q.z+(q.caido>0?0:bob*.6),q.y,ang,q.caido>0?0:Math.sin(performance.now()/(corre?75:160)+q.ph)*.55*(q.cruza||corre?1.4:1)*(huye&&!corre?.2:1),q.esc||(q.esc=.92+((i*37)%17)/100),q.tilt||0)}")

# ---- tráfico: reescrito con reacciones
i=s.index("function updateTraffic(dt){");j=s.index(" for(const v of APARC){v.g.visible=driving;",i)
s=s[:i]+r"""function updateTraffic(dt){frameN++;window.__TT=(window.__TT||0)+dt;cercaT-=dt;if(cercaT<=0){cercaT=1;rutasCerca();densHora()}updatePeatones(dt);
 const nAct=Math.max(6,Math.round(TRAF.length*DENS.t)),jug=driving&&MODO!=='heli'&&MODO!=='moto';
 const pvx=Math.cos(P.a)*P.v,pvy=-Math.sin(P.a)*P.v;
 for(let ci=0;ci<TRAF.length;ci++){const c=TRAF[ci];
  if(ci>=nAct){if(c.g.visible)c.g.visible=false;c.inact=true;continue}
  if(c.inact){c.inact=false;if(CERCA.length&&recolocar(c,CERCA,driving?3:0,F.R))c.z=null;trafReset(c)}
  if(CERCA.length&&Math.hypot(c.x-F.x,c.y-F.y)>F.R*1.04){recolocar(c,CERCA,driving?3:0,F.R);c.z=null;c.vv=c.v;c.parT=0;trafReset(c)}
  const [x0,y0,a0]=posRuta(c.r,c.s);const fx=Math.cos(a0)*c.dir,fy=-Math.sin(a0)*c.dir,ang0=a0+(c.dir<0?Math.PI:0),rvx=Math.sin(ang0),rvy=Math.cos(ang0);
  c.v=(c.r.c==='m'?.24:c.r.c==='T'?.62:.45)*c.k*(c.cede>0?.45:1);
  // ¿el jugador está delante? (medido desde donde está el coche de verdad, no desde el centro del carril)
  const dpx=P.x-c.x,dpy=P.y-c.y,ahead=dpx*fx+dpy*fy,latS=dpx*rvx+dpy*rvy,lat=Math.abs(latS);
  const blockedBy=jug&&ahead>0&&ahead<.2&&lat<.055;
  if(c.ko>0){// golpeado: se desplaza con el empujón, gira y se queda parado
   c.ko-=dt;const dm=Math.exp(-dt*3.2);c.ox+=c.kvx*dt;c.oy+=c.kvy*dt;c.kvx*=dm;c.kvy*=dm;c.rot+=c.kw*dt;c.kw*=dm;c.vv=0;
   if(c.ko<=0){c.enf=1;if(Math.hypot(c.x-P.x,c.y-P.y)<1.2){claxon(c.x,c.y,c.tipo,2);burbuja(c,azar(c.bus?TXT.bus:TXT.choque),'enf')}}}
  else{const dm=Math.exp(-dt*1.1);c.ox*=dm;c.oy*=dm;c.rot*=Math.exp(-dt*2.2);
   if(blockedBy){c.tb=(c.tb||0)+dt;
    if(c.tb>.7&&!c.pitado){c.pitado=true;claxon(c.x,c.y,c.tipo,1);burbuja(c,azar(TXT.pita),'')}
    if(c.tb>1.3&&Math.abs(P.v)<.2&&!(c.adel>0)){const sg=latS>0?-1:1;if(carrilLibre(c,x0,y0,fx,fy,rvx,rvy,sg*.085)){c.latT=sg*.085;c.adel=2.6}}
    if(c.tb>8)c.pasa=2}
   else{c.tb=0;if(c.tb2>0)c.tb2-=dt;else c.pitado=false}
   if(c.pasa>0)c.pasa-=dt;
   // de frente y rápido (vas por su carril): se aparta, frena y te pita
   const pdot=Math.cos(P.a)*fx-Math.sin(P.a)*fy;
   if(jug&&!(c.esq>0)&&P.v>.25&&pdot<-.5&&ahead>0&&ahead<.5&&lat<.07){const sg=latS>0?-1:1;if(carrilLibre(c,x0,y0,fx,fy,rvx,rvy,sg*.07)){c.latT=sg*.07}c.esq=1.6;claxon(c.x,c.y,c.tipo,3);burbuja(c,azar(TXT.frente),'sus')}
  }
  if(c.esq>0){c.esq-=dt;if(c.esq<=0&&!(c.adel>0)&&!(c.cede>0))c.latT=0}
  if(c.adel>0){c.adel-=dt;if(c.adel<=0&&!(c.esq>0)&&!(c.cede>0))c.latT=0}
  if(c.cede>0){c.cede-=dt;if(c.cede<=0&&!(c.esq>0)&&!(c.adel>0))c.latT=0}
  c.lat=(c.lat||0)+((c.latT||0)-(c.lat||0))*Math.min(1,dt*2.6);
  // sigue al coche de delante y para ante peatones en la calzada
  let delante=false;if(c.libre>0)c.libre-=dt;else for(const o of TRAF){if(o===c||o.inact)continue;const ex=o.x-c.x,ey=o.y-c.y;const al=ex*fx+ey*fy;if(al>0&&al<.13&&Math.abs(ex*fy-ey*fx)<.03){delante=true;break}}
  if(delante){c.td=(c.td||0)+dt;if(c.td>1.2){c.td=0;c.libre=1.5;if(Math.hypot(c.x-F.x,c.y-F.y)>1.4&&recolocar(c,CERCA,driving?3:0,F.R)){c.z=null;trafReset(c)}}}else c.td=0;
  let peaton=false;for(const q of PEA){if(!(q.cruza||q.caido>0||q.esq>0)||q.x>1e4)continue;const ex=q.x-c.x,ey=q.y-c.y,al=ex*fx+ey*fy;if(al>0&&al<.12&&Math.abs(ex*fy-ey*fx)<.04){peaton=true;break}}
  const rojo=semaforoRojo(c.x,c.y,fx,fy);
  if(c.bus){if(c.parT>0)c.parT-=dt;else{const pz=paradaCerca(c.x,c.y,fx,fy);if(pz&&pz!==c.ultPar){c.ultPar=pz;c.parT=4+Math.random()*3}}}
  const para=c.ko>0||(blockedBy&&!(c.pasa>0)&&!(c.adel>0)&&!(c.cede>0))||delante||peaton||rojo||(c.bus&&c.parT>0)||(c.esq>0&&ahead>0&&ahead<.5&&lat<.07);
  c.vv=(c.vv??c.v)+((para?0:c.v)-(c.vv??c.v))*Math.min(1,dt*(c.esq>0?6:3));
  c.s+=c.dir*c.vv*dt;if(c.s>c.r.L||c.s<0){siguiente(c,false);c.latT=0}
  const[x,y,a]=posRuta(c.r,c.s);const off=(c.r.c==='m'?.02:.04)+(c.lat||0);const ang=a+(c.dir<0?Math.PI:0);
  c.x=x+Math.sin(ang)*off+(c.ox||0);c.y=y+Math.cos(ang)*off+(c.oy||0);
  if(c.z==null||(frameN+ci)%3===0)c.z=groundY(c.x,c.y);c.g.position.set(c.x,c.z,c.y);c.g.rotation.y=ang+(c.rot||0)-((c.latT||0)-(c.lat||0))*2.2;c.g.visible=F.vida&&Math.hypot(c.x-F.x,c.y-F.y)<F.R*1.1}
 burbujasTick()
"""+s[j:]

# ---- funciones nuevas (antes del tráfico)
r("const TRAF=[];window.TRAF=TRAF;let RUTAS=null;",r"""const TRAF=[];window.TRAF=TRAF;let RUTAS=null;
// ---------- ciudad viva: densidad según la hora, reacciones del tráfico y de los peatones, claxon y bocadillos
const DENS={t:1,p:1};window.DENS=DENS;
const DTAB_T=[[0,.5],[2,.3],[6,.3],[8,1],[21,1],[24,.5]],DTAB_P=[[0,.35],[2,.12],[6.5,.12],[9,1],[21,1],[24,.35]];
const dInterp=(T,h)=>{for(let k=1;k<T.length;k++)if(h<=T[k][0]){const[a,va]=T[k-1],[b,vb]=T[k];return va+(vb-va)*(h-a)/(b-a)}return T[T.length-1][1]};
function densHora(){const h=((CIELO.h%24)+24)%24;DENS.t=dInterp(DTAB_T,h);DENS.p=dInterp(DTAB_P,h)}
const azar=a=>a[Math.floor(Math.random()*a.length)];
const TXT={
 choque:['¡Mira por dónde vas!','¡Pero bueno, home!','¡Carallo!','¡Aprende a conducir!','¡Mi coche nuevo!','¡Esto lo pagas tú!','¡Animal!'],
 bus:['¡Que llevo gente!','¡Al de Vitrasa no, home!','¡Pero qué haces!'],
 pita:['¡Piii piii!','¡Muévete!','¡Que é para hoxe!','¡Venga, home!','¡Que levo présa!'],
 frente:['¡Ei, ei, ei!','¡Por tu carril!','¡Que vas al revés!','¡Madre mía!'],
 cede:['Vale, vale…','¡Pasa, pasa!','¡Qué prisas!','Tranquilo, home'],
 susto:['¡Ay, mi madre!','¡Cuidado!','¡Ostras!','¡Que me matas!','¡Vai devagar!','¡Ei, meu!'],
 caido:['¡Ayyy!','¡Mi espalda!','¡Uyyy!'],
 enfadado:['¡Llamo a la policía!','¡Loco del volante!','¡Te he visto, eh!','¡Carallo, qué daño!'],
 pitaP:['¡Ya voy, ya voy!','¡Qué prisas!','¡Tranquilo!','¡Uy, perdón!']};
function trafReset(c){c.ko=0;c.ox=c.oy=0;c.rot=0;c.lat=0;c.latT=0;c.esq=0;c.adel=0;c.cede=0;c.tb=0;c.pasa=0;c.pitado=false}
function carrilLibre(c,x0,y0,fx,fy,rvx,rvy,l){const off=(c.r.c==='m'?.02:.04)+l;for(const d of[0,.08,.16]){const t=cell(x0+fx*d+rvx*off,y0+fy*d+rvy*off).t;if(t===3||t===0||t===6||t===-1)return false}return true}
// claxon sintetizado (dos tonos), con volumen según la distancia
let _clxT=0;
function claxon(x,y,tipo,n=1){if(!AC||!soundOn||tipo!=='jug')return;   // los coches del tráfico ya no pitan (solo el jugador)
 const d=Math.hypot(x-P.x,y-P.y),vol=(tipo==='jug'?.13:.11)*Math.max(0,1-d/1.8);if(vol<.008)return;
 const t0=AC.currentTime,fr=tipo==='bus'?[196,247]:tipo==='moto'?[587,698]:tipo==='jug'?[349,440]:tipo==='furgoneta'?[294,370]:[392,494],f=AC.createBiquadFilter();f.type='lowpass';f.frequency.value=2200;f.connect(master);
 let t=t0;for(let k=0;k<n;k++){const dur=(n>1?.16:.32)+Math.random()*.08,g=AC.createGain();g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(vol,t+.015);g.gain.setValueAtTime(vol,t+dur-.03);g.gain.linearRampToValueAtTime(0,t+dur);g.connect(f);
  for(const fq of fr){const o=AC.createOscillator();o.type='sawtooth';o.frequency.value=fq*(.98+Math.random()*.04);o.connect(g);o.start(t);o.stop(t+dur+.02)}t+=dur+.09}}
// el jugador pita: el coche de delante se aparta, los peatones de delante se apartan
function pitar(){if(!driving||MODO==='heli'||MODO==='pie'||RACE.on)return;const now=performance.now();if(now-_clxT<350)return;_clxT=now;claxon(P.x,P.y,'jug',1);padVibra(.15,0,90);
 if(REP.on&&!REP.heli)return;const hx=Math.cos(P.a),hy=-Math.sin(P.a);
 for(const c of TRAF){if(c.inact||!c.g.visible||c.ko>0)continue;const ex=c.x-P.x,ey=c.y-P.y,al=ex*hx+ey*hy;if(al<0||al>.45||Math.abs(ex*hy-ey*hx)>.06)continue;
  const ca=c.g.rotation.y;if(Math.cos(ca)*hx-Math.sin(ca)*hy<.4)continue;const[x0,y0,a0]=posRuta(c.r,c.s);const fx=Math.cos(a0)*c.dir,fy=-Math.sin(a0)*c.dir,an=a0+(c.dir<0?Math.PI:0);
  if(carrilLibre(c,x0,y0,fx,fy,Math.sin(an),Math.cos(an),.05)){c.latT=.05;c.cede=3}else c.cede=1.5;burbuja(c,azar(TXT.cede),'')}
 for(const q of PEA){if(q.x>1e4||q.caido>0)continue;const ex=q.x-P.x,ey=q.y-P.y,al=ex*hx+ey*hy;if(al<0||al>.4||Math.abs(ex*hy-ey*hx)>.1)continue;peaEsquiva(q,ex,ey,hx,hy,.035);if(Math.random()<.5)burbuja(q,azar(TXT.pitaP),'')}}
addEventListener('keydown',e=>{if(driving&&e.code==='KeyH'&&!e.repeat)pitar()});
{const bp=document.getElementById('bPita');if(bp)bp.addEventListener('pointerdown',e=>{e.preventDefault();pitar()})}
// choques con el tráfico (coche y moto): empujas al otro, frenas, y el conductor protesta
function choqueTrafico(){const ca0=Math.cos(P.a),sa0=-Math.sin(P.a);let vx=ca0*P.v,vy=sa0*P.v;
 for(const c of TRAF){if(c.inact||!c.g.visible||c.pasa>0)continue;const ca=c.g.rotation.y,hx=Math.cos(ca),hy=-Math.sin(ca),hl=c.bus?.07:c.tipo==='moto'?.014:.03;
  const rx=P.x-c.x,ry=P.y-c.y;if(Math.abs(rx)>.2||Math.abs(ry)>.2)continue;const t=Math.max(-hl,Math.min(hl,rx*hx+ry*hy)),qx=rx-hx*t,qy=ry-hy*t,d=Math.hypot(qx,qy),lim=(c.tipo==='moto'?.014:c.bus?.03:.022)+.024;
  if(d>=lim||d<1e-6)continue;const nx=qx/d,ny=qy/d;P.x+=nx*(lim-d);P.y+=ny*(lim-d);
  const tv=c.ko>0?0:(c.vv||0),tvx=hx*tv,tvy=hy*tv,vn=(vx-tvx)*nx+(vy-tvy)*ny;if(vn>=0)continue;const imp=-vn,m=c.bus?.25:c.tipo==='moto'?1.4:.8;
  vx-=nx*vn*(1.25+(c.bus?.3:0));vy-=ny*vn*(1.25+(c.bus?.3:0));P.v=vx*ca0+vy*sa0;
  if(imp>.06){golpe();padVibra(Math.min(1,.3+imp),Math.min(1,imp*1.5),200);c.ko=Math.max(c.ko||0,.9+imp*2.4);c.kvx=(c.kvx||0)-nx*imp*.45*m;c.kvy=(c.kvy||0)-ny*imp*.45*m;c.kw=(Math.random()<.5?-1:1)*imp*7*m;c.esq=0;c.adel=0;c.latT=c.lat||0;REP.on||(window.CHOQUES=(window.CHOQUES||0)+1)}
  else if(!c.pitado){c.pitado=true;c.tb2=2;claxon(c.x,c.y,c.tipo,1)}}}
// peatones: esquivan si vas hacia ellos, se caen si los rozas, y luego protestan
function peaEsquiva(q,ex,ey,hx,hy,v){if(q.esq>0||q.caido>0)return;let px=ex-hx*(ex*hx+ey*hy),py=ey-hy*(ex*hx+ey*hy);let l=Math.hypot(px,py);if(l<.006){px=-hy*(Math.random()<.5?1:-1);py=hx*(px===-hy?1:-1);l=1}
 q.evx=px/l*v*(1.8+Math.random()*.5);q.evy=py/l*v*(1.8+Math.random()*.5);q.esq=.55+Math.random()*.25}
function peaReacciona(q,dt){let face=null;
 if(q.caido>0){q.caido-=dt;const dm=Math.exp(-dt*4);q.ex+=q.kvx*dt;q.ey+=q.kvy*dt;q.kvx*=dm;q.kvy*=dm;q.tilt=q.caido>.9?Math.min(1.45,(q.tilt||0)+dt*7):Math.max(0,q.tilt-dt*2);
  if(q.caido<=0){q.tilt=0;q.enfT=1.4;if(Math.hypot(q.x-P.x,q.y-P.y)<1.2)burbuja(q,azar(TXT.enfadado),'enf')}return Math.atan2(-q.kvy0,q.kvx0)+Math.PI}
 if(q.enfT>0){q.enfT-=dt;face=Math.atan2(-(P.y-q.y),P.x-q.x)}
 if(q.esq>0){q.esq-=dt;const nx=q.ex+q.evx*dt,ny=q.ey+q.evy*dt,t=cell(q.x+nx,q.y+ny).t;if(t!==3&&t!==0&&t!==6&&t!==-1){q.ex=nx;q.ey=ny}face=Math.atan2(-q.evy,q.evx)}
 else if(q.ex||q.ey){const dm=Math.exp(-dt*.5);q.ex*=dm;q.ey*=dm;if(Math.abs(q.ex)+Math.abs(q.ey)<.002)q.ex=q.ey=0}
 const car_=driving&&(MODO==='coche'||MODO==='motoc')&&!RACE.on&&!(REP.on&&!REP.heli);if(!car_)return face;
 const sp=Math.abs(P.v);if(sp<.1)return face;const sg=Math.sign(P.v),hx=Math.cos(P.a)*sg,hy=-Math.sin(P.a)*sg,ex=q.x-P.x,ey=q.y-P.y,d=Math.hypot(ex,ey);
 if(d<.034&&sp>.14){q.caido=2.6;q.esq=0;q.kvx=q.kvx0=hx*sp*.3+ex/d*.06;q.kvy=q.kvy0=hy*sp*.3+ey/d*.06;P.v*=.85;golpe();padVibra(.4,.5,140);if(Math.random()<.8)burbuja(q,azar(TXT.caido),'sus');return face}
 const al=ex*hx+ey*hy,lt=Math.abs(ex*hy-ey*hx);if(al>-.01&&al<.1+.3*sp&&lt<.055){peaEsquiva(q,ex,ey,hx,hy,.05);if(Math.random()<.45)burbuja(q,azar(TXT.susto),'sus')}
 return face}
// bocadillos encima de quien habla (se proyectan a la pantalla en cada fotograma)
const BURB=[],_vB=new THREE.Vector3();
function burbuja(o,txt,cls){if(!driving||RACE.on)return;const now=performance.now();if(o._bT&&now-o._bT<3800)return;if(Math.hypot(o.x-P.x,o.y-P.y)>1.3)return;o._bT=now;
 let b=BURB.find(x=>!x.on);if(!b){if(BURB.length>=5)b=BURB.reduce((a,x)=>a.t0<x.t0?a:x);else{const el=document.createElement('div');el.className='burb';document.body.appendChild(el);b={el};BURB.push(b)}}
 Object.assign(b,{on:true,o,t0:now,ttl:2300});b.el.textContent=txt;b.el.className='burb '+(cls||'')}
window.__VIDA={burbuja:(...a)=>burbuja(...a),pitar:()=>pitar(),BURB};
function burbujasTick(){const now=performance.now();let rc=null;for(const b of BURB){if(!b.on)continue;const age=now-b.t0;
  if(age>b.ttl||!driving||RACE.on||b.o.x>1e4){b.on=false;b.el.style.display='none';continue}
  _vB.set(b.o.x,(b.o.z??0)+(b.o.g?(b.o.bus?.1:.075):.072),b.o.y).project(pcam);if(_vB.z>1||Math.abs(_vB.x)>1.1||Math.abs(_vB.y)>1.1){b.el.style.display='none';continue}
  rc=rc||R.domElement.getBoundingClientRect();b.el.style.display='block';b.el.style.left=(rc.left+(_vB.x*.5+.5)*rc.width)+'px';b.el.style.top=(rc.top+(-_vB.y*.5+.5)*rc.height)+'px';
  b.el.style.opacity=Math.min(1,(b.ttl-age)/300,age/120).toFixed(2)}}""")

# ---- sin bocinazos de fondo de la ciudad
r("if(t>nextHorn){nextHorn=t+30+Math.random()*30;if(mar<.5)horn()}}","if(t>nextHorn){nextHorn=t+30+Math.random()*30}}")
# ---- colisión del coche del jugador con el tráfico
# (sin choques con el tráfico: el coche del jugador atraviesa los coches, a petición del usuario)

# ---- mando: LB = claxon (fuera del helicóptero)
r("if(dn(5)&&!heli&&RACE.on)usarTurbo()}","if(dn(5)&&!heli&&RACE.on)usarTurbo();if(dn(4)&&!heli)pitar()}")

# ---- aviso la primera vez que conduces por la ciudad
r("function setDrive(on,modo='coche'){","function setDrive(on,modo='coche'){if(on&&!window.SOLO_CARRERA&&!window._avClx){window._avClx=1;setTimeout(()=>{if(driving&&!RACE.on)mostrar(matchMedia('(pointer:coarse)').matches?'📯 Toca 📯 para pitar · la ciudad reacciona a cómo conduces':'📯 H (o LB en el mando) para pitar · la ciudad reacciona a cómo conduces')},5000)}")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok vida')
