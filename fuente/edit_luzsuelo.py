import sys,os
# ================= Luz en el suelo bajo las luces de Navidad (luzsuelo.js) =================
# Bajo cada arco de luces encendido, el asfalto y las aceras se tiñen de luz cálida (más fuerte bajo la guirnalda y
# junto a los postes); el arco que toca late suave para guiarte. Muñecos, regalo gigante y árbol de Porta do Sol llevan
# la suya (la del árbol, azulada). Solo de noche. Láminas aditivas que siguen el suelo: sin luces reales, valen para el móvil.
# Toca las cinco páginas; va al final de build.sh (después de edit_oclusion.py).
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'luzsuelo.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'function luzSueloTick(' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # cada arco nuevo lleva su mancha de luz en el suelo
    r("LUZ.arcos.push(a);return a}","LUZ.arcos.push(a);try{luzSuelo(a)}catch(e){console.error(e)}return a}")
    # muñecos, regalo y árbol: la suya al encenderse
    r("a.lit=true;a.t=0;","a.lit=true;a.t=0;if(a.tipo)try{luzSueloEsp(a)}catch(e){console.error(e)}")
    r("function lucesEspRestore(){","function lucesEspRestore(){try{luzSueloEspFin()}catch(e){}")
    # brillo en cada imagen (antes del corte de lucesTick cuando no hay arcos)
    r("function lucesTick(dt){","function lucesTick(dt){try{luzSueloTick(dt)}catch(e){if(!window.__lsuErr){window.__lsuErr=1;console.error(e)}}")
    i=s.index("function lucesTick(dt){")
    s=s[:i]+JS+'\n'+s[i:]
    open(f,'w',encoding='utf8').write(s);print('ok luzsuelo',f)
