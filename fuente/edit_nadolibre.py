# Nadar y bucear en cualquier punto del mar (mundo abierto), con el protagonista.
#  - a pie, al caminar hacia el agua el personaje se mete en el mar y nada (también desde playas, muelles y paseos)
#  - Z / LB (o joystick derecho abajo) bucea: el fondo marino de fondomar.js es continuo en todo el mar (se va cargando
#    por cuadrados a tu alrededor) y más hondo cuanto más lejos de la costa
#  - aire limitado como en la misión de buceo; en la superficie lo recuperas
#  - nadando hacia tierra (o con E cerca de la orilla) sales del agua y sigues a pie
# Reutiliza el modo 'nado' y el mundo submarino de la misión del regalo perdido (BUC), que sigue funcionando igual.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
FUN=r'''
// ---------- nado libre: meterse al mar desde cualquier orilla, nadar y bucear (edit_nadolibre.py)
function nadoEntra(x,y){const B=BUC;Object.assign(B,{on:true,libre:true,fase:'libre',t:0,tiene:true,aire:1,W:null,D:[x,y],moto:null,reg:null,boya:null,WY:-.03});
 const nad=new THREE.Group(),piv=new THREE.Group(),f=mkPersona();f.scale.setScalar(.8);f.position.y=-.026;piv.add(f);piv.rotation.z=-1.2;nad.add(piv);
 piv.userData.br=f.userData.brazos?f.userData.brazos.children:[];piv.userData.pi=f.userData.piernas?f.userData.piernas.children:[];
 const lz=new THREE.PointLight(0xa8ecff,0,.9,1.5);lz.position.set(.05,.02,0);nad.add(lz);nad.userData.luz=lz;nad.userData.f=piv;nad.position.set(x,B.WY-.012,y);scene.add(nad);B.nad=nad;
 cambiarModo('nado');document.body.classList.add('heli');P.x=x;P.y=y;P.z=B.WY-.012;P.v=Math.min(Math.max(P.v,0),.12);P.vz=0;camInit=false;document.getElementById('aire').hidden=false;
 mostrar(document.body.classList.contains('pad')?'🏊 Nadando · joystick derecho ↓ bucea · ↑ sube · vuelve a la orilla para salir':'🏊 Nadando · Z bucea · Q sube · nada hasta la orilla para salir')}
function nadoFin(){const B=BUC;B.libre=false;buceoLimpia();const s_=document.querySelector('#vel small');if(s_)s_.textContent='km/h · flechas o WASD · E subir/bajar'}
function nadoSale(x,y){nadoFin();cambiarModo('pie');P.x=x;P.y=y;P.v=0;P.vz=0;camInit=false;mostrar('🚶 Fuera del agua')}
function nadoMundo(){const B=BUC;if(B.W){scene.remove(B.W);B.W.traverse(o=>{if(o.geometry)o.geometry.dispose()});B.W=null}B.D=[P.x,P.y];buceoMundo(B.D,B.WY)}
// orilla a la que salir: un punto de tierra transitable delante (o cerca) del nadador
function nadoOrilla(){let best=null,bd=1e9;for(let r=.03;r<=.14;r+=.015)for(let k=0;k<24;k++){const t=k/24*6.2832,x=P.x+Math.cos(t)*r,y=P.y+Math.sin(t)*r;if(!pieOK(cell(x,y).t))continue;
  let ok=true;for(let q=0;q<6;q++){const t2=q/6*6.2832;if(!pieOK(cell(x+Math.cos(t2)*.012,y+Math.sin(t2)*.012).t))ok=false}const s=r+Math.abs(Math.atan2(Math.sin(-Math.atan2(y-P.y,x-P.x)-P.a),Math.cos(-Math.atan2(y-P.y,x-P.x)-P.a)))*.03;if(ok&&s<bd){bd=s;best=[x,y]}}return best}
'''
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function nadoEntra(' in s:
        # páginas con la versión anterior (fondo que se regeneraba al alejarte): fondo continuo, sin límite al bucear
        M=[("""if(baja&&!bajo&&(!B.W||Math.hypot(P.x-B.D[0],P.y-B.D[1])>B.RZ*.45))nadoMundo()}""","""if(baja&&!bajo){if(!B.W)nadoMundo();else if(B.stream)B.stream(B,9)}}"""),
           ("""(B.W&&(!B.libre||bajo)&&Math.hypot(nx-B.D[0],ny-B.D[1])>B.RZ-.06)""","""(B.W&&!B.libre&&Math.hypot(nx-B.D[0],ny-B.D[1])>B.RZ-.06)"""),
           ("""mostrar(B.libre?(cell(nx,ny).t!==0?'Sube a la superficie para salir a la orilla':'Sube a la superficie para seguir explorando'):""","""mostrar(B.libre?'Sube a la superficie para salir a la orilla':""")]
        n=0
        for a,b in M:
            if a in s:s=s.replace(a,b);n+=1
        if n:open(f,'w',encoding='utf8').write(s);print('actualizado nadolibre',f,n)
        else:print('ya estaba',f)
        continue
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:100]); s=s.replace(a,b)
    # funciones nuevas, antes de updateNado
    r("function updateNado(dt){",FUN.strip('\n')+"\nfunction updateNado(dt){")
    # updateNado: el nado libre no depende de la misión de reparto
    r("function updateNado(dt){const B=BUC;if(!REP.on||!B.on){buceoLimpia();cambiarModo('coche');return}",
      "function updateNado(dt){const B=BUC;if(!B.on||(!B.libre&&!REP.on)){const lb=B.libre;if(lb)nadoFin();else buceoLimpia();cambiarModo(lb?'pie':'coche');return}")
    r(" const sup=B.WY-.012,bajo=P.z<sup-.015,tnow=performance.now()/1000;",
      " const sup=B.WY-.012,bajo=P.z<sup-.015,tnow=performance.now()/1000;\n"
      " if(B.libre){B.t+=dt;if(B.W)buceoMundoTick(dt);const baja=keys.alt_dn||(PAD.ry||0)>.3;if(baja&&!bajo){if(!B.W)nadoMundo();else if(B.stream)B.stream(B,9)}}")
    # movimiento: en libre, en la superficie se sale a tierra; bajo el agua no te alejas del fondo generado
    r("let nx=P.x+Math.cos(P.a)*P.v*dt,ny=P.y-Math.sin(P.a)*P.v*dt;if(cell(nx,ny).t!==0||Math.hypot(nx-B.D[0],ny-B.D[1])>B.RZ-.06){",
      "let nx=P.x+Math.cos(P.a)*P.v*dt,ny=P.y-Math.sin(P.a)*P.v*dt;"
      "if(B.libre&&!bajo&&cell(nx,ny).t!==0&&P.v>.03){const o=pieOK(cell(nx,ny).t)?[nx+Math.cos(P.a)*.015,ny-Math.sin(P.a)*.015]:nadoOrilla();if(o&&pieOK(cell(o[0],o[1]).t)){nadoSale(o[0],o[1]);return}}"
      "if(B.libre&&!B.W&&cell(nx,ny).t===0){}else if(cell(nx,ny).t!==0||(B.W&&!B.libre&&Math.hypot(nx-B.D[0],ny-B.D[1])>B.RZ-.06)){")
    r("mostrar('Hasta aquí: no te alejes de la zona de buceo')","mostrar(B.libre?'Sube a la superficie para salir a la orilla':'Hasta aquí: no te alejes de la zona de buceo')")
    r("const fz=B.hB(P.x,P.y)+.022;","const fz=B.W?B.hB(P.x,P.y)+.022:-9;")
    r("Math.max(P.z+hg,B.hB(P.x-dx*dist,P.y-dz*dist)+.04)","Math.max(P.z+hg,B.W?B.hB(P.x-dx*dist,P.y-dz*dist)+.04:-9)")
    r("const camBajo=pcam.position.y<B.WY-.003;window.__BAJO=camBajo;document.getElementById('bajoAgua').hidden=!camBajo;B.esf.visible=camBajo;for(const w of WATERS)w.visible=!camBajo;B.esf.position.copy(pcam.position);B.part.visible=camBajo;for(const m of B.rayos)m.visible=camBajo;B.sup.visible=camBajo;",
      "const camBajo=!!B.W&&pcam.position.y<B.WY-.003;window.__BAJO=camBajo;document.getElementById('bajoAgua').hidden=!camBajo;for(const w of WATERS)w.visible=!camBajo;"
      # bajo el agua solo se ve el fondo: se esconde el mundo de superficie (tierra, base azul de la maqueta, coches...) y se repone al sacar la cabeza
      "if(camBajo){B.oculta=B.oculta||[];for(const o of scene.children)if(o.visible&&!o.isLight&&!o.isCamera&&o!==B.W&&o!==B.nad&&!o.userData.submarino&&!(B.reg&&o===B.reg.g)){o.visible=false;if(!B.oculta.includes(o))B.oculta.push(o)}}else if(B.oculta){for(const o of B.oculta)o.visible=true;B.oculta=null}"
      "if(B.W){B.esf.visible=camBajo;B.esf.position.copy(pcam.position);B.part.visible=camBajo;for(const m of B.rayos)m.visible=camBajo;B.sup.visible=camBajo}")
    r("function buceoLimpia(sube){const B=BUC;","function buceoLimpia(sube){const B=BUC;if(B.oculta){for(const o of B.oculta)o.visible=true;B.oculta=null}")
    # acción (E): salir a la orilla
    r("function buceoObjetivo(){","function buceoObjetivo(){if(BUC.libre){if(MODO==='nado'&&P.z>BUC.WY-.05&&nadoOrilla()){objetivo={k:'buceo'};return '🚶 Salir del agua'}objetivo=null;return null}")
    r("function buceoAccion(){","function buceoAccion(){if(BUC.libre){if(MODO==='nado'){const o=P.z>BUC.WY-.05?nadoOrilla():null;if(o)nadoSale(o[0],o[1]);else mostrar(P.z>BUC.WY-.05?'Nada hasta la orilla para salir':'Sube a la superficie (Q) para salir del agua')}return true}")
    # cambiar de modo por menú, lugar o vehículo mientras nadas: se recoge todo
    r("function cambiarModo(m){","function cambiarModo(m){if(BUC.libre&&m!=='nado')nadoFin();")
    # a pie: caminar hacia el mar te mete en el agua
    r(" let dx_=Math.cos(P.a)*P.v*dt,dy_=-Math.sin(P.a)*P.v*dt;",
      " if(PIE&&P.v>.05&&!BUC.on&&!REP.on&&!P.tun&&!P.ferry){const ax=P.x+Math.cos(P.a)*.022,ay=P.y-Math.sin(P.a)*.022;if(cell(ax,ay).t===0&&cell(ax+Math.cos(P.a)*.04,ay-Math.sin(P.a)*.04).t===0){nadoEntra(ax,ay);return}}\n let dx_=Math.cos(P.a)*P.v*dt,dy_=-Math.sin(P.a)*P.v*dt;")
    open(f,'w',encoding='utf8').write(s);print('ok nadolibre',f)
