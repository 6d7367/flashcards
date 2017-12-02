#!/usr/bin/env python3

import tkinter as tk

class Mode():
	def start(self, root):
		pass

	def show_next(self, *args, **kwargs):
		pass

class FlashCardsMode(Mode):
	def start(self, root):
		frm1 = tk.Frame(root)
		frm2 = tk.Frame(root)

		fnt = ("Helvetica", 29)

		self.text_top = tk.StringVar(root)
		self.text_top.set("TEXT TOP")

		self.text_bottom = tk.StringVar(root)
		self.text_bottom.set("TEXT TOP")

		label1 = tk.Label(frm1, textvar = self.text_top , font = fnt)
		label2 = tk.Label(frm2, textvar = self.text_bottom, font = fnt)

		label1.pack(fill = tk.BOTH)
		label2.pack(fill = tk.BOTH)

		frm1.pack(side = tk.TOP, expand = 1)
		frm2.pack(side = tk.BOTTOM, expand = 1)

		root.bind('<Button-1>', self.show_next)

	def show_next(self, *args, **kwargs):
		pass


class App(tk.Tk):
	def __init__(self, mode):
		super().__init__()

		self.geometry('700x400')
		self.title('Flash Cards')

		self.mode = mode
		self.mode.start(self)


if __name__ == '__main__':
	mode = FlashCardsMode()
	app = App(mode)

	app.mainloop()
