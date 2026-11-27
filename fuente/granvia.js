// ---------- Fachadas reales de Gran Vía (granvia.js)
// Tramo bajo de Gran Vía, de Hispanidade a Praza de América. Colores y materiales sacados de Street View y Google Earth
// (noviembre 2026), edificio a edificio en la acera del noroeste (la del sureste son jardines, el IES Santa Irene y casas bajas).
// Cada punto es [x, y del juego, r, g, b, tipo] con tipo 2 = enlucido / pintura y 3 = piedra (sillería, granito o ladrillo visto).
// Al preparar cada edificio (subeMalla), si el centro de su base cae cerca de un punto, toma ese color; si está en el corredor de
// la avenida sin punto propio, toma un color de la paleta del centro (antes aquí salía la textura genérica sin color).
const GVR=[
 [89.382,37.410,0.88,0.84,0.76,2]/*GV112 crema, bandas blancas*/,
 [88.894,37.979,0.9,0.9,0.88,2]/*GV114 blanco gris*/,
 [88.406,38.549,0.88,0.88,0.86,2]/*GV116 galerias*/,
 [87.918,39.119,0.9,0.85,0.74,2]/*GV118 crema beige*/,
 [86.942,40.258,0.8,0.78,0.72,3]/*GV130 piedra gris beige*/,
 [86.617,40.638,0.45,0.33,0.25,2]/*marron oscuro*/,
 [86.455,40.828,0.9,0.8,0.68,2]/*GV134 crema salmon toldos*/,
 [86.118,41.161,0.72,0.62,0.5,2]/*esquina Tarragona beige marron*/,
 [84.938,42.049,0.66,0.36,0.26,3]/*ladrillo rojo*/,
 [84.694,42.223,0.92,0.92,0.9,2]/*GV150 blanco*/,
 [84.374,42.444,0.9,0.62,0.5,2]/*salmon alto*/,
 [84.167,42.585,0.76,0.72,0.64,3]/*GV154 granito antiguo*/,
 [83.796,42.839,0.88,0.6,0.52,2]/*salmon rosado*/,
 [83.548,43.009,0.86,0.74,0.52,2]/*GV158 ocre arena*/,
 [83.053,43.348,0.92,0.9,0.85,2]/*blanco crema*/,
 [82.723,43.574,0.62,0.36,0.28,3]/*ladrillo rojo marron*/,
 [82.558,43.687,0.8,0.5,0.4,2]/*salmon ladrillo*/,
 [82.352,43.828,0.8,0.74,0.62,3]/*GV164 granito arena*/,
 [81.733,44.251,0.66,0.65,0.63,3]/*granito gris*/,
 [81.320,44.534,0.92,0.88,0.8,2]/*crema*/,
 [81.138,44.652,0.86,0.55,0.45,2]/*GV174 salmon terracota*/,
 [80.710,44.912,0.93,0.9,0.84,2]/*blanco crema*/,
 [80.497,45.042,0.82,0.5,0.4,2]/*GV178 salmon ladrillo*/,
 [80.280,45.107,0.6,0.34,0.26,3]/*ladrillo rojo*/,
 [79.787,45.255,0.93,0.88,0.78,2]/*esquina Lopez Mora crema*/];window.__GVR=GVR;
const GV_EJE=[[90.0,37.61],[86.78,41.37],[86.24,41.86],[84.96,42.77],[81.54,45.11],[80.8,45.56],[80.12,45.8],[78.58,46.11]];
function gvCorr(x,y){let m=9;for(let i=1;i<GV_EJE.length;i++){const a=GV_EJE[i-1],b=GV_EJE[i],dx=b[0]-a[0],dy=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));m=Math.min(m,Math.hypot(x-a[0]-t*dx,y-a[1]-t*dy))}return m<1.0}
function gvColor(x,y){let best=null,bd=.27;for(const p of GVR){const d=Math.hypot(x-p[0],y-p[1]);if(d<bd){bd=d;best=p}}return best?[0,best[2],best[3],best[4],best[5]]:null}
// ---------- fin de granvia.js
