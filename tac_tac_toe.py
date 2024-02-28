import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Check if there's a win on the board
def check_win(game_board):
    # Check rows and columns for a win
    for i in range(3):
        if game_board[i][0] == game_board[i][1] == game_board[i][2] != " ":
            return game_board[i][0]
        if game_board[0][i] == game_board[1][i] == game_board[2][i] != " ":
            return game_board[0][i]
    # Check diagonals for a win
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != " " or game_board[0][2] == game_board[1][1] == game_board[2][0] != " ":
        return game_board[1][1]
    return None

# Check if the board is full and it's a tie
def check_tie(game_board):
    for row in game_board:
        if " " in row:
            return False
    return True

# The main class for our game
class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x300") # Adjusted window size for instruction label
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(pady=(20, 0))
        # Display instructions
        self.instructions_label = tk.Label(self.root, text="Use keys (1-9) to make a move.\n1 = top left, 9 = bottom right.", font=('Helvetica', 13))
        self.instructions_label.pack(pady=(10, 20))
        # Get player names and setting up the game
        self.p1_name, self.p2_name = self.player_names()
        self.first_player, self.second_player = self.first_player_decision(self.p1_name, self.p2_name)
        self.symbols = {self.first_player: "X", self.second_player: "O"}
        self.turn = self.first_player
        self.game_board = [[" " for _ in range(3)] for _ in range(3)]
        self.board_buttons = [[None for _ in range(3)] for _ in range(3)]
        self.turn_label = tk.Label(self.root, text="", font=('Helvetica', 12))
        self.turn_label.pack(pady=10)
        self.display_turn()
        self.build_board()
        self.keyboard_input()

    # Bind keyboard events
    def keyboard_input(self):
        # Either the keyboard or mouse can be used to play the game
        self.root.bind("1", lambda event: self.button_clicking(0, 0))
        self.root.bind("2", lambda event: self.button_clicking(0, 1))
        self.root.bind("3", lambda event: self.button_clicking(0, 2))
        self.root.bind("4", lambda event: self.button_clicking(1, 0))
        self.root.bind("5", lambda event: self.button_clicking(1, 1))
        self.root.bind("6", lambda event: self.button_clicking(1, 2))
        self.root.bind("7", lambda event: self.button_clicking(2, 0))
        self.root.bind("8", lambda event: self.button_clicking(2, 1))
        self.root.bind("9", lambda event: self.button_clicking(2, 2))

    # Get player names, with defaults if they cancel
    def player_names(self):
        p1 = simpledialog.askstring("Player Name", "Enter player 1 name:")
        if not p1:
            p1 = "Player 1"
        while True:
            p2 = simpledialog.askstring("Player Name", "Enter player 2 name:")
            if not p2:
                p2 = "Player 2"
            if p2 != p1:
                break
            else:
                messagebox.showerror("Name Error", "Both players cannot share the same name.")
        return p1, p2

    # Decide who goes first, either by choice or random
    def first_player_decision(self, p1, p2):
        while True:
            choice = simpledialog.askstring("Player Order", "Randomize first player? (yes/no):").lower()
            if choice in ["yes", "no"]:
                if choice == "yes":
                    return (p1, p2) if random.randint(0, 1) == 0 else (p2, p1)
                else:
                    # Code to manually decide who goes first, if not randomizing
                    while True:
                        fp = simpledialog.askstring("Player Order", f"Who starts, {p1} or {p2}?")
                        if fp in [p1, p2]:
                            return (p1, p2) if fp == p1 else (p2, p1)
                        else:
                            messagebox.showerror("Error", "Please enter a valid name.")
            else:
                messagebox.showerror("Invalid Input", "Please type 'yes' or 'no'.")

    # Create the board with clickable buttons
    def build_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.game_frame, text=' ', width=8, height=3, command=lambda r=i, c=j: self.button_clicking(r, c))
                btn.grid(row=i, column=j)
                self.board_buttons[i][j] = btn

    # Update the status label to show who's turn it is
    def display_turn(self):
        self.turn_label.config(text=f"{self.turn}'s turn ({self.symbols[self.turn]})")

    # Make button clicks for making moves
    def button_clicking(self, row, col):
        if self.game_board[row][col] == " ":
            self.game_board[row][col] = self.symbols[self.turn]
            self.board_buttons[row][col].config(text=self.symbols[self.turn])
            if check_win(self.game_board):
                # Show the winner and close the game
                messagebox.showinfo("Game Over", f"{self.turn} wins!")
                self.root.destroy()
            elif check_tie(self.game_board):
                # Show that it is a tie and close the game
                messagebox.showinfo("Game Over", "It's a tie!")
                self.root.destroy()
            else:
                # Switch which player's turn it is
                self.turn = self.second_player if self.turn == self.first_player else self.first_player
                self.display_turn()
        else:
            messagebox.showerror("Error", "Spot taken. Try another.")

# Main function to start the game
def main():
    window = tk.Tk()
    window.title("Tic Tac Toe")
    TicTacToeGame(window)
    window.mainloop()

if __name__ == "__main__":
    main()
