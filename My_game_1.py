import pygame
import sys
import random

pygame.init()

screen=pygame.display.set_mode((512,768))

screen_width=screen.get_width()
screen_height=screen.get_height()

pygame.display.set_caption('无聊的游戏')

background=pygame.image.load("D:\\33838\\OneDrive - MSFT\\桌面\\pygame\\AnimatedStreet.png")
background=pygame.transform.scale(background,(screen_width,screen_height))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("D:\\33838\\OneDrive - MSFT\\桌面\\pygame\\Player.png")
        self.width=self.image.get_width()
        self.height=self.image.get_height()

        self.x=screen_width/2
        self.y=screen_height-self.height-20

        self.rect=self.image.get_rect(center=(self.x,self.y))

        self.speed=10

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("D:\\33838\\OneDrive - MSFT\\桌面\\pygame\\Enemy.png")
        
        x=screen_width/2
        y=0

        self.rect=self.image.get_rect(center=(x,y))

        self.speed_=random.randint(10,20)
    
    def move(self):
        self.rect.move_ip(0,self.speed_)
        if self.rect.y>screen_height:
            self.rect.y=-self.rect.height
            self.rect.x=random.randint(0,screen_width-self.rect.width)
            self.speed_=random.randint(10,20)

# 加载背景音乐
music=pygame.mixer.Sound("D:\\33838\\OneDrive - MSFT\\桌面\\pygame\\background.wav")
# 播放音乐
# play(num) 默认为0，表示播放一次  -1 表示无限循环
music.play(-1)

crash=pygame.mixer.Sound("D:\\33838\\OneDrive - MSFT\\桌面\\pygame\\crash.wav")

font_big=pygame.font.SysFont("楷体",60)
game_over=font_big.render("GAME OVER",True,"#FF0000")

running=True

player=Player()
enemy_list=[]
enemies=pygame.sprite.Group()
for i in range(3):
    enemy=Enemy()
    enemy_list.append(enemy)
    # 定义敌人精灵组，将所有的敌人收到精灵组中
    enemies.add(enemy)

FPS=60
CLOCK=pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 碰撞检测
    # pygame.sprite.spritecollide(做碰撞检测的对象,精灵组,False)
    hit=pygame.sprite.spritecollide(player,enemies,False)
    # print(hit)
    # False 碰撞后玩家和被碰撞的敌人依旧存在精灵组里面，继续做碰撞检测
    # True 碰撞之后，被碰撞的精灵组中的敌人会从精灵组中移除，就不再做碰撞检测了
    
    screen.blit(background,(0,0))
    screen.blit(player.image,player.rect)

    if hit:
        crash.play()
        screen.blit(game_over,(125,350))
        running=False

    for enemy in enemy_list:
        screen.blit(enemy.image,enemy.rect)
        if running==True:
            enemy.move()

    if running==True:
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            if player.rect.y<=0:
                player.rect.y=0
            else:    
                player.rect.move_ip(0,-player.speed)
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            if player.rect.y>=screen_height-player.height:
                player.rect.y=screen_height-player.height
            else:    
                player.rect.move_ip(0,player.speed)
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            if player.rect.x<=0:
                player.rect.x=0
            else:
                player.rect.move_ip(-player.speed,0)
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            if player.rect.x>=screen_width-player.width:
                player.rect.x=screen_width-player.width
            else:    
                player.rect.move_ip(player.speed,0)

    pygame.display.update()
    CLOCK.tick(FPS)