import Tkinter
import random
import threading
import time
class Tetris:
    'Tetris game'
    def __init__(self,screen):
        self.__box      = [[0,0],[0,0],[0,0],[0,0],[0,0]]
        self.__boxPt   = (1.5,4.5)
        self.__screen   = screen
        self.__addTuple = lambda tuple1,tuple2:(tuple1[0]+tuple2[0],tuple1[1]+tuple2[1])
        self.__scrData  = [[0 for x in range(10)] for y in range(20)]
        self.__safeScreenRowAndLine  = lambda row,line : row >-1 and row < 20 and line > -1 and line < 10
        self.__randomCreateBox()
    def __randomCreateBox(self):#   I_ J L O S T Z
        boxs  = [ [[-0.5,-1.5],[-0.5,-0.5],[-0.5,0.5],[-0.5,1.5]], [[-1.5,-0.5],[0,-0.5],[0,0],[0,1.5]], [[-0.5,-1.5],[-0.5,-0.5],[-0.5,0.5],[-1.5,0.5]],[[-0.5,-0.5],[-0.5,0.5],[0.5,-0.5],[0.5,0.5]], [[-0.5,-1.5],[-0.5,-0.5],[-1.5,-0.5],[-1.5,0.5]],[[-0.5,-1.5],[-0.5,-0.5],[-1.5,-0.5],[-0.5,0.5]], [[-1.5,-1.5],[-1.5,-0.5],[-0.5,-0.5],[-0.5,0.5]] ]
        # self.__box = boxs[random.randint(0,6)]
        self.__box = boxs[1]
    def __fixedBox(self):
        for cube in self.__box:
            self.__scrData[int(self.__boxPt[0]+cube[0])][int(self.__boxPt[1]+cube[1])] = 1
    def __eliminate(self):
        row = 19
        while row > 0:
            if self.__scrData[row] == [1]*10:
                for r in range(row,0,-1):self.__scrData[r] = self.__scrData[r-1]
                continue
            row -= 1
    def __collistion(self,box):
        for cube in self.__box:
            if not self.__safeScreenRowAndLine( int(self.__boxPt[0]+cube[0]) ,int(self.__boxPt[1]+cube[1])) or self.__scrData[int(self.__boxPt[0]+cube[0])][int(self.__boxPt[1]+cube[1])] == 1:
                return True
        return False
    def rotate(self):
        for cub in self.__box : 
            cub.reverse()
            # cub[0] = -cub[0]
            cub[1] = -cub[1]
        self.draw()
    def move(self,type):
        move_dic = {'Left':((0,-1),(0,1)),'Right':((0,1),(0,-1)),'Down':((1,0),(-1,0))}
        self.__boxPt = self.__addTuple(self.__boxPt,move_dic.get(type)[0])
        if self.__collistion(self.__box):
            self.__boxPt = self.__addTuple(self.__boxPt,move_dic.get(type)[1])
            if type == "Down":
                self.__fixedBox()
                self.__eliminate()
                self.__boxPt = (1.5,4.5)
                self.__randomCreateBox()
                self.draw()
            return True
        else:
            self.draw()
            return False
    def quickDown(self):
        while not self.move("Down"):pass
    def draw(self):
        drawPexels = lambda pt,color:self.__screen.create_rectangle(10+int(pt[1])*12,10+int(pt[0])*12,20+int(pt[1])*12,20+int(pt[0])*12,fill=color)
        screen.delete("all")
        for r in range(20):
            for l in range(10):drawPexels((r,l),"black" if self.__scrData[r][l] else "gray") 
        for cub in self.__box:drawPexels(self.__addTuple(cub,self.__boxPt),"black")
top      = Tkinter.Tk()
screen   = Tkinter.Canvas(top,width=400,height= 400,bg = "green")
game     = Tetris(screen)
game.draw()
def keyFunc(event):
    if event.keycode   == 8124162:
        game.move("Left")
    elif event.keycode == 8189699:
        game.move("Right")
    elif event.keycode == 8255233:
        game.move("Down")
    elif event.keycode == 8320768:
        game.rotate()
    elif event.keycode == 3211296:
        game.quickDown()
screen.pack()
top.bind('<Key>',keyFunc)
def timeFunc():
    global top
    game.move("Down")
    top.after(1000,timeFunc)
# top.after(1000,timeFunc)
Tkinter.mainloop()
