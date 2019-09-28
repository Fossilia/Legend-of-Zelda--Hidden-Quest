from pygame import*
from random import*
from math import*

X=0
Y=1

init()
mixer.init()
size = width, height = 800, 600
screen = display.set_mode(size)
backPic = image.load("Images/maps/house.jpg").convert()
overPic = image.load("Images/maps/overworld.jpg").convert()
overPic=transform.scale(overPic, (int(overPic.get_width()*2.5),int(overPic.get_height()*2.5)))
linkPic = image.load("Images/link/link.jpg")
Hmask = image.load("Images/maps/HouseMask.jpg")
Omask=overPic
#Omask = image.load("Images/maps/overworld.jpg").convert()
mask=Hmask
barrier = (254,0,0)
housepos=[125,100]
worldpos=[1640,170]
pos=housepos
push=False
unlock=True
house = True
currentPic = backPic
frame=0     # current frame within the move
move=1      # current move being performed
mixer.music.load('Sounds/House.mp3')
mixer.music.play(-1,1.0)
music=True


def drawScene(screen,guy):
    """ draws the current state of the game """
    screen.blit(currentPic, (-guy[X]-1640,-guy[Y]-170))
    print(pos[X],pos[Y])
    pic = pics[move][int(frame)]
    screen.blit(pic,(400-pic.get_width()//2,300-pic.get_height()//2))
    #screen.blit(linkPic, (250,250))
    display.flip()

def check(x,y):
    if x<0 or x >= mask.get_width() or y<0 or y >= mask.get_height():
        return False
    else:
        if mask.get_at((x,y)) == barrier:
            #print(mask.get_at((x,y)))
            return False
        else:
            #print(mask.get_at((x,y)))
            return True

def moveGuy(guy):
    global move, frame
    keys = key.get_pressed()

    newMove = -1        
    if keys[K_RIGHT] and check(pos[X]+guy[X]+15,pos[Y]+guy[Y]):
        newMove = RIGHT
        guy[X] += 2
    elif keys[K_DOWN] and check(pos[X]+guy[X],pos[Y]+guy[Y]+15):
        newMove = DOWN
        guy[Y] += 2
    elif keys[K_UP] and check(pos[X]+guy[X],pos[Y]+guy[Y]-15):
        newMove = UP
        guy[Y] -= 2
    elif keys[K_LEFT] and check(pos[X]+guy[X]-15,pos[Y]+guy[Y]):
        newMove = LEFT
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
    
def newLoc(Picture,newmask,newpos,camera):
    global unlock,mask,currentPic,pos
    currentPic = Picture
    unlock = camera
    mask=newmask
    pos=newpos
    screen.fill((0,0,0))
    time.wait(500)

#screen.blit(CurrentPic, (75,-80))
display.flip()
guy = [0,0,0]
#screen.blit(CurrentPic, (-guy[X],guy[Y]))

frame=0     # current frame within the move
move=1      # current move being performed


pics = []
pics.append(makeMove("Link-",31,40,2))      # RIGHT
pics.append(makeMove("Link-",1,10,2))     # DOWN
pics.append(makeMove("Link-",21,30,2))    # UP
pics.append(makeMove("Link-",11,20,2))    # LEFT

RIGHT = 0 # These are just the indicies of the moves
DOWN = 1  
UP = 2
LEFT = 3

running=True

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
    
    if unlock==True:
        screen.blit(currentPic, (150,100))
        
        pic = pics[move][int(frame)]
        screen.blit(pic,(275+guy[X]-pic.get_width()//2,190+guy[Y]-pic.get_height()//2))
        
        #screen.blit(linkPic, (250+guy[X],250-guy[Y]))
        #print(guy[X])
        moveGuy(guy)
    else:
       # pos=worldpos
        moveGuy(guy)
        drawScene(screen,guy)
    #print(guy[X],guy[Y])
    
    if guy[X] > 105 and guy[X] < 138 and guy[Y] == 264 and currentPic == backPic:
        newLoc(overPic,Omask,worldpos,False)
        guy[Y]+=10
        mixer.music.stop()
        music=False
        
    elif guy[X] > 105 and guy[X] < 138 and guy[Y] == 254 and currentPic == overPic:
        newLoc(backPic,Hmask,housepos,True)
        guy[Y]-=10
        if music==False:
            mixer.music.play(-1,1.0)
            music=True

    display.flip()
quit()
