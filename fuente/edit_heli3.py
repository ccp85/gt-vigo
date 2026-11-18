import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------- noche desde el principio también en helicóptero ----------
r("CIELO.modo='auto';CIELO.h=17.2;","CIELO.modo='auto';CIELO.h=20.8;")
r("if(!REP.heli&&REP.red)repLuz();","repLuz();")
# ---------- nombre de la calle por la que vas, siempre visible abajo ----------
r("if(MODO==='heli'){calleCand='';return}","if(MODO==='heli'&&!REP.on){calleCand='';return}")
r('<div id="nPop" hidden></div>','<div id="nPop" hidden></div><div id="nCalle" hidden></div>')
r("#nPop{position:fixed;","body.rep #calle{display:none!important}#nCalle{position:fixed;left:50%;bottom:calc(112px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:12;pointer-events:none;background:rgba(20,14,44,.78);color:#fff;font:700 15px var(--body);padding:6px 14px;border-radius:999px;box-shadow:0 0 0 1.5px #ffd24a inset;white-space:nowrap;max-width:calc(100vw - 40px);overflow:hidden;text-overflow:ellipsis}#nCalle[hidden]{display:none}\n#nPop{position:fixed;")
r(" const m=REP.marca;if(m&&m.visible){"," {const el=document.getElementById('nCalle'),tx=(REP.on&&calleAct)?'🛣 '+calleAct:'';if(el.textContent!==tx)el.textContent=tx;el.hidden=!tx}\n const m=REP.marca;if(m&&m.visible){")
r("document.getElementById('nFlecha').hidden=true;","document.getElementById('nFlecha').hidden=true;document.getElementById('nCalle').hidden=true;")
# ---------- helicóptero: monedas en el aire y aros de turbo camino de cada tejado ----------
r("const tgt=keys.up?1.6:keys.down?-.45:0;","const tgt=keys.up?1.6*(REP.on&&REP.boost>0?1.6:1):keys.down?-.45:0;")
r("function repSiguiente(){if(REP.heli){const d=repTejado();REP.dest=d;if(!d){REP.reint=1;repHud();return}","function repSiguiente(){if(REP.heli){const d=repTejado();REP.dest=d;if(!d){REP.reint=1;repHud();return}repAire(d);")
r("function repPila(){","""// monedas en arco y aros de turbo entre el helicóptero y el próximo tejado
function repAire(d){const A=REP.aire;if(A){for(const o of A.objs){scene.remove(o);const i=REP.objs.indexOf(o);if(i>=0)REP.objs.splice(i,1)}}
 const x0=P.x,y0=P.y,z0=Math.max(P.z,d[3]+.25),z1=d[3]+.3,du=new THREE.Object3D(),C=[],RG=[],L=Math.hypot(d[1]-x0,d[2]-y0);if(L<.6){REP.aire=null;return}
 const nC=Math.min(24,Math.round(L*3));for(let k=0;k<nC;k++){const t=.12+.7*k/(nC-1||1);const x=x0+(d[1]-x0)*t,y=y0+(d[2]-y0)*t;let z=z0+(z1-z0)*t+Math.sin(t*Math.PI)*.35+Math.sin(k*.8)*.04;const ms=repMallas(x,y),hr=ms.length?repAltura(x,y,ms):-1;z=Math.max(z,hr+.2,groundY(x,y)+.2);C.push({x,y,z,on:true})}
 for(const t of L>2?[.33,.62]:[.45]){const x=x0+(d[1]-x0)*t,y=y0+(d[2]-y0)*t,ms=repMallas(x,y),hr=ms.length?repAltura(x,y,ms):-1;RG.push({x,y,z:Math.max(z0+(z1-z0)*t+Math.sin(t*Math.PI)*.35,hr+.25,groundY(x,y)+.25),on:true,a:Math.atan2(d[2]-y0,d[1]-x0)})}
 const mc=new THREE.InstancedMesh(new THREE.CylinderGeometry(.03,.03,.008,18).rotateX(Math.PI/2),new THREE.MeshStandardMaterial({color:0xffc21f,emissive:0xb07800,emissiveIntensity:.9,metalness:.8,roughness:.25}),C.length);mc.frustumCulled=false;
 const objs=[mc];for(const g of RG){const m=new THREE.Mesh(new THREE.TorusGeometry(.13,.014,10,40),new THREE.MeshBasicMaterial({color:0x35e0ff,toneMapped:false,transparent:true,opacity:.9}));m.position.set(g.x,g.z,g.y);m.rotation.y=-g.a+Math.PI/2;g.m=m;objs.push(m)}
 for(const o of objs){scene.add(o);REP.objs.push(o)}REP.aire={C,RG,mc,du,objs}}
function repAireTick(dt){const A=REP.aire;if(!A)return;const t=NAV.uT.value,du=A.du;let ch=false;
 A.C.forEach((c,i)=>{if(c.on){const dd=Math.hypot(c.x-P.x,c.y-P.y,c.z-P.z-.03);if(dd<.22){const k_=Math.min(1,dt*9);c.x+=(P.x-c.x)*k_;c.y+=(P.y-c.y)*k_;c.z+=(P.z+.03-c.z)*k_}if(dd<.07){c.on=false;REP.mon=(REP.mon||0)+1;ch=true;if(!REP.sT||t-REP.sT>.07){REP.sT=t;try{sonMoneda()}catch(e){}}}}
  du.position.set(c.x,c.z,c.y);du.rotation.set(0,t*3+i*.4,0);du.scale.setScalar(c.on?1:1e-4);du.updateMatrix();A.mc.setMatrixAt(i,du.matrix)});A.mc.instanceMatrix.needsUpdate=true;
 for(const g of A.RG){g.m.material.opacity=g.on?.75+.25*Math.sin(t*6):.15;if(g.on&&Math.hypot(g.x-P.x,g.y-P.y,g.z-P.z-.02)<.15){g.on=false;REP.boost=1.6;ch=true;aviso('⚡ ¡TURBO!',.7,'peq');try{sonCaja()}catch(e){}}}
 if(REP.boost>0)REP.boost-=dt;if(ch)repHud()}
function repPila(){""")
r("if(!REP.heli&&!REP.fin&&REP.red){repArcadeTick(dt);","if(REP.heli&&!REP.fin)repAireTick(dt);\n if(!REP.heli&&!REP.fin&&REP.red){repArcadeTick(dt);")
r("+(REP.heli?'':`<span class=\"r\">🪙 ${REP.mon||0}</span>`)}","+`<span class=\"r\">🪙 ${REP.mon||0}</span>`}")
r("heliDesvestir();REP.heli=false;","heliDesvestir();REP.heli=false;REP.aire=null;")
r("REP.dest=null;REP.ult=[];REP.ent=0;REP.mon=0;","REP.dest=null;REP.ult=[];REP.ent=0;REP.mon=0;REP.aire=null;")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok heli3')
