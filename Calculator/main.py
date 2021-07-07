import tkinter as tk
from calc import *

# Window settings:
window = tk.Tk()
screen = tk.Text(window, font=('Consolas', 20), bd=3, bg='black', fg='white', width = 23, height=2, wrap='none')
window.geometry("353x472+500+225")
window.resizable(False, False)
# FLOPPA
floppa = tk.PhotoImage(file="smart_floppa.png")
window.title("Floppa Calculator")
window.iconphoto(False, floppa)

# This function updates the calculator screen:
def update_screen(input, output=None):
	# Here the character entered by the user is added to the screen:
	screen['state'] = 'normal'
	screen.delete(1.0, 'end')
	screen.insert(1.0, str(input))
	screen.tag_add('title', 1.0, '1.end')
	screen.tag_config('title', justify='right')
	# Here the answer is displayed on the screen:
	if output != None:
		if len(str(output)) > 17:
			output = '%.7e' % Round(float(output))
		screen.delete(2.0, 'end')
		screen.insert(2.0, '\n'+str(output).replace('.', ','))
		screen.tag_add('title', 2.0, '2.end')
		screen.tag_config('title', justify='right')
	screen['state'] = 'disabled'
	# It's just a bunch of if: (elif:) else's that fixes bugs:
	screen_text = screen.get(1.0, 'end').replace('\n', '')
	# This blocks or unlocks the ability to enter a comma so that the user cannot enter multiple commas by writing a fractional number (without this part of the code a bug can occur, for example the user can enter something like '5,05,123,1', which leads to an error inside eval()):
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
	# This blocks or unlocks the ability to press the '=' button.(There is a bug that occurs when the last symbol on the calculator screen is a mathematical operation sign and the user presses the '=' button. This leads to an error inside eval(). Well, I also added a check to see if the user entered only one number without any operations. The '=' button and the corresponding key on the keyboard will be locked until the user enters at least one full mathematical operation):
	if screen_text[-1] in "+-*/%^," or screen_text.replace(',', '').isdigit():
		buttons[22]['state'] = 'disabled'
		window.bind('<Return>', lambda e: None)
		window.bind('<space>' , lambda e: None)
		window.bind('='	      , lambda e: None)
	else:
		buttons[22]['state'] = 'normal'
		window.bind('<Return>', calculate)
		window.bind('<space>' , calculate)
		window.bind('='       , calculate)

# This function adds the number the user clicked on to the calculator screen:
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

# This function adds or replaces a simple mathematical operation entered by the user on the screen, and also adds a comma to the numbers:
def add_op(operation):
	screen_text = screen.get(1.0, 'end').replace('\n', '')
	if screen_text[-1] in "+-*/^,":
		screen_text = screen_text[:-1]
	screen_text += operation
	update_screen(screen_text)

# NOT CODED YET
def add_spec(operation):
	pass

# This function locks or unlocks the buttons whose indexes are passed to it:
def block_btn(*btns, block=True):
	for i in btns:
		if block == True:
			buttons[i]['state'] = 'disabled'
		else:
			buttons[i]['state'] =  'normal'

# This function calculates the response to what the user has entered and displays it on the screen:
def calculate(event=None):
	exercise = screen.get(1.0, 'end').replace('\n', '').replace(',', '.').replace('^', '**').replace('π', 'math.pi')
	try:
		update_screen(screen.get(1.0, 'end'), str(Round(eval(exercise))))
	# Only very smart calculators can knew infinity:
	except ZeroDivisionError:
		update_screen(screen.get(1.0, 'end'), '∞')
	# In python when expressing very large or very small numbers using an exponent, it cannot be greater than ~300, otherwise there will be this error:
	except OverflowError:
		update_screen(screen.get(1.0, 'end'), 'Overflow!')
	# And it's just in case:
	except Exception:
		update_screen(screen.get(1.0, 'end'), 'Error')
	block_btn(*range(3, 14), *range(15, 19), 22, 26) # here I lock the buttons so that the user can't enter anything (because there will be a bug) and the only thing he can do is clear the screen (this is a temporary solution to the problem, then I'll change it to another).

# This function clears the screen:
def clear_screen(event=None):
	block_btn(*range(3, 14), *range(15, 19), 22, 26, block=False) # here I on the contrary unlock buttons because the user has already cleared the screen.
	screen.delete(1.0, 'end')
	screen.delete(2.0, 'end')
	update_screen(0)

# NOT CODED YET
def clear_entry():
	pass

# NOT CODED YET
def clear_last():
	pass

# just a function is needed so that not yet coded buttons do not cause an error:
def update():
	pass

buttons = [] # list where all buttons are contained.
btn_num = 0  # helper  variable used in the make_btn() function.
# A function that creates a button with specified parameters:
def make_btn(**kw):
	global btn_num
	buttons.append(tk.Button(window, text=kw['t'], font=kw['f'], bg=kw['bg'], fg=kw['fg'], command=kw['cmd'], width=kw['w'], activebackground=kw['abg'], activeforeground=kw['afg']))
	buttons[btn_num].grid(row=kw['r'], column=kw['c'], stick='wens', ipady=5, rowspan=kw['rs'], columnspan=kw['cs'])
	btn_num+=1

# This function creates the entire program interface:
def make_interface():
	# This is a dictionary of dictionaries, which contains the parameters of all buttons:
	buttons = {'C':{'cmd':lambda:clear_screen(),'f':('Arial',20),'bg':'#FF8500','fg':'white','abg':'#0095FF','afg':'white','r':1,'c':2,'w':None,'rs':None,'cs':None},'CE':{'cmd':lambda:clear_entry(),'f':('Arial' ,20), 'bg':'#FF8500', 'fg':'white', 'abg':'#0095FF', 'afg':'white', 'r':1, 'c':1, 'w':None, 'rs':None, 'cs':None},'←':{'cmd':lambda:clear_last(),'f':('Impact',20 , 'bold'), 'bg':'#FF8500', 'fg':'white', 'abg':'#0095FF', 'afg':'white', 'r':1, 'c':0, 'w':None, 'rs':None, 'cs':None},'1':{'cmd':lambda:add_num(1),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':2,'c':0,'abg':None,'afg':None,'rs':None,'cs':None},'2':{'cmd':lambda:add_num(2),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':2,'c':1,'abg':None,'afg':None,'rs':None,'cs':None},'3':{'cmd':lambda:add_num(3),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':2,'c':2,'abg':None,'afg':None,'rs':None,'cs':None},'4':{'cmd':lambda:add_num(4),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':3,'c':0,'abg':None,'afg':None,'rs':None,'cs':None},'5':{'cmd':lambda:add_num(5),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':3,'c':1,'abg':None,'afg':None,'rs':None,'cs':None},'6':{'cmd':lambda:add_num(6),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':3,'c':2,'abg':None,'afg':None,'rs':None,'cs':None},'7':{'cmd':lambda:add_num(7),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':4,'c':0,'abg':None,'afg':None,'rs':None,'cs':None},'8':{'cmd':lambda:add_num(8),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':4,'c':1,'abg':None,'afg':None,'rs':None,'cs':None},'9':{'cmd':lambda:add_num(9),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':4,'c':2,'abg':None,'afg':None,'rs':None,'cs':None},'0':{'cmd':lambda:add_num(0),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':5,'c':0,'abg':None,'afg':None,'rs':None,'cs':2},',':{'cmd':lambda:add_op(','),'f':('Arial',20,'bold'),'bg':'black','fg':'white','r':5,'c':2,'w':3,'abg':None,'afg':None,'rs':None,'cs':None},'±':{'cmd':lambda:update(),'f':('Arial',20),'bg':'gray','fg':'white','r':1,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'/':{'cmd':lambda:add_op('/'),'f':('Arial',20),'bg':'gray','fg':'white','r':2,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'*':{'cmd':lambda:add_op('*'),'f':('Arial',20),'bg':'gray','fg':'white','r':3,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'+':{'cmd':lambda:add_op('+'),'f':('Arial',20),'bg':'gray','fg':'white','r':4,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'-':{'cmd':lambda:add_op('-'),'f':('Arial',20),'bg':'gray','fg':'white','r':5,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'ⁿ√x':{'cmd':lambda:update(),'f':('Arial',17),'bg':'gray','fg':'white','r':1,'c':4,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'%':{'cmd':lambda:add_op('%'),'f':('Arial',20),'bg':'gray','fg':'white','r':2,'c':4,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'1/x':{'cmd':lambda:update(),'f':('Arial',17),'bg':'gray','fg':'white','r':3,'c':4,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'=':{'cmd':lambda:calculate(),'f':('Arial',25,'bold'),'bg':'#FF8500','fg':'white','r':4,'c':4,'w':None,'abg':'#0095FF','afg':'white','rs':2,'cs':None},'(':{'cmd':lambda:update(),'f':('Consolas',20),'bg':'gray','fg':'white','r':7,'c':0,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},')':{'cmd':lambda:update(),'f':('Consolas',20),'bg':'gray','fg':'white','r':7,'c':1,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'n!':{'cmd':lambda:update(),'f':('Arial',20),'bg':'gray','fg':'white','r':7,'c':2,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'xⁿ':{'cmd':lambda:add_op('^'),'f':('Consolas',20),'bg':'gray','fg':'white','r':7,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'π':{'cmd':lambda:add_num('π'),'f':('Consolas',20),'bg':'gray','fg':'white','r':7,'c':4,'w':None,'abg':None,'afg':None,'rs':None,'cs':None}}
	# This is a dictionary that contains all keyboard binds(keys are events and values are functions associated with them):
	binds = {'1':lambda e:add_num(1),'2':lambda e:add_num(2),'3':lambda e:add_num(3),'4':lambda e:add_num(4),'5':lambda e:add_num(5),'6':lambda e:add_num(6),'7':lambda e:add_num(7),'8':lambda e:add_num(8),'9':lambda e:add_num(9),'0':lambda e:add_num(0),'π':lambda e:add_num('π'),',':lambda e:add_op(','),'/':lambda e:add_op('/'),'*':lambda e:add_op('*'),'+':lambda e:add_op('+'),'-':lambda e:add_op('-'),'^':lambda e:add_op('^'),'<Control-L>':clear_screen,'<Control-l>':clear_screen,'C':clear_screen,'<Return>':calculate,'<space>':calculate,'=':calculate,'a':lambda e:None,'b':lambda e:None,'c':lambda e:None,'d':lambda e:None,'e':lambda e:None}

	# This loop creates all the buttons and keyboard binds:
	for btn, bnd in zip(buttons, binds):
		make_btn(cmd = buttons[btn]['cmd'], t=btn , f=buttons[btn]['f'], bg=buttons[btn]['bg'], fg=buttons[btn]['fg'], abg=buttons[btn]['abg'], afg=buttons[btn]['afg'], r=buttons[btn]['r'], c=buttons[btn]['c'], w=buttons[btn]['w'], rs=buttons[btn]['rs'], cs=buttons[btn]['cs'])
		window.bind(bnd, binds[bnd])

	# Places the calculator screen on the window:
	screen.grid(row=0, column=0, columnspan=5)
	update_screen(0)

	# Here I have so far disabled the buttons, the work of which I have not yet coded:
	block_btn(1, 2, 14, 19, 20, 21, 24, 23, 25)

make_interface()

window.mainloop()
