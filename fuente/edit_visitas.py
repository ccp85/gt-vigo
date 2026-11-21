import sys,os
# ================= Contador de visitas en la pantalla de inicio (visitas.js) =================
# Debajo de «GT VIGO»: «👀 1.234 visitas · 87 este mes», leído de GoatCounter (gtvigo.goatcounter.com/counter/TOTAL.json).
# Solo sale si en GoatCounter está activado «Allow adding visitor counts on your website».
# Toca las cinco páginas; va después de edit_analitica.py.
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'visitas.js'),encoding='utf8').read().strip('\n')
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'id="gtvVisitas"' in s:print('ya estaba',f);continue
    a='<script data-goatcounter="https://gtvigo.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n'
    assert s.count(a)==1,(f,'falta edit_analitica.py')
    s=s.replace(a,a+'<script id="gtvVisitas">\n'+JS+'\n</script>\n')
    open(f,'w',encoding='utf8').write(s);print('ok visitas',f)
