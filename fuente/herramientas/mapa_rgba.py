# Genera vigo_mapa.rgba.gz a partir de vigo_mapa.png: los mismos píxeles en crudo (RGBA, alfa 255), comprimidos con gzip.
# Los juegos lo cargan con DecompressionStream directamente en el array del mapa, sin decodificar la imagen ni pasarla
# por lienzos (al cargar se ahorran unos 240 MB de memoria, lo que tumbaba móviles de 3-4 GB). Si falta o no cuadra el
# tamaño, los juegos vuelven a vigo_mapa.png.
# ¡Volver a ejecutarlo cada vez que cambie vigo_mapa.png!   python3 fuente/herramientas/mapa_rgba.py [carpeta]
import sys,os,gzip
from PIL import Image
d=sys.argv[1] if len(sys.argv)>1 else '.'
for z in ['vigo']:
    png=os.path.join(d,z+'_mapa.png')
    im=Image.open(png)
    assert not ({'icc_profile','gamma','srgb','chromaticity'} & set(im.info)),'el PNG lleva perfil de color: el navegador cambiaría los valores'
    raw=im.convert('RGBA').tobytes()
    open(os.path.join(d,z+'_mapa.rgba.gz'),'wb').write(gzip.compress(raw,9,mtime=0))
    print('ok',z,im.size,len(raw))
