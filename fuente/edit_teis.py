import json
f='index.html';s=open(f).read()
# barcos de los astilleros (de vigo_extras.json, 'cascos'): x, y, z, largo, manga, alto, ángulo
CAS='[[111.756, -4.16, -0.03, 1.4, 0.26, 0.13, -3.107], [112.278, -6.412, -0.03, 1.2, 0.24, 0.13, 0.947], [129.072, -13.976, -0.03, 1.0, 0.2, 0.13, 1.385], [126.632, -12.32, -0.03, 0.8, 0.18, 0.13, 1.74]]'
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= TEIS Y A GUÍA: ASTILLEROS Y ERMITA =================
# Google Earth solo como referencia. En los dos astilleros (Guixar y ensenada de Teis) los barcos del mapa pasan a estar
# "en construcción": gran pórtico grúa sobre el casco, andamios por los costados y superestructura a medio montar.
# En la cima del Monte da Guía, una ermita blanca genérica con espadaña y un mirador con barandilla, bancos y cruceiro.
r("function subeZonas(){psolChk();","function subeZonas(){psolChk();teisChk();")
r("function subePaso(){",r"""const TEIS={ast:new Set(),erm:0,CAS:"""+CAS+r"""};window.__TEIS=TEIS;
setInterval(()=>{teisChk()},3000);
function teisChk(){if(!MAPA||!MI)return;try{
 // astilleros: cada barco se monta cuando su zona está cargada (el suelo junto al casco existe)
 TEIS.CAS.forEach((c,i)=>{if(TEIS.ast.has(i))return;const[x,y]=c;let ok=false;for(let r_=.3;r_<=1.6&&!ok;r_+=.4)for(let a_=0;a_<6.28;a_+=.79)if(sueloRap(x+Math.cos(a_)*r_,y+Math.sin(a_)*r_)!=null){ok=true;break}if(!ok)return;TEIS.ast.add(i);setTimeout(()=>{try{astillero(c)}catch(e){console.warn('astillero',e);TEIS.err=String(e)}},400)});
 if(!TEIS.erm&&sueloRap(117,-9.2)!=null){TEIS.erm=1;setTimeout(()=>{try{ermidaGuia()}catch(e){console.warn('guia',e);TEIS.err2=String(e)}},700)}}catch(e){}}
function astillero([x,y,z,L,B,H,ang]){const LT=!!window.LITE,G=new THREE.Group();G.name='astillero';G.position.set(x,0,y);G.rotation.y=ang;
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.6},o));
 const AM=M(0xf2b630,{metalness:.3}),RO=M(0xc8382a,{metalness:.3}),GR=M(0x9aa0a8,{metalness:.5,roughness:.4}),IM=M(0x8a8f96,{roughness:.8}),MI_=M(0xa0452e,{roughness:.85}),AND=M(0xb8bcc2,{metalness:.6,roughness:.35}),LU=M(0xfff2cc,{emissive:0xffd88a,emissiveIntensity:.8});
 const P=new Map(),add=(w,h,d,m,px,py,pz,ry=0)=>{const g=new THREE.BoxGeometry(w,h,d);g.rotateY(ry);g.translate(px,py,pz);if(g.attributes.uv)g.deleteAttribute('uv');if(!P.has(m))P.set(m,[]);P.get(m).push(g)};
 const top=z+H*.5+.04;// cubierta aproximada del casco
 // 1) pórtico grúa (tipo Goliath) que cruza el barco por la mitad
 {const SP=B/2+.12,HH=Math.max(.55,top+.38),gx=-L*.08;
  for(const sd of[-1,1]){add(.03,HH+.06,.03,AM,gx-.06,HH/2-.03,sd*SP);add(.03,HH+.06,.03,AM,gx+.06,HH/2-.03,sd*SP);add(.16,.025,.035,AM,gx,-.02,sd*SP);add(.15,.012,.012,AM,gx,HH*.5,sd*SP)}
  add(.05,.05,SP*2+.08,RO,gx-.035,HH+.01,0);add(.05,.05,SP*2+.08,RO,gx+.035,HH+.01,0);add(.13,.012,SP*2+.08,AM,gx,HH+.04,0);
  add(.08,.035,.06,AM,gx,HH-.03,B*.15);add(.006,HH-.04-top-.03,.006,GR,gx,(HH-.04+top+.03)/2,B*.15);
  // letrero y luces en la viga
  for(const sd of[-1,1])add(.012,.008,.012,LU,gx,HH-.022,sd*SP*.6)}
 // 2) andamios por los dos costados
 {const sx=L/2-.08,n=Math.max(4,Math.round((L-.25)/.06));for(const sd of[-1,1]){const zz=sd*(B/2+.018);
   for(let k=0;k<=n;k++){const px=-sx+.12+k*(2*sx-.12)/n;add(.004,top+.07,.004,AND,px,(top+.07)/2-.03,zz)}
   for(let lv=0;lv<4;lv++){const hy=.0+lv*(top+.02)/3;add(2*sx-.12,.004,.004,AND,.06,hy,zz);add(2*sx-.12,.0025,.018,AM,.06,hy-.003,zz-sd*.006)}}}
 // 3) superestructura a medio montar hacia la popa (bloques de acero en imprimación)
 {const px=-L/2+.16;add(.2,.06,B*.8,IM,px,top+.03,0);add(.14,.05,B*.7,MI_,px-.02,top+.085,0);add(.07,.045,B*.5,IM,px-.04,top+.13,-B*.08);
  add(.05,.05,.05,MI_,-L*.05,top+.025,B*.2);add(.06,.04,.05,IM,L*.12,top+.02,-B*.18);add(.04,.13,.04,GR,px+.08,top+.1,B*.32)}
 for(const[m,gs]of P){const me=new THREE.Mesh(mergeGeometries(gs),m);me.castShadow=!LT&&m!==LU;me.receiveShadow=true;G.add(me)}
 scene.add(G)}
function ermidaGuia(){const LT=!!window.LITE,t=(x,y)=>cell(x,y).t,gy=(x,y)=>sueloRap(x,y);
 // sitio libre lo más alto posible cerca de la cima
 let best=null,bh=-9;for(let r=0;r<.55;r+=.03)for(let a=0;a<6.283;a+=.4){const x=117+Math.cos(a)*r,y=-9.2+Math.sin(a)*r;let ok=true;
  for(let u=-.13;u<=.13&&ok;u+=.04)for(let v=-.1;v<=.1;v+=.04){const c=t(x+u,y+v);if(c!==1){ok=false;break}}if(!ok)continue;const h=gy(x,y);if(h!=null&&h>bh){bh=h;best=[x,y]}}
 if(!best)return;TEIS.ermida=best;const[x,y]=best,z=bh;const G=new THREE.Group();G.position.set(x,z,y);G.name='ermidaGuia';
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.75},o));
 const BL=M(0xf4f2ea),PI_=M(0xbdb4a2,{roughness:.95}),TE=M(0xb5512f),HI=M(0x2a2d33,{metalness:.5,roughness:.45}),MA=M(0x7a5232),GR=M(0x9a9184,{roughness:1});
 const bx=(w,h,d,m,px,py,pz,ry=0)=>{const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(px,py,pz);o.rotation.y=ry;o.castShadow=!LT;o.receiveShadow=true;G.add(o);return o};
 // explanada de piedra
 {const g=new THREE.CylinderGeometry(.2,.21,.012,32);const o=new THREE.Mesh(g,PI_);o.position.y=.0;o.receiveShadow=true;G.add(o)}
 // nave con tejado a dos aguas, cabecera y pórtico
 bx(.13,.05,.07,BL,0,.03,0);
 {const sh=new THREE.Shape();sh.moveTo(-.04,0);sh.lineTo(0,.028);sh.lineTo(.04,0);sh.lineTo(-.04,0);const g=new THREE.ExtrudeGeometry(sh,{depth:.14,bevelEnabled:false});g.translate(0,0,-.07);g.rotateY(Math.PI/2);const o=new THREE.Mesh(g,TE);o.position.set(0,.055,0);o.castShadow=!LT;G.add(o)}
 bx(.03,.07,.05,BL,-.07,.04,0);// cabecera
 // espadaña en la fachada (oeste) con dos campanas
 bx(.012,.11,.06,BL,.072,.06,0);bx(.014,.012,.066,PI_,.072,.115,0);
 for(const s of[-1,1]){const c=new THREE.Mesh(new THREE.SphereGeometry(.0065,8,6,0,6.283,0,Math.PI*.6),M(0xa0742a,{metalness:.6,roughness:.35}));c.position.set(.072,.085,s*.014);c.rotation.x=Math.PI;G.add(c)}
 {const cr=new THREE.Group();cr.add(new THREE.Mesh(new THREE.BoxGeometry(.003,.02,.003),PI_));const b=new THREE.Mesh(new THREE.BoxGeometry(.003,.003,.012),PI_);b.position.y=.004;cr.add(b);cr.position.set(.072,.13,0);G.add(cr)}
 bx(.004,.03,.018,MA,.0785,.02,0);// puerta
 for(const s of[-1,1])bx(.06,.012,.004,M(0x30486b,{roughness:.3}),-.005,.04,s*.0352);// ventanas
 // cruceiro de piedra y bancos alrededor
 {const cx=.13,cz=.08;bx(.03,.012,.03,GR,cx,.006,cz);bx(.007,.07,.007,GR,cx,.045,cz);bx(.007,.007,.026,GR,cx,.07,cz)}
 for(let k=0;k<5;k++){const a=Math.PI*.6+k*.35,bx_=Math.cos(a)*.17,bz=Math.sin(a)*.17;bx(.03,.004,.009,MA,bx_,.01,bz,-a+Math.PI/2);bx(.03,.008,.002,MA,bx_+Math.cos(a)*.004,.015,bz+Math.sin(a)*.004,-a+Math.PI/2)}
 // barandilla del mirador en el borde norte de la explanada
 for(let k=0;k<=18;k++){const a=-Math.PI*.95+k/18*Math.PI*.9,px=Math.cos(a)*.195,pz=Math.sin(a)*.195;bx(.0018,.018,.0018,HI,px,.015,pz);if(k<18){const a2=a+Math.PI*.9/18,qx=Math.cos(a2)*.195,qz=Math.sin(a2)*.195;bx(Math.hypot(qx-px,qz-pz),.0018,.0018,HI,(px+qx)/2,.024,(pz+qz)/2,-Math.atan2(qz-pz,qx-px))}}
 scene.add(G)}
function subePaso(){""")
open(f,'w').write(s)
print('ok teis')
