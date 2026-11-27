// ---------- sombras en cascada con WebGPU (gpu_csm.js) ----------
// Al conducir (calidad alta y de día, y en las carreras con sombras): el sol usa sombras en cascada de three.js
// (CSMShadowNode) atadas a la cámara del coche. Tres mapas: hasta ~1,2 u (unos 50 m) uno muy nítido de 2048 px que se
// rehace en cada imagen; hasta ~6 u otro de 2048 px cada dos imágenes; y hasta la niebla uno barato de 1024 px cada tres
// imágenes (la ría, los montes lejanos). Fundido entre cascadas para que no se vea el corte. Sustituye a la cascada lejana
// del motor viejo (sol_cascada_lejana), que con WebGPU no hacía nada y se dibujaba igual.
// En la maqueta: un solo mapa, pero ajustado a lo que se ve en pantalla (antes cubría siempre toda la maqueta): al
// acercarte las sombras se afinan; al alejarte quedan como antes. Encajado en su rejilla para que no tiemblen.
// Cambiar de un modo a otro obliga a rehacer los materiales (lo mismo que ya pasaba al subir o bajar del coche).
// Con window.__CSM_OFF=true se vuelve a las sombras de antes (al siguiente cambio de modo).
const CSMG={csm:null,act:'normal',offPrev:false,forz:false,f:0,cerca:1.2,medio:6,lejos:30};window.CSMG=CSMG;
function csmNuevo(){const C=new GT_CSM.CSMShadowNode(sun,{cascades:3,maxFar:CSMG.lejos,mode:'custom',lightMargin:15,
  customSplitsCallback:(n,near,far,br)=>{br.push(Math.min(.9,CSMG.cerca/far),Math.min(.95,CSMG.medio/far),1)}});
 C.fade=true;C._init({camera:pcam,renderer:R});
 C.lights.forEach((l,i)=>{const s=l.shadow;if(i===2)s.mapSize.set(1024,1024);s.camera.near=.05;s.camera.far=110;s.camera.updateProjectionMatrix();s.autoUpdate=i===0});
 C.updateFrustums();return C}
// maqueta: el mapa de sombras del sol cubre solo lo que se ve (cámara ortográfica), con margen para lo que hace sombra desde fuera
const _mqP=[new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3()],
 _mqM=new THREE.Matrix4(),_mqO=new THREE.Vector3(),_mqD=new THREE.Vector3(),_mqU=new THREE.Vector3(0,1,0);
function sombraMaqueta(){const c=sun.shadow.camera;cam.updateMatrixWorld();cam.getWorldDirection(_mqD);if(Math.abs(_mqD.y)<.05)return;
 let k=0;for(const[x,y]of[[-1,-1],[1,-1],[1,1],[-1,1]])for(const h of[0,3]){_mqO.set(x,y,-1).unproject(cam);const t=(h-_mqO.y)/_mqD.y;_mqP[k++].copy(_mqO).addScaledVector(_mqD,t)}
 sun.updateMatrixWorld();sun.target.updateMatrixWorld();_mqM.lookAt(sun.position,sun.target.position,_mqU).setPosition(sun.position).invert();
 let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;for(const p of _mqP){p.applyMatrix4(_mqM);x0=Math.min(x0,p.x);x1=Math.max(x1,p.x);y0=Math.min(y0,p.y);y1=Math.max(y1,p.y)}
 const mz=Math.max(x1-x0,y1-y0)*1.08+2,E=Math.pow(2,Math.ceil(Math.log2(mz)*4)/4),q=E/sun.shadow.mapSize.x;   // tamaño a saltos (no tiembla al hacer zoom)
 const cx=Math.round((x0+x1)/2/q)*q,cy=Math.round((y0+y1)/2/q)*q;
 if(c.left!==cx-E/2||c.bottom!==cy-E/2||c.right!==cx+E/2){Object.assign(c,{left:cx-E/2,right:cx+E/2,bottom:cy-E/2,top:cy+E/2,near:1,far:400});c.updateProjectionMatrix()}}
// pone el modo: con la sombra ya soltada (la imagen anterior se dibujó sin sombra del sol)
function csmAplicar(m){if(CSMG.csm){try{CSMG.csm.dispose()}catch(e){}CSMG.csm=null}
 if(m==='csm'){CSMG.csm=csmNuevo();sun.shadow.shadowNode=CSMG.csm}else delete sun.shadow.shadowNode;CSMG.act=m}
// cada imagen, justo antes de dibujar
function csmTick(){if(window.LITE)return;
 const obj=!window.__CSM_OFF&&driving?'csm':'normal';   // cascadas en el coche; en la maqueta, el mapa ajustado a la vista
 if(CSMG.forz){CSMG.forz=false;csmAplicar(obj);if(!sun.castShadow)sun.castShadow=true}
 else if(obj!==CSMG.act){if(!sun.castShadow){if(CSMG.offPrev)csmAplicar(obj)}else{sun.castShadow=false;CSMG.forz=true}}   // una imagen sin sombra para soltar la de antes
 CSMG.offPrev=!sun.castShadow;
 if(CSMG.act==='csm'&&CSMG.csm){const C=CSMG.csm;C.maxFar=Math.max(CSMG.medio+2,Math.min(CSMG.lejos,FOG.far+2));C.updateFrustums();
  CSMG.f=(CSMG.f+1)%6;const L=C.lights;if(L[1]&&CSMG.f%2===0)L[1].shadow.needsUpdate=true;if(L[2]&&CSMG.f%3===0)L[2].shadow.needsUpdate=true}
 else if(!window.__CSM_OFF&&!driving&&sun.castShadow&&!CSMG.forz)sombraMaqueta()}
// ---------- fin de gpu_csm.js
