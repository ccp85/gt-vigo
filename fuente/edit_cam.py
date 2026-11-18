import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
r("const dist=CD;hgt=PIE?.15+(.2-dist)*.4:(MOTO?.28:MOTOC?.25:.34)+((MOTOC?.36:.46)-dist)*.6;",
  "let dist=CD;hgt=PIE?.15+(.2-dist)*.4:(MOTO?.28:MOTOC?.25:.34)+((MOTOC?.36:.46)-dist)*.6;\n // reparto: cámara siempre detrás de la carroza y sobre la calzada (nunca dentro de un edificio); si la calle se acaba detrás, se acerca y sube\n if(REP.on&&REP.red&&MODO==='coche'){let dd=.36;for(let q=1;q<=14;q++){const s_=q/14*.36;if(!repLibre(P.x-dx*s_,P.y-dz*s_)){dd=Math.max(.1,s_-.04);break}}REP.cd=REP.cd??dd;REP.cd+=(dd-REP.cd)*Math.min(1,dt*(dd<REP.cd?16:2.5));dist=REP.cd;hgt=.26+(.36-dist)*1.1}")
r("if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*(camC?14:6)));","if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*(camC||(REP.on&&REP.red&&MODO==='coche')?14:6)));")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok cam')
