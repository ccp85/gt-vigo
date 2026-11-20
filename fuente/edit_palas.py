# Palas en la playa (palas.js), en las cinco páginas (en carreras y Navidad no aparece).
#  - Con sol, yendo a pie por una playa aparece cerca una chica en bikini dando toques con su pala.
#  - Acércate: «🏓 Jugar a las palas con ella» (E / botón). La bola va y viene: muévete a los lados (◀ ▶) hasta el aro verde
#    y golpea (E / botón «Golpe») justo cuando llegue. Golpe perfecto = bola más rápida; cada toque acelera el peloteo.
#    Cuenta toques seguidos y guarda el récord. ▼ (o ▲ un rato) para dejarlo. Con lluvia o de noche se acaba.
#  Necesita edit_playasol.py (sitios de playa y PLY.f).
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'palas.js'),encoding='utf8').read().strip('\n')+'\n\n'
M='// enganche para grabar tráilers'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function palasTick(' in s:
        a=s.index('// ---- palas en la playa (edit_palas.py)');b=s.index(M)
        s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado palas',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r(M,JS+M)
    r("function accion(){if(!driving)return;","function accion(){if(!driving)return;if(PAL.on){palasGolpe();return}if(palasCerca()){palasEmpieza();return}")
    r("function hudAccion(dt){const txt=buscarObjetivo();","function hudAccion(dt){const pt=palasTxt(),txt=pt||buscarObjetivo();")
    r("b.textContent=MODO==='pie'?(objetivo?'Subir':'—'):'Bajar';if(MODO==='heli')b.classList.toggle('off',!objetivo);b.classList.toggle('off',!objetivo);",
      "b.textContent=PAL.on?'Golpe':pt?'Jugar':MODO==='pie'?(objetivo?'Subir':'—'):'Bajar';if(MODO==='heli')b.classList.toggle('off',!objetivo);b.classList.toggle('off',!objetivo&&!pt&&!PAL.on);")
    r("if(MODO==='pie'&&txt){a.textContent=","if(MODO==='pie'&&txt&&!PAL.on){a.textContent=")
    r("addEventListener('pointerdown',e=>{if(MODO==='pie'&&objetivo){e.preventDefault();accion()}});","addEventListener('pointerdown',e=>{if(MODO==='pie'&&(objetivo||palasCerca())){e.preventDefault();accion()}});")
    r("for(let i=0;i<ns;i++)updateCar(d0/ns);if(REP.on)repTick(d0)}","for(let i=0;i<ns;i++)updateCar(d0/ns);if(REP.on)repTick(d0)}try{palasTick(d0)}catch(e){console.error(e)}")
    r("try{playaSolTick(dt)}catch(e){}","try{playaSolTick(dt);if(!driving&&PAL.chica&&PAL.chica.visible)palasTick(0)}catch(e){}")
    open(f,'w',encoding='utf8').write(s);print('ok palas',f)
