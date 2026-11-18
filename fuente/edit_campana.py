import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------------- campaña: centro ×4, alrededores ×2, helicóptero a una chimenea, moto de agua a Cangas… y así se va abriendo Vigo
i=s.index("function repMisionNueva(ini){");j=s.index("function repPila(){",i)
s=s[:i]+r"""const CAMP_MAR=['Cangas','Moaña','Cíes'];
function campMision(k){if(k<4)return{v:'coche',rad:6+.6*k,txt:'🎄 Centro · '+(k+1)+'/4'};if(k<6)return{v:'coche',rad:11+2*(k-4),txt:'🏘️ Alrededores · '+(k-3)+'/2'};
 if(k===6)return{v:'heli',txt:'🚁 Helicóptero · chimenea'};if(k===7)return{v:'moto',mar:'Cangas',txt:'🌊 Moto de agua · Cangas'};
 const c=Math.floor((k-8)/4),j=(k-8)%4;if(j<2)return{v:'coche',rad:Math.min(REP_RMAX,15+3*c+1.5*j),txt:'🗺️ Vigo · ruta larga'};if(j===2)return{v:'heli',txt:'🚁 Helicóptero · chimenea'};
 const n=CAMP_MAR[(c+1)%3];return{v:'moto',mar:n,txt:'🌊 Moto de agua · '+(n==='Cíes'?'Islas Cíes':n)}}
function aguaOK(x,y){if(cell(x,y).t!==0)return false;for(const[a,b]of[[.07,0],[-.07,0],[0,.07],[0,-.07],[.05,.05],[-.05,-.05],[.05,-.05],[-.05,.05]])if(cell(x+a,y+b).t!==0)return false;return true}
function aguaCerca(x,y,R=5){if(aguaOK(x,y))return[x,y];for(let r=.05;r<=R;r+=.05)for(let k=0,n=Math.max(8,Math.round(r*40));k<n;k++){const t=k/n*6.2832,X=x+Math.cos(t)*r,Y=y+Math.sin(t)*r;if(aguaOK(X,Y))return[X,Y]}return null}
function linea(Q){const o=[Q[0]];for(let i=1;i<Q.length;i++){const a=Q[i-1],b=Q[i],n=Math.max(1,Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/.1));for(let k=1;k<=n;k++)o.push([a[0]+(b[0]-a[0])*k/n,a[1]+(b[1]-a[1])*k/n])}return o}
// ruta por el agua (A* sobre una rejilla de 14 m que evita la costa)
function rutaAgua(x0,y0,x1,y1){const h=.2,M=6,mx=Math.min(x0,x1)-M,my=Math.min(y0,y1)-M,W=Math.ceil((Math.max(x0,x1)+M-mx)/h)+1,H=Math.ceil((Math.max(y0,y1)+M-my)/h)+1,N=W*H;
 const OK=new Int8Array(N).fill(-1),ok=i=>{if(OK[i]<0)OK[i]=aguaOK(mx+(i%W)*h,my+Math.floor(i/W)*h)?1:0;return OK[i]===1};
 const id=(x,y)=>Math.round((y-my)/h)*W+Math.round((x-mx)/h),s0=id(x0,y0),e=id(x1,y1),ex=e%W,ey=Math.floor(e/W);
 const g=new Float32Array(N).fill(1e9),from=new Int32Array(N).fill(-1),cl=new Uint8Array(N),hp=[],hf=[];
 const push=(i,v)=>{hp.push(i);hf.push(v);let c=hp.length-1;while(c>0){const p=(c-1)>>1;if(hf[p]<=hf[c])break;[hp[p],hp[c]]=[hp[c],hp[p]];[hf[p],hf[c]]=[hf[c],hf[p]];c=p}};
 const pop=()=>{const r_=hp[0],li=hp.pop(),lf=hf.pop();if(hp.length){hp[0]=li;hf[0]=lf;let c=0;for(;;){const l=2*c+1,rr=l+1;let m=c;if(l<hp.length&&hf[l]<hf[m])m=l;if(rr<hp.length&&hf[rr]<hf[m])m=rr;if(m===c)break;[hp[m],hp[c]]=[hp[c],hp[m]];[hf[m],hf[c]]=[hf[c],hf[m]];c=m}}return r_};
 const D=[[1,0,1],[-1,0,1],[0,1,1],[0,-1,1],[1,1,1.414],[1,-1,1.414],[-1,1,1.414],[-1,-1,1.414]];g[s0]=0;push(s0,0);let n=0,hay=false;
 while(hp.length&&n<700000){const i=pop();if(cl[i])continue;cl[i]=1;n++;if(i===e){hay=true;break}const ix=i%W,iy=Math.floor(i/W);
  for(const[dx,dy,c]of D){const jx=ix+dx,jy=iy+dy;if(jx<0||jy<0||jx>=W||jy>=H)continue;const j=jy*W+jx;if(cl[j]||!(j===e||ok(j)))continue;const ng=g[i]+c*h;if(ng<g[j]){g[j]=ng;from[j]=i;push(j,ng+Math.hypot(jx-ex,jy-ey)*h*1.05)}}}
 if(!hay)return null;const raw=[];for(let i=e;i>=0;i=from[i]){raw.push([mx+(i%W)*h,my+Math.floor(i/W)*h]);if(i===s0)break}raw.reverse();raw[0]=[x0,y0];raw[raw.length-1]=[x1,y1];
 const vis=(a,b)=>{const L=Math.hypot(b[0]-a[0],b[1]-a[1]),m=Math.ceil(L/.08);for(let k=1;k<m;k++){const t=k/m;if(!aguaOK(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t))return false}return true};
 const sp=[raw[0]];let a=0;while(a<raw.length-1){let j=a+1;while(j+1<raw.length&&j-a<70&&vis(raw[a],raw[j+1]))j++;sp.push(raw[j]);a=j}return linea(sp)}
function gpsSet(d,pts){GPS.on=true;GPS.libre=true;GPS.dest=d;GPS.pts=pts;GPS.acc=[0];for(let i=1;i<pts.length;i++)GPS.acc.push(GPS.acc[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));GPS.idx=0;GPS.fuera=0;GPS.t=0;gpsGiros();gpsMalla();GPS_DEST.visible=false}
window.__CAMP={rutaAgua:(...a)=>rutaAgua(...a),aguaCerca:(...a)=>aguaCerca(...a),campMision:k=>campMision(k)};
function campRuta(d){if(MODO==='coche'){gpsIniciar(d);return}if(MODO==='heli'){gpsSet(d,linea([[P.x,P.y],[d[1],d[2]]]));return}const rr=rutaAgua(P.x,P.y,d[1],d[2]);gpsSet(d,rr||linea([[P.x,P.y],[d[1],d[2]]]))}
function campVeh(v,x,y,a){P.v=0;P.turn=null;P.stuck=0;if(v==='heli'){Object.assign(P,{x,y,a,z:groundY(x,y)+.3,vz:0});HELI.posado=false;HELI.techoT=0;cambiarModo('heli');heliVestir(REP.spec,RACE.sel.col)}else{Object.assign(P,{x,y,a});cambiarModo(v)}camInit=false;window.CD=undefined}
function campDestino(d){REP.dest=d;REP.ult.push([d[1],d[2]]);if(REP.ult.length>5)REP.ult.shift();REP.marca.visible=true;repMarcaColor(0xffd24a);
 if(MODO==='heli'){repChimenea(d);repAire(d);REP.marca.position.set(d[1],d[3]+.09,d[2])}else REP.marca.position.set(d[1],groundY(d[1],d[2]),d[2]);
 campRuta(d);REP.t=repTiempo();repHud()}
function repMisionNueva(ini){if(ini){REP.rad=REP_R0;repMuro()}const k=REP.nEnt||0;let m=campMision(k);REP.fase='entregar';REP.carga=1;repPila();REP.dest=null;
 if(m.v==='moto'){const pu=aguaCerca(89.5,10.83),fd=FERRY_DEST[m.mar],tg=fd&&aguaCerca(fd[1][0],fd[1][1],8);if(!pu||!tg)m={v:'coche',rad:REP.rad,txt:'🗺️ Vigo · ruta larga'};else{
   REP.puerto=['Puerto de Vigo',pu[0],pu[1]];campVeh('moto',pu[0],pu[1],Math.atan2(-(tg[1]-pu[1]),tg[0]-pu[0]));REP.mis=m;campDestino([m.mar==='Cíes'?'Islas Cíes':'Puerto de '+m.mar,tg[0],tg[1]]);
   aviso('🌊 Misión '+(k+1)+' · ¡Moto de agua!',2,'cuenta');setTimeout(()=>{if(REP.on&&!REP.fin)mostrar('Navega hasta '+(m.mar==='Cíes'?'las Islas Cíes':m.mar)+' siguiendo la flecha')},2200);return}}
 if(m.v==='heli'){campVeh('heli',REP_DEP[1],REP_DEP[2],P.a);REP.mis=m;REP.buscar=0;const d=repTejado();if(d)campDestino(d);else repHud();
  aviso('🚁 Misión '+(k+1)+' · ¡Al helicóptero!',2,'cuenta');setTimeout(()=>{if(REP.on&&!REP.fin)mostrar('⤒ Q sube · ⤓ Z baja · aterriza en el tejado junto a la chimenea iluminada')},2200);return}
 REP.mis=m;if(m.rad>REP.rad)REP.rad=m.rad;if(MODO!=='coche'){campVeh('coche',REP_DEP[1],REP_DEP[2],0);aviso('🎅 ¡De vuelta a la carroza!',1.4,'peq')}
 const W=repMuroR()-.15;let d=null;for(let q=0;q<12;q++){const c=repElegir(),pp=gpsCalcular(P.x,P.y,c[1],c[2]);d=c;if(pp&&pp.length>1&&pp.every(p=>Math.hypot(p[0]-REP_DEP[1],p[1]-REP_DEP[2])<W))break}
 campDestino(d);if(!ini)repPop('🎁 Misión '+(k+1)+' · '+m.txt,'aviso')}
function repVolver(){REP.fase='recoger';const m=REP.mis||{v:'coche'},D=m.v==='moto'&&REP.puerto?REP.puerto:REP_DEP;REP.dest=D;REP.marca.position.set(D[1],groundY(D[1],D[2]),D[2]);REP.marca.visible=true;repMarcaColor(0x3fe07a);gpsParar();campRuta(D);REP.t=repTiempo();repHud()}
function repMision(dt){const m=REP.mis||{v:'coche'};if(REP.fin)return;
 if(!REP.dest){if(m.v==='heli'&&REP.fase==='entregar'){REP.buscar=(REP.buscar||0)-(dt||.016);if(REP.buscar<=0){REP.buscar=1;const d=repTejado();if(d)campDestino(d)}}return}
 const d=REP.dest,dd=Math.hypot(d[1]-P.x,d[2]-P.y),H=MODO==='heli',lleg=H?(HELI.posado&&dd<(REP.fase==='entregar'?.32:.5)):dd<(MODO==='moto'?.4:.28);if(!lleg)return;
 if(REP.fase==='entregar'){const bon=Math.max(0,Math.round(REP.t)),pts=100+(m.v==='heli'?150:m.v==='moto'?250:0)+bon*10;REP.pts+=pts;REP.ent++;REP.nEnt=(REP.nEnt||0)+1;REP.carga=0;repPila();try{sonCaja();setTimeout(sonJoJo,260);setTimeout(()=>sonPublico(1),700);confeti()}catch(e){}REP.shake=.5;repPop('+'+pts+' ⭐','gran');
  if(H&&REP.chim){REP.chim.userData.haz.visible=false;REP.chim.userData.humo=1.6}if(REP.aire){for(const o of REP.aire.objs)scene.remove(o);REP.aire=null}
  const m2=campMision(REP.nEnt),ab=m2.v==='coche'&&m2.rad>REP.rad;if(ab)REP.rad=m2.rad;repVolver();
  const sig=m2.v==='heli'?' · ¡te espera el helicóptero!':m2.v==='moto'?' · ¡te espera la moto de agua!':'';setTimeout(()=>aviso((ab?'🔓 ¡Nueva zona desbloqueada! ':'↩️ ')+'Vuelve a '+(m.v==='moto'?'Vigo':'Policarpo Sanz')+sig,2.2,'peq'),1300)}
 else{try{sonCaja()}catch(e){}repMisionNueva(false)}}
"""+s[j:]
r(" else if(REP.red)repMision();"," else if(REP.red)repMision(dt);")
# vehículos en la campaña (REP.heli queda para el modo helicóptero clásico)
r("if(REP.heli&&!REP.fin)repAireTick(dt);","if((REP.heli||MODO==='heli')&&!REP.fin)repAireTick(dt);")
r("if(!REP.heli&&!REP.fin)navSonidos(dt,repEnZona(P.x,P.y));else sonMotor(0,false);sonRotor(REP.heli&&!REP.fin,P.v);","if(MODO!=='heli'&&!REP.fin)navSonidos(dt,repEnZona(P.x,P.y));else sonMotor(0,false);sonRotor(MODO==='heli'&&!REP.fin,P.v);")
r("navEstela(P.x,P.y,REP.heli?P.z+.05:car.position.y,","navEstela(P.x,P.y,MODO==='heli'?P.z+.05:MODO==='moto'?moto.position.y:car.position.y,")
r("const dx=P.x-REP_DEP[1],dy=P.y-REP_DEP[2],d=Math.hypot(dx,dy);if(d>REP.radV){const k=(REP.radV-.02)/d;","const dx=P.x-REP_DEP[1],dy=P.y-REP_DEP[2],d=Math.hypot(dx,dy),RL=Math.max(REP.radV,W);if(d>RL){const k=(RL-.02)/d;")
r("function repLimite(dt){if(!REP.rad)return;","function repLimite(dt){if(!REP.rad)return;if(REP.muro)REP.muro.visible=MODO==='coche';if(MODO!=='coche')return;")
r("if(!REP.heli&&REP.red){REP.stT=","if(!REP.heli&&REP.red&&MODO!=='heli'){REP.stT=")
r("if(!REP.heli&&REP.red&&d&&!GPS.on){REP.rgT=(REP.rgT||0)-dt;if(REP.rgT<=0){REP.rgT=1;gpsIniciar(d)}}","if(!REP.heli&&REP.red&&d&&!GPS.on){REP.rgT=(REP.rgT||0)-dt;if(REP.rgT<=0){REP.rgT=1;campRuta(d)}}")
r("GPS.on=true;GPS.dest=d;GPS.pts=pts;GPS.acc=[0];","GPS.on=true;GPS.libre=false;GPS.dest=d;GPS.pts=pts;GPS.acc=[0];")
r("if(bd>.3){GPS.fuera+=.25;if(GPS.fuera>1){const d=GPS.dest;if(!REP.on)mostrar('Recalculando…');gpsIniciar(d);return}}","if(bd>(GPS.libre?.7:.3)){GPS.fuera+=.25;if(GPS.fuera>1){const d=GPS.dest;if(!REP.on)mostrar('Recalculando…');if(GPS.libre)campRuta(d);else gpsIniciar(d);return}}")
r("if(REP.on&&REP.heli&&REP.dest){","if(REP.on&&(REP.heli||MODO!=='coche')&&REP.dest){")
r("REP.nEnt=0;REP.fase='entregar';","REP.nEnt=0;REP.mis=null;REP.puerto=null;REP.fase='entregar';")
# marcador: tamaño de llegada por vehículo y HUD con la misión
r("""<span class="r ${REP.fase==='recoger'?'ok':''}">${REP.fase==='recoger'?'↩️ Policarpo Sanz':'📍'} ${d?fmtD(dd):'—'}</span>`;return}""",
  """<span class="r ${REP.fase==='recoger'?'ok':''}">${REP.fase==='recoger'?(REP.mis&&REP.mis.v==='moto'?'↩️ Puerto de Vigo':'↩️ Policarpo Sanz'):'📍'} ${d?fmtD(dd):(MODO==='heli'?'buscando tejado…':'—')}</span>`+(MODO==='heli'&&d&&dd<.8?'<span class="r ok">⤓ Aterriza</span>':'')+(REP.mis?`<span class="d">Misión ${(REP.nEnt||0)+(REP.fase==='recoger'?0:1)} · ${REP.fase==='recoger'?'vuelve a por otro regalo':REP.mis.txt}</span>`:'');return}""")
r("'Recoge el regalo en Policarpo Sanz, entrégalo y abre más ciudad. Sin límite de tiempo'","'Misiones por el centro, los alrededores, en helicóptero hasta una chimenea y en moto de agua hasta Cangas… y Vigo se va abriendo'")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok campana')
