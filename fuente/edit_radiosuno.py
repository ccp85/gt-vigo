import sys,os,json
# ================= RADIO SUNO: canciones propias de Navidad (hechas con Suno) en el reparto de Navidad =================
# Nueva emisora «🎶 Vigo Nadal» con las canciones de la carpeta musica/ (mp3 de verdad, no sintetizadas).
# Solo en Navidad (window.SOLO_NAVIDAD: nav.html y navm.html) y es la primera emisora, así que el reparto arranca con ellas.
# Es la única emisora de Navidad (ya no están 🎄 Radio Navidad ni 🌴 Vigo Reggae); el mundo abierto sigue con las suyas.
# Las canciones suenan con un <audio> conectado a la radio (RADIO.g): se callan andando, nadando o buceando, igual que el resto.
# Al acabar una pasa sola a la siguiente; M / Ⓨ y el panel 📻 funcionan igual. Si un mp3 no carga, salta al siguiente.
# Va al final de build.sh (después de edit_radionavidad.py) y toca las cinco páginas (fuera de Navidad no cambia nada).
# Para añadir canciones: copiar el mp3 a musica/ (96 kbps estéreo basta) y añadir una línea a SUNO.
SUNO=[
 ('Vigo en Navidad','vigo-en-navidad.mp3'),
 ('Merry Christmas, Vigo','merry-christmas-vigo.mp3'),
 ('Vigo, Bo Nadal','vigo-bo-nadal.mp3'),
 ('Santa Claus in Vigo','santa-claus-in-vigo.mp3'),
 ('Three Kings in Vigo','three-kings-in-vigo.mp3'),
 ('Kings Yah Come','kings-yah-come.mp3'),
 ('Vigo Lights','vigo-lights.mp3'),
 ('Acéndense as Luces','acendense-as-luces.mp3'),
 ('Vigo Se Enciende','vigo-se-enciende.mp3'),
 ('Christmas House Groove','christmas-house-groove.mp3'),
 ('Vigo enciende la Navidad','vigo-enciende-la-navidad.mp3'),
 ('Let Your Christmas Shine','let-your-christmas-shine.mp3'),
 ('8-Bit Christmas','8-bit-christmas.mp3'),
 ('Vigo, Turn the Night to Day','vigo-turn-the-night-to-day.mp3'),
 ('Light It Up, Vigo','light-it-up-vigo.mp3'),
 ('Vigo in Christmas','vigo-in-christmas.mp3'),
 ('Festive Club Drop','festive-club-drop.mp3'),
 ('Vigo en Navidad II','vigo-en-navidad-1.mp3'),
 ('Silent Night Waltz','silent-night-waltz.mp3'),
 ('Vigo Lights Up','vigo-lights-up.mp3'),
 ('Navidad de 8-Bit','navida-de-8-bit.mp3'),
 ('Merry Christmas, Vigo II','merry-christmas-vigo-1.mp3'),
 ('Vigo, Turn the Night to Day II','vigo-turn-the-night-to-day-1.mp3'),
 ('Christmas House Groove II','christmas-house-groove-1.mp3'),
 ('Vigo en Navidad III','vigo-en-navidad-2.mp3'),
 ('Pixelated Carol','pixelated-carol.mp3'),
 ('Canción sorpresa','untitled.mp3'),
]
if os.path.isdir('musica'):
    for _,a in SUNO: assert os.path.exists('musica/'+a),a
LISTA=json.dumps([{'nom':n,'f':'musica/'+a} for n,a in SUNO],ensure_ascii=False)

JS=r"""
// ---------- 🎶 Vigo Nadal: canciones propias en mp3 (edit_radiosuno.py)
const SUNO=__LISTA__.map(c=>({nom:c.nom,f:c.f,mp3:true,bpm:120,bars:1,paso(){}}));
function radioMp3(S,ct){const Q=RADIO;
 if(!Q.au){Q.au=new Audio();Q.au.preload='auto';Q.au.playsInline=true;Q.auErr=0;
  Q.auSrc=AC.createMediaElementSource(Q.au);Q.auG=AC.createGain();Q.auG.gain.value=1.15;Q.auSrc.connect(Q.auG);Q.auG.connect(Q.g);
  Q.au.addEventListener('playing',()=>{Q.auErr=0});
  Q.au.addEventListener('ended',()=>{const S_=CANCIONES[Q.i];if(!S_||!S_.mp3||S_.f!==Q.auF)return;Q.i=(Q.i+1)%CANCIONES.length;Q.run=false;radioGuarda();radioAviso();radioPanelPinta()});
  Q.au.addEventListener('error',()=>{const S_=CANCIONES[Q.i];if(!S_||!S_.mp3)return;Q.auF=null;
   if(++Q.auErr>=4){emisoraPon(((Q.e||0)+1)%EMISORAS.length,0,true);return}Q.i=(Q.i+1)%CANCIONES.length;Q.run=false;radioGuarda()})}
 if(Q.auF!==S.f){Q.auF=S.f;Q.au.src=S.f;Q.run=false}
 if(!Q.run){Q.run=true;Q.g.gain.cancelScheduledValues(ct);Q.g.gain.setTargetAtTime(.42,ct,.4);if(!Q.dicho){Q.dicho=1;setTimeout(radioAviso,2500)}}
 if(Q.au.ended)return;
 if(Q.au.paused&&!Q.au.dataset.pide){Q.au.dataset.pide=1;const p=Q.au.play();if(p&&p.then)p.then(()=>{delete Q.au.dataset.pide},()=>{delete Q.au.dataset.pide});else delete Q.au.dataset.pide}
 Q.g.gain.setTargetAtTime(MODO==='heli'?.3:.42,ct,.3)}
function radioMp3Para(){const Q=RADIO;if(Q.au&&!Q.au.paused)Q.au.pause()}
// los navegadores del móvil solo dejan arrancar un <audio> dentro de un toque o tecla
['pointerdown','touchend','keydown'].forEach(ev=>addEventListener(ev,()=>{const Q=RADIO,S=CANCIONES[Q.i];if(Q.au&&Q.au.paused&&Q.run&&S&&S.mp3)Q.au.play().catch(()=>{})},{capture:true,passive:true}));
"""

for f in (sys.argv[1:] or [x for x in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(x)]):
    s=open(f,encoding='utf-8').read()
    if 'radioMp3(' in s: print('ya estaba',f); continue
    def r(a,b,n=1):
        global s
        assert s.count(a)==n,(f,s.count(a),a[:90]); s=s.replace(a,b)
    a="const EMISORAS=window.SOLO_NAVIDAD?[{nom:'🎄 Radio Navidad',c:VILLANCICOS},{nom:'🌴 Vigo Reggae',c:REGGAE}]:"
    r(a,JS.replace('__LISTA__',LISTA)+"const EMISORAS=window.SOLO_NAVIDAD?[{nom:'🎶 Vigo Nadal',c:SUNO}]:")
    # la radio parada (bajas del vehículo, carrera, sin sonido): también calla el mp3
    r("if(!play){if(RADIO.run){RADIO.run=false;RADIO.g.gain.setTargetAtTime(0,ct,.3)}return}",
      "if(!play){radioMp3Para();if(RADIO.run){RADIO.run=false;RADIO.g.gain.setTargetAtTime(0,ct,.3)}return}")
    r("const S=CANCIONES[RADIO.i],sm=60/S.bpm/4;",
      "const S=CANCIONES[RADIO.i],sm=60/S.bpm/4;if(S.mp3){radioMp3(S,ct);return}radioMp3Para();")
    # apagar la radio desde el panel
    r("if(b.dataset.off){RADIO.on=false;RADIO.run=false;","if(b.dataset.off){radioMp3Para();RADIO.on=false;RADIO.run=false;")
    open(f,'w',encoding='utf-8').write(s)
