// ---------- CANTOS DE CALLES: calzadas, aceras y zonas verdes con lados (no láminas flotando) ----------
// En las zonas, calzada, aceras y jardines son láminas planas puestas a distinta altura sobre la tierra (verde ≈ +0,015,
// calzada ≈ +0,025, aceras ≈ +0,04) y sin lados: en el borde se veía el canto abierto y parecían hojas flotando sobre el suelo.
// Aquí, al cargar cada zona, se buscan los bordes de esas láminas que dan a algo más bajo (tierra, jardín, calzada) y se les
// pone un lado vertical que baja justo hasta lo que hay al lado: bordillo de las aceras, canto del asfalto y talud de tierra de
// los jardines, un poco más oscuros abajo (el contacto con el suelo). Los bordes que quedan tapados por otra lámina igual o más
// alta no llevan lado. El cálculo va en segundo plano (Web Worker) para no frenar la carga; los lados se reparten en trozos
// de 16×16 u que se ocultan con la niebla como el resto. No cambian las alturas del suelo: coches y peatones pisan igual.
const FALDON=(()=>{
 const src=`
 const TIPO={suelo:0,verde:1,calzada:2,acera:3,edificio:4};
 function leer(a){const n=a.n,S=a.st,o=a.of,ar=a.ar,out=new Float32Array(n*3),m=a.mw;
  const k=a.norm?(ar instanceof Int16Array?1/32767:ar instanceof Uint16Array?1/65535:ar instanceof Int8Array?1/127:ar instanceof Uint8Array?1/255:1):1;
  for(let i=0;i<n;i++){let x=ar[i*S+o]*k,y=ar[i*S+o+1]*k,z=ar[i*S+o+2]*k;if(a.norm&&k!==1&&(ar instanceof Int16Array||ar instanceof Int8Array)){x=Math.max(x,-1);y=Math.max(y,-1);z=Math.max(z,-1)}
   out[i*3]=m[0]*x+m[4]*y+m[8]*z+m[12];out[i*3+1]=m[1]*x+m[5]*y+m[9]*z+m[13];out[i*3+2]=m[2]*x+m[6]*y+m[10]*z+m[14]}return out}
 self.onmessage=e=>{const T0=performance.now();const {id,mallas,col}=e.data;try{
  // 1) todas las superficies en mundo
  const M=mallas.map(q=>{const p=leer(q);const ix=q.ix||(()=>{const a=new Uint32Array(q.n);for(let i=0;i<q.n;i++)a[i]=i;return a})();return {t:q.t,p,ix}});
  let x0=1e9,z0=1e9,x1=-1e9,z1=-1e9;for(const m of M){const p=m.p;for(let i=0;i<p.length;i+=3){const x=p[i],z=p[i+2];if(x<x0)x0=x;if(x>x1)x1=x;if(z<z0)z0=z;if(z>z1)z1=z}}
  if(!(x1>x0))return self.postMessage({id,trozos:[]});
  // 2) rejilla de triángulos para saber qué hay (y a qué altura) en cualquier punto
  const G=.2,NX=Math.ceil((x1-x0)/G)+1,NZ=Math.ceil((z1-z0)/G)+1,cnt=new Uint32Array(NX*NZ+1);
  let NT=0;for(const m of M)NT+=m.ix.length/3;const TM=new Uint16Array(NT),TI=new Uint32Array(NT);{let t=0;for(let k=0;k<M.length;k++){const n=M[k].ix.length/3;for(let i=0;i<n;i++){TM[t]=k;TI[t]=i;t++}}}
  const caja=(t,f)=>{const m=M[TM[t]],p=m.p,ix=m.ix,b=TI[t]*3;const a=ix[b]*3,c=ix[b+1]*3,d=ix[b+2]*3;
   const gx0=Math.max(0,Math.floor((Math.min(p[a],p[c],p[d])-x0)/G)),gx1=Math.min(NX-1,Math.floor((Math.max(p[a],p[c],p[d])-x0)/G));
   const gz0=Math.max(0,Math.floor((Math.min(p[a+2],p[c+2],p[d+2])-z0)/G)),gz1=Math.min(NZ-1,Math.floor((Math.max(p[a+2],p[c+2],p[d+2])-z0)/G));
   for(let gz=gz0;gz<=gz1;gz++)for(let gx=gx0;gx<=gx1;gx++)f(gz*NX+gx)};
  for(let t=0;t<NT;t++)caja(t,c=>cnt[c+1]++);for(let c=1;c<cnt.length;c++)cnt[c]+=cnt[c-1];
  const ent=new Uint32Array(cnt[cnt.length-1]),fill=cnt.slice(0,NX*NZ);for(let t=0;t<NT;t++)caja(t,c=>{ent[fill[c]++]=t});
  // altura más alta de las láminas que tapan el punto (x,z); null si no hay nada. Dentro de la planta de un edificio, +Infinity
  // (el borde da contra una fachada: no lleva lado)
  const techo=(x,z,yr)=>{const gx=Math.floor((x-x0)/G),gz=Math.floor((z-z0)/G);if(gx<0||gz<0||gx>=NX||gz>=NZ)return null;const c=gz*NX+gx;let h=null;
   for(let e=cnt[c];e<cnt[c+1];e++){const t=ent[e],m=M[TM[t]],p=m.p,b=TI[t]*3;const a=m.ix[b]*3,bb=m.ix[b+1]*3,d=m.ix[b+2]*3;
    const ax=p[a],az=p[a+2],v0x=p[bb]-ax,v0z=p[bb+2]-az,v1x=p[d]-ax,v1z=p[d+2]-az,v2x=x-ax,v2z=z-az;
    const den=v0x*v1z-v1x*v0z;if(Math.abs(den)<1e-12)continue;const u=(v2x*v1z-v1x*v2z)/den,v=(v0x*v2z-v2x*v0z)/den;
    if(u<-1e-6||v<-1e-6||u+v>1+1e-6)continue;if(m.t===TIPO.edificio)return Infinity;const y=p[a+1]+u*(p[bb+1]-p[a+1])+v*(p[d+1]-p[a+1]);if(y>yr+.1)continue;if(h===null||y>h)h=y}return h};   // lo que pasa muy por encima (un puente) no cuenta
  // 3) bordes abiertos de cada lámina (aristas de un solo triángulo) que dan a algo más bajo → lado vertical
  const T8=16,TR=new Map(),EPS=.006;
  const trozo=(x,z)=>{const k=Math.floor(x/T8)+','+Math.floor(z/T8);let o=TR.get(k);if(!o){o={p:[],n:[],c:[],x:0,z:0,k:0};TR.set(k,o)}return o};
  // un lado vertical de A a B (arriba) que baja d; la cara mira hacia (nx,nz)
  const lado=(p,a,b,d,base)=>{const ax=p[a],ay=p[a+1],az=p[a+2],bx=p[b],by=p[b+1],bz=p[b+2];let dx=bx-ax,dz=bz-az;const L=Math.hypot(dx,dz);if(L<1e-6)return;
   const nx=dz/L,nz=-dx/L,mx=(ax+bx)/2,mz=(az+bz)/2;const o=trozo(mx,mz),P=o.p,N=o.n,C=o.c;
   const fuera=(dz*d)*nx+(-dx*d)*nz>0;   // (B-A)×(A'-A) hacia fuera
   const V=[[ax,ay,az,1],[bx,by,bz,1],[bx,by-d,bz,0],[ax,ay-d,az,0]];
   for(const i of (fuera?[0,1,2,0,2,3]:[0,2,1,0,3,2])){const v=V[i];P.push(v[0],v[1],v[2]);N.push(nx,0,nz);const s=v[3]?1:.7;C.push(base[0]*s,base[1]*s,base[2]*s)}
   o.x+=mx;o.z+=mz;o.k++};
  for(const m of M){if(m.t===TIPO.suelo||m.t===TIPO.edificio)continue;const p=m.p,ix=m.ix,nv=p.length/3;
   const w=new Int32Array(nv),mapa=new Map();for(let i=0;i<nv;i++){const k=Math.round(p[i*3]*1e4)+'|'+Math.round(p[i*3+1]*1e4)+'|'+Math.round(p[i*3+2]*1e4);let r=mapa.get(k);if(r===undefined){r=i;mapa.set(k,i)}w[i]=r}
   const A=new Map();
   for(let i=0;i<ix.length;i+=3)for(let s=0;s<3;s++){const a=w[ix[i+s]],b=w[ix[i+(s+1)%3]],c=w[ix[i+(s+2)%3]];if(a===b)continue;const k=a<b?a*4194304+b:b*4194304+a;const q=A.get(k);if(q)q[2]=-1;else A.set(k,[a,b,c])}
   const base=col[m.t];
   // aristas que llevan lado, orientadas de modo que «fuera» quede a la derecha: normal = (dz,-dx)
   const EA=[],EB=[],ED=[];
   for(const q of A.values()){if(q[2]<0)continue;const a=q[0]*3,b=q[1]*3,c=q[2]*3;
    const ax=p[a],ay=p[a+1],az=p[a+2],bx=p[b],by=p[b+1],bz=p[b+2];let dx=bx-ax,dz=bz-az;const L=Math.hypot(dx,dz);if(L<1e-5)continue;dx/=L;dz/=L;
    let nx=dz,nz=-dx,giro=false;const mx=(ax+bx)/2,mz=(az+bz)/2;if((p[c]-mx)*nx+(p[c+2]-mz)*nz>0){nx=-nx;nz=-nz;giro=true}   // normal hacia fuera de la lámina
    const ym=(ay+by)/2;let bajo=Infinity,tapado=0,cuantos=0;
    for(const f of (L>.05?[.2,.5,.8]:[.5])){const h=techo(ax+(bx-ax)*f+nx*EPS,az+(bz-az)*f+nz*EPS,ym);cuantos++;
     if(h!==null&&h>=ym-.004){tapado++;continue}bajo=Math.min(bajo,h===null?ym-.05:h)}
    if(tapado===cuantos)continue;
    let d=ym-bajo+.003;if(d<.005)continue;if(d>.15)d=.15;
    if(giro){EA.push(q[1]);EB.push(q[0])}else{EA.push(q[0]);EB.push(q[1])}ED.push(d)}
   // se encadenan las aristas (cada una sigue a la que empieza donde ella acaba) y los tramos casi rectos se juntan en un solo lado:
   // los bordes vienen en escalera (pasos de ~0,01 u) y muy troceados: se sigue la línea media de la escalera (desvío máx. ~0,009)
   // y así salen muchos menos triángulos
   const sal=new Map(),ent=new Map();for(let i=0;i<EA.length;i++){sal.set(EA[i],sal.has(EA[i])?-1:i);ent.set(EB[i],(ent.get(EB[i])||0)+1)}
   const usado=new Uint8Array(EA.length);
   const sig=i=>{if(ent.get(EB[i])!==1)return -1;const j=sal.get(EB[i]);return j===undefined||j<0||usado[j]?-1:j};
   const medio=i=>ent.get(EA[i])===1&&sal.get(EA[i])===i;
   const tramo=c=>{const n=c.length,pt=[EA[c[0]]*3];for(const i of c)pt.push(EB[i]*3);
    let s0=0;while(s0<n){let e=s0+1,dm=ED[c[s0]];
     while(e<n){const e2=e+1,a=pt[s0],b=pt[e2];const dx=p[b]-p[a],dz=p[b+2]-p[a+2],L=Math.hypot(dx,dz);if(L>2||L<1e-6)break;let ok=true,dd=Math.max(dm,ED[c[e]]);
      for(let k=s0;k<e2&&ok;k++){if(Math.abs(ED[c[k]]-ED[c[s0]])>.005)ok=false}
      for(let k=s0+1;k<e2&&ok;k++){const q=pt[k];const t=((p[q]-p[a])*dx+(p[q+2]-p[a+2])*dz)/(L*L);if(t<0||t>1){ok=false;break}
       const ox=p[a]+dx*t-p[q],oz=p[a+2]+dz*t-p[q+2],oy=p[a+1]+(p[b+1]-p[a+1])*t-p[q+1];if(ox*ox+oz*oz>8e-5||Math.abs(oy)>.0015)ok=false}
      if(!ok)break;dm=dd;e=e2}
     lado(p,pt[s0],pt[e],dm,base);s0=e}};
   for(let i=0;i<EA.length;i++){if(usado[i]||medio(i))continue;const c=[i];usado[i]=1;let j;while((j=sig(c[c.length-1]))>=0){usado[j]=1;c.push(j)}tramo(c)}
   for(let i=0;i<EA.length;i++){if(usado[i])continue;const c=[i];usado[i]=1;let j;while((j=sig(c[c.length-1]))>=0){usado[j]=1;c.push(j)}tramo(c)}   // anillos cerrados
  }
  const trozos=[],tr=[];for(const o of TR.values()){if(!o.k)continue;const p=new Float32Array(o.p),n=new Float32Array(o.n),c=new Float32Array(o.c);trozos.push({p,n,c,x:o.x/o.k,z:o.z/o.k});tr.push(p.buffer,n.buffer,c.buffer)}
  self.postMessage({id,trozos,ms:Math.round(performance.now()-T0),nt:NT},tr)}catch(err){self.postMessage({id,err:String(err&&err.stack||err)})}};`;
 let W=null;try{W=new Worker(URL.createObjectURL(new Blob([src],{type:'text/javascript'})))}catch(e){console.warn('faldones',e)}
 const PEND={};let n=0;if(W)W.onmessage=e=>{const q=PEND[e.data.id];delete PEND[e.data.id];if(q)q(e.data)};
 const tipo=nm=>/^(calzada|carril)/.test(nm)?2:/^(aceras|acera|plaza|paseo)/.test(nm)?3:/^verde/.test(nm)?1:/^(tierra|playa|playita|roca|labio|muelle|puente)/.test(nm)?0:/^(edificios|cubiertas|tejados)/.test(nm)?4:-1;
 const lin=c=>[c.r,c.g,c.b];
 function datos(o){const g=o.geometry,at=g&&g.attributes.position;if(!at)return null;o.updateMatrixWorld(true);
  const il=at.isInterleavedBufferAttribute,ar=il?at.data.array:at.array,st=il?at.data.stride:at.itemSize,of=il?at.offset:0;
  const ix=g.index?(g.index.array instanceof Uint32Array?g.index.array.slice():Uint32Array.from(g.index.array)):null;
  return {n:at.count,ar:ar.slice(),st,of,norm:!!at.normalized,mw:o.matrixWorld.elements.slice(),ix}}
 return function(root){if(!W||root.userData.faldones)return;root.userData.faldones=1;
  const mallas=[],col={};let cTierra=null,cVerde=null;
  root.traverse(o=>{if(!o.isMesh||o.isInstancedMesh)return;const t=tipo(o.name);if(t<0)return;const d=datos(o);if(!d)return;d.t=t;mallas.push(d);
   const m=[].concat(o.material)[0];if(!m||!m.color)return;
   if(t===2&&!col[2])col[2]=lin(m.color.clone().multiplyScalar(.85));            // canto del asfalto, algo más oscuro que la calzada
   if(t===3&&!col[3])col[3]=lin(m.color.clone().multiplyScalar(.9));             // bordillo: piedra como la acera
   if(t===1&&!cVerde)cVerde=m.color.clone();if(/^tierra/.test(o.name)&&!cTierra)cTierra=m.color.clone()});
  if(!mallas.some(m=>m.t>0&&m.t<4))return;
  // talud de los jardines: tierra oscura con un poco del verde
  const ct=(cTierra||new THREE.Color(.73,.67,.56)).clone().multiplyScalar(.5);if(cVerde)ct.lerp(cVerde,.3);col[1]=lin(ct);
  col[2]=col[2]||[.085,.085,.13];col[3]=col[3]||[.48,.45,.4];col[0]=[0,0,0];
  const id=++n;PEND[id]=r=>{if(r.err){console.warn('faldones',r.err);return}(window.__FALDON=window.__FALDON||[]).push([root.name,r.ms,r.nt,r.trozos.reduce((s,t)=>s+t.p.length/9,0)]);if(!r.trozos.length||!root.parent)return;   // la zona ya se descargó
   const mat=window.LITE?new THREE.MeshLambertMaterial({vertexColors:true}):new THREE.MeshStandardMaterial({vertexColors:true,roughness:.92,metalness:0});
   root.updateMatrixWorld(true);const inv=root.matrixWorld.equals(new THREE.Matrix4())?null:root.matrixWorld.clone().invert();
   for(const t of r.trozos){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(t.p,3));g.setAttribute('normal',new THREE.BufferAttribute(t.n,3));g.setAttribute('color',new THREE.BufferAttribute(t.c,3));
    g.computeBoundingSphere();const m=new THREE.Mesh(g,mat);m.name='faldon';m.castShadow=!window.LITE;m.receiveShadow=true;m.userData.noLote=true;m.matrixAutoUpdate=false;
    if(inv)m.applyMatrix4(inv);root.add(m);m.updateMatrix();m.updateMatrixWorld(true);if(typeof TROZOS!=='undefined')TROZOS.push({m,x:t.x,y:t.z,tes:true})}
   if(typeof recortar==='function')recortar(0,true)};
  const tr=[];for(const m of mallas){tr.push(m.ar.buffer);if(m.ix)tr.push(m.ix.buffer)}
  W.postMessage({id,mallas,col},tr)}})();
