f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= PROTAGONISTA NUEVO (modelo aportado por el usuario, Tripo: protagonista.glb) =================
# Solo mundo abierto (index.html): se aplica DESPUÉS de edit_skatetest.py, así nav/navm/gp no cambian.
# protagonista.glb viene de tools/obj2glb.py: girado para mirar a +X, altura 1, partido en 5 mallas
# (cuerpo, piernaA/B, brazoA/B; A = lado -Z). Cada pierna/brazo se mete en el pivote del muñeco antiguo,
# así la animación de andar, el piloto de la moto de agua, etc. siguen funcionando igual.
# Mientras carga (o si falla) se ve el muñeco antiguo.
r(" g.traverse(o=>{if(o.isMesh)o.castShadow=true});return g}\nfunction mkMoto",
  " g.traverse(o=>{if(o.isMesh)o.castShadow=true});g.userData.viejo=[];g.traverse(o=>{if(o.isMesh)g.userData.viejo.push(o)});PROTA.lista.push(g);protaPon(g);return g}\n"
  "const PROTA={lista:[],m:null,S:.08};window.PROTA=PROTA;\n"
  "function protaPon(g){const M=PROTA.m;if(!M||g.userData.prota)return;g.userData.prota=true;\n"
  " for(const o of g.userData.viejo)if(o.parent)o.parent.remove(o);\n"
  " const pon=(o,par,x,y,z)=>{const m=new THREE.Mesh(o.geometry,o.material);m.scale.setScalar(PROTA.S);m.position.set(x,y,z);m.castShadow=true;par.add(m)};\n"
  " pon(M.cuerpo,g,0,0,0);\n"
  " const pi=g.userData.piernas.children;pon(M.piernaA,pi[0],0,-.03,-pi[0].position.z);pon(M.piernaB,pi[1],0,-.03,-pi[1].position.z);\n"
  " const br=g.userData.brazos.children;for(const[k,n]of[[0,'brazoA'],[1,'brazoB']]){const b=br[k];pon(M[n],b,-b.position.x,-b.position.y,-b.position.z)}}\n"
  "new GLTFLoader().load('protagonista.glb',gl=>{const M={};gl.scene.traverse(o=>{if(o.isMesh){o.material.metalness=0;o.material.roughness=.7;M[o.name]=o}});\n"
  " if(!M.cuerpo||!M.piernaA||!M.brazoB)return;PROTA.m=M;PROTA.lista.forEach(protaPon)},undefined,e=>console.warn('protagonista.glb',e));\n"
  "function mkMoto")
open(f,'w').write(s)
print('ok protagonista')
