# Menos coches por la carretera y sin acumulaciones (las cinco páginas y gpu.html; va al final de la cadena, después de edit_trafico).
#  - Menos coches: 48 en el ordenador (antes 84), 34 en tableta/móvil con gráficos completos (antes 56), 8/7 en LITE (antes 12/10).
#  - Las avenidas siguen teniendo más tráfico, pero se reparte algo más (peso principal 6 en vez de 9, secundaria 4,5 en vez de 6).
#  - Al colocar un coche se exige más hueco con los demás (1 en vez de 0,6) en todos los intentos; si no hay sitio, no se coloca.
#  - En los cruces eligen la salida con menos coches cerca (mira más lejos y lo penaliza más).
#  - Cada segundo se deshacen los grupos: si un coche tiene dos o más coches muy pegados y está fuera de la vista, se lleva a otra calle.
#  - Las colas: lejos (más de 1,4) se recoloca como antes a los 1,2 s; a media distancia, a los 5 s; junto al jugador espera en la cola
#    y ya no atraviesa al de delante a los 1,2 s (eso amontonaba coches unos encima de otros), solo si lleva 8 s atascado.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','gpu.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '// menos tráfico (edit_menostrafico)' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("const NT=matchMedia('(pointer:coarse)').matches?(window.LITE?10:56):(window.LITE?12:84);",
      "const NT=matchMedia('(pointer:coarse)').matches?(window.LITE?7:34):(window.LITE?8:48);")
    r("const WRUTA=r=>(r.c==='P'?9:r.c==='S'?6:",
      "const WRUTA=r=>(r.c==='P'?6:r.c==='S'?4.5:")
    # hueco mínimo al colocar, obligatorio para los coches
    r("function recolocar(o,lista,dmin,dmax){const grupo=o.g?TRAF:PEA,sep=o.g?.6:.18;",
      "function recolocar(o,lista,dmin,dmax){const grupo=o.g?TRAF:PEA,sep=o.g?1:.18;")
    r("if(k<13&&grupo.some(q=>q!==o&&Math.abs(q.x-x)<sep&&Math.abs(q.y-y)<sep))continue;",
      "if((o.g||k<13)&&grupo.some(q=>q!==o&&!q.inact&&Math.abs(q.x-x)<sep&&Math.abs(q.y-y)<sep))continue;")
    # en los cruces, evitar las salidas con coches
    r("for(const q of TRAF){if(q!==o&&Math.abs(q.x-ex[0])<.18&&Math.abs(q.y-ex[1])<.18)ocup++}}",
      "for(const q of TRAF){if(q!==o&&!q.inact&&Math.abs(q.x-ex[0])<.32&&Math.abs(q.y-ex[1])<.32)ocup++}}")
    r("-ocup*1.5+","-ocup*2.6+")
    # colas: recolocar antes al que lleva rato parado detrás de otro
    r("if(delante){c.td=(c.td||0)+dt;if(c.td>1.2){c.td=0;c.libre=1.5;if(Math.hypot(c.x-F.x,c.y-F.y)>1.4&&recolocar(c,CERCA,driving?3:0,F.R)){c.z=null;trafReset(c)}}}else c.td=0;",
      "if(delante){c.td=(c.td||0)+dt;const dj_=Math.hypot(c.x-F.x,c.y-F.y),lim_=dj_>1.4?1.2:dj_>.9?5:8;if(c.td>lim_){c.td=0;if(lim_<8&&recolocar(c,CERCA,driving?3:0,F.R)){c.z=null;trafReset(c)}else c.libre=1.5}}else c.td=0;   // cerca del jugador espera en la cola en vez de atravesar al de delante")
    # cada segundo, deshacer grupos de coches fuera de la vista
    r("if(cercaT<=0){cercaT=1;rutasCerca();densHora()}",
      "if(cercaT<=0){cercaT=1;rutasCerca();densHora();desagrupar()}")
    r("function updateTraffic(dt){",
      "// menos tráfico (edit_menostrafico): si un coche tiene dos o más pegados y no se ve, se va a otra calle\n"
      "function desagrupar(){if(!CERCA.length)return;const dv=driving?1.3:F.R*.85;\n"
      " for(const c of TRAF){if(c.inact||c.ko>0)continue;if(Math.hypot(c.x-F.x,c.y-F.y)<dv)continue;let n=0;\n"
      "  for(const o of TRAF){if(o===c||o.inact)continue;if(Math.abs(o.x-c.x)<.3&&Math.abs(o.y-c.y)<.3)n++}\n"
      "  if(n>=2&&recolocar(c,CERCA,driving?3:0,F.R)){c.z=null;c.vv=c.v;c.parT=0;c.td=0;trafReset(c)}}}\n"
      "function updateTraffic(dt){")
    open(f,'w',encoding='utf8').write(s);print('ok menostrafico',f)
