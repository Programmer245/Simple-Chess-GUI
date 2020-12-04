'''Simple Chess Main Module'''

import tkinter

### CONSTANTS

BOARD_SIZE = 640 # Sets the board size
SQUARE_SIZE = BOARD_SIZE/8 # Sets the chess square size

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

        for i in range(8):
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

### PIECE CLASSES

class Piece:
    'Parent class that defines the general behaviour of all chess pieces'

    piece_dictionary = {
            '':{'black':'\u265F', 'white':'\u2659'}, 
            'R':{'black':'\u265C', 'white':'\u2656'}, 
            'N':{'black':'\u265E', 'white':'\u2658'}, 
            'B':{'black':'\u265D', 'white':'\u2657'}, 
            'Q':{'black':'\u265B', 'white':'\u2655'}, 
            'K':{'black':'\u265A', 'white':'\u2654'}
            } # Stores all the chess pieces and their unicode symbols

    piece_instances = [] # Stores all the piece instances

    def __init__(self, side, position, canvas): # Canvas argument is canvas where pieces will be drawn
        self.side = side # Specifies the side the piece is on (black or white)
        self.position = position # Specifies the position of the piece on the board as string of 2 digits indicating the column as row such as 02 (column 0 row 2)
        self.captured = False # Flag specifying if the piece has been captured

        Piece.piece_instances.append(self) # Adds the instance to the list of piece instances

        self.draw_piece(canvas) # After each piece instance is created, it is automatically displayed

    def draw_piece(self, canvas):
        'Draws the piece on the board; takes canvas as argument'

        self.text_object_id = canvas.create_text((0.5+int(self.position[0]))*80, (0.5+int(self.position[1]))*80, text=Piece.piece_dictionary[self.identifier][self.side], font=('System', 60, 'bold')) # Stores the canvas text instance

class Pawn(Piece):
    'Child class that creates instances of pawns'

    def __init__(self, side, position, canvas):
        self.identifier = '' # Identifier used for chess notation and to assign a unicode sequence to each piece
        super().__init__(side, position, canvas) # Inherits the parent class attributes
    
class Rook(Piece):
    'Child class that creates instances of rooks'

    def __init__(self, side, position, canvas):
        self.identifier = 'R' # Identifier used for chess notation and to assign a unicode sequence to each piece
        super().__init__(side, position, canvas) # Inherits the parent class attributes

class Knight(Piece):
    'Child class that creates instances of knights'

    def __init__(self, side, position, canvas):
        self.identifier = 'N' # Identifier used for chess notation and to assign a unicode sequence to each piece
        super().__init__(side, position, canvas) # Inherits the parent class attributes

class Bishop(Piece):
    'Child class that creates instances of bishops'

    def __init__(self, side, position, canvas):
        self.identifier = 'B' # Identifier used for chess notation and to assign a unicode sequence to each piece
        super().__init__(side, position, canvas) # Inherits the parent class attributes

class Queen(Piece):
    'Child class that creates instances of queens'

    def __init__(self, side, position, canvas):
        self.identifier = 'Q' # Identifier used for chess notation and to assign a unicode sequence to each piece
        super().__init__(side, position, canvas) # Inherits the parent class attributes

class King(Piece):
    'Child class that creates instances of kings'

    def __init__(self, side, position, canvas):
        self.identifier = 'K' # Identifier used for chess notation and to assign a unicode sequence to each piece
        super().__init__(side, position, canvas) # Inherits the parent class attributes

### WINDOW INSTANCE CREATED

root = tkinter.Tk() # Defines main window
root.title('Simple Chess') # Sets window title
root.iconbitmap(r'resources/chess_icon.ico') # Sets window icon
root.resizable('False', 'False') # Disables window resizing

Game(root) # Creates window

tkinter.mainloop()