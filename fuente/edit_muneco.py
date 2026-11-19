# Protagonista a pie pulido (muneco.js) y media vuelta al andar hacia atrás, en las cinco páginas.
#  - mkPersona nuevo: mismo estilo cartoon pero acabado (cabeza grande con ojos con brillo, cejas, sonrisa y mofletes,
#    flequillo y tupé, sudadera con capucha, bolsillo y cordones, vaqueros con dobladillo, zapatillas redondeadas).
#    Mantiene userData.piernas/brazos con dos hijos (los usan nadar, la moto de agua y el ferry) y añade rodillas,
#    codos, tronco y cabeza articulados (animPersona).
#  - a pie, ↓ ya no anda de espaldas: el muñeco se da la vuelta y camina hacia la cámara, que se queda detrás,
#    así se le ve de frente. Al soltar o pulsar ↑ vuelve a girarse.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'muneco.js'),encoding='utf8').read().strip('\n')+'\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function animPersona(' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    a=s.index('function mkPersona(){');b=s.index('function mkMoto(')
    s=s[:a]+JS+s[b:]
    # hacia atrás: misma velocidad que un paso tranquilo hacia delante (antes -.1 de espaldas)
    r("if(PIE){const tgt=keys.up?.24:keys.down?-.1:0;","if(PIE){const tgt=keys.up?.24:keys.down?-.17:0;")
    # media vuelta: el modelo mira hacia donde camina; P.a (y la cámara) no cambian
    r("veh.rotation.y=P.a;if(veh===car)",
      "veh.rotation.y=P.a;if(PIE){const atras=!keys.up&&(keys.down||P.v<-.03)?1:0;P.vuelta=(P.vuelta||0)+(atras-(P.vuelta||0))*Math.min(1,dt*9);veh.rotation.y=P.a+P.vuelta*Math.PI}else P.vuelta=0;if(veh===car)")
    r("sombraPie.visible=PIE;if(PIE){const amp=Math.min(1,Math.abs(P.v)*6);veh.position.y+=.0015+Math.abs(Math.sin(tnow*14))*.003*amp;const pl=veh.userData.piernas.children;pl[0].rotation.z=Math.sin(tnow*14)*.6*amp;pl[1].rotation.z=-Math.sin(tnow*14)*.6*amp;if(veh.userData.brazos){const ba=veh.userData.brazos.children;ba[0].rotation.z=-Math.sin(tnow*14)*.5*amp;ba[1].rotation.z=Math.sin(tnow*14)*.5*amp}",
      "sombraPie.visible=PIE;if(PIE){const amp=Math.min(1,Math.abs(P.v)*6);veh.position.y+=.0015+Math.abs(Math.sin(tnow*14))*.003*amp;animPersona(veh,tnow,amp);")
    open(f,'w',encoding='utf8').write(s);print('ok muneco',f)
