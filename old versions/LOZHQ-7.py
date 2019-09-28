from pygame import*
from random import*
from math import*

init()
mixer.init()
X=0
Y=1
guy = [0,0]
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

RIGHT = 0 # These are just the indicies of the moves
DOWN = 1  
UP = 2
LEFT = 3

frameDelay = 10
intialDelay = 5
myClock = time.Clock()

mixer.music.load('Sounds/music/House.mp3')
mixer.music.play(0,1.0)

#outside------------------------------------------------------

def drawScene(screen,guy):
    """ draws the current state of the game """
    global intialDelay, playerRect
    intialDelay=5
    screen.blit(currentPic, (-guy[X]-1645,-guy[Y]-190))
    #print(playerRect)
    if attack==False:
        pic = pics[move][int(frame)]
        screen.blit(pic,(400-pic.get_width()//2,300-pic.get_height()//2))
        playerRect=playerRect.move(400-pic.get_width()//2,300-pic.get_height()//2)
        #print(playerRect)
    if attack == True: 
        screen.blit(apics[frame2+dire],(400-apics[frame2].get_width()//2,300-apics[frame2].get_width()//2))
        playerRect = playerRect.move(400-apics[frame2].get_width()//2,300-apics[frame2].get_width()//2)
    addEnemy(gChuchu, 0, 100, 500, 15, 1, randint(300,700),1)
    addEnemy(bChuchu, 1, -200, 600, 15, 1, randint(300,500),3)
    hud()
    display.flip()

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
    global move, frame, dire, stop, pause
    keys = key.get_pressed()
    if pause[0]==False:
        newMove = -1
        if keys[K_RIGHT] and check(pos[X]+guy[X]+15,pos[Y]+guy[Y]):
            newMove = RIGHT
            dire = 14
            stop = 6
            guy[X] += 2
        elif keys[K_DOWN] and check(pos[X]+guy[X],pos[Y]+guy[Y]+15):
            newMove = DOWN
            dire = 0
            guy[Y] += 2
            stop = 8
        elif keys[K_UP] and check(pos[X]+guy[X],pos[Y]+guy[Y]-15):
            newMove = UP
            dire = 20
            stop = 6
            guy[Y] -= 2
        elif keys[K_LEFT] and check(pos[X]+guy[X]-15,pos[Y]+guy[Y]):
            newMove = LEFT
            dire = 8
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
    if pause[0] == True:
        frame = 0
  
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
    global heart,rupee,button,health
    for i in range(health):
        screen.blit(heart,(10+i*30,10))

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

gChupics = []
bChupics = []
eDelay = 15
eFrame = 0
eTime = [300,300,300]
eX = [0,0,0]
eY = [0,0,0]
eTurn = False

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

randY = [0,0,0]
randX = [0,0,0]
enemyXY = [[0,0],[0,0],[0,0]]
eRects = [0,0,0]
push = [[0,0],[0,0],[0,0]]
eHealth=[0,0,0]
eDmg=[0,0,0]

def addEnemy(enemy, num, x, y, stop, speed, length, health):
    
    global epics, eDelay, eFrame, guy, eX, eY, eTime, eTurn, randX, randY, enemyXY,eRects, playerRect, dire, push, eHealth, eDmg, pause
    
    eTime[num]-= 1
    eDelay-=1
    
    if eDelay == 0:
        eFrame+=1
        eDelay = 15
    if eFrame == stop:
        eFrame = 0
    if pause[1] == False:
        if eTurn == True:
           #eX-=speed
            eY[num]+=randY[num]
        if eTurn == False:
            eX[num]+=randX[num]
            #eY+=randY[num]
        if eTime[num] == 0 and eTurn == True:
            eTime[num] = length
            eTurn = False
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
        if eTime[num] == 0 and eTurn == False:
            eTime[num] = length
            eTurn = True
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
            
    enemyXY[num]=[-guy[X]+x+eX[num]+push[num][X],-guy[Y]+y+eY[num]+push[num][Y]]
    eRects[num]=enemy.get_rect()
    eRects[num]=eRects[num].move(enemyXY[num][X],enemyXY[num][Y])
    
    #newP = playerRect.move(-guy[X]-x,-guy[Y]-y)

    if eRects[num].colliderect(playerRect):
        collide(eRects[num],1,num)
        print("hit")
    eHealth[num] = health-eDmg[num]
    print(eHealth)
    #draw.rect(screen, (0,0,0),playerRect)
    #draw.rect(screen, (0,0,0),eRects[num])
    #print(eRects[0],playerRect)
    if eHealth[num]>0:
        screen.blit(enemy,(enemyXY[num][X],enemyXY[num][Y]))
    #print(eY[num])


# collision--------------------------------------------------

def collide(rect, dmg, num):
    global health, attack, push, eDmg, eHealth, frame2, pause
    
    if eHealth[num]>0:
    
        if attack == False:
            pause[0] = True
            time.set_timer(USEREVENT + 1, 300)

            health-=dmg
            if dire == 14:
                guy[X] -= 20
                #time.wait(500)
            if dire == 8:
                guy[X] += 20
    
            if dire == 0:
                guy[Y] -= 20
    
            if dire == 20:
                guy[Y] += 20
    
    
        if attack == True:
            pause[1] = True
            time.set_timer(USEREVENT + 1, 300)
            sound2 = mixer.Sound("sounds/Hit.wav")
            sound2.play()
            if dire == 14:
                push[num][X] += 30
                eDmg[num]+=1
    
            if dire == 8:
                push[num][X] -= 30
                eDmg[num]+=1
    
            if dire == 0:
                push[num][Y] += 30
                eDmg[num]+=1
    
            if dire == 20:
                push[num][Y] -= 30
                eDmg[num]+=1


pic = pics[move][int(frame)]
playerRect = Rect(0,0,15,15)
pause = [False,False]

running=True

while running:
    for evt in event.get():
        if evt.type == USEREVENT + 1:
            pause[0] = False
            pause[1] = False
        if evt.type==QUIT:
            running=False
       
    keys = key.get_pressed()

    
    gChuchu = gChupics[eFrame]
    bChuchu = bChupics[eFrame]
    
    #print(bChuRect,gChuRect)
    #if playerRect.colliderect(bChuRect):
        #print("Hit")
    
   #Rect.colliderect



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
       if attack == False:
           moveGuy(guy)
       drawScene(screen,guy)
    
       gChuchu = gChupics[eFrame]
       bChuchu = bChupics[eFrame]
       pic = pics[move][int(frame)]
       playerRect = pic.get_rect()
       bChuRect = bChuchu.get_rect()
       gChuRect = gChuchu.get_rect()
       
       #doorRect = Rect(30-guy[X],210-guy[Y],60,60)

#doors------------------------------------------------------
    #draw.rect(screen,(0,0,255),doorRect,3)
    
    if guy[X] > 105 and guy[X] < 138 and guy[Y] == 264 and currentPic == backPic:
        newLoc(overPic,Omask,worldpos,False,"Outside",10)
        
    elif guy[X] > 105 and guy[X] < 138 and guy[Y] == 254 and currentPic == overPic:
        newLoc(backPic,Hmask,housepos,True,"House",-10)

#attack------------------------------------------------------
    
    if keys[K_SPACE]:
        attack = True
        playerRect = apics[frame2+dire].get_rect()

        
    if attack == True:
        if unlock == True :
            screen.blit(apics[frame2+dire],(270+guy[X]-apics[frame2].get_width()//2,195+guy[Y]-apics[frame2].get_width()//2))
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
