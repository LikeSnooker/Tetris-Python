import Tkinter
import random
import threading
import time
class Tetris:
    'Tetris game'
    def __init__(self,screen):
        self.__box      = [[0 for x in range(4)] for y in range(4)]
        self.__box_row  = 1
        self.__box_line = 3
        self.__score    = 0
        self.__screen   = screen
        self.__screen_data  = [[0 for x in range(10)] for y in range(20)]
        self.__boxRow2ScreenRow   = lambda row  : row  + self.__box_row  
        self.__boxLine2ScreenLine = lambda line : line + self.__box_line
        self.__screenRow2BoxRow   = lambda row  : row  - self.__box_row
        self.__screenLine2BoxLine = lambda line : line - self.__box_line 
        self.__safeScreenRowAndLine  = lambda row,line : row >-1 and row < 20 and line > -1 and line < 10
        self.__safeBoxRowAndLine     = lambda row,line : row >-1 and row <4   and line > -1 and line < 4
        self.__randomCreateBox()
    def __randomCreateBox(self):
        boxs  = [ [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]] ,[[0,0,1,0],[0,0,1,0],[0,1,1,0],[0,0,0,0]] ,
                  [[0,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,0,0]] ,[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]] ,
                  [[0,0,0,0],[0,1,1,0],[1,1,0,0],[0,0,0,0]] ,[[0,0,0,0],[0,1,0,0],[1,1,1,0],[0,0,0,0]] ,
                  [[0,0,0,0],[1,1,0,0],[0,1,1,0],[0,0,0,0]] ]
        self.__box = boxs[random.randint(0,6)]
    def __fixedBox(self):
        for row in range(4):
            for line in range(4):
                if self.__safeScreenRowAndLine(self.__boxRow2ScreenRow(row),self.__boxLine2ScreenLine(line) ):
                    if self.__box[row][line] == 1:
                        self.__screen_data[ self.__boxRow2ScreenRow(row) ][ self.__boxLine2ScreenLine(line) ] = 1
    def __eliminate(self):
        row    = self.__box_row + 3 if self.__box_row + 3 < 19 else 19
        rows   = 0
        while row > self.__box_row:
            if self.__screen_data[row] == [1,1,1,1,1,1,1,1,1,1]:
                for r in range(row,0,-1):self.__screen_data[r] = self.__screen_data[r-1]
                continue
            row -= 1
        self.__score += [100,300,500,1000][rows -1]
    def __collistion(self,box):
        for row in range(4):
            for line in range(4):
                screen_row  = self.__box_row  + row
                screen_line = self.__box_line + line
                if box[row][line] == 1:
                    if screen_row > 19 or screen_line < 0 or screen_line > 9:
                        return True
                    elif self.__screen_data[screen_row][screen_line] == 1:
                        return True
        return False
    def rotate(self):
        box_temp = [[0 for n in range(4)] for i in range(4)];
        for row in range(4) :
            for line in range(4) :
                box_temp[row][line] = self.__box[3-line][row];
        if not self.__collistion(box_temp):
            self.__box = box_temp
        self.draw()
    def move(self,type):
        move_dic = {'Left':[0,-1,0,1],'Right':[0,1,0,-1],'Down':[1,0,-1,0]}
        self.__box_row  += move_dic.get(type)[0]
        self.__box_line += move_dic.get(type)[1]
        if self.__collistion(self.__box):
            self.__box_row  += move_dic.get(type)[2];
            self.__box_line += move_dic.get(type)[3];
            if type == "Down":
                self.__fixedBox()
                self.__eliminate()
                self.__box_row  = 1
                self.__box_line = 3
                self.__randomCreateBox()
                self.draw()
            return True
        else:
            self.draw()
            return False
    def quickDown(self):
        while not self.move("Down"):pass
    def draw(self):
        screen.delete("all")
        origin_x , origin_y = 10,10
        for row in range(20):
            for line in range(10):
                x1,y1,x2,y2 = origin_x + line * 12,origin_y + row  * 12,origin_x + line * 12 + 10,origin_y + row  * 12 + 10
                self.__screen.create_rectangle(x1,y1,x2,y2,fill = "gray")
                if self.__screen_data[row][line]:
                    self.__screen.create_rectangle(x1,y1,x2,y2,fill = "black")
                box_row,box_line = self.__screenRow2BoxRow(row),self.__screenLine2BoxLine(line)
                if self.__safeBoxRowAndLine(box_row,box_line) and self.__box[box_row][box_line] == 1:
                    self.__screen.create_rectangle(x1,y1,x2,y2,fill = "black")
top      = Tkinter.Tk()
screen   = Tkinter.Canvas(top,width=400,height= 400,bg = "green")
label    = Tkinter.Label (top,text = 'hello world')
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
label.pack()
top.bind('<Key>',keyFunc)
label.config(text='wocaonima' )
def timeFunc():
    global top
    game.move("Down")
    top.after(1000,timeFunc)
top.after(1000,timeFunc)
Tkinter.mainloop()
