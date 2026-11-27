# Carga del mapa de celdas (vigo_mapa.png, 5346x5722) sin el pico de memoria que reiniciaba móviles de 3-4 GB.
# Antes: se decodificaba la imagen entera (122 MB), se copiaba a dos lienzos de media imagen (61 MB cada uno), se leía
# cada mitad (otros 61 MB) y se juntaba en el array final (122 MB): más de 360 MB a la vez solo para esto.
# Ahora se baja vigo_mapa.rgba.gz (los mismos píxeles en crudo, ver herramientas/mapa_rgba.py) y se descomprime por
# trozos directamente en el array final con DecompressionStream: unos 122 MB y nada más, y además más rápido.
# Si el navegador no tiene DecompressionStream, falta el archivo o no cuadra el tamaño, vuelve a la imagen, pero leída en
# 8 franjas en vez de 2 (lienzos de 15 MB) y soltando la imagen al acabar. Toca las siete páginas; va al final de todo.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html','webgl.html','gpu.html'] if os.path.exists(f)]
OLD="""(async()=>{try{const j=await (await fetch(ZONA+'_mapa.json')).json();const im=new Image();im.src=ZONA+'_mapa.png';await im.decode();
 const T=Math.ceil(j.h/2),out=new Uint8ClampedArray(j.w*j.h*4);for(let y0=0;y0<j.h;y0+=T){const hh=Math.min(T,j.h-y0),c=document.createElement('canvas');c.width=j.w;c.height=hh;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,-y0);out.set(g.getImageData(0,0,j.w,hh).data,y0*j.w*4);c.width=c.height=1}MI=out;MAPA=j}catch(e){console.warn(e)}})();"""
NEW="""(async()=>{try{const j=await (await fetch(ZONA+'_mapa.json')).json();const N=j.w*j.h*4;let out=null,crudo=false;
 // mapa en crudo comprimido: se descomprime por trozos en el array final (sin imagen ni lienzos: mucha menos memoria al cargar)
 try{if(typeof DecompressionStream==='function'&&!/[?&]mapapng=1/.test(location.search)){const r=await fetch(ZONA+'_mapa.rgba.gz');if(r.ok&&r.body){const o=new Uint8ClampedArray(N);let k=0;
   const rd=r.body.pipeThrough(new DecompressionStream('gzip')).getReader();for(;;){const {done,value}=await rd.read();if(done)break;if(k+value.length>N)throw new Error('mapa crudo: tamaño');o.set(value,k);k+=value.length}
   if(k===N){out=o;crudo=true}else console.warn('mapa crudo: tamaño',k,N)}}}catch(e){console.warn('mapa crudo',e)}
 if(!out){const im=new Image();im.src=ZONA+'_mapa.png';await im.decode();
  const T=Math.ceil(j.h/8);out=new Uint8ClampedArray(N);for(let y0=0;y0<j.h;y0+=T){const hh=Math.min(T,j.h-y0),c=document.createElement('canvas');c.width=j.w;c.height=hh;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,-y0);out.set(g.getImageData(0,0,j.w,hh).data,y0*j.w*4);c.width=c.height=1}im.src=''}
 window.__MAPA_CRUDO=crudo;MI=out;MAPA=j}catch(e){console.warn(e)}})();"""
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'mapa crudo' in s:print('ya estaba',f);continue
    assert s.count(OLD)==1,(f,s.count(OLD))
    s=s.replace(OLD,NEW);open(f,'w',encoding='utf8').write(s);print('ok mapacrudo',f)
