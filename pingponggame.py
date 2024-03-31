from pygame import *
init()
'''Required classes'''


#parent class for sprites
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height)) #e.g. 55,55 - parameters
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update_player1(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_player2(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    


#game scene:
back = (200, 255, 255) #background color (background)
win_width = 800
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)
clock = time.Clock()

speed_x = 3
speed_y = 3

#flags responsible for game state


FPS = 60


#creating ball and paddles   
racket1 = Player('platform.png', 30, 200, 4, 50, 150) 
racket2 = Player('platform.png', win_width - 80, 200, 4, 50, 150)
ball = GameSprite('ball.png', 200, 200, 4, 50, 50)


font.init()
font = font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

mixer.init()
mixer.music.load('backmusic.ogg')
mixer.music.play(-1)
lose = mixer.Sound('die.ogg')


game = True
finish = False
touch = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        ''' Place objects on the window '''
        window.fill(back)
        racket1.reset()
        racket2.reset()
        ball.reset()
        racket1.update_player1()
        racket2.update_player2()
        
        ''' Movement of ball '''
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        #if the ball reaches screen edges, change its movement direction
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1
        
        ''' Collision '''
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
        
            if speed_x > 0:
                speed_x += 1
                speed_y += 1
            else:
                speed_x -= 1
                speed_y -= 1
            # touch += 1
            # if touch >= 3 and touch < 10:
            #     change += 5
        
        # elif touch >= 10 and touch < 15:
        #     speed_x += 1
        #     speed_y += 1
        # else:
        #     speed_x += 1
        #     speed_y += 1
        ''' Win-lose '''
        #if ball flies behind this paddle, display loss condition for player 1
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            lose.play()
            mixer.music.stop()
            
        #if ball flies behind this paddle, display loss condition for player 2
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            lose.play()
            mixer.music.stop()


    display.update()
    clock.tick(60)


