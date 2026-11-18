f='index.html';s=open(f).read()
a="window.__dbg={cell:(x,y)=>cell(x,y),"
assert s.count(a)==1
s=s.replace(a,"window.__dbg={rm:(x,y)=>repMallas(x,y),ra:(x,y,m)=>repAltura(x,y,m),cell:(x,y)=>cell(x,y),")
open(f,'w').write(s);print('ok')
