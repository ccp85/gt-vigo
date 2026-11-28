# Calidad automática sin vaivén (va después de edit_fpsmovil.py; toca las siete páginas).
# Con el límite de 30 fps, cada 1,2 s la calidad automática veía «30 fps justos», subía la resolución; si el móvil no
# llegaba, la volvía a bajar al momento, y así sin parar. Cada cambio de resolución rehace la imagen de la pantalla
# entera y da un tirón: en un móvil justo (p. ej. Redmi Note 9) eso eran tirones periódicos todo el rato.
# Ahora: como mucho un cambio cada 4 s; para subir hacen falta 3 mediciones buenas seguidas (unos 4 s); y tras una
# bajada no se vuelve a subir en 45 s. Bajar sigue siendo rápido si de verdad va lento.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','webgl.html','gpu.html'] if os.path.exists(f)]
OLD=" if(window.NOADAPT){}else if(window.LITE){if(ft>(a30?1/27:1/45)){if(QF>.35)QF=Math.max(.35,QF-.1);else if(prAct>PRmin)nv=Math.max(PRmin,prAct-.125)}else if(ft<(a30?1/28.5:1/55)){if(prAct<PRmax)nv=Math.min(PRmax,prAct+.125);else if(QF<QMAX)QF=Math.min(QMAX,QF+.05)}}else if(ft>(a30?1/27:1/34)){if(prAct>PRmin)nv=Math.max(PRmin,prAct-.2);else QF=Math.max(.5,QF-.15)}else if(ft<(a30?1/28.5:1/52)){if(QF<1)QF=Math.min(1,QF+.1);else if(prAct<PRmax)nv=Math.min(PRmax,prAct+.2)}"
NEW=(" const ah_=performance.now(),RA=window.__RA||(window.__RA={t:0,bloq:0,ok:0}),q0_=QF,baja_=()=>{RA.t=ah_;RA.bloq=ah_+45000;RA.ok=0},sube_=()=>ah_>RA.bloq&&++RA.ok>=3;   // sin vaivén: ver edit_sinvaiven.py\n"
 " if(window.NOADAPT||ah_-RA.t<4000){}else if(window.LITE){if(ft>(a30?1/27:1/45)){baja_();if(QF>.35)QF=Math.max(.35,QF-.1);else if(prAct>PRmin)nv=Math.max(PRmin,prAct-.125)}else if(ft<(a30?1/28.5:1/55)){if(sube_()){RA.ok=0;if(prAct<PRmax)nv=Math.min(PRmax,prAct+.125);else if(QF<QMAX)QF=Math.min(QMAX,QF+.05)}}else RA.ok=0}"
 "else if(ft>(a30?1/27:1/34)){baja_();if(prAct>PRmin)nv=Math.max(PRmin,prAct-.2);else QF=Math.max(.5,QF-.15)}else if(ft<(a30?1/28.5:1/52)){if(sube_()){RA.ok=0;if(QF<1)QF=Math.min(1,QF+.1);else if(prAct<PRmax)nv=Math.min(PRmax,prAct+.2)}}else RA.ok=0\n"
 " if(nv!==prAct||QF!==q0_)RA.t=ah_;")
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'sin vaivén: ver edit_sinvaiven.py' in s:print('ya estaba',f);continue
    assert s.count(OLD)==1,(f,s.count(OLD))
    s=s.replace(OLD,NEW);open(f,'w',encoding='utf8').write(s);print('ok sinvaiven',f)
