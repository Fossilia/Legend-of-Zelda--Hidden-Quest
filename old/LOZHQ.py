from pygame import*
from random import*
from math import*

X=0
Y=1

init()
size = width, height = 800, 600
screen = display.set_mode(size)
backPic = image.load("Images/maps/house.jpg")
linkPic = image.load("Images/link/link.jpg")
unlock=False

def drawScene(screen,guy):
    """ draws the current state of the game """
    screen.blit(backPic, (-guy[X],-guy[Y]))
    pic = pics[move][int(frame)]
    screen.blit(pic,(300+pic.get_width()//2,280+pic.get_height()//2))
    #screen.blit(linkPic, (250,250))
    display.flip()


def moveGuy(guy):
    global move, frame
    keys = key.get_pressed()

    newMove = -1        
    if keys[K_RIGHT]:
        newMove = RIGHT
        guy[X] += 2
    elif keys[K_DOWN]:
        newMove = DOWN
        guy[Y] += 2
    elif keys[K_UP]:
        newMove = UP
        guy[Y] -= 2
    elif keys[K_LEFT]:
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

offset = -70
#screen.blit(backPic, (75,-80))
display.flip()
guy = [0,0,0]
screen.blit(backPic, (-guy[X],guy[Y]))

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
        screen.blit(backPic, (-75,-80))
        
        pic = pics[move][int(frame)]
        screen.blit(pic,(265+guy[X]-pic.get_width()//2,250+guy[Y]-pic.get_height()//2))
        
        #screen.blit(linkPic, (250+guy[X],250-guy[Y]))
        print(guy[X])
        moveGuy(guy)
    else:
        moveGuy(guy)
        drawScene(screen, guy)

    display.flip()
quit()
