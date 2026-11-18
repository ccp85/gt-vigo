import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MISIÓN «ENCENDIDO DE LUCES» (Reparto de Navidad) =================
# Por las calles del centro hay arcos de luces apagados. Hay que pasar por debajo de cada uno (la flecha y el GPS guían
# al siguiente) y se van encendiendo bombilla a bombilla. Los arcos encendidos se quedan así el resto de la partida.

# 1) campaña: la misión 3 es el encendido; luego vuelve en cada ciclo con más arcos
i=s.index("function campMision(k){");j=s.index("function aguaOK(",i)
s=s[:i]+r"""function campMision(k){const S=[['c',0],['c',1],['L'],['c',2],['c',3],['a',0],['a',1],['h'],['m']];
 if(k<S.length){const e=S[k];if(e[0]==='c')return{v:'coche',rad:6+.6*e[1],txt:'🎄 Centro · '+(e[1]+1)+'/4'};if(e[0]==='a')return{v:'coche',rad:11+2*e[1],txt:'🏘️ Alrededores · '+(e[1]+1)+'/2'};
  if(e[0]==='L')return{v:'coche',luces:true,n:5,txt:'✨ Encendido de luces'};if(e[0]==='h')return{v:'heli',txt:'🚁 Helicóptero · chimenea'};return{v:'moto',mar:'Cangas',txt:'🌊 Moto de agua · Cangas'}}
 const c=Math.floor((k-9)/5),j=(k-9)%5;if(j<2)return{v:'coche',rad:Math.min(REP_RMAX,15+3*c+1.5*j),txt:'🗺️ Vigo · ruta larga'};if(j===2)return{v:'heli',txt:'🚁 Helicóptero · chimenea'};
 if(j===3)return{v:'coche',luces:true,n:Math.min(9,6+c),txt:'✨ Encendido de luces · '+(c+2)};
 const n=CAMP_MAR[(c+1)%3];return{v:'moto',mar:n,txt:'🌊 Moto de agua · '+(n==='Cíes'?'Islas Cíes':n)}}
// ---------- arcos de luces
const LUZ={arcos:[],ruta:[],i:0,on:false,t:0};window.__LUZ=LUZ;
const LUZ_CALLES=/Príncipe|Porta do Sol|Gran Vía|Urzaiz|Colón|Policarpo|García Barbón|Praza de América|Elduayen|Velázquez Moreno|Areal|Marqués de Valladares|Pi i Margall|Venezuela|Camelias|Carral|Reconquista|Lepanto/i;
const LUZ_ON=[0xffd27a,0xfff3d0,0xffc35a,0xfff3d0],LUZ_OFF=new THREE.Color(0x6b5f45),_lc=new THREE.Color(),_lm=new THREE.Matrix4();
const LUZ_G={bom:new THREE.SphereGeometry(.0058,8,6),est:new THREE.OctahedronGeometry(.011,0),pos:new THREE.CylinderGeometry(.0022,.0028,1,6)};
const LUZ_M={gua:new THREE.MeshStandardMaterial({color:0x1f4d2c,roughness:.8}),pos:new THREE.MeshStandardMaterial({color:0x2b2d33,roughness:.5,metalness:.4})};
function luzAncho(x,y,nx,ny){let w=.045;const ok=t=>t===1||t===2||t===4||t===5;for(let s=.03;s<=.15;s+=.005){if(!ok(cell(x+nx*s,y+ny*s).t)||!ok(cell(x-nx*s,y-ny*s).t))break;w=s}return w}
function luzArco(d){let tx=d[3]||1,ty=d[4]||0;const L=Math.hypot(tx,ty)||1;tx/=L;ty/=L;const nx=-ty,ny=tx,x=d[1],y=d[2];const w=Math.max(.04,Math.min(.13,luzAncho(x,y,nx,ny)-.008));
 const g0=groundY(x,y),gA=groundY(x+nx*w,y+ny*w),gB=groundY(x-nx*w,y-ny*w),h0=Math.max(gA,gB,g0)+.058,G=new THREE.Group();
 // postes
 for(const[sg,gg] of [[1,gA],[-1,gB]]){const pm=new THREE.Mesh(LUZ_G.pos,LUZ_M.pos);const hh=h0+.006-gg;pm.scale.y=hh;pm.position.set(x+nx*w*sg,gg+hh/2,y+ny*w*sg);pm.castShadow=true;G.add(pm)}
 // guirnalda en arco
 const Q=[];for(let k=0;k<=16;k++){const t=k/16;Q.push(new THREE.Vector3(x+nx*w*(2*t-1),h0+.028*Math.sin(Math.PI*t),y+ny*w*(2*t-1)))}
 const tubo=new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(Q),40,.0035,5,false),LUZ_M.gua);G.add(tubo);
 // bombillas: arco, flecos colgando, estrella de luces en el centro y bajando por los postes
 const B=[],ARC=t=>[x+nx*w*(2*t-1),h0+.028*Math.sin(Math.PI*t),y+ny*w*(2*t-1)];const nb=Math.max(14,Math.round(w*2/.0075));
 for(let k=0;k<=nb;k++){const t=k/nb,p_=ARC(t);B.push([p_[0],p_[1]-.004,p_[2],Math.abs(t-.5)])}
 const nf=Math.max(4,Math.round(w*2/.026));for(let k=1;k<nf;k++){const t=k/nf;if(Math.abs(t-.5)<.12)continue;const p_=ARC(t);for(let q=1;q<=3;q++)B.push([p_[0],p_[1]-.004-q*.0085,p_[2],Math.abs(t-.5)+q*.05])}
 const cy=h0+.05;for(let k=0;k<14;k++){const th=k/14*Math.PI*2;B.push([x+nx*Math.cos(th)*.02,cy+Math.sin(th)*.02,y+ny*Math.cos(th)*.02,.02+k*.004])}
 for(let k=0;k<5;k++){const th=Math.PI/2+k/5*Math.PI*2;B.push([x+nx*Math.cos(th)*.011,cy+Math.sin(th)*.011,y+ny*Math.cos(th)*.011,.01])}
 for(const sg of[1,-1])for(let q=1;q<=5;q++){const gg=sg>0?gA:gB;B.push([x+nx*w*sg,h0-(h0-gg)*q/6,y+ny*w*sg,.55+q*.1])}
 const bm=new THREE.InstancedMesh(LUZ_G.bom,new THREE.MeshBasicMaterial({color:0xffffff}),B.length);B.forEach((b,i)=>{_lm.makeTranslation(b[0],b[1],b[2]);bm.setMatrixAt(i,_lm);bm.setColorAt(i,LUZ_OFF)});bm.instanceColor.needsUpdate=true;bm.frustumCulled=false;G.add(bm);
 const est=new THREE.Mesh(LUZ_G.est,new THREE.MeshBasicMaterial({color:LUZ_OFF.clone()}));est.position.set(x,cy,y);G.add(est);
 scene.add(G);REP.objs.push(G);const a={g:G,bm,B,est,x,y,w,tx,ty,nom:'Arco de luces · '+(d[0]||'calle'),lit:false,t:0};LUZ.arcos.push(a);return a}
function lucesInicio(m){const pool=repPool(),dd=d=>Math.hypot(d[1]-REP_DEP[1],d[2]-REP_DEP[2]),R=Math.max(3,(REP.rad||REP_R0)-.5);
 const C=pool.filter(d=>d.length>4&&dd(d)>.8&&dd(d)<R&&repLibre(d[1],d[2]));const mez=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
 const sel=[],ok=d=>sel.every(s_=>Math.hypot(s_[1]-d[1],s_[2]-d[2])>1.1)&&LUZ.arcos.every(a=>Math.hypot(a.x-d[1],a.y-d[2])>.7);
 for(const d of mez(C.filter(d=>LUZ_CALLES.test(d[0]))))if(sel.length<m.n&&ok(d)&&!sel.some(s_=>s_[0]===d[0]))sel.push(d);
 for(const d of mez(C.slice()))if(sel.length<m.n&&ok(d))sel.push(d);
 // orden: siempre al más cercano, empezando por donde estás
 const ord=[];let cx=P.x,cy=P.y;while(sel.length){let bi=0,bd=1e9;sel.forEach((d,i)=>{const e=Math.hypot(d[1]-cx,d[2]-cy);if(e<bd){bd=e;bi=i}});const d=sel.splice(bi,1)[0];ord.push(d);cx=d[1];cy=d[2]}
 LUZ.ruta=ord.map(luzArco);LUZ.i=0;LUZ.on=true;LUZ.pts=0;lucesSiguiente()}
function lucesSiguiente(){const a=LUZ.ruta[LUZ.i];if(!a){lucesFin();return}campDestino([a.nom,a.x,a.y]);REP.marca.visible=false;repHud()}
function lucesEnciende(a){a.lit=true;a.t=0;const n=LUZ.ruta.length,i=LUZ.i+1,pts=60;REP.pts+=pts;LUZ.pts+=pts;
 try{sonCampana(1,.4);setTimeout(()=>bip(1320,.12,.08),120);setTimeout(()=>bip(1760,.16,.07),260)}catch(e){}padVibra(.2,.5,160);
 repPop('✨ '+i+'/'+n+' · +'+pts,'aviso');LUZ.i++;if(LUZ.i<n)setTimeout(()=>{if(REP.on&&!REP.fin&&LUZ.on)lucesSiguiente()},350);else setTimeout(lucesFin,600)}
function lucesFin(){if(!LUZ.on)return;LUZ.on=false;const bon=200+Math.max(0,Math.round(REP.t||0))*5;REP.pts+=bon;REP.ent++;REP.nEnt=(REP.nEnt||0)+1;
 try{sonJoJo();setTimeout(()=>sonPublico(1.2),500);confeti()}catch(e){}REP.shake=.4;aviso('✨ ¡Vigo ya brilla! +'+(LUZ.pts+bon)+' ⭐',2.4,'cuenta');
 const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;repVolver();
 const sig=m2.v==='heli'?' · ¡te espera el helicóptero!':m2.v==='moto'?' · ¡te espera la moto de agua!':'';setTimeout(()=>{if(REP.on&&!REP.fin)aviso((ab?'🔓 ¡Nueva zona desbloqueada! ':'↩️ ')+'Vuelve a Policarpo Sanz'+sig,2.2,'peq')},2600)}
function lucesTick(dt){if(!LUZ.arcos.length)return;LUZ.t+=dt;
 for(const a of LUZ.arcos){const B=a.B,bm=a.bm;let cambia=false;
  if(!a.lit){// el arco que toca parpadea un poco para que se vea desde lejos
   const act=LUZ.on&&LUZ.ruta[LUZ.i]===a;const v=act?(.25+.55*(Math.sin(LUZ.t*5)*.5+.5)):0;if(a.vAct!==v){a.vAct=v;for(let i=0;i<B.length;i++)bm.setColorAt(i,_lc.copy(LUZ_OFF).lerp(_lc.clone().setHex(0xffd27a),v*(i%2===0?1:.35)));a.est.material.color.copy(LUZ_OFF).lerp(new THREE.Color(0xffd27a),v);cambia=true}}
  else{a.t+=dt;const prog=a.t*2.2;   // se encienden del centro hacia los postes
   for(let i=0;i<B.length;i++){const on=prog>B[i][3]*1.6;const tw=on?(.82+.18*Math.sin(LUZ.t*3+i*1.7)):0;_lc.setHex(LUZ_ON[i%4]).multiplyScalar(on?tw*1.25:0);if(!on)_lc.copy(LUZ_OFF);bm.setColorAt(i,_lc)}
   a.est.material.color.setHex(0xfff0b0).multiplyScalar(prog>.3?1.3+.2*Math.sin(LUZ.t*4):.3);cambia=true}
  if(cambia)bm.instanceColor.needsUpdate=true}}
"""+s[j:]

# 2) inicio de misión: si toca encendido de luces
r("function repMisionNueva(ini){if(ini){REP.rad=REP_R0;repMuro()}",
  "function repMisionNueva(ini){if(ini){REP.rad=REP_R0;repMuro();LUZ.arcos=[];LUZ.ruta=[];LUZ.on=false}")
r(" REP.mis=m;if(m.rad>REP.rad)REP.rad=m.rad;if(MODO!=='coche'){campVeh('coche',REP_DEP[1],REP_DEP[2],0);aviso('🎅 ¡De vuelta a la carroza!',1.4,'peq')}",
  r""" if(m.luces){REP.mis=m;if(MODO!=='coche')campVeh('coche',REP_DEP[1],REP_DEP[2],0);REP.carga=0;repPila();lucesInicio(m);
  aviso('✨ Misión '+(k+1)+' · ¡Encendido de luces!',2,'cuenta');setTimeout(()=>{if(REP.on&&!REP.fin)mostrar('Pasa por debajo de los arcos apagados: ¡enciende la Navidad en '+LUZ.ruta.length+' calles!')},2200);return}
 REP.mis=m;if(m.rad>REP.rad)REP.rad=m.rad;if(MODO!=='coche'){campVeh('coche',REP_DEP[1],REP_DEP[2],0);aviso('🎅 ¡De vuelta a la carroza!',1.4,'peq')}""")
# 3) en marcha: animación y paso por debajo de cada arco
r("function repMision(dt){const m=REP.mis||{v:'coche'};if(REP.fin)return;",
  r"""function repMision(dt){const m=REP.mis||{v:'coche'};window.__TR=(window.__TR||0)+(dt||.016);lucesTick(dt||.016);if(REP.fin)return;
 if(m.luces&&REP.fase==='entregar'){if(LUZ.on){const a=LUZ.ruta[LUZ.i];if(a&&!a.lit&&Math.hypot(a.x-P.x,a.y-P.y)<Math.max(.1,a.w+.02))lucesEnciende(a)}return}""")
r("campMision:k=>campMision(k)};","campMision:k=>campMision(k),nueva:i=>repMisionNueva(i),mision:()=>repMision(.016)};")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok luces')
