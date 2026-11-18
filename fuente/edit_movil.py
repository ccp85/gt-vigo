import re
f='index.html';s=open(f).read()
# ---------------- móvil en vertical: el acelerador se salía de la pantalla y los botones de arriba tapaban el minimapa
css=r"""@media (max-width:440px){
 #pad{padding:0 10px}#pad .g{gap:6px}#pad button{width:56px;height:56px;font-size:19px}
 #pad .alt{flex-direction:column;align-items:center;justify-content:flex-end;gap:6px}
 #pad #bAcc{width:auto!important;min-width:56px;height:40px!important;border-radius:14px!important;padding:0 10px;font-size:14px!important}
 #pad #bPita{width:44px!important;height:44px!important;font-size:18px!important}
 body.drive .bar{left:132px!important;right:8px!important;justify-content:flex-end;gap:4px;max-width:none}
 body.drive .bar button{padding:6px 9px;font-size:12px}
 body:not(.drive) .bar{flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start;max-width:calc(100% - 16px);padding-bottom:4px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
 body:not(.drive) .bar button,body:not(.drive) .bar select{flex:0 0 auto}
}
"""
s=s.replace('</style>',css+'</style>',1)
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok movil')
