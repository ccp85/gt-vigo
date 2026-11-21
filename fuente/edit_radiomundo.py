import sys,os
# ================= RADIO DEL MUNDO ABIERTO: la de Navidad =================
# En el mundo abierto (y en las demás páginas) la radio ya no es 📻 Radio Vigo (canciones sintetizadas) ni 🌴 Vigo Reggae:
# ahora es la misma emisora que en el modo Navidad, 🎶 Vigo Nadal, con las canciones propias en mp3 de la carpeta musica/
# (edit_radiosuno.py). Es la única emisora, así que M / Ⓨ y el panel 📻 pasan de una canción a otra.
# Si tenías guardada otra emisora, se queda en esta (emisoraPon ya ajusta el número). Va después de edit_radiosuno.py.
A="const EMISORAS=window.SOLO_NAVIDAD?[{nom:'🎶 Vigo Nadal',c:SUNO}]:[{nom:'📻 Radio Vigo',c:VIGO3},{nom:'🌴 Vigo Reggae',c:REGGAE}];"
B="const EMISORAS=[{nom:'🎶 Vigo Nadal',c:SUNO}];   // edit_radiomundo.py: la radio de Navidad también en el mundo abierto"
for f in (sys.argv[1:] or [x for x in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(x)]):
    s=open(f,encoding='utf-8').read()
    if B in s: print('ya estaba',f); continue
    assert s.count(A)==1,f
    s=s.replace(A,B); open(f,'w',encoding='utf-8').write(s); print('ok radiomundo',f)
