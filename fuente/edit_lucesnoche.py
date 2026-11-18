import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= ENCENDIDO DE LUCES: DE NOCHE, SOLO EN EL CENTRO, POR LAS GRANDES AVENIDAS =================
# · La misión es nocturna: al empezar se hace de noche y la ciudad está apagada (edificios, farolas y luz ambiente bajan).
# · Los arcos solo van por el centro, sobre todo por las grandes avenidas (Gran Vía, Urzaiz, García Barbón, Colón,
#   Policarpo Sanz, Príncipe, Porta do Sol, Rosalía de Castro, Areal…), y hay más: 10 la primera vez, hasta 16 después.
# · Cada arco que enciendes da un fogonazo de luz y la ciudad entera se va iluminando un poco más; al final, todo brilla.
r("luces:true,centro:true,n:5,","luces:true,centro:true,n:10,")
r("luces:true,n:Math.min(9,6+c)","luces:true,n:Math.min(16,11+c)")
r("sel.every(s_=>Math.hypot(s_[1]-d[1],s_[2]-d[2])>1.1)","sel.every(s_=>Math.hypot(s_[1]-d[1],s_[2]-d[2])>.8)")
r("for(const d of mez(C.filter(d=>LUZ_CALLES.test(d[0]))))if(sel.length<m.n&&ok(d)&&!sel.some(s_=>s_[0]===d[0]))sel.push(d);",
  "{const cen=d=>d[1]>86&&d[1]<103.5&&d[2]>13.6&&d[2]<26.5,AV=C.filter(d=>cen(d)&&LUZ_AV.test(d[0]));for(let pas=0;pas<3;pas++)for(const d of mez(AV.slice()))if(sel.length<m.n&&ok(d)&&sel.filter(s_=>s_[0]===d[0]).length<=pas)sel.push(d);\n  for(const d of mez(C.filter(d=>cen(d)&&LUZ_CALLES.test(d[0]))))if(sel.length<m.n&&ok(d))sel.push(d)}")
r("function lucesInicio(m){",r"""const LUZ_AV=/Gran Vía|Urz[aá]iz|García Barbón|Colón|Policarpo Sanz|Príncipe|Porta do Sol|Rosalía de Castro|Areal|Elduayen|Marqués de Valladares|Velázquez Moreno|Venezuela|Camelias|Lepanto|Praza de Compostela/i;
// noche y ciudad apagada durante la misión; luces de los arcos encendidos
function lucesNoche(on){if(on){if(LUZ.hPrev===undefined)LUZ.hPrev=CIELO.h;LUZ.ilum=0;LUZ.obj=0;LUZ.flash=0;LUZ.noche=true;
  if(!LUZ.pl){LUZ.pl=[];for(let k=0;k<4;k++){const l=new THREE.PointLight(0xffd690,0,1.6,1.4);l.position.set(0,-50,0);scene.add(l);LUZ.pl.push(l)}}}
 else{LUZ.noche=false;if(LUZ.hPrev!==undefined){CIELO.h=LUZ.hPrev;LUZ.hPrev=undefined}if(LUZ.pl)for(const l of LUZ.pl){l.intensity=0;l.position.y=-50}}}
function lucesBrillo(){if(!LUZ.noche)return;if(!REP.on){lucesNoche(false);return}const f=LUZ.ilum||0,fl=LUZ.flash||0,k=.3+.7*f;
 hemi.intensity=hemi.intensity*k+fl*.35;sun.intensity*=k;UF.uLuz.value*=.2+.8*f;LAMPARA_MAT.emissiveIntensity*=.25+.75*f;R.toneMappingExposure*=.85+.15*f+.06*fl}
function lucesInicio(m){lucesNoche(true);""")
r("R.toneMappingExposure=1.05*(1-.12*rain);","R.toneMappingExposure=1.05*(1-.12*rain);lucesBrillo();")
r("a.lit=true;a.t=0;","a.lit=true;a.t=0;LUZ.flash=1;LUZ.obj=(LUZ.i+1)/Math.max(1,LUZ.ruta.length);")
r("function lucesTick(dt){if(!LUZ.arcos.length)return;LUZ.t+=dt;",r"""function lucesTick(dt){if(!LUZ.arcos.length)return;LUZ.t+=dt;
 if(LUZ.noche){if(LUZ.on)CIELO.h=22.3;LUZ.ilum+=((LUZ.obj||0)-LUZ.ilum)*Math.min(1,dt*1.5);LUZ.flash=Math.max(0,(LUZ.flash||0)-dt*.8);
  // las 4 luces reales van a los arcos encendidos más cercanos al jugador
  const enc=LUZ.arcos.filter(a=>a.lit).sort((a,b)=>Math.hypot(a.x-P.x,a.y-P.y)-Math.hypot(b.x-P.x,b.y-P.y));
  LUZ.pl.forEach((l,i)=>{const a=enc[i];if(!a){l.intensity=0;return}l.position.set(a.x,groundY(a.x,a.y)+.16,a.y);l.intensity=(1.1+2.2*Math.max(0,1-a.t*.7))*(.85+.15*Math.sin(LUZ.t*3+i))})}""")
r("function lucesFin(){if(!LUZ.on)return;LUZ.on=false;","function lucesFin(){if(!LUZ.on)return;LUZ.on=false;LUZ.obj=1;LUZ.flash=1.4;setTimeout(()=>lucesNoche(false),4200);")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok lucesnoche')
