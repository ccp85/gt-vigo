// ===== Pantalla de inicio v2 (interfaz). Los modelos 3D van en inicio3d.js =====
(function(){
const SZ=document.getElementById('selz');if(!SZ||!SZ.classList.contains('v2'))return;
const V={
 coche:{acc:'#ff5a36',acc2:'#ffb03a',rgb:'255,90,54',verbo:'Conducir el',go:'¡ARRANCA!',btn:'bCoche',txt:'coche'},
 moto:{acc:'#22d3ee',acc2:'#a5f3fc',rgb:'34,211,238',verbo:'Pilotar la',go:'¡A RODAR!',btn:'bMotoC',txt:'moto'},
 heli:{acc:'#c6f432',acc2:'#fff59d',rgb:'198,244,50',verbo:'Volar el',go:'¡DESPEGUE!',btn:'bHeli',txt:'helicóptero'}};
const cards=[...SZ.querySelectorAll('.iCard')],$=id=>document.getElementById(id),mapa=$('iMapa');
let cur=0,sndOn=false,ac=null;
const visible=()=>!SZ.hidden&&SZ.getClientRects().length>0;
const letras=(el,t)=>{el.innerHTML=[...t].map((c,i)=>`<span style="--i:${i}">${c===' '?'&nbsp;':c}</span>`).join('')};
cards.forEach(c=>{const n=c.querySelector('.name');letras(n,n.dataset.n)});
function sel(i,quiet){
 cur=(i+cards.length)%cards.length;
 cards.forEach((c,k)=>{const on=k===cur;c.classList.toggle('on',on);c.setAttribute('aria-checked',on)});
 const c=cards[cur],v=V[c.dataset.v],n=c.querySelector('.name');
 SZ.style.setProperty('--acc',v.acc);SZ.style.setProperty('--acc2',v.acc2);SZ.style.setProperty('--accRGB',v.rgb);SZ.style.setProperty('--gx',[22,50,78][cur]+'%');
 letras(n,n.dataset.n);$('iSub').textContent=v.verbo+' '+n.dataset.n;$('iMapaV').textContent=v.txt;
 try{localStorage.setItem('gtvigo_veh',c.dataset.v)}catch(e){}
 if(!quiet)vroom(c.dataset.v);
}
window.GTV_INICIO={get vehiculo(){return cards[cur].dataset.v},sel};
cards.forEach((c,i)=>{
 c.addEventListener('click',()=>{if(i===cur)$('selzJugar').click();else sel(i)});
 c.addEventListener('focus',()=>{if(i!==cur&&document.body.classList.contains('pad'))sel(i)});
});
// teclado: flechas para elegir, Enter para jugar (solo con el menú a la vista, sin el mapa ni la carrera encima)
document.addEventListener('keydown',e=>{
 if(!visible())return;
 if(!mapa.hidden){if(e.key==='Escape'){mapa.hidden=true;e.stopImmediatePropagation()}return}
 const sc=$('selCar');if(sc&&!sc.hidden)return;
 if(e.key==='ArrowRight'||e.key==='ArrowDown'){sel(cur+1);e.preventDefault();e.stopImmediatePropagation()}
 else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){sel(cur-1);e.preventDefault();e.stopImmediatePropagation()}
 else if(e.key==='Enter'){const a=document.activeElement;if(a&&a.tagName==='BUTTON'&&SZ.contains(a)&&!a.classList.contains('iCard'))return;$('selzJugar').click();e.preventDefault();e.stopImmediatePropagation()}
},true);
// deslizar en el móvil
{let x0=null,y0=null;const el=$('iSel');
 el.addEventListener('touchstart',e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
 el.addEventListener('touchend',e=>{if(x0==null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy))sel(cur+(dx<0?1:-1));x0=null},{passive:true})}

// sonido del menú (sintetizado): motor o rotor al elegir
function vroom(k){
 if(!sndOn)return;try{if(!ac)ac=new (window.AudioContext||window.webkitAudioContext)();if(ac.state==='suspended')ac.resume()}catch(e){return}
 const a=ac,t=a.currentTime,g=a.createGain(),f=a.createBiquadFilter();f.type='lowpass';f.frequency.value=k==='moto'?2200:1200;g.connect(a.destination);f.connect(g);
 if(k==='heli'){g.gain.value=.5;for(let i=0;i<7;i++){const o=a.createOscillator(),gg=a.createGain();o.type='triangle';o.frequency.value=70;o.connect(gg);gg.connect(f);
  gg.gain.setValueAtTime(0,t+i*.08);gg.gain.linearRampToValueAtTime(.5,t+i*.08+.01);gg.gain.exponentialRampToValueAtTime(.001,t+i*.08+.07);o.start(t+i*.08);o.stop(t+i*.08+.08)}return}
 const o=a.createOscillator(),o2=a.createOscillator(),b=k==='moto'?110:60;o.type='sawtooth';o2.type='square';
 o.frequency.setValueAtTime(b,t);o.frequency.exponentialRampToValueAtTime(b*3.2,t+.35);o.frequency.exponentialRampToValueAtTime(b*1.6,t+.7);
 o2.frequency.setValueAtTime(b/2,t);o2.frequency.exponentialRampToValueAtTime(b*1.6,t+.35);
 o.connect(f);o2.connect(f);g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.18,t+.05);g.gain.exponentialRampToValueAtTime(.001,t+.8);
 o.start(t);o2.start(t);o.stop(t+.8);o2.stop(t+.8)}
$('iSnd').onclick=()=>{sndOn=!sndOn;$('iSnd').textContent=sndOn?'🔊':'🔈';try{localStorage.setItem('gtvigo_menusnd',sndOn?'1':'0')}catch(e){}if(sndOn)vroom(cards[cur].dataset.v)};

// mapa para elegir dónde empezar (el juego dibuja en #selzMap y arranca con su clic)
const abrirMapa=()=>{mapa.hidden=false;$('iMapaX').focus({preventScroll:true})};
$('iMapaB').onclick=abrirMapa;$('iMapaX').onclick=()=>{mapa.hidden=true};
mapa.addEventListener('click',e=>{if(e.target===mapa)mapa.hidden=true});

// al jugar: animación y, en cuanto la ciudad está cargada, se monta en el vehículo elegido
let arm=0;
function cartel(k){const v=V[k],g=document.createElement('div');g.id='iGo';g.style.setProperty('--accRGB',v.rgb);
 g.innerHTML=`<div><b>${v.go}</b><small>${(v.verbo+' '+cards[cur].querySelector('.name').dataset.n).toUpperCase()}</small></div>`;
 document.querySelector('#iGo')?.remove();document.body.appendChild(g);setTimeout(()=>g.remove(),1600)}
function arrancar(){
 const k=cards[cur].dataset.v,id=++arm,t0=performance.now();cartel(k);vroom(k);
 const paso=()=>{if(id!==arm||visible())return;
  const listo=window.msgOff===true&&$('load').hidden;
  if(!listo){if(performance.now()-t0<180000)setTimeout(paso,250);return}
  setTimeout(()=>{if(id!==arm||visible())return;
   if(k==='coche'&&document.body.classList.contains('drive'))return;
   const b=$(V[k].btn);b&&b.click()},450)};
 setTimeout(paso,300);
}
$('selzJugar').addEventListener('click',()=>{if(!$('selzJugar').disabled)setTimeout(()=>{if(!visible())arrancar()},0)});
$('selzMap').addEventListener('click',()=>setTimeout(()=>{if(!visible()){mapa.hidden=true;arrancar()}},0));
['selzCarrera','selzNavidad'].forEach(id=>$(id).addEventListener('click',()=>{arm++;mapa.hidden=true}));
// el botón «🗺️ Mapa» del juego vuelve a este menú con el mapa abierto
document.addEventListener('DOMContentLoaded',()=>{const b=$('bZonas');b&&b.addEventListener('click',()=>{arm++;setTimeout(()=>{if(visible())abrirMapa()},0)})});

const L=['SAMIL','BOUZAS','MONTE DO CASTRO','GRAN VÍA','PRAZA DE AMÉRICA','PUENTE DE RANDE','CASCO VELLO','TORALLA','O AREAL','CASTRELOS','CÍES'];
const tk=L.map(l=>l+' <em>◆</em> ').join('');$('iTk').innerHTML=tk+tk;
let ini=0;try{ini=Math.max(0,['coche','moto','heli'].indexOf(localStorage.getItem('gtvigo_veh')));sndOn=localStorage.getItem('gtvigo_menusnd')==='1';$('iSnd').textContent=sndOn?'🔊':'🔈'}catch(e){}
sel(ini,true);
})();
