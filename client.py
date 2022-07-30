from http import server
from random import random
import socket
from tkinter import *
from  threading import Thread
from turtle import right
from PIL import ImageTk,Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None


canvas1 = None
canvas2 = None

playerName = None
nameEntry = None

nameWindow = None
gameWindow = None

leftBoxes = []
rightBoxes = []
finishingBox = None
playerType = None
dice = None
rollButton = None


def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1
    global screen_width
    global screen_height
    
    nameWindow = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes("-fullscreen",True)
    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="./assets/background.png")

    canvas1 = Canvas(nameWindow,width=500,height=500)
    canvas1.pack(fill="both",expand=True)
    
    canvas1.create_image(0,0,image=bg,anchor="nw")
    canvas1.create_text(screen_width/2,screen_height/5,text="enter name",font=("Chalkboard SE",100),fill="white")
    
    nameEntry = Entry(nameWindow,width=15,justify='center',font=("Chalkboard SE",50),bd=5,bg="white") 
    nameEntry.place(x=screen_width/2 -220,y=screen_height/4 +100)

    button = Button(nameWindow,text="save",font=("Chalkboard SE",30),width="15",command=saveName,height=2,bg="#80deea",bd=3)
    button.place(x=screen_width/2-130,y=screen_height/2-30)

    nameWindow.resizable(True,True)
    nameWindow.mainloop()

def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0,END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())
    gameWindow()

def gameWindow():
    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder",
    font=("Chalkboard SE",100), fill="white")
    leftBoard()
    rightBoard()
    finishingBox()
    global rollButton
    rollButton =  Button(gameWindow,text="Roll dice",fg="black",bg="grey",font=("Chalkboard SE",15),command=Rolldice,width=15,height=5)
    
    global playerName
    global playerType
    global playerTurn
    if playerType=='player1' and playerTurn:
        rollButton.place(x=screen_width/2-80,y=screen_height/2+250)
    else:
        rollButton.pack_forget()

    dice = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 100, text = "\u2680", font=("Chalkboard SE",250), fill="white")
    gameWindow.resizable(True,True)
    gameWindow.mainloop()
def finishingBox():
    global gameWindow
    global finishingBox
    global screen_width
    global screen_height

    finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=8, height=4, borderwidth=0, bg="green", fg="white")
    finishingBox.place(x=screen_width/2 - 68, y=screen_height/2 -160)
   # Creating Dice with value 1
def rollDice():
    global SERVER
    diceChoices=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    value = random.choice(diceChoices)
    global playerType,playerName,playerTurn
    rollButton.destroy()
    playerTurn = False
    if playerType=='Player1':
        server.send(f'{value}player2turn'.encode())
    if playerType=='Player2':
        server.send(f'{value}player1turn'.encode())    

def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height

    xpos = 30
    for box in range(0,11):
        if box==0:
            boxlabel = Label(gameWindow,font=("Helvetica",30),width=1,height=1,relief='ridge',borderwidth=0,bg="red")       
            boxlabel.place(x=xpos,y=screen_height/2-80)
            leftBoxes.append(boxlabel)
            xpos +=35
        else:
            boxlabel = Label(gameWindow,font=("Helvetica",30),width=1,height=1,relief='ridge',borderwidth=0,bg="white")
            boxlabel.place(x=xpos,y=screen_height/2-100)
            leftBoxes.append(boxlabel) 
            xpos += 55       
            
def rightBoard():
    global gameWindow
    global rightBoxes
    global screen_height

    xpos = 850
    for box in range(0,11):
        if box==10:
            boxlabel = Label(gameWindow,font=("Helvetica",30),width=1,height=1,relief='ridge',borderwidth=0,bg="yellow")
            boxlabel.place(x=xpos,y=screen_height/2-88)
            rightBoxes.append(boxlabel)
            xpos += 35
        else:
            boxlabel = Label(gameWindow,font=("Helvetica",30),width=1,height=1,relief='ridge',borderwidth=0,bg="white")
            boxlabel.place(x=xpos,y=screen_height/2-88)
            rightBoxes.append(boxlabel)
            xpos += 55                

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 5000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))


    # Creating First Window
    askPlayerName()




setup()