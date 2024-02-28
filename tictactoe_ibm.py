import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Check if there's a win on the board
def check_win(board):
    # Check rows and columns for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] != " " or board[0][2] == board[1][1] == board[2][0] != " ":
        return board[1][1]
    return None

# Check if the board is full and it's a tie
def check_tie(board):
    for row in board:
        if " " in row:
            return False
    return True

# The main class for our game
class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x300")  # Adjusted window size for instruction label
        self.frame = tk.Frame(self.master)  # Frame for the game buttons
        self.frame.pack(pady=(20, 0))

        # Display instructions
        self.instructions = tk.Label(self.master, text="Use keys (1-9) to make a move.\n1 = top left, 9 = bottom right.", font=('Helvetica', 13))
        self.instructions.pack(pady=(10, 20))

        # Getting player names and setting up the game
        self.player1, self.player2 = self.get_player_names()
        self.first_player, self.second_player = self.pick_first_player(self.player1, self.player2)
        self.player_symbols = {self.first_player: "X", self.second_player: "O"}
        self.current_player = self.first_player
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.status_label = tk.Label(self.master, text="", font=('Helvetica', 12))
        self.status_label.pack(pady=10)
        self.update_status_label()
        self.create_board()
        self.keyboard_input()

    # Bind keyboard events
    def keyboard_input(self):
        self.master.bind("1", lambda event: self.button_click(0, 0))
        self.master.bind("2", lambda event: self.button_click(0, 1))
        self.master.bind("3", lambda event: self.button_click(0, 2))
        self.master.bind("4", lambda event: self.button_click(1, 0))
        self.master.bind("5", lambda event: self.button_click(1, 1))
        self.master.bind("6", lambda event: self.button_click(1, 2))
        self.master.bind("7", lambda event: self.button_click(2, 0))
        self.master.bind("8", lambda event: self.button_click(2, 1))
        self.master.bind("9", lambda event: self.button_click(2, 2))

    # Get player names, with defaults if they cancel
    def get_player_names(self):
        player1 = simpledialog.askstring("Player Name", "Enter the name of player 1:")
        if not player1:
            player1 = "Player 1"

        while True:
            player2 = simpledialog.askstring("Player Name", "Enter the name of player 2:")
            if not player2:
                player2 = "Player 2"
            if player2 != player1:
                break
            else:
                messagebox.showerror("Name Error", "Player 2 cannot have the same name as Player 1. Please enter a different name.")

        return player1, player2

    # Decide who goes first, either by choice or random
    def pick_first_player(self, player1, player2):
        while True:
            choice = simpledialog.askstring("Player Order", "Do you want to randomize who goes first? (yes/no):").lower()
            if choice in ["yes", "no"]:
                if choice == "yes":
                    return (player1, player2) if random.randint(0, 1) == 0 else (player2, player1)
                else:
                    # Code to manually decide who goes first, if not randomizing
                    while True:
                        first_player = simpledialog.askstring("Player Order", f"Who goes first, {player1} or {player2}?")
                        if first_player in [player1, player2]:
                            return (player1, player2) if first_player == player1 else (player2, player1)
                        else:
                            messagebox.showerror("Error", "Enter a valid player name.")
            else:
                messagebox.showerror("Invalid Input", "Answer 'yes' or 'no'.")

    # Create the board with clickable buttons
    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.frame, text=' ', width=8, height=3,
                                   command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    # Update the status label to show who's turn it is
    def update_status_label(self):
        self.status_label.config(text=f"{self.current_player}'s turn ({self.player_symbols[self.current_player]})")

    # Make button clicks for making moves
    def button_click(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.player_symbols[self.current_player]
            self.buttons[row][col].config(text=self.player_symbols[self.current_player])
            winner_symbol = check_win(self.board)
            if winner_symbol:
                # Show the winner and close the game
                winner_name = self.first_player if self.player_symbols[self.first_player] == winner_symbol else self.second_player
                messagebox.showinfo("Game Over", f"{winner_name} wins the game")
                self.master.destroy()
            elif check_tie(self.board):
                # Show that it is a tie and close the game
                messagebox.showinfo("Game Over", "The game is a tie")
                self.master.destroy()
            else:
                # Switch which player's turn it is
                self.current_player = self.second_player if self.current_player == self.first_player else self.first_player
                self.update_status_label()
        else:
            messagebox.showerror("Error", "This is already taken. Choose another one.")

# Main function to start the game
def play_gui_game():
    gui = tk.Tk()
    gui.title("Tic Tac Toe")
    TicTacToeGUI(gui)
    gui.mainloop()

if __name__ == "__main__":
    play_gui_game()
