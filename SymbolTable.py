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
                    if name in self.symbols:
                        raise SyntaxError("Variable " + name + " is already declared")

                value = 'NOOB' # defult value, it means no value assigned in LOLCODE

                if (i + 3 <len(token) and token[i+2] == 'ASSIGN'):
                    value = lexeme[i + 3]
                
                self.symbols[name] = value

            i += 1 # increment

            # 'i < len(token)' error handler so it wouldn't cause an indexerror
            if i < len(token) and token[i] == 'PRINT':
                j = i + 1
                output = ""     # initial placeholder where what would be printed would be stored
                # read the rest of the line until a newline occurs
                while j < len(token) and token[j] != 'NEWLINE': 
                    if token[j] == 'VAR':
                        # if the value encountered is a variable, we translate it into its value then append to the output variable
                        output += str(self.symbols.get(lexeme[j], 'NOOB')).strip('"') 
                    elif token[j] in ('YARN', 'NUM', 'NUMBAR', 'TROOF'):
                        output += lexeme[j].strip('"')
                    j += 1
                self.symbols['IT'] = output
                i = j   # continue the loop from the index of the newline
        
        return self.symbols

    def display(self):
        print("\n Symbol Table")

        print("{:20}{}".format("Identifier", "Value"))

        for name, value in self.symbols.items():
            print("{:20}{}".format(name,value))



