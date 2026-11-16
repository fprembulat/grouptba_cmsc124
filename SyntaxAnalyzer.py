# file for syntax analyzer

# -----------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------

def syntax(token, lexeme):

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
            raise SyntaxError("Variable declaration must be inside WAZZUP and BUHBYE")

        # output statement
        elif token[i] == 'PRINT':
            i = print_helper(token, i)

        elif token[i] == 'ORLY':
            i = orly_helper(token, i)

        elif token[i] == 'WTF':
            i = wtf_helper(token, i)
        
        elif token[i] == 'IMINYR':
            i = loop_helper(token, lexeme, i)

        elif token[i] == 'IIZ':
            i = function_call_helper(token, i)
        
        elif token[i] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
            i = arithmetic_helper(token, i)

        elif token[i] in ('BOTHSAEM', 'DIFFRINT'):
            i = comparison_helper(token, i)

        elif token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
            i = boolean_helper(token, i)

        elif token[i] == 'NOT':
            i = not_helper(token, i)

        elif token[i] in ('ALLOF', 'ANYOF'):
            i = infinite_boolean_helper(token, i)

        elif token[i] == 'SMOOSH':
            i = smoosh_helper(token, i)

        elif token[i] == 'MAEK':
            i = typecasting_helper(token, i)

        elif token[i] == 'HOWIZI':
            i = function_helper(token, i)

        # input statement
        elif token[i] == 'GIMMEH':
            i = input_helper(token, i)

        elif token[i] == 'VAR':
            if i + 1 <len(token) and token[i + 1] == 'ISNOWA':
                i = isnowa_helper(token, i)
            elif i + 1 < len(token) and token[i + 1] == 'NEWLINE':
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
        i += 1

        if i < len(token) and token[i] == 'A':
            if i + 1 >= len(token) or token[i + 1] not in ('TYPE', 'NOOB'):
                raise SyntaxError("ITZ A must be followed by a valid type")
            return i + 2
        elif i < len(token) and token[i] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
            i = arithmetic_helper(token, i)
        elif i < len(token) and token[i] in ('BOTHSAEM', 'DIFFRINT'):
            i = comparison_helper(token, i)
        elif i < len(token) and token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
            i = boolean_helper(token, i)
        elif i < len(token) and token[i] in ('ALLOF', 'ANYOF'):
            i = infinite_boolean_helper(token, i)
        elif i < len(token) and token[i] == 'NOT':
            i = not_helper(token, i)
        elif i < len(token) and token[i] == 'SMOOSH':
            i = smoosh_helper(token, i)
        elif i < len(token) and token[i] == 'MAEK':
            i = typecasting_helper(token, i)
        elif i < len(token) and token[i] in ('NUM', 'NUMBAR', 'YARN', 'TROOF', 'VAR', 'NOOB'):
            i += 1
        else:
            raise SyntaxError("ITZ must be followed by a valid value or expression")
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

    while i < len(token) and token[i] != 'NEWLINE':

        # Read one value or expression
        if token[i] == 'SMOOSH':
            i = smoosh_helper(token, i)

        elif token[i] == 'MAEK':
            i = typecasting_helper(token, i)

        elif token[i] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
            i = arithmetic_helper(token, i)

        elif token[i] in ('BOTHSAEM', 'DIFFRINT'):
            i = comparison_helper(token, i)

        elif token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
            i = boolean_helper(token, i)

        elif token[i] in ('ALLOF', 'ANYOF'):
            i = infinite_boolean_helper(token, i)

        elif token[i] == 'NOT':
            i = not_helper(token, i)

        elif token[i] in ('VAR', 'NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB'):
            i += 1

        else:
            raise SyntaxError("Invalid value after VISIBLE")

        if i < len(token) and token[i] != 'NEWLINE':

            if token[i] != 'PLUS':
                raise SyntaxError("VISIBLE values must be separated by +")

            i += 1

            if i >= len(token) or token[i] == 'NEWLINE':
                raise SyntaxError("PLUS must be followed by a value")

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

    i += 2

    if i >= len(token):
        raise SyntaxError("R must be followed by a value")

    if token[i] == 'SMOOSH':
        return smoosh_helper(token, i)

    elif token[i] == 'MAEK':
        return typecasting_helper(token, i)

    elif token[i] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
        return arithmetic_helper(token, i)

    elif token[i] in ('BOTHSAEM', 'DIFFRINT'):
        return comparison_helper(token, i)

    elif token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
        return boolean_helper(token, i)

    elif token[i] in ('ALLOF', 'ANYOF'):
        return infinite_boolean_helper(token, i)

    elif token[i] == 'NOT':
        return not_helper(token, i)

    elif token[i] in ('VAR', 'NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB'):
        return i + 1

    else:
        raise SyntaxError("R must be followed by a valid value or expression")
# -----------------------------------------------------

# ARITHMETIC OPERAND HELPER
# -----------------------------------------------------
def arithmetic_operand_helper(token, i):
    if token[i] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
        return arithmetic_helper(token, i)
    
    if token[i] in ('NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB', 'VAR'):
        return i + 1
    
    raise SyntaxError("Invalid arithmetic operand")
# -----------------------------------------------------

# ARITHMETIC HELPER
# -----------------------------------------------------
def arithmetic_helper(token, i):
    operator = token[i]

    if i + 1 >= len(token):
        raise SyntaxError(operator + " OF must have a first operand")

    first_end = arithmetic_operand_helper(token, i + 1)

    if first_end >= len(token) or token[first_end] != 'AN':
        raise SyntaxError(operator + " OF must have AN between operands")

    if first_end + 1 >= len(token):
        raise SyntaxError(operator + " OF must have a second operand")

    second_end = arithmetic_operand_helper(token, first_end + 1)

    return second_end
# -----------------------------------------------------


# COMPARISON OPERAND HELPER
# -----------------------------------------------------
def comparison_operand_helper(token, i):

    if token[i] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
        return arithmetic_helper(token, i)

    if token[i] in ('NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB', 'VAR'):
        return i + 1

    raise SyntaxError("Invalid comparison operand")
# -----------------------------------------------------


# COMPARISON HELPER
# -----------------------------------------------------
def comparison_helper(token, i):
    operator = token[i]

    if i + 1 >= len(token):
        raise SyntaxError(operator + " must have a first operand")

    first_end = comparison_operand_helper(token, i + 1)

    if first_end >= len(token) or token[first_end] != 'AN':
        raise SyntaxError(operator + " must have AN between operands")

    if first_end + 1 >= len(token):
        raise SyntaxError(operator + " must have a second operand")

    second_end = comparison_operand_helper(token, first_end + 1)

    return second_end
# -----------------------------------------------------

# BOOLEAN OPERAND HELPER
# -----------------------------------------------------
def boolean_operand_helper(token, i):

    if token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
        return boolean_helper(token, i)

    if token[i] == 'NOT':
        return not_helper(token, i)

    if token[i] in ('BOTHSAEM', 'DIFFRINT'):
        return comparison_helper(token, i)

    if token[i] in ('TROOF', 'NUM', 'NUMBAR', 'YARN', 'NOOB', 'VAR'):
        return i + 1

    raise SyntaxError("Invalid Boolean operand")
# -----------------------------------------------------


# BOOLEAN HELPER
# -----------------------------------------------------
def boolean_helper(token, i):
    operator = token[i]

    if i + 1 >= len(token):
        raise SyntaxError(operator + " OF must have a first operand")

    first_end = boolean_operand_helper(token, i + 1)

    if first_end >= len(token) or token[first_end] != 'AN':
        raise SyntaxError(operator + " OF must have AN between operands")

    if first_end + 1 >= len(token):
        raise SyntaxError(operator + " OF must have a second operand")

    second_end = boolean_operand_helper(token, first_end + 1)

    return second_end
# -----------------------------------------------------


# NOT HELPER
# -----------------------------------------------------
def not_helper(token, i):

    if i + 1 >= len(token):
        raise SyntaxError("NOT must be followed by a boolean value")

    return boolean_operand_helper(token, i + 1)
# -----------------------------------------------------

# SMOOSH HELPER
# -----------------------------------------------------
def smoosh_helper(token, i):
    i += 1

    if i >= len(token) or token[i] not in ('YARN', 'VAR', 'NUM', 'NUMBAR', 'TROOF', 'NOOB'):
        raise SyntaxError("SMOOSH must have a first value")

    i += 1

    while i < len(token) and token[i] == 'AN':
        i += 1

        if i >= len(token) or token[i] not in ('YARN', 'VAR', 'NUM', 'NUMBAR', 'TROOF', 'NOOB'):
            raise SyntaxError("AN must be followed by a value")

        i += 1

    return i
# -----------------------------------------------------

# TYPECASTING HELPER
# -----------------------------------------------------
def typecasting_helper(token, i):

    if i + 1 >= len(token) or token[i + 1] not in ('VAR', 'NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB'):
        raise SyntaxError("MAEK must be followed by a value")

    i += 2

    if i < len(token) and token[i] == 'A':
        i += 1

    if i >= len(token) or token[i] != 'TYPE':
        raise SyntaxError("MAEK must be followed by a valid type")

    return i + 1
# -----------------------------------------------------


# ISNOWA HELPER
# -----------------------------------------------------
def isnowa_helper(token, i):
    if i + 1 >= len(token) or token[i + 1] != 'ISNOWA':
        raise SyntaxError("Variable must be followed by IS NOW A")
    
    if i + 2 >= len(token) or token[i + 2] != 'TYPE':
        raise SyntaxError("IS NOW A must be followed by a type")

    return i + 3
# -----------------------------------------------------

# INFINITE BOOLEAN OPERAND HELPER
# -----------------------------------------------------
def infinite_boolean_operand_helper(token, i):

    if token[i] == 'NOT':
        return not_helper(token, i)

    if token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
        return boolean_helper(token, i)

    if token[i] in ('BOTHSAEM', 'DIFFRINT'):
        return comparison_helper(token, i)

    if token[i] in ('TROOF', 'VAR', 'NUM', 'NUMBAR', 'YARN', 'NOOB'):
        return i + 1

    if token[i] in ('ALLOF', 'ANYOF'):
        raise SyntaxError("ALL OF and ANY OF cannot be nested")

    raise SyntaxError("Invalid infinite Boolean operand")
# -----------------------------------------------------


# INFINITE BOOLEAN HELPER
# -----------------------------------------------------
def infinite_boolean_helper(token, i):
    operator = token[i]

    i += 1

    if i >= len(token):
        raise SyntaxError(operator + " must have at least one operand")

    i = infinite_boolean_operand_helper(token, i)

    while i < len(token) and token[i] == 'AN':
        i += 1

        if i >= len(token):
            raise SyntaxError(operator + " must have an operand after AN")

        i = infinite_boolean_operand_helper(token, i)

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

    while i < len(token) and token[i] not  in ('MEBBE', 'NOWAI', 'OIC'):
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

    while i < len(token) and token[i] == 'MEBBE':
        i += 1

        if i >= len(token) or token[i] not in ('TROOF', 'VAR'):
            raise SyntaxError("MEBBE must be followed by a condition")

        i += 1

        while i < len(token) and token[i] not in ('MEBBE', 'NOWAI', 'OIC'):
            if token[i] == 'NEWLINE':
                i += 1
            elif token[i] == 'PRINT':
                i = print_helper(token, i)
            elif token[i] == 'VAR':
                if i + 1 < len(token) and token[i + 1] == 'R':
                    i = assign_helper(token, i)
                else:
                    raise SyntaxError("Invalid statement inside MEBBE")
            elif token[i] == 'END':
                raise SyntaxError("O RLY must end with OIC")
            else: 
                raise SyntaxError("Invalid statement inside MEBBE")
        
            
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

    if i >= len(token) or token[i] != 'OIC':
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

            if i >= len(token) or token[i] not in ('NUM', 'NUMBAR', 'YARN', 'TROOF'):
                raise SyntaxError("OMG must be followed by a value")

            has_omg = True
            i += 1
        elif token[i] == 'OMGWTF':
            if has_omgwtf:
                raise SyntaxError("OMGWTF can only appear once")
            if not has_omg:
                raise SyntaxError("OMG must appear before OMGWTF")

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

    if i >= len(token) or token[i] != 'OIC':
        raise SyntaxError("WTF must end with OIC")

    return i + 1
# -----------------------------------------------------

# LOOP HELPER
# -----------------------------------------------------
def loop_helper(token, lexeme, i):
    if i + 1 >= len(token) or token[i + 1] != 'VAR':
        raise SyntaxError("IM IN YR must be followed by a loop name")

    loop_name = lexeme[i + 1]

    i += 2

    if i >= len(token) or token[i] not in ('UPPIN', 'NERFIN'):
        raise SyntaxError("Loop must contain UPPIN or NERFIN")

    i += 1
    
    if i >= len(token) or token[i] != 'YR':
        raise SyntaxError("UPPIN or NERFIN must be followed by YR")

    i += 1

    if i >= len(token) or token[i] != 'VAR':
        raise SyntaxError("YR must be followed by a variable")

    i += 1

    if i >= len(token) or token[i] not in ('TIL', 'WILE'):
        raise SyntaxError("Loop must contain TIL or WILE")
    
    i += 1

    if i >= len(token) or token[i] == 'NEWLINE':
        raise SyntaxError("Loop must have a condition")
    
    elif token[i] in ('BOTHSAEM', 'DIFFRINT'):
        i = comparison_helper(token, i)

    elif token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
        i = boolean_helper(token, i)
    
    elif token[i] == 'NOT':
        i = not_helper(token, i)

    elif token[i] in ('VAR', 'TROOF'):
        i += 1

    else:
        raise SyntaxError("Invalid loop condition")

    if i < len(token) and token[i] == 'NEWLINE':
        i += 1

    while i < len(token):
        if token[i] == 'NEWLINE':
            i += 1
        elif token[i] == 'PRINT':
            i = print_helper(token, i)
        elif token[i] == 'GIMMEH':
            i = input_helper(token, i)
        elif token[i] == 'GTFO':
            i += 1
        elif token[i] == 'VAR':
            if i + 1 < len(token) and token[i + 1] == 'R':
                i = assign_helper(token, i)
            else:
                raise SyntaxError("Invalid statement inside the loop")
        elif token[i] == 'IMOUTTAYR':
            if i + 1 >= len(token) or token[i + 1] != 'VAR':
                raise SyntaxError("IM OUTTA YR must be followed by a loop name")
            if lexeme[i + 1] != loop_name:
                raise SyntaxError("Loop closing name does not match")
            
            return i + 2
        elif token[i] == 'END':
            raise SyntaxError("Loop must end with IM OUTTA YR")
        else: raise SyntaxError("Invalid statement inside loop")
    raise SyntaxError("Loop must end with IM OUTTA YR") 
# -----------------------------------------------------

# FUNCTION HELPER
# -----------------------------------------------------
def function_helper(token, i):
    if i + 1 >= len(token) or token[i + 1] != 'VAR':
        raise SyntaxError("HOW IZ I must be followed by a function name")
    
    i += 2

    if i < len(token) and token[i] == 'YR':
        while True:
            i += 1

            if i >= len(token) or token[i] != 'VAR':
                raise SyntaxError("YR must be followed by a parameter name")

            i += 1

            if i < len(token) and token[i] == 'AN':
                i += 1

                if i >= len(token) or token[i] != 'YR':
                    raise SyntaxError("AN must be followed by YR")
            else: 
                break
    
    if i >= len(token) or token[i] != 'NEWLINE':
        raise SyntaxError("Function declaration must end with a newline")
    
    i += 1

    while i < len(token) and token[i] != 'IFUSAYSO':
        if token[i] == 'NEWLINE':
            i += 1
        elif token[i] == 'PRINT':
            i = print_helper(token, i)

        elif token[i] == 'FOUNDYR':
            i += 1

            if i >= len(token) or token[i] in ('NEWLINE', 'IFUSAYSO'):
                raise SyntaxError("FOUND YR must be followed by a value")
            
            if token[i] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
                i = arithmetic_helper(token, i)
            
            elif token[i] in ('BOTHSAEM', 'DIFFRINT'):
                i = comparison_helper(token, i)
            
            elif token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
                i = boolean_helper(token, i)

            elif token[i] == 'NOT':
                i = not_helper(token, i)
            
            elif token[i] in ('ALLOF', 'ANYOF'):
                i = infinite_boolean_helper(token, i)

            elif token[i] == 'SMOOSH':
                i = smoosh_helper(token, i)
            
            elif token[i] == 'MAEK':
                i = typecasting_helper(token, i)
            
            elif token[i] in ('NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB', 'VAR'):
                i += 1
            else: raise SyntaxError("Invalid return value")

        elif token[i] == 'GTFO':
            i += 1
        elif token[i] == 'VAR':
            if i + 1 < len(token) and token[i + 1] == 'R':
                i = assign_helper(token, i)
            else:
                raise SyntaxError("Invalid statement inside function")
        else:
            raise SyntaxError("Invalid statement inside function")
    if i >= len(token) or token[i] != 'IFUSAYSO':
        raise SyntaxError("Functino must end with IF U SAY SO")
    
    return i + 1
# -----------------------------------------------------

# FUNCTION CALL HELPER
# -----------------------------------------------------
def function_call_helper(token, i):

    if i + 1 >= len(token) or token[i + 1] != 'VAR':
        raise SyntaxError("I IZ must be followed by a function name")
    
    i += 2

    if i < len(token) and token[i] == 'YR':
        while True:
            i += 1
            if i >= len(token):
                raise SyntaxError("YR must be followed by an argument")
            
            if token[i] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
                i = arithmetic_helper(token, i)
            elif token[i] in ('BOTHSAEM', 'DIFFRINT'):
                i = comparison_helper(token, i)    
            elif token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
                i = boolean_helper(token, i)
            elif token[i] == 'NOT':
                i = not_helper(token, i)
            elif token[i] in ('ALLOF', 'ANYOF'):
                i = infinite_boolean_helper(token, i)
            elif token[i] == 'SMOOSH':
                i = smoosh_helper(token, i)
            elif token[i] == 'MAEK':
                i = typecasting_helper(token, i)
            elif token[i] in ('NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB', 'VAR'):
                i += 1
            else:
                raise SyntaxError("YR must be followed by an argumenet")

            if i < len(token) and token[i] == 'AN':
                i += 1
                if i >= len(token) or token[i] != 'YR':
                    raise SyntaxError("AN must be followed by YR")
            else: 
                break

    if i >= len(token) or token[i] != 'MKAY':
        raise SyntaxError("Function call must end with MKAY")
    
    return i + 1
# -----------------------------------------------------