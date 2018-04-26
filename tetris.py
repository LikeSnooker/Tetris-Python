import Tkinter
import random
box      = [[0 for x in range(4)] for y in range(4)]
box_row  = 1
box_line = 3
score    = 0
top = Tkinter.Tk()
screen   = Tkinter.Canvas(top,width=400,height= 400,bg = "green")
label    = Tkinter.Label (top,text = 'hello world')
screen.pack()
label.pack()
screen_d = [[0 for x in range(10)] for y in range(20)]
def box_empty(box):
    for r in range(4):
        for l in range(4):
            box[r][l] = 0
def box_I(box):
    box_empty(box)
    box[0][0] = 1
    box[1][0] = 1
    box[2][0] = 1
    box[3][0] = 1

def box_J(box):
    box_empty(box)
    box[0][0] = 1
    box[1][0] = 1
    box[1][1] = 1
    box[1][2] = 1

def box_L(box):
    box_empty(box)
    box[0][2] = 1
    box[1][0] = 1
    box[1][1] = 1
    box[1][2] = 1

def box_O(box):
    box_empty(box)
    box[0][0] = 1
    box[0][1] = 1
    box[1][0] = 1
    box[1][1] = 1

def box_S(box):
    box_empty(box)
    box[0][1] = 1
    box[0][2] = 1
    box[1][0] = 1
    box[1][1] = 1

def box_T(box):
    box_empty(box)
    box[0][1] = 1
    box[1][0] = 1
    box[1][1] = 1
    box[1][2] = 1

def box_Z(box):
    box_empty(box)
    box[0][0] = 1
    box[0][1] = 1
    box[1][1] = 1
    box[1][2] = 1

def createBox(box,type):
    func_dic = {'I':box_I,'J':box_J,'L':box_L,'O':box_O,'S':box_S,'T':box_T,'Z':box_Z}
    func_dic.get(type)(box)
def randomCreateBox(box):
    box_types = ['I','J','L','O','S','T','Z']
    createBox(box,box_types[random.randint(0,6)])
def fixedBox(box):
    for row in range(4):
        for line in range(4):
            if box[row][line]:
                screen_d[box_row+row][box_line+line] = 1

def eliminateRow(row):
    for r in range(row,0,-1):
        for l in range(10):
            screen_d[r][l] = screen_d[r-1][l]

def eliminate():
    global score
    bottom = box_row + 3 if box_row + 3 < 19 else 19
    rows   = 0
    for row in range(bottom,box_row-1,-1):
        has_space = False
        for line in range(10):
            if screen_d[row][line] == 0:
                has_space = True
                break
        if not has_space :
            rows +=1
            eliminateRow(row)
    if rows == 1:
         score += 100
    elif rows == 2:
        score += 300
    elif rows == 3:
        score += 500
    elif rows == 4:
        score += 1000
def collistion():
    for row in range(4):
        for line in range(4):
            screen_row  = box_row + row
            screen_line = box_line + line
            if box[row][line] == 1:
                if screen_row > 19 or screen_line < 0 or screen_line > 9:
                    return True
                elif screen_d[screen_row][screen_line] == 1:
                    return True
    return False
def rotate():
    global box
    box_temp = [[0 for n in range(4)] for i in range(4)];
    for row in range(4) :
        for line in range(4) :
            box_temp[row][line] = box[3-line][row];
    box = box_temp
def move(type):
    global box_row
    global box_line
    box_row_retrace  = 0
    box_line_retrace = 0
    if type == "Left":
        box_line -= 1
        box_row_retrace  = 0
        box_line_retrace = +1
    elif type == "Right":
        box_line += 1
        box_row_retrace  = 0
        box_line_retrace = -1
    elif type == "Down":
        box_row  += 1
        box_row_retrace  = -1
        box_line_retrace = 0
    if collistion():
        box_row  += box_row_retrace;
        box_line += box_line_retrace;
        return True
    else:
        return False
def quickDown():
    global box
    global box_row
    global box_line
    global label
    global score
    dd = move("Down")
    while not dd:
        dd = move("Down")
    fixedBox(box)
    eliminate()
    box_row = 1
    box_line = 3
    randomCreateBox(box)
    label.config(text=str(score))
def keyFunc(event):
    global screen 
    global screen_d
    global box
    collistion = False
    if event.keycode   == 8124162:
        collistion = move("Left")
    elif event.keycode == 8189699:
        collistion = move("Right")
    elif event.keycode == 8255233:
        collistion = move("Down")
    elif event.keycode == 8320768:
        rotate()
    elif event.keycode == 3211296:
        quickDown()
    if not collistion:
        draw(screen_d,screen)
def draw(screen_data,screen):
    screen.delete("all")
    global box
    origin_x = 10
    origin_y = 10
    for row in range(20):
        for line in range(10):
            x1 = origin_x + line * 12
            y1 = origin_y + row  * 12
            x2 = x1 + 10
            y2 = y1 + 10
            screen.create_rectangle(x1,y1,x2,y2,fill = "gray")
            if screen_data[row][line]:
                screen.create_rectangle(x1,y1,x2,y2,fill = "black")
    for row in range(4):
        for line in range(4):
            if box[row][line]:
                x1 = origin_x + (line+ box_line) * 12
                y1 = origin_y + (row+  box_row)  * 12
                x2 = x1 + 10
                y2 = y1 + 10
                screen.create_rectangle(x1,y1,x2,y2,fill = "black")

randomCreateBox(box)
draw(screen_d,screen)
top.bind('<Key>',keyFunc)
screen.update()
label.config(text='wocaonima' )
Tkinter.mainloop()