# Nigrán con detalle: zona 1 (Patos – Prado – Monteferro) y zona 2 (Panxón: puerto, Templo Votivo do Mar y barcas).
# Hornea nigran_detalle.json y añade el pinar de Monteferro a baiona_inst.json.
# Referencias: Google Earth (satélite), Street View y fotos de la playa de Patos, Prado, el Monumento a la Marina Universal,
# la batería J-3 y el Mirador de las Estelas (solo como referencia; todo lo que sale en el juego es geometría propia).
# uso:
#   1) glb de la zona a partir de baiona_glb_*.png (cada parte: bytes RGB con 4 bytes de largo delante):
#      python3 -c "import json,numpy as np;from PIL import Image;pj=json.load(open('baiona_partes.json'));o=b''
#      for i in range(pj['partes']): r=np.array(Image.open(f'baiona_glb_{i+1}.png').convert('RGB')).tobytes();n=int.from_bytes(r[:4],'little');o+=r[4:4+n]
#      open('baiona.glb','wb').write(o)"
#   2) node bouzas_glbtris.mjs baiona.glb tris.json tierra,verde,verde_paseo,playa,roca,calzada,aceras,edificios,muro_costa,muelles,agua,zocalo
#   3) python3 nigran_hornear.py tris.json RAIZ_DEL_REPO   (necesita numpy y scipy)
# El script es repetible: quita antes los árboles que añadió la vez anterior (llevan la marca a[7]=1).
import json, sys, math, os
import numpy as np
TRIS, RAIZ = sys.argv[1], sys.argv[2]
X0, X1, Z0, Z1, RES = -50.0, -8.0, 112.0, 142.0, 25          # 25 px por unidad (1 u ≈ 78 m → píxel ≈ 3 m)
W, H = int((X1 - X0) * RES), int((Z1 - Z0) * RES)
ORDER = ['agua', 'tierra', 'verde', 'verde_paseo', 'roca', 'playa', 'muro_costa', 'muelles', 'zocalo', 'aceras', 'calzada', 'edificios']
CID = {n: i + 1 for i, n in enumerate(ORDER)}
# ---------- 1) raster: superficie más alta y su tipo ----------
T = json.load(open(TRIS))
def rasteriza(x0_, x1_, z0_, z1_):
    global X0, X1, Z0, Z1, W, H, Y, C, XX, ZZ
    X0, X1, Z0, Z1 = x0_, x1_, z0_, z1_; W, H = int((X1 - X0) * RES), int((Z1 - Z0) * RES)
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
    xs = X0 + (np.arange(W) + .5) / RES; zs = Z0 + (np.arange(H) + .5) / RES
    XX, ZZ = np.meshgrid(xs, zs)
rasteriza(X0, X1, Z0, Z1)
def pix(x, z): return int((z - Z0) * RES), int((x - X0) * RES)
def cl(x, z):
    j, i = pix(x, z)
    return ORDER[C[j, i] - 1] if 0 <= j < H and 0 <= i < W and C[j, i] else 'mar'
def hy(x, z):
    j, i = pix(x, z); return float(Y[j, i])
def media(x, z, r=.03):
    j, i = pix(x, z); k = max(1, int(r * RES)); s = Y[max(0, j - k):j + k + 1, max(0, i - k):i + k + 1]; return float(s[s > -5].mean())
MAR = (C == 0) | (C == CID['agua'])
from scipy import ndimage
dmar = ndimage.distance_transform_edt(~MAR) / RES          # distancia al mar (u)
CAL = (C == CID['calzada']) | (C == CID['edificios'])
dcal = ndimage.distance_transform_edt(~CAL) / RES
rs = [12345]
def rn():
    rs[0] = (rs[0] * 16807) % 2147483647; return rs[0] / 2147483647
R4 = lambda v: round(float(v), 4)
OUT = {}
# ---------- 2) Monteferro: máscara de la península ----------
MF = ((XX < -35.5) & np.isin(C, [CID['tierra'], CID['verde'], CID['roca']])) | ((XX < -33.5) & (C == CID['verde']))
MF &= (ZZ > 126.5)
# monumento: en la cima, junto al final de la carretera
cal_mf = (C == CID['calzada']) & (XX < -38)
k = np.argmax(np.where(cal_mf, Y, -9)); rx, rz = XX.flat[k], ZZ.flat[k]                     # final de la carretera
v = MF & (C == CID['verde'])
k = np.argmax(np.where(v, Y, -9)); sx, sz = XX.flat[k], ZZ.flat[k]                            # punto más alto
ang = math.atan2(sz - rz, sx - rx); d = math.hypot(sx - rx, sz - rz)
mx, mz = rx + math.cos(ang) * max(.17, d * .45), rz + math.sin(ang) * max(.17, d * .45)
OUT['monumento'] = [R4(mx), R4(mz), R4(media(mx, mz, .07) - .004), R4(math.pi)]   # la Virgen mira al oeste (Cíes); ángulo = dirección (cos, sin) en x,z
OUT['explanada'] = [R4(mx), R4(mz), .2, R4(rx), R4(rz)]
# pendiente local
gz, gx = np.gradient(Y, 1 / RES)
PEND = np.hypot(gx, gz)
def mejor(cx, cz, r, extra=lambda x, z: True):
    best = None
    for _ in range(4000):
        a = rn() * 6.283; q = math.sqrt(rn()) * r; x, z = cx + math.cos(a) * q, cz + math.sin(a) * q
        j, i = pix(x, z)
        if not (0 <= j < H and 0 <= i < W) or not MF[j, i] or C[j, i] != CID['verde'] or dcal[j, i] < .08 or not extra(x, z): continue
        s = PEND[max(0, j - 3):j + 4, max(0, i - 3):i + 4].mean() + q * .05
        if best is None or s < best[0]: best = (s, x, z)
    return best[1], best[2]
# batería J-3: al norte del monumento, sobre el cantil que mira a la bahía
bx, bz = mejor(mx - .9, mz - 2.4, .5, lambda x, z: dmar[pix(x, z)] < 1.0)
norte = math.atan2(-1, 0)
OUT['bateria'] = {'canones': [], 'bunkers': []}
for k_, (ox, oz) in enumerate([(0, 0), (.34, .12), (-.3, .2)]):
    x, z = bx + ox, bz + oz
    if cl(x, z) != 'verde': continue
    # apunta al mar más cercano
    j, i = pix(x, z); best = (9, 0)
    for a in np.linspace(0, 6.283, 48, endpoint=False):
        for q in np.arange(.1, 1.6, .05):
            jj, ii = pix(x + math.cos(a) * q, z + math.sin(a) * q)
            if 0 <= jj < H and 0 <= ii < W and MAR[jj, ii]:
                if q < best[0]: best = (q, a)
                break
    OUT['bateria']['canones'].append([R4(x), R4(z), R4(media(x, z, .04) - .003), R4(best[1])])
for (ox, oz, w, l) in [(.16, .3, .07, .045), (-.12, .42, .06, .04), (.48, .38, .05, .035)]:
    x, z = bx + ox, bz + oz
    if cl(x, z) not in ('verde', 'tierra'): continue
    OUT['bateria']['bunkers'].append([R4(x), R4(z), R4(media(x, z, .04) - .006), R4(rn() * .6 - .3), w, l])
# Mirador de las Estelas: la punta SO de la península, un poco hacia dentro
cand = MF & (dmar > .1) & (dmar < .22)
s = np.where(cand, -(XX - mx) + (ZZ - mz) * 1.1, -1e9); k = np.argmax(s); ex, ez = XX.flat[k], ZZ.flat[k]
OUT['mirador'] = [R4(ex), R4(ez), R4(media(ex, ez, .04) - .003), R4(math.atan2(ez - mz, ex - mx))]
# rosa de los vientos, un poco al norte del mirador
cand = MF & (dmar > .15) & (dmar < .4)
s = np.where(cand, -np.hypot(XX - (ex + .1), ZZ - (ez - .7)), -1e9); k = np.argmax(s); wx, wz = XX.flat[k], ZZ.flat[k]
OUT['rosa'] = [R4(wx), R4(wz), R4(media(wx, wz, .04))]
# ---------- 3) bolos de granito en la costa de Monteferro y en las puntas de Patos ----------
BOL = []
costa = (MF & (dmar < .32)) | ((C == CID['roca']) & (XX > -33) & (dmar < .3))
ii = np.argwhere(costa); usados = []
for _ in range(9000):
    if len(BOL) >= 900: break
    j, i = ii[int(rn() * len(ii))]; x, z = XX[j, i] + (rn() - .5) / RES, ZZ[j, i] + (rn() - .5) / RES
    if dcal[j, i] < .05: continue
    r = .008 + rn() ** 2 * .03 * (1.3 - dmar[j, i] * 2)
    if any((x - a) ** 2 + (z - b) ** 2 < (r + c) ** 2 * .8 for a, b, c in usados[-400:]): continue
    usados.append((x, z, r)); BOL.append([R4(x), R4(z), R4(Y[j, i] - r * .35), R4(r), round(rn(), 3)])
OUT['bolos'] = BOL
# ---------- 4) suelo de Monteferro: tipo de suelo por celda (monte, roca de costa, explanada) ----------
# En el juego se repintan los propios triángulos de la tierra y el verde de la zona (mismo plano, sin huecos ni montes asomando).
S = .05; gx0, gz0 = -47.2, 126.6; gw, gh = int((-33.4 - gx0) / S) + 1, int((140.2 - gz0) / S) + 1
GK = []
for j in range(gh):
    for i in range(gw):
        x, z = gx0 + i * S, gz0 + j * S; jj, ii_ = pix(x, z)
        if not (0 <= jj < H and 0 <= ii_ < W) or not MF[jj, ii_]: GK.append('0'); continue
        k = 1 if C[jj, ii_] == CID['verde'] else 2
        if math.hypot(x - mx, z - mz) < .2: k = 3
        GK.append(str(k))
OUT['suelo'] = {'x0': gx0, 'z0': gz0, 's': S, 'w': gw, 'h': gh, 'k': ''.join(GK)}
# ---------- 5) paseo de Patos: muro, farolas, pasarelas, socorristas y la ola de Prado ----------
P = (C == CID['playa']) & (XX > -31.8) & (XX < -19.6) & (ZZ > 126.3) & (ZZ < 134.4)
tierra_cerca = ndimage.binary_dilation(~(P | MAR), iterations=1)
borde = P & tierra_cerca & ~ndimage.binary_dilation(MAR, iterations=2)
pts = np.argwhere(borde)
bx_ = XX[pts[:, 0], pts[:, 1]]; bz_ = ZZ[pts[:, 0], pts[:, 1]]
# la playa va del SO (Abra) al NE (Prado): se ordena a lo largo de ese eje y en cada tramo se toma el borde más metido en tierra
A0, A1 = np.array([-31.6, 133.9]), np.array([-19.9, 126.5]); DV = (A1 - A0) / np.linalg.norm(A1 - A0); NV = np.array([-DV[1], DV[0]])
if NV[1] < 0: NV = -NV
ss = (bx_ - A0[0]) * DV[0] + (bz_ - A0[1]) * DV[1]; nn = (bx_ - A0[0]) * NV[0] + (bz_ - A0[1]) * NV[1]
L = []
for sa in np.arange(0, np.linalg.norm(A1 - A0) + .06, .06):
    m = (ss >= sa) & (ss < sa + .06)
    if m.sum():
        k = np.argmax(np.where(m, nn, -1e9)); L.append((float(bx_[k]), float(bz_[k])))
L = np.array(L)
# suavizado
Ls = L.copy()
for _ in range(3): Ls[1:-1, 1] = (Ls[:-2, 1] + Ls[1:-1, 1] * 2 + Ls[2:, 1]) / 4
seg = np.hypot(np.diff(Ls[:, 0]), np.diff(Ls[:, 1])); U = np.concatenate([[0], np.cumsum(seg)]); LL = U[-1]
def en(u):
    k = min(len(U) - 2, max(0, np.searchsorted(U, u) - 1)); f = (u - U[k]) / max(1e-9, U[k + 1] - U[k])
    x = Ls[k, 0] + (Ls[k + 1, 0] - Ls[k, 0]) * f; z = Ls[k, 1] + (Ls[k + 1, 1] - Ls[k, 1]) * f
    tx, tz = Ls[k + 1, 0] - Ls[k, 0], Ls[k + 1, 1] - Ls[k, 1]; l = math.hypot(tx, tz); tx, tz = tx / l, tz / l
    return x, z, tx, tz, -tz, tx        # normal (nx,nz) hacia tierra: (-tz, tx) → z mayor
def arena(x, z, nx, nz):
    # tramo de arena hacia el mar desde el borde: (inicio, fin) en unidades
    q = 0
    while q < .2 and any(cl(x - nx * (q + e), z - nz * (q + e)) != 'playa' for e in (0, .03, .06)): q += .005
    q0 = q
    while q < .6 and cl(x - nx * q, z - nz * q) not in ('agua', 'mar'): q += .005      # hasta el agua (la arena puede llevar franjas de tierra)
    return q0, q
def suelo_ok(x, z): return cl(x, z) in ('tierra', 'aceras', 'verde', 'verde_paseo', 'playa')
MURO = []; tramo = []; acc = []
u = .15; huecos = list(np.arange(.9, LL - .3, 1.35))
while u < LL - .1:
    if any(abs(u - h) < .04 for h in huecos):
        if len(tramo) > 3: MURO.append(tramo)
        tramo = []; u += .03; continue
    x, z, tx, tz, nx, nz = en(u); x += nx * .008; z += nz * .008
    if cl(x, z) in ('edificios', 'calzada'):
        if len(tramo) > 3: MURO.append(tramo)
        tramo = []; u += .03; continue
    tramo += [R4(x), R4(z), R4(max(hy(x, z), hy(x - nx * .02, z - nz * .02)))]; u += .03
if len(tramo) > 3: MURO.append(tramo)
OUT['muro'] = MURO
FAR = []
u = .3
while u < LL - .1:
    x, z, tx, tz, nx, nz = en(u)
    for off in (.03, .045, .02, .06):
        fx, fz = x + nx * off, z + nz * off
        if suelo_ok(fx, fz) and cl(fx, fz) != 'playa' and dcal[pix(fx, fz)] > .008:
            FAR.append([R4(fx), R4(fz), R4(hy(fx, fz))]); break
    u += .3
OUT['farolas'] = FAR
PAS = []
for h in huecos:
    x, z, tx, tz, nx, nz = en(h)
    # largo de la pasarela: hasta un tercio del ancho de la arena
    q0, q1 = arena(x, z, nx, nz)
    PAS.append([R4(x), R4(z), R4(hy(x - nx * .01, z - nz * .01)), R4(math.atan2(-nz, -nx)), R4(max(.05, min(.14, q0 + (q1 - q0) * .4)))])
OUT['pasarelas'] = PAS
SOC = []
for f in (.33, .68):
    x, z, tx, tz, nx, nz = en(LL * f); q0, q1 = arena(x, z, nx, nz); q = q0 + (q1 - q0) * .55
    sx_, sz_ = x - nx * q, z - nz * q
    SOC.append([R4(sx_), R4(sz_), R4(hy(sx_, sz_)), R4(math.atan2(-nz, -nx))])
OUT['socorristas'] = SOC
# la ola de Prado: al final norte de la playa, en tierra junto a la última pasarela
x, z, tx, tz, nx, nz = en(LL - .35)
for off in (.05, .07, .09, .04):
    ox_, oz_ = x + nx * off, z + nz * off
    if suelo_ok(ox_, oz_) and cl(ox_, oz_) != 'playa': break
OUT['ola'] = [R4(ox_), R4(oz_), R4(hy(ox_, oz_)), R4(math.atan2(-nz, -nx))]
PAS.append([R4(x), R4(z), R4(hy(x - nx * .01, z - nz * .01)), R4(math.atan2(-nz, -nx)), .08])
# ---------- 6) pinar y eucaliptal de Monteferro → baiona_inst.json ----------
fi = os.path.join(RAIZ, 'baiona_inst.json'); I = json.load(open(fi))
I['arboles'] = [a for a in I['arboles'] if not (len(a) > 7 and a[7] == 1)]
nc = len(I['colores'])
NUEVOS_COL = ['#5f7a5c', '#6b8263', '#2a4a2e', '#33532f', '#203d25', '#28462a', '#2e4b26']
I['colores'] = [c for c in I['colores'] if c not in NUEVOS_COL] + NUEVOS_COL
CE1, CE2 = I['colores'].index('#5f7a5c'), I['colores'].index('#6b8263')
PINO = [I['colores'].index(c) for c in ('#2a4a2e', '#33532f', '#203d25', '#28462a', '#2e4b26', '#2f5a35', '#365e30')]
exist = [(a[0], a[1]) for a in I['arboles'] if -48 < a[0] < -33 and 126 < a[1] < 141]
# rejilla de ocupación para distancias mínimas
celda = {}
def libre(x, z, r):
    ci, cj = int(x / .1), int(z / .1)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            for (a, b) in celda.get((ci + di, cj + dj), ()):
                if (x - a) ** 2 + (z - b) ** 2 < r * r: return False
    return True
def ocupa(x, z): celda.setdefault((int(x / .1), int(z / .1)), []).append((x, z))
for a, b in exist: ocupa(a, b)
evitar = [(mx, mz, .3), (ex, ez, .22), (wx, wz, .12)] + [(c[0], c[1], .14) for c in OUT['bateria']['canones']] + [(b[0], b[1], .12) for b in OUT['bateria']['bunkers']]
def ruido(x, z): return .5 + .25 * math.sin(x * 2.3 + math.sin(z * 1.7) * 1.4) + .25 * math.sin(z * 2.9 + math.cos(x * 1.3) * 2.1)
ii = np.argwhere(MF & (C == CID['verde']) & (dcal > .07) & (dmar > .12)); NUEVOS = []
for _ in range(60000):
    if len(NUEVOS) >= 6500: break
    j, i = ii[int(rn() * len(ii))]; x, z = XX[j, i] + (rn() - .5) / RES, ZZ[j, i] + (rn() - .5) / RES
    if any(math.hypot(x - a, z - b) < r for a, b, r in evitar): continue
    n = ruido(x, z)
    if n < .26: continue                                    # claros con tojo y helecho
    if not libre(x, z, .085 - n * .025): continue
    ocupa(x, z); y = float(Y[j, i]) - .004
    euca = ruido(x * 1.7 + 9, z * 1.7 - 4) > .62 and dmar[j, i] > .4      # eucaliptos en manchas, lejos del borde
    if euca: NUEVOS.append([R4(x), R4(z), R4(y), R4(.04 + rn() * .02), R4(.3 + rn() * .12), [CE1, CE2][int(rn() * 2)], 1, 1])
    else:
        exp = min(1, dmar[j, i] / .8)                       # junto al mar, pinos más bajos y achaparrados
        redondo = 1 if rn() < .45 else 0                    # pino marítimo: muchos con la copa ya redondeada
        NUEVOS.append([R4(x), R4(z), R4(y), R4((.045 if redondo else .05) + rn() * .025), R4((.15 + rn() * .1) * (.7 + .3 * exp)), PINO[int(rn() * len(PINO))], redondo, 1])
I['arboles'] += NUEVOS
json.dump(I, open(fi, 'w'), separators=(',', ':'))
# ---------- 7) Panxón: Templo Votivo do Mar, dique del puerto, rampa y barcas fondeadas ----------
# otro raster, más al sur, y su propio azar (así la zona 1 sale igual que antes)
rasteriza(-40.0, -14.0, 130.0, 156.0)
MAR = (C == 0) | (C == CID['agua'])
rs = [777]
PX = {}
# el templo: el edificio grande de la ladera sobre la playa (se quita del catastro y se pone el templo de verdad)
E = C == CID['edificios']; lab, nlab = ndimage.label(E)
k = lab[pix(-23.18, 141.84)]
assert k, 'no encuentro el edificio del templo'
m = lab == k; js, is_ = np.nonzero(m); px_ = XX[js, is_]; pz_ = ZZ[js, is_]
cx, cz = float(px_.mean()), float(pz_.mean())
cov = np.cov(np.vstack([px_ - cx, pz_ - cz])); ev, evec = np.linalg.eigh(cov); ax = evec[:, 1]
u = (px_ - cx) * ax[0] + (pz_ - cz) * ax[1]; v = (px_ - cx) * -ax[1] + (pz_ - cz) * ax[0]
largo, ancho = float(u.max() - u.min()), float(v.max() - v.min())
# la fachada mira a la playa (al extremo oeste de la playa de Panxón)
pl = np.array([-24.2, 144.6]); d1 = np.array([cx + ax[0] * largo / 2, cz + ax[1] * largo / 2]); d2 = np.array([cx - ax[0] * largo / 2, cz - ax[1] * largo / 2])
if np.linalg.norm(d2 - pl) < np.linalg.norm(d1 - pl): ax = -ax
ang = math.atan2(ax[1], ax[0])
anillo = ndimage.binary_dilation(m, iterations=6) & ~ndimage.binary_dilation(m, iterations=2) & ~E & (C != CID['calzada'])
suelo_t = float(np.median(Y[anillo])) if anillo.any() else float(np.median(Y[m]))
# contorno a quitar (casco convexo del edificio, un poco más ancho)
from scipy.spatial import ConvexHull
pts = np.column_stack([px_, pz_]); hull = pts[ConvexHull(pts).vertices]
cen = hull.mean(0); hull = cen + (hull - cen) * 1.06
PX['templo'] = {'x': R4(cx), 'z': R4(cz), 'y': R4(suelo_t), 'a': R4(ang), 'largo': R4(largo), 'ancho': R4(ancho), 'quita': [R4(c) for p in hull for c in p]}
# dique: la lengua estrecha de tierra con su calzada que sale de la punta hacia el SE
caja_d = (XX > -25.45) & (XX < -24.0) & (ZZ > 146.0) & (ZZ < 148.0) & ~MAR
js, is_ = np.nonzero(caja_d); dx_, dz_ = XX[js, is_], ZZ[js, is_]
cxd, czd = dx_.mean(), dz_.mean(); cov = np.cov(np.vstack([dx_ - cxd, dz_ - czd])); ev, evec = np.linalg.eigh(cov); axd = evec[:, 1]
if axd[1] < 0: axd = -axd                                     # de la raíz (N) a la punta (S)
ud = (dx_ - cxd) * axd[0] + (dz_ - czd) * axd[1]
raiz = (cxd + axd[0] * ud.min(), czd + axd[1] * ud.min()); punta = (cxd + axd[0] * ud.max(), czd + axd[1] * ud.max())
nd = np.array([-axd[1], axd[0]])                                # normal: hacia el E (dársena) si nd[0] > 0
if nd[0] < 0: nd = -nd
# ancho y cota de la losa a lo largo del dique
EJE = []
for t in np.linspace(0, 1, 24):
    x, z = raiz[0] + (punta[0] - raiz[0]) * t, raiz[1] + (punta[1] - raiz[1]) * t
    wl = wr = 0
    while wl < .3 and not MAR[pix(x - nd[0] * wl, z - nd[1] * wl)]: wl += .005
    while wr < .3 and not MAR[pix(x + nd[0] * wr, z + nd[1] * wr)]: wr += .005
    EJE.append([R4(x), R4(z), R4(hy(x, z)), R4(wl), R4(wr)])
PX['dique'] = {'eje': EJE, 'n': [R4(nd[0]), R4(nd[1])]}
# rampa: en la raíz del dique, por el lado de la dársena
rx, rz = raiz[0] + (punta[0] - raiz[0]) * .18, raiz[1] + (punta[1] - raiz[1]) * .18
q = 0
while q < .4 and not MAR[pix(rx + nd[0] * q, rz + nd[1] * q)]: q += .005
PX['rampa'] = [R4(rx + nd[0] * q), R4(rz + nd[1] * q), R4(hy(rx + nd[0] * (q - .02), rz + nd[1] * (q - .02))), R4(math.atan2(nd[1], nd[0]))]
# barcas fondeadas en la dársena, entre el dique y la playa
dagua = ndimage.distance_transform_edt(MAR) / RES               # distancia a tierra desde el agua
BAR = []; ocup = []
zona = MAR & (dagua > .07) & (XX > -25.2) & (XX < -21.6) & (ZZ > 145.4) & (ZZ < 149.2)
ii = np.argwhere(zona)
for _ in range(20000):
    if len(BAR) >= 46: break
    j, i = ii[int(rn() * len(ii))]; x, z = XX[j, i], ZZ[j, i]
    if math.hypot(x - punta[0], z - punta[1]) > 2.6 or dagua[j, i] > 1.3: continue
    if any((x - a) ** 2 + (z - b) ** 2 < .1 ** 2 for a, b in ocup): continue
    ocup.append((x, z)); r = rn()
    tipo = 0 if r < .45 else (1 if r < .85 else 2)                 # 0 gamela, 1 planeadora, 2 velero pequeño
    BAR.append([R4(x), R4(z), tipo, int(rn() * 8), R4(-2.35 + (rn() - .5) * .5), round(rn(), 3)])
PX['barcas'] = BAR
OUT['panxon'] = PX
print('templo', PX['templo']['x'], PX['templo']['z'], PX['templo']['y'], 'largo', largo, 'ancho', ancho, 'dique', raiz, punta, 'barcas', len(BAR), 'rampa', PX['rampa'])

# ---------- 8) Playa América – A Ramallosa: paseo, letrero, la lagoa con sus marismas y el puente medieval ----------
rasteriza(-28.0, -4.0, 146.0, 190.0)
MAR = (C == 0) | (C == CID['agua'])
rs = [4242]
AM = {}
dcal = ndimage.distance_transform_edt(~((C == CID['calzada']) | (C == CID['edificios']))) / RES
# paseo de Playa América: la playa va de N (Panxón) a S (Monte Lourido); tierra al este
P = (C == CID['playa']) & (XX > -23.5) & (XX < -18.0) & (ZZ > 147.6) & (ZZ < 166.8)
borde = P & ndimage.binary_dilation(~(P | MAR), iterations=1) & ~ndimage.binary_dilation(MAR, iterations=2)
pts = np.argwhere(borde); bx_ = XX[pts[:, 0], pts[:, 1]]; bz_ = ZZ[pts[:, 0], pts[:, 1]]
A0, A1 = np.array([-20.3, 147.8]), np.array([-21.9, 166.6]); DV = (A1 - A0) / np.linalg.norm(A1 - A0); NV = np.array([-DV[1], DV[0]])
if NV[0] < 0: NV = -NV                                     # hacia tierra (este)
ss = (bx_ - A0[0]) * DV[0] + (bz_ - A0[1]) * DV[1]; nn = (bx_ - A0[0]) * NV[0] + (bz_ - A0[1]) * NV[1]
L = []
for sa in np.arange(0, np.linalg.norm(A1 - A0) + .06, .06):
    m = (ss >= sa) & (ss < sa + .06)
    if m.sum(): k = np.argmax(np.where(m, nn, -1e9)); L.append((float(bx_[k]), float(bz_[k])))
Ls = np.array(L)
for _ in range(4): Ls[1:-1] = (Ls[:-2] + Ls[1:-1] * 2 + Ls[2:]) / 4
seg = np.hypot(np.diff(Ls[:, 0]), np.diff(Ls[:, 1])); U = np.concatenate([[0], np.cumsum(seg)]); LL = U[-1]
def en(u):
    k = min(len(U) - 2, max(0, np.searchsorted(U, u) - 1)); f_ = (u - U[k]) / max(1e-9, U[k + 1] - U[k])
    x = Ls[k, 0] + (Ls[k + 1, 0] - Ls[k, 0]) * f_; z = Ls[k, 1] + (Ls[k + 1, 1] - Ls[k, 1]) * f_
    tx, tz = Ls[k + 1, 0] - Ls[k, 0], Ls[k + 1, 1] - Ls[k, 1]; l = math.hypot(tx, tz); tx, tz = tx / l, tz / l
    nx, nz = -tz, tx
    if nx < 0: nx, nz = -nx, -nz
    return x, z, tx, tz, nx, nz
huecos = list(np.arange(.8, LL - .3, 1.3)); MURO = []; tramo = []; u = .1
while u < LL - .1:
    x, z, tx, tz, nx, nz = en(u); x += nx * .008; z += nz * .008
    if any(abs(u - h) < .04 for h in huecos) or cl(x, z) in ('edificios', 'calzada'):
        if len(tramo) > 3: MURO.append(tramo)
        tramo = []; u += .03; continue
    tramo += [R4(x), R4(z), R4(max(hy(x, z), hy(x - nx * .02, z - nz * .02)))]; u += .03
if len(tramo) > 3: MURO.append(tramo)
AM['muro'] = MURO
FAR, PAL = [], []
u = .25
while u < LL - .1:
    x, z, tx, tz, nx, nz = en(u)
    for off in (.03, .045, .02, .06):
        fx, fz = x + nx * off, z + nz * off
        if suelo_ok(fx, fz) and cl(fx, fz) != 'playa' and dcal[pix(fx, fz)] > .008: FAR.append([R4(fx), R4(fz), R4(hy(fx, fz))]); break
    for off in (.075, .09, .06, .11):
        px2, pz2 = x + nx * off + tx * .15, z + nz * off + tz * .15
        if suelo_ok(px2, pz2) and cl(px2, pz2) != 'playa' and dcal[pix(px2, pz2)] > .02: PAL.append([R4(px2), R4(pz2), R4(hy(px2, pz2)), round(rn(), 3)]); break
    u += .3
AM['farolas'] = FAR; AM['palmeras'] = PAL
PAS = []
for h in huecos:
    x, z, tx, tz, nx, nz = en(h); q0, q1 = arena(x, z, nx, nz)
    PAS.append([R4(x), R4(z), R4(hy(x - nx * .01, z - nz * .01)), R4(math.atan2(-nz, -nx)), R4(max(.05, min(.14, q0 + (q1 - q0) * .4)))])
AM['pasarelas'] = PAS
SOC = []
for f_ in (.3, .62):
    x, z, tx, tz, nx, nz = en(LL * f_); q0, q1 = arena(x, z, nx, nz); q = q0 + (q1 - q0) * .55
    SOC.append([R4(x - nx * q), R4(z - nz * q), R4(hy(x - nx * q, z - nz * q)), R4(math.atan2(-nz, -nx))])
AM['socorristas'] = SOC
# letrero «PRAIA AMÉRICA»: en el césped del paseo, al sur, mirando al mar
x, z, tx, tz, nx, nz = en(LL * .86)
for off in (.1, .13, .08, .16, .2):
    lx, lz = x + nx * off, z + nz * off
    if suelo_ok(lx, lz) and cl(lx, lz) != 'playa' and dcal[pix(lx, lz)] > .06: break
AM['letrero'] = [R4(lx), R4(lz), R4(media(lx, lz, .05)), R4(math.atan2(-nz, -nx))]
# el puente medieval de A Ramallosa: el cruce más corto de la lagoa en su extremo este (donde empieza el río)
best = None
for cx in np.arange(-9.4, -7.9, .05):
    for a in np.radians(np.arange(-35, 36, 5)):
        dx, dz = math.sin(a), math.cos(a)                    # casi N-S
        # desde un punto del agua hacia los dos lados hasta tierra
        for cz in np.arange(183.4, 185.4, .1):
            if not MAR[pix(cx, cz)]: continue
            q1 = 0
            while q1 < 2 and MAR[pix(cx - dx * q1, cz - dz * q1)]: q1 += .01
            q2 = 0
            while q2 < 2 and MAR[pix(cx + dx * q2, cz + dz * q2)]: q2 += .01
            if q1 >= 2 or q2 >= 2: continue
            l = q1 + q2
            if l < .9: continue                                   # que cruce la lagoa, no un brazo
            if best is None or l < best[0]: best = (l, cx - dx * q1, cz - dz * q1, cx + dx * q2, cz + dz * q2)
l, x1, z1, x2, z2 = best
ux, uz = (x2 - x1) / l, (z2 - z1) / l
x1, z1, x2, z2 = x1 - ux * .08, z1 - uz * .08, x2 + ux * .08, z2 + uz * .08      # apoyos en tierra
AM['puente'] = [R4(x1), R4(z1), R4(media(x1, z1, .03)), R4(x2), R4(z2), R4(media(x2, z2, .03))]
# marismas: manchas de junco y lodo en la lagoa, sobre todo junto a las orillas y en el lado sur (Ladeira)
LAG = MAR & (C == CID['agua']) & (XX > -17) & (ZZ > 179.5) & (XX < -7.8)
dt = ndimage.distance_transform_edt(LAG) / RES
S_ = .05; mx0, mz0 = -17.0, 179.5; mw, mh = int(10 / S_), int(8.5 / S_); MK = []
for j in range(mh):
    for i in range(mw):
        x, z = mx0 + i * S_, mz0 + j * S_; jj, ii_ = pix(x, z)
        if not (0 <= jj < H and 0 <= ii_ < W) or not LAG[jj, ii_]: MK.append('0'); continue
        n = .5 + .25 * math.sin(x * 3.1 + math.sin(z * 2.3) * 1.6) + .25 * math.sin(z * 2.7 + math.cos(x * 1.9) * 2.2)
        # más marisma cerca de la orilla y hacia el sur; un canal libre por el centro
        v = n - dt[jj, ii_] * .9 + (z - 182) * .05
        MK.append('2' if v > .55 else ('1' if v > .42 else '0'))     # 2 junco, 1 lodo
mk = ''.join(MK); AM['marisma'] = {'x0': mx0, 'z0': mz0, 's': S_, 'w': mw, 'h': mh, 'k': mk}
# garzas en los bordes de la marisma
G_ = []
for _ in range(4000):
    if len(G_) >= 9: break
    i, j = int(rn() * mw), int(rn() * mh)
    if mk[j * mw + i] != '1': continue
    x, z = mx0 + i * S_, mz0 + j * S_
    if any(math.hypot(x - a, z - b) < .4 for a, b, *_ in G_): continue
    G_.append([R4(x), R4(z), R4(rn() * 6.28), round(rn(), 2)])
AM['garzas'] = G_
OUT['america'] = AM
print('america: muro', len(MURO), 'farolas', len(FAR), 'palmeras', len(PAL), 'pasarelas', len(PAS), 'letrero', AM['letrero'], 'puente', AM['puente'], 'largo', l, 'marisma', mk.count('2'), mk.count('1'), 'garzas', len(G_))
# ---------- 9) Interior de Nigrán: concello, iglesias parroquiales, hórreos, cruceiros y viñas ----------
# El mapa del juego no está exactamente georreferenciado en el interior: cada sitio se lleva al hueco libre (ni calle
# ni casa, poco inclinado y con una calle cerca) más próximo al punto calculado desde sus coordenadas reales.
RES_ = RES; RES = 10
rasteriza(-18.0, 40.0, 116.0, 180.0)
MAR = (C == 0) | (C == CID['agua'])
rs = [9191]
IN = {}
# ajuste lat/lon -> mapa con puntos conocidos de las zonas 1-3
GEO = [((42.15342, -8.84612), (OUT['monumento'][0], OUT['monumento'][1])), ((42.14582, -8.82370), (OUT['panxon']['templo']['x'], OUT['panxon']['templo']['z'])),
       ((42.11540, -8.81264), ((OUT['america']['puente'][0] + OUT['america']['puente'][3]) / 2, (OUT['america']['puente'][1] + OUT['america']['puente'][4]) / 2)),
       ((42.15904, -8.81959), (OUT['ola'][0], OUT['ola'][1]))]
Ag = np.array([[lo, la, 1] for (la, lo), _ in GEO]); gx_ = np.linalg.lstsq(Ag, [p[0] for _, p in GEO], rcond=None)[0]; gz_ = np.linalg.lstsq(Ag, [p[1] for _, p in GEO], rcond=None)[0]
def geo(la, lo): return float(gx_ @ [lo, la, 1]), float(gz_ @ [lo, la, 1])
OCU = (C == CID['calzada']) | (C == CID['edificios']) | (C == CID['aceras']) | MAR
docu = ndimage.distance_transform_edt(~OCU) / RES
CAL = C == CID['calzada']; dcal = ndimage.distance_transform_edt(~CAL) / RES
DED = ndimage.distance_transform_edt(~(C == CID['edificios'])) / RES
gz2, gx2 = np.gradient(Y, 1 / RES); PEND = np.hypot(gx2, gz2)
usados = []
def hueco(x0, z0, r, rmax=3.0):
    best = None
    j0, i0 = pix(x0, z0); k = int(rmax * RES)
    for j in range(max(0, j0 - k), min(H, j0 + k + 1)):
        for i in range(max(0, i0 - k), min(W, i0 + k + 1)):
            if docu[j, i] < r or dcal[j, i] > r + .5 or PEND[j, i] > .6: continue
            x, z = XX[j, i], ZZ[j, i]
            if any(math.hypot(x - a, z - b) < r + rr + .1 for a, b, rr in usados): continue
            d = math.hypot(x - x0, z - z0) + PEND[j, i] * .5
            if best is None or d < best[0]: best = (d, x, z)
    if best is None: return None
    _, x, z = best; usados.append((x, z, r))
    # mira a la calle más cercana
    j, i = pix(x, z); jj, ii = np.unravel_index(np.argmin(np.where(CAL[max(0, j - 15):j + 16, max(0, i - 15):i + 16], np.hypot(*np.mgrid[-min(15, j):min(16, H - j), -min(15, i):min(16, W - i)]), 1e9)), (min(16, H - j) + min(15, j), min(16, W - i) + min(15, i)))
    cxk, czk = XX[max(0, j - 15) + jj, max(0, i - 15) + ii], ZZ[max(0, j - 15) + jj, max(0, i - 15) + ii]
    m_ = (np.hypot(XX - x, ZZ - z) < r * 1.2) & ~OCU
    yb = float(np.median(Y[m_])) if m_.any() else float(Y[j, i])
    return [R4(x), R4(z), R4(yb), R4(math.atan2(czk - z, cxk - x))]
SIT = {'concello': (42.14164, -8.80656, .3), 'sanfiz': (42.14219, -8.79223, .24), 'camos': (42.14689, -8.76512, .24), 'parada': (42.13012, -8.77801, .24),
       'priegue': (42.16150, -8.79802, .24), 'chandebrito': (42.16202, -8.75368, .24)}
for k, (la, lo, r) in SIT.items():
    x0, z0 = geo(la, lo); IN[k] = hueco(x0, z0, r)
    print('sitio', k, R4(x0), R4(z0), '->', IN[k])
IN['iglesias'] = [[k] + IN.pop(k) for k in ('sanfiz', 'camos', 'parada', 'priegue', 'chandebrito') if IN.get(k)]
# hórreos: junto a casas del rural (casas sueltas, con terreno libre al lado)
RUR = ~OCU & (DED > .05) & (DED < .3) & (dcal > .06) & (PEND < .5) & (XX > -16.5)
dens = ndimage.uniform_filter((C == CID['edificios']).astype(float), 25)
RUR &= dens < .12                                               # nada de centros densos
ii = np.argwhere(RUR); HOR_ = []; ocup = []
print('candidatos horreos', len(ii), 'edif', int((C == CID['edificios']).sum()), 'libre', int((~OCU).sum()))
for _ in range(60000):
    if len(HOR_) >= 170: break
    if not len(ii): break
    j, i = ii[int(rn() * len(ii))]; x, z = XX[j, i], ZZ[j, i]
    if any((x - a) ** 2 + (z - b) ** 2 < .9 ** 2 for a, b in ocup): continue
    if any(math.hypot(x - a, z - b) < rr + .2 for a, b, rr in usados): continue
    ocup.append((x, z))
    # paralelo a la casa más cercana (aprox.: perpendicular al gradiente de distancia)
    gj = DED[min(H - 1, j + 1), i] - DED[max(0, j - 1), i]; gi = DED[j, min(W - 1, i + 1)] - DED[j, max(0, i - 1)]
    HOR_.append([R4(x), R4(z), R4(Y[j, i]), R4(math.atan2(gj, gi) + math.pi / 2), round(rn(), 2)])
IN['horreos'] = HOR_
# cruceiros en cruces de caminos del rural
dens_c = ndimage.uniform_filter(CAL.astype(float), 7)
CR = ~OCU & (dcal > .05) & (dcal < .16) & (dens_c > .22) & (dens < .12) & (XX > -16.5)
ii = np.argwhere(CR); CRU = []; oc2 = []
print('candidatos cruceiros', len(ii))
for _ in range(40000):
    if len(CRU) >= 28: break
    if not len(ii): break
    j, i = ii[int(rn() * len(ii))]; x, z = XX[j, i], ZZ[j, i]
    if any((x - a) ** 2 + (z - b) ** 2 < 2.2 ** 2 for a, b in oc2): continue
    if any(math.hypot(x - a, z - b) < .15 for a, b, *_ in HOR_): continue
    oc2.append((x, z)); CRU.append([R4(x), R4(z), R4(Y[j, i]), R4(rn() * 6.28)])
IN['cruceiros'] = CRU
# viñas en emparrado: parcelas libres y llanas del rural
VI = ~OCU & (docu > .14) & (PEND < .25) & (dens < .1) & (dens > .005) & (XX > -16.5)
ii = np.argwhere(VI); VIN = []; oc3 = []
print('candidatos vinas', len(ii))
for _ in range(40000):
    if len(VIN) >= 36: break
    if not len(ii): break
    j, i = ii[int(rn() * len(ii))]; x, z = XX[j, i], ZZ[j, i]
    if any((x - a) ** 2 + (z - b) ** 2 < 1.4 ** 2 for a, b in oc3): continue
    if any(math.hypot(x - a, z - b) < rr + .3 for a, b, rr in usados): continue
    oc3.append((x, z)); VIN.append([R4(x), R4(z), R4(Y[j, i]), R4(rn() * 3.14), round(.09 + rn() * .05, 3), round(.06 + rn() * .04, 3)])
IN['vinas'] = VIN
RES = RES_
OUT['interior'] = IN
print('interior: iglesias', len(IN['iglesias']), 'horreos', len(HOR_), 'cruceiros', len(CRU), 'vinas', len(VIN))
OUT['pinar'] = len(NUEVOS)
json.dump(OUT, open(os.path.join(RAIZ, 'nigran_detalle.json'), 'w'), separators=(',', ':'))
print('monumento', OUT['monumento'], 'bateria', OUT['bateria'], 'mirador', OUT['mirador'], 'rosa', OUT['rosa'])
print('bolos', len(BOL), 'suelo', gw, gh, 'muro', len(MURO), sum(len(m) // 3 for m in MURO), 'farolas', len(FAR), 'pasarelas', len(PAS), 'socorristas', SOC, 'ola', OUT['ola'], 'pinar', len(NUEVOS), 'playa larga', LL)
