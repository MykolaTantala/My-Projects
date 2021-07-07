from tkinter import Tk, Frame, Label, Button

if __name__ == '__main__':
	print("To start the Snake Game you need to run the file 'snake.py'")
	exit()

"""Це "інтерфейс". Я не хотів прописувати його в основному коді, тому написав цей модуль.
Ну його перша версія була просто фреймом, який зберігав статистику.
Спочатку я задумував для нього більше функцій ніж просто містити 2 мітки, тому перетворив його в клас.
Але в результаті я багато чого не доробив, а потім вирізав, а всередині цього інтерфейсу лишив просто 2 мітки.
Одна показує ігрові очки, інша ігровий рекорд"""
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