ChangeLog:
===

(Every commit has been assigned a version tag)

***

29/11/2020 - v0.1-alpha:

*Added*

+ Set up development environment
+ Created .gitignore file
+ Created Changelog.md
+ Created LICENCE.md
+ Created README.md
+ Added Experimental folder (added to .git/info/exclude)

*Pending*

- Add main module
- Add documentation to README.md file 

/UNSTABLE BUILD/

***

02/12/2020 - v0.2-alpha:

*Added*

+ Resources folder added
+ main.pyw module added 
+ Added class Game
+ Added left and right frames
+ Added chess grid
+ Added empty summary labels that will display the enemy captured pieces

*Pending*

- Need to add all widgets in frames
- Need to add piece logic and classes

/UNSTABLE BUILD/

***

04/12/2020 - v0.3-alpha:

*Added*

+ Added Piece parent class and all other subclasses to define piece behavior
+ Added __create_pieces method for creating all the piece instances
+ Added empty __reset_pieces method for resetting all pieces to their original state
+ Added empty __draw_piece method for redrawing a particular piece 
+ Refactored code

*Pending*

- Need to add all widgets in frames
- Need to add piece logic
- Need to bind mouse actions to pieces

/UNSTABLE BUILD/

***

05/12/2020 - v0.4-alpha:

*Added*

+ Removed __draw_piece method and implemented canvas text creation directly in __init method of Piece class
+ Bound mouse movement events to chess pieces
+ Added __moved method for handling piece movement

*Pending*

- Need to add all widgets in frames
- Need to add piece logic
- Need to create rectangle around square chess piece is in and finish coding __moved method

/UNSTABLE BUILD/

***

06/12/2020 - v0.4.1-alpha:

*Added*

+ Added __selected, __moved, and __released methods to handle different canvas events
+ Highlight box functionality partially implemented

*Pending*

- Need to add all widgets in frames
- Need to add piece logic
- PLEASE REFACTOR CODE, LOGIC IS TERRIBLE
- Separate Piece class and its subclasses from main module

/UNSTABLE BUILD/

***

10/12/2020 - v0.5-alpha:

*Added*

+ Added __create_highlight_box method
+ Refactored code that handles piece movement to improve logic
+ Added submodules constants.py and piece_classes.py to allow each section of code to be more easily modified
+ Updated .gitignore

*Pending*

- Need to add all widgets in frames
- Need to add piece logic
- Review code logic

/UNSTABLE BUILD/

***

14/12/2020 - v0.5.1-alpha:

*Added*

+ When piece is released, it is automatically centred in square

*Pending*

- Need to add all widgets in frames
- Need to add piece logic
- Review code logic
- Need to adjust code for moving piece beyond canvas or outside window

/UNSTABLE BUILD/

***

16/12/2020 - v0.5.2-alpha:

*Added*

+ Added __possible_move method for validating whether a move is possible
+ Added __clicked method for handling when piece is clicked
+ Refactored code
+ __released method now resets the position of the piece if move is illegal

*Pending*

- Need to add all widgets in frames
- Need to add piece logic
- Need to adjust code for moving piece beyond canvas or outside window

/UNSTABLE BUILD/

***

19/12/2020 - v0.5.3-alpha:

*Added*

+ Updated __moved method so that piece position is reset if moved beyond chess board boundaries

*Pending*

- Need to add all widgets in frames
- Need to update __possible_move method

/UNSTABLE BUILD/

***

22/12/2020 - v0.5.4-alpha:

*Added*

+ Renamed constants module to global_vars.py
+ Added allowed variable in Piece class for indicating which side is allowed to move
+ Players must now make alternating moves (first white then black etc.)

*Pending*

- Need to add all widgets in frames
- Need to update __possible_move method
- Need to add movement logic for pieces

/UNSTABLE BUILD/

***

27/12/2020 - v0.6-alpha:

*Added*

+ Some behavioral fixes
+ Updated Pawn movement and functional behavior in in_range method
+ Refactored code
+ Added piece_opposites dictionary for ease of use
+ Spelling fixes

*Pending*

- Need to add all widgets in frames
- Need to update __possible_move method
- Need to add En Passant for pawn and need to remove captured piece

/UNSTABLE BUILD/

***

28/12/2020 - v0.6.1-alpha:

*Added*

+ Double move behavior for pawn added
+ Added self.moved and self.en_passant attributes to Pawn class

*Pending*

- Need to add all widgets in frames
- Need to update __possible_move method
- Need to add En Passant for pawn
- Need to remove captured pieces from the board
- Need to reuse in_range logic for both black and white pawns to simplify code

/UNSTABLE BUILD/

***

30/12/2020 - v0.6.2-alpha:

*Added*

+ Imported operators module for better code structure
+ Added operators dictionary for storing different arithmetic functions to be used depending on the color of the piece being moved
+ Refactored code
+ En passant feature added

*Pending*

- Need to add all widgets in frames
- Need to update __possible_move method
- Need to remove captured pieces from the board
- If any other move is made after a piece is pushed twice, en passant cannot happen anymore

/UNSTABLE BUILD/

***

30/12/2020 - v0.6.3-alpha:

*Added*

+ Captured pieces are removed from the board
+ Updated Knight movement and functional behavior

*Pending*

- Need to add all widgets in frames
- Need to update __possible_move method
- If any other move is made after a piece is pushed twice, en passant cannot happen anymore
- Need to promote pawn to queen if end is reached
- Need to ensure reveal check does not happen

/UNSTABLE BUILD/

***

01/01/2021 - v0.6.4-alpha:

*Added*

+ If any move is made, en passant is disabled
+ Added empty promote method for promoting pawn instance to another piece
+ Refactored code

*Pending*

- Need to add all widgets in frames
- Need to ensure reveal check does not happen
- Need to update promote method for pawn
- Need to review logic in __release method. Same player can move twice by keep moving a piece

/UNSTABLE BUILD/

***

02/01/2021 - v0.6.5-alpha-exp:

*Added*

+ Added Experimental Branch
+ Imported copy module for saving piece instance states
+ Added checked static method in King class
+ Added disable en_passant method in Pawn class
+ Added adjust method in Pawn class for adjusting specific attributes after a successful move
+ Major code refactor
+ Fixed same player can move twice bug

*Pending*

- Need to add all widgets in frames
- Need to finish movement behavior for rook, bishop, queen, and king
- Need to update promote method for pawn

/UNSTABLE BUILD/

***

02/01/2021 - v0.6.6-alpha-exp:

*Added*

+ Updated Bishop movement and functional behavior

*Pending*

- Need to add all widgets in frames
- Need to finish movement behavior for rook, queen, and king
- Need to update promote method for pawn
- Need to double check piece behavioral logic and add a way for queen to utilize rook and bishop behavioral methods

/UNSTABLE BUILD/

***

05/01/2021 - v0.6.7-alpha:

*Added*

+ Merged Experimental_Branch with master branch; v0.6.5-alpha-exp and v0.6.6-alpha-exp changed to v0.6.5-alpha and v0.6.6-alpha
+ Deleted Experimental_Branch
+ Updated Rook movement and functional behavior
+ Updated Queen movement and functional behavior

*Pending*

- Need to add all widgets in frames
- Need to finish movement behavior for king
- Need to update promote method for pawn

/UNSTABLE BUILD/

***

05/01/2021 - v0.7-alpha:

*Added*

+ Imported PIL library for image processing
+ Added several resources to resources directory
+ Added all widgets in frames

*Pending*

- Need to finish movement behavior for king
- Need to update promote method for pawn
- Need to adjust color palate for GUI

/UNSTABLE BUILD/

***

05/01/2021 - v0.7.1-alpha:

*Added*

+ When instances of pieces are created, the parent widget is required as argument instead of the canvas
+ tkinter library now imported in piece_classes.py rather than main.pyw
+ Added promote pawn behavior


*Pending*

- Need to finish movement behavior for king
- Need to adjust color palate for GUI

/UNSTABLE BUILD/