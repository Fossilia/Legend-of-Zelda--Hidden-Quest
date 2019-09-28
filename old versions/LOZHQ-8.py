from pygame import*
from random import*
from math import*

init()
mixer.init()
font.init()
X=0
Y=1
guy = [0,0]
boost = [0,0]
pics = []
apics = []
doorRect = Rect(30,210,60,60)
screen = display.set_mode((800,600))
backPic = image.load("Images/maps/house.jpg").convert()
overPic = image.load("Images/maps/overworld.jpg").convert()
overPic=transform.scale(overPic, (int(overPic.get_width()*2.5),int(overPic.get_height()*2.5)))
linkPic = image.load("Images/link/link.jpg")
heart = image.load("Images/assets/heart.png")
heart = transform.smoothscale(heart,(30,25))
rupee = image.load("Images/assets/rupee.png")
rupee = transform.smoothscale(rupee,(33,25))
Hmask = image.load("Images/maps/HouseMask.jpg")
Omask = image.load("Images/maps/Omask.jpg")
Omask =transform.scale(Omask, (int(Omask.get_width()*2.5),int(Omask.get_height()*2.5)))
mask=Hmask
barrier = (254,0,0)
housepos=[125,100]
worldpos=[2040,500]
pos=housepos
push=False
health=6
keys = key.get_pressed()
unlock=True
house = True
attack = False
dire = 1
currentPic = backPic
frame2 = 0  #attack frame
frame=0     # current frame within the move
move=1      # current move being performed
stop = 8    # where the attack frame stops
rupees = 0

RIGHT = 0 # These are just the indicies of the moves
DOWN = 1  
UP = 2
LEFT = 3
haveSword = False

randY = [0]*30
randX = [0]*30
enemyXY = [[0,0],[0,0],[0,0]]
eRects = [0]*30
push = [[0,0],[0,0],[0,0]]
eHealth=[0]*30
eDmg=[0]*30
eX = [0]*30
eY = [0]*30
pause = False
ePause = [False]*30

for i in range(30):
    enemyXY.append([0,0])
    push.append([0,0])

gChupics = []
bChupics = []
eDelay = 15
eFrame = 0
eTime = [300]*30
eTurn = False

showT = False
pString = ""

frameDelay = 10
intialDelay = 5
myClock = time.Clock()

mixer.music.load('Sounds/music/House.mp3')
mixer.music.play(0,1.0)

playerRect = Rect(0,0,15,15)
hurtChu = image.load("Images/enemies/hurtChu.png")
hurtChu = transform.scale(hurtChu, (hurtChu.get_height()*2,hurtChu.get_width()*2))

running=True

#text------------------------------------------------------

def popText(text):
    myfont = font.SysFont('Comic Sans MS', 20)
    myfont2 = font.SysFont('Comic Sans MS', 15)
    pop = myfont.render(text, False, (255, 255, 255))
    pop2 = myfont2.render("Press space to close", False, (255, 255, 255))
    draw.rect(screen, (0,0,0),(250,350,300,100))
    draw.rect(screen, (255,255,255),(250,350,300,100),3)
    screen.blit(pop,(320,360))
    screen.blit(pop2,(380,420))

#barrier-------------------------------------------------------
    
def check(x,y):
    if x<0 or x >= mask.get_width() or y<0 or y >= mask.get_height():
        return False
    else:
        if mask.get_at((x,y)) == barrier:
            #print(mask.get_at((x,y)),guy[X],guy[Y])
            return False
        else:
           # print(mask.get_at((x,y)),guy[X],guy[Y])
            return True
        
#movement------------------------------------------------------

def moveGuy(guy):
    global move, frame, dire, stop, pause, boost
    keys = key.get_pressed()
    if pause == False and showT == False:
        newMove = -1
        if keys[K_RIGHT] and check(pos[X]+guy[X]+15,pos[Y]+guy[Y]):
            newMove = RIGHT
            dire = 14
            boost[X] = 15
            boost[Y] = 0
            stop = 6
            guy[X] += 2
        elif keys[K_DOWN] and check(pos[X]+guy[X],pos[Y]+guy[Y]+15):
            newMove = DOWN
            dire = 0
            boost[X] = 0
            boost[Y] = 15
            guy[Y] += 2
            stop = 8
        elif keys[K_UP] and check(pos[X]+guy[X],pos[Y]+guy[Y]-15):
            newMove = UP
            dire = 20
            boost[X] = 0
            boost[Y] = -15
            stop = 6
            guy[Y] -= 2
        elif keys[K_LEFT] and check(pos[X]+guy[X]-15,pos[Y]+guy[Y]):
            newMove = LEFT
            dire = 8
            boost[X] = -15
            boost[Y] = 0
            stop = 6
            guy[X] -= 2
        else:
            frame = 0

        if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame = frame + 0.2 # adding 0.2 allows us to slow down the animation
            if frame >= len(pics[move]):
                frame = 1
        elif newMove != -1:     # a move was selected
            move = newMove      # make that our current move
            frame = 1
    if pause == True:
        frame = 0
        if dire == 14:
            guy[X] -= 8
            # time.wait(500)
        if dire == 8:
            guy[X] += 8

        if dire == 0:
            guy[Y] -= 8

        if dire == 20:
            guy[Y] += 8
  
#frames-----------------------------------------------------
        
def makeMove(name,start,end,size):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        #redo = transform.scale(image.load("%s/%s%03d.png" % (name,name,i)),(50,80))
        move.append(transform.scale(image.load("%s/%s%03d.png" % (name,name,i)),(image.load("%s/%s%03d.png" % (name,name,i)).get_width()*size,image.load("%s/%s%03d.png" % (name,name,i)).get_height()*size)))
    return move

#changing place---------------------------------------------

def newLoc(Picture,newmask,newpos,camera,music,move):
    global unlock,mask,currentPic,pos,guy
    currentPic = Picture
    unlock = camera
    mask=newmask
    pos=newpos
    mixer.music.stop()
    guy[X]+=move
    mixer.music.load('Sounds/music/'+music+'.mp3')
    mixer.music.play(-1,0.0)
    screen.fill((0,0,0))
    display.flip()
    time.wait(500)
    
#hud---------------------------------------------------------

def hud():
    global heart,rupee,button,health,rupees
    for i in range(health):
        screen.blit(heart,(10+i*30,10))
    screen.blit(rupee,(710,10))
    myfont = font.SysFont('Comic Sans MS', 20)
    rupeeText = myfont.render(str(rupees), False, (255, 255, 255))
    screen.blit(rupeeText,(745,7))

#attack frames-----------------------------------------------

for i in range(8):
    apics.append(transform.scale(image.load("Images/link/attack-down/attack-down" + str(i) + ".png"),(image.load("Images/link/attack-down/attack-down" + str(i) + ".png").get_width()*2,image.load("Images/link/attack-down/attack-down" + str(i) + ".png").get_height()*2)))
for i in range(6):
    apics.append(transform.scale(image.load("Images/link/attack-side/attack-side" + str(i) + ".png"),(image.load("Images/link/attack-side/attack-side" + str(i) + ".png").get_width()*2,image.load("Images/link/attack-side/attack-side" + str(i) + ".png").get_height()*2)))
for i in range(8,14):
    apics.append(transform.flip(apics[i],True,False))
for i in range(6):
    apics.append(transform.scale(image.load("Images/link/attack-up/attack-up" + str(i) + ".png"),(image.load("Images/link/attack-up/attack-up" + str(i) + ".png").get_width()*2,image.load("Images/link/attack-up/attack-up" + str(i) + ".png").get_height()*2)))

#enemyframes--------------------------------------------------

for i in range(15):
        gChupics.append(transform.scale(image.load("images/enemies/G-chuchu/G-chuchu" + str(i) + ".png"),(image.load("images/enemies/G-chuchu/G-chuchu" + str(i) + ".png").get_width()*2,image.load("images/enemies/G-chuchu/G-chuchu" + str(i) + ".png").get_height()*2)))
        
for i in range(15):
        bChupics.append(transform.scale(image.load("images/enemies/B-chuchu/B-chuchu" + str(i) + ".png"),(image.load("images/enemies/B-chuchu/B-chuchu" + str(i) + ".png").get_width()*2,image.load("images/enemies/B-chuchu/B-chuchu" + str(i) + ".png").get_height()*2)))

#walking------------------------------------------------------
    
pics.append(makeMove("Link-",31,40,2))    # RIGHT
pics.append(makeMove("Link-",1,10,2))     # DOWN
pics.append(makeMove("Link-",21,30,2))    # UP
pics.append(makeMove("Link-",11,20,2))    # LEFT

#enemies------------------------------------------------------

def addEnemy(enemy,hurt, num, x, y, stop, speed, length, health):
    
    global epics, eDelay, eFrame, guy, eX, eY, eTime, eTurn, randX, randY, enemyXY,eRects, playerRect, dire, push, eHealth, eDmg, pause, ePause, pos
    
    eTime[num]-= 1
    eDelay-=1
    
    if eDelay == 0:
        eFrame+=1
        eDelay = 30
    if eFrame == stop:
        eFrame = 0
    if ePause[num] == False:
        if eTurn == True:
            if check(int(enemyXY[num][X])-pos[X],int(enemyXY[num][Y])-pos[Y]):
                print(check(int(enemyXY[num][X])-pos[X],int(enemyXY[num][Y])-pos[Y]))
                eY[num] += randY[num] * speed
            else:
                eY[num] -= randY[num] * speed
            #eY[num]+=randY[num]*speed
        if eTurn == False:
            if check(int(enemyXY[num][X])-pos[X],int(enemyXY[num][Y])-pos[Y]):
                print(check(int(enemyXY[num][X])-pos[X],int(enemyXY[num][Y])-pos[Y]))
                eX[num] += randX[num] * speed
            else:
                eX[num] -= randX[num] * speed
            #eX[num]+=randX[num]*speed
        if eTime[num] == 0:
            eTime[num] = length
            eTurn = not eTurn
            randY[num] = randint(-1,1)
            randX[num] = randint(-1,1)
            if randY[num]==-1 and eY[num]<-150:
                randY[num]=1
            if randY[num]==1 and eY[num]>200:
                randY[num]=-1
            if randX[num]==-1 and eX[num]<-150:
                randX[num]=1
            if randX[num]==1 and eX[num]>200:
                randX[num]=-1

    if ePause[num] == True:
         enemy = hurt
         if dire == 14:
             push[num][X] += 10
             #eDmg[num] += 1

         if dire == 8:
             push[num][X] -= 10
             #eDmg[num] += 1

         if dire == 0:
             push[num][Y] += 10
             #eDmg[num] += 1

         if dire == 20:
             push[num][Y] -= 10

    enemyXY[num]=[-guy[X]+x+eX[num]/2+push[num][X],-guy[Y]+y+eY[num]/2+push[num][Y]]
    eRects[num]=enemy.get_rect()
    eRects[num]=eRects[num].move(enemyXY[num][X],enemyXY[num][Y])
    
    #newP = playerRect.move(-guy[X]-x,-guy[Y]-y)

    if eRects[num].colliderect(playerRect):
        collide(eRects[num],1,num)
        #print("hit")
    eHealth[num] = health-eDmg[num]
   # print(eHealth)
    #draw.rect(screen, (0,0,0),playerRect)
    #draw.rect(screen, (0,0,0),eRects[num])
    #print(eRects[0],playerRect)
    if eHealth[num]>0:
        screen.blit(enemy,(enemyXY[num][X],enemyXY[num][Y]))
    #print(eY[num])


# collision--------------------------------------------------

def collide(rect, dmg, num):
    global health, attack, push, eDmg, eHealth, frame2, pause, colNum, ePause, rupees
    
    if eHealth[num]>0:
    
        if attack == False:
            pause = True
            sound2 = mixer.Sound("sounds/Hurt.wav")
            sound2.play()
            time.set_timer(K_PAUSE, 80)
            health-=dmg
    
    
        if attack == True:
            ePause[num] = True
            time.set_timer(K_PAUSE, 80)
            sound2 = mixer.Sound("sounds/Hit.wav")
            sound2.play()
            eDmg[num]+=1
            if eHealth[num] == 1:
                rand = randint(0,2)
                if rand == 0 and 6>health:
                    health+=1
                    sound2 = mixer.Sound("sounds/Heart.wav")
                    sound2.play()
                elif rand == 2:
                    rupees+=randint(1,5)
                    sound2 = mixer.Sound("sounds/Rupee.wav")
                    sound2.play()
                    print(rupees)
                else:
                    sound2 = mixer.Sound("sounds/Die.wav")
                    sound2.play()


while running:
    for evt in event.get():
        if evt.type == K_PAUSE:
            pause = False
            ePause = [False]*30
        if evt.type==QUIT:
            running=False
       
    keys = key.get_pressed()
    
    
    
    gChuchu = gChupics[eFrame]
    bChuchu = bChupics[eFrame]
    
    #print(bChuRect,gChuRect)
    #if playerRect.colliderect(bChuRect):
        #print("Hit")
    
   #Rect.colliderect

    gChuchu = gChupics[eFrame]
    bChuchu = bChupics[eFrame]
    pic = pics[move][int(frame)]
    if attack == False:
        playerRect = Rect(0, 0, 30, 40)
    bChuRect = bChuchu.get_rect()
    gChuRect = gChuchu.get_rect()

    pic = pics[move][int(frame)]

#Indoor-----------------------------------------------------
    
    if unlock==True:
        screen.blit(currentPic, (150,100))
        if attack == False:
            intialDelay=5
            pic = pics[move][int(frame)]
            screen.blit(pic,(275+guy[X]-pic.get_width()//2,190+guy[Y]-pic.get_height()//2))
            playerRect=playerRect.move(275+guy[X],190+guy[Y])
            #print(playerRect)
            moveGuy(guy)
        hud()

    else:
       intialDelay = 5
       screen.blit(currentPic, (-guy[X] - 1645, -guy[Y] - 190))
       # print(playerRect)
       if attack == False:
           moveGuy(guy)
           pic = pics[move][int(frame)]
           screen.blit(pic, (400 - pic.get_width() // 2, 300 - pic.get_height() // 2))
           playerRect = playerRect.move(400 - pic.get_width() // 2, 300 - pic.get_height() // 2)
           # print(playerRect)
           
       addEnemy(gChuchu, hurtChu, 0, 100, 500, 15, 1, randint(300, 700), 1)
       addEnemy(bChuchu, hurtChu, 1, -200, 600, 15, 1, randint(300, 500), 3)
       addEnemy(bChuchu, hurtChu, 2, -200, 600, 15, 1, randint(300, 500), 4)
       addEnemy(bChuchu, hurtChu, 3, -300, 600, 15, 1, randint(300, 500), 3)
       addEnemy(bChuchu, hurtChu, 4, -100, 600, 15, 6, randint(300, 500), 8)
       hud()
       #display.flip()
       
       #doorRect = Rect(30-guy[X],210-guy[Y],60,60)

#doors------------------------------------------------------
    #draw.rect(screen,(0,0,255),doorRect,3)
    
    if guy[X] > 105 and guy[X] < 138 and guy[Y] == 264 and currentPic == backPic:
        sound2 = mixer.Sound("sounds/Door.wav")
        sound2.play()
        newLoc(overPic,Omask,worldpos,False,"Outside",10)
        
    elif guy[X] > 105 and guy[X] < 138 and guy[Y] == 254 and currentPic == overPic:
        sound2 = mixer.Sound("sounds/Door.wav")
        sound2.play()
        newLoc(backPic,Hmask,housepos,True,"House",-10)
        
    elif guy[X] > 270 and guy[X] < 300 and guy[Y] == 210 and currentPic == backPic and keys[K_x] and haveSword == False and dire == 20:
        haveSword = True
        showT = True
        pString = "You got a Sword!"
        
        
    if showT:
        popText(pString)
        if keys[K_SPACE]:
            showT = False
        
#attack------------------------------------------------------
    
    if keys[K_SPACE] and haveSword:
        attack = True

        
    if attack:
        playerRect = apics[frame2+dire].get_rect()
        if unlock == True :
            screen.blit(apics[frame2+dire],(270+guy[X]-apics[frame2].get_width()//2,195+guy[Y]-apics[frame2].get_width()//2))
            playerRect = playerRect.move(boost[X] + 270+guy[X]-apics[frame2].get_width()//2,boost[Y] + 195+guy[Y]-apics[frame2].get_width()//2)
        if unlock == False:
           screen.blit(apics[frame2 + dire],(400 - apics[frame2].get_width() // 2, 300 - apics[frame2].get_width() // 2))
           playerRect = playerRect.move(boost[X] + 400 - apics[frame2].get_width() // 2,boost[Y] + 300 - apics[frame2].get_width() // 2)
        display.flip()
        frameDelay -= 1                         # count down to zero
        if frameDelay == 0:                     # then advance frame like normal
            frameDelay = intialDelay
            frame2 += 1
            if frame2 == stop:
                attack = False
                frame2 = 0
                playerRect = pic.get_rect()

        #end---------------------------------------------------------
                
    myClock.tick(100)
    display.flip()
quit()
