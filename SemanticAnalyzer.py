# the syntax analyzer checks if the code is written in the right ORDER
# (example: I HAS A must be followed by a variable name)

# the semantic analyzer checks if the code MAKES SENSE
# (example: you cannot use a variable that was never declared)

# to do this, we keep a dictionary called "symbols"
#   key   = variable name   (example: 'age')
#   value = variable type   (example: 'NUM') 


# -----------------------------------------------------
# ERROR CLASS
# -----------------------------------------------------
# our own error so we can tell semantic errors apart from syntax errors
class SemanticError(Exception):
    pass
# -----------------------------------------------------


# -----------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------
def semantic(token, lexeme):

    # dictionary that stores declared variables and their types
    symbols = {}

    # start after HAI
    i = 1

    # -----------------------------------------------------
    # loop through all tokens until KTHXBYE
    while i < len(token) - 1:

        # skip newlines
        if token[i] == 'NEWLINE':
            i += 1

        # variable declaration block
        elif token[i] == 'WAZZUP':
            i = wazzup_helper(token, lexeme, i, symbols)

        # variable declaration
        elif token[i] == 'VARDEC':
            i = vardec_helper(token, lexeme, i, symbols)

        # output statement
        elif token[i] == 'PRINT':
            i = print_helper(token, lexeme, i, symbols)

        # if-else conditional
        elif token[i] == 'ORLY':
            i = orly_helper(token, lexeme, i, symbols)

        # switch-case conditional
        elif token[i] == 'WTF':
            i = wtf_helper(token, lexeme, i, symbols)

        # input statement
        elif token[i] == 'GIMMEH':
            i = input_helper(token, lexeme, i, symbols)

        # variable at the start of a line
        elif token[i] == 'VAR':
            # assignment (x R 5)
            if i + 1 < len(token) and token[i + 1] == 'R':
                i = assign_helper(token, lexeme, i, symbols)

            # variable alone on a line, just make sure it exists
            else:
                get_operand_type(token, lexeme, i, symbols)
                i += 1

        # other statements will be added here in the next bits
        # for now, just move to the next token
        else:
            i += 1
    # -----------------------------------------------------

    return symbols

# -----------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------

# GET OPERAND TYPE HELPER
# -----------------------------------------------------
def get_operand_type(token, lexeme, index, symbols):

    if token[index] == 'VAR':
        var_name = lexeme[index]

        if var_name not in symbols:
            raise SemanticError("Variable " + var_name + " is not declared")

        return symbols[var_name]

    else:
        return token[index]
# -----------------------------------------------------

# VARDEC HELPER
# -----------------------------------------------------
def vardec_helper(token, lexeme, i, symbols):

    # the variable name comes right after I HAS A
    var_name = lexeme[i + 1]

    # rule 1: no declaring the same variable twice
    if var_name in symbols:
        raise SemanticError("Variable " + var_name + " is already declared")

    # if there is no ITZ, the variable has no value yet (NOOB)
    var_type = 'NOOB'

    # move past I HAS A and the variable name
    i += 2

    # check if there is an ITZ
    if i < len(token) and token[i] == 'ASSIGN':

        # simple value after ITZ (a literal or another variable)
        if token[i + 1] in ('NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB', 'VAR'):
            # rule 2 is checked inside get_operand_type
            var_type = get_operand_type(token, lexeme, i + 1, symbols)
            i += 2

        # arithmetic after ITZ (SUM OF a AN b)
        elif token[i + 1] in ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'):
            var_type = arithmetic_helper(token, lexeme, i + 1, symbols)
            # move past: ITZ, operator, first value, AN, second value
            i += 5

        # comparison after ITZ (BOTH SAEM a AN b)
        elif token[i + 1] in ('BOTHSAEM', 'DIFFRINT'):
            var_type = comparison_helper(token, lexeme, i + 1, symbols)
            # move past: ITZ, operator, first value, AN, second value
            i += 5

        # boolean after ITZ (BOTH OF a AN b, EITHER OF a AN b, WON OF a AN b)
        elif token[i + 1] in ('BOTHOF', 'EITHER', 'WONOF'):
            var_type = boolean_helper(token, lexeme, i + 1, symbols)
            # move past: ITZ, operator, first value, AN, second value
            i += 5

        # NOT after ITZ (NOT a)
        elif token[i + 1] == 'NOT':
            var_type = not_helper(token, lexeme, i + 1, symbols)
            # move past: ITZ, NOT, value
            i += 3

        # infinite boolean after ITZ (ALL OF a AN b MKAY, ANY OF a AN b MKAY)
        elif token[i + 1] in ('ALLOF', 'ANYOF'):
            var_type = 'TROOF'
            i = infinite_boolean_helper(token, lexeme, i + 1, symbols)

        else:
            i += 1

    # save the variable AFTER checking the value
    # (so "I HAS A x ITZ x" correctly says x is not declared)
    symbols[var_name] = var_type

    return i
# -----------------------------------------------------

# WAZZUP HELPER
# -----------------------------------------------------
def wazzup_helper(token, lexeme, i, symbols):

    # move past WAZZUP
    i += 1

    while i < len(token) and token[i] != 'BUHBYE':

        if token[i] == 'VARDEC':
            i = vardec_helper(token, lexeme, i, symbols)

        # skip newlines (and anything else, the syntax analyzer already checked it)
        else:
            i += 1

    # move past BUHBYE
    return i + 1
# -----------------------------------------------------

# ASSIGNMENT HELPER
# -----------------------------------------------------
def assign_helper(token, lexeme, i, symbols):

    var_name = lexeme[i]

    # rule 1: left side must be declared
    get_operand_type(token, lexeme, i, symbols)

    # rule 2: right side (comes after R) is checked inside get_operand_type
    new_type = get_operand_type(token, lexeme, i + 2, symbols)

    # update the type of the variable
    symbols[var_name] = new_type

    # move past: variable, R, value
    return i + 3
# -----------------------------------------------------

# PRINT HELPER
# -----------------------------------------------------
def print_helper(token, lexeme, i, symbols):

    # move past VISIBLE
    i += 1

    while i < len(token) and token[i] in ('VAR', 'NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB'):

        if token[i] == 'VAR':
            get_operand_type(token, lexeme, i, symbols)

        i += 1

    return i
# -----------------------------------------------------

# INPUT HELPER
# -----------------------------------------------------
def input_helper(token, lexeme, i, symbols):

    var_name = lexeme[i + 1]

    # variable must be declared
    get_operand_type(token, lexeme, i + 1, symbols)

    # user input is text
    symbols[var_name] = 'YARN'

    # move past: GIMMEH, variable
    return i + 2
# -----------------------------------------------------

# ARITHMETIC HELPER
# -----------------------------------------------------
def arithmetic_helper(token, lexeme, i, symbols):

    operator = lexeme[i]

    # the values are at i + 1 and i + 3 (i + 2 is AN)
    first_type = get_operand_type(token, lexeme, i + 1, symbols)
    second_type = get_operand_type(token, lexeme, i + 3, symbols)

    # check the first value
    if first_type not in ('NUM', 'NUMBAR', 'YARN'):
        raise SemanticError(operator + " cannot use a " + first_type + " value (" + lexeme[i + 1] + ")")

    # check the second value
    if second_type not in ('NUM', 'NUMBAR', 'YARN'):
        raise SemanticError(operator + " cannot use a " + second_type + " value (" + lexeme[i + 3] + ")")

    # decide the type of the answer
    if first_type == 'NUMBAR' or second_type == 'NUMBAR':
        return 'NUMBAR'
    else:
        return 'NUM'
# -----------------------------------------------------

# COMPARISON HELPER
# -----------------------------------------------------
# checks BOTH SAEM a AN b and DIFFRINT a AN b
#   both values must be numbers or YARN (same rule as arithmetic)
#   the answer of a comparison is always WIN or FAIL, so it gives back TROOF
def comparison_helper(token, lexeme, i, symbols):

    operator = lexeme[i]

    # the values are at i + 1 and i + 3 (i + 2 is AN)
    first_type = get_operand_type(token, lexeme, i + 1, symbols)
    second_type = get_operand_type(token, lexeme, i + 3, symbols)

    # check the first value
    if first_type not in ('NUM', 'NUMBAR', 'YARN'):
        raise SemanticError(operator + " cannot use a " + first_type + " value (" + lexeme[i + 1] + ")")

    # check the second value
    if second_type not in ('NUM', 'NUMBAR', 'YARN'):
        raise SemanticError(operator + " cannot use a " + second_type + " value (" + lexeme[i + 3] + ")")

    # a comparison always answers WIN or FAIL
    return 'TROOF'
# -----------------------------------------------------

# BOOLEAN HELPER
# -----------------------------------------------------
# checks BOTH OF a AN b, EITHER OF a AN b, WON OF a AN b
#   both values must be TROOF (WIN or FAIL)
def boolean_helper(token, lexeme, i, symbols):

    operator = lexeme[i]

    # the values are at i + 1 and i + 3 (i + 2 is AN)
    first_type = get_operand_type(token, lexeme, i + 1, symbols)
    second_type = get_operand_type(token, lexeme, i + 3, symbols)

    # check the first value
    if first_type != 'TROOF':
        raise SemanticError(operator + " requires a TROOF value, got " + first_type + " (" + lexeme[i + 1] + ")")

    # check the second value
    if second_type != 'TROOF':
        raise SemanticError(operator + " requires a TROOF value, got " + second_type + " (" + lexeme[i + 3] + ")")

    return 'TROOF'
# -----------------------------------------------------

# NOT HELPER
# -----------------------------------------------------
# checks NOT a
#   the value after NOT must be TROOF (WIN or FAIL)
def not_helper(token, lexeme, i, symbols):

    operand_type = get_operand_type(token, lexeme, i + 1, symbols)

    if operand_type != 'TROOF':
        raise SemanticError("NOT requires a TROOF value, got " + operand_type + " (" + lexeme[i + 1] + ")")

    return 'TROOF'
# -----------------------------------------------------

# INFINITE BOOLEAN HELPER
# -----------------------------------------------------
# checks ALL OF a AN b AN c MKAY and ANY OF a AN b MKAY
#   every value before MKAY must be TROOF (WIN or FAIL)
def infinite_boolean_helper(token, lexeme, i, symbols):

    operator = lexeme[i]

    # move past ALL OF / ANY OF to the first operand
    i += 1

    # check the first operand
    first_type = get_operand_type(token, lexeme, i, symbols)
    if first_type != 'TROOF':
        raise SemanticError(operator + " requires a TROOF value, got " + first_type + " (" + lexeme[i] + ")")

    i += 1

    # check all remaining operands separated by AN
    while i < len(token) and token[i] == 'AN':
        # move past AN to the next operand
        i += 1

        next_type = get_operand_type(token, lexeme, i, symbols)
        if next_type != 'TROOF':
            raise SemanticError(operator + " requires a TROOF value, got " + next_type + " (" + lexeme[i] + ")")

        i += 1

    # move past MKAY
    return i + 1
# -----------------------------------------------------

# ORLY HELPER
# -----------------------------------------------------
# checks statements inside O RLY? ... YA RLY ... NO WAI ... OIC
def orly_helper(token, lexeme, i, symbols):

    # move past O RLY?
    i += 1

    while i < len(token) and token[i] != 'OIC':

        if token[i] == 'PRINT':
            i = print_helper(token, lexeme, i, symbols)

        elif token[i] == 'VAR':
            i = assign_helper(token, lexeme, i, symbols)

        # skip NEWLINE, YARLY, NOWAI
        else:
            i += 1

    # move past OIC
    return i + 1
# -----------------------------------------------------

# WTF HELPER
# -----------------------------------------------------
# checks statements inside WTF? ... OMG ... OMGWTF ... OIC
def wtf_helper(token, lexeme, i, symbols):

    # move past WTF?
    i += 1

    # keep track of OMG values so the same case is not used twice
    seen_omg = []

    while i < len(token) and token[i] != 'OIC':

        if token[i] == 'OMG':
            case_value = lexeme[i + 1]

            if case_value in seen_omg:
                raise SemanticError("Duplicate OMG value " + case_value)

            seen_omg.append(case_value)
            # move past OMG and its value
            i += 2

        elif token[i] == 'PRINT':
            i = print_helper(token, lexeme, i, symbols)

        elif token[i] == 'VAR':
            i = assign_helper(token, lexeme, i, symbols)

        # skip NEWLINE, OMGWTF, GTFO
        else:
            i += 1

    # move past OIC
    return i + 1
# -----------------------------------------------------

