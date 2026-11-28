# Climas: el tiempo pasa a ser una mezcla de presets (en todas las páginas). Cada preset toca, además de nubes, lluvia y
# niebla: turbidez del aire (tur), sol directo (sol), luz difusa del cielo (dif), exposición (exp), sombras suaves (som),
# tono dorado (oro), brétema baja (bre) y chaparrones a rachas (chub). Los valores se mezclan poco a poco al cambiar.
#  despejado atlántico · nubes = nublado plateado · bretema = brétema matinal · lluvia = chubasco · dorado = atardecer dorado · neboa
# En las páginas con WebGPU, la turbidez y el dorado entran en el cielo físico (gpu_cielofis.js) y la brétema en la niebla
# baja (gpu_bretema.js). Para misiones: tiempoPreset('neboa',true) pone un clima (true = de golpe, sin transición).
import sys,os,glob
FILES=sys.argv[1:] or [f for f in ['index.html','gpu.html','webgl.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
MARCA='// climas: presets que se mezclan'
for f in FILES:
    s=open(f,encoding='utf8').read()
    if MARCA in s: print('ya estaba',f);continue
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("const TIEMPO={modo:'auto',act:'despejado',sig:150,txt:'',W:{cov:0,rain:0,fog:0}};",
      "const TIEMPO={modo:'auto',act:'despejado',sig:150,txt:'',W:{cov:0,rain:0,fog:0,tur:0,sol:1,dif:0,exp:1,som:0,oro:0,bre:0,chub:0},rach:.5,rt:0};")
    r("const TOBJ={despejado:{cov:0,rain:0,fog:0},nubes:{cov:.72,rain:0,fog:.12},lluvia:{cov:1,rain:1,fog:.38},neboa:{cov:.3,rain:0,fog:1}};",
      MARCA+""" (cov nubes, rain lluvia, fog niebla, tur turbidez del aire, sol sol directo, dif luz difusa, exp exposición,
// som sombras suaves, oro tono dorado, bre brétema baja, chub chaparrones a rachas)
const TOBJ={despejado:{cov:0,rain:0,fog:0,tur:0,sol:1,dif:0,exp:1,som:0,oro:0,bre:0,chub:0},                 // despejado atlántico: aire limpio, sombras duras
 nubes:{cov:.85,rain:0,fog:.12,tur:3,sol:.85,dif:.28,exp:1.07,som:1,oro:0,bre:0,chub:0},                     // nublado plateado: luz difusa, sombras suaves
 bretema:{cov:.2,rain:0,fog:.18,tur:2,sol:1,dif:.1,exp:1.03,som:.35,oro:.12,bre:.45,chub:0},                // brétema matinal: niebla baja en la ría, el resto despejado
 lluvia:{cov:1,rain:1,fog:.38,tur:4,sol:1,dif:.1,exp:1,som:1,oro:0,bre:.08,chub:1},                          // chubasco: a rachas, suelo mojado y reflejos
 dorado:{cov:.15,rain:0,fog:.05,tur:3.5,sol:1.08,dif:0,exp:1.04,som:0,oro:1,bre:0,chub:0},                   // atardecer dorado: calima cálida y sol de oro
 neboa:{cov:.3,rain:0,fog:1,tur:0,sol:1,dif:0,exp:1,som:.6,oro:0,bre:0,chub:0}};                             // néboa cerrada
// para misiones y eventos: tiempoPreset('neboa') (con transición) o tiempoPreset('neboa',true) (de golpe); 'auto' vuelve al tiempo que cambia solo
window.tiempoPreset=(n,inm)=>{if(n==='auto'){TIEMPO.modo='auto';return}if(!TOBJ[n])return;TIEMPO.modo=n;TIEMPO.act=n;if(inm)Object.assign(TIEMPO.W,TOBJ[n])};""")
    r("const TICO={auto:'🌦️',despejado:'☀️',nubes:'⛅',lluvia:'🌧️',neboa:'🌫️'},TNOM={despejado:'Despejado',nubes:'Nubes',lluvia:'Chuvia',neboa:'Néboa'};",
      "const TICO={auto:'🌦️',despejado:'☀️',nubes:'🌥️',bretema:'🌁',lluvia:'🌧️',dorado:'🌇',neboa:'🌫️'},TNOM={despejado:'Despejado',nubes:'Nublado',bretema:'Brétema',lluvia:'Chubasco',dorado:'Dorado',neboa:'Néboa'};")
    # cambios al azar: brétema por la mañana, dorado al atardecer, tras el chubasco queda plateado
    r(" const P=a==='lluvia'?{nubes:.6,despejado:.25,lluvia:.15}:a==='neboa'?{despejado:.55,nubes:.45}:a==='nubes'?{despejado:.45,lluvia:.3,nubes:.1,neboa:.15}:{despejado:.35,nubes:.4,neboa:(h>5&&h<11)?.2:.08,lluvia:.1};",
      " const man=h>5.5&&h<11,tar=h>18.3&&h<21.3;\n const P=a==='lluvia'?{nubes:.6,despejado:.22,lluvia:.18}:a==='neboa'?{despejado:.5,nubes:.4,bretema:man?.2:0}:a==='bretema'?{despejado:.6,nubes:.3,bretema:man?.15:0}:a==='dorado'?{despejado:.5,dorado:tar?.35:0,nubes:.25}:a==='nubes'?{despejado:.4,lluvia:.3,nubes:.12,neboa:.08,dorado:tar?.15:0}:{despejado:.3,nubes:.35,bretema:man?.25:0,neboa:man?.08:.03,lluvia:.1,dorado:tar?.35:0};")
    # luz: sol directo, luz difusa, tono dorado y sombras suaves según el clima
    r("sun.intensity*=1-.78*ov;hemi.intensity*=1+.12*ov;","sun.intensity*=(1-.78*ov)*W.sol;hemi.intensity*=1+.12*ov+W.dif;")
    r(" R.toneMappingExposure=1.05*(1-.12*rain);",""" {const dia=1-CIELO.nf;if(W.oro>.01){sun.color.lerp(_c2.set(0xffb15a),W.oro*.45*dia);hemi.color.lerp(_c2.set(0xffd6a6),W.oro*.22*dia);SKYU.uHor.value.lerp(_c1.set(0xf2c27a).multiplyScalar(.2+.8*dia),W.oro*.28*dia)}
  const S=sun.shadow;S.radius=1+5*W.som;S.intensity=1-.5*W.som;if(window.CSMG&&CSMG.csm)for(const l of CSMG.csm.lights){l.shadow.radius=S.radius;l.shadow.intensity=S.intensity}}
 R.toneMappingExposure=1.05*(1-.12*rain)*W.exp;""")
    # chubasco: la lluvia va a rachas y moja antes
    r(" lluviaTick(dt,rain);TIEMPO.moj=THREE.MathUtils.clamp((TIEMPO.moj||0)+(rain>.3?dt/35*rain:-dt/160),0,1);",
      " TIEMPO.rt+=dt;TIEMPO.rach=.5+.5*Math.sin(TIEMPO.rt*.21)*Math.sin(TIEMPO.rt*.067+1.3);\n lluviaTick(dt,rain*(1-W.chub*.55+W.chub*.75*TIEMPO.rach));TIEMPO.moj=THREE.MathUtils.clamp((TIEMPO.moj||0)+(rain>.3?dt/(35-17*W.chub)*rain:-dt/160),0,1);")
    # botón: todos los climas; brétema y dorado llevan el reloj a su hora si el reloj va solo
    r("document.getElementById('bTiempo').onclick=e=>{const M=['auto','despejado','nubes','lluvia','neboa'];TIEMPO.modo=M[(M.indexOf(TIEMPO.modo)+1)%5];",
      "document.getElementById('bTiempo').onclick=e=>{const M=['auto','despejado','nubes','bretema','lluvia','dorado','neboa'];TIEMPO.modo=M[(M.indexOf(TIEMPO.modo)+1)%M.length];\n if(CIELO.modo==='auto'){const h=CIELO.h;if(TIEMPO.modo==='dorado'&&!(h>19&&h<21.3))CIELO.h=20.3;if(TIEMPO.modo==='bretema'&&!(h>6.8&&h<10.5))CIELO.h=8.2}")
    open(f,'w',encoding='utf8').write(s);print('ok climas',f)
