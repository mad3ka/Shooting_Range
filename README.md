# Shooting Range 

A low-poly 3D target-shooting game written in pure Python with pygame. Hit targets to earn points, then spend the points on upgrades. You can play in third-person or first-person view.

The game has its own small software 3D renderer, so it needs no game engine and no art files. Everything is drawn in code, including the sounds.

## Features

- **Third-person and first-person views.** Switch between them at any time with one key.
- **Four target types:** static, moving, flying drones, and a rare fast golden target.
- **Scoring with depth:** bullseye bonus, hit-streak combo, and a bonus for long shots.
- **Upgrade shop** with 10 upgrades. Most have several levels.
- **Multiple save slots** (up to 8): continue your last game, start a new one, load or delete old ones.
- **Rebindable controls:** keyboard keys and mouse buttons, mouse sensitivity, and inverted vertical look.
- **Two languages:** English and Russian. You can switch at any time.
- **Visuals:** sky with sun and drifting clouds, mountains, forest, fog, shadows, particles, tracers, muzzle flash, and a radar.

## Requirements

- Python 3.9 or newer
- [pygame-ce](https://pyga.me/) 2.5 or newer

## Installation

```bash
pip install pygame-ce
```

## Running

```bash
python3 main.py
```

The window is 1280×720.

## Controls

These are the default bindings. All of them except mouse look and Esc can be changed in **Settings**.

| Action             | Default key  |
|--------------------|--------------|
| Move               | W A S D      |
| Sprint             | Left Shift   |
| Jump               | Space        |
| Look               | Mouse        |
| Shoot              | Left mouse   |
| Aim (zoom)         | Right mouse  |
| Reload             | R            |
| Upgrade shop       | B            |
| Toggle camera view | V            |
| Pause              | Esc          |

In the shop, click an upgrade or press `1`–`0` to buy it.

In the main menu and the pause menu, `L` switches the language.

## Gameplay

### Targets

| Target  | Look                          | Base points |
|---------|-------------------------------|-------------|
| Static  | Red and white, on a post      | 10          |
| Moving  | Blue and white, slides around | 20          |
| Flying  | Orange drone with rotors      | 35          |
| Golden  | Small, glowing, very fast     | 150         |

A golden target appears roughly every 20–30 seconds and disappears after 8 seconds. When you hit a target, a new one appears somewhere else on the range.

### Scoring

The points for each hit are:

```
base points × ring × combo × score multiplier × distance bonus
```

- **Ring:** how close you hit to the centre. A bullseye gives ×3. The outer rings give ×2, ×1.5, ×1.2 and ×1.
- **Combo:** each hit in a row adds ×0.1, up to ×3. A miss resets the combo. So does going 4 seconds without a hit.
- **Score multiplier:** comes from the *Score Multiplier* upgrade.
- **Distance bonus:** `1 + distance / 40`, so long shots are worth more.

Your spread gets wider while you move, and much wider in the air. Aiming with the right mouse button makes it tighter.

### Upgrades

The price of each upgrade is `base price × 1.7^level`.

| Upgrade          | Max level | Base price | Effect per level                                   |
|------------------|-----------|------------|----------------------------------------------------|
| Fire Rate        | 5         | 60         | 18% shorter time between shots                     |
| Extended Mag     | 5         | 50         | +4 rounds (8 at the start)                         |
| Fast Reload      | 5         | 50         | 20% faster reload (1.5 s at the start)             |
| Accuracy         | 5         | 70         | 30% less bullet spread                             |
| Score Multiplier | 6         | 120        | +25% points                                        |
| Light Boots      | 4         | 60         | +0.9 m/s run speed, higher jump                    |
| Scope            | 3         | 80         | Stronger zoom when aiming                          |
| Full Auto        | 1         | 250        | Hold the shoot button to fire continuously         |
| Explosive Rounds | 3         | 400        | Each shot explodes and hits nearby targets (1.8 / 2.8 / 3.8 m) |
| More Targets     | 4         | 150        | +2 targets on the range (8 at the start)           |

## Saves and settings

All files are created next to `main.py`:

| File                | Contents                                                       |
|---------------------|----------------------------------------------------------------|
| `saves/slot_N.json` | One save slot: name, points, upgrades, statistics, play time   |
| `settings.json`     | Language, key bindings, mouse sensitivity, invert-Y, camera view, last played slot |

- **Your progress is saved automatically.** This happens when you buy an upgrade, pause, or return to the main menu. It also happens every 30 seconds while you play.
- **Settings are shared by all save slots.**
- **Older versions of the game** used a single `save.json` file. On the first start, it is moved into slot 1 and renamed to `save_old.json`.
- **To reset everything,** delete the `saves/` folder and `settings.json`.

## Project structure

The whole game is in one file, [main.py](main.py). It contains:

- **3D math and the renderer:** camera, polygon clipping, painter's-algorithm sorting, fog, and shadows.
- **Procedural assets:** sky, clouds, mountains, trees, the arena, and synthesized sound effects.
- **Gameplay:** player movement and collisions, shooting, scoring, targets, and upgrades.
- **User interface:** the HUD, shop, menus, save-slot screens, and settings.
- **Localisation:** the `T` dictionary holds all English and Russian text.

## Notes

- **Fonts.** On macOS the game uses the system fonts *DIN Alternate* and *Avenir Next*. On other systems it uses Arial, or pygame's default font if Arial is missing.
- **Performance.** Rendering runs on the CPU in Python, so frame rate depends on your processor. It is usually 60–100+ FPS on a modern laptop.
