## grouptba_cmsc124


------------------------------------------------------------------------------------
.____       _____      _____   ________  _________  ________  ________  ___________
|    |     /     \    /  _  \  \_____  \ \_   ___ \ \_____  \ \______ \ \_   _____/
|    |    /  \ /  \  /  /_\  \  /   |   \/    \  \/  /   |   \ |    |  \ |    __)_ 
|    |___/    Y    \/    |    \/    |    \     \____/    |    \|    `   \|        \
|_______ \____|__  /\____|__  /\_______  /\______  /\_______  /_______  /_______  /
        \/       \/         \/         \/        \/         \/        \/        \/ 
------------------------------------------------------------------------------------

# LMAOCODE

A LOLCODE interpreter with a Tkinter GUI, written in Python. 

It tokenizes and runs .lol programs and then shows the tokens, the symbol table, and the program output.

# Requirements:

* Python 3.6 or newer
* Tkinter (bundled with Python on Windows and macOS)

To install Tkinter on linux:
`sudo apt install python3-tk`

# How to run:

1. a. Clone the git repository by downloading the zip file or using the command:

`git clone https://github.com/fprembulat/grouptba_cmsc124.git`

1. b. Unzip the file if you downloaded the ZIP file

2. Go into the main folder of the file (the directory where the Principal.py is located)

3. Run the Principal.py file through double-click or run this code in the terminal in the same directory

Windows:

`py Principal.py`

Linux/macOS:

`python3 Principal.py`

4. Select the files you want to run using the 'Open' button and then run the files using the 'Run' button.

# How the interpreter works / File breakdown

File 					|				Role
=============================================================================================================
Principal.py 			| Main file. Tkinter window with the editor, tokens, symbol table, and console. Calls
						| interpreter when Run is pressed
						|
Buffer.py 				| Loads the initial 'program.lol' into the editor at startup.
						|
LexicalAnalyzer.py 		| Regex-based tokenizer. Turns the program into tokens and lexemes
						|
SyntaxAnalyzer.py		| Checks statement order and structure. Raises 'SyntaxErrors'
						|
SemanticAnalyzer.py		| Checks that the code makes sense (semantics wise). Raises 'SemanticError'
						|
Interpreter.py			| Contains the Parser and Interpreter that runs the program. Raises 'InterpreterError' at runtime.
						|
LexemeTable.py			| Maps each token to a type/classification for the token table
						|
SymbolTable.py 			| Stores variable names and their values as text.
						|


References:

https://github.com/christianrfg/lexical-analyzer/tree/master
