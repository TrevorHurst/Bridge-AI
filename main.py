import turtle, time
class Shapes:
    def line(x1,y1,x2,y2):
        turtle.pu()
        turtle.goto(x1,y1)
        turtle.pd()
        turtle.goto(x2,y2)
        turtle.pu()
    def dot(x,y,r,color='black'):
        turtle.pu()
        turtle.color(color)
        turtle.goto(x,y)
        turtle.dot(r)
        turtle.color('black')

class Wall:
    def __init__(s,xs,ys):
        s.x1 = xs[0]
        s.y1 = ys[0]
        s.x2 = xs[1]
        s.y2 = ys[1]
        s.leng = ((s.x2-s.x1)**2+(s.y2-s.y1)**2)**.5
        s.points = []
        try:
            s.slope = [(s.y2-s.y1),(s.x2-s.x1)]
            cx = s.x1
            cy = s.y1
            for i in range(round(s.leng)):
                s.points.append([cx,cy])
                cx+=s.slope[0]
                cy+=s.slope[1]
        except: 
            s.slope = "undefined"
            cy = max(s.y1,s.y2)
            while cy > min(s.y1,s.y2):
                s.points.append([s.x1,cy])
                cy-=1

    def show(s):
        Shapes.line(s.x1,s.y1,s.x2,s.y2)

def rbrain():
    from random import randint
    global lt
    a = [Move([randint(-1,1),randint(-1,1)]) for i in range(lt)]
    return a
def distance(p1,p2):
    xdist = abs(p1[0]-p2[0])
    ydist = abs(p1[1]-p2[1])
    return xdist * xdist + ydist * ydist

class Move:
    def __init__(s,val,w = 0):
        s.x = round(val[0])
        s.y = round(val[1])
        s.weight = w

class Brain:
    def __init__(s,x,y,brain=False):
        s.x = x
        s.y = y
        s.r = 2
        s.fitness = 0
        s.dead = False
        if not brain:
            s.brain = rbrain()
        else:
            s.brain = brain
    def show(s,color='black'):
        if not s.dead:
            Shapes.dot(s.x,s.y,s.r,color)
        else:
            s.fitness-=10
            #Shapes.dot(s.x,s.y,'red')
    def update(s):
        s.readnext()
    def readnext(s):
        from random import uniform
        global step, walls
        if not s.dead:
            s.d = distance([s.x,s.y],goal)
            s.x+= s.brain[step].x
            s.y+= s.brain[step].y
            s.checkfitness()
            
    def checkfitness(s): 
        global goal
        a = s.fitness
        d = distance([s.x,s.y],goal)
        s.fitness -= d
        if s.d < d:
            s.brain[step].weight+=1
        else:
            s.brain[step].weight-=1

    def check(s,wall):
        if s.dead == False:
            for point in wall.points:
                s.dead = distance([s.x,s.y],[point[0],point[1]]) < s.r


    def breed(s,other):
        from random import uniform
        global lt, lr
        nb = []
        j = 0
        while j < lt:
            if uniform(0,1) > lr:# use learning rate to 
                if s.brain[j].weight < other.brain[j].weight:
                    nb.append(s.brain[j])#.fuzz()
                else:
                    nb.append(other.brain[j])#.fuzz()
                j += 1
            else:
                if s.brain[j].weight < other.brain[j].weight:
                    nb.append(s.brain[j])
                else:
                    nb.append(other.brain[j])
                j += 1
        return nb

lt = 100 # number of steps brain is alive
brainum =  50 # number of brains
lr = .05 # learning rate
walls = []
#walls.append(Wall([-35,0],[35,5]))
#walls.append(Wall([-35,0],[-35,-5]))
#walls.append(Wall([0,0],[25,-25]))
walls.append(Wall([-60,-10],[25,25]))
walls.append(Wall([-60,-60],[25,-25]))
walls.append(Wall([-60,-10],[-25,-25]))
walls.append(Wall([-10,-10],[-25,-5]))
walls.append(Wall([-10,-10],[5,25]))
walls.append(Wall([-10,10],[5,5]))
walls.append(Wall([-10,10],[-5,-5]))
walls.append(Wall([10,60],[25,25]))
walls.append(Wall([10,60],[-25,-25]))
walls.append(Wall([60,60],[-25,25]))
walls.append(Wall([10,10],[25,5]))
walls.append(Wall([10,10],[-25,-5]))

goal = [35,0]
startpos = (-35,0)

brains = [Brain(startpos[0],startpos[1]) for i in range(brainum)]
turtle.tracer(0,0)
turtle.ht()
time1 = time.time()
while True:
    print(time.time()-time1)
    time1 = time.time()
    step = 0
    while step < lt:
        turtle.clear()
        for wall in walls:
            wall.show()
            for i in wall.points:
                Shapes.dot(i[0],i[1],2,"yellow")
        f = float(0)
        for brain in brains:
            brain.update()
            for wall in walls:
                brain.check(wall)
            brain.show()
            sortedbs = list(sorted(brains,key=lambda a: a.x,reverse=True))
        sortedbs[0].show('green')
        turtle.update()
        step+=1
    tb = sortedbs[0].brain
    ii = 0
    while ii < brainum-1:
        brains[ii] = Brain(startpos[0],startpos[1],brains[ii].breed(brains[ii+1]))
        ii+=1
    brains[len(brains)-1] = Brain(startpos[0],startpos[1],tb)
    lr*=.9
