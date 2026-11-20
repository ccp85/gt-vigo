# Más tráfico en las avenidas y peatones solo por la acera (las cinco páginas; va al final de la cadena).
#  Coches:
#   - Hay más: 84 en el ordenador (antes 56), 56 en tableta/móvil con gráficos completos (antes 40), 12/10 en LITE (antes 8/7).
#   - Al colocarse alrededor del jugador eligen la calle según su importancia y su longitud (antes, una calle al azar,
#     y como hay muchísimos tramos cortos de calles pequeñas, las avenidas como Gran Vía se quedaban vacías).
#     Peso: principal 9, secundaria 6, autovía 3, terciaria 3, calle pequeña 0,5; los callejones sin salida, muy poco.
#  Peatones:
#   - No van por rotondas (ni por la isleta ni dando la vuelta a la calzada).
#   - Al esquivar un coche ya no saltan a la calzada.
#   - Si al ajustar la distancia al bordillo el paso suave los dejaba un momento sobre el asfalto, ahora se colocan directamente en la acera.
#   - Comprobación final: si alguien acaba en la calzada sin estar en un paso de cebra, se quita y sale otro en otra acera.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if '// tráfico por importancia (edit_trafico)' in s:print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    # --- más coches
    r("const NT=matchMedia('(pointer:coarse)').matches?(window.LITE?7:40):(window.LITE?8:56);",
      "const NT=matchMedia('(pointer:coarse)').matches?(window.LITE?10:56):(window.LITE?12:84);")
    r("const W=r=>r.c==='m'?1:r.c==='T'?6:4;",
      "const W=r=>WRUTA(r)/Math.min(r.L,3);")
    # --- rutas cercanas: lista con pesos para los coches y sin rotondas para los peatones
    r("function rutasCerca(){const R2=F.R+.5;CERCA=[];CERCA_P=[];if(!RUTAS)return;for(const r of RUTAS){const b=r.bb;if(F.x<b[0]-R2||F.x>b[2]+R2||F.y<b[1]-R2||F.y>b[3]+R2)continue;CERCA.push(r);if((r.c==='m'||r.c==='E'||r.c==='S'||r.c==='P')&&!r.b)CERCA_P.push(r)}}",
      "// tráfico por importancia (edit_trafico): los coches se colocan sobre todo en avenidas y calles principales\n"
      "const WRUTA=r=>(r.c==='P'?9:r.c==='S'?6:r.c==='T'?3:r.c==='E'?3:.5)*Math.min(r.L,3)*(r.dead?.15:1);let CERCA_W=[],CERCA_WT=0;\n"
      "function rutaPeso(){const t=Math.random()*CERCA_WT;let lo=0,hi=CERCA_W.length-1;while(lo<hi){const m=(lo+hi)>>1;if(CERCA_W[m]<t)lo=m+1;else hi=m}return CERCA[lo]}\n"
      "function rutasCerca(){const R2=F.R+.5;CERCA=[];CERCA_P=[];CERCA_W=[];CERCA_WT=0;if(!RUTAS)return;for(const r of RUTAS){const b=r.bb;if(F.x<b[0]-R2||F.x>b[2]+R2||F.y<b[1]-R2||F.y>b[3]+R2)continue;CERCA.push(r);CERCA_WT+=r.ring?0:WRUTA(r);CERCA_W.push(CERCA_WT);if((r.c==='m'||r.c==='E'||r.c==='S'||r.c==='P')&&!r.b&&!r.ring)CERCA_P.push(r)}}")
    r("function recolocar(o,lista,dmin,dmax){const grupo=o.g?TRAF:PEA,sep=o.g?.6:.18;for(let k=0;k<16;k++){const r=lista[Math.floor(Math.random()*lista.length)];",
      "function recolocar(o,lista,dmin,dmax){const grupo=o.g?TRAF:PEA,sep=o.g?.6:.18;for(let k=0;k<16;k++){const r=(o.g&&lista===CERCA&&CERCA_WT>0)?rutaPeso():lista[Math.floor(Math.random()*lista.length)];")
    # --- peatones: no siguen por rotondas
    r("if(soloPeaton&&(r.c==='T'||r.b))continue;",
      "if(soloPeaton&&(r.c==='T'||r.b||r.ring))continue;")
    # --- peatones: al esquivar no se meten en la calzada (solo acera, suelo o paso de cebra)
    r("const nx=q.ex+q.evx*dt,ny=q.ey+q.evy*dt,t=cell(q.x+nx,q.y+ny).t;if(t!==3&&t!==0&&t!==6&&t!==-1){q.ex=nx;q.ey=ny}",
      "const nx=q.ex+q.evx*dt,ny=q.ey+q.evy*dt,cn=cell(q.x+nx,q.y+ny),t=cn.t;if(t===1||t===5||(t===2&&cn.c)){q.ex=nx;q.ey=ny}")
    # --- peatones: el ajuste suave de la distancia al bordillo no los deja sobre el asfalto, y comprobación final
    r("q.oxs=(q.oxs??ox)+(ox-(q.oxs??ox))*Math.min(1,dt*4);q.ox=ox;",
      "q.oxs=(q.oxs??ox)+(ox-(q.oxs??ox))*Math.min(1,dt*4);q.ox=ox;if(!q.cruza){const tc=cell(x+sd*(off+q.oxs),y+cd*(off+q.oxs)).t;if(tc!==1&&tc!==5)q.oxs=ox}")
    r("{const vr=peaReacciona(q,dt);q.x+=q.ex||0;q.y+=q.ey||0;if(vr!=null)ang=vr}",
      "{const vr=peaReacciona(q,dt);q.x+=q.ex||0;q.y+=q.ey||0;if(vr!=null)ang=vr}\n"
      "  if(!q.cruza&&!(q.caido>0)){const cf=cell(q.x,q.y);if(cf.t===2&&!cf.c){if(q.ex||q.ey){q.x-=q.ex||0;q.y-=q.ey||0;q.ex=q.ey=0;q.esq=0}const cb=cell(q.x,q.y);if(cb.t===2&&!cb.c){q.r=null;q.x=1e5;PEA_G.hide(i);continue}}}   // nunca por la calzada fuera del paso de cebra")
    open(f,'w',encoding='utf8').write(s);print('ok trafico',f)
