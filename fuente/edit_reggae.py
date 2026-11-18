import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= RADIO VIGO: 5 SINGLES DE REGGAE (composición propia) =================
# One drop / steppers, skank en los tiempos 2 y 4, burbuja de órgano, bajo melódico y melódica.
# Solo en el mundo abierto (en el juego de Navidad la radio sigue siendo solo de villancicos).
r("function radioAviso(){",r"""function reggae(nom,bpm,tono,acordes,bajo,mel,op){op=op||{};const bars=48;
 const TRI=q=>q==='m'?[0,3,7]:q==='M7'?[0,4,7,11]:q==='m7'?[0,3,7,10]:[0,4,7];
 return{nom,bpm,bars,paso(k,t){const Q=RADIO,sm=60/bpm/4,s_=k%16,b=Math.floor(k/16),c=acordes[b%acordes.length],r_=tono+c[0],tri=TRI(c[1]);
  const intro=b<4,rompe=b>=28&&b<32,fin=b>=44,mel_on=b>=8&&!rompe;
  if(s_===0&&b%4===0)Q.wet.gain.setValueAtTime(op.dub?.5:.22,t),Q.fb.gain.setValueAtTime(op.dub?.48:.3,t);
  // batería: one drop (bombo y aro en el 3) o steppers (bombo en negras)
  if(!rompe){if(op.steppers?s_%4===0:s_===8)rBombo(t,.7);if(s_===8)rRuido(t,.06,.2,'bandpass',1900,3);
   if(s_%2===0)rRuido(t,.025,s_%4===2?.05:.03,'highpass',8500,.7);if(s_===14&&b%2)rRuido(t,.12,.04,'highpass',7000,.5);
   if(b%8===7&&s_>=12)rRuido(t,.05,.12,'bandpass',900+s_*60,2)}
  // bajo
  if(!fin||s_<8)for(const[st,iv,l]of bajo)if(st===s_)musNota('triangle',mf(r_-24+iv),t,sm*l*.9,.2,Q.duck),musNota('sine',mf(r_-36+iv),t,sm*l*.9,.12,Q.duck);
  // skank (2 y 4) y burbuja de órgano
  if(!intro){if(s_===4||s_===12)for(const d of tri)musNota('square',mf(r_+d),t,sm*.55,.022,Q.lp,d?6:-6);
   if(s_%4===2||s_%4===3)musNota('sawtooth',mf(r_+tri[s_%4===2?0:1]-12+(s_%8>3?12:0)),t,sm*.5,.012,Q.lp)}
  // melódica
  if(mel_on){const L=mel.length?32:0,ph=k%32;for(const[st,n,l]of mel)if(st===ph)musNota(op.lead||'square',mf(tono+12+n+((b>=16&&b<24)||b>=36?12:0)),t,sm*l*.92,.05,Q.lp,4),musNota('triangle',mf(tono+n),t,sm*l*.92,.025,Q.lp)}}}}
const REGGAE=[
 reggae('Reggae da Ría',74,57,[[0,'m'],[5,'m'],[0,'m'],[7,'m']],[[0,0,3],[3,0,1],[6,7,2],[8,12,2],[10,10,2],[12,7,3],[15,5,1]],
  [[0,7,4],[4,10,2],[6,12,4],[12,10,2],[14,7,2],[16,5,6],[22,3,2],[24,5,4],[28,0,4]]),
 reggae('Samil Sound System',78,55,[[0],[5],[7],[5]],[[0,0,4],[6,4,2],[8,7,3],[11,9,1],[12,7,2],[14,4,2]],
  [[0,4,2],[2,7,2],[4,9,4],[10,7,2],[12,4,4],[16,2,2],[18,4,2],[20,7,6],[28,4,2],[30,2,2]]),
 reggae('Rastas en Bouzas',80,50,[[0,'m'],[5,'m'],[8],[7]],[[0,0,2],[2,0,2],[4,7,2],[6,0,2],[8,0,2],[10,3,2],[12,7,2],[14,5,2]],
  [[0,0,2],[2,3,2],[4,5,4],[8,7,6],[16,8,2],[18,7,2],[20,5,4],[24,3,4],[28,2,4]],{steppers:true}),
 reggae('Cíes Dub',70,52,[[0,'m'],[0,'m'],[8],[10]],[[0,0,6],[7,7,1],[8,12,4],[13,10,1],[14,7,2]],
  [[0,12,6],[8,10,2],[10,7,6],[20,5,2],[22,7,8]],{dub:true,lead:'triangle'}),
 reggae('Bus de Coia',82,48,[[0],[9,'m'],[5],[7]],[[0,0,3],[3,0,1],[4,7,2],[8,12,2],[10,7,2],[12,4,2],[14,2,2]],
  [[0,7,2],[2,9,2],[4,12,4],[8,9,2],[10,7,2],[12,4,4],[16,5,2],[18,4,2],[20,2,4],[24,0,2],[26,2,2],[28,4,4]])];
CANCIONES.push(...REGGAE);
function radioAviso(){""")
r("else if(v!==null)RADIO.i=(+v||0)%3","else if(v!==null)RADIO.i=(+v||0)%10")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok reggae')
