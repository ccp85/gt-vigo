import sys,os
# ================= Analíticas con GoatCounter (analitica.js) =================
# Cuenta visitas de cada página (mundo abierto, Gran Premio, Navidad, móvil y ordenador) y eventos propios:
#   zona/<id>          zona del mapa a la que llega el jugador (una vez por partida)
#   modo/<m>           coche, moto, helicóptero, a pie, lancha...
#   carrera/gp|navidad empezar una carrera
#   navidad/<pj>       personaje elegido en el reparto de Navidad
#   mision/<texto>     misión que empieza
# Sin cookies. Panel: https://gtvigo.goatcounter.com. Toca las cinco páginas; va al final de build.sh.
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'analitica.js'),encoding='utf8').read().strip('\n')
CAB=('<script id="gtvAnalitica">\n'+JS+'\n</script>\n'
     '<script data-goatcounter="https://gtvigo.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'id="gtvAnalitica"' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    i=s.index('</title>')+len('</title>\n')
    s=s[:i]+CAB+s[i:]
    r("function cargaZona(id,NP,k,N){","function cargaZona(id,NP,k,N){try{gtvEv('zona/'+id,'Zona '+id)}catch(e){}")
    r("function cambiarModo(m){","function cambiarModo(m){try{gtvEv('modo/'+m,'Modo '+m)}catch(e){}")
    r("function empezarCarrera_(){const sel=RACE.sel,spec=LISTA()[sel.c];",
      "function empezarCarrera_(){const sel=RACE.sel,spec=LISTA()[sel.c];try{gtvEv('carrera/'+(RACE.nav?'navidad':'gp'),RACE.nav?'Carrera Navidad':'Gran Premio')}catch(e){}")
    r("const sel=RACE.sel,spec=NAVC[sel.c];",
      "const sel=RACE.sel,spec=NAVC[sel.c];try{gtvEv('navidad/'+((spec&&spec.corto)||sel.c),'Navidad · '+((spec&&spec.corto)||sel.c))}catch(e){}")
    r("let m=campMision(k);","let m=campMision(k);try{gtvEv('mision/'+((m&&m.txt)||k),'Misión: '+((m&&m.txt)||k))}catch(e){}")
    open(f,'w',encoding='utf8').write(s);print('ok analitica',f)
