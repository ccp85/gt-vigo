import re
f='index.html';s=open(f).read()
def rx(pat,b):
    global s
    m=list(re.finditer(pat,s,re.S));assert len(m)==1,(len(m),pat[:60]);s=s[:m[0].start()]+b+s[m[0].end():]
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
rx(r"function repCalleCerca\(x,y\)\{.*?\n","""function repCalleCerca(x,y){let bn='',bd=1e9;for(let i=-1;i<=1;i++)for(let j=-1;j<=1;j++)for(const[ax,ay,bx,by,k]of CGRID.get((Math.floor(x)+i)+','+(Math.floor(y)+j))||[]){const vx=bx-ax,vy=by-ay,L2=vx*vx+vy*vy||1e-9;let t=((x-ax)*vx+(y-ay)*vy)/L2;t=Math.max(0,Math.min(1,t));const d=Math.hypot(ax+vx*t-x,ay+vy*t-y);if(d<bd){bd=d;bn=CALLES[k][0]}}return bn||'Vigo'}
// mallas de edificios cargadas que cubren un punto; les crea el árbol de colisión si aún no lo tienen
function repMallas(x,y){const out=[],nuevas=[];const caja=o=>{if(!o.userData.bbw){if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();o.userData.bbw=o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld)}const b=o.userData.bbw;return x>=b.min.x&&x<=b.max.x&&y>=b.min.z&&y<=b.max.z};
 for(const o of window.OBST||[])if(!o.userData.suelo&&caja(o))out.push(o);
 for(let i=BVHQ.length-1;i>=0;i--){const o=BVHQ[i];if(o.userData.suelo)continue;let rr=o;while(rr.parent)rr=rr.parent;if(rr!==scene||!caja(o))continue;try{o.geometry.computeBoundsTree()}catch(e){}nuevas.push(o);out.push(o);BVHQ.splice(i,1)}
 if(nuevas.length)window.OBST=(window.OBST||[]).concat(nuevas);return out}
function repAltura(x,y,ms){RCH.set(new THREE.Vector3(x,8,y),ABAJO);RCH.far=10;const h=RCH.intersectObjects(ms,false)[0];return h?h.point.y:-1}
""")
rx(r"// tejado plano de un edificio a media distancia.*?\n(?=// chimenea)","""// tejado plano de un edificio en cualquier parte de Vigo, entre 300 y 700 m de donde estás (en zonas ya cargadas)
function repTejado(){const x0=P.x,y0=P.y;
 for(let t=0;t<600;t++){const a=Math.random()*6.283,rr=REP_HMIN+Math.random()*(REP_HMAX-REP_HMIN),x=x0+Math.cos(a)*rr,y=y0+Math.sin(a)*rr;
  if(cell(x,y).t!==3||REP.ult.some(u=>Math.hypot(u[0]-x,u[1]-y)<1))continue;if(!ZMETA.zonas.some(z=>typeof ZEST[z.id]==='object'&&zonaDist(z,x,y)<.01))continue;
  const ms=repMallas(x,y);if(!ms.length)continue;const h=repAltura(x,y,ms);if(h<0||h-groundY(x,y)<.12)continue;
  let ok=true;for(const[dx,dy]of[[.09,0],[-.09,0],[0,.09],[0,-.09],[.06,.06],[-.06,-.06]]){if(Math.abs(repAltura(x+dx,y+dy,ms)-h)>.012){ok=false;break}}if(!ok)continue;
  return[repCalleCerca(x,y),+x.toFixed(3),+y.toFixed(3),h]}return null}
""")
r("const REP_C1=[91,18.5,2.8],REP_C2=[95.5,19.3,7.6],REP_MIN=2.8,REP_MAX=7;","const REP_C1=[91,18.5,2.8],REP_C2=[95.5,19.3,7.6],REP_MIN=2.8,REP_MAX=7,REP_HMIN=4.3,REP_HMAX=10;")
r("function repSiguiente(){if(REP.heli){repBVH();const d=repTejado();","function repSiguiente(){if(REP.heli){const d=repTejado();")
r("(s.veh?' · aterriza en los tejados junto a la chimenea':'')","(s.veh?' · vuela por todo Vigo y aterriza junto a las chimeneas':'')")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok heli2')
