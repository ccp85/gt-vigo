import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= RUTAS DE REPARTO SENCILLAS Y POR GRANDES AVENIDAS =================
# · Los destinos de las entregas en coche están siempre en grandes avenidas.
# · Se elige la ruta con menos giros (al principio, como mucho 2; luego 3 y después 4).
# · Las avenidas se amplían según avanzas: centro → avenidas de alrededor → todas las avenidas de Vigo.
r("let pool=repPool();if(cen){const pc=pool.filter(d=>RUTA_CEN.test(d[0]));if(pc.length>4)pool=pc}",
  "let pool=repPool();{const pc=pool.filter(d=>repAvenidas().test(d[0]));if(pc.length>4)pool=pc}")
r("const W=repMuroR()-.15;let d=null;for(let q=0;q<12;q++){const c=repElegir(),pp=gpsCalcular(P.x,P.y,c[1],c[2]);d=c;if(pp&&pp.length>1&&pp.every(p=>Math.hypot(p[0]-REP_DEP[1],p[1]-REP_DEP[2])<W))break}",
  "const W=repMuroR()-.15,lim=repGirosMax();let d=null,bs=1e9;for(let q=0;q<16;q++){const c=repElegir(),pp=gpsCalcular(P.x,P.y,c[1],c[2]);if(!pp||pp.length<2){if(!d)d=c;continue}const dentro=pp.every(p=>Math.hypot(p[0]-REP_DEP[1],p[1]-REP_DEP[2])<W),g=rutaGiros(pp),sc=g+(dentro?0:20);if(sc<bs){bs=sc;d=c}if(dentro&&g<=lim)break}")
r("function repCocheCalle(){",r"""// avenidas por etapas: el centro, luego las avenidas de alrededor y al final todas las grandes vías de Vigo
const AV_CEN=/Príncipe|García Barbón|Policarpo Sanz|Urz[aá]iz|Estación de Vigo|Colón|Porta do Sol|Rosalía de Castro|Gran Vía|Lepanto|Vía Norte/i,
 AV_MED=/Príncipe|García Barbón|Policarpo Sanz|Urz[aá]iz|Estación de Vigo|Colón|Porta do Sol|Rosalía de Castro|Gran Vía|Lepanto|Vía Norte|Areal|Beiramar|Camelias|Venezuela|Pi i Margall|Gregorio Espino|Elduayen|Marqués de Valladares|Velázquez Moreno|Praza de Compostela|Praza de España|Praza de América|Avenida de Madrid|Pizarro/i,
 AV_TODO=/Avenida|Gran Vía|Urz[aá]iz|García Barbón|Colón|Policarpo Sanz|Príncipe|Porta do Sol|Rosalía de Castro|Areal|Lepanto|Vía Norte|Venezuela|Pi i Margall|Elduayen|Marqués de Valladares|Pizarro|Praza de/i;
function repEtapa(){const m=REP.mis||{},k=REP.nEnt||0;return m.centro||k<5?0:k<12?1:2}
function repAvenidas(){return[AV_CEN,AV_MED,AV_TODO][repEtapa()]}
function repGirosMax(){return[2,3,4][repEtapa()]}
function rutaGiros(pp){let n=0,prev=null,ax=pp[0][0],ay=pp[0][1];for(let i=1;i<pp.length;i++){const dx=pp[i][0]-ax,dy=pp[i][1]-ay;if(Math.hypot(dx,dy)<.14)continue;const h=Math.atan2(dy,dx);if(prev!==null){let d=Math.abs(h-prev);if(d>Math.PI)d=2*Math.PI-d;if(d>.8)n++}prev=h;ax=pp[i][0];ay=pp[i][1]}return n}
function repCocheCalle(){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok avenidas')
