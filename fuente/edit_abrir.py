import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# sin cascabeles
r("if(v>.12&&SFX.bT<=0){SFX.bT=.34;sonCascabel(.025+.03*Math.min(1,v))}","")
# puntos de entrega por toda la ciudad (los objetos arcade siguen en el centro)
r("if(repEnZona(x,y)&&(esCalzada(x,y)||n==='Rúa do Príncipe')&&repLibre(x,y)&&(!REP.red||[0,1,2,3,4,5,6,7].every(q=>repLibre(x+Math.cos(q*.785)*.07,y+Math.sin(q*.785)*.07))))out.push(",
  "if(Math.abs(x-95)<17&&Math.abs(y-19)<14&&(esCalzada(x,y)||n==='Rúa do Príncipe')&&(!repEnZona(x,y)||(repLibre(x,y)&&(!REP.red||[0,1,2,3,4,5,6,7].every(q=>repLibre(x+Math.cos(q*.785)*.07,y+Math.sin(q*.785)*.07))))))out.push(")
r("const pool=repPool().filter(d=>d.length>4)","const pool=repPool().filter(d=>d.length>4&&repEnZona(d[1],d[2])&&repLibre(d[1],d[2]))")
r("function repElegir(){","""// la ciudad se abre poco a poco: cada entrega amplía la zona de reparto desde el centro y alarga las rutas
const REP_C0=[91,18.2];const repRadio=()=>Math.min(16,2.4+.55*(REP.nEnt||0));
function repElegir(){if(REP.red&&!REP.heli){const pool=repPool(),k=REP.nEnt||0,Rz=repRadio(),mn=Math.min(5,1.1+.2*k),mx=Math.min(11,2.6+.45*k);const lejos=d=>Math.hypot(d[1]-REP_C0[0],d[2]-REP_C0[1]);
  let L=pool.filter(d=>{const e=Math.hypot(d[1]-P.x,d[2]-P.y);return lejos(d)<Rz&&e>mn&&e<mx&&!REP.ult.some(u=>Math.hypot(u[0]-d[1],u[1]-d[2])<.6)});
  if(!L.length)L=pool.filter(d=>lejos(d)<Rz&&Math.hypot(d[1]-P.x,d[2]-P.y)>mn*.5);if(!L.length)L=pool;return L[Math.floor(Math.random()*L.length)]}
 return repElegir0()}
function repElegir0(){""")
# más tiempo por cada regalo entregado; avisos de zona nueva
r("const n=REP.carga,x2=REP.t<=60?2:1,pts=n*100*REP.mul*x2;REP.pts+=pts;REP.ent+=n;REP.carga=0;repPila();REP.t+=REP_TBONO;",
  "const n=REP.carga,x2=REP.t<=60?2:1,pts=n*100*REP.mul*x2;REP.pts+=pts;REP.ent+=n;REP.carga=0;repPila();const tb=4+3*n;REP.t+=tb;REP.nEnt=(REP.nEnt||0)+1;\n if(REP.nEnt%3===0&&repRadio()<16)setTimeout(()=>aviso('🗺️ ¡La ciudad se abre! Rutas más largas',1.6,'peq'),1300);setTimeout(()=>repPop('⏱ +'+tb+' s','aviso'),1250);")
# empieza en el centro (Policarpo Sanz)
r("REP.on=true;REP.pool=null;REP.red=null;GPSF=null;if(!REP.heli){","REP.on=true;REP.pool=null;REP.red=null;GPSF=null;REP.nEnt=0;if(!REP.heli){P.x=90.6;P.y=17.86;P.a=0;P.v=0;")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok abrir')
