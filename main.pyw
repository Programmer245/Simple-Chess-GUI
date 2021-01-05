'''Simple Chess Main Module'''

import tkinter

from piece_classes import * # Imports all the piece classes (including constants.py)

from PIL import ImageTk, Image # Image processing library

### DEFINING THE ROOT (MUST BE DEFINED BEFORE PHOTOIMAGE OBJECT IS CREATED)

root = tkinter.Tk() # Defines main window
root.title('Simple Chess') # Sets window title
root.iconbitmap(r'resources/chess_icon.ico') # Sets window icon
root.resizable('False', 'False') # Disables window resizing

chess_img = Image.open(r'resources\chess_img.png') # Opens the image
chess_img = chess_img.resize((150, 150), Image.ANTIALIAS) # Resizes the opened photo before converting it into a PhotoImage
chess_img = ImageTk.PhotoImage(chess_img) # Converts image into a PhotoImage

reset_arrow = Image.open(r'resources\reset_arrow.png')
reset_arrow = reset_arrow.resize((90, 70), Image.ANTIALIAS)
reset_arrow = ImageTk.PhotoImage(reset_arrow)

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
        self.imageLabel = tkinter.Label(self.right_frame, image=chess_img, relief='solid', bd=2, bg='yellow') # Label with the image
        self.move_tracker = tkinter.Listbox(self.right_frame, selectmode=tkinter.SINGLE, width=40, height=23) # Chess move tracker
        self.reset_button = tkinter.Button(self.right_frame, image=reset_arrow, relief='flat', state=tkinter.DISABLED, command=self.__reset) # Reset button
        self.win_label = tkinter.Label(self.right_frame, text='White wins by checkmate') # Label that displays who has won the game

        self.right_frame.grid(row=0, column=1)
        self.imageLabel.grid(row=0, column=0, columnspan=2, pady=(10,0))
        self.move_tracker.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.reset_button.grid(row=2, column=1)
        self.win_label.grid(row=3, column=0, columnspan=2, pady=(0,10))

        ### ### PROMOTION BUTTONS LABEL FRAME
        self.promotion_buttons_frame = tkinter.LabelFrame(self.right_frame, text='Promotion') # Promotion button label frame containing all the promotion buttons
        self.knight_promotion_btn = tkinter.Button(self.promotion_buttons_frame, text='\u2654', font=('Helvetica', 15, 'bold'), state=tkinter.DISABLED)
        self.bishop_promotion_btn = tkinter.Button(self.promotion_buttons_frame, text='\u2657', font=('Helvetica', 15, 'bold'), state=tkinter.DISABLED)
        self.rook_promotion_btn = tkinter.Button(self.promotion_buttons_frame, text='\u2656', font=('Helvetica', 15, 'bold'), state=tkinter.DISABLED)
        self.queen_promotion_btn = tkinter.Button(self.promotion_buttons_frame, text='\u2655', font=('Helvetica', 15, 'bold'), state=tkinter.DISABLED)

        self.promotion_buttons_frame.grid(row=2, column=0, pady=(0,10))
        self.knight_promotion_btn.grid(row=0, column=0)
        self.bishop_promotion_btn.grid(row=0, column=1)
        self.rook_promotion_btn.grid(row=1, column=0)
        self.queen_promotion_btn.grid(row=1, column=1)

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

    def __reset(self):
        'Resets the game'

        pass

### WINDOW INSTANCE CREATED

Game(root) # Creates window

tkinter.mainloop()