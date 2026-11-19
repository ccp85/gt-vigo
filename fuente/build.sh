#!/bin/bash
# Base reconstruida = última compilación buena (incluye todas las ediciones hasta edit_lite.py).
# edit_auto.py original se perdió (se sobrescribió): NO volver a ejecutar la cadena antigua desde index_bak_leds.html.
# Las ediciones nuevas se añaden a la lista NUEVAS en orden.
NUEVAS="noaccion skate3 skcalle trailer samil casprobe castrelos castro policia lancha navmovil ap9 suelofix coia nautico teis nitido samil2 puerto rampas2 principe ap9norte skatetest ecuador inicio oficiales variantes mundomovil radionavidad aguareal fondomar nadolibre coche500 calles sonagua $*"
cd /home/claude/work/vigo/visor && cp /home/claude/work/carrera/nav/index_base.html index.html && for e in $NUEVAS; do python3 /home/claude/work/carrera/nav/edit_$e.py >/dev/null 2>/tmp/build_err.txt || { echo FAIL $e; tail -3 /tmp/build_err.txt; exit 1; }; done; node /tmp/claude-0/-home-claude/e864c9b5-a070-51cb-ae38-d51f10abb096/scratchpad/syn.js
