f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= SKATE 3: SALTOS GUIADOS, NUNCA A LA CALLE =================
# Al llegar al borde de un tejado se busca el tejado más cercano en la dirección en la que vas (con un margen a los
# lados): el salto te lleva siempre hasta él. Si en esa dirección no hay ninguno, te frenas en el borde y eliges otro
# girando con ◀ ▶. Nunca se pisa la calle: si un paso fuera a sacarte del tejado, no se da.
r("function skateSalta(){",r"""function skDestino(x,y,a,z){let best=null;for(const da of[0,.14,-.14,.28,-.28,.42,-.42]){for(let d=.08;d<=1.05;d+=.025){const px=x+Math.cos(a+da)*d,py=y-Math.sin(a+da)*d,h=skAlt(px,py);
   if(!h[1])continue;if(h[0]>z+.3)break;const q=skAlt(px+Math.cos(a+da)*.035,py-Math.sin(a+da)*.035);if(!q[1])continue;
   const sc=d+Math.abs(da)*.9;if(!best||sc<best.sc)best={x:px,y:py,z:h[0],d,sc,a:a+da};break}}return best}
function skVuelo(L){const S=SKT;S.guiado={t:0,D:.42+L.d*.55,x0:S.x,y0:S.y,z0:S.z,x1:L.x,y1:L.y,z1:L.z,H:.07+L.d*.16+Math.max(0,L.z-S.z)};S.air=true;S.spin=0;S.flip=0;S.a=Math.atan2(-(L.y-S.y),L.x-S.x);try{bip(520,.06,.05)}catch(e){}}
function skGuiado(dt){const S=SKT,G_=S.guiado;G_.t+=dt;const k=Math.min(1,G_.t/G_.D);
 S.x=G_.x0+(G_.x1-G_.x0)*k;S.y=G_.y0+(G_.y1-G_.y0)*k;S.z=G_.z0+(G_.z1-G_.z0)*k+Math.sin(Math.PI*k)*G_.H;
 if(keys.left)S.spin+=dt*11;if(keys.right)S.spin-=dt*11;if(keys.down)S.flip+=dt*10;
 if(k>=1){S.guiado=null;S.air=false;S.z=G_.z1;S.v=Math.max(S.v,.45);const g=Math.floor(Math.abs(S.spin)/5.6),fl=Math.floor(S.flip/5.6);
  if(g||fl){const pts=(g*50+fl*80)*(1+S.combo*.5);S.combo++;REP.pts+=Math.round(pts);repPop((fl?'🛹 Kickflip ':'')+(g?g*360+'° ':'')+'+'+Math.round(pts)+(S.combo>1?' · combo x'+S.combo:''),'aviso');try{bip(880,.08,.05)}catch(e){}}else S.combo=0;
  S.spin=0;S.flip=0;REP.shake=.1;S.safe=[S.x,S.y,S.a,S.z]}}
function skateSalta(){const S=SKT;if(S.fase!=='patina'||S.air||S.cae>0||S.guiado)return;const L=skDestino(S.x,S.y,S.a,S.z);if(L&&L.d>.12){skVuelo(L);return}S.air=true;S.vz=.7;S.v=0;S.spin=0;S.flip=0;try{bip(520,.06,.05)}catch(e){}}
function skateSaltaViejo(){""")
r("if(S.fase==='vuelta'){skVuelta(dt);return}","if(S.fase==='vuelta'){skVuelta(dt);return}if(S.guiado){skGuiado(dt);for(const c of S.chim)c.ar.rotation.z=tn*2;skColoca(dt,tn);return}")
r("const dx=Math.cos(S.a),dy=-Math.sin(S.a),nx=S.x+dx*S.v*dt","const ox_=S.x,oy_=S.y,dx=Math.cos(S.a),dy=-Math.sin(S.a),nx=S.x+dx*S.v*dt")
r("const h=skAlt(S.x,S.y);","let h=skAlt(S.x,S.y);if(!S.air&&!h[1]){S.x=ox_;S.y=oy_;S.v=0;h=skAlt(S.x,S.y)}")
r("if(h[0]<S.z-.03){S.air=true;S.vz=0}else S.z+=(h[0]-S.z)*Math.min(1,dt*18);","S.z+=(h[0]-S.z)*Math.min(1,dt*(h[0]<S.z?12:18));")
r("{const e2=skAlt(S.x+dx*.05,S.y+dy*.05);if(!e2[1]&&h[1]&&S.v>.2){skateSalta();if(!S.avS||tn-S.avS>3){S.avS=tn;aviso('⤒ ¡Salto!',.5,'peq')}}}",
  "{const e2=skAlt(S.x+dx*.05,S.y+dy*.05);if(!e2[1]&&h[1]){const L=skDestino(S.x,S.y,S.a,S.z);if(L&&L.d>.06){skVuelo(L)}else{S.v=0;S.x-=dx*.01;S.y-=dy*.01;if(!S.avB||tn-S.avB>2.2){S.avB=tn;aviso('◀ ▶ Gira hacia otro tejado',1,'peq')}}}}")
r("if(!S.air&&hn[0]-S.z<.2){S.air=true;S.vz=Math.sqrt(2*2.3*(hn[0]-S.z+.04));S.spin=0;S.flip=0;S.x=nx;S.y=ny}",
  "if(!S.air&&hn[0]-S.z<.2){const q=skAlt(nx+dx*.06,ny+dy*.06);if(q[1]&&q[0]>S.z+.02)skVuelo({x:nx+dx*.06,y:ny+dy*.06,z:q[0],d:.08});else{S.v=0;S.a+=Math.PI*.9}}")
r("S.cae=1.1;S.combo=0;S.v=0;aviso('😵 ¡A la calle! Vuelves al último tejado',1.3,'peq');REP.shake=.35;try{bip(200,.25,.08)}catch(e){}",
  "[S.x,S.y,S.a,S.z]=S.safe;S.air=false;S.vz=0;S.v=.3;S.combo=0;S.spin=0;S.flip=0;camInit=false")
r("Math.hypot(c.x-S.x,c.y-S.y)<.085&&S.z<c.h+.2","Math.hypot(c.x-S.x,c.y-S.y)<.12&&S.z<c.h+.3")
open(f,'w').write(s)
print('ok skate3')
