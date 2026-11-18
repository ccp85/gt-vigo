import re
f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
r("function bip(f,d=.18,v=.18){","""// ---- efectos de Navidad (todo sintetizado): motor de la carroza, cascabeles, público, campanadas y «¡Jo, jo, jo!»
const SFX={};
function sfxRuido(t0,dur,f0,q,vol,tipo='bandpass'){const s=AC.createBufferSource(),f=AC.createBiquadFilter(),g=AC.createGain();s.buffer=NB;s.loop=true;f.type=tipo;f.frequency.value=f0;f.Q.value=q;env(g,t0,.02,vol,dur);s.connect(f);f.connect(g);g.connect(master);s.start(t0,Math.random()*1.5);s.stop(t0+dur+.1)}
function sonCascabel(v=.05){if(!AC||!soundOn)return;const t0=AC.currentTime;for(let k=0;k<2;k++){const t=t0+k*.04+Math.random()*.012;for(const f of[2600,3920,5230]){const o=AC.createOscillator(),g=AC.createGain();o.type='sine';o.frequency.value=f*(1+(Math.random()-.5)*.03);env(g,t,.002,v*2600/f,.16);o.connect(g);g.connect(master);o.start(t);o.stop(t+.22)}}}
function sonCampana(n=3,gap=.9){if(!AC||!soundOn)return;const t0=AC.currentTime+.05;for(let k=0;k<n;k++){const t=t0+k*gap;for(const[f,a,d]of[[392,.16,2.6],[784,.07,1.7],[1176,.05,1.1],[523,.05,1.9],[985,.03,.8]]){const o=AC.createOscillator(),g=AC.createGain();o.type='sine';o.frequency.value=f;env(g,t,.004,a,d);o.connect(g);g.connect(master);o.start(t);o.stop(t+d+.1)}}}
function sonJoJo(){if(!AC||!soundOn)return;const t0=AC.currentTime+.05;for(let k=0;k<3;k++){const t=t0+k*.27,o=AC.createOscillator(),f1=AC.createBiquadFilter(),f2=AC.createBiquadFilter(),g=AC.createGain(),g2=AC.createGain();o.type='sawtooth';o.frequency.setValueAtTime(155-k*10,t);o.frequency.exponentialRampToValueAtTime(110-k*8,t+.22);
 f1.type='bandpass';f1.frequency.value=560;f1.Q.value=5;f2.type='bandpass';f2.frequency.value=950;f2.Q.value=7;o.connect(f1);o.connect(f2);f1.connect(g);f2.connect(g2);g2.gain.value=.6;g2.connect(g);g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.55,t+.035);g.gain.exponentialRampToValueAtTime(.001,t+.24);g.connect(master);o.start(t);o.stop(t+.3);sfxRuido(t,.05,1700,1,.05)}}
function sonPublico(f=1){if(!AC||!soundOn)return;const t0=AC.currentTime;sfxRuido(t0,1.3*f,900,.7,.09*f);sfxRuido(t0+.1,1.1*f,1700,1.2,.05*f);for(let k=0;k<Math.round(45*f);k++)sfxRuido(t0+Math.random()*1.6*f,.025,2600+Math.random()*2200,2,.05)}
function sonMotor(v,on){if(!AC)return;if(!SFX.m){if(!soundOn||!on)return;const o=AC.createOscillator(),o2=AC.createOscillator(),fl=AC.createBiquadFilter(),g=AC.createGain();o.type='sawtooth';o2.type='square';fl.type='lowpass';fl.frequency.value=500;g.gain.value=0;o.connect(fl);o2.connect(fl);fl.connect(g);g.connect(master);o.start();o2.start();SFX.m={o,o2,fl,g}}
 const m=SFX.m,t=AC.currentTime,a=Math.min(1,Math.abs(v||0)),act=on&&soundOn;m.o.frequency.setTargetAtTime(46+a*90,t,.08);m.o2.frequency.setTargetAtTime(23+a*45,t,.08);m.fl.frequency.setTargetAtTime(320+a*900,t,.1);m.g.gain.setTargetAtTime(act?.03+.045*a:0,t,.12)}
// cada fotograma: motor, cascabeles según la velocidad y, de vez en cuando, el público animando
function navSonidos(dt,zonaGente){const v=Math.abs(P.v||0);sonMotor(v,true);SFX.bT=(SFX.bT||0)-dt*Math.min(1.6,v*1.4);if(v>.12&&SFX.bT<=0){SFX.bT=.34;sonCascabel(.025+.03*Math.min(1,v))}
 SFX.pT=(SFX.pT==null?5:SFX.pT)-dt;if(SFX.pT<=0){SFX.pT=5+Math.random()*6;if(v>.4&&zonaGente)sonPublico(.55)}}
function bip(f,d=.18,v=.18){""")
# Reparto: motor/cascabeles/público; «jo jo jo» y aplausos al entregar; campanadas en el último minuto y a medianoche
r("if(!REP.heli&&!REP.fin&&REP.red){repArcadeTick(dt);","if(!REP.heli&&!REP.fin)navSonidos(dt,repEnZona(P.x,P.y));else sonMotor(0,false);\n if(!REP.heli&&!REP.fin&&REP.red){repArcadeTick(dt);")
r("sonCaja();setTimeout(sonMoneda,150);","sonCaja();setTimeout(sonMoneda,150);setTimeout(sonJoJo,260);")
r("REP.mul=Math.min(5,REP.mul+1);REP.ct=REP.cmb;REP.shake=.5;","REP.mul=Math.min(5,REP.mul+1);REP.ct=REP.cmb;REP.shake=.5;setTimeout(()=>sonPublico(n>=4?1.2:.8),700);")
r("aviso('🔔 ¡Último minuto! Puntos ×2',1.8,'cuenta')","aviso('🔔 ¡Último minuto! Puntos ×2',1.8,'cuenta');sonCampana(3,.8)")
r("const acabado=C&&REP.t<=0;","const acabado=C&&REP.t<=0;sonMotor(0,false);if(acabado)sonCampana(12,.55);else if(sc>0)sonPublico(1);")
r("function salirReparto(menu=true){","function salirReparto(menu=true){sonMotor(0,false);")
# Carrera de Navidad: motor, cascabeles y público; campanadas y aplausos en la meta
r("function navTick(dt){","function navTick(dt){if(RACE.nav&&RACE.on){if(RACE.fase==='carrera')navSonidos(dt,true);else sonMotor(0,false)}")
r("function terminar(){musPara(posicion()<=3);","function terminar(){musPara(posicion()<=3);if(RACE.nav){sonMotor(0,false);sonCampana(3,.7);setTimeout(()=>sonPublico(1.3),400);setTimeout(sonJoJo,1800)}")
r("function salirCarrera(menu=true){if(!RACE.on)return;","function salirCarrera(menu=true){if(!RACE.on)return;sonMotor(0,false);")
# botón de sonido visible en todos los modos
r("body.solo:not(.carrera) .bar>#bSnd","body.solo:not(.carrera):not(.rep) .bar>#bSnd")
open(f,'w').write(s)
def var(tit,scr,out):
    g=open(out).read().split('\n');i=[k for k,l in enumerate(g) if 'window.SOLO_CARRERA=1' in l][0];nxt=g[i+1]
    t=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%tit,s,count=1)
    t=re.sub(r'<header><h1>[^<]*</h1>','<header><h1>%s</h1>'%tit,t,count=1)
    L=t.split('\n');L.insert(L.index(nxt),scr);open(out,'w').write('\n'.join(L))
var('GT Vigo · Gran Premio','<script>window.SOLO_CARRERA=1;document.body.classList.add("solo")</script>','gp.html')
var('GT Vigo · Reparto de Navidad','<script>window.SOLO_CARRERA=1;window.SOLO_NAVIDAD=1;document.body.classList.add("solo")</script>','nav.html')
print('ok sonido')
