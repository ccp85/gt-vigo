# Sombras en cascada (las cinco páginas; va al final de la cadena).
# Antes había un único mapa de sombras de 2048 px que seguía al coche y cubría ±5 u: cerca, nítido;
# más allá, los edificios y árboles no proyectaban sombra. Ahora hay dos cascadas:
#  - cerca: el mismo mapa de siempre (±5 u alrededor del coche), igual de nítido.
#  - lejos: un segundo mapa de 2048 px que cubre ±40 u (unos 3 km de lado), adelantado hacia donde mira la
#    cámara, para que las fachadas, árboles y monumentos lejanos también den sombra.
# Cada punto usa la cascada cercana si cae dentro y la lejana si no, con un fundido en el borde para que
# no se vea el corte. La segunda luz es solo de sombra (intensidad 0): no cambia la iluminación.
# Para no gastar de más, la cascada lejana se recalcula como mucho cada 0,4 s (o al moverte más de 3 u),
# y se encaja en su rejilla de píxeles para que las sombras lejanas no tiemblen.
# Además, en el mundo abierto al conducir antes no había sombras del sol (solo las manchas bajo los coches):
# ahora, con «calidad alta» (tecla G) y de día, el sol proyecta sombras reales con las dos cascadas. La cascada
# cercana se recalcula cada dos imágenes. En «rendimiento», de noche o en estilo cómic, todo sigue como antes.
# Sigue a la de siempre: si la sombra del sol se apaga (noche, carrera de noche), también se apaga esta.
# En el móvil (LITE) no se añade: allí no hay sombras.
import os
CHUNK=r'''// ---------- sombras en cascada: el sombreado de la luz del sol elige entre la cascada cercana (0) y la lejana (1)
{const CH=THREE.ShaderChunk,o=CH.lights_fragment_begin,i0=o.indexOf('#if ( NUM_DIR_LIGHTS > 0 ) && defined( RE_Direct )'),i1=o.indexOf('#pragma unroll_loop_end',i0),i2=o.indexOf('#endif',i1);
 if(i0>=0&&i1>i0&&i2>i1){const orig=o.slice(i0,i2+6);
  const nuevo=`#if defined( RE_Direct ) && defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHTS == 2 ) && ( NUM_DIR_LIGHT_SHADOWS == 2 )
	DirectionalLight directionalLight = directionalLights[ 0 ];
	getDirectionalLightInfo( directionalLight, directLight );
	if ( directLight.visible && receiveShadow ) {
		vec4 gtC0 = vDirectionalShadowCoord[ 0 ];vec3 gtP0 = gtC0.xyz / gtC0.w;
		float gtE = max( abs( gtP0.x - .5 ), abs( gtP0.y - .5 ) );
		float gtK = smoothstep( .40, .48, gtE );
		float gtS0 = gtK < 1. ? getShadow( directionalShadowMap[ 0 ], directionalLightShadows[ 0 ].shadowMapSize, directionalLightShadows[ 0 ].shadowBias, directionalLightShadows[ 0 ].shadowRadius, vDirectionalShadowCoord[ 0 ] ) : 1.;
		float gtS1 = gtK > 0. ? getShadow( directionalShadowMap[ 1 ], directionalLightShadows[ 1 ].shadowMapSize, directionalLightShadows[ 1 ].shadowBias, directionalLightShadows[ 1 ].shadowRadius, vDirectionalShadowCoord[ 1 ] ) : 1.;
		directLight.color *= mix( gtS0, gtS1, gtK );
	}
	RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#else
`+orig+`
#endif`;
  CH.lights_fragment_begin=o.slice(0,i0)+nuevo+o.slice(i2+6)}else console.warn('cascadas: no encontré el bloque de luces')}
'''
OLD_SUN="sun.shadow.normalBias=.035;scene.add(sun);scene.add(sun.target);"
NEW_SUN=OLD_SUN+("const sunF=new THREE.DirectionalLight(0xffffff,0);sunF.name='sol_cascada_lejana';sunF.shadow.mapSize.set(2048,2048);sunF.shadow.bias=-.00005;sunF.shadow.normalBias=.02;sunF.shadow.autoUpdate=false;"
 "if(!window.LITE){sunF.castShadow=sun.castShadow;scene.add(sunF);scene.add(sunF.target);"
 "let cs_=sun.castShadow;Object.defineProperty(sun,'castShadow',{get(){return cs_},set(v){cs_=v;sunF.castShadow=v;if(v)sunF.shadow.needsUpdate=true},configurable:true})}window.__SUNF=sunF;")
OLD_FOL="sun.target.position.set(P.x,0,P.y);sun.position.copy(sun.target.position).add(SUNOFF)}"
NEW_FOL=("sun.target.position.set(P.x,0,P.y);sun.position.copy(sun.target.position).add(SUNOFF);"
 "if(sunF.parent){const S=40,c2=sunF.shadow.camera;if(c2.right!==S){Object.assign(c2,{left:-S,right:S,top:S,bottom:-S,near:30,far:150});c2.updateProjectionMatrix()}"
 "const v=pcam.getWorldDirection(sunF.__v||(sunF.__v=new THREE.Vector3()));const l=Math.hypot(v.x,v.z)||1,tx=P.x+v.x/l*S*.55,tz=P.y+v.z/l*S*.55,now=performance.now();"
 "const d=sunF.__x===undefined?1e9:Math.hypot(tx-sunF.__x,tz-sunF.__z);"
 "if(d>3||now-(sunF.__t||0)>400){const q=2*S/2048;sunF.__x=Math.round(tx/q)*q;sunF.__z=Math.round(tz/q)*q;sunF.__t=now;"
 "sunF.target.position.set(sunF.__x,0,sunF.__z);sunF.position.copy(sunF.target.position).add(SUNOFF);sunF.target.updateMatrixWorld();sunF.updateMatrixWorld();sunF.shadow.needsUpdate=true}}}")
ANCLA="const R=new THREE.WebGLRenderer("
OLD_LOOP="if(COMIC.on)comicRender();else if(POST.on)postRender();else R.render(scene,pcam)"
ANCLA2="function postInit(){"
TICK=("// ---------- sombras del sol al conducir por el mundo abierto (solo en calidad alta y de día)\n"
 "// el mapa del mundo es diminuto (1 u ≈ 40 m): la cámara de sombra se ciñe en profundidad y el sesgo se reduce para que farolas,\n"
 "// coches y árboles den sombra; y el suelo, fachadas y tejados, que antes no recibían sombra, pasan a recibirla mientras dure.\n"
 "let SOMB_ON=false,SOMB_F=0,SOMB_T=0,SOMB_OLD=null;const SOMB_RS=new Set();"
 "function sombrasRecv(){window.__SUNF.parent.traverse(o=>{if(!o.isMesh||o.receiveShadow||!o.visible)return;const m=o.material;if(!m||Array.isArray(m)||m.transparent||!(m.isMeshStandardMaterial||m.isMeshLambertMaterial||m.isMeshPhongMaterial))return;o.receiveShadow=true;SOMB_RS.add(o)})}"
 "function sombrasSet(on){const c=sun.shadow.camera;if(on){SOMB_OLD={b:sun.shadow.bias,nb:sun.shadow.normalBias,n:c.near,f:c.far};sun.shadow.bias=-.00004;sun.shadow.normalBias=.004;sunFollow();Object.assign(c,{near:60,far:120});c.updateProjectionMatrix();sombrasRecv();SOMB_T=performance.now()}"
 "else{for(const o of SOMB_RS)o.receiveShadow=false;SOMB_RS.clear();if(SOMB_OLD){sun.shadow.bias=SOMB_OLD.b;sun.shadow.normalBias=SOMB_OLD.nb;Object.assign(c,{near:SOMB_OLD.n,far:SOMB_OLD.f});c.updateProjectionMatrix();SOMB_OLD=null}}}"
 "function sombrasTick(){if(window.LITE||!driving||RACE.on){if(SOMB_ON){SOMB_ON=false;sombrasSet(false);if(!RACE.on)R.shadowMap.autoUpdate=true}return}"
 "const want=POST.on&&!COMIC.on&&CIELO.nf<.6;if(want!==SOMB_ON){SOMB_ON=want;sun.castShadow=want;R.shadowMap.autoUpdate=!want;sombrasSet(want)}"
 "if(want){sunFollow();SOMB_F=(SOMB_F+1)%2;if(SOMB_F===0)R.shadowMap.needsUpdate=true;const t=performance.now();if(t-SOMB_T>2000){SOMB_T=t;sombrasRecv()}}}\n")
for f in ['index.html','indexm.html','gp.html','nav.html','navm.html']:
    if not os.path.exists(f):continue
    s=open(f,encoding='utf-8').read()
    if "sol_cascada_lejana" in s:print('ya estaba',f);continue
    for a in (OLD_SUN,OLD_FOL,ANCLA,OLD_LOOP,ANCLA2):assert s.count(a)==1,(f,a[:40])
    s=s.replace(OLD_SUN,NEW_SUN).replace(OLD_FOL,NEW_FOL).replace(ANCLA,CHUNK+ANCLA).replace(OLD_LOOP,'sombrasTick();'+OLD_LOOP).replace(ANCLA2,TICK+ANCLA2)
    open(f,'w',encoding='utf-8').write(s)
    print('ok cascadas',f)
