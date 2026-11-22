// ================= Misión del GPS: 🎄 Reparto de Navidad · navmision.js (lo mete edit_navmision.py) =================
// El minijuego de Navidad 2026 también se juega desde el mundo abierto: en el GPS, «🎯 Misiones» → «🎄 Reparto de Navidad».
// La línea azul lleva al centro de Vigo (donde arranca el reparto) y allí espera un regalo gigante con su aro dorado.
// Al llegar se abre la elección de personaje (Papá Noel, Melchor, Gaspar o Baltasar; carroza o helicóptero), sin «Modo»:
// desde el GPS siempre es reparto, nunca carrera. Al terminar («Menú» o Esc) o con «← Volver» no vas a la pantalla de
// inicio como desde el botón «🎄 Navidad 2026», sino que vuelves al mundo abierto, en tu coche, donde lo dejaste.
const NVMIS={ruta:false,fin:null,on:false,vuelta:null,mk:null};
const NVM_DEST=[90.78,18.04];   // donde arranca el reparto (empezarReparto)
MISIONES.push({id:'navidad',ico:'🎄',n:'Reparto de Navidad',d:'Minijuego Navidad 2026 · Papá Noel o los Reyes Magos',da:'Vas camino del centro · toca para cancelar',ir:()=>navmisIr(),on:()=>NVMIS.ruta,fin:()=>navmisCancelar()});
{const st=document.createElement('style');st.textContent=`body.navmis #selCar .opt.nveh:not(.nvr){display:none!important}
#gpsMenu button.mis[data-m=navidad]:not(.act){background:linear-gradient(135deg,#d8232d,#8e0f1a);color:#fff3d0;border-color:#ffd24a}
#gpsMenu button.mis[data-m=navidad]:not(.act) .tag{background:#ffd24a;color:#8e0f1a}`;document.head.appendChild(st)}
// ---- GPS: ir al centro
function navmisIr(){if(REP.on||RACE.on)return;
 if(driving&&Math.hypot(NVM_DEST[0]-P.x,NVM_DEST[1]-P.y)<1.2){navmisAbrir();return}
 if(typeof TAXI!=='undefined'&&TAXI.on)taxiFin('otro');
 if(typeof AE!=='undefined'&&AE.on)aeFin('abandono');
 if(!driving)setDrive(true,'coche');
 if(MODO!=='coche'&&MODO!=='pie'){const G=gpsGrafo(),i=G?gpsNodo(P.x,P.y):-1;if(i>=0){const A=G.ADJ[i];let a=P.a;if(A&&A.length){const j=A[0];a=Math.atan2(-(G.Y[j]-G.Y[i]),G.X[j]-G.X[i])}Object.assign(P,{x:G.X[i],y:G.Y[i],a,v:0});P.z=groundY(P.x,P.y)}
  cambiarModo('coche');camInit=false;mostrar('🚗 Te subes a un coche para ir al centro')}
 gpsIniciar(['🎄 Reparto de Navidad · centro de Vigo',NVM_DEST[0],NVM_DEST[1]]);
 if(GPS.on){NVMIS.ruta=true;NVMIS.fin=GPS.pts[GPS.pts.length-1].slice();setTimeout(()=>{if(NVMIS.ruta)mostrar('🎄 Sigue la línea azul hasta el centro de Vigo ('+fmtD(GPS.acc[GPS.acc.length-1])+'): allí empieza el reparto')},400)}}
function navmisCancelar(){if(NVMIS.ruta&&GPS.on&&GPS.dest&&/Navidad/.test(GPS.dest[0]))gpsParar();NVMIS.ruta=false;mostrar('🎄 Reparto de Navidad cancelado')}
// ---- llegar: elección de personaje (solo reparto)
function navmisAbrir(){if(REP.on||RACE.on||NVMIS.on)return;NVMIS.ruta=false;if(NVMIS.mk)NVMIS.mk.visible=false;if(GPS.on)gpsParar();P.v=0;
 NVMIS.vuelta={x:P.x,y:P.y,a:P.a};NVMIS.on=true;document.body.classList.add('navmis');RACE.sel.modo=0;
 try{gtvEv('mision/navidad','Misión · Reparto de Navidad')}catch(e){}
 if(driving)setDrive(false);
 document.getElementById('selz').hidden=true;document.getElementById('selzNavidad').onclick()}   // .onclick() y no .click(): en el móvil no salta a navm.html
// ---- volver al mundo abierto, en coche, donde lo dejaste
function navmisVolver(){if(!NVMIS.on)return;NVMIS.on=false;document.body.classList.remove('navmis');
 document.getElementById('selCar').hidden=true;document.getElementById('selz').hidden=true;try{cerrarPrevia()}catch(e){}
 const v=NVMIS.vuelta;NVMIS.vuelta=null;if(v){START=[v.x,v.y];START_A=v.a}
 if(!driving)setDrive(true,'coche');mostrar('🎄 ¡Bo Nadal! Sigues por Vigo · en el GPS tienes más misiones')}
{const _sr=salirReparto;salirReparto=function(menu=true){const vol=menu&&NVMIS.on;_sr(vol?false:menu);if(vol)navmisVolver()}}
{const _sc=salirCarrera;salirCarrera=function(menu=true){const vol=menu&&NVMIS.on;_sc(vol?false:menu);if(vol)navmisVolver()}}
document.querySelector('#selCar .volver').addEventListener('click',()=>{if(NVMIS.on&&!REP.on&&!RACE.on)setTimeout(navmisVolver,0)});
// ---- marcador: aro dorado y regalo gigante girando
function navmisMarca(){const g=new THREE.Group();
 const r=new THREE.Mesh(new THREE.RingGeometry(.075,.095,32),new THREE.MeshBasicMaterial({color:0xffd24a,transparent:true,opacity:.8,side:THREE.DoubleSide,depthWrite:false,fog:false}));r.rotation.x=-Math.PI/2;r.position.y=.006;g.add(r);g.userData.r=r;
 const c=new THREE.Mesh(new THREE.CylinderGeometry(.035,.035,.6,16,1,true),new THREE.MeshBasicMaterial({color:0xe0303a,transparent:true,opacity:.22,side:THREE.DoubleSide,depthWrite:false,fog:false}));c.position.y=.3;g.add(c);
 const b=new THREE.Group(),cin=new THREE.MeshStandardMaterial({color:0xffd24a,roughness:.35,metalness:.4});
 b.add(new THREE.Mesh(new THREE.BoxGeometry(.034,.03,.034),new THREE.MeshStandardMaterial({color:0xc4161f,roughness:.5})));
 b.add(new THREE.Mesh(new THREE.BoxGeometry(.036,.031,.007),cin));b.add(new THREE.Mesh(new THREE.BoxGeometry(.007,.031,.036),cin));
 for(const k of[0,1]){const l=new THREE.Mesh(new THREE.TorusGeometry(.007,.0024,6,14),cin);l.position.y=.019;l.rotation.y=k*Math.PI/2;b.add(l)}
 b.position.y=.12;g.add(b);g.userData.b=b;g.visible=false;scene.add(g);return g}
// ---- cada fotograma: marcador, llegada y ruta que ya no es la nuestra
function navmisTick(dt){if(!NVMIS.mk)NVMIS.mk=navmisMarca();const mk=NVMIS.mk,f=NVMIS.fin;
 if(NVMIS.ruta&&f&&!REP.on&&!RACE.on&&Math.hypot(f[0]-P.x,f[1]-P.y)<.32){navmisAbrir();return}   // antes de mirar el GPS: al llegar, el GPS se apaga solo
 if(NVMIS.ruta&&(!GPS.on||!GPS.dest||!/Navidad/.test(GPS.dest[0])))NVMIS.ruta=false;
 mk.visible=!!(NVMIS.ruta&&f&&!REP.on&&!RACE.on&&Math.hypot(f[0]-P.x,f[1]-P.y)<30);
 if(mk.visible){const now=performance.now()/1000;mk.position.set(f[0],groundY(f[0],f[1]),f[1]);mk.userData.b.position.y=.12+Math.sin(now*3)*.02;mk.userData.b.rotation.y=now*1.6;mk.userData.r.material.opacity=.55+.3*Math.sin(now*4)}
}
