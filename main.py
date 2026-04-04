import pygame
import random

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

BG = pygame.transform.scale(pygame.image.load("BG.jpg"), (WIDTH, HEIGHT))

player_width = 55
player_height = 40
JUMP_strength = -6.25
gravity = 0.5

pipe_width = 70
pipe_gap = 180
pipe_speed = 3

cap_height = 25
cap_width = pipe_width + 24

bird = pygame.transform.scale(pygame.image.load("bird.png"), (player_width, player_height))

def draw(player, player_x, player_y, pipes):
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

    pygame.display.update() 
 
def main():
    run = True

    player = bird

    clock = pygame.time.Clock()

    player_x = 75
    player_y = 200

    floor_y = HEIGHT - 80

    player_vel = 0

    pipes = []
    pipe_count = 0
    pipe_increment = 90

    hit = False
   
    while run:
        clock.tick(60)
        pipe_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        if not hit:
        
            if pipe_count > pipe_increment:
                pipe_count = 0
            
                top_height = random.randint(150, 400)
                new_pipe = {
                    "x": WIDTH,
                    "top_height": top_height,
                    "bottom_y": top_height + pipe_gap
                }
                pipes.append(new_pipe)
            
        
            for pipe in pipes:
                pipe["x"] -= pipe_speed
        
            for pipe in pipes[:]:
                if pipe["x"] < -pipe_width:
                    pipes.remove(pipe)

        
            jump = pygame.key.get_pressed()
            if jump[pygame.K_SPACE] and player_y + JUMP_strength >= 0:
                player_vel = JUMP_strength
    
            player_vel += gravity
            player_y += player_vel
            if player_y >= floor_y:
                player_y = floor_y
                player_vel = 0
        
            bird_rect = pygame.Rect(player_x, player_y, player_width, player_height)

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
                    hit = True
                    break

        draw(player, player_x, player_y, pipes)

    pygame.quit()

if __name__ == "__main__":
    main()