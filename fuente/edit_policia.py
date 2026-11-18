f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= COCHE PATRULLA (modelo aportado por el usuario: coche_policia_vigo.js) =================
r("moto:{p:2,col:[0x15171c,0xd51f1f,0x1f6fd0,0xf2f2ee,0x2fa84f]}};","moto:{p:2,col:[0x15171c,0xd51f1f,0x1f6fd0,0xf2f2ee,0x2fa84f]},policia:{p:1,col:[0xf4f4f4]}};")
r("furgoneta:'furgoneta',moto:'moto'};","furgoneta:'furgoneta',moto:'moto',policia:'coche de policía'};")
r(" else if(tipo==='descapotable'){",r""" else if(tipo==='policia'){polVigo(g,pint,{VID,FARO,PILO,CROM,NEG});g.add(manchaSombra(.06,.11))}
 else if(tipo==='descapotable'){""")
r("if(m.material.userData.faro)FAROMATS.add(m.material);","if(m.material.userData.faro)FAROMATS.add(m.material);if(m.material.userData.sirena!=null)SIRMATS.add(m.material);")
r("function vestirCoche(src,tipo){",r"""// luces del techo del coche patrulla: dos grupos que se alternan
const SIRMATS=new Set();{let f=0;setInterval(()=>{f^=1;for(const m of SIRMATS)m.emissiveIntensity=(m.userData.sirena===f)?3.2:.15},140)}
// modelo low-poly del coche patrulla (4.5 m a lo largo de +Z en el original): se construye a escala real y se aplana en mallas sueltas,
// con el frente hacia +X y unos 0.105 de largo como el resto de coches del tráfico
function polVigo(g,pint,K){const R=new THREE.Group();
 const C=(c,mt=.1,ro=.6)=>MV(c,ro,mt);
 const mB=pint,mAO=C(0x0b2a4a,.1,.55),mAM=C(0x1a4d8c,.1,.5),mAC=C(0x3a7bc8,.15,.45),mN=C(0x1a1a1a,.2,.7),mGO=C(0x2a2a2a,.15,.65),mPl=K.CROM,mCr=K.VID,mR=K.PILO,mAm=K.FARO,mNM=C(0x111111,.05,.9);
 const sir=k=>{const m=new THREE.MeshStandardMaterial({color:k?0x2a7bff:0x29b6f6,emissive:k?0x2a6bff:0x2fc4ff,emissiveIntensity:1,roughness:.2,metalness:.2});m.userData.sirena=k;SIRMATS.add(m);return m};const mL0=sir(0),mL1=sir(1);
 const LARGO=4.5,ANCHO=1.82,AR=.32,RR=.34;
 const box=(w,h,d,mat,x,y,z,rx=0,nom)=>{const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);m.rotation.x=rx;if(nom)m.name=nom;R.add(m);return m};
 box(ANCHO,.48,LARGO*.92,mB,0,AR+.18,0,0,'carroceria');
 box(ANCHO+.04,.18,LARGO*.94,mAO,0,AR+.02,0);
 box(ANCHO*.92,.62,LARGO*.55,mB,0,AR+.72,-.15,0,'carroceria');
 box(ANCHO*.88,.08,LARGO*.48,mB,0,AR+1.05,-.12,0,'carroceria');
 box(ANCHO*.95,.12,LARGO*.28,mB,0,AR+.52,LARGO*.32,-.08,'carroceria');
 box(ANCHO*.96,.55,LARGO*.22,mAO,0,AR+.42,-LARGO*.38);
 box(ANCHO*.85,.42,.06,mCr,0,AR+.82,LARGO*.12,-.35);
 box(ANCHO*.82,.38,.06,mCr,0,AR+.78,-LARGO*.28,.25);
 for(const sx of[-1,1]){box(.06,.38,LARGO*.38,mCr,sx*ANCHO*.46,AR+.78,-.08);box(.08,.42,LARGO*.62,mAO,sx*ANCHO*.48,AR+.38,.05);
  const t=.18;for(const[z,y,m]of[[.35,.55,mAC],[.35+t,.55,mB],[.35,.55+t,mB],[.35+t,.55+t,mAC],[.75,.55,mB],[.75+t,.55,mAC],[.75,.55+t,mAC],[.75+t,.55+t,mB]])box(.05,t,t,m,sx*ANCHO*.49,AR+y,z);
  box(.12,.08,.18,mN,sx*ANCHO*.52,AR+.72,LARGO*.08);box(.18,.22,.04,mAM,sx*ANCHO*.47,AR+.48,.55);
  box(.22,.1,.08,mAm,sx*.55,AR+.42,LARGO*.455);box(.08,.04,.04,sx<0?mL0:mL1,sx*.35,AR+.38,LARGO*.46);box(.2,.12,.06,mR,sx*.62,AR+.48,-LARGO*.455)}
 box(ANCHO*.55,.08,.22,mN,0,AR+1.12,-.05);box(.16,.06,.1,mL0,-.18,AR+1.14,-.05);box(.16,.06,.1,mL1,.18,AR+1.14,-.05);
 box(ANCHO+.06,.16,.12,mGO,0,AR+.12,LARGO*.46);box(ANCHO+.06,.16,.1,mGO,0,AR+.12,-LARGO*.46);
 box(.45,.22,.03,mB,0,AR+.78,-LARGO*.42);
 const cil=(r_,h,mat,x,z,seg)=>{const m=new THREE.Mesh(new THREE.CylinderGeometry(r_,r_,h,seg),mat);m.rotation.z=Math.PI/2;m.position.set(x,RR,z);R.add(m)};
 for(const z of[LARGO*.32,-LARGO*.3])for(const sx of[-1,1]){const x=sx*ANCHO*.42;cil(RR,.22,mNM,x,z,16);cil(RR*.62,.24,mPl,x,z,12);cil(RR*.22,.26,mGO,x,z,8)}
 // a escala del juego y girado para que el frente mire a +X; se hornea la transformación en cada malla
 const S=.105/LARGO;R.scale.setScalar(S);R.rotation.y=Math.PI/2;R.updateMatrixWorld(true);
 for(const m of [...R.children]){const q=new THREE.Mesh(m.geometry.clone().applyMatrix4(m.matrixWorld),m.material);q.name=m.name;g.add(q)}}
function vestirCoche(src,tipo){""")
open(f,'w').write(s)
print('ok policia')
