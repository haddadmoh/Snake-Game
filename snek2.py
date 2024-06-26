from tkinter import*
from tkinter import messagebox
import pygame
import random
#------------------------------------Constants and initial variables------------------------------------------------#
gameover = False
game_paused = False
music = False
# A list that contains the initial coordinates of the snake
snek_coordinates = [[290, 300]]
space_size = 10
# Initialize direction and score
direction = ""
score = 0
speed = 80
#-------------------------------------------------------------------------------------------------------------------#

#------------------------------------Functions's definiton----------------------------------------------------------#
def toggle_sound():
    global music
    if not music:
        pygame.mixer.init()
        pygame.mixer.music.load("p3.mp3")
        pygame.mixer.music.play(-1)
        music = True
    else:
        pygame.mixer.music.stop()
        music = False

def set_difficulty(level):
    global speed
    if level == "Easy":
        speed = 80
    elif level == "Medium":
        speed = 60
    else:
        speed = 40

def show_instructions():
    instructions = "Use arrow keys to control the snake.\nEat the food to grow longer."
    messagebox.showinfo("Instructions", instructions)
   
def exit_game():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        win.destroy()

def menu():
    m = Menu(win)
    win.config(menu = m)
    
    sm1 = Menu(win, tearoff = 0)
    m.add_cascade(label = "Game", menu = sm1)
    sm1.add_command(label = "Pause/Resume", command = toggle_pause)
    sm1.add_separator()
    sm1.add_command(label = "Exit", command = exit_game)

    sm2 = Menu(win, tearoff=0)
    m.add_cascade(label = "Options", menu = sm2)
    sm2.add_command(label = "Easy", command = lambda: set_difficulty("Easy"))
    sm2.add_command(label = "Medium", command = lambda: set_difficulty("Medium"))
    sm2.add_command(label = "Hard", command = lambda: set_difficulty("Hard"))
    sm2.add_separator()
    sm2.add_command(label="soundtrack", command = toggle_sound)
    
    sm3 = Menu(win, tearoff = 0)
    m.add_cascade(label = "Help", menu = sm3)
    sm3.add_command(label = "Instructions", command = show_instructions)
    
def toggle_pause():
    global game_paused,gameover
    game_paused = not game_paused
    if gameover:
        return
    if game_paused:
        ch.place(relx=0.5, rely=0.5, anchor=CENTER)
        ch.config(text="Game Paused", fg="white", bg="gray")
    else:
        ch.place_forget()
        ch.config(text="", bg="white")

def spawn_food():
    global space_size
    x = random.randrange(10, 590, 10) 
    y = random.randrange(10, 450, 10)
    return can.create_oval(x, y, x + space_size, y + space_size, fill='green')

def set_direction(new_direction):
    global direction
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
            
    if new_direction == "right":
        if direction != "left":
            direction = new_direction
    
    if new_direction == "up":
        if direction != "down":
            direction = new_direction
    
    if new_direction == "down":
        if direction != "up":
            direction = new_direction

def create_snek():
    global snek_coordinates
    can.delete('snek')
    for i in snek_coordinates :
        x = i[0]
        y = i[1]
        can.create_rectangle(x, y, x + space_size, y + space_size, fill = 'blue', tag = 'snek')

def check_collision():
    head_x, head_y = snek_coordinates[0]
    if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 500 or (head_x, head_y) in snek_coordinates[1:]:
        return True

    else:
        return False

def game_over():
    global gameover
    gameover = True
    ch.place(relx=0.5, rely=0.5, anchor=CENTER)
    ch.config(text="Game Over!", fg="white", bg="red")
    #music = True
    #toggle_sound()

def update_game():
    global food,score,speed
    if gameover:
        return
    if not game_paused:
        head_x, head_y = snek_coordinates[0]
        if direction == "up":
            head_y -= 10
        elif direction == "down":
            head_y += 10
        elif direction == "left":
            head_x -= 10
        elif direction == "right":
            head_x += 10    
        snek_coordinates.insert(0,(head_x,head_y))
        if (head_x == can.coords(food)[0]) and (head_y == can.coords(food)[1]):
            can.delete(food)
            food = spawn_food()
            score += 1
            label.config(text="Score:{}".format(score))
        else :
            del snek_coordinates[-1]   
        if check_collision():
            game_over()   
        create_snek()
    win.after(speed, update_game)
#-------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------Main program---------------------------------------------------------#
# Create the main window
win = Tk()
win.geometry("600x500")
win.title("Snek game")

menu()

# A label to show score
label = Label(win, text="Score:{}".format(score), font=('consolas', 20))
label.pack()

# Create a canvas and draw an object (snek)
can = Canvas(win, width = 600, height = 500, bg = 'ivory')
can.pack()

# Will later be used to show game status "Game paused"
ch = Label(can, text="Game Running", font=("Helvetica", 16))
# Food creation
food = spawn_food()

# Bind key events to set_direction function
win.bind("<Right>",lambda event:set_direction("right"))
win.bind("<Left>",lambda event:set_direction("left"))
win.bind("<Up>",lambda event:set_direction("up"))
win.bind("<Down>",lambda event:set_direction("down"))
win.bind('<Escape>', lambda e:win.destroy())
win.bind('p', lambda event: toggle_pause())

update_game()

win.mainloop()