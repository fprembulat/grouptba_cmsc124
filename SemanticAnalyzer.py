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

        # expressions (SUM OF, BOTH SAEM, BOTH OF, ...) will be added in the next bits
        # for now, just move past ITZ
        else:
            i += 1

    # save the variable AFTER checking the value
    # (so "I HAS A x ITZ x" correctly says x is not declared)
    symbols[var_name] = var_type

    return i
# -----------------------------------------------------

# WAZZUP HELPER
# -----------------------------------------------------
# checks every declaration between WAZZUP and BUHBYE

# i starts at WAZZUP
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

