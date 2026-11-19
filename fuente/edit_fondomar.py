# Fondo marino hiperrealista de la Ría de Vigo para la misión de buceo (las cinco páginas).
# Fondo continuo en todo el mar, por cuadrados de 60 m que se cargan alrededor del nadador; más hondo cuanto más lejos de la costa.
# Sustituye buceoMundo() y buceoMundoTick() por las de fondomar.js (mismos nombres y mismos datos que usa el resto del buceo:
# B.hB, B.RZ, B.peces, B.rayos, B.sup, B.part, B.burb, B.esf) y cambia el agua vista desde dentro: niebla verde atlántica
# que se oscurece con la profundidad y de noche, y el velo de pantalla con viñeta.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'fondomar.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function cuadro(' in s:print('ya estaba',f);continue
    if 'function fmMat(' in s:
        # actualiza un fondo anterior (versión de un solo círculo) al fondo continuo
        a=s.find('// ---------- el mundo bajo el agua');b=s.find('\nfunction buceoMundoTick(',a);c=s.find('\nfunction ',b+5)
        assert a>0 and b>a and c>b,(f,a,b,c)
        s=s[:a]+JS+s[c:];open(f,'w',encoding='utf8').write(s);print('actualizado fondomar',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    a=s.find('// ---------- el mundo bajo el agua');b=s.find('\nfunction buceoMundoTick(',a);c=s.find('\nfunction ',b+5)
    assert a>0 and b>a and c>b,(f,a,b,c)
    s=s[:a]+JS+s[c:]
    r("if(camBajo){const pr=Math.min(1,(B.WY-pcam.position.y)/.3);FOG.color.setRGB(.03+.03*(1-pr),.3-.12*pr,.43-.12*pr);B.esf.material.color.copy(FOG.color);FOG.near=.02;FOG.far=1.25-.35*pr}",
      "if(camBajo){const pr=Math.min(1,(B.WY-pcam.position.y)/.3),nk=1-.85*SKYU.uNight.value;FOG.color.setRGB((.028-.02*pr)*nk,(.2-.12*pr)*nk,(.21-.115*pr)*nk);B.esf.material.color.copy(FOG.color);FOG.near=.03;FOG.far=1.15-.4*pr}")
    r("background:radial-gradient(ellipse at 50% -10%,rgba(150,235,255,.22),rgba(0,60,90,.18) 45%,rgba(0,20,40,.55) 100%)",
      "background:radial-gradient(ellipse at 50% -15%,rgba(180,245,225,.14),rgba(0,45,50,.1) 45%,rgba(0,10,14,.62) 100%)")
    open(f,'w',encoding='utf8').write(s);print('ok fondomar',f)
