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
- `edit_*.py`: cada script añade o cambia una parte del juego (Samil, Castrelos, Monte do Castro, entrada por la AP-9, coche de policía, lancha, misión de skate, etc.). Se aplican en el orden de la lista `NUEVAS` de `build.sh`. **No reutilizar el nombre de un script existente** al añadir uno nuevo.
- `edit_navmovil.py` con `navmovil_lotes.js`, `navmovil.css` y `navmovil_cabecera.html`: versión móvil. Añade la cabecera de móvil a todas las páginas (codificación y ancho de pantalla) y el menú de carroza a dos columnas con el móvil en horizontal; solo en `navm.html`, junta en lotes las piezas que no se mueven para dibujar muchas menos cosas por imagen (en el centro, de unas 1.100 a unas 350) y ajusta los botones en vertical. También trocea los suelos de cada zona para dibujar solo lo que se ve, simplifica las figuras repetidas miles de veces y baja la calidad sola si el móvil no llega a unas 22 imágenes por segundo. Con `?fps=1` muestra en pantalla imágenes por segundo, nivel de calidad, dibujos y triángulos. Con `navmovil_salto.html`, en un móvil `nav.html` y el botón «🎄 Navidad 2026» del juego completo llevan solos a `navm.html` (con `?pc=1` en la dirección se queda la versión de gráficos completos).
- `edit_inicio.py` con `inicio.html`, `inicio.css`, `inicio.js` e `inicio3d.js`: pantalla de inicio. «GT VIGO» con letras animadas y tres tarjetas grandes con el coche, la moto y el helicóptero en 3D (se eligen con un toque, deslizando, con ◀ ▶ o con el mando). El vehículo elegido es con el que arrancas en el mundo abierto, tanto con JUGAR como al tocar un sitio en «🗺️ Elegir lugar». El botón «🗺️ Mapa» del juego vuelve a este menú con el mapa abierto. Recuerda el último vehículo elegido. Los modelos del menú usan su propio dibujo, que solo funciona mientras se ve el menú.
- `edit_mundomovil.py` con `mundomovil.js`, `mundomovil.css` y `mundomovil_salto.html`: mundo abierto para móvil (`indexm.html`). Va al final de la cadena y solo toca `index.html`, todo con `window.LITE` (en el ordenador no cambia nada; `gp`, `nav` y `navm` quedan igual). En la vista de maqueta junta los árboles y farolas de cada zona en una pieza por tipo (en el centro con el puerto, de unas 2.000 a unas 780 piezas por imagen); carga zonas en un radio de 16 como mucho (antes 30), suelta antes las lejanas y no deja alejar tanto el zoom (memoria); los botones de la maqueta van en una fila que se desliza y se esconde el texto de presentación.
- `build.sh`: copia la base, aplica los scripts en orden y genera `index.html`, `indexm.html`, `gp.html`, `nav.html` y `navm.html` (el último script, `edit_skatetest.py`, produce las variantes; también crea un `navskate.html` de pruebas que no se incluye aquí).
- `syn.js`: comprobación rápida de sintaxis de los HTML generados.

Las rutas de `build.sh` son las de la máquina donde se desarrolló; para usarlo en otra hay que ajustarlas.

## Créditos y notas

- Mapa: © colaboradores de OpenStreetMap. Edificios: Dirección General del Catastro.
- Google Earth y fotos se usaron solo como referencia visual: todos los modelos (Samil, Castrelos, fortaleza del Castro, Porta do Sol, la cúpula del parque infantil de la Rúa Venezuela, etc.) son propios y genéricos.
- El coche patrulla y la lancha se basan en modelos low-poly aportados por el autor.
- El protagonista (a pie y pilotando la moto de agua) es `protagonista.glb`, un modelo aportado por el autor. Se genera desde su `.obj` + textura con `fuente/herramientas/obj2glb.py` (lo gira, lo parte en cuerpo/piernas/brazos y comprime la textura); `fuente/edit_protagonista.py` lo carga solo en `index.html`.
