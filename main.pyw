import tkinter as tk
import random

from tkinter import messagebox

class Minesweeper:
	def __init__(self, master, rows, cols, num_mines):
		self.master = master
		self.rows = rows
		self.cols = cols
		self.num_mines = num_mines
		self.minefield = [[0 for _ in range(cols)] for _ in range(rows)]
		self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
		self.flags = [[False for _ in range(cols)] for _ in range(rows)]
		self.game_over = False

		self.create_minefield()
		self.create_gui()

	def create_minefield(self):
		mines = random.sample(range(self.rows * self.cols), self.num_mines)
		
		for mine in mines:
			row = mine // self.cols
			col = mine % self.cols
			self.minefield[row][col] = -1

		for row in range(self.rows):
			for col in range(self.cols):
				if self.minefield[row][col] != -1:
					self.minefield[row][col] = self.count_neighbor_mines(row, col)

	def count_neighbor_mines(self, row, col):
		count = 0
		for i in range(-1, 2):
			for j in range(-1, 2):
				if 0 <= row + i < self.rows and 0 <= col + j < self.cols:
					if self.minefield[row + i][col + j] == -1:
						count += 1
		return count

	def create_gui(self):
		self.frame = tk.Frame(self.master)
		self.frame.pack()

		for row in range(self.rows):
			for col in range(self.cols):
				button = tk.Button(
					self.frame, width=2, height=1, 
					command=lambda r=row, c=col: self.button_click(r, c)
				)
				button.bind('<Button-3>', lambda event, r=row, c=col: self.button_right_click(event, r, c))
				button.bind('<Double-Button-1>', lambda event, r=row, c=col: self.button_double_click(event, r, c))
				button.grid(row=row, column=col)
				self.buttons[row][col] = button

	def button_click(self, row, col):
		if self.game_over:
			return

		if self.flags[row][col]:
			return

		if self.minefield[row][col] == -1:
			self.game_over = True
			self.buttons[row][col].config(text='x', fg='red', borderwidth=2, relief='groove')
			self.reveal_mines()
			self.show_message('You lost the game!')
		elif self.minefield[row][col] == 0:
			self.clear_zeros(row, col)
		else:
			self.buttons[row][col].config(text=str(self.minefield[row][col]), borderwidth=2, relief='groove', state='disabled')

		if self.check_win():
			self.game_over = True
			self.show_message('Congratulations! You won the game!')

	def button_right_click(self, event, row, col):
		if self.game_over:
			return

		if self.buttons[row][col]['state'] == 'normal':
			if not self.flags[row][col]:
				self.buttons[row][col].config(text='F', fg='blue')
				self.flags[row][col] = True
			else:
				self.buttons[row][col].config(text='', fg='black')
				self.flags[row][col] = False

	def reveal_mines(self):
		for row in range(self.rows):
			for col in range(self.cols):
				if self.minefield[row][col] == -1:
					self.buttons[row][col].config(text='x', fg='red', borderwidth=2, relief='groove')

	def clear_zeros(self, row, col):
		if (
			0 <= row < self.rows and
			0 <= col < self.cols and
			self.buttons[row][col]['state'] != 'disabled'
		):
			value = str(self.minefield[row][col])
			if value == '0':
				value = ' '
			
			self.buttons[row][col].config(text=value, borderwidth=2, relief='groove', state='disabled')
			if self.minefield[row][col] == 0:
				for i in range(-1, 2):
					for j in range(-1, 2):
						self.clear_zeros(row + i, col + j)

	def button_double_click(self, event, row, col):
		if self.game_over:
			return

		if self.buttons[row][col]['state'] == 'disabled' and self.minefield[row][col] > 0:
			flagged_neighbors = self.get_flagged_neighbors(row, col)
			if len(flagged_neighbors) == self.minefield[row][col]:
				self.clear_unflagged_neighbors(row, col, flagged_neighbors)

	def get_flagged_neighbors(self, row, col):
		flagged_neighbors = []
		for i in range(-1, 2):
			for j in range(-1, 2):
				if 0 <= row + i < self.rows and 0 <= col + j < self.cols:
					if self.flags[row + i][col + j]:
						flagged_neighbors.append((row + i, col + j))
		return flagged_neighbors

	def clear_unflagged_neighbors(self, row, col, flagged_neighbors):
		for i in range(-1, 2):
			for j in range(-1, 2):
				if 0 <= row + i < self.rows and 0 <= col + j < self.cols:
					if not self.flags[row + i][col + j] and self.buttons[row + i][col + j]['state'] == 'normal':
						self.button_click(row + i, col + j)

	def check_win(self):
		for row in range(self.rows):
			for col in range(self.cols):
				if (
					self.minefield[row][col] != -1 and
					not self.flags[row][col] and
					self.buttons[row][col]['state'] != 'disabled'
				):
					return False
		return True

	def show_message(self, message):
		messagebox.showinfo('Game Over', message)
	
	def restart_game(self):
		for row in range(self.rows):
			for col in range(self.cols):
				self.buttons[row][col].config(text=" ", borderwidth = 2, relief='raised', bg='SystemButtonFace', state='normal')
				self.flags[row][col] = False

		self.minefield = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
		self.create_minefield()
		self.game_over = False

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Minesweeper')
	root.resizable(False, False)
	
	rows = 10
	cols = 10
	num_mines = 10
	game = Minesweeper(root, rows, cols, num_mines)

	button = tk.Button(game.master, text='⟳', width=4, height=2, command=game.restart_game)
	button.pack()
	
	root.mainloop()
