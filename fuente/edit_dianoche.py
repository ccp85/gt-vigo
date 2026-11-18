import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
i=s.index("function navMundo(");j=s.index("function repMarca(")
pre,seg,post=s[:i],s[i:j],s[j:]
def rs(a,b):
    global seg
    assert seg.count(a)==1,(seg.count(a),a[:80]); seg=seg.replace(a,b)
# noria y mercadillo en el aparcamiento exterior de la estación (entre García Barbón y Vialia, acceso por San Lourenzo)
rs("{const nx=109.2,ny=20.45,","{const nx=100.8,ny=18.95,")
rs("{const NX=109.2,NY=20.45,X0=107.3,X1=110.6,Y0=18.1,Y1=21.6,pu=[];","{const NX=100.8,NY=18.95,X0=98.8,X1=103,Y0=18.05,Y1=20,pu=[];")
s=pre+seg+post
# el día pasa a noche poco a poco (ciclo normal); de noche no se queda oscuro
r("function repLuz(){SKYU.uZen.value.setRGB(.16,.2,.48);SKYU.uHor.value.setRGB(.95,.6,.7);SKYU.uNight.value=.35;SKYU.uDusk.value=.8;FOG.color.setRGB(.52,.44,.66);NUBE_MAT.color.setRGB(.8,.7,.95);\n hemi.color.setRGB(.95,.92,1.1);hemi.groundColor.setRGB(.6,.5,.6);hemi.intensity=1.5;sun.color.setRGB(1,.85,.75);sun.intensity=.75;if(sun.castShadow)sun.castShadow=false;R.toneMappingExposure=1.3;UMO.uWet.value=0;TIEMPO.moj=0}",
  "function repLuz(){hemi.intensity=Math.max(hemi.intensity,1.05);R.toneMappingExposure=Math.max(R.toneMappingExposure,1.15);UMO.uWet.value=0;TIEMPO.moj=0}")
r("CIELO.h=20.8;repCircuito()","CIELO.h=17.6;repCircuito()")
r("CIELO.modo='auto';CIELO.h=20.8;","CIELO.modo='auto';CIELO.h=17.6;")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok dianoche')
