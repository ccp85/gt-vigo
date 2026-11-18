# GT Vigo

Juego 3D en el navegador (three.js) ambientado en Vigo y su ría: calles de OpenStreetMap, edificios del Catastro con sus plantas reales, tráfico, peatones, barcos, ferris, helicópteros y misiones.

## Juegos

| Archivo | Qué es |
|---|---|
| `index.html` | Mundo abierto: coche, moto de agua, lancha, helicóptero y a pie por todo Vigo |
| `gp.html` | Gran Premio: carreras por un circuito urbano |
| `nav.html` | Reparto de Navidad (PC, gráficos completos) |
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
- `edit_*.py`: cada script añade o cambia una parte del juego (Samil, Castrelos, Monte do Castro, coche de policía, lancha, misión de skate, etc.). Se aplican en el orden de la lista `NUEVAS` de `build.sh`. **No reutilizar el nombre de un script existente** al añadir uno nuevo.
- `edit_navmovil.py` con `navmovil_lotes.js`, `navmovil.css` y `navmovil_cabecera.html`: versión móvil. Añade la cabecera de móvil a todas las páginas (codificación y ancho de pantalla) y el menú de carroza a dos columnas con el móvil en horizontal; solo en `navm.html`, junta en lotes las piezas que no se mueven para dibujar muchas menos cosas por imagen (en el centro, de unas 1.100 a unas 350) y ajusta los botones en vertical.
- `build.sh`: copia la base, aplica los scripts en orden y genera `index.html`, `gp.html`, `nav.html` y `navm.html` (el último script, `edit_skatetest.py`, produce las variantes; también crea un `navskate.html` de pruebas que no se incluye aquí).
- `syn.js`: comprobación rápida de sintaxis de los HTML generados.

Las rutas de `build.sh` son las de la máquina donde se desarrolló; para usarlo en otra hay que ajustarlas.

## Créditos y notas

- Mapa: © colaboradores de OpenStreetMap. Edificios: Dirección General del Catastro.
- Google Earth y fotos se usaron solo como referencia visual: todos los modelos (Samil, Castrelos, fortaleza del Castro, Porta do Sol, la cúpula del parque infantil de la Rúa Venezuela, etc.) son propios y genéricos.
- El coche patrulla y la lancha se basan en modelos low-poly aportados por el autor.
- El protagonista (a pie y pilotando la moto de agua) es `protagonista.glb`, un modelo aportado por el autor. Se genera desde su `.obj` + textura con `fuente/herramientas/obj2glb.py` (lo gira, lo parte en cuerpo/piernas/brazos y comprime la textura); `fuente/edit_protagonista.py` lo carga solo en `index.html`.
