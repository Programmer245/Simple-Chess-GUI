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

+ Added Piece parent class and all other subclasses to define piece behaviour
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
+ Bound mouse movement events to chess piees
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