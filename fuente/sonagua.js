// ---------- sonido del agua: nadar, bucear y el mundo submarino (sonagua.js, lo mete edit_sonagua.py; todo sintetizado)
// bajo el agua todo el sonido del juego se apaga con un filtro (más cuanto más hondo), y suena el fondo de la ría:
// retumbo que respira con el oleaje, la rompiente lejana, chasquidos de camarones pistola, tus burbujas, las brazadas
// y un latido cuando queda poco aire. En la superficie: chapoteo, salpicadura de cada brazada y la bocanada al sacar la cabeza.
const SAG={nada:false,bajo:false,brazada:0,burb:2,lat:0};
function sagNodos(){if(SAG.g||!AC||!master||!NB)return;
 SAG.fl=AC.createBiquadFilter();SAG.fl.type='lowpass';SAG.fl.frequency.value=20000;SAG.fl.Q.value=.7;
 try{master.disconnect()}catch(e){}master.connect(SAG.fl);SAG.fl.connect(AC.destination);
 SAG.g=AC.createGain();SAG.g.gain.value=0;SAG.g.connect(AC.destination);
 const capa=(fq,tipo,q,lf,prof,off)=>{const z=AC.createBufferSource();z.buffer=NB;z.loop=true;const f=AC.createBiquadFilter();f.type=tipo;f.frequency.value=fq;f.Q.value=q;
  const mod=AC.createGain();mod.gain.value=1;const o=AC.createOscillator();o.frequency.value=lf;const og=AC.createGain();og.gain.value=prof;o.connect(og);og.connect(mod.gain);o.start();
  const g=AC.createGain();g.gain.value=0;z.connect(f);f.connect(mod);mod.connect(g);g.connect(SAG.g);z.start(0,off);return g};
 SAG.rum=capa(170,'lowpass',.8,.11,.45,0);     // retumbo grave
 SAG.mar=capa(420,'bandpass',.6,.07,.6,.7);    // rompiente lejana filtrada
 SAG.sup=capa(1100,'bandpass',.5,.33,.55,1.3)} // chapoteo en la superficie
function sagSal(g){if(AC.createStereoPanner){const p=AC.createStereoPanner();g.connect(p);p.connect(SAG.g);return p}g.connect(SAG.g);return g}
function sagRuido(t,d,f,q,v,tipo='bandpass',pan=0,att=.01,f2=0){const s=AC.createBufferSource(),fl=AC.createBiquadFilter(),g=AC.createGain();s.buffer=NB;fl.type=tipo;fl.frequency.setValueAtTime(f,t);if(f2)fl.frequency.exponentialRampToValueAtTime(f2,t+d);fl.Q.value=q;
 g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+att);g.gain.exponentialRampToValueAtTime(.0005,t+d);s.connect(fl);fl.connect(g);const p=sagSal(g);if(p.pan)p.pan.value=pan;s.start(t,Math.random()*1.5);s.stop(t+d+.05)}
// burbuja: un tono que sube muy rápido, como la resonancia de una burbuja al formarse
function sagBurbuja(t,f,v,pan=0){const o=AC.createOscillator(),g=AC.createGain();o.frequency.setValueAtTime(f,t);o.frequency.exponentialRampToValueAtTime(f*2.4,t+.05);
 g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.004);g.gain.exponentialRampToValueAtTime(.0005,t+.07);o.connect(g);const p=sagSal(g);if(p.pan)p.pan.value=pan;o.start(t);o.stop(t+.09)}
function sagExhala(t,n,v){for(let k=0;k<n;k++)sagBurbuja(t+k*.045+Math.random()*.06,260+Math.random()*700,v*(.5+Math.random()),(Math.random()-.5)*.6);sagRuido(t,.7,500,.7,v*.6,'bandpass',0,.05)}
function sagZambullida(){const t=AC.currentTime;sagRuido(t,.9,3500,.5,.3,'lowpass',0,.008,500);sagRuido(t,.45,1800,.8,.16,'bandpass',0,.005);sagExhala(t+.15,16,.05)}
function sagHunde(){const t=AC.currentTime;sagRuido(t,.6,900,.6,.2,'lowpass',0,.01,180);sagExhala(t+.05,10,.05)}
function sagSube(){const t=AC.currentTime;sagRuido(t,.45,2600,.6,.2,'bandpass',0,.005);sagRuido(t,.25,5000,.4,.08,'highpass',0,.003);sagRuido(t+.2,.55,1300,1.6,.08,'bandpass',0,.12)}
function sagGotas(){const t=AC.currentTime;sagRuido(t,.35,2200,.6,.12,'bandpass',0,.005);for(let k=0;k<6;k++){const tk=t+.25+k*.18+Math.random()*.12;sagBurbuja(tk,1100+Math.random()*900,.035,(Math.random()-.5)*.8)}}
function sagLatido(t){for(const[d,v]of[[0,.22],[.16,.14]]){const o=AC.createOscillator(),g=AC.createGain();o.frequency.setValueAtTime(70,t+d);o.frequency.exponentialRampToValueAtTime(42,t+d+.12);
 g.gain.setValueAtTime(0,t+d);g.gain.linearRampToValueAtTime(v,t+d+.01);g.gain.exponentialRampToValueAtTime(.0005,t+d+.2);o.connect(g);g.connect(SAG.g);o.start(t+d);o.stop(t+d+.25)}}
function sagTick(){if(!AC||!master)return;sagNodos();if(!SAG.g)return;const ct=AC.currentTime,dt=.04,B=BUC;
 const on=soundOn&&driving,nada=driving&&MODO==='nado'&&!!B.on,bajo=nada&&!!window.__BAJO,prof=nada?Math.max(0,B.WY-.012-(P.z||0)):0;
 SAG.g.gain.setTargetAtTime(on?.9:0,ct,.15);
 SAG.fl.frequency.setTargetAtTime(bajo?Math.max(240,560-prof*1000):20000,ct,bajo?.06:.12);
 SAG.rum.gain.setTargetAtTime(bajo?.5:0,ct,.25);SAG.mar.gain.setTargetAtTime(bajo?.07*Math.max(.25,1-prof*3):0,ct,.3);SAG.sup.gain.setTargetAtTime(nada&&!bajo?.06:0,ct,.25);
 if(on){if(nada&&!SAG.nada)sagZambullida();else if(!nada&&SAG.nada&&MODO==='pie')sagGotas();if(bajo&&!SAG.bajo)sagHunde();else if(!bajo&&SAG.bajo&&nada)sagSube()}
 SAG.nada=nada;SAG.bajo=bajo;if(!on||!nada)return;
 const v=Math.min(1,Math.abs(P.v||0)/.25);
 if(v>.15){SAG.brazada-=dt*(.8+v*1.2);if(SAG.brazada<=0){SAG.brazada=1;if(bajo)sagRuido(ct,.7,240,.9,.14*v,'lowpass',0,.25);else{sagRuido(ct,.32,1800+Math.random()*900,.7,.12*v,'bandpass',(Math.random()-.5)*.5,.012);sagRuido(ct+.05,.2,4200,.5,.045*v,'highpass')}}}
 if(!bajo)return;
 SAG.burb-=dt;if(SAG.burb<=0){SAG.burb=3.5+Math.random()*3;sagExhala(ct+.02,10+Math.floor(Math.random()*10),.04)}
 const n=Math.floor(Math.random()*1.6+.5);for(let k=0;k<n;k++)sagRuido(ct+Math.random()*.04,.012,3500+Math.random()*3000,.8,.015+Math.random()*.04,'highpass',Math.random()*1.8-.9,.0008);
 if(B.aire<.3){SAG.lat-=dt;if(SAG.lat<=0){SAG.lat=.85;sagLatido(ct+.02)}}
 if(B.pulpos)for(const o of B.pulpos){if(o.huye>2.3&&!o.sonado){o.sonado=1;sagRuido(ct,.6,700,.8,.12,'lowpass',0,.02,200)}if(o.huye<=0)o.sonado=0}}
setInterval(sagTick,40);
