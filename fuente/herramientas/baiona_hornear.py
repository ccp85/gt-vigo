# Baiona con detalle, zona 1: Casco Vello y porto.
# Hornea baiona_detalle.json: muro, farolas, bancos y árboles del paseo marítimo (da Ribeira al porto deportivo),
# la réplica de la Carabela Pinta atracada en el peirao central, la lonxa y los norays del muelle pesquero,
# gamelas fondeadas en la dársena, la Colexiata de Santa María en lo alto del casco (en lugar del bloque del catastro)
# y las calles del casco con losas de granito.
# Referencias: Google Earth, Street View y fotos (solo como referencia; todo lo que sale en el juego es geometría propia).
# uso (igual que nigran_hornear.py):
#   1) glb de la zona a partir de baiona_glb_*.png (ver nigran_hornear.py)
#   2) node bouzas_glbtris.mjs baiona.glb tris.json tierra,verde,verde_paseo,playa,roca,calzada,aceras,edificios,muro_costa,muelles,agua,zocalo,barcos,piezas
#   3) python3 baiona_hornear.py tris.json RAIZ_DEL_REPO   (necesita numpy y scipy)
import json, sys, math, os
import numpy as np
from scipy import ndimage
TRIS, RAIZ = sys.argv[1], sys.argv[2]
X0, X1, Z0, Z1, RES = -51.0, -36.0, 168.0, 182.0, 40           # 40 px por unidad (1 u ≈ 78 m → píxel ≈ 2 m)
W, H = int((X1 - X0) * RES), int((Z1 - Z0) * RES)
ORDER = ['agua', 'tierra', 'verde', 'verde_paseo', 'roca', 'playa', 'muro_costa', 'muelles', 'zocalo', 'aceras', 'calzada', 'edificios', 'barcos', 'piezas']
CID = {n: i + 1 for i, n in enumerate(ORDER)}
T = json.load(open(TRIS))
Y = np.full((H, W), -9.0, np.float32); C = np.zeros((H, W), np.uint8)
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
XX, ZZ = np.meshgrid(X0 + (np.arange(W) + .5) / RES, Z0 + (np.arange(H) + .5) / RES)
def pix(x, z): return int((z - Z0) * RES), int((x - X0) * RES)
def dentro(j, i): return 0 <= j < H and 0 <= i < W
MAR = (C == 0) | (C == CID['agua']) | (C == CID['barcos'])
def media(x, z, r=.02):
    # altura del suelo alrededor (solo tierra: el agua de la orilla no cuenta)
    j, i = pix(x, z); k = max(1, int(r * RES)); sl = (slice(max(0, j - k), j + k + 1), slice(max(0, i - k), i + k + 1))
    s = Y[sl][~MAR[sl] & (Y[sl] > -5)]
    return float(np.median(s)) if s.size else 0.0
TIERRA = ~MAR
dmar = ndimage.distance_transform_edt(~MAR) / RES
dtie = ndimage.distance_transform_edt(MAR) / RES
CAL = C == CID['calzada']
dcal = ndimage.distance_transform_edt(~CAL) / RES
BAR = (C == CID['barcos']) | (C == CID['piezas']); dbar = ndimage.distance_transform_edt(~BAR) / RES
rs = [4242]
def rn():
    rs[0] = (rs[0] * 16807) % 2147483647; return rs[0] / 2147483647
R4 = lambda v: round(float(v), 4)
OUT = {}
# ---------- 1) vía principal (la avenida del paseo): calzada ancha ----------
ancho = ndimage.distance_transform_edt(CAL) / RES
VIA = ndimage.binary_dilation(ancho > .07, iterations=int(.1 * RES)) & CAL
dvia = ndimage.distance_transform_edt(~VIA) / RES
# ---------- 2) paseo marítimo: orilla junto a la avenida, de la Ribeira al porto deportivo ----------
orilla = TIERRA & ndimage.binary_dilation(MAR, iterations=1) & (dvia < .28) & (XX > -48.6) & (XX < -37.5) & (ZZ > 171.6)
pts = np.argwhere(orilla)
# eje de la costa: dirección principal de los puntos
P = np.c_[XX[orilla], ZZ[orilla]]; cen = P.mean(0); _, _, vt = np.linalg.svd(P - cen); d = vt[0]
if d[0] < 0: d = -d
s = (P - cen) @ d; o = np.argsort(s); P, s = P[o], s[o]
# un punto cada ~0,02 u, con la media de los que caen en cada tramo
TR = []
for k in np.arange(s.min(), s.max(), .02):
    m = (s >= k) & (s < k + .02)
    if m.sum(): TR.append(P[m].mean(0))
TR = np.array(TR)
# tramos continuos (se cortan en los arranques de los peiraos)
tramos = [[TR[0]]]
for p in TR[1:]:
    if np.hypot(*(p - tramos[-1][-1])) > .07: tramos.append([p])
    else: tramos[-1].append(p)
MURO, FAR, BAN, ARB = [], [], [], []
nrm = np.array([-d[1], d[0]])                                    # normal a la costa
# hacia tierra: el lado con menos mar
jx, ix = pix(*(cen + nrm * .1))
if dentro(jx, ix) and MAR[jx, ix]: nrm = -nrm
acum = 0
for t in tramos:
    t = np.array(t)
    if len(t) < 4: continue
    # suaviza
    t2 = t.copy()
    for _ in range(3): t2[1:-1] = (t2[:-2] + t2[1:-1] * 2 + t2[2:]) / 4
    lin = []
    for x, z in t2:
        x, z = x + nrm[0] * .006, z + nrm[1] * .006
        lin += [R4(x), R4(z), R4(media(x, z, .012))]
    MURO.append(lin)
    for k in range(1, len(t2)):
        acum += np.hypot(*(t2[k] - t2[k - 1]))
        x, z = t2[k]
        # el paseo es la franja entre el muro y la avenida
        if acum > .28:
            acum = 0; fx, fz = x + nrm[0] * .03, z + nrm[1] * .03
            j, i = pix(fx, fz)
            if dentro(j, i) and not MAR[j, i] and not CAL[j, i]:
                FAR.append([R4(fx), R4(fz), R4(media(fx, fz, .01))])
                # banco y árbol entre farolas
                bx, bz = x - d[0] * .14 + nrm[0] * .026, z - d[1] * .14 + nrm[1] * .026
                j, i = pix(bx, bz)
                if dentro(j, i) and not MAR[j, i] and not CAL[j, i]:
                    BAN.append([R4(bx), R4(bz), R4(media(bx, bz, .01)), R4(math.atan2(-nrm[1], -nrm[0]))])
                ax, az = x - d[0] * .07 + nrm[0] * .05, z - d[1] * .07 + nrm[1] * .05
                j, i = pix(ax, az)
                if dentro(j, i) and not MAR[j, i] and not CAL[j, i] and dvia[j, i] > .012:
                    ARB.append([R4(ax), R4(az), R4(media(ax, az, .01)), round(rn(), 2)])
OUT['paseo'] = {'muro': MURO, 'farolas': FAR, 'bancos': BAN, 'arboles': ARB}
# ---------- 3) Carabela Pinta: atracada en el lado sur del peirao central ----------
# peirao central: el brazo de tierra que sale de la avenida hacia el norte entre los dos puertos deportivos
REG = TIERRA & (XX > -45) & (XX < -43.0) & (ZZ > 174.0) & (ZZ < 175.4) & ~VIA
P2 = np.c_[XX[REG], ZZ[REG]]; c2 = P2.mean(0); _, _, v2 = np.linalg.svd(P2 - c2); dm = v2[0]
if dm[0] < 0: dm = -dm
nm_ = np.array([-dm[1], dm[0]])
if nm_[1] < 0: nm_ = -nm_                                       # hacia el sur (dársena)
# borde sur del peirao, a mitad de largo
best = None
for u in np.linspace(-.25, .25, 26):
    for v in np.arange(0, .6, .005):
        x, z = c2 + dm * u + nm_ * v; j, i = pix(x, z)
        if dentro(j, i) and MAR[j, i]:
            # la carabela entera (0,27 × 0,08) tiene que caber en el agua
            ok = True
            for a in np.linspace(-.15, .15, 9):
                for b in (.02, .06, .1):
                    jj, ii = pix(*(np.array([x, z]) + dm * a + nm_ * b))
                    if not (dentro(jj, ii) and MAR[jj, ii] and dbar[jj, ii] > .03): ok = False
            if ok and (best is None or abs(u) < abs(best[0])): best = (u, x, z)
            break
u, x, z = best
cx, cz = np.array([x, z]) + nm_ * .052
OUT['carabela'] = [R4(cx), R4(cz), R4(math.atan2(dm[1], dm[0])), R4(media(x - nm_[0] * .05, z - nm_[1] * .05, .015)), R4(x - nm_[0] * .03), R4(z - nm_[1] * .03)]
# ---------- 4) muelle pesquero: lonxa y norays ----------
REGP = TIERRA & (XX > -43.7) & (XX < -42.0) & (ZZ > 175.6) & (ZZ < 176.9) & ~VIA
LIB = REGP & ~CAL & (C != CID['edificios'])
dlib = ndimage.distance_transform_edt(LIB) / RES
k = np.argmax(np.where(LIB, dlib - np.hypot(XX - (-43.15), ZZ - 176.0) * .05, -9)); lx, lz = XX.flat[k], ZZ.flat[k]
rmax = float(dlib.flat[k])
OUT['lonxa'] = [R4(lx), R4(lz), R4(media(lx, lz, .02)), R4(math.atan2(dm[1], dm[0])), R4(min(.24, rmax * 2.4)), R4(min(.11, rmax * 1.5))]
NOR = []
bord = (REGP | (TIERRA & (XX > -45) & (XX < -42.8) & (ZZ > 173.6) & (ZZ < 175.4) & ~VIA)) & ndimage.binary_dilation(MAR, iterations=1) & (dvia > .1)
pb = np.argwhere(bord); ocu = []
for j, i in pb[np.argsort(pb[:, 0] * 10000 + pb[:, 1])]:
    x, z = XX[j, i], ZZ[j, i]
    if any((x - a) ** 2 + (z - b) ** 2 < .07 ** 2 for a, b in ocu): continue
    ocu.append((x, z)); x2, z2 = x + 0, z + 0
    # un poco hacia dentro del muelle
    gj = dmar[min(H - 1, j + 1), i] - dmar[max(0, j - 1), i]; gi = dmar[j, min(W - 1, i + 1)] - dmar[j, max(0, i - 1)]; n = math.hypot(gi, gj) or 1
    NOR.append([R4(x + gi / n * .012), R4(z + gj / n * .012), R4(media(x, z, .008))])
OUT['norays'] = NOR
# ---------- 5) gamelas fondeadas en la dársena, entre el peirao central y el muelle pesquero ----------
GAM = []; oc = [(OUT['carabela'][0] + dm[0] * a, OUT['carabela'][1] + dm[1] * a) for a in (-.12, 0, .12)]
cand = MAR & (dtie > .04) & (dtie < .3) & (dbar > .06) & (XX > -45) & (XX < -42.75) & (ZZ > 174.6) & (ZZ < 176.4)
ii = np.argwhere(cand)
for _ in range(20000):
    if len(GAM) >= 26 or not len(ii): break
    j, i = ii[int(rn() * len(ii))]; x, z = XX[j, i], ZZ[j, i]
    if any((x - a) ** 2 + (z - b) ** 2 < .1 ** 2 for a, b in oc): continue
    oc.append((x, z)); GAM.append([R4(x), R4(z), int(rn() * 3 > 2), int(rn() * 8), R4(rn() * 6.28), round(rn(), 3)])
OUT['gamelas'] = GAM
# ---------- 6) Colexiata de Santa María: el bloque grande de lo alto del casco ----------
ED = C == CID['edificios']
lab, nl = ndimage.label(ED)
# la iglesia (unos 40 × 20 m, orientada al oeste) es el bloque del catastro junto al atrio con el cruceiro, en lo alto del casco
j, i = pix(-48.1, 176.57); m = lab == lab[j, i]
assert lab[j, i] and m.sum() < 40 * 40, m.sum()
# rectángulo orientado que encierra el bloque
P3 = np.c_[XX[m], ZZ[m]]; c3 = P3.mean(0); _, _, v3 = np.linalg.svd(P3 - c3); de = v3[0]
pu, pv = (P3 - c3) @ de, (P3 - c3) @ np.array([-de[1], de[0]])
cc = c3 + de * (pu.max() + pu.min()) / 2 + np.array([-de[1], de[0]]) * (pv.max() + pv.min()) / 2
Lc, Wc = pu.max() - pu.min() + 2 / RES, pv.max() - pv.min() + 2 / RES
# la fachada mira al oeste, como en las iglesias románicas
if de[0] > 0: de = -de
ang = math.atan2(de[1], de[0])
quita = []
for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
    q = cc + de * su * (Lc / 2 + .01) + np.array([-de[1], de[0]]) * sv * (Wc / 2 + .01); quita += [R4(q[0]), R4(q[1])]
ys = Y[m & ~ED] if (m & ~ED).any() else None
yb = float(np.percentile(Y[ndimage.binary_dilation(m, iterations=3) & ~ED & ~MAR], 30))
OUT['colexiata'] = {'x': R4(cc[0]), 'z': R4(cc[1]), 'y': R4(yb), 'a': R4(ang), 'l': R4(Lc), 'w': R4(Wc), 'quita': quita}
# ---------- 7) calles del casco con losas de granito: rejilla de celdas sobre las rúas peatonales, aceras y calles estrechas (sin la avenida) ----------
S = .025; gx0, gz0, gx1, gz1 = -50.6, 172.4, -44.2, 178.4
gw, gh = int((gx1 - gx0) / S) + 1, int((gz1 - gz0) / S) + 1
casco = ((CAL & ~ndimage.binary_dilation(VIA, iterations=2)) | (C == CID['aceras'])) & (dvia > .01)
GK = []
for j in range(gh):
    for i in range(gw):
        x, z = gx0 + i * S, gz0 + j * S; jj, ii_ = pix(x, z)
        GK.append('1' if dentro(jj, ii_) and casco[jj, ii_] else '0')
OUT['losas'] = {'x0': gx0, 'z0': gz0, 's': S, 'w': gw, 'h': gh, 'k': ''.join(GK)}
json.dump(OUT, open(os.path.join(RAIZ, 'baiona_detalle.json'), 'w'), separators=(',', ':'))
print('paseo: muro', len(MURO), sum(len(m) // 3 for m in MURO), 'farolas', len(FAR), 'bancos', len(BAN), 'arboles', len(ARB))
print('carabela', OUT['carabela'], 'lonxa', OUT['lonxa'], 'norays', len(NOR), 'gamelas', len(GAM))
print('colexiata', OUT['colexiata'], 'losas', GK.count('1'))
