# Orillas de las playas sin cortes y arena realista (orilla.js), en las cinco páginas; va al final de la cadena.
# Las playas eran una lámina plana unos metros por encima del mar que caía en vertical al agua (labio, zócalo y muro
# de costa): parecían cortadas y biseladas, con un escalón. Al cargar cada zona, en una franja de unos 15 m junto al
# agua la arena baja poco a poco hasta meterse en el mar (malla fina propia que sigue unos metros bajo el agua) y lo
# viejo que asomaba en esa franja deja de dibujarse (máscara por zona). El suelo por el que se camina y la gente de la
# playa usan la arena nueva. La arena se pinta en el sombreado: manchas, grano, ondulaciones del viento, restos de la
# pleamar, arena mojada brillante, la resaca que sube y baja con su espuma y la playa oscura con lluvia.
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
JS=open(os.path.join(D,'orilla.js'),encoding='utf8').read().strip('\n')+'\n'
INI='// ---------- orillas de las playas y arena realista (orilla.js'
FIN='// ---------- fin de orilla.js\n'
ANCLA='// suelo mojado: cuando llueve'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if INI in s:   # ya aplicado: solo se actualiza el bloque
        a=s.index(INI);b=s.index(FIN)+len(FIN)
        s=s[:a]+JS+FIN+s[b:];open(f,'w',encoding='utf8').write(s);print('actualizado orilla',f);continue
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r(ANCLA,JS+FIN+ANCLA)
    r("vidaPlaya(root);","try{orillaZona(root)}catch(e){console.warn('orilla',e)}vidaPlaya(root);")
    r("if(h.length)return h[0].point.y}return groundMap(x,y)};","if(h.length)return oriSuelo(h[0],x,y)}{const v=ORI.Z.length?ORI.h(x,y):null;if(v!==null)return v}return groundMap(x,y)};")
    r(" return best}\nfunction subeMalla("," if(best==null&&ORI.Z.length){const v=ORI.h(x,z);if(v!==null)return v}return best}\nfunction subeMalla(")
    r("if(h.length===1)return h[0].point.y;\n for(const q of h){if(q.point.y<=prev+.09)return q.point.y}return h[h.length-1].point.y}",
      "if(h.length===1)return oriSuelo(h[0],x,y);\n for(const q of h){const yq=oriSuelo(q,x,y);if(yq<=prev+.09)return yq}return oriSuelo(h[h.length-1],x,y)}")
    r("if(h.length&&(best==null||h[0].point.y>best))best=h[0].point.y","if(h.length){const yq=oriSuelo(h[0],x,z);if(best==null||yq>best)best=yq}")
    r("const pick=()=>{const r=Math.random()*tot;","const pick=()=>oriPick(pick_());const pick_=()=>{const r=Math.random()*tot;")
    r("z:p.y,tx:-w[1]","z:oriZ(p.x+w[0]*(w[2]-.05),p.z+w[1]*(w[2]-.05),p.y),tx:-w[1]")
    open(f,'w',encoding='utf8').write(s);print('ok orilla',f)
