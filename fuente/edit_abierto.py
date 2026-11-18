import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# mundo abierto: la red del centro solo sirve para la ruta y para colocar entregas; no hay vallas ni bloqueos
r("(RR&&!repLibre(x,y))","(RR&&REP.cerrado&&!repLibre(x,y))")
r("&&!(REP.on&&REP.red&&!repLibre(x,y))","&&!(REP.on&&REP.red&&REP.cerrado&&!repLibre(x,y))")
r("for(const o of[pan,pie,ban]){o.frustumCulled=false;scene.add(o);REP.objs.push(o)}","if(REP.cerrado)for(const o of[pan,pie,ban]){o.frustumCulled=false;scene.add(o);REP.objs.push(o)}")
# cámara: se acerca solo si detrás hay un edificio (no por salirse de la red)
r("if(!repLibre(P.x-dx*s_,P.y-dz*s_)){","{const t_=cell(P.x-dx*s_,P.y-dz*s_).t;if(t_!==3&&t_!==6&&t_!==-1)continue}{")
r("REP.red={x0,y0,res,w,h,m};GPSF=repLibre;","REP.red={x0,y0,res,w,h,m};GPSF=REP.cerrado?repLibre:null;")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok abierto')
