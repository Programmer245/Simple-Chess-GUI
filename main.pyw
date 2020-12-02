'''Simple Chess Main Module'''

import tkinter

class Game:
    'Creates the entire game'

    def __init__(self, parent):
        self.parent = parent # Sets the parent window

        self.board_size = 640 # Sets the board size
        self.square_size = self.board_size/8 # Sets the chess square size

        # self.pieces = ['\u2654', '\u2655', '\u2656', '\u2657', '\u2658', '\u2659', '\u265A', '\u265B', '\u265C', '\u265D', '\u265E', '\u265F']

        self.__widgets()
        self.__draw_board()

    ### PACKING WIDGETS

    def __widgets(self):
        'Initiates the widgets'

        ### LEFT FRAME

        self.left_frame = tkinter.Frame(self.parent, bg='lightblue', width=300, height=300)
        self.chess_board = tkinter.Canvas(self.left_frame, width=self.board_size, height=self.board_size, highlightthickness=0, highlightbackground='black') # Creates the chess board
        self.top_summary = tkinter.Label(self.left_frame, text='TestingTop') # Shows all captured enemy pieces
        self.bottom_summary = tkinter.Label(self.left_frame, text='TestingBottom')

        self.left_frame.grid(row=0, column=0)
        self.chess_board.grid(row=1, column=0, padx=20) # Adds some spacing with the outside of the frame
        self.top_summary.grid(row=0, column=0, padx=20, pady=5, sticky='w') # Left centred in frame
        self.bottom_summary.grid(row=2, column=0, padx=20, pady=5, sticky='e') # Right centred in frame

        ### RIGHT FRAME

        self.right_frame = tkinter.Frame(self.parent, bg='lightpink', width=300, height=300)

        self.right_frame.grid(row=0, column=1)

    def __draw_board(self):
        'Draws the chess board'

        for row in range(8):
            for column in range(8):
                if (row+column+1) % 2 == 0: # Draws alternating black squares
                    self.chess_board.create_rectangle(self.square_size*column, self.square_size*row, self.square_size*column + self.square_size, self.square_size*row + self.square_size, fill='green', outline='') # Creates the squares 

root = tkinter.Tk() # Defines main window
root.title('Simple Chess') # Sets window title
root.iconbitmap(r'resources/chess_icon.ico') # Sets window icon
root.resizable('False', 'False') # Disables window resizing

Game(root) # Creates window

tkinter.mainloop()