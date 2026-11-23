# Playa da Calzoa / As Barcas (Coruxo), al final de Samil tras la desembocadura del Lagares (calzoa.js), en las cinco
# páginas; va al final de la cadena. Se monta cuando está cargada la zona de Samil: río con banco de arena, plaza con
# árboles, fuente, mesas y bancos, rampa de hormigón con barandilla, muros con grafitis, malecón hacia Canido con rocas,
# barcas varadas en la hierba, dunas con matorral y senda, y el conjunto de apartamentos escalonados con su piscina
# (sustituye a los edificios genéricos que había ahí). Ver calzoa.js.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'calzoa.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- playa da Calzoa / As Barcas (calzoa.js)'
FIN='// ---------- fin de calzoa.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado calzoa',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("samChk();","samChk();try{calChk()}catch(e){console.warn('calzoa',e)}")
    r("function subePaso(){",JS+"function subePaso(){")
    open(f,'w',encoding='utf8').write(s);print('ok calzoa',f)
