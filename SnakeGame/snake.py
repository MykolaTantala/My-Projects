"""Snake game relize version 1.7

Ну я написав змійку. Цього разу я майже не писав коментарів. Думаю цього докстрінгу вистачить.
Насправді код достатньо простий і займає лише 98 рядків, не враховуючи модуль interface.py.
Хоча релізній версії далеко до тої чистоти коду, яка була при першій робочій версії.
Тоді код займав лише 70 рядків. Ну але як завжди маленькі майже незамітні доповнення займають більше коду ніж основна логіка програми.
Хоча я зробив не усе, що задумував, інакше було б ще більше рядків коду.

Щодо того як тут усе влаштовано, то я використав ООП. Ну насправді можна було обійтися без нього і код був би коротший,
але ООП - це сила, тому хай буде. Є три класи: Голова змії, тіло змії і сама змія.
Ще був клас, який відповідав за створення яблочок на ігровому полі, але потім я замінив його на функцію create_apple().

Сама змія програмно представляє із себе список, перший елемент якого є головою, а усе інше хвостом. Ну тут все зрозуміло.
На рахунок того як рухається змія, то я не використовував метод Canvas.move(), щоб переміщати змію по ігровому полю.
Замість цього я зробив усе по принципу, який придумали наші діди на початку кайнозойської ери, коли програмували першу Nokia.
Хвіст видаляється - голова прибавляється. В результаті з'являється ілюзія того, що змійка рухається.
Написати таку логіку було дуже просто, бо я колись вже робив гру змійка ще на Scratch.

Змійка змінює напрям свого руху з допомогою методу change_dir(). І тут я мушу звернути увагу на існування БАГУ.
Він існує через те, що розробники tkinter'а не продумали цей момент і tkinter не має простого рішення цій проблемі.
Якщо коротко, то якщо, наприклад, змійка рухається вверх і в правильний момент в інтервалі часу між викликом методу after() і викликом методу move(),
одночасно або з дуже маленьким проміжком часу натиснути на клавіші стрілка вниз і стрілка вправо, то змійка розвернеться і поповзе сама у себе. 
В такому випадку вона укусить сама себе, що призводить до програшу. Якби можна було заблокувати можливість одночасно двом клавішам запускати функції, то такого багу б не було.
Я все таки написав рішення для цього багу, але воно мені не сподобалося, бо через нього змійкою ставало важче керувати.
Може той код можна, якось удосконалити, щоб він не сковував рух змійки, але я поки що вросто вирізав його і залишив цей баг.

P.S Про усе, що є в цій грі я написав у README.txt"""

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
		directions = {'up'   :((self.x+2, self.y+2), (self.x+7, self.y+2)),                           # Ось це все просто малює квадратну голову з двома однопіксельними очима.
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
		displacement = {'up'   :(  0,-10), # У цьому словнику зберігаються усі зміщення голови змії при русі у певну сторону. Вони додаються до колишніх координат голови змійки і так вона переміщується.
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

win.protocol("WM_DELETE_WINDOW", win.quit) # Цей рядок вирішує помилку зв'язану із закриттям ігрового вікна кнопкою 'x'. В tkinter'і часто бувають такі проблеми, коли вікно разом з усіма його об'єктами закривається, але деякі частини коду продовжують взаємодіяти з цими уже не існуючими об'єктами, що призводить до помилки. У моєму випадку, якщо закрити вікно, то усі об'єкти на ньому видаляються і через це запускаються їхні деструктори, що містять код пов'язаний з Canvas. Функція quit() запобігає цьому і закриває вікно без помилок.

win.mainloop()