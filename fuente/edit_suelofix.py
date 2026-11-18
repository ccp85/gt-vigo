f='index.html';s=open(f).read()
def r(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# Altura aproximada del suelo (cuando aún no hay malla de suelo con BVH): las celdas peatonales (5) y de paseo/puente (4)
# devolvían una altura fija (0.02 y 0.1), casi a nivel del mar, y en el centro los peatones quedaban hundidos varios metros.
r("const groundMap=(x,y)=>{const c=cell(x,y);return c.t===4?.1:c.t===5?.02:c.z+(c.t===2?.025:0)};",
  "const groundMap=(x,y)=>{const c=cell(x,y);return c.t===4?Math.max(.1,c.z):c.t===5?Math.max(.02,c.z+.01):c.z+(c.t===2?.025:0)};")
open(f,'w').write(s);print('ok suelofix')
