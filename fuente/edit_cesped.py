# Césped y hierba más reales (las cinco páginas; va al final de la cadena).
# Los jardines, parques y medianas («verde» de cada zona), las jardineras de las rampas de Gran Vía y los taludes de
# césped de la AP-9 eran de un verde pastel liso. Ahora se pintan en el propio sombreado, en coordenadas del mundo
# (sin texturas que cargar ni repeticiones visibles):
#  - verde más natural y menos chillón, con manchas más claras y más oscuras (de 25 a 2 m) y calvas secas
#    amarillentas de paja aquí y allá;
#  - matas (≈ 0,7 m) y, de cerca, briznas (≈ 10 cm) que además mueven la luz (relieve en la normal), así que el sol
#    rasante hace brillar el césped; todo se difumina con la distancia para que no haya parpadeo;
#  - en parte de los parques, franjas de corte de cortacésped claras y oscuras de unos 2,5 m;
#  - margaritas blancas y alguna flor amarilla salpicadas (solo de cerca);
#  - con lluvia el césped se oscurece poco a poco (usa el mismo «mojado» que las calles).
# En el móvil (LITE) va sin briznas, relieve ni flores (solo color, manchas y matas).
import os
ANCLA="// las mallas grandes de cada zona (edificios"
OLD_ZONA="if(sm)for(const mm of [].concat(o.material))mojado(mm,sm)}"
NEW_ZONA="if(sm)for(const mm of [].concat(o.material))mojado(mm,sm)}if(/^verde/.test(o.name))for(const mm of [].concat(o.material))cesped(mm);"
OLD_CES="const CES=new THREE.MeshStandardMaterial({color:0x5f9a3e,roughness:1,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2})"
OLD_AP="cesped:SM({vertexColors:true,roughness:1,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2})"
NEW_AP="cesped:cesped(SM({vertexColors:true,roughness:1,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}))"
FN=r'''// ---------- césped de verdad (edit_cesped.py): manchas, calvas secas, matas, briznas, franjas de corte y margaritas, todo en el sombreado
function cesped(m){if(!m||m.userData.ces)return m;m.userData.ces=1;const prev=m.onBeforeCompile;const pk=m.customProgramCacheKey?m.customProgramCacheKey.bind(m):null;const LT=!!window.LITE;
 m.onBeforeCompile=(sh,r)=>{if(prev)prev(sh,r);sh.uniforms.uGWet=UMO.uWet;
  sh.vertexShader='varying vec3 vWg;\n'+sh.vertexShader.replace('#include <worldpos_vertex>','#include <worldpos_vertex>\n vWg=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='uniform float uGWet;varying vec3 vWg;\nfloat hG(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}\nfloat nG(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hG(i),hG(i+vec2(1,0)),f.x),mix(hG(i+vec2(0,1)),hG(i+vec2(1,1)),f.x),f.y);}\n'+sh.fragmentShader
   .replace('#include <color_fragment>',`#include <color_fragment>
    vec2 gq=vWg.xz;float gfw=max(length(fwidth(gq)),1e-6);
    float gc=1.-smoothstep(.0025,.012,gfw);                                   // detalle de cerca (briznas, flores)
    float gm=1.-smoothstep(.015,.07,gfw);                                     // detalle medio (matas, franjas)
    float gL=nG(gq*2.2)*.45+nG(gq*8.)*.35+nG(gq*19.)*.2;                       // manchas (25-2 m)
    float gD=smoothstep(.64,.88,nG(gq*2.3+7.))*(.6+.4*nG(gq*11.));            // calvas secas
    float gK=nG(gq*38.)*.6+nG(gq*95.)*.4;                                     // matas
    vec3 gb=diffuseColor.rgb*vec3(.40,.43,.27);                                // verde natural (menos pastel)
    vec3 gcol=mix(gb*vec3(.62,.74,.62),gb*vec3(1.22,1.14,.92),smoothstep(.2,.8,gL));
    gcol=mix(gcol,gcol*vec3(1.7,1.32,.7)+vec3(.025,.018,0.),gD*.6);           // paja
    gcol*=mix(1.,.72+.56*gK,gm);
    float gS=smoothstep(.5,.6,nG(gq*.6+3.));                                  // franjas de corte en parte de los parques
    gcol*=1.+.075*gS*gm*smoothstep(-.35,.35,sin(gq.x*50.+nG(gq*.4)*2.))*2.-.075*gS*gm;
    ${LT?'':`float gB=hG(floor(gq*430.));gcol*=mix(1.,.84+.32*gB,gc);            // briznas
    vec2 fcl=floor(gq*160.),ffr=fract(gq*160.)-.5;float fh=hG(fcl+11.);
    float fl=step(.968,fh)*(1.-smoothstep(.10,.19,length(ffr)))*gc*step(.45,nG(gq*3.+21.));
    gcol=mix(gcol,fh>.988?vec3(.85,.62,.06):vec3(.86,.86,.80),fl);`}
    gcol*=1.-.25*uGWet;
    diffuseColor.rgb=gcol;`)
   .replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\n roughnessFactor=mix(.92,.62,uGWet);')
   .replace('#include <normal_fragment_maps>',LT?'#include <normal_fragment_maps>':`#include <normal_fragment_maps>
    {vec2 gp=gq*95.;float e=.35;vec2 gd=vec2(nG(gp+vec2(e,0.))-nG(gp-vec2(e,0.)),nG(gp+vec2(0.,e))-nG(gp-vec2(0.,e)));
     vec2 gp2=gq*430.;gd+=vec2(hG(floor(gp2+vec2(1.,0.)))-hG(floor(gp2-vec2(1.,0.))),hG(floor(gp2+vec2(0.,1.)))-hG(floor(gp2-vec2(0.,1.))))*.35*gc;
     normal=normalize(normal+(viewMatrix*vec4(gd.x,0.,gd.y,0.)).xyz*.55*gm);}`)};
 m.customProgramCacheKey=()=>(pk?pk():'')+'|ces';m.needsUpdate=true;return m}
'''
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'function cesped(m){' in s:print('ya estaba',f);continue
    for a in (ANCLA,OLD_ZONA):assert s.count(a)==1,(f,a[:40])
    s=s.replace(ANCLA,FN+ANCLA).replace(OLD_ZONA,NEW_ZONA)
    if s.count(OLD_CES)==1:s=s.replace(OLD_CES,"const CES=cesped("+OLD_CES[len("const CES="):]+")")
    if s.count(OLD_AP)==1:s=s.replace(OLD_AP,NEW_AP)
    open(f,'w',encoding='utf-8').write(s)
    print('ok cesped',f)
