'''Simple Chess Piece Class Module'''

from global_vars import * # Imports some behavioral constants

import operator # Used for piece movement behavior

import copy # Used for saving state of piece instances

class Piece:
    'Parent class that defines the general behavior of all chess pieces'

    allowed = 'white' # Indicates which side is allowed to make a move

    piece_opposites = {
            'black': 'white',
            'white': 'black'
            }

    piece_unicode_identifiers = {
            '': {'black': '\u265F', 'white': '\u2659'}, 
            'R': {'black': '\u265C', 'white': '\u2656'}, 
            'N': {'black': '\u265E', 'white': '\u2658'}, 
            'B': {'black': '\u265D', 'white': '\u2657'}, 
            'Q': {'black': '\u265B', 'white': '\u2655'}, 
            'K': {'black': '\u265A', 'white': '\u2654'}
            } # Stores all the chess pieces and their unicode symbols

    piece_instances = [] # Stores all the piece instances

    def __init__(self, side, position, canvas):

        Piece.piece_instances.append(self) # Adds the instance to the list of piece instances

        self.side = side # Specifies the side the piece is on (black or white)
        self.position = position # Specifies the position of the piece on the board as string of 2 digits indicating the column as row such as 02 (column 0 row 2)
        self.canvas = canvas # Canvas where piece will be displayed

        self.text_object_id = self.canvas.create_text((0.5+int(self.position[0]))*SQUARE_SIZE, (0.5+int(self.position[1]))*SQUARE_SIZE, text=Piece.piece_unicode_identifiers[self.identifier][self.side], font=('System', 55, 'bold')) # Stores the canvas text instance representing the piece
        
        canvas.tag_bind(self.text_object_id, '<B1-Motion>', self.__moved) # Binds all pieces in the canvas to the moved method when the mouse is held and moved
        canvas.tag_bind(self.text_object_id, '<Button-1>', self.__clicked) # Binds all pieces in the canvas to the clicked method when the mouse is clicked
        canvas.tag_bind(self.text_object_id, '<ButtonRelease-1>', self.__released) # Binds all pieces in the canvas to the selected method when the mouse is released

    def __moved(self, event):
        'Handles piece being dragged across board'

        try:
            temp = f'{event.x//80}{event.y//80}' # Temporary variable storing the piece position
            
            if '-1' in temp or event.x > BOARD_SIZE or event.y > BOARD_SIZE: # Exception is raised if piece is outside of board boundaries
                raise ValueError 

            # If program gets to this point, then piece is still inside the board

            if self.position != temp: # Piece has been moved to a different square
                self.position = temp # Updates position
                self.canvas.delete(self.highlight_box) # Deletes previous highlight box
                self.__create_highlight_box() # Creates new highlight box in new square
        except ValueError: # Piece is outside board
            print('Invalid position')
        finally: # Regardless of whether piece is outside board or not
            print(self.position) # Prints out the square the piece is currently on

            self.canvas.coords(self.text_object_id, event.x, event.y) # Allows piece to be moved by repositioning it on the canvas as mouse moves around

    def __clicked(self, event):
        'Handles piece being selected prior to being dragged'

        self.old_position = self.position # Stores the old piece position
        self.__create_highlight_box() # Creates the highlight box

    def __released(self, event):
        'Handles releasing a piece'

        print('Released')

        self.canvas.delete(self.highlight_box) # Deletes the previous highlight box

        return_value = self.__possible_move(event) # Stores return value which may be True, False, or instance of captured piece

        if not return_value: # If the move is invalid
            self.position = self.old_position # Resets the position of the piece
        else: # Move is valid and reveal check does not occur
            Pawn.disable_en_passant() # Disables en passant for all pawns

            if 'adjust' in dir(self): # If instance has method adjust
                self.adjust() # Adjusts attributes

            if isinstance(return_value, Piece): # If a piece has been captured
                self.canvas.delete(return_value.text_object_id) # Deletes captured piece from board
                Piece.piece_instances.remove(return_value) # Removes captured piece from list of pieces on the board

            Piece.allowed = Piece.piece_opposites[Piece.allowed] # Updates the side that is allowed to make a move
            
        # If code does not go into if statement above, the move is legal and the position of the piece does not get reset
        self.canvas.coords(self.text_object_id, (0.5+int(self.position[0]))*80, (0.5+int(self.position[1]))*80) # When piece is released, it gets placed in the middle of the square automatically

    def __create_highlight_box(self):
        'Creates a highlight box around the square the piece is currently on'

        self.highlight_box = self.canvas.create_rectangle(SQUARE_SIZE*int(self.position[0]), SQUARE_SIZE*int(self.position[1]), SQUARE_SIZE*int(self.position[0]) + SQUARE_SIZE, SQUARE_SIZE*int(self.position[1]) + SQUARE_SIZE, fill='', outline='blue', width=2) # Creates the highlight box over the square the selected piece is hovering on

    def __possible_move(self, event):
        'Returns True or False depending on whether a move is legal or not'

        if event.x < 0 or event.x > BOARD_SIZE or event.y < 0 or event.y > BOARD_SIZE: # If piece is outside board it is an invalid move
            return False 

        if self.side != Piece.allowed or self.position == self.old_position: # If player makes a move outside their turn or the piece is not moved to any new square it is an invalid move
            return False

        # If gets to this point, piece has been released inside chess board

        pieces_copy = copy.copy(Piece.piece_instances) # Makes a copy of piece instances

        return_value = self.in_range(self.old_position, self.position) # Stores return value which may be True, False, or instance of captured piece

        if not return_value: # Square cannot be reached
            return False
        else: # Square can be reached
            if isinstance(return_value, Piece): # If a piece can be captured by move
                pieces_copy.remove(return_value) # Removes the piece from the pieces_copy temporary environment
            if not King.checked(self.side, pieces_copy): # If reveal check does not occur value is returned
                return return_value
        
class Pawn(Piece):
    'Child class that creates instances of pawns'

    operators_dictionary = {
            'white': operator.sub,
            'black': operator.add
            } # Stores arithmetic functions used in calculating pawn movement ranges

    def __init__(self, side, position, canvas):
        self.identifier = '' # Identifier used for chess notation and to assign a unicode sequence to each piece
        self.moved = False # Flag indicating whether piece has moved
        self.en_passant = False # Flag indicating whether en passant can be done on the piece
        super().__init__(side, position, canvas) # Inherits the parent class attributes

    def in_range(self, initial, final):
        '''Returns True for possible move, False for impossible move, or instance of captured piece
        
        Takes initial and final square position as arguments'''

        self.operator_fun = Pawn.operators_dictionary[self.side] # Stores the correct arithmetic function for the respective pawn being moved

        if not self.moved and final == f'{initial[0]}{self.operator_fun(int(initial[1]), 2)}': # If the pawn has not moved before and it is pushed twice
                for piece in Piece.piece_instances: # Checks all the pieces
                    if piece == self: # Skips itself
                        continue
                    elif piece.position == final or piece.position == f'{initial[0]}{self.operator_fun(int(initial[1]), 1)}': # Path is blocked by another piece
                        return False 
                return True # Move can be made

        elif final == f'{initial[0]}{self.operator_fun(int(initial[1]), 1)}': # If pawn if pushed up
            for piece in Piece.piece_instances: # Checks all the pieces
                if piece == self: # Skips itself
                    continue
                elif piece.position == final: # Square is blocked by another piece
                    return False 
            return True # Square is empty

        elif final == f'{int(initial[0])-1}{self.operator_fun(int(initial[1]), 1)}' or final == f'{int(initial[0])+1}{self.operator_fun(int(initial[1]), 1)}': # If pawn tries to take another piece directly or by en passant
            for piece in Piece.piece_instances: # Checks all the pieces
                if piece == self or self.side == piece.side: # Skips itself or any friendly piece
                    continue
                elif piece.position == final or (piece.position == f'{final[0]}{initial[1]}' and not piece.identifier and piece.en_passant): # An enemy piece is on the diagonal square or an enemy pawn is on either side with en passant enabled
                    return piece # Enemy piece can be captured
            # If gets to this point, there is no piece that can be captured and en passant cannot be done
            
        return False # Unreachable square

    def promote(self, piece_class):
        'Promotes a pawn instance to another piece; takes piece class as argument'

        pass

    def adjust(self):
        'Adjusts some attributes after a successful move'

        if Pawn.operators_dictionary[Piece.piece_opposites[self.side]](int(self.position[1]), 4) == 4: # Pawn has reached end of the board
                print('Promote pawn')

        if self.position == f'{self.old_position[0]}{self.operator_fun(int(self.old_position[1]), 2)}': # If pawn pushed twice
            self.en_passant = True # En passant enabled for the pawn

        self.moved = True # Piece has been moved

    @staticmethod
    def disable_en_passant():
        'Disables en passant for all pawns'
        for piece in Piece.piece_instances:
            if not piece.identifier:
                piece.en_passant = False # Disables en passant for all pawns
    
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

    def in_range(self, initial, final):
        '''Returns True for possible move, False for impossible move, or instance of captured piece
        
        Takes initial and final square position as arguments'''

        if (abs(int(final[0])-int(initial[0])) == 1 and abs(int(final[1])-int(initial[1])) == 2) or (abs(int(final[0])-int(initial[0])) == 2 and abs(int(final[1])-int(initial[1])) == 1): # If knight moves in an L shape
            for piece in Piece.piece_instances: # Checks all the pieces
                if piece != self and piece.position == final: # Square is blocked by another piece
                    if self.side == piece.side: # Square blocked by friendly piece
                        return False
                    else:
                        return piece # Enemy piece can be captured
            return True # Square is empty

        return False # Unreachable square

class Bishop(Piece):
    'Child class that creates instances of bishops'

    def __init__(self, side, position, canvas):
        self.identifier = 'B' # Identifier used for chess notation and to assign a unicode sequence to each piece
        super().__init__(side, position, canvas) # Inherits the parent class attributes

    def in_range(self, initial, final):
        '''Returns True for possible move, False for impossible move, or instance of captured piece
        
        Takes initial and final square position as arguments'''

        if abs(int(final[0])-int(initial[0])) == abs(int(final[1])-int(initial[1])): # If final square is on the same diagonal as the bishop
            horizontal_operator = operator.add if int(final[0]) > int(initial[0]) else operator.sub # Stores the appropriate operator depending on the circumstance
            vertical_operator = operator.add if int(final[1]) > int(initial[1]) else operator.sub
            
            for i in range(1, abs(int(final[0])-int(initial[0]))): # Finds every square on the appropriate diagonal up to the target square
                intermediate_pos = f'{horizontal_operator(int(initial[0]), i)}{vertical_operator(int(initial[1]), i)}'
                
                for piece in Piece.piece_instances: # Checks all pieces
                    if piece != self and piece.position == intermediate_pos: # If any piece is in the way of bishop
                        return False # Square is blocked and cannot be reached

            for piece in Piece.piece_instances: # Checks all the pieces
                if piece != self and piece.position == final: # Square is blocked by another piece
                    if self.side == piece.side: # Square blocked by friendly piece
                        return False
                    else:
                        return piece # Enemy piece can be captured
            return True # Square is empty

        return False # Unreachable square

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

    @staticmethod
    def checked(side, environment=Piece.piece_instances):
        '''Returns True or False if king of color side is being checked
        
        Environment argument is list of pieces being examined. Default argument can be overwritten'''

        return False # Temporary return False

        for piece in environment: 
            if piece.identifier == 'K' and piece.side == side: 
                king_position = piece.position # Stores position of king
                for piece in environment:
                    if piece.identifier != 'K': # Piece must not be a king
                        return_value = piece.in_range(piece.position, king.position)
                        if isinstance(return_value, Piece): # If piece can 'capture' the king then it is in check
                            return True
                return False # King is not in range of any piece and is not checked
