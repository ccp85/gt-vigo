# Montones de nieve junto a las aceras (Navidad). El trabajador de calles.js (bordillos) devuelve además los tramos de bordillo
# de acera que dan a la calzada (bor); nieve.js pone a lo largo montones de nieve que crecen con la nevada. Va después de edit_nieve.py.
import sys,os
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
for f in FILES:
    s=open(f,encoding='utf8').read()
    if 'BOR.push(' in s:print('ya estaba',f);continue
    assert 'function nveMontones(' in s,f
    def r(a,b):
        global s
        assert s.count(a)==1,(f,s.count(a),a[:90]); s=s.replace(a,b)
    r("const T8=16,TR=new Map(),EPS=.006;","const T8=16,TR=new Map(),EPS=.006,BOR=[];")
    r("lado(p,pt[s0],pt[e],dm,base);s0=e}};","if(m.t===3&&dm>.006&&dm<.04){const a=pt[s0],b=pt[e];BOR.push(p[a],p[a+1],p[a+2],p[b],p[b+1],p[b+2],dm)}lado(p,pt[s0],pt[e],dm,base);s0=e}};")
    r("self.postMessage({id,trozos,ms:","const bor=new Float32Array(BOR);tr.push(bor.buffer);self.postMessage({id,trozos,bor,ms:")
    r("if(r.err){console.warn('faldones',r.err);return}","if(r.err){console.warn('faldones',r.err);return}try{if(r.bor&&r.bor.length&&root.parent)nveMontones(root,r.bor)}catch(e){console.warn('montones',e)}")
    open(f,'w',encoding='utf8').write(s);print('ok montones',f)
