# Colegio Compañía de María (Vigo) con su iglesia — GT Vigo
# Script para Blender 4.x / 5.x: pestaña Scripting > Abrir > Ejecutar.
# Crea la colección "CompaniaMaria" (borra la anterior si existe).
#
# Referencias: vista aérea Google Maps (escala 20 m / 10 m), Street View de
# Rúa Doutor Carlos Colmeiro Laforet (mar 2023) y Rúa do Ecuador (may 2026),
# fotos del colegio.  Medidas sacadas de la aérea (~0,11 m/píxel).
#
# Ejes locales (metros), ya orientados como en la realidad (Z arriba):
#   X = a lo largo de la fachada de la iglesia, de NO (Manuel Núñez) a SE (Simón Bolívar)
#   Y = hacia la calle Colmeiro Laforet (la fachada de la iglesia mira a +Y, al NE)
#   (el modelo se construye con Y hacia Ecuador y al final se refleja)
#   Z = arriba; Z=0 es la explanada del colegio; Colmeiro Laforet va ~5 m más baja.
# Origen real aprox.: esquina N del bloque principal = 42.23455 N, -8.72038 O.
# Rumbo del eje +X: ~108° (ESE).  Para el mapa de GT Vigo: rotar Z = -18°.

import bpy, bmesh, math
import numpy as np
from mathutils import Vector

COL = "CompaniaMaria"
# GAME=True: versión para GT Vigo (sin calles ni suelo del entorno, con zócalos que se hunden en el terreno)
GAME = globals().get("GAME", False)

# ------------------------------------------------------------------ escena
if COL in bpy.data.collections:
    old = bpy.data.collections[COL]
    for o in list(old.all_objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.collections.remove(old)
col = bpy.data.collections.new(COL)
bpy.context.scene.collection.children.link(col)

# ------------------------------------------------------------------ texturas (numpy, sin PIL)
rng = np.random.default_rng(7)

def _noise(w, h, scale):
    sw, sh = max(2, w // scale), max(2, h // scale)
    g = rng.random((sh + 1, sw + 1))
    ys = np.linspace(0, sh, h, endpoint=False); xs = np.linspace(0, sw, w, endpoint=False)
    y0 = ys.astype(int); x0 = xs.astype(int); fy = (ys - y0)[:, None]; fx = (xs - x0)[None, :]
    a = g[y0][:, x0]; b = g[y0][:, x0 + 1]; c = g[y0 + 1][:, x0]; d = g[y0 + 1][:, x0 + 1]
    fy = fy * fy * (3 - 2 * fy); fx = fx * fx * (3 - 2 * fx)
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy

def make_image(name, arr):
    h, w = arr.shape[:2]
    if name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[name])
    img = bpy.data.images.new(name, w, h, alpha=False)
    rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = np.clip(arr, 0, 1)
    img.pixels.foreach_set(rgba[::-1].ravel())   # Blender empieza abajo
    img.pack()
    return img

def tex_granite(base, w=256, h=256, joints=True, block=(64, 32)):
    n = 0.55 * _noise(w, h, 4) + 0.3 * _noise(w, h, 16) + 0.15 * rng.random((h, w))
    arr = np.array(base)[None, None, :] * (0.82 + 0.3 * n[..., None])
    speck = rng.random((h, w)) > 0.985
    arr[speck] *= 0.55
    if joints:  # sillería: hiladas con juntas
        bw, bh = block
        yy, xx = np.mgrid[0:h, 0:w]
        off = ((yy // bh) % 2) * (bw // 2)
        jm = ((yy % bh) < 2) | (((xx + off) % bw) < 2)
        arr[jm] *= 0.72
        # cada sillar con un tono algo distinto
        tone = rng.uniform(0.92, 1.08, (h // bh + 1, w // bw + 2))
        arr *= tone[yy // bh, (xx + off) // bw][..., None]
    return arr

def tex_render(base, w=256, h=256):
    n = 0.7 * _noise(w, h, 32) + 0.3 * _noise(w, h, 6)
    arr = np.array(base)[None, None, :] * (0.9 + 0.14 * n[..., None])
    stain = _noise(w, h, 64)[..., None]
    return arr * (1 - 0.12 * np.clip(stain - 0.5, 0, 1) * 2)

def tex_tiles(base, w=256, h=256):
    yy, xx = np.mgrid[0:h, 0:w]
    row = yy // 16
    wave = np.abs(np.sin((xx + (row % 2) * 8) * math.pi / 16))
    shade = 0.75 + 0.25 * wave
    shade *= np.where((yy % 16) < 3, 0.7, 1.0)
    tone = rng.uniform(0.85, 1.12, (h // 16 + 1, w // 16 + 2))
    arr = np.array(base)[None, None, :] * shade[..., None] * tone[row, (xx + (row % 2) * 8) // 16][..., None]
    moss = (_noise(w, h, 24) > 0.72)[..., None]
    return np.where(moss, arr * np.array([0.8, 0.9, 0.7]), arr)

def tex_corrugated(base, w=256, h=64):
    yy, xx = np.mgrid[0:h, 0:w]
    s = 0.78 + 0.22 * np.sin(xx * math.pi / 6)
    arr = np.array(base)[None, None, :] * s[..., None] * (0.92 + 0.12 * _noise(w, h, 16))[..., None]
    return arr

def tex_court(w=512, h=320):
    arr = np.ones((h, w, 3)) * np.array([0.56, 0.42, 0.38])
    arr *= (0.9 + 0.15 * _noise(w, h, 24))[..., None]
    sky = np.array([0.40, 0.52, 0.55])
    def line(mask): arr[mask] = [0.92, 0.92, 0.9]
    yy, xx = np.mgrid[0:h, 0:w]
    m = 12
    line((np.abs(xx - m) < 2) & (yy > m) & (yy < h - m)); line((np.abs(xx - (w - m)) < 2) & (yy > m) & (yy < h - m))
    line((np.abs(yy - m) < 2) & (xx > m) & (xx < w - m)); line((np.abs(yy - (h - m)) < 2) & (xx > m) & (xx < w - m))
    line((np.abs(xx - w // 2) < 2) & (yy > m) & (yy < h - m))
    r = np.hypot(xx - w / 2, yy - h / 2); line(np.abs(r - 34) < 2)
    for cx in (m, w - m):
        r2 = np.hypot(xx - cx, yy - h / 2); line((np.abs(r2 - 120) < 2) & (np.abs(xx - cx) < 120))
    return arr

def tex_mural(w=512, h=128):
    # Mural del muro de Colmeiro Laforet: tucán, flores y letras azules (estilizado, propio)
    arr = np.ones((h, w, 3)) * np.array([0.62, 0.60, 0.55]) * (0.85 + 0.2 * _noise(w, h, 8))[..., None]
    yy, xx = np.mgrid[0:h, 0:w]
    def disc(cx, cy, r, col, sx=1, sy=1):
        arr[((xx - cx) / sx) ** 2 + ((yy - cy) / sy) ** 2 < r * r] = col
    # fondo pintado (zona central del mural)
    zone = (xx > 140) & (xx < 330)
    arr[zone] = arr[zone] * 0.3 + np.array([0.62, 0.78, 0.80]) * 0.7
    for i, (cx, cy, c) in enumerate([(165, 90, (0.95, 0.55, 0.25)), (190, 60, (0.98, 0.80, 0.25)),
                                      (300, 40, (0.35, 0.45, 0.85)), (315, 95, (0.85, 0.30, 0.50))]):
        for k in range(6):
            a = k * math.pi / 3
            disc(cx + 11 * math.cos(a), cy + 11 * math.sin(a), 8, c)
        disc(cx, cy, 6, (0.98, 0.95, 0.6))
    arr[(yy > 70) & (yy < 76) & (xx > 210) & (xx < 300)] = (0.40, 0.28, 0.18)   # rama
    disc(245, 55, 22, (0.08, 0.08, 0.1), 1.0, 1.25)          # cuerpo tucán
    disc(258, 40, 10, (0.95, 0.95, 0.9))                       # pecho/cara
    beak = (yy > 32) & (yy < 50) & (xx > 262) & (xx < 300) & ((yy - 32) < (300 - xx) * 0.5)
    arr[beak] = (0.98, 0.72, 0.12)
    disc(262, 37, 2.5, (0.1, 0.3, 0.8))
    for k in range(5):
        a = -0.6 + 0.3 * k
        for t in range(28):
            disc(150 + 40 * k + t * math.cos(a) * 0.8, 120 - t * 1.6, 3, (0.20, 0.55, 0.25))
    # franja azul con letras (bloques) a la izquierda
    band = (xx > 10) & (xx < 135) & (yy > 50) & (yy < 82)
    arr[band] = (0.20, 0.38, 0.75)
    for i in range(8):
        x0 = 16 + i * 15
        arr[(xx > x0) & (xx < x0 + 10) & (yy > 56) & (yy < 76) & (((xx - x0) < 3) | ((yy - 56) < 3) | ((yy - 56) > 16))] = (0.92, 0.95, 1.0)
    graf = (_noise(w, h, 6) > 0.8) & (xx > 360) & (yy > 70)
    arr[graf] = (0.15, 0.15, 0.2)
    return arr

def tex_rose(w=128, h=128):
    arr = np.ones((h, w, 3)) * np.array([0.55, 0.52, 0.47])
    yy, xx = np.mgrid[0:h, 0:w]; r = np.hypot(xx - 64, yy - 64); a = np.arctan2(yy - 64, xx - 64)
    glass = (r < 56) & (r > 10) & (np.abs(((a * 12 / (2 * math.pi)) % 1) - 0.5) > 0.12) & (np.abs(r - 34) > 3)
    arr[glass] = (0.10, 0.12, 0.16)
    arr[r < 8] = (0.12, 0.14, 0.2)
    return arr

# ------------------------------------------------------------------ materiales
MATS = {}
def mat(name, color=None, img=None, rough=0.8, metal=0.0, emit=None):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.get("CM_" + name) or bpy.data.materials.new("CM_" + name)
    m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if img is not None:
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = img
        nt.links.new(t.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (*color, 1)
    m.diffuse_color = (*(color or (0.6, 0.6, 0.6)), 1)
    MATS[name] = m
    return m

GRANITO = (0.56, 0.53, 0.47)
M = dict(
    granito=mat("granito", GRANITO, make_image("CM_granito", tex_granite(GRANITO))),
    granito_liso=mat("granito_liso", (0.6, 0.57, 0.51), make_image("CM_granito_liso", tex_granite((0.6, 0.57, 0.51), joints=False))),
    revoco=mat("revoco_crema", (0.86, 0.80, 0.66), make_image("CM_revoco", tex_render((0.86, 0.80, 0.66)))),
    revoco_blanco=mat("revoco_blanco", (0.88, 0.87, 0.83), make_image("CM_revoco_b", tex_render((0.88, 0.87, 0.83)))),
    teja=mat("teja", (0.66, 0.30, 0.19), make_image("CM_teja", tex_tiles((0.68, 0.31, 0.19)))),
    chapa=mat("chapa_roja", (0.55, 0.17, 0.13), make_image("CM_chapa", tex_corrugated((0.6, 0.2, 0.15))), rough=0.55, metal=0.3),
    vidrio=mat("vidrio", (0.07, 0.09, 0.11), rough=0.08, metal=0.2),
    marco=mat("carpinteria_blanca", (0.9, 0.9, 0.88), rough=0.5),
    persiana=mat("persiana", (0.82, 0.8, 0.74), rough=0.6),
    madera=mat("madera_puerta", (0.30, 0.17, 0.09), rough=0.6),
    hierro=mat("hierro", (0.12, 0.12, 0.12), rough=0.5, metal=0.7),
    baranda=mat("baranda_gris", (0.78, 0.79, 0.8), rough=0.4, metal=0.6),
    hormigon=mat("hormigon", (0.46, 0.45, 0.41), make_image("CM_hormigon", tex_granite((0.48, 0.47, 0.43), joints=False))),
    mural=mat("mural", (0.6, 0.6, 0.6), make_image("CM_mural", tex_mural())),
    pista=mat("pista", (0.56, 0.42, 0.38), make_image("CM_pista", tex_court())),
    roseton=mat("roseton", (0.5, 0.5, 0.5), make_image("CM_roseton", tex_rose())),
    cesped=mat("cesped", (0.24, 0.42, 0.16), make_image("CM_cesped", tex_render((0.26, 0.44, 0.17)))),
    hoja=mat("hojas", (0.16, 0.30, 0.12)),
    hoja2=mat("hojas_oscuras", (0.10, 0.22, 0.10)),
    tronco=mat("tronco", (0.28, 0.21, 0.15)),
    asfalto=mat("asfalto", (0.20, 0.20, 0.21), make_image("CM_asfalto", tex_render((0.22, 0.22, 0.23)))),
    adoquin=mat("adoquin", (0.42, 0.40, 0.37), make_image("CM_adoquin", tex_granite((0.44, 0.42, 0.38), block=(16, 12)))),
    acera=mat("acera", (0.62, 0.6, 0.56), make_image("CM_acera", tex_granite((0.62, 0.6, 0.56), block=(48, 48)))),
    azotea=mat("azotea", (0.32, 0.32, 0.33)),
    solar=mat("placa_solar", (0.08, 0.12, 0.25), rough=0.15, metal=0.4),
    bronce=mat("campana", (0.45, 0.33, 0.15), rough=0.3, metal=0.9),
    piedra_estatua=mat("estatua", (0.82, 0.81, 0.78)),
    blanco_pista=mat("linea", (0.95, 0.95, 0.95)),
)

# ------------------------------------------------------------------ utilidades
def link(o):
    col.objects.link(o); return o

def mesh_obj(name, verts, faces, material, uv_scale=None):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    o = link(bpy.data.objects.new(name, me)); o.data.materials.append(material)
    if uv_scale: box_uv(o, uv_scale)
    return o

def box_uv(o, s=3.0):
    """Proyección cúbica en coordenadas de mundo: s = metros por repetición."""
    me = o.data
    if not me.uv_layers: me.uv_layers.new()
    uv = me.uv_layers.active.data
    mw = o.matrix_world
    for p in me.polygons:
        n = p.normal; ax = max(range(3), key=lambda i: abs(n[i]))
        for li in p.loop_indices:
            co = mw @ me.vertices[me.loops[li].vertex_index].co
            if ax == 0: u, v = co.y, co.z
            elif ax == 1: u, v = co.x, co.z
            else: u, v = co.x, co.y
            uv[li].uv = (u / s, v / s)

def box(name, x0, y0, z0, x1, y1, z1, material, uv=3.0):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    o = mesh_obj(name, v, f, material); box_uv(o, uv); return o

def cyl(name, x, y, z0, z1, r, material, seg=12, r_top=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r_top is None else r_top, depth=z1 - z0)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me)); o.location = (x, y, (z0 + z1) / 2); o.data.materials.append(material)
    return o

def sphere(name, x, y, z, r, material, sub=2, sx=1, sy=1, sz=1):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me)); o.location = (x, y, z); o.scale = (sx, sy, sz)
    o.data.materials.append(material); return o

def hip_roof(name, x0, y0, x1, y1, z, h, material, over=0.5):
    x0 -= over; y0 -= over; x1 += over; y1 += over
    w, d = x1 - x0, y1 - y0
    if w >= d:
        r = d / 2; a = (x0 + r, (y0 + y1) / 2, z + h); b = (x1 - r, (y0 + y1) / 2, z + h)
    else:
        r = w / 2; a = ((x0 + x1) / 2, y0 + r, z + h); b = ((x0 + x1) / 2, y1 - r, z + h)
    v = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z), a, b]
    if w >= d: f = [(0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5), (3, 0, 4)]
    else: f = [(0, 1, 4), (1, 2, 5, 4), (2, 3, 5), (3, 0, 4, 5)]
    o = mesh_obj(name, v, f, material); box_uv(o, 2.0); return o

def ring_roof(name, outer, inner, z, h, material, over=0.5):
    """Cubierta a cuatro aguas alrededor de un patio (claustro)."""
    (ox0, oy0, ox1, oy1), (ix0, iy0, ix1, iy1) = outer, inner
    ox0 -= over; oy0 -= over; ox1 += over; oy1 += over
    ix0 += over * 0.6; iy0 += over * 0.6; ix1 -= over * 0.6; iy1 -= over * 0.6
    mx0, my0, mx1, my1 = (ox0 + ix0) / 2, (oy0 + iy0) / 2, (ox1 + ix1) / 2, (oy1 + iy1) / 2
    O = [(ox0, oy0, z), (ox1, oy0, z), (ox1, oy1, z), (ox0, oy1, z)]
    R = [(mx0, my0, z + h), (mx1, my0, z + h), (mx1, my1, z + h), (mx0, my1, z + h)]
    I = [(ix0, iy0, z), (ix1, iy0, z), (ix1, iy1, z), (ix0, iy1, z)]
    v = O + R + I; f = []
    for i in range(4):
        j = (i + 1) % 4
        f.append((i, j, 4 + j, 4 + i)); f.append((4 + i, 4 + j, 8 + j, 8 + i))
    o = mesh_obj(name, v, f, material); box_uv(o, 2.0); return o

def gable_roof(name, x0, y0, x1, y1, z, h, material, along="y", over=0.4):
    x0 -= over; y0 -= over; x1 += over; y1 += over
    if along == "y":
        xm = (x0 + x1) / 2
        v = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z), (xm, y0, z + h), (xm, y1, z + h)]
    else:
        ym = (y0 + y1) / 2
        v = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z), (x0, ym, z + h), (x1, ym, z + h)]
    f = [(0, 4, 5, 3), (1, 2, 5, 4), (0, 1, 4), (2, 3, 5)] if along == "y" else [(0, 1, 5, 4), (2, 3, 4, 5), (0, 4, 3), (1, 2, 5)]
    o = mesh_obj(name, v, f, material); box_uv(o, 2.0); return o

PARTS = []   # (objeto) para unir al final por material

def window(face, along0, z0, w, h, frame=0.08, depth=0.12, surround=None, shutter=False, kind="vert"):
    """Ventana en una fachada. face = (eje fijo, valor, signo normal)."""
    ax, val, sgn = face
    def b(a0, a1, zz0, zz1, d0, d1, m):
        if ax == "y":
            return box("v", a0, val + sgn * d0, zz0, a1, val + sgn * d1, zz1, m)
        return box("v", val + sgn * d0, a0, zz0, val + sgn * d1, a1, zz1, m)
    out = []
    out.append(b(along0, along0 + w, z0, z0 + h, -0.02, 0.02, M["vidrio"]))
    if shutter:
        out.append(b(along0, along0 + w, z0 + h * 0.72, z0 + h, 0.0, 0.03, M["persiana"]))
    # marco
    out.append(b(along0 - frame, along0, z0 - frame, z0 + h + frame, 0, 0.05, M["marco"]))
    out.append(b(along0 + w, along0 + w + frame, z0 - frame, z0 + h + frame, 0, 0.05, M["marco"]))
    out.append(b(along0, along0 + w, z0 + h, z0 + h + frame, 0, 0.05, M["marco"]))
    if kind == "wide":
        out.append(b(along0 + w / 2 - 0.03, along0 + w / 2 + 0.03, z0, z0 + h, 0, 0.04, M["marco"]))
    if surround:  # recercado de piedra
        s = 0.22
        out.append(b(along0 - s, along0 - frame, z0 - 0.1, z0 + h + 0.2, 0, 0.08, surround))
        out.append(b(along0 + w + frame, along0 + w + s, z0 - 0.1, z0 + h + 0.2, 0, 0.08, surround))
        out.append(b(along0 - s, along0 + w + s, z0 + h + frame, z0 + h + 0.3, 0, 0.1, surround))
    out.append(b(along0 - 0.15, along0 + w + 0.15, z0 - 0.12, z0, 0, 0.14, M["granito_liso"]))   # alféizar
    PARTS.extend(out)

def window_rows(face, a_start, a_end, n, floors, w, h, **kw):
    step = (a_end - a_start) / n
    for fz in floors:
        for i in range(n):
            window(face, a_start + step * i + (step - w) / 2, fz, w, h, **kw)

# =================================================================== TERRENO Y CALLES
Z_CALLE = -5.0              # Colmeiro Laforet bajo la explanada
PARTS.append(box("explanada", -26, -6, -6, 96, 76, 0, M["adoquin"], 2.0))
PARTS.append(box("calle_colmeiro", -26, -19, Z_CALLE - 0.4, 96, -12, Z_CALLE, M["asfalto"], 6))
PARTS.append(box("placita_baja", -7, -12, Z_CALLE - 0.4, 40, -6.6, Z_CALLE + 0.05, M["adoquin"], 2))
PARTS.append(box("acera_ecuador", -26, 74, -0.4, 96, 77, 0.12, M["acera"], 2))
PARTS.append(box("calle_ecuador", -26, 77, -0.6, 96, 86, -0.02, M["asfalto"], 6))
PARTS.append(box("calle_bolivar", 88, -19, -5.2, 96, 86, -0.05, M["asfalto"], 6))
PARTS.append(box("acera_ne", -26, -21, Z_CALLE - 0.4, 96, -19, Z_CALLE + 0.12, M["acera"], 2))

# Jardincillos y bancos en la placita de abajo (Street View)
PARTS.append(box("jardin_bajo1", -4, -11.5, Z_CALLE, 8, -7, Z_CALLE + 0.5, M["cesped"], 3))
PARTS.append(box("jardin_bajo2", 26, -11.5, Z_CALLE, 38, -7.5, Z_CALLE + 0.5, M["cesped"], 3))
for bx in (14, 20):
    PARTS.append(box("banco_asiento", bx, -7.2, Z_CALLE + 0.42, bx + 1.8, -6.7, Z_CALLE + 0.5, M["madera"]))
    PARTS.append(box("banco_resp", bx, -6.75, Z_CALLE + 0.5, bx + 1.8, -6.65, Z_CALLE + 0.95, M["madera"]))
    for px in (bx + 0.1, bx + 1.6):
        PARTS.append(box("banco_pata", px, -7.2, Z_CALLE, px + 0.1, -6.7, Z_CALLE + 0.42, M["hierro"]))

# =================================================================== MURO DE CONTENCIÓN (con murales)
muro = box("muro_contencion", -26, -6.6, Z_CALLE - 0.2, 88, -6.0, 0.6, M["hormigon"], 3)
PARTS.append(muro)
# panel del mural (tucán, flores y letras azules) a la izquierda de la escalera
mur = mesh_obj("mural", [(-6, -6.62, Z_CALLE + 0.3), (26, -6.62, Z_CALLE + 0.3), (26, -6.62, -0.2), (-6, -6.62, -0.2)],
               [(0, 1, 2, 3)], M["mural"])
mur.data.uv_layers.new(); uvd = mur.data.uv_layers.active.data
for li, uvc in zip(range(4), [(1, 0), (0, 0), (0, 1), (1, 1)]): uvd[li].uv = uvc   # (invertido por el reflejo final)
# escalera que sube de la placita a la verja de la iglesia (dos tramos, en paralelo al muro)
STEPS = 16
for i in range(STEPS):
    zt = Z_CALLE + (i + 1) * (-Z_CALLE + 0.6) / STEPS
    x = 2 + i * 0.32
    PARTS.append(box("peldaño", x, -8.4, Z_CALLE, x + 0.34, -6.6, zt, M["granito_liso"], 2))
PARTS.append(box("rellano", 7.1, -8.4, Z_CALLE, 9.5, -6.6, 0.6, M["granito_liso"], 2))
# barandilla gris sobre el muro y la escalera
def railing(x0, y0, x1, y1, z0, z1, h=1.1, n=None):
    L = math.hypot(x1 - x0, y1 - y0); n = n or max(2, int(L / 0.12))
    for i in range(n + 1):
        t = i / n; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t; z = z0 + (z1 - z0) * t
        PARTS.append(box("barrote", x - 0.015, y - 0.015, z, x + 0.015, y + 0.015, z + h, M["baranda"]))
    # pasamanos
    me_v = [(x0, y0 - 0.03, z0 + h), (x1, y1 - 0.03, z1 + h), (x1, y1 + 0.03, z1 + h), (x0, y0 + 0.03, z0 + h),
            (x0, y0 - 0.03, z0 + h + 0.05), (x1, y1 - 0.03, z1 + h + 0.05), (x1, y1 + 0.03, z1 + h + 0.05), (x0, y0 + 0.03, z0 + h + 0.05)]
    PARTS.append(mesh_obj("pasamanos", me_v, [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], M["baranda"]))
railing(-26, -6.3, 7.1, -6.3, 0.6, 0.6)
railing(9.6, -6.3, 56, -6.3, 0.6, 0.6)
railing(2, -8.4, 7.1, -8.4, Z_CALLE + 0.3, 0.6, n=40)

# =================================================================== BLOQUE PRINCIPAL
EAVE = 14.0
# --- Ala NO moderna (x 0..17): planta baja con arcos + 4 alturas de ventanas apaisadas
PARTS.append(box("ala_NO", 0, 0, 0, 17, 33, EAVE, M["revoco_blanco"], 4))
PARTS.append(box("ala_NO_zocalo", -0.1, -0.1, 0, 17.1, 33.1, 1.0, M["granito"], 3))
PARTS.append(box("ala_NO_cornisa", -0.3, -0.3, EAVE - 0.35, 17.3, 33.3, EAVE, M["granito_liso"], 3))
fNE = ("y", 0.0, -1)          # fachada que mira a Colmeiro Laforet (+Y es -v... aquí la fachada está en y=0 mirando a -y)
# OJO: la calle está en y negativo, así que la fachada principal mira a -Y.
window_rows(fNE, 0.6, 16.4, 6, [4.0, 6.8, 9.6, 12.0], 1.9, 1.4, kind="wide", shutter=True)
for i in range(6):                      # arcos de planta baja
    a0 = 0.6 + i * (15.8 / 6) + 0.45
    PARTS.append(box("arco_hueco", a0, -0.06, 0.6, a0 + 1.7, 0.02, 2.6, M["vidrio"]))
fSO_NO = ("y", 33.0, 1)
window_rows(fSO_NO, 0.6, 16.4, 6, [1.2, 4.0, 6.8, 9.6, 12.0], 1.9, 1.4, kind="wide", shutter=True)
fNO = ("x", 0.0, -1)
window_rows(fNO, 1, 32, 10, [1.2, 4.0, 6.8, 9.6, 12.0], 1.6, 1.4, kind="wide", shutter=True)
hip_roof("tejado_ala_NO", 0, 0, 17, 33, EAVE, 4.2, M["teja"])
box("lucernario_1", 9.5, 8.8, EAVE + 1.0, 14.0, 13.3, EAVE + 2.8, M["revoco_blanco"])
box("lucernario_1_hueco", 9.9, 9.2, EAVE + 2.75, 13.6, 12.9, EAVE + 2.85, M["vidrio"])
box("lucernario_2", 6.3, 22.5, EAVE + 1.0, 9.5, 25.7, EAVE + 2.2, M["revoco_blanco"])
box("lucernario_2_hueco", 6.6, 22.8, EAVE + 2.15, 9.2, 25.4, EAVE + 2.25, M["vidrio"])

# --- Ala SE clásica (claustro, x 27..56): revoco crema, esquinas y recercados de granito
X0, X1, Y0, Y1 = 27.0, 56.0, 0.0, 33.0
PAT = (34.5, 8.5, 44.0, 17.0)         # patio del claustro
for (a, b_, c, d) in [(X0, Y0, X1, PAT[1]), (X0, PAT[3], X1, Y1), (X0, PAT[1], PAT[0], PAT[3]), (PAT[2], PAT[1], X1, PAT[3])]:
    PARTS.append(box("claustro", a, b_, 0, c, d, EAVE, M["revoco"], 4))
PARTS.append(box("claustro_zocalo", X0 - 0.1, -0.1, 0, X1 + 0.1, Y1 + 0.1, 1.2, M["granito"], 3))
PARTS.append(box("claustro_imposta", X0 - 0.12, -0.12, 3.55, X1 + 0.12, Y1 + 0.12, 3.8, M["granito_liso"], 3))
PARTS.append(box("claustro_cornisa", X0 - 0.35, -0.35, EAVE - 0.4, X1 + 0.35, Y1 + 0.35, EAVE, M["granito_liso"], 3))
for (qx, qy) in [(X1, Y0), (X1, Y1), (X0, Y1)]:      # esquinales de sillería
    PARTS.append(box("esquinal", qx - 0.75, qy - 0.75, 0, qx + 0.08, qy + 0.08, EAVE, M["granito"], 1.5))
FLOORS_C = [1.6, 4.6, 7.8, 11.0]
window_rows(("y", 0.0, -1), X0 + 1.2, X1 - 1.0, 9, FLOORS_C, 1.05, 1.75, surround=M["granito_liso"], shutter=True)
window_rows(("x", X1, 1), 1.0, 32.0, 10, FLOORS_C, 1.05, 1.75, surround=M["granito_liso"], shutter=True)
window_rows(("y", Y1, 1), X0 + 1.2, X1 - 1.0, 9, FLOORS_C, 1.05, 1.75, surround=M["granito_liso"], shutter=True)
# patio interior
window_rows(("y", PAT[1], 1), PAT[0] + 0.5, PAT[2] - 0.5, 3, FLOORS_C, 1.0, 1.6)
window_rows(("y", PAT[3], -1), PAT[0] + 0.5, PAT[2] - 0.5, 3, FLOORS_C, 1.0, 1.6)
ring_roof("tejado_claustro", (X0, Y0, X1, Y1), PAT, EAVE, 3.8, M["teja"])
PARTS.append(box("patio_suelo", PAT[0], PAT[1], 0, PAT[2], PAT[3], 0.05, M["granito_liso"], 2))

# =================================================================== IGLESIA
CX = 22.0                    # eje de la iglesia
NAVE_W = 10.0
NX0, NX1 = CX - NAVE_W / 2, CX + NAVE_W / 2
NAVE_EAVE, NAVE_RIDGE = 12.5, 16.0
PARTS.append(box("nave", NX0, 0, 0, NX1, 30, NAVE_EAVE, M["granito"], 3))
gable_roof("tejado_nave", NX0, 0.2, NX1, 30, NAVE_EAVE, NAVE_RIDGE - NAVE_EAVE, M["teja"], along="y")

# --- Fachada (mira a -Y, a Colmeiro Laforet). Sobresale 0,8 m
FY = -0.8
FW = 11.0
FX0, FX1 = CX - FW / 2, CX + FW / 2
COR = 12.6                    # cornisa
APEX = 16.6                   # vértice del frontón
PARTS.append(box("fachada", FX0, FY, 0, FX1, 0.2, COR, M["granito"], 2.2))
PARTS.append(box("fachada_zocalo", FX0 - 0.1, FY - 0.15, 0, FX1 + 0.1, 0.2, 0.9, M["granito_liso"], 2))
# pilastras de esquina (cajeadas)
for px in (FX0 - 0.15, FX1 - 1.05):
    PARTS.append(box("pilastra", px, FY - 0.3, 0, px + 1.2, FY + 0.1, COR - 0.6, M["granito_liso"], 2))
    PARTS.append(box("pilastra_cajeado", px + 0.25, FY - 0.36, 1.2, px + 0.95, FY - 0.28, COR - 1.4, M["granito"], 2))
# entablamento + cornisa
PARTS.append(box("friso", FX0 - 0.2, FY - 0.35, COR - 0.6, FX1 + 0.2, 0.2, COR - 0.1, M["granito_liso"], 2))
PARTS.append(box("cornisa", FX0 - 0.45, FY - 0.65, COR - 0.1, FX1 + 0.45, 0.2, COR + 0.25, M["granito_liso"], 2))
# frontón triangular con molduras
def tri_prism(name, x0, x1, zb, zt, y0, y1, m):
    xm = (x0 + x1) / 2
    v = [(x0, y0, zb), (x1, y0, zb), (xm, y0, zt), (x0, y1, zb), (x1, y1, zb), (xm, y1, zt)]
    f = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    o = mesh_obj(name, v, f, m); box_uv(o, 2.2); PARTS.append(o); return o
tri_prism("tímpano", FX0 + 0.1, FX1 - 0.1, COR + 0.25, APEX, FY - 0.1, 0.2, M["granito"])
def slab_between(name, p0, p1, half_w, depth_y, m):
    (x0, z0), (x1, z1) = p0, p1
    dx, dz = x1 - x0, z1 - z0; L = math.hypot(dx, dz); nx, nz = -dz / L * half_w, dx / L * half_w
    y0, y1 = depth_y
    v = [(x0 - nx, y0, z0 - nz), (x1 - nx, y0, z1 - nz), (x1 + nx, y0, z1 + nz), (x0 + nx, y0, z0 + nz)]
    v += [(a, y1, c) for (a, _, c) in v]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    o = mesh_obj(name, v, f, m); box_uv(o, 2); PARTS.append(o); return o
slab_between("moldura_fronton_I", (FX0 - 0.45, COR + 0.35), (CX, APEX + 0.35), 0.2, (FY - 0.6, 0.2), M["granito_liso"])
slab_between("moldura_fronton_D", (CX, APEX + 0.35), (FX1 + 0.45, COR + 0.35), 0.2, (FY - 0.6, 0.2), M["granito_liso"])
# escudo en el tímpano
PARTS.append(box("escudo", CX - 0.7, FY - 0.25, COR + 0.7, CX + 0.7, FY - 0.05, COR + 2.4, M["granito_liso"], 1))
sphere("escudo_corona", CX, FY - 0.2, COR + 2.55, 0.32, M["granito_liso"], 1, 1.3, 0.5, 0.6)
# pináculos / bolas en los extremos del frontón
for px in (FX0 - 0.2, FX1 + 0.2):
    PARTS.append(box("pedestal_bola", px - 0.35, FY - 0.45, COR + 0.25, px + 0.35, FY + 0.25, COR + 0.85, M["granito_liso"], 1))
    sphere("bola", px, FY - 0.1, COR + 1.2, 0.36, M["granito_liso"], 2)
    cyl("bola_punta", px, FY - 0.1, COR + 1.5, COR + 1.9, 0.08, M["granito_liso"], 6, 0.0)

# rosetón
ros = cyl("roseton", CX, FY - 0.12, 0, 0.12, 0.95, M["roseton"], 32)
ros.rotation_euler = (math.pi / 2, 0, 0); ros.location = (CX, FY - 0.12, 9.3)
me = ros.data; me.uv_layers.new(); uvd = me.uv_layers.active.data
for p in me.polygons:
    for li in p.loop_indices:
        co = me.vertices[me.loops[li].vertex_index].co
        uvd[li].uv = (co.x / 1.9 + 0.5, co.y / 1.9 + 0.5)
mold = cyl("roseton_moldura", CX, 0, 0, 0.2, 1.2, M["granito_liso"], 32)
mold.rotation_euler = (math.pi / 2, 0, 0); mold.location = (CX, FY + 0.03, 9.3)
PARTS += [ros, mold]

# hornacina con la Virgen
PARTS.append(box("hornacina_fondo", CX - 0.55, FY - 0.02, 5.9, CX + 0.55, FY + 0.05, 7.4, M["granito_liso"], 1))
h_arc = cyl("hornacina_arco", 0, 0, 0, 0.3, 0.62, M["granito_liso"], 16); h_arc.rotation_euler = (math.pi / 2, 0, 0)
h_arc.location = (CX, FY - 0.1, 7.4); PARTS.append(h_arc)
PARTS.append(box("repisa", CX - 0.6, FY - 0.45, 5.75, CX + 0.6, FY, 5.95, M["granito_liso"], 1))
cyl("virgen_cuerpo", CX, FY - 0.25, 5.95, 7.1, 0.22, M["piedra_estatua"], 10, 0.12)
sphere("virgen_cabeza", CX, FY - 0.25, 7.22, 0.13, M["piedra_estatua"], 1)
# ventanas altas (vidrieras estrechas con arco) a ambos lados
for vx in (CX - 3.6, CX + 3.0):
    PARTS.append(box("vidriera", vx, FY - 0.04, 4.5, vx + 0.6, FY + 0.05, 9.6, M["vidrio"], 1))
    a = cyl("vidriera_arco", 0, 0, 0, 0.1, 0.3, M["vidrio"], 10); a.rotation_euler = (math.pi / 2, 0, 0)
    a.location = (vx + 0.3, FY - 0.0, 9.6); PARTS.append(a)
    PARTS.append(box("vidriera_recerco", vx - 0.18, FY - 0.12, 4.35, vx + 0.78, FY - 0.02, 4.5, M["granito_liso"], 1))
# portada: puerta de madera con arco de medio punto, pilastras y frontón curvo
PARTS.append(box("puerta", CX - 1.1, FY - 0.12, 0.3, CX + 1.1, FY - 0.02, 3.4, M["madera"], 1))
pa = cyl("puerta_arco", 0, 0, 0, 0.1, 1.1, M["madera"], 16); pa.rotation_euler = (math.pi / 2, 0, 0)
pa.location = (CX, FY - 0.12, 3.4); PARTS.append(pa)
for px in (CX - 1.75, CX + 1.25):
    PARTS.append(box("portada_pilastra", px, FY - 0.4, 0.3, px + 0.5, FY, 4.6, M["granito_liso"], 1))
PARTS.append(box("portada_dintel", CX - 1.95, FY - 0.5, 4.6, CX + 1.95, FY, 5.0, M["granito_liso"], 1))
tri_prism("portada_fronton", CX - 2.1, CX + 2.1, 5.0, 5.9, FY - 0.55, FY, M["granito_liso"])
for i in range(3):            # escalinata de la iglesia
    PARTS.append(box("escalon_iglesia", CX - 2.4 + i * 0.25, FY - 1.4 + i * 0.4, 0, CX + 2.4 - i * 0.25, FY, 0.1 + i * 0.1, M["granito_liso"], 1))

# --- Espadaña / campanario sobre el vértice
BZ = APEX - 0.3
PARTS.append(box("campanario_base", CX - 1.05, FY - 0.3, BZ, CX + 1.05, FY + 1.6, BZ + 1.0, M["granito_liso"], 1))
PARTS.append(box("campanario_cuerpo_I", CX - 1.0, FY - 0.25, BZ + 1.0, CX - 0.55, FY + 1.55, BZ + 3.1, M["granito"], 1))
PARTS.append(box("campanario_cuerpo_D", CX + 0.55, FY - 0.25, BZ + 1.0, CX + 1.0, FY + 1.55, BZ + 3.1, M["granito"], 1))
PARTS.append(box("campanario_dintel", CX - 1.0, FY - 0.25, BZ + 3.1, CX + 1.0, FY + 1.55, BZ + 3.55, M["granito"], 1))
PARTS.append(box("campanario_cornisa", CX - 1.2, FY - 0.45, BZ + 3.55, CX + 1.2, FY + 1.75, BZ + 3.8, M["granito_liso"], 1))
camp = cyl("campana", CX, FY + 0.65, BZ + 1.7, BZ + 2.7, 0.42, M["bronce"], 14, 0.2)
cyl("yugo", CX, FY + 0.65, BZ + 2.7, BZ + 3.1, 0.06, M["hierro"], 6); PARTS.append(camp)
cup = cyl("cupulin", CX, FY + 0.65, BZ + 3.8, BZ + 5.0, 1.0, M["granito_liso"], 8, 0.15); cup.rotation_euler = (0, 0, math.pi / 8); PARTS.append(cup)
sphere("cupulin_bola", CX, FY + 0.65, BZ + 5.15, 0.22, M["granito_liso"], 1)
PARTS.append(box("cruz_v", CX - 0.05, FY + 0.6, BZ + 5.3, CX + 0.05, FY + 0.7, BZ + 6.5, M["hierro"], 1))
PARTS.append(box("cruz_h", CX - 0.35, FY + 0.6, BZ + 6.0, CX + 0.35, FY + 0.7, BZ + 6.1, M["hierro"], 1))
for px in (CX - 1.15, CX + 1.15):
    sphere("bola_campanario", px, FY + 0.65, BZ + 4.0, 0.18, M["granito_liso"], 1)

# =================================================================== EXPLANADA DELANTERA (jardín y verja)
PARTS.append(box("cesped_I", -4, -5.8, 0, 13.5, -1.0, 0.12, M["cesped"], 3))
PARTS.append(box("cesped_D", 30.5, -5.8, 0, 56, -1.0, 0.12, M["cesped"], 3))
# verja de hierro delante de la iglesia
for i in range(36):
    x = CX - 4.5 + i * 0.25
    PARTS.append(box("verja", x, -3.53, 0, x + 0.04, -3.47, 2.0, M["hierro"], 1))
PARTS.append(box("verja_trav", CX - 4.5, -3.55, 1.85, CX + 4.5, -3.45, 1.95, M["hierro"], 1))
for px in (CX - 4.7, CX + 4.5):
    PARTS.append(box("verja_pilar", px, -3.7, 0, px + 0.3, -3.3, 2.3, M["granito_liso"], 1))

def tree(name, x, y, z, h=8, r=3.2, dark=False):
    cyl(name + "_tronco", x, y, z, z + h * 0.45, 0.25, M["tronco"], 8, 0.18)
    mm = M["hoja2"] if dark else M["hoja"]
    import random
    rr = random.Random(hash(name) & 0xffff)
    for k in range(6):
        sphere(name + "_copa", x + rr.uniform(-r * .5, r * .5), y + rr.uniform(-r * .5, r * .5),
               z + h * 0.55 + rr.uniform(0, h * 0.35), r * rr.uniform(0.55, 0.8), mm, 2)
tree("arbol_izq1", 10.0, -3.4, 0, 9, 3.4)
tree("arbol_izq2", 2.0, -4.3, 0, 8, 3.0, True)
tree("arbol_der1", 33.5, -3.6, 0, 9.5, 3.6)
tree("arbol_der2", 42.0, -4.2, 0, 8, 3.2, True)
tree("arbol_der3", 50.0, -4.4, 0, 7, 2.8)
tree("conifera_NO", -8.0, -4.4, 0, 13, 2.4, True)
tree("arbol_placita", 30, -9.5, Z_CALLE, 6, 2.2)
tree("arbol_placita2", 1, -9.8, Z_CALLE, 6, 2.0)

# =================================================================== PABELLÓN DEPORTIVO (chapa roja, Colmeiro Laforet)
PX0, PX1, PY0, PY1 = 57.0, 88.0, -5.8, 7.0
PARTS.append(box("pabellon", PX0, PY0, 0, PX1, PY1, 6.0, M["revoco_blanco"], 4))
gable_roof("pabellon_tejado", PX0, PY0, PX1, PY1, 6.0, 1.6, M["chapa"], along="x")
PARTS.append(box("pabellon_reja", PX0 + 1, PY0 - 0.05, 1.5, PX1 - 1, PY0 + 0.05, 5.2, M["hierro"], 1))
pm = mesh_obj("mural_pabellon", [(57.5, -6.62, Z_CALLE + 0.5), (70, -6.62, Z_CALLE + 0.5), (70, -6.62, 0.4), (57.5, -6.62, 0.4)],
              [(0, 1, 2, 3)], M["mural"])
pm.data.uv_layers.new(); uvd = pm.data.uv_layers.active.data
for li, uvc in zip(range(4), [(1, 0), (0.62, 0), (0.62, 1), (1, 1)]): uvd[li].uv = uvc

# =================================================================== PISTA POLIDEPORTIVA y edificios del recinto
pista = mesh_obj("pista", [(18, 36, 0.06), (56, 36, 0.06), (56, 61, 0.06), (18, 61, 0.06)], [(0, 1, 2, 3)], M["pista"])
pista.data.uv_layers.new(); uvd = pista.data.uv_layers.active.data
for li, uvc in zip(range(4), [(0, 0), (1, 0), (1, 1), (0, 1)]): uvd[li].uv = uvc
for cx_ in (19.0, 55.0):      # canastas
    cyl("canasta_poste", cx_, 48.5, 0, 3.05, 0.08, M["baranda"], 8)
    PARTS.append(box("tablero", cx_ - 0.05 + (0.9 if cx_ < 30 else -0.9), 47.6, 2.9, cx_ + 0.05 + (0.9 if cx_ < 30 else -0.9), 49.4, 4.0, M["marco"], 1))
# soportal / porche entre bloque y pista
PARTS.append(box("porche_losa", 17, 33, 3.4, 56, 35.5, 3.7, M["hormigon"], 3))
for i in range(14):
    PARTS.append(box("porche_pilar", 17.5 + i * 2.85, 35.0, 0, 17.8 + i * 2.85, 35.3, 3.4, M["hormigon"], 1))
# edificio de Rúa do Ecuador (granito, ventanas corridas con rejas, cubierta plana)
PARTS.append(box("edif_ecuador", 4, 62, 0, 60, 74, 14.5, M["granito"], 2.5))
PARTS.append(box("edif_ecuador_azotea", 4.3, 62.3, 14.5, 59.7, 73.7, 14.7, M["azotea"], 3))
PARTS.append(box("edif_ecuador_peto", 4, 73.6, 14.5, 60, 74, 15.4, M["granito_liso"], 2))
for z_ in (3.4, 6.9, 10.4):
    PARTS.append(box("imposta_ecuador", 3.9, 73.95, z_ - 0.15, 60.1, 74.25, z_, M["granito_liso"], 2))
window_rows(("y", 74.0, 1), 5, 59, 18, [1.2, 4.2, 7.7, 11.2], 2.3, 1.7, kind="wide", shutter=True)
window_rows(("y", 62.0, -1), 5, 59, 18, [4.2, 7.7, 11.2], 2.3, 1.7, kind="wide")
if not GAME:   # en el juego ya están (anexo de placas solares y edificios de Simón Bolívar)
    # anexo oeste (cubiertas rojas con placas solares)
    PARTS.append(box("anexo_O", -12, 20, 0, 2, 60, 11, M["revoco_blanco"], 4))
    for k in range(4):
        gable_roof("anexo_tejado", -12, 20 + k * 10, 2, 30 + k * 10, 11, 1.6, M["teja"], along="x", over=0.2)
    for k in range(3):
        o = box("placas", -10, 22 + k * 11, 0, -1, 25.5 + k * 11, 0.08, M["solar"], 1)
        o.location = (0, 0, 11.4); o.rotation_euler = (-0.15, 0, 0)
    window_rows(("x", 2.0, 1), 21, 59, 12, [1.2, 4.6, 8.0], 1.6, 1.5, kind="wide")
    window_rows(("x", -12.0, -1), 21, 59, 12, [4.6, 8.0], 1.4, 1.4)
    # edificio blanco de la esquina con Simón Bolívar
    PARTS.append(box("edif_bolivar", 62, 28, 0, 82, 50, 13, M["revoco_blanco"], 4))
    hip_roof("edif_bolivar_tejado", 62, 28, 82, 40, 13, 2.6, M["teja"])
    PARTS.append(box("edif_bolivar_azotea", 62.2, 40, 13, 81.8, 49.8, 13.2, M["azotea"], 3))
    window_rows(("x", 82, 1), 29, 49, 7, [1.2, 4.4, 7.6, 10.4], 1.4, 1.5, shutter=True)
    window_rows(("y", 28, -1), 63, 81, 6, [1.2, 4.4, 7.6, 10.4], 1.4, 1.5, shutter=True)
if not GAME:
    # muro y valla del recinto en Ecuador
    PARTS.append(box("valla_ecuador_muro", -12, 73.6, 0, 4, 74, 1.2, M["granito"], 2))
    for i in range(80):
        x = -11.8 + i * 0.22
        PARTS.append(box("valla_barrote", x, 73.78, 1.2, x + 0.03, 73.82, 2.6, M["hierro"], 1))

    # =================================================================== limpieza / unión por material
    for i in range(6):
        a0 = 0.6 + i * (15.8 / 6) + 0.45
        a = cyl("arco_pb", 0, 0, 0, 0.08, 0.85, M["vidrio"], 14); a.rotation_euler = (math.pi / 2, 0, 0)
        a.location = (a0 + 0.85, -0.02, 2.6)

SKIP_GAME = ("explanada", "calle_", "acera_", "pista", "canasta", "tablero", "placita_baja")
if GAME:
    for o in list(col.objects):
        if o.name.startswith(SKIP_GAME):
            bpy.data.objects.remove(o, do_unlink=True)
    # zócalos bajo cada edificio para que nunca queden flotando sobre el terreno del juego
    for (x0, y0, x1, y1) in [(0, 0, 17, 33), (NX0, -0.8, NX1, 30), (27, 0, 56, 33), (PX0, PY0, PX1, PY1),
                             (4, 62, 60, 74), (17, 33, 56, 35.5)]:
        box("zocalo_juego", x0 + 0.05, y0 + 0.05, -6, x1 - 0.05, y1 - 0.05, 0.02, M["granito"], 3)

def join_by_material():
    groups = {}
    for o in list(col.objects):
        if o.type != "MESH" or not o.data.materials: continue
        groups.setdefault(o.data.materials[0].name, []).append(o)
    out = []
    for mname, objs in groups.items():
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs: o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        if len(objs) > 1: bpy.ops.object.join()
        o = bpy.context.view_layer.objects.active
        o.name = "CdM_" + mname.replace("CM_", "")
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        out.append(o)
    return out

joined = join_by_material()
from mathutils import Matrix
for o in joined:
    for p in o.data.polygons: p.use_smooth = False
    # reflejo en Y: el modelo se construyó con +Y hacia Ecuador; así queda como en la realidad
    o.data.transform(Matrix.Scale(-1, 4, (0, 1, 0)))
    o.data.flip_normals()
    o.data.update()

# Raíz para mover/rotar todo el conjunto
root = bpy.data.objects.new("CompaniaMaria_root", None); link(root)
for o in joined: o.parent = root
print("Colegio Compañía de María creado:", len(joined), "mallas,",
      sum(len(o.data.polygons) for o in joined), "caras")
