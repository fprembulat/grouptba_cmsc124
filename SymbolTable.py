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

            i += 1 # increment
        
        return self.symbols

    def display(self):
        print("\n Symbol Table")

        print("{:20}{}".format("Identifier", "Value"))

        for name, value in self.symbols.items():
            print("{:20}{}".format(name,value))


    # a list like [('add(3, 4)', '7')]
    def function_calls(self, token, lexeme):
        functions = {}      # name, parameters
        results = []

        i = 0
        # first pass which remembers every function
        while i < len(token):
            if token[i] == 'HOWIZI':
                name = lexeme[i + 1]
                functions[name] = [[], None]
                i += 2
                while token[i] != 'NEWLINE':
                    if token[i] == 'VAR':
                        functions[name][0].append(lexeme[i])
                    i += 1
                while token[i] != 'IFUSAYSO':
                    if token[i] == 'FOUNDYR' and functions[name][1] is None:
                        functions[name][1] = i + 1
                    i += 1
            i += 1

        # second pass where we run all the function calls
        i = 0
        while i < len(token):
            if token[i] == 'IIZ':
                name = lexeme[i + 1]
                args = []
                i += 2
                while token[i] != 'MKAY':
                    if token[i] == 'YR':
                        args.append(self.expression(token, lexeme, i + 1, None))
                    i += 1

                if name not in functions:
                    raise SyntaxError("Function " + name + " is not defined")
                params, found = functions[name]
                if len(args) != len(params):
                    raise SyntaxError("Function " + name + " needs " + str(len(params)) + " argument(s) but got " + str(len(args)))

                value = None
                if found is not None:
                    value = self.expression(token, lexeme, found, dict(zip(params, args)))

                label = name + "(" +  ", ".join(self.show(a) for a in args) + ")"
                results.append((label, self.show(value)))
            i += 1

        return results

    # a single vaue, or OP a AN b
    def expression(self, token, lexeme, j, scope):
        if token[j] not in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
            return self.operand(token, lexeme, j, scope)

        op = token[j]
        a = self.operand(token, lexeme, j + 1, scope)
        b = self.operand(token, lexeme, j + 3, scope)

        if type(a) not in (int, float) or type(b) not in (int, float):
            raise SyntaxError(lexeme[j] + " needs two number operands")

        if op == 'SUM':
            return a + b
        if op == 'DIFF':
            return a - b
        if op == 'PRODUKT':
            return a * b
        if op == 'BIGGR':
            return max(a, b)
        if op == 'SMALLR':
            return min(a, b)

        if b == 0:
            raise SyntaxError(lexeme[j] + " cannot divide by zero")
        if op == 'QUOSHUNT':
            if type(a) is int and type(b) is int:
                return int(a/b)
            else:
                return a/b

        return a % b

    # one literal, a parameter or a variable
    def operand(self, token, lexeme, j, scope):
        if token[j] == 'NUM':
            return int(lexeme[j])
        if token[j] == 'NUMBAR':
            return float(lexeme[j])
        if token[j] == 'YARN':
            return lexeme[j].strip('"')
        if token[j] == 'TROOF':
            return lexeme[j] == 'WIN'
        if token[j] == 'VAR':
            name = lexeme[j]
            if scope is None:                   # if in a calll, we use the symbol table
                return self.to_value(self.symbols.get(name, 'NOOB'))    
            if name not in scope:               # else if in a function, only its parameters exist
                raise SyntaxError("Variable " + name + " is not a parameter of this function")
            return scope[name]

        return None


    # the symbol table keeps values as text so we turn them into values
    def to_value(self, raw):
        if raw.startswith('"'):
            return raw.strip('"')
        if raw in ('WIN', 'FAIL'):
            return raw == 'WIN'
        try:
            return int(raw)
        except ValueError:
            pass
        try:
            return float(raw)
        except ValueError:
            return None

    # how the value is shown in the tbale
    def show(self, value):
        if value is None:
            return 'NOOB'
        if value is True:
            return 'WIN'
        if value is False:
            return 'FAIL'
        return str(value)
