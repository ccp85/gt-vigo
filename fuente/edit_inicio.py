# ================= PANTALLA DE INICIO v2 =================
# Sustituye la pantalla de inicio (#selz) por una nueva: «GT VIGO» con letras animadas y tres tarjetas grandes
# con el coche, la moto y el helicóptero en 3D. El vehículo elegido es con el que arrancas en el mundo abierto
# (al pulsar JUGAR o al tocar un sitio del mapa, que ahora se abre con «🗺️ Elegir lugar»).
# Mantiene los ids que usa el juego (selz, selzJugar, selzCarrera, selzNavidad, selzMap).
# Archivos: inicio.html (marcado), inicio.css, inicio.js (interfaz) e inicio3d.js (modelos 3D, renderer propio
# que solo dibuja mientras se ve el menú). En gp/nav/navm el menú sigue oculto (body.solo).
# Se aplica a los 4 juegos (index, gp, nav, navm). Va DESPUÉS de edit_ecuador.py en build.sh.
import os,re
D=os.path.dirname(os.path.abspath(__file__))
rd=lambda n:open(os.path.join(D,n),encoding='utf-8').read()
NUEVO=(rd('inicio.html').strip()+'\n<style id="inicioV2">\n'+rd('inicio.css')+'</style>\n<script>\n'+rd('inicio.js')+'</script>\n<script type="module">\n'+rd('inicio3d.js')+'</script>')
VIEJO_RE=re.compile(r'<div id="selz"><h2 class="gt">GT <span>VIGO</span></h2>.*?<button id="selzNavidad">[^<]*</button></div></div>',re.S)
PCT_A="bJ.textContent=p<100?'▶ Mundo abierto · '+p+'%':'▶ Mundo abierto'"
PCT_B="{const ip=document.getElementById('iPct');if(ip)ip.textContent=p<100?'Cargando Vigo · '+p+'%':''}"
for f in ['index.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'id="inicioV2"' in s:print('ya estaba',f);continue
    m=VIEJO_RE.findall(s);assert len(m)==1,(f,len(m))
    s=VIEJO_RE.sub(lambda _:NUEVO,s,count=1)
    assert s.count(PCT_A)==1,(f,'pct');s=s.replace(PCT_A,PCT_B)
    open(f,'w',encoding='utf-8').write(s)
print('ok inicio')
