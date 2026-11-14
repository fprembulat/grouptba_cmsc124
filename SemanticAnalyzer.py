# file for semantic analyzer
#
# the syntax analyzer checks if the code is written in the right ORDER
# (example: I HAS A must be followed by a variable name)
#
# the semantic analyzer checks if the code MAKES SENSE
# (example: you cannot use a variable that was never declared)
#
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
    # (no need to check HAI and KTHXBYE again, the syntax analyzer already did that)
    i = 1

    # -----------------------------------------------------
    # loop through all tokens until KTHXBYE
    while i < len(token) - 1:

        # skip newlines
        if token[i] == 'NEWLINE':
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
# gives back the type of the value found at token[index]
#   - if it is a variable, check that it is declared,
#     then give back the type saved in symbols
#   - if it is a literal (NUM, NUMBAR, YARN, TROOF, NOOB),
#     the token itself is already the type
def get_operand_type(token, lexeme, index, symbols):

    if token[index] == 'VAR':
        var_name = lexeme[index]

        if var_name not in symbols:
            raise SemanticError("Variable " + var_name + " is not declared")

        return symbols[var_name]

    else:
        return token[index]
# -----------------------------------------------------

