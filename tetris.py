import Tkinter ;import random ;import threading;import time
class Tetris:
    def __init__(self,screen):
        self.__boxPt    = (1,4)
        self.__screen   = screen
        self.__addTuple = lambda tuple1,tuple2:(tuple1[0]+tuple2[0],tuple1[1]+tuple2[1])
        self.__scrData  = [[0 for x in range(10)] for y in range(20)]
        self.__safeScreenRowAndLine  = lambda row,line : row >-1 and row < 20 and line > -1 and line < 10
        self.__randomCreateBox()
    def __randomCreateBox(self):#   I_ J L O S T Z
        self.__boxs  = [ [ [[+0,-1],[+0,+0],[+0,+1],[+0,+2]], [[-1,+1],[+0,+1],[+1,+1],[+2,+1]], [[+1,-1],[+1,+0],[+1,+1],[+1,+2]], [[-1,+0],[+0,+0],[+1,+0],[+2,+0]] ],
                         [ [[-1,-1],[+0,-1],[+0,+0],[+0,+1]], [[-1,-0],[+0,+0],[+1,+0],[-1,+1]], [[+0,-1],[+0,+0],[+0,+1],[+1,+1]], [[+1,-1],[+0,+0],[+1,+0],[-1,-0]] ],
                         [ [[+0,-1],[+0,+0],[+0,+1],[-1,+1]], [[-1,-0],[+0,+0],[+1,+0],[+1,+1]], [[+0,-1],[+0,+0],[+0,+1],[+1,-1]], [[-1,-1],[-1,+0],[+0,+0],[+1,+0]] ],
                         [ [[-0,-0],[-0,+1],[+1,-0],[+1,+1]], [[-0,-0],[-0,+1],[+1,-0],[+1,+1]], [[-0,-0],[-0,+1],[+1,-0],[+1,+1]], [[-0,-0],[-0,+1],[+1,-0],[+1,+1]] ],
                         [ [[+0,-1],[+0,+0],[-1,+0],[-1,+1]], [[-1,+0],[+0,+0],[+0,+1],[+1,+1]], [[+1,-1],[+1,+0],[+0,+0],[+0,+1]], [[-1,-1],[+0,-1],[+0,+0],[+1,+0]] ],
                         [ [[+0,-1],[+0,+0],[-1,+0],[+0,+1]], [[-1,+0],[+0,+0],[+0,+1],[+1,+0]], [[+0,-1],[+0,+0],[+0,+1],[+1,+0]], [[-0,-1],[+0,+0],[-1,+0],[+1,+0]] ],
                         [ [[-1,-1],[-1,+0],[+0,+0],[+0,+1]], [[-0,+0],[+1,+0],[+0,+1],[-1,+1]], [[+0,-1],[+0,+0],[+1,+0],[+1,+1]], [[-0,-1],[+1,-1],[+0,+0],[-1,+0]] ] ]
        self.__boxType,self.__boxIndex = random.randint(0,6),0
    def __fixedBox(self):
        for cube in self.__boxs[self.__boxType][self.__boxIndex]:
            self.__scrData[self.__boxPt[0]+cube[0]][self.__boxPt[1]+cube[1]] = 1
    def __eliminate(self):
        row = 19
        while row > 0:
            if self.__scrData[row] == [1]*10:
                for r in range(row,0,-1):self.__scrData[r] = self.__scrData[r-1]
                continue
            row -= 1
    def __collistion(self,box):
        for cube in self.__boxs[self.__boxType][self.__boxIndex]:
            if not self.__safeScreenRowAndLine( self.__boxPt[0]+cube[0] ,self.__boxPt[1]+cube[1]) or self.__scrData[self.__boxPt[0]+cube[0]][self.__boxPt[1]+cube[1]] == 1:
                return True
        return False
    def rotate(self):
        self.__boxIndex = (self.__boxIndex + 1)%4
        self.draw()
    def move(self,type):
        move_dic = {'Left':((0,-1),(0,1)),'Right':((0,1),(0,-1)),'Down':((1,0),(-1,0))}
        self.__boxPt = self.__addTuple(self.__boxPt,move_dic.get(type)[0])
        if self.__collistion(self.__boxs[self.__boxType][self.__boxIndex]):
            self.__boxPt = self.__addTuple(self.__boxPt,move_dic.get(type)[1])
            if type == "Down":
                self.__fixedBox()
                self.__eliminate()
                self.__boxPt = (1,4)
                self.__randomCreateBox()
                self.draw()
            return True
        else:
            self.draw()
            return False
    def quickDown(self):
        while not self.move("Down"):pass
    def draw(self):
        drawPexels = lambda pt,color:self.__screen.create_rectangle(10+pt[1]*12,10+pt[0]*12,20+pt[1]*12,20+pt[0]*12,fill=color)
        screen.delete("all")
        for r in range(20):
            for l in range(10):drawPexels((r,l),"black" if self.__scrData[r][l] else "gray") 
        for cub in self.__boxs[self.__boxType][self.__boxIndex]:drawPexels(self.__addTuple(cub,self.__boxPt),"black")
top      = Tkinter.Tk()
screen   = Tkinter.Canvas(top,width=400,height= 400,bg = "green")
game     = Tetris(screen)
game.draw()
def keyFunc(event):
    print event.char
    keyFunDic = {'j':[game.move,"Left"],'l':[game.move,"Right"],'i':[game.rotate,None],'k':[game.move,"Down"],' ':[game.quickDown,None]}
    if not keyFunDic.get(event.char) == None:
        keyFunDic.get(event.char)[0](keyFunDic.get(event.char)[1]) if not (keyFunDic.get(event.char)[1] == None) else keyFunDic.get(event.char)[0]()
screen.pack()
top.bind('<Key>',keyFunc)
def timeFunc():
    global top
    game.move("Down")
    top.after(1000,timeFunc)
top.after(1000,timeFunc)
Tkinter.mainloop()
