import ply.lex as lex 

codigoSoma = """
(defun soma (lista)
   (if (eq lista nil) 0
       (+ (car lista) (soma (cdr lista)))))
"""
codigoConcat = """ 
(defun concat (lista1 lista2) 
  (if (eq lista1 nil) lista2
    (cons (car lista1)
      (concat (cdr lista1) lista2))))
"""
codigoInverter = """ 
(defun inverter (lista) 
  (if (eq lista nil) nil
    (concat (inverter (cdr lista)) 
      (cons (car lista) nil))))
"""

codigoOrdenar = """ """

# Palavras reservadas do Lisp
reserved = {
    'defun': 'DEFUN',
    'car': 'CAR',
    'cdr': 'CDR',
    'cons': 'CONS',
    'eq': 'EQ',
    'nil': 'NIL',
    't': 'T',  
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
    for tok in lexer:
        print(f"{tok.lineno}: {tok.type} ({repr(tok.value)})")

# Teste
if __name__ == '__main__':
    print("Tokenizando códigos\n")

    print("////Soma////\n")
    tokenizar(codigoSoma)

    print("\n////Concatena////\n")
    tokenizar(codigoConcat)

    print("\n////Inverte////\n")
    tokenizar(codigoInverter)
