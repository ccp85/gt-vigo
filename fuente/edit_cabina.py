# Vista interior del coche: 🎥 Cámara (o tecla C) pasa por persecución → pegada → interior. La vista interior pone la cámara
# en el asiento del conductor con salpicadero, capó del color del coche, volante que gira con la dirección, cuadro con
# velocímetro y cuentarrevoluciones, pantalla central con el minimapa, la calle, la hora y la emisora, pilares, techo,
# puertas y retrovisores (interior e izquierdo) que muestran la calle de atrás. En la carrera sale como «🪟 Interior».
# Solo con el coche (no moto, ni a pie, ni carroza de Navidad). Toca las siete páginas; va al final de todo (después de edit_fpsmovil.py).
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','webgl.html','gpu.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'cabina.js'),encoding='utf8').read()
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function cabCam(' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("let CAMC=0;try{CAMC=(+localStorage.getItem('gtvigo_cam')||0)===1?1:0}catch(e){}",
      "let CAMC=0;try{const v_=+localStorage.getItem('gtvigo_cam')||0;CAMC=v_===1||v_===3?v_:0}catch(e){}")
    r("function camCambia(){CAMC=CAMC?0:1;try{localStorage.setItem('gtvigo_cam',CAMC)}catch(e){}camInit=false;window.CD=undefined;const t_=CAMC?'🎥 Cámara pegada al coche':'🎥 Cámara de persecución';",
      JS+"\nfunction camCambia(){CAMC=CAMC===0?1:CAMC===1&&cabOK()?3:0;try{localStorage.setItem('gtvigo_cam',CAMC)}catch(e){}if(CAMC!==3)cabOff();camInit=false;window.CD=undefined;const t_=CAMC===3?'🎥 Vista interior':CAMC?'🎥 Cámara pegada al coche':'🎥 Cámara de persecución';")
    r("const camC=CAMC===1&&!PIE&&!MOTO;if(CAMC===2){",
      "if(CAMC===3&&cabOK()){cabCam(dt,gy);hudAccion(dt);document.getElementById('vel').firstChild.nodeValue=Math.round(Math.abs(P.v)*125);return}cabOff();const camC=CAMC===1&&!PIE&&!MOTO;if(CAMC===2){")
    r("if(CAMC===2){camCenital(dt,gy,vv,1,RACE.turboT>0?.15:0)}else{",
      "if(CAMC===3&&cabOK())cabCam(dt,gy);else{cabOff();if(CAMC===2){camCenital(dt,gy,vv,1,RACE.turboT>0?.15:0)}else{")
    r("pcam.fov=60+12*vv+(RACE.turboT>0?10:0);pcam.updateProjectionMatrix()}\n FOG.far=22",
      "pcam.fov=60+12*vv+(RACE.turboT>0?10:0);pcam.updateProjectionMatrix()}}\n FOG.far=22")
    r("if(driving){pcam.up.set(0,1,0);car.scale","if(!driving)cabOff();if(driving){pcam.up.set(0,1,0);car.scale")
    if f not in ('nav.html','navm.html'):
        r('<button data-k="1">🚗 Pegada</button></div>','<button data-k="1">🚗 Pegada</button><button data-k="3">🪟 Interior</button></div>')
    open(f,'w',encoding='utf8').write(s);print('ok cabina',f)
