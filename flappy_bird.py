import pygame
import random
import sys
import os
import math

pygame.init()

# ─────────────────────────────────────────────
# UTILITY
# ─────────────────────────────────────────────

def resource_path(relative_path):
    """Return absolute path to a resource, works for both dev and PyInstaller builds."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ─────────────────────────────────────────────
# WINDOW & DISPLAY
# ─────────────────────────────────────────────

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

BG = pygame.transform.scale(
    pygame.image.load(resource_path("BG.jpg")), (WIDTH, HEIGHT)
)


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

PLAYER_WIDTH  = 110
PLAYER_HEIGHT = 65
JUMP_STRENGTH = -8
GRAVITY       = 0.5

PIPE_WIDTH     = 70
PIPE_GAP       = 180
PIPE_SPEED     = 3
CAP_HEIGHT     = 25
CAP_WIDTH      = PIPE_WIDTH + 24

FLOOR_Y        = HEIGHT - 80
PIPE_INTERVAL  = 90          # Frames between pipe spawns
PLAYER_START_X = 75
PLAYER_START_Y = 200

# Hitbox insets for fairer collision detection
HITBOX_Y_INSET      = 8
HITBOX_WIDTH_INSET  = 15
HITBOX_HEIGHT_INSET = 12


# ─────────────────────────────────────────────
# FONTS
# ─────────────────────────────────────────────

score_font     = pygame.font.SysFont('bauhaus93',  60)
game_over_font = pygame.font.SysFont('bauhaus93',  90)
final_font     = pygame.font.SysFont('comicsans',  45)
replay_font    = pygame.font.SysFont('comicsans',  35)
start_font     = pygame.font.SysFont('bauhaus93', 100)


# ─────────────────────────────────────────────
# ASSETS
# ─────────────────────────────────────────────

bird_sprite = pygame.transform.scale(
    pygame.image.load(resource_path("bird.png")), (PLAYER_WIDTH, PLAYER_HEIGHT)
)

# Semi-transparent dark overlay for start and game-over screens
overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
overlay.fill((40, 40, 40, 180))


# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────

def make_initial_state():
    """Return a fresh game state dictionary."""
    return {
        "phase":          "start",      # "start" | "running" | "game_over"
        "player_x":       PLAYER_START_X,
        "player_y":       PLAYER_START_Y,
        "player_vel":     0,
        "pipes":          [],
        "pipe_count":     0,            # Frame counter for pipe spawning
        "score":          0,
    }


# ─────────────────────────────────────────────
# DRAWING HELPERS
# ─────────────────────────────────────────────

def draw_pipes(pipes):
    """Draw all pipe pairs with border, fill, highlight, and caps."""
    for pipe in pipes:
        # Dark green border layer
        pygame.draw.rect(WIN, (0, 130, 0), (pipe["x"], 0,               PIPE_WIDTH, pipe["top_height"]))
        pygame.draw.rect(WIN, (0, 130, 0), (pipe["x"], pipe["bottom_y"], PIPE_WIDTH, HEIGHT - pipe["bottom_y"]))

        # Lighter green inner fill (inset 4 px)
        pygame.draw.rect(WIN, (0, 205, 0), (pipe["x"] + 4, 4,                    PIPE_WIDTH - 8, pipe["top_height"] - 8))
        pygame.draw.rect(WIN, (0, 205, 0), (pipe["x"] + 4, pipe["bottom_y"] + 4, PIPE_WIDTH - 8, HEIGHT - pipe["bottom_y"] - 8))

        # Highlight strip for 3-D effect
        pygame.draw.rect(WIN, (120, 255, 120), (pipe["x"] + 8, 4,                    10, pipe["top_height"] - 8))
        pygame.draw.rect(WIN, (120, 255, 120), (pipe["x"] + 8, pipe["bottom_y"] + 4, 10, HEIGHT - pipe["bottom_y"] - 8))

        # Caps
        top_cap_y = pipe["top_height"] - CAP_HEIGHT
        pygame.draw.rect(WIN, (0, 180, 0), (pipe["x"] - 12, top_cap_y,       CAP_WIDTH, CAP_HEIGHT))
        pygame.draw.rect(WIN, (0, 180, 0), (pipe["x"] - 12, pipe["bottom_y"], CAP_WIDTH, CAP_HEIGHT))

        # Cap borders
        pygame.draw.rect(WIN, (0, 130, 0), (pipe["x"] - 12, top_cap_y,       CAP_WIDTH, CAP_HEIGHT), width=4)
        pygame.draw.rect(WIN, (0, 130, 0), (pipe["x"] - 12, pipe["bottom_y"], CAP_WIDTH, CAP_HEIGHT), width=4)


def draw_score(score):
    """Draw the score with a drop shadow."""
    shadow     = score_font.render(f"SCORE: {score}", True, (0,   0,   0))
    score_surf = score_font.render(f"SCORE: {score}", True, (255, 215, 0))
    WIN.blit(shadow,     (WIDTH // 2 - 76, 34))
    WIN.blit(score_surf, (WIDTH // 2 - 80, 30))


# ─────────────────────────────────────────────
# SCREENS
# ─────────────────────────────────────────────

def draw_game(state):
    """Render the main gameplay frame: background, bird, pipes, score."""
    WIN.blit(BG, (0, 0))
    WIN.blit(bird_sprite, (state["player_x"], state["player_y"]))
    draw_pipes(state["pipes"])
    draw_score(state["score"])


def draw_start_screen(state):
    """Render the title screen with a floating bird animation."""
    WIN.blit(BG, (0, 0))

    # Bird bobs up and down using a sine wave
    floating_y = PLAYER_START_Y + 12 * math.sin(pygame.time.get_ticks() * 0.004)
    WIN.blit(bird_sprite, (state["player_x"], floating_y))

    WIN.blit(overlay, (0, 0))

    title      = start_font.render("Flappy Bird",            True, (255, 215,   0))
    title_sh   = start_font.render("Flappy Bird",            True, (  0,   0,   0))
    prompt     = replay_font.render("Press Space Bar to start!", True, (255, 255, 255))
    prompt_sh  = replay_font.render("Press Space Bar to start!", True, (  0,   0,   0))

    WIN.blit(title_sh, ((WIDTH - title.get_width()) // 2 + 4, HEIGHT // 3 + 4))
    WIN.blit(title,    ((WIDTH - title.get_width()) // 2,     HEIGHT // 3))
    WIN.blit(prompt_sh, ((WIDTH - prompt.get_width()) // 2 + 2, HEIGHT // 2 + 84))
    WIN.blit(prompt,    ((WIDTH - prompt.get_width()) // 2,     HEIGHT // 2 + 82))


def draw_game_over_screen(state):
    """Render the last game frame then overlay the game-over panel."""
    draw_game(state)
    WIN.blit(overlay, (0, 0))

    heading    = game_over_font.render("GAME OVER!",                    True, (255,  50,  50))
    heading_sh = game_over_font.render("GAME OVER!",                    True, (  0,   0,   0))
    fs         = final_font.render(f"FINAL SCORE: {state['score']}",   True, (255, 255,   0))
    fs_sh      = final_font.render(f"FINAL SCORE: {state['score']}",   True, (  0,   0,   0))
    replay     = replay_font.render("Press Space Bar to restart again", True, (255, 255, 255))
    replay_sh  = replay_font.render("Press Space Bar to restart again", True, (  0,   0,   0))

    WIN.blit(heading_sh, ((WIDTH - heading_sh.get_width()) // 2,     HEIGHT // 3))
    WIN.blit(heading,    ((WIDTH - heading.get_width())    // 2 - 8, HEIGHT // 3))
    WIN.blit(fs_sh,      ((WIDTH - fs_sh.get_width())     // 2 + 4, HEIGHT // 2 + 34))
    WIN.blit(fs,         ((WIDTH - fs.get_width())        // 2,     HEIGHT // 2 + 30))
    WIN.blit(replay_sh,  ((WIDTH - replay_sh.get_width()) // 2 + 2, HEIGHT // 2 + 84))
    WIN.blit(replay,     ((WIDTH - replay.get_width())    // 2,     HEIGHT // 2 + 82))


# ─────────────────────────────────────────────
# CORE LOOP FUNCTIONS
# ─────────────────────────────────────────────

def handle_events(state):
    """Process input events. Returns (state, run) — run=False signals quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return state, False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if state["phase"] == "start":
                state["phase"] = "running"

            elif state["phase"] == "running":
                state["player_vel"] = JUMP_STRENGTH   # Flap

            elif state["phase"] == "game_over":
                state = make_initial_state()           # Full reset
                state["phase"] = "running"             # Skip title screen

    return state, True


def update(state):
    """Advance physics, pipes, scoring, and collision. Mutates state in place."""
    if state["phase"] != "running":
        return state

    # ── Pipe spawning ──
    state["pipe_count"] += 1
    if state["pipe_count"] > PIPE_INTERVAL:
        state["pipe_count"] = 0
        top_height = random.randint(150, 400)
        state["pipes"].append({
            "x":          WIDTH,
            "top_height": top_height,
            "bottom_y":   top_height + PIPE_GAP,
            "passed":     False
        })

    # ── Pipe movement & cleanup ──
    for pipe in state["pipes"]:
        pipe["x"] -= PIPE_SPEED

    state["pipes"] = [p for p in state["pipes"] if p["x"] > -PIPE_WIDTH]

    # ── Scoring ──
    for pipe in state["pipes"]:
        if not pipe["passed"] and pipe["x"] + PIPE_WIDTH < state["player_x"]:
            state["score"] += 1
            pipe["passed"] = True

    # ── Physics ──
    state["player_vel"] += GRAVITY
    state["player_y"]   += state["player_vel"]

    # Clamp to floor
    if state["player_y"] >= FLOOR_Y:
        state["player_y"]  = FLOOR_Y
        state["player_vel"] = 0

    # ── Collision detection ──
    bird_rect = pygame.Rect(
        state["player_x"],
        state["player_y"] + HITBOX_Y_INSET,
        PLAYER_WIDTH  - HITBOX_WIDTH_INSET,
        PLAYER_HEIGHT - HITBOX_HEIGHT_INSET
    )

    for pipe in state["pipes"]:
        top_rect    = pygame.Rect(pipe["x"], 0,               PIPE_WIDTH, pipe["top_height"])
        bottom_rect = pygame.Rect(pipe["x"], pipe["bottom_y"], PIPE_WIDTH, HEIGHT - pipe["bottom_y"])

        if top_rect.colliderect(bird_rect) or bottom_rect.colliderect(bird_rect):
            state["phase"] = "game_over"
            break

    return state


def render(state):
    """Choose which screen to draw based on the current phase."""
    if state["phase"] == "start":
        draw_start_screen(state)
    elif state["phase"] == "running":
        draw_game(state)
    elif state["phase"] == "game_over":
        draw_game_over_screen(state)

    pygame.display.update()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    clock = pygame.time.Clock()
    state = make_initial_state()
    run   = True

    while run:
        clock.tick(60)
        state, run = handle_events(state)
        state      = update(state)
        render(state)

    pygame.quit()


if __name__ == "__main__":
    main()