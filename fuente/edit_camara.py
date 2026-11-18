import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------------- cámara que no se mete en los edificios (conduciendo y a pie por la ciudad)
# Antes solo se comprobaba con un rayo contra los edificios, y esos «árboles de colisión» tardan en construirse tras cargar
# cada barrio: al principio la cámara atravesaba las fachadas. Ahora se usa también el plano de la ciudad (instantáneo):
# si detrás hay un edificio, la cámara se acerca y sube; y si al seguir al coche cae dentro de uno, salta a su sitio.
r("let dist=CD;hgt=PIE?.15+(.2-dist)*.4:(MOTO?.28:MOTOC?.25:.34)+((MOTOC?.36:.46)-dist)*.6;",
  r"""let dist=CD;hgt=PIE?.15+(.2-dist)*.4:(MOTO?.28:MOTOC?.25:.34)+((MOTOC?.36:.46)-dist)*.6;
 if(!(((REP.on&&REP.red)||(RACE.on&&RACE.nav))&&MODO==='coche')){const mx=dist+.04;let dd=mx;
  for(let q=1;q<=14;q++){const s_=q/14*mx,t_=cell(P.x-dx*s_,P.y-dz*s_).t;if(t_===3||t_===6||t_===-1){dd=Math.max(PIE?.07:.11,s_-.05);break}}
  window.CAMF=window.CAMF??dd;CAMF+=(dd-CAMF)*Math.min(1,dt*(dd<CAMF?16:2.5));if(CAMF<dist){hgt+=(dist-CAMF)*(PIE?.5:.8);dist=CAMF}}""")
r("if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*(camC||(((REP.on&&REP.red)||(RACE.on&&RACE.nav))&&MODO==='coche')?14:6)));",
  "if(!camInit){pcam.position.copy(want);camInit=true}else pcam.position.lerp(want,Math.min(1,dt*(camC||(((REP.on&&REP.red)||(RACE.on&&RACE.nav))&&MODO==='coche')?14:6)));\n {const t_=cell(pcam.position.x,pcam.position.z).t;if(t_===3||t_===6||t_===-1)pcam.position.lerp(want,Math.min(1,dt*20))}")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok camara')
# ---------------- bloques negros a pie de calle → escaparates de cristal
s=open('index.html').read()
r("vidaPlaya(root);",r"""root.traverse(o=>{if(o.isMesh&&/^piezas/.test(o.name)){const m=o.material;if(m&&!Array.isArray(m)&&m.name==='#2c3438')vitrina(m)}});vidaPlaya(root);""")
r("function fachadaViva(m){",r"""// las piezas oscuras de una planta de alto delante de los bajos se veían como bloques negros: ahora son escaparates de cristal
// (montantes claros, reflejo del cielo, luz cálida dentro de noche) con remate de piedra arriba
function vitrina(m){if(m.userData.vit)return;m.userData.vit=1;m.color.set('#ffffff');m.roughness=.2;m.metalness=.1;m.emissive=new THREE.Color(0xffc98a);m.emissiveIntensity=1;
 m.onBeforeCompile=sh=>{Object.assign(sh.uniforms,UF,{uZen:SKYU.uZen,uHor:SKYU.uHor,uNf:SKYU.uNight});
  sh.vertexShader='varying vec3 vWV;\n'+sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\n vWV=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='uniform float uLuz,uNf;uniform vec3 uZen,uHor;varying vec3 vWV;float vGl;\nfloat hV(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}\n'+sh.fragmentShader
   .replace('#include <color_fragment>',`#include <color_fragment>
    vec3 nV=normalize(cross(dFdx(vWV),dFdy(vWV)));vGl=0.;
    if(abs(nV.y)>.6){diffuseColor.rgb=vec3(.74,.72,.68)*(.9+.1*hV(floor(vWV.xz*300.)));}
    else{vec2 tg=normalize(vec2(-nV.z,nV.x));float u=dot(vWV.xz,tg)*62.;float yy=vWV.y*62.;
     float mu=smoothstep(.84,.9,abs(fract(u)-.5)*2.);float tr=step(.82,fract(yy*.22));
     float fr=max(mu,tr);vGl=1.-fr;diffuseColor.rgb=mix(vec3(.09,.12,.16),vec3(.78,.78,.76),fr);}`)
   .replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\n roughnessFactor=mix(.75,.08,vGl);')
   .replace('#include <emissivemap_fragment>','#include <emissivemap_fragment>\n totalEmissiveRadiance*=vGl*uLuz*.9*step(.35,hV(floor(vWV.xz*40.)));')
   .replace('#include <opaque_fragment>',`{vec3 Vv=normalize(cameraPosition-vWV);float fr=.12+.7*pow(1.-abs(Vv.y),3.);vec3 sky=mix(uHor,uZen,.4)*(1.-.75*uNf);outgoingLight=mix(outgoingLight,sky*.55,vGl*fr*.28);}
    #include <opaque_fragment>`)};
 m.customProgramCacheKey=()=>'vit';m.needsUpdate=true}
function fachadaViva(m){""")
open('index.html','w').write(s)
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok vitrina')
