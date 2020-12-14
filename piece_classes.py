'''Simple Chess Piece Class Module'''

from constants import * # Imports the behavioural constants

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

    def __init__(self, side, position, canvas):

        Piece.piece_instances.append(self) # Adds the instance to the list of piece instances

        self.side = side # Specifies the side the piece is on (black or white)
        self.position = position # Specifies the position of the piece on the board as string of 2 digits indicating the column as row such as 02 (column 0 row 2)
        self.canvas = canvas # Stores the canvas where pieces will be drawn for easy reference
        self.captured = False # Flag specifying if the piece has been captured

        self.text_object_id = self.canvas.create_text((0.5+int(self.position[0]))*80, (0.5+int(self.position[1]))*80, text=Piece.piece_dictionary[self.identifier][self.side], font=('System', 55, 'bold')) # Stores the canvas text instance
        canvas.tag_bind(self.text_object_id, '<B1-Motion>', self.__moved) # Binds all pieces in the canvas to the moved method when the mouse is held and moved
        canvas.tag_bind(self.text_object_id, '<Button-1>', self.__create_highlight_box) # Binds all pieces in the canvas to the create highlight box method when the mouse is clicked
        canvas.tag_bind(self.text_object_id, '<ButtonRelease-1>', self.__released) # Binds all pieces in the canvas to the selected method when the mouse is released

    def __moved(self, event):
        'Handles piece being dragged across board'

        old_position = self.position # Stores old piece position
        self.position = f'{event.x//80}{event.y//80}' # Updates position of piece

        if self.position != old_position: # Piece has been moved to a different square
            self.canvas.delete(self.highlight_box) # Deletes previous highlight box
            self.__create_highlight_box() # Creates new highlight box in new square

        self.canvas.coords(self.text_object_id, event.x, event.y) # Allows piece to be moved by repositioning it on the canvas as mouse moves around
        print(self.position)

    def __released(self, event):
        'Handles releasing a piece'

        self.canvas.delete(self.highlight_box) # Deletes the previous highlight box
        self.canvas.coords(self.text_object_id, (0.5+int(self.position[0]))*80, (0.5+int(self.position[1]))*80) # When piece is released, it gets placed in the middle of the square automatically

    def __create_highlight_box(self, event=None):
        'Creates a highlight box around the square the piece is currently on'

        self.highlight_box = self.canvas.create_rectangle(SQUARE_SIZE*int(self.position[0]), SQUARE_SIZE*int(self.position[1]), SQUARE_SIZE*int(self.position[0]) + SQUARE_SIZE, SQUARE_SIZE*int(self.position[1]) + SQUARE_SIZE, fill='', outline='blue', width=2) # Creates the highlight box over the square the selected piece is hovering on

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