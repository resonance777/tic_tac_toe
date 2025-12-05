import tkinter as tk
import random
import json
import os

# Constants
WINDOW_TITLE = "Tic-Tac-Toe – Ruslan Sabitov"
BOARD_SIZE = 3
SCORES_FILE = "scores.json"

# Colors
BG_COLOR = "#222831"
BOARD_BG = "#393E46"
BTN_BG = "#EEEEEE"
BTN_FG = "#222831"
BTN_DISABLED_BG = "#B2B2B2"
WIN_HIGHLIGHT_BG = "#00ADB5"
STATUS_FG = "#EEEEEE"


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.configure(bg=BG_COLOR)

        # game status
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.winning_cells = []
        self.game_over = False

        # game mode: computer / pvp
        self.mode_var = tk.StringVar(value="computer")
        self.vs_computer = True

        # selection of player's symbol (player vs computer)
        self.symbol_var = tk.StringVar(value="X")
        self.player_symbol = "X"
        self.computer_symbol = "O"

        # difficulty: easy / medium / hard
        self.difficulty_var = tk.StringVar(value="easy")

        # who is moving now
        self.current_player = self.player_symbol

        # SCORE: X, O, draw
        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.load_scores()

        self.create_widgets()
        self.update_turn_text()
        self.update_score_labels()

    def create_widgets(self):
        # Heading 
        self.title_label = tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=("Arial", 20, "bold"),
            bg=BG_COLOR,
            fg=STATUS_FG,
        )
        self.title_label.pack(pady=(10, 5))

        # Mode selection
        mode_frame = tk.Frame(self.root, bg=BG_COLOR)
        mode_frame.pack(pady=(0, 10))

        tk.Label(
            mode_frame, text="Mode:", font=("Arial", 10),
            bg=BG_COLOR, fg=STATUS_FG
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            mode_frame, text="Player vs Computer",
            variable=self.mode_var, value="computer",
            command=self.change_mode,
            bg=BG_COLOR, fg=STATUS_FG, selectcolor=BOARD_BG,
            font=("Arial", 9)
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            mode_frame, text="Player vs Player",
            variable=self.mode_var, value="pvp",
            command=self.change_mode,
            bg=BG_COLOR, fg=STATUS_FG, selectcolor=BOARD_BG,
            font=("Arial", 9)
        ).pack(side="left", padx=5)

        # choosing symbol X/O (player vs computer) 
        self.symbol_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.symbol_frame.pack(pady=(0, 10))

        tk.Label(
            self.symbol_frame, text="Choose your symbol:",
            font=("Arial", 10), bg=BG_COLOR, fg=STATUS_FG
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            self.symbol_frame, text="X", variable=self.symbol_var, value="X",
            command=self.change_symbol, bg=BG_COLOR,
            fg=STATUS_FG, selectcolor=BOARD_BG, font=("Arial", 9)
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            self.symbol_frame, text="O", variable=self.symbol_var, value="O",
            command=self.change_symbol, bg=BG_COLOR,
            fg=STATUS_FG, selectcolor=BOARD_BG, font=("Arial", 9)
        ).pack(side="left", padx=5)

        # Selection of difficulty (player vs computer)
        self.difficulty_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.difficulty_frame.pack(pady=(0, 10))

        tk.Label(
            self.difficulty_frame,
            text="Difficulty:",
            font=("Arial", 10),
            bg=BG_COLOR,
            fg=STATUS_FG
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            self.difficulty_frame,
            text="Easy",
            variable=self.difficulty_var,
            value="easy",
            bg=BG_COLOR,
            fg=STATUS_FG,
            selectcolor=BOARD_BG,
            font=("Arial", 9)
        ).pack(side="left", padx=3)

        tk.Radiobutton(
            self.difficulty_frame,
            text="Medium",
            variable=self.difficulty_var,
            value="medium",
            bg=BG_COLOR,
            fg=STATUS_FG,
            selectcolor=BOARD_BG,
            font=("Arial", 9)
        ).pack(side="left", padx=3)

        tk.Radiobutton(
            self.difficulty_frame,
            text="Hard",
            variable=self.difficulty_var,
            value="hard",
            bg=BG_COLOR,
            fg=STATUS_FG,
            selectcolor=BOARD_BG,
            font=("Arial", 9)
        ).pack(side="left", padx=3)

        # Field (canvas + buttons)
        self.canvas = tk.Canvas(
            self.root, width=300, height=300,
            bg=BOARD_BG, highlightthickness=0
        )
        self.canvas.pack()

        self.buttons = []
        for r in range(BOARD_SIZE):
            row_btns = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(
                    self.canvas,
                    text="", width=3, height=1,
                    font=("Arial", 28, "bold"),
                    bg=BTN_BG, fg=BTN_FG,
                    command=lambda row=r, col=c: self.handle_click(row, col),
                )
                self.canvas.create_window(c * 100 + 50, r * 100 + 50, window=btn)
                row_btns.append(btn)
            self.buttons.append(row_btns)

        # Status
        self.status_label = tk.Label(
            self.root, font=("Arial", 12),
            bg=BG_COLOR, fg=STATUS_FG
        )
        self.status_label.pack(pady=(5, 5))

        # Score
        self.score_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.score_frame.pack(pady=(0, 10))

        self.score_x_label = tk.Label(
            self.score_frame,
            font=("Arial", 10),
            bg=BG_COLOR,
            fg=STATUS_FG
        )
        self.score_x_label.pack(side="left", padx=5)

        self.score_o_label = tk.Label(
            self.score_frame,
            font=("Arial", 10),
            bg=BG_COLOR,
            fg=STATUS_FG
        )
        self.score_o_label.pack(side="left", padx=5)

        self.score_draws_label = tk.Label(
            self.score_frame,
            font=("Arial", 10),
            bg=BG_COLOR,
            fg=STATUS_FG
        )
        self.score_draws_label.pack(side="left", padx=5)

                # Button of reset scores
        self.reset_scores_button = tk.Button(
            self.root,
            text="Reset scores",
            font=("Arial", 10),
            command=self.reset_scores
        )
        self.reset_scores_button.pack(pady=(0, 5))


        # Button of a new game 
        self.reset_button = tk.Button(
            self.root, text="New Game",
            font=("Arial", 12), command=self.reset_game
        )
        self.reset_button.pack(pady=(0, 10))


    # working with scores
 

    def load_scores(self):
        if not os.path.exists(SCORES_FILE):
            return
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.scores["X"] = int(data.get("X", 0))
            self.scores["O"] = int(data.get("O", 0))
            self.scores["draws"] = int(data.get("draws", 0))
        except Exception:
            pass
    
    def reset_scores(self):
        """Full reset of the results history (X, O, draws)."""
        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.update_score_labels()
        self.save_scores()

    def save_scores(self):
        """Saving the score in scores.json."""
        try:
            with open(SCORES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.scores, f, indent=2)
        except Exception:
            pass

    def update_score_labels(self):
        """Updating the invoice display in the interface."""
        self.score_x_label.config(text=f"X wins: {self.scores['X']}")
        self.score_o_label.config(text=f"O wins: {self.scores['O']}")
        self.score_draws_label.config(text=f"Draws: {self.scores['draws']}")

    
    # Mode and symbol
   

    def change_mode(self):
        """Switching between vs computer and PvP."""
        self.vs_computer = self.mode_var.get() == "computer"

        if self.vs_computer:
            # showing choice of symbol and difficulty
            self.symbol_frame.pack(pady=(0, 10))
            self.difficulty_frame.pack(pady=(0, 10))
        else:
            # hiding the character selection and difficulty in PvP
            self.symbol_frame.forget()
            self.difficulty_frame.forget()
            # PvP: X is always the first
            self.player_symbol = "X"
            self.computer_symbol = "O"
            self.current_player = "X"

        self.reset_game()

    def change_symbol(self):
        """The player chooses X or O in vs Computer mode."""
        self.player_symbol = self.symbol_var.get()
        self.computer_symbol = "O" if self.player_symbol == "X" else "X"
        self.reset_game()

    
    # Logic of game
   

    def handle_click(self, row, col):
        if self.game_over or self.board[row][col] is not None:
            return

        # in player vs computer mode, you can only walk with the mouse when the player's turn is
        if self.vs_computer and self.current_player != self.player_symbol:
            return

        if self.vs_computer:
            symbol = self.player_symbol
        else:
            symbol = self.current_player

        self.make_move(row, col, symbol)

        if self.check_end_after_move():
            return

        if self.vs_computer:
            # move of computer
            self.current_player = self.computer_symbol
            self.update_turn_text()
            self.root.after(300, self.computer_move)
        else:
            # PvP: switching of player
            self.current_player = "O" if self.current_player == "X" else "X"
            self.update_turn_text()

    def make_move(self, row, col, symbol):
        self.board[row][col] = symbol
        self.buttons[row][col].config(text=symbol, state="disabled")

    
    # Move of computer and levels of difficulty
    

    def computer_move(self):
        """The computer's progress is adjusted for difficulty."""
        if self.game_over:
            return

        difficulty = self.difficulty_var.get()

        if difficulty == "easy":
            row, col = self.get_random_move()
        elif difficulty == "medium":
            row, col = self.get_medium_move()
        else:
            row, col = self.get_hard_move()

        if row is None:
            return

        self.make_move(row, col, self.computer_symbol)

        if self.check_end_after_move():
            return

        self.current_player = self.player_symbol
        self.update_turn_text()

    def get_random_move(self):
        free = [
            (r, c)
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
            if self.board[r][c] is None
        ]
        if not free:
            return None, None
        return random.choice(free)

    def find_winning_move(self, symbol):
        """looking for a move that leads to a symbol victory in one turn."""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] is None:
                    self.board[r][c] = symbol
                    winner, _ = self.check_winner()
                    self.board[r][c] = None
                    if winner == symbol:
                        return r, c
        return None, None

    def get_medium_move(self):
        """
        Medium:
        1) if we can win in one turn, we win
        2) if the player can win in one turn, we block
        3) otherwise — random
        """
        r, c = self.find_winning_move(self.computer_symbol)
        if r is not None:
            return r, c

        r, c = self.find_winning_move(self.player_symbol)
        if r is not None:
            return r, c

        return self.get_random_move()

    def get_hard_move(self):
        """
        Hard:
        1) win if possible
        2) block the player
        3) occupy the center
        4) take a corner
        5) otherwise — random
        """
        r, c = self.find_winning_move(self.computer_symbol)
        if r is not None:
            return r, c

        r, c = self.find_winning_move(self.player_symbol)
        if r is not None:
            return r, c

        center = (1, 1)
        if self.board[center[0]][center[1]] is None:
            return center

        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        free_corners = [(r, c) for (r, c) in corners if self.board[r][c] is None]
        if free_corners:
            return random.choice(free_corners)

        return self.get_random_move()

    
    # Victory / draw
    

    def check_end_after_move(self):
        winner, cells = self.check_winner()

        if winner:
            self.game_over = True
            self.winning_cells = cells
            self.highlight_winner()
            self.draw_win_line(cells)

            # Uploading score by symbol (X or O)
            if winner in self.scores:
                self.scores[winner] += 1
                self.update_score_labels()
                self.save_scores()

            # Text of status
            if self.vs_computer:
                if winner == self.player_symbol:
                    text = f"You ({winner}) win!"
                else:
                    text = f"Computer ({winner}) wins!"
            else:
                text = f"Player {winner} wins!"

            self.status_label.config(text=text)
            self.disable_all_buttons()
            return True

        if self.is_draw():
            self.game_over = True
            self.status_label.config(text="Draw!")
            # uploading draws
            self.scores["draws"] += 1
            self.update_score_labels()
            self.save_scores()
            self.disable_all_buttons()
            return True

        return False

    def check_winner(self):
        # lines
        for r in range(BOARD_SIZE):
            if (
                self.board[r][0]
                and self.board[r][0] == self.board[r][1] == self.board[r][2]
            ):
                return self.board[r][0], [(r, 0), (r, 1), (r, 2)]

        # columns
        for c in range(BOARD_SIZE):
            if (
                self.board[0][c]
                and self.board[0][c] == self.board[1][c] == self.board[2][c]
            ):
                return self.board[0][c], [(0, c), (1, c), (2, c)]

        # diagonals
        if (
            self.board[0][0]
            and self.board[0][0] == self.board[1][1] == self.board[2][2]
        ):
            return self.board[0][0], [(0, 0), (1, 1), (2, 2)]

        if (
            self.board[0][2]
            and self.board[0][2] == self.board[1][1] == self.board[2][0]
        ):
            return self.board[0][2], [(0, 2), (1, 1), (2, 0)]

        return None, []

    def is_draw(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] is None:
                    return False
        return self.check_winner()[0] is None

    
    # visuality
    

    def draw_win_line(self, cells):
        (r1, c1) = cells[0]
        (r2, c2) = cells[-1]

        CELL = 100
        OFFSET = 50

        x1 = c1 * CELL + OFFSET
        y1 = r1 * CELL + OFFSET
        x2 = c2 * CELL + OFFSET
        y2 = r2 * CELL + OFFSET

        self.canvas.create_line(
            x1, y1, x2, y2,
            fill="#00E0FF", width=8,
            capstyle="round", tags="win_line"
        )

    def highlight_winner(self):
        for r, c in self.winning_cells:
            self.buttons[r][c].config(bg=WIN_HIGHLIGHT_BG)

    def update_turn_text(self):
        if self.vs_computer:
            if self.current_player == self.player_symbol:
                self.status_label.config(text=f"Your turn ({self.player_symbol})")
            else:
                self.status_label.config(text=f"Computer's turn ({self.computer_symbol})")
        else:
            self.status_label.config(text=f"Player {self.current_player}'s turn")

    def disable_all_buttons(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c].config(
                    state="disabled",
                    disabledforeground=BTN_FG,
                    bg=BTN_DISABLED_BG,
                )

    def reset_game(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.game_over = False
        self.winning_cells = []

        if self.vs_computer:
            self.player_symbol = self.symbol_var.get()
            self.computer_symbol = "O" if self.player_symbol == "X" else "X"
            self.current_player = self.player_symbol
        else:
            self.player_symbol = "X"
            self.computer_symbol = "O"
            self.current_player = "X"

        self.canvas.delete("win_line")

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c].config(text="", state="normal", bg=BTN_BG)

        self.update_turn_text()
        self.update_score_labels()

        if self.vs_computer and self.player_symbol == "O":
            self.current_player = self.computer_symbol
            self.update_turn_text()
            self.root.after(300, self.computer_move)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
