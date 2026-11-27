# Hornea <zona>_jardin.json y <zona>_suelo.png a partir de las mallas de una zona (sacadas del glb con bouzas_glbtris.mjs).
# Uso: python3 bouzas_raster.py '{"tris":"teis_tris.json","pre":"teis_","rect":[x0,x1,z0,z1]}'
#      python3 bouzas_hornear.py '{"zona":"teis","tris":"teis_tris.json","pre":"teis_","rect":[...],"out":RAIZ, ...}'
# Ajustes usados:
#  Bouzas: {"cascos":[[50.6,37.4,54.7,41.6]],"fuera":"ZZ < 37.2","dique":[33.0,38.9,36.6,41.95]}, rect [25.6,66.6,23.0,56.0]
#  Teis:   {"nave":0.12,"euca":0.45,"pav":1,"prob":0.15,"bosque":0.22,"postes":0.55,"madera":0.35,"parras":0.07,
#           "huerta":0.35,"tiposMuro":[0,0,0,3,3,3,2,1]}, rect [110.0,147.0,-38.4,-2.0]
# (antes: cubierta del suelo,
# cubierta del suelo de las parcelas (césped, prado, solado de granito), muros de cierre y sebes, árboles de jardín,
# palmeras y arbustos, y el contorno del dique del Museo do Mar.
import json, sys, os, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from skimage import measure
from shapely.geometry import LineString, Polygon
CFG = json.loads(sys.argv[1])
T = json.load(open(CFG['tris'])); PRE = CFG['pre']; OUT = CFG.get('out', '.')
X0, X1, Z0, Z1 = CFG['rect']; RES = 50
W, H = int((X1 - X0) * RES), int((Z1 - Z0) * RES)
C = np.load(PRE + 'cls.npy')            # 0 agua/nada 1 tierra 2 verde 3 roca 4 playa 5 paseo/muelle 6 acera 7 calzada 8 edificio
# ---- alturas exactas del suelo (interpolación baricéntrica de los triángulos de suelo)
Hs = np.full((H, W), np.nan, np.float32)
for nm in ['tierra', 'verde', 'verde_paseo', 'playa', 'aceras', 'calzada', 'paseo', 'roca']:
    if nm not in T: continue
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
CASCOS = CFG.get('cascos', [])
xx = X0 + (np.arange(W) + .5) / RES; zz = Z0 + (np.arange(H) + .5) / RES
XX, ZZ = np.meshgrid(xx, zz)
enCasco = np.zeros_like(XX, bool)
for c_ in CASCOS: enCasco |= (XX > c_[0]) & (XX < c_[2]) & (ZZ > c_[1]) & (ZZ < c_[3])
# naves y edificios grandes: su tierra alrededor es patio industrial solado, no jardín
area = ndi.sum(np.ones_like(lab), lab, index=np.arange(nlab + 1)) / RES / RES
grande = area[PAR] > CFG.get('nave', 9.0)
# fuera: la terminal y el puerto (al norte) y la franja pegada al agua
fuera = eval(CFG.get('fuera', 'np.zeros_like(XX, bool)')) | (dW < .05)
rng = np.random.default_rng(23)
# ---- cubierta del suelo: máscara RGB a 0.04 (R césped, G prado/monte, B solado) que pinta la propia tierra en el shader
hshv = lambda a, b: (np.sin(a * 12.9898 + b * 78.233) * 43758.5453) % 1
fuera_s = eval(CFG.get('fuera', 'np.zeros_like(XX, bool)')) | (dW < .04)
okT = TIE & ~fuera_s
paved = okT & (enCasco | (dens > .42) | (grande & (dB < .25)) | ((dB < .028) & (hshv(PAR.astype(np.float64), 3.1) < .45)))
lawn = okT & ~paved & (dB <= .32)
prado = okT & ~paved & (dB > .32)
def baja(m):
    f = ndi.gaussian_filter(m.astype(np.float32), .8)
    h2, w2 = f.shape[0] // 2 * 2, f.shape[1] // 2 * 2
    return f[:h2, :w2].reshape(h2 // 2, 2, w2 // 2, 2).mean((1, 3))
# la tierra junto al borde de la máscara se extiende un poco para que no asome el beige bajo las curvas de las aceras
def crece(m): return ndi.binary_dilation(m, iterations=2) & ~np.isin(C, [0, 4]) & ~(fuera_s & ~TIE)
RGB = np.stack([baja(crece(lawn) & ~paved), baja(crece(prado) & ~paved & ~lawn), baja(paved)], -1)
Image.fromarray(np.clip(RGB * 255 + .5, 0, 255).astype(np.uint8)).save(os.path.join(OUT, CFG['zona'] + '_suelo.png'), optimize=True)
print('mascara', RGB.shape, 'cesped', lawn.mean(), 'prado', prado.mean(), 'solado', paved.mean())
CEL = .04; NX, NZ = int((X1 - X0) / CEL), int((Z1 - Z0) / CEL); S = 2
cat = np.zeros((NZ, NX), np.int8)
cat[(RGB[:NZ, :NX, 0] > .5)] = 1; cat[(RGB[:NZ, :NX, 1] > .5)] = 2; cat[(RGB[:NZ, :NX, 2] > .5)] = 3
runs = []
# ---- muros de cierre: borde de la tierra habitada que da a acera/calzada
hab = TIE & ~fuera & (dB < .42) & ~grande
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
        ok = dS[rr, qq] < .05 and not enCasco[rr, qq] and dB[rr, qq] > .012 and not grande[rr, qq]
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
ok_arbol &= ~grande
for x, z, i, j in poisson(ok_arbol & sub, CFG.get('rmin', .05), CFG.get('prob', .16), 5):
    p = PAR[j, i]; db = dB[j, i]; monte = db > .32
    rr = rng.random()
    if not monte and rr < .09: pal.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(.07 + rng.random() * .05, 3)]); continue
    if monte and rr < CFG.get('euca', 0):   # eucalipto: alto, estrecho y gris verdoso
        arb.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(.03 + rng.random() * .015, 3), round(.26 + rng.random() * .14, 3), 8 + int(rng.integers(0, 2)), 1]); continue
    if monte: kind = 0 if rr < .55 else 1; r_ = .045 + rng.random() * .03; hh = .18 + rng.random() * .12   # pinar y frondosas en lo no edificado
    else: kind = 1 if rr < .72 else 0; r_ = .028 + rng.random() * .026; hh = .09 + rng.random() * .09    # frutales, magnolios, cipreses
    if kind == 0 and not monte and rng.random() < .5: r_ *= .55; hh *= 1.25                                   # ciprés esbelto
    arb.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(r_, 3), round(hh, 3), int(rng.integers(0, 8)), kind])
ok_arbu = jard & (dB > .015) & (dB < .2) & (dS > .02) & ~fuera
for x, z, i, j in poisson(ok_arbu & sub, .035, .07, 9):
    arbu.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(.009 + rng.random() * .01, 3), int(rng.integers(0, 6))])
print('arboles', len(arb), 'palmeras', len(pal), 'arbustos', len(arbu))
dique = []
if CFG.get('dique'):
    q0 = CFG['dique']
    sel = (XX > q0[0]) & (XX < q0[2]) & (ZZ > q0[1]) & (ZZ < q0[3]) & (C == 8)
    lb2, n2 = ndi.label(sel)
    best = max(range(1, n2 + 1), key=lambda k: (lb2 == k).sum())
    cnt = measure.find_contours(np.pad((lb2 == best).astype(float), 1), .5)[0] - 1
    poly = Polygon([(X0 + q / RES, Z0 + r / RES) for r, q in cnt]).simplify(.01)
    dique = [round(v, 3) for p in list(poly.exterior.coords)[:-1] for v in p]
# ---- postes de la luz a lo largo de los muros que dan a la calle, con el tendido entre postes seguidos
postes = []; cables = []
if CFG.get('postes'):
    pr = np.random.default_rng(31)
    for m in muros:
        P = np.array(m[1:]).reshape(-1, 3); seg = np.linalg.norm(np.diff(P[:, :2], axis=0), axis=1); L = seg.sum()
        if L < .5: continue
        cum = np.r_[0, np.cumsum(seg)]; prev = None
        for d in np.arange(.15 + pr.random() * .2, L, CFG['postes']):
            k = min(len(seg) - 1, np.searchsorted(cum, d) - 1); f = (d - cum[k]) / max(seg[k], 1e-6)
            p = P[k] + (P[k + 1] - P[k]) * f; dx, dz = P[k + 1][:2] - P[k][:2]
            # un poco hacia la calle (fuera de la parcela): el lado con acera/calzada más cerca
            n = np.array([-dz, dx]) / max(np.hypot(dx, dz), 1e-6)
            best = None
            for sgn in (1, -1):
                q = p[:2] + n * .012 * sgn; ii = int((q[0] - X0) * RES); jj = int((q[1] - Z0) * RES)
                if 0 <= ii < W and 0 <= jj < H and np.isin(C[jj, ii], [6, 7]): best = q; break
            q = best if best is not None else p[:2]
            postes.append([round(q[0], 3), round(q[1], 3), round(h(q[0], q[1]), 4), round(float(-np.arctan2(dz, dx)), 2), int(pr.random() < CFG.get('madera', .3))])
            if prev is not None: cables.append([prev, len(postes) - 1])
            prev = len(postes) - 1
print('postes', len(postes), 'cables', len(cables))
# ---- parras sobre emparrado en algunos jardines
parras = []
if CFG.get('parras'):
    pr = np.random.default_rng(41); usados = set()
    ys, xs = np.where((catPx == 1) & (dB > .04) & (dB < .14) & (dS > .05))
    for o in pr.permutation(len(xs))[:200000]:
        p = PAR[ys[o], xs[o]]
        if p in usados or hshv(float(p), 5.5) > CFG['parras']: continue
        usados.add(p); x = X0 + xs[o] / RES; z = Z0 + ys[o] / RES
        parras.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(pr.random() * 3.14, 2), round(.05 + pr.random() * .03, 3), round(.035 + pr.random() * .025, 3)])
print('parras', len(parras))
# ---- bosque denso en el monte (eucaliptos y pinos)
if CFG.get('bosque'):
    okm = (catPx == 2) & (dB > .3) & (dS > .04) & ~fuera
    for x, z, i, j in poisson(okm & sub, .045, CFG['bosque'], 13):
        rr = rng.random()
        if rr < CFG.get('euca', 0): arb.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(.03 + rng.random() * .015, 3), round(.26 + rng.random() * .14, 3), 8 + int(rng.integers(0, 2)), 1])
        else: arb.append([round(x, 3), round(z, 3), round(h(x, z), 4), round(.04 + rng.random() * .03, 3), round(.17 + rng.random() * .12, 3), int(rng.integers(0, 8)), 0 if rr < .8 else 1])
    print('arboles con bosque', len(arb))
out = {'v': 2, 'mascara': [X0, Z0, (W // 2 * 2) / RES, (H // 2 * 2) / RES], 'muros': muros, 'lindes': lindes, 'arboles': arb, 'palmeras': pal, 'arbustos': arbu, 'dique': dique, 'pav': CFG.get('pav', 0), 'huerta': CFG.get('huerta', 0), 'postes': postes, 'cables': cables, 'parras': parras}
if CFG.get('tiposMuro'): out['tiposMuro'] = CFG['tiposMuro']
s = json.dumps(out, separators=(',', ':'))
open(os.path.join(OUT, CFG['zona'] + '_jardin.json'), 'w').write(s)
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
im.save(PRE + 'prev.png')
