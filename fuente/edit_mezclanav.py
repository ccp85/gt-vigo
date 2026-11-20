# ================= MEZCLA DE NAVIDAD: efectos más bajos que la música =================
# En el reparto de Navidad (window.SOLO_NAVIDAD: nav.html y navm.html) los efectos (motor de la carroza, cascabeles, público,
# campanadas, mar…) se oían muy altos al lado de las canciones. Aquí todo lo que no es la radio baja a algo menos de la mitad
# (volumen general 0,8 → 0,36) y la radio lleva un refuerzo que lo compensa (×2,2), así que la música suena igual que antes.
# Fuera de Navidad no cambia nada. Va al final de build.sh (después de edit_radiosuno.py) y toca las cinco páginas.
import sys,os
for f in (sys.argv[1:] or [x for x in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(x)]):
    s=open(f,encoding='utf-8').read()
    if 'NAV_SFX' in s: print('ya estaba',f); continue
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("master.gain.setTargetAtTime(soundOn&&driving?.8:0,ct,.15);",
      "master.gain.setTargetAtTime(soundOn&&driving?.8*(window.SOLO_NAVIDAD?NAV_SFX:1):0,ct,.15);")
    r("Q.g=AC.createGain();Q.g.gain.value=0;Q.g.connect(master);",
      "Q.g=AC.createGain();Q.g.gain.value=0;{const bo=AC.createGain();bo.gain.value=window.SOLO_NAVIDAD?1/NAV_SFX:1;Q.g.connect(bo);bo.connect(master)}")
    r("const RADIO={","const NAV_SFX=.45;   // Navidad: volumen de los efectos (la radio se compensa)\nconst RADIO={")
    open(f,'w',encoding='utf-8').write(s); print('ok mezcla',f)
