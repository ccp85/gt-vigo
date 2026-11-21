// Contador de visitas en la pantalla de inicio (dentro de la cabecera, debajo de «GT VIGO»), leído de GoatCounter.
// Necesita activar en gtvigo.goatcounter.com → Settings → «Allow adding visitor counts on your website».
// Si no está activado o falla la red, no se muestra nada. GoatCounter guarda las cifras hasta 4 h en caché.
(function(){
  var B='https://gtvigo.goatcounter.com/counter/TOTAL.json';
  function pide(q){return fetch(B+q,{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){return j&&j.count?String(j.count).replace(/,/g,'.'):null}).catch(function(){return null})}
  function pon(){
    var sz=document.getElementById('selz');if(!sz||document.getElementById('iVis'))return;
    var d=new Date(),mes=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-01';
    Promise.all([pide(''),pide('?start='+mes)]).then(function(v){
      if(!v[0])return;
      var st=document.createElement('style');
      st.textContent='#selz #iVis{position:static;inset:auto;transform:none;width:max-content;height:auto;margin:clamp(8px,1.6vh,16px) auto 0;display:flex;gap:.6em;align-items:center;padding:5px 12px;border-radius:999px;background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.18);color:rgba(255,255,255,.85);font:700 12px/1.2 var(--body,system-ui);letter-spacing:.04em;backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);pointer-events:none;white-space:nowrap}#selz #iVis b{color:#fff}#selz #iVis i{opacity:.4;font-style:normal}';
      document.head.appendChild(st);
      var el=document.createElement('div');el.id='iVis';el.setAttribute('aria-label','Visitas');
      el.innerHTML='👀 <span><b>'+v[0]+'</b> visitas</span>'+(v[1]?'<i>·</i><span><b>'+v[1]+'</b> este mes</span>':'');
      var h=sz.querySelector('.iHead');
      if(h)h.appendChild(el);else{el.style.cssText='position:absolute;top:12px;left:12px';sz.appendChild(el)}
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',pon);else pon();
})();
