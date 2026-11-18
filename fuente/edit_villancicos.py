import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= RADIO NAVIDAD: 5 villancicos tradicionales (dominio público) en el juego de Navidad =================
# El mundo abierto sigue con las 3 canciones de Radio Vigo. Melodías tradicionales del s. XVIII-XIX, arreglo propio
# (bajo, acordes, cascabeles, campanitas), sintetizadas en directo.
r("function radioAviso(){",r"""// villancicos con arreglo arcade (chiptune): melodía de onda cuadrada con eco, arpegios rápidos, bajo de triángulo y batería de ruido
function villancico(nom,bpm,spb,pick,mel,ch){let tot=0;const EV=new Map();{let p=0;for(const[n,l]of mel){if(n)EV.set(p,[n,l]);p+=l}tot=p}
 const sm0=60/bpm/4,TRI=q=>q==='m'?[0,3,7]:q==='7'?[0,4,10]:[0,4,7];
 return{nom,bpm,bars:Math.ceil(tot*2/16)+1,paso(k,t){const Q=RADIO,rep=Math.floor(k/tot),p=k%tot;if(rep>1)return;const e=EV.get(p),bt=p-pick;
  if(bt>=0){const b=Math.floor(bt/spb),s_=bt%spb,c=ch[b%ch.length],r_=c[0],tri=TRI(c[1]);
   // bajo de triángulo en corcheas (raíz y octava)
   if(s_%2===0)musNota('triangle',mf(r_-24+(s_%4===2?12:0)),t,sm0*1.6,.16,Q.duck);
   // arpegio de 16 en 16, muy de máquina recreativa
   musNota('square',mf(r_+12+tri[(bt>>0)%3]+(rep?12:0)),t,sm0*.7,rep?.014:.011,Q.lp,(bt%2)?8:-8);
   // batería: bombo, caja de ruido y charles
   if(spb===16){if(s_===0||s_===8||s_===10&&b%2)rBombo(t,.55);if(s_===4||s_===12)rRuido(t,.1,.2,'bandpass',2200,.7)}else{if(s_===0)rBombo(t,.55);if(s_===4||s_===8)rRuido(t,.09,.16,'bandpass',2200,.7)}
   if(s_%2===1||rep)rRuido(t,.03,s_%2?.045:.03,'highpass',9000,.8);if(s_===0&&b%4===0)rRuido(t,.4,.06,'highpass',6000,.5)}
  if(e){const[n,l]=e,d=sm0*l*.9,o=rep?12:0;musNota('square',mf(n+o),t,d,.05,Q.lp);musNota('square',mf(n+o),t+sm0*1.5,d,.018,Q.lp,7);if(rep)musNota('sine',mf(n+24),t,Math.min(d,.22),.022,Q.lp);else musNota('triangle',mf(n+12),t,Math.min(d,.18),.02,Q.lp)}}}}
const VILLANCICOS=[
 villancico('Cascabeles (Jingle Bells)',152,16,0,[[62,4],[71,4],[69,4],[67,4],[62,12],[62,2],[62,2],[62,4],[71,4],[69,4],[67,4],[64,16],[64,4],[72,4],[71,4],[69,4],[66,16],[74,4],[74,4],[72,4],[69,4],[71,16],
  [71,4],[71,4],[71,8],[71,4],[71,4],[71,8],[71,4],[74,4],[67,6],[69,2],[71,16],[72,4],[72,4],[72,6],[72,2],[72,4],[71,4],[71,4],[71,2],[71,2],[71,4],[69,4],[69,4],[71,4],[69,8],[74,8],
  [71,4],[71,4],[71,8],[71,4],[71,4],[71,8],[71,4],[74,4],[67,6],[69,2],[71,16],[72,4],[72,4],[72,6],[72,2],[72,4],[71,4],[71,4],[71,2],[71,2],[74,4],[74,4],[72,4],[69,4],[67,16]],
  [[55],[55],[55],[60],[60],[62],[62],[55],[55],[55],[55],[55],[60],[55],[57,'7'],[62],[55],[55],[55],[55],[60],[55],[62],[55]]),
 villancico('Al mundo paz (Joy to the World)',128,16,0,[[74,4],[73,3],[71,1],[69,6],[67,2],[66,4],[64,4],[62,6],[69,2],[71,6],[71,2],[73,6],[73,2],[74,12],[74,2],[74,2],
  [74,2],[73,2],[71,2],[69,2],[69,3],[67,1],[66,2],[74,2],[74,2],[73,2],[71,2],[69,2],[69,3],[67,1],[66,2],[66,2],[66,2],[66,2],[66,2],[66,1],[67,1],[69,6],[67,1],[66,1],
  [64,2],[64,2],[64,2],[64,1],[66,1],[67,6],[66,1],[64,1],[62,2],[74,4],[71,2],[69,3],[67,1],[66,2],[67,2],[66,4],[64,4],[62,8]],
  [[62],[62],[67],[62],[62],[62],[62],[57],[62],[62]]),
 villancico('Os deseamos feliz Navidad',150,12,4,[[62,4],[67,4],[67,2],[69,2],[67,2],[66,2],[64,4],[64,4],[64,4],[69,4],[69,2],[71,2],[69,2],[67,2],[66,4],[62,4],[62,4],[71,4],[71,2],[72,2],[71,2],[69,2],[67,4],[64,4],[62,2],[62,2],[64,4],[69,4],[66,4],[67,8],
  [62,4],[67,4],[67,4],[67,4],[66,8],[66,4],[67,4],[66,4],[64,4],[62,8],[69,4],[71,4],[69,4],[67,4],[74,4],[62,4],[62,2],[62,2],[64,4],[69,4],[66,4],[67,12]],
  [[55],[60],[62],[62],[64],[60],[62],[55],[55],[62],[60],[62],[64],[60],[62],[55]]),
 villancico('Ding Dong, campanas en el cielo',140,16,0,[[67,4],[67,4],[69,2],[67,2],[66,2],[64,2],[62,12],[62,4],[64,4],[67,4],[67,4],[66,4],[67,12],[67,4],
  [67,4],[67,4],[69,2],[67,2],[66,2],[64,2],[62,12],[62,4],[64,4],[67,4],[67,4],[66,4],[67,16],
  [74,6],[72,2],[71,2],[72,2],[74,2],[71,2],[72,6],[71,2],[69,2],[71,2],[72,2],[69,2],[71,6],[69,2],[67,2],[69,2],[71,2],[67,2],[69,6],[67,2],[66,2],[67,2],[69,2],[66,2],
  [67,2],[69,2],[71,4],[69,4],[66,4],[67,16]],
  [[55],[62],[60],[55],[55],[62],[60],[55],[62],[60],[64,'m'],[62],[55],[55]]),
 villancico('Fa la la (Deck the Halls)',140,16,0,[[72,6],[70,2],[69,4],[67,4],[65,4],[67,4],[69,4],[65,4],[67,2],[69,2],[70,2],[67,2],[69,6],[67,2],[65,4],[64,4],[65,8],
  [72,6],[70,2],[69,4],[67,4],[65,4],[67,4],[69,4],[65,4],[67,2],[69,2],[70,2],[67,2],[69,6],[67,2],[65,4],[64,4],[65,8],
  [67,6],[69,2],[70,4],[67,4],[69,6],[70,2],[72,4],[67,4],[69,2],[71,2],[72,4],[74,2],[76,2],[77,4],[76,4],[74,4],[72,8],
  [72,6],[70,2],[69,4],[67,4],[65,4],[67,4],[69,4],[65,4],[74,2],[74,2],[74,2],[74,2],[72,6],[70,2],[69,4],[67,4],[65,8]],
  [[53],[53],[58],[53],[53],[53],[58],[53],[60],[53],[60],[60],[53],[53],[58],[53]])];
if(window.SOLO_NAVIDAD){CANCIONES.length=0;CANCIONES.push(...VILLANCICOS);RADIO.i=RADIO.i%CANCIONES.length}
function radioAviso(){""")
r("mostrar(RADIO.on?'📻 Radio Vigo · '","mostrar(RADIO.on?(window.SOLO_NAVIDAD?'🎄 Radio Navidad · ':'📻 Radio Vigo · ')")
# en el juego de Navidad no suena ninguna música antigua: ni la de carrera; la radio (solo villancicos) suena siempre
r("function musTick(){if(!MUS.run||!AC)return;","function musTick(){if(!MUS.run||!AC)return;if(window.SOLO_NAVIDAD){if(MUS.g)MUS.g.gain.setTargetAtTime(0,AC.currentTime,.1);return}")
r("play=RADIO.on&&driving&&!RACE.on&&soundOn;","play=RADIO.on&&driving&&(!RACE.on||!!window.SOLO_NAVIDAD)&&soundOn;")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok villancicos')
