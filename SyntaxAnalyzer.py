# file for syntax analyzer

# -----------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------
def syntax(token, lexeme):
    token, lexeme = remove_sline_comm(token, lexeme)

    # remove multiline comments everywhere (before any other check)
    i = 0
    while i < len(token):
        if token[i] == 'OBTW':
            token, lexeme = comm_helper(token, lexeme, i)
        else:
            i += 1

    i = 0

    # strip leading newlines
    while token and token[0] == 'NEWLINE':
        token.pop(0)
        lexeme.pop(0)

    # functions before HAI
    while i < len(token) and token[i] == 'HOWIZI':
        i = function_helper(token, lexeme, i)

        while i < len(token) and token[i] == 'NEWLINE':
            i += 1

    if i >= len(token) or token[i] != 'START':
        raise SyntaxError("Program must start with HAI")

    # KTHXBYE must exist; the first END token is the program's end
    if 'END' not in token:
        raise SyntaxError("Program must end with KTHXBYE")

    end_i = token.index('END')

    # start after HAI
    i += 1

    # main loop: runs until KTHXBYE
    while i < end_i:

        if token[i] == 'NEWLINE':
            i += 1
            continue

        elif token[i] == 'WAZZUP':
            i = wazzup_helper(token, i)
        elif token[i] == 'VARDEC':
            raise SyntaxError("Variables must be declared inside WAZZUP")

        elif token[i] == 'PRINT':
            i = print_helper(token, i)

        elif token[i] == 'ORLY':
            i = orly_helper(token, lexeme, i)

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
            i = function_helper(token, lexeme, i)

        elif token[i] == 'GIMMEH':
            i = input_helper(token, i)

        elif token[i] == 'VAR':
            if i + 1 < len(token) and token[i + 1] == 'ISNOWA':
                i = isnowa_helper(token, i)
            elif i + 1 < len(token) and token[i + 1] == 'NEWLINE':
                i += 1
            else:
                i = assign_helper(token, i)

        else:
            raise SyntaxError('Unexpected token: ' + token[i])
        
        if i < end_i and token[i] != 'NEWLINE':
            raise SyntaxError("Each statement mustbe on its own line")

    # after KTHXBYE: only newlines and functions are allowed
    i = end_i + 1

    while i < len(token) and token[i] == 'NEWLINE':
        i += 1

    while i < len(token) and token[i] == 'HOWIZI':
        i = function_helper(token, lexeme, i)

        while i < len(token) and token[i] == 'NEWLINE':
            i += 1

    if i < len(token):
        raise SyntaxError("Only functions and comments are allowed after KTHXBYE")
# -----------------------------------------------------

# HELPER FUNCTIONS
# -----------------------------------------------------

# -----------------------------------------------------
# COMMENT REMOVER HELPER
# -----------------------------------------------------
def remove_sline_comm(token, lexeme):
    i = 0

    while i < len(token):
        if token[i] == 'BTW':
            while i < len(token) and token[i] != 'NEWLINE':
                token.pop(i)
                lexeme.pop(i)
        else:
            i += 1

    return token, lexeme

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
        elif i < len(token) and token[i] == 'IIZ':
            i = function_call_helper(token, i)
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
def comm_helper(token, lexeme, i):	
    if i > 0 and token[i - 1] != 'NEWLINE':
        raise SyntaxError("OBTW must be on its own line")

    j = i + 1
    while j < len(token) and token[j] != 'TLDR':
        j += 1

    if j >= len(token):
        raise SyntaxError("OBTW must be closed with TLDR")

    if j > 0 and token[j - 1] != 'NEWLINE':
        raise SyntaxError("TLDR must be on its own line")
    
    if j + 1 < len(token) and token[j + 1] != 'NEWLINE':
        raise SyntaxError("TLDR must be on its own line")

    del token[i:j + 1]
    del lexeme[i:j + 1]

    return token, lexeme
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
        
        elif token[i] == 'IIZ':
            i = function_call_helper(token, i)

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

    elif token[i] == 'IIZ':
        return function_call_helper(token, i)

    elif token[i] in ('VAR', 'NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB'):
        return i + 1

    else:
        raise SyntaxError("R must be followed by a valid value or expression")
# -----------------------------------------------------

# ARITHMETIC OPERAND HELPER
# -----------------------------------------------------
def arithmetic_operand_helper(token, i):

    if token[i] == 'IIZ':
        return function_call_helper(token, i)
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
            raise SyntaxError("Invalid declarations inside WAZZUP")
                
    if i >= len(token):
        raise SyntaxError("WAZZUP must end with BUHBYE")
    
    return i + 1
# -----------------------------------------------------

# ORLY HELPER
# -----------------------------------------------------
def block_helper(token, lexeme, i, terminators, where):
    while i < len(token) and token[i] not in terminators:
        t = token[i]
        if t == 'NEWLINE':
            i += 1
            continue
        elif t == 'PRINT':
            i = print_helper(token, i)
        elif t == 'VAR' and i + 1 < len(token) and token[i + 1] == 'R':
            i = assign_helper(token, i)
        elif t == 'VAR' and i + 1 < len(token) and token[i + 1] == 'ISNOWA':
            i = isnowa_helper(token, i)
        elif t == 'ORLY':
            i = orly_helper(token, lexeme, i)
        elif t == 'GTFO':
            i += 1
        elif t == 'FOUNDYR':
            i = foundyr_helper(token, i)
        elif t in ('BOTHSAEM', 'DIFFRINT'):
            i = comparison_helper(token, i)
        elif t in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
            i = arithmetic_helper(token, i)
        elif t in ('BOTHOF', 'EITHER', 'WONOF'):
            i = boolean_helper(token, i)
        elif t == 'NOT':
            i = not_helper(token, i)
        elif t in ('ALLOF', 'ANYOF'):
            i = infinite_boolean_helper(token, i)
        elif t == 'IIZ':
            i = function_call_helper(token, i)
        elif t == 'IMINYR':
            i = loop_helper(token, lexeme, i)
        elif t == 'GIMMEH':
            i = input_helper(token, i)
        elif t == 'MAEK':
            i = typecasting_helper(token, i)
        elif t == 'SMOOSH':
            i = smoosh_helper(token, i)
        elif t == 'WTF':
            i = wtf_helper(token, i)
        elif t == 'END':
            raise SyntaxError(where + " must be closed before KTHXBYE")
        else:
            #raise SyntaxError(f"Invalid statement inside {where}: token={t}, lexeme={lexeme[i]}")
            raise SyntaxError(f"Invalid statement inside {where}")

        if i < len(token) and token[i] != 'NEWLINE':
            raise SyntaxError("Each statement must be on its own line")
    return i


def orly_helper(token, lexeme, i):
    i += 1
    while i < len(token) and token[i] == 'NEWLINE':
        i += 1

    if i >= len(token) or token[i] != 'YARLY':
        raise SyntaxError("O RLY must be followed by YA RLY")
    i += 1

    i = block_helper(token, lexeme, i, ('MEBBE', 'NOWAI', 'OIC'), "YA RLY")

    while i < len(token) and token[i] == 'MEBBE':
        i += 1

        if i >= len(token) or token[i] == 'NEWLINE':
            raise SyntaxError("MEBBE must be followed by a condition")

        if token[i] in ('BOTHSAEM', 'DIFFRINT'):
            i = comparison_helper(token, i)

        elif token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
            i = boolean_helper(token, i)

        elif token[i] in ('ALLOF', 'ANYOF'):
            i = infinite_boolean_helper(token, i)

        elif token[i] == 'NOT':
            i = not_helper(token, i)

        elif token[i] in ('VAR', 'TROOF'):
            i += 1

        else:
            raise SyntaxError("Invalid MEBBE condition")

        i = block_helper(token, lexeme, i, ('MEBBE', 'NOWAI', 'OIC'), "MEBBE")

    if i < len(token) and token[i] == 'NOWAI':
        i += 1
        i = block_helper(token, lexeme, i, ('OIC',), "NO WAI")

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

        # TIL / WILE and its condition are optional
    if i < len(token) and token[i] in ('TIL', 'WILE'):
        i += 1

        if i >= len(token) or token[i] == 'NEWLINE':
            raise SyntaxError("TIL/WILE must be followed by a condition")

        elif token[i] in ('BOTHSAEM', 'DIFFRINT'):
            i = comparison_helper(token, i)
        elif token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
            i = boolean_helper(token, i)
        elif token[i] == 'NOT':
            i = not_helper(token, i)
        elif token[i] in ('ALLOF', 'ANYOF'):
            i = infinite_boolean_helper(token, i)
        elif token[i] in ('VAR', 'TROOF'):
            i += 1
        else:
            raise SyntaxError("Invalid loop condition")

    # header must end here
    if i < len(token) and token[i] != 'NEWLINE':
        raise SyntaxError("Loop header must end with a newline")

    # loop body
    i = block_helper(token, lexeme, i, ('IMOUTTAYR',), "loop")

    if i >= len(token) or token[i] != 'IMOUTTAYR':
        raise SyntaxError("Loop must end with IM OUTTA YR")

    if i + 1 >= len(token) or token[i + 1] != 'VAR':
        raise SyntaxError("IM OUTTA YR must be followed by a loop name")

    if lexeme[i + 1] != loop_name:
        raise SyntaxError("Loop closing name does not match")

    return i + 2
# -----------------------------------------------------
# -----------------------------------------------------

# FOUNDYR HELPER
# -----------------------------------------------------
def foundyr_helper(token, i):
    i += 1

    if i >= len(token) or token[i] in ('NEWLINE', 'IFUSAYSO'):
        raise SyntaxError("FOUND YR must be followed by a value")

    if token[i] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
        return arithmetic_helper(token, i)
    elif token[i] in ('BOTHSAEM', 'DIFFRINT'):
        return comparison_helper(token, i)
    elif token[i] in ('BOTHOF', 'EITHER', 'WONOF'):
        return boolean_helper(token, i)
    elif token[i] == 'NOT':
        return not_helper(token, i)
    elif token[i] in ('ALLOF', 'ANYOF'):
        return infinite_boolean_helper(token, i)
    elif token[i] == 'SMOOSH':
        return smoosh_helper(token, i)
    elif token[i] == 'MAEK':
        return typecasting_helper(token, i)
    elif token[i] == 'IIZ':
        return function_call_helper(token, i)
    elif token[i] in ('NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB', 'VAR'):
        return i + 1

    raise SyntaxError("Invalid return value")
# -----------------------------------------------------

# FUNCTION HELPER
# -----------------------------------------------------
def function_helper(token, lexeme, i):
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

    i = block_helper(token, lexeme, i, ('IFUSAYSO',), "function")

    if i >= len(token) or token[i] != 'IFUSAYSO':
        raise SyntaxError("Function must end with IF U SAY SO")

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
            elif token[i] == 'IIZ':
                i = function_call_helper(token, i)
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