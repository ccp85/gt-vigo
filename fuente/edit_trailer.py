f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# para grabar el trailer: window.NOADAPT congela la calidad adaptativa (no baja resolución ni detalle)
r("if(window.LITE){if(ft>1/27)","if(window.NOADAPT){}else if(window.LITE){if(ft>1/27)")
r("function empezarEn(z,p){","window.__empezarEn=id=>empezarEn(ZMETA.zonas.find(q=>q.id===id));function empezarEn(z,p){")
open(f,'w').write(s)
print('ok trailer')
