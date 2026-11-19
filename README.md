# GT Vigo

Juego 3D en el navegador (three.js) ambientado en Vigo y su ría: calles de OpenStreetMap, edificios del Catastro con sus plantas reales, tráfico, peatones, barcos, ferris, helicópteros y misiones.

## Juegos

| Archivo | Qué es |
|---|---|
| `index.html` | Mundo abierto: coche, moto de agua, lancha, helicóptero y a pie por todo Vigo. Empieza en la pantalla de inicio, donde eliges coche, moto o helicóptero |
| `gp.html` | Gran Premio: carreras por un circuito urbano |
| `indexm.html` | Mundo abierto para móvil (versión LITE, como `navm.html`; además, en la maqueta los árboles y farolas de cada zona se dibujan juntos, se cargan menos zonas a la vez y los botones van en una fila. En un móvil `index.html` salta sola aquí; con `?pc=1` se queda en la de gráficos completos) |
| `nav.html` | Reparto de Navidad (PC, gráficos completos; en el móvil salta solo a `navm.html`) |
| `navm.html` | Reparto de Navidad para móvil (versión LITE: sin sombras ni efectos, 30 fps, piezas quietas agrupadas en lotes y botones adaptados al móvil en vertical) |

Los `.json` y `.png` de la raíz son los datos que cargan los juegos: zonas del mapa (`*_glb_*.png`, `*_inst.json`, `*_partes.json`), calles, tráfico, circuitos, mobiliario, fachadas, etc. Tienen que estar en la misma carpeta que los `.html`.

## Jugar en local

Los juegos cargan los datos con `fetch`, así que no basta con abrir el `.html` con doble clic: hay que servir la carpeta.

```bash
python3 -m http.server 8000
# y abre http://localhost:8000/index.html
```

## Publicar con GitHub Pages

En el repositorio: **Settings → Pages → Source: Deploy from a branch → `main` / root**. El juego queda en `https://ccp85.github.io/gt-vigo/` (mundo abierto) y los demás en `.../gp.html`, `.../nav.html`, etc.

## Código fuente (`fuente/`)

Los `.html` se generan a partir de una base y una cadena de scripts de edición:

- `index_base.html`: base reconstruida con todas las ediciones antiguas ya aplicadas.
- `edit_*.py`: cada script añade o cambia una parte del juego (Samil y su segunda pasada con aparcamientos y jardines tras el paseo, Castrelos, Monte do Castro, entrada por la AP-9, Castelao y Coia, dársena del Náutico, calles de Príncipe, Porta do Sol, Colón y Policarpo Sanz con enlosado de granito, farolas, bancos, jardineras, terrazas y árboles, rampas de Gran Vía con pérgolas poligonales de colores y jardineras, puerto con pesqueros en el Berbés, remolcadores, mercantes atracados y fondeados, barcos navegando y campas de coches, astilleros de Teis y ermita de A Guía, coche de policía, lancha, misión de skate, etc.). Se aplican en el orden de la lista `NUEVAS` de `build.sh`. **No reutilizar el nombre de un script existente** al añadir uno nuevo.
- `edit_navmovil.py` con `navmovil_lotes.js`, `navmovil.css` y `navmovil_cabecera.html`: versión móvil. Añade la cabecera de móvil a todas las páginas (codificación y ancho de pantalla) y el menú de carroza a dos columnas con el móvil en horizontal; solo en `navm.html`, junta en lotes las piezas que no se mueven para dibujar muchas menos cosas por imagen (en el centro, de unas 1.100 a unas 350) y ajusta los botones en vertical. También trocea los suelos de cada zona para dibujar solo lo que se ve, simplifica las figuras repetidas miles de veces y baja la calidad sola si el móvil no llega a unas 22 imágenes por segundo. Con `?fps=1` muestra en pantalla imágenes por segundo, nivel de calidad, dibujos y triángulos. Con `navmovil_salto.html`, en un móvil `nav.html` y el botón «🎄 Navidad 2026» del juego completo llevan solos a `navm.html` (con `?pc=1` en la dirección se queda la versión de gráficos completos).
- `edit_inicio.py` con `inicio.html`, `inicio.css`, `inicio.js` e `inicio3d.js`: pantalla de inicio. «GT VIGO» con letras animadas y tres tarjetas grandes con el coche, la moto y el helicóptero en 3D (se eligen con un toque, deslizando, con ◀ ▶ o con el mando). El vehículo elegido es con el que arrancas en el mundo abierto, tanto con JUGAR como al tocar un sitio en «🗺️ Elegir lugar». El botón «🗺️ Mapa» del juego vuelve a este menú con el mapa abierto. Recuerda el último vehículo elegido. Los modelos del menú usan su propio dibujo, que solo funciona mientras se ve el menú.
- `edit_oficiales.py` con `oficiales.js` y `oficiales_juego.js`: vehículos oficiales. El Ría GT 300, la Castro 600 y el Cíes H-1 se dibujan una sola vez (`oficiales.js`) y salen igual en la pantalla de inicio y en el juego: conduces el Ría GT 300, la moto es la Castro 600 con el protagonista y casco a juego, y tu helicóptero y los aparcados son el Cíes H-1. Carrera y reparto siguen con sus coches. Va después de `edit_inicio.py` y antes de `edit_mundomovil.py`.
- `edit_nitido.py` con `nitido.js`: móvil sin pixelado (`navm.html` e `indexm.html`; va antes de `edit_skatetest.py`). Resolución: empieza en 1 como antes, sube hasta 1,5 si el móvil va sobrado y no baja de 0,75 (antes, 0,55). Sin antialias en el móvil (con él y más resolución algún móvil se quedaba en negro al cargar). Para compensar, las piezas de las zonas, sus extras y los lotes pasan a material mate (`MeshLambertMaterial`, mucho más barato por punto y casi igual en esta maqueta); no se tocan los que llevan su propio brillo (asfalto mojado, charcos), ni coches ni personajes. Las texturas de más de 1536 px se reducen. La calidad automática de `navmovil_lotes.js` ahora recorta distancia (niebla) en vez de resolución. Además, en el móvil: asfalto sin grano fino ni grietas (3 cálculos de ruido menos por punto), reflejo del cielo en los coches cada 60 s en vez de cada 4 s (evita un tirón periódico de GPU), detalles de fachada al conducir hasta 4 de distancia en vez de 6,.
- `edit_mundomovil.py` con `mundomovil.js`, `mundomovil.css` y `mundomovil_salto.html`: mundo abierto para móvil (`indexm.html`). Va al final de la cadena y solo toca `index.html`, todo con `window.LITE` (en el ordenador no cambia nada; `gp`, `nav` y `navm` quedan igual). En la vista de maqueta junta los árboles y farolas de cada zona en una pieza por tipo (en el centro con el puerto, de unas 2.000 a unas 780 piezas por imagen); carga zonas en un radio de 16 como mucho (antes 30), suelta antes las lejanas y no deja alejar tanto el zoom (memoria); los botones de la maqueta van en una fila que se desliza y se esconde el texto de presentación. La pantalla de inicio (que tiene su propio motor gráfico) va a resolución 1 en el móvil y se libera entera al entrar al juego.
- `edit_radionavidad.py`: el reparto de Navidad (`nav.html`, `navm.html`) arranca siempre en 🎄 Radio Navidad con los villancicos. Guarda la emisora y el encendido de la radio aparte del mundo abierto, así que dejar 🌴 Vigo Reggae o la radio apagada en GT Vigo ya no afecta a Navidad. Va al final de la cadena y toca las cinco páginas.
- `edit_aguareal.py`: agua realista en todo el mar (va al final de la cadena y toca las cinco páginas). Oleaje de 8 trenes de olas con la velocidad real de cada longitud de onda (mar de fondo entrando por la ría), rizos de viento con calmas que se desplazan, color según la profundidad (azul petróleo en la ría, turquesa en lo poco hondo, arena bajo el agua en las playas), reflejo del cielo de cada hora, destellos del sol, rompiente en la orilla y borreguillos mar adentro. Las olas demasiado pequeñas para verse se apagan solas (sin parpadeo en la maqueta). En el móvil (`LITE`), 5 trenes de olas y sin rizos finos.
- `edit_fondomar.py` + `fondomar.js`: fondo marino continuo en todo el mar, por cuadrados de 60 m que se cargan alrededor del nadador y se descargan al alejarse. La profundidad sale de la distancia a la costa (se calcula una vez para todo el mapa): baja rápido junto a la orilla y se estabiliza mar adentro en unos 45-50 m, con canales y bajos suaves. Cada cuadrado tiene siempre lo mismo (rocas, algas, bateas, pulpos...) porque depende de su posición. Hecho como la Ría de Vigo de verdad. Arena con ondulaciones y restos de conchas, fango en lo hondo, bolos de granito con coralina rosa y algas, laminarias, praderas de zostera, una batea con cuerdas de mejillón, vieiras, erizos, estrellas de mar y anémonas. Bancos de sardinas, sargos y maragotas. Pulpos junto a las rocas que mueven los brazos y se camuflan; si te acercas buceando, salen disparados con el manto por delante y sueltan tinta. Cáusticas del sol en el fondo, el color se va perdiendo con la distancia (el rojo primero), rayos de luz, la superficie vista desde abajo (ventana de Snell) y nieve marina. Niebla verde atlántica que se oscurece con la profundidad y de noche. En el móvil (`LITE`) lleva menos detalle.
- `edit_nadolibre.py`: nadar y bucear en cualquier punto del mar con el protagonista. A pie, al caminar hacia el agua (playa, muelle o paseo) te metes a nadar; Z / LB bucea y puedes recorrer todo el fondo sin subir (solo te limita el aire); el aire se gasta bajo el agua; nadando hacia la orilla, o con E cerca de ella, sales a tierra. Bajo el agua se esconde el mundo de superficie (también en la misión del regalo perdido) y las burbujas son redondas.
- `build.sh`: copia la base, aplica los scripts en orden y genera `index.html`, `indexm.html`, `gp.html`, `nav.html` y `navm.html` (el último script, `edit_skatetest.py`, produce las variantes; también crea un `navskate.html` de pruebas que no se incluye aquí).
- `syn.js`: comprobación rápida de sintaxis de los HTML generados.

Las rutas de `build.sh` son las de la máquina donde se desarrolló; para usarlo en otra hay que ajustarlas.

## Créditos y notas

- Mapa: © colaboradores de OpenStreetMap. Edificios: Dirección General del Catastro.
- Google Earth y fotos se usaron solo como referencia visual: todos los modelos (Samil, Castrelos, fortaleza del Castro, Porta do Sol, la cúpula del parque infantil de la Rúa Venezuela, etc.) son propios y genéricos.
- El coche patrulla y la lancha se basan en modelos low-poly aportados por el autor.
