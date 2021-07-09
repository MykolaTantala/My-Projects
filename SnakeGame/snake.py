"""Snake game release version 1.7

Well, I wrote a snake. This time I almost did not write comments. I think this docstring will be enough.
In fact, the code is quite simple and takes only 98 lines, not including the interface.py module.
Although the release version is far from the purity of the code that was in the first working version.
At that time, the code occupied only 70 lines. Well, as always, small almost imperceptible additions take up more code than the basic logic of the program.
Although I didn't do everything I set out to do, otherwise there would be even more lines of code.

As for how everything is arranged here, I used OOP. Well, in fact, it could do without it and the code would be shorter,
but OOP is a force, so let it be. There are three classes: the head of the snake, the body of the snake and the snake itself.
There was another class that was responsible for creating apples on the board, but then I replaced it with the create_apple() function.

The snake itself is a list, the first element of which is the head, and everything else is the tail. Well, everything is clear here.
As for how the snake moves, I did not use the Canvas.move() method to move the snake around the game field.
Instead, I did everything according to the principle that our grandfathers came up with at the beginning of the Cenozoic era, when they programmed the first Nokia.
The tail is removed - the head is added. The result is the illusion that the snake is moving.
It was very easy to write such logic, because I used to make a snake game on Scratch.

The snake changes the direction of its movement using the change_dir() method. And here I must pay attention to the existence of BUG.
It exists because the developers of tkinter did not think about this point and tkinter does not have a simple solution to this problem.
In short, if, for example, the snake moves up and at the right time in the time interval between calling the after() method and calling the move() method,
Simultaneously or with a very short period of time press the down arrow key and the right arrow, the snake will turn around and crawl into itself.
In this case, it will bite itself, which leads to loss. If I could block the ability to run two keys at the same time, there would be no such bug.
I still wrote a solution for this bug, but I didn't like it, because it made the snake harder to control.
Maybe that code can be improved somehow so that it does not restrict the movement of the snake, but for now I just cut it out and left this bug."""

from random    import randint as rand
from tkinter   import *
from interface import *

win = Tk()
win.resizable(False, False)
i = Interface(win)
c = Canvas(win, width=500, height=500, bg="black", bd=-2)
c.pack()

class SnakeHead:
	def __init__(self, dir, x, y):
		tp_coords = {(500, y  ):(  0, y  , 'right'), # У цьому словнику зберігаються усі координати потрібні, для того щоб, коли змійка доходить до краю ігрового поля, вона переносилася на протилежний край.
						 (-10, y  ):(490, y  , 'left' ), #
						 (x  , -10):(x  , 490, 'up'   ), #
						 (x  , 500):(x  , 0  , 'down' )} #
		self.direction, self.x, self.y = dir, x, y
		if (x, y) in tp_coords:
			self.x, self.y, self.direction = tp_coords[x, y]
		self.create_head()
	def __del__(self):
		c.delete("head")
	def create_head(self):
		directions = {'up'   :((self.x+2, self.y+2), (self.x+7, self.y+2)),                           # Here it all just draws a square head with two one-pixel eyes.
						  'down' :((self.x+2, self.y+7), (self.x+7, self.y+7)),                           #
						  'right':((self.x+7, self.y+2), (self.x+7, self.y+7)),                           #
						  'left' :((self.x+2, self.y+2), (self.x+2, self.y+7))}                           #
		c.create_rectangle((self.x, self.y), (self.x+10, self.y+10), fill  =  '#73C800', tag = "head")#
		c.create_rectangle(directions[self.direction][0], directions[self.direction][0], tag = "head")#
		c.create_rectangle(directions[self.direction][1], directions[self.direction][1], tag = "head")#

class SnakeBody:
	def __init__(self, x, y):
		self.x, self.y = x, y
		self.create_body()
	def __del__(self):
		c.delete(self.body_id)
	def create_body(self):
		self.body_id = c.create_rectangle((self.x, self.y), (self.x+10, self.y+10), fill = 'green4')

class Snake:
	snake, length, speed, call_id = [SnakeHead('left', 240, 240), SnakeBody(250, 240), SnakeBody(260, 240), SnakeBody(270, 240)], 4, 200, "after#0"
	def move(self):
		self.call_id = c.after(self.speed, self.move)
		displacement = {'up'   :(  0,-10), # This dictionary stores all the displacements of the snake's head when moving in a certain direction. They are added to the former coordinates of the snake's head and so it moves.
							 'down' :(  0, 10), #
							 'right':( 10, 0 ), #
							 'left' :(-10, 0 )} #
		args = self.snake[0].__dict__
		del self.snake[0]
		self.snake.insert(0, SnakeHead(args['direction'], args['x']+displacement[args['direction']][0], args['y']+displacement[args['direction']][1]))
		self.snake.insert(1, SnakeBody(args['x'], args['y']))
		if len(self.snake) > self.length:
			del self.snake[-1]
		self.collide()
	def change_dir(self, dir):
		if (dir, self.snake[0].direction) in (('up', 'up'), ('down', 'down'), ('right', 'right'), ('left', 'left'), ('up', 'down'), ('down', 'up'), ('right', 'left'), ('left', 'right')):
			return False
		self.snake[0].direction = dir
	def collide(self):
		global score
		apple_coords, gold_apple_coords = c.coords("apple")[0:2], c.coords("gold_apple")[0:2]
		if apple_coords == [self.snake[0].x, self.snake[0].y] or gold_apple_coords == [self.snake[0].x, self.snake[0].y]:
			if self.speed > 70:
				self.speed -= 2
			if apple_coords == [self.snake[0].x, self.snake[0].y]:
				self.length += 1
				score += 1
				c.delete("apple")
				create_apple()
			elif gold_apple_coords == [self.snake[0].x, self.snake[0].y]:
				self.length += 3
				score += 10
				c.delete("gold_apple")
			i.set_score(score)
		for body in self.snake[1:len(self.snake)]:
			if (body.x, body.y) == (self.snake[0].x, self.snake[0].y):
				game_over(self.call_id)
score = 0

def game_over(call_id):
	win.after_cancel(call_id)
	c.create_text(250, 200, text="GAME OVER", justify='center', font="Arial 50 bold", fill='white')
	c.create_text(250, 250, text=f"Score: {score}", justify='center', font="Arial 30", fill='white')
	with open("record.txt", 'r') as high_score:
		if score > int(high_score.read()):
			c.create_text(250, 300, text=f"New record!", justify='center', font="Arial 30", fill='white')
			high_score = open("record.txt", 'w')
			high_score.write(str(score))

def create_apple(apple_type="apple", apple_color="red"):
	global s 
	snake_coords = []
	for body in s.snake:
		snake_coords.append((body.x, body.y))
	while True:
		rand_x, rand_y = rand(0, 450)//10*10, rand(0, 450)//10*10
		if (rand_x, rand_y) not in snake_coords:
			break
	c.create_oval((rand_x, rand_y), (rand_x+10, rand_y+10), tag = apple_type, fill = apple_color)
	if rand(0, 10) == 0 and apple_type == "apple" and not c.coords("gold_apple"):
		create_apple("gold_apple", 'yellow')
		c.after(5000, c.delete, "gold_apple")

binds = {('<Up>', 'W', 'w'): lambda e: s.change_dir('up'), ('<Down>', 'S', 's'): lambda e: s.change_dir('down'), ('<Right>', 'D', 'd'): lambda e: s.change_dir('right'), ('<Left>', 'A', 'a'): lambda e: s.change_dir('left')}
for bind1, bind2, bind3 in binds:
	win.bind(bind1, binds[bind1, bind2, bind3])
	win.bind(bind2, binds[bind1, bind2, bind3])
	win.bind(bind3, binds[bind1, bind2, bind3])

s = Snake()
s.move()
create_apple()

win.protocol("WM_DELETE_WINDOW", win.quit) # This line resolves the error associated with closing the game window with the 'x' button. In tkinter, there are often problems when a window with all its objects closes, but some parts of the code continue to interact with these non-existent objects, which leads to an error. In my case, if you close a window, all objects on it are deleted and because of this their destructors containing the code connected with Canvas are started. The quit() function prevents this and closes the window without errors.

win.mainloop()
