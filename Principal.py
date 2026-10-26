# THIS IS THE MAIN FILE
from Buffer import Buffer
from LexicalAnalyzer import LexicalAnalyzer
from SymbolTable import SymbolTable
from LexemeTable import LexemeTable

if __name__ == '__main__':

    # objects
    buffer = Buffer()
    analyzer = LexicalAnalyzer()
    symbol_table = SymbolTable()
    lexeme_table = LexemeTable()

    # Lists for every list returned list from the function tokenize
    token = []
    lexeme = []

    for code in buffer.load_buffer():
        t, lex = analyzer.tokenize(code) # tokenize the code

        token += t
        lexeme += lex
    
    lexeme_table.build(token, lexeme)
    print(symbol_table.build(token,lexeme))


