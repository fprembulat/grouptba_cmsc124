# file for syntax analyzer

# -----------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------

def syntax(token):

    # -----------------------------------------------------
    # check if program starts with HAI
    if not token or token[0] != 'START':
        raise SyntaxError('must start with HAI')

    # check if program ends with KTHXBYE
    if token[-1] != 'END':
        raise SyntaxError('must end with KTHXBYE')
    # -----------------------------------------------------

    # start after HAI
    i = 1

    # -----------------------------------------------------
    # loop through all tokens until KTHXBYE
    while i < len(token) - 1:

        # skip newlines
        if token[i] == 'NEWLINE':
            i += 1
        
        elif token[i] == 'WAZZUP':
            i = wazzup_helper(token, i)

        # variable declaration
        elif token[i] == 'VARDEC':
            i = vardec_helper(token, i)

        # output statement
        elif token[i] == 'PRINT':
            i = print_helper(token, i)

        elif token[i] == 'ORLY':
            i = orly_helper(token, i)

        elif token[i] == 'WTF':
            i = wtf_helper(token, i)

        # input statement
        elif token[i] == 'GIMMEH':
            i = input_helper(token, i)

        elif token[i] == 'VAR':
            if i + 1 < len(token) and token[i + 1] == 'NEWLINE':
                i += 1
            else:
                i = assign_helper(token, i)    

        # multiline comment
        elif token[i] == 'OBTW':
            i = comm_helper(token, i)

        # unexpected token
        else:
            raise SyntaxError('Unexpected token: ' + token[i])
    # -----------------------------------------------------

# -----------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------

# VARDEC HELPER
# -----------------------------------------------------
def vardec_helper(token, i):
    if i + 1 >= len(token) or token[i + 1] != 'VAR':
        raise SyntaxError("Variable declaration must have a variable name")

    i += 2

    if i < len(token) and token[i] == 'ASSIGN':
        if i + 1 < len(token) and token[i + 1] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
            i = arithmetic_helper(token, i+1)

        elif i + 1 < len(token) and token[i + 1] in ('BOTHSAEM', 'DIFFRINT'):
            i = comparison_helper(token, i + 1)
        
        elif i + 1 < len(token) and token[i + 1] in ('BOTHOF', 'EITHER', 'WONOF'):
            i = boolean_helper(token, i + 1)

        elif i + 1 < len(token) and token[i + 1] in ('ALLOF', 'ANYOF'):
            i = infinite_boolean_helper(token, i + 1)

        elif i + 1 < len(token) and token[i + 1] == 'NOT':
            i = not_helper(token, i + 1)
        
        elif i + 1 <len(token) and token[i + 1] in ('NUM', 'YARN', 'VAR', 'NOOB'):
            i += 2
        
        else:
            raise SyntaxError("Assign must be followed by a value")
    return i
# -----------------------------------------------------

# -----------------------------------------------------
def comm_helper(token, i):	
    i += 1

    while i < len(token):
        if token[i] == 'TLDR':
            return i + 1

        i += 1

    raise SyntaxError("OBTW must be closed with TLDR")
# -----------------------------------------------------

# -----------------------------------------------------
def print_helper(token, i):
    i += 1

    if i >= len(token) or token[i] == 'NEWLINE':
        raise SyntaxError('VISIBLE must be followed by a value')

    if token[i] not in ('VAR', 'NUM', 'YARN', 'NOOB'):
        raise SyntaxError("Invalid value")

    i += 1
    
    while i < len(token) and token[i] in ('VAR', 'NUM', 'YARN', 'NOOB'):
        i += 1

    return i
# -----------------------------------------------------

# -----------------------------------------------------
def input_helper(token, i):
	if i + 1 >= len(token) or token[i + 1] != 'VAR':
		raise SyntaxError('GIMMEH must be followed by a variable')

	return i + 2
# -----------------------------------------------------

# ASSIGNMENT HELPER
# -----------------------------------------------------
def assign_helper(token, i):
    if i + 1 >= len(token) or token[i + 1] != 'R':
        raise SyntaxError("Variable must be followed by R")

    if i + 2 >= len(token) or token[i + 2] not in ('VAR', 'NUM', 'YARN', 'NOOB'):
        raise SyntaxError("R must be followed by a value")
    
    return i + 3
# -----------------------------------------------------

# ARITHMETIC HELPER
# -----------------------------------------------------
def arithmetic_helper(token, i):

    operator = token[i]

    if i + 1 >= len(token) or token[i + 1] not in ('NUM', 'VAR'):
        raise SyntaxError(operator + " OF must have a first operand")

    if i + 2 >= len(token) or token[i + 2] != 'AN':
        raise SyntaxError(operator + " OF must have AN between operands")
    
    if i + 3 >= len(token) or token[i + 3] not in ('NUM', 'VAR'):
        raise SyntaxError(operator + " OF must have a second operand")
    
    return i + 4
# -----------------------------------------------------

# COMPARISON HELPER
# -----------------------------------------------------
def comparison_helper(token, i):
    operator = token[i]

    if i + 1 >= len(token) or token[i + 1] not in ('NUM', 'VAR'):
        raise SyntaxError(operator + " OF must have a first operand")

    if i + 2 >= len(token) or token[i + 2] != 'AN':
        raise SyntaxError(operator + " OF must have AN between operands")
    
    if i + 3 >= len(token) or token[i + 3] not in ('NUM', 'VAR'):
        raise SyntaxError(operator + " OF must have a second operand")

    return i + 4
# -----------------------------------------------------

# BOOLEAN HELPER
# -----------------------------------------------------
def boolean_helper(token, i):
    operator = token[i]

    if i + 1 >= len(token) or token[i + 1] not in ('TROOF', 'VAR'):
        raise SyntaxError(operator + " OF must have a first operand")

    if i + 2 >= len(token) or token[i + 2] != 'AN':
        raise SyntaxError(operator + " OF must have AN between operands")
    
    if i + 3 >= len(token) or token[i + 3] not in ('TROOF', 'VAR'):
        raise SyntaxError(operator + " OF must have a second operand")

    return i + 4
# -----------------------------------------------------

# NOT HELPER
# -----------------------------------------------------
def not_helper(token, i):
    if i + 1 >= len(token) or token[i + 1] not in ('TROOF', 'VAR'):
        raise SyntaxError("NOT must be followed by a boolean value")

    return i + 2
# -----------------------------------------------------



# INFINITE BOOLEAN HELPER
# -----------------------------------------------------
def infinite_boolean_helper(token, i):
    operator = token[i]

    i += 1

    if i >= len(token) or token[i] not in ('TROOF', 'VAR'):
        raise SyntaxError(operator + " must have atleast one operand")
    
    i += 1

    while i < len(token) and token[i] == 'AN':
        i += 1

        if i >= len(token) or token[i] not in ('TROOF', 'VAR'):
            raise SyntaxError(operator + " must have an operand after AN")
            
        i += 1

    if i >= len(token) or token[i] != 'MKAY':
        raise SyntaxError(operator + " must end with MKAY")

    return i + 1
# -----------------------------------------------------

# WAZZUP HELPER
# -----------------------------------------------------
def wazzup_helper(token, i):
    i += 1

    while i < len(token) and token[i] == 'NEWLINE':
        i += 1

    while i <len(token) and token[i] != 'BUHBYE':
        if token[i] == 'VARDEC':
            i = vardec_helper(token, i)
        elif token[i] == 'NEWLINE':
            i += 1
        elif token[i] == 'END':
            raise SyntaxError("WAZZUP must end with BUHBYE")
        else:
            raise SyntaxError("Only variable declarations are allowed inside WAZZUP")
    
    if i >= len(token):
        raise SyntaxError("WAZZUP must end with BUHBYE")
    
    return i + 1
# -----------------------------------------------------

# ORLY HELPER
# -----------------------------------------------------
def orly_helper(token, i):
    i += 1

    while i < len(token) and token[i] == 'NEWLINE':
        i += 1

    if i >= len(token) or token[i] != 'YARLY':
        raise SyntaxError("O RLY must be followed by YA RLY")

    i += 1

    while i < len(token) and token[i] not  in ('NOWAI', 'OIC'):
        if token[i] == 'NEWLINE':
            i += 1
        elif token[i] == 'PRINT':
            i = print_helper(token, i)
        elif token[i] == 'VAR':
            if i + 1 < len(token) and token[i + 1] == 'R':
                i = assign_helper(token, i)
            else:
                raise SyntaxError("Invalid statement inside YA RLY")
        elif token[i] == 'END':
            raise SyntaxError("O RLY must end with OIC")
        else:
            raise SyntaxError("Invalid statement inside YA RLY")
            
    if i < len(token) and token[i] == 'NOWAI':
        i += 1

        while i < len(token) and token[i] not  in ('NOWAI', 'OIC'):
            if token[i] == 'NEWLINE':
                i += 1
            elif token[i] == 'PRINT':
                i = print_helper(token, i)
            elif token[i] == 'VAR':
                if i + 1 < len(token) and token[i + 1] == 'R':
                    i = assign_helper(token, i)
                else: 
                    raise SyntaxError("Invalid statement inside NOWAI")
            elif token[i] == 'END':
                raise SyntaxError("O RLY must end with OIC")
            else: 
                raise SyntaxError("Invalid statement inside NOWAI")

    if i >= len(token):
        raise SyntaxError("O RLY must end with OIC")
    
    return i + 1
# -----------------------------------------------------

# WTF HELPER
# -----------------------------------------------------
def wtf_helper(token, i):
    i += 1

    while i < len(token) and token[i] == 'NEWLINE':
        i += 1

    has_omg = False
    has_omgwtf = False

    while i < len(token) and token[i] != 'OIC':
        if token[i] == 'NEWLINE':
            i += 1
        elif token[i] == 'OMG':
            if has_omgwtf:
                raise SyntaxError("OMG cannot appear after OMGWTF")
            i += 1

            if i >= len(token) or token[i] not in ('NUM', 'YARN', 'TROOF'):
                raise SyntaxError("OMG must be followed by a value")

            has_omg = True
            i += 1
        elif token[i] == 'OMGWTF':
            if has_omgwtf:
                raise SyntaxError("OMGWTF can only appear once")

            has_omgwtf = True
            i += 1
        elif token[i] == 'PRINT':
            i = print_helper(token, i)
        elif token[i] == 'VAR':
            if i + 1 < len(token) and token[i + 1] == 'R':
                i = assign_helper(token, i)
            else:
                raise SyntaxError("Invalid statement inside WTF")
        elif token[i] == 'GTFO':
            i += 1
        else:
            raise SyntaxError("Invalid statement inside WTF")
        
    if not has_omg:
        raise SyntaxError("WTF must have at least one OMG case")

    if i >= len(token):
        raise SyntaxError("WTF must end with OIC")

    return i + 1
# -----------------------------------------------------

