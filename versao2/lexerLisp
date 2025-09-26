import ply.lex as lex 
import tkinter as tk
from tkinter import filedialog

# Palavras reservadas do Lisp
reserved = {
    'defun' : 'DEFUN',
    'if'    : 'IF',
    'cond'  : 'COND',
    'car'   : 'CAR',
    'cdr'   : 'CDR',
    'cons'  : 'CONS',
    'eq'    : 'EQ',
    'nil'   : 'NIL',
    't'     : 'T',  
}

# Lista de tokens
tokens = [
    # operadores aritméticos
    'SOMA', 'SUBT', 'MULT', 'DIVIDE',

    # comparadores
    'IGUAL', 'DIF',

    # literais
    'ID', 'INTEIRO', 'FLUTUANTE', 

    # delimitadores
    'EPAREN', 'DPAREN', 'ECOLCH', 'DCOLCH', 'PVIRGU', 'DOISP',
] + list(reserved.values())

# Expressões regulares
t_SOMA    = r'\+'
t_SUBT    = r'-'
t_MULT    = r'\*'
t_DIVIDE  = r'/'

t_EPAREN  = r'\('
t_DPAREN  = r'\)'
t_ECOLCH  = r'\['
t_DCOLCH  = r'\]'
t_PVIRGU  = r';'
t_DOISP   = r':'

t_IGUAL   = r'='
t_DIF     = r'!='

# Ignorar espaços e tabs
t_ignore = ' \t'

#inteiro

def t_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Identificadores e palavras reservadas
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# Comentários 
def t_COMENTARIO(t):
    r'//.*'
    pass

# Nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erro
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir lexer
lexer = lex.lex()

# Tokenizar arquivo
def tokenizar(code_str):
    lexer.input(code_str)
    jalToken = tk.Tk()
    jalToken.title("Tokens identificados")

    #interface
    frame = tk.Frame(jalToken)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    labels = []

    #loop
    for tok in lexer:
        label_text = f"Linha {tok.lineno}: {tok.type} ({repr(tok.value)})"
        label = tk.Label(scrollable_frame, text=label_text, anchor="w")
        label.pack(fill=tk.X)
        labels.append(label)

    canvas.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill=tk.Y)

    jalToken.mainloop()

# Teste
if __name__ == '__main__':
    
    jal = tk.Tk()
    jal.withdraw()

    caminhoCodigoLisp = filedialog.askopenfilename(
    title='Por favor,\tselecione um arquivo:',
    initialdir='/home',
    filetypes = (('Código', '*.lsp'), ('Todos os arquivos', '*.*'))
    )

    if caminhoCodigoLisp:
        # Pode agora abrir e ler o ficheiro, por exemplo:
        with open(caminhoCodigoLisp, 'r') as f:
            codigoLisp = f.read()
            tokenizar(codigoLisp)
