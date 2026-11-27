// Extrae triángulos (en coordenadas del mundo) de las mallas de un glb con EXT_meshopt_compression + KHR_mesh_quantization
// uso: node glbtris.mjs zona.glb salida.json malla1,malla2,...
import fs from 'fs';
import { MeshoptDecoder } from 'meshoptimizer';
const [,, fin, fout, lista] = process.argv;
const want = new Set(lista.split(','));
const g = fs.readFileSync(fin);
const jl = g.readUInt32LE(12); const J = JSON.parse(g.subarray(20, 20 + jl).toString('utf8'));
const binOff = 20 + jl + 8; const BIN = g.subarray(binOff);
await MeshoptDecoder.ready;
const bvCache = new Map();
function bv(i) {
  if (bvCache.has(i)) return bvCache.get(i);
  const v = J.bufferViews[i]; const e = v.extensions && v.extensions.EXT_meshopt_compression;
  let out;
  if (e) {
    const src = BIN.subarray(e.byteOffset || 0, (e.byteOffset || 0) + e.byteLength);
    out = new Uint8Array(e.count * e.byteStride);
    MeshoptDecoder.decodeGltfBuffer(out, e.count, e.byteStride, new Uint8Array(src), e.mode, e.filter || 'NONE');
  } else out = new Uint8Array(BIN.subarray(v.byteOffset || 0, (v.byteOffset || 0) + v.byteLength));
  bvCache.set(i, { u8: out, stride: (e ? e.byteStride : v.byteStride) || 0 });
  return bvCache.get(i);
}
function acc(i) {
  const a = J.accessors[i]; const b = bv(a.bufferView); const n = { VEC3: 3, VEC2: 2, SCALAR: 1, VEC4: 4 }[a.type];
  const CT = { 5120: [Int8Array, 1, 127], 5121: [Uint8Array, 1, 255], 5122: [Int16Array, 2, 32767], 5123: [Uint16Array, 2, 65535], 5125: [Uint32Array, 4, 0], 5126: [Float32Array, 4, 0] }[a.componentType];
  const [T, sz, mx] = CT; const stride = b.stride || n * sz; const dv = new DataView(b.u8.buffer, b.u8.byteOffset, b.u8.byteLength);
  const out = new Float64Array(a.count * n);
  for (let k = 0; k < a.count; k++) for (let c = 0; c < n; c++) {
    const o = (a.byteOffset || 0) + k * stride + c * sz; let v;
    if (T === Int8Array) v = dv.getInt8(o); else if (T === Uint8Array) v = dv.getUint8(o); else if (T === Int16Array) v = dv.getInt16(o, true);
    else if (T === Uint16Array) v = dv.getUint16(o, true); else if (T === Uint32Array) v = dv.getUint32(o, true); else v = dv.getFloat32(o, true);
    if (a.normalized && mx) v = Math.max(v / mx, -1);
    out[k * n + c] = v;
  }
  return out;
}
const R = {};
for (const nd of J.nodes) {
  if (!want.has(nd.name) || nd.mesh == null) continue;
  const t = nd.translation || [0, 0, 0], s = nd.scale || [1, 1, 1];
  const tris = [];
  for (const p of J.meshes[nd.mesh].primitives) {
    const P = acc(p.attributes.POSITION); const I = p.indices != null ? acc(p.indices) : null;
    const nv = P.length / 3; const idx = I || Array.from({ length: nv }, (_, i) => i);
    for (let k = 0; k < idx.length; k++) { const v = idx[k]; tris.push(+(P[v * 3] * s[0] + t[0]).toFixed(4), +(P[v * 3 + 1] * s[1] + t[1]).toFixed(4), +(P[v * 3 + 2] * s[2] + t[2]).toFixed(4)); }
  }
  R[nd.name] = tris;
  console.log(nd.name, tris.length / 9, 'tri');
}
fs.writeFileSync(fout, JSON.stringify(R));
