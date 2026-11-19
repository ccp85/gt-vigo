# Descarga OpenStreetMap (Overpass) y relieve (tiles terrarium de AWS) para alargar la AP-9 de Rande a Pontevedra
import json,math,os,time,urllib.request,urllib.parse
S,W,N,E=42.270,-8.735,42.462,-8.575
OUT='datos_norte'
EPS=['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter']
def op(q,name):
  for k in range(6):
    for u in EPS:
      try:
        r=urllib.request.urlopen(urllib.request.Request(u,data=urllib.parse.urlencode({'data':q}).encode(),headers={'User-Agent':'gt-vigo-datos'}),timeout=300).read()
        if r[:1]==b'{':
          open(f'{OUT}/{name}.json','wb').write(r);print(name,len(r));return
        print('resp rara',u,r[:120])
      except Exception as e: print('err',u,e)
      time.sleep(5)
  raise SystemExit('overpass falla '+name)
bb=f'({S},{W},{N},{E})'
op(f'[out:json][timeout:240];(way["highway"]["highway"!~"footway|path|steps|cycleway|bridleway|pedestrian|corridor|proposed|construction|platform|elevator"]{bb};);out geom tags;','vias')
op(f'[out:json][timeout:240];(way["railway"~"rail|narrow_gauge"]{bb};way["natural"="coastline"]{bb};way["waterway"~"river|stream|canal"]{bb};way["natural"="water"]{bb};relation["natural"="water"]{bb};way["waterway"="riverbank"]{bb};relation["waterway"="riverbank"]{bb};way["man_made"~"pier|breakwater"]{bb};);out geom tags;','agua_tren')
op(f'[out:json][timeout:240];(way["landuse"]{bb};relation["landuse"]{bb};way["natural"~"wood|scrub|heath|grassland|sand|beach|wetland|bare_rock"]{bb};relation["natural"~"wood|scrub|heath|wetland"]{bb};way["leisure"~"park|pitch|golf_course|stadium"]{bb};);out geom tags;','suelos')
op(f'[out:json][timeout:300];(way["building"]{bb};relation["building"]{bb};);out geom tags;','edificios')
op(f'[out:json][timeout:120];(node["place"]{bb};node["amenity"~"fuel|school|hospital"]{bb};node["tourism"]{bb};node["historic"]{bb};node["highway"~"motorway_junction|toll_gantry"]{bb};node["barrier"="toll_booth"]{bb};way["barrier"="toll_booth"]{bb};way["amenity"="fuel"]{bb};);out geom tags;','puntos')
# relieve: tiles terrarium z14
z=14
def t(lon,lat):
  n=2**z;x=(lon+180)/360*n;y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n;return x,y
x0,y0=t(W,N);x1,y1=t(E,S)
os.makedirs(f'{OUT}/dem',exist_ok=True);n=0
for tx in range(int(x0),int(x1)+1):
  for ty in range(int(y0),int(y1)+1):
    u=f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{tx}/{ty}.png'
    for k in range(4):
      try: open(f'{OUT}/dem/{z}_{tx}_{ty}.png','wb').write(urllib.request.urlopen(u,timeout=60).read());n+=1;break
      except Exception as e: print('dem err',u,e);time.sleep(3)
print('dem tiles',n)
