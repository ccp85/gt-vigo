// Hornea las marcas viales rectas de cada zona (lineasrectas.js) en <zona>_lineas.bin.
// Uso, desde la carpeta del juego:  node fuente/herramientas/lineas_hornear.mjs [zona ...]
// Lee <zona>_partes.json + <zona>_glb_N.png (GLB dentro de un PNG), vigo_trafico.json y escribe <zona>_lineas.bin.
// Necesita el decodificador de meshopt:  npm i meshoptimizer  (en cualquier carpeta del camino)
// Volver a hornear si cambian las calles (vigo_trafico.json), la calzada o las marcas de una zona.
import fs from 'fs';import zlib from 'zlib';import path from 'path';import {fileURLToPath} from 'url';
import {MeshoptDecoder} from 'meshoptimizer';
const AQUI=path.dirname(fileURLToPath(import.meta.url));
globalThis.window=globalThis;globalThis.THREE={};
(0,eval)(fs.readFileSync(path.join(AQUI,'..','lineasrectas.js'),'utf8'));
await MeshoptDecoder.ready;
function png(file){const d=fs.readFileSync(file);let p=8,w=0,h=0;const idat=[];
 while(p<d.length){const len=d.readUInt32BE(p),t=d.toString('latin1',p+4,p+8);if(t==='IHDR'){w=d.readUInt32BE(p+8);h=d.readUInt32BE(p+12)}else if(t==='IDAT')idat.push(d.subarray(p+8,p+8+len));else if(t==='IEND')break;p+=12+len}
 const raw=zlib.inflateSync(Buffer.concat(idat)),bpp=3,st=w*bpp,out=new Uint8Array(st*h);
 for(let y=0;y<h;y++){const f=raw[y*(st+1)],src=y*(st+1)+1,o=y*st;for(let x=0;x<st;x++){const a=x>=bpp?out[o+x-bpp]:0,b=y?out[o-st+x]:0,c=(x>=bpp&&y)?out[o-st+x-bpp]:0;let v=raw[src+x];
  if(f===1)v+=a;else if(f===2)v+=b;else if(f===3)v+=(a+b)>>1;else if(f===4){const pp=a+b-c,pa=Math.abs(pp-a),pb=Math.abs(pp-b),pc=Math.abs(pp-c);v+=(pa<=pb&&pa<=pc)?a:(pb<=pc?b:c)}out[o+x]=v&255}}
 return out}
function glbZona(id){const pj=JSON.parse(fs.readFileSync(id+'_partes.json'));if(pj.formato!=='png')throw new Error('formato '+pj.formato);
 // cada PNG lleva delante la longitud (uint32) de su trozo del GLB
 const parts=[...Array(pj.partes)].map((_,i)=>{const p=Buffer.from(png(id+'_glb_'+(i+1)+'.png'));return p.subarray(4,4+p.readUInt32LE(0))});
 return Buffer.concat(parts)}
function mallas(g){const jl=g.readUInt32LE(12);const j=JSON.parse(g.subarray(20,20+jl).toString('utf8'));const bin=g.subarray(20+jl+8);const cache={};
 const bv=i=>{if(cache[i])return cache[i];const v=j.bufferViews[i],e=v.extensions&&v.extensions.EXT_meshopt_compression;
  if(e){const src=new Uint8Array(bin.buffer,bin.byteOffset+(e.byteOffset||0),e.byteLength),out=new Uint8Array(e.count*e.byteStride);MeshoptDecoder.decodeGltfBuffer(out,e.count,e.byteStride,src,e.mode,e.filter);return cache[i]={u8:out,st:e.byteStride}}
  return cache[i]={u8:new Uint8Array(bin.buffer,bin.byteOffset+(v.byteOffset||0),v.byteLength),st:v.byteStride}};
 const G={5120:'getInt8',5121:'getUint8',5122:'getInt16',5123:'getUint16',5125:'getUint32',5126:'getFloat32'},S={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4},NC={SCALAR:1,VEC2:2,VEC3:3,VEC4:4};
 const acc=i=>{const a=j.accessors[i],b=bv(a.bufferView),nc=NC[a.type],es=S[a.componentType],st=b.st||nc*es,dv=new DataView(b.u8.buffer,b.u8.byteOffset),out=new Float64Array(a.count*nc);
  for(let k=0;k<a.count;k++)for(let c=0;c<nc;c++){let v=dv[G[a.componentType]]((a.byteOffset||0)+k*st+c*es,true);
   if(a.normalized){if(a.componentType===5122)v=Math.max(v/32767,-1);else if(a.componentType===5123)v/=65535;else if(a.componentType===5120)v=Math.max(v/127,-1);else if(a.componentType===5121)v/=255}out[k*nc+c]=v}return out};
 const res=[];for(const n of j.nodes){if(n.mesh==null)continue;if(n.rotation||n.matrix||n.children)throw new Error('nodo con giro/hijos: '+n.name);const t=n.translation||[0,0,0],s=n.scale||[1,1,1];
  for(const p of j.meshes[n.mesh].primitives){const P=acc(p.attributes.POSITION);for(let i=0;i<P.length;i+=3){P[i]=P[i]*s[0]+t[0];P[i+1]=P[i+1]*s[1]+t[1];P[i+2]=P[i+2]*s[2]+t[2]}
   const I=p.indices!=null?Uint32Array.from(acc(p.indices)):Uint32Array.from({length:P.length/3},(_,i)=>i);
   res.push({nombre:n.name||'',mat:(j.materials[p.material]||{}).name||'',P:Float32Array.from(P),I})}}
 return res}
const TRAF=JSON.parse(fs.readFileSync('vigo_trafico.json'));
const ids=process.argv.slice(2).length?process.argv.slice(2):fs.readdirSync('.').filter(f=>/_partes\.json$/.test(f)).map(f=>f.replace('_partes.json',''));
for(const id of ids){const t0=Date.now();let M;try{M=mallas(glbZona(id))}catch(e){console.log(id,'sin GLB:',e.message);continue}
 const cal=M.filter(m=>/^calzada/.test(m.nombre)||(/^puente/.test(m.nombre)&&m.mat==='calzada'));const lin=M.filter(m=>/^lineas/.test(m.nombre));
 if(!cal.length||lin.length!==1){console.log(id,'sin calzada o marcas',cal.length,lin.length);if(fs.existsSync(id+'_lineas.bin'))fs.unlinkSync(id+'_lineas.bin');continue}
 // triángulos de asfalto (solo los que miran hacia arriba)
 const T=[];for(const m of cal)for(let k=0;k<m.I.length;k+=3){const a=m.I[k]*3,b=m.I[k+1]*3,c=m.I[k+2]*3,P=m.P;
  const ux=P[b]-P[a],uy=P[b+1]-P[a+1],uz=P[b+2]-P[a+2],vx=P[c]-P[a],vy=P[c+1]-P[a+1],vz=P[c+2]-P[a+2];const nx=uy*vz-uz*vy,ny=uz*vx-ux*vz,nz=ux*vy-uy*vx;
  if(Math.abs(ny)<.7*Math.hypot(nx,ny,nz))continue;T.push(P[a],P[a+1],P[a+2],P[b],P[b+1],P[b+2],P[c],P[c+1],P[c+2])}
 const tris=Float32Array.from(T);let x0=1e9,z0=1e9,x1=-1e9,z1=-1e9;for(let i=0;i<tris.length;i+=3){x0=Math.min(x0,tris[i]);x1=Math.max(x1,tris[i]);z0=Math.min(z0,tris[i+2]);z1=Math.max(z1,tris[i+2])}
 const ways=[];for(const w of TRAF){let a=1e9,b=1e9,c=-1e9,d=-1e9;for(const q of w.p){a=Math.min(a,q[0]);c=Math.max(c,q[0]);b=Math.min(b,q[1]);d=Math.max(d,q[1])}
  if(c<x0-.1||a>x1+.1||d<z0-.1||b>z1+.1)continue;ways.push({c:w.c,u:w.u,p:w.p,bb:[a,b,c,d]})}
 const L=lin[0],comps=window.__lineasComps(L.P,L.I);
 const r=await window.__lineasConstruir(tris,ways,{comps});
 const keep=[];for(const cid of r.keep)for(const t of comps[cid].ts)for(let j=0;j<3;j++){const v=L.I[t+j]*3;keep.push(L.P[v],L.P[v+1],L.P[v+2])}
 const buf=window.__lineasCodifica(r.rects,keep);fs.writeFileSync(id+'_lineas.bin',Buffer.from(buf));
 console.log(id,JSON.stringify(r.n),'rect',r.rects.length/7,'kB',(buf.byteLength/1024).toFixed(0),'s',((Date.now()-t0)/1000).toFixed(1))}
