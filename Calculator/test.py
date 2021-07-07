import tkinter as tk
from calc import *

# Налаштування вікна:
window = tk.Tk()
screen = tk.Text(window, font=('Consolas', 20), bd=3, bg='black', fg='white', width = 23, height=2, wrap='none')
window.geometry("353x472+500+225")
window.resizable(False, False)

def update():
	pass

def add_num(num):
	pass

def add_op(op):
	pass

def calculate():
	pass

def clear_screen():
	pass

def clear_entry():
	pass

def clear_last():
	pass

buttons_objects = [] # список, де зберігаються усі кнопки.
btn_num = 0  # допоміжна змінна, що використовується у функції make_btn().
# Функція, яка створює кнопку із заданими параметрами. Усім необов'язковим аргументам задано значення None. Усі обов'язкові аргумети зберігаються в kw:
def make_btn(**kw):
	global btn_num
	buttons_objects.append(tk.Button(window, text=kw['t'], font=kw['f'], bg=kw['bg'], fg=kw['fg'], command=kw['cmd'], width=kw['w'], activebackground=kw['abg'], activeforeground=kw['afg']))
	buttons_objects[btn_num].grid(row=kw['r'], column=kw['c'], stick='wens', ipady=5, rowspan=kw['rs'], columnspan=kw['cs'])
	btn_num+=1

buttons={'C':{'cmd':lambda:clear_screen(),'f':('Arial',20),'bg':'#FF8500','fg':'white','abg':'#0095FF','afg':'white','r':1,'c':2,'w':None,'rs':None,'cs':None},'CE':{'cmd':lambda:clear_entry(),'f':('Arial',20),'bg':'#FF8500','fg':'white','abg':'#0095FF','afg':'white','r':1,'c':1,'w':None,'rs':None,'cs':None},'←' :{'cmd':lambda:clear_last(),'f':('Impact',20,'bold'),'bg':'#FF8500','fg':'white','abg':'#0095FF','afg':'white','r':1,'c':0,'w':None,'rs':None,'cs':None},'1':{'cmd':lambda:add_num(1),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':2,'c':0,'abg':None,'afg':None,'rs':None,'cs':None},'2':{'cmd':lambda:add_num(2),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':2,'c':1,'abg':None,'afg':None,'rs':None,'cs':None},'3':{'cmd':lambda:add_num(3),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':2,'c':2,'abg':None,'afg':None,'rs':None,'cs':None},'4':{'cmd':lambda:add_num(4),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':3,'c':0,'abg':None,'afg':None,'rs':None,'cs':None},'5':{'cmd':lambda:add_num(5),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':3,'c':1,'abg':None,'afg':None,'rs':None,'cs':None},'6':{'cmd':lambda:add_num(6),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':3,'c':2,'abg':None,'afg':None,'rs':None,'cs':None},'7':{'cmd':lambda:add_num(7),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':4,'c':0,'abg':None,'afg':None,'rs':None,'cs':None},'8':{'cmd':lambda:add_num(8),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':4,'c':1,'abg':None,'afg':None,'rs':None,'cs':None},'9':{'cmd':lambda:add_num(9),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':4,'c':2,'abg':None,'afg':None,'rs':None,'cs':None},'0':{'cmd':lambda:add_num(0),'f':('Arial',20),'bg':'black','fg':'white','w':3,'r':5,'c':0,'abg':None,'afg':None,'rs':None,'cs':2},',':{'cmd':lambda:add_op(','),'f':('Arial',20,'bold'),'bg':'black','fg':'white','r':5,'c':2,'w':3,'abg':None,'afg':None,'rs':None,'cs':None},'±':{'cmd':lambda:update(),'f':('Arial',20),'bg':'gray','fg':'white','r':1,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'/':{'cmd':lambda:add_op('/'),'f':('Arial',20),'bg':'gray','fg':'white','r':2,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'*':{'cmd':lambda:add_op('*'),'f':('Arial',20),'bg':'gray','fg':'white','r':3,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'+':{'cmd':lambda:add_op('+'),'f':('Arial',20),'bg':'gray','fg':'white','r':4,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'-':{'cmd':lambda:add_op('-'),'f':('Arial',20),'bg':'gray','fg':'white','r':5,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'ⁿ√x':{'cmd':lambda:update(),'f':('Arial',17),'bg':'gray','fg':'white','r':1,'c':4,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'%':{'cmd':lambda:add_op('%'),'f':('Arial',20),'bg':'gray','fg':'white','r':2,'c':4,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'1/x':{'cmd':lambda:update(),'f':('Arial',17),'bg':'gray','fg':'white','r':3,'c':4,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'=':{'cmd':lambda:calculate(),'f':('Arial',25,'bold'),'bg':'#FF8500','fg':'white','r':4,'c':4,'w':None,'abg':'#0095FF','afg':'white','rs':2,'cs':None},'(':{'cmd':lambda:update(),'f':('Consolas',20),'bg':'gray','fg':'white','r':7,'c':0,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},')':{'cmd':lambda:update(),'f':('Consolas',20),'bg':'gray','fg':'white','r':7,'c':1,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'n!':{'cmd':lambda:update(),'f':('Arial',20),'bg':'gray','fg':'white','r':7,'c':2,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'xⁿ':{'cmd':lambda:update(),'f':('Consolas',20),'bg':'gray','fg':'white','r':7,'c':3,'w':None,'abg':None,'afg':None,'rs':None,'cs':None},'π':{'cmd':lambda:update(),'f':('Consolas',20),'bg':'gray','fg':'white','r':7,'c':4,'w':None,'abg':None,'afg':None,'rs':None,'cs':None}}
binds = {'1':lambda e:add_num(1),
				'2':lambda e:add_num(2),
				'3':lambda e:add_num(3),
				'4':lambda e:add_num(4),
				'5':lambda e:add_num(5),
				'6':lambda e:add_num(6),
				'7':lambda e:add_num(7),
				'8':lambda e:add_num(8),
				'9':lambda e:add_num(9),
				'0':lambda e:add_num(0),
				'π':lambda e:add_num('π'),
				',':lambda e:add_op(','),
				'/':lambda e:add_op('/'),
				'*':lambda e:add_op('*'),
				'+':lambda e:add_op('+'),
				'-':lambda e:add_op('-'),
				'^':lambda e:add_op('^'),
				'<Control-L>':clear_screen,
				'<Control-l>':clear_screen,
				'C':clear_screen,
				'<Return>':calculate,
				'<space>':calculate,
				'=':calculate,
				'a':lambda e:None,
				'b':lambda e:None,
				'c':lambda e:None,
				'd':lambda e:None,
				'e':lambda e:None}

def make_interface():
	screen.grid(row=0, column=0, columnspan=5)
	for btn, bnd in zip(buttons, binds):
		make_btn(cmd = buttons[btn]['cmd'], t=btn , f=buttons[btn]['f'], bg=buttons[btn]['bg'], fg=buttons[btn]['fg'], abg=buttons[btn]['abg'], afg=buttons[btn]['afg'], r=buttons[btn]['r'], c=buttons[btn]['c'], w=buttons[btn]['w'], rs=buttons[btn]['rs'], cs=buttons[btn]['cs'])
		window.bind(bnd, binds[bnd])

make_interface()

window.mainloop()