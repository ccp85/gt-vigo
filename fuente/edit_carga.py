import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---------------- carga más rápida
# 1) three.js minificado (pesa la mitad)
r('"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"','"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js"')
# 2) los JSON grandes viajan comprimidos dentro de un PNG (X.json → X_json.png, ~4-5 veces menos); si falta el PNG, se usa el .json
r("async function pngBytesAsync(buf){",r"""const JPNG=/^(vigo_(trafico|mobiliario|extras|calles|fondo|zonas|circuito|circuito_facil|circuito_navidad|fachadas|costuras)|[a-z0-9]+_inst)\.json$/;
{const f0=window.fetch.bind(window);window.fetch=async(u,o)=>{if(typeof u==='string'&&JPNG.test(u)){try{const r=await f0(u.replace(/\.json$/,'_json.png'),o);if(r.ok){const b=await pngBytesAsync(await r.arrayBuffer());return new Response(b,{status:200,headers:{'Content-Type':'application/json'}})}}catch(e){console.warn('json.png',u,e)}}return f0(u,o)}}
async function pngBytesAsync(buf){""")
# 4) porcentaje de descarga en el botón del menú y en el aviso de carga
r("return {pj,bufs:await Promise.all(rs.map(r=>r.arrayBuffer()))}})()","return {pj,bufs:await Promise.all(rs.map((r,i)=>leerProg(r,id,i)))}})()")
r("const PRE={};function precargar(id){",r"""const DLP={};
async function leerProg(r,id,i){const tot=+r.headers.get('content-length')||0;if(!r.body||!tot)return r.arrayBuffer();const D=DLP[id]=DLP[id]||{g:{},t:{}};D.t[i]=tot;D.g[i]=0;
 const rd=r.body.getReader(),out=new Uint8Array(tot);let n=0;for(;;){const{done,value}=await rd.read();if(done)break;if(n+value.length>out.length){const o2=new Uint8Array(Math.max(out.length*2,n+value.length));o2.set(out.subarray(0,n));return finLeer(rd,o2,n,value,id,i)}out.set(value,n);n+=value.length;D.g[i]=n;dlPinta(id)}
 D.g[i]=tot;_dlT=0;dlPinta(id);return out.buffer.slice(0,n)}
async function finLeer(rd,o,n,v,id,i){let out=o;out.set(v,n);n+=v.length;for(;;){const{done,value}=await rd.read();if(done)break;if(n+value.length>out.length){const o2=new Uint8Array((n+value.length)*2);o2.set(out.subarray(0,n));out=o2}out.set(value,n);n+=value.length}return out.buffer.slice(0,n)}
function dlPct(id){const D=DLP[id];if(!D)return null;let g=0,t=0;for(const k in D.t){g+=D.g[k];t+=D.t[k]}return t?Math.min(100,Math.round(g/t*100)):null}
let _dlT=0;function dlPinta(id){const now=performance.now();if(now-_dlT<150)return;_dlT=now;const p=dlPct(id);if(p==null)return;
 const bJ=document.getElementById('selzJugar');if(id==='centro'&&bJ&&!document.getElementById('selz').hidden)bJ.textContent=p<100?'▶ Mundo abierto · '+p+'%':'▶ Mundo abierto';
 const st=document.getElementById('stream');if(st&&!st.hidden&&/^Cargando/.test(st.textContent))st.textContent=st.textContent.replace(/ · \d+%$/,'').replace(/…$/,'')+'… · '+p+'%';
 const lm=document.getElementById('load');if(lm&&!lm.hidden&&/^Cargando|^Descargando/.test(lm.textContent||''))lm.textContent=(lm.textContent||'').replace(/ · \d+%$/,'')+' · '+p+'%'}
const PRE={};function precargar(id){""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok carga')
