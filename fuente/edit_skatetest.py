import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# Versión de prueba: window.MIS0 = número de misión con la que empieza el reparto (sin la llegada en trineo)
r("if((REP.red&&!REP.heli)){REP.rad=REP_R0;introInicio()}",
  "if((REP.red&&!REP.heli)){REP.rad=REP_R0;if(window.MIS0!=null){REP.nEnt=window.MIS0;REP.rad=Math.max(REP.rad,16);setTimeout(()=>{if(REP.on)repMisionNueva(false)},300)}else introInicio()}")
open(f,'w').write(s)
def var(tit,scr,out,ref=None):
    g=open(ref or out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
var('GT Vigo · Navidad Móvil','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;window.LITE=1;document.body.classList.add("solo","lite")</script>','navm.html','nav.html')
var('GT Vigo · Prueba Skate','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;window.LITE=1;window.MIS0=2;document.body.classList.add("solo","lite")</script>','navskate.html','nav.html')
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
print('ok skatetest')
