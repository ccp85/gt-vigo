#!/bin/bash
# Base reconstruida = última compilación buena (incluye todas las ediciones hasta edit_lite.py).
# edit_auto.py original se perdió (se sobrescribió): NO volver a ejecutar la cadena antigua desde index_bak_leds.html.
# Las ediciones nuevas se añaden a la lista NUEVAS en orden.
NUEVAS="noaccion skate3 skcalle trailer samil casprobe castrelos castro policia lancha navmovil ap9 suelofix coia nautico teis nitido samil2 puerto rampas2 principe tejadoscentro fachadascentro relieve ap9norte skatetest ecuador inicio oficiales variantes mundomovil radionavidad aguareal fondomar nadolibre coche500 calles sonagua muneco playasol delfines palas ojos trafico nieve radiosuno mezclanav solonavidad carrozas oclusion reflejos luzsuelo analitica visitas cesped cascadas radiomundo fondoheli adornosmundo asfalto ruedasfantasma taxi charcos luzentorno suavizado olas surf mandogps aguapro autoescuela basket navmision buceoflash orilla huellas calzoa fps30 peatones barreras bouzas menostrafico colegio $*"
cd /home/claude/work/vigo/visor && cp /home/claude/work/carrera/nav/index_base.html index.html && for e in $NUEVAS; do python3 /home/claude/work/carrera/nav/edit_$e.py >/dev/null 2>/tmp/build_err.txt || { echo FAIL $e; tail -3 /tmp/build_err.txt; exit 1; }; done; node /tmp/claude-0/-home-claude/e864c9b5-a070-51cb-ae38-d51f10abb096/scratchpad/syn.js
# después de la cadena: index.html de la cadena (WebGL) pasa a ser webgl.html, la versión clásica de reserva;
# gpu.html es la prueba con marcador y el nuevo index.html es el juego principal con WebGPU:
# cp index.html webgl.html
# python3 /home/claude/work/carrera/nav/edit_webgpu.py webgl.html gpu.html
# python3 /home/claude/work/carrera/nav/edit_webgpu.py webgl.html index.html --principal
# y encima, en las dos páginas con WebGPU: python3 /home/claude/work/carrera/nav/edit_cielofis.py index.html gpu.html
# y después: python3 /home/claude/work/carrera/nav/edit_bretema.py index.html gpu.html
# y después: python3 /home/claude/work/carrera/nav/edit_csm.py index.html gpu.html
# y después: python3 /home/claude/work/carrera/nav/edit_noche.py index.html gpu.html
# y al final de todo, en las siete páginas: python3 /home/claude/work/carrera/nav/edit_fpsmovil.py
# y después, en las cuatro páginas del mundo abierto (index, indexm, webgl y gpu): python3 /home/claude/work/carrera/nav/edit_tutorial.py
