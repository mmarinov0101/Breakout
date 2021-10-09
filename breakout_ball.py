#Set screen revolution to 1536x864
#Cheat code - "gobig" for the paddle to become wide as the screen so the ball can't fall
from tkinter import *
import time
import random

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(20,20,50,50, fill = color)
        self.canvas.move(self.id, 500, 500)
        self.x = 5
        self.y = 6
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.is_at_bottom = False


    def touch_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True;
            return False;


    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = -(self.y)
        if pos[3] >= self.canvas_height:
            self.is_at_bottom = True
        if pos[0] <= 0:
            self.x = -(self.x)
        if pos[2] >= self.canvas_width:
            self.x = -(self.x)
        if self.touch_paddle(pos) == True:
            self.y = -(self.y)


class Paddle:
    def __init__(self, canvas, x1, y1, x2, y2, z, color):  # we use the variable z to display the paddles in a two-dimensional array
        self.canvas = canvas
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill = color)
        self.canvas.move(self.id, 10, z)



class MovingPaddle():
    def __init__(self, canvas, x1, y1, x2, y2, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill = color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -8

    def turn_right(self, evt):
        self.x = 8

def createPaddles(m, n, paddle_array, canvas):  # Creates a two-dimensional array of paddles
    for i in range(m):
        row = []
        for j in range(n):
            row.append(0)
        paddle_array.append(row)


    x = 20
    y = 10
    colours = ["orange", "yellow", "green", "blue", "white", "brown"]
    for i in range(m):
        for j in range(n):
            pad = Paddle(canvas, x, 80, x+130, 110, y, colours[0])
            random.shuffle(colours)
            paddle_array[i][j] = pad.id
            x = x + 150
        y = y + 40
        x = 20

def collision(pos, id, canvas):   #Checks if the ball hits a paddle
    result = False
    paddle_pos = canvas.coords(id)
    if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
        if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
            result = True;
    if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
        if pos[1] <= paddle_pos[3] and pos[1] >= paddle_pos[1]:
            result = True;
    return result

def check_collision(paddle, canvas, ball, paddle_array, scoreText, button6_window, button7_window, window, first_game = True):  #Deletes paddles/rows, the game ends if there are no rows left
    ball_pos = canvas.coords(ball.id)
    row = len(paddle_array)
    if(row == 0):
        canvas.delete(button6_window)
        canvas.delete(button7_window)
        displayWinOrLose(True, paddle, ball, paddle_array, window, canvas)
    for i in range(row):
        col1 = len(paddle_array[i])
        for j in range(col1):
            if collision(ball_pos, paddle_array[i][j], canvas) == True:
                canvas.delete(paddle_array[i][j])
                del paddle_array[i][j]
                global score, score_reset
                if((not first_game) and (score_reset == True)): #Checks if the user plays another game and restarts the score
                    score = 0
                    score_reset = False
                score = score + 10
                canvas.itemconfig(scoreText, text="Score: " + str(score))
                if(len(paddle_array[i]) == 0):
                    del paddle_array[i]
                    if(len(paddle_array) != 0):
                        col2 = len(paddle_array[i-1])
                    else:
                        col2 = 0
                        ball.y = -(ball.y)
                    canvas.move(ball.id, ball.x, ball.y)
                    if col1 != col2:
                        break
                else:
                    col2 = len(paddle_array[i])
                    ball.y = -(ball.y)
                    canvas.move(ball.id, ball.x, ball.y)
                    if col1 != col2:
                        break


def displayWinOrLose(win, paddle, ball, paddle_array, window, canvas):  #Prompts the player to put their information to be stored in the scoreboard
    if(win):
        result = "YOU WON!"
    else:
        result = "YOU LOST!"
    game_result = canvas.create_text(750, 400, fill="white", font="Times 50 italic bold", text=result)
    window.update()
    time.sleep(2)
    if not win:
        for i in range(len(paddle_array)):
            for j in range(len(paddle_array[i])):
                canvas.delete(paddle_array[i][j])
        window.update()
    canvas.delete(ball.id)
    canvas.delete(paddle.id)
    canvas.delete(game_result)
    nameLabel = canvas.create_text(750, 300, fill="white", font="Times 50 italic bold", text="Name for Scoreboard:")
    playerName = Entry(window)
    playerName_window = canvas.create_window(750, 400, window=playerName)
    button = Button(window, text="Save", command=lambda: saveScore(playerName.get(), window), bg="white")
    button_window = canvas.create_window(750, 500, window=button)
    window.mainloop()

def saveScore(playerName, window):                  #Puts the player's name and score in a list with previous
    players_info = []                               #players, sorts the list and saves it to a file, which
    players_info = makeListOfPlayers(players_info)  #will be used to display the scoreboard
    current_player = []
    current_player.append(playerName)
    current_player.append(str(score))
    players_info.append(current_player)

    global score_reset
    score_reset = True
    
    for i in range(len(players_info)):
        for j in range(len(players_info)):
            if i == j:
                continue
            if int(players_info[i][1]) > int(players_info[j][1]):
                temp = players_info[i]
                players_info[i] = players_info[j]
                players_info[j] = temp
    file = open("scoreBoard.txt", "w")
    for i in range(len(players_info)):
        for j in range(2):
            file.write(players_info[i][j] + " ")
        file.write("\n")
    file.close()
    showScoreBoard(window)

def showScoreBoard(window):
    window.destroy()
    players_info = []
    players_info = makeListOfPlayers(players_info)

    window = Tk()
    window.title("Scoreboard")
    window.resizable(0, 0)
    window.wm_attributes("-topmost", 1)
    canvas = Canvas(window, width = 700, height = 800, bd = 0, highlightthickness = 0, bg= "lightblue")
    canvas.pack()
    scoreboard = canvas.create_text(350, 100, fill="black", font="Times 50 italic bold", text="Scoreboard:")
    headings = canvas.create_text(350, 300, fill="black", font="Times 30 italic bold", text="RANK            SCORE            NAME")
    for i in range(len(players_info)):
        k = 45*i
        playerPosition = canvas.create_text(100, k + 380, fill="black", font="Times 25 italic bold", anchor=W, text=str(i+1))
        playerName = canvas.create_text(350, k + 380, fill="black", font="Times 25 italic bold", text=players_info[i][1])
        playerScore = canvas.create_text(650, k + 380, fill="black", font="Times 25 italic bold", anchor=E, text=players_info[i][0])
    button21 = Button(window, text="Main menu", command=lambda: menu(False, window, canvas, False), bg="gray")
    button21_window = canvas.create_window(350, 760, window=button21, width=150, height=50)
    window.update()
    window.mainloop()

def makeListOfPlayers(players_info):   #Reads information from a file and makes a list of each player's name and score
    file = open("scoreBoard.txt", "r")
    file_input = file.read()
    file.close()
    file_input = file_input.split()
    players_info = []
    for i in range(int(len(file_input)/2)):
        single_player_info = []
        for j in range(2):  
            single_player_info.append(file_input[0])
            file_input.pop(0)
        players_info.append(single_player_info)
    return players_info

def pause(ball, paddle, canvas, window, button6_window, button7_window, img=""):
    canvas.delete(button6_window)
    canvas.delete(button7_window)
    if img != "":
        imgg = canvas.create_image(768,432,image=img, anchor=CENTER)
        txt = "RESUME"
    else:
        imgg = ""
        txt = "UNPAUSE"

    old_x = ball.x
    old_y = ball.y
    old_z = paddle.x
    ball.x = 0
    ball.y = 0

    button7_window = canvas.create_window(768, 432)
    button7 = Button(window, text=txt, command=lambda: unpause(ball, paddle, old_x, old_y, old_z, button7_window, imgg, canvas, window), bg="white")
    canvas.itemconfig(button7_window, window=button7, height=50, width=100)
    paddle.x = 0
    paddle.canvas.unbind_all('<KeyPress-Left>')
    paddle.canvas.unbind_all('<KeyPress-Right>')

def unpause(ball, paddle, old_x, old_y, old_z, button, imgg, canvas, window):
    canvas.delete(button)
    if imgg != "":
        canvas.delete(imgg)
    countdown = canvas.create_text(768, 432, fill="white", font="Times 60 italic bold", text="3")
    canvas.update()
    time.sleep(1)
    canvas.itemconfig(countdown, text="2")
    canvas.update()
    time.sleep(1)
    canvas.itemconfig(countdown, text="1")
    canvas.update()
    time.sleep(1)
    canvas.delete(countdown)
    button6_window = canvas.create_window(1450, 30)
    button6 = Button(window, text="Pause", command=lambda: pause(ball, paddle, canvas, window, button6_window, button7_window), bg="white")
    canvas.itemconfig(button6_window, window=button6)
    
    img = PhotoImage(file="excel3.png")
    button7_window = canvas.create_window(1350, 30)
    button7 = Button(window, text="Boss Key", command=lambda: pause(ball, paddle, canvas, window, button6_window, button7_window, img), bg="white")
    canvas.itemconfig(button7_window, window=button7)

    ball.x = old_x
    ball.y = old_y
    paddle.x = old_z
    paddle.canvas.bind_all('<KeyPress-Left>', paddle.turn_left)
    paddle.canvas.bind_all('<KeyPress-Right>', paddle.turn_right)

def onKeyPress(canvas, paddle_id, event):
    global pressedButtons
    pressedButtons = pressedButtons + event.char
    for i in range(len(pressedButtons)):
        if(i <= len(pressedButtons)-5):
            if pressedButtons[i:i+5] == "gobig":
                canvas.coords(paddle_id, 0, 780, 1536, 810)
                pressedButtons = pressedButtons.replace("gobig", "")


def startGame(canvas, window, welcome,
    button1_window, button2_window, button4_window, button5_window, score, first_game = True):
    canvas.delete(welcome)
    canvas.delete(button1_window)
    canvas.delete(button2_window)
    canvas.delete(button4_window)
    canvas.delete(button5_window)

    
    file = open("colours.txt", "r") #Chooses a color for the ball/paddle
    file_input = file.read()
    file.close()
    file_input = file_input.split()
    listOfShapes = []
    for i in range(2):
        shape = []
        for j in range(2):
            shape.append(file_input[0])
            file_input.pop(0)
        listOfShapes.append(shape)
    paddle = MovingPaddle(canvas, 420, 480, 720, 510, listOfShapes[0][1])
    ball = Ball(canvas, paddle, listOfShapes[1][1])

    window.bind('<KeyPress>',lambda event, a=canvas, b=paddle.id: onKeyPress(a, b, event)) #For the cheat code

    paddle_array = []  # An array which will store the ID of every non-moving paddle
    createPaddles(5, 10, paddle_array, canvas)

    txt = "Score: " + str(score)
    scoreText = canvas.create_text(100, 30, fill="white", font="Times 30 italic bold", text=txt)

    countdown = canvas.create_text(768, 432, fill="white", font="Times 60 italic bold", text="3")
    canvas.update()
    time.sleep(1)
    canvas.itemconfig(countdown, text="2")
    canvas.update()
    time.sleep(1)
    canvas.itemconfig(countdown, text="1")
    canvas.update()
    time.sleep(1)
    canvas.delete(countdown)

    button6_window = canvas.create_window(1450, 30)
    button6 = Button(window, text="Pause", command=lambda: pause(ball, paddle, canvas, window, button6_window, button7_window), bg="white")
    canvas.itemconfig(button6_window, window=button6)
    
    img = PhotoImage(file="excel3.png")
    button7_window = canvas.create_window(1350, 30)
    button7 = Button(window, text="Boss Key", command=lambda: pause(ball, paddle, canvas, window, button6_window, button7_window, img), bg="white")
    canvas.itemconfig(button7_window, window=button7)

    while ball.is_at_bottom == False:
        ball.draw()
        paddle.draw()
        check_collision(paddle, canvas, ball, paddle_array, scoreText, button6_window, button7_window, window, first_game)
        window.update()
        time.sleep(0.01)
    canvas.delete(button6_window)
    canvas.delete(button7_window)
    displayWinOrLose(False, paddle, ball, paddle_array, window, canvas)

def change_colours(option, color, canvas, window): #Option 1 for paddle and 2 for ball
    file = open("colours.txt", "r")
    file_input = file.read()
    file.close()
    file_input = file_input.split()
    listOfShapes = []
    for i in range(2):
        shape = []
        for j in range(2):
            shape.append(file_input[0])
            file_input.pop(0)
        listOfShapes.append(shape)
    if(option == 1): #Paddle
        listOfShapes[0][1] = color
    if(option == 2): #Ball
        listOfShapes[1][1] = color
    file = open("colours.txt", "w")
    for i in range(2):
        for j in range(2):
            file.write(listOfShapes[i][j] + " ")
        file.write("\n")
    file.close()
    update_text = canvas.create_text(750, 560, fill="white", font="Times 35 italic bold", text="The change has been made!")
    window.update()
    time.sleep(2)
    canvas.delete(update_text)

def settings(window, canvas, welcome, button1_window, button2_window, button4_window, button5_window):
    canvas.delete(welcome)
    canvas.delete(button1_window)
    canvas.delete(button2_window)
    canvas.delete(button4_window)
    canvas.delete(button5_window)
    colour_ball_txt = canvas.create_text(250, 160, fill="white", font="Times 35 italic bold", text="Ball Color")
    button8 = Button(window, command=lambda: change_colours(2, "red", canvas,window), bg="red")
    button8_window = canvas.create_window(150, 280, window=button8, width=100, height=100)
    button9 = Button(window, command=lambda: change_colours(2, "blue", canvas,window), bg="blue")
    button9_window = canvas.create_window(251, 280, window=button9, width=100, height=100)
    button10 = Button(window, command=lambda: change_colours(2, "green", canvas,window), bg="green")
    button10_window = canvas.create_window(351, 280, window=button10, width=100, height=100)
    button11 = Button(window, command=lambda: change_colours(2, "orange", canvas,window), bg="orange")
    button11_window = canvas.create_window(150, 381, window=button11, width=100, height=100)
    button12 = Button(window, command=lambda: change_colours(2, "white", canvas,window), bg="white")
    button12_window = canvas.create_window(251, 381, window=button12, width=100, height=100)
    button13 = Button(window, command=lambda: change_colours(2, "brown", canvas,window), bg="brown")
    button13_window = canvas.create_window(351, 381, window=button13, width=100, height=100)
    colour_paddle_text = canvas.create_text(1250, 160, fill="white", font="Times 35 italic bold", text="Paddle Color")
    button14 = Button(window, command=lambda: change_colours(1, "red", canvas,window), bg="red")
    button14_window = canvas.create_window(1150, 280, window=button14, width=100, height=100)
    button15 = Button(window, command=lambda: change_colours(1, "blue", canvas,window), bg="blue")
    button15_window = canvas.create_window(1251, 280, window=button15, width=100, height=100)
    button16 = Button(window, command=lambda: change_colours(1, "green", canvas,window), bg="green")
    button16_window = canvas.create_window(1351, 280, window=button16, width=100, height=100)
    button17 = Button(window, command=lambda: change_colours(1, "orange", canvas,window), bg="orange")
    button17_window = canvas.create_window(1150, 381, window=button17, width=100, height=100)
    button18 = Button(window, command=lambda: change_colours(1, "white", canvas,window), bg="white")
    button18_window = canvas.create_window(1251, 381, window=button18, width=100, height=100)
    button19 = Button(window, command=lambda: change_colours(1, "brown", canvas,window), bg="brown")
    button19_window = canvas.create_window(1351, 381, window=button19, width=100, height=100)

    button20 = Button(window, text="Main menu", command=lambda: menu(False, window, canvas), bg="brown")
    button20_window = canvas.create_window(768, 731, window=button20, width=400, height=80)

def menu(first_time = True, window="", canvas="", first_game = True):
    if(first_time):
        window = Tk()
        canvas = Canvas(window, width = 1536, height = 864, bd = 0, highlightthickness = 0, bg= "black")
    else:
        canvas.destroy()
        canvas = Canvas(window, width = 1536, height = 864, bd = 0, highlightthickness = 0, bg= "black")
    score = 0
    window.title("Breakout Ball!")
    window.resizable(0, 0)
    window.wm_attributes("-topmost", 1)
    canvas.pack()
    welcome = canvas.create_text(768, 130, fill="white", font="Times 50 italic bold", text="Welcome to Breakout!")
    button1 = Button(window, text="Start", command=lambda: startGame(canvas, window, welcome,
    button1_window, button2_window, button4_window, button5_window, score, first_game), bg="gray")
    button1_window = canvas.create_window(768, 330, window=button1, width=200, height=40)
    button2 = Button(window, text="Scoreboard", command=lambda: showScoreBoard(window), bg="gray")
    button2_window = canvas.create_window(768, 460, window=button2, width=200, height=40)
    button4 = Button(window, text="Settings", command=lambda: settings(window, canvas, welcome,
    button1_window, button2_window, button4_window, button5_window), bg="gray")
    button4_window = canvas.create_window(768, 590, window=button4, width=200, height=40)
    button5 = Button(window, text="Exit", command=window.destroy, bg="gray")
    button5_window = canvas.create_window(768, 720, window=button5, width=200, height=40)
    window.mainloop()

pressedButtons = "0000" # Used to check the input a user has throughout the whole game, looking for the cheat code
score_reset = True # Restarts the result if the user decides to play another game without restarting the game
score = 0
menu()
