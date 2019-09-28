#Final Project
#Faisal Bagalagel
#Kill Chuchus and stuff

from pygame import*
from random import*
from math import*

init()
mixer.init()
font.init()
X=0
Y=1
link = [0,0]
boost = [0,0]
pics = []
apics = []
screen = display.set_mode((800,600))
#images
backPic = image.load("Images/maps/house.jpg").convert()
overPic = image.load("Images/maps/overworld.jpg").convert()
overPic=transform.smoothscale(overPic, (int(overPic.get_width()*2.5),int(overPic.get_height()*2.5)))
linkPic = image.load("Images/link/link.jpg")
heart = image.load("Images/assets/heart.png")
heart = transform.smoothscale(heart,(30,25))
rupee = image.load("Images/assets/rupee.png")
rupee = transform.smoothscale(rupee,(33,25))
Hmask = image.load("Images/maps/HouseMask.jpg")
Omask = image.load("Images/maps/Omask.jpg")
power = image.load("Images/assets/power.png")
power = transform.smoothscale(power,(25,25))
swift = image.load("Images/assets/wisdom.png")
swift = transform.smoothscale(swift,(25,25))
protect = image.load("Images/assets/courage.png")
protect = transform.smoothscale(protect,(25,25))
hurtChu = image.load("Images/enemies/hurtChu.png")
hurtChu = transform.scale(hurtChu, (hurtChu.get_height()*2,hurtChu.get_width()*2))
Omask =transform.scale(Omask, (int(Omask.get_width()*2.5),int(Omask.get_height()*2.5)))

over = image.load("Images/menu/GameOver.jpg")
start = image.load("Images/menu/start.jpg")
start = transform.smoothscale(start,(800,600))
instruct = image.load("Images/menu/instruct.jpg")
instruct = transform.smoothscale(instruct,(800,600))
win = image.load("Images/menu/Win.jpg")
win = transform.smoothscale(win,(800,600))

gameWin = False
gameInstruct = False
gameStart = True
gameOver = False

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

#variables related to enemy values
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

#enemy frame lists
gChupics = []
bChupics = []
dChupics = []
bigChupics = []
rChupics = []
grChupics =[]

eDelay = 15
eFrame = 0
bigFrame = 0
eTime = [300]*30
eTurn = False

showT = False
pString = ""

eList = []
moveX = []
moveY = []
ChuChu = [0,0]
chuList = []
speedList = []
chuNum = 0
lengthList = []
healthList = [1,1]
eP = True

#spirtual stone checks
powerCheck = False
speedCheck = False
healthCheck = False
maxH = 6
pSpeed = 2
pDmg = 1
bossSpawn = False
bossText = False
bossCount = 350

eSpawn = False

frameDelay = 10
intialDelay = 5
myClock = time.Clock()

playerRect = Rect(0,0,15,15)

healthRestore = False
enemies = 0
gameStarted = False

running=True

#text------------------------------------------------------

def popText(text,pos): #function that blits a rect at a certain posion (bottom of screen if True, top if false) with text on it
    myfont = font.SysFont('Comic Sans MS', 17)
    myfont2 = font.SysFont('Comic Sans MS', 12)
    pop = myfont.render(text, False, (255, 255, 255))
    pop2 = myfont2.render("Press space to close", False, (255, 255, 255))
    
    if pos:
        draw.rect(screen, (0,0,0),(100,400,600,100))
        draw.rect(screen, (255,255,255),(100,400,600,100),3)
        screen.blit(pop,(175,410))
        screen.blit(pop2,(330,470))
    else:
        draw.rect(screen, (0,0,0),(250,100,300,100))
        draw.rect(screen, (255,255,255),(250,100,300,100),3)
        screen.blit(pop,(280,130))
    
#barrier-------------------------------------------------------
    
def check(x,y): #mask to check is there is any red on the mask for collision with the environment
    if x<0 or x >= mask.get_width() or y<0 or y >= mask.get_height():
        return False
    else:
        if mask.get_at((x,y)) == barrier:
            return False
        else:
            return True
        
#movement------------------------------------------------------

def movelink(link): #players movement using the arrow keys
    global move, frame, dire, stop, pause, boost, pSpeed
    keys = key.get_pressed()
    if pause == False and showT == False:
        newMove = -1
        if keys[K_RIGHT] and check(pos[X]+link[X]+15,pos[Y]+link[Y]):
            newMove = RIGHT
            dire = 14
            boost[X] = 15
            boost[Y] = 0
            stop = 6
            link[X] += pSpeed
        elif keys[K_DOWN] and check(pos[X]+link[X],pos[Y]+link[Y]+15):
            newMove = DOWN
            dire = 0
            boost[X] = 0
            boost[Y] = 15
            link[Y] += pSpeed
            stop = 8
        elif keys[K_UP] and check(pos[X]+link[X],pos[Y]+link[Y]-15):
            newMove = UP
            dire = 20
            boost[X] = 0
            boost[Y] = -15
            stop = 6
            link[Y] -= pSpeed
        elif keys[K_LEFT] and check(pos[X]+link[X]-15,pos[Y]+link[Y]):
            newMove = LEFT
            dire = 8
            boost[X] = -15
            boost[Y] = 0
            stop = 6
            link[X] -= pSpeed
        else:
            frame = 0

        if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame = frame + 0.2 # adding 0.2 allows us to slow down the animation
            if frame >= len(pics[move]):
                frame = 1
        elif newMove != -1:     # a move was selected
            move = newMove      # make that our current move
            frame = 1
            
    if pause == True: #pushes the player back if he got hit
        frame = 0
        if dire == 14:
            link[X] -= 8
           
        if dire == 8:
            link[X] += 8

        if dire == 0:
            link[Y] -= 8

        if dire == 20:
            link[Y] += 8
  
#frames-----------------------------------------------------
        
def makeMove(name,start,end,size): #used to get image lists for walking

    move = []
    for i in range(start,end+1):
        move.append(transform.scale(image.load("%s/%s%03d.png" % (name,name,i)),(image.load("%s/%s%03d.png" % (name,name,i)).get_width()*size,image.load("%s/%s%03d.png" % (name,name,i)).get_height()*size)))
    return move

#changing place---------------------------------------------

def newLoc(Picture,newmask,newpos,camera,music,move): #changes location of player
    global unlock,mask,currentPic,pos,link
    currentPic = Picture
    unlock = camera
    mask=newmask
    pos=newpos
    mixer.music.stop()
    link[X]+=move
    mixer.music.load('Sounds/music/'+music+'.mp3')
    mixer.music.play(-1,0.0)
    screen.fill((0,0,0))
    display.flip()
    time.wait(500)
    
#hud---------------------------------------------------------

def hud(): #blits hearts, rupees, stones 
    global heart,rupee,button,health,rupees
    for i in range(health):
        screen.blit(heart,(10+i*30,10))
    screen.blit(rupee,(710,10))
    myfont = font.SysFont('Comic Sans MS', 20)
    rupeeText = myfont.render(str(rupees), False, (255, 255, 255))
    screen.blit(rupeeText,(745,7))
    if powerCheck:
        screen.blit(power,(580,10))
    if speedCheck:
        screen.blit(swift,(610,10))
    if healthCheck:
        screen.blit(protect,(640,10))

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
        
for i in range(15):
        rChupics.append(transform.scale(image.load("images/enemies/R-chuchu/R-chuchu" + str(i) + ".png"),(image.load("images/enemies/R-chuchu/R-chuchu" + str(i) + ".png").get_width()*2,image.load("images/enemies/R-chuchu/R-chuchu" + str(i) + ".png").get_height()*2)))
        
for i in range(15):
        grChupics.append(transform.scale(image.load("images/enemies/GR-chuchu/GR-chuchu" + str(i) + ".png"),(image.load("images/enemies/GR-chuchu/GR-chuchu" + str(i) + ".png").get_width()*2,image.load("images/enemies/GR-chuchu/GR-chuchu" + str(i) + ".png").get_height()*2)))
        
for i in range(15):
        dChupics.append(transform.scale(image.load("images/enemies/D-chuchu/D-chuchu" + str(i) + ".png"),(image.load("images/enemies/D-chuchu/D-chuchu" + str(i) + ".png").get_width()*2,image.load("images/enemies/D-chuchu/D-chuchu" + str(i) + ".png").get_height()*2)))
        
for i in range(8):
        bigChupics.append(transform.scale(image.load("images/enemies/BIG-chuchu/BIG-chuchu" + str(i) + ".png"),(image.load("images/enemies/BIG-chuchu/BIG-chuchu" + str(i) + ".png").get_width()*3,image.load("images/enemies/BIG-chuchu/BIG-chuchu" + str(i) + ".png").get_height()*3)))
        

#walking------------------------------------------------------
    
pics.append(makeMove("Link-",31,40,2))    # RIGHT
pics.append(makeMove("Link-",1,10,2))     # DOWN
pics.append(makeMove("Link-",21,30,2))    # UP
pics.append(makeMove("Link-",11,20,2))    # LEFT

#enemies------------------------------------------------------

def addEnemy(enemy, num, x, y): #adds an enemy to the game with a specific number a starting coordinates. The function must be run all the time with the enemies specific number for the enemy to continue to exist
    
    global epics, eDelay, eFrame, link, eX, eY, eTime, eTurn, randX, randY, enemyXY,eRects, playerRect, dire, push, eHealth, eDmg, pause, ePause, pos, gChupics, bChupics, hurtChu, screenRect, gameWin, gameStarted
    
    eTime[num]-= 1
    px = 400 - pic.get_width() // 2
    py = 300 - pic.get_height() // 2
    
    #each enemy has different states and properties assigned to them, eg, different amount of health, speed, dmg                            
    if enemy == bChuchu:
        health = 3
        hurt = hurtChu
        speed = 2
        dmg = 1
        drop = 6
        length = randint(500, 1000)
        
    if enemy == gChuchu:
        health = 1
        hurt = hurtChu
        speed = 2
        dmg = 1
        drop = 5
        length = randint(500, 1000)
        
    if enemy == rChuchu:
        health = 6
        hurt = hurtChu
        speed = 3
        dmg = 2
        drop = 40
        length = randint(500, 1000)
        
    if enemy == dChuchu:
        health = 2
        hurt = hurtChu
        speed = 1.5
        dmg = 2
        drop = 30
        length = randint(500, 1000)
        
    if enemy == grChuchu:
        health = 4
        hurt = hurtChu
        speed = 0.5
        dmg = 1
        drop = 15
        length = randint(700, 2000)
        
    if enemy == bigChuchu:
        health = 80
        hurt = hurtChu
        speed = 0.7
        dmg = 1
        drop = 300
        length = randint(500, 1000)
        
    targetMove = False
    
    eRects[num]=enemy.get_rect()
    eRects[num]=eRects[num].move(enemyXY[num][X],enemyXY[num][Y])
    
    #AI of enemies that follow the player
    if enemy == bigChuchu or enemy == dChuchu or enemy == grChuchu:
            
            targetMove = True
            if enemyXY[num][X] > px:
                push[num][X] -= speed
                
            elif enemyXY[num][X] < px:
                push[num][X] += speed
                
            # Movement along y direction
            if enemyXY[num][Y] < py:
                push[num][Y] += speed
                
            elif enemyXY[num][Y] > py:
                push[num][Y] -= speed
        
    #AI of enemies that move in random directions
    if ePause[num] == False and targetMove == False:
        if eTurn == True:
            
            eY[num] += randY[num] * speed
            
        if eTurn == False:
            
            eX[num] += randX[num] * speed
            
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
            
    
    bChuRect = bChuchu.get_rect()
    gChuRect = gChuchu.get_rect()
       
    #pushes the enemy if they got hit by the player
    if enemy!=bigChuchu and ePause[num] == True:
            enemy = hurt
            if dire == 14:
                push[num][X] += 10
                
            if dire == 8:
                push[num][X] -= 10
    
            if dire == 0:
                push[num][Y] += 10
    
            if dire == 20:
                push[num][Y] -= 10

    enemyXY[num]=[-link[X]+x+eX[num]/2+push[num][X],-link[Y]+y+eY[num]/2+push[num][Y]]

    #what happens when the enemy collides with the player
    if eRects[num].colliderect(playerRect):
        collide(eRects[num],dmg,num,drop)
       
    eHealth[num] = health-eDmg[num]
   
    if eHealth[num]>0:
        screen.blit(enemy,(enemyXY[num][X],enemyXY[num][Y]))
        
    if eHealth[num]<=0 and enemy == bigChuchu: #if you kill the big Chuchu you win the game
        gameWin = True
        gameStarted = False
            
    


# collision--------------------------------------------------

def collide(rect, dmg, num, drop): #controls what happens when the player and enemy collide
    global health, attack, push, eDmg, eHealth, frame2, pause, colNum, ePause, rupees, pDmg, maxH
    
    if eHealth[num]>0:
    
        if attack == False and pause == False: #the player is hurt if he is not attacking
            pause = True 
            sound2 = mixer.Sound("sounds/Hurt.wav")
            sound2.play()
            time.set_timer(K_PAUSE, 80)  #timer so that the player is pushed back for a set amount of seconds
            health-=dmg
    
    
        if attack == True and ePause[num] == False: #the enemy is hurt if the player is attacking
            ePause[num] = True
            time.set_timer(K_PAUSE, 80) #timer so that the enemy is pushed back for a set amount of seconds
            sound2 = mixer.Sound("sounds/Hit.wav")
            sound2.play()
            eDmg[num]+=pDmg
            if eHealth[num] == pDmg: #what happens when you kill an enemy
                rand = randint(0,2)
                    
                if rand == 0 and maxH>health: #what you get when you kill the enemies
                    health+=1
                    sound2 = mixer.Sound("sounds/Heart.wav")
                    sound2.play()
                
                else:
                    sound2 = mixer.Sound("sounds/Die.wav")
                    sound2.play()
                    
                rupees+=randint(2,drop)
                sound2 = mixer.Sound("sounds/Rupee.wav")
                sound2.play()
                


while running:
    for evt in event.get():
        if evt.type == K_PAUSE: #used to stop enemies and the player from being pushed back from a hit
            pause = False
            for i in range(len(ePause)):
                ePause[i] = False
        if evt.type == USEREVENT : #used for spawing enemies
            enemies+=1
            eP = True
        if evt.type==QUIT:
            running=False
            
    keys = key.get_pressed()
    
#Menus--------------------------------------------------------------------
    
    if gameStart: #start menu
        screen.blit(start,(0,0))
        mixer.music.load('Sounds/music/menu.mp3')
        mixer.music.play(0,0)
        
        if keys[K_SPACE]: #transistion to instruct menu
            gameInstruct = True
            gameStart = False
            
    if gameInstruct: #instruct menu
        screen.blit(instruct,(0,0))
        
        if keys[K_x] and gameInstruct: #transistion to game
            mixer.music.load('Sounds/music/House.mp3')
            mixer.music.play(0,1.0)
            gameInstruct = False
            gameStart = False
            gameStarted = True
            
    if gameOver:
        screen.blit(over,(0,0)) #gameover screen
        
    if gameWin:
        screen.blit(win,(0,0)) #win screen
        mixer.music.stop()
            
#game Start----------------------------------------------------------------
            
    if gameStarted:
        #frame timer for enemies
        eDelay-=1
        
        if eDelay == 0:
            eFrame+=1
            bigFrame+=1
            eDelay = 15
        if eFrame == 15:
            eFrame = 0
        if bigFrame == 8:
            bigFrame = 0
        
        #makes sure the enemies areon the right frame    
        gChuchu = gChupics[eFrame]
        bChuchu = bChupics[eFrame]
        rChuchu = rChupics[eFrame]
        dChuchu = dChupics[eFrame]
        grChuchu = grChupics[eFrame]
        bigChuchu = bigChupics[bigFrame]
        
        if eP == True and eSpawn == True:
            time.set_timer(USEREVENT, 1800) #sets a timer so that enemies can spawn
            eP = False
            
            healthRestore = False
            
            randY.append(0) #adds empty values to lists so that the indexes dont go out of range
            randX.append(0)
            enemyXY.append([0,0])
            eRects.append(0)
            push.append([0,0])
            eHealth.append(0)
            eDmg.append(0)
            eX .append(0)
            eY.append(0)
            eTime.append(300)
            ePause.append(False)
            
            rand2 = randint(-650,1700) #get random postions
            rand3 = randint(300,1900)
            screenRect = Rect(0,0,800,600) #create rect for visible screen
            
            if screenRect.collidepoint(rand2-link[X],rand3-link[Y]): #makes sure they spawn off the screen
                    rand3+=600
            moveX.append(rand2)
            moveY.append(rand3)
            
            #spawns different types of enemies according to how many enemies have already spawned        
            if enemies < 20: 
                    ChuChu.append(0)
                
            elif enemies > 15 and enemies < 40:
                    rand = randint(0,1)
                    if rand==0:
                        ChuChu.append(0)
                    else:
                        ChuChu.append(1)
                    
            elif enemies > 40 and enemies < 70:
                    rand = randint(0,2)
                    if rand==0:
                        ChuChu.append(0)
                    if rand==1:
                        ChuChu.append(1)
                    else:
                        ChuChu.append(2)
                        
            elif enemies > 70 and enemies < 100:
                    rand = randint(0,3)
                    if rand==0:
                        ChuChu.append(0)
                    if rand==1:
                        ChuChu.append(1)
                    if rand==2:
                        ChuChu.append(2)
                    else:
                        ChuChu.append(3)
                        
            elif enemies > 100:
                    rand = randint(0,4)
                    if rand==0:
                        ChuChu.append(0)
                    if rand==1:
                        ChuChu.append(1)
                    if rand==2:
                        ChuChu.append(2)
                    if rand==3:
                        ChuChu.append(3)
                    else:
                        ChuChu.append(4)
                        
            if healthCheck and powerCheck and speedCheck and bossSpawn == False: #if you collect all the stones
                    ChuChu.append(5) #Big Chuchu spawns
                    bossText = True
                    bossSpawn = True
                    
            chuList.append(chuNum)
            chuNum+=1
            speedList.append(2)
            healthList.append(1)
    
        pic = pics[move][int(frame)]
        if attack == False:
            playerRect = Rect(0,0,20,35)
    
        pic = pics[move][int(frame)]
            
    
    #Indoor-----------------------------------------------------
        
        if unlock==True:
            screen.fill((0,0,0))
            screen.blit(currentPic, (150,100)) #blits the house in one spot
            if attack == False:
                intialDelay=5
                pic = pics[move][int(frame)]
                screen.blit(pic,(275+link[X]-pic.get_width()//2,190+link[Y]-pic.get_height()//2)) #blits the player in differnt places according to his postion
                playerRect=playerRect.move(275+link[X],190+link[Y]) #moves his collsion hitbox with him
                movelink(link)
            hud()
            
    #outdoors----------------------------------------------------
        else: #if your not inside, your outside
            intialDelay = 5
            screen.blit(currentPic, (-link[X] - 1645, -link[Y] - 190)) #blits the background in accordance to links postion
            
            if attack == False:
                movelink(link)
                pic = pics[move][int(frame)]
                screen.blit(pic, (400 - pic.get_width() // 2, 300 - pic.get_height() // 2)) #blits link in one spot
                playerRect = playerRect.move(400 - pic.get_width() // 2, 300 - pic.get_height() // 2)
                
            for i in range(enemies): #runs all the enmey functions that were added
                
                    if ChuChu[i] == 0:
                        addEnemy(gChuchu,chuList[i],moveX[i],moveY[i])
                    elif ChuChu[i] == 1:
                        addEnemy(bChuchu,chuList[i],moveX[i],moveY[i])
                    elif ChuChu[i] == 2:
                        addEnemy(grChuchu,chuList[i],moveX[i],moveY[i])
                    elif ChuChu[i] == 3:
                        addEnemy(rChuchu,chuList[i],moveX[i],moveY[i])
                    elif ChuChu[i] == 4:
                        addEnemy(dChuchu,chuList[i],moveX[i],moveY[i])
                    elif ChuChu[i] == 5:
                        addEnemy(bigChuchu,chuList[i],400,1000)
                
        hud()
    
        if bossText: #checks if boss has spawned, if so start timer
            bossCount-=1
            print(bossCount)
            if bossCount>0:
                pString2 = "BIG CHUCHU HAS SPAWNED!"
                popText(pString2,False)
    
    #power ups-------------------------------------------------------------
        
        #all these check if link is in certain postions in the map and checks if he interacts with the statues
        if link[X] > 1580 and link[X] < 1605 and link[Y] > 10 and link[Y] < 18 and keys[K_x] and dire == 20 and speedCheck == False:#speed
            showT = True
            if rupees > 49:
                rupees-=50
                pString = "You sacrifced 50 rupees to get the Emerald of Swiftness!"
                speedCheck = True
                pSpeed = 4
                sound2 = mixer.Sound("sounds/item.wav")
                sound2.play()
            else:
                pString = "Need "+str(50-rupees)+" rupees to get the Emerald of Swiftness."
            
        if link[X] < -1230 and link[X] > -1285 and link[Y] > 1205 and link[Y] < 1240 and keys[K_x] and dire == 20 and healthRestore == False:#health
            showT = True
            if rupees > 19:
                Restore = True
                rupees-=20
                health
                pString = "You sacrifced 20 rupees to restore your health!"
                health = maxH
                sound2 = mixer.Sound("sounds/heart.wav")
                sound2.play()
            else:
                pString = "Need "+str(20-rupees)+" rupees to restore your health."
            
        if link[X] < -1320 and link[X] > -1385 and link[Y] > 605 and link[Y] < 640 and keys[K_x] and dire == 20 and powerCheck == False:#power
            showT = True
            if rupees > 49:
                rupees-=50
                pString = "You sacrifced 50 rupees to get the Ruby of Power!"
                powerCheck = True
                pDmg = 3
                sound2 = mixer.Sound("sounds/item.wav")
                sound2.play()
            else:
                pString = "Need "+str(50-rupees)+" rupees to get the Ruby of Power."
        
        if link[X] > 1610 and link[X] < 1660 and link[Y] > 1210 and link[Y] < 1225 and keys[K_x] and dire == 20 and healthCheck == False:#health+
            showT = True
            if rupees > 49:
                rupees-=50
                pString = "You sacrifced 50 rupees to get the Sapphire of Protection!"
                healthCheck = True
                maxH = 12
                health=maxH
                sound2 = mixer.Sound("sounds/item.wav")
                sound2.play()
            else:
                pString = "Need "+str(50-rupees)+" rupees to get the Sapphire of Protection."
        
    #doors--------------------------------------------------------------------------------------
        
        #checks if link is touching the door and changes the background accordingly
        if link[X] > 105 and link[X] < 138 and link[Y] == 264 and currentPic == backPic:
            sound2 = mixer.Sound("sounds/Door.wav")
            sound2.play()
            eSpawn = True
            newLoc(overPic,Omask,worldpos,False,"Outside",10)
            
        elif link[X] > 105 and link[X] < 138 and link[Y] == 254 and currentPic == overPic:
            sound2 = mixer.Sound("sounds/Door.wav")
            sound2.play()
            newLoc(backPic,Hmask,housepos,True,"House",-10)
            
        elif link[X] > 270 and link[X] < 320 and link[Y] == 210 and currentPic == backPic and keys[K_x] and haveSword == False and dire == 20:
            haveSword = True
            showT = True
            pString = "You got a Sword!"
            sound2 = mixer.Sound("sounds/item.wav")
            sound2.play()
            
            
        if showT: #shows text but closes it if the player presses space
            popText(pString,True)
            if keys[K_SPACE]:
                showT = False
                
    #prompts for when certain types of enemies are spawning
        if enemies > 15 and enemies < 22 and showT!=True: 
                pString = "Blue chuchus are spawning!"
                popText(pString,False)
                
        if enemies > 40 and enemies < 47 and showT!=True:
                pString = "Gray chuchus are spawning!"
                popText(pString,False)
                
        if enemies > 70 and enemies < 77 and showT!=True:
                pString = "Rock chuchus are spawning!"
                popText(pString,False)
                
        if enemies > 100 and enemies < 107 and showT!=True:
                pString = "Deadly chuchus are spawning!"
                popText(pString,False)
            
    #attack------------------------------------------------------
        
        if keys[K_SPACE] and haveSword:
            attack = True
    
        if attack: #blits the players attack frame in the player postion
            playerRect = apics[frame2+dire].get_rect()
            if unlock == True :
                screen.blit(apics[frame2+dire],(270+link[X]-apics[frame2].get_width()//2,195+link[Y]-apics[frame2].get_width()//2))
                playerRect = playerRect.move(boost[X] + 270+link[X]-apics[frame2].get_width()//2,boost[Y] + 195+link[Y]-        apics[frame2].get_width()//2)
            if unlock == False:
                screen.blit(apics[frame2 + dire],(400 - apics[frame2].get_width() // 2, 300 - apics[frame2].get_width() // 2))
                playerRect = playerRect.move(boost[X] + 400 - apics[frame2].get_width() // 2,boost[Y] + 300 - apics[frame2].get_width() // 2)
            display.flip()
            #frames delay for attack animation
            frameDelay -= 1                        
            if frameDelay == 0:                    
                frameDelay = intialDelay
                frame2 += 1
                if frame2 == stop:
                    attack = False
                    frame2 = 0
                    playerRect = pic.get_rect()
    
    #death---------------------------------------------------------
        if health <= 0: #checks if you have no health
            gameOver = True
            gameStarted = False
            mixer.music.stop()
                    
    myClock.tick(100)
    display.flip()
quit()
