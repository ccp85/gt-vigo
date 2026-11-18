import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= MÁS ADORNOS DE NAVIDAD (diseños propios, genéricos) =================
# · Papá Noeles gigantes colgados de la fachada con su escala de cuerda (Príncipe, Policarpo Sanz, Urzaiz, Colón).
# · Renos dorados (estatuas macizas) en Príncipe y Policarpo Sanz.
# · Casetas de Papá Noel de madera con tejado nevado en las aceras de Policarpo Sanz.
# · Muñecos de nieve a lo largo de Príncipe.
# Cada figura se funde en una malla por material para no cargar el móvil.
r("  // bola de cristal con un oso polar dentro (Príncipe)",r"""  {const OCU=[],ocu=(p,d)=>{if(OCU.some(q=>Math.hypot(q[0]-p[0],q[1]-p[1])<d))return true;OCU.push(p);return false};
   const fus=g=>{g.updateMatrixWorld(true);const inv=new THREE.Matrix4().copy(g.matrixWorld).invert(),by=new Map();g.traverse(o=>{if(!o.isMesh)return;let ge=o.geometry.clone().applyMatrix4(new THREE.Matrix4().multiplyMatrices(inv,o.matrixWorld));if(ge.index)ge=ge.toNonIndexed();for(const k of Object.keys(ge.attributes))if(!['position','normal','uv'].includes(k))ge.deleteAttribute(k);if(!by.has(o.material))by.set(o.material,[]);by.get(o.material).push(ge)});
    while(g.children.length)g.remove(g.children[0]);for(const[m,L]of by){const mg=mergeGeometries(L);if(mg){const o=new THREE.Mesh(mg,m);o.castShadow=true;o.receiveShadow=true;g.add(o)}}};
   const SM=(c,r_=.6,mt=0,e=0,ec)=>new THREE.MeshStandardMaterial({color:c,roughness:r_,metalness:mt,emissive:ec||c,emissiveIntensity:e});
   const ROJO=SM(0xc4161f,.55,0,.12),BLA=SM(0xf6f4ee,.85,0,.1),NEGRO=SM(0x161414,.45),PIEL=SM(0xf0c8a8,.7),DOR=SM(0xe9b73a,.22,1,.35,0x7a5200),CAR=SM(0x2a2522,.6),
    NAR=SM(0xf07a1a,.6),MAD=SM(0x8a5a32,.8),MAD2=SM(0x6b4426,.85),TEJ=SM(0xb3241f,.6),NIE=SM(0xffffff,.9,0,.25),VERD=SM(0x1f6a3a,.7),CUE=SM(0xb08a52,.9);
   const cil=(r1,r2,h,sg=10)=>new THREE.CylinderGeometry(r1,r2,h,sg),esf=(r_,a=12,b=9)=>new THREE.SphereGeometry(r_,a,b);
   // --- reno dorado macizo (mira hacia +x)
   const renoOro=(p,rot)=>{const g=G(p,rot);add(g,cil(.05,.054,.012,24),SM(0x8a1a22,.5),0,.006,0);add(g,cil(.054,.054,.003,24),DOR,0,.0135,0);
    add(g,esf(.034),DOR,0,.085,0).scale.set(1.75,.95,.9);add(g,esf(.028),DOR,.04,.092,0).scale.set(1,1.05,.95);
    add(g,cil(.012,.018,.06),DOR,.06,.125,0,0,0,-.55);add(g,esf(.017),DOR,.082,.157,0).scale.set(1.35,.95,.85);add(g,cil(.007,.011,.024),DOR,.1,.152,0,0,0,Math.PI/2+.25);
    add(g,esf(.005),SM(0x8a1a1a,.4),.112,.151,0);for(const s_ of[1,-1]){add(g,esf(.006),DOR,.076,.173,s_*.014).scale.set(.6,1,1.7);add(g,esf(.0035),NEGRO,.092,.163,s_*.01);
     const a1=add(g,cil(.0026,.0034,.05,6),DOR,.075,.195,s_*.01,s_*.35,0,.3);add(g,cil(.002,.0026,.022,6),DOR,.088,.21,s_*.022,s_*.7,0,-.6);add(g,cil(.002,.0026,.022,6),DOR,.066,.214,s_*.026,s_*.9,0,.7);add(g,cil(.0018,.0022,.018,6),DOR,.078,.224,s_*.02,s_*.3,0,-.2)}
    for(const[x,z,fl]of[[.035,.016,1],[.035,-.016,0],[-.04,.016,0],[-.04,-.016,1]]){const pv=new THREE.Group();pv.position.set(x,.075,z);pv.rotation.z=fl&&x>0?.35:0;g.add(pv);add(pv,cil(.0075,.005,.06,8),DOR,0,-.03,0);add(pv,cil(.006,.0065,.008,8),NEGRO,0,-.062,0)}
    add(g,esf(.008),DOR,-.062,.098,0).scale.set(1,.7,.7);add(g,new THREE.TorusGeometry(.03,.005,6,18),SM(0xc4161f,.5,0,.3),.05,.11,0,0,Math.PI/2,.5);fus(g);halo(p[0],groundMap(p[0],p[1])+.16,p[1],0xffd27a,.18)};
   // --- muñeco de nieve con bufanda, sombrero, zanahoria y brazos de rama
   const muneco=(p,rot)=>{const g=G(p,rot);add(g,esf(.042,14,10),NIE,0,.04,0);add(g,esf(.031,14,10),NIE,0,.1,0);add(g,esf(.022,14,10),NIE,0,.145,0);
    add(g,cil(.017,.017,.004,14),NEGRO,0,.165,0);add(g,cil(.012,.013,.028,14),NEGRO,0,.18,0);add(g,cil(.0125,.0125,.005,14),ROJO,0,.17,0);
    add(g,new THREE.ConeGeometry(.0045,.03,8),NAR,.032,.145,0,0,0,-Math.PI/2);for(const s_ of[1,-1])add(g,esf(.0035),NEGRO,.018,.153,s_*.008);for(const y of[.092,.108,.124])add(g,esf(.0035),NEGRO,.03,y-.012,0);
    add(g,new THREE.TorusGeometry(.021,.0055,6,16),ROJO,0,.128,0,Math.PI/2,0,0);add(g,new THREE.BoxGeometry(.008,.03,.012),ROJO,.012,.112,.016,0,0,.2);
    for(const s_ of[1,-1]){add(g,cil(.0022,.0022,.05,5),MAD2,0,.115,s_*.045,s_*.9,0,0);add(g,cil(.0016,.0016,.014,5),MAD2,0,.13,s_*.064,s_*.2,0,0)}fus(g)};
   // --- caseta de Papá Noel: madera, tejado de teja roja nevado, mostrador, cartel y Papá Noel dentro (mira hacia +x)
   const cv=document.createElement('canvas');cv.width=256;cv.height=64;{const c=cv.getContext('2d');c.fillStyle='#7a1018';c.fillRect(0,0,256,64);c.strokeStyle='#f5c84a';c.lineWidth=5;c.strokeRect(4,4,248,56);c.fillStyle='#fff6dc';c.font='bold 30px Georgia,serif';c.textAlign='center';c.textBaseline='middle';c.fillText('Papá Noel',128,34)}
   const tCart=new THREE.CanvasTexture(cv);tCart.colorSpace=THREE.SRGBColorSpace;const CART=new THREE.MeshStandardMaterial({map:tCart,roughness:.6,emissive:0xffffff,emissiveMap:tCart,emissiveIntensity:.35});
   const caseta=(p,rot)=>{const g=G(p,rot);add(g,new THREE.BoxGeometry(.07,.006,.09),MAD2,0,.003,0);
    add(g,new THREE.BoxGeometry(.06,.075,.006),MAD,-.003,.043,.042);add(g,new THREE.BoxGeometry(.06,.075,.006),MAD,-.003,.043,-.042);add(g,new THREE.BoxGeometry(.006,.075,.09),MAD,-.03,.043,0);
    add(g,new THREE.BoxGeometry(.012,.03,.09),MAD2,.027,.018,0);add(g,new THREE.BoxGeometry(.02,.004,.094),MAD,.03,.035,0);for(const z of[.043,-.043])add(g,new THREE.BoxGeometry(.006,.075,.006),MAD2,.03,.043,z);
    for(const s_ of[1,-1]){add(g,new THREE.BoxGeometry(.05,.004,.104),TEJ,s_*.019,.095,0,0,0,-s_*.62);add(g,new THREE.BoxGeometry(.046,.003,.104),NIE,s_*.0205,.0975,0,0,0,-s_*.62)}
    add(g,new THREE.BoxGeometry(.06,.042,.006),MAD,-.003,.098,.042).scale.set(1,1,1);add(g,new THREE.BoxGeometry(.06,.042,.006),MAD,-.003,.098,-.042);
    const ca=add(g,new THREE.PlaneGeometry(.06,.015),CART,.0335,.072,0,0,Math.PI/2,0);
    add(g,cil(.012,.015,.03,10),ROJO,-.005,.05,0);add(g,esf(.0095),PIEL,-.005,.073,0);add(g,esf(.0085),BLA,.0,.068,0).scale.set(.9,1.2,1.1);add(g,new THREE.ConeGeometry(.009,.022,10),ROJO,-.007,.09,0,0,0,.35);add(g,esf(.0035),BLA,-.012,.101,0);
    for(let k=0;k<4;k++)add(g,new THREE.BoxGeometry(.012,.012,.012),[ROJO,VERD,DOR,BLA][k],.03,.044,-.03+k*.02,0,k,0);fus(g);
    const z0=groundMap(p[0],p[1]),c=Math.cos(rot),sn=Math.sin(rot);for(let k=0;k<=10;k++){const lz=-.05+k*.01,lx=.045;luz(p[0]+c*lx+sn*lz,z0+.082,p[1]-sn*lx+c*lz,[0xffd98a,0xff4040,0x3fe07a][k%3],k,2.5,.008)}};
   // --- Papá Noel gigante colgado de una fachada con su escala de cuerda (de espaldas a la pared, mirando a la calle = +x)
   const nGig=(x,y,ang,zb)=>{const g=new THREE.Group();g.position.set(x,zb,y);g.rotation.y=ang;pon(g);
    for(const z of[.018,-.018])add(g,cil(.0018,.0018,.34,5),CUE,-.004,.0,z);for(let k=0;k<12;k++)add(g,new THREE.BoxGeometry(.004,.003,.04),MAD2,-.004,-.15+k*.028,0);
    add(g,cil(.026,.032,.07,12),ROJO,.02,-.02,0);add(g,cil(.033,.033,.01,12),NEGRO,.02,-.04,0);add(g,new THREE.BoxGeometry(.012,.012,.004),DOR,.052,-.04,0);add(g,cil(.034,.034,.008,12),BLA,.02,-.058,0);
    add(g,esf(.02),PIEL,.022,.032,0);add(g,esf(.021),BLA,.03,.022,0).scale.set(.8,1.25,1.15);add(g,esf(.005),SM(0xe07a6a,.6),.041,.035,0);for(const s_ of[1,-1])add(g,esf(.0028),NEGRO,.038,.041,s_*.008);
    add(g,new THREE.ConeGeometry(.02,.05,12),ROJO,.012,.062,0,0,0,.45);add(g,new THREE.TorusGeometry(.019,.005,6,14),BLA,.022,.047,0,Math.PI/2,0,0);add(g,esf(.008),BLA,-.008,.082,0);
    add(g,cil(.007,.0075,.06,8),ROJO,.012,.02,.03,-.25,0,0).position.set(.012,.035,.035);add(g,esf(.009),BLA,.006,.062,.04);add(g,esf(.009),SM(0x1a1a1a,.6),.004,.066,.04);
    add(g,cil(.007,.0075,.055,8),ROJO,.03,-.005,-.04,.9,0,.2);add(g,esf(.009),NEGRO,.04,-.02,-.06);
    for(const[z,rz]of[[.012,.3],[-.012,-.15]]){add(g,cil(.009,.008,.06,8),ROJO,.025,-.09,z,0,0,rz);add(g,new THREE.BoxGeometry(.026,.014,.014),NEGRO,.035,-.123,z)}
    add(g,esf(.022),SM(0x8a5a2b,.9),.005,-.005,0).scale.set(.6,1.2,1.1);fus(g)};
   const pies=(nombres,paso,fn)=>recorre(nombres,paso,fn);
   // renos dorados: Príncipe (a un lado) y Policarpo Sanz (en las aceras)
   let kq=0;pies(['Rúa do Príncipe'],1.15,(x,y,tx,ty,k)=>{const nx=-ty,ny=tx,sg=k%2?1:-1,p=sitio(x+nx*.09*sg,y+ny*.09*sg,.03);if(ocu(p,.09))return;renoOro(p,Math.atan2(-ty,tx)+(k%2?Math.PI:0))});
   pies(['Rúa Policarpo Sanz'],1.05,(x,y,tx,ty,k)=>{if(k%2)return;const nx=-ty,ny=tx,sg=(k>>1)%2?1:-1,o=borde(x,y,nx,ny,sg)+.05,p=sitio(x+nx*o*sg,y+ny*o*sg,.03);if(ocu(p,.1))return;renoOro(p,Math.atan2(-ty,tx)+((k>>1)%2?Math.PI:0))});
   // casetas de Papá Noel en Policarpo Sanz (en la acera, mirando a la calle)
   pies(['Rúa Policarpo Sanz'],1.05,(x,y,tx,ty,k)=>{if(!(k%2))return;const nx=-ty,ny=tx,sg=(k>>1)%2?-1:1,o=borde(x,y,nx,ny,sg)+.06,p=sitio(x+nx*o*sg,y+ny*o*sg,.045);if(ocu(p,.11))return;caseta(p,Math.atan2(ny*sg,-nx*sg))});
   // muñecos de nieve en Príncipe (al otro lado que los renos dorados)
   pies(['Rúa do Príncipe'],.95,(x,y,tx,ty,k)=>{const nx=-ty,ny=tx,sg=k%2?-1:1,p=sitio(x+nx*.1*sg,y+ny*.1*sg,.03);if(ocu(p,.09))return;muneco(p,Math.atan2(ny*sg,-nx*sg))});
   // Papá Noeles gigantes en fachadas: se busca la pared desde la calle y se cuelga a media altura
   {let kn=0;const PG=[];pies(['Rúa do Príncipe','Rúa Policarpo Sanz','Rúa de Urzáiz','Rúa de Urzaiz','Rúa Colón','Rúa García Barbón'],1.6,(x,y,tx,ty,k)=>{if(x<84||x>106||y<12||y>26||PG.some(q=>Math.hypot(q[0]-x,q[1]-y)<1.2))return;const nx=-ty,ny=tx,sg=k%2?1:-1;
     let d=0;while(d<.5&&cell(x+nx*sg*(d+.01),y+ny*sg*(d+.01)).t!==3)d+=.01;if(d>=.5)return;const wx=x+nx*sg*(d-.004),wy=y+ny*sg*(d-.004),z0=groundMap(wx,wy);
     PG.push([x,y]);nGig(wx,wy,Math.atan2(ny*sg,-nx*sg),z0+.27);kn++})}
  }
  // bola de cristal con un oso polar dentro (Príncipe)""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok adornos')
