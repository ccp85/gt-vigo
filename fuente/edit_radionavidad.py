import sys,os
# ================= RADIO NAVIDAD: el reparto de Navidad arranca siempre con los villancicos =================
# Antes compartía con el mundo abierto la emisora y el encendido guardados (gtvigo_emisora / gtvigo_radio):
# si en GT Vigo dejabas puesta 🌴 Vigo Reggae o apagabas la radio, en Navidad salía reggae o nada.
# Ahora Navidad guarda lo suyo aparte y siempre empieza en 🎄 Radio Navidad.
# va al final de build.sh, cuando ya existen las cinco páginas
for f in (sys.argv[1:] or [x for x in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(x)]):
    s=open(f,encoding='utf-8').read()
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("localStorage.getItem('gtvigo_radio')","localStorage.getItem(window.SOLO_NAVIDAD?'gtvigo_nav_radio':'gtvigo_radio')")
    r("localStorage.setItem('gtvigo_radio',","localStorage.setItem(window.SOLO_NAVIDAD?'gtvigo_nav_radio':'gtvigo_radio',")
    r("e=+localStorage.getItem('gtvigo_emisora')||0","e=window.SOLO_NAVIDAD?0:(+localStorage.getItem('gtvigo_emisora')||0)")
    r("localStorage.setItem('gtvigo_emisora',","localStorage.setItem(window.SOLO_NAVIDAD?'gtvigo_nav_emisora':'gtvigo_emisora',")
    open(f,'w',encoding='utf-8').write(s)
