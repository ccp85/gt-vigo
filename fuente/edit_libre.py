f='index.html';S=open(f).read()
i=S.index("function navMundo(");j=S.index("function repMarca(")
pre,seg,post=S[:i],S[i:j],S[j:]
def rs(a,b):
    global seg
    assert seg.count(a)==1,(seg.count(a),a[:80]); seg=seg.replace(a,b)
rs("recorre(['Rúa de Urzáiz','Rúa de Urzaiz','Avenida da Gran Vía','Rúa Colón','Rúa García Barbón','Rúa Rosalía de Castro','Vía Norte','Rúa de Lepanto','Rúa Areal','Avenida de Beiramar','Rúa Progreso','Rúa Velázquez Moreno','Rúa do Marqués de Valladares','Rúa Carral','Rúa Elduayen','Rúa Pizarro','Rúa Cánovas del Castillo','Avenida das Camelias','Rúa de Venezuela'],.16,",
  "recorre(['Rúa de Urzáiz','Rúa de Urzaiz','Avenida da Gran Vía','Rúa Colón'],.7,")
rs("N=Math.max(8,Math.round((wl+wr)/.016));","N=Math.max(6,Math.round((wl+wr)/.03));")
rs("recorre(['Rúa do Príncipe'],.05,(x,y,tx,ty,k)=>{const nx=-ty,ny=tx;let wl=.09,wr=.09;const z0=groundMap(x,y);\n  for(let q=0;q<=16;q++){const t=q/16,",
  "recorre(['Rúa do Príncipe'],.3,(x,y,tx,ty,k)=>{const nx=-ty,ny=tx;let wl=.09,wr=.09;const z0=groundMap(x,y);\n  for(let q=0;q<=10;q++){const t=q/10,")
rs("recorre(['Rúa Policarpo Sanz'],.1,","recorre(['Rúa Policarpo Sanz'],.4,")
rs("N=Math.round(per/.014);","N=Math.round(per/.03);")
rs("for(let k=0;k<3200;k++){const t=k/3200,","for(let k=0;k<700;k++){const t=k/700,")
rs("a=t*110+(k%3)*2.094;","a=t*60+(k%3)*2.094;")
rs("  for(let j=0;j<24;j++){const a=j/24*6.283;for(let k=0;k<26;k++){const t=k/26;luz(ax+Math.cos(a)*RB*(1-t)*1.01,z0+.018+t*H,ay+Math.sin(a)*RB*(1-t)*1.01,0x7fc4ff,-k*.45+j,6,.009)}}\n","")
rs("for(let k=0;k<420;k++){const u=(k+.5)/420,","for(let k=0;k<120;k++){const u=(k+.5)/120,")
rs("for(let k=0;k<180;k++){const a=k/180*6.283;","for(let k=0;k<90;k++){const a=k/90*6.283;")
rs("   for(let k=0;k<20;k++){const a=k/20*6.283;for(let j=1;j<12;j++){const r=RN*j/12;L2(Math.cos(a)*r,Math.sin(a)*r,[0x3fe07a,0xffd24a,0xffffff,0xff4fb0][k%4],-j*.7+k,.012)}}\n","")
rs("   for(let q=0;q<14;q++){const a=q/14*6.283;luz(x+Math.cos(a)*.055,z0+.004,y+Math.sin(a)*.055,q%2?0xffd98a:0xff5a4a,q,3,.009)}})}","   })}")
s=pre+seg+post
def r(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
r("// REPARTO DE NAVIDAD: mundo abierto decorado; reparte los regalos en los puntos que marca el mapa antes de que se acabe el tiempo",
  "// REPARTO DE NAVIDAD: mundo abierto decorado; reparto libre sin tiempo: cada entrega abre otra cercana por el centro")
r("const REP_TIEMPO=[240,180,135],REP_BONO=[20,15,10],REP_N=8;","""// zona de juego: el centro (Príncipe / Policarpo Sanz) pesa más; alrededor, hasta Vialia y el Areal
const REP_C1=[91,18.5,2.8],REP_C2=[95.5,19.3,7.6],REP_MIN=2.8,REP_MAX=7;
// candidatos: puntos de calzada a lo largo de las calles con nombre dentro de la zona (se generan una vez)
function repPool(){if(REP.pool)return REP.pool;const out=[],esCalzada=(x,y)=>{const t=cell(x,y).t;return t===2||t===4};if(CALLES)for(const[n,c,ls]of CALLES){if(c===4||/Autoestrada|Autovía|Autopista|Túnel|Enlace/i.test(n))continue;for(const l of ls){let acc=.2;for(let i=0;i+3<l.length;i+=2){const ax=l[i],ay=l[i+1],bx=l[i+2],by=l[i+3],L=Math.hypot(bx-ax,by-ay);if(L<1e-6)continue;
  while(acc<L){const x=ax+(bx-ax)*acc/L,y=ay+(by-ay)*acc/L;if(Math.hypot(x-REP_C2[0],y-REP_C2[1])<REP_C2[2]&&esCalzada(x,y))out.push([n,+x.toFixed(2),+y.toFixed(2)]);acc+=.35}acc-=L}}}
 for(const d of REP_PUNTOS)if(Math.hypot(d[1]-REP_C2[0],d[2]-REP_C2[1])<REP_C2[2])out.push(d);
 if(out.length>20)REP.pool=out;return out.length?out:REP_PUNTOS}
// siguiente entrega: a media distancia (entre 200 y 500 m en línea recta), sin repetir las últimas, con más peso en el centro
function repElegir(){const pool=repPool(),x=P.x,y=P.y,cerca=pool.filter(d=>{const e=Math.hypot(d[1]-x,d[2]-y);return e>REP_MIN&&e<REP_MAX&&!REP.ult.some(u=>Math.hypot(u[0]-d[1],u[1]-d[2])<.6)});
 const L=cerca.length?cerca:pool.filter(d=>Math.hypot(d[1]-x,d[2]-y)>REP_MIN);const cen=L.filter(d=>Math.hypot(d[1]-REP_C1[0],d[2]-REP_C1[1])<REP_C1[2]);
 const de=(cen.length&&Math.random()<.6)?cen:L;for(let t=0;t<8;t++){const d=de[Math.floor(Math.random()*de.length)];const pts=gpsCalcular(x,y,d[1],d[2]);if(!pts||pts.length<2)continue;let lr=0;for(let i=1;i<pts.length;i++)lr+=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);const e=pts[pts.length-1];
  if(lr<11&&Math.hypot(e[0]-d[1],e[1]-d[2])<.15)return d}return de[Math.floor(Math.random()*de.length)]}
// récords guardados en este dispositivo: nombre y número de regalos
const REP_KREC='gtvigo_reparto_records';function repRecords(){try{const a=JSON.parse(localStorage.getItem(REP_KREC)||'[]');return Array.isArray(a)?a:[]}catch(e){return[]}}
function repGuardar(nombre,n){const a=repRecords();a.push({n:nombre.slice(0,18),r:n,f:Date.now()});a.sort((p,q)=>q.r-p.r||p.f-q.f);const top=a.slice(0,10);try{localStorage.setItem(REP_KREC,JSON.stringify(top));localStorage.setItem('gtvigo_nombre',nombre)}catch(e){}return top}""")
r("function repHud(){const el=document.getElementById('nHud');if(!REP.on){el.hidden=true;return}el.hidden=false;const d=REP.lista[REP.k];\n el.innerHTML=`<div class=\"t ${REP.t<20?'poco':''}\">⏱ ${fmtS(REP.t)}</div><div class=\"r\">🎁 ${REP.ent}/${REP.lista.length}</div>`+(d?`<div class=\"d\">Entrega en <b>${d[0]}</b> · ${fmtD(Math.hypot(d[1]-P.x,d[2]-P.y))}</div>`:'')}",
  "function repHud(){const el=document.getElementById('nHud');if(!REP.on){el.hidden=true;return}el.hidden=false;const d=REP.dest;\n const rec=repRecords()[0];el.querySelector('.cnt').innerHTML=`<div class=\"t\">🎁 ${REP.ent}</div><div class=\"r\">${rec?'Récord '+rec.r:'regalos'}</div>`+(d?`<div class=\"d\">Entrega en <b>${d[0]}</b> · ${fmtD(Math.hypot(d[1]-P.x,d[2]-P.y))}</div>`:'')}")
r("function repSiguiente(){const d=REP.lista[REP.k];if(!d){repFin(true);return}\n","function repSiguiente(){const d=repElegir();REP.dest=d;REP.ult.push([d[1],d[2]]);if(REP.ult.length>5)REP.ult.shift();\n")
r(""" // ocho entregas al azar, ordenadas por cercanía
 const pool=REP_PUNTOS.slice().sort(()=>Math.random()-.5).slice(0,REP_N);const L=[];let cx=START[0],cy=START[1];
 while(pool.length){let bi=0,bd=1e9;pool.forEach((d,i)=>{const e=Math.hypot(d[1]-cx,d[2]-cy);if(e<bd&&e>.6){bd=e;bi=i}});const d=pool.splice(bi,1)[0];L.push(d);cx=d[1];cy=d[2]}
 REP.lista=L;REP.k=0;REP.ent=0;REP.t=REP_TIEMPO[sel.dif];REP.tot=0;REP.fin=false;REP.on=true;""",
 """ REP.dest=null;REP.ult=[];REP.ent=0;REP.fin=false;REP.guardado=false;REP.on=true;""")
r("function repEntrega(){const d=REP.lista[REP.k];REP.ent++;REP.k++;REP.t+=REP_BONO[RACE.sel.dif];\n sonCaja();setTimeout(sonMoneda,150);aviso('🎁 ¡Entregado! +'+REP_BONO[RACE.sel.dif]+' s',1.1,'peq');",
  "function repEntrega(){const d=REP.dest;REP.dest=null;REP.ent++;\n sonCaja();setTimeout(sonMoneda,150);const rec=repRecords()[0];aviso(rec&&REP.ent===rec.r+1?'🏆 ¡Nuevo récord! '+REP.ent:'🎁 ¡Entregado! · '+REP.ent,1.1,'peq');")
i=s.index("function repFin(ok){");j=s.index("function salirReparto(")
s=s[:i]+"""function repLista(top,marca){return top.length?'<ol>'+top.map((e,i)=>`<li class="${e===marca?'yo':''}"><span>${i+1}. ${e.n.replace(/[<>&"]/g,'')}</span><b>🎁 ${e.r}</b></li>`).join('')+'</ol>':'<p class="vacio">Aún no hay récords. ¡Sé el primero!</p>'}
function repFin(){if(REP.fin)return;REP.fin=true;gpsParar();REP.marca.visible=false;const el=document.getElementById('nFin');
 const top=repRecords(),entra=!REP.guardado&&REP.ent>0&&(top.length<10||REP.ent>top[top.length-1].r);
 el.querySelector('h3').textContent=REP.ent?'🎄 ¡Buen reparto!':'🎄 Reparto de Navidad';
 el.querySelector('p').innerHTML=REP.ent?`Has repartido <b>${REP.ent}</b> ${REP.ent===1?'regalo':'regalos'}.`+(top[0]&&REP.ent>top[0].r?' ¡Nuevo récord!':''):'Aún no has entregado ningún regalo.';
 const g=el.querySelector('.guarda');g.hidden=!entra;if(entra){let nm='';try{nm=localStorage.getItem('gtvigo_nombre')||''}catch(e){}g.querySelector('input').value=nm}
 el.querySelector('.pts').innerHTML='<h4>🏆 Récords</h4>'+repLista(top);el.hidden=false;if(entra&&(!top[0]||REP.ent>top[0].r))try{confeti()}catch(e){}}
function repGuardarClick(){const el=document.getElementById('nFin'),inp=el.querySelector('.guarda input');const nm=(inp.value||'').trim()||'Anónimo';if(REP.guardado||!REP.ent)return;REP.guardado=true;
 const top=repGuardar(nm,REP.ent);const yo=top.find(e=>e.n===nm.slice(0,18)&&e.r===REP.ent&&Date.now()-e.f<5000);el.querySelector('.guarda').hidden=true;el.querySelector('.pts').innerHTML='<h4>🏆 Récords</h4>'+repLista(top,yo);repHud()}
function repSeguir(){const el=document.getElementById('nFin');el.hidden=true;if(!REP.on)return;REP.fin=false;if(REP.guardado){REP.ent=0;REP.guardado=false}repSiguiente()}
"""+s[j:]
r(" if(REP.fin)return;REP.t-=dt;\n const d=REP.lista[REP.k];if(d&&Math.hypot(d[1]-P.x,d[2]-P.y)<.2)repEntrega();\n if(REP.t<=0){REP.t=0;repFin(false)}\n",
  " if(REP.fin)return;\n const d=REP.dest;if(d&&Math.hypot(d[1]-P.x,d[2]-P.y)<.2)repEntrega();\n")
r('<div id="nHud" hidden></div>','<div id="nHud" hidden><div class="cnt"></div><button class="fin">🏁 Terminar</button></div>')
r('<div id="nFin" hidden><div class="c"><h3></h3><p></p><div class="pts"></div><div class="acc"><button class="menu">Menú</button><button class="otra">↻ Otra vez</button></div></div></div>',
  '<div id="nFin" hidden><div class="c"><h3></h3><p></p><div class="guarda"><input maxlength="18" placeholder="Tu nombre" autocomplete="nickname"><button>💾 Guardar récord</button></div><div class="pts"></div><div class="acc"><button class="menu">Menú</button><button class="otra">↻ Empezar de cero</button><button class="seguir">🎁 Seguir</button></div></div></div>')
r("#nFin .acc{display:flex;gap:10px;justify-content:center}","""#nHud .cnt{display:flex;flex-wrap:wrap;gap:4px 12px;justify-content:center;align-items:center;flex:1}#nHud .r{font:600 13px var(--body);opacity:.85}#nHud .fin{pointer-events:auto;border:0;border-radius:999px;background:#c4161f;color:#fff;font:700 13px var(--body);padding:7px 12px;cursor:pointer}
#nFin .guarda{display:flex;gap:8px;margin:4px 0 10px}#nFin .guarda[hidden]{display:none}#nFin .guarda input{flex:1;min-width:0;border:1px solid var(--rule);border-radius:12px;padding:10px 12px;font:600 16px var(--body);background:var(--paper,#fff);color:var(--ink)}#nFin .guarda button{border:0;border-radius:12px;background:#1f8a3c;color:#fff;font:700 14px var(--body);padding:0 14px;cursor:pointer}
#nFin .pts{font:600 15px var(--body);color:var(--ink);margin:4px 0 14px;text-align:left}#nFin .pts h4{margin:0 0 6px;text-align:center;font:800 16px var(--body);color:#c4161f}#nFin ol{list-style:none;margin:0;padding:0;max-height:38vh;overflow:auto}#nFin li{display:flex;justify-content:space-between;padding:6px 10px;border-radius:10px}#nFin li:nth-child(odd){background:rgba(127,127,127,.1)}#nFin li.yo{background:#ffd24a;color:#2a1a00}#nFin .vacio{text-align:center;opacity:.7;margin:0}
#nFin .acc{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}#nFin .acc .seguir{background:#1f8a3c!important;color:#fff!important;border-color:#1f8a3c!important}""")
r("{const nf=document.getElementById('nFin');nf.querySelector('.otra').onclick=()=>{nf.hidden=true;salirReparto(false);empezarReparto()};nf.querySelector('.menu').onclick=()=>{nf.hidden=true;salirReparto(true)}}",
  "{const nf=document.getElementById('nFin');nf.querySelector('.otra').onclick=()=>{nf.hidden=true;salirReparto(false);empezarReparto()};nf.querySelector('.menu').onclick=()=>{nf.hidden=true;salirReparto(true)};nf.querySelector('.seguir').onclick=repSeguir;nf.querySelector('.guarda button').onclick=repGuardarClick;nf.querySelector('.guarda input').addEventListener('keydown',e=>{e.stopPropagation();if(e.key==='Enter')repGuardarClick()});document.querySelector('#nHud .fin').onclick=()=>{if(REP.on&&!REP.fin)repFin()}}")
r("addEventListener('keydown',e=>{if(REP.on&&e.code==='Escape')salirReparto(true)});","addEventListener('keydown',e=>{if(REP.on&&e.code==='Escape'){if(REP.fin)salirReparto(true);else repFin()}});")
r("document.getElementById('bCoche').onclick=()=>{if(REP.on){salirReparto(true);return}","document.getElementById('bCoche').onclick=()=>{if(REP.on){if(REP.ent>0&&!REP.fin)repFin();else salirReparto(true);return}")
r("el.querySelector('[data-t]').parentNode.style.display=el.querySelector('[data-h]').parentNode.style.display=el.querySelector('[data-v]').parentNode.style.display=RACE.nav?'none':'';",
  "el.querySelector('[data-t]').parentNode.style.display=el.querySelector('[data-h]').parentNode.style.display=el.querySelector('[data-v]').parentNode.style.display=el.querySelector('[data-d]').parentNode.style.display=RACE.nav?'none':'';")
r("'Reparte los regalos por el centro de Vigo antes de que se acabe el tiempo'","'Reparte todos los regalos que puedas por el centro de Vigo y bate el récord'")
a=" if(GPS.on&&GPS.pts){g.strokeStyle='#2f8cff';g.lineWidth=.06*14/miniZoom*1.6;g.lineJoin='round';g.beginPath();const P_=GPS.pts;for(let i=GPS.idx;i<P_.length;i+=2){if(i===GPS.idx)g.moveTo(P_[i][0],P_[i][1]);else g.lineTo(P_[i][0],P_[i][1])}g.lineTo(P_[P_.length-1][0],P_[P_.length-1][1]);g.stroke()}"
assert s.count(a)==1
s=s.replace(a," if(GPS.on&&GPS.pts){const P_=GPS.pts,ruta=()=>{g.beginPath();for(let i=GPS.idx;i<P_.length;i+=2){if(i===GPS.idx)g.moveTo(P_[i][0],P_[i][1]);else g.lineTo(P_[i][0],P_[i][1])}g.lineTo(P_[P_.length-1][0],P_[P_.length-1][1])};g.lineJoin=g.lineCap='round';\n  g.strokeStyle='#ffffff';g.lineWidth=W2*.06/k;ruta();g.stroke();g.strokeStyle='#1f7bff';g.lineWidth=W2*.04/k;ruta();g.stroke();\n  const e=P_[P_.length-1];g.fillStyle='#ffd24a';g.strokeStyle='#c4161f';g.lineWidth=W2*.015/k;g.beginPath();g.arc(e[0],e[1],W2*.04/k,0,7);g.fill();g.stroke()}")
a=" const na=P.a-Math.PI/2,r=W2/2-16;"
assert s.count(a)==1
s=s.replace(a," if(GPS.on&&GPS.pts){const e=GPS.pts[GPS.pts.length-1],dx=e[0]-P.x,dy=e[1]-P.y,ra=Math.atan2(dy,dx)+(P.a-Math.PI/2),dd=Math.hypot(dx,dy)*k;if(dd>W2/2-10){const rr=W2/2-12;g.save();g.translate(W2/2+Math.cos(ra)*rr,W2/2+Math.sin(ra)*rr);g.rotate(ra);g.fillStyle='#1f7bff';g.strokeStyle='#fff';g.lineWidth=2.5;g.beginPath();g.moveTo(10,0);g.lineTo(-7,-8);g.lineTo(-7,8);g.closePath();g.fill();g.stroke();g.restore()}}\n"+a)
open(f,'w').write(s)
import re
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok')
