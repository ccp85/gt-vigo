// ---------- algas que se mecen con el mar de fondo (gpu_algas.js, solo gpu.html) ----------
// Laminarias, praderas de zostera y anémonas del fondo marino (fondomar.js). Antes se movían cada una hacia su lado y, en el
// motor nuevo, con un vaivén calculado ya a la escala del mundo (demasiado grande para las pequeñas). Ahora:
//  · el mar de fondo las lleva a todas a la vez adelante y atrás (el vaivén de las olas llega al fondo y pasa como una onda),
//    más fuerte cuanto menos hondo, y la corriente las tumba un poco hacia un lado;
//  · cada hoja ondea con su propio aleteo y se dobla más cuanto más arriba, sin estirarse;
//  · al pasar nadando entre ellas se apartan y se quedan agitándose (más si vas rápido).
// En la ría de Vigo no hay posidonia (es del Mediterráneo): su pariente atlántica es la zostera, que ya estaba en el fondo.
const ALG={u:null};window.__ALG=ALG;
GT.instM=()=>TSL.Fn(bd=>{const o=bd.object,T=TSL;if(!o||!o.isInstancedMesh||!o.instanceMatrix)return T.mat4(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1);
 const f=o.instanceMatrix.usage===THREE.DynamicDrawUsage?T.instancedDynamicBufferAttribute:T.instancedBufferAttribute;
 return T.mat4(...[0,4,8,12].map(k=>f(new THREE.InterleavedBufferAttribute(o.instanceMatrix,4,k))))})();
function gpuAlga(m,uT,uWY,iph){const T=TSL,{vec2,vec3,float,sin,cos,exp,max,min,smoothstep,length,dot,positionLocal,positionGeometry}=T;
 if(!ALG.u)ALG.u={uN:T.uniform(new THREE.Vector4(0,-99,0,0)),uV:T.uniform(0)};const uN=ALG.u.uN,uV=ALG.u.uV;
 const M=GT.instM(),h=length(M.element(1).xyz),base=M.element(3).xyz,p=positionLocal;
 const hh=max(positionGeometry.y,0),bend=hh.mul(hh),dir=vec2(.82,.57),perp=vec2(-.57,.82);
 const hondo=max(uWY.sub(base.y),0),olas=exp(hondo.mul(-7)).mul(.75).add(.25);
 const fase=uT.mul(.85).sub(dot(base.xz,dir).mul(9));                       // el vaivén viaja con la ola
 const vaiven=sin(fase).mul(.55).add(sin(fase.mul(2.1).add(1.3)).mul(.12)).mul(olas);
 const corriente=GT.vn(base.xz.mul(4).add(uT.mul(.03))).mul(.25).add(.12);
 const aleteo=sin(uT.mul(2.6).add(iph.mul(2)).add(hh.mul(5))).mul(.14).add(sin(uT.mul(5.3).add(iph.mul(5)).add(hh.mul(11))).mul(.04));
 // nadador cerca: las hojas se apartan y se agitan
 const d3=p.sub(uN.xyz),dl=length(d3.xz),dv=d3.y.abs();
 const cerca=smoothstep(.06,.012,dl).mul(smoothstep(.05,.01,dv)).mul(uN.w),apart=d3.xz.div(max(dl,1e-5));
 const agita=sin(uT.mul(9).add(iph.mul(3)).add(hh.mul(7))).mul(uV.mul(.5).add(.15));
 const lado=vec2(dir.mul(vaiven.add(corriente))).add(perp.mul(aleteo)).mul(.5);
 const off=lado.add(apart.mul(cerca).mul(agita.add(.9))).mul(bend).mul(h);
 const y=dot(off,off).div(max(h.mul(1.6),1e-5));                              // se doblan, no se estiran
 m.positionNode=p.add(vec3(off.x,y.negate(),off.y))}
function algasTick(){const A=ALG.u;if(!A)return;const on=MODO==='nado'?1:0;
 A.uN.value.set(P.x,P.z||0,P.y,on);A.uV.value=Math.min(1,Math.abs(P.v||0)/.15)}
// ---------- fin de gpu_algas.js
