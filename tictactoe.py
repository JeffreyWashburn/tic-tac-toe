import tkinter
from tkinter import ttk
from functools import partial # <-- package a function and its arguments
from random import choice

class App(ttk.Frame):
    def __init__(self, master):
        # call the ttk frame constructor
        super().__init__(master)

        # instantiate, configure and grid ttk widgets
        self.create_widgets()
        self.configure_widgets()
        self.grid_widgets()
        self.configure_grid()
        
        # initialize the variables needed for tic tac toe game
        self.make_board()

    def make_board(self):
        self.winner = None

        # keys are 'rows' and values are lists of 'columns'
        # each column contains its associated button object and its state
        self.board = {
            0: [[self.btn_tl, None], [self.btn_tm, None], [self.btn_tr, None]],
            1: [[self.btn_ml, None], [self.btn_mm, None], [self.btn_mr, None]],
            2: [[self.btn_bl, None], [self.btn_bm, None], [self.btn_br, None]]
        }

        # list of tuples to keep track of available positions (row, column)
        self.available_positions = []
        for row in range(3):
            for column in range(3):
                self.available_positions.append((row, column))

    def reset(self):
        """set everything back to default and erase button texts
        so we can play a new game
        """

        self.make_board()

        # configure each buttons text option to an empty string
        for row in range(3):
            for column in range(3):
                self.board[row][column][0]['text'] = ''
    
    def check_winner(self, row, column, symbol):
        """Call below helpers to check for win conditions
        """
        self.check_row(row, symbol)
        self.check_column(column, symbol)
        self.check_diag(row, column, symbol)

    def play(self, symbol, pos):
        """Called when a button is clicked. Mark a button and computer makes a 
        move, check for win
        """

        # player tries to click a button when game is over
        if self.winner is not None:
            print("Game over")
            return

        # unpack the row and column from the pos     
        row, column = pos

        # if the requested position is available, mark and check for a win
        if self.available_positions:
            if (row, column) in self.available_positions:
                self.mark(symbol, row, column)
                self.available_positions.remove((row, column))
                self.check_winner(row, column, 'x')
            else:
                return
            if self.winner == 'x':
                print('Win')
                return

        # same as above, if the player did not already win
        if self.available_positions:
            row, column = choice(self.available_positions)
            self.mark('o', row, column)
            self.available_positions.remove((row, column))
            self.check_winner(row, column, 'o')
        if self.winner == 'o':
            print('Loose')
            return

    def mark(self, symbol, row, column):
        """Called by .play()
        """

        # check if position is available and place a symbol
        if self.available_positions:
            # place symbol in self.board
            self.board[row][column][1] = symbol
            # configure button widget text option to symbol
            self.board[row][column][0]['text'] = symbol

    def check_row(self, row, symbol):
        """Count the number of symbol occurrences in a row
        """

        tally = 0
        for column in range(3):
            if self.board[row][column][1] == symbol:
                tally += 1
        if tally == 3:
            self.winner = symbol

    def check_column(self, column, symbol):
        """Count the number of symbol occurrences in a column
        """

        tally = 0
        for row in range(3):
            if self.board[row][column][1] == symbol:
                tally += 1
        if tally == 3:
            self.winner = symbol

    def check_diag(self, row, column, symbol):
        """Count symbols occurring in either of the two diagonal patterns
        """

        # get the current state of buttons..
        # tl -> top left; mm -> middle middle; etc...
        tl = self.board[0][0][1]
        mm = self.board[1][1][1]
        br = self.board[2][2][1]
        bl = self.board[0][2][1]
        tr = self.board[0][2][1]

        # we know if mm isn't on then we can return early
        if mm == symbol:
            if tl == symbol and br == symbol:
                self.winner = symbol
                return
            if tr == symbol and bl == symbol:
                self.winner = symbol
                return
            else:
                return
        else:
            return

    def create_widgets(self):
        """Instantiate the button widgets, passing self as the master
        """

        # we pass self since 'self' is a ttk frame
        # the tic tac toe buttons
        self.btn_tl = ttk.Button(self)
        self.btn_tm = ttk.Button(self)
        self.btn_tr = ttk.Button(self)
        self.btn_ml = ttk.Button(self)
        self.btn_mm = ttk.Button(self)
        self.btn_mr = ttk.Button(self)
        self.btn_bl = ttk.Button(self)
        self.btn_bm = ttk.Button(self)
        self.btn_br = ttk.Button(self)

        # the reset button
        self.btn_reset = ttk.Button(self)

    def configure_widgets(self):
        """Set the ttk configuration options for our widgets
        """

        # 'command' - callback function executed when button is pressed
        # since we can't pass it a function with arguments, we use the partial 
        # function from the functools module
        self.btn_tl['command'] = partial(self.play, "x", (0,0))
        self.btn_tm['command'] = partial(self.play, "x", (0,1))
        self.btn_tr['command'] = partial(self.play, "x", (0,2))
        self.btn_ml['command'] = partial(self.play, "x", (1,0))
        self.btn_mm['command'] = partial(self.play, "x", (1,1))
        self.btn_mr['command'] = partial(self.play, "x", (1,2))
        self.btn_bl['command'] = partial(self.play, "x", (2,0))
        self.btn_bm['command'] = partial(self.play, "x", (2,1))
        self.btn_br['command'] = partial(self.play, "x", (2,2))

        self.btn_reset['text'] = "Reset"
        self.btn_reset['command'] = self.reset

    def grid_widgets(self):
        """Use the tk grid geometry manager to place widgets into window
        """

        # we must first make sure we grid self, since self is the frame
        # that the other widgets are slave to
        self.grid(row=0, column=0, sticky="nsew")

        # grid in the other widgets
        self.btn_tl.grid(row=0, column=0, sticky="nsew")
        self.btn_tm.grid(row=0, column=1, sticky="nsew")
        self.btn_tr.grid(row=0, column=2, sticky="nsew")
        self.btn_ml.grid(row=1, column=0, sticky="nsew")
        self.btn_mm.grid(row=1, column=1, sticky="nsew")
        self.btn_mr.grid(row=1, column=2, sticky="nsew")
        self.btn_bl.grid(row=2, column=0, sticky="nsew")
        self.btn_bm.grid(row=2, column=1, sticky="nsew")
        self.btn_br.grid(row=2, column=2, sticky="nsew")

        self.btn_reset.grid(row=3, column=0, columnspan=3, sticky="nsew")

    def configure_grid(self):
        """Call gridconfigure and rowconfiugre on the widgets so they can be
        resized
        """

        for r in range(3):
            self.rowconfigure(r, weight=1)
        for c in range(3):
            self.columnconfigure(c, weight=1)

def play():
    """Program entry point
    """
    root = tkinter.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    window = App(root)
    window.mainloop()

if __name__ == "__main__":
    play()