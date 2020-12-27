'''Simple Chess Main Module'''

import tkinter
from piece_classes import * # Imports all the piece classes (including constants.py)

### MAIN CLASS

class Game:
    'Creates the entire game'

    def __init__(self, parent):
        self.parent = parent # Sets the parent window

        self.__widgets() # Creates all widgets
        self.__draw_board() # Draws the chess board
        self.__create_pieces() # Creates all the piece instances

    ### PACKING WIDGETS

    def __widgets(self):
        'Initiates the widgets'

        ### LEFT FRAME

        self.left_frame = tkinter.Frame(self.parent, bg='lightblue', width=300, height=300)
        self.chess_board = tkinter.Canvas(self.left_frame, width=BOARD_SIZE, height=BOARD_SIZE, highlightthickness=0, highlightbackground='black') # Creates the chess board
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
                    self.chess_board.create_rectangle(SQUARE_SIZE*column, SQUARE_SIZE*row, SQUARE_SIZE*column + SQUARE_SIZE, SQUARE_SIZE*row + SQUARE_SIZE, fill='green', outline='') # Creates the squares 

    def __create_pieces(self):
        'Creates all chess pieces'

        for i in range(8): # Creates the pawns
            position = f'{i}1'
            Pawn('black', position, self.chess_board)
        for i in range(8):
            position = f'{i}6'
            Pawn('white', position, self.chess_board)
        
        Rook('black', '00', self.chess_board) # Creates the rooks 
        Rook('black', '70', self.chess_board)
        Rook('white', '07', self.chess_board)
        Rook('white', '77', self.chess_board)

        Knight('black', '10', self.chess_board) # Creates the knights
        Knight('black', '60', self.chess_board)
        Knight('white', '17', self.chess_board)
        Knight('white', '67', self.chess_board)

        Bishop('black', '20', self.chess_board) # Creates the bishops
        Bishop('black', '50', self.chess_board)
        Bishop('white', '27', self.chess_board)
        Bishop('white', '57', self.chess_board)

        Queen('black', '30', self.chess_board) # Creates the queens
        Queen('white', '47', self.chess_board)
        
        King('black', '40', self.chess_board) # Creates the kings
        King('white', '37', self.chess_board)

    def __reset_pieces(self):
        'Resets the chess pieces to their original states'

        pass

### WINDOW INSTANCE CREATED

root = tkinter.Tk() # Defines main window
root.title('Simple Chess') # Sets window title
root.iconbitmap(r'resources/chess_icon.ico') # Sets window icon
root.resizable('False', 'False') # Disables window resizing

Game(root) # Creates window

tkinter.mainloop()