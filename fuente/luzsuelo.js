// ---------- luz en el suelo (luzsuelo.js, lo mete edit_luzsuelo.py)
// Las luces de Navidad tiñen el suelo: bajo cada arco encendido aparece una mancha de luz cálida en el asfalto y las aceras
// (más fuerte bajo la guirnalda y junto a los postes), que se enciende con el arco, titila con las bombillas y, en el arco
// que toca, late suave para guiarte. Los muñecos, el regalo gigante y el árbol de Porta do Sol tienen la suya, más grande
// (la del árbol, fría y azulada como sus LED). Solo de noche: al hacerse de día se apagan poco a poco.
// Son láminas que siguen el relieve del suelo, con mezcla aditiva, sin luces de verdad: casi no cuestan, también en el móvil.
const LSU={k:0,esp:[],tex:{}};window.__LSU=LSU;
function lsuTex(tipo){if(LSU.tex[tipo])return LSU.tex[tipo];const N=128,c=document.createElement('canvas');c.width=c.height=N;const x=c.getContext('2d');x.globalCompositeOperation='lighter';
 const spot=(cx,cy,rx,ry,a)=>{x.save();x.translate(cx,cy);x.scale(1,ry/rx);const g=x.createRadialGradient(0,0,0,0,0,rx);g.addColorStop(0,`rgba(255,255,255,${a})`);g.addColorStop(.45,`rgba(255,255,255,${a*.45})`);g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.beginPath();x.arc(0,0,rx,0,6.2832);x.fill();x.restore()};
 if(tipo==='arco'){// u = a lo ancho de la calle, v = a lo largo: banda bajo la guirnalda, más luz en el centro (estrella) y en los postes
  spot(64,64,62,52,.55);spot(64,64,44,26,.5);spot(64,64,18,14,.35);for(const u of[22,106])spot(u,64,14,22,.35);
  for(let k=1;k<12;k++)spot(16+k*8,64,6,26,.07)}
 else spot(64,64,64,64,.75),spot(64,64,30,30,.35);
 const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;LSU.tex[tipo]=t;return t}
function lsuMat(tipo,col){return new THREE.MeshBasicMaterial({map:lsuTex(tipo),color:col,transparent:true,opacity:0,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,
 polygonOffset:true,polygonOffsetFactor:-4,polygonOffsetUnits:-4,toneMapped:true,fog:true})}
// lámina que sigue el suelo: centro (x,y), eje u=(ux,uy) con semiancho a, eje v=(-uy,ux) con semilargo b
function lsuLamina(x,y,ux,uy,a,b,nu,nv,mat){const vx=-uy,vy=ux,P=[],UV=[],I=[];
 for(let j=0;j<=nv;j++)for(let i=0;i<=nu;i++){const s=2*i/nu-1,t=2*j/nv-1,X=x+ux*a*s+vx*b*t,Y=y+uy*a*s+vy*b*t;
  P.push(X,0,Y);UV.push(i/nu,j/nv)}
 for(let j=0;j<nv;j++)for(let i=0;i<nu;i++){const q=j*(nu+1)+i;I.push(q,q+1,q+nu+1,q+1,q+nu+2,q+nu+1)}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(P,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(UV,2));g.setIndex(I);
 const m=new THREE.Mesh(g,mat);m.frustumCulled=false;m.renderOrder=2;m.castShadow=m.receiveShadow=false;lsuAltura(m);return m}
// alturas del suelo: los arcos se crean al empezar la misión, a veces antes de que esté cargado el suelo de esa calle
// (entonces groundY da la altura del mapa, más baja, y la luz quedaría enterrada). Se vuelve a medir al tocarle y al encenderse.
function lsuAltura(m){const p=m.geometry.attributes.position;for(let k=0;k<p.count;k++){const X=p.getX(k),Y=p.getZ(k);let h;try{h=groundY(X,Y)}catch(e){h=groundMap(X,Y)}p.setY(k,h+.0025)}p.needsUpdate=true}
// arco: se cuelga de su grupo, así se va con él
function luzSuelo(a){const mat=lsuMat('arco',0xffb84d),A=a.w+.045,B=.16;mat.color.multiplyScalar(1.45);
 a.suelo=lsuLamina(a.x,a.y,-a.ty,a.tx,A,B,window.LITE?6:10,window.LITE?3:4,mat);a.g.add(a.suelo)}
// muñecos, regalo y árbol: al encenderse
function luzSueloEsp(a){if(a.suelo)return;const arb=a.tipo==='arbol',r=arb?.85:a.tipo==='regalo'?.34:.3;
 const mat=lsuMat('esp',arb?0xa9d4ff:a.tipo==='regalo'?0xffc46a:0xffe2a8),m=lsuLamina(a.x,a.y,1,0,r,r,window.LITE?6:10,window.LITE?6:10,mat);
 scene.add(m);a.suelo=m;LSU.esp.push(a)}
function luzSueloEspFin(){for(const a of LSU.esp){if(a.suelo){scene.remove(a.suelo);a.suelo.geometry.dispose();a.suelo.material.dispose();a.suelo=null}}LSU.esp=[]}
function luzSueloTick(dt){const ob=LUZ.noche?1:0;LSU.k+=(ob-LSU.k)*Math.min(1,dt*(ob?1.5:.6));const K=LSU.k,T=LUZ.t||0;
 for(const a of LUZ.arcos){const s=a.suelo;if(!s)continue;let v;
  const est=a.lit?2:(a.vAct||0)>0?1:0;if(est>(s.userData.med||0)){s.userData.med=est;lsuAltura(s)}
  if(a.lit){const on=Math.min(1,Math.max(0,a.t*2.2-.15)/1.1);v=on*(.9+.1*Math.sin(T*3+a.x*7))*(1+.6*Math.max(0,1-a.t*.9))}
  else v=(a.vAct||0)*.45;
  const o=Math.min(1.3,v)*K;s.material.opacity=o;s.visible=o>.003}
 for(const a of LSU.esp){const s=a.suelo;if(!s)continue;let v=Math.min(1,(a.t||0)*1.2);
  if(a.tipo==='arbol')v=CINE.on?(CINE.star?1.25+.15*Math.sin(T*4):Math.min(1,Math.max(0,(CINE.t-.6)/4.2))*.9):1.1+.1*Math.sin(T*2.3);
  const o=v*K*.8;s.material.opacity=o;s.visible=o>.003}}
