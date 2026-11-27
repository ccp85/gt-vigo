# Baiona con detalle, zona 2: la fortaleza de Monterreal (Parador).
# Añade la clave 'monterreal' a baiona_detalle.json: almenas sobre el borde exterior de la muralla, garitas en las
# esquinas, la Torre do Reloxo, la Torre do Príncipe y la Tenaza, la puerta de entrada con el escudo, el paseo perimetral
# por fuera de la muralla junto al mar, bolos de granito en las calas y tres miradores (puntos de foto del GPS).
# Referencias: Google Earth, Street View y fotos (solo como referencia; todo lo que sale en el juego es geometría propia).
# uso: los mismos pasos 1) y 2) que baiona_hornear.py (con 'piezas' en la lista de mallas) y luego
#   3) python3 monterreal_hornear.py tris.json RAIZ_DEL_REPO   (necesita numpy, scipy y scikit-image)
import json, sys, math, os
import numpy as np
from scipy import ndimage
from skimage import measure
TRIS, RAIZ = sys.argv[1], sys.argv[2]
X0, X1, Z0, Z1, RES = -51.2, -44.0, 163.4, 171.8, 80          # 80 px por unidad (píxel ≈ 1 m)
W, H = int((X1 - X0) * RES), int((Z1 - Z0) * RES)
ORDER = ['agua', 'tierra', 'verde', 'verde_paseo', 'roca', 'playa', 'muro_costa', 'muelles', 'aceras', 'calzada', 'edificios', 'barcos', 'piezas']
CID = {n: i + 1 for i, n in enumerate(ORDER)}
T = json.load(open(TRIS))
Y = np.full((H, W), -9.0, np.float32); C = np.zeros((H, W), np.uint8); YS = np.full((H, W), -9.0, np.float32)   # YS: suelo sin piezas
for nm in ORDER:
    t = np.array(T.get(nm, []), np.float64).reshape(-1, 3, 3)
    if not len(t): continue
    xs, zs = t[:, :, 0], t[:, :, 2]
    t = t[(xs.max(1) > X0) & (xs.min(1) < X1) & (zs.max(1) > Z0) & (zs.min(1) < Z1)]
    for tri in t:
        px = (tri[:, 0] - X0) * RES; pz = (tri[:, 2] - Z0) * RES
        i0, i1 = max(0, int(np.floor(px.min()))), min(W - 1, int(np.ceil(px.max())))
        j0, j1 = max(0, int(np.floor(pz.min()))), min(H - 1, int(np.ceil(pz.max())))
        if i1 < i0 or j1 < j0: continue
        ii, jj = np.meshgrid(np.arange(i0, i1 + 1) + .5, np.arange(j0, j1 + 1) + .5)
        (x0, x1, x2), (z0, z1, z2) = px, pz
        den = (z1 - z2) * (x0 - x2) + (x2 - x1) * (z0 - z2)
        if abs(den) < 1e-9: continue
        a = ((z1 - z2) * (ii - x2) + (x2 - x1) * (jj - z2)) / den; b = ((z2 - z0) * (ii - x2) + (x0 - x2) * (jj - z2)) / den; c = 1 - a - b
        ins = (a >= -1e-6) & (b >= -1e-6) & (c >= -1e-6)
        if not ins.any(): continue
        y = a * tri[0, 1] + b * tri[1, 1] + c * tri[2, 1]
        sub = Y[j0:j1 + 1, i0:i1 + 1]; sc = C[j0:j1 + 1, i0:i1 + 1]
        u = ins & (y >= sub - .002); sub[u] = y[u]; sc[u] = CID[nm]
        if nm != 'piezas':
            s2 = YS[j0:j1 + 1, i0:i1 + 1]; u2 = ins & (y >= s2 - .002); s2[u2] = y[u2]
XX, ZZ = np.meshgrid(X0 + (np.arange(W) + .5) / RES, Z0 + (np.arange(H) + .5) / RES)
def pix(x, z): return int((z - Z0) * RES), int((x - X0) * RES)
def dentro(j, i): return 0 <= j < H and 0 <= i < W
MAR = (C == 0) | (C == CID['agua']) | (C == CID['barcos'])
dmar = ndimage.distance_transform_edt(~MAR) / RES
def suelo(x, z, r=.012):
    j, i = pix(x, z); k = max(1, int(r * RES)); sl = (slice(max(0, j - k), j + k + 1), slice(max(0, i - k), i + k + 1))
    s = YS[sl][~MAR[sl] & (YS[sl] > -5)]
    return float(np.median(s)) if s.size else 0.0
rs = [777]
def rn():
    rs[0] = (rs[0] * 16807) % 2147483647; return rs[0] / 2147483647
R4 = lambda v: round(float(v), 4)
OUT = {}
# península: todo lo que no es mar al norte de la playa de la Ribeira
PEN = ~MAR & (ZZ < 171.2) & ~((XX > -46.3) & (ZZ > 168.6))
PEN &= ~((XX > -44.6))                                            # sin el dique
# ---------- 1) muralla: bordes de la cara superior de las piezas ----------
P = np.array(T['piezas'], np.float64).reshape(-1, 3, 3)
cen = P.mean(1)
P = P[(cen[:, 0] > -50.9) & (cen[:, 0] < -44.4) & (cen[:, 2] > 163.6) & (cen[:, 2] < 171.25)]
nrm = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
top = P[(np.abs(nrm[:, 1]) > .9) & (P[:, :, 1].min(1) > .05)]
# aristas de borde: las que pertenecen a un solo triángulo de las caras de arriba
key = lambda p: (round(p[0], 4), round(p[2], 4))
# las caras de arriba vienen repetidas (dos veces la misma): una sola de cada
vistos = set(); tops = []
for tri in top:
    k = tuple(sorted(key(p) for p in tri))
    if k not in vistos: vistos.add(k); tops.append(tri)
top = np.array(tops)
cnt = {}
for tri in top:
    for a, b in ((0, 1), (1, 2), (2, 0)):
        k = tuple(sorted([key(tri[a]), key(tri[b])])); cnt.setdefault(k, []).append((tri[a], tri[b], tri.mean(0)))
bordes = [v[0] for k, v in cnt.items() if len(v) == 1]
# lado de fuera: el lado con el suelo más bajo (la muralla da al mar o a la ladera)
ALM, CORN = [], []
for a, b, cc in bordes:
    d = b - a; L = math.hypot(d[0], d[2])
    if L < .004: continue
    tx, tz = d[0] / L, d[2] / L; nx, nz = -tz, tx
    mx, mz = (a[0] + b[0]) / 2, (a[2] + b[2]) / 2
    if (cc[0] - mx) * nx + (cc[2] - mz) * nz > 0: nx, nz = -nx, -nz     # normal hacia fuera de la cara de arriba
    yo = suelo(mx + nx * .03, mz + nz * .03, .008); yi = suelo(mx - nx * .06, mz - nz * .06, .008)
    if not (yo < yi - .01): continue                                   # solo el borde que mira hacia fuera y abajo
    y = (a[1] + b[1]) / 2
    n = max(1, int(L / .012))
    for k in range(n):
        u = (k + .5) / n
        ALM.append([R4(a[0] + d[0] * u - nx * .0025), R4(a[2] + d[2] * u - nz * .0025), R4(y), R4(math.atan2(tz, tx))])
    CORN.append((a[0], a[2], b[0], b[2], y, nx, nz))
# garitas: en las esquinas salientes del borde de fuera (giro fuerte entre aristas que se tocan)
ext = {}
for ax, az, bx, bz, y, nx, nz in CORN:
    for p, q in (((ax, az), (bx, bz)), ((bx, bz), (ax, az))):
        ext.setdefault((round(p[0], 3), round(p[1], 3)), []).append((q, y, nx, nz))
GAR = []
for p, L in ext.items():
    if len(L) != 2: continue
    (q1, y, n1x, n1z), (q2, _, n2x, n2z) = L
    if n1x * n2x + n1z * n2z > .45: continue                          # casi recto
    ox, oz = n1x + n2x, n1z + n2z; on = math.hypot(ox, oz) or 1
    # saliente: la bisectriz de las normales apunta fuera
    if any(math.hypot(p[0] - g[0], p[1] - g[1]) < 1.0 for g in GAR): continue
    GAR.append([R4(p[0] + ox / on * .004), R4(p[1] + oz / on * .004), R4(y), R4(math.atan2(oz / on, ox / on))])
OUT['almenas'] = ALM; OUT['garitas'] = GAR
# punto del borde exterior más cercano a (x, z): para poner las torres sobre la muralla
def enMuro(x, z):
    best = None
    for ax, az, bx, bz, y, nx, nz in CORN:
        dx, dz = bx - ax, bz - az; l2 = dx * dx + dz * dz
        u = max(0, min(1, ((x - ax) * dx + (z - az) * dz) / l2)); px, pz = ax + dx * u, az + dz * u
        d = math.hypot(px - x, pz - z)
        if best is None or d < best[0]: best = (d, px, pz, y, nx, nz)
    return best[1:]
# ---------- 2) torres: do Reloxo (NE, mirando a la bahía), do Príncipe (O, al océano) y la Tenaza (E, la boca del porto) ----------
TOR = {}
for nom, (x, z) in {'reloxo': (-46.95, 167.3), 'principe': (-49.95, 166.3), 'tenaza': (-45.05, 167.85)}.items():
    px, pz, y, nx, nz = enMuro(x, z)
    # si ya hay una torre del mapa ahí, la nueva arranca por encima de ella
    cx_, cz_ = px - nx * .02, pz - nz * .02
    cer = top[np.hypot(top[:, :, 0].mean(1) - cx_, top[:, :, 2].mean(1) - cz_) < .07]
    if len(cer): y = max(y, float(cer[:, :, 1].max()))
    TOR[nom] = [R4(px - nx * .02), R4(pz - nz * .02), R4(y), R4(math.atan2(nz, nx)), R4(suelo(px - nx * .08, pz - nz * .08))]
OUT['torres'] = TOR
# ---------- 3) puerta de entrada: donde la carretera cruza la muralla por el sur ----------
CAL = C == CID['calzada']; PZ = C == CID['piezas']
cerca = CAL & (ndimage.distance_transform_edt(~PZ) / RES < .03) & (ZZ > 168.3) & (XX > -47.8) & (XX < -46.2)
lab, nl = ndimage.label(cerca)
print('cruces carretera-muralla', [(round(float(XX[lab == l].mean()), 2), round(float(ZZ[lab == l].mean()), 2), int((lab == l).sum())) for l in range(1, nl + 1)])
l = min(range(1, nl + 1), key=lambda l: math.hypot(XX[lab == l].mean() + 46.9, ZZ[lab == l].mean() - 169.0))
gx, gz = XX[lab == l].mean(), ZZ[lab == l].mean()
loc = CAL & (np.hypot(XX - gx, ZZ - gz) < .12)
Pp = np.c_[XX[loc], ZZ[loc]]; _, _, vt = np.linalg.svd(Pp - Pp.mean(0)); dr = vt[0]
anch = ndimage.distance_transform_edt(CAL) / RES
j, i = pix(gx, gz)
OUT['puerta'] = [R4(gx), R4(gz), R4(suelo(gx, gz, .01)), R4(math.atan2(dr[1], dr[0])), R4(max(.03, min(.06, float(anch[max(0, j - 4):j + 5, max(0, i - 4):i + 5].max()) * 2 + .006)))]
# ---------- 4) paseo perimetral: senda por fuera de la muralla, siguiendo la costa ----------
dpz = ndimage.distance_transform_edt(~PZ) / RES
cont = measure.find_contours(np.where(PEN | MAR, dmar, 0).astype(float), .085)
SEN = []
for cc in cont:
    pts = [(X0 + (q[1] + .5) / RES, Z0 + (q[0] + .5) / RES) for q in cc]
    tramo = []
    def corta():
        global tramo
        if len(tramo) > 12:
            lin = []
            for k in range(0, len(tramo), 3):
                x, z = tramo[k]; lin += [R4(x), R4(z), R4(suelo(x, z, .006))]
            SEN.append(lin)
        tramo = []
    for x, z in pts:
        j, i = pix(x, z)
        ok = dentro(j, i) and PEN[j, i] and dpz[j, i] > .02 and C[j, i] not in (CID['calzada'], CID['edificios'], CID['aceras'], CID['playa'])
        if ok and (not tramo or math.hypot(x - tramo[-1][0], z - tramo[-1][1]) < .05): tramo.append((x, z))
        else: corta()
    corta()
OUT['senda'] = SEN
# ---------- 5) bolos de granito en las calas y las puntas ----------
BOL = []; usados = []
costa = PEN & (dmar < .07) & (C != CID['playa']) & (dpz > .015)
ii = np.argwhere(costa)
for _ in range(30000):
    if len(BOL) >= 750 or not len(ii): break
    j, i = ii[int(rn() * len(ii))]; x, z = XX[j, i] + (rn() - .5) / RES, ZZ[j, i] + (rn() - .5) / RES
    r = .006 + rn() ** 2 * .022 * (1.2 - dmar[j, i] * 8)
    if any((x - a) ** 2 + (z - b) ** 2 < (r + c) ** 2 * .8 for a, b, c in usados[-300:]): continue
    usados.append((x, z, r)); BOL.append([R4(x), R4(z), R4(min(YS[j, i], .05) - r * .3), R4(r), round(rn(), 3)])
OUT['bolos'] = BOL
# ---------- 6) miradores (puntos de foto): sobre la senda, mirando al mar ----------
def puntoSenda(x, z):
    best = None
    for s in SEN:
        for k in range(0, len(s), 3):
            d = math.hypot(s[k] - x, s[k + 1] - z)
            if best is None or d < best[0]: best = (d, s[k], s[k + 1], s[k + 2])
    return best[1:]
MIR = []
for nom, (x, z), mira in [('Mirador do Príncipe', (-50.35, 166.4), 'las Cíes y el océano'), ('Mirador da Tenaza', (-45.2, 168.35), 'el porto y la villa'), ('Mirador da Punta', (-49.4, 164.2), 'la ría y Monteferro')]:
    px, pz, y = puntoSenda(x, z)
    # mira al mar más cercano
    best = (9, 0)
    for a in np.linspace(0, 6.283, 72, endpoint=False):
        for q in np.arange(.02, .6, .01):
            j, i = pix(px + math.cos(a) * q, pz + math.sin(a) * q)
            if dentro(j, i) and MAR[j, i]:
                if q < best[0]: best = (q, a)
                break
    MIR.append([nom, R4(px), R4(pz), R4(y), R4(best[1]), mira])
OUT['miradores'] = MIR
p = os.path.join(RAIZ, 'baiona_detalle.json')
D = json.load(open(p)); D['monterreal'] = OUT
json.dump(D, open(p, 'w'), separators=(',', ':'))
print('almenas', len(ALM), 'garitas', len(GAR), 'torres', TOR, 'puerta', OUT['puerta'])
print('senda', len(SEN), sum(len(s) // 3 for s in SEN), 'bolos', len(BOL), 'miradores', MIR)
