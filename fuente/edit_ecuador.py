# ================= RÚA DO ECUADOR =================
# Mejoras de la zona de la Rúa do Ecuador mirando Google Earth (solo como referencia; modelos propios y genéricos):
#  - arbolado en la acera norte de la calle y farolas en la acera sur (antes la calle estaba pelada)
#  - Parque Infantil de la Rúa Venezuela (cruce con Simón Bolívar): plaza pavimentada con la cúpula
#    geodésica transparente que cubre los columpios, seto junto a la calzada, bancos y árboles
#  - pista polideportiva en el patio del colegio que da a la calle
# Se aplica a los 4 juegos (index, gp, nav, navm). Va DESPUÉS de edit_protagonista.py en build.sh.
import sys
JS = r"""const ECU={hecha:0,L:[98.922,25.675,96.119,24.85,95.785,24.764,92.891,23.775,89.352,22.495,89.179,22.328],PZ:[93.37,24.97],PATIO:[93.2,23.3]};window.__ECU=ECU;
function ecuChk(){if(ECU.hecha||!MAPA||!MI)return;for(const[x,y]of[[93.37,24.97],[93.2,23.3],[90.54,22.92],[97.0,25.11],[92.42,23.6]])if(sueloRap(x,y)==null)return;
 if(!repMallas(92.42,23.75).length&&!repMallas(92.42,23.45).length)return;ECU.hecha=1;setTimeout(()=>{try{ecuCrea()}catch(e){console.warn('ecuador',e);ECU.err=String(e)}},800)}
function ecuCrea(){const G=new THREE.Group();G.name='ruaEcuador';const SOMB=!window.LITE;
 const t=(x,y)=>cell(x,y).t,gy=(x,z)=>{const v=sueloRap(x,z);return v==null?groundY(x,z):v};
 const libre=(x,y)=>{const ms=repMallas(x,y);if(!ms.length)return true;return repAltura(x,y,ms)<gy(x,y)+.03};
 const cruce=(x,y,r)=>{for(let a=-r;a<=r+1e-6;a+=.02)for(let b=-r;b<=r+1e-6;b+=.02)if(cell(x+a,y+b).c)return true;return false};
 const PARTS=new Map(),add=(geo,mat,x,y,z,ry=0,rx=0)=>{const g=geo.index?geo.toNonIndexed():geo.clone();if(g.attributes.uv)g.deleteAttribute('uv');if(rx)g.rotateX(rx);g.rotateY(ry);g.translate(x,y,z);if(!PARTS.has(mat))PARTS.set(mat,[]);PARTS.get(mat).push(g)};
 const M=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.8},o));
 const HIE=M(0x22262b,{roughness:.45,metalness:.6}),FAR=M(0xfff1c8,{emissive:0xffcf7a,emissiveIntensity:.9,roughness:.3}),TRON=M(0x6b5a48),
  HOJ=M(0x4f8a3c),HOJ2=M(0x3f7a33),GRA=M(0xa9a69e,{roughness:.9}),MAD=M(0x6b4a2f),SETO=M(0x2f6a2e),
  ROJ=M(0xc8372d,{roughness:.6}),AMA=M(0xf2c443,{roughness:.6}),AZU=M(0x2f6fd0,{roughness:.6}),CAU=M(0x3f8a5a,{roughness:.95}),CAU2=M(0x2f6fa0,{roughness:.95}),
  PIS=M(0x7f9187,{roughness:.95}),LIN=M(0xf4f4ef,{roughness:.7}),VALLA=M(0x8a949b,{roughness:.5,metalness:.4});
 const cil=(r1,r2,h,s=8)=>new THREE.CylinderGeometry(r1,r2,h,s),cub=(a,b,c)=>new THREE.BoxGeometry(a,b,c);
 const arbol=(x,y,k=1)=>{const z=gy(x,y);add(cub(.014,.002,.014),HIE,x,z+.001,y);add(cil(.0018*k,.0026*k,.05*k,6),TRON,x,z+.025*k,y);
  add(new THREE.IcosahedronGeometry(.021*k,1),HOJ,x,z+.062*k,y);add(new THREE.IcosahedronGeometry(.015*k,1),HOJ2,x+.009*k,z+.075*k,y-.005*k);add(new THREE.IcosahedronGeometry(.013*k,1),HOJ,x-.008*k,z+.072*k,y+.006*k)};
 const farola=(x,y,a)=>{const z=gy(x,y);add(cil(.0011,.0016,.075),HIE,x,z+.0375,y);const dx=Math.cos(a)*.012,dy=-Math.sin(a)*.012;
  add(cub(.024,.0012,.0012),HIE,x+dx/2,z+.074,y+dy/2,a);add(cub(.007,.0035,.005),HIE,x+dx,z+.0725,y+dy,a);add(cub(.006,.0012,.004),FAR,x+dx,z+.0705,y+dy,a)};
 const banco=(x,y,a)=>{const z=gy(x,y);add(cub(.03,.0012,.009),MAD,x,z+.0055,y,a);add(cub(.03,.007,.0012),MAD,x-Math.sin(a)*.0045,z+.009,y-Math.cos(a)*.0045,a);
  for(const s of[-1,1])add(cub(.0015,.0055,.008),HIE,x+Math.cos(a)*.013*s,z+.0027,y-Math.sin(a)*.013*s,a)};
 const n={arboles:0,farolas:0};
 // ---------- 1) Arbolado y farolas a lo largo de la calle (acera norte: árboles; acera sur: farolas)
 {const L=ECU.L,pts=[];for(let i=0;i<L.length;i+=2)pts.push([L[i],L[i+1]]);const usados=[];const lejos=(x,y,d)=>!usados.some(q=>Math.hypot(q[0]-x,q[1]-y)<d);
  for(let k=0;k<pts.length-1;k++){const[ax,ay]=pts[k],[bx,by]=pts[k+1],l=Math.hypot(bx-ax,by-ay);if(l<.3)continue;const ux=(bx-ax)/l,uy=(by-ay)/l,nx=uy,ny=-ux;// n apunta al norte
   for(let s=.12;s<l-.08;s+=.025){const cx=ax+ux*s,cy=ay+uy*s;if(t(cx,cy)!==2)continue;
    for(const lado of[1,-1]){// borde de la calzada -> acera elevada -> fachada
     let o=0,s0=gy(cx,cy),ini=null,fin=null;for(o=.005;o<.3;o+=.005){const x=cx+nx*o*lado,y=cy+ny*o*lado,tt=t(x,y);if(tt===3){fin=o;break}if(tt!==2&&tt!==1)break;const h=gy(x,y);if(ini==null&&h>s0+.003)ini=o;s0=h}
     if(ini==null||fin==null||fin-ini<.025||fin-ini>.09)continue;const om=(ini+fin)/2,x=cx+nx*om*lado,y=cy+ny*om*lado;
     // detrás tiene que haber edificio (si no, es una bocacalle) y lejos de pasos de cebra
     if(t(x+nx*lado*.06,y+ny*lado*.06)!==3||t(x+ux*.05+nx*lado*.06,y+uy*.05+ny*lado*.06)!==3||t(x-ux*.05+nx*lado*.06,y-uy*.05+ny*lado*.06)!==3)continue;
     if(cruce(x,y,.05)||!libre(x,y))continue;
     if(lado===1){if(!lejos(x,y,.1))continue;usados.push([x,y]);arbol(x,y,(fin-ini)>.045?1:.85);n.arboles++}
     else{if(!lejos(x,y,.28))continue;usados.push([x,y]);farola(x,y,Math.atan2(-ny*-lado,nx*-lado));n.farolas++}}}}}
 // ---------- 2) Parque infantil de la Rúa Venezuela: plaza, cúpula geodésica, seto, bancos y árboles
 {const res=MAPA.res,cx=i=>MAPA.ox+i/res,cy=j=>MAPA.oy+j/res,on=new Set(),[px,py]=ECU.PZ,Q=[[Math.round((px-MAPA.ox)*res),Math.round((py-MAPA.oy)*res)]];
  while(Q.length&&on.size<400){const[i,j]=Q.pop(),k=i+','+j;if(on.has(k)||Math.abs(cx(i)-px)>.8||Math.abs(cy(j)-py)>.4||t(cx(i),cy(j))!==1)continue;on.add(k);Q.push([i+1,j],[i-1,j],[i,j+1],[i,j-1])}
  ECU.plaza=on.size;if(on.size>20){
   // pavimento
   const hv=new Map(),HV=(i,j)=>{const k=i+','+j;if(!hv.has(k))hv.set(k,gy(cx(i-.5),cy(j-.5))+.0035);return hv.get(k)};const pos=[],uv=[],S=.11;
   for(const k of on){const[i,j]=k.split(',').map(Number);const xa=cx(i-.5),xb=cx(i+.5),ya=cy(j-.5),yb=cy(j+.5);const A=[xa,HV(i,j),ya],B=[xb,HV(i+1,j),ya],C=[xb,HV(i+1,j+1),yb],D=[xa,HV(i,j+1),yb];
    for(const p of[A,D,C,A,C,B]){pos.push(...p);uv.push(p[0]/S,p[2]/S)}}
   {const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.computeVertexNormals();
    const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({map:psolGranito(),color:0xd8d4cc,roughness:.85,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2}));m.receiveShadow=true;m.renderOrder=1;G.add(m)}
   // sitio de la cúpula: la celda más lejos del borde
   const borde=[];for(const k of on){const[i,j]=k.split(',').map(Number);if(!on.has((i+1)+','+j)||!on.has((i-1)+','+j)||!on.has(i+','+(j+1))||!on.has(i+','+(j-1)))borde.push([i,j])}
   let best=null,bd=-1;for(const k of on){const[i,j]=k.split(',').map(Number);let d=1e9;for(const[a,b]of borde)d=Math.min(d,Math.hypot(a-i,b-j));if(d>bd){bd=d;best=[i,j]}}
   const DX=cx(best[0]),DY=cy(best[1]),R=Math.min(.15,Math.max(.07,bd/res-.012)),z0=gy(DX,DY)+.004;ECU.cupula={x:+DX.toFixed(3),y:+DY.toFixed(3),r:+R.toFixed(3)};
   // suelo de caucho de colores bajo la cúpula
   {const d1=new THREE.Mesh(new THREE.CircleGeometry(R*.97,40),M(0x3f8a5a,{roughness:.95,polygonOffset:true,polygonOffsetFactor:-4,polygonOffsetUnits:-4}));d1.rotation.x=-Math.PI/2;d1.position.set(DX,z0+.0008,DY);d1.receiveShadow=true;G.add(d1);
    const d2=new THREE.Mesh(new THREE.RingGeometry(R*.38,R*.62,32),M(0x2f6fa0,{roughness:.95,polygonOffset:true,polygonOffsetFactor:-5,polygonOffsetUnits:-5}));d2.rotation.x=-Math.PI/2;d2.position.set(DX,z0+.0012,DY);d2.receiveShadow=true;G.add(d2)}
   // zócalo
   add(cil(R+.004,R+.006,.006,40),GRA,DX,z0+.003,DY);
   // cúpula geodésica (icosaedro subdividido, media esfera achatada): barras + vidrio
   {const ico=new THREE.IcosahedronGeometry(1,2).toNonIndexed(),p=ico.attributes.position,tri=[],H=.78;
    for(let i=0;i<p.count;i+=3){const v=[0,1,2].map(q=>new THREE.Vector3(p.getX(i+q),p.getY(i+q),p.getZ(i+q)));if((v[0].y+v[1].y+v[2].y)/3<-.04)continue;
     for(const w of v){w.y=Math.max(0,w.y)*H}tri.push(v)}
    const vid=[];for(const v of tri)for(const w of v)vid.push(DX+w.x*R,z0+.006+w.y*R,DY+w.z*R);
    {const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vid,3));g.computeVertexNormals();
     const m=new THREE.Mesh(g,new THREE.MeshPhysicalMaterial({color:0xd6ecf2,roughness:.08,metalness:0,transparent:true,opacity:.2,side:THREE.DoubleSide,depthWrite:false}));m.renderOrder=3;G.add(m)}
    const ya=new Set(),bar=(a,b)=>{const k=[a,b].map(w=>w.x.toFixed(3)+','+w.y.toFixed(3)+','+w.z.toFixed(3)).sort().join('|');if(ya.has(k))return;ya.add(k);
     const A=new THREE.Vector3(DX+a.x*R,z0+.006+a.y*R,DY+a.z*R),B=new THREE.Vector3(DX+b.x*R,z0+.006+b.y*R,DY+b.z*R),L=A.distanceTo(B);if(L<1e-5)return;
     const g=new THREE.CylinderGeometry(.0009,.0009,L,4,1).toNonIndexed();g.deleteAttribute('uv');const q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),B.clone().sub(A).normalize());
     g.applyQuaternion(q);const c=A.clone().add(B).multiplyScalar(.5);g.translate(c.x,c.y,c.z);if(!PARTS.has(HIE))PARTS.set(HIE,[]);PARTS.get(HIE).push(g)};
    for(const v of tri){bar(v[0],v[1]);bar(v[1],v[2]);bar(v[2],v[0])}
    add(cil(.012,.014,.006,12),HIE,DX,z0+.006+R*H+.002,DY);add(cil(.006,.012,.006,12),LIN,DX,z0+.006+R*H+.007,DY)}
   // juegos bajo la cúpula: torre con tobogán, columpios y muelles
   {const a=Math.random()*0,c=Math.cos(a),s=Math.sin(a),P=(lx,lz)=>[DX+lx*c+lz*s,DY-lx*s+lz*c],Z=z0+.001,k=R/.15;
    const[tx,ty]=P(-.035*k,-.01*k);for(const[ox,oz]of[[-1,-1],[1,-1],[1,1],[-1,1]])add(cil(.0012,.0012,.03),AMA,tx+ox*.009,Z+.015,ty+oz*.009);
    add(cub(.022,.002,.022),AZU,tx,Z+.017,ty);add(new THREE.ConeGeometry(.018,.012,4),ROJ,tx,Z+.036,ty,Math.PI/4);
    add(cub(.008,.0015,.034),ROJ,tx+.019,Z+.009,ty,0,.5);add(cub(.006,.012,.0015),AZU,tx-.014,Z+.009,ty+.01);
    const[sx,sy]=P(.04*k,.025*k);add(cub(.05,.0016,.0016),HIE,sx,Z+.03,sy);for(const e of[-1,1]){add(cub(.0016,.031,.0016),HIE,sx+e*.025,Z+.0155,sy-.009,0,.28);add(cub(.0016,.031,.0016),HIE,sx+e*.025,Z+.0155,sy+.009,0,-.28)}
    for(const e of[-1,1]){add(cub(.0005,.019,.0005),HIE,sx+e*.01,Z+.02,sy);add(cub(.009,.0012,.005),ROJ,sx+e*.01,Z+.0105,sy)}
    const[mx,my]=P(.035*k,-.045*k);add(cil(.0012,.0012,.008),HIE,mx,Z+.004,my);add(cub(.012,.006,.004),AMA,mx,Z+.011,my);
    const[nx2,ny2]=P(-.01*k,.06*k);add(cil(.0012,.0012,.008),HIE,nx2,Z+.004,ny2);add(cub(.012,.006,.004),AZU,nx2,Z+.011,ny2)}
   // seto junto a la calzada (con huecos en los pasos de cebra) y bancos/árboles por la plaza
   let nh=0;for(const[i,j]of borde){const x=cx(i),y=cy(j);let calz=false;for(const[a,b]of[[1,0],[-1,0],[0,1],[0,-1]])if(t(cx(i+a),cy(j+b))===2)calz=true;
    if(!calz||cruce(x,y,.07)||Math.hypot(x-DX,y-DY)<R+.02)continue;add(cub(.051,.012,.051),SETO,x,gy(x,y)+.006,y);nh++}
   ECU.seto=nh;
   const pz=[];for(const k of on){const[i,j]=k.split(',').map(Number);const x=cx(i),y=cy(j),d=Math.hypot(x-DX,y-DY);if(d<R+.03)continue;if(borde.some(([a,b])=>a===i&&b===j))continue;if(!libre(x,y))continue;pz.push([x,y,d])}
   pz.sort((a,b)=>a[2]-b[2]);const us=[];const pick=(sp,max,f)=>{let c=0;for(const p of pz){if(c>=max)break;if(us.some(q=>Math.hypot(q[0]-p[0],q[1]-p[1])<sp))continue;us.push(p);f(p);c++}return c};
   ECU.bancos=pick(.07,4,p=>banco(p[0],p[1],Math.atan2(DX-p[0],DY-p[1])));
   pz.reverse();ECU.arbPlaza=pick(.1,4,p=>arbol(p[0],p[1],.9))}}
 // ---------- 3) Pista polideportiva en el patio del colegio (orientada con la calle)
 {const a=Math.atan2(-.318,.948),c=Math.cos(a),s=Math.sin(a),W=.3,Hh=.17,[x0,y0]=ECU.PATIO;
  const dentro=(x,y)=>{for(let u=-W/2-.02;u<=W/2+.02+1e-6;u+=.025)for(let v=-Hh/2-.02;v<=Hh/2+.02+1e-6;v+=.025){const X=x+u*c+v*s,Y=y-u*s+v*c;if(t(X,Y)!==1||!libre(X,Y))return false}return true};
  let sit=null;for(let r=0;r<=.45&&!sit;r+=.02)for(let q=0;q<Math.max(1,Math.round(r*40));q++){const an=q/Math.max(1,Math.round(r*40))*Math.PI*2,x=x0+Math.cos(an)*r,y=y0+Math.sin(an)*r;if(dentro(x,y)){sit=[x,y];break}}
  ECU.pista=sit&&sit.map(v=>+v.toFixed(3));if(sit){const[X,Y]=sit,P=(u,v)=>[X+u*c+v*s,Y-u*s+v*c];let zm=-1e9;for(const u of[-W/2,0,W/2])for(const v of[-Hh/2,0,Hh/2]){const[x,y]=P(u,v);zm=Math.max(zm,gy(x,y))}const Z=zm+.004;
   const pl=(w,h,mat,u,v,dz,po)=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),mat);m.rotation.set(-Math.PI/2,0,a,'YXZ');const[x,y]=P(u,v);m.position.set(x,Z+dz,y);m.receiveShadow=true;G.add(m);return m};
   pl(W+.03,Hh+.03,M(0x9a6b55,{roughness:.95,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3}),0,0,0);
   pl(W,Hh,M(0x5f8f7a,{roughness:.95,polygonOffset:true,polygonOffsetFactor:-4,polygonOffsetUnits:-4}),0,0,.0004);
   const lin=(u,v,w,h)=>{const[x,y]=P(u,v);add(cub(w,.0006,h),LIN,x,Z+.0009,y,a)},e=.0016;
   lin(0,-Hh/2+e/2,W,e);lin(0,Hh/2-e/2,W,e);lin(-W/2+e/2,0,e,Hh);lin(W/2-e/2,0,e,Hh);lin(0,0,e,Hh);
   {const g=new THREE.RingGeometry(.022,.0236,32);const m=new THREE.Mesh(g,LIN);m.rotation.x=-Math.PI/2;const[x,y]=P(0,0);m.position.set(x,Z+.001,y);G.add(m)}
   for(const sg of[-1,1]){const ar=new THREE.RingGeometry(.05,.0516,24,1,sg>0?Math.PI/2:-Math.PI/2,Math.PI);const m=new THREE.Mesh(ar,LIN);m.rotation.set(-Math.PI/2,0,a,'YXZ');const[x,y]=P(sg*W/2,0);m.position.set(x,Z+.001,y);G.add(m);
    // porterías y canastas
    const[gx,gyy]=P(sg*(W/2-.004),0);for(const v of[-1,1]){const[x,y]=P(sg*(W/2-.004),v*.023);add(cil(.0008,.0008,.016,5),LIN,x,Z+.008,y)}add(cub(.0016,.0016,.047),ROJ,gx,Z+.016,gyy,a);
    const[bx,by]=P(sg*(W/2+.008),0);add(cil(.001,.001,.04,5),HIE,bx,Z+.02,by);add(cub(.0012,.009,.014),LIN,bx-sg*c*.002,Z+.04,by+sg*s*.002,a);add(new THREE.TorusGeometry(.0035,.0006,4,12),ROJ,bx-sg*c*.006,Z+.036,by+sg*s*.006,0,Math.PI/2)}
   // valla perimetral
   const VR=M(0x9fb0a8,{transparent:true,opacity:.35,side:THREE.DoubleSide,depthWrite:false,roughness:.6});const vh=.035,U=W/2+.015,V=Hh/2+.015;
   for(const[u0,v0,u1,v1]of[[-U,-V,U,-V],[U,-V,U,V],[U,V,-U,V],[-U,V,-U,-V]]){const L=Math.hypot(u1-u0,v1-v0),nP=Math.round(L/.04);
    for(let q=0;q<=nP;q++){const[x,y]=P(u0+(u1-u0)*q/nP,v0+(v1-v0)*q/nP);add(cil(.0007,.0007,vh,4),VALLA,x,Z+vh/2,y)}
    const[mx,my]=P((u0+u1)/2,(v0+v1)/2),ang=a+Math.atan2(-(v1-v0),u1-u0);const m=new THREE.Mesh(new THREE.PlaneGeometry(L,vh),VR);m.rotation.y=ang;m.position.set(mx,Z+vh/2,my);m.renderOrder=2;G.add(m)}}}
 Object.assign(ECU,n);
 for(const[mat,gs]of PARTS){const m=new THREE.Mesh(mergeGeometries(gs),mat);m.castShadow=SOMB&&mat!==FAR;m.receiveShadow=true;G.add(m)}
 scene.add(G);ECU.G=G}
"""
for f in (sys.argv[1:] or ['index.html','gp.html','nav.html','navm.html']):
    s=open(f,encoding='utf-8').read()
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("function subeZonas(){psolChk();","function subeZonas(){psolChk();ecuChk();")
    r("function subePaso(){",JS+"function subePaso(){")
    # el raycast de depuración no debe chocar con la cúpula ni con los árboles nuevos
    if "!(window.__PSOL&&__PSOL.G&&__PSOL.G.children.includes(i.object))" in s:
        r("!(window.__PSOL&&__PSOL.G&&__PSOL.G.children.includes(i.object))","!(window.__PSOL&&__PSOL.G&&__PSOL.G.children.includes(i.object))&&!(window.__ECU&&__ECU.G&&__ECU.G.children.includes(i.object))")
    open(f,'w',encoding='utf-8').write(s)
print('ok ecuador')
