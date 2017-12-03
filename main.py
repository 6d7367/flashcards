#!/usr/bin/env python3

import tkinter as tk
import random
import threading
import time

DEFAULT_DATA_FILE = "data/eo-en.txt"

class Mode():
	def __init__(self, path_to_dict):
		self.data = []
		with open(path_to_dict, 'r') as f:
			for line in f:
				line = line.strip()

				# comment/empty line
				if line.startswith('#') or (len(line) < 1):
					continue

				try:
					original, translated = line.split(':')
					self.data.append({ "original": original.strip(), "translated": translated.strip() })
				except Exception as e:
					msg = "Error on '{}' line".format(line.strip())
					print(msg)

		self.data_len = len(self.data)


	def start(self, root):
		pass

	def show_next(self, *args, **kwargs):
		pass

class FlashCardsMode(Mode):
	def start(self, root):
		frm1 = tk.Frame(root)
		frm2 = tk.Frame(root)
		frm3 = tk.Frame(root)

		fnt = ("Helvetica", 29)

		self.text_top = tk.StringVar(root)
		self.text_top.set("")

		self.text_bottom = tk.StringVar(root)
		self.text_bottom.set("")

		label1 = tk.Label(frm1, textvar = self.text_top , font = fnt)
		label2 = tk.Label(frm2, textvar = self.text_bottom, font = fnt)

		self.auto = tk.IntVar()
		checkbox = tk.Checkbutton(frm3, text = "Auto (5 seconds)", variable = self.auto)


		label1.pack(fill = tk.BOTH)
		label2.pack(fill = tk.BOTH)
		checkbox.pack(side = tk.LEFT)

		frm1.pack(side = tk.TOP, expand = 1)
		frm2.pack(side = tk.TOP, expand = 1)
		frm3.pack(side = tk.BOTTOM, fill = tk.X)

		root.bind('<Button-1>', self.show_next)

		self.show_next()

		self.run_thread = True
		self.thread = threading.Thread(target = self.change_auto)
		self.thread.setDaemon(True)
		self.thread.start()


	def show_next(self, *args, **kwargs):
		if self.data_len < 1:
			return

		new_pair_number = random.randint(0, self.data_len - 1)
		new_pair = self.data[new_pair_number]

		self.text_top.set(new_pair['original'])
		self.text_bottom.set(new_pair['translated'])

	def change_auto(self):
		while self.run_thread:
			if self.auto.get():
				self.show_next()
				time.sleep(5)



class App(tk.Tk):
	def __init__(self, mode):
		super().__init__()

		self.geometry('700x400')
		self.title('Flash Cards')

		self.mode = mode
		self.mode.start(self)

if __name__ == '__main__':
	mode = FlashCardsMode(DEFAULT_DATA_FILE)
	app = App(mode)

	app.mainloop()
