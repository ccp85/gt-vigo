# Adornos de Navidad también en el mundo abierto (index.html e indexm.html; va al final de la cadena, después de edit_mundomovil.py).
#  - Usa la misma decoración del reparto de Navidad (navMundo): guirnaldas y angelitos sobre las calles, túnel de luces de Príncipe,
#    túnel de Policarpo Sanz, árbol gigante y bosque de luz de Porta do Sol, regalo y bola gigantes de Urzaiz, noria y mercadillo
#    de Vialia, photocall del Areal, renos, muñecos de nieve, casetas y Papás Noel, globo, Estrella Polar de García Barbón,
#    mercado de la Alameda y el gentío de Príncipe y Vialia.
#  - Se monta al acercarte al centro, en cuanto están cargadas sus zonas, y se queda puesta. Al empezar una carrera o el reparto se quita (ellos ponen la suya)
#    y al volver al mundo abierto se pone otra vez.
#  - Los adornos del mundo abierto no cuentan como «modo Navidad»: no hace nevar (nieve.js) ni apaga el sol de las playas (playasol.js).
#  - Sin la nieve fija que cae alrededor de la cámara (las nevadas de verdad son las de nieve.js, de vez en cuando).
import os
FILES=[f for f in ['index.html','indexm.html'] if os.path.exists(f)]
JS=r"""
// ---------- adornos de Navidad en el mundo abierto (edit_adornosmundo.py)
const MNAV={objs:null,t:0};window.__MNAV=MNAV;
function mundoNavQuitar(){if(!MNAV.objs)return;for(const o of MNAV.objs)scene.remove(o);if(NAV.refl===MNAV.refl)navQuitar();MNAV.objs=null;MNAV.refl=null;MNAV.t=0}   // navQuitar solo si NAV aún es la nuestra
// zonas del mapa que tocan los adornos (Porta do Sol, Príncipe, Vialia, Gran Vía, Praza de España, Areal, Policarpo Sanz): todas cargadas
const MNAV_PTS=[[87.45,18],[90.6,19.5],[102,20.8],[96.3,25.2],[93.7,30.1],[95.5,14.5],[89.5,17.5],[93.1,18.4]];
function mundoNavListo(){if(!ZMETA)return false;for(const z of ZMETA.zonas)if(MNAV_PTS.some(p=>zonaDist(z,p[0],p[1])===0)&&(!ZEST[z.id]||typeof ZEST[z.id]!=='object'))return false;return true}
function mundoNavTick(dt){if(window.SOLO_NAVIDAD||window.SOLO_CARRERA)return;
 if(REP.on||RACE.on||(RACE.objs&&RACE.objs.length)){mundoNavQuitar();return}   // la carrera o el reparto ponen la suya
 if(!MNAV.objs){if(Math.hypot(P.x-95,P.y-22)>10||!mundoNavListo()){MNAV.t=0;return}MNAV.t+=dt;if(MNAV.t<1)return;   // espera a que carguen las zonas del centro
  navQuitar();MNAV.objs=[];navMundo(MNAV.objs);MNAV.refl=NAV.refl;if(NAV.nieve){scene.remove(NAV.nieve);NAV.nieve=null}if(NAV.tr){scene.remove(NAV.tr.pt);NAV.tr=null}return}
 if(NAV.on)navTick(dt)}
"""
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function mundoNavTick(' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    MN="(typeof NAV!=='undefined'&&NAV.on&&!(window.__MNAV&&__MNAV.objs))"
    r("function nieveActiva(){return (typeof REP!=='undefined'&&REP.on)||(typeof NAV!=='undefined'&&NAV.on)}","function nieveActiva(){return (typeof REP!=='undefined'&&REP.on)||"+MN+"}")
    r("noche=Math.max(CIELO.nf||0,(typeof NAV!=='undefined'&&NAV&&NAV.on)?1:0);","noche=Math.max(CIELO.nf||0,"+MN+"?1:0);")
    r("function repTick(dt){",JS.lstrip('\n')+"function repTick(dt){")
    r("try{palasTick(d0)}catch(e){console.error(e)}","try{palasTick(d0)}catch(e){console.error(e)}try{mundoNavTick(d0)}catch(e){console.error(e)}")
    open(f,'w',encoding='utf8').write(s);print('ok adornosmundo',f)
