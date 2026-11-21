# Asfalto y marcas viales más reales (las cinco páginas; va al final de la cadena).
# Asfalto:
#  - la calzada de las zonas era gris azulado/lila (#5a5a71) y con el tono de cine salía morada: ahora gris asfalto
#    neutro (#54565b); igual en la AP-9 (#5c5e70/#55576a → #545659/#4d4f52) y en el circuito de carreras (#5c5c6c → #56585c);
#  - el árido de cerca ya no sale en cuadraditos (ruido suave en vez de celdas);
#  - además del árido, manchas y parches que ya tenía (edit de «mojado»): leves cambios de tono cálido/frío a lo largo de
#    la calle y, de cerca, manchas de aceite oscuras y alargadas aquí y allá.
# Marcas viales (malla «lineas» de cada zona):
#  - blanco menos chillón (#f4f2ed → #d9d7cf), así ya no deslumbran ni brillan con el resplandor;
#  - pintura gastada: zonas donde se ve el asfalto a través, más de cerca con grano, y de lejos se funden un poco con la
#    calzada para que los cruces con muchas marcas no se vean tan cargados;
#  - con lluvia se mojan igual que la calzada (se oscurecen y entran en los charcos), antes quedaban secas por encima.
# En el móvil (LITE): color nuevo y desgaste, sin manchas de aceite ni grano.
import os
OLD_ZONA="if(/^verde/.test(o.name))for(const mm of [].concat(o.material))cesped(mm);"
NEW_ZONA=OLD_ZONA+"if(/^(calzada|puente)/.test(o.name))for(const mm of [].concat(o.material))if(mm&&mm.name==='calzada')asfaltoReal(mm);if(/^lineas/.test(o.name))for(const mm of [].concat(o.material)){marcaVial(mm);mojado(mm,.9)}"
ANCLA="// ---------- césped de verdad (edit_cesped.py)"
COLS=[("const AS=col(0x5c5e70),AS2=col(0x55576a)","const AS=col(0x545659),AS2=col(0x4d4f52)"),
      ("const mA=new THREE.MeshStandardMaterial({color:0x5c5c6c,","const mA=new THREE.MeshStandardMaterial({color:0x56585c,")]
FN=r'''// ---------- asfalto y marcas viales (edit_asfalto.py): gris neutro, tonos y aceite en la calzada; marcas menos blancas, gastadas y que se mojan
const ASF_GLSL='float hA(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}\nfloat nA(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hA(i),hA(i+vec2(1,0)),f.x),mix(hA(i+vec2(0,1)),hA(i+vec2(1,1)),f.x),f.y);}\n';
function asfaltoReal(m){if(!m||m.userData.asf)return m;m.userData.asf=1;m.color.set(0x54565b);const prev=m.onBeforeCompile;const pk=m.customProgramCacheKey?m.customProgramCacheKey.bind(m):null;const LT=!!window.LITE;
 m.onBeforeCompile=(sh,r)=>{if(prev)prev(sh,r);
  sh.vertexShader='varying vec3 vWa;\n'+sh.vertexShader.replace('#include <worldpos_vertex>','#include <worldpos_vertex>\n vWa=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='varying vec3 vWa;\n'+ASF_GLSL+sh.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
   {vec2 aq=vWa.xz;float afw=max(length(fwidth(aq)),1e-6);
    float tn=nA(aq*.8)*.6+nA(aq*3.1)*.4-.5;diffuseColor.rgb*=1.+vec3(.06,.035,-.05)*tn*2.;      // tono cálido/frío
    ${LT?'':`vec2 oc=floor(aq*26.),of=fract(aq*26.)-.5;float oh=hA(oc);
    vec2 od=of+(vec2(hA(oc+5.),hA(oc+9.))-.5)*.3;float oa=hA(oc+13.)*3.14;od=mat2(cos(oa),-sin(oa),sin(oa),cos(oa))*od;
    float oil=step(.92,oh)*(1.-smoothstep(.10,.30,length(od*vec2(1.,2.2))+(nA(aq*300.)-.5)*.12))*(1.-smoothstep(.008,.035,afw));
    diffuseColor.rgb*=1.-.38*oil;`}}`)};
 m.customProgramCacheKey=()=>(pk?pk():'')+'|asf';m.needsUpdate=true;return m}
function marcaVial(m){if(!m||m.userData.mv)return m;m.userData.mv=1;m.color.set(0xd9d7cf);m.roughness=Math.min(m.roughness??.8,.7);const prev=m.onBeforeCompile;const pk=m.customProgramCacheKey?m.customProgramCacheKey.bind(m):null;const LT=!!window.LITE;
 m.onBeforeCompile=(sh,r)=>{if(prev)prev(sh,r);
  sh.vertexShader='varying vec3 vWv;\n'+sh.vertexShader.replace('#include <worldpos_vertex>','#include <worldpos_vertex>\n vWv=(modelMatrix*vec4(transformed,1.)).xyz;');
  sh.fragmentShader='varying vec3 vWv;\n'+ASF_GLSL+sh.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
   {vec2 vq=vWv.xz;float vfw=max(length(fwidth(vq)),1e-6);vec3 asf=vec3(.088,.093,.104);              // color del asfalto (lineal)
    float cerca=1.-smoothstep(.004,.02,vfw),lejos=smoothstep(.012,.07,vfw);
    float gas=smoothstep(.5,.85,nA(vq*45.)*.6+nA(vq*130.)*.4)*.8;                                       // pintura gastada
    ${LT?'':'gas=max(gas,smoothstep(.6,.8,nA(vq*380.))*.6*cerca);'}                                      // grano: puntos sin pintura
    diffuseColor.rgb=mix(diffuseColor.rgb,asf,clamp(gas*(.35+.65*cerca)+lejos*.28,0.,.85));}`)};
 m.customProgramCacheKey=()=>(pk?pk():'')+'|mv';m.needsUpdate=true;return m}
'''
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if 'function asfaltoReal(m){' in s:print('ya estaba',f);continue
    for a in (OLD_ZONA,ANCLA):assert s.count(a)==1,(f,a[:40])
    s=s.replace(ANCLA,FN+ANCLA).replace(OLD_ZONA,NEW_ZONA)
    a="float grano=(hM(floor(q*420.))-.5)"   # el árido de cerca salía en cuadraditos: ruido suave en vez de celdas
    if s.count(a)==1:s=s.replace(a,"float grano=(nM(q*420.)-.5)*1.3")
    for a,b in COLS:
        if s.count(a)==1:s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s)
    print('ok asfalto',f)
