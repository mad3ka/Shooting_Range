import array
import json
import math
import os
import random
import sys
import time

import pygame

W, H = 1280, 720
FPS = 120
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "saves")
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
OLD_SAVE_PATH = os.path.join(BASE_DIR, "save.json")
MAX_SLOTS = 8

NEAR = 0.1
FOG_START = 30.0
FOG_END = 115.0
BASE_FOV = 70.0
SKY_TOP = (34, 88, 176)
SKY_HORIZON = (206, 225, 240)
FOG_COLOR = SKY_HORIZON
GROUND_COLOR = (96, 142, 78)
TILE_A = (116, 170, 90)
TILE_B = (104, 158, 82)
ARENA = 40.0
WALL_H = 3.2
GRAVITY = 22.0
PLAYER_R = 0.35
PLAYER_H = 1.8

GOLD = (255, 200, 60)
ACCENT = (255, 196, 60)
RING_MULT = (3.0, 2.0, 1.5, 1.2, 1.0)
RING_COLORS = ((255, 215, 0), (255, 150, 90), (255, 255, 255), (230, 236, 245), (210, 218, 230))


T = {
    "ru": {
        "caption": "Тир-Полигон",
        "title": "ТИР-ПОЛИГОН",
        "subtitle": "Стреляй по мишеням · копи очки · покупай улучшения",
        "resume": "ПРОДОЛЖИТЬ",
        "language": "РУССКИЙ  /  English",
        "quit": "ВЫХОД",
        "controls": "УПРАВЛЕНИЕ",
        "tip": "Центр мишени — x3 очков · Серия попаданий — комбо · Дальний выстрел — бонус",
        "score": "ОЧКИ",
        "combo": "КОМБО",
        "accuracy": "Точность {}%",
        "ammo": "ПАТРОНЫ",
        "reloading": "ПЕРЕЗАРЯДКА",
        "reload_hint": "{} — перезарядка",
        "upgrade_ready": "Доступно улучшение — нажми {}",
        "hint": "{} — магазин · Esc — пауза",
        "bullseye": "В ЯБЛОЧКО!",
        "gold_hit": "ЗОЛОТАЯ МИШЕНЬ! +{}",
        "gold_spawn": "Появилась золотая мишень!",
        "long_shot": "дальний выстрел",
        "combo_lost": "комбо сброшено",
        "shop_title": "МАГАЗИН УЛУЧШЕНИЙ",
        "max": "МАКС",
        "level": "Уровень {} / {}",
        "stats": "Попаданий: {}   ·   В яблочко: {}   ·   Лучшее комбо: {}   ·   Точность: {}%",
        "shop_hint": "Клик или 1–0 — купить  ·  {} / Esc — назад",
        "pause": "ПАУЗА",
        "pause_hint": "Esc — продолжить  ·  прогресс сохраняется автоматически",
        "continue": "ПРОДОЛЖИТЬ",
        "new_game": "НОВАЯ ИГРА",
        "load_game": "ЗАГРУЗИТЬ ИГРУ",
        "settings": "НАСТРОЙКИ",
        "main_menu": "ГЛАВНОЕ МЕНЮ",
        "back": "НАЗАД",
        "slot_info": "{} · {} очков",
        "default_name": "Игра {}",
        "new_title": "НОВАЯ ИГРА",
        "name_prompt": "Название сохранения",
        "create": "СОЗДАТЬ",
        "cancel": "ОТМЕНА",
        "name_hint": "Enter — создать  ·  Esc — отмена",
        "slots_title": "СОХРАНЕНИЯ",
        "slots_empty": "Сохранений пока нет",
        "slot_stats": "Улучшений: {}  ·  Попаданий: {}  ·  Комбо: {}",
        "slot_time": "{}  ·  в игре {}",
        "last": "ПОСЛЕДНЕЕ",
        "delete_q": "Удалить это сохранение?",
        "yes": "ДА",
        "no": "НЕТ",
        "slots_full": "Максимум {} сохранений — удалите старое",
        "slots_hint": "Клик — загрузить  ·  Esc — назад",
        "hours": "{} ч {:02d} мин",
        "minutes": "{} мин",
        "points_word": "очков",
        "controls_title": "КЛАВИШИ",
        "mouse": "МЫШЬ",
        "sensitivity": "Чувствительность",
        "invert_y": "Инверсия по вертикали",
        "on": "ВКЛ",
        "off": "ВЫКЛ",
        "lang_title": "ЯЗЫК",
        "reset_controls": "СБРОСИТЬ КЛАВИШИ",
        "press_key": "Нажмите клавишу...",
        "rebind_hint": "Клик по клавише — переназначить  ·  Esc — отмена / назад",
        "fixed_keys": "Мышь — обзор  ·  Esc — пауза",
        "look": "Обзор",
        "pause_action": "Пауза",
        "act_forward": "Вперёд",
        "act_back": "Назад",
        "act_left": "Влево",
        "act_right": "Вправо",
        "act_sprint": "Бег",
        "act_jump": "Прыжок",
        "act_shoot": "Выстрел",
        "act_aim": "Прицел (зум)",
        "act_reload": "Перезарядка",
        "act_shop": "Магазин",
        "act_camera": "Сменить вид",
        "camera_title": "ВИД КАМЕРЫ",
        "cam_third": "От 3-го лица",
        "cam_first": "От 1-го лица",
        "lmb": "ЛКМ",
        "rmb": "ПКМ",
        "mmb": "СКМ",
        "mouse_n": "Мышь {}",
        "space": "Пробел",
        "mouse_key": "Мышь",
        "up_fire_rate": ("Скорострельность", "Стреляй чаще"),
        "up_mag": ("Большой магазин", "Больше патронов"),
        "up_reload": ("Быстрая перезарядка", "Меньше ожидания"),
        "up_accuracy": ("Точность", "Меньше разброс пуль"),
        "up_mult": ("Множитель очков", "Больше очков за попадание"),
        "up_speed": ("Лёгкие ботинки", "Быстрее бег, выше прыжок"),
        "up_zoom": ("Оптический прицел", "Сильнее зум на ПКМ"),
        "up_auto": ("Автоматический огонь", "Зажми ЛКМ — очередь"),
        "up_explosive": ("Взрывные пули", "Взрыв задевает соседние мишени"),
        "up_targets": ("Больше мишеней", "+2 мишени на полигоне"),
        "st_fire_rate": "{:.1f} выстр/с",
        "st_mag": "{} патронов",
        "st_reload": "{:.2f} с",
        "st_accuracy": "разброс {}%",
        "st_speed": "{:.1f} м/с",
        "st_zoom": "зум x{:.1f}",
        "st_yes": "есть",
        "st_no": "нет",
        "st_explosive": "радиус {:.1f} м",
        "st_targets": "{} мишеней",
    },
    "en": {
        "caption": "Shooting Range",
        "title": "SHOOTING RANGE",
        "subtitle": "Hit the targets · earn points · buy upgrades",
        "resume": "RESUME",
        "language": "ENGLISH  /  Русский",
        "quit": "QUIT",
        "controls": "CONTROLS",
        "tip": "Bullseye — x3 points · Hit streak — combo · Long shot — bonus",
        "score": "SCORE",
        "combo": "COMBO",
        "accuracy": "Accuracy {}%",
        "ammo": "AMMO",
        "reloading": "RELOADING",
        "reload_hint": "{} — reload",
        "upgrade_ready": "Upgrade available — press {}",
        "hint": "{} — shop · Esc — pause",
        "bullseye": "BULLSEYE!",
        "gold_hit": "GOLDEN TARGET! +{}",
        "gold_spawn": "A golden target appeared!",
        "long_shot": "long shot",
        "combo_lost": "combo lost",
        "shop_title": "UPGRADE SHOP",
        "max": "MAX",
        "level": "Level {} / {}",
        "stats": "Hits: {}   ·   Bullseyes: {}   ·   Best combo: {}   ·   Accuracy: {}%",
        "shop_hint": "Click or 1–0 — buy  ·  {} / Esc — back",
        "pause": "PAUSED",
        "pause_hint": "Esc — resume  ·  progress is saved automatically",
        "continue": "CONTINUE",
        "new_game": "NEW GAME",
        "load_game": "LOAD GAME",
        "settings": "SETTINGS",
        "main_menu": "MAIN MENU",
        "back": "BACK",
        "slot_info": "{} · {} points",
        "default_name": "Game {}",
        "new_title": "NEW GAME",
        "name_prompt": "Save name",
        "create": "CREATE",
        "cancel": "CANCEL",
        "name_hint": "Enter — create  ·  Esc — cancel",
        "slots_title": "SAVED GAMES",
        "slots_empty": "No saved games yet",
        "slot_stats": "Upgrades: {}  ·  Hits: {}  ·  Combo: {}",
        "slot_time": "{}  ·  played {}",
        "last": "LAST",
        "delete_q": "Delete this save?",
        "yes": "YES",
        "no": "NO",
        "slots_full": "Maximum of {} saves — delete an old one",
        "slots_hint": "Click — load  ·  Esc — back",
        "hours": "{}h {:02d}m",
        "minutes": "{} min",
        "points_word": "points",
        "controls_title": "KEY BINDINGS",
        "mouse": "MOUSE",
        "sensitivity": "Sensitivity",
        "invert_y": "Invert vertical look",
        "on": "ON",
        "off": "OFF",
        "lang_title": "LANGUAGE",
        "reset_controls": "RESET BINDINGS",
        "press_key": "Press a key...",
        "rebind_hint": "Click a binding to change it  ·  Esc — cancel / back",
        "fixed_keys": "Mouse — look  ·  Esc — pause",
        "look": "Look",
        "pause_action": "Pause",
        "act_forward": "Forward",
        "act_back": "Backward",
        "act_left": "Left",
        "act_right": "Right",
        "act_sprint": "Sprint",
        "act_jump": "Jump",
        "act_shoot": "Shoot",
        "act_aim": "Aim (zoom)",
        "act_reload": "Reload",
        "act_shop": "Shop",
        "act_camera": "Toggle view",
        "camera_title": "CAMERA VIEW",
        "cam_third": "Third person",
        "cam_first": "First person",
        "lmb": "LMB",
        "rmb": "RMB",
        "mmb": "MMB",
        "mouse_n": "Mouse {}",
        "space": "Space",
        "mouse_key": "Mouse",
        "up_fire_rate": ("Fire Rate", "Shoot faster"),
        "up_mag": ("Extended Mag", "More rounds per magazine"),
        "up_reload": ("Fast Reload", "Less waiting"),
        "up_accuracy": ("Accuracy", "Tighter bullet spread"),
        "up_mult": ("Score Multiplier", "More points per hit"),
        "up_speed": ("Light Boots", "Run faster, jump higher"),
        "up_zoom": ("Scope", "Stronger zoom on RMB"),
        "up_auto": ("Full Auto", "Hold LMB to spray"),
        "up_explosive": ("Explosive Rounds", "Blast hits nearby targets"),
        "up_targets": ("More Targets", "+2 targets on the range"),
        "st_fire_rate": "{:.1f} shots/s",
        "st_mag": "{} rounds",
        "st_reload": "{:.2f} s",
        "st_accuracy": "spread {}%",
        "st_speed": "{:.1f} m/s",
        "st_zoom": "zoom x{:.1f}",
        "st_yes": "yes",
        "st_no": "no",
        "st_explosive": "radius {:.1f} m",
        "st_targets": "{} targets",
    },
}


def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_mul(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def v_dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def v_len(a):
    return math.sqrt(v_dot(a, a))


def v_norm(a):
    length = v_len(a) or 1.0
    return v_mul(a, 1.0 / length)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return (int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t))


def scale_color(c, k):
    return (min(255, int(c[0] * k)), min(255, int(c[1] * k)), min(255, int(c[2] * k)))


LIGHT = v_norm((0.4, 0.85, -0.35))


def fog_k(depth):
    if depth <= FOG_START:
        return 0.0
    return min(1.0, (depth - FOG_START) / (FOG_END - FOG_START))


def fog(color, depth):
    if depth <= FOG_START:
        return color
    return lerp_color(color, FOG_COLOR, fog_k(depth))


def shade(color, normal):
    diffuse = max(0.0, v_dot(normal, LIGHT))
    sky = 0.08 * max(0.0, normal[1])
    return scale_color(color, 0.52 + 0.5 * diffuse + sky)


def rotate(v, yaw, pitch=0.0):
    x, y, z = v
    if pitch:
        cp, sp = math.cos(pitch), math.sin(pitch)
        y, z = y * cp + z * sp, -y * sp + z * cp
    if yaw:
        cy, sy = math.cos(yaw), math.sin(yaw)
        x, z = x * cy + z * sy, -x * sy + z * cy
    return (x, y, z)


def ray_aabb(o, d, b):
    tmin, tmax = -1e9, 1e9
    for i in range(3):
        if abs(d[i]) < 1e-9:
            if o[i] < b[i] or o[i] > b[i + 3]:
                return None
        else:
            t1 = (b[i] - o[i]) / d[i]
            t2 = (b[i + 3] - o[i]) / d[i]
            if t1 > t2:
                t1, t2 = t2, t1
            tmin = max(tmin, t1)
            tmax = min(tmax, t2)
            if tmin > tmax:
                return None
    if tmin < 0:
        return None
    return tmin


def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def clip_near(pts):
    out = []
    n = len(pts)
    for i in range(n):
        a = pts[i]
        b = pts[(i + 1) % n]
        a_in = a[2] >= NEAR
        if a_in:
            out.append(a)
        if a_in != (b[2] >= NEAR):
            t = (NEAR - a[2]) / (b[2] - a[2])
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, NEAR))
    return out


def clip_screen(pts, margin=50):
    for axis, limit, keep_less in ((0, -margin, False), (0, W + margin, True),
                                   (1, -margin, False), (1, H + margin, True)):
        if not pts:
            return pts
        out = []
        n = len(pts)
        for i in range(n):
            a = pts[i]
            b = pts[(i + 1) % n]
            a_in = (a[axis] <= limit) if keep_less else (a[axis] >= limit)
            b_in = (b[axis] <= limit) if keep_less else (b[axis] >= limit)
            if a_in:
                out.append(a)
            if a_in != b_in:
                t = (limit - a[axis]) / (b[axis] - a[axis])
                out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        pts = out
    return pts


def needs_screen_clip(pts):
    for x, y in pts:
        if x < -50 or x > W + 50 or y < -50 or y > H + 50:
            return True
    return False


def clip_line(a, b):
    if a[2] < NEAR and b[2] < NEAR:
        return None
    if a[2] < NEAR:
        t = (NEAR - a[2]) / (b[2] - a[2])
        a = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, NEAR)
    elif b[2] < NEAR:
        t = (NEAR - b[2]) / (a[2] - b[2])
        b = (b[0] + (a[0] - b[0]) * t, b[1] + (a[1] - b[1]) * t, NEAR)
    return a, b


CORNERS = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
           (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
BOX_FACES = [((0, 1, 2, 3), (0, 0, -1)), ((4, 5, 6, 7), (0, 0, 1)),
             ((0, 3, 7, 4), (-1, 0, 0)), ((1, 2, 6, 5), (1, 0, 0)),
             ((0, 1, 5, 4), (0, -1, 0)), ((3, 2, 6, 7), (0, 1, 0))]


def box_faces(center, half, color, yaw=0.0, pitch=0.0, top=None):
    hx, hy, hz = half
    pts = [v_add(center, rotate((sx * hx, sy * hy, sz * hz), yaw, pitch)) for sx, sy, sz in CORNERS]
    faces = []
    for idx, n in BOX_FACES:
        if n[1] < 0 and not pitch:
            continue
        col = top if (top and n[1] > 0) else color
        faces.append(([pts[i] for i in idx], rotate(n, yaw, pitch), col))
    return faces


def radial_glow(radius, color, power=2.0):
    surf = pygame.Surface((radius * 2, radius * 2))
    for r in range(radius, 0, -2):
        k = (1 - r / radius) ** power
        pygame.draw.circle(surf, scale_color(color, k), (radius, radius), r)
    return surf


class Camera:
    def __init__(self):
        self.pos = (0.0, 2.0, -4.0)
        self.yaw = 0.0
        self.pitch = 0.0
        self.fov = math.radians(BASE_FOV)
        self.update()

    def update(self):
        self.cy, self.sy = math.cos(self.yaw), math.sin(self.yaw)
        self.cp, self.sp = math.cos(self.pitch), math.sin(self.pitch)
        self.f = (W / 2) / math.tan(self.fov / 2)

    @property
    def forward(self):
        return (self.sy * self.cp, self.sp, self.cy * self.cp)

    @property
    def right(self):
        return (self.cy, 0.0, -self.sy)

    @property
    def up(self):
        return (-self.sp * self.sy, self.cp, -self.sp * self.cy)

    def to_cam(self, p):
        dx = p[0] - self.pos[0]
        dy = p[1] - self.pos[1]
        dz = p[2] - self.pos[2]
        x1 = dx * self.cy - dz * self.sy
        z1 = dx * self.sy + dz * self.cy
        return (x1, dy * self.cp - z1 * self.sp, dy * self.sp + z1 * self.cp)

    def project(self, c):
        return (W * 0.5 + self.f * c[0] / c[2], H * 0.5 - self.f * c[1] / c[2])


BASE_F = (W / 2) / math.tan(math.radians(BASE_FOV) / 2)


class Sounds:
    def __init__(self):
        self.sounds = {}
        try:
            init = pygame.mixer.get_init()
            if not init:
                return
            self.freq, _, self.channels = init
        except pygame.error:
            return
        rnd = random.Random(1)
        tau = 2 * math.pi

        def noise():
            return rnd.uniform(-1, 1)

        self.sounds["shot"] = self.make(0.2, lambda t: noise() * math.exp(-t * 26)
                                        + 0.9 * math.sin(tau * 85 * t) * math.exp(-t * 18), 0.4)
        self.sounds["hit"] = self.make(0.25, lambda t: math.sin(tau * 1320 * t) * math.exp(-t * 14), 0.3)
        self.sounds["bull"] = self.make(0.45, lambda t: 0.5 * math.exp(-t * 7) * (
            math.sin(tau * 1760 * t) + (math.sin(tau * 2640 * t) if t > 0.09 else 0)), 0.38)
        self.sounds["reload"] = self.make(0.5, lambda t: sum(
            noise() * math.exp(-(t - c) * 90) for c in (0.03, 0.38) if t > c), 0.35)
        self.sounds["empty"] = self.make(0.06, lambda t: noise() * math.exp(-t * 120), 0.3)
        self.sounds["buy"] = self.make(0.36, lambda t: math.sin(tau * (660, 880, 1320, 1320)[min(3, int(t / 0.09))] * t)
                                       * math.exp(-(t % 0.09) * 12), 0.3)
        self.sounds["boom"] = self.make(0.6, lambda t: (noise() * 0.8 + math.sin(tau * 55 * t)) * math.exp(-t * 6), 0.45)
        self.sounds["gold"] = self.make(0.5, lambda t: math.sin(tau * (600 + 1400 * t) * t) * math.exp(-t * 3), 0.25)
        self.sounds["deny"] = self.make(0.18, lambda t: math.sin(tau * 160 * t) * math.exp(-t * 10), 0.3)
        self.sounds["click"] = self.make(0.05, lambda t: math.sin(tau * 900 * t) * math.exp(-t * 60), 0.25)

    def make(self, dur, fn, vol):
        buf = array.array("h")
        for i in range(int(self.freq * dur)):
            s = int(max(-1.0, min(1.0, fn(i / self.freq))) * vol * 32767)
            for _ in range(self.channels):
                buf.append(s)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def play(self, name):
        snd = self.sounds.get(name)
        if snd:
            snd.play()


UPGRADES = [
    ("fire_rate", 5, 60, (255, 120, 70)),
    ("mag", 5, 50, (240, 190, 70)),
    ("reload", 5, 50, (90, 200, 255)),
    ("accuracy", 5, 70, (120, 230, 140)),
    ("mult", 6, 120, (255, 210, 60)),
    ("speed", 4, 60, (110, 170, 255)),
    ("zoom", 3, 80, (170, 140, 255)),
    ("auto", 1, 250, (255, 110, 150)),
    ("explosive", 3, 400, (255, 140, 40)),
    ("targets", 4, 150, (240, 80, 80)),
]
ZOOM_FOVS = (50.0, 38.0, 28.0, 20.0)
EXPLOSIVE_R = (0.0, 1.8, 2.8, 3.8)


def upgrade_price(base, lvl):
    return int(base * 1.7 ** lvl)


def stat_text(key, lvl, lang):
    s = T[lang]
    if key == "fire_rate":
        return s["st_fire_rate"].format(1 / (0.30 * 0.82 ** lvl))
    if key == "mag":
        return s["st_mag"].format(8 + 4 * lvl)
    if key == "reload":
        return s["st_reload"].format(1.5 * 0.8 ** lvl)
    if key == "accuracy":
        return s["st_accuracy"].format(round(100 * 0.7 ** lvl))
    if key == "mult":
        return "x%.2f" % (1 + 0.25 * lvl)
    if key == "speed":
        return s["st_speed"].format(6 + 0.9 * lvl)
    if key == "zoom":
        return s["st_zoom"].format(BASE_FOV / ZOOM_FOVS[lvl])
    if key == "auto":
        return s["st_yes"] if lvl else s["st_no"]
    if key == "explosive":
        return s["st_explosive"].format(EXPLOSIVE_R[lvl]) if lvl else s["st_no"]
    if key == "targets":
        return s["st_targets"].format(8 + 2 * lvl)
    return ""


ACTIONS = ("forward", "back", "left", "right", "sprint", "jump", "shoot", "aim", "reload", "shop", "camera")
DEFAULT_BINDINGS = {
    "forward": "k:%d" % pygame.K_w,
    "back": "k:%d" % pygame.K_s,
    "left": "k:%d" % pygame.K_a,
    "right": "k:%d" % pygame.K_d,
    "sprint": "k:%d" % pygame.K_LSHIFT,
    "jump": "k:%d" % pygame.K_SPACE,
    "shoot": "m:1",
    "aim": "m:3",
    "reload": "k:%d" % pygame.K_r,
    "shop": "k:%d" % pygame.K_b,
    "camera": "k:%d" % pygame.K_v,
}
MOUSE_INDEX = {1: 0, 2: 1, 3: 2, 6: 3, 7: 4}
SENS_MIN, SENS_MAX = 0.25, 3.0


def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def write_json(path, data):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
        return True
    except OSError:
        return False


def new_slot_data(name):
    now = time.time()
    return {"name": name, "created": now, "updated": now, "play_time": 0.0, "points": 0, "upgrades": {},
            "best_combo": 0, "hits": 0, "shots": 0, "bullseyes": 0}


def normalize_slot(data):
    for key, value in new_slot_data("").items():
        data.setdefault(key, value)
    return data


def slot_path(slot_id):
    return os.path.join(SAVE_DIR, "slot_%d.json" % slot_id)


def list_slots():
    slots = []
    try:
        names = os.listdir(SAVE_DIR)
    except OSError:
        return slots
    for name in names:
        if not (name.startswith("slot_") and name.endswith(".json")):
            continue
        try:
            slot_id = int(name[5:-5])
        except ValueError:
            continue
        data = read_json(os.path.join(SAVE_DIR, name))
        if isinstance(data, dict):
            data = normalize_slot(data)
            data["id"] = slot_id
            slots.append(data)
    slots.sort(key=lambda s: s["updated"], reverse=True)
    return slots


def load_settings():
    data = read_json(SETTINGS_PATH)
    if not isinstance(data, dict):
        data = {}
    if data.get("lang") not in T:
        data["lang"] = "ru"
    binds = dict(DEFAULT_BINDINGS)
    for key, value in (data.get("bindings") or {}).items():
        if key in binds and isinstance(value, str) and value[:2] in ("k:", "m:"):
            binds[key] = value
    data["bindings"] = binds
    try:
        data["sensitivity"] = max(SENS_MIN, min(SENS_MAX, float(data.get("sensitivity", 1.0))))
    except (TypeError, ValueError):
        data["sensitivity"] = 1.0
    data["invert_y"] = bool(data.get("invert_y", False))
    if data.get("camera_mode") not in ("third", "first"):
        data["camera_mode"] = "third"
    data.setdefault("last_slot", None)
    return data


def migrate_old_save(settings):
    if not os.path.exists(OLD_SAVE_PATH) or list_slots():
        return
    old = read_json(OLD_SAVE_PATH)
    if not isinstance(old, dict):
        return
    if old.get("lang") in T:
        settings["lang"] = old["lang"]
    data = new_slot_data(T[settings["lang"]]["default_name"].format(1))
    for key in ("points", "upgrades", "best_combo", "hits", "shots", "bullseyes"):
        if key in old:
            data[key] = old[key]
    if write_json(slot_path(1), data):
        settings["last_slot"] = 1
        try:
            os.replace(OLD_SAVE_PATH, os.path.join(BASE_DIR, "save_old.json"))
        except OSError:
            pass


class Target:
    COLORS = {
        "static": ((245, 245, 245), (214, 48, 49), (245, 245, 245), (214, 48, 49), (255, 214, 64)),
        "moving": ((245, 245, 245), (41, 128, 255), (245, 245, 245), (41, 128, 255), (255, 214, 64)),
        "flying": ((255, 244, 228), (255, 128, 0), (255, 244, 228), (255, 128, 0), (40, 40, 40)),
        "gold": ((255, 200, 0), (255, 245, 160), (255, 200, 0), (255, 250, 210), (255, 120, 0)),
    }
    INFO = {"static": (0.6, 10), "moving": (0.55, 20), "flying": (0.5, 35), "gold": (0.42, 150)}
    RADAR = {"static": (240, 70, 70), "moving": (70, 150, 255), "flying": (255, 150, 30), "gold": (255, 225, 0)}

    def __init__(self, kind, pos):
        self.kind = kind
        self.radius, self.points = Target.INFO[kind]
        self.place(pos)

    def place(self, pos):
        self.base = pos
        self.pos = pos
        self.state = "alive"
        self.timer = 0.0
        self.spawn_t = 0.0
        self.t = random.uniform(0, 10)
        a = random.uniform(0, 2 * math.pi)
        self.axis = (math.cos(a), 0.0, math.sin(a))
        self.amp = random.uniform(2.5, 5.0)
        self.speed = random.uniform(0.8, 1.6)
        self.life = 8.0
        a = random.uniform(0, 2 * math.pi)
        self.vel = (math.cos(a) * 8, 0.0, math.sin(a) * 8)

    def update(self, dt):
        self.t += dt
        self.spawn_t += dt
        if self.state == "dying":
            self.timer -= dt
            if self.timer <= 0:
                self.state = "dead"
                self.timer = 1.2
            return
        if self.state == "dead":
            self.timer -= dt
            return
        if self.kind == "moving":
            s = math.sin(self.t * self.speed) * self.amp
            self.pos = (self.base[0] + self.axis[0] * s, self.base[1], self.base[2] + self.axis[2] * s)
        elif self.kind == "flying":
            a = self.t * self.speed * 0.6
            self.pos = (self.base[0] + math.cos(a) * self.amp,
                        self.base[1] + math.sin(self.t * 1.3) * 0.8,
                        self.base[2] + math.sin(a) * self.amp)
        elif self.kind == "gold":
            x = self.pos[0] + self.vel[0] * dt
            z = self.pos[2] + self.vel[2] * dt
            vx, vz = self.vel[0], self.vel[2]
            if abs(x) > ARENA - 4:
                vx = -vx
            if abs(z) > ARENA - 4:
                vz = -vz
            if random.random() < dt * 0.8:
                a = random.uniform(0, 2 * math.pi)
                vx, vz = math.cos(a) * 8, math.sin(a) * 8
            self.vel = (vx, 0.0, vz)
            self.pos = (x, 2.6 + math.sin(self.t * 2.2) * 1.2, z)
            self.life -= dt
            if self.life <= 0:
                self.state = "dead"
                self.timer = 0.0


class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        self.clock = pygame.time.Clock()
        self.load_fonts()
        self.sfx = Sounds()
        self.cam = Camera()
        self.settings = load_settings()
        migrate_old_save(self.settings)
        self.write_settings()
        self.slot_id = None
        self.save = new_slot_data("")
        self.slots = []
        self.refresh_slots()
        pygame.display.set_caption(self.t("caption"))

        self.build_visuals()
        self.build_world()
        self.build_scenery()

        self.targets = []
        self.reset_session()

        self.state = "menu"
        self.time = 0.0
        self.skip_motion = 0
        self.buttons = []
        self.shop_rects = []
        self.items = []
        self.settings_return = "menu"
        self.rebinding = None
        self.dragging_slider = False
        self.slider_rect = pygame.Rect(0, 0, 0, 0)
        self.confirm_delete = None
        self.name_input = ""
        self.autosave_timer = 30.0

    def reset_session(self):
        self.ppos = (0.0, 0.0, -6.0)
        self.vy = 0.0
        self.on_ground = True
        self.yaw = 0.0
        self.pitch = -0.05
        self.walk_phase = 0.0
        self.moving = False
        self.aim_t = 0.0
        self.cam_dist = 4.4

        self.ammo = self.mag_size
        self.cooldown = 0.0
        self.reloading = False
        self.reload_timer = 0.0
        self.recoil = 0.0
        self.combo = 0
        self.combo_timer = 0.0
        self.hit_marker = 0.0
        self.hit_marker_bull = False
        self.muzzle_flash = 0.0
        self.kick = 0.0
        self.session_hits = 0
        self.session_shots = 0
        self.shown_points = float(self.save["points"])

        self.targets = []
        self.sync_targets()
        self.gold_timer = random.uniform(18, 28)
        self.particles = []
        self.tracers = []
        self.texts = []
        self.shockwaves = []
        self.message = None

    @property
    def lang(self):
        return self.settings["lang"]

    def t(self, key, *args):
        s = T[self.lang].get(key, key)
        return s.format(*args) if args else s

    def toggle_language(self):
        self.settings["lang"] = "en" if self.lang == "ru" else "ru"
        pygame.display.set_caption(self.t("caption"))
        self.sfx.play("click")
        self.write_settings()

    def is_down(self, action, keys, mouse):
        kind, code = self.settings["bindings"][action].split(":")
        code = int(code)
        if kind == "k":
            return bool(keys[code])
        idx = MOUSE_INDEX.get(code)
        return idx is not None and idx < len(mouse) and bool(mouse[idx])

    def event_is(self, e, action):
        kind, code = self.settings["bindings"][action].split(":")
        if kind == "k":
            return e.type == pygame.KEYDOWN and e.key == int(code)
        return e.type == pygame.MOUSEBUTTONDOWN and e.button == int(code)

    def binding_label(self, binding):
        kind, code = binding.split(":")
        code = int(code)
        if kind == "m":
            names = {1: self.t("lmb"), 2: self.t("mmb"), 3: self.t("rmb")}
            return names.get(code, self.t("mouse_n", code - 2 if code >= 6 else code))
        if code == pygame.K_SPACE:
            return self.t("space")
        name = pygame.key.name(code) or "?"
        return name.upper() if len(name) == 1 else name.title()

    def key_label(self, action):
        return self.binding_label(self.settings["bindings"][action])

    def assign_binding(self, binding):
        binds = self.settings["bindings"]
        old = binds[self.rebinding]
        for action, value in binds.items():
            if value == binding and action != self.rebinding:
                binds[action] = old
        binds[self.rebinding] = binding
        self.rebinding = None
        self.sfx.play("click")
        self.write_settings()

    def write_settings(self):
        write_json(SETTINGS_PATH, self.settings)

    def refresh_slots(self):
        self.slots = list_slots()

    def continue_slot(self):
        for slot in self.slots:
            if slot["id"] == self.settings.get("last_slot"):
                return slot
        return self.slots[0] if self.slots else None

    def enter_slot(self, slot_id):
        data = read_json(slot_path(slot_id))
        if not isinstance(data, dict):
            self.refresh_slots()
            self.sfx.play("deny")
            return
        self.save = normalize_slot(data)
        self.slot_id = slot_id
        self.settings["last_slot"] = slot_id
        self.write_settings()
        self.reset_session()
        self.sfx.play("click")
        self.set_state("play")
        self.update_camera()

    def create_slot(self):
        if len(self.slots) >= MAX_SLOTS:
            self.sfx.play("deny")
            return
        slot_id = max([s["id"] for s in self.slots] + [0]) + 1
        name = self.name_input.strip() or self.t("default_name", slot_id)
        write_json(slot_path(slot_id), new_slot_data(name))
        self.refresh_slots()
        self.enter_slot(slot_id)

    def delete_slot(self, slot_id):
        try:
            os.remove(slot_path(slot_id))
        except OSError:
            pass
        if self.settings.get("last_slot") == slot_id:
            self.settings["last_slot"] = None
            self.write_settings()
        if self.slot_id == slot_id:
            self.slot_id = None
            self.save = new_slot_data("")
        self.confirm_delete = None
        self.refresh_slots()
        self.sfx.play("boom")

    def lvl(self, key):
        return self.save["upgrades"].get(key, 0)

    @property
    def fire_cd(self):
        return 0.30 * 0.82 ** self.lvl("fire_rate")

    @property
    def mag_size(self):
        return 8 + 4 * self.lvl("mag")

    @property
    def reload_time(self):
        return 1.5 * 0.8 ** self.lvl("reload")

    @property
    def base_spread(self):
        return 0.028 * 0.7 ** self.lvl("accuracy")

    @property
    def point_mult(self):
        return 1 + 0.25 * self.lvl("mult")

    @property
    def move_speed(self):
        return 6 + 0.9 * self.lvl("speed")

    @property
    def jump_speed(self):
        return 7.5 + 0.6 * self.lvl("speed")

    @property
    def zoom_fov(self):
        return ZOOM_FOVS[self.lvl("zoom")]

    @property
    def explosive_r(self):
        return EXPLOSIVE_R[self.lvl("explosive")]

    @property
    def target_count(self):
        return 8 + 2 * self.lvl("targets")

    def current_spread(self):
        s = self.base_spread
        if self.moving:
            s *= 1.8
        if not self.on_ground:
            s *= 2.5
        s *= lerp(1.0, 0.35, self.aim_t)
        return s + self.recoil

    def write_save(self):
        if self.slot_id is None:
            return
        self.save["updated"] = time.time()
        write_json(slot_path(self.slot_id), self.save)

    def load_fonts(self):
        din = pygame.font.match_font("dinalternate")

        def display(size):
            if din:
                return pygame.font.Font(din, size)
            return pygame.font.SysFont("arial", size, bold=True)

        body = "avenirnext,helveticaneue,arial"
        self.f_title = display(104)
        self.f_huge = display(60)
        self.f_big = display(42)
        self.f_num = display(30)
        self.f_numsm = display(22)
        self.f_mid = pygame.font.SysFont(body, 23, bold=True)
        self.f_text = pygame.font.SysFont(body, 18)
        self.f_small = pygame.font.SysFont(body, 15)
        self.f_label = pygame.font.SysFont(body, 13, bold=True)

    def build_visuals(self):
        g = H * 2
        self.sky = pygame.Surface((W, g))
        for y in range(g):
            k = (y / g) ** 2.4
            self.sky.fill(lerp_color(SKY_TOP, SKY_HORIZON, k), (0, y, W, 1))

        self.sun_glow = radial_glow(220, (255, 214, 150), 2.6)
        self.gold_glow = radial_glow(64, (255, 190, 40), 1.6)
        self.flash_glow = radial_glow(48, (255, 170, 60), 1.4)

        small = pygame.Surface((64, 36), pygame.SRCALPHA)
        for y in range(36):
            for x in range(64):
                dx = (x + 0.5) / 32 - 1
                dy = (y + 0.5) / 18 - 1
                d = math.sqrt(dx * dx * 0.8 + dy * dy)
                small.set_at((x, y), (0, 0, 10, int(max(0.0, min(1.0, (d - 0.55) / 0.75)) ** 1.6 * 150)))
        self.vignette = pygame.transform.smoothscale(small, (W, H))

        self.menu_shade = pygame.Surface((W, H), pygame.SRCALPHA)
        for x in range(W):
            a = int(215 * max(0.0, 1 - x / (W * 0.72)) ** 1.3)
            self.menu_shade.fill((8, 14, 30, a), (x, 0, 1, H))

        self.shadow_layer = pygame.Surface((W, H), pygame.SRCALPHA)

        rng = random.Random(11)
        self.clouds = []
        for i in range(16):
            surf = self.make_cloud(rng)
            az = rng.uniform(0, 2 * math.pi)
            el = rng.uniform(0.07, 0.42)
            self.clouds.append([az, el, surf, {}])
        self.radar_bg = self.build_radar()

    def make_cloud(self, rng):
        w = rng.randint(150, 280)
        h = int(w * 0.4)
        big = 4
        surf = pygame.Surface((w * big, h * big), pygame.SRCALPHA)
        blobs = []
        for i in range(rng.randint(6, 10)):
            ew = rng.uniform(0.2, 0.42) * w
            eh = rng.uniform(0.45, 0.85) * h
            cx = w * (0.18 + 0.64 * i / 9) + rng.uniform(-8, 8)
            cx = max(ew / 2 + 3, min(w - ew / 2 - 3, cx))
            cy = h - eh / 2 - 3 - rng.uniform(0, h * 0.25) * (1 - abs(cx / w - 0.5) * 2)
            blobs.append(pygame.Rect(int((cx - ew / 2) * big), int((cy - eh / 2) * big), int(ew * big), int(eh * big)))
        for r in blobs:
            pygame.draw.ellipse(surf, (214, 224, 238, 255), r)
        for r in blobs:
            pygame.draw.ellipse(surf, (255, 255, 255, 255), r.inflate(-r.w * 0.12, -r.h * 0.3).move(0, -r.h * 0.12))
        out = pygame.transform.smoothscale(surf, (w, h))
        out = pygame.transform.smoothscale(pygame.transform.smoothscale(out, (w // 2, h // 2)), (w, h))
        out.set_alpha(200)
        return out

    def build_radar(self):
        surf = pygame.Surface((176, 176), pygame.SRCALPHA)
        pygame.draw.circle(surf, (10, 18, 32, 165), (88, 88), 86)
        pygame.draw.circle(surf, (255, 255, 255, 30), (88, 88), 58, 1)
        pygame.draw.circle(surf, (255, 255, 255, 30), (88, 88), 29, 1)
        pygame.draw.circle(surf, (255, 255, 255, 110), (88, 88), 86, 2)
        return surf

    def build_world(self):
        rng = random.Random(42)
        self.boxes = []
        self.static_faces = []
        self.shadow_polys = []

        def add_face(verts, normal, color, style=None, bias=0.0):
            n = len(verts)
            center = (sum(p[0] for p in verts) / n, sum(p[1] for p in verts) / n, sum(p[2] for p in verts) / n)
            radius = max(v_len(v_sub(p, center)) for p in verts)
            self.static_faces.append((verts, normal, color, center, style, bias, radius))

        def add_box(cx, cy, cz, hx, hy, hz, color, top=None, style=None, solid=True):
            b = (cx - hx, cy - hy, cz - hz, cx + hx, cy + hy, cz + hz)
            if solid:
                self.boxes.append(b)
            self.add_shadow_box(b)
            for verts, n, col in box_faces((cx, cy, cz), (hx, hy, hz), color, top=top):
                add_face(verts, n, col, style)

        for s in range(-10, 10):
            u0, u1 = s * 4.0, s * 4.0 + 4.0
            col = (172, 176, 186) if s % 2 == 0 else (160, 165, 176)
            for fixed, sign, axis in ((ARENA, -1, "z"), (-ARENA, 1, "z"), (ARENA, -1, "x"), (-ARENA, 1, "x")):
                outer = fixed - sign * 1.0
                inset = fixed + sign * 0.01
                if axis == "z":
                    face = [(u0, 0, fixed), (u1, 0, fixed), (u1, WALL_H, fixed), (u0, WALL_H, fixed)]
                    band = [(u0, 0, inset), (u1, 0, inset), (u1, 0.55, inset), (u0, 0.55, inset)]
                    stripe = [(u0, 2.75, inset), (u1, 2.75, inset), (u1, 2.9, inset), (u0, 2.9, inset)]
                    top = [(u0, WALL_H, fixed), (u1, WALL_H, fixed), (u1, WALL_H, outer), (u0, WALL_H, outer)]
                    n = (0, 0, sign)
                else:
                    face = [(fixed, 0, u0), (fixed, 0, u1), (fixed, WALL_H, u1), (fixed, WALL_H, u0)]
                    band = [(inset, 0, u0), (inset, 0, u1), (inset, 0.55, u1), (inset, 0.55, u0)]
                    stripe = [(inset, 2.75, u0), (inset, 2.75, u1), (inset, 2.9, u1), (inset, 2.9, u0)]
                    top = [(fixed, WALL_H, u0), (fixed, WALL_H, u1), (outer, WALL_H, u1), (outer, WALL_H, u0)]
                    n = (sign, 0, 0)
                add_face(face, n, col)
                add_face(band, n, (92, 98, 112), bias=0.05)
                add_face(stripe, n, (230, 170, 40) if s % 2 == 0 else (40, 44, 52), bias=0.05)
                add_face(top, (0, 1, 0), (196, 200, 208))
                if s % 2 == 0:
                    if axis == "z":
                        bx, bz, hx, hz = u0, fixed + sign * 0.2, 0.3, 0.2
                    else:
                        bx, bz, hx, hz = fixed + sign * 0.2, u0, 0.2, 0.3
                    add_box(bx, WALL_H / 2 + 0.1, bz, hx, WALL_H / 2 + 0.1, hz, (140, 146, 158),
                            top=(200, 204, 212), solid=False)
        a, h = ARENA, WALL_H
        walls = [(-a - 1, 0, a, a + 1, h, a + 1), (-a - 1, 0, -a - 1, a + 1, h, -a),
                 (a, 0, -a - 1, a + 1, h, a + 1), (-a - 1, 0, -a - 1, -a, h, a + 1)]
        self.boxes += walls
        for b in walls:
            self.add_shadow_box(b)

        placed = []
        for x, z in ((18, 18), (-18, 18), (18, -18), (-18, -18)):
            add_box(x, 3.0, z, 0.9, 3.0, 0.9, (204, 178, 136), top=(226, 204, 166))
            add_box(x, 0.25, z, 1.15, 0.25, 1.15, (150, 132, 104), top=(176, 158, 128), solid=False)
            add_box(x, 6.1, z, 1.1, 0.12, 1.1, (176, 154, 118), top=(220, 200, 160), solid=False)
            placed.append((x, z, 1.2))
        for x, z, hx, hz in ((0, 22, 4.0, 1.4), (-24, 0, 1.4, 4.0), (24, 4, 1.4, 4.0)):
            add_box(x, 0.45, z, hx, 0.45, hz, (106, 114, 130), top=(146, 154, 168))
            add_face([(x - hx + 0.25, 0.91, z - hz + 0.25), (x + hx - 0.25, 0.91, z - hz + 0.25),
                      (x + hx - 0.25, 0.91, z + hz - 0.25), (x - hx + 0.25, 0.91, z + hz - 0.25)],
                     (0, 1, 0), (122, 130, 146), bias=0.05)
            placed.append((x, z, max(hx, hz)))
        for _ in range(26):
            for _ in range(40):
                x = rng.uniform(-34, 34)
                z = rng.uniform(-34, 34)
                s = rng.choice((0.6, 0.8, 1.0))
                if math.hypot(x, z) < 9:
                    continue
                if any(abs(x - px) < s + ps + 1.6 and abs(z - pz) < s + ps + 1.6 for px, pz, ps in placed):
                    continue
                placed.append((x, z, s))
                wood = (rng.randint(176, 200), rng.randint(122, 140), rng.randint(64, 80))
                add_box(x, s, z, s, s, s, wood, top=scale_color(wood, 1.12), style="crate")
                if rng.random() < 0.35:
                    s2 = s * 0.65
                    add_box(x + rng.uniform(-0.15, 0.15), 2 * s + s2, z + rng.uniform(-0.15, 0.15),
                            s2, s2, s2, scale_color(wood, 0.92), top=scale_color(wood, 1.05), style="crate")
                break

        self.tiles = []
        step = 4.0
        n = int(ARENA * 2 / step)
        for i in range(n):
            for j in range(n):
                x0 = -ARENA + i * step
                z0 = -ARENA + j * step
                col = TILE_A if (i + j) % 2 == 0 else TILE_B
                self.tiles.append(([(x0, 0, z0), (x0 + step, 0, z0), (x0 + step, 0, z0 + step), (x0, 0, z0 + step)],
                                   col, (x0 + step / 2, 0, z0 + step / 2)))

    def add_shadow_box(self, b):
        sx = -LIGHT[0] / LIGHT[1]
        sz = -LIGHT[2] / LIGHT[1]
        pts = []
        for x in (b[0], b[3]):
            for z in (b[2], b[5]):
                pts.append((x + sx * b[1], z + sz * b[1]))
                pts.append((x + sx * b[4], z + sz * b[4]))
        hull = convex_hull(pts)
        poly = [(x, 0.0, z) for x, z in hull]
        center = (sum(p[0] for p in poly) / len(poly), 0.0, sum(p[2] for p in poly) / len(poly))
        reach = max(math.hypot(p[0] - center[0], p[2] - center[2]) for p in poly)
        self.shadow_polys.append((poly, center, reach))

    def build_scenery(self):
        rng = random.Random(3)
        self.mountains = []
        layers = (((172, 190, 212), 0.13, 3, (236, 242, 250)),
                  ((134, 158, 180), 0.08, 5, None),
                  ((84, 122, 96), 0.035, 11, None))
        for li, (col, base_h, freq, snow) in enumerate(layers):
            p = [rng.uniform(0, 6.28) for _ in range(4)]
            ridge = []
            n = 96
            for i in range(n + 1):
                a = i / n * 2 * math.pi
                h = base_h * (0.55 + 0.25 * math.sin(a * freq + p[0]) + 0.15 * math.sin(a * freq * 2.3 + p[1])
                              + 0.08 * math.sin(a * freq * 4.7 + p[2]) + 0.05 * math.sin(a * 29 + p[3]))
                ridge.append((math.sin(a), max(0.005, h), math.cos(a)))
            self.mountains.append((col, ridge, snow, base_h))

        self.trees = []
        for _ in range(70):
            a = rng.uniform(0, 2 * math.pi)
            r = rng.uniform(47, 80)
            s = rng.uniform(0.8, 1.5)
            dark = (rng.randint(36, 50), rng.randint(84, 104), rng.randint(52, 64))
            self.trees.append(((math.sin(a) * r, 0.0, math.cos(a) * r), s, dark))

    def box_at(self, pos):
        px, py, pz = pos
        for b in self.boxes:
            if (px + PLAYER_R > b[0] and px - PLAYER_R < b[3] and pz + PLAYER_R > b[2]
                    and pz - PLAYER_R < b[5] and py + PLAYER_H > b[1] and py < b[4]):
                return b
        return None

    def support_height(self, pos):
        best = 0.0
        for b in self.boxes:
            if b[0] < pos[0] < b[3] and b[2] < pos[2] < b[5] and b[4] <= pos[1] + 0.05:
                best = max(best, b[4])
        return best

    def spawn_pos(self, kind):
        for _ in range(60):
            x = random.uniform(-ARENA + 5, ARENA - 5)
            z = random.uniform(-ARENA + 5, ARENA - 5)
            if math.hypot(x - self.ppos[0], z - self.ppos[2]) < 9:
                continue
            if kind == "flying":
                y = random.uniform(4.0, 6.5)
            else:
                y = random.uniform(1.3, 2.3)
            m = 1.3 if kind != "moving" else 2.0
            if any(b[0] - m < x < b[3] + m and b[2] - m < z < b[5] + m for b in self.boxes):
                continue
            if any(math.hypot(x - t.base[0], z - t.base[2]) < 2.5 for t in self.targets):
                continue
            return (x, y, z)
        return (random.uniform(-20, 20), 5.0, random.uniform(-20, 20))

    def sync_targets(self):
        kinds = ("static", "moving", "static", "flying", "moving", "static")
        normal = [t for t in self.targets if t.kind != "gold"]
        while len(normal) < self.target_count:
            kind = kinds[len(normal) % len(kinds)]
            t = Target(kind, self.spawn_pos(kind))
            if kind == "moving":
                t.amp = random.uniform(1.5, 3.0)
            self.targets.append(t)
            normal.append(t)

    def burst(self, pos, colors, count, speed, life=0.7, size=0.08):
        for _ in range(count):
            d = v_norm((random.uniform(-1, 1), random.uniform(-0.3, 1.2), random.uniform(-1, 1)))
            v = v_mul(d, random.uniform(0.3, 1.0) * speed)
            self.particles.append([pos, v, random.uniform(0.5, 1.0) * life, random.choice(colors), size])

    def float_text(self, pos, text, color, size="mid"):
        self.texts.append([pos, text, color, 1.1, size])

    def show_message(self, text, color=(255, 255, 255), dur=1.6):
        self.message = [text, color, dur, dur]

    @property
    def first_person(self):
        return self.settings["camera_mode"] == "first"

    def gun_pose(self):
        pivot = v_add(self.ppos, (0.0, 1.35, 0.0))
        return pivot, self.yaw, self.pitch

    def viewmodel_offset(self):
        bob_x = bob_y = 0.0
        if self.moving and self.on_ground:
            k = 1 - self.aim_t * 0.8
            bob_x = math.sin(self.walk_phase) * 0.014 * k
            bob_y = abs(math.cos(self.walk_phase)) * 0.012 * k
        gx = lerp(0.25, 0.0, self.aim_t) + bob_x
        gy = lerp(-0.25, -0.128, self.aim_t) + bob_y + self.kick * 0.3
        gz = lerp(0.82, 0.74, self.aim_t) - self.kick * 1.4
        return gx, gy, gz

    def muzzle_pos(self):
        if self.first_person:
            gx, gy, gz = self.viewmodel_offset()
            return v_add(self.cam.pos, rotate((gx, gy + 0.015, gz + 0.45), self.cam.yaw, self.cam.pitch))
        pivot, yaw, pitch = self.gun_pose()
        return v_add(pivot, rotate((0.28, 0.06, 1.08), yaw, pitch))

    def toggle_camera(self):
        self.set_camera_mode("third" if self.first_person else "first")
        self.show_message(self.t("cam_first") if self.first_person else self.t("cam_third"), (220, 236, 255), 1.0)

    def set_camera_mode(self, mode):
        self.settings["camera_mode"] = mode
        self.sfx.play("click")
        self.write_settings()

    def raycast(self, o, d, maxd=250.0):
        best_t = maxd
        best = ("none", None, 0.0)
        if d[1] < -1e-6:
            t = -o[1] / d[1]
            if 0 < t < best_t:
                best_t, best = t, ("ground", None, 0.0)
        for b in self.boxes:
            t = ray_aabb(o, d, b)
            if t is not None and t < best_t:
                best_t, best = t, ("box", b, 0.0)
        for tg in self.targets:
            if tg.state != "alive":
                continue
            oc = v_sub(tg.pos, o)
            tca = v_dot(oc, d)
            if tca < 0:
                continue
            d2 = v_dot(oc, oc) - tca * tca
            r2 = tg.radius * tg.radius
            if d2 > r2:
                continue
            t = tca - math.sqrt(r2 - d2)
            if t < best_t:
                best_t, best = t, ("target", tg, math.sqrt(max(0.0, d2)) / tg.radius)
        return best_t, best

    def start_reload(self):
        if self.reloading or self.ammo >= self.mag_size:
            return
        self.reloading = True
        self.reload_timer = self.reload_time
        self.sfx.play("reload")

    def shoot(self):
        if self.reloading or self.cooldown > 0:
            return
        if self.ammo <= 0:
            self.sfx.play("empty")
            self.start_reload()
            return
        self.ammo -= 1
        self.cooldown = self.fire_cd
        self.save["shots"] += 1
        self.session_shots += 1
        self.sfx.play("shot")

        cam = self.cam
        spread = self.current_spread()
        ang = random.uniform(0, 2 * math.pi)
        r = spread * math.sqrt(random.random())
        d = v_norm(v_add(cam.forward, v_add(v_mul(cam.right, math.cos(ang) * r), v_mul(cam.up, math.sin(ang) * r))))
        t, (kind, obj, ring) = self.raycast(cam.pos, d)
        point = v_add(cam.pos, v_mul(d, t))

        self.tracers.append([self.muzzle_pos(), point, 0.08])
        self.muzzle_flash = 0.05
        self.kick = 0.05
        self.recoil = min(0.06, self.recoil + 0.012)
        self.pitch = min(0.95, self.pitch + lerp(0.012, 0.005, self.aim_t))

        hit_any = False
        if kind == "target":
            self.hit_target(obj, ring)
            hit_any = True
        elif kind == "ground":
            self.burst(point, ((140, 118, 84), (96, 132, 74), (170, 150, 110)), 9, 3.0, 0.5, 0.06)
        elif kind == "box":
            self.burst(point, ((206, 166, 104), (130, 96, 56), (255, 230, 170)), 9, 3.0, 0.5, 0.06)

        if self.explosive_r > 0 and kind != "none":
            hit_any = self.explode(point, obj if kind == "target" else None) or hit_any

        if not hit_any:
            if self.combo >= 5:
                self.float_text(point, self.t("combo_lost"), (255, 120, 120), "small")
            self.combo = 0

        if self.ammo <= 0:
            self.start_reload()

    def explode(self, point, skip):
        r = self.explosive_r
        self.sfx.play("boom")
        self.burst(point, ((255, 180, 40), (255, 100, 20), (255, 230, 120), (90, 90, 90)), 28, 6.0, 0.6, 0.13)
        self.shockwaves.append([point, 0.0, r])
        hit = False
        for tg in self.targets:
            if tg is skip or tg.state != "alive":
                continue
            if v_len(v_sub(tg.pos, point)) < r + tg.radius:
                self.hit_target(tg, 1.0, explosion=True)
                hit = True
        return hit

    def hit_target(self, tg, ring_frac, explosion=False):
        ring = 4 if explosion else min(4, int(ring_frac * 5))
        dist = v_len(v_sub(tg.pos, v_add(self.ppos, (0, 1.4, 0))))
        self.combo += 1
        self.combo_timer = 4.0
        self.save["best_combo"] = max(self.save["best_combo"], self.combo)
        combo_mult = 1 + min(self.combo - 1, 20) * 0.1
        pts = int(round(tg.points * RING_MULT[ring] * combo_mult * self.point_mult * (1 + dist / 40)))
        self.save["points"] += pts
        self.save["hits"] += 1
        self.session_hits += 1

        self.float_text(tg.pos, "+%d" % pts, RING_COLORS[ring], "big" if ring == 0 else "mid")
        if tg.kind == "gold":
            self.show_message(self.t("gold_hit", pts), GOLD)
            self.sfx.play("bull")
        elif ring == 0:
            self.save["bullseyes"] += 1
            self.show_message(self.t("bullseye"), GOLD, 1.0)
            self.sfx.play("bull")
        else:
            self.sfx.play("hit")
        if dist > 35 and not explosion:
            self.float_text(v_add(tg.pos, (0, -0.6, 0)), self.t("long_shot"), (180, 230, 255), "small")

        tg.state = "dying"
        tg.timer = 0.25
        self.burst(tg.pos, Target.COLORS[tg.kind], 24, 5.0, 0.8, 0.09)
        self.hit_marker = 0.15
        self.hit_marker_bull = ring == 0

    def move_player(self, dx, dz, dt):
        x, y, z = self.ppos
        if dx and not self.box_at((x + dx, y, z)):
            x += dx
        if dz and not self.box_at((x, y, z + dz)):
            z += dz
        self.vy -= GRAVITY * dt
        ny = y + self.vy * dt
        self.on_ground = False
        if ny <= 0:
            ny = 0.0
            self.vy = 0.0
            self.on_ground = True
        else:
            b = self.box_at((x, ny, z))
            if b:
                if self.vy <= 0:
                    ny = b[4]
                    self.on_ground = True
                else:
                    ny = y
                self.vy = 0.0
        self.ppos = (x, ny, z)

    def update(self, dt):
        self.time += dt
        self.save["play_time"] += dt
        self.autosave_timer -= dt
        if self.autosave_timer <= 0:
            self.autosave_timer = 30.0
            self.write_save()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed(num_buttons=5)

        aiming = self.is_down("aim", keys, mouse)
        self.aim_t = max(0.0, min(1.0, self.aim_t + (dt if aiming else -dt) * 7))

        fx, fz = math.sin(self.yaw), math.cos(self.yaw)
        rx, rz = math.cos(self.yaw), -math.sin(self.yaw)
        mx = mz = 0.0
        if self.is_down("forward", keys, mouse):
            mx += fx
            mz += fz
        if self.is_down("back", keys, mouse):
            mx -= fx
            mz -= fz
        if self.is_down("right", keys, mouse):
            mx += rx
            mz += rz
        if self.is_down("left", keys, mouse):
            mx -= rx
            mz -= rz
        length = math.hypot(mx, mz)
        self.moving = length > 0
        speed = self.move_speed
        if self.is_down("sprint", keys, mouse) and self.aim_t < 0.5:
            speed *= 1.5
        speed *= lerp(1.0, 0.55, self.aim_t)
        if self.moving:
            mx, mz = mx / length * speed * dt, mz / length * speed * dt
            self.walk_phase += dt * speed * 1.7
        self.move_player(mx, mz, dt)

        self.cooldown = max(0.0, self.cooldown - dt)
        self.recoil = max(0.0, self.recoil - dt * 0.12)
        if self.lvl("auto") and self.is_down("shoot", keys, mouse):
            self.shoot()
        if self.reloading:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.reloading = False
                self.ammo = self.mag_size

        if self.combo > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo = 0

        self.gold_timer -= dt
        if self.gold_timer <= 0:
            self.gold_timer = random.uniform(20, 32)
            self.targets.append(Target("gold", self.spawn_pos("gold")))
            self.show_message(self.t("gold_spawn"), GOLD, 2.0)
            self.sfx.play("gold")

        for tg in self.targets:
            tg.update(dt)
            if tg.state == "dead" and tg.timer <= 0 and tg.kind != "gold":
                tg.place(self.spawn_pos(tg.kind))
        self.targets = [t for t in self.targets if not (t.kind == "gold" and t.state == "dead")]

        self.update_effects(dt)
        self.update_camera()

    def update_effects(self, dt):
        for p in self.particles:
            p[1] = (p[1][0], p[1][1] - GRAVITY * 0.5 * dt, p[1][2])
            p[0] = v_add(p[0], v_mul(p[1], dt))
            p[2] -= dt
        self.particles = [p for p in self.particles if p[2] > 0 and p[0][1] > -0.1]
        for tr in self.tracers:
            tr[2] -= dt
        self.tracers = [t for t in self.tracers if t[2] > 0]
        for tx in self.texts:
            tx[0] = v_add(tx[0], (0, dt * 1.3, 0))
            tx[3] -= dt
        self.texts = [t for t in self.texts if t[3] > 0]
        for sw in self.shockwaves:
            sw[1] += dt
        self.shockwaves = [s for s in self.shockwaves if s[1] < 0.35]
        self.hit_marker = max(0.0, self.hit_marker - dt)
        self.muzzle_flash = max(0.0, self.muzzle_flash - dt)
        self.kick = max(0.0, self.kick - dt * 0.5)
        if self.message:
            self.message[2] -= dt
            if self.message[2] <= 0:
                self.message = None
        for cloud in self.clouds:
            cloud[0] += dt * 0.004
        self.shown_points += (self.save["points"] - self.shown_points) * min(1.0, dt * 9)
        if abs(self.save["points"] - self.shown_points) < 0.5:
            self.shown_points = float(self.save["points"])

    def update_camera(self):
        cam = self.cam
        cam.yaw = self.yaw
        cam.pitch = self.pitch
        cam.fov = math.radians(lerp(BASE_FOV, self.zoom_fov, self.aim_t))
        cam.update()
        if self.first_person:
            bob = abs(math.sin(self.walk_phase)) * 0.035 if (self.moving and self.on_ground) else 0.0
            cam.pos = (self.ppos[0], self.ppos[1] + 1.62 + bob, self.ppos[2])
            self.cam_dist = 0.0
            return
        fwd, right = cam.forward, cam.right
        shoulder = lerp(0.95, 0.7, self.aim_t)
        dist = lerp(4.4, 2.2, self.aim_t)
        pivot = (self.ppos[0] + right[0] * shoulder, self.ppos[1] + 1.95, self.ppos[2] + right[2] * shoulder)
        back = v_mul(fwd, -1)
        for b in self.boxes:
            t = ray_aabb(pivot, back, b)
            if t is not None and t < dist + 0.25:
                dist = max(0.25, t - 0.25)
        if back[1] < 0 and pivot[1] + back[1] * dist < 0.3:
            dist = max(0.25, (pivot[1] - 0.3) / -back[1])
        self.cam_dist = dist
        cam.pos = v_add(pivot, v_mul(back, dist))

    def update_menu(self, dt):
        self.time += dt
        for tg in self.targets:
            tg.update(dt)
        self.update_effects(dt)
        a = self.time * 0.06 + 0.6
        cam = self.cam
        cam.pos = (math.sin(a) * 31, 8.5, math.cos(a) * 31)
        cam.yaw = a + math.pi - 0.35
        cam.pitch = -0.2
        cam.fov = math.radians(BASE_FOV)
        cam.update()

    def capture_mouse(self, on):
        pygame.event.set_grab(on)
        pygame.mouse.set_visible(not on)
        if on:
            pygame.mouse.get_rel()
            self.skip_motion = 2

    def set_state(self, state):
        if self.state == "play" and state != "play":
            self.write_save()
        if state == "newgame":
            pygame.key.start_text_input()
        elif self.state == "newgame":
            pygame.key.stop_text_input()
        if state in ("menu", "slots"):
            self.refresh_slots()
        self.state = state
        self.rebinding = None
        self.dragging_slider = False
        self.confirm_delete = None
        self.capture_mouse(state == "play")

    def click_button(self, pos):
        for rect, action in self.buttons:
            if rect.collidepoint(pos):
                self.do_action(action)
                return True
        return False

    def do_action(self, action):
        if isinstance(action, tuple):
            kind, arg = action
            if kind == "load":
                self.enter_slot(arg)
            elif kind == "delete":
                self.sfx.play("click")
                self.confirm_delete = arg
            elif kind == "confirm_delete":
                self.delete_slot(arg)
            elif kind == "camera_mode":
                self.set_camera_mode(arg)
            elif kind == "rebind":
                self.sfx.play("click")
                self.rebinding = arg
            return
        if action == "continue":
            slot = self.continue_slot()
            if slot:
                self.enter_slot(slot["id"])
        elif action == "new":
            if len(self.slots) >= MAX_SLOTS:
                self.sfx.play("deny")
                self.set_state("slots")
                return
            self.sfx.play("click")
            self.name_input = self.t("default_name", max([s["id"] for s in self.slots] + [0]) + 1)
            self.set_state("newgame")
        elif action == "create":
            self.create_slot()
        elif action == "load_menu":
            self.sfx.play("click")
            self.set_state("slots")
        elif action == "cancel_delete":
            self.sfx.play("click")
            self.confirm_delete = None
        elif action == "settings":
            self.sfx.play("click")
            self.settings_return = self.state
            self.set_state("settings")
        elif action == "back":
            self.sfx.play("click")
            self.set_state(self.settings_return if self.state == "settings" else "menu")
        elif action == "resume":
            self.sfx.play("click")
            self.set_state("play")
            self.update_camera()
        elif action == "main_menu":
            self.sfx.play("click")
            self.write_save()
            self.set_state("menu")
        elif action == "lang":
            self.toggle_language()
        elif action == "invert":
            self.settings["invert_y"] = not self.settings["invert_y"]
            self.sfx.play("click")
            self.write_settings()
        elif action == "reset_controls":
            self.settings["bindings"] = dict(DEFAULT_BINDINGS)
            self.settings["sensitivity"] = 1.0
            self.settings["invert_y"] = False
            self.settings["camera_mode"] = "third"
            self.sfx.play("buy")
            self.write_settings()
        elif action == "quit":
            self.quit()

    def set_sensitivity_from_mouse(self, x):
        r = self.slider_rect
        k = max(0.0, min(1.0, (x - r.x) / max(1, r.w)))
        self.settings["sensitivity"] = round(SENS_MIN + k * (SENS_MAX - SENS_MIN), 2)

    def handle_event(self, e):
        if e.type == pygame.QUIT:
            self.quit()
        if self.state == "menu":
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.click_button(e.pos)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.do_action("continue" if self.continue_slot() else "new")
                elif e.key == pygame.K_l:
                    self.toggle_language()
                elif e.key == pygame.K_ESCAPE:
                    self.quit()
        elif self.state == "play":
            if e.type == pygame.MOUSEMOTION:
                if self.skip_motion > 0:
                    self.skip_motion -= 1
                    return
                sens = 0.0025 * self.settings["sensitivity"] * (self.cam.fov / math.radians(BASE_FOV))
                dy = e.rel[1] if self.settings["invert_y"] else -e.rel[1]
                self.yaw += e.rel[0] * sens
                self.pitch = max(-1.1, min(0.95, self.pitch + dy * sens))
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.set_state("pause")
            elif e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if self.event_is(e, "shoot"):
                    self.shoot()
                elif self.event_is(e, "shop"):
                    self.set_state("shop")
                elif self.event_is(e, "reload"):
                    self.start_reload()
                elif self.event_is(e, "camera"):
                    self.toggle_camera()
                    self.update_camera()
                elif self.event_is(e, "jump") and self.on_ground:
                    self.vy = self.jump_speed
                    self.on_ground = False
        elif self.state == "shop":
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for rect, key in self.shop_rects:
                    if rect.collidepoint(e.pos):
                        self.buy(key)
                        return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.set_state("play")
            elif self.event_is(e, "shop"):
                self.set_state("play")
            elif e.type == pygame.KEYDOWN:
                if pygame.K_1 <= e.key <= pygame.K_9:
                    self.buy(UPGRADES[e.key - pygame.K_1][0])
                elif e.key == pygame.K_0:
                    self.buy(UPGRADES[9][0])
        elif self.state == "pause":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.do_action("resume")
                elif e.key == pygame.K_l:
                    self.toggle_language()
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.click_button(e.pos)
        elif self.state == "settings":
            if self.rebinding:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.rebinding = None
                    else:
                        self.assign_binding("k:%d" % e.key)
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button in MOUSE_INDEX:
                    self.assign_binding("m:%d" % e.button)
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.slider_rect.inflate(0, 24).collidepoint(e.pos):
                    self.dragging_slider = True
                    self.set_sensitivity_from_mouse(e.pos[0])
                else:
                    self.click_button(e.pos)
            elif e.type == pygame.MOUSEMOTION and self.dragging_slider:
                self.set_sensitivity_from_mouse(e.pos[0])
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and self.dragging_slider:
                self.dragging_slider = False
                self.write_settings()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.do_action("back")
        elif self.state == "slots":
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.click_button(e.pos)
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                if self.confirm_delete is not None:
                    self.confirm_delete = None
                else:
                    self.do_action("back")
        elif self.state == "newgame":
            if e.type == pygame.TEXTINPUT:
                if len(self.name_input) < 20:
                    self.name_input = (self.name_input + e.text)[:20]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    self.name_input = self.name_input[:-1]
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.create_slot()
                elif e.key == pygame.K_ESCAPE:
                    self.do_action("back")
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.click_button(e.pos)

    def buy(self, key):
        for k, max_lvl, base, _ in UPGRADES:
            if k != key:
                continue
            lvl = self.lvl(k)
            price = upgrade_price(base, lvl)
            if lvl >= max_lvl or self.save["points"] < price:
                self.sfx.play("deny")
                return
            self.save["points"] -= price
            self.save["upgrades"][k] = lvl + 1
            self.sfx.play("buy")
            if k == "mag":
                self.ammo = self.mag_size
                self.reloading = False
            if k == "targets":
                self.sync_targets()
            self.write_save()

    def cheapest_available(self):
        prices = [upgrade_price(base, self.lvl(k)) for k, m, base, _ in UPGRADES if self.lvl(k) < m]
        return min(prices) if prices else None

    def quit(self):
        self.write_save()
        pygame.quit()
        sys.exit()

    def add_face(self, verts, normal, color, outline=True, style=None, bias=0.0):
        cam = self.cam
        p0 = verts[0]
        cp = cam.pos
        if (cp[0] - p0[0]) * normal[0] + (cp[1] - p0[1]) * normal[1] + (cp[2] - p0[2]) * normal[2] <= 0:
            return
        cv = [cam.to_cam(p) for p in verts]
        if any(c[2] < NEAR for c in cv):
            cv = clip_near(cv)
            if len(cv) < 3:
                return
            style = None
        depth = sum(c[2] for c in cv) / len(cv)
        pts = [cam.project(c) for c in cv]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        if max(xs) < 0 or min(xs) > W or max(ys) < 0 or min(ys) > H:
            return
        if needs_screen_clip(pts):
            pts = clip_screen(pts)
            if len(pts) < 3:
                return
            style = None
        col = fog(shade(color, normal), depth)
        self.items.append((depth - bias, 0, pts, col, outline and not bias, style))

    def add_box(self, center, half, color, yaw=0.0, pitch=0.0, top=None):
        for verts, n, col in box_faces(center, half, color, yaw, pitch, top):
            self.add_face(verts, n, col)

    def draw_ground_poly(self, surf, world_pts, color, use_fog=True):
        cam = self.cam
        cv = [cam.to_cam(p) for p in world_pts]
        if all(c[2] < NEAR for c in cv):
            return None
        if any(c[2] < NEAR for c in cv):
            cv = clip_near(cv)
            if len(cv) < 3:
                return None
        pts = [cam.project(c) for c in cv]
        if needs_screen_clip(pts):
            pts = clip_screen(pts)
            if len(pts) < 3:
                return None
        if use_fog:
            depth = sum(c[2] for c in cv) / len(cv)
            color = fog(color, depth)
        return pygame.draw.polygon(surf, color, pts)

    def draw_sky(self):
        cam, scr = self.cam, self.screen
        horizon = H * 0.5 + cam.f * math.tan(cam.pitch)
        top = horizon - self.sky.get_height()
        if top > 0:
            scr.fill(SKY_TOP, (0, 0, W, int(top) + 1))
        scr.blit(self.sky, (0, int(top)))

        sun = cam.to_cam(v_add(cam.pos, v_mul(LIGHT, 1000)))
        if sun[2] > 0:
            sx, sy = cam.project(sun)
            g = self.sun_glow
            scr.blit(g, (sx - g.get_width() / 2, sy - g.get_height() / 2), special_flags=pygame.BLEND_RGB_ADD)
            pygame.draw.circle(scr, (255, 248, 225), (sx, sy), 34)
            pygame.draw.circle(scr, (255, 255, 250), (sx, sy), 26)

        zoom = cam.f / BASE_F
        zkey = round(zoom * 10)
        for az, el, surf, cache in self.clouds:
            d = (math.sin(az) * math.cos(el), math.sin(el), math.cos(az) * math.cos(el))
            c = cam.to_cam(v_add(cam.pos, v_mul(d, 1000)))
            if c[2] < 200:
                continue
            sx, sy = cam.project(c)
            img = cache.get(zkey)
            if img is None:
                if zkey == 10:
                    img = surf
                else:
                    img = pygame.transform.smoothscale(surf, (int(surf.get_width() * zkey / 10),
                                                              int(surf.get_height() * zkey / 10)))
                cache[zkey] = img
            w, h = img.get_size()
            if -w < sx < W + w and -h < sy < H + h:
                scr.blit(img, (sx - w / 2, sy - h / 2))

        half_fov = cam.fov / 2 + 0.12
        for col, ridge, snow, base_h in self.mountains:
            n = len(ridge) - 1
            for i in range(n):
                diff = (i + 0.5) / n * 2 * math.pi - cam.yaw
                if abs((diff + math.pi) % (2 * math.pi) - math.pi) > half_fov:
                    continue
                a, b = ridge[i], ridge[i + 1]
                quad = [(a[0] * 1000, a[1] * 1000, a[2] * 1000), (b[0] * 1000, b[1] * 1000, b[2] * 1000),
                        (b[0] * 1000, -80, b[2] * 1000), (a[0] * 1000, -80, a[2] * 1000)]
                cv = [cam.to_cam(v_add(cam.pos, p)) for p in quad]
                if any(c[2] < 150 for c in cv):
                    continue
                pts = [cam.project(c) for c in cv]
                if needs_screen_clip(pts):
                    pts = clip_screen(pts)
                if len(pts) >= 3:
                    pygame.draw.polygon(scr, col, pts)
                thr = base_h * 0.8
                if snow and (a[1] > thr or b[1] > thr):
                    ta = max(0.0, a[1] - thr) * 0.6
                    tb = max(0.0, b[1] - thr) * 0.6
                    snow_quad = [quad[0], quad[1], (quad[1][0], (b[1] - tb) * 1000, quad[1][2]),
                                 (quad[0][0], (a[1] - ta) * 1000, quad[0][2])]
                    pts = [cam.project(cam.to_cam(v_add(cam.pos, p))) for p in snow_quad]
                    if needs_screen_clip(pts):
                        pts = clip_screen(pts)
                    if len(pts) >= 3:
                        pygame.draw.polygon(scr, snow, pts)
        return horizon

    def draw_ground(self, horizon):
        cam, scr = self.cam, self.screen
        if horizon >= H:
            return
        gy = max(0, int(horizon))
        scr.fill(GROUND_COLOR, (0, gy, W, H - gy))
        y = gy
        while y < H:
            dy = (-(y + 0.5 - H * 0.5) / cam.f) * cam.cp + cam.sp
            depth = FOG_END if dy >= 0 else -cam.pos[1] / dy
            if depth < FOG_START:
                break
            scr.fill(fog(GROUND_COLOR, depth), (0, y, W, 1))
            y += 1

        for verts, col, c in self.tiles:
            if self.in_view(c, 2.9):
                self.draw_ground_poly(scr, verts, col)

    def in_view(self, p, radius):
        cam = self.cam
        x, y, z = cam.to_cam(p)
        if z < -radius or z > FOG_END + radius:
            return False
        kx = (W * 0.5) / cam.f
        ky = (H * 0.5) / cam.f
        reach = radius * 1.8
        return abs(x) < (z + radius) * kx + reach and abs(y) < (z + radius) * ky + reach

    def draw_shadows(self):
        layer = self.shadow_layer
        cam = self.cam
        dirty = None
        cx, cz = cam.pos[0], cam.pos[2]
        polys = []
        for poly, center, reach in self.shadow_polys:
            d = math.hypot(center[0] - cx, center[2] - cz) - reach
            if d < FOG_END:
                polys.append((poly, max(0.0, d)))
        if self.state != "menu":
            sh = self.support_height(self.ppos)
            polys.append((self.ellipse(self.ppos[0] + 0.15, sh, self.ppos[2] - 0.1, 0.55, 0.45), 0.0))
        for tg in self.targets:
            if tg.state == "dead":
                continue
            px, py, pz = tg.pos
            off = py * 0.5
            if tg.kind in ("flying", "gold"):
                polys.append((self.ellipse(px - off * 0.47, 0.0, pz + off * 0.41, tg.radius * 0.8, tg.radius * 0.6), 0.0))
            else:
                polys.append((self.ellipse(px - py * 0.47, 0.0, pz + py * 0.41, tg.radius * 0.9, 0.12), 0.0))
                polys.append((self.ellipse(px, 0.0, pz, 0.45, 0.45), 0.0))
        for poly, d in polys:
            alpha = int(85 * (1 - fog_k(d)))
            if alpha <= 4:
                continue
            r = self.draw_ground_poly(layer, poly, (0, 0, 20, alpha), use_fog=False)
            if r:
                dirty = r if dirty is None else dirty.union(r)
        if dirty:
            dirty = dirty.clip(layer.get_rect())
            self.screen.blit(layer, dirty.topleft, dirty)
            layer.fill((0, 0, 0, 0), dirty)

    @staticmethod
    def ellipse(x, y, z, rx, rz):
        return [(x + math.cos(i / 12 * 6.283) * rx, y + 0.01, z + math.sin(i / 12 * 6.283) * rz) for i in range(12)]

    def add_player(self):
        yaw = self.yaw
        swing = math.sin(self.walk_phase) * 0.22 if (self.moving and self.on_ground) else 0.0
        bob = abs(math.cos(self.walk_phase)) * 0.04 if self.moving else 0.0

        def body(local, half, color, top=None):
            self.add_box(v_add(self.ppos, rotate(local, yaw)), half, color, yaw, 0.0, top)

        pants, shirt, vest, skin = (58, 64, 82), (66, 112, 188), (52, 70, 58), (238, 196, 160)
        body((-0.14, 0.08, swing + 0.04), (0.12, 0.08, 0.17), (44, 36, 30))
        body((0.14, 0.08, -swing + 0.04), (0.12, 0.08, 0.17), (44, 36, 30))
        body((-0.14, 0.5, swing), (0.11, 0.36, 0.12), pants)
        body((0.14, 0.5, -swing), (0.11, 0.36, 0.12), pants)
        body((0.0, 0.88 + bob, 0.0), (0.29, 0.06, 0.17), (40, 36, 34))
        body((0.0, 1.18 + bob, 0.0), (0.28, 0.28, 0.16), shirt, top=(84, 132, 206))
        body((0.0, 1.16 + bob, 0.02), (0.3, 0.22, 0.18), vest)
        body((0.0, 1.22 + bob, -0.26), (0.2, 0.24, 0.09), (110, 92, 62), top=(130, 110, 76))
        body((0.0, 1.5 + bob, 0.0), (0.09, 0.05, 0.09), skin)
        body((0.0, 1.71 + bob, 0.0), (0.17, 0.17, 0.17), skin)
        body((0.0, 1.66 + bob, -0.05), (0.18, 0.13, 0.14), (70, 46, 30))
        body((0.0, 1.89 + bob, 0.0), (0.19, 0.04, 0.19), (210, 60, 45), top=(230, 80, 60))
        body((0.0, 1.87 + bob, 0.21), (0.17, 0.02, 0.1), (180, 46, 36))

        pivot, gyaw, gpitch = self.gun_pose()

        def arm(local, half, color, extra_yaw=0.0):
            self.add_box(v_add(pivot, rotate(local, gyaw, gpitch)), half, color, gyaw + extra_yaw, gpitch)

        arm((0.3, -0.02, 0.24), (0.08, 0.08, 0.26), shirt)
        arm((0.3, -0.02, 0.5), (0.07, 0.07, 0.04), (40, 40, 44))
        arm((-0.08, -0.06, 0.34), (0.07, 0.07, 0.28), shirt, 0.5)
        arm((0.28, 0.04, 0.26), (0.05, 0.09, 0.14), (96, 66, 40))
        arm((0.28, 0.06, 0.62), (0.055, 0.08, 0.26), (48, 50, 58))
        arm((0.28, 0.08, 0.98), (0.025, 0.025, 0.14), (30, 30, 34))
        arm((0.28, 0.18, 0.55), (0.035, 0.035, 0.14), (24, 24, 28))
        arm((0.28, -0.1, 0.56), (0.04, 0.1, 0.06), (36, 36, 42))

    def draw_viewmodel(self):
        cam = self.cam
        world_items = self.items
        self.items = []
        gx, gy, gz = self.viewmodel_offset()
        yaw, pitch = cam.yaw, cam.pitch + self.kick * 0.6
        shirt, glove, metal, dark = (66, 112, 188), (58, 52, 48), (92, 98, 112), (54, 58, 68)

        def part(local, half, color, extra_yaw=0.0):
            center = v_add(cam.pos, rotate(local, cam.yaw, cam.pitch))
            self.add_box(center, half, color, yaw + extra_yaw, pitch)

        part((gx + 0.08, gy - 0.11, gz - 0.2), (0.045, 0.045, 0.18), shirt, -0.15)
        part((gx + 0.025, gy - 0.065, gz - 0.02), (0.035, 0.04, 0.04), glove)
        part((gx - 0.1, gy - 0.085, gz + 0.1), (0.042, 0.042, 0.16), shirt, 0.45)
        part((gx - 0.025, gy - 0.05, gz + 0.2), (0.032, 0.035, 0.045), glove)
        part((gx, gy - 0.015, gz - 0.27), (0.034, 0.055, 0.08), (110, 76, 46))
        part((gx, gy, gz), (0.038, 0.055, 0.2), metal)
        part((gx, gy + 0.015, gz + 0.32), (0.017, 0.017, 0.13), dark)
        part((gx, gy + 0.082, gz - 0.02), (0.024, 0.024, 0.1), dark)
        part((gx, gy - 0.09, gz + 0.05), (0.028, 0.055, 0.04), (36, 36, 42))
        part((gx, gy + 0.06, gz + 0.16), (0.008, 0.02, 0.008), (255, 200, 60))

        self.items.sort(key=lambda it: it[0], reverse=True)
        for item in self.items:
            pygame.draw.polygon(self.screen, item[3], item[2])
            pygame.draw.polygon(self.screen, scale_color(item[3], 0.7), item[2], 1)
        self.items = world_items

        rear = cam.to_cam(v_add(cam.pos, rotate((gx, gy + 0.082, gz - 0.121), yaw, pitch)))
        if rear[2] > NEAR:
            sx, sy = cam.project(rear)
            r = cam.f * 0.019 / rear[2]
            pygame.draw.circle(self.screen, (20, 22, 28), (sx, sy), r * 1.12)
            pygame.draw.circle(self.screen, (52, 96, 140), (sx, sy), r)
            pygame.draw.circle(self.screen, (98, 160, 210), (sx - r * 0.15, sy - r * 0.15), r * 0.62)
            pygame.draw.arc(self.screen, (220, 240, 255), (sx - r * 0.7, sy - r * 0.7, r * 1.4, r * 1.4),
                            1.9, 2.9, max(1, int(r * 0.12)))

    def add_tree(self, base, s, dark, cam):
        c = cam.to_cam(base)
        if c[2] < 5:
            return
        sx, sy = cam.project(c)
        k = cam.f / c[2]
        height = 9.5 * s * k
        if sx < -height or sx > W + height or sy - height > H:
            return
        self.items.append((c[2], 3, (sx, sy, k * s, dark)))

    def draw_tree(self, data, depth):
        sx, sy, k, dark = data
        scr = self.screen
        light = scale_color(dark, 1.45)
        trunk = fog((96, 70, 48), depth)
        pygame.draw.rect(scr, trunk, (sx - 0.18 * k, sy - 1.4 * k, 0.36 * k, 1.4 * k))
        for i in range(3):
            base_y = sy - (1.0 + i * 1.8) * k
            half = (2.3 - i * 0.55) * k
            top_y = base_y - 3.0 * k
            pygame.draw.polygon(scr, fog(dark, depth), [(sx - half, base_y), (sx, top_y), (sx, base_y)])
            pygame.draw.polygon(scr, fog(light, depth), [(sx, base_y), (sx, top_y), (sx + half, base_y)])

    def render_world(self):
        cam = self.cam
        self.items = []
        horizon = self.draw_sky()
        self.draw_ground(horizon)
        self.draw_shadows()

        cp = cam.pos
        for verts, n, col, c, style, bias, radius in self.static_faces:
            p0 = verts[0]
            if (cp[0] - p0[0]) * n[0] + (cp[1] - p0[1]) * n[1] + (cp[2] - p0[2]) * n[2] <= 0:
                continue
            if self.in_view(c, radius):
                self.add_face(verts, n, col, True, style, bias)

        for base, s, dark in self.trees:
            self.add_tree(base, s, dark, cam)

        for tg in self.targets:
            if tg.state == "dead":
                continue
            scale = 1.0 if tg.state == "alive" else max(0.0, tg.timer / 0.25)
            if tg.state == "alive" and tg.spawn_t < 0.3:
                scale = tg.spawn_t / 0.3
            if tg.kind in ("static", "moving") and tg.state == "alive":
                px, py, pz = tg.pos
                h = (py - tg.radius * 0.9) / 2
                self.add_box((px, h, pz), (0.05, h, 0.05), (128, 96, 64))
                self.add_box((px, 0.07, pz), (0.38, 0.07, 0.38), (84, 88, 98), top=(110, 114, 124))
            c = cam.to_cam(tg.pos)
            if c[2] < 0.3:
                continue
            sx, sy = cam.project(c)
            r = cam.f * tg.radius * scale / c[2]
            if r < 0.5 or sx + r * 2 < 0 or sx - r * 2 > W or sy + r * 2 < 0 or sy - r * 2 > H:
                continue
            self.items.append((c[2], 1, (sx, sy, r, tg)))

        if self.state != "menu" and not self.first_person and self.cam_dist > 0.8:
            self.add_player()

        for p in self.particles:
            c = cam.to_cam(p[0])
            if c[2] < NEAR:
                continue
            sx, sy = cam.project(c)
            s = max(1.5, cam.f * p[4] / c[2])
            self.items.append((c[2], 2, (sx, sy, s, fog(p[3], c[2]))))

        for pos, age, radius in self.shockwaves:
            c = cam.to_cam(pos)
            if c[2] < NEAR:
                continue
            sx, sy = cam.project(c)
            k = age / 0.35
            self.items.append((c[2] - 0.5, 4, (sx, sy, cam.f * radius * (0.3 + 0.7 * k) / c[2], k)))

        self.items.sort(key=lambda it: it[0], reverse=True)
        scr = self.screen
        for item in self.items:
            depth, kind, data = item[0], item[1], item[2]
            if kind == 0:
                col = item[3]
                pygame.draw.polygon(scr, col, data)
                if item[4]:
                    pygame.draw.polygon(scr, scale_color(col, 0.7), data, 1)
                if item[5] == "crate":
                    self.draw_crate_detail(data, col)
            elif kind == 1:
                self.draw_target(data, depth)
            elif kind == 2:
                sx, sy, s, col = data
                pygame.draw.circle(scr, col, (sx, sy), s * 0.6)
            elif kind == 3:
                self.draw_tree(data, depth)
            else:
                sx, sy, r, k = data
                pygame.draw.circle(scr, lerp_color((255, 240, 180), (255, 120, 40), k), (sx, sy), r,
                                   max(1, int(6 * (1 - k))))

        in_game = self.state not in ("menu", "slots", "newgame") and not (
            self.state == "settings" and self.settings_return == "menu")
        if self.first_person and in_game:
            self.draw_viewmodel()

        for a, b, life in self.tracers:
            seg = clip_line(cam.to_cam(a), cam.to_cam(b))
            if seg:
                p0, p1 = cam.project(seg[0]), cam.project(seg[1])
                pygame.draw.line(scr, (255, 190, 90), p0, p1, 4)
                pygame.draw.line(scr, (255, 252, 220), p0, p1, 2)
        if self.muzzle_flash > 0 and self.state != "menu":
            c = cam.to_cam(self.muzzle_pos())
            if c[2] > NEAR:
                sx, sy = cam.project(c)
                r = cam.f * (0.045 if self.first_person else 0.16) / c[2]
                g = pygame.transform.scale(self.flash_glow, (int(r * 5) + 2, int(r * 5) + 2))
                scr.blit(g, (sx - g.get_width() / 2, sy - g.get_height() / 2), special_flags=pygame.BLEND_RGB_ADD)
                star = []
                spin = random.uniform(0, 1)
                for i in range(12):
                    rr = r if i % 2 == 0 else r * 0.4
                    a = spin + i / 12 * 2 * math.pi
                    star.append((sx + math.cos(a) * rr, sy + math.sin(a) * rr))
                pygame.draw.polygon(scr, (255, 210, 110), star)
                pygame.draw.circle(scr, (255, 255, 230), (sx, sy), r * 0.35)

        for pos, text, color, life, size in self.texts:
            c = cam.to_cam(pos)
            if c[2] < NEAR:
                continue
            font = {"big": self.f_big, "mid": self.f_num}.get(size, self.f_text)
            sx, sy = cam.project(c)
            alpha = int(255 * min(1.0, life * 2))
            self.text(text, font, color, (sx, sy), "center", alpha=alpha, outline=True)

    def draw_crate_detail(self, pts, col):
        if len(pts) != 4:
            return
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        if max(xs) - min(xs) < 14 or max(ys) - min(ys) < 14:
            return
        cx = sum(xs) / 4
        cy = sum(ys) / 4
        inner = [(p[0] + (cx - p[0]) * 0.2, p[1] + (cy - p[1]) * 0.2) for p in pts]
        dark = scale_color(col, 0.72)
        light = scale_color(col, 1.08)
        pygame.draw.polygon(self.screen, dark, inner, 2)
        pygame.draw.line(self.screen, dark, inner[0], inner[2], 3)
        pygame.draw.line(self.screen, light, (inner[0][0] + 1, inner[0][1] - 1), (inner[2][0] + 1, inner[2][1] - 1), 1)

    def draw_target(self, data, depth):
        sx, sy, r, tg = data
        scr = self.screen
        colors = Target.COLORS[tg.kind]
        if tg.kind == "gold":
            pulse = 2.6 + 0.3 * math.sin(self.time * 10)
            size = int(r * pulse * 2) + 2
            g = pygame.transform.scale(self.gold_glow, (size, size))
            scr.blit(g, (sx - size / 2, sy - size / 2), special_flags=pygame.BLEND_RGB_ADD)
        if tg.kind == "flying":
            arm_y = sy - r * 0.15
            pygame.draw.line(scr, fog((50, 52, 60), depth), (sx - r * 1.45, arm_y), (sx + r * 1.45, arm_y),
                             max(1, int(r * 0.14)))
            for side in (-1, 1):
                rx = sx + side * r * 1.45
                pygame.draw.line(scr, fog((50, 52, 60), depth), (rx, arm_y), (rx, arm_y - r * 0.35), max(1, int(r * 0.1)))
                blade = abs(math.cos(self.time * 30 + side)) * r * 0.65 + r * 0.1
                pygame.draw.ellipse(scr, fog((150, 156, 166), depth),
                                    (rx - blade, arm_y - r * 0.42, blade * 2, max(2, r * 0.14)))
        pygame.draw.circle(scr, fog((60, 44, 30), depth), (sx + r * 0.08, sy + r * 0.08), r)
        for i, col in enumerate(colors):
            pygame.draw.circle(scr, fog(col, depth), (sx, sy), max(1.0, r * (5 - i) / 5))
        pygame.draw.circle(scr, fog((34, 34, 40), depth), (sx, sy), r, max(1, int(r * 0.07)))
        if r > 6:
            pygame.draw.arc(scr, fog((255, 255, 255), depth), (sx - r * 0.8, sy - r * 0.8, r * 1.6, r * 1.6),
                            1.9, 2.9, max(1, int(r * 0.08)))

    def text(self, text, font, color, pos, anchor="topleft", shadow=True, alpha=255, outline=False):
        surf = font.render(text, True, color)
        rect = surf.get_rect(**{anchor: (int(pos[0]), int(pos[1]))})
        if outline:
            ol = font.render(text, True, (10, 12, 20))
            ol.set_alpha(int(alpha * 0.8))
            for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2)):
                self.screen.blit(ol, rect.move(dx, dy))
        elif shadow:
            sh = font.render(text, True, (0, 0, 0))
            sh.set_alpha(int(alpha * 0.55))
            self.screen.blit(sh, rect.move(2, 2))
        if alpha < 255:
            surf.set_alpha(alpha)
        self.screen.blit(surf, rect)
        return rect

    def panel(self, rect, color=(12, 20, 36, 180), radius=14, border=None, accent=None):
        rect = pygame.Rect(rect)
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surf, color, surf.get_rect(), border_radius=radius)
        hl = pygame.Surface((rect.w, max(1, rect.h // 2)), pygame.SRCALPHA)
        pygame.draw.rect(hl, (255, 255, 255, 14), hl.get_rect(), border_top_left_radius=radius,
                         border_top_right_radius=radius)
        surf.blit(hl, (0, 0))
        if border:
            pygame.draw.rect(surf, border, surf.get_rect(), 2, border_radius=radius)
        self.screen.blit(surf, rect.topleft)
        if accent:
            pygame.draw.rect(self.screen, accent, (rect.x, rect.y + 12, 4, rect.h - 24), border_radius=2)
        return rect

    def blur_background(self, tint=(6, 10, 22, 150)):
        small = pygame.transform.smoothscale(self.screen, (W // 10, H // 10))
        small = pygame.transform.smoothscale(small, (W // 5, H // 5))
        self.screen.blit(pygame.transform.smoothscale(small, (W, H)), (0, 0))
        dim = pygame.Surface((W, H), pygame.SRCALPHA)
        dim.fill(tint)
        self.screen.blit(dim, (0, 0))

    def button(self, rect, label, action, primary=False, sub=None, danger=False, font=None):
        rect = pygame.Rect(rect)
        font = font or self.f_mid
        hover = rect.collidepoint(pygame.mouse.get_pos())
        draw = rect.move(6, 0) if hover and rect.w > 200 else rect
        if primary:
            fill = (255, 206, 80, 245) if hover else (255, 190, 50, 230)
            self.panel(draw, fill, 12)
            color, sub_color = (34, 24, 6), (90, 64, 18)
        elif danger:
            self.panel(draw, (220, 70, 70, 235) if hover else (180, 50, 54, 220), 12)
            color, sub_color = (255, 240, 240), (255, 210, 210)
        else:
            self.panel(draw, (255, 255, 255, 46 if hover else 24), 12, (255, 255, 255, 120 if hover else 60))
            color, sub_color = (240, 244, 252), (170, 182, 204)
        if sub:
            self.text(label, font, color, (draw.centerx, draw.centery - 10), "center", shadow=False)
            self.text(sub, self.f_small, sub_color, (draw.centerx, draw.centery + 15), "center", shadow=False)
        else:
            self.text(label, font, color, draw.center, "center", shadow=False)
        self.buttons.append((rect, action))
        return rect

    def draw_icon(self, key, cx, cy, col):
        s = self.screen
        if key == "fire_rate":
            pygame.draw.polygon(s, col, [(cx + 5, cy - 17), (cx - 9, cy + 3), (cx - 1, cy + 3),
                                         (cx - 5, cy + 17), (cx + 9, cy - 4), (cx + 1, cy - 4)])
        elif key == "mag":
            for i in range(3):
                x = cx - 11 + i * 11
                pygame.draw.rect(s, col, (x - 4, cy - 4, 8, 18), border_radius=2)
                pygame.draw.polygon(s, col, [(x - 4, cy - 5), (x, cy - 15), (x + 4, cy - 5)])
        elif key == "reload":
            pygame.draw.arc(s, col, (cx - 14, cy - 14, 28, 28), 0.7, 5.6, 4)
            ex, ey = cx + 14 * math.cos(0.7), cy - 14 * math.sin(0.7)
            pygame.draw.polygon(s, col, [(ex - 7, ey - 3), (ex + 7, ey - 5), (ex + 2, ey + 8)])
        elif key == "accuracy":
            pygame.draw.circle(s, col, (cx, cy), 13, 3)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                pygame.draw.line(s, col, (cx + dx * 8, cy + dy * 8), (cx + dx * 18, cy + dy * 18), 3)
            pygame.draw.circle(s, col, (cx, cy), 3)
        elif key == "mult":
            self.text("x2", self.f_num, col, (cx, cy + 1), "center", shadow=False)
        elif key == "speed":
            for i, w in enumerate((10, 16, 10)):
                y = cy - 8 + i * 8
                pygame.draw.line(s, col, (cx - 16, y), (cx - 16 + w, y), 3)
            pygame.draw.polygon(s, col, [(cx - 2, cy - 12), (cx + 14, cy), (cx - 2, cy + 12), (cx + 3, cy)])
        elif key == "zoom":
            pygame.draw.circle(s, col, (cx - 4, cy - 4), 10, 3)
            pygame.draw.line(s, col, (cx + 4, cy + 4), (cx + 14, cy + 14), 6)
        elif key == "auto":
            for i in range(3):
                x = cx - 14 + i * 10
                pygame.draw.rect(s, col, (x, cy - 4, 8, 8), border_radius=2)
                pygame.draw.polygon(s, col, [(x + 8, cy - 4), (x + 12, cy), (x + 8, cy + 4)])
        elif key == "explosive":
            star = []
            for i in range(16):
                rr = 17 if i % 2 == 0 else 8
                a = i / 16 * 2 * math.pi
                star.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
            pygame.draw.polygon(s, col, star)
        elif key == "targets":
            pygame.draw.circle(s, col, (cx, cy), 16)
            pygame.draw.circle(s, (20, 26, 40), (cx, cy), 11)
            pygame.draw.circle(s, col, (cx, cy), 6)

    def draw_hud(self):
        scr = self.screen
        cx, cy = W // 2, H // 2

        gap = max(5.0, self.cam.f * self.current_spread()) + 4
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a = (cx + dx * gap, cy + dy * gap)
            b = (cx + dx * (gap + 10), cy + dy * (gap + 10))
            pygame.draw.line(scr, (10, 12, 20), a, b, 4)
            pygame.draw.line(scr, (255, 255, 255), a, b, 2)
        pygame.draw.circle(scr, (10, 12, 20), (cx, cy), 3)
        pygame.draw.circle(scr, (255, 255, 255), (cx, cy), 2)
        if self.hit_marker > 0:
            mc = GOLD if self.hit_marker_bull else (255, 90, 90)
            k = 1 + (0.15 - self.hit_marker) * 3
            for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                pygame.draw.line(scr, mc, (cx + dx * 8 * k, cy + dy * 8 * k), (cx + dx * 16 * k, cy + dy * 16 * k), 3)

        card = self.panel((18, 18, 290, 108), accent=ACCENT)
        self.text(self.t("score"), self.f_label, (170, 186, 210), (card.x + 22, card.y + 14), shadow=False)
        self.text("{:,}".format(int(round(self.shown_points))).replace(",", " "), self.f_huge, (255, 226, 120),
                  (card.x + 20, card.y + 30))
        acc = 100 * self.session_hits / self.session_shots if self.session_shots else 0
        self.text(self.t("accuracy", int(acc)), self.f_small, (196, 206, 222), (card.right - 16, card.y + 14),
                  "topright", shadow=False)

        if self.combo > 1:
            mult = 1 + min(self.combo - 1, 20) * 0.1
            box = self.panel((18, 134, 290, 50), (40, 22, 12, 190), accent=(255, 140, 60))
            self.text(self.t("combo"), self.f_label, (255, 190, 140), (box.x + 22, box.y + 10), shadow=False)
            self.text("x%.1f" % mult, self.f_num, (255, 170, 90), (box.x + 22, box.y + 22), shadow=False)
            self.text("%d" % self.combo, self.f_numsm, (255, 220, 190), (box.right - 16, box.y + 8), "topright",
                      shadow=False)
            w = int(150 * max(0.0, self.combo_timer / 4.0))
            pygame.draw.rect(scr, (90, 50, 30), (box.right - 166, box.y + 36, 150, 5), border_radius=3)
            pygame.draw.rect(scr, (255, 150, 70), (box.right - 166, box.y + 36, w, 5), border_radius=3)

        card = self.panel((W - 278, H - 118, 260, 100), accent=(120, 210, 255))
        self.text(self.t("ammo"), self.f_label, (170, 186, 210), (card.x + 22, card.y + 14), shadow=False)
        low = self.ammo <= max(1, self.mag_size // 4)
        self.text("%d" % self.ammo, self.f_huge, (255, 100, 100) if low else (255, 255, 255),
                  (card.x + 20, card.y + 32))
        num_w = self.f_huge.size("%d" % self.ammo)[0]
        self.text("/ %d" % self.mag_size, self.f_num, (150, 164, 186), (card.x + 28 + num_w, card.y + 54))
        n = self.mag_size
        bw = min(8, int(130 / n) - 2) if n else 8
        bw = max(2, bw)
        x0 = card.right - 18 - n * (bw + 2)
        for i in range(n):
            filled = i < self.ammo
            colr = (255, 214, 110) if filled else (60, 70, 88)
            pygame.draw.rect(scr, colr, (x0 + i * (bw + 2), card.y + 16, bw, 14), border_radius=2)
        if self.reloading:
            k = 1 - self.reload_timer / self.reload_time
            pygame.draw.rect(scr, (40, 50, 66), (card.x + 22, card.bottom - 16, card.w - 40, 6), border_radius=3)
            pygame.draw.rect(scr, (120, 220, 255), (card.x + 22, card.bottom - 16, int((card.w - 40) * k), 6),
                             border_radius=3)
            pygame.draw.arc(scr, (120, 220, 255), (cx - 26, cy - 26, 52, 52), math.pi / 2,
                            math.pi / 2 + k * 2 * math.pi, 3)
            self.text(self.t("reloading"), self.f_label, (150, 228, 255), (cx, cy + 36), "midtop")
        else:
            self.text(self.t("reload_hint", self.key_label("reload")), self.f_small, (150, 164, 186), (card.right - 16, card.y + 38),
                      "topright", shadow=False)

        cheapest = self.cheapest_available()
        if cheapest is not None and self.save["points"] >= cheapest:
            pulse = 0.5 + 0.5 * math.sin(self.time * 5)
            label = self.t("upgrade_ready", self.key_label("shop"))
            w = self.f_mid.size(label)[0] + 40
            self.panel((18, H - 62, w, 44), (20, 70, 40, int(170 + 60 * pulse)), 22, (120, 255, 150, 160))
            self.text(label, self.f_mid, (170, 255, 190), (38, H - 40), "midleft", shadow=False)
        else:
            label = self.t("hint", self.key_label("shop"))
            w = self.f_small.size(label)[0] + 32
            self.panel((18, H - 54, w, 34), (12, 20, 36, 150), 17)
            self.text(label, self.f_small, (220, 228, 240), (34, H - 37), "midleft", shadow=False)

        if self.message:
            text, color, left, dur = self.message
            age = dur - left
            pop = 1.0 + max(0.0, 0.15 - age) / 0.15 * 0.5
            alpha = int(255 * min(1.0, left * 2.5))
            surf = self.f_huge.render(text, True, color)
            ol = self.f_huge.render(text, True, (20, 14, 6))
            if pop != 1.0:
                size = (int(surf.get_width() * pop), int(surf.get_height() * pop))
                surf = pygame.transform.smoothscale(surf, size)
                ol = pygame.transform.smoothscale(ol, size)
            surf.set_alpha(alpha)
            ol.set_alpha(int(alpha * 0.7))
            r = surf.get_rect(center=(cx, 130))
            for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (3, 3)):
                scr.blit(ol, r.move(dx, dy))
            scr.blit(surf, r)

        self.draw_radar()

    def draw_radar(self):
        rx, ry = W - 194, 18
        cx, cy = rx + 88, ry + 88
        scr = self.screen
        scr.blit(self.radar_bg, (rx, ry))
        half = self.cam.fov / 2
        cone = [(cx, cy)] + [(cx + math.sin(a) * 84, cy - math.cos(a) * 84)
                             for a in (-half + i * half / 4 for i in range(9))]
        cone_s = pygame.Surface((176, 176), pygame.SRCALPHA)
        pygame.draw.polygon(cone_s, (255, 255, 255, 26), [(x - rx, y - ry) for x, y in cone])
        scr.blit(cone_s, (rx, ry))
        scale = 84 / 45.0
        cam = self.cam
        for tg in self.targets:
            if tg.state != "alive":
                continue
            dx, dz = tg.pos[0] - self.ppos[0], tg.pos[2] - self.ppos[2]
            x = (dx * cam.cy - dz * cam.sy) * scale
            z = (dx * cam.sy + dz * cam.cy) * scale
            d = math.hypot(x, z)
            if d > 80:
                x, z = x * 80 / d, z * 80 / d
            r = 6 if tg.kind == "gold" else 4
            pygame.draw.circle(scr, (10, 12, 20), (cx + x, cy - z), r + 1)
            pygame.draw.circle(scr, Target.RADAR[tg.kind], (cx + x, cy - z), r)
        pygame.draw.polygon(scr, (255, 255, 255), [(cx, cy - 8), (cx - 6, cy + 6), (cx, cy + 3), (cx + 6, cy + 6)])

    def draw_shop(self):
        scr = self.screen
        self.blur_background()
        self.text(self.t("shop_title"), self.f_huge, (255, 255, 255), (W // 2, 50), "center")
        pts_label = "{:,}".format(self.save["points"]).replace(",", " ")
        pw = self.f_num.size(pts_label)[0] + 70
        pill = self.panel((W // 2 - pw // 2, 84, pw, 40), (255, 190, 50, 230), 20)
        pygame.draw.circle(scr, (120, 80, 10), (pill.x + 22, pill.centery), 9)
        pygame.draw.circle(scr, (255, 236, 150), (pill.x + 22, pill.centery), 6)
        self.text(pts_label, self.f_num, (40, 26, 6), (pill.x + 40, pill.centery + 1), "midleft", shadow=False)

        self.shop_rects = []
        mouse = pygame.mouse.get_pos()
        card_w, card_h = 570, 94
        x0 = W // 2 - card_w - 10
        y0 = 140
        for i, (key, max_lvl, base, icol) in enumerate(UPGRADES):
            x = x0 + (i % 2) * (card_w + 20)
            y = y0 + (i // 2) * (card_h + 10)
            rect = pygame.Rect(x, y, card_w, card_h)
            lvl = self.lvl(key)
            maxed = lvl >= max_lvl
            price = upgrade_price(base, lvl)
            can = not maxed and self.save["points"] >= price
            hover = rect.collidepoint(mouse)
            bg = (22, 34, 54, 225) if not hover else (34, 50, 76, 240)
            border = (255, 210, 80, 200) if maxed else ((120, 230, 140, 200) if can else (255, 255, 255, 40))
            self.panel(rect, bg, 14, border)
            self.shop_rects.append((rect, key))

            icon = pygame.Rect(x + 14, y + 15, 64, 64)
            ibg = pygame.Surface(icon.size, pygame.SRCALPHA)
            pygame.draw.rect(ibg, icol + (60,), ibg.get_rect(), border_radius=14)
            pygame.draw.rect(ibg, icol + (140,), ibg.get_rect(), 2, border_radius=14)
            scr.blit(ibg, icon.topleft)
            self.draw_icon(key, icon.centerx, icon.centery, icol)
            self.text(str((i + 1) % 10), self.f_label, (150, 160, 180), (x + 18, y + 8), shadow=False)

            name, desc = T[self.lang]["up_" + key]
            self.text(name, self.f_mid, (255, 255, 255), (x + 92, y + 10), shadow=False)
            self.text(desc, self.f_small, (166, 178, 198), (x + 92, y + 40), shadow=False)
            now = stat_text(key, lvl, self.lang)
            if maxed:
                self.text(now, self.f_small, (255, 214, 110), (x + 92, y + 64), shadow=False)
            else:
                r = self.text(now, self.f_small, (150, 170, 196), (x + 92, y + 64), shadow=False)
                r = self.text("  »  ", self.f_small, (110, 124, 146), r.topright, shadow=False)
                self.text(stat_text(key, lvl + 1, self.lang), self.f_small, (130, 225, 255), r.topright,
                          shadow=False)

            for p in range(max_lvl):
                pc = (255, 205, 70) if p < lvl else (56, 66, 86)
                pygame.draw.rect(scr, pc, (x + card_w - 20 - (max_lvl - p) * 15, y + 14, 11, 11), border_radius=3)
            bx = pygame.Rect(0, 0, 124, 36)
            bx.bottomright = (x + card_w - 16, y + card_h - 12)
            if maxed:
                self.panel(bx, (255, 205, 70, 50), 18, (255, 205, 70, 170))
                self.text(self.t("max"), self.f_mid, (255, 214, 100), bx.center, "center", shadow=False)
            else:
                if can:
                    self.panel(bx, (60, 190, 100, 235) if hover else (46, 160, 84, 220), 18)
                    tc = (240, 255, 244)
                else:
                    self.panel(bx, (80, 40, 46, 160), 18, (230, 100, 100, 120))
                    tc = (240, 150, 150)
                pygame.draw.circle(scr, (255, 214, 90), (bx.x + 18, bx.centery), 7)
                self.text(str(price), self.f_numsm, tc, (bx.x + 32, bx.centery + 1), "midleft", shadow=False)

        s = self.save
        acc = 100 * s["hits"] / s["shots"] if s["shots"] else 0
        self.text(self.t("stats", s["hits"], s["bullseyes"], s["best_combo"], int(acc)),
                  self.f_small, (196, 206, 222), (W // 2, H - 50), "center")
        self.text(self.t("shop_hint", self.key_label("shop")), self.f_small, (150, 162, 182), (W // 2, H - 24), "center")

    @staticmethod
    def fmt_points(n):
        return "{:,}".format(int(n)).replace(",", " ")

    def fmt_time(self, seconds):
        minutes = int(seconds // 60)
        if minutes >= 60:
            return self.t("hours", minutes // 60, minutes % 60)
        return self.t("minutes", minutes)

    def draw_menu(self):
        scr = self.screen
        scr.blit(self.menu_shade, (0, 0))
        self.buttons = []
        x = 90
        self.text(self.t("title"), self.f_title, (255, 216, 100), (x, 80), outline=True)
        pygame.draw.rect(scr, ACCENT, (x + 4, 198, 90, 5), border_radius=3)
        self.text(self.t("subtitle"), self.f_mid, (226, 234, 248), (x + 2, 218))

        y = 280
        cont = self.continue_slot()
        if cont:
            self.button((x, y, 360, 66), self.t("continue"), "continue", primary=True,
                        sub=self.t("slot_info", cont["name"], self.fmt_points(cont["points"])))
            y += 78
        self.button((x, y, 360, 52), self.t("new_game"), "new", primary=not cont)
        y += 62
        if self.slots:
            self.button((x, y, 360, 52), self.t("load_game"), "load_menu")
            y += 62
        self.button((x, y, 360, 52), self.t("settings"), "settings")
        y += 62
        self.button((x, y, 360, 52), self.t("quit"), "quit")

        rows = [(self.key_label(a), self.t("act_" + a)) for a in ACTIONS]
        rows += [(self.t("mouse_key"), self.t("look")), ("Esc", self.t("pause_action"))]
        card = self.panel((W - 470, 236, 380, 56 + len(rows) * 27), (10, 16, 30, 190), 16, accent=ACCENT)
        self.text(self.t("controls"), self.f_label, (170, 186, 210), (card.x + 26, card.y + 18), shadow=False)
        for i, (k, v) in enumerate(rows):
            ry = card.y + 42 + i * 27
            kw = self.f_label.size(k)[0] + 18
            chip = pygame.Rect(card.x + 150 - kw, ry, kw, 24)
            self.panel(chip, (255, 255, 255, 30), 6, (255, 255, 255, 70))
            self.text(k, self.f_label, (255, 214, 110), chip.center, "center", shadow=False)
            self.text(v, self.f_text, (228, 234, 246), (card.x + 166, ry + 12), "midleft", shadow=False)

        self.text(self.t("tip"), self.f_small, (206, 216, 232), (x + 2, H - 44))

    def draw_slots(self):
        scr = self.screen
        self.blur_background()
        self.buttons = []
        self.text(self.t("slots_title"), self.f_huge, (255, 255, 255), (W // 2, 56), "center")
        mouse = pygame.mouse.get_pos()
        last = self.settings.get("last_slot")
        card_w, card_h = 540, 110
        x0 = W // 2 - card_w - 10
        if not self.slots:
            self.text(self.t("slots_empty"), self.f_mid, (200, 210, 226), (W // 2, H // 2 - 40), "center")
        for i, slot in enumerate(self.slots[:MAX_SLOTS]):
            x = x0 + (i % 2) * (card_w + 20)
            y = 104 + (i // 2) * (card_h + 12)
            rect = pygame.Rect(x, y, card_w, card_h)
            sid = slot["id"]
            if self.confirm_delete == sid:
                self.panel(rect, (70, 20, 26, 235), 14, (255, 110, 110, 200))
                self.text(self.t("delete_q"), self.f_mid, (255, 220, 220), (x + 24, y + 22), shadow=False)
                self.text(slot["name"], self.f_small, (230, 170, 170), (x + 24, y + 56), shadow=False)
                self.button((x + card_w - 250, y + card_h - 54, 110, 40), self.t("yes"), ("confirm_delete", sid),
                            danger=True)
                self.button((x + card_w - 130, y + card_h - 54, 110, 40), self.t("no"), "cancel_delete")
                continue
            hover = rect.collidepoint(mouse)
            accent = ACCENT if sid == last else (120, 210, 255)
            self.panel(rect, (34, 50, 76, 240) if hover else (22, 34, 54, 225), 14,
                       (255, 255, 255, 90 if hover else 36), accent=accent)
            r = self.text(slot["name"], self.f_mid, (255, 255, 255), (x + 22, y + 12), shadow=False)
            if sid == last:
                badge = pygame.Rect(r.right + 12, y + 16, self.f_label.size(self.t("last"))[0] + 16, 22)
                self.panel(badge, (255, 196, 60, 220), 11)
                self.text(self.t("last"), self.f_label, (40, 28, 6), badge.center, "center", shadow=False)
            levels = sum(slot["upgrades"].values()) if isinstance(slot["upgrades"], dict) else 0
            self.text(self.t("slot_stats", levels, slot["hits"], slot["best_combo"]), self.f_small,
                      (170, 184, 206), (x + 22, y + 48), shadow=False)
            date = time.strftime("%d.%m.%Y  %H:%M", time.localtime(slot["updated"]))
            self.text(self.t("slot_time", date, self.fmt_time(slot["play_time"])), self.f_small, (130, 146, 170),
                      (x + 22, y + 74), shadow=False)
            self.text(self.fmt_points(slot["points"]), self.f_big, (255, 226, 120), (x + card_w - 22, y + 44),
                      "topright", shadow=False)
            self.text(self.t("points_word"), self.f_label, (170, 186, 210), (x + card_w - 22, y + 86), "topright",
                      shadow=False)
            dele = pygame.Rect(x + card_w - 46, y + 10, 32, 32)
            dhover = dele.collidepoint(mouse)
            pygame.draw.rect(scr, (200, 70, 70) if dhover else (70, 80, 100), dele, border_radius=8)
            for a, b in (((dele.x + 10, dele.y + 10), (dele.right - 10, dele.bottom - 10)),
                         ((dele.right - 10, dele.y + 10), (dele.x + 10, dele.bottom - 10))):
                pygame.draw.line(scr, (255, 255, 255), a, b, 3)
            self.buttons.append((dele, ("delete", sid)))
            self.buttons.append((rect, ("load", sid)))

        by = H - 92
        self.button((W // 2 - 250, by, 240, 50), self.t("back"), "back")
        if len(self.slots) < MAX_SLOTS:
            self.button((W // 2 + 10, by, 240, 50), self.t("new_game"), "new", primary=True)
        else:
            self.text(self.t("slots_full", MAX_SLOTS), self.f_small, (255, 160, 160), (W // 2 + 130, by + 25),
                      "center")
        self.text(self.t("slots_hint"), self.f_small, (150, 162, 182), (W // 2, H - 24), "center")

    def draw_newgame(self):
        scr = self.screen
        self.blur_background()
        self.buttons = []
        self.text(self.t("new_title"), self.f_huge, (255, 255, 255), (W // 2, 190), "center")
        card = self.panel((W // 2 - 300, 250, 600, 230), (12, 20, 36, 220), 16, accent=ACCENT)
        self.text(self.t("name_prompt"), self.f_label, (170, 186, 210), (card.x + 30, card.y + 24), shadow=False)
        field = pygame.Rect(card.x + 30, card.y + 50, card.w - 60, 60)
        self.panel(field, (255, 255, 255, 26), 12, (255, 196, 60, 200))
        r = self.text(self.name_input, self.f_big, (255, 255, 255), (field.x + 18, field.centery + 2), "midleft",
                      shadow=False)
        if int(self.time * 2) % 2 == 0:
            pygame.draw.rect(scr, ACCENT, (r.right + 4, field.y + 14, 3, field.h - 28))
        self.button((card.x + 30, card.bottom - 76, 260, 50), self.t("create"), "create", primary=True)
        self.button((card.right - 290, card.bottom - 76, 260, 50), self.t("cancel"), "back")
        self.text(self.t("name_hint"), self.f_small, (150, 162, 182), (W // 2, card.bottom + 26), "center")

    def draw_settings(self):
        scr = self.screen
        self.blur_background()
        self.buttons = []
        self.text(self.t("settings"), self.f_huge, (255, 255, 255), (W // 2, 52), "center")

        left = self.panel((W // 2 - 590, 96, 620, 516), (12, 20, 36, 220), 16, accent=ACCENT)
        self.text(self.t("controls_title"), self.f_label, (170, 186, 210), (left.x + 26, left.y + 18), shadow=False)
        mouse = pygame.mouse.get_pos()
        for i, action in enumerate(ACTIONS):
            ry = left.y + 44 + i * 38
            row = pygame.Rect(left.x + 16, ry, left.w - 32, 35)
            if row.collidepoint(mouse) or self.rebinding == action:
                pygame.draw.rect(scr, (40, 56, 84), row, border_radius=8)
            self.text(self.t("act_" + action), self.f_text, (230, 236, 248), (row.x + 12, row.centery), "midleft",
                      shadow=False)
            chip = pygame.Rect(row.right - 216, ry + 2, 210, 31)
            if self.rebinding == action:
                pulse = int(160 + 90 * math.sin(self.time * 8))
                self.panel(chip, (255, 196, 60, 60), 8, (255, 196, 60, pulse))
                self.text(self.t("press_key"), self.f_small, (255, 220, 130), chip.center, "center", shadow=False)
            else:
                hover = chip.collidepoint(mouse)
                self.panel(chip, (255, 255, 255, 50 if hover else 28), 8, (255, 255, 255, 110 if hover else 60))
                self.text(self.key_label(action), self.f_mid, (255, 214, 110), chip.center, "center", shadow=False)
            self.buttons.append((row, ("rebind", action)))
        self.text(self.t("fixed_keys"), self.f_small, (140, 154, 178), (left.x + 28, left.bottom - 30), shadow=False)

        right = self.panel((W // 2 + 50, 96, 540, 516), (12, 20, 36, 220), 16, accent=(120, 210, 255))
        x = right.x + 30
        self.text(self.t("mouse"), self.f_label, (170, 186, 210), (x, right.y + 18), shadow=False)
        self.text(self.t("sensitivity"), self.f_text, (230, 236, 248), (x, right.y + 50), shadow=False)
        sens = self.settings["sensitivity"]
        self.text("x%.2f" % sens, self.f_num, (130, 225, 255), (right.right - 30, right.y + 44), "topright",
                  shadow=False)
        track = pygame.Rect(x, right.y + 96, right.w - 60, 8)
        self.slider_rect = track
        k = (sens - SENS_MIN) / (SENS_MAX - SENS_MIN)
        pygame.draw.rect(scr, (50, 62, 84), track, border_radius=4)
        pygame.draw.rect(scr, (120, 210, 255), (track.x, track.y, int(track.w * k), track.h), border_radius=4)
        knob = (track.x + track.w * k, track.centery)
        pygame.draw.circle(scr, (10, 14, 24), knob, 13)
        pygame.draw.circle(scr, (255, 255, 255), knob, 11)
        dk = (1.0 - SENS_MIN) / (SENS_MAX - SENS_MIN)
        pygame.draw.line(scr, (150, 164, 186), (track.x + track.w * dk, track.bottom + 6),
                         (track.x + track.w * dk, track.bottom + 12), 2)

        self.text(self.t("invert_y"), self.f_text, (230, 236, 248), (x, right.y + 156), "midleft", shadow=False)
        on = self.settings["invert_y"]
        tog = pygame.Rect(right.right - 30 - 64, right.y + 140, 64, 32)
        pygame.draw.rect(scr, (60, 190, 100) if on else (60, 70, 92), tog, border_radius=16)
        pygame.draw.circle(scr, (255, 255, 255), (tog.right - 16 if on else tog.x + 16, tog.centery), 12)
        self.text(self.t("on") if on else self.t("off"), self.f_label, (170, 186, 210), (tog.x - 12, tog.centery),
                  "midright", shadow=False)
        self.buttons.append((pygame.Rect(x, right.y + 136, right.w - 60, 40), "invert"))

        pygame.draw.line(scr, (255, 255, 255, 30), (x, right.y + 196), (right.right - 30, right.y + 196), 1)
        self.text(self.t("camera_title"), self.f_label, (170, 186, 210), (x, right.y + 212), shadow=False)
        half = (right.w - 70) // 2
        for i, mode in enumerate(("third", "first")):
            label = self.t("cam_third") if mode == "third" else self.t("cam_first")
            self.button((x + i * (half + 10), right.y + 238, half, 50), label, ("camera_mode", mode),
                        primary=self.settings["camera_mode"] == mode)
        self.text(self.t("lang_title"), self.f_label, (170, 186, 210), (x, right.y + 310), shadow=False)
        self.button((x, right.y + 336, right.w - 60, 50), self.t("language"), "lang")
        self.button((x, right.y + 420, right.w - 60, 50), self.t("reset_controls"), "reset_controls")

        self.button((W // 2 - 140, H - 92, 280, 50), self.t("back"), "back", primary=True)
        self.text(self.t("rebind_hint"), self.f_small, (150, 162, 182), (W // 2, H - 24), "center")

    def draw_pause(self):
        self.blur_background()
        self.buttons = []
        self.text(self.t("pause"), self.f_title, (255, 255, 255), (W // 2, 170), "center", outline=True)
        if self.slot_id is not None:
            self.text(self.save["name"], self.f_mid, (255, 214, 110), (W // 2, 240), "center")
        bx = W // 2 - 170
        self.button((bx, 280, 340, 58), self.t("resume"), "resume", primary=True)
        self.button((bx, 350, 340, 52), self.t("settings"), "settings")
        self.button((bx, 414, 340, 52), self.t("main_menu"), "main_menu")
        self.button((bx, 478, 340, 52), self.t("quit"), "quit")
        self.text(self.t("pause_hint"), self.f_small, (196, 206, 222), (W // 2, 566), "center")

    def render(self):
        self.render_world()
        self.screen.blit(self.vignette, (0, 0))
        in_menu = self.state in ("menu", "slots", "newgame") or (
            self.state == "settings" and self.settings_return == "menu")
        if not in_menu:
            self.draw_hud()
        screens = {"menu": self.draw_menu, "shop": self.draw_shop, "pause": self.draw_pause,
                   "settings": self.draw_settings, "slots": self.draw_slots, "newgame": self.draw_newgame}
        if self.state in screens:
            screens[self.state]()

    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            for e in pygame.event.get():
                self.handle_event(e)
            if self.state == "play":
                self.update(dt)
            elif self.state in ("menu", "slots", "newgame") or (
                    self.state == "settings" and self.settings_return == "menu"):
                self.update_menu(dt)
            else:
                self.time += dt
                self.update_camera()
            self.render()
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
