import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= REPARTO DE NAVIDAD: RUTAS SEGUIDAS + MISIÓN DE LLEGADA EN CARROZA VOLADORA =================
# · Ya no hay que volver a Policarpo Sanz: al entregar, la siguiente entrega sale desde donde estás.
# · El mapa se abre poco a poco: primero solo el centro (Príncipe, García Barbón, Policarpo Sanz, Vialia, Urzaiz),
#   luego los alrededores y después toda la ciudad.
# · Misión 0: Papá Noel (o el Rey Mago elegido) llega por el aire desde la ría en su carroza tirada por renos voladores,
#   recoge los regalos que flotan en el cielo; el último está a la altura del árbol gigante de Porta do Sol. Al cogerlo,
#   la carroza baja en espiral hasta Policarpo Sanz, el personaje salta a su carroza de calle y empiezan las rutas.

# --- 1) etapas de la campaña: el centro primero (solo sus calles), luego alrededores, luego toda la ciudad
r("if(e[0]==='c')return{v:'coche',rad:6+.6*e[1],txt:'🎄 Centro · '+(e[1]+1)+'/4'};if(e[0]==='a')return{v:'coche',rad:11+2*e[1],txt:'🏘️ Alrededores · '+(e[1]+1)+'/2'};",
  "if(e[0]==='c')return{v:'coche',rad:12.5,centro:true,txt:'🎄 Centro · '+(e[1]+1)+'/4'};if(e[0]==='a')return{v:'coche',rad:15+2*e[1],txt:'🏘️ Alrededores · '+(e[1]+1)+'/2'};")
r("if(e[0]==='L')return{v:'coche',luces:true,n:5,txt:'✨ Encendido de luces'};",
  "if(e[0]==='L')return{v:'coche',luces:true,centro:true,n:5,txt:'✨ Encendido de luces'};")
# --- 2) elegir la siguiente entrega desde donde está el jugador (no desde el almacén)
r("function repElegir(){if(REP.red&&!REP.heli){const pool=repPool(),",
  r"""const RUTA_CEN=/Príncipe|García Barbón|Policarpo Sanz|Urz[aá]iz|Estación de Vigo|Vialia|Lepanto|Vía Norte/i;
function repElegir(){if(REP.red&&!REP.heli){const m=REP.mis||{},cen=!!m.centro,R=REP.rad||REP_R0,dep=d=>Math.hypot(d[1]-REP_DEP[1],d[2]-REP_DEP[2]),dp=d=>Math.hypot(d[1]-P.x,d[2]-P.y),nuevo=d=>!REP.ult.some(u=>Math.hypot(u[0]-d[1],u[1]-d[2])<.8);
  let pool=repPool();if(cen){const pc=pool.filter(d=>RUTA_CEN.test(d[0]));if(pc.length>4)pool=pc}
  // rutas seguidas: a media distancia de donde estás; al abrirse una zona nueva, se tira hacia lo nuevo
  const dmn=cen?1.6:2.4,dmx=cen?7:Math.min(11,4+R*.35),lejos=R-dep(P)>4&&!cen;
  let L=pool.filter(d=>dep(d)<R-.3&&dp(d)>dmn&&dp(d)<dmx&&nuevo(d));if(lejos&&L.length>6){const Lf=L.filter(d=>dep(d)>R-6);if(Lf.length>2&&Math.random()<.6)L=Lf}
  if(!L.length)L=pool.filter(d=>dep(d)<R-.3&&dp(d)>1.2&&nuevo(d));if(!L.length)L=pool.filter(d=>dep(d)<R);if(!L.length)L=repPool();return L[Math.floor(Math.random()*L.length)]}
 return repElegir0()}
function repElegirViejo(){if(REP.red&&!REP.heli){const pool=repPool(),""")
# --- 3) la carroza de calle aparece en la calle más cercana (al bajar del helicóptero o de la moto)
r("function repMisionNueva(ini){",
  r"""function repCocheCalle(){let b=null,bd=1e9;for(const d of repPool()){if(d.length<5)continue;const e=Math.hypot(d[1]-P.x,d[2]-P.y);if(e<bd){bd=e;b=d}}
 if(!b){campVeh('coche',REP_DEP[1],REP_DEP[2],0);return}campVeh('coche',b[1],b[2],Math.atan2(-b[4],b[3]))}
function repMisionNueva(ini){""")
# moto: primero hay que llegar en coche al puerto, donde espera la moto de agua
r("REP.puerto=['Puerto de Vigo',pu[0],pu[1]];campVeh('moto',",
  r"""REP.puerto=['Puerto de Vigo',pu[0],pu[1]];if(MODO==='coche'&&!REP.enPuerto&&Math.hypot(pu[0]-P.x,pu[1]-P.y)>.6){let b=null,bd=1e9;for(const q of repPool()){const e=Math.hypot(q[1]-pu[0],q[2]-pu[1]);if(e<bd){bd=e;b=q}}
    if(b&&bd<2.5){REP.mis=m;REP.enPuerto=1;REP.fase='puerto';REP.carga=1;repPila();campDestino(['Puerto de Vigo · moto de agua',b[1],b[2]]);repMarcaColor(0x35e0ff);aviso('🌊 Misión '+(k+1)+' · ¡Al puerto!',2,'cuenta');setTimeout(()=>{if(REP.on&&!REP.fin)mostrar('Conduce hasta el Puerto de Vigo: allí te espera la moto de agua')},2200);return}}
   REP.enPuerto=0;campVeh('moto',""")
r("if(m.v==='heli'){campVeh('heli',REP_DEP[1],REP_DEP[2],P.a);","if(m.v==='heli'){campVeh('heli',P.x,P.y,P.a);")
r("if(m.luces){REP.mis=m;if(MODO!=='coche')campVeh('coche',REP_DEP[1],REP_DEP[2],0);","if(m.luces){REP.mis=m;if(MODO!=='coche')repCocheCalle();")
r("if(MODO!=='coche'){campVeh('coche',REP_DEP[1],REP_DEP[2],0);aviso('🎅 ¡De vuelta a la carroza!',1.4,'peq')}",
  "if(MODO!=='coche'){repCocheCalle();aviso((REP.spec&&REP.spec.t!=='sleigh'?'👑':'🎅')+' ¡De vuelta a la carroza!',1.4,'peq')}")
# --- 4) al entregar: la siguiente ruta empieza al momento desde ahí (solo la moto vuelve al puerto de Vigo)
r("""  const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;repVolver();
  const sig=m2.v==='heli'?' · ¡te espera el helicóptero!':m2.v==='moto'?' · ¡te espera la moto de agua!':'';setTimeout(()=>aviso((ab?'🔓 ¡Nueva zona desbloqueada! ':'↩️ ')+'Vuelve a '+(m.v==='moto'?'Vigo':'Policarpo Sanz')+sig,2.2,'peq'),1300)}""",
  """  const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;
  if(m.v==='moto'){repVolver();setTimeout(()=>{if(REP.on&&!REP.fin)aviso('↩️ Vuelve al Puerto de Vigo',2,'peq')},1300)}
  else repSigue(ab,1100)}""")
r("""function repVolver(){""","""function repSigue(ab,ms){REP.dest=null;REP.fase='espera';REP.marca.visible=false;gpsParar();repHud();
 setTimeout(()=>{if(!REP.on||REP.fin)return;repMisionNueva(false);if(ab)setTimeout(()=>{if(REP.on&&!REP.fin)aviso('🔓 ¡Nueva zona de Vigo desbloqueada!',2.4,'peq')},900)},ms)}
function repVolver(){""")
r(""" const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;repVolver();
 const sig=m2.v==='heli'?' · ¡te espera el helicóptero!':m2.v==='moto'?' · ¡te espera la moto de agua!':'';setTimeout(()=>{if(REP.on&&!REP.fin)aviso((ab?'🔓 ¡Nueva zona desbloqueada! ':'↩️ ')+'Vuelve a Policarpo Sanz'+sig,2.2,'peq')},2600)}""",
  """ const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;repSigue(ab,2600)}""")
r("${REP.fase==='recoger'?(REP.mis&&REP.mis.v==='moto'?'↩️ Puerto de Vigo':'↩️ Policarpo Sanz'):'📍'}",
  "${REP.fase==='recoger'?'↩️ Puerto de Vigo':REP.fase==='puerto'?'🌊 Puerto':REP.mis&&REP.mis.v==='intro'?'🎁':'📍'}")

r("(MODO==='heli'&&d&&dd<.8?'<span class=\"r ok\">⤓ Aterriza</span>':'')","(MODO==='heli'&&d&&dd<.8&&!(REP.mis&&REP.mis.v==='intro')?'<span class=\"r ok\">⤓ Aterriza</span>':'')")
r("+(REP.mis?`<span class=\"d\">Misión ${(REP.nEnt||0)+(REP.fase==='recoger'?0:1)}","+(REP.mis&&REP.mis.v==='intro'?`<span class=\"d\">✨ Llegada a Vigo</span>`:'')+(REP.mis&&REP.mis.v!=='intro'?`<span class=\"d\">Misión ${(REP.nEnt||0)+(REP.fase==='recoger'?0:1)}")
r("${d?fmtD(dd):(MODO==='heli'?'buscando tejado…':'—')}","${d?fmtD(dd):(MODO==='heli'&&!(REP.mis&&REP.mis.v==='intro')?'buscando tejado…':'—')}")
# --- 5) misión de llegada: carroza voladora con renos
r("function repMision(dt){const m=REP.mis||{v:'coche'};window.__TR=(window.__TR||0)+(dt||.016);lucesTick(dt||.016);if(REP.fin)return;",
  "function repMision(dt){const m=REP.mis||{v:'coche'};window.__TR=(window.__TR||0)+(dt||.016);lucesTick(dt||.016);if(REP.fin)return;if(m.v==='intro'){introTick(dt||.016);return}")
r("function repCocheCalle(){",r"""const INTRO={on:false,G:[],i:0,anim:null,t:0};window.__INTRO=INTRO;
function introRenos(spec){const g=new THREE.Group();g.name='introTrineo';const M=(c,r_=.5,mt=0,e=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r_,metalness:mt,emissive:e?c:0,emissiveIntensity:e});
 const santa=spec.t==='sleigh',C=santa?0xc4161f:spec.col[0],ORO=M(0xf5c84a,.25,.9),CU=M(C,.35,.3),OSC=M(0x4a2a16,.7);
 const add=(geo,mat,x,y,z,rx=0,ry=0,rz=0,par=g)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.rotation.set(rx,ry,rz);par.add(m);return m};
 // carroza: caja, respaldo alto, frontal curvo, filos dorados y patines con la punta enroscada
 add(new THREE.BoxGeometry(.11,.03,.07),CU,0,.035,0);add(new THREE.BoxGeometry(.024,.068,.072),CU,-.05,.056,0);add(new THREE.BoxGeometry(.03,.022,.07),CU,.052,.044,0);
 add(new THREE.CylinderGeometry(.036,.036,.072,16,1,false,0,Math.PI),CU,-.05,.09,0,Math.PI/2,0,0);
 for(const z of[.037,-.037]){add(new THREE.BoxGeometry(.12,.006,.004),ORO,0,.051,z);add(new THREE.CylinderGeometry(.0028,.0028,.14,6),ORO,-.005,.006,z,0,0,Math.PI/2);
  add(new THREE.TorusGeometry(.018,.0028,6,14,Math.PI),ORO,.065,.024,z,0,0,-Math.PI/2);for(const x of[-.035,.03])add(new THREE.CylinderGeometry(.002,.002,.018,5),ORO,x,.015,z)}
 // saco de regalos
 add(new THREE.SphereGeometry(.026,12,9),M(0x8a5a2b,.9),-.028,.07,0).scale.set(1,1.15,1);const CR=[0xd51f1f,0x1fae4a,0xf2c230,0x1f6fd0,0xc23fd0];for(let k=0;k<5;k++)add(new THREE.BoxGeometry(.014,.014,.014),M(CR[k],.5,0,.25),-.04+(k%3)*.012,.098+(k>2?.01:0),-.012+(k%2)*.024,0,k,0);
 if(!santa){// carroza de Rey Mago: dosel con columnas doradas y corona
  for(const[x,z]of[[.035,.03],[.035,-.03],[-.035,.03],[-.035,-.03]])add(new THREE.CylinderGeometry(.0022,.0022,.07,6),ORO,x,.085,z);add(new THREE.BoxGeometry(.09,.006,.075),CU,0,.122,0);add(new THREE.CylinderGeometry(.014,.018,.012,10),ORO,0,.131,0)}
 // cuatro renos voladores (el de delante con la nariz roja), arneses dorados
 const PEL=M(0x7a4a2a,.8),PEC=M(0xe8dcc8,.85),NAR=M(0xff2a1a,.4,0,1.6),NEG=M(0x1a1410,.5),ren=[];
 for(const[x,z,lead]of[[.16,.03,0],[.16,-.03,0],[.25,.03,1],[.25,-.03,1]]){const R=new THREE.Group();R.position.set(x,.03,z);g.add(R);
  const cu=add(new THREE.CylinderGeometry(.011,.012,.04,10),PEL,0,.03,0,0,0,Math.PI/2,R);add(new THREE.SphereGeometry(.011,10,8),PEL,.02,.03,0,0,0,0,R);add(new THREE.SphereGeometry(.012,10,8),PEL,-.02,.03,0,0,0,0,R);
  add(new THREE.SphereGeometry(.007,8,6),PEC,-.03,.036,0,0,0,0,R);add(new THREE.CylinderGeometry(.006,.007,.026,8),PEL,.028,.047,0,0,0,-.7,R);
  add(new THREE.SphereGeometry(.009,10,8),PEL,.038,.06,0,0,0,0,R);add(new THREE.CylinderGeometry(.0045,.006,.016,8),PEL,.048,.057,0,0,0,Math.PI/2,R);
  add(new THREE.SphereGeometry(lead?.0042:.003,8,6),lead?NAR:NEG,.057,.057,0,0,0,0,R);
  for(const s_ of[1,-1]){add(new THREE.SphereGeometry(.0028,6,5),PEC,.036,.068,s_*.0065,0,0,0,R).scale.set(.6,1,1.4);
   add(new THREE.CylinderGeometry(.0013,.0016,.024,5),OSC,.034,.078,s_*.007,s_*.35,0,.25,R);add(new THREE.CylinderGeometry(.001,.0013,.011,5),OSC,.04,.085,s_*.011,s_*.6,0,-.5,R);add(new THREE.CylinderGeometry(.001,.0013,.01,5),OSC,.028,.088,s_*.012,s_*.7,0,.9,R)}
  const legs=[];for(const[lx,lz]of[[.014,.006],[.014,-.006],[-.016,.006],[-.016,-.006]]){const pv=new THREE.Group();pv.position.set(lx,.024,lz);R.add(pv);add(new THREE.CylinderGeometry(.0024,.0018,.026,5),PEL,0,-.013,0,0,0,0,pv);legs.push(pv)}
  add(new THREE.BoxGeometry(.006,.004,.028),ORO,.012,.042,0,0,0,0,R);ren.push({R,legs,ph:x*30+(z>0?1.3:0)})}
 for(const z of[.03,-.03])add(new THREE.CylinderGeometry(.0013,.0013,.2,5),M(0x6a3a1a,.6),.16,.074,z,0,0,Math.PI/2-.06);
 add(new THREE.CylinderGeometry(.0018,.0018,.07,5),ORO,.16,.058,0,Math.PI/2,0,0);add(new THREE.CylinderGeometry(.0018,.0018,.07,5),ORO,.25,.058,0,Math.PI/2,0,0);
 // estela de polvo de estrellas
 const N=60,eg=new THREE.BufferGeometry(),ep=new Float32Array(N*3);eg.setAttribute('position',new THREE.BufferAttribute(ep,3));
 const cvE=document.createElement('canvas');cvE.width=cvE.height=32;{const c=cvE.getContext('2d'),gr=c.createRadialGradient(16,16,0,16,16,16);gr.addColorStop(0,'rgba(255,255,255,1)');gr.addColorStop(.35,'rgba(255,236,170,.8)');gr.addColorStop(1,'rgba(255,220,120,0)');c.fillStyle=gr;c.fillRect(0,0,32,32)}
 const est=new THREE.Points(eg,new THREE.PointsMaterial({color:0xffe9a0,map:new THREE.CanvasTexture(cvE),size:.022,transparent:true,opacity:.9,depthWrite:false,toneMapped:false,blending:THREE.AdditiveBlending}));est.frustumCulled=false;
 g.userData={ren,est,ep,N,k:0,tt:0};return g}
function introVestir(){heliVestir(REP.spec,RACE.sel.col);const u=heli.userData;u.introVis=heli.children.map(o=>o.visible);for(const o of heli.children)if(o.name!=='navPiloto')o.visible=false;
 const g=introRenos(REP.spec);heli.add(g);scene.add(g.userData.est);INTRO.trineo=g;const pil=heli.getObjectByName('navPiloto');if(pil){INTRO.pil0=pil.position.clone()}}
function introDesvestir(){const g=INTRO.trineo;if(g){heli.remove(g);scene.remove(g.userData.est);INTRO.trineo=null}const u=heli.userData;if(u.introVis){heli.children.forEach((o,i)=>{if(i<u.introVis.length)o.visible=u.introVis[i]});u.introVis=null}
 const pil=heli.getObjectByName('navPiloto');if(pil&&INTRO.pil0)pil.position.copy(INTRO.pil0)}
function introRegalo(x,y,z,k,N){const g=new THREE.Group(),C=[0xd51f1f,0x1fae4a,0x1f6fd0,0xc23fd0,0xf2c230][k%5],ult=k===N-1,S=ult?.085:.06;
 const M=(c,e)=>new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:e,roughness:.45});g.add(new THREE.Mesh(new THREE.BoxGeometry(S,S,S),M(C,.35)));
 const O=M(0xffd24a,.7);for(const[a,b,c]of[[S*1.03,S*1.03,S*.2],[S*.2,S*1.03,S*1.03]])g.add(new THREE.Mesh(new THREE.BoxGeometry(a,b,c),O));
 for(const s_ of[1,-1]){const l=new THREE.Mesh(new THREE.TorusGeometry(S*.22,S*.07,6,12),O);l.position.set(s_*S*.18,S*.6,0);l.rotation.y=Math.PI/2;g.add(l)}
 const hal=new THREE.Mesh(new THREE.SphereGeometry(S*1.9,16,12),new THREE.MeshBasicMaterial({color:ult?0xfff0a0:0xffe08a,transparent:true,opacity:.18,depthWrite:false,toneMapped:false,blending:THREE.AdditiveBlending}));g.add(hal);
 const haz=new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,1.4,8,1,true),new THREE.MeshBasicMaterial({color:0xffe9a0,transparent:true,opacity:.35,depthWrite:false,toneMapped:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide}));haz.position.y=.72;haz.visible=false;g.add(haz);
 g.position.set(x,z,y);scene.add(g);REP.objs.push(g);return{x,y,z,g,hal,haz,on:true,ult}}
function introInicio(){const I=INTRO;I.on=true;I.i=0;I.anim=null;I.t=0;REP.mis={v:'intro',txt:'Llegada'};REP.fase='intro';REP.carga=0;repPila();REP.marca.visible=false;REP.rad=REP.rad||REP_R0;
 const T=[87.45,18.0],gt=groundMap(T[0],T[1]),Tz=gt+2.2+.34,S=aguaCerca(86.6,5.6,5)||[86.6,5.6],z0=Math.max(groundY(S[0],S[1]),0)+1.45;
 const N=12,dx=T[0]-S[0],dy=T[1]-S[1],L=Math.hypot(dx,dy),nx=-dy/L,ny=dx/L;for(const o of I.G)scene.remove(o.g);I.G=[];
 for(let k=1;k<=N;k++){const t=k/N,lat=Math.sin(t*Math.PI*2.3)*1.15*(1-t*t),x=S[0]+dx*t+nx*lat,y=S[1]+dy*t+ny*lat,z=k===N?Tz:z0+(Tz-.15-z0)*t+Math.sin(t*Math.PI)*.35+Math.sin(k*1.7)*.06;I.G.push(introRegalo(x,y,Math.max(z,groundY(x,y)+.9),k-1,N))}
 const g0=I.G[0];campVeh('heli',S[0],S[1],Math.atan2(-(g0.y-S[1]),g0.x-S[0]));P.z=z0;P.v=.9;HELI.posado=false;introVestir();camInit=false;
 REP.dest=['🎁 Regalo 1/'+N,g0.x,g0.y];gpsSet(REP.dest,linea([[P.x,P.y],[g0.x,g0.y]]));repHud();document.getElementById('bSaltar').hidden=false;
 const quien=REP.spec&&REP.spec.t!=='sleigh'?'👑 '+REP.spec.corto:'🎅 Papá Noel';aviso(quien+' llega a Vigo',2.4,'cuenta');
 setTimeout(()=>{if(I.on&&!I.anim)mostrar('◀ ▶ guía a los renos · ⤒ Q / ⤓ Z altura · recoge los '+N+' regalos que flotan sobre la ría')},2500)}
function introTick(dt){const I=INTRO;if(!I.on)return;I.t+=dt;const g=I.trineo;
 if(g){const u=g.userData;u.tt+=dt;for(const R of u.ren){R.R.position.y=.03+Math.sin(u.tt*7+R.ph)*.004;R.legs.forEach((l,i)=>l.rotation.z=Math.sin(u.tt*11+R.ph+(i>1?Math.PI:0))*.7)}
  u.k=(u.k+1)%u.N;const b=new THREE.Vector3(-.07,.01,0).applyMatrix4(heli.matrixWorld);u.ep[u.k*3]=b.x+(Math.random()-.5)*.02;u.ep[u.k*3+1]=b.y+(Math.random()-.5)*.02;u.ep[u.k*3+2]=b.z+(Math.random()-.5)*.02;u.est.geometry.attributes.position.needsUpdate=true}
 for(const q of I.G)if(q.on){q.g.rotation.y+=dt*1.5;q.g.position.y=q.z+Math.sin(I.t*2.4+q.x)*.015;const s=1+.12*Math.sin(I.t*5+q.y);q.hal.scale.set(s,s,s)}
 if(I.anim){introAnim(dt);return}
 const q=I.G[I.i];if(!q)return;q.haz.visible=true;
 // vuelo asistido: los renos siempre avanzan y suben o bajan solos hacia el regalo si no tocas la altura
 if(!keys.down)P.v=Math.max(P.v,1.05);if(!keys.alt_up&&!keys.alt_dn)P.z+=(q.z-P.z)*Math.min(1,dt*1.3);
 if(Math.hypot(q.x-P.x,q.y-P.y)<.2&&Math.abs(q.z-(P.z+.05))<.28){q.on=false;scene.remove(q.g);REP.pts+=50;try{sonMoneda();if(q.ult){sonJoJo();setTimeout(()=>sonPublico(1.2),400)}}catch(e){}
  I.i++;repPop(q.ult?'🎁 ¡Todos los regalos! +50 ⭐':'🎁 '+I.i+'/'+I.G.length+' · +50 ⭐',q.ult?'gran':'');
  const n=I.G[I.i];if(n){REP.dest=['🎁 Regalo '+(I.i+1)+'/'+I.G.length,n.x,n.y];gpsSet(REP.dest,linea([[P.x,P.y],[n.x,n.y]]))}else introBaja();repHud()}
 else if(I.t%0.5<dt&&REP.dest){gpsSet(REP.dest,linea([[P.x,P.y],[q.x,q.y]]))}}
function introBaja(){const I=INTRO;REP.dest=null;gpsParar();const L=[REP_DEP[1],REP_DEP[2]];I.anim={t:0,x0:P.x,y0:P.y,z0:P.z,L,zl:groundY(L[0],L[1]),a0:Math.atan2(P.y-L[1],P.x-L[0]),f:1};
 const quien=REP.spec&&REP.spec.t!=='sleigh'?REP.spec.corto:'Papá Noel';aviso('✨ ¡'+quien+' baja a la ciudad!',2.6,'cuenta');try{confeti()}catch(e){}}
function introAnim(dt){const A=INTRO.anim;A.t+=dt;P.v=0;P.vz=0;
 if(A.f===1){const D=6,k=Math.min(1,A.t/D),e=k*k*(3-2*k),r_=1.1*Math.sin(Math.PI*Math.min(1,e*1.25))*(1-e),an=A.a0+e*Math.PI*2.6;
  const x=A.x0+(A.L[0]-A.x0)*e+Math.cos(an)*r_,y=A.y0+(A.L[1]-A.y0)*e+Math.sin(an)*r_,z=A.zl+(A.z0-A.zl)*(1-e*e*e);
  const vx=x-P.x,vy=y-P.y;if(Math.hypot(vx,vy)>1e-5)P.a=Math.atan2(-vy,vx);P.x=x;P.y=y;P.z=z;HELI.posado=false;if(k>=1){A.f=2;A.t=0;try{sonCaja();setTimeout(sonJoJo,200)}catch(e){}}return}
 // el personaje salta de la carroza voladora a la calle
 const pil=heli.getObjectByName('navPiloto');P.z=A.zl;if(pil&&INTRO.pil0){const k=Math.min(1,A.t/1.1);pil.position.set(INTRO.pil0.x-k*.02,INTRO.pil0.y+Math.sin(k*Math.PI)*.09-k*.05,INTRO.pil0.z+k*.11)}
 if(A.t>1.4)introFin(false)}
function introFin(salto){const I=INTRO;if(!I.on)return;I.on=false;I.anim=null;for(const q of I.G)scene.remove(q.g);I.G=[];introDesvestir();document.getElementById('bSaltar').hidden=true;
 if(salto)campVeh('coche',REP_DEP[1],REP_DEP[2],0);else repCocheCalle();P.v=0;REP.mis=null;REP.fase='entregar';repMisionNueva(true);
 const quien=REP.spec&&REP.spec.t!=='sleigh'?'👑 '+REP.spec.corto:'🎅 Papá Noel';aviso(quien+' ya está en Vigo · ¡a repartir!',2,'cuenta');
 setTimeout(()=>{if(REP.on&&!REP.fin)mostrar('▲ acelera · ◀ ▶ gira · sigue el GPS: cada entrega te lleva a la siguiente')},2200)}
function repCocheCalle(){""")
# arranque: primero la llegada por el aire
r("if((REP.red&&!REP.heli))repMisionNueva(true);else repSiguiente();aviso('🎄 ¡A repartir!',1.4,'cuenta');if(!REP.heli)setTimeout(()=>{if(REP.on&&!REP.fin)mostrar('▲ acelera · ◀ ▶ gira · sigue el GPS y lleva el regalo a la marca dorada')},1600);",
  "if((REP.red&&!REP.heli)){REP.rad=REP_R0;introInicio()}else{repSiguiente();aviso('🎄 ¡A repartir!',1.4,'cuenta');if(!REP.heli)setTimeout(()=>{if(REP.on&&!REP.fin)mostrar('▲ acelera · ◀ ▶ gira · sigue el GPS y lleva el regalo a la marca dorada')},1600)}")
# botón para saltar la llegada
r('<button id="bFull"','<button id="bSaltar" hidden style="position:fixed;top:calc(12px + env(safe-area-inset-top));left:50%;transform:translateX(-50%);z-index:60;padding:8px 16px;border-radius:20px;border:1px solid rgba(255,255,255,.5);background:rgba(20,24,40,.72);color:#fff;font:600 14px system-ui;cursor:pointer">⏭ Saltar llegada</button><button id="bFull"')
r("const INTRO={on:false,","document.getElementById('bSaltar').addEventListener('click',e=>{e.preventDefault();e.currentTarget.blur();introFin(true)});\nconst INTRO={on:false,")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok rutas')
