# THE INTERPRETER RUNS A PROGRAM AFTER IT PASSED THE SYNTAX AND SEMANTIC ANALYZERS

import math
import re
from decimal import Decimal, ROUND_DOWN, InvalidOperation

NUMBAR_DECIMALS = 2         # a NUMBAR is shown with this many decimals (truncated, not rounded)
MAX_STEPS = 1_000_000       # stops runaway programs (like a loop that never ends)
MAX_DEPTH = 200             # stops runaway recursion


# -----------------------------------------------------
# ERRORS AND SIGNALS
# -----------------------------------------------------
class InterpreterError(Exception):
    """a problem found while running the program (example: dividing by zero)"""
    pass


class ReturnSignal(Exception):
    """raised by FOUND YR to leave a function with a value"""
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    """raised by GTFO to leave a loop, a switch-case, or a function"""
    pass


# -----------------------------------------------------
# TOKEN GROUPS
# -----------------------------------------------------
LITERALS = {'NUM', 'NUMBAR', 'YARN', 'TROOF', 'NOOB'}
ARITHMETIC = {'SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR'}
COMPARISON = {'BOTHSAEM', 'DIFFRINT'}
BOOLEAN = {'BOTHOF', 'EITHER', 'WONOF'}
EXPRESSION_START = (LITERALS | ARITHMETIC | COMPARISON | BOOLEAN |
                    {'VAR', 'NOT', 'NOTOF', 'ANYOF', 'ALLOF', 'SMOOSH', 'MAEK', 'IIZ'})

NUMBER_PATTERN = re.compile(r'^-?[0-9]+(\.[0-9]+)?$')

# the value of "I HAS A x ITZ A <type>"
DEFAULT_VALUES = {'TROOF': False, 'NUMBR': 0, 'NUMBAR': 0.0, 'YARN': '', 'NOOB': None}


# =====================================================
# PARSER: tokens -> tree
# =====================================================
#   expressions:  ('lit', value)            ('var', name)
#                 ('bin', op, left, right)  ('not', expr)
#                 ('multi', 'ALLOF'|'ANYOF', [expr])
#                 ('smoosh', [expr])        ('maek', expr, type)
#                 ('call', name, [expr])
#   statements:   ('vardec', name, expr, type)   ('print', [expr])
#                 ('gimmeh', name)               ('assign', name, expr)
#                 ('cast', name, type)           ('expr', expr)
#                 ('orly', yes, [(cond, block)], no)
#                 ('func', name, [params], body) ('return', expr)   ('gtfo',)
class Parser:

    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme
        self.i = 0

    # ----- small helpers -----
    def peek(self, k=0):
        j = self.i + k
        return self.token[j] if j < len(self.token) else None

    def next(self):
        if self.i >= len(self.token):
            raise InterpreterError("Unexpected end of the program")
        pair = (self.token[self.i], self.lexeme[self.i])
        self.i += 1
        return pair

    def expect(self, tok, message):
        if self.peek() != tok:
            raise InterpreterError(message)
        return self.next()[1]

    def skip_newlines(self):
        while self.peek() == 'NEWLINE':
            self.i += 1

    def parse_type(self):
        tok, lex = self.next()
        if tok not in ('TYPE', 'NOOB'):
            raise InterpreterError("Expected a type (TROOF, NUMBR, NUMBAR, YARN, NOOB), got " + lex)
        return lex

    # ----- program and blocks -----
    def parse_program(self):
        self.skip_newlines()
        self.expect('START', "The program must start with HAI")

        statements = []
        self.skip_newlines()

        if self.peek() == 'WAZZUP':
            self.i += 1
            statements += self.parse_block({'BUHBYE'})
            self.expect('BUHBYE', "WAZZUP must end with BUHBYE")

        statements += self.parse_block({'END'})
        self.expect('END', "The program must end with KTHXBYE")
        return statements

    def parse_block(self, stop):
        # reads statements until one of the "stop" tokens (which is NOT consumed)
        statements = []
        while True:
            self.skip_newlines()
            t = self.peek()
            if t is None:
                raise InterpreterError("Unexpected end of the program")
            if t in stop:
                return statements
            statements.append(self.parse_statement())

    # ----- statements -----
    def parse_statement(self):
        t = self.peek()

        if t == 'VARDEC':
            return self.parse_vardec()
        if t == 'PRINT':
            return self.parse_print()
        if t == 'GIMMEH':
            self.i += 1
            return ('gimmeh', self.expect('VAR', "GIMMEH must be followed by a variable"))
        if t == 'ORLY':
            return self.parse_orly()
        if t == 'WTF':
            raise InterpreterError("Switch-case (WTF?) is not implemented yet")
        if t == 'IMINYR':
            raise InterpreterError("Loops (IM IN YR) are not implemented yet")
        if t == 'HOWIZI':
            return self.parse_function()
        if t == 'FOUNDYR':
            self.i += 1
            return ('return', self.parse_expr())
        if t == 'GTFO':
            self.i += 1
            return ('gtfo',)

        if t == 'VAR' and self.peek(1) == 'R':
            name = self.next()[1]
            self.i += 1                                  # R
            return ('assign', name, self.parse_expr())
        if t == 'VAR' and self.peek(1) == 'ISNOWA':
            name = self.next()[1]
            self.i += 1                                  # IS NOW A
            return ('cast', name, self.parse_type())

        if t in EXPRESSION_START:
            return ('expr', self.parse_expr())           # the answer is saved in IT

        raise InterpreterError("Unexpected " + self.lexeme[self.i])

    def parse_vardec(self):
        self.i += 1
        name = self.expect('VAR', "I HAS A must be followed by a variable name")
        expr = None
        type_name = None

        if self.peek() == 'ASSIGN':
            self.i += 1
            if self.peek() == 'A':                       # ITZ A <type>
                self.i += 1
                type_name = self.parse_type()
            else:
                expr = self.parse_expr()

        return ('vardec', name, expr, type_name)

    def parse_print(self):
        self.i += 1
        exprs = [self.parse_expr()]

        while True:
            if self.peek() == 'PLUS':                    # VISIBLE a + b
                self.i += 1
                exprs.append(self.parse_expr())
            elif self.peek() in EXPRESSION_START:        # VISIBLE a b
                exprs.append(self.parse_expr())
            else:
                break

        return ('print', exprs)

    def parse_orly(self):
        self.i += 1
        self.skip_newlines()
        self.expect('YARLY', "O RLY? must be followed by YA RLY")

        yes = self.parse_block({'MEBBE', 'NOWAI', 'OIC'})

        mebbes = []
        while self.peek() == 'MEBBE':
            self.i += 1
            cond = self.parse_expr()
            mebbes.append((cond, self.parse_block({'MEBBE', 'NOWAI', 'OIC'})))

        no = None
        if self.peek() == 'NOWAI':
            self.i += 1
            no = self.parse_block({'OIC'})

        self.expect('OIC', "O RLY? must end with OIC")
        return ('orly', yes, mebbes, no)

    def parse_function(self):
        self.i += 1
        name = self.expect('VAR', "HOW IZ I must be followed by a function name")

        params = []
        if self.peek() == 'YR':
            self.i += 1
            params.append(self.expect('VAR', "YR must be followed by a parameter name"))
            while self.peek() == 'AN' and self.peek(1) == 'YR':
                self.i += 2
                params.append(self.expect('VAR', "YR must be followed by a parameter name"))

        body = self.parse_block({'IFUSAYSO'})
        self.expect('IFUSAYSO', "A function must end with IF U SAY SO")
        return ('func', name, params, body)

    # ----- expressions -----
    def parse_expr(self):
        tok, lex = self.next()

        if tok == 'NUM':
            return ('lit', int(lex))
        if tok == 'NUMBAR':
            return ('lit', float(lex))
        if tok == 'YARN':
            return ('lit', lex[1:-1])                    # remove the double quotes
        if tok == 'TROOF':
            return ('lit', lex == 'WIN')
        if tok == 'NOOB':
            return ('lit', None)
        if tok == 'VAR':
            return ('var', lex)

        # two values:  OP <expr> AN <expr>
        if tok in ARITHMETIC or tok in COMPARISON or tok in BOOLEAN:
            left = self.parse_expr()
            self.expect('AN', lex + " must have AN between its two values")
            right = self.parse_expr()
            return ('bin', tok, left, right)

        if tok in ('NOT', 'NOTOF'):
            return ('not', self.parse_expr())

        # many values:  ALL OF <expr> AN <expr> ... MKAY
        if tok in ('ALLOF', 'ANYOF'):
            items = [self.parse_expr()]
            while self.peek() == 'AN':
                self.i += 1
                items.append(self.parse_expr())
            self.expect('MKAY', lex + " must end with MKAY")
            return ('multi', tok, items)

        # SMOOSH <expr> AN <expr> ...  (an "AN YR" belongs to a function call, so stop there)
        if tok == 'SMOOSH':
            items = [self.parse_expr()]
            while self.peek() == 'AN' and self.peek(1) != 'YR':
                self.i += 1
                items.append(self.parse_expr())
            return ('smoosh', items)

        # MAEK <expr> [A] <type>
        if tok == 'MAEK':
            value = self.parse_expr()
            if self.peek() == 'A':
                self.i += 1
            return ('maek', value, self.parse_type())

        # I IZ <name> [YR <expr> [AN YR <expr>]...] MKAY
        if tok == 'IIZ':
            name = self.expect('VAR', "I IZ must be followed by a function name")
            args = []
            if self.peek() == 'YR':
                self.i += 1
                args.append(self.parse_expr())
                while self.peek() == 'AN' and self.peek(1) == 'YR':
                    self.i += 2
                    args.append(self.parse_expr())
            self.expect('MKAY', "A function call must end with MKAY")
            return ('call', name, args)

        raise InterpreterError("Unexpected " + lex)


# =====================================================
# VALUE HELPERS
#   NOOB = None   TROOF = True/False   NUMBR = int   NUMBAR = float   YARN = str
# =====================================================
def format_float(x):
    # a NUMBAR is truncated to NUMBAR_DECIMALS decimals when it becomes text
    if x != x or x in (math.inf, -math.inf):
        return str(x)
    try:
        quantum = Decimal(1).scaleb(-NUMBAR_DECIMALS)
        return str(Decimal(repr(x)).quantize(quantum, rounding=ROUND_DOWN))
    except InvalidOperation:
        return repr(x)


def to_yarn(v):
    if v is None:
        return "NOOB"
    if isinstance(v, bool):
        return "WIN" if v else "FAIL"
    if isinstance(v, float):
        return format_float(v)
    return str(v)


def to_troof(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v != ""
    return bool(v)


def to_number(v):
    if v is None:
        raise InterpreterError("NOOB cannot be used as a number")
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, (int, float)):
        return v

    text = v.strip()
    if not NUMBER_PATTERN.match(text):
        raise InterpreterError('Cannot convert YARN "' + v + '" to a number')
    return float(text) if '.' in text else int(text)


def numeric_value(v):
    # a number, or a YARN that looks like a number; anything else gives None
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    text = v.strip()
    if NUMBER_PATTERN.match(text):
        return float(text) if '.' in text else int(text)
    return None


def equal(a, b):
    # used by BOTH SAEM, DIFFRINT, and the OMG cases of WTF?
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    x, y = numeric_value(a), numeric_value(b)
    if x is not None and y is not None:
        return x == y
    return type(a) == type(b) and a == b


def cast(v, type_name):
    if type_name == 'TROOF':
        return to_troof(v)
    if type_name == 'NUMBR':
        return 0 if v is None else int(to_number(v))
    if type_name == 'NUMBAR':
        return 0.0 if v is None else float(to_number(v))
    if type_name == 'YARN':
        return to_yarn(v)
    if type_name == 'NOOB':
        return None
    raise InterpreterError("Unknown type " + type_name)


def truncated_division(x, y):
    q = abs(x) // abs(y)
    return -q if (x < 0) != (y < 0) else q


def arithmetic(op, a, b):
    x, y = to_number(a), to_number(b)
    both_int = isinstance(x, int) and isinstance(y, int)

    if op == 'SUM':
        return x + y
    if op == 'DIFF':
        return x - y
    if op == 'PRODUKT':
        return x * y
    if op == 'BIGGR':
        return max(x, y)
    if op == 'SMALLR':
        return min(x, y)

    if y == 0:
        raise InterpreterError("Cannot divide by zero")

    if op == 'QUOSHUNT':
        return truncated_division(x, y) if both_int else x / y

    # MOD
    if both_int:
        return x - y * truncated_division(x, y)
    return math.fmod(x, y)


# =====================================================
# INTERPRETER: runs the tree
# =====================================================
class Scope:
    # the variables of one place in the program (the main program, or one function call)
    def __init__(self):
        self.vars = {}
        self.it = None          # IT, the answer of the last expression statement


class Interpreter:

    def __init__(self, write=None, read=None):
        # write(text): where VISIBLE output goes     read(name): where GIMMEH input comes from
        self.write = write or (lambda text: print(text, end=""))
        self.read = read or (lambda name: input(name + "> "))

        self.functions = {}     # STORED FUNCTIONS:  name -> (parameters, body)
        self.globals = Scope()  # variables of the main program
        self.steps = 0
        self.depth = 0

    def run(self, token, lexeme):
        program = Parser(token, lexeme).parse_program()
        self.steps = 0
        self.depth = 0

        try:
            self.run_block(program, self.globals)
        except (BreakSignal, ReturnSignal):
            pass                # GTFO or FOUND YR outside of anything: just stop

    # ----- running statements -----
    def tick(self):
        self.steps += 1
        if self.steps > MAX_STEPS:
            raise InterpreterError("Program stopped: too many steps (is there a loop that never ends?)")

    def run_block(self, statements, scope):
        for stmt in statements:
            self.run_statement(stmt, scope)

    def run_statement(self, stmt, scope):
        self.tick()
        kind = stmt[0]

        if kind == 'vardec':
            _, name, expr, type_name = stmt
            if name in scope.vars:
                raise InterpreterError("Variable " + name + " is already declared")
            if expr is not None:
                value = self.evaluate(expr, scope)
            elif type_name is not None:
                value = DEFAULT_VALUES.get(type_name)
            else:
                value = None
            scope.vars[name] = value

        elif kind == 'print':
            text = "".join(to_yarn(self.evaluate(e, scope)) for e in stmt[1])
            self.write(text + "\n")

        elif kind == 'gimmeh':
            name = stmt[1]
            self.find(name, scope)                       # must be declared
            value = self.read(name)
            if value is None:
                raise InterpreterError("Input was cancelled")
            self.set_var(name, value, scope)             # input is always a YARN

        elif kind == 'assign':
            self.set_var(stmt[1], self.evaluate(stmt[2], scope), scope)

        elif kind == 'cast':
            self.set_var(stmt[1], cast(self.get_var(stmt[1], scope), stmt[2]), scope)

        elif kind == 'expr':
            scope.it = self.evaluate(stmt[1], scope)

        elif kind == 'orly':
            self.run_orly(stmt, scope)

        elif kind == 'func':
            # store the function so it can be called later
            self.functions[stmt[1]] = (stmt[2], stmt[3])

        elif kind == 'return':
            raise ReturnSignal(self.evaluate(stmt[1], scope))

        elif kind == 'gtfo':
            raise BreakSignal()

    def run_orly(self, stmt, scope):
        _, yes, mebbes, no = stmt

        if to_troof(scope.it):
            self.run_block(yes, scope)
            return

        for cond, block in mebbes:
            if to_troof(self.evaluate(cond, scope)):
                self.run_block(block, scope)
                return

        if no is not None:
            self.run_block(no, scope)

    # ----- variables -----
    def find(self, name, scope):
        if name in scope.vars:
            return scope
        if name in self.globals.vars:                    # functions may also use main variables
            return self.globals
        raise InterpreterError("Variable " + name + " is not declared")

    def get_var(self, name, scope):
        if name == 'IT':
            return scope.it
        return self.find(name, scope).vars[name]

    def set_var(self, name, value, scope):
        if name == 'IT':
            scope.it = value
        else:
            self.find(name, scope).vars[name] = value

    # ----- evaluating expressions -----
    def evaluate(self, e, scope):
        kind = e[0]

        if kind == 'lit':
            return e[1]

        if kind == 'var':
            return self.get_var(e[1], scope)

        if kind == 'bin':
            _, op, left, right = e
            a = self.evaluate(left, scope)
            b = self.evaluate(right, scope)
            return self.binary(op, a, b)

        if kind == 'not':
            return not to_troof(self.evaluate(e[1], scope))

        if kind == 'multi':
            _, which, items = e
            values = [to_troof(self.evaluate(x, scope)) for x in items]
            return all(values) if which == 'ALLOF' else any(values)

        if kind == 'smoosh':
            return "".join(to_yarn(self.evaluate(x, scope)) for x in e[1])

        if kind == 'maek':
            return cast(self.evaluate(e[1], scope), e[2])

        if kind == 'call':
            args = [self.evaluate(x, scope) for x in e[2]]
            return self.call(e[1], args)

        raise InterpreterError("Cannot evaluate " + kind)

    def binary(self, op, a, b):
        if op in ARITHMETIC:
            return arithmetic(op, a, b)
        if op == 'BOTHSAEM':
            return equal(a, b)
        if op == 'DIFFRINT':
            return not equal(a, b)

        x, y = to_troof(a), to_troof(b)
        if op == 'BOTHOF':
            return x and y
        if op == 'EITHER':
            return x or y
        return x != y                                    # WONOF

    # ----- calling a stored function -----
    def call(self, name, args):
        if name not in self.functions:
            raise InterpreterError("Function " + name + " is not defined")

        params, body = self.functions[name]
        if len(args) != len(params):
            raise InterpreterError("Function " + name + " needs " + str(len(params)) +
                                   " argument(s) but got " + str(len(args)))

        self.depth += 1
        if self.depth > MAX_DEPTH:
            raise InterpreterError("Function " + name + " called itself too many times")

        local = Scope()                                  # each call has its own variables
        local.vars = dict(zip(params, args))

        try:
            self.run_block(body, local)
            result = local.it                            # no FOUND YR: the answer is IT
        except ReturnSignal as signal:
            result = signal.value
        except BreakSignal:                              # GTFO: return NOOB
            result = None
        finally:
            self.depth -= 1

        return result