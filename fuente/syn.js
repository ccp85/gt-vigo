// comprobación rápida de sintaxis de los HTML generados: node syn.js [carpeta] (por defecto, la carpeta actual)
const fs=require('fs'),path=require('path'),dir=process.argv[2]||process.cwd();
for(const f of ['index','indexm','gp','nav','navm']){const p=path.join(dir,f+'.html');if(!fs.existsSync(p))continue;const s=fs.readFileSync(p,'utf8');const re=/<script type="module">([\s\S]*?)<\/script>/g;let m,k=0;while(m=re.exec(s)){const c=m[1].replace(/^\s*import[^;]*;/gm,'');try{new Function(c);k++}catch(e){console.log(f,'ERR',e.message)}}console.log(f,'ok',k)}
