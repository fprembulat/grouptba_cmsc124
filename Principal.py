# THIS IS THE MAIN FILE
import tkinter as tk
from tkinter import ttk, messagebox

from Buffer import Buffer
from LexicalAnalyzer import LexicalAnalyzer
from SymbolTable import SymbolTable
from LexemeTable import LexemeTable
from SyntaxAnalyzer import syntax


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LOLCODE Interpreter")
        self.geometry("1000x650")
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.build_toolbar()
        self.build_tables()

        self.analyze()

    # builder functions that help build the layout itself
    def build_toolbar(self):
        bar = ttk.Frame(self, padding=6)
        bar.grid(row=0, column=0, sticky="ew")
        ttk.Label(bar, text="program.lol").pack(side="left")
        self.status = ttk.Label(bar, text="")
        self.status.pack(side="left", padx=16)

    def build_tables(self):
        panes = ttk.PanedWindow(self, orient="horizontal")
        panes.grid(row=1, column=0, sticky="nsew", padx=6)

        tok_frame = ttk.LabelFrame(panes, text="Tokens and lexemes")
        self.token_tree = self.make_table(
            tok_frame, ("Lexeme", "Token", "Classification"), (160, 110, 170)
        )
        panes.add(tok_frame, weight=3)

        sym_frame = ttk.LabelFrame(panes, text="Symbol table")
        self.symbol_tree = self.make_table(sym_frame, ("Identifier", "Value"), (120, 140))
        panes.add(sym_frame, weight=2)

    def make_table(self, parent, columns, widths):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for c, w in zip(columns, widths):
            tree.heading(c, text=c)
            tree.column(c, width=w, anchor="w")
        scroll = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tree

    # helper functions
    def not_ready(self, name):
        messagebox.showinfo(name, f"{name} is not implemented yet.")

    def clear_tables(self):
        for tree in (self.token_tree, self.symbol_tree):
            tree.delete(*tree.get_children())

    # does the main work of the program
    def analyze(self):
        self.clear_tables()

        # objects
        buffer = Buffer()
        analyzer = LexicalAnalyzer()
        symbol_table = SymbolTable()
        lexeme_table = LexemeTable()

        token = []
        lexeme = []

        try:
            for code in buffer.load_buffer():
                t, lex = analyzer.tokenize(code)  # tokenize the code
                token += t
                lexeme += lex

            syntax(token)

            # gets the tokens and lexemes as well as their classification
            for lex, tok in zip(lexeme, token):
                if tok == "NEWLINE":
                    cls = "Line Break"
                else:
                    cls = lexeme_table.classifications.get(tok, "Keyword")
                self.token_tree.insert("", "end", values=(lex, tok, cls))

            # symbol table: {identifier: value}
            for name, value in symbol_table.build(token, lexeme).items():
                self.symbol_tree.insert("", "end", values=(name, value))

        except SyntaxError as e:
            self.status.config(text="SyntaxError")
            messagebox.showerror("SyntaxError", str(e))


if __name__ == "__main__":
    App().mainloop()
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

        print(lexeme_table.build(token, lexeme))
        print(symbol_table.build(token,lexeme))
        print("Syntax OK")
    except SyntaxError as e:
        print('SyntaxError:', e)


