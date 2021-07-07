import tkinter as tk
from calc import *

# Налаштування вікна:
window = tk.Tk()
screen = tk.Text(window, font=('Consolas', 20), bd=3, bg='black', fg='white', width = 23, height=2, wrap='none')
window.geometry("353x472+500+225")
window.resizable(False, False)
# ФЛОППА
floppa = tk.PhotoImage(file="smart_floppa.png")
window.title("Floppa Calculator")
window.iconphoto(False, floppa)

# Ця функція оновлює екран калькулятора:
def update_screen(input, output=None):
	# Тут на екран добавляється символ, який ввів користувач:
	screen['state'] = 'normal'
	screen.delete(1.0, 'end')
	screen.insert(1.0, str(input))
	screen.tag_add('title', 1.0, '1.end')
	screen.tag_config('title', justify='right')
	# Тут на екран виводиться відповідь:
	if output != None:
		if len(str(output)) > 17:
			output = '%.7e' % Round(float(output))
		screen.delete(2.0, 'end')
		screen.insert(2.0, '\n'+str(output).replace('.', ','))
		screen.tag_add('title', 2.0, '2.end')
		screen.tag_config('title', justify='right')
	screen['state'] = 'disabled'
	# Це просто купа з if: (elif:) else'ів, яка виправляє баги:
	screen_text = screen.get(1.0, 'end').replace('\n', '')
	# Тут блокується або розблоковується можливість ввести кому, щоб користувач не міг ввести декілька ком, записуючи дробне число(без цієї частини коду може статися баг, наприклад користувач може ввести щось типу '5,05,123,1', що призводить до помилки всередині eval()):
	if len(screen_text) > 1:
		if screen_text[-1] == ',':
			buttons[13]['state'] = 'disabled'
			window.bind(',', lambda e: None)
		elif screen_text[-2] in "+-*/%^" and '0' <= screen_text[-1] <= '9':
			buttons[13]['state'] = 'normal'
			window.bind(',', lambda e: add_op(','))
	elif input == 0 and len(screen_text) == 1:
		buttons[13]['state'] = 'normal'
		window.bind(',', lambda e: add_op(','))
	if screen_text[-1] == 'π':
		buttons[13]['state'] = 'disabled'
		window.bind(',', lambda e: None)
	# Тут блокується або розблоковується можливість натиснути кнопку '='.(Є такий баг, що стається, коли останнім символом на екрані калькулятора є знак математичної операції і користувач натискає на кнопку '='. Це також призводить до помилки в середині eval(). Ну і ще я добавив перевірку на те чи користувач ввів лише одне число без будь-яких операцій. Кнопка '=' і відповідна клавіша клавіатури буде заблокована поки користувач не введе хоча б одну повноцінну математичну операцію):
	if screen_text[-1] in "+-*/%^," or screen_text.replace(',', '').isdigit():
		buttons[22]['state'] = 'disabled'
		window.bind('<Return>', lambda e: None)
		window.bind('<space>' , lambda e: None)
		window.bind('='		 , lambda e: None)
	else:
		buttons[22]['state'] = 'normal'
		window.bind('<Return>', calculate)
		window.bind('<space>' , calculate)
		window.bind('='       , calculate)

# Ця функція добавляє число, на яке натиснув користувач, на екран калькулятора:
def add_num(num):
	screen_text = screen.get(1.0, 'end').replace('\n', '')
	if screen_text == '0':
		if num == 0:
			return False
		else:
			screen_text = screen_text[:-1]
	else:
		if 3 > len(screen_text) > 1 and screen_text[0] == '0' and screen_text[1] in "+-*/%^,":
			pass
		elif screen_text[-1] == '0' and screen_text[-2] in "+-*/%^":
			screen_text = screen_text[:-1]
	if num == 'π' and screen_text[-1] not in "+-*/%^":
		return False
	screen_text = screen_text + str(num)
	update_screen(screen_text)

# Ця функція добавляє або заміняє на екрані просту математичну операцію, яку ввів користувач, а також добавляє кому до чисел:
def add_op(operation):
	screen_text = screen.get(1.0, 'end').replace('\n', '')
	if screen_text[-1] in "+-*/^,":
		screen_text = screen_text[:-1]
	screen_text += operation
	update_screen(screen_text)

# Ця функція добавляє на екран складну математичну операцію, яку ввів користувач:
def add_spec(operation):
	pass

# Ця функція блокує або розблоковує кнопки індекси, яких їй передаються:
def block_btn(*btns, block=True):
	for i in btns:
		if block == True:
			buttons[i]['state'] = 'disabled'
		else:
			buttons[i]['state'] =  'normal'

# Ця функція вираховує відповідь до того, що ввів користувач і виводить її на екран:
def calculate(event=None):
	exercise = screen.get(1.0, 'end').replace('\n', '').replace(',', '.').replace('^', '**').replace('π', 'math.pi')
	try:
		update_screen(screen.get(1.0, 'end'), str(Round(eval(exercise))))
	# Лише дуже розумні калькулятори можуть пізнати нескінченність:
	except ZeroDivisionError:
		update_screen(screen.get(1.0, 'end'), '∞')
	# В python під час вираження дуже великих або дуже малих чисел з допомогою експонента, він не може бути більшим за 300, інакше буде ця помилка, тому цей калькулятор не може вираховувати дуже великі числа як калькулятор Windows'а:
	except OverflowError:
		update_screen(screen.get(1.0, 'end'), 'Overflow!')
	# А це просто на всякий випадок:
	except Exception:
		update_screen(screen.get(1.0, 'end'), 'Error')
	block_btn(*range(3, 14), *range(15, 19), 22, 26) # тут я блокую кнопки, щоб користувач не міг нічого ввести(бо станеться баг) і єдине, що він може зробити це очистити екран(це тимчасове вирішення проблеми, потім я зміню його на інше).

# Ця функція очищає екран:
def clear_screen(event=None):
	# if buttons[3]['state'] == 'disabled':
	block_btn(*range(3, 14), *range(15, 19), 22, 26, block=False) # тут я навпаки розблоковую кнопки, бо користувач уже очистив екран.
	screen.delete(1.0, 'end')
	screen.delete(2.0, 'end')
	update_screen(0)

# Ця функція видаляє останнє значення, що ввів користувач:
def clear_entry():
	pass

# Ця функція видаляє останній символ, що ввів користувач:
def clear_last():
	pass

# просто функція потрібна для того, щоб ще не прописані кнопки не икликали помилку:
def update():
	pass

buttons = [] # список, де зберігаються усі кнопки.
btn_num = 0  # допоміжна змінна, що використовується у функції make_btn().
# Функція, яка створює кнопку із заданими параметрами, а також задає прив'язку до клавіш клавіатури. Усім необов'язковим аргументам задано значення None. Усі обов'язкові аргумети зберігаються в kw:
def make_btn(**kw):
	global btn_num
	buttons.append(tk.Button(window, text=kw['t'], font=kw['f'], bg=kw['bg'], fg=kw['fg'], command=kw['cmd'], width=kw['w'], activebackground=kw['abg'], activeforeground=kw['afg']))
	buttons[btn_num].grid(row=kw['r'], column=kw['c'], stick='wens', ipady=5, rowspan=kw['rs'], columnspan=kw['cs'])
	btn_num+=1

# Насправді я з самого початку створив цикл майже такий самий як у вас. 
# У мене не вийшло задавати параметр 'command' лише через те, що я не знав як правильно задати значення параметру lambda функції.
#
# Менше кажучи ось це моя lambda:
#        command = lambda: function(i) # прив'язує змінну 'i', в якій є значення, яке в ній зберегли під час останньої ітерації, тому усі кнопки мали прив'язку до однієї і тієї ж функції з одним і тим же параметром і при натисканні записували на екран один і той же символ.
# А це ваша:
#        command = lambda num = i: function(num) # тут до кнопок прив'язуються функції з різними параметрами і всі кнопки записують на екран різні символи.
#
# Якби я одразу знав як це реалізувати, то з самого пачатку написав би невеликий цикл, а не 28 схожих рядків коду.
# Інтерфейс вашого калькулятора дуже простий. Усі кнопки однакові і не мають ніяких параметрів крім тексту і команди, тому їх можна легко створити у циклі.
# Інтерфейс мого калькулятора набагато складніший. Усі кнопки мають різний колір, розмір тексту, деякі розтягуються по рядках, деякі по стовбцях, у деяких є товстий текст,
# а також вони мають параметри, які не дають їм наповзати одна на одну і кнопки в певних групах мають мати однакові розміри і т.д.
# Помістити усе це в цикл, дуже складно, хоча у мене вийшло. Але, щоб усе це помістити в цикл, потрібно записати в ньому декілька доволі складних конструкцій if: (elif:) else:
# або ж створити декілька циклів. Цей код був ще десь на 20% довший ніж той, що був перед цим.
# Я вже подумав, що не варіант створювати кнопки у циклі, але потім придумав як це зробити, не використовуючи конструкції if: (elif:) else: .
# Я створив словник із словників, у якому ключі є текстом кнопки, а значення є словниками, в яких зберігаються параметри усіх кнопок.
# Хоча він має довжину майже 4000 символів... Ну зате займає лише один рядок коду. Плюс цикл займав лише 2 рядки коду. Значить я скоротив 28 рядків коду до 3 рядків.
# Ну і аналогічно я скоротив код, який добавляв прив'язку до клавіш клавіатури. Це було ще мінус 19 рядків коду.
# Далі я подумав, що можна якось об'єднати ті 2 цикли, що я написав в 1 цикл. Ну і я це зробив з допомогою функції zip().
# В кінцевому результаті вийшло скоротити 51 рядок коду до 5 рядків.

# Ця функція створює весь інтерфейс програми:
def make_interface():
	# Ви запускаєте усе на MacOS, тому у вас калькулятор виглядає абсолютно не так як на Windows(я добавив у .zip архів зображення того, як він виглядає на Windows).
	# Кнопки мали не такий колір фону і колір тексту, який я прописав, тому майже неможливо було відрізнити заблоковані кнопки від робочих
	# і калькулятором неможливо було нормально користуватися, не знаю чи це допоможе, але я замінив усі Hex-кольори на прості слова типу 'orange' і 'blue'.
	# Чисто теоретично вони у вас неправильно відображаються і може це допоможе. І ще я зробив чорний фон. Може це теж щось змінить.
	# Tkinter розміщає на вікні кнопки і інші частини інтерфейсу, які є прописаними в операційній системі. Як на мене це мінус, бо на tkinter'і неможливо написати програму,
	# яка буде мати повністю однаковий інтерфейс на усіх ОС і треба усе прописувати окремо під кожну ОС.

	# Це словник із словників, в якому зберігаються параметри усіх кнопок:
	buttons = {'C' : {'cmd': lambda: clear_screen(),  'f':('Arial' ,20), 'bg':'#FF8500', 'fg':'white', 'abg':'#0095FF', 'afg':'white', 'r':1, 'c':2, 'w':None, 'rs':None, 'cs':None},
				  'CE': {'cmd': lambda: clear_entry(),   'f':('Arial' ,20), 'bg':'#FF8500', 'fg':'white', 'abg':'#0095FF', 'afg':'white', 'r':1, 'c':1, 'w':None, 'rs':None, 'cs':None},
				  '←' : {'cmd': lambda: clear_last(),    'f':('Impact',20 , 'bold'), 'bg':'#FF8500', 'fg':'white', 'abg':'#0095FF', 'afg':'white', 'r':1, 'c':0, 'w':None, 'rs':None, 'cs':None},

				  '1' : {'cmd': lambda: add_num(1)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':2, 'c':0, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '2' : {'cmd': lambda: add_num(2)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':2, 'c':1, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '3' : {'cmd': lambda: add_num(3)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':2, 'c':2, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '4' : {'cmd': lambda: add_num(4)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':3, 'c':0, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '5' : {'cmd': lambda: add_num(5)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':3, 'c':1, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '6' : {'cmd': lambda: add_num(6)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':3, 'c':2, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '7' : {'cmd': lambda: add_num(7)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':4, 'c':0, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '8' : {'cmd': lambda: add_num(8)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':4, 'c':1, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '9' : {'cmd': lambda: add_num(9)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':4, 'c':2, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '0' : {'cmd': lambda: add_num(0)  ,    'f':('Arial' ,20), 'bg':'black', 'fg':'white', 'w':3, 'r':5, 'c':0, 'abg':None, 'afg':None, 'rs':None, 'cs':2   },

				  ',' : {'cmd': lambda: add_op(',') ,    'f':('Arial' ,20 , 'bold'), 'bg':'black', 'fg':'white','r':5, 'c':2, 'w':3, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '±' : {'cmd': lambda: update()    ,    'f':('Arial' ,20), 'bg':'gray' , 'fg':'white', 'r':1, 'c':3, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '/' : {'cmd': lambda: add_op('/') ,    'f':('Arial' ,20), 'bg':'gray' , 'fg':'white', 'r':2, 'c':3, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '*' : {'cmd': lambda: add_op('*') ,    'f':('Arial' ,20), 'bg':'gray' , 'fg':'white', 'r':3, 'c':3, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '+' : {'cmd': lambda: add_op('+') ,    'f':('Arial' ,20), 'bg':'gray' , 'fg':'white', 'r':4, 'c':3, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '-' : {'cmd': lambda: add_op('-') ,    'f':('Arial' ,20), 'bg':'gray' , 'fg':'white', 'r':5, 'c':3, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},

				 'ⁿ√x': {'cmd': lambda: update()    ,    'f':('Arial' ,17), 'bg':'gray' , 'fg':'white', 'r':1, 'c':4, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '%' : {'cmd': lambda: add_op('%') ,    'f':('Arial' ,20), 'bg':'gray' , 'fg':'white', 'r':2, 'c':4, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				 '1/x': {'cmd': lambda: update()    ,    'f':('Arial' ,17), 'bg':'gray' , 'fg':'white', 'r':3, 'c':4, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  '=' : {'cmd': lambda: calculate() ,    'f':('Arial' ,25 , 'bold'), 'bg':'#FF8500' , 'fg':'white', 'r':4, 'c':4, 'w':None, 'abg':'#0095FF', 'afg':'white', 'rs':2, 'cs':None},

				  '(' : {'cmd': lambda: update()    ,    'f':('Consolas', 20), 'bg':'gray', 'fg':'white', 'r':7, 'c':0, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  ')' : {'cmd': lambda: update()    ,    'f':('Consolas', 20), 'bg':'gray', 'fg':'white', 'r':7, 'c':1, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  'n!': {'cmd': lambda: update()    ,    'f':('Arial'   , 20), 'bg':'gray', 'fg':'white', 'r':7, 'c':2, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  'xⁿ': {'cmd': lambda: add_op('^') ,    'f':('Consolas', 20), 'bg':'gray', 'fg':'white', 'r':7, 'c':3, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None},
				  'π' : {'cmd': lambda: add_num('π'),    'f':('Consolas', 20), 'bg':'gray', 'fg':'white', 'r':7, 'c':4, 'w':None, 'abg':None, 'afg':None, 'rs':None, 'cs':None}}

	# Це словник, в якому зберігаються усі прив'язки до клавіш клавіатури(ключі - це под):
	binds = {'1': lambda e: add_num(1),
				'2': lambda e: add_num(2),
				'3': lambda e: add_num(3),
				'4': lambda e: add_num(4),
				'5': lambda e: add_num(5),
				'6': lambda e: add_num(6),
				'7': lambda e: add_num(7),
				'8': lambda e: add_num(8),
				'9': lambda e: add_num(9),
				'0': lambda e: add_num(0),
				'π': lambda e: add_num('π'),
				',': lambda e: add_op(','),
				'/': lambda e: add_op('/'),
				'*': lambda e: add_op('*'),
				'+': lambda e: add_op('+'),
				'-': lambda e: add_op('-'),
				'^': lambda e: add_op('^'),
				'<Control-L>': clear_screen,
				'<Control-l>': clear_screen,
				'C'			 : clear_screen,
				'<Return>'	 : calculate,
				'<space>'	 : calculate,
				'='			 : calculate,
				'a':lambda e:None,
				'b':lambda e:None,
				'c':lambda e:None,
				'd':lambda e:None,
				'e':lambda e:None}
	
	# Цей цикл створює усі кнопки і прив'язки до клавіш клавіатури:
	for btn, bnd in zip(buttons, binds):
		make_btn(cmd = buttons[btn]['cmd'], t=btn , f=buttons[btn]['f'], bg=buttons[btn]['bg'], fg=buttons[btn]['fg'], abg=buttons[btn]['abg'], afg=buttons[btn]['afg'], r=buttons[btn]['r'], c=buttons[btn]['c'], w=buttons[btn]['w'], rs=buttons[btn]['rs'], cs=buttons[btn]['cs'])
		window.bind(bnd, binds[bnd])

	# Розміщає на вікні екран калькулятора:
	screen.grid(row=0, column=0, columnspan=5)
	update_screen(0)

	# Тут я поки що відключив кнопки, роботу яких ще не прописав:
	block_btn(1, 2, 14, 19, 20, 21, 24, 23, 25)

make_interface()

window.mainloop()