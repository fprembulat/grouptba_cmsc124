import re

class LexicalAnalyzer:
    lin_num = 1

    def tokenize(self, code):
        rules = [
            ('START', r'HAI'),
            ('END', r'KTHXBYE'),
            ('WAZZUP', r'WAZZUP'),
            ('BUHBYE', r'BUHBYE'),
            ('BTW', r'BTW'),
            ('OBTW', r'OBTW'),
            ('TLDR', r'TLDR'),
            ('VARDEC', r'I HAS A'),
            ('ASSIGN', r'ITZ'),
            ('R', r'R'),
            ('SUM', r'SUM OF'),
            ('DIFF', r'DIFF OF'),
            ('PRODUKT', r'PRODUKT OF'),
            ('MAEK', r'MAEK'),
            ('A', r'A'),
            ('ISNOWA', r'IS NOW A'),
            ('PRINT', r'VISIBLE'),
            ('GIMMEH', r'GIMMEH'),
            ('ORLY', r'O RLY\?'),
            ('YARLY', r'YA RLY'),
            ('MEBBE', r'MEBBE'),
            ('NOWAI', r'NO WAI'),
            ('OIC', r'OIC'),
            ('WTF', r'WTF\?'),
            ('OMG', r'OMG'),
            ('OMGWTF', r'OMGWTF'),
            ('QUOSHUNTOF', r'QUOSHUNT OF'),
            ('MOD', r'MOD OF'),
            ('BIGGR', r'BIGGR OF'),
            ('SMALLR', r'SMALLR OF'),
            ('EITHER', r'EITHER OF'),
            ('NOTOF', r'NOT OF'),
            ('WONOF', r'WON OF'),
            ('ANYOF', r'ANY OF'),
            ('ALLOF', r'ALL OF'),
            ('IF', r'IF'),
            ('BOTHSAEM', r'BOTH SAEM'),
            ('DIFFRINT', r'DIFFRINT'),
            ('SMOOSH', r'SMOOSH'),
            ('IMINYR', r'IM IN YR'),
            ('IMOUTTAYR', r'IM OUTTA YR'),
            ('HOWIZI', r'HOW IZ I'),
            ('IFUSAYSO', r'IF U SAY SO'),
            ('FOUNDYR', r'FOUND YR'),
            ('IIZ', r'I IZ'),
            ('UPPIN', r'UPPIN'),
            ('NERFIN', r'NERFIN'),
            ('YR', r'YR'),
            ('TIL', r'TIL'),
            ('WILE', r'WILE'),
            ('GTFO', r'GTFO'),
            ('MKAY', r'MKAY'),
            ('VAR', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('FUNC', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('LOOP', r'[a-zA-Z][a-zA-Z0-9_]*'),
            ('NUM', r'-?[0-9]+'),
            ('NUMBAR', r'-?[0-9]+\.[0-9]+'),
            ('YARN', r'"[^"]*"'),
            ('TROOF', r'(WIN|FAIL)'),
            ('TYPE', r'(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)')
        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        lin_start = 0

        # Lists of output for the program
        token = []
        lexeme = []
        row = []
        column = []

        # It analyzes the code to find the lexemes and their respective Tokens
        for m in re.finditer(tokens_join, code):
            token_type = m.lastgroup
            token_lexeme = m.group(token_type)

            if token_type == 'NEWLINE':
                lin_start = m.end()
                self.lin_num += 1
            elif token_type == 'SKIP':
                continue
            elif token_type == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' % (token_lexeme, self.lin_num))
            else:
                col = m.start() - lin_start
                column.append(col)
                token.append(token_type)
                lexeme.append(token_lexeme)
                row.append(self.lin_num)
                # To print information about a Token
                print('Token = {0}, Lexeme = \'{1}\', Row = {2}, Column = {3}'.format(token_type, token_lexeme, self.lin_num, col))

        return token, lexeme, row, column
    