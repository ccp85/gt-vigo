import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= ENCENDIDO DE LUCES: UNA RUTA FIJA Y FLUIDA =================
# Praza de España (arcos en la rotonda y muñecos de nieve en la isleta) → bajando por Gran Vía con muchos arcos
# seguidos → regalo gigante de Urzaiz con Gran Vía → Urzaiz → Colón → Policarpo Sanz → árbol de Porta do Sol.
# Arcos separados ~65 m y con menos brillo para que no deslumbren.
# muñecos de nieve en la isleta de la rotonda de Praza de España
r("   // renos dorados: Príncipe (a un lado) y Policarpo Sanz (en las aceras)",
  "   for(let k=0;k<4;k++){const a=k*1.571+.4;muneco([93.72+Math.cos(a)*.16,30.14+Math.sin(a)*.16],-a)}NAV.munP=NAV.munP.slice(0,-4);\n   // fuente de la isleta de Praza de España (diseño genérico: pilón de granito, tazas y chorros de agua)\n   {const fx=93.72,fy=30.14,g=G([fx,fy]),GR=SM(0xb9b6ad,.85),AG=new THREE.MeshStandardMaterial({color:0x5fb8e8,roughness:.1,metalness:.2,transparent:true,opacity:.8,emissive:0x1a5a8a,emissiveIntensity:.5});\n    add(g,cil(.1,.105,.025,28),GR,0,.0125,0);add(g,cil(.092,.092,.004,28),AG,0,.024,0);add(g,cil(.014,.018,.07,12),GR,0,.06,0);add(g,cil(.045,.03,.012,20),GR,0,.075,0);add(g,cil(.04,.04,.003,20),AG,0,.081,0);add(g,cil(.008,.01,.04,10),GR,0,.1,0);add(g,cil(.022,.016,.008,14),GR,0,.12,0);\n    const ch=new THREE.MeshBasicMaterial({color:0xcfefff,transparent:true,opacity:.55,depthWrite:false});add(g,new THREE.ConeGeometry(.01,.05,8,1,true),ch,0,.15,0);\n    for(let k=0;k<8;k++){const a=k/8*6.283,j=add(g,new THREE.CylinderGeometry(.002,.004,.06,6,1,true),ch,Math.cos(a)*.065,.05,Math.sin(a)*.065);j.rotation.set(Math.sin(a)*.5,0,-Math.cos(a)*.5)}\n    fus(g);halo(fx,groundMap(fx,fy)+.12,fy,0x9fd8ff,.1)}\n   // renos dorados: Príncipe (a un lado) y Policarpo Sanz (en las aceras)")
r("LUZ.ruta=ord.slice(0,2).map(luzArco).concat(lucesEspeciales());","LUZ.ruta=lucesRutaFija();")
r("_lc.setHex(LUZ_ON[i%4]).multiplyScalar(on?tw*1.25:0);","_lc.setHex(LUZ_ON[i%4]).multiplyScalar(on?tw*.95:0);")
r("a.lit=true;a.t=0;LUZ.flash=1;","a.lit=true;a.t=0;LUZ.flash=a.tipo?1:.35;")
r("function lucesInicio(m){",r"""function lucesRutaFija(){REP.rad=Math.max(REP.rad||0,14.5);const E=lucesEspeciales(),esp=t=>E.find(e=>e.tipo===t),L=[];
 // arco en un punto de una polilínea, cada 'paso' a partir de 'ini'
 const tramo=(pts,ini,paso,nom,max)=>{let acc=0,sig=ini,n=0;for(let i=1;i<pts.length&&n<(max||99);i++){const a=pts[i-1],b=pts[i],dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy);while(sig<=acc+l&&n<(max||99)){const t=(sig-acc)/l;L.push(luzArco([nom,a[0]+dx*t,a[1]+dy*t,dx/l,dy/l]));n++;sig+=paso}acc+=l}};
 // 1) rotonda de Praza de España: tres arcos siguiendo el giro y los muñecos de la isleta
 const C=[93.72,30.14],RR=.29,a0=Math.atan2(P.y-C[1],P.x-C[0]);for(let k=0;k<3;k++){const a=a0+.7+k*2.094,x=C[0]+Math.cos(a)*RR,y=C[1]+Math.sin(a)*RR;L.push(luzArco(['Praza de España',x,y,-Math.sin(a),Math.cos(a)]))}
 const mu=esp('munecos');if(mu){mu.x=C[0];mu.y=C[1];mu.w=.38;mu.nom='⛄ Muñecos de nieve · Praza de España';L.push(mu)}
 // 2) Gran Vía hacia arriba: muchos arcos seguidos
 LUZ.wMax=.07;tramo([[94.01,29.5],[94.36,28.73],[94.47,28.58],[94.68,28.12],[95.66,25.93],[96.12,24.85],[97.33,22.2]].map(p=>[p[0]+.035*.91,p[1]+.035*.41]),.35,.92,'Avenida da Gran Vía');LUZ.wMax=0;
 const re=esp('regalo');if(re){re.w=.45;L.push(re)}
 // 3) Urzaiz hacia el centro y 4) Colón
 tramo([[97.0,21.58],[96.49,21.43],[94.57,20.76],[93.64,20.41]],.45,.95,'Rúa de Urzaiz');
 tramo([[93.35,20.06],[93.27,19.92],[93.24,19.82],[93.13,18.4],[93.08,17.62]],.5,.95,'Rúa Colón',2);
 // 5) Policarpo Sanz hasta el árbol
 tramo([[93.08,17.62],[90.06,18.17],[89.88,18.19],[89.1,18.11],[88.4,17.99]],.45,.95,'Rúa Policarpo Sanz');
 L.push(esp('arbol'));return L}
function lucesInicio(m){""")
r("const w=Math.max(.04,Math.min(.13,luzAncho(x,y,nx,ny)-.008));","const w=Math.max(.04,Math.min(LUZ.wMax||.13,luzAncho(x,y,nx,ny)-.008));")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok rutaluces')
