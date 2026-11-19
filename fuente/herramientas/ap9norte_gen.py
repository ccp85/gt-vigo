# Uso: 1) cargar el juego con las zonas teis, rande, este, hueco3, centro y puerto y ejecutar ap9norte_hornear.js en la
#    consola (con window.__GR=GROUND expuesto); guardar el JSON devuelto como bake2.json.
# 2) python3 ap9norte_gen.py -> datos.json, que va incrustado en fuente/edit_ap9norte.py.
# Genera los datos de la AP-9 (Vigo -> Pontevedra) para edit_ap9norte.py a partir del horneado (bake2.json)
import json,math,random
import numpy as np
random.seed(7)
B=json.load(open('/home/claude/ana/bake2.json'))
OLD=lambda x,y: x<126 and -3<y<21
# Área de servizo de San Simón (PK 144, margen derecha hacia Pontevedra): marco local u (a lo largo) / v (hacia fuera desde el borde)
_b23=[b for b in B if b['k']==23][0]['S'];_j=[j for j,r in enumerate(_b23) if r[1]<-56.36][0]
SA0=np.array(_b23[_j][:2]);_t=np.array(_b23[_j+4][:2])-np.array(_b23[_j-4][:2]);SAT=_t/np.linalg.norm(_t);SAN=np.array([-SAT[1],SAT[0]]);SAE=.22
def SAuv(x,y):
  d=np.array([x,y])-SA0;return float(d@SAT),float(d@SAN)-SAE
def EXCL(x,y):
  u,v=SAuv(x,y);return -0.95<u<0.85 and -0.05<v<0.66
L=[]
for b in B:
  S=b['S']
  if len(S)<6: continue
  A=np.array([[r[0],r[1]] for r in S])
  T=np.gradient(A,axis=0);T/=np.linalg.norm(T,axis=1,keepdims=True)+1e-9
  N=np.c_[-T[:,1],T[:,0]]   # derecha del sentido de la marcha (exterior)
  L.append(dict(k=b['k'],S=S,A=A,T=T,N=N,dy=A[-1,1]-A[0,1]))
allp=np.concatenate([np.c_[l['A'],np.full(len(l['A']),i)] for i,l in enumerate(L)])
def near_other(p,i,r):
  d=np.hypot(allp[:,0]-p[0],allp[:,1]-p[1]);d[allp[:,2]==i]=9;return d.min()<r
R3=lambda v:round(float(v),3)
rails=[];slopes=[];trees=[];props=[]
def runs(mask,minlen=4):
  out=[];i=0;n=len(mask)
  while i<n:
    if mask[i]:
      j=i
      while j<n and mask[j]: j+=1
      if j-i>=minlen: out.append((i,j))
      i=j
    else: i+=1
  return out
def medf(v,w=7):
  v=np.array(v,float);o=v.copy();h=w//2
  for i in range(len(v)): o[i]=np.median(v[max(0,i-h):i+h+1])
  return o
# ---------- borde exterior: biondas, pantallas, taludes, árboles ----------
for i,l in enumerate(L):
  S=l['S'];A=l['A'];N=l['N'];n=len(S)
  e=np.array([r[4] for r in S]);f=np.array([r[5] for r in S]);br=np.array([r[3]=='p' for r in S])
  hz=[r[6] for r in S];bh=np.array([max(0,r[8]) for r in S])
  ok=np.array([(e[j]<=.30) and not br[j] and not OLD(*A[j]) for j in range(n)])
  es=medf(np.where(ok,e,.25),7)
  # no poner bionda si a la derecha hay otra calzada de la AP (rampa pegada)
  for j in range(n):
    if ok[j] and near_other(A[j]+N[j]*(es[j]+.04),i,.05): ok[j]=False
    if ok[j] and l['dy']<0 and EXCL(*(A[j]+N[j]*es[j])): ok[j]=False
  fz=np.array([ok[j] and A[j,1]<-44 and f[j]>=.09 for j in range(n)])
  for a,b2 in runs(fz,6):
    rails.append(['F',[R3(v) for j in range(a,b2) for v in (A[j]+N[j]*(es[j]+.062))]])
  for a,b2 in runs(ok,5):
    urb=[bool(bh[max(0,j-8):j+9].max()>.1) and A[j,1]>-44 for j in range(a,b2)]
    # tramos con edificios cerca -> pantalla acústica
    seg=[];cur=None
    for j,u in zip(range(a,b2),urb):
      t='S' if u else 'G'
      if t!=cur:
        if seg and len(seg[1])>1: rails.append(seg)
        seg=[t,[]];cur=t
        if j>a: seg[1]+= [R3(A[j-1,0]+N[j-1,0]*(es[j-1]-.006)),R3(A[j-1,1]+N[j-1,1]*(es[j-1]-.006))]
      seg[1]+= [R3(A[j,0]+N[j,0]*(es[j]-.006)),R3(A[j,1]+N[j,1]*(es[j]-.006))]
    if seg and len(seg[1])>2: rails.append(seg)
    # taludes
    st=None
    for j in range(a,b2):
      W=min(f[j],.2)
      good=W>=.05 and hz[j][1] is not None
      if good:
        kind=1 if hz[j][1]>.03 else 0
        if st is None or st[0]!=kind:
          if st and len(st[1])>=8: slopes.append(st)
          st=[kind,[]]
        p=A[j]+N[j]*es[j];q=A[j]+N[j]*(es[j]+W)
        st[1]+=[R3(p[0]),R3(p[1]),R3(q[0]),R3(q[1])]
      else:
        if st and len(st[1])>=8: slopes.append(st)
        st=None
    if st and len(st[1])>=8: slopes.append(st)
  # árboles en terreno libre (también donde no hay bionda, salvo puente y tramo viejo)
  for j in range(0,n,1):
    if br[j] or OLD(*A[j]) or e[j]>.32: continue
    fr=min(f[j],.5)
    if fr<.1: continue
    for t in range(3):
      if random.random()<.5: continue
      d=e[j]+.06+random.random()*(fr-.07)
      p=A[j]+N[j]*d+np.array([random.uniform(-.025,.025),random.uniform(-.025,.025)])
      if near_other(p,-1,.17) or EXCL(*p): continue
      ty=0 if random.random()<.55 else (1 if random.random()<.75 else 2)
      trees+= [R3(p[0]),R3(p[1]),ty,int(random.uniform(80,125))]
# ---------- mediana (desde las calzadas hacia Pontevedra) ----------
southi=[i for i,l in enumerate(L) if l['dy']>0]
SP=np.concatenate([np.c_[L[i]['A'],np.full(len(L[i]['A']),i)] for i in southi])
med=[]
for i,l in enumerate(L):
  if l['dy']>0: continue
  A=l['A'];N=l['N'];S=l['S'];n=len(A);mid=[None]*n
  for j in range(n):
    if OLD(*A[j]): continue
    d=np.hypot(SP[:,0]-A[j,0],SP[:,1]-A[j,1]);q=np.argmin(d)
    if .04<=d[q]<=.26 and np.dot(SP[q,:2]-A[j],N[j])<0: mid[j]=((A[j]+SP[q,:2])/2,d[q],S[j][3]=='p')
  for a,b2 in runs([m is not None for m in mid],5):
    P=np.array([mid[j][0] for j in range(a,b2)])
    # suavizado
    Q=P.copy()
    for j in range(1,len(P)-1): Q[j]=(P[j-1]+2*P[j]+P[j+1])/4
    ty='A' if Q[:,1].mean()<-44.5 else 'M'
    rails.append([ty,[R3(v) for p in Q for v in p]])
    # farolas en la mediana desde Vigo hasta el norte del puente
    for j in range(0,len(Q),7):
      if Q[j,1]>-44.5:
        t=Q[min(len(Q)-1,j+1)]-Q[max(0,j-1)];props.append(['L',R3(Q[j,0]),R3(Q[j,1]),R3(math.atan2(t[0],t[1]))])
# ---------- PK sobre el eje hacia Pontevedra ----------
chain=[]
for k in [27,37,33,44,29,23,41]:
  l=[x for x in L if x['k']==k][0];chain.append(l['A'])
C=np.concatenate(chain);s=np.r_[0,np.cumsum(np.hypot(*np.diff(C,axis=0).T))]
# inicio del puente (primera muestra 'p' de k33) = PK 147.6, escala 0.124 km por unidad
l33=[x for x in L if x['k']==33][0];jp=[j for j,r in enumerate(l33['S']) if r[3]=='p'][0]
s0=s[np.argmin(np.hypot(*(C-l33['A'][jp]).T))]
PKf=lambda ss:147.6-(ss-s0)*0.124
def pk_of(p):
  d=np.hypot(*(C-p).T);j=np.argmin(d);return PKf(s[j]),d[j]
def at_pk(pk,north=True):
  ss=s0+(147.6-pk)/0.124;j=int(np.clip(np.searchsorted(s,ss),1,len(C)-1))
  p=C[j-1]+(C[j]-C[j-1])*((ss-s[j-1])/max(1e-9,s[j]-s[j-1]))
  if north: return p
  # punto equivalente en la calzada hacia Vigo
  d=np.hypot(SP[:,0]-p[0],SP[:,1]-p[1]);q=np.argmin(d);return SP[q,:2]
def frame(p,north=True):
  # devuelve punto de línea, tangente, normal derecha, borde exterior e (calzada correspondiente)
  best=None
  for i,l in enumerate(L):
    if (l['dy']<0)!=north: continue
    d=np.hypot(*(l['A']-p).T);j=np.argmin(d)
    if best is None or d[j]<best[0]: best=(d[j],i,j)
  _,i,j=best;l=L[i];r=l['S'][j];e=r[4] if r[4]<=.3 else .24
  return l['A'][j],l['T'][j],l['N'][j],e,r[3]=='p',i,j
info={'s0':float(s0),'len':float(s[-1])}
print('PK inicio cadena',PKf(0),'fin',PKf(s[-1]))
json.dump(dict(rails=rails,slopes=slopes,trees=trees,props=props),open('parcial.json','w'))
import pickle;pickle.dump(dict(C=C,s=s,s0=s0),open('chain.pkl','wb'))
print(len(rails),sum(len(r[1])//2 for r in rails),len(slopes),len(trees)//4,len(props))
from collections import Counter;print(Counter(r[0] for r in rails))
# ---------- señalización por PK ----------
def side_pt(pk,north,off=.035):
  p=at_pk(pk,north);P0,T0,N0,e,br,i,j=frame(p,north)
  return P0+N0*((.24 if br else e)+off),math.atan2(T0[0],T0[1]),P0,T0,N0,(.24 if br else e)
def med_pt(P0,N0):
  d=np.hypot(SP[:,0]-P0[0],SP[:,1]-P0[1]) if True else None
  return d
def gantry(pk,north,panels):
  q,ang,P0,T0,N0,e=side_pt(pk,north,.03)
  # pie izquierdo: en la mediana (mitad entre las dos calzadas)
  other=[l for l in L if (l['dy']<0)!=north]
  best=9;mp=None
  for l in other:
    d=np.hypot(*(l['A']-P0).T);j=np.argmin(d)
    if d[j]<best and np.dot(l['A'][j]-P0,N0)<0: best=d[j];mp=(P0+l['A'][j])/2
  if mp is None or best>.3: mp=P0-N0*.06
  props.append(['P',R3(mp[0]),R3(mp[1]),R3(q[0]),R3(q[1]),R3(ang),panels])
def lateral(kind,pk,north,*extra,off=.035):
  q,ang,*_=side_pt(pk,north,off);props.append([kind,R3(q[0]),R3(q[1]),R3(ang),*extra])
NB=dict(k='AP-9',c='a');N552=dict(k='N-552',c='n');CRG=dict(k='CRG-4.1',c='o');A52=dict(k='A-52',c='a');AP9V=dict(k='AP-9V',c='a')
# hacia Pontevedra
lateral('V',149.85,True,100);lateral('V',145.2,True,100);lateral('V',142.8,True,100)
gantry(150.02,True,[dict(u=.5,w=.62,k='v',t=['PONTE DE RANDE','CIRCULE CON PRECAUCIÓN'])])
lateral('N',149.95,True,'Redondela')
gantry(149.45,True,[dict(u=.3,w=.36,k='d',b=[NB],t=['Pontevedra','Santiago'],a='uu'),dict(u=.76,w=.34,k='x',n='148',t=['Redondela','Chapela'],b=[N552],s='1.500 m')])
gantry(148.4,True,[dict(u=.3,w=.36,k='d',b=[NB],t=['Pontevedra','Santiago'],a='uu'),dict(u=.76,w=.34,k='x',n='148',t=['Redondela','Chapela'],b=[N552],a='r')])
for n_,d_ in [(3,.3),(2,.2),(1,.1)]: lateral('B',148.0+d_,True,n_,off=.02)
lateral('X',147.98,True,'148',off=.03)
lateral('C',147.95,True,dict(k='r',t=['Ponte de Rande','1.558 m']))
gantry(147.72,True,[dict(u=.3,w=.36,k='d',b=[NB],t=['Pontevedra','Santiago'],a='uu'),dict(u=.76,w=.34,k='x',n='146',t=['Moaña','Cangas'],b=[CRG],s='1.700 m')])
lateral('W',147.58,True,off=.05);lateral('Q',147.66,True,off=.05)
lateral('X',145.93,True,'146',off=.03);lateral('W',146.0,True,off=.05)
lateral('C',145.45,True,dict(k='c',t=['Pontevedra  16','Santiago  70','A Coruña  145']))
gantry(143.6,True,[dict(u=.5,w=.62,k='v',t=['PONTEVEDRA  10 MIN','SANTIAGO  45 MIN'])])
lateral('Q',143.7,True,off=.05)
# hacia Vigo
lateral('V',142.6,False,100);lateral('V',144.6,False,100);lateral('V',148.4,False,100);lateral('V',149.95,False,100)
lateral('C',142.3,False,dict(k='c',t=['Redondela  6','Vigo  13']))
gantry(143.3,False,[dict(u=.5,w=.62,k='v',t=['VIGO CENTRO  12 MIN','PRECAUCIÓN NA PONTE'])])
gantry(145.25,False,[dict(u=.3,w=.36,k='d',b=[NB],t=['Vigo','Tui'],a='uu'),dict(u=.76,w=.34,k='x',n='146',t=['Moaña','Cangas'],b=[CRG],a='r')])
for n_,d_ in [(3,.3),(2,.2),(1,.1)]: lateral('B',145.9-d_,False,n_,off=.02)
lateral('X',145.92,False,'146',off=.03)
lateral('C',145.97,False,dict(k='r',t=['Ponte de Rande','1.558 m']))
lateral('W',146.02,False,off=.05);lateral('Q',145.98,False,off=.05)
gantry(147.8,False,[dict(u=.3,w=.36,k='d',b=[NB],t=['Vigo','Tui'],a='uu'),dict(u=.76,w=.34,k='x',n='148',t=['Redondela','Chapela'],b=[N552],a='r')])
lateral('W',147.62,False,off=.05)
lateral('X',148.05,False,'148',off=.03)
gantry(148.9,False,[dict(u=.5,w=.62,k='v',t=['VIGO CENTRO  6 MIN','AP-9V · PORTO'])])
lateral('N',149.55,False,'Vigo')
gantry(149.8,False,[dict(u=.3,w=.36,k='d',b=[NB,A52],t=['Tui · Ourense','Porriño'],a='u'),dict(u=.76,w=.34,k='d',b=[AP9V],t=['Vigo','Centro · Porto'],a='u')])
lateral('Q',149.7,False,off=.05)
# ---- Rande · Moaña · Vilaboa ----
pkSA=pk_of(SA0)[0];print('PK área',pkSA)
props.append(['A',R3(SA0[0]),R3(SA0[1]),R3(SAT[0]),R3(SAT[1]),SAE])
lateral('C',pkSA+1.0,True,dict(k='sa',t=['San Simón','1.000 m']))
lateral('C',pkSA+.5,True,dict(k='sa',t=['San Simón','500 m']))
lateral('Y',pkSA+.115,True,off=.04)
lateral('N',145.8,True,'Moaña');lateral('N',144.6,True,'Vilaboa')
lateral('N',144.75,False,'Moaña');lateral('N',147.5,False,'Redondela')
lateral('C',145.55,True,dict(k='t',t=['Enseada de San Simón','Illas de San Simón e San Antón']))
lateral('C',143.0,False,dict(k='t',t=['Ponte de Rande','Ría de Vigo']))
lateral('V',143.7,True,100);lateral('V',145.7,False,100)
# hitos hectométricos en el tramo norte
for hm in range(1420,1476):
  if hm%10==0: continue
  for north in (True,False):
    q,ang,P0,T0,N0,e=side_pt(hm/10,north,.03)
    if EXCL(*q): continue
    props.append(['H',R3(q[0]),R3(q[1]),R3(ang),hm%10])
# hitos kilométricos y postes SOS en los dos sentidos
for pk in range(142,152):
  for north in (True,False):
    q,ang,P0,T0,N0,e=side_pt(pk,north,.03)
    if OLD(*q): continue
    props.append(['K',R3(q[0]),R3(q[1]),R3(ang),pk])
for pk in [149.6,148.5,144.5,142.5]:
  for north in (True,False):
    lateral('O',pk,north,off=.04)
print('PK separación Teis',pk_of(np.array([140.3,-15.7])))
json.dump(dict(rails=rails,slopes=slopes,trees=trees,props=props),open('datos.json','w'),separators=(',',':'),ensure_ascii=False)
import os;print('bytes',os.path.getsize('datos.json'));from collections import Counter;print(Counter(p[0] for p in props))
