(async()=>{const L=await (await fetch('vigo_calles.json')).json();const T=__V.THREE;const rc=new T.Raycaster();const dn=new T.Vector3(0,-1,0),o=new T.Vector3();
const hit=(x,y)=>{o.set(x,8,y);rc.set(o,dn);rc.far=20;const h=rc.intersectObjects(__GR,false);if(!h.length)return null;let b=h[0];for(const q of h)if(q.point.y>b.point.y)b=q;return [b.object.name||(b.object.parent&&b.object.parent.name)||'?',b.point.y]};
const ROAD=n=>/^(calzada|lineas|labio|puente_tablero|aceras|costuras)/.test(n);
const bld=(x,y)=>{try{const ms=__dbg.rm(x,y);if(!ms.length)return 0;const g=hit(x,y);const a=__dbg.ra(x,y,ms);return (a==null||!g)?0:Math.max(0,a-g[1])}catch(e){return -1}};
const lines=[];
for(const [n,c,ls] of L){if(n!=='Autoestrada do Atlántico')continue;for(const l of ls){const P=[];for(let i=0;i+1<l.length;i+=2)P.push([l[i],l[i+1]]);if(Math.max(...P.map(p=>p[1]))>29)continue;lines.push(P)}}
lines.push([[145.98,-36.93],[145.35,-43.23]]);lines.push([[145.28,-43.23],[145.91,-36.95]]);
const out=[];
lines.forEach((P,k)=>{const S=[];let carry=0;
 for(let i=0;i<P.length-1;i++){const a=P[i],b=P[i+1],LL=Math.hypot(b[0]-a[0],b[1]-a[1]);if(LL<1e-6)continue;const tx=(b[0]-a[0])/LL,ty=(b[1]-a[1])/LL,nx=-ty,ny=tx;
  let s=carry;for(;s<LL;s+=.05){const x=a[0]+tx*s,y=a[1]+ty*s;const c0=hit(x,y);
   const row=[+x.toFixed(3),+y.toFixed(3),c0?+c0[1].toFixed(3):null,c0?c0[0][0]:'-'];
   for(const sd of[1,-1]){let d=.01,bar=0;for(;d<.6;d+=.01){const h=hit(x+nx*sd*d,y+ny*sd*d);const nm=h?h[0]:'-';if(nm.startsWith('baranda')){bar=1;continue}if(!ROAD(nm))break}
    let f=d;for(;f<d+.5;f+=.02){const h=hit(x+nx*sd*f,y+ny*sd*f);if(!h||!/^(tierra|verde)/.test(h[0]))break}
    const hz=[.03,.1,.2].map(e=>{const h=hit(x+nx*sd*(d+e),y+ny*sd*(d+e));return h&&c0?+(h[1]-c0[1]).toFixed(3):null});
    const bh=sd>0?Math.max(...[.06,.15,.3].map(e=>bld(x+nx*sd*(d+e),y+ny*sd*(d+e)))):0;
    row.push(+d.toFixed(2),+(f-d).toFixed(2),hz,bar,+bh.toFixed(3))}
   S.push(row)}carry=s-LL}
 out.push({k,P,S})});
return JSON.stringify(out)})()
