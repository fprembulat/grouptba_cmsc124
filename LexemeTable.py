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
            'NUUMBAR': 'Literal',
            'YARN': 'Literal',
            'YARN': 'Literal',
            'TROOF': 'Literal',
            'TYPE': 'Type Literal',
            'PRINT': 'Output Keyword',
            'GIMMEH': 'Input Keyword',
            'SUM': 'Arithmetic Operator',
            'DIFF': 'Arithmetic Operator',
            'PRODUKT': 'Arithmetic Operator',
            'QUOSHUNTOF': 'Arithmetic Operator',
            'MOD': 'Arithmetic Operator',
            'BOTHSAEM': 'Comparison Operator',
            'DIFFRINT': 'Comparison Operator',
            'WAZZUP': 'Code Delimiter',
            'BUHBYE': 'Code Delimiter',
            'OBTW': 'Comment Delimiter',
            'TLDR': 'Comment Delimiter',
            'BTW': 'Comment',
            'R': 'Variable Assignment',
            'MAEK': 'Typecasting Keyword',
            'ISNOWA': 'Typecasting Keyword'
        }

    def build(self, token, lexeme):
        lexemes = []
        for i in range(len(token)):
            classification = self.classifications.get(token[i], "Keyword")
            lexemes.append(lexeme[i])
        return lexemes
