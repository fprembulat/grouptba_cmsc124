# RECOGNIZES LEXEMES AND CLASSIFIES TOKENS

import re

class LexicalAnalyzer:
    def __init__(self):

        self.rules = [
            ('START', r'HAI\b'),
            ('END', r'KTHXBYE\b'),

            ('WAZZUP', r'WAZZUP\b'),
            ('BUHBYE', r'BUHBYE\b'),

            ('OBTW', r'OBTW\b'),
            ('TLDR', r'TLDR\b'),
            ('BTW', r'BTW[^\n]*'),

            ('SMOOSH', r'SMOOSH\b'),

            ('VARDEC', r'I HAS A\b'),
            ('ASSIGN', r'ITZ\b'),
            ('ISNOWA', r'IS NOW A\b'),

            ('QUOSHUNT', r'QUOSHUNT OF\b'),
            ('PRODUKT', r'PRODUKT OF\b'),
            ('SMALLR', r'SMALLR OF\b'),
            ('BOTHSAEM', r'BOTH SAEM\b'),
            ('DIFFRINT', r'DIFFRINT\b'),
            ('SUM', r'SUM OF\b'),
            ('DIFF', r'DIFF OF\b'),
            ('MOD', r'MOD OF\b'),
            ('BIGGR', r'BIGGR OF\b'),
            ('BOTHOF', r'BOTH OF\b'),
            ('EITHER', r'EITHER OF\b'),
            ('NOT', r'NOT\b'),
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
            ('AN', r'AN\b'),
            ('A', r'A\b'),
            ('R', r'R\b'),

            # recognize types before variable identifiers
            ('NOOB', r'NOOB\b'),
            ('TYPE', r'(?:TROOF|NUMBR|NUMBAR|YARN|TYPE)\b'),

            # recognize boolean values before variable identifiers
            ('TROOF', r'(?:WIN|FAIL)\b'),

            # recognize decimal numbers before whole numbers
            ('NUMBAR', r'-?[0-9]+\.[0-9]+'),
            ('NUM', r'-?[0-9]+'),

            # recognize strings enclosed in double quotes
            ('YARN', r'"[^"\n]*"'),

            # recognize variable identifiers
            ('VAR', r'[a-zA-Z_][a-zA-Z0-9_]*'),

            # recognize plus symbol for visible
            ('PLUS', r'\+'),

            # ignore spaces, tabs, and carriage returns (Windows line endings)
            ('SKIP', r'[ \t\r]+'),

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

        # True while we are between OBTW and TLDR
        in_comment = False

        for match in self.regex.finditer(code):
            token_type = match.lastgroup
            value = match.group()

            # inside a multiline comment only TLDR (the end) and newlines are kept,
            # everything else is comment text and must not be checked or reported
            if in_comment and token_type not in ('TLDR', 'NEWLINE'):
                continue

            if token_type == 'OBTW':
                in_comment = True
            elif token_type == 'TLDR':
                in_comment = False

            if token_type == 'SKIP':
                continue

            if token_type == 'NEWLINE':
                token.append('NEWLINE')
                lexeme.append('\\n')
                continue

            if token_type == 'MISMATCH':
                print('Lexical Error')
                continue

            token.append(token_type)
            lexeme.append(value)
            
        return token, lexeme