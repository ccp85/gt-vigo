import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ================= RADIO VIGO: tres canciones originales (sintetizadas) mientras conduces fuera de las carreras =================
s=s.replace('</style>','body.drive .bar #bRadio{display:inline-block!important}body.carrera .bar #bRadio{display:none!important}#bRadio.off{opacity:.55}\n</style>',1)
r('<button id="bFull" title="Pantalla completa" aria-label="Pantalla completa">⛶</button>','<button id="bFull" title="Pantalla completa" aria-label="Pantalla completa">⛶</button>\n  <button id="bRadio" style="display:none" title="Radio: cambiar canción (M)" aria-label="Radio">📻</button>')
r("setTimeout(()=>{const b=document.getElementById('rMus');",r"""// ---------- Radio Vigo
const RADIO={i:0,on:true,run:false,k:0,t:0,g:null};window.__RADIO=RADIO;
try{const v=localStorage.getItem('gtvigo_radio');if(v==='off')RADIO.on=false;else if(v!==null)RADIO.i=(+v||0)%3}catch(e){}
function radNodos(){if(RADIO.g||!AC||!master)return;const Q=RADIO;Q.g=AC.createGain();Q.g.gain.value=0;Q.g.connect(master);
 Q.duck=AC.createGain();Q.duck.connect(Q.g);Q.lp=AC.createBiquadFilter();Q.lp.type='lowpass';Q.lp.frequency.value=3200;Q.lp.Q.value=2;Q.lp.connect(Q.duck);
 Q.dl=AC.createDelay(1);Q.fb=AC.createGain();Q.fb.gain.value=.3;Q.wet=AC.createGain();Q.wet.gain.value=.25;Q.lp.connect(Q.dl);Q.dl.connect(Q.fb);Q.fb.connect(Q.dl);Q.dl.connect(Q.wet);Q.wet.connect(Q.g);
 Q.gai=AC.createBiquadFilter();Q.gai.type='bandpass';Q.gai.frequency.value=1500;Q.gai.Q.value=.9;Q.gai.connect(Q.lp)}
function rBombo(t,v){const o=AC.createOscillator(),g=AC.createGain();o.frequency.setValueAtTime(150,t);o.frequency.exponentialRampToValueAtTime(45,t+.13);g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+.3);o.connect(g);g.connect(RADIO.g);o.start(t);o.stop(t+.33);
 RADIO.duck.gain.cancelScheduledValues(t);RADIO.duck.gain.setValueAtTime(.4,t);RADIO.duck.gain.linearRampToValueAtTime(1,t+.2)}
function rRuido(t,d,v,tipo,fq,q=1){const z=AC.createBufferSource();z.buffer=NB;const fl=AC.createBiquadFilter();fl.type=tipo;fl.frequency.value=fq;fl.Q.value=q;const g=AC.createGain();g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+d);z.connect(fl);fl.connect(g);g.connect(RADIO.g);z.start(t,Math.random()*1.5);z.stop(t+d+.05)}
const MEL1=[[[0,74,3],[4,72,2],[6,69,2],[8,72,4],[12,74,4]],[[0,77,6],[8,74,2],[10,72,2],[12,70,4]],[[0,72,3],[4,69,2],[6,72,2],[8,77,4],[12,76,4]],[[0,76,8],[8,72,4],[12,67,4]]];
const GAITA=[[74,78,81,78,74,78,81,83],[84,83,81,79,78,76,74,76],[78,81,86,84,83,81,79,78],[76,79,78,76,74,0,74,0]];
const CANCIONES=[
 {nom:'Noite na Ría',bpm:96,bars:64,paso(k,t){const s=k%16,b=Math.floor(k/16),Q=RADIO,sm=60/96/4,ac=[[62,65,69],[58,62,65],[60,65,69],[60,64,67]][b%4],intro=b<4;
  if(s===0||s===8)rBombo(t,.8);if(!intro&&(s===4||s===12))rRuido(t,.25,.33,'bandpass',1400,.7);if(s%2===1)rRuido(t,.04,.06,'highpass',9000);
  if(s%2===0){const n=ac[0]-24+(s%4===2?12:0);musNota('sawtooth',mf(n),t,sm*1.8,.12,Q.duck)}
  if(s===0)for(const n of ac)for(const de of[-12,12])musNota('sawtooth',mf(n),t,sm*15,.017,Q.duck,de);
  if(b>=8)musNota('square',mf(ac[s%3]+12),t,sm*.8,.018,Q.lp,s%2?6:-6);
  if(!intro){const up=b%8>=4;for(const[st,n,l] of MEL1[b%4])if(st===s)musNota(up?'triangle':'square',mf(n+(up?12:0)),t,sm*l*.95,up?.06:.04,Q.lp)}}},
 {nom:'Funk de Bouzas',bpm:112,bars:64,paso(k,t){const s=k%16,b=Math.floor(k/16),Q=RADIO,sm=60/112/4,dos=b%2===1,root=dos?45:40;
  if(s===0||s===7||s===10)rBombo(t,.85);if(b>=1&&(s===4||s===12))rRuido(t,.16,.4,'bandpass',1900,.9);
  rRuido(t,.03,s%2?.045:.08,'highpass',8000);if(s===14)rRuido(t,.18,.07,'highpass',7000);
  const BL=[0,null,12,null,null,0,null,10,12,null,7,null,0,null,10,12],o=BL[s];if(o!=null)musNota('sawtooth',mf(root+o),t,sm*(o===0?1.6:.9),.15,Q.duck);
  const ch=dos?[61,64,67,71]:[64,67,71,74];if(b>=2&&(s===2||s===6||s===11||s===14))for(const n of ch)musNota('square',mf(n),t,sm*.7,.018,Q.lp,s%2?5:-5);
  if(b>=4&&b%4===3)for(const[st,n] of [[0,76],[2,79],[4,81],[7,79],[10,76],[12,74]])if(st===s){musNota('sawtooth',mf(n),t,sm*1.6,.045,Q.lp,-7);musNota('sawtooth',mf(n),t,sm*1.6,.045,Q.lp,7)}
  if(b>=8&&b%8<3)for(const[st,n] of [[0,83],[3,81],[6,79],[8,76],[11,79],[14,81]])if(st===s)musNota('triangle',mf(n),t,sm*2.4,.055,Q.lp)}},
 {nom:'Muiñeira Turbo',bpm:128,bars:64,paso(k,t){const s=k%16,b=Math.floor(k/16),Q=RADIO,sm=60/128/4,r_=[50,50,48,43,50,50,48,50][b%8],intro=b<2;
  if(s%4===0)rBombo(t,intro?.5:.8);if(!intro&&(s===4||s===12))rRuido(t,.14,.3,'bandpass',2200,.8);
  if(s%2===0)rRuido(t,.06,s%4===0?.1:.06,'bandpass',6500,1.5);                                   // pandeireta
  if(!intro&&s%2===0)musNota('sawtooth',mf(r_-12+(s%4===2?7:0)),t,sm*1.7,.11,Q.duck);              // baixo: raíz e quinta
  if(s===0&&b%2===0){musNota('sawtooth',mf(50),t,sm*32,.03,Q.gai,-4);musNota('sawtooth',mf(57),t,sm*32,.024,Q.gai,4)}   // ronco da gaita
  if(b>=2&&s%2===0){const G=GAITA[b%4][s/2];if(G){musNota('square',mf(G),t,sm*1.9,.042,Q.gai);musNota('sawtooth',mf(G),t,sm*1.9,.028,Q.gai,8)}}}}];
function radioGuarda(){try{localStorage.setItem('gtvigo_radio',RADIO.on?String(RADIO.i):'off')}catch(e){}const b=document.getElementById('bRadio');if(b)b.classList.toggle('off',!RADIO.on)}
function radioAviso(){try{mostrar(RADIO.on?'📻 Radio Vigo · '+(RADIO.i+1)+'/'+CANCIONES.length+' · «'+CANCIONES[RADIO.i].nom+'» · M cambia':'📻 Radio apagada · M para encenderla')}catch(e){}}
function radioSig(){if(!RADIO.on){RADIO.on=true;RADIO.i=0}else if(RADIO.i>=CANCIONES.length-1)RADIO.on=false;else RADIO.i++;RADIO.run=false;
 if(!RADIO.on&&RADIO.g)RADIO.g.gain.setTargetAtTime(0,AC.currentTime,.1);radioGuarda();radioAviso()}
function radioTick(){if(!AC||!master)return;radNodos();if(!RADIO.g)return;const ct=AC.currentTime,play=RADIO.on&&driving&&!RACE.on&&soundOn;
 if(!play){if(RADIO.run){RADIO.run=false;RADIO.g.gain.setTargetAtTime(0,ct,.3)}return}
 const S=CANCIONES[RADIO.i],sm=60/S.bpm/4;
 if(!RADIO.run){RADIO.run=true;RADIO.k=0;RADIO.t=ct+.1;RADIO.dl.delayTime.setValueAtTime(60/S.bpm*.75,ct);RADIO.g.gain.cancelScheduledValues(ct);RADIO.g.gain.setTargetAtTime(.42,ct,.4);if(!RADIO.dicho){RADIO.dicho=1;setTimeout(radioAviso,2500)}}
 if(RADIO.t<ct-.2)RADIO.t=ct+.02;
 while(RADIO.t<ct+.22){S.paso(RADIO.k,RADIO.t);RADIO.k++;RADIO.t+=sm;if(RADIO.k>=16*S.bars){RADIO.i=(RADIO.i+1)%CANCIONES.length;RADIO.run=false;radioGuarda();radioAviso();return}}
 RADIO.g.gain.setTargetAtTime(MODO==='heli'?.3:.42,ct,.3)}
setInterval(radioTick,40);
addEventListener('keydown',e=>{if(driving&&!RACE.on&&e.code==='KeyM'&&!e.repeat)radioSig()});
{const b=document.getElementById('bRadio');if(b){b.onclick=e=>{e.stopPropagation();radioSig()};b.classList.toggle('off',!RADIO.on)}}
setTimeout(()=>{const b=document.getElementById('rMus');""")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok radio')
