
from SyntaxAnalyzer import syntax
from LexicalAnalyzer import LexicalAnalyzer

# -----------------------------------------------------
# WAZZUP TEST CASES
# -----------------------------------------------------

tests = [
    {
        "name": "Valid WAZZUP declaration block",
        "code": """
HAI
WAZZUP
I HAS A name
I HAS A age
BUHBYE
VISIBLE "Hello"
KTHXBYE
""",
        "expected": "Syntax OK"
    },

    {
        "name": "Missing BUHBYE",
        "code": """
HAI
WAZZUP
I HAS A name
KTHXBYE
""",
        "expected": "WAZZUP must end with BUHBYE"
    },

    {
        "name": "Invalid statement inside WAZZUP",
        "code": """
HAI
WAZZUP
VISIBLE "Hello"
BUHBYE
KTHXBYE
""",
        "expected": "Only variable declarations are allowed inside WAZZUP"
    },

    {
        "name": "Variable declaration outside WAZZUP",
        "code": """
HAI
I HAS A name
KTHXBYE
""",
        "expected": "Variable declarations must be inside WAZZUP"
    },

    {
        "name": "WAZZUP after an ordinary statement",
        "code": """
HAI
VISIBLE "Hello"
WAZZUP
I HAS A name
BUHBYE
KTHXBYE
""",
        "expected": "WAZZUP must appear before other statements"
    }
]

# -----------------------------------------------------
# RUN TESTS
# -----------------------------------------------------

for test in tests:

    print("\n======================================")
    print("TEST:", test["name"])
    print("======================================")

    try:
        # Create lexer
        lexer = LexicalAnalyzer()

        # Tokenize the test program
        tokens, lexemes = lexer.tokenize(test["code"].strip())

        # Run syntax analyzer
        syntax(tokens)

        actual = "Syntax OK"

    except SyntaxError as error:
        actual = str(error)

    # Compare actual and expected results
    if actual == test["expected"]:
        print("PASSED")
    else:
        print("FAILED")

    print("Expected:", test["expected"])
    print("Actual:  ", actual)

# -----------------------------------------------------
# END OF TESTING
# -----------------------------------------------------

print("\n======================================")
print("TESTING COMPLETE")
print("======================================")
