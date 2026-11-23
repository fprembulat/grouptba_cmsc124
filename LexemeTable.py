# for lexeme classification

class LexemeTable:
    def __init__(self):
        self.classifications = {
            'START': 'Code Delimiter',
            'END': 'Code Delimiter',
            'VARDEC': 'Variable Declaration',
            'VAR': 'Variable Identifier',
            'ASSIGN': 'Variable Assignment',
            'NUM': 'Literal',
            'NUMBAR': 'Literal',
            'YARN': 'Literal',
            'TROOF': 'Literal',
            'NOOB': 'Literal',
            'TYPE': 'Type Literal',
            'PRINT': 'Output Keyword',
            'GIMMEH': 'Input Keyword',
            'SUM': 'Arithmetic Operator',
            'DIFF': 'Arithmetic Operator',
            'PRODUKT': 'Arithmetic Operator',
            'QUOSHUNT': 'Arithmetic Operator',
            'MOD': 'Arithmetic Operator',
            'BIGGR': 'Arithmetic Operator',
            'SMALLR': 'Arithmetic Operator',
            'BOTHSAEM': 'Comparison Operator',
            'DIFFRINT': 'Comparison Operator',
            'WAZZUP': 'Code Delimiter',
            'BUHBYE': 'Code Delimiter',
            'OBTW': 'Comment Delimiter',
            'TLDR': 'Comment Delimiter',
            'BTW': 'Comment',
            'R': 'Variable Assignment',
            'MAEK': 'Typecasting Keyword',
            'ISNOWA': 'Typecasting Keyword',
            'A': 'Typecasting Keyword',
            'SMOOSH': 'String Concatenation',
            'BOTHOF': 'Boolean Operator',
            'EITHER': 'Boolean Operator',
            'NOT': 'Boolean Operator',
            'WONOF': 'Boolean Operator',
            'ANYOF': 'Boolean Operator',
            'ALLOF': 'Boolean Operator',
            'ORLY': 'Conditional Statement',
            'YARLY': 'Conditional Statement',
            'NOWAI': 'Conditional Statement',
            'MEBBE': 'Conditional Statement',
            'OIC': 'Conditional Statement',
            'WTF': 'Switch Statement',
            'OMGWTF': 'Switch Statement',
            'OMG': 'Switch Statement',
            'IMINYR': 'Loop Delimiter',
            'IMOUTTAYR': 'Loop Delimiter',
            'HOWIZI': 'Function Delimiter',
            'IFUSAYSO': 'Function Delimiter',
            'FOUNDYR': 'Return Keyword',
            'IIZ': 'Function Call',
            'YR': 'Parameter Keyword',
            'UPPIN': 'Increment',
            'NERFIN': 'Decrement',
            'TIL': 'Loop Delimiter',
            'WILE': 'Loop Delimiter',
            'GTFO': 'Loop Delimiter',
            'MKAY': 'Operation Delimiter',
            'AN': 'Operand Separator',
            'PLUS': 'Output Separator',
            'NEWLINE': 'Line Break',
        }

    # gives the classification of one token (example: 'SUM' -> 'Arithmetic Operator')
    def classify(self, token_type):
        return self.classifications.get(token_type, "Keyword")

    # gives back the list of lexemes (same output as before)
    def build(self, token, lexeme):
        lexemes = []
        for i in range(len(token)):
            lexemes.append(lexeme[i])
        return lexemes
