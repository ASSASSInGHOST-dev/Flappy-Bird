import pygame
import random
import sys
import os
import math

pygame.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

BG = pygame.transform.scale(
    pygame.image.load(resource_path("BG.jpg")), (WIDTH, HEIGHT)
)

player_width = 110
player_height = 65
JUMP_strength = -8
gravity = 0.5

pipe_width = 70
pipe_gap = 180
pipe_speed = 3

cap_height = 25
cap_width = pipe_width + 24

score_font = pygame.font.SysFont('bauhaus93', 60)
Game_Over_Font = pygame.font.SysFont('bauhaus93', 90)
final_font = pygame.font.SysFont('comicsans', 45)
re_play = pygame.font.SysFont('comicsans', 35)
start_font = pygame.font.SysFont('bauhaus93', 100)

bird = pygame.transform.scale(
    pygame.image.load(resource_path("bird.png")), (player_width, player_height)
)

surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
surface.fill((40, 40, 40, 180))

def draw(player, player_x, player_y, pipes, score):
    WIN.blit(BG, (0, 0))

    WIN.blit(player, (player_x, player_y))

    for pipe in pipes:

        pygame.draw.rect(WIN, (0, 130, 0), (pipe["x"], 0, pipe_width, pipe["top_height"]))      #top pipe border
    
        pygame.draw.rect(WIN, (0, 130, 0), (pipe["x"], pipe["bottom_y"], pipe_width, HEIGHT - pipe["bottom_y"]))        #bottom pipe border
        
        pygame.draw.rect(WIN, (0, 205, 0), (pipe["x"] + 4, 4, pipe_width - 8, pipe["top_height"] - 8))      #top pipe main body
    
        pygame.draw.rect(WIN, (0, 205, 0), (pipe["x"] + 4, pipe["bottom_y"] + 4, pipe_width - 8, HEIGHT - pipe["bottom_y"] -8))    #bottom pipe main body

        #3D feel with subtle highlight
        pygame.draw.rect(WIN, (120, 255, 120), (pipe["x"] + 8, 4, 10, pipe["top_height"] - 8))

        pygame.draw.rect(WIN, (120, 255, 120), (pipe["x"] + 8, pipe["bottom_y"] + 4, 10, HEIGHT - pipe["bottom_y"] -8))
        
        top_cap_y = pipe["top_height"] - cap_height
        
        pygame.draw.rect(WIN, (0, 180, 0), (pipe["x"] - 12, top_cap_y, cap_width, cap_height))      #top pipe cap

        pygame.draw.rect(WIN, (0, 180, 0), (pipe["x"] - 12, pipe["bottom_y"], cap_width, cap_height))   #bottom pipe cap

        #border on pipe capes
        pygame.draw.rect(WIN, (0, 130, 0), (pipe["x"] - 12, top_cap_y, cap_width, cap_height), width=4)
        
        pygame.draw.rect(WIN, (0, 130, 0), (pipe["x"] - 12, pipe["bottom_y"], cap_width, cap_height), width=4)
    
    shadow = score_font.render(f"SCORE: {score}", True, (0, 0, 0))

    score_disp = score_font.render(f"SCORE: {score}", True, (255, 215, 0))

    WIN.blit(shadow, (WIDTH // 2 -76, 34))
    WIN.blit(score_disp, (WIDTH // 2 - 80, 30)) 
 
def Game_Over_Screen(state, score):
     Game_Over = Game_Over_Font.render(f"GAME OVER!", True, (255, 50, 50))
     Game_Over_Shadow = Game_Over_Font.render(f"GAME OVER!", True, (0, 0, 0))
     final_score = final_font.render(f"FINAL SCORE:{score}", True, (255, 255, 0))
     fs_shadow = final_font.render(f"FINAL SCORE:{score}", True, (0, 0, 0))
     replay = re_play.render(f"Press Space Bar to restart again", True, (255, 255, 255))
     replay_sh = re_play.render(f"Press Space Bar to restart again", True, (0, 0, 0))
     
     if state == "game_over":
         WIN.blit(surface, (0, 0))
         WIN.blit(Game_Over_Shadow, ((WIDTH - Game_Over_Shadow.get_width()) // 2, HEIGHT // 3))
         WIN.blit(Game_Over, ((WIDTH - Game_Over.get_width()) // 2 - 8, HEIGHT // 3))
         WIN.blit(fs_shadow, ((WIDTH - fs_shadow.get_width()) // 2 + 4, HEIGHT // 2 + 34))
         WIN.blit(final_score, ((WIDTH - final_score.get_width()) // 2 , HEIGHT // 2 + 30 ))
         WIN.blit(replay_sh, ((WIDTH - replay_sh.get_width()) // 2 + 2, HEIGHT // 2 + 84))
         WIN.blit(replay, ((WIDTH - replay.get_width()) // 2, HEIGHT // 2 + 82))

def start_screen(state):
    start_scr = start_font.render(f"Flappy Bird", True, (255, 215, 0))
    shadow = start_font.render("Flappy Bird", True, (0, 0, 0))
    start = re_play.render(f"Press Space Bar to start!", True, (255, 255, 255))
    start_sh = re_play.render(f"Press Space Bar to start!", True, (0, 0, 0))
    
    if state == "start":
        WIN.blit(surface, (0, 0))
        WIN.blit(shadow, ((WIDTH - start_scr.get_width()) // 2 + 4, HEIGHT // 3 + 4))
        WIN.blit(start_scr, ((WIDTH - start_scr.get_width()) // 2, HEIGHT // 3))
        WIN.blit(start_sh, ((WIDTH - start_sh.get_width()) // 2 + 2, HEIGHT // 2 + 84))
        WIN.blit(start, ((WIDTH - start.get_width()) // 2, HEIGHT // 2 + 82))

def main():
    run = True

    player = bird

    score = 0

    state = "start"

    clock = pygame.time.Clock()

    player_x = 75
    player_y = 200

    floor_y = HEIGHT - 80

    player_vel = 0

    pipes = []
    pipe_count = 0
    pipe_increment = 90

    max_jump = 65
    max_fall = 70
   
    while run:
        clock.tick(60)
        pipe_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if state == "start":
                        state = "running"
                    elif state == "running":
                        player_vel = JUMP_strength
                        player_y += 12
                    elif state == "game_over":
                        state = "running"

                        score = 0
                        
                        player_x = 75
                        player_y = 200

                        floor_y = HEIGHT - 80

                        player_vel = 0

                        pipes = []
                        pipe_count = 0
                        pipe_increment = 90

        
        if state == "running":
            if pipe_count > pipe_increment:
                pipe_count = 0
            
                top_height = random.randint(150, 400)
                new_pipe = {
                    "x": WIDTH,
                    "top_height": top_height,
                    "bottom_y": top_height + pipe_gap,
                    "passed": False
                }
                pipes.append(new_pipe)
            
        
            for pipe in pipes:
                pipe["x"] -= pipe_speed
        
            for pipe in pipes[:]:
                if pipe["x"] < -pipe_width:
                    pipes.remove(pipe)

            for pipe in pipes:
                if not pipe.get("passed", False) and pipe["x"] + pipe_width < player_x:
                    score +=1
                    pipe["passed"] = True

            player_vel += gravity
            player_y += -12
            player_y += player_vel
            if player_y >= floor_y:
                player_y = floor_y
                player_vel = 0

            bird_rect = pygame.Rect(player_x, player_y + 8, player_width - 15, player_height - 12)

            for pipe in pipes[:]:
                #rect for top pipe
                top_pipe_rect = pygame.Rect(
                    pipe["x"],
                    0,
                    pipe_width,
                    pipe["top_height"]
                )

                #rect for bottom pipe
                bottom_pipe_rect = pygame.Rect(
                    pipe["x"],
                    pipe["bottom_y"],
                    pipe_width,
                    HEIGHT - pipe["bottom_y"]
                )

                if top_pipe_rect.colliderect(bird_rect) or bottom_pipe_rect.colliderect(bird_rect):
                    state = "game_over"
                    break        
        
        if state == "start":
            WIN.blit(BG, (0, 0))
            floating_y = 200 + 12 * math.sin(pygame.time.get_ticks() * 0.004)
            WIN.blit(player, (player_x, floating_y))
            start_screen(state)

        elif state == "running":
            draw(player, player_x, player_y, pipes, score)

        elif state == "game_over":
            draw(player, player_x, player_y, pipes, score)
            Game_Over_Screen(state, score)

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()