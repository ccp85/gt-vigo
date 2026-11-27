import json, numpy as np
from PIL import Image, ImageDraw
T = json.load(open('bz_tris.json'))
X0, X1, Z0, Z1, RES = 25.6, 66.6, 23.0, 56.0, 50  # 50 px/unit = 0.02 u (~1.4 m)
W, H = int((X1 - X0) * RES), int((Z1 - Z0) * RES)
# capas en orden de pintado (las últimas tapan)
CAPAS = [('tierra', 1), ('verde', 2), ('verde_paseo', 2), ('roca', 3), ('playa', 4), ('playita_16162', 4), ('paseo', 5), ('paseo_madera', 5),
         ('muelles', 5), ('aceras', 6), ('carril_bici', 6), ('calzada', 7), ('puente_8390', 7), ('edificios', 8)]
cls = Image.new('L', (W, H), 0)
hgt = np.zeros((H, W), np.float32)
d = ImageDraw.Draw(cls)
for nm, k in CAPAS:
    t = T[nm]
    for i in range(0, len(t), 9):
        p = [((t[i + j * 3] - X0) * RES, (t[i + j * 3 + 2] - Z0) * RES) for j in range(3)]
        d.polygon(p, fill=k)
C = np.array(cls)
# alturas del suelo (tierra/verde/playa) por rasterizado aproximado: media de los 3 vértices por triángulo
hi = Image.new('F', (W, H), 0.0); dh = ImageDraw.Draw(hi)
for nm in ['tierra', 'verde', 'verde_paseo', 'playa', 'aceras', 'calzada', 'paseo']:
    t = T[nm]
    for i in range(0, len(t), 9):
        p = [((t[i + j * 3] - X0) * RES, (t[i + j * 3 + 2] - Z0) * RES) for j in range(3)]
        dh.polygon(p, fill=float((t[i + 1] + t[i + 4] + t[i + 7]) / 3))
np.save('cls.npy', C); np.save('hgt.npy', np.array(hi))
pal = np.array([(20, 40, 90), (215, 200, 170), (90, 160, 70), (120, 110, 100), (245, 225, 170), (170, 120, 80), (150, 150, 155), (70, 70, 80), (230, 120, 90)], np.uint8)
Image.fromarray(pal[C]).save('cls.png')
print(W, H, np.bincount(C.ravel(), minlength=9))
