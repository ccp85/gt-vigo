f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= EDIFICIOS DEL CENTRO: TEJADOS COMO EN GOOGLE EARTH =================
# Porta do Sol, Príncipe, Policarpo Sanz, Colón y alrededor de la Alameda. En Google Earth casi todos los tejados
# son de teja roja a cuatro aguas, con algunas mansardas de pizarra y azoteas llenas de casetones y chimeneas.
#  - menos tejados de pizarra en esa zona (antes la mitad pasaba a pizarra; ahora uno de cada seis)
#  - chimeneas de granito con sombrerete y antenas sobre los tejados de teja
#  - en las azoteas planas: casetones de ascensor, máquinas de aire, depósitos de agua, claraboyas y antenas
r("const hh=Math.abs(Math.sin(V.x*71.3+V.z*193.1)*24634.6345)%1;if(hh<.5)tip.set(c,1)}",
  "const hh=Math.abs(Math.sin(V.x*71.3+V.z*193.1)*24634.6345)%1;if(hh<(enFocoT(V.x,V.z)?.17:.5))tip.set(c,1)}")
r("function subeZonas(){psolChk();","function subeZonas(){psolChk();tcChk();")
r("function subePaso(){",r"""const FOCO_T=[[85.8,14.2,95.2,21.6]];const enFocoT=(x,y)=>FOCO_T.some(Z=>x>Z[0]&&x<Z[2]&&y>Z[1]&&y<Z[3]);
const TC={hecha:0};window.__TC=TC;setInterval(()=>{if(!TC.hecha)tcChk()},3000);
function tcChk(){if(TC.hecha||!MAPA)return;for(const[x,y]of[[90,19.13],[87,19],[92.5,17.8]])if(sueloRap(x,y)==null)return;
 if(repAltura(90.08,19.6,repMallas(90.08,19.6))<0)return;TC.hecha=1;setTimeout(()=>{try{tcCrea()}catch(e){console.warn('tejados',e);TC.err=String(e)}},2500)}
function tcCrea(){const LT=!!window.LITE,G=new THREE.Group();G.name='tejados_centro';let rs=77;const rn=()=>(rs=(rs*16807)%2147483647)/2147483647;
 const top=(x,y)=>repAltura(x,y,repMallas(x,y)),gy=(x,y)=>sueloRap(x,y);
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.85},o));
 const GRA=M(0xb3aca1),GRO=M(0x8f8a82),BLA=M(0xe4e2dc),MET=M(0x9aa1a8,{metalness:.5,roughness:.45}),OSC=M(0x3b3f45,{metalness:.3,roughness:.5}),
  CRI=M(0x8fb3c9,{metalness:.3,roughness:.15}),TER=M(0xa5503a);
 const L=new Map(),add=(geo,mat,x,y,z,ry=0,sx=1,sy=1,sz=1)=>{if(!L.has(mat))L.set(mat,new Map());const m=L.get(mat);if(!m.has(geo))m.set(geo,[]);m.get(geo).push([x,y,z,ry,sx,sy,sz])};
 const B=new THREE.BoxGeometry(1,1,1),CY=new THREE.CylinderGeometry(.5,.5,1,10),PO=new THREE.CylinderGeometry(.5,.5,1,4);
 const tareas=[];const[X0,Y0,X1,Y1]=FOCO_T[0],PS=LT?.05:.034;
 for(let x=X0;x<X1;x+=PS)for(let y0=Y0;y0<Y1;y0+=PS*6)tareas.push(((x,y0)=>()=>{for(let y=y0;y<Math.min(Y1,y0+PS*6-1e-6);y+=PS){const px=x+(rn()-.5)*PS*.8,py=y+(rn()-.5)*PS*.8,ct=cell(px,py).t;if(ct===0||ct===2||ct===4)continue;const g=gy(px,py);if(g==null)continue;
   const h=top(px,py);if(h<g+.1)continue;
   // pendiente del tejado con cuatro muestras alrededor
   const e=.008,hx1=top(px+e,py),hx0=top(px-e,py),hy1=top(px,py+e),hy0=top(px,py-e);if(Math.min(hx1,hx0,hy1,hy0)<g+.08)continue;
   const sx=(hx1-hx0)/(2*e),sy=(hy1-hy0)/(2*e),pend=Math.hypot(sx,sy),ry=rn()*.2+Math.round(rn()*2)*Math.PI/2,r=rn();
   if(pend<.08){// azotea plana
    if(r<.07){const w=.016+rn()*.012,d=.014+rn()*.01,hh=.012+rn()*.008;add(B,GRA,px,h+hh/2,py,ry,w,hh,d);add(B,GRO,px,h+hh+.0012,py,ry,w*1.06,.0024,d*1.06);if(rn()<.5)add(PO,MET,px+.004,h+hh+.012,py,0,.0008,.022,.0008)}
    else if(r<.15){for(let k=0;k<1+((rn()*2)|0);k++){const ox=(rn()-.5)*.02,oy=(rn()-.5)*.02;add(B,BLA,px+ox,h+.003,py+oy,ry,.008,.006,.005)}}
    else if(r<.19){add(CY,MET,px,h+.007,py,0,.012,.014,.012);add(CY,MET,px,h+.0145,py,0,.0125,.0015,.0125)}
    else if(r<.24){add(B,CRI,px,h+.002,py,ry,.014,.004,.01)}
    else if(r<.27){add(PO,OSC,px,h+.015,py,0,.0007,.03,.0007);add(B,OSC,px,h+.026,py,ry,.012,.0007,.0007)}}
   else if(pend<1.6){// tejado de teja: chimeneas y alguna antena
    if(r<.2){const cw=.005+rn()*.003,ch=.012+rn()*.006;add(B,GRA,px,h+ch/2-.003,py,ry,cw,ch,cw*1.3);add(B,GRO,px,h+ch-.002,py,ry,cw*1.35,.0018,cw*1.65);
     if(rn()<.4)add(B,TER,px,h+ch+.0013,py,ry,cw*.6,.0035,cw*.6)}
    else if(r<.26){add(PO,OSC,px,h+.012,py,0,.0006,.026,.0006);add(B,OSC,px,h+.02,py,ry,.011,.0006,.0006);add(B,OSC,px,h+.016,py,ry+Math.PI/2,.008,.0006,.0006)}}}})(x,y0));
 tareas.push(()=>{const mm=new THREE.Matrix4(),q=new THREE.Quaternion(),V=new THREE.Vector3(),S=new THREE.Vector3(),Y=new THREE.Vector3(0,1,0);let n=0;
  for(const[mat,gs]of L)for(const[geo,A]of gs){const im=new THREE.InstancedMesh(geo,mat,A.length);A.forEach(([x,y,z,ry,a,b,c],i)=>{q.setFromAxisAngle(Y,ry);mm.compose(V.set(x,y,z),q,S.set(a,b,c));im.setMatrixAt(i,mm)});
   im.castShadow=!LT;im.receiveShadow=true;im.computeBoundingSphere();G.add(im);n+=A.length}
  scene.add(G);TC.G=G;TC.piezas=n;TC.lista=1});
 let tU=performance.now();const paso=()=>{const t0=performance.now(),gap=t0-tU;tU=t0;const bud=Math.min(80,Math.max(8,gap*.25));while(tareas.length&&performance.now()-t0<bud){const f_=tareas.shift();try{f_()}catch(e){console.warn('tejados',e);TC.err=String(e)}}TC.quedan=tareas.length;if(tareas.length)setTimeout(paso,20)};paso()}
function subePaso(){""")
open(f,'w').write(s)
print('ok tejadoscentro')
