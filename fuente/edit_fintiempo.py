import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# El cronómetro ⚡ del reparto es solo un bonus por rapidez: nunca se «acaba el tiempo». Y Esc / Menú del mando
# piden confirmación antes de terminar la partida.
r("const acabado=C&&REP.t<=0;","const acabado=false;")
r("if(REP.on&&e.code==='Escape'){if(REP.fin)salirReparto(true);else repFin()}","if(REP.on&&e.code==='Escape'){if(REP.fin)salirReparto(true);else if(performance.now()-(REP.escT||0)<2500)repFin();else{REP.escT=performance.now();mostrar('Pulsa otra vez Esc (o Menú en el mando) para terminar la partida')}}")
r("if(REP.muro)REP.muro.visible=MODO==='coche';","if(REP.muro)REP.muro.visible=MODO==='coche'&&!CINE.on;")
# tráfico y gente paseando también en el Reparto de Navidad (sin choques, como en el mundo abierto)
r("if(!REP.on||REP.heli)updateTraffic(d0);else for(const c of TRAF)c.g.visible=false","updateTraffic(d0)")
# el almacén de regalos, en mitad de Policarpo Sanz (antes quedaba pegado a la Casa das Artes y la cámara se metía dentro)
r("REP_DEP=['Policarpo Sanz · almacén de regalos',90.6,17.86];","REP_DEP=['Policarpo Sanz · almacén de regalos',90.78,18.04];")
r("P.x=90.6;P.y=17.86;P.a=0;","P.x=90.78;P.y=18.04;P.a=Math.PI;")
r("if(salto)campVeh('coche',REP_DEP[1],REP_DEP[2],0);","if(salto)campVeh('coche',REP_DEP[1],REP_DEP[2],Math.PI);")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok fintiempo')
