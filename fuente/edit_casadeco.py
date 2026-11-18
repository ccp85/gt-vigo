import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= CASA DE LA MISIÓN DE SIGILO: MÁS DETALLE Y DECORACIÓN NAVIDEÑA =================
# Suelos de madera y baldosa, papel pintado, ventanas con la noche nevada, chimenea con repisa, troncos, calcetines
# y fuego que parpadea, guirnaldas con lucecitas en lo alto de las paredes, coronas, cuadros, estantería con libros,
# sillón, mesa de cocina, fogones y ollas, galletas y leche para Papá Noel, regalos bajo el árbol, plantas,
# alfombras, cama con manta navideña, nieve cayendo fuera y dos luces cálidas (chimenea y árbol).
r("const CASA_ARBOL=[1.6,.14],CASA_PUERTA=[.34,1.18];",
  "CASA_MUEB.push([.74,.07,.05,.16,.14,0x6b4426,1],[1.13,.47,.1,.09,.06,0x8a2a3a,0],[.5,1.1,.16,.05,.04,0x7a4a2a,0],[.8,.68,.16,.11,.05,0x9a6a44,0],[.38,.04,.12,.06,.06,0x8a5a32,0]);\nconst CASA_ARBOL=[1.6,.14],CASA_PUERTA=[.34,1.18];")
r(" box(0,0,.7,.55,.004,M(0x9a6a44,.7));box(0,.55,.7,.65,.004,M(0xb7845a,.7));box(.7,0,1.1,.6,.004,M(0xa8744a,.7));box(.7,.6,1.1,.6,.004,M(0xd9d6cc,.5));",
  r""" const TX=(w,h,fn,rx,ry)=>{const c=document.createElement('canvas');c.width=w;c.height=h;fn(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(rx,ry);return t};
 const MADERA=(rx,ry,c0)=>new THREE.MeshStandardMaterial({roughness:.6,map:TX(128,128,(x,w,h)=>{for(let i=0;i<8;i++){const v=Math.random()*24-12;x.fillStyle=`rgb(${c0[0]+v},${c0[1]+v*.8},${c0[2]+v*.6})`;x.fillRect(0,i*16,w,15);x.fillStyle='rgba(40,20,10,.35)';x.fillRect(0,i*16+15,w,1);x.fillRect((i*37)%w,i*16,1,16)}},rx,ry)});
 const BALD=new THREE.MeshStandardMaterial({roughness:.4,map:TX(64,64,(x)=>{for(let i=0;i<4;i++)for(let j=0;j<4;j++){x.fillStyle=(i+j)%2?'#e8e2d4':'#b9c6cf';x.fillRect(i*16,j*16,16,16)}},10,6)});
 box(0,0,.7,.55,.004,MADERA(4,4,[150,104,68]));box(0,.55,.7,.65,.004,MADERA(4,4,[170,122,80]));box(.7,0,1.1,.6,.004,MADERA(6,4,[160,110,70]));box(.7,.6,1.1,.6,.004,BALD);""")
r(" const MUR=M(0xf0e6d6,.85),ZOC=M(0x6b4426,.7);",
  " const MUR=new THREE.MeshStandardMaterial({roughness:.85,map:TX(64,64,(x,w,h)=>{x.fillStyle='#efe2cf';x.fillRect(0,0,w,h);for(let i=0;i<w;i+=16){x.fillStyle='#e3cfb4';x.fillRect(i,0,6,h)}x.fillStyle='#b8323a';for(let j=8;j<h;j+=32)for(let i=11;i<w;i+=16)x.fillRect(i,j,2,2)},6,2)}),ZOC=M(0x6b4426,.7);")
r(" // el protagonista\n C.fig=figNav(REP.spec||{t:'sleigh',col:[0xc4161f]});C.fig.scale.setScalar(.8);G.add(C.fig);",
  r""" // ---------- decoración navideña y detalles
 const D={};C.deco=D;const add=(geo,mat,x,y,z,ry=0)=>{const m=new THREE.Mesh(geo,mat);m.position.set(ox+x,b+y,oz+z);m.rotation.y=ry;m.castShadow=true;G.add(m);return m};
 const ROJO=M(0xc4161f,.6),VERDE=M(0x1f6a3a,.8),ORO=new THREE.MeshStandardMaterial({color:0xf5c84a,roughness:.3,metalness:.8}),BLANCO=M(0xf6f4ee,.9);
 // chimenea: repisa, ladrillo, troncos, fuego y calcetines
 box(1.715,.22,.06,.26,.012,M(0x5a3a1e,.6),.1);box(1.7,.31,.02,.08,.004,M(0x222222,.6));for(const z of[.31,.35])add(new THREE.CylinderGeometry(.008,.008,.06,8),M(0x5a3a22,.9),1.745,.012,z+.02,Math.PI/2).rotation.z=Math.PI/2;
 D.fuego=box(1.728,.3,.022,.1,.04,M(0xff8a2a,.4,2.6),.004);
 [[.26,0xc4161f],[.33,0x1f6a3a],[.4,0xc4161f]].forEach(([z,c])=>{box(1.7,z,.012,.022,.035,M(c,.7),.06);box(1.7,z-.002,.014,.026,.008,BLANCO,.095);box(1.692,z+.008,.012,.02,.01,M(c,.7),.058)});
 for(let k=0;k<9;k++)add(new THREE.SphereGeometry(.007,6,5),VERDE,1.71,.118,.23+k*.03);
 // guirnaldas con lucecitas en lo alto de las paredes
 {const P_=[];for(const w of CASA_MUROS){const lar=Math.max(w[2],w[3]);if(lar<.2)continue;const hor=w[2]>w[3];for(let t=.02;t<lar-.01;t+=.028){const x=hor?w[0]+t:w[0]+w[2]/2,z=hor?w[1]+w[3]/2:w[1]+t;P_.push([x,CASA_H-.004-Math.abs(Math.sin(t*22))*.012,z])}}
  const im=new THREE.InstancedMesh(new THREE.SphereGeometry(.0042,6,5),new THREE.MeshBasicMaterial({color:0xffffff,toneMapped:false}),P_.length),du=new THREE.Object3D(),cc=new THREE.Color(),COL=[0xff3b3b,0xffd24a,0x3fe07a,0x4aa8ff,0xff7ad0];
  P_.forEach((p,i)=>{du.position.set(ox+p[0],b+p[1],oz+p[2]);du.updateMatrix();im.setMatrixAt(i,du.matrix);im.setColorAt(i,cc.setHex(COL[i%COL.length]))});G.add(im);D.leds=im;D.ledCol=COL}
 // coronas de Navidad, cuadros y ventanas con la noche nevada
 for(const[x,z,ry]of[[.34,1.165,0],[.03,.3,Math.PI/2],[1.2,.03,0],[1.77,.85,Math.PI/2]]){const c=add(new THREE.TorusGeometry(.022,.008,8,18),VERDE,x,.1,z,ry);for(let k=0;k<6;k++){const a=k/6*6.283,bb=new THREE.Mesh(new THREE.SphereGeometry(.004,6,5),ROJO);bb.position.set(Math.cos(a)*.022,Math.sin(a)*.022,.007);c.add(bb)}const lz=new THREE.Mesh(new THREE.BoxGeometry(.016,.01,.004),ROJO);lz.position.set(0,-.022,.009);c.add(lz)}
 const VEN=M(0x9fc8ff,.2,.55),MARCO=BLANCO;for(const[x,z,w,d]of[[.15,-.002,.14,.034],[.45,-.002,.12,.034],[1.0,-.002,.16,.034],[1.42,-.002,.16,.034],[-.002,.2,.034,.12],[-.002,.85,.034,.12],[1.768,.72,.034,.14]]){box(x,z,w,d,.06,MARCO,.05);box(x+(w>d?.006:0),z+(w>d?0:.006),w>d?w-.012:d,w>d?d+.002:d-.012,.048,VEN,.056)}
 for(const[x,z,w,d,c]of[[.2,.528,.09,.006,0x3f6a8a],[.95,.575,.08,.006,0xc23f6a],[.025,.75,.006,.08,0x2fa84f],[1.25,.032,.08,.006,0xf2c230]])box(x,z,w,d,.05,M(c,.7),.07);
 // estantería con libros, sillón, banco, mesa de cocina con sillas, fogones con ollas, fregadero
 for(let q=0;q<3;q++)for(let k=0;k<5;k++)box(.745,.08+k*.03,.04,.024,.028,M([0xc4161f,0x2a4fa8,0xf2c230,0x1f6a3a,0x8a2a6a][(k+q)%5],.7),.02+q*.042);
 box(1.13,.47,.1,.02,.08,M(0x8a2a3a,.7));for(const[x,z]of[[.78,.74],[.98,.74]])box(x,z,.03,.03,.035,M(0x6b4426,.7));
 box(1.0,1.09,.16,.07,.004,M(0x222326,.4),.071);for(const x of[1.04,1.11])add(new THREE.CylinderGeometry(.012,.012,.02,12),M(0x9aa3ad,.3),x,.085,1.12);box(1.3,1.09,.1,.06,.004,M(0x8ea9bf,.2),.071);
 // galletas y leche para Papá Noel en la mesa del salón
 add(new THREE.CylinderGeometry(.022,.022,.003,16),BLANCO,1.4,.042,.37);add(new THREE.CylinderGeometry(.006,.006,.022,10),M(0xffffff,.2),1.39,.054,.355);for(let k=0;k<3;k++)add(new THREE.CylinderGeometry(.007,.007,.003,10),M(0xb07a3a,.8),1.405+Math.cos(k*2)*.01,.046,.375+Math.sin(k*2)*.01);
 // regalos de la familia bajo el árbol
 for(let k=0;k<6;k++){const a=k/6*6.283+.4,sz=.016+(k%3)*.005,x=CASA_ARBOL[0]+Math.cos(a)*.085,z=CASA_ARBOL[1]+Math.sin(a)*.085;if(z<.04)continue;box(x-sz/2,z-sz/2,sz,sz,sz,M([0xc4161f,0x2a4fa8,0xf2c230,0x1f6a3a,0xc23fd0,0xffffff][k],.5),.004);box(x-sz/2-.001,z-.002,sz+.002,.004,sz+.002,ORO,.004)}
 // alfombras, cama con manta navideña, plantas
 box(.2,.62,.12,.45,.002,M(0x2a4a6a,.9),.005);box(.08,.36,.2,.12,.002,M(0x6a2a3a,.9),.005);box(.06,.14,.24,.22,.012,ROJO,.05);for(let k=0;k<4;k++)box(.06,.15+k*.055,.24,.012,.013,BLANCO,.05);box(.1,.07,.07,.05,.015,M(0x1f6a3a,.8),.05);box(.2,.07,.07,.05,.015,M(0x1f6a3a,.8),.05);
 for(const[x,z]of[[.07,1.1],[1.72,.07],[.66,.07],[1.72,1.0]]){add(new THREE.CylinderGeometry(.014,.011,.025,10),M(0xb0603a,.8),x,.013,z);add(new THREE.SphereGeometry(.022,10,8),VERDE,x,.045,z)}
 // muérdago en la puerta del salón y estrella colgada
 add(new THREE.SphereGeometry(.01,8,6),VERDE,1.18,.13,.6);add(new THREE.SphereGeometry(.0035,6,5),M(0xffffff,.4,.6),1.18,.118,.6);
 // nieve cayendo fuera de la casa
 {const N=320,pos=new Float32Array(N*3);for(let k=0;k<N;k++){let x,z;do{x=-1+Math.random()*(CASA_W+2);z=-1+Math.random()*(CASA_D+2)}while(x>-.05&&x<CASA_W+.05&&z>-.05&&z<CASA_D+.05);pos.set([ox+x,b+Math.random()*.6,oz+z],k*3)}
  const ge=new THREE.BufferGeometry();ge.setAttribute('position',new THREE.BufferAttribute(pos,3));const pt=new THREE.Points(ge,new THREE.PointsMaterial({color:0xffffff,size:.008,transparent:true,opacity:.85,depthWrite:false}));pt.frustumCulled=false;G.add(pt);D.nieve=pt}
 // dos luces cálidas (se crean una vez y se quedan en la escena para no recompilar materiales)
 if(!CASM.luces){CASM.luces=[new THREE.PointLight(0xff9a40,0,.55,2),new THREE.PointLight(0xffd8a0,0,.45,2)];for(const l of CASM.luces)scene.add(l)}
 CASM.luces[0].position.set(ox+1.68,b+.08,oz+.35);CASM.luces[1].position.set(ox+CASA_ARBOL[0]-.05,b+.12,oz+CASA_ARBOL[1]+.06);
 // el protagonista
 C.fig=figNav(REP.spec||{t:'sleigh',col:[0xc4161f]});C.fig.scale.setScalar(.8);G.add(C.fig);""")
r("function updateCasa(dt){const C=CASM;if(!REP.on||!C.on){casaSale(false);return}",
  r"""function casaDecoTick(dt){const D=CASM.deco;if(!D)return;const t=performance.now()/1000;
 if(D.fuego){const f=.75+.25*Math.sin(t*17)*Math.sin(t*7.3);D.fuego.material.emissiveIntensity=2.2*f;if(CASM.luces)CASM.luces[0].intensity=.45*f}if(CASM.luces)CASM.luces[1].intensity=.3+.06*Math.sin(t*3);
 if(D.leds&&Math.random()<.35){const im=D.leds,cc=new THREE.Color();for(let q=0;q<6;q++){const i=Math.floor(Math.random()*im.count);im.setColorAt(i,cc.setHex(Math.random()<.25?0x222222:D.ledCol[Math.floor(Math.random()*D.ledCol.length)]))}im.instanceColor.needsUpdate=true}
 if(D.nieve){const a=D.nieve.geometry.attributes.position,y0=CASM.base;for(let k=0;k<a.count;k++){let y=a.getY(k)-dt*.07;if(y<y0)y=y0+.6;a.setY(k,y);a.setX(k,a.getX(k)+Math.sin(t+k)*.0003)}a.needsUpdate=true}}
function updateCasa(dt){const C=CASM;if(!REP.on||!C.on){casaSale(false);return}casaDecoTick(dt);""")
r("function casaSale(ok){const C=CASM;","function casaSale(ok){const C=CASM;if(C.luces)for(const l of C.luces)l.intensity=0;C.deco=null;")
r("bo=new THREE.Mesh(new THREE.SphereGeometry(.006,6,5),M(CB[k%5],.4,1.3))","bo=new THREE.Mesh(new THREE.SphereGeometry(.006,6,5),M(CB[k%5],.4,.6))")
r("const est=new THREE.Mesh(new THREE.OctahedronGeometry(.012),M(0xffe08a,.4,1.6))","const est=new THREE.Mesh(new THREE.OctahedronGeometry(.012),M(0xffe08a,.4,.8))")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok casadeco')
