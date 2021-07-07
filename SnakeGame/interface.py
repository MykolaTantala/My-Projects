from tkinter import Tk, Frame, Label, Button

if __name__ == '__main__':
	print("To start the Snake Game you need to run the file 'snake.py'")
	exit()

"""This is the "interface". I didn't want to prescribe it in the main code, so I wrote this module.
Well, its first version was just a frame that kept statistics.
At first, I designed more functions for it than just containing 2 labels, so I turned it into a class.
But as a result, I did not finish much, and then cut, and inside this interface left just 2 labels.
One shows game points, the other a game record"""
class Interface:
	def __init__(self, win):
		self.make_interface(win)
	def make_interface(self, win):
		self.interface = Frame(win, bg='black', highlightbackground="white", highlightthickness=2)
		self.interface.pack(fill='x')
		self.score_text = Label(self.interface, text="Score: 0", font=('Arial', 20), bg='black', fg='white', width=9, anchor='w')
		self.score_text.pack(side='left')
		high_score = open('record.txt', 'r')
		self.high_score_text = Label(self.interface, text = f"High score: {high_score.read()}", font=('Arial', 20), bg='black', fg='white', width=15)
		high_score.close()
		self.high_score_text.pack(side='right')
	def set_score(self, score):
		self.score_text["text"] = f"Score: {score}"
