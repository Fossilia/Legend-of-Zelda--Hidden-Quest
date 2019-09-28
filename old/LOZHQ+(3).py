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
    global intialDelay
    intialDelay=5
    screen.blit(currentPic, (-guy[X]-1645,-guy[Y]-190))
    if attack==False:
        pic = pics[move][int(frame)]
        screen.blit(pic,(400-pic.get_width()//2,300-pic.get_height()//2))
    if attack == True:
        screen.blit(apics[frame2+dire],(400-apics[frame2].get_width()//2,300-apics[frame2].get_width()//2))
        
    draw.rect(screen,(0,0,255),doorRect,3)

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
    global move, frame, dire, stop
    keys = key.get_pressed()

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
        
#enemy-------------------------------------------------------



#attack frames-----------------------------------------------

#for i in range(8):
    #apics.append(transform.scale(image.load("Images/link/attack-down/attack-down" + str(i) + ".png"),(image.load("Images/link/attack-down/attack-down" + str(i) + ".png").get_width()*2,image.load("Images/link/attack-down/attack-down" + str(i) + ".png").get_height()*2)))
#for i in range(6):
 #   apics.append(transform.scale(image.load("Images/link/attack-side/attack-side" + str(i) + ".png"),(image.load("Images/link/attack-side/attack-side" + str(i) + ".png").get_width()*2,image.load("Images/link/attack-side/attack-side" + str(i) + ".png").get_height()*2)))
#for i in range(8,14):
    #apics.append(transform.flip(apics[i],True,False))
#for i in range(6):
   # apics.append(transform.scale(image.load("Images/link/attack-up/attack-up" + str(i) + ".png"),(image.load("Images/link/attack-up/attack-up" + str(i) + ".png").get_width()*2,image.load("Images/link/attack-up/attack-up" + str(i) + ".png").get_height()*2)))

#walking------------------------------------------------------
    
pics.append(makeMove("Link-",31,40,2))    # RIGHT
pics.append(makeMove("Link-",1,10,2))     # DOWN
pics.append(makeMove("Link-",21,30,2))    # UP
pics.append(makeMove("Link-",11,20,2))    # LEFT

enemyX=0
enemyY=0
enemyM = True
running=True

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
       
    keys = key.get_pressed()

#Indoor-----------------------------------------------------
    
    if unlock==True:
        screen.blit(currentPic, (150,100))
        if attack == False:
            intialDelay=5
            pic = pics[move][int(frame)]
            moveGuy(guy)
            screen.blit(pic,(275+guy[X]-pic.get_width()//2,190+guy[Y]-pic.get_height()//2))
            doorRect = Rect(105,254,40,20)
            draw.rect(screen,(0,0,255),doorRect,3)

        hud()
    else:
       if attack == False:
           moveGuy(guy)
       drawScene(screen,guy)
       doorRect = Rect(30-guy[X]+enemyX,310-guy[Y]+enemyY,60,60)
       if enemyX<200 and enemyM==True:
            enemyX+=1
       if enemyX<200 and enemyM==False:
            enemyX-=1
       if enemyX==200:
            #enemyX-=1
            enemyM=False
       if enemyX==0:
            enemyM==True
       
#doors------------------------------------------------------
    
    if guy[X] > 105 and guy[X] < 138 and guy[Y] == 264 and currentPic == backPic:
        newLoc(overPic,Omask,worldpos,False,"Outside",10)
        
    elif guy[X] > 105 and guy[X] < 138 and guy[Y] == 254 and currentPic == overPic:
        newLoc(backPic,Hmask,housepos,True,"House",-10)

#attack------------------------------------------------------
    
    if keys[K_SPACE]:
        attack = True
        
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
                
#end---------------------------------------------------------
                
    myClock.tick(100)
    display.flip()
quit()
