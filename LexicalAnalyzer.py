# RECOGNIZES LEXEMES AND CLASSIFIES TOKENS

import re

class LexicalAnalyzer:
    def __init__(self):

        self.rules = [
            ('START', r'HAI'),
            ('END', r'KTHXBYE'),

            ('WAZZUP', r'WAZZUP'),
            ('BUHBYE', r'BUHBYE'),

            ('OBTW', r'OBTW\b'),
            ('TLDR', r'TLDR\b'),
            ('BTW', r'BTW\b'),

            ('VARDEC', r'I HAS A\b'),
            ('ASSIGN', r'ITZ\b'),
            ('ISNOWA', r'IS NOW A\b'),

            ('QUOSHUNTOF', r'QUOSHUNT OF\b'),
            ('PRODUKT', r'PRODUKT OF\b'),
            ('SMALLR', r'SMALLR OF\b'),
            ('BOTHSAEM', r'BOTH SAEM\b'),
            ('DIFFRINT', r'DIFFRINT\b'),
            ('SUM', r'SUM OF\b'),
            ('DIFF', r'DIFF OF\b'),
            ('MOD', r'MOD OF\b'),
            ('BIGGR', r'BIGGR OF\b'),
            ('EITHER', r'EITHER OF\b'),
            ('NOTOF', r'NOT OF\b'),
            ('WONOF', r'WON OF\b'),
            ('ANYOF', r'ANY OF\b'),
            ('ALLOF', r'ALL OF\b'),

            ('ORLY', r'O RLY\?'),
            ('YARLY', r'YA RLY\b'),
            ('NOWAI', r'NO WAI\b'),
            ('MEBBE', r'MEBBE\b'),
            ('OIC', r'OIC\b'),

            ('WTF', r'WTF\?'),
            ('OMGWTF', r'OMGWTF\b'),
            ('OMG', r'OMG\b'),

            ('IMINYR', r'IM IN YR\b'),
            ('IMOUTTAYR', r'IM OUTTA YR\b'),
            ('HOWIZI', r'HOW IZ I\b'),
            ('IFUSAYSO', r'IF U SAY SO\b'),
            ('FOUNDYR', r'FOUND YR\b'),
            ('IIZ', r'I IZ\b'),

            ('UPPIN', r'UPPIN\b'),
            ('NERFIN', r'NERFIN\b'),
            ('TIL', r'TIL\b'),
            ('WILE', r'WILE\b'),
            ('GTFO', r'GTFO\b'),

            ('PRINT', r'VISIBLE\b'),
            ('GIMMEH', r'GIMMEH\b'),

            ('MKAY', r'MKAY\b'),
            ('YR', r'YR\b'),
            ('MAEK', r'MAEK\b'),
            ('A', r'A\b'),
            ('R', r'R\b'),

            # recognize types before variable identifiers
            ('TYPE', r'(?:TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)\b'),

            # recognize boolean values before variable identifiers
            ('TROOF', r'(?:WIN|FAIL)\b'),

            # recognize decimal numbers before whole numbers
            ('NUMBAR', r'-?[0-9]+\.[0-9]+'),
            ('NUM', r'-?[0-9]+'),

            # recognize strings enclosed in double quotes
            ('YARN', r'"[^"\n]*"'),

            # recognize variable identifiers
            ('VAR', r'[a-zA-Z_][a-zA-Z0-9_]*'),

            # ignore spaces and tabs
            ('SKIP', r'[ \t]+'),

            # track newlines
            ('NEWLINE', r'\n'),

            # catch any unrecognized character
            ('MISMATCH', r'.'),
        ]

        # combine all token rules into one regex
        self.regex = re.compile(
            '|'.join(
                '(?P<{}>{})'.format(name, pattern)
                for name, pattern in self.rules
            )
        )

    def tokenize(self, code):
        # store the infos
        token = []
        lexeme = []

        # track the current line and column

        # track the current line
        line_no = 1
        line_start = 0
        # check if comment
        is_comment = False

        for match in self.regex.finditer(code):

            token_type = match.lastgroup
            value = match.group()

            position = match.end

            if token_type == 'OBTW':
                is_comment = True
                continue

            if is_comment:
                if token_type == 'TLDR':
                    is_comment = False
                continue

            if token_type in ('SKIP', 'NEWLINE'):
                continue

            if token_type == 'BTW':
                next_nl = code.find('\n', position)

                if next_nl == 1:
                    break

                position = next_nl + 1
                continue

            if token_type == 'MISMATCH':
                print("Lexical Error")
                continue

            token.append(token_type)
            lexeme.append(value)

        return token, lexeme

            