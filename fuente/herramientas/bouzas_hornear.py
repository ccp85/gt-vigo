# Hornea bouzas_jardin.json a partir de las mallas de la zona (bz_tris.json, sacado del glb con glbtris.mjs):
# cubierta del suelo de las parcelas (césped, prado, solado de granito), muros de cierre y sebes, árboles de jardín,
# palmeras y arbustos, y el contorno del dique del Museo do Mar.
# Uso (en una carpeta de trabajo): sacar el glb de bouzas_glb_1.png (4 bytes de largo + glb), luego
#   node bouzas_glbtris.mjs bouzas.glb bz_tris.json tierra,verde,verde_paseo,playa,playita_16162,aceras,calzada,paseo,paseo_madera,muelles,roca,edificios,carril_bici,puente_8390,piezas
#   python3 bouzas_raster.py && python3 bouzas_hornear.py RAIZ_DEL_REPO
# Necesita numpy, scipy, scikit-image, shapely y Pillow.
import sys, json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from skimage import measure
from shapely.geometry import LineString, Polygon
import os
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
T = json.load(open('bz_tris.json'))
X0, X1, Z0, Z1, RES = 25.6, 66.6, 23.0, 56.0, 50
W, H = int((X1 - X0) * RES), int((Z1 - Z0) * RES)
C = np.load('cls.npy')            # 0 agua/nada 1 tierra 2 verde 3 roca 4 playa 5 paseo/muelle 6 acera 7 calzada 8 edificio
# ---- alturas exactas del suelo (interpolación baricéntrica de los triángulos de suelo)
Hs = np.full((H, W), np.nan, np.float32)
for nm in ['tierra', 'verde', 'verde_paseo', 'playa', 'aceras', 'calzada', 'paseo', 'roca']:
    t = np.array(T[nm]).reshape(-1, 3, 3)
    for tri in t:
        px = (tri[:, 0] - X0) * RES; pz = (tri[:, 2] - Z0) * RES; py = tri[:, 1]
        x0, x1 = int(max(0, np.floor(px.min()))), int(min(W - 1, np.ceil(px.max())))
        z0, z1 = int(max(0, np.floor(pz.min()))), int(min(H - 1, np.ceil(pz.max())))
        if x1 < x0 or z1 < z0: continue
        xs, zs = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(z0, z1 + 1) + .5)
        d = (pz[1] - pz[2]) * (px[0] - px[2]) + (px[2] - px[1]) * (pz[0] - pz[2])
        if abs(d) < 1e-9: continue
        a = ((pz[1] - pz[2]) * (xs - px[2]) + (px[2] - px[1]) * (zs - pz[2])) / d
        b = ((pz[2] - pz[0]) * (xs - px[2]) + (px[0] - px[2]) * (zs - pz[2])) / d
        c = 1 - a - b; ins = (a >= -.02) & (b >= -.02) & (c >= -.02)
        sub = Hs[z0:z1 + 1, x0:x1 + 1]
        v = a * py[0] + b * py[1] + c * py[2]
        sub[ins] = np.where(np.isnan(sub[ins]), v[ins], np.maximum(sub[ins], v[ins]))
# rellenar huecos con el vecino más cercano
msk = np.isnan(Hs); idx = ndi.distance_transform_edt(msk, return_distances=False, return_indices=True); Hs = Hs[tuple(idx)]
def h(x, z):
    i = int(np.clip((x - X0) * RES, 0, W - 1)); j = int(np.clip((z - Z0) * RES, 0, H - 1)); return float(Hs[j, i])
# ---- distancias (en unidades del mundo)
TIE = C == 1
dB = ndi.distance_transform_edt(C != 8) / RES        # a edificio
dS = ndi.distance_transform_edt(~np.isin(C, [6, 7])) / RES   # a acera o calzada
dW = ndi.distance_transform_edt(~np.isin(C, [0, 4])) / RES   # a agua o playa
# edificios etiquetados (cada parcela es la tierra más cercana a cada edificio)
lab, nlab = ndi.label(C == 8)
_, ind = ndi.distance_transform_edt(lab == 0, return_indices=True)
PAR = lab[ind[0], ind[1]]
# densidad de edificación alrededor (radio ~0.12): casco y manzanas cerradas -> solado, no jardín
dens = ndi.uniform_filter((C == 8).astype(np.float32), size=13)
CASCO = (50.6, 37.4, 54.7, 41.6)
xx = X0 + (np.arange(W) + .5) / RES; zz = Z0 + (np.arange(H) + .5) / RES
XX, ZZ = np.meshgrid(xx, zz)
enCasco = (XX > CASCO[0]) & (XX < CASCO[2]) & (ZZ > CASCO[1]) & (ZZ < CASCO[3])
# fuera: la terminal y el puerto (al norte) y la franja pegada al agua
fuera = (ZZ < 37.2) | (dW < .05)
rng = np.random.default_rng(23)
# ---- cubierta del suelo: máscara RGB a 0.04 (R césped, G prado/monte, B solado) que pinta la propia tierra en el shader
hshv = lambda a, b: (np.sin(a * 12.9898 + b * 78.233) * 43758.5453) % 1
fuera_s = (ZZ < 37.2) | (dW < .04)
okT = TIE & ~fuera_s
paved = okT & (enCasco | (dens > .42) | ((dB < .028) & (hshv(PAR.astype(np.float64), 3.1) < .45)))
lawn = okT & ~paved & (dB <= .32)
prado = okT & ~paved & (dB > .32)
def baja(m):
    f = ndi.gaussian_filter(m.astype(np.float32), .8)
    h2, w2 = f.shape[0] // 2 * 2, f.shape[1] // 2 * 2
    return f[:h2, :w2].reshape(h2 // 2, 2, w2 // 2, 2).mean((1, 3))
# la tierra junto al borde de la máscara se extiende un poco para que no asome el beige bajo las curvas de las aceras
def crece(m): return ndi.binary_dilation(m, iterations=2) & ~np.isin(C, [0, 4]) & ~(fuera_s & ~TIE)
RGB = np.stack([baja(crece(lawn) & ~paved), baja(crece(prado) & ~paved & ~lawn), baja(paved)], -1)
Image.fromarray(np.clip(RGB * 255 + .5, 0, 255).astype(np.uint8)).save(os.path.join(OUT, 'bouzas_suelo.png'), optimize=True)
print('mascara', RGB.shape, 'cesped', lawn.mean(), 'prado', prado.mean(), 'solado', paved.mean())
CEL = .04; NX, NZ = int((X1 - X0) / CEL), int((Z1 - Z0) / CEL); S = 2
cat = np.zeros((NZ, NX), np.int8)
cat[(RGB[:NZ, :NX, 0] > .5)] = 1; cat[(RGB[:NZ, :NX, 1] > .5)] = 2; cat[(RGB[:NZ, :NX, 2] > .5)] = 3
runs = []
# ---- muros de cierre: borde de la tierra habitada que da a acera/calzada
hab = TIE & ~fuera & (dB < .42)
muros = []
def simpl(pts, tol=.012):
    if len(pts) < 2: return []
    ls = LineString(pts).simplify(tol, preserve_topology=False)
    return list(ls.coords)
cs = measure.find_contours(ndi.binary_closing(hab, iterations=1).astype(float), .5)
for c in cs:
    near = []
    for (r, q) in c:
        rr, qq = int(np.clip(r, 0, H - 1)), int(np.clip(q, 0, W - 1))
        ok = dS[rr, qq] < .05 and not enCasco[rr, qq] and dB[rr, qq] > .012
        near.append(ok)
    seg = []
    def cierra():
        if len(seg) >= 5:
            pts = [(X0 + q / RES, Z0 + r / RES) for r, q in seg]
            sp = simpl(pts)
            L = LineString(sp).length if len(sp) > 1 else 0
            if L > .06:
                tipo = int(rng.choice([0, 0, 0, 1, 1, 2, 3], 1)[0])   # 0 granito, 1 enlucido blanco con albardilla, 2 granito con sebe, 3 bloque con verja
                muros.append([tipo] + [round(v, 3) for p in sp for v in (p[0], p[1], h(p[0], p[1]))])
    for k, ok in enumerate(near):
        if ok: seg.append(c[k])
        else: cierra(); seg = []
    cierra()
print('muros', len(muros), 'tramos', sum((len(m) - 1) // 3 - 1 for m in muros))
# ---- lindes entre parcelas (sebes y muros medianeros) dentro del césped
catPx = np.zeros((H, W), np.int8)
cu = cat.repeat(S, 0).repeat(S, 1); catPx[:min(H, cu.shape[0]), :min(W, cu.shape[1])] = cu[:H, :W]
jard = np.isin(catPx, [1, 2])
P2 = np.where(catPx == 1, PAR, 0)
lindes = []
bd = np.zeros((H, W), bool)
bd[:, 1:] |= (P2[:, 1:] != P2[:, :-1]) & (P2[:, 1:] > 0) & (P2[:, :-1] > 0)
bd[1:, :] |= (P2[1:, :] != P2[:-1, :]) & (P2[1:, :] > 0) & (P2[:-1, :] > 0)
lb, nl = ndi.label(ndi.binary_dilation(bd), structure=np.ones((3, 3)))
for k in range(1, nl + 1):
    ys, xs = np.where(lb == k)
    if len(xs) < 8: continue
    # recta principal de la linde (PCA)
    P = np.c_[X0 + xs / RES, Z0 + ys / RES]; m = P.mean(0); u, s_, vt = np.linalg.svd(P - m, full_matrices=False); d = vt[0]
    tt = (P - m) @ d; a, b = m + d * tt.min(), m + d * tt.max()
    if np.linalg.norm(b - a) < .05 or s_[1] / max(s_[0], 1e-6) > .35: continue
    lindes.append([int(rng.random() < .55), round(a[0], 3), round(a[1], 3), round(h(*a), 4), round(b[0], 3), round(b[1], 3), round(h(*b), 4)])
print('lindes', len(lindes))
# ---- árboles, palmeras y arbustos (Poisson por rejilla)
arb = []; pal = []; arbu = []
def poisson(maskfun, rmin, prob, seed):
    r = np.random.default_rng(seed); cell = rmin / np.sqrt(2); grid = {}; out = []
    ys, xs = np.where(maskfun)
    order = r.permutation(len(xs))
    for o in order:
        if r.random() > prob: continue
        x = X0 + (xs[o] + r.random()) / RES; z = Z0 + (ys[o] + r.random()) / RES
        gx, gz = int(x / cell), int(z / cell); ok = True
        for dx in (-2, -1, 0, 1, 2):
            for dz in (-2, -1, 0, 1, 2):
                q = grid.get((gx + dx, gz + dz))
                if q and (q[0] - x) ** 2 + (q[1] - z) ** 2 < rmin * rmin: ok = False; break
            if not ok: break
        if ok: grid[(gx, gz)] = (x, z); out.append((x, z, xs[o], ys[o]))
    return out
ok_arbol = jard & (dB > .03) & (dS > .035) & ~fuera
sub = np.zeros_like(ok_arbol); sub[::3, ::3] = True
for x, z, i, j in poisson(ok_arbol & sub, .05, .16, 5):
    p = PAR[j, i]; db = dB[j, i]; monte = db > .32
    rr = rng.random()
    if not monte and rr < .09: pal.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(.07 + rng.random() * .05, 3)]); continue
    if monte: kind = 0 if rr < .55 else 1; r_ = .045 + rng.random() * .03; hh = .18 + rng.random() * .12   # pinar y frondosas en lo no edificado
    else: kind = 1 if rr < .72 else 0; r_ = .028 + rng.random() * .026; hh = .09 + rng.random() * .09    # frutales, magnolios, cipreses
    if kind == 0 and not monte and rng.random() < .5: r_ *= .55; hh *= 1.25                                   # ciprés esbelto
    arb.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(r_, 3), round(hh, 3), int(rng.integers(0, 8)), kind])
ok_arbu = jard & (dB > .015) & (dB < .2) & (dS > .02) & ~fuera
for x, z, i, j in poisson(ok_arbu & sub, .035, .07, 9):
    arbu.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(.009 + rng.random() * .01, 3), int(rng.integers(0, 6))])
print('arboles', len(arb), 'palmeras', len(pal), 'arbustos', len(arbu))
# ---- dique del Museo do Mar: componente de edificio alargada al NO
sel = (XX > 33.0) & (XX < 36.6) & (ZZ > 38.9) & (ZZ < 41.95) & (C == 8)
lb2, n2 = ndi.label(sel)
best = max(range(1, n2 + 1), key=lambda k: (lb2 == k).sum())
cnt = measure.find_contours(np.pad((lb2 == best).astype(float), 1), .5)[0] - 1
poly = Polygon([(X0 + q / RES, Z0 + r / RES) for r, q in cnt]).simplify(.01)
ed = np.array(T['edificios']).reshape(-1, 3, 3)
print('dique area', poly.area, 'pts', len(poly.exterior.coords))
dique = [round(v, 3) for p in list(poly.exterior.coords)[:-1] for v in p]
out = {'v': 2, 'mascara': [X0, Z0, (W // 2 * 2) / RES, (H // 2 * 2) / RES], 'muros': muros, 'lindes': lindes, 'arboles': arb, 'palmeras': pal, 'arbustos': arbu, 'dique': dique, 'casco': CASCO}
s = json.dumps(out, separators=(',', ':'))
open(os.path.join(OUT, 'bouzas_jardin.json'), 'w').write(s)
print('bytes', len(s))
# vista previa
pv = np.zeros((NZ, NX, 3), np.uint8)
pv[cat == 1] = (110, 170, 80); pv[cat == 2] = (140, 150, 90); pv[cat == 3] = (170, 165, 155); pv[cat == 4] = (200, 200, 195)
im = Image.fromarray(pv).resize((NX * 2, NZ * 2), Image.NEAREST); d = ImageDraw.Draw(im)
k = 2 / CEL
for m in muros:
    p = m[1:]; d.line([((p[i] - X0) * k, (p[i + 1] - Z0) * k) for i in range(0, len(p), 3)], fill=(255, 60, 60), width=1)
for l in lindes: d.line([((l[1] - X0) * k, (l[2] - Z0) * k), ((l[4] - X0) * k, (l[5] - Z0) * k)], fill=(30, 90, 30), width=1)
for a in arb: d.point(((a[0] - X0) * k, (a[1] - Z0) * k), fill=(0, 60, 0))
for a in pal: d.point(((a[0] - X0) * k, (a[1] - Z0) * k), fill=(255, 200, 0))
im.save('prev.png')
