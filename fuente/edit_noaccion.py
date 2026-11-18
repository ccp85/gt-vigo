import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= SIN BOTÓN DE ACCIÓN =================
# En el móvil no hay botón de acción en el reparto, así que todo lo que pedía E / Ⓐ ocurre solo al llegar:
# subir al tejado con el skate, saltar en el borde de los tejados, entrar a escondidas en la casa, dejar el regalo
# bajo el árbol (quedándote quieto a su lado), tirarte al agua desde la moto y volver a subir con el regalo.
# E / Ⓐ / espacio siguen funcionando en ordenador y con mando.
r("if(S.cerca){S.av-=dt;if(S.av<=0){S.av=3;mostrar(document.body.classList.contains('pad')?'Ⓐ para subir al tejado con el skate':'E (o el botón de acción) para subir al tejado con el skate')}}",
  "if(S.cerca){S.ac=(S.ac||0)+dt;if(S.ac>.6){S.ac=-2.5;aviso('🛹 ¡Al tejado!',1,'peq');skateSube()}}else if((S.ac||0)>0)S.ac=0;else if(S.ac<0)S.ac=Math.min(0,S.ac+dt)")
r("const e=skAlt(S.x+dx*.12,S.y+dy*.12);if(!e[1]&&h[1]&&S.v>.3&&(!S.avS||tn-S.avS>1.4)){S.avS=tn;aviso('⤒ ¡SALTA!',.6,'peq')}",
  "{const e2=skAlt(S.x+dx*.05,S.y+dy*.05);if(!e2[1]&&h[1]&&S.v>.2){skateSalta();if(!S.avS||tn-S.avS>3){S.avS=tn;aviso('⤒ ¡Salto!',.5,'peq')}}}")
r("mostrar('◀ ▶ gira · ▲ impulso · ▼ frena · '+(document.body.classList.contains('pad')?'Ⓐ':'E / espacio')+' salta · sigue los haces dorados: '+S.chim.length+' chimeneas')",
  "mostrar('◀ ▶ gira · ▲ impulso · ▼ frena · saltas solo al llegar al borde · en el aire ◀ ▶ giros y ▼ flip · sigue los haces dorados: '+S.chim.length+' chimeneas')")
r("if(C.fase==='puerta'){C.av-=dt;if(C.av<=0){C.av=3;mostrar(document.body.classList.contains('pad')?'Ⓐ para entrar a escondidas':'E (o el botón de acción) para entrar a escondidas')}}",
  "if(C.fase==='puerta'){C.ac=(C.ac||0)+dt;if(C.ac>.6){C.ac=0;casaEntra()}}else C.ac=0")
r("if(C.dejando>0){C.dejando+=dt;","if(!C.regalo&&!(C.dejando>0)&&!C.pillado&&!L&&Math.hypot(C.px-CASA_ARBOL[0],C.pz-CASA_ARBOL[1])<.17)C.dejando=.001;\n  if(C.dejando>0){C.dejando+=dt;")
r("mostrar('Flechas / ◀ ▶ ▲ ▼ para moverte · evita los conos amarillos · deja el regalo bajo el árbol y sal por la puerta')",
  "mostrar('Flechas / ◀ ▶ ▲ ▼ para moverte · evita los conos amarillos · quédate quieto junto al árbol para dejar el regalo y sal por la puerta')")
r("if(B.fase==='saltar'){B.av-=dt;if(B.av<=0){B.av=3;mostrar(document.body.classList.contains('pad')?'Ⓐ para tirarte al agua y bucear':'E (o el botón de acción) para tirarte al agua y bucear')}}return}",
  "if(B.fase==='saltar'){B.ac=(B.ac||0)+dt;if(B.ac>.6){B.ac=0;buceoSalta()}}else B.ac=0;return}")
r("function buceoTick(dt){const B=BUC;B.t+=dt;","function buceoTick(dt){const B=BUC;B.t+=dt;if(MODO==='nado'&&B.tiene&&B.moto&&Math.hypot(B.moto.position.x-P.x,B.moto.position.z-P.y)<.16&&P.z>B.WY-.05){buceoSube();return}")
# en el móvil, botones ⤒ ⤓ para subir y bucear mientras nadas
r("document.body.classList.toggle('heli',driving&&m==='heli');","document.body.classList.toggle('heli',driving&&m==='heli');document.body.classList.toggle('nado',driving&&m==='nado');")
r("#pad .alt{align-items:flex-end;gap:8px}","#pad .alt{align-items:flex-end;gap:8px}body.nado #pad .alt [data-k]{display:block}body.nado #pad .alt{flex-direction:column;align-items:center;gap:6px}")
open(f,'w').write(s)
def var(tit,scr,out,ref=None):
    g=open(ref or out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
var('GT Vigo · Navidad Móvil','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;window.LITE=1;document.body.classList.add("solo","lite")</script>','navm.html','nav.html')
print('ok auto')
