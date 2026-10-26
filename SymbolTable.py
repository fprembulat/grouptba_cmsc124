# SymbolTable.py
# this file handles the symbol table

class SymbolTable:

    def __init__(self):
        self.symbols = {} # this is a dictionary that stores the var names and values

    def build(self, token, lexeme):
        i = 0 # initialize to 0 

        while i < len(token): # go through all token
            # look for a variable declaration
            if token[i] == 'VARDEC':
                # should be followed by a valid variable name
                if i + 1 < len(token) and token[i+1] == 'VAR':
                    name = lexeme[i+1] # store the name

                value = 'NOOB' # defult value, it means no value assigned in LOLCODE

                if (i + 3 <len(token) and token[i+2] == 'ASSIGN'):
                    value = lexeme[i + 3]
                
                self.symbols[name] = value

            i += 1 # increment
        
        return self.symbols

    def display(self):
        print("\n Symbol Table")

        print("{:20}{}".format("Identifier", "Value"))

        for name, value in self.symbols.items():
            print("{:20}{}".format(name,value))



