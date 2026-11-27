# Cielo físico y sol real sobre Vigo (gpu_cielofis.js), solo en las páginas con WebGPU (index.html y gpu.html); va al final
# de la cadena, después de edit_webgpu.py. Cielo con dispersión de Rayleigh y Mie (modelo de Preetham, el del SkyMesh de
# three.js) sobre el cielo de siempre (luna, estrellas y nubes, ahora teñidas por el sol); el sol sale y se pone por donde
# lo hace en Vigo (por defecto un día de mediados de agosto; ?dia=hoy usa la fecha de hoy); color del sol según el aire
# que atraviesa; colores del cenit y del horizonte (mar, fachadas, niebla, fondo) sacados del mismo cielo; y el mapa de
# entorno (PMREM) de los reflejos se dibuja con ese cielo. Con window.__CIELOFIS_OFF=true vuelve el cielo de antes.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','gpu.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'gpu_cielofis.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- cielo físico (gpu_cielofis.js)'
FIN='// ---------- fin de gpu_cielofis.js\n'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:
        a=s.index(INI);b=s.index(FIN)+len(FIN);s=s[:a]+JS+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado cielofis',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("function gpuAgua(glob,surfM){",JS+"function gpuAgua(glob,surfM){")
    r("try{sky.material=gpuCielo()}","try{sky.material=gpuCieloFis()}")
    # el sol, donde está de verdad sobre Vigo a esa hora
    r("const el=Math.sin(th);_sd.set(Math.cos(th),Math.max(el,-.6)*.85,.5*Math.max(Math.sin(th),.2)).normalize();",
      "let el;if(window.__CIELOFIS_OFF){el=Math.sin(th);_sd.set(Math.cos(th),Math.max(el,-.6)*.85,.5*Math.max(Math.sin(th),.2)).normalize()}else el=solVigo(h,_sd);")
    # colores del cielo y luz sacados de la atmósfera
    r("SKYU.uZen.value.copy(zen);SKYU.uHor.value.copy(hor);","try{cieloFis(_sd,el,zen,hor)}catch(e){if(!window.__cfE){window.__cfE=1;console.warn('cielo físico',e)}}SKYU.uZen.value.copy(zen);SKYU.uHor.value.copy(hor);")
    r(" UW.uN.value=nf;"," try{cieloFisLuz(el,day)}catch(e){}UW.uN.value=nf;")
    # la noche pasa más deprisa: ahora según la luz, no a horas fijas (el sol sale y se pone según el día del año)
    r("const noche=CIELO.h<7||CIELO.h>21.5;","const noche=CIELO.nf>.6;")
    # mapa de entorno de los reflejos (envCoches → PMREM): el mismo cielo
    r("let c=select(d.y.greaterThan(0),mix(uHor,uZen,pow(max(d.y,0),.6)),","let c=select(d.y.greaterThan(0),GT.cieloCol(d,mix(uHor,uZen,pow(max(d.y,0),.6))),")
    open(f,'w',encoding='utf8').write(s);print('ok cielofis',f)
