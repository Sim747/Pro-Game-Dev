import pygame 
import os
pygame.font.init()

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Meow")

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)

BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)

HEALTH_FONT = pygame.font.SysFont('Arial',40)
WINNER_FONT = pygame.font.SysFont('Arial',100)

MEOW = "meow.png"
FPS = 60
VEL = 5
MEOW_VEL = 7
MAX_MEOW = 3
BLACK_CAT_WIDTH,BLACK_CAT_HEIGHT = 55,40
GREY_CAT_WIDTH,GREY_CAT_HEIGHT = 55,40

#events
GREY_CAT_HIT = pygame.USEREVENT + 1
BLACK_CAT_HIT = pygame.USEREVENT + 2

GREY_CAT_IMAGE = pygame.image.load(os.path.join("cat.png"))
GREY_CAT = pygame.transform.rotate(pygame.transform.scale(GREY_CAT_IMAGE,(GREY_CAT_WIDTH,GREY_CAT_HEIGHT)),90)

BLACK_CAT_IMAGE = pygame.image.load(os.path.join("spaceship2.png "))
BLACK_CAT = pygame.transform.rotate(pygame.transform.scale(BLACK_CAT_IMAGE,(BLACK_CAT_WIDTH,BLACK_CAT_HEIGHT)),270)

GRASS = pygame.transform.scale(pygame.image.load(os.path.join("backgroundgrass.jpg")),(WIDTH,HEIGHT))

def draw_window(GREY,BLACK,BLACK_bullets,GREY_bullets,BLACK_health,GREY_health):
    WIN.blit(GRASS,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    BLACK_CAT_health_text = HEALTH_FONT.render("Health:"+str(BLACK_health),1,WHITE)
    GREY_CAT_health_text = HEALTH_FONT.render("Health:"+str(GREY_health),1,WHITE)
    WIN.blit(BLACK_CAT_health_text,(WIDTH-BLACK_CAT_health_text.get_width()-10,10))
    WIN.blit(GREY_CAT_health_text,(10,10))

    WIN.blit(GREY_CAT,(GREY.x,GREY.y))
    WIN.blit(BLACK_CAT,(BLACK.x,BLACK.y))

    for bullet in BLACK_bullets:
        pygame.draw.rect(WIN,BLACK,bullet)
   
    for bullet in GREY_bullets:
        pygame.draw.rect(WIN,GREY,bullet)
    
    
    pygame.display.update()

def GREY_handle_movement(keys_pressed,GREY):
    if keys_pressed[pygame.K_LEFT] and GREY.x - VEL > 0:
        GREY.x = GREY.x - VEL
    if keys_pressed[pygame.K_RIGHT] and GREY.x - VEL + GREY.width < BORDER.x:
        GREY.x = GREY.x + VEL
    if keys_pressed[pygame.K_UP] and GREY.y - VEL > 0:
        GREY.y = GREY.y - VEL
    if keys_pressed[pygame.K_DOWN] and GREY.y + VEL + GREY.height < HEIGHT -15:
        GREY.y = GREY.y + VEL


def BLACK_handle_movement(keys_pressed,BLACK):
    if keys_pressed[pygame.K_a] and BLACK.x - VEL > BORDER.x + BORDER.width:
        BLACK.x = BLACK.x - VEL
    if keys_pressed[pygame.K_d] and BLACK.x + VEL + BLACK.width < WIDTH:
        BLACK.x = BLACK.x + VEL
    if keys_pressed[pygame.K_w] and BLACK.y - VEL > 0:
        BLACK.y = BLACK.y - VEL
    if keys_pressed[pygame.K_s] and BLACK.y + VEL + BLACK.height < HEIGHT -15:
        BLACK.y = BLACK.y + VEL

def handle_bullets(GREY_bullets,BLACK_bullets,GREY,BLACK):
    for MEOW in GREY_bullets:
        MEOW.x = MEOW.x + MEOW_VEL
        if BLACK.colliderect(MEOW):
          pygame.event.post(pygame.event.Event(BLACK_CAT_HIT))
          GREY_bullets.remove(MEOW)
        elif MEOW.x > WIDTH:
          GREY_bullets.remove(MEOW)

    for MEOW in BLACK_bullets:
        MEOW.x = MEOW.x - MEOW_VEL
        if GREY.colliderect(MEOW):
          pygame.event.post(pygame.event.Event(GREY_CAT_HIT))
          BLACK_bullets.remove(MEOW)
        elif MEOW.x < 0 :
          BLACK_bullets.remove(MEOW)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2 -draw_text.get_width()/2,
                        HEIGHT/2 -draw_text.get_width()/2))

    pygame.display.update()
    pygame.time.delay(5000)



    


def main():
   BLACK = pygame.Rect(700,300,BLACK_CAT_WIDTH,BLACK_CAT_HEIGHT)
   GREY = pygame.Rect(100,300,GREY_CAT_WIDTH,GREY_CAT_HEIGHT)

   BLACK_bullets = []
   GREY_bullets = []

   BLACK_CAT_health = 10
   GREY_CAT_health = 10
   
   clock = pygame.time.Clock()
   run = True
   while run:
       clock.tick(FPS)
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               run = False
               pygame.quit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_LCTRL and len(GREY_bullets) < MAX_MEOW:
                bullet = pygame.Rect(GREY.x + GREY.width,GREY.y + GREY.height//2-2,10,5)
                GREY_bullets.append(MEOW) 
               if event.key == pygame.K_LCTRL and len(BLACK_bullets) < MAX_MEOW:
                MEOW = pygame.Rect(BLACK.x,BLACK.y + BLACK.height//2-2,10,5)
                BLACK_bullets.append(MEOW)

           if event.type == BLACK_CAT_HIT:
                BLACK_CAT_health = BLACK_CAT_health - 1 
            
           if event.type == GREY_CAT_HIT:
                GREY_CAT_health= GREY_CAT_health -1
        
       winner_text = " "
       if BLACK_CAT_health <= 0:
            winner_text = "grey cat Wins"
       if GREY_CAT_health <= 0:
            winner_text = "black cat Wins"
       if winner_text != " ":
            draw_winner(winner_text)
            break 


       keys_pressed = pygame.key.get_pressed()
       GREY_handle_movement(keys_pressed,GREY)
       BLACK_handle_movement(keys_pressed,BLACK)
       handle_bullets(GREY_bullets,BLACK_bullets,GREY,BLACK)
       draw_window(BLACK,GREY,BLACK_bullets,GREY_bullets,BLACK_CAT_health,GREY_CAT_health)


   main()

if __name__ == "__main__":
   main()    