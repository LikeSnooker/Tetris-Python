import Tkinter ;import random ;import threading;import time;import sys
class Tetris:
    def __init__(self,screen):
        self.__boxPt ,self.__screen   =(1,4),screen
        self.__addTuple = lambda tuple1,tuple2:(tuple1[0]+tuple2[0],tuple1[1]+tuple2[1])
        self.__scrData  = [[0 for x in range(10)] for y in range(20)]
        self.__safeScreenRowAndLine  = lambda row,line : row >-1 and row < 20 and line > -1 and line < 10
        self.__boxs     = [ [ [[+0,-1],[+0,+0],[+0,+1],[+0,+2]], [[-1,+1],[+0,+1],[+1,+1],[+2,+1]], [[+1,-1],[+1,+0],[+1,+1],[+1,+2]], [[-1,+0],[+0,+0],[+1,+0],[+2,+0]] ],   [ [[-1,-1],[+0,-1],[+0,+0],[+0,+1]], [[-1,-0],[+0,+0],[+1,+0],[-1,+1]], [[+0,-1],[+0,+0],[+0,+1],[+1,+1]], [[+1,-1],[+0,+0],[+1,+0],[-1,-0]] ],   [ [[+0,-1],[+0,+0],[+0,+1],[-1,+1]], [[-1,-0],[+0,+0],[+1,+0],[+1,+1]], [[+0,-1],[+0,+0],[+0,+1],[+1,-1]], [[-1,-1],[-1,+0],[+0,+0],[+1,+0]] ],   [ [[-0,-0],[-0,+1],[+1,-0],[+1,+1]], [[-0,-0],[-0,+1],[+1,-0],[+1,+1]], [[-0,-0],[-0,+1],[+1,-0],[+1,+1]], [[-0,-0],[-0,+1],[+1,-0],[+1,+1]] ],   [ [[+0,-1],[+0,+0],[-1,+0],[-1,+1]], [[-1,+0],[+0,+0],[+0,+1],[+1,+1]], [[+1,-1],[+1,+0],[+0,+0],[+0,+1]], [[-1,-1],[+0,-1],[+0,+0],[+1,+0]] ],   [ [[+0,-1],[+0,+0],[-1,+0],[+0,+1]], [[-1,+0],[+0,+0],[+0,+1],[+1,+0]], [[+0,-1],[+0,+0],[+0,+1],[+1,+0]], [[-0,-1],[+0,+0],[-1,+0],[+1,+0]] ],   [ [[-1,-1],[-1,+0],[+0,+0],[+0,+1]], [[-0,+0],[+1,+0],[+0,+1],[-1,+1]], [[+0,-1],[+0,+0],[+1,+0],[+1,+1]], [[-0,-1],[+1,-1],[+0,+0],[-1,+0]] ] ] #This array contains each box and the way it rotates. like this ...... [[I1,I2,I3,I4],[J1,J2,J3,J4],[L1,L2,L3,L4],[O1,02,O3,O4],[S1,S2,S3,S4],[T1,T2,T3,T4],[Z1,Z2,Z3,Z4] ]
        self.__randomCreateBox()
    def __randomCreateBox(self): 
        self.__boxPt,self.__boxType,self.__boxIndex = (1,4),random.randint(0,6),0
        if self.__collistion(self.__boxs[self.__boxType][self.__boxIndex]):sys.exit()
    def __collistion(self,box): #
        for cube in self.__boxs[self.__boxType][self.__boxIndex]:
            if not self.__safeScreenRowAndLine( self.__boxPt[0]+cube[0] ,self.__boxPt[1]+cube[1]) or self.__scrData[self.__boxPt[0]+cube[0]][self.__boxPt[1]+cube[1]] == 1:
                return True
        return False
    def update(self,type):
        update_dic = {'Left'  : ['_Tetris__boxPt'   , lambda : (self.__boxPt[0]   , self.__boxPt[1] - 1) ], 'Right': ['_Tetris__boxPt'   , lambda : (self.__boxPt[0]   , self.__boxPt[1] + 1) ], 'Down' : ['_Tetris__boxPt'   , lambda : (self.__boxPt[0]+1 , self.__boxPt[1])     ], 'Up'   : ['_Tetris__boxIndex', lambda : (self.__boxIndex +1) % 4] }
        old = getattr(self,update_dic.get(type)[0])
        setattr(self,update_dic.get(type)[0], update_dic.get(type)[1]() )
        rest = self.__collistion(self.__boxs[self.__boxType][self.__boxIndex])
        if rest:
            setattr(self,update_dic.get(type)[0],old)
            if type == "Down": 
                for cube in self.__boxs[self.__boxType][self.__boxIndex]:self.__scrData[self.__boxPt[0]+cube[0]][self.__boxPt[1]+cube[1]] = 1
                row = 19
                while row > 0:
                    if self.__scrData[row] == [1]*10 : 
                        for r in range(row,0,-1):self.__scrData[r],row = self.__scrData[r-1],row + (1 if r == row else 0)
                    row -= 1
                self.__randomCreateBox()
        self.draw()
        return True if rest else False
    def quickDown(self):
        while not self.update("Down"):pass
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
    keyFunDic = {'j':[game.update,"Left"],'l':[game.update,"Right"],'i':[game.update,"Up"],'k':[game.update,"Down"],' ':[game.quickDown ,None]}
    if not keyFunDic.get(event.char) == None:
        keyFunDic.get(event.char)[0](keyFunDic.get(event.char)[1]) if not (keyFunDic.get(event.char)[1] == None) else keyFunDic.get(event.char)[0]()
screen.pack()
top.bind('<Key>',keyFunc)
def timeFunc():
    global top
    game.update("Down")
    top.after(1000,timeFunc)
top.after(1000,timeFunc)
Tkinter.mainloop()

