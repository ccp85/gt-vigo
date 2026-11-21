// Analíticas con GoatCounter (gtvigo.goatcounter.com): sin cookies, no necesita aviso de cookies.
// gtvEv('zona/samil','Zona Samil') cuenta un evento una sola vez por partida (no repite si vuelves a la misma zona).
// En localhost GoatCounter no cuenta nada, así que las pruebas en local no ensucian los datos.
(function(){
  var hechos={},cola=[];
  function slug(t){return String(t).normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9/]+/g,'-').replace(/-*\/-*/g,'/').replace(/^-+|-+$/g,'')||'x'}
  function manda(){
    var gc=window.goatcounter;if(!gc||!gc.count)return false;
    while(cola.length){var e=cola.shift();try{gc.count({path:e[0],title:e[1],event:true})}catch(_){}}
    return true;
  }
  window.gtvEv=function(nombre,titulo){
    try{
      var p=slug(nombre);if(hechos[p])return;hechos[p]=1;
      cola.push([p,titulo||nombre]);
      if(!manda()){var n=0,iv=setInterval(function(){if(manda()||++n>60)clearInterval(iv)},1000)}
    }catch(_){}
  };
})();
