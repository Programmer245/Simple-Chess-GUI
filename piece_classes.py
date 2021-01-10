'''Simple Chess Piece Class Module'''

from global_vars import * # Imports some behavioral constants

import tkinter
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

    def __init__(self, side, position, parent):
        '''
        Init method for Piece class

        Takes side of piece (black or white)
        Takes initial position of piece (string of format colrow)
        Takes parent widget where pieces will be displayed
        '''

        Piece.piece_instances.append(self) # Adds the instance to the list of piece instances

        self.side = side # Specifies the side the piece is on (black or white)
        self.position = position # Specifies the position of the piece on the board as string of 2 digits indicating the column as row such as 02 (column 0 row 2)
        self.parent = parent # Specifies the parent GUI
        self.canvas = parent.chess_board # Canvas where piece will be displayed

        self.text_object_id = self.canvas.create_text((0.5+int(self.position[0]))*SQUARE_SIZE, (0.5+int(self.position[1]))*SQUARE_SIZE, text=Piece.piece_unicode_identifiers[self.identifier][self.side], font=('System', 55, 'bold')) # Stores the canvas text instance representing the piece
        
        self.canvas.tag_bind(self.text_object_id, '<B1-Motion>', self.__moved) # Binds all pieces in the canvas to the moved method when the mouse is held and moved
        self.canvas.tag_bind(self.text_object_id, '<Button-1>', self.__clicked) # Binds all pieces in the canvas to the clicked method when the mouse is clicked
        self.canvas.tag_bind(self.text_object_id, '<ButtonRelease-1>', self.__released) # Binds all pieces in the canvas to the selected method when the mouse is released

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
            else:
                print('King is checked')
                return False
        
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

    def adjust(self):
        'Adjusts some attributes after a successful move'

        if Pawn.operators_dictionary[Piece.piece_opposites[self.side]](int(self.position[1]), 4) == 4: # Pawn has reached end of the board
                self.promote() # Promote the pawn

        if self.position == f'{self.old_position[0]}{self.operator_fun(int(self.old_position[1]), 2)}': # If pawn pushed twice
            self.en_passant = True # En passant enabled for the pawn

        self.moved = True # Piece has been moved

    def promote(self):
        'Promotes a pawn instance to another piece; takes piece class as argument'

        self.parent.chess_board.config(state=tkinter.DISABLED) # Disables the canvas
        self.parent.promoted_pawn = self # Indicates which pawn is going to be promoted by storing it as an attribute of the Game class

        for button in self.parent.promotion_button_list:
            button.config(state=tkinter.NORMAL) # Enables all the promotion buttons
        
    def selected_promote(self, piece_class):
        'Secondary method to promote() that takes class of piece to promote pawn to as argument'

        self.parent.chess_board.config(state=tkinter.NORMAL) # Enables the canvas
        
        for button in self.parent.promotion_button_list:
            button.config(state=tkinter.DISABLED) # Disables all the promotion buttons

        self.canvas.delete(self.text_object_id) # Deletes itself from board
        Piece.piece_instances.remove(self) # Removes itself from list of pieces on the board        

        piece_class(self.side, self.position, self.parent) # Creates new piece by promoting the pawn

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
        self.moved = False # Flag indicating whether piece has moved
        super().__init__(side, position, canvas) # Inherits the parent class attributes

    def in_range(self, initial, final):
        '''Returns True for possible move, False for impossible move, or instance of captured piece
        
        Takes initial and final square position as arguments'''

        horizontal_diff = int(final[0])-int(initial[0]) # Stores the difference between initial and final x
        vertical_diff = int(final[1])-int(initial[1]) # Stores the difference between initial and final y

        if horizontal_diff == 0 or vertical_diff == 0: # If final square is on the same row/column as the rook
            if horizontal_diff == 0: # If final square is in same column
                operator_fun = operator.add if int(final[1]) > int(initial[1]) else operator.sub # Stores the appropriate operator depending on the circumstance
                for i in range(1, abs(vertical_diff)): # Finds every square on the appropriate column up to the target square
                    intermediate_pos = f'{initial[0]}{operator_fun(int(initial[1]), i)}'

                    for piece in Piece.piece_instances: # Checks all pieces
                        if piece != self and piece.position == intermediate_pos: # If any piece is in the way of bishop
                            return False # Square is blocked and cannot be reached

            elif vertical_diff == 0: # If final square is in same row
                operator_fun = operator.add if int(final[0]) > int(initial[0]) else operator.sub # Stores the appropriate operator depending on the circumstance
                for i in range(1, abs(horizontal_diff)): # Finds every square on the appropriate row up to the target square
                    intermediate_pos = f'{operator_fun(int(initial[0]), i)}{initial[1]}'

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

    def in_range(self, initial, final):
        '''Returns True for possible move, False for impossible move, or instance of captured piece
        
        Takes initial and final square position as arguments; inherits linear and diagonal movement from rook and bishop'''

        # Queen inherits movement from both the rook and the bishop

        linear_movement = Rook.in_range(self, initial, final) # Stores return value of possible horizontal movement for the queen
        diagonal_movement = Bishop.in_range(self, initial, final) # Stores return value of possible diagonal movement for the queen

        if linear_movement: # If returns True or instance of captured piece from linear movement inherited from rook
            return linear_movement
        elif diagonal_movement: # If returns True or instance of captured piece from diagonal movement inherited from bishop
            return diagonal_movement
        
        return False # Unreachable square

class King(Piece):
    'Child class that creates instances of kings'

    def __init__(self, side, position, canvas):
        self.identifier = 'K' # Identifier used for chess notation and to assign a unicode sequence to each piece
        self.moved = False # Flag indicating whether piece has moved
        super().__init__(side, position, canvas) # Inherits the parent class attributes

    def in_range(self, initial, final):
        '''Returns True for possible move, False for impossible move, or instance of captured piece
        
        Takes initial and final square position as arguments'''

        if abs(int(final[0])-int(initial[0])) in (0, 1) and abs(int(final[1])-int(initial[1])) in (0, 1): # If final square is around king
            for piece in Piece.piece_instances: # Checks all the pieces
                if piece != self and piece.position == final: # Square is blocked by another piece
                    if self.side == piece.side: # Square blocked by friendly piece
                        return False
                    else:
                        return piece # Enemy piece can be captured
            return True # Square is empty

        elif abs(int(final[0])-int(initial[0])) == 2 and int(final[1])-int(initial[1]) == 0: # King tries to castle
            if not self.moved and not self.checked(self.side, Piece.piece_instances): # If king hasn't moved and it is not in check

                rooks = [] # List containing all the rooks that have not moved
                for piece in Piece.piece_instances:
                    if piece.identifier == 'R' and not piece.moved: # Looks for rooks that have not moved
                        rooks.append(piece) # Appends the rook to the list of rooks

                ### WHITE KING LOGIC

                if self.side == 'white': 
                    if self.position == '27': # White king tries to long castle
                        self.castled_rook = None # No rook to castle with has been found
                        for rook in rooks: # Looks through list of rooks
                            if rook.position == '07' and self.side == rook.side: # If friendly rook's position is correct
                                self.castled_rook = rook # Stores rook instance
                        if not self.castled_rook: # No rook to castle with has been found
                            return False

                        for piece in Piece.piece_instances:
                            if piece == self: # Skips itself
                                continue
                            elif piece.position == '17' or piece.position == '27' or piece.position == '37': # Piece is in the way of long castle
                                print('Piece in the way of long castle')
                                return False 
                            elif self.side != piece.side and (piece.in_range(piece.position, '27') or piece.in_range(piece.position, '37')): # Piece threatens a square between long castle
                                print('Piece threatens long castle')
                                return False

                    elif self.position == '67': # White king tries to short castle
                        self.castled_rook = None # No rook to castle with has been found
                        for rook in rooks: # Looks through list of rooks
                            if rook.position == '77' and self.side == rook.side: # If friendly rook's position is correct
                                self.castled_rook = rook # Stores rook instance
                        if not self.castled_rook: # No rook to castle with has been found
                            return False

                        for piece in Piece.piece_instances:
                            if piece == self: # Skips itself
                                continue
                            elif piece.position == '57' or piece.position == '67': # Piece is in the way of long castle
                                print('Piece in the way')
                                return False 
                            elif self.side != piece.side and (piece.in_range(piece.position, '57') or piece.in_range(piece.position, '67')): # Piece threatens a square between long castle
                                print('Piece threatens short castle')
                                print(f'In the way at {piece.position}')
                                return False

                ### BLACK KING LOGIC

                else: 
                    if self.position == '20': # Black king tries to long castle
                        self.castled_rook = None # No rook to castle with has been found
                        for rook in rooks: # Looks through list of rooks
                            if rook.position == '00' and self.side == rook.side: # If friendly rook's position is correct
                                self.castled_rook = rook # Stores rook instance
                        if not self.castled_rook: # No rook to castle with has been found
                            return False

                        for piece in Piece.piece_instances:
                            if piece == self: # Skips itself
                                continue
                            elif piece.position == '10' or piece.position == '20' or piece.position == '30': # Piece is in the way of long castle
                                print('Piece in the way of long castle')
                                return False 
                            elif self.side != piece.side and (piece.in_range(piece.position, '20') or piece.in_range(piece.position, '30')): # Piece threatens a square between long castle
                                print('Piece threatens long castle')
                                return False

                    elif self.position == '60': # Black king tries to short castle
                        self.castled_rook = None # No rook to castle with has been found
                        for rook in rooks: # Looks through list of rooks
                            if rook.position == '70' and self.side == rook.side: # If friendly rook's position is correct
                                self.castled_rook = rook # Stores rook instance
                        if not self.castled_rook: # No rook to castle with has been found
                            return False

                        for piece in Piece.piece_instances:
                            if piece == self: # Skips itself
                                continue
                            elif piece.position == '50' or piece.position == '60': # Piece is in the way of long castle
                                print('Piece in the way')
                                return False 
                            elif self.side != piece.side and (piece.in_range(piece.position, '50') or piece.in_range(piece.position, '60')): # Piece threatens a square between long castle
                                print('Piece threatens short castle')
                                print(f'In the way at {piece.position}')
                                return False

            pieces_copy = copy.copy(Piece.piece_instances) # Makes a copy of the piece instances

            for piece in pieces_copy:
                if piece.position == self.castled_rook.position and piece != self and self.side == piece.side and piece.identifier == 'R': # Searches for correct rook
                    if self.position == '27': # White king long castle
                        piece.position = '37' # Updates position of rook after castling
                    elif self.position == '67': # White king short castle
                        piece.position = '57' # Updates position of rook after castling
                    elif self.position == '20': # Black king long castle
                        piece.position = '30'
                    elif self.position == '60': # Black king short castle
                        piece.position = '50'

            if not self.checked(self.side, pieces_copy): # If king will not be checked after castling, it is a valid move
                print('Valid castling move')
                return True

        return False # Unreachable square

    def adjust(self):
        'Adjusts some attributes after a successful move'

        if abs(int(self.position[0])-int(self.old_position[0])) == 2 and int(self.position[1])-int(self.old_position[1]) == 0: # King has castled
            if self.position == '27': # White king long castle
                self.castled_rook.position = '37' # Updates position of rook after castling
            elif self.position == '67': # White king short castle
                self.castled_rook.position = '57' # Updates position of rook after castling
            elif self.position == '20': # Black king long castle
                self.castled_rook.position = '30'
            elif self.position == '60': # Black king short castle
                self.castled_rook.position = '50'

            self.canvas.coords(self.castled_rook.text_object_id, (0.5+int(self.castled_rook.position[0]))*80, (0.5+int(self.castled_rook.position[1]))*80)

    @staticmethod
    def checked(side, environment=Piece.piece_instances):
        '''Returns True or False if king of color side is being checked
        
        Environment argument is list of pieces being examined. Default argument can be overwritten'''

        for piece in environment: 
            if piece.identifier == 'K' and piece.side == side: 
                king_position = piece.position # Stores position of king

        for piece in environment:
            if side != piece.side: # Searches every enemy piece
                if piece.in_range(piece.position, king_position): # If piece can 'capture' the king then it is in check
                    print(piece.in_range(piece.position, king_position))
                    print(piece.position, piece.identifier)
                    return True
        print('King is not checked')
        return False # King is not in range of any piece and is not checked