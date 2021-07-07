from random import randint as rand
from turtle import Turtle, Screen
from time import sleep

# This is a superclass of all buttons. It sets characteristics for all buttons, and the __init __() method allows you to set these characteristics when creating a new object:
class Button:
	def __init__(self, x, y, l=100, w=40, t="Exit"):
		self.length = l
		self.width  = w
		self.x_cor  = x
		self.y_cor  = y
		self.text   = t

# This is a subclass of the Button class. It has a method that draws rectangular buttons based on their parameters:
class RectangleButton(Button):
	def paint_button(self, size=27, color="black", text_color="white"):
		p.pencolor(color)
		p.pensize(5)
		p.penup()
		p.fillcolor(color)
		p.begin_fill()
		p.goto(self.x_cor,  self.y_cor)
		p.pendown()
		p.goto(self.x_cor + self.length,   self.y_cor)
		p.goto(self.x_cor + self.length,   self.y_cor + self.width)
		p.goto(self.x_cor,  self.y_cor +   self.width)
		p.goto(self.x_cor,  self.y_cor)
		p.end_fill()
		p.goto(self.x_cor + self.length/2, self.y_cor)
		p.pencolor(text_color)
		p.write(self.text, move = False, align="center", font = ("Arial", size, "normal"))

# This is a class for creating an exit button. It is rectangular, so it inherits from the RectangleButton class and has a method that determines when a player clicks a button and closes the game:
class ExitButton(RectangleButton):
	# This method closes the game only when the player presses anywhere in the middle between the 4 corners of the button:
	def on_button_click(self, x, y):
		if (x > self.x_cor and y > self.y_cor) and (x < self.x_cor + self.length and y < self.y_cor + self.width):
			window.bye()

# This is a class for creating a button that restarts the game. It is round, so it is NOT inherited from the RectangleButton class and has a method that determines when a player presses a button and restarts the game. And it also has a method that draws a button:
class ResetButton(Button):
	diameter = 55
	# This method draws a round restart button in the specified coordinates with the specified diameter:
	def paint_button(self):
		p.pencolor("white")
		p.setheading(90)
		p.pensize(3)
		p.penup()
		p.goto(self.x_cor, self.y_cor)
		p.pendown()
		p.dot(self.diameter, "black")
		p.penup()
		p.goto(self.x_cor + self.diameter/3.5, self.y_cor)
		p.pendown()
		p.circle(self.diameter/3.5, 320, 700)
		pos = p.pos()
		p.left(120)
		p.forward(self.diameter/7)
		p.penup()
		p.goto(pos)
		p.pendown()
		p.right(270)
		p.forward(self.diameter/7)

	# This is a special method that restarts the game only when the player presses anywhere between the center of the button and its edge. It determines the square of the distance between the center of the circle and the point where the player clicked, and if it is less than the square of the radius, it means that the player clicked on the button (P.S. I got the geometry and here ...):
	def on_button_click(self, x, y):
		if (x-self.x_cor)**2 + (y-self.y_cor)**2 < (self.diameter/2)**2:
			window.clear()
			before_game()

# This function is required to select game settings before starting the game:
def before_game():
	global game_mode, window, p, exit_button, reset_button, first_entry, bot_shape
	print("GM 1 - Playing with a friend\nGM 2 - Game against the bot")
	gm = input("Type game mode(1/2): ")
	if gm == '1':
		game_mode = None
	if gm == '2':
		game_mode = False
		fentry = input("You want to have first entry?(yes/no): ")
		if fentry == "yes":
			first_entry = True
			bot_shape   = True
		if fentry == "no":
			first_entry = False
			bot_shape   = False
	start_game()

# This function starts the game - creates a playing field and interface:
def start_game():
	global row_1, row_2, row_3, is_circle, game_end, window, p
	# Startup settings:
	window.title("Tic Tac Toe")
	window.setup(width=0.5)
	window.bgcolor("white")
	p.hideturtle()
	p.pencolor("black")
	p.pensize(3)
	p.speed(0)
	# It's just a mountain of goto () that draws a field for the game:
	p.penup()
	p.goto(-100, 300)
	p.pendown()
	p.goto(-100, 100)
	p.goto( 100, 100)
	p.goto( 100, 300)
	p.goto( 100,-300)
	p.goto( 100,-100)
	p.goto(-100,-100)
	p.goto(-100,-300)
	p.goto(-100, 100)
	p.goto(-300, 100)
	p.goto( 300, 100)
	p.penup()
	p.goto(-300,-100)
	p.pendown()
	p.goto( 300,-100)
	# Here I just copied a few variables that are outside the functions and classes at the end of the program, because their values must be reset each time the game is restarted (in detail about what is responsible for each variable, I wrote at the end of the code):
	row_1 = [None, None, None]
	row_2 = [None, None, None]
	row_3 = [None, None, None]
	is_circle = False
	game_end  = False

	# Creates an object - the exit button from the game:
	exit_button = ExitButton(-150, 350)
	# Creates an object - the game restart button:
	reset_button = ResetButton(100, 370)

	# Draws buttons:
	exit_button.paint_button()
	reset_button.paint_button()

	# Here, if the player did not want to go first when playing with the bot, the bot will immediately make its move:
	if game_mode == False and first_entry == False:
		stupid_bot_AI(row_1 + row_2 + row_3)
		print(row_1, row_2, row_3, game_end)

	# Passes the value of the on_click () method, which determines which cell the player clicked on:
	window.onclick(on_click, add=True)
	# Passes the value of the on_button_click () method and adds a new binding:
	window.onclick(exit_button.on_button_click, add=True)
	window.onclick(reset_button.on_button_click, add=True)

# This function is an artificial intelligence of a "stupid" bot (ie it is a bot that puts a cross or a zero in any empty cell):
def stupid_bot_AI(game_area):
	global is_circle
	is_circle = bot_shape
	while True:
		entry = rand(0, 8)
		if game_area[entry] == None:
			if entry <  3:
				filler(entry  , 0)
			if entry >= 3 and entry <= 5:
				filler(entry-3, 1)
			if entry >  5 and entry <= 8:
				filler(entry-6, 2)
			break

# Function that draws crosses or zeros in the right place:
def tic_tac_toe(x, y):
	p.penup()
	p.goto(x, y)
	p.pendown()
	p.pensize(12)
	if is_circle == False:
		p.setheading(45)
		p.pencolor("red")
		for i in range(4):
			p.forward(90)
			p.goto(x, y)
			p.right(90)
	if is_circle == True:
		p.pencolor("blue")
		p.setheading(90)
		p.penup()
		p.goto(x+75, y)
		p.pendown()
		p.circle(75, None, 700)

# This function draws a line along 3 shapes in the right place:
def paint_line(p1, p2):
	p.pencolor("black")
	p.pensize(25)
	p.penup()
	p.goto(p1)
	p.pendown()
	p.goto(p2)
	p.penup()
	sleep(1)

# This function determines the victory in the game and draws a line along 3 figures that are in one line:
def game_win(game_area):
	global game_end
	for i in range(3):
		if row_1[i] == row_2[i] == row_3[i] == is_circle:
			paint_line((x_coords[i], 300), (x_coords[i], -300))
		elif i == 2:
			if row_1[0]   == row_1[1] == row_1[2] == is_circle:
				paint_line((-300, 200), (300, 200))
			elif row_2[0] == row_2[1] == row_2[2] == is_circle:
				paint_line((-300,   0), (300,   0))
			elif row_3[0] == row_3[1] == row_3[2] == is_circle:
				paint_line((-300,-200), (300,-200))
			else:
				if row_1[0] == row_2[1] == row_3[2] == is_circle:
					paint_line((-275, 275), ( 275,-275))
				if row_1[2] == row_2[1] == row_3[0] == is_circle:
					paint_line(( 275, 275), (-275,-275))
	for line in combinations:
		if game_area[line[0]] == game_area[line[1]] == game_area[line[2]] == is_circle:
			game_end = True
			if is_circle == True:
				end_game("Circles")
			else:
				end_game("Criss-crosses")
	# Here the function declares a draw (a draw occurs when all the cells are already filled, and 3 figures have not been in a row. The game is over. There are no winners):
	if None not in game_area and game_end == False:
		game_end = True
		end_game("Draw")

# This function announces the winner:
def end_game(winner):
	if winner == "Draw":
		print("Tie!")
		sleep(1)
	else:
		if game_mode == None:
			if winner == "Circles":
				print("Circles won!")
			if winner == "Criss-crosses":
				print("Crosses won!")
		else:
			if bot_shape == is_circle:
				print("The bot won!")
			else:
				print("You won!")
	sleep(3)
	window.bye()

# This is a helper function. It fills the contents of each cell:
def filler(column, row):
	tic_tac_toe(x_coords[column], y_coords[row])
	if row == 0:
		row_1[column] = is_circle
	if row == 1:
		row_2[column] = is_circle
	if row == 2:
		row_3[column] = is_circle

# This function, together with window.onclick (), reads which cell the player clicks on and sets this cell to:
def on_click(x, y):
	global is_circle, game_mode

	if game_mode == False or game_mode == True:
		is_circle = not bot_shape

	if x < -100  and x > -300:
		index = 0
	elif x < 100 and x > -100:
		index = 1
	elif x < 300 and x >  100:
		index = 2
	else:
		index = None
	none_on_click = False # This is an helper variable that is required for the bot to make its move only after the player clicks an empty cell and fills it.
	if index != None:
		if y > 100 and  y <  300:
			if row_1[index] != True and row_1[index] != False:
				filler(index, 0)
				none_on_click = True
		if y > -100 and y <  100:
			if row_2[index] != True and row_2[index] != False:
				filler(index, 1)
				none_on_click = True
		if y > -300 and y < -100:
			if row_3[index] != True and row_3[index] != False:
				filler(index, 2)
				none_on_click = True
		game_win(row_1 + row_2 + row_3)

	# Here, if the game mode is set with a friend, then every time one of the players clicks on the cell, the value of is_circle changes to the opposite (ie the cross changes to zero or vice versa):
	if game_mode == None and none_on_click == True:
		if (x > -300 and y < 300) and (x < 300 and y >-300):
			is_circle = not is_circle
	# Here, if the game mode is set against the bot, then every time the player makes his move, the bot is launched, which immediately makes its move:
	if game_mode == False and none_on_click == True and game_end == False:
		stupid_bot_AI(row_1 + row_2 + row_3)
		game_win(row_1 + row_2 + row_3)

# Creates an object - a window and a turtle:
window = Screen()
p = Turtle()

# These are the parameters of the playing field:
# These tuples contain the contents of each cell. None is an empty cell, True is a cell with a cross, and False is a cell with a circle.
row_1       = (None, None, None)
row_2       = (None, None, None)
row_3       = (None, None, None)
x_coords    = (-200,    0,  200) # all possible X-coordinates of the cell. (The coordinate of each cell is a point in its center)
y_coords    = ( 200,    0, -200) # all possible Y-coordinates of the cell.
combinations = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)) # Here all combinations at which 3 figures become in one line are contained.
is_circle   = True  # If set to False, the function draws a cross, and if set to True, a circle.
game_mode   = None  # If the value is None, then it is a game mode with a friend, if the value is False, then it is a game mode against a bot.
game_end    = False # This variable indicates to the bot that the three pieces are already in a line and the game is over so that he does not try to move on.
first_entry = False # This variable indicates who walks first when playing with the bot. If set to True, then the player goes first, and if set to False, then the bot.
bot_shape   = True  # This is an helper variable that indicates which figure the player and the bot are walking. Since crosses always go first, if the player chooses to walk first, he will walk crosses, and the bot will walk zeros and vice versa.

before_game()

window.mainloop()
