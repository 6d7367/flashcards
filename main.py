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

	def remove(self):
		pass

class FlashCardsMode(Mode):
	def start(self, root):
		self.root = root
		self.frm1 = tk.Frame(self.root)
		self.frm2 = tk.Frame(self.root)
		self.frm3 = tk.Frame(self.root)

		fnt = ("Helvetica", 29)

		self.text_top = tk.StringVar(self.root)
		self.text_top.set("")

		self.text_bottom = tk.StringVar(self.root)
		self.text_bottom.set("")

		label1 = tk.Label(self.frm1, textvar = self.text_top , font = fnt)
		label2 = tk.Label(self.frm2, textvar = self.text_bottom, font = fnt)

		self.auto = tk.IntVar()
		checkbox = tk.Checkbutton(self.frm3, text = "Auto (5 seconds)", variable = self.auto)


		label1.pack(fill = tk.BOTH)
		label2.pack(fill = tk.BOTH)
		checkbox.pack(side = tk.LEFT)

		self.frm1.pack(side = tk.TOP, expand = 1)
		self.frm2.pack(side = tk.TOP, expand = 1)
		self.frm3.pack(side = tk.BOTTOM, fill = tk.X)

		self.root.bind('<Button-1>', self.show_next)

		self.show_next()

		self.run_thread = True
		self.thread = threading.Thread(target = self.change_auto)
		self.thread.setDaemon(True)
		self.thread.start()


	def show_next(self, *args, **kwargs):
		print('FlashCardsMode.show_next')
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

	def remove(self):
		self.frm1.destroy()
		self.frm2.destroy()
		self.frm3.destroy()

		self.root.unbind('<Button-1>')
		pass

class QuestionMode(Mode):
	def start(self, root):
		self.question_frame = tk.Frame(root)
		self.choices_frame = tk.Frame(root)
		self.next_frame = tk.Frame(root)

		style_question = ("Helvetica", 29)
		style_choice = ("Helvetica", 18)

		self.question_var = tk.StringVar(root)
		self.question_var.set("?")
		question_label = tk.Label(self.question_frame, textvar = self.question_var , font = style_question)

		self.answer_variable = tk.IntVar()
		self.choices = {}

		self.default_color = "#000"
		self.wrong_color = "#f00"
		self.right_color = "#0c0"

		for i in range(4):
			choice_text_var = tk.StringVar()
			choice_text_var.set("choice {}".format(i))
			self.choices[i] = {
				"text_var": choice_text_var,
				"radio": tk.Radiobutton(self.choices_frame, fg = self.default_color, textvar = choice_text_var, value = i, variable = self.answer_variable, command = self._check_answer, font = style_choice),
				"is_true": False,
			}
			self.choices[i]["radio"].pack(anchor = tk.W)

		tk.Button(self.next_frame, text = ">>", command = self.show_next).pack(pady = 10)


		question_label.pack(fill = tk.BOTH)

		self.question_frame.pack(side = tk.TOP, expand = 1)
		self.choices_frame.pack(side = tk.TOP, expand = 1)
		self.next_frame.pack(side = tk.BOTTOM, fill = tk.X)

		self.show_next()

	def show_next(self, *args, **kwargs):
		print('QuestionMode.show_next')
		self._default_choices_colors()

		new_choices = self._next_questions()

		for k, choice in new_choices["choices"].items():
			choice_text = self.data[choice]["translated"]
			self.choices[k]["text_var"].set(choice_text)
			self.choices[k]["is_true"] = False

			if k == new_choices["right_answer"]:
				question_text = self.data[choice]["original"]
				self.question_var.set(question_text)
				self.choices[k]["is_true"] = True
	
	def _default_choices_colors(self):
		for _, choice in self.choices.items():
			choice["radio"].configure(fg = self.default_color)

	def _next_questions(self):
		new_choices_indexes = {}
		while True:
			if len(new_choices_indexes) == 4:
				break

			word_index = random.randint(0, self.data_len - 1)
			if word_index not in new_choices_indexes.values():
				new_choices_indexes[len(new_choices_indexes)] = word_index

		right_answer_index = random.randint(0, 3)

		return { "choices": new_choices_indexes, "right_answer": right_answer_index }

	def _check_answer(self):
		self._default_choices_colors()
		answer = self.answer_variable.get()
		for k, choice in self.choices.items():
			if k == answer:
				if not choice["is_true"]:
					choice["radio"].configure(fg = self.wrong_color)

			if choice["is_true"]:
				choice["radio"].configure(fg = self.right_color)

	def remove(self):
		self.question_frame.destroy()
		self.choices_frame.destroy()
		self.next_frame.destroy()




class App(tk.Tk):
	def __init__(self, path_to_dict, modes):
		super().__init__()

		self.geometry('700x400')
		self.title('Flash Cards')

		self.path_to_dict = path_to_dict
		self.modes = modes
		self.mode = None


		top_frame = tk.Frame(self)


		tk.Button(top_frame, text = "Dict", command = lambda: self.change_mode(0) ).grid(row = 0, column = 0, sticky=tk.W+tk.E)
		tk.Button(top_frame, text = "Quiz", command = lambda: self.change_mode(1) ).grid(row = 0, column = 1, sticky=tk.W+tk.E)

		top_frame.pack(fill = tk.X)
		top_frame.columnconfigure(0, weight = 1)
		top_frame.columnconfigure(1, weight = 1)

	def change_mode(self, mode_number):
		if self.mode:
			self.mode.remove()
			del self.mode

		self.mode = self.modes[mode_number](self.path_to_dict)
		self.mode.start(self)


if __name__ == '__main__':
	app = App(DEFAULT_DATA_FILE, [ FlashCardsMode, QuestionMode ])
	app.mainloop()
