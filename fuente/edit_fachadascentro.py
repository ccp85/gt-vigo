f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= FACHADAS Y BAJOS DEL CENTRO (Porta do Sol, Príncipe, Policarpo Sanz, Colón, Alameda) =================
# Como en las fotos del centro de Vigo: edificios de sillería de granito con bajos comerciales enmarcados en piedra.
#  - bajos: pilastras de granito entre escaparates, zócalo oscuro, dintel corrido encima de los rótulos
#  - portales de madera con montante de cristal, persianas metálicas a medio bajar y banderolas
#  - cantoneras de granito en las esquinas de cada fachada e imposta entre bajo y primera planta
#  - dinteles de piedra sobre las ventanas que no tienen mirador
# las fachadas de Príncipe, Policarpo Sanz y Colón se quedaban sin tratar: están en la pieza 'puerto' de la maqueta, y solo se
# procesaba la pieza 'centro', una sola vez, al llegar
# sus primeros edificios, y los que se cargaban después nunca recibían bajos ni miradores. Ahora se repasa cada vez que llega algo
# (y cada edificio se trata una sola vez, cuando ya hay suelo debajo: sin suelo no se sabe hacia dónde da la fachada)
r("if(rt.parent&&rt.name==='centro'&&!rt.userData.fachC){rt.userData.fachC=1;setTimeout(()=>{try{centroFachadas(rt)}",
  "if(rt.parent&&!rt.userData.fachP){rt.userData.fachP=1;setTimeout(()=>{rt.userData.fachP=0;try{centroFachadas(rt)}")
r("rt.traverse(o=>{if(!o.isMesh||o.isInstancedMesh)return;const m=o.material;if(Array.isArray(m)||!m||!m.userData.real)return;const g=o.geometry,pos=g.attributes.position,ix=g.index;if(!ix)return;",
  "rt.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||o.userData.fachH)return;const m=o.material;if(Array.isArray(m)||!m||!m.userData.real)return;const g=o.geometry,pos=g.attributes.position,ix=g.index;if(!ix)return;o.updateMatrixWorld(true);if(!g.boundingSphere)g.computeBoundingSphere();{const cc=g.boundingSphere.center.clone().applyMatrix4(o.matrixWorld),rr=g.boundingSphere.radius*o.matrixWorld.getMaxScaleOnAxis();if(!ZONAS_C.some(Z=>cc.x+rr>Z[0]&&cc.x-rr<Z[2]&&cc.z+rr>Z[1]&&cc.z-rr<Z[3])){o.userData.fachH=1;return}if(sueloRap(cc.x,cc.z)==null)return}o.userData.fachH=1;")
# y el mapa de celdas es más grueso que los edificios: a ambos lados de muchas fachadas marcaba "edificio" y se descartaban.
# Ahora una fachada vale si da a calle en el mapa o si delante hay sitio libre de verdad (rayos contra los edificios)
r("if(!calle(cell(mx+nx*.025,my+ny*.025).t)){if(calle(cell(mx-nx*.025,my-ny*.025).t)){nx=-nx;ny=-ny}else continue}",
  "{const lib=(x,y)=>{const g=sueloRap(x,y);return g!=null&&repAltura(x,y,repMallas(x,y))<g+.012},fu=(sx)=>calle(cell(mx+nx*sx*.025,my+ny*sx*.025).t)||(lib(mx+nx*sx*.02,my+ny*sx*.02)&&lib(mx+nx*sx*.07,my+ny*sx*.07));if(!fu(1)){if(fu(-1)){nx=-nx;ny=-ny}else continue}}")
r("{const M0=fachMats();if(!M0.tam){","{const M0=fachMats();fachMats2(M0);if(!M0.tam){")
r("add('los',M.los,V.set(mid+nx*.006,z0+Math.max(.06,h-.004),midy+ny*.006),Q,S.set(Ln,.007,.013),null);",
  "add('los',M.los,V.set(mid+nx*.006,z0+Math.max(.06,h-.004),midy+ny*.006),Q,S.set(Ln,.007,.013),null);"
  "if(nf>=2){add('zoc',M.zoc,V.set(mid+nx*.003,z0+.003,midy+ny*.003),Q,S.set(Ln,.006,.008),null);add('pil',M.pil,V.set(mid+nx*.005,z0+.0905,midy+ny*.005),Q,S.set(Ln,.007,.012),null);"
  "if(Ln>.06)for(const e of[.006,Ln-.006])add('pil',M.pil,V.set(ax+ux*e+nx*.003,z0+h/2,ay+uy*e+ny*.003),Q,S.set(.012,h,.007),null)}")
r("if(nf>=2){add('esc',M.esc,P(.0025,.034),Q,S.set(BAY*.88,.058,.004),null);",
  "if(nf>=2){const hb=((b*31+sd*17)%11+11)%11;"
  "add('pil',M.pil,V.set(px-ux*BAY*.5+nx*.004,z0+.044,py-uy*BAY*.5+ny*.004),Q,S.set(BAY*.16,.088,.008),null);"
  "if(hb===0){add('por',M.por,P(.0025,.036),Q,S.set(BAY*.7,.062,.004),null);add('pil',M.pil,P(.0035,.004),Q,S.set(BAY*.8,.008,.01),null)}"
  "else{add('esc',M.esc,P(.0025,.034),Q,S.set(BAY*.84,.058,.004),null);if(hb<3)add('per',M.per,P(.0032,.063-(hb===1?.009:.017)),Q,S.set(BAY*.84,hb===1?.018:.034,.002),null)}"
  "if(hb===5){add('ban',M.ban,V.set(px+nx*.016,z0+.112,py+ny*.016),Q,S.set(.0018,.016,.022),c.set(ROT[((sd+b*3)%ROT.length+ROT.length)%ROT.length]).clone())}")
r("if(((b*7+f*3+sd)%5+5)%5<3){add('los',M.los,P(.007,y+.003)",
  "add('pil',M.pil,P(.003,y+.061),Q,S.set(BAY*.64,.0045,.005),null);if(((b*7+f*3+sd)%5+5)%5<3){add('los',M.los,P(.007,y+.003)")
r("function subePaso(){",r"""window.__fachG=()=>FACH;
// los edificios pasan a 'real' poco a poco después de cargar la zona: se repasa cada pocos segundos (cada edificio una sola vez)
setInterval(()=>{try{for(const z of ZROOTS){const rt=z.root;if(rt.parent)centroFachadas(rt)}}catch(e){console.warn('centroFachadas',e)}},4000);
function fachMats2(M){if(M.pil)return;const tx=(w,h,f)=>{const c=document.createElement('canvas');c.width=w;c.height=h;f(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=4;return t};
 let r2=11;const rr=()=>(r2=(r2*16807)%2147483647)/2147483647;
 // sillería de granito gris claro con juntas
 const graT=tx(64,64,(g,w,h)=>{g.fillStyle='#8f897f';g.fillRect(0,0,w,h);for(let j=0;j<4;j++)for(let i=0;i<2;i++){const v=178+((rr()*24)|0),o=(j%2)*16;g.fillStyle=`rgb(${v},${v-4},${v-12})`;g.fillRect((i*32+o)%64+1,j*16+1,30,14);if((i*32+o)%64+32>64)g.fillRect(0,j*16+1,((i*32+o)%64+32)-64-1,14);
  for(let k=0;k<40;k++){const q=v-35+((rr()*70)|0);g.fillStyle=`rgba(${q},${q},${q-5},.5)`;g.fillRect(rr()*64,j*16+1+rr()*14,1,1)}}});
 // portal de madera con montante de cristal y tirador
 const porT=tx(32,64,(g,w,h)=>{g.fillStyle='#4a2f1c';g.fillRect(0,0,w,h);g.fillStyle='#9fb6c8';g.fillRect(3,3,w-6,12);g.fillStyle='#4a2f1c';g.fillRect(w/2-1,3,2,12);
  g.fillStyle='#5d3b22';g.fillRect(3,18,w/2-4,h-21);g.fillRect(w/2+1,18,w/2-4,h-21);g.fillStyle='#3a2414';g.fillRect(6,22,w/2-10,18);g.fillRect(w/2+4,22,w/2-10,18);g.fillRect(6,44,w/2-10,15);g.fillRect(w/2+4,44,w/2-10,15);g.fillStyle='#c9a24a';g.fillRect(w/2-3,40,2,4);g.fillRect(w/2+1,40,2,4)});
 // persiana metálica enrollable
 const perT=tx(16,64,(g,w,h)=>{g.fillStyle='#a3a7ab';g.fillRect(0,0,w,h);for(let y=0;y<h;y+=4){g.fillStyle='#7d8287';g.fillRect(0,y,w,1);g.fillStyle='#c4c8cb';g.fillRect(0,y+1,w,1)}g.fillStyle='#55595e';g.fillRect(0,h-3,w,3)});
 M.pil=new THREE.MeshStandardMaterial({map:graT,roughness:.9});M.zoc=new THREE.MeshStandardMaterial({color:0x5c5a57,roughness:.8});
 M.por=new THREE.MeshStandardMaterial({map:porT,roughness:.6});M.per=new THREE.MeshStandardMaterial({map:perT,roughness:.45,metalness:.5});M.ban=new THREE.MeshStandardMaterial({roughness:.5})}
function subePaso(){""")
open(f,'w').write(s)
print('ok fachadascentro')
