import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# El encendido de luces y la misión de sigilo solo se juegan una vez por partida.
r("esCasaK=k=>k===2||(k>12&&(k-13)%6===0)","esCasaK=k=>k===7")
r("esSkaK=k=>k===7||(k>14&&(k-15)%6===0)","esSkaK=k=>k===2||(k>14&&(k-15)%6===0)")
r("if(j===3)return{v:'coche',luces:true,n:Math.min(16,11+c),txt:'✨ Encendido de luces · '+(c+2)}","if(j===3)return{v:'coche',rad:Math.min(REP_RMAX,17+3*c),txt:'🗺️ Vigo · ruta larga'}")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok unavez')
