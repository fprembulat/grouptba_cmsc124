# THIS IS THE MAIN FILE
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from Buffer import Buffer
from SemanticAnalyzer import SemanticError
from Interpreter import Interpreter, InterpreterError


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LOLCODE Interpreter")
        self.geometry("1000x650")
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.symbol_rows = {}       # identifier -> row id in the symbol table

        self.build_toolbar()
        self.build_tables()
        self.build_console()
        self.load_editor()

        self.analyze()

    # builder functions that help build the layout itself
    def build_toolbar(self):
        bar = ttk.Frame(self, padding=6)
        bar.grid(row=0, column=0, sticky="ew")
        ttk.Label(bar, text="program.lol").pack(side="left")
        ttk.Button(bar, text="Run", command=self.analyze).pack(side="left", padx=(16, 0))
        self.status = ttk.Label(bar, text="")
        self.status.pack(side="left", padx=16)

    def build_tables(self):
        panes = ttk.PanedWindow(self, orient="horizontal")
        panes.grid(row=1, column=0, sticky="nsew", padx=6)

        # text editor
        edit_frame = ttk.LabelFrame(panes, text="Text editor")
        self.editor = scrolledtext.ScrolledText(edit_frame, width=40, font=("Consolas", 11))
        self.editor.pack(fill="both", expand=True)
        panes.add(edit_frame, weight=3)

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
    def clear_tables(self):
        for tree in (self.token_tree, self.symbol_tree):
            tree.delete(*tree.get_children())
        self.symbol_rows = {}

    def load_editor(self):
        # shows the contents of program.lol in the text editor
        for code in Buffer().load_buffer():
            self.editor.insert("1.0", code)

    # symbol table: the interpreter calls this every time a variable changes
    def update_symbol(self, name, value):
        if name in self.symbol_rows:
            self.symbol_tree.item(self.symbol_rows[name], values=(name, value))
        else:
            self.symbol_rows[name] = self.symbol_tree.insert("", "end", values=(name, value))

    # console: shows the output of the program and takes input for GIMMEH
    def build_console(self):
        self.running = False

        frame = ttk.LabelFrame(self, text="Console")
        frame.grid(row=2, column=0, sticky="nsew", padx=6, pady=6)

        self.console = scrolledtext.ScrolledText(
            frame, height=8, state="disabled", font=("Consolas", 11)
        )
        self.console.pack(fill="both", expand=True)

        # input field, only usable while the program waits for GIMMEH
        input_bar = ttk.Frame(frame)
        input_bar.pack(fill="x")
        ttk.Label(input_bar, text="Input:").pack(side="left", padx=(0, 6))
        self.input_text = tk.StringVar()
        self.input_done = tk.IntVar(value=0)
        self.input_entry = ttk.Entry(input_bar, textvariable=self.input_text, state="disabled")
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.input_entry.bind("<Return>", lambda event: self.input_done.set(1))

    def write_console(self, text):
        self.console.config(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.config(state="disabled")
        self.update_idletasks()

    def clear_console(self):
        self.console.config(state="normal")
        self.console.delete("1.0", "end")
        self.console.config(state="disabled")

    def read_input(self, name):
        # called by the interpreter on GIMMEH: waits until Enter is pressed in the input field
        self.write_console(name + "> ")
        self.input_entry.config(state="normal")
        self.input_entry.focus_set()
        self.input_done.set(0)
        try:
            self.wait_variable(self.input_done)
        except tk.TclError:
            return None
        text = self.input_text.get()
        self.input_text.set("")
        self.input_entry.config(state="disabled")
        self.write_console(text + "\n")
        return text

    # does the main work of the program
    def analyze(self):
        if self.running:        # a program is still waiting for input
            return
        self.clear_tables()
        self.clear_console()
        self.status.config(text="")

        # the code comes from the text editor
        code = self.editor.get("1.0", "end-1c").rstrip()

        # the interpreter owns the lexical analyzer, syntax/semantic analyzers,
        # lexeme table and symbol table; the GUI only gives it the console and the table callback
        self.interpreter = Interpreter(self.write_console, self.read_input, self.update_symbol)

        try:
            # lexical + syntax + semantic analysis
            rows = self.interpreter.analyze(code)

            # tokens, lexemes and their classification
            for lex, tok, cls in rows:
                self.token_tree.insert("", "end", values=(lex, tok, cls))

            # run the program: output -> console, variables -> symbol table (updated live)
            self.running = True
            try:
                self.interpreter.execute()
            finally:
                self.running = False

        except SyntaxError as e:
            self.status.config(text="SyntaxError")
            messagebox.showerror("SyntaxError", str(e))
        except SemanticError as e:
            self.status.config(text="SemanticError")
            messagebox.showerror("SemanticError", str(e))
        except InterpreterError as e:
            self.write_console("\nRuntimeError: " + str(e) + "\n")
            self.status.config(text="RuntimeError")


if __name__ == "__main__":
    App().mainloop()