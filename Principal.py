# THIS IS THE MAIN FILE
from Buffer import Buffer
from LexicalAnalyzer import LexicalAnalyzer
from SymbolTable import SymbolTable
from LexemeTable import LexemeTable
from SyntaxAnalyzer import syntax

if __name__ == '__main__':

    # objects
    buffer = Buffer()
    analyzer = LexicalAnalyzer()
    symbol_table = SymbolTable()
    lexeme_table = LexemeTable()

    token = []
    lexeme = []

    try: 

        for code in buffer.load_buffer():
            t, lex = analyzer.tokenize(code) # tokenize the code
            token += t
            lexeme += lex
    
        print("Tokens: ", token)
        print("Lexemes: ", lexeme)
        syntax(token)
        print('Syntax OK')

        print(lexeme_table.build(token, lexeme))
        print(symbol_table.build(token,lexeme))
    except SyntaxError as e:
        print('SyntaxError:', e)


