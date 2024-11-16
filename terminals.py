#terminals.py

#Lista de nombres de tokens
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'keyword', 'identificador', 'inicioBloque', 'finBloque', 'finInstruccion',
    'asignacion', 'comentario', 'comentario_bloque', 'cadena', 'coma', 'eof',
    'int', 'float', 'char', 'char_literal'
)

#Reglas de expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_inicioBloque = r'\{'
t_finBloque = r'\}'
t_finInstruccion = r'\;'
t_asignacion = r'\='
t_coma = r'\,'
t_eof = r'\$'

def t_int(t):
    r'(int)'
    return t

def t_float(t):
    r'(float)'
    return t

def t_char(t):
    r'(char)'
    return t

#Regla para números (enteros y decimales)
def t_NUMBER(t):
    r'\d+(\.\d+)?'  
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

#Regla para caracteres tipo char
def t_char_literal(t):
    r"\'(.)\'"
    t.value = t.value[1]  #Extrae el carácter entre las comillas
    return t

def t_keyword(t):
    r'(return)|(if)|(else)|(do)|(while)|(for)|(void)'
    return t

def t_identificador(t):
    r'([a-z]|[A-Z]|_)([a-z]|[A-Z]|\d|_)*'
    return t

def t_cadena(t):
    r'\".*\"'
    return t

def t_comentario(t):
    r'\/\/.*'
    return t

def t_comentario_bloque(t):
    r'\/\*(.|\n)*?\*\/'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



#Ignora espacios y tabs
t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    return t
