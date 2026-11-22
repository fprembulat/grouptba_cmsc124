# the syntax analyzer checks if the code is written in the right ORDER
# (example: I HAS A must be followed by a variable name)

# the semantic analyzer checks if the code MAKES SENSE
# (example: you cannot use a variable that was never declared)

# to do this, we keep a dictionary called "symbols"
#   key   = variable name   (example: 'age')
#   value = variable type   (example: 'NUM')
# and a dictionary called "functions"
#   key   = function name   (example: 'addNumbers')
#   value = (parameter list, body start index, return type)


# -----------------------------------------------------
# ERROR CLASS
# -----------------------------------------------------
# our own error so we can tell semantic errors apart from syntax errors
class SemanticError(Exception):
    pass
# -----------------------------------------------------


# -----------------------------------------------------
# TOKEN GROUPS
# -----------------------------------------------------
ARITH_OPS = ('SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR')
CMP_OPS = ('BOTHSAEM', 'DIFFRINT')
BOOL_OPS = ('BOTHOF', 'EITHER', 'WONOF')
INF_OPS = ('ALLOF', 'ANYOF')
LITERALS = ('NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB')

EXPR_TOKENS = (
    LITERALS
    + ('VAR', 'NOT', 'SMOOSH', 'MAEK', 'IIZ')
    + ARITH_OPS
    + CMP_OPS
    + BOOL_OPS
    + INF_OPS
)
# -----------------------------------------------------


# -----------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------
def semantic(token, lexeme):

    # dictionary that stores declared variables and their types
    # IT always exists in LOLCODE and starts as NOOB
    symbols = {'IT': 'NOOB'}

    # dictionary that stores defined functions
    functions = {}

    # start after HAI
    i = 1

    # -----------------------------------------------------
    # loop through all tokens until KTHXBYE
    while i < len(token) - 1:
        i = statement_helper(token, lexeme, i, symbols, functions)
    # -----------------------------------------------------

    return symbols


# -----------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------

# STATEMENT HELPER
# -----------------------------------------------------
# checks one statement starting at index i and gives back the next index
def statement_helper(token, lexeme, i, symbols, functions):

    # skip newlines and single-line comments
    if token[i] in ('NEWLINE', 'BTW'):
        return i + 1

    # skip multiline comments if still present
    elif token[i] == 'OBTW':
        while i < len(token) and token[i] != 'TLDR':
            i += 1
        return i + 1

    # variable declaration block 
    elif token[i] == 'WAZZUP':
        return wazzup_helper(token, lexeme, i, symbols, functions)

    # variable declaration
    elif token[i] == 'VARDEC':
        return vardec_helper(token, lexeme, i, symbols, functions)

    # output statement
    elif token[i] == 'PRINT':
        return print_helper(token, lexeme, i, symbols, functions)

    # if-else conditional
    elif token[i] == 'ORLY':
        return orly_helper(token, lexeme, i, symbols, functions)

    # switch-case conditional
    elif token[i] == 'WTF':
        return wtf_helper(token, lexeme, i, symbols, functions)

    # loop statement
    elif token[i] == 'IMINYR':
        return loop_helper(token, lexeme, i, symbols, functions)

    # function definition
    elif token[i] == 'HOWIZI':
        return function_helper(token, lexeme, i, symbols, functions)

    # function return (FOUND YR <expr>)
    elif token[i] == 'FOUNDYR':
        ret_type, i = get_operand_type(token, lexeme, i + 1, symbols, functions)
        symbols['IT'] = ret_type
        return i

    # break statement
    elif token[i] == 'GTFO':
        return i + 1

    # input statement
    elif token[i] == 'GIMMEH':
        return input_helper(token, lexeme, i, symbols)

    # variable at the start of a line
    elif token[i] == 'VAR':
        # assignment (x R 5)
        if i + 1 < len(token) and token[i + 1] == 'R':
            return assign_helper(token, lexeme, i, symbols, functions)

        # typecasting (x IS NOW A NUMBR)
        elif i + 1 < len(token) and token[i + 1] == 'ISNOWA':
            return isnowa_helper(token, lexeme, i, symbols)

        # variable alone on a line, make sure it exists and save its type in IT
        else:
            var_type, i = get_operand_type(token, lexeme, i, symbols, functions)
            symbols['IT'] = var_type
            return i

    # standalone expression (example: BOTH SAEM x AN 10, I IZ sayHello MKAY)
    # the result of a standalone expression is stored in IT
    elif token[i] in EXPR_TOKENS:
        expr_type, i = get_operand_type(token, lexeme, i, symbols, functions)
        symbols['IT'] = expr_type
        return i

    else:
        return i + 1
# -----------------------------------------------------

# GET OPERAND TYPE HELPER
# -----------------------------------------------------
# checks one value or nested expression starting at index
# gives back (value_type, next_index)
def get_operand_type(token, lexeme, index, symbols, functions=None):

    if functions is None:
        functions = {}

    tok = token[index]

    # variable
    if tok == 'VAR':
        var_name = lexeme[index]

        if var_name not in symbols:
            raise SemanticError("Variable " + var_name + " is not declared")

        return symbols[var_name], index + 1

    # literal value (NUM, NUMBAR, YARN, TROOF, NOOB)
    elif tok in LITERALS:
        return tok, index + 1

    # arithmetic expression (SUM OF a AN b, ...)
    elif tok in ARITH_OPS:
        return arithmetic_helper(token, lexeme, index, symbols, functions)

    # comparison expression (BOTH SAEM a AN b, DIFFRINT a AN b)
    elif tok in CMP_OPS:
        return comparison_helper(token, lexeme, index, symbols, functions)

    # boolean expression (BOTH OF a AN b, EITHER OF a AN b, WON OF a AN b)
    elif tok in BOOL_OPS:
        return boolean_helper(token, lexeme, index, symbols, functions)

    # NOT expression (NOT a)
    elif tok == 'NOT':
        return not_helper(token, lexeme, index, symbols, functions)

    # infinite boolean expression (ALL OF ... MKAY, ANY OF ... MKAY)
    elif tok in INF_OPS:
        return infinite_boolean_helper(token, lexeme, index, symbols, functions)

    # string concatenation (SMOOSH a AN b ...)
    elif tok == 'SMOOSH':
        return smoosh_helper(token, lexeme, index, symbols, functions)

    # explicit typecast (MAEK a [A] <type>)
    elif tok == 'MAEK':
        return typecasting_helper(token, lexeme, index, symbols, functions)

    # function call (I IZ func [YR a [AN YR b ...]] MKAY)
    elif tok == 'IIZ':
        return function_call_helper(token, lexeme, index, symbols, functions)

    else:
        return tok, index + 1
# -----------------------------------------------------

# CONVERT TYPE NAME HELPER
# -----------------------------------------------------
# converts a LOLCODE type keyword (like NUMBR) into the token type name we store ('NUM')
def normalize_type(type_lexeme):

    if type_lexeme == 'NUMBR':
        return 'NUM'

    return type_lexeme
# -----------------------------------------------------

# VARDEC HELPER
# -----------------------------------------------------
def vardec_helper(token, lexeme, i, symbols, functions=None):

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

        # ITZ A <type> (example: I HAS A x ITZ A NUMBR)
        if i + 1 < len(token) and token[i + 1] == 'A':
            var_type = normalize_type(lexeme[i + 2])
            i += 3

        # any value or expression after ITZ
        else:
            var_type, i = get_operand_type(token, lexeme, i + 1, symbols, functions)

    # save the variable AFTER checking the value
    # (so "I HAS A x ITZ x" correctly says x is not declared)
    symbols[var_name] = var_type

    return i
# -----------------------------------------------------

# WAZZUP HELPER
# -----------------------------------------------------
def wazzup_helper(token, lexeme, i, symbols, functions=None):

    # move past WAZZUP
    i += 1

    while i < len(token) and token[i] != 'BUHBYE':

        if token[i] == 'VARDEC':
            i = vardec_helper(token, lexeme, i, symbols, functions)

        # skip newlines (and anything else, the syntax analyzer already checked it)
        else:
            i += 1

    # move past BUHBYE
    return i + 1
# -----------------------------------------------------

# ASSIGNMENT HELPER
# -----------------------------------------------------
def assign_helper(token, lexeme, i, symbols, functions=None):

    var_name = lexeme[i]

    # rule 1: left side must be declared
    get_operand_type(token, lexeme, i, symbols, functions)

    # handles function calls on the right side of R
    if token[i + 2] == 'IIZ':
        symbols[var_name] = 'NOOB'
        while i < len(token) and token[i] != 'MKAY':
            i += 1
        return i + 1

    # rule 2: right side (comes after R) is checked inside get_operand_type
    new_type = get_operand_type(token, lexeme, i + 2, symbols)

    # update the type of the variable
    symbols[var_name] = new_type

    return next_i
# -----------------------------------------------------

# ISNOWA HELPER
# -----------------------------------------------------
# checks <variable> IS NOW A <type>
def isnowa_helper(token, lexeme, i, symbols):

    var_name = lexeme[i]

    # variable must be declared before typecasting it
    get_operand_type(token, lexeme, i, symbols)

    # update the variable's type
    symbols[var_name] = normalize_type(lexeme[i + 2])

    # move past: variable, IS NOW A, type
    return i + 3
# -----------------------------------------------------

# PRINT HELPER
# -----------------------------------------------------
# checks VISIBLE <expr> [+ <expr> ...]
def print_helper(token, lexeme, i, symbols, functions=None):

    # move past VISIBLE
    i += 1

    while i < len(token) and token[i] != 'NEWLINE' and token[i] != 'END':

        if token[i] == 'PLUS':
            i += 1
            continue

        if token[i] in EXPR_TOKENS:
            _, i = get_operand_type(token, lexeme, i, symbols, functions)
        else:
            break

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
def arithmetic_helper(token, lexeme, i, symbols, functions=None):

    operator = lexeme[i]
    op_token = token[i]

    # read the first operand (starts at i + 1)
    first_index = i + 1
    first_type, next_i = get_operand_type(token, lexeme, first_index, symbols, functions)

    # move past AN
    if next_i < len(token) and token[next_i] == 'AN':
        next_i += 1

    # read the second operand
    second_index = next_i
    second_type, next_i = get_operand_type(token, lexeme, second_index, symbols, functions)

    # check the first value
    if first_type not in ('NUM', 'NUMBAR', 'YARN', 'ANY'):
        raise SemanticError(operator + " cannot use a " + first_type + " value (" + lexeme[first_index] + ")")
    if first_type == 'YARN':
        check_yarn_is_number(token, lexeme, first_index, operator)

    # check the second value
    if second_type not in ('NUM', 'NUMBAR', 'YARN', 'ANY'):
        raise SemanticError(operator + " cannot use a " + second_type + " value (" + lexeme[second_index] + ")")
    if second_type == 'YARN':
        check_yarn_is_number(token, lexeme, second_index, operator)

    # check division by zero for QUOSHUNT OF and MOD OF when the second value is a literal 0
    if op_token in ('QUOSHUNT', 'MOD') and token[second_index] in ('NUM', 'NUMBAR'):
        if float(lexeme[second_index]) == 0:
            raise SemanticError(operator + " cannot divide by zero")

    # decide the type of the answer
    if first_type == 'NUMBAR' or second_type == 'NUMBAR':
        return 'NUMBAR', next_i
    else:
        return 'NUM', next_i
# -----------------------------------------------------

# CHECK YARN IS NUMBER HELPER
# -----------------------------------------------------
# checks if a YARN used in math actually contains digits (like "12" or "3.5")
# if it contains letters (like "hi"), float() fails and we catch the ValueError
def check_yarn_is_number(token, lexeme, index, operator):

    # if the token itself is a YARN literal
    if token[index] == 'YARN':
        yarn_value = lexeme[index]

    # if it is a variable holding a YARN, find the value assigned to it
    elif token[index] == 'VAR':
        var_name = lexeme[index]
        yarn_value = None

        j = 0
        while j < index:
            # from: I HAS A s ITZ "hi"
            if token[j] == 'VARDEC' and lexeme[j + 1] == var_name and j + 3 < len(token) and token[j + 2] == 'ASSIGN':
                yarn_value = lexeme[j + 3]

            # from: s R "hi"
            elif token[j] == 'VAR' and lexeme[j] == var_name and j + 2 < len(token) and token[j + 1] == 'R':
                yarn_value = lexeme[j + 2]

            j += 1
    else:
        yarn_value = None

    # if we found the string value (like '"hi"' or '"12"'), test if it is a number
    if yarn_value is not None and yarn_value.startswith('"'):
        # remove the double quotes around the string
        text = yarn_value.strip('"')

        try:
            float(text)
        except ValueError:
            raise SemanticError(operator + " cannot convert YARN " + yarn_value + " to a number")
# -----------------------------------------------------

# COMPARISON HELPER
# -----------------------------------------------------
# checks BOTH SAEM a AN b and DIFFRINT a AN b
#   both values must be numbers or YARN (same rule as arithmetic)
#   the answer of a comparison is always WIN or FAIL, so it gives back TROOF
def comparison_helper(token, lexeme, i, symbols, functions=None):

    operator = lexeme[i]

    # read the first operand
    first_index = i + 1
    first_type, next_i = get_operand_type(token, lexeme, first_index, symbols, functions)

    # move past AN
    if next_i < len(token) and token[next_i] == 'AN':
        next_i += 1

    # read the second operand
    second_index = next_i
    second_type, next_i = get_operand_type(token, lexeme, second_index, symbols, functions)

    # check the first value
    if first_type not in ('NUM', 'NUMBAR', 'YARN', 'ANY'):
        raise SemanticError(operator + " cannot use a " + first_type + " value (" + lexeme[first_index] + ")")

    # check the second value
    if second_type not in ('NUM', 'NUMBAR', 'YARN', 'ANY'):
        raise SemanticError(operator + " cannot use a " + second_type + " value (" + lexeme[second_index] + ")")

    # a comparison always answers WIN or FAIL
    return 'TROOF', next_i
# -----------------------------------------------------

# BOOLEAN HELPER
# -----------------------------------------------------
# checks BOTH OF a AN b, EITHER OF a AN b, WON OF a AN b
#   both values must be TROOF (WIN or FAIL)
def boolean_helper(token, lexeme, i, symbols, functions=None):

    operator = lexeme[i]

    # read the first operand
    first_index = i + 1
    first_type, next_i = get_operand_type(token, lexeme, first_index, symbols, functions)

    # move past AN
    if next_i < len(token) and token[next_i] == 'AN':
        next_i += 1

    # read the second operand
    second_index = next_i
    second_type, next_i = get_operand_type(token, lexeme, second_index, symbols, functions)

    # check the first value
    if first_type not in ('TROOF', 'ANY'):
        raise SemanticError(operator + " requires a TROOF value, got " + first_type + " (" + lexeme[first_index] + ")")

    # check the second value
    if second_type not in ('TROOF', 'ANY'):
        raise SemanticError(operator + " requires a TROOF value, got " + second_type + " (" + lexeme[second_index] + ")")

    return 'TROOF', next_i
# -----------------------------------------------------

# NOT HELPER
# -----------------------------------------------------
# checks NOT a
#   the value after NOT must be TROOF (WIN or FAIL)
def not_helper(token, lexeme, i, symbols, functions=None):

    operand_index = i + 1
    operand_type, next_i = get_operand_type(token, lexeme, operand_index, symbols, functions)

    if operand_type not in ('TROOF', 'ANY'):
        raise SemanticError("NOT requires a TROOF value, got " + operand_type + " (" + lexeme[operand_index] + ")")

    return 'TROOF', next_i
# -----------------------------------------------------

# INFINITE BOOLEAN HELPER
# -----------------------------------------------------
# checks ALL OF a AN b AN c MKAY and ANY OF a AN b MKAY
#   every value before MKAY must be TROOF (WIN or FAIL)
def infinite_boolean_helper(token, lexeme, i, symbols, functions=None):

    operator = lexeme[i]

    # move past ALL OF / ANY OF to the first operand
    i += 1

    # check the first operand
    op_index = i
    first_type, i = get_operand_type(token, lexeme, op_index, symbols, functions)
    if first_type not in ('TROOF', 'ANY'):
        raise SemanticError(operator + " requires a TROOF value, got " + first_type + " (" + lexeme[op_index] + ")")

    # check all remaining operands separated by AN
    while i < len(token) and token[i] == 'AN':
        # move past AN to the next operand
        i += 1

        op_index = i
        next_type, i = get_operand_type(token, lexeme, op_index, symbols, functions)
        if next_type not in ('TROOF', 'ANY'):
            raise SemanticError(operator + " requires a TROOF value, got " + next_type + " (" + lexeme[op_index] + ")")

    # move past MKAY
    if i < len(token) and token[i] == 'MKAY':
        i += 1

    return 'TROOF', i
# -----------------------------------------------------

# SMOOSH HELPER
# -----------------------------------------------------
# checks SMOOSH a AN b AN c
#   joins all values into one string, so the answer is always YARN
def smoosh_helper(token, lexeme, i, symbols, functions=None):

    # move past SMOOSH to the first value
    i += 1
    _, i = get_operand_type(token, lexeme, i, symbols, functions)

    # check all remaining values separated by AN
    while i < len(token) and token[i] == 'AN':
        i += 1
        _, i = get_operand_type(token, lexeme, i, symbols, functions)

    return 'YARN', i
# -----------------------------------------------------

# TYPECASTING HELPER
# -----------------------------------------------------
# checks MAEK <value> [A] <type>
def typecasting_helper(token, lexeme, i, symbols, functions=None):

    # check the value after MAEK
    _, i = get_operand_type(token, lexeme, i + 1, symbols, functions)

    # skip optional A
    if i < len(token) and token[i] == 'A':
        i += 1

    target_type = normalize_type(lexeme[i])

    # move past the target type
    return target_type, i + 1
# -----------------------------------------------------

# ORLY HELPER
# -----------------------------------------------------
# checks statements inside O RLY? ... YA RLY ... [MEBBE <cond> ...] [NO WAI ...] OIC
def orly_helper(token, lexeme, i, symbols, functions=None):

    # move past O RLY?
    i += 1

    while i < len(token) and token[i] != 'OIC':

        if token[i] in ('NEWLINE', 'YARLY', 'NOWAI'):
            i += 1

        # MEBBE must be followed by a condition expression
        elif token[i] == 'MEBBE':
            _, i = get_operand_type(token, lexeme, i + 1, symbols, functions)

        else:
            i = statement_helper(token, lexeme, i, symbols, functions)

    # move past OIC
    return i + 1
# -----------------------------------------------------

# WTF HELPER
# -----------------------------------------------------
# checks statements inside WTF? ... OMG ... OMGWTF ... OIC
def wtf_helper(token, lexeme, i, symbols, functions=None):

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

        elif token[i] in ('NEWLINE', 'OMGWTF', 'GTFO'):
            i += 1

        else:
            i = statement_helper(token, lexeme, i, symbols, functions)

    # move past OIC
    return i + 1
# -----------------------------------------------------

# LOOP HELPER
# -----------------------------------------------------
# checks IM IN YR <label> UPPIN/NERFIN YR <var> [TIL/WILE <cond>] ... IM OUTTA YR <label>
def loop_helper(token, lexeme, i, symbols, functions=None):

    # loop name comes after IM IN YR
    loop_name = lexeme[i + 1]

    # operation (UPPIN or NERFIN) is at i + 2, YR is at i + 3, counter variable is at i + 4
    operator = lexeme[i + 2]
    var_index = i + 4
    var_type, _ = get_operand_type(token, lexeme, var_index, symbols, functions)

    # counter variable must be a number (or numeric YARN) so UPPIN/NERFIN can add/subtract 1
    if var_type not in ('NUM', 'NUMBAR', 'YARN', 'ANY'):
        raise SemanticError(operator + " cannot use a " + var_type + " value (" + lexeme[var_index] + ")")
    if var_type == 'YARN':
        check_yarn_is_number(token, lexeme, var_index, operator)

    # move past IM IN YR, label, UPPIN/NERFIN, YR, variable
    i += 5

    # optional TIL / WILE condition
    if i < len(token) and token[i] in ('TIL', 'WILE'):
        _, i = get_operand_type(token, lexeme, i + 1, symbols, functions)
    elif i < len(token) and token[i] != 'NEWLINE':
        _, i = get_operand_type(token, lexeme, i, symbols, functions)

    # check statements inside the loop until IM OUTTA YR
    while i < len(token) and token[i] != 'IMOUTTAYR':
        i = statement_helper(token, lexeme, i, symbols, functions)

    # check closing loop name
    if i + 1 < len(token) and lexeme[i + 1] != loop_name:
        raise SemanticError("Loop closing name " + lexeme[i + 1] + " does not match " + loop_name)

    # move past IM OUTTA YR and the closing loop name
    return i + 2
# -----------------------------------------------------

# FUNCTION HELPER
# -----------------------------------------------------
# checks HOW IZ I <name> [YR <param> [AN YR <param> ...]] ... IF U SAY SO
def function_helper(token, lexeme, i, symbols, functions):

    func_name = lexeme[i + 1]

    # rule 1: no defining the same function twice
    if func_name in functions:
        raise SemanticError("Function " + func_name + " is already defined")

    # move past HOW IZ I and function name
    i += 2

    # read parameters
    params = []
    while i < len(token) and token[i] == 'YR':
        param_name = lexeme[i + 1]
        if param_name in params:
            raise SemanticError("Parameter " + param_name + " is already declared")
        params.append(param_name)
        i += 2

        if i < len(token) and token[i] == 'AN':
            i += 1

    body_start = i

    # check the function body using a local symbol table with its parameters
    local_symbols = {'IT': 'NOOB'}
    for param in params:
        local_symbols[param] = 'ANY'

    return_type = 'NOOB'
    while i < len(token) and token[i] != 'IFUSAYSO':
        if token[i] == 'FOUNDYR':
            return_type, i = get_operand_type(token, lexeme, i + 1, local_symbols, functions)
            local_symbols['IT'] = return_type
        else:
            i = statement_helper(token, lexeme, i, local_symbols, functions)

    # save the function so I IZ calls can check it
    functions[func_name] = (params, body_start, return_type)

    # move past IF U SAY SO
    return i + 1
# -----------------------------------------------------

# FUNCTION CALL HELPER
# -----------------------------------------------------
# checks I IZ <name> [YR <arg> [AN YR <arg> ...]] MKAY
def function_call_helper(token, lexeme, i, symbols, functions):

    func_name = lexeme[i + 1]

    # move past I IZ and function name
    i += 2

    # check all arguments passed with YR
    arg_types = []
    while i < len(token) and token[i] == 'YR':
        arg_type, i = get_operand_type(token, lexeme, i + 1, symbols, functions)
        arg_types.append(arg_type)

        if i < len(token) and token[i] == 'AN':
            i += 1

    # move past MKAY
    if i < len(token) and token[i] == 'MKAY':
        i += 1

    # rule 1: function must be defined before calling it
    if func_name not in functions:
        raise SemanticError("Function " + func_name + " is not defined")

    params, body_start, return_type = functions[func_name]

    # rule 2: argument count must match parameter count
    if len(arg_types) != len(params):
        raise SemanticError(
            "Function " + func_name + " expects " + str(len(params))
            + " argument(s), got " + str(len(arg_types))
        )

    # check the function body with the actual argument types to get the exact return type
    call_symbols = {'IT': 'NOOB'}
    for param, arg_type in zip(params, arg_types):
        call_symbols[param] = arg_type

    j = body_start
    call_return = return_type
    while j < len(token) and token[j] != 'IFUSAYSO':
        if token[j] == 'FOUNDYR':
            call_return, j = get_operand_type(token, lexeme, j + 1, call_symbols, functions)
            call_symbols['IT'] = call_return
        else:
            j = statement_helper(token, lexeme, j, call_symbols, functions)

    return call_return, i
# -----------------------------------------------------
