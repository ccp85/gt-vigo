// ===== Pantalla de inicio: tres modelos de cada vehículo =====
// ‹ › en la tarjeta elegida (o ▲ ▼ con el teclado) cambian de modelo. Se guarda en localStorage 'gtvigo_modelos'
// y avisa al dibujo 3D del menú (GTV_MODELO3D) y al juego (GTV_ponModelo). Datos de cada modelo: GTV_OF_INFO (oficiales.js)
(function(){
const SZ=document.getElementById('selz'),INFO=window.GTV_OF_INFO,INI=window.GTV_INICIO;
if(!SZ||!SZ.classList.contains('v2')||!INFO||!INI||window.SOLO_CARRERA)return;
const MS={coche:0,moto:0,heli:0};
try{const v=JSON.parse(localStorage.getItem('gtvigo_modelos')||'{}');for(const k in MS)if([0,1,2].includes(v[k]))MS[k]=v[k]}catch(e){}
const css=document.createElement('style');css.textContent=`
#selz.v2 .iCard .mdl{position:absolute;left:50%;bottom:37%;transform:translateX(-50%);display:none;align-items:center;gap:10px;z-index:3}
#selz.v2 .iCard.on .mdl{display:flex}
#selz.v2 .iCard .mdl i{font-style:normal;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:rgba(10,11,28,.6);border:1px solid rgba(var(--cr),.7);color:var(--c);font:700 20px/1 var(--body);cursor:pointer;transition:transform .15s,background .15s}
#selz.v2 .iCard .mdl i:hover{background:rgba(var(--cr),.25);transform:scale(1.08)}
#selz.v2 .iCard .mdl i:active{transform:scale(.92)}
#selz.v2 .iCard .mdl b{display:flex;gap:6px}
#selz.v2 .iCard .mdl b u{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.25);transition:.2s}
#selz.v2 .iCard .mdl b u.on{background:var(--c);box-shadow:0 0 8px rgba(var(--cr),.9);width:20px;border-radius:4px}
@media (orientation:portrait){#selz.v2 .iCard .mdl{bottom:39%}}`;
document.head.appendChild(css);
const cards=[...SZ.querySelectorAll('.iCard')],idx=c=>cards.indexOf(c);
const letras=(el,t)=>{el.innerHTML=[...t].map((c,i)=>`<span style="--i:${i}">${c===' '?'&nbsp;':c}</span>`).join('')};
function pinta(c){const k=c.dataset.v,i=MS[k],d=INFO[k][i];
 c.querySelector('.kind').textContent=d.k;const n=c.querySelector('.name');n.dataset.n=d.n;letras(n,d.n);
 c.querySelectorAll('.stats .b i').forEach((b,j)=>b.style.setProperty('--v',d.s[j]+'%'));
 c.querySelectorAll('.mdl b u').forEach((u,j)=>u.classList.toggle('on',j===i));
 c.setAttribute('aria-label',c.querySelector('.num b').textContent+': '+d.n+' (modelo '+(i+1)+' de 3)')}
function cambia(k,d){const c=cards.find(c=>c.dataset.v===k);if(!c)return;
 MS[k]=(MS[k]+d+3)%3;try{localStorage.setItem('gtvigo_modelos',JSON.stringify(MS))}catch(e){}
 pinta(c);
 if(c.classList.contains('on'))INI.sel(idx(c),true);
 window.GTV_MODELO3D&&window.GTV_MODELO3D(k,MS[k]);
 window.GTV_ponModelo&&window.GTV_ponModelo(k,MS[k])}
cards.forEach(c=>{const k=c.dataset.v,m=document.createElement('span');m.className='mdl';
 m.innerHTML='<i role="button" aria-label="Modelo anterior">‹</i><b><u></u><u></u><u></u></b><i role="button" aria-label="Modelo siguiente">›</i>';
 c.appendChild(m);
 m.addEventListener('click',e=>{e.stopPropagation();e.preventDefault();const t=e.target.closest('i');if(t)cambia(k,t===m.firstChild?-1:1)});
 pinta(c)});
INI.sel(cards.findIndex(c=>c.classList.contains('on')),true);
// el menú y el juego arrancan con lo guardado
for(const k in MS){window.GTV_MODELO3D&&window.GTV_MODELO3D(k,MS[k]);window.GTV_ponModelo&&window.GTV_ponModelo(k,MS[k])}
// teclado: ▲ ▼ cambian el modelo del vehículo elegido (◀ ▶ siguen cambiando de vehículo)
addEventListener('keydown',e=>{
 if(SZ.hidden||!SZ.getClientRects().length||!document.getElementById('iMapa').hidden)return;
 const sc=document.getElementById('selCar');if(sc&&!sc.hidden)return;
 if(e.key==='ArrowUp'||e.key==='ArrowDown'){cambia(INI.vehiculo,e.key==='ArrowDown'?1:-1);e.preventDefault();e.stopImmediatePropagation()}
},true);
const h=SZ.querySelector('.iHint');if(h)h.textContent='◀ ▶ vehículo · ▲ ▼ modelo · Enter jugar';
})();
