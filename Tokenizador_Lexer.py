import ply.lex as lex
from tabulate import tabulate

#Global scope tracker
currentScopeLevel = 0

#Definición de tokens
tokens = (
    'KEYWORD', 'IDENTIFIER', 'CONSTANT', 'STRING', 'CHARACTER',
    'OPERATOR', 'BLOCK_START', 'BLOCK_END', 'OPEN_PAREN', 'CLOSE_PAREN',
    'END_OF_STATEMENT', 'COMMENT'
)

#Reglas de expresión regular para tokens simples
t_BLOCK_START = r'\{'
t_BLOCK_END = r'\}'
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_END_OF_STATEMENT = r';'
t_OPERATOR = r'[+\-*/=<>|&]'

#Reglas de expresión regular
def t_KEYWORD(t):
    r'\b(int|float|char|double|if|else|while|for|void|switch|case|break|return|struct|typedef|sizeof|do|const|enum)\b'
    t.type = 'KEYWORD'
    return t

def t_IDENTIFIER(t):
    r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    t.type = 'IDENTIFIER'
    return t

def t_CONSTANT(t):
    r'\b\d+(\.\d+)?\b'
    t.type = 'CONSTANT'
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.type = 'STRING'
    return t

def t_CHARACTER(t):
    r"'.'"
    t.type = 'CHARACTER'
    return t

def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    t.type = 'COMMENT'
    #Actualizar el número de línea para comentarios multilínea
    t.lexer.lineno += t.value.count('\n')
    return t

#Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

#Seguimiento de la línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Manejo de errores léxicos
error_tokens = []  
def t_error(t):
    error_tokens.append((t.value[0], "Token no válido", t.lexer.lineno))
    t.lexer.skip(1)

#Construir el lexer
lexer = lex.lex()

#Función para obtener el nivel de anidación en formato de texto
def get_scope_level(scope_level):
    if scope_level == 0:
        return "Global"
    elif scope_level == 1:
        return "Bloque"
    else:
        return f"Anidado (Nivel {scope_level - 1})"

#Función para tokenizar el código
def tokenize(source_code):
    global currentScopeLevel
    tokens = []
    lexer.input(source_code)
    
    for tok in lexer:
        if tok.type == 'BLOCK_START':
            currentScopeLevel += 1
        elif tok.type == 'BLOCK_END':
            currentScopeLevel -= 1
        tokens.append((tok.value, tok.type, get_scope_level(currentScopeLevel), tok.lineno))
    
    return tokens

#Función para imprimir la tabla de tokens con ID numérico y ámbito
def print_tokens(tokens):
    print("\n<<<<<<<<<<<<<<<<<<<<<< Tabla de Tokens >>>>>>>>>>>>>>>>>>>>>>>")
    headers = ["ID", "Valor", "Tipo", "Ámbito", "Línea"]
    formatted_data = [[idx + 1, t[0], t[1], t[2], t[3]] for idx, t in enumerate(tokens)]
    print(tabulate(formatted_data, headers, tablefmt="fancy_grid"))

#Función para imprimir la tabla de errores
def print_error_tokens(error_tokens):
    print("\n<<<<<<<<<<<<<<<<<<<<<< Tabla de Errores >>>>>>>>>>>>>>>>>>>>>>>")
    headers = ["ID", "Valor", "Descripción", "Línea"]
    formatted_data = [[idx + 1, e[0], e[1], e[2]] for idx, e in enumerate(error_tokens)]
    print(tabulate(formatted_data, headers, tablefmt="fancy_grid"))

#Lee el código fuente desde un archivo
with open("test.c", "r") as file:
    source_code = file.read()
    tokens = tokenize(source_code)

print_tokens(tokens)
print_error_tokens(error_tokens)


