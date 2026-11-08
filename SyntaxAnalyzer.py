# file for syntax analyzer

# -----------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------

def syntax(lex):

    # -----------------------------------------------------
    # check if program starts with HAI
    if not lex or lex[0] != 'START':
        raise SyntaxError('must start with HAI')

    # check if program ends with KTHXBYE
    if lex[-1] != 'END':
        raise SyntaxError('must end with KTHXBYE')
    # -----------------------------------------------------

    # start after HAI
    i = 1

    # -----------------------------------------------------
    # loop through all tokens until KTHXBYE
    while i < len(lex) - 1:

        # skip newlines
        if lex[i] == 'NEWLINE':
            i += 1

        # variable declaration
        elif lex[i] == 'VARDEC':
            i = vardec_helper(lex, i)

        # output statement
        elif lex[i] == 'PRINT':
            i = print_helper(lex, i)

        # input statement
        elif lex[i] == 'GIMMEH':
            i = input_helper(lex, i)

        elif lex[i] == 'VAR':
            i = assign_helper(lex, i)

        # multiline comment
        elif lex[i] == 'OBTW':
            i = comm_helper(lex, i)

        # unexpected token
        else:
            raise SyntaxError('Unexpected token: ' + lex[i])
    # -----------------------------------------------------

# -----------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------

# VARDEC HELPER
# -----------------------------------------------------
def vardec_helper(lex, i):
    if i + 1 >= len(lex) or lex[i + 1] != 'VAR':
        raise SyntaxError("Variable declaration must have a variable name")

    i += 2

    if i < len(lex) and lex[i] == 'ASSIGN':
        if i + 1 < len(lex) and lex[i + 1] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
            i = arithmetic_helper(lex, i+1)

        elif i + 1 < len(lex) and lex[i + 1] in ('BOTHSAEM', 'DIFFRINT'):
            i = comparison_helper(lex, i + 1)
        
        elif i + 1 < len(lex) and lex[i + 1] in ('BOTHOF', 'EITHER', 'WONOF'):
            i = boolean_helper(lex, i + 1)

        elif i + 1 < len(lex) and lex[i + 1] in ('ALLOF', 'ANYOF'):
            i = infinite_boolean_helper(lex, i + 1)

        elif i + 1 < len(lex) and lex[i + 1] == 'NOT':
            i = not_helper(lex, i + 1)
        
        elif i + 1 <len(lex) and lex[i + 1] in ('NUM', 'YARN', 'VAR'):
            i += 2
        
        else:
            raise SyntaxError("Assign must be followed by a value")
    return i
# -----------------------------------------------------

# -----------------------------------------------------
def comm_helper(lex):	
    i += 1

    while i < len(lex):
        if lex[i] == 'TLDR':
            return i + 1

        i += 1

    raise SyntaxError("OBTW must be closed with TLDR")
# -----------------------------------------------------

# -----------------------------------------------------
def print_helper(lex, i):
    i += 1

    if i >= len(lex) or lex[i] == 'NEWLINE':
        raise SyntaxError('VISIBLE must be followed by a value')

    if lex[i] not in ('VAR', 'NUM', 'YARN'):
        raise SyntaxError("Invalid value")

    i += 1
    
    while i < len(lex) and lex[i] in ('VAR', 'NUM', 'YARN'):
        i += 1

    return i
# -----------------------------------------------------

# -----------------------------------------------------
def input_helper(lex, i):
	if i + 1 >= len(lex) or lex[i + 1] != 'VAR':
		raise SyntaxError('GIMMEH must be followed by a variable')

	return i + 2
# -----------------------------------------------------

# ASSIGNMENT HELPER
# -----------------------------------------------------
def assign_helper(lex, i):
    if i + 1 >= len(lex) or lex[i + 1] != 'R':
        raise SyntaxError("Variable must be followed by R")

    if i + 2 >= len(lex) or lex[i + 2] not in ('VAR', 'NUM', 'YARN'):
        raise SyntaxError("R must be followed by a value")
    
    return i + 3
# -----------------------------------------------------

# ARITHMETIC HELPER
# -----------------------------------------------------
def arithmetic_helper(lex, i):

    operator = lex[i]

    if i + 1 >= len(lex) or lex[i + 1] not in ('NUM', 'VAR'):
        raise SyntaxError(operator + " OF must have a first operand")

    if i + 2 >= len(lex) or lex[i + 2] != 'AN':
        raise SyntaxError(operator + " OF must have AN between operands")
    
    if i + 3 >= len(lex) or lex[i + 3] not in ('NUM', 'VAR'):
        raise SyntaxError(operator + " OF must have a second operand")
    
    return i + 4
# -----------------------------------------------------

# COMPARISON HELPER
# -----------------------------------------------------
def comparison_helper(lex, i):
    operator = lex[i]

    if i + 1 >= len(lex) or lex[i + 1] not in ('NUM', 'VAR'):
        raise SyntaxError(operator + " OF must have a first operand")

    if i + 2 >= len(lex) or lex[i + 2] != 'AN':
        raise SyntaxError(operator + " OF must have AN between operands")
    
    if i + 3 >= len(lex) or lex[i + 3] not in ('NUM', 'VAR'):
        raise SyntaxError(operator + " OF must have a second operand")

    return i + 4
# -----------------------------------------------------

# BOOLEAN HELPER
# -----------------------------------------------------
def boolean_helper(lex, i):
    operator = lex[i]

    if i + 1 >= len(lex) or lex[i + 1] not in ('TROOF', 'VAR'):
        raise SyntaxError(operator + " OF must have a first operand")

    if i + 2 >= len(lex) or lex[i + 2] != 'AN':
        raise SyntaxError(operator + " OF must have AN between operands")
    
    if i + 3 >= len(lex) or lex[i + 3] not in ('TROOF', 'VAR'):
        raise SyntaxError(operator + " OF must have a second operand")

    return i + 4
# -----------------------------------------------------

# NOT HELPER
# -----------------------------------------------------
def not_helper(lex, i):
    if i + 1 >= len(lex) or lex[i + 1] not in ('TROOF', 'VAR'):
        raise SyntaxError("NOT must be followed by a boolean value")

    return i + 2
# -----------------------------------------------------

# INFINITE BOOLEAN HELPER
# -----------------------------------------------------
def infinite_boolean_helper(lex, i):
    operator = lex[i]

    i += 1

    if i >= len(lex) or lex[i] not in ('TROOF', 'VAR'):
        raise SyntaxError(operator + " must have atleast one operand")
    
    i += 1

    while i < len(lex) and lex[i] == 'AN':
        i += 1

        if i >= len(lex) or lex[i] not in ('TROOF', 'VAR'):
            raise SyntaxError(operator + " must have an operand after AN")
            
        i += 1

    if i >= len(lex) or lex[i] != 'MKAY':
        raise SyntaxError(operator + " must end with MKAY")

    return i + 1
# -----------------------------------------------------