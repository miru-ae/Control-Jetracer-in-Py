import pygame, sys, time, random
from pygame.locals import *

# 라이브러리 초기화
pygame.init()
mainClock = pygame.time.Clock()
while True:
#디스플레이 설정
    WINDOWWIDTH = 600
    WINDOWHEIGHT = 600
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('피하면서 먹기')

    #먹이 설정
    NEWFOOD = 50
    FOODSIZE = 10
    foods = []
    for i in range(20):
         foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

    # 색깔 설정
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    INDIGO = (75,0,130)
    PINK = (255,105,180)
    YELLOW = (255,255,0)

    # 움직임 변수 설정
    DOWNLEFT = 1
    DOWNRIGHT = 3
    UPLEFT = 7
    UPRIGHT = 9
    DOWN = 2
    UP = 8
    RIGHT = 6
    LEFT = 4

    MOVESPEED = 7

    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False

    MOVESPEEDY = 3

    player = pygame.Rect(300, 300, 40, 40)

    #여러가지 함수 설정
    def terminate():
        pygame.quit()
        sys.exit()

    def waitForPlayerToPressKey():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()
                    return 5
                    
    def drawText(text, font, surface, x, y):
        textobj = font.render(text, 1, WHITE)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        surface.blit(textobj, textrect)



    font = pygame.font.SysFont(None, 48)

    # 블록데이터를 설정
    b1 = {'rect':pygame.Rect(300, 80, 100, 100), 'color':RED, 'dir':UPRIGHT}
    b2 = {'rect':pygame.Rect(200, 200, 20, 20), 'color':GREEN, 'dir':UPLEFT}
    b3 = {'rect':pygame.Rect(100, 150, 60, 60), 'color':BLUE, 'dir':DOWNLEFT}
    b4 = {'rect':pygame.Rect(250, 350, 30, 30), 'color':WHITE, 'dir':DOWN}
    b5 = {'rect':pygame.Rect(400, 250, 50, 103), 'color':INDIGO, 'dir':RIGHT}
    blocks = [b1, b2, b3, b4, b5]
    play = [player]
    prey1 = b1['rect']
    prey2 = b2['rect']
    prey3 = b3['rect']
    prey4 = b4['rect']
    prey5 = b5['rect']

    #게임 이미지
    gameset = pygame.Rect(150, 150, 350, 350)
    setimage = pygame.image.load('gm.png')
    stretchedimage = pygame.transform.scale(setimage, (350,350))
    gameclear = pygame.Rect(150, 50, 350, 350)
    clearimg = pygame.image.load('gameend.png')
    stretchimg = pygame.transform.scale(clearimg, (350,500))


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        # 바탕 검은 색
        windowSurface.fill(BLACK)

        for b in blocks:
            # 블록 움직이기
            if b['dir'] == DOWNLEFT:
                b['rect'].left -= MOVESPEED
                b['rect'].top += MOVESPEED
            if b['dir'] == DOWNRIGHT:
                b['rect'].left += MOVESPEED
                b['rect'].top += MOVESPEED
            if b['dir'] == UPLEFT:
                b['rect'].left -= MOVESPEED
                b['rect'].top -= MOVESPEED
            if b['dir'] == UPRIGHT:
                b['rect'].left += MOVESPEED
                b['rect'].top -= MOVESPEED
            if b['dir'] == DOWN:
                b['rect'].top -= MOVESPEED
            if b['dir'] == UP:
                b['rect'].top += MOVESPEED
            if b['dir'] == LEFT:
                b['rect'].left -= MOVESPEED
            if b['dir'] == RIGHT:
                b['rect'].left += MOVESPEED

            # 블록 벽에 튕기기
            if b['rect'].top < 0:
                if b['dir'] == UPLEFT:
                    b['dir'] = DOWNLEFT
                if b['dir'] == UPRIGHT:
                    b['dir'] = DOWNRIGHT
                if b['dir'] == DOWN:
                    b['dir'] = UP
            if b['rect'].bottom > WINDOWHEIGHT:
                if b['dir'] == DOWNLEFT:
                    b['dir'] = UPLEFT
                if b['dir'] == DOWNRIGHT:
                    b['dir'] = UPRIGHT
                if b['dir'] == UP:
                    b['dir'] = DOWN
            if b['rect'].left < 0:
                if b['dir'] == DOWNLEFT:
                    b['dir'] = DOWNRIGHT
                if b['dir'] == UPLEFT:
                    b['dir'] = UPRIGHT
                if b['dir'] == LEFT:
                    b['dir'] = RIGHT
            if b['rect'].right > WINDOWWIDTH:
                if b['dir'] == DOWNRIGHT:
                    b['dir'] = DOWNLEFT
                if b['dir'] == UPRIGHT:
                    b['dir'] = UPLEFT
                if b['dir'] == RIGHT:
                    b['dir'] = LEFT
            pygame.draw.rect(windowSurface, b['color'], b['rect'])

            #키보드로 조종
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                     
            if moveDown and player.bottom < WINDOWHEIGHT:
                player.top += MOVESPEEDY
            if moveUp and player.top > 0:
                player.top -= MOVESPEEDY
            if moveLeft and player.left > 0:
                player.left -= MOVESPEEDY
            if moveRight and player.right < WINDOWWIDTH:
                player.right += MOVESPEEDY

            #먹이 먹기
            for food in foods[:]:
                if player.colliderect(food):
                    foods.remove(food)

            for i in range(len(foods)):
                pygame.draw.rect(windowSurface, PINK, foods[i])

            end=0
            if player.colliderect(prey1) or player.colliderect(prey2) or player.colliderect(prey3) or player.colliderect(prey4) or player.colliderect(prey5):
                windowSurface.blit(stretchedimage,gameset)
                pygame.display.update()
                #terminate()
                drawText(str(waitForPlayerToPressKey()),font,windowSurface,0,0)
                end=waitForPlayerToPressKey()
                break

            if len(foods) == 0:
                windowSurface.blit(stretchimg,gameclear)
                pygame.display.update()
                time.sleep(2)
                drawText(str(waitForPlayerToPressKey()),font,windowSurface,0,0)
                end=waitForPlayerToPressKey()
                break

        if end==5:
            break
        #플레이어 그리기        
        pygame.draw.rect(windowSurface, YELLOW, player)

        # 화면에 띄우기
        pygame.display.update()
        time.sleep(0.02)
        mainClock.tick(40)