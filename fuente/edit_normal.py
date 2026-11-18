import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# carroza = coche normal (misma física que en el mundo abierto), solo con dirección algo más viva para girar bien en las calles
r("else if(REP.on&&REP.red&&MODO==='coche'){P.a+=steer*4.2*(REP.giro||1)*dt*Math.max(.45,Math.min(1,Math.abs(P.v)/.1))*(P.v<-.01?-1:1);if(steer&&P.v>.6)P.v-=(P.v-.6)*Math.min(1,dt*4)}",
  "else if(REP.on&&REP.red&&MODO==='coche'){P.a+=steer*3.1*(REP.giro>1?1.2:1)*dt*Math.max(.55,Math.min(1,Math.abs(P.v)/.12))*(1-.15*Math.min(1,Math.abs(P.v)))*(P.v<-.01?-1:1)}")
r("if(bl!==br)P.a+=(br>bl?1:-1)*(REP.on?(keys.left||keys.right?0:2.2):1.3)*dt*Math.min(1,P.v*2)}","if(bl!==br)P.a+=(br>bl?1:-1)*1.3*dt*Math.min(1,P.v*2)}")
r("if(vn<0&&REP.on&&MODO==='coche'){","if(vn<0&&false){")
r("*(REP.on&&REP.red?1.25:1)","")
r("*(REP.on&&REP.red?1.7:1)","")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok normal')
