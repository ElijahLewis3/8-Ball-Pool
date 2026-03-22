# Billiards Physics Simulator

A full-stack 8-ball pool simulator featuring a custom physics engine written in C, Python game logic with SQLite persistence, and an interactive web-based frontend.

Built as the capstone assignment for **CIS*2750 – Software Systems Development and Integration** at the University of Guelph (Winter 2024).

## Architecture

| Layer | Technology | Description |
|-------|-----------|-------------|
| Physics Engine | C | Handles ball movement, collision detection (ball-ball, ball-cushion, ball-hole), rolling friction/drag, and time-step simulation |
| Language Binding | SWIG | Generates Python bindings from the C library, enabling seamless cross-language integration |
| Game Logic & Database | Python, SQLite | Manages game state, player turns, shot history, and table serialization via an ORM-style `Database` class |
| Web Server | Python (`http.server`) | Serves the frontend, processes shot requests, and streams SVG frame data back to the client |
| Frontend | HTML, CSS, JavaScript | Renders the pool table as SVG, captures mouse-drag input on the cue ball, and animates shot playback frame-by-frame |

## How It Works

1. Players enter their names and a game name on the homepage
2. The pool table renders as an inline SVG with all 11 balls in a standard rack formation
3. Click and drag on the cue ball to aim, a guide line shows the shot direction
4. On release, the velocity vector is sent to the server, which runs the C physics simulation
5. The simulation produces frame-by-frame table states stored in SQLite, converted to SVG, and streamed back to the browser for animated playback

## Key Features

- **Real-time physics simulation** — elastic collisions, rolling friction, pocket detection, and cushion bouncing computed at 0.1ms time steps
- **Interactive aiming** — click-drag interface with visual guide line; shot power scales with drag distance
- **Persistent game state** — full shot history stored in SQLite (games, players, shots, table snapshots)
- **SVG rendering pipeline** — each frame rendered as a self-contained SVG, enabling smooth animation in the browser

## Building

**Prerequisites:** `clang`, `swig`, Python 3.11+

```bash
make            # compiles C library, generates SWIG bindings, builds shared objects
export LD_LIBRARY_PATH=$(pwd)
python3 server.py 8080
```

Then open `http://localhost:8080/homepage.html` in your browser.


## Technologies

C · Python · SWIG · SQLite · JavaScript · SVG · HTML/CSS
