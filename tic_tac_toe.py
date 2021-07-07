from random import randint as rand
from turtle import Turtle, Screen
from time import sleep

# Це суперклас усіх кнопок. Він задає характеристики усім кнопкам, а функція __init__() дає змогу задавати ці характеристики під час створення нового об'єкта:
class Button:
	length = 100
	width  = 40
	x_cor  = 0
	y_cor  = 0
	text   = ""
	def __init__(self, x, y, l=100, w=40, t="Exit"):
		self.length = l
		self.width  = w
		self.x_cor  = x
		self.y_cor  = y
		self.text   = t

# Це підклас класу Button. Він має метод, який малює прямокутні кнопки, спираючись на їхні параметри:
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

# Це клас для створення кнопки виходу з гри. Вона прямокутна, тому наслідується від класу RectangleButton і має метод, що визначає, коли гравець натиснув на кнопку і закриває гру:
class ExitButton(RectangleButton):
	# Цей метод закриває гру лише тоді, коли гравець натискає у будь-якому місці, що знаходиться у середині між 4 кутами кнопки:
	def on_button_click(self, x, y):
		if (x > self.x_cor and y > self.y_cor) and (x < self.x_cor + self.length and y < self.y_cor + self.width):
			window.bye()

# Це клас для створення кнопки, що перезапускає гру. Вона кругла, тому НЕ наслідується від класу RectangleButton і має метод, що визначає, коли гравець натиснув на кнопку і перезапускає гру. І ще має метод, що малює кнопку:
class ResetButton(Button):
	diameter = 55
	# Цей метод малює круглу кнопку перезапуску у заданих координатах із заданим діаметром:
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

	# Це спеціальний метод, який перезапускає гру лише тоді, коли гравець натискає у будь-якому місці, що знаходиться між центром кнопки і її краєм. Він визначає квадрат відстані між центром кола і точкою, куди натиснув гравець, і якщо він менший за квадрат радіуса, то це означає, що гравець натиснув на кнопку(P.S. Мене геометрія і тут дістала...):
	def on_button_click(self, x, y):
		if (x-self.x_cor)**2 + (y-self.y_cor)**2 < (self.diameter/2)**2:
			window.clear()
			before_game()

class RelatedButtons:
	binding_num = 0
	is_main     = False
	def __init__(bn, mn):
		self.binding_num = bn
		self.is_main     = mn

class SettingsButton(RectangleButton, RelatedButtons):
	is_selected = False
	def on_button_click(self, x, y):
		if (x > self.x_cor and y > self.y_cor) and (x < self.x_cor + self.length and y < self.y_cor + self.width):
			self.is_selected = not self.is_selected
			if self.is_selected == False:
				self.paint_button()
			else:
				self.paint_button(color="gray")

# Ця функція створює інтерфейс для вибору ігрових налаштувань перед початком гри:
def before_game():
	global game_mode, window, p, exit_button, reset_button, first_entry, bot_shape
	gm = input("Type game mode: ")
	if gm == '0':
		game_mode = None
	if gm == '1':
		game_mode = False
		fentry = input("You want to have first entry?: ")
		if fentry == "yes":
			first_entry = True
			bot_shape   = True
		if fentry == "no":
			first_entry = False
			bot_shape   = False
	if gm == '2':
		game_mode = True
		fentry = input("You want to have first entry?: ")
		if fentry == "yes":
			first_entry = True
			bot_shape   = True
		if fentry == "no":
			first_entry = False
			bot_shape   = False

	# Стартові налаштування:
	# window.title("Tic Tac Toe")
	# window.setup(width=0.5)
	# window.bgcolor("white")
	# p.hideturtle()
	# p.pencolor("black")
	# p.pensize(3)
	# p.speed(0)

	# gm1_button = SettingsButton(100, 0, 125, 40, "VS Bot")
	# gm1_button.paint_button(size=25)

	# gm2_button = SettingsButton(-275, 0, 175, 40, "With friend")
	# gm2_button.paint_button(size=25)

	# window.onclick(gm1_button.on_button_click, add=True)
	# window.onclick(gm2_button.on_button_click, add=True)

	start_game()

# Ця функція запускає гру - створює ігрове поле та інтерфейс:
def start_game():
	global row_1, row_2, row_3, is_circle, game_end, entry_num, window, p
	# del exit_button, reset_button
	# Стартові налаштування:
	window.title("Tic Tac Toe")
	window.setup(width=0.5)
	window.bgcolor("white")
	p.hideturtle()
	p.pencolor("black")
	p.pensize(3)
	p.speed(0)
	# Це просто гора із goto(), яка малює поле для гри(можна було б використати пару циклів і forward(), але нащо):
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
	# Тут я просто скопіював декілька змінних, що є за межами функцій і класів у кінці програми, бо їхні значення треба скидати кожен раз, коли гра перезапускається(детально про те за що відповідає кожна змінна я написав у кінці коду):
	row_1 = [None, None, None]
	row_2 = [None, None, None]
	row_3 = [None, None, None]
	is_circle = False
	game_end  = False
	entry_num = 0

	# Створює об'єкт - кнопку виходу з гри:
	exit_button = ExitButton(-150, 350)
	# Створює об'єкт - кнопку перезапуску гри:
	reset_button = ResetButton(100, 370)

	# Малює кнопки:
	exit_button.paint_button()
	reset_button.paint_button()

	# Тут, якщо при грі з ботом гравець не захотів ходити першим, бот одразу зробить свій хід:
	if game_mode == False and first_entry == False:
		stupid_bot_AI(row_1 + row_2 + row_3)
		print(row_1, row_2, row_3, game_end)
	if game_mode == True  and first_entry == False:
		smart_bot_AI_1block(row_1 + row_2 + row_3)
		print(row_1, row_2, row_3, game_end)

	# Передає значення функії on_click(), яка визначає, на яку клітинку натиснув гравець:
	window.onclick(on_click, add=True)
	# Передає значення методу on_button_click() і добавляє нову прив'язку:
	window.onclick(exit_button.on_button_click, add=True)
	window.onclick(reset_button.on_button_click, add=True)

# Ця функція є штучним інтелектом "тупого" бота(тобто це бот, який ставить хрестик або нулик у будь-яку пусту клітинку):
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

# Ці дві функції є горами із конструкцій if: else: , тобто штучним інтелектом розумного бота(це бот, який думає куди ставити хрестик або нулик). Його штучний інтелект поділяється на 3 блоки: перші два блоки відповідають за атаку і забезпечення перемоги, а третій за захист і зниження імовірності програшу:
# Цей блок відаовідає за перші декілька ходів бота. Він ходить по схемі, яка зменшує імовірність програшу бота майже до нуля:
def smart_bot_AI_1block(game_area):
	global is_circle, entry_num
	is_circle = bot_shape
	# Я вирішив зробити цього бота достатньо, але не занадто розумним, щоб більша частина партій проти нього завершувалася нічією. Тому, якщо він ходить першим, то завжди ставить хрестик у центр або в будь-який кут ігрового поля, бо це найвигідніша позиція. В такому випадку грати проти цього бота набагато складніше і імовірність того, що переможе бот теж висока.
	if first_entry == False:
		if entry_num == 0:
			s_entry = rand(0, 1)
			# Тут бот ставить хрестик у центр ігрового поля:
			if s_entry == 0:
				filler(1, 1)
			else:
				# Тут бот ставить хрестик у будь-який з чотирьх кутів. 1 це верхній лівий кут, 2 це верхній правий і т.д.(про масштабування думати вже пізно... Ну головне щоб працювало):
				s_entry = rand(1, 4)
				if s_entry == 1:
					filler(0, 0)
				if s_entry == 2:
					filler(2, 0)
				if s_entry == 3:
					filler(0, 2)
				if s_entry == 4:
					filler(2, 2)
		if game_area[0] == False or game_area[2] == False or game_area[6] == False or game_area[8] == False:
			if game_area[1] == True or game_area[3] == True or game_area[5] == True or game_area[7] == True:
				if game_area[0] == False and game_area[3] == True:
					if entry_num == 1:
						filler(1, 1)
					if entry_num == 2:
						smart_bot_AI_2block()
						if game_end == False and game_area[2] == None:
							filler(2, 0)

			# Тут, якщо бот першим ходом поставив хрестик в один із 4 кутів і гравець також поставив нулик в один із 3 кутів, що лишились, то бот поставить хрестик у будь-який із 2 кутів, що лишилися, бо це найвигідніший хід:
			if game_area[0] == True or game_area[2] == True or game_area[6] == True or game_area[8] == True:
				if entry_num == 1:
					if game_area[4] == None:
						while True:
							s_entry = rand(1, 4)
							if s_entry == 1 and game_area[0] == None:
								filler(0, 0)
								break
							elif s_entry == 2 and game_area[2] == None:
								filler(2, 0)
								break
							elif s_entry == 3 and game_area[6] == None:
								filler(0, 2)
								break
							elif s_entry == 4 and game_area[8] == None:
								filler(2, 2)
								break
				if entry_num == 2:
					smart_bot_AI_2block()
					if game_end == False:
						while True:
							s_entry = rand(1, 4)
							if s_entry == 1 and game_area[0] == None:
								filler(0, 0)
								break
							elif s_entry == 2 and game_area[2] == None:
								filler(2, 0)
								break
							elif s_entry == 3 and game_area[6] == None:
								filler(0, 2)
								break
							elif s_entry == 4 and game_area[8] == None:
								filler(2, 2)
								break
				if entry_num == 3 and game_end == False:
					smart_bot_AI_2block()
			# Тут, якщо бот першим ходом поставив хрестик в один із 4 кутів, а гравець поставив нулик в центр ігрового поля, то бот поставить хрестик у кут, що знаходиться навпроти по діагоналі від того кута, що він уже поставив, бо це найвигідніший хід:
			if game_area[4] == True:
				if entry_num == 1:
					if game_area[4] == True:
						if game_area[0] == False:
							filler(2, 2)
						if game_area[2] == False:
							filler(0, 2)
						if game_area[6] == False:
							filler(2, 0)
						if game_area[8] == False:
							filler(0, 0)
				if entry_num == 2:
					if game_area[0] == True or game_area[2] == True or game_area[6] == True or game_area[8] == True:
						if game_end == False:
							while True:
								s_entry = rand(1, 4)
								if s_entry == 1 and game_area[0] == None:
									filler(0, 0)
									break
								elif s_entry == 2 and game_area[2] == None:
									filler(2, 0)
									break
								elif s_entry == 3 and game_area[6] == None:
									filler(0, 2)
									break
								elif s_entry == 4 and game_area[8] == None:
									filler(2, 2)
									break
				if entry_num == 3 and game_end == False:
					smart_bot_AI_2block()

	entry_num += 1

# Цей блок забезпечує перемогу бота. Він є чимось схожим на функцію game_win(), що є трохи далі у коді. Кожен раз, коли цей блок запускається, він знаходить 2 хрестики(або нулики, якщо бот ходить другим), що стоять на одній лінії, і перевіряє чи можна до них поставити 3 хрестик і забезпечити перемогу бота:
def smart_bot_AI_2block():
	global is_circle
	is_circle = bot_shape
	if game_end == False:
		for i in range(3):
			if (row_2[i]   == row_3[i] == is_circle) and row_1[i] == None:
				filler(i, 0)
			elif (row_1[i] == row_3[i] == is_circle) and row_2[i] == None:
				filler(i, 1)
			elif (row_1[i] == row_2[i] == is_circle) and row_3[i] == None:
				filler(i, 2)
			elif i == 2:
				if (row_1[1]   == row_1[2] == is_circle) and row_1[0] == None:
					filler(0, 0)
				elif (row_1[0] == row_1[2] == is_circle) and row_1[1] == None:
					filler(1, 0)
				elif (row_1[0] == row_1[1] == is_circle) and row_1[2] == None:
					filler(2, 0)

				elif (row_2[1] == row_2[2] == is_circle) and row_2[0] == None:
					filler(0, 1)
				elif (row_2[0] == row_2[2] == is_circle) and row_2[1] == None:
					filler(1, 1)
				elif (row_2[0] == row_2[1] == is_circle) and row_2[2] == None:
					filler(2, 1)

				elif (row_3[1] == row_3[2] == is_circle) and row_3[0] == None:
					filler(0, 2)
				elif (row_3[0] == row_3[2] == is_circle) and row_3[1] == None:
					filler(1, 2)
				elif (row_3[0] == row_3[1] == is_circle) and row_3[2] == None:
					filler(2, 2)
				else:
					if ((row_1[0] == row_3[2] == is_circle) or (row_1[2] == row_3[0] == is_circle)) and row_2[1] == None:
						filler(1, 1)
	game_win(row_1 + row_2 + row_3)

# Цей блок не дає гравцю виграти. Він є чимось схожим на другий блок. Кожен раз, коли цей блок запускається, він знаходить 2 нулики(або хрестики, якщо гравець ходить першим), що стоять на одній лінії, і якщо у цій лінії є пуста клітинка(туди може сходити гравець), він ставить туди хрестик, щоб перекрити її:
def smart_bot_AI_3block():
	global is_circle
	is_circle = bot_shape
	if game_end == False:
		# for i in range(3):
		# 	if (row_2[i]   == row_3[i] != is_circle) and row_1[i] == None:
		# 		filler(i, 0)
		# 	elif (row_1[i] == row_3[i] != is_circle) and row_2[i] == None:
		# 		filler(i, 1)
		# 	elif (row_1[i] == row_2[i] != is_circle) and row_3[i] == None:
		# 		filler(i, 2)
		# 	elif i == 2:
		# 		if (row_1[1]   == row_1[2] != is_circle) and row_1[0] == None:
		# 			filler(0, 0)
		# 		elif (row_1[0] == row_1[2] != is_circle) and row_1[1] == None:
		# 			filler(1, 0)
		# 		elif (row_1[0] == row_1[1] != is_circle) and row_1[2] == None:
		# 			filler(2, 0)

		# 		elif (row_2[1] == row_2[2] != is_circle) and row_2[0] == None:
		# 			filler(0, 1)
		# 		elif (row_2[0] == row_2[2] != is_circle) and row_2[1] == None:
		# 			filler(1, 1)
		# 		elif (row_2[0] == row_2[1] != is_circle) and row_2[2] == None:
		# 			filler(2, 1)

		# 		elif (row_3[1] == row_3[2] != is_circle) and row_3[0] == None:
		# 			filler(0, 2)
		# 		elif (row_3[0] == row_3[2] != is_circle) and row_3[1] == None:
		# 			filler(1, 2)
		# 		elif (row_3[0] == row_3[1] != is_circle) and row_3[2] == None:
		# 			filler(2, 2)
		# 		else:
		# 			if ((row_1[0] == row_3[2] != is_circle) or (row_1[2] == row_3[0] != is_circle)) and row_2[1] == None:
		# 				filler(1, 1)
		combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
		for line in combinations:
			if game_area[line[0]] == game_area[line[1]] == game_area[line[2]] == is_circle:
				game_end = True
	game_win(row_1 + row_2 + row_3)

# Функція, що малює хрестики або нулики у потрібному місці:
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

# Ця функція малює риску вздовж 3 фігур у потрібному місці:
def paint_line(p1, p2):
	p.pencolor("black")
	p.pensize(25)
	p.penup()
	p.goto(p1)
	p.pendown()
	p.goto(p2)
	p.penup()
	sleep(1)

#Ця функція визначає перемогу у грі і малює риску вздовж 3 фігур, що стали в одну лінію.(Я не сильно парився з алгоритмами і просто записав більшість комбінацій в if: (elif): else: . Можна якось покращити код так, щоб усе працювало навіть на ігровому полі розміром більше 3x3, але нащо тратити на це час):
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
	# Тут функція оголошує нічию (нічия відбувається тоді, коли усі клітинки вже заповнені, а 3 фігури так і не стали в ряд. Гру завершено. Переможців немає).
	if None not in game_area and game_end == False:
		game_end = True
		end_game("Draw")

# Ця функція оголошує переможця і створює інтерфейс після завершення гри:
def end_game(winner):
	if winner == "Draw":
		print("Нічия!")
		sleep(1)
		window.bye()
	else:
		if game_mode == None:
			if winner == "Circles":
				print("Нулики перемогли!")
			if winner == "Criss-crosses":
				print("Хрестики перемогли!")
			window.bye()
		if game_mode == False or game_mode == True:
			if bot_shape == is_circle:
				print("Бот переміг!")
			else:
				print("Ти переміг!")
			window.bye()

# Це допоміжна функція. Вона заповнює вміст кожної клітинки
def filler(column, row):
	tic_tac_toe(x_coords[column], y_coords[row])
	if row == 0:
		row_1[column] = is_circle
	if row == 1:
		row_2[column] = is_circle
	if row == 2:
		row_3[column] = is_circle

# Ця функція разом з window.onclick() зчитує, на яку клітинку натискає гравець і задає цій клітинці значення(може тут можна щось спростити, але я поки не придумав як, тому хай буде такий код. Головне щоб працювало):
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
	none_on_click = False # Це допоміжна змінна, яка потрібна для того, щоб бот робив свій хід тільки після того, коли гравець натиснув на пусту клітинку і заповнив її.
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
		print(row_1, row_2, row_3, game_end)

	# Тут якщо установлено режим гри з другом, то кожен раз, коли один з гравців натискає на клітинку значення is_circle змінюється на протилежне(тобто хрестик міняється на нулик або навпаки):
	if game_mode == None and none_on_click == True:
		if (x > -300 and y < 300) and (x < 300 and y >-300):
			is_circle = not is_circle
	# Тут якщо установлено режим гри проти бота, то кожен раз, коли гравець робить свій хід, запускається бот, який одразу робить свій хід:
	if game_mode == False and none_on_click == True and game_end == False:
		stupid_bot_AI(row_1 + row_2 + row_3)
		game_win(row_1 + row_2 + row_3)
		print(row_1, row_2, row_3, game_end)
	if game_mode == True  and none_on_click == True and game_end == False:
		smart_bot_AI_1block(row_1 + row_2 + row_3)
		# game_win()
		print(row_1, row_2, row_3, game_end)

# Створює об'єкт - вікно і черепаха:
window = Screen()
p = Turtle()

# Це параметри ігрового поля:
# Ці списки зберігають вміст кожної клітинки. None - це пуста клітинка, True - це клітинка з хрестиком, а False - це клітинка з кружечком.
# Нульовий індекс це ліва клітинка кожного рядка(зробив так, бо, на жаль, в Python, якщо створити масив, створений із масивів, то значення кожному елементу масиву, що є у цьому масиві, не можна одразу задати за допомогою подвійного індексу(row[i,j]) як в інших мовах програмування і треба робити лишні маніпуляції в коді).
row_1       = [None, None, None]
row_2       = [None, None, None]
row_3       = [None, None, None]
x_coords    = [-200,    0,  200] # усі можливі X-кординати клітинки.(координата кожної клітинка це точка в її центрі)
y_coords    = [ 200,    0, -200] # усі можливі Y-кординати клітинки.
combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]] # Тут зберігаються усі комбінації, при яких 3 фігури стають в одну лінію.
is_circle   = True  # Вказує функції, що потрібно малювати і вставляти у список. Якщо значення False, то функція малює хрестик, а якщо значення True - кружечок.
game_mode   = None  # Ця змінна вказує функції режим гри. Якщо значення None, то це режим гри з другом, якщо значення False, то це режим гри проти "тупого" бота, а якщо значення True, то це режим гри проти "розумного" бота.
game_end    = False # Ця змінна вказує боту, що три фігури уже стали в ряд і гру завершено, щоб він не намагався ходити далі.
first_entry = False # Ця змінна вказує хто ходить першим при грі з ботом. Якщо значення True, то першим ходить гравець, а якщо значення False, то - бот.
bot_shape   = True  # Це допоміжна змінна, яка вказує якою фігурою ходить гравець і бот. Оскільки хрестики завжди ходять першими, то якщо гравець вибрав ходити першим, то він буде ходити хрестиками, а бот буде ходити нуликами і навпаки(прийшлося зробити таку змінну, бо було багато багів з тим, що бот ходив то хрестиком то нуликом, а мав ходити однією і тією ж фігурою. Напевно через те що я з самого початку неправильно це реалізував. Але ця змінна виправляє такі баги)
entry_num   = 0     # Ця змінна вказує розумному боту скільки він уже зробив ходів

before_game()

# Цей метод потрібен для того, щоб ігрове вікно не закривалось одразу після запуску:
window.mainloop()