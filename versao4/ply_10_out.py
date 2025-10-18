import ply.lex as lex
import ply.yacc as yacc
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import scrolledtext
import pprint

# Palavras reservadas do Lisp
reserved = {
    'defun'  : 'DEFUN',
    'if'     : 'IF',
    'cond'   : 'COND',
    'car'    : 'CAR',
    'cdr'    : 'CDR',
    'cons'   : 'CONS',
    'eq'     : 'EQ',
    'nil'    : 'NIL',
    'T'      : 'T',  
}

# Lista de tokens
tokens = [
    # operadores aritméticos
    'SOMA', 'SUBT', 'MULT', 'DIV',

    # comparadores
    'IGUAL', 'DIF', 'MENOR', 'MENOR_IGUAL', 'MAIOR', 'MAIOR_IGUAL',

    # literais
    'ID', 'INTEIRO', 'FLUTUANTE', 

    # delimitadores
    'EPAREN', 'DPAREN', 'ECOLCH', 'DCOLCH', 'PVIRGU', 'DOISP',
] + list(reserved.values())

# Expressões regulares
t_SOMA    = r'\+'
t_SUBT    = r'-'
t_MULT    = r'\*'
t_DIV  = r'/'

t_EPAREN  = r'\('
t_DPAREN  = r'\)'
t_ECOLCH  = r'\['
t_DCOLCH  = r'\]'
t_PVIRGU  = r';'
t_DOISP   = r':'

t_IGUAL       = r'='
t_DIF         = r'!='
t_MENOR       = r'<'
t_MENOR_IGUAL = r'<='
t_MAIOR       = r'>'
t_MAIOR_IGUAL = r'>=' 

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


# REGRAS DO PARSER  ANALISE SINTATICA

def p_programa(p):
    '''programa : seq_funcoes'''
    p[0] = p[1]

def p_seq_funcoes(p):
    '''seq_funcoes : funcao
                   | funcao seq_funcoes'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_funcao(p):
    '''funcao : EPAREN DEFUN ID EPAREN parametros DPAREN corpo DPAREN'''
    p[0] = ('Funcao', p[3], p[5], p[7])

def p_corpo(p):
    '''corpo : seq_expr'''
    p[0] = p[1]

def p_seq_expr(p):
    '''seq_expr : expr
                | expr seq_expr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_expr_comp(p):
    '''expr_comp : EPAREN operador_comparativo argumentos DPAREN'''
    p[0] = ('Comparacao', p[2], p[3])

def p_expr(p):
    '''expr : expr_arit
            | expr_comp
            | chamada_funcao
            | condicional_cond
            | condicional_if
            | NIL
            | ID
            | INTEIRO
            | T'''
    p[0] = p[1]

def p_condicional_if(p):
    '''condicional_if : EPAREN IF expr expr expr DPAREN
                      | EPAREN IF expr expr DPAREN'''
    if len(p) == 7:
        p[0] = ('If', p[3], p[4], p[5])
    else:
        p[0] = ('If', p[3], p[4])

def p_condicional_cond(p):
    '''condicional_cond : EPAREN COND lista_cond DPAREN'''
    p[0] = ('Cond', p[3])

def p_lista_cond(p):
    '''lista_cond : condicao_cond
                  | condicao_cond lista_cond'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]
    
def p_condicao_cond(p):
    '''condicao_cond : EPAREN condicao corpo DPAREN'''
    p[0] = ('Condicao', p[2], p[3])

def p_condicao(p):
    '''condicao : expr_comp
                | T'''
    p[0] = p[1]

def p_operador_comparativo(p):
    '''operador_comparativo : IGUAL
                            | DIF
                            | MENOR
                            | MENOR_IGUAL
                            | MAIOR
                            | MAIOR_IGUAL
                            | EQ'''
    p[0] = p[1]

def p_chamada_funcao(p):
    '''chamada_funcao : EPAREN ID argumentos DPAREN
                      | EPAREN CDR argumentos DPAREN
                      | EPAREN CAR argumentos DPAREN
                      | EPAREN CONS argumentos DPAREN'''
    p[0] = ('Funcao chamada', p[2], p[3])

def p_parametros(p):
    '''parametros :
                  | ID parametros'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_expr_arit(p):
    '''expr_arit : EPAREN operador_arit argumentos DPAREN'''
    p[0] = ('Aritmetica', p[2], p[3])

def p_argumentos(p):
    '''argumentos : 
                  | elemento argumentos'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_elemento(p):
    '''elemento : ID
                | INTEIRO
                | expr
                | NIL
                | T'''
    p[0] = p[1]

def p_operador_arit(p):
    '''operador_arit : MULT
                     | DIV
                     | SOMA
                     | SUBT'''
    p[0] = p[1]

def p_error(p):
    if p:
        error_msg = f"Erro de sintaxe próximo a '{p.value}' na linha {p.lineno}"
    else:
        error_msg = "Erro de sintaxe no final do código"
    raise SyntaxError(error_msg)

# Construir parser
parser = yacc.yacc()


def on_closing():
    jal.destroy()  # fecha a janela
    jal.quit()


# Lexer e Parser

def lexer_parser(codigo_lisp):
    jal = tk.Tk()
    jal.protocol("WM_DELETE_WINDOW", on_closing)
    jal.title("Analise Lexica e Sintatica")

    tokens = ""

    print("====== TOKENS ENCONTRADOS ======")
    lexer.input(codigo_lisp)  
    
    while True:
        tok = lexer.token()
        if not tok:
            break  
        token = f"Tipo: {tok.type}, Valor: {tok.value}, Linha: {tok.lineno}"
        tokens = tokens + token + "\n"
        print(f"Tipo: {tok.type}, Valor: {tok.value}, Linha: {tok.lineno}")

    print("\n=== ÁRVORE SINTÁTICA ===\n\n")
    resultado = parser.parse(codigo_lisp)
    arvore = pprint.pformat(resultado)

    tokens_arvore = "TOKENS\n\n\n" + tokens + "\n\n\nARVORE SINTATICA\n\n" + arvore
    pprint.pprint(resultado)


    frame = ttk.Frame(jal, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)
    
    analise_feita = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=30)
    analise_feita.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    analise_feita.insert(tk.END, tokens_arvore)
    analise_feita.config(state=tk.DISABLED)


    jal.mainloop()

# MAIN

if __name__ == '__main__':
    jal = tk.Tk()
    jal.protocol("WM_DELETE_WINDOW", on_closing)
    jal.withdraw()

    caminhoCodigoLisp = filedialog.askopenfilename(
        title='Selecione um arquivo Lisp:',
        initialdir='/home',
        filetypes=(('Código Lisp', '*.lsp'), ('Todos os arquivos', '*.*'))
    )

    if caminhoCodigoLisp:
        with open(caminhoCodigoLisp, 'r') as f:
            codigoLisp = f.read()
            lexer_parser(codigoLisp)
