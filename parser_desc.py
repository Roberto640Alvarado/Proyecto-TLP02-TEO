# ------------------------------------------------------------
# Lexer y parser para C #Equipo 
# ------------------------------------------------------------
import ply.lex as lex
from ll1_tables import tabla_variables  #tablas LL(1)
from terminals import *  #tokens y reglas de expresión regular
from non_terminals import *  #Los no terminales
from tabulate import tabulate
from termcolor import colored

stack = ['eof', 0]

#Construye el lexer
lexer = lex.lex()

#Añadir una regla para rastrear el número de línea --> Para tabla de tokens
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def print_tokens_table(tokens):
    headers = ["ID", "Tipo", "Valor", "Línea", "Posición"]
    formatted_data = [[idx + 1, tok.type, tok.value, tok.lineno, tok.lexpos] for idx, tok in enumerate(tokens)]
    
    table = tabulate(formatted_data, headers, tablefmt="fancy_grid")
    print(colored(table, "green"))

#Funcion que realiza el análisis sintáctico
def miParser(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as f:
            fuente = f.read() + '$'
        
        lexer.input(fuente)
        lexer.lineno = 1  #Reiniciar el número de línea
        
        #Obtener todos los tokens en una lista para mostrarlos en una tabla
        tokens = []
        tok = lexer.token()
        while tok:
            tokens.append(tok)
            tok = lexer.token()
        
        #Imprimir los tokens
        print("\n<<<<<<<<<<<<<<<<<<<<<< Tabla de Tokens >>>>>>>>>>>>>>>>>>>>>>>")
        print_tokens_table(tokens)
        
        #Reiniciar el lexer para procesar los tokens en el parser
        lexer.input(fuente)
        tok = lexer.token()
        x = stack[-1]

        print("\n<<<<<<<<<<<<<<<<<<<<<< PROCESO DE PARSER >>>>>>>>>>>>>>>>>>>>>>>")
        while True:
            print(f"Token actual: {tok.type}, Pila: {stack}")  #Mensaje de depuración
            if x == tok.type and x == 'eof':
                print("Cadena terminada exitosamente")
                return
            else:
                if x == tok.type and x != 'eof':
                    stack.pop()
                    x = stack[-1]
                    tok = lexer.token()
                elif x in tokens and x != tok.type:
                    print(f"Error: se esperaba {x} pero se encontró {tok.type}")
                    print(f"En la posición: {tok.lexpos}")
                    print("Pila actual:", stack)
                    return
                elif x not in tokens:                
                    celda = buscar_en_tabla(x, tok.type, tabla_variables)
                    if celda is None:
                        print(f"Error: NO se esperaba {tok.type}")
                        print(f"En posición: {tok.lexpos}")                    
                        return
                    else:
                        stack.pop()
                        agregar_pila(celda)
                        x = stack[-1]
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def buscar_en_tabla(no_terminal, terminal, tabla):
    for i in range(len(tabla)):
        if tabla[i][0] == no_terminal and tabla[i][1] == terminal:
            return tabla[i][2]

def agregar_pila(produccion):
    for elemento in reversed(produccion):
        if elemento != 'vacia': 
            stack.append(elemento)

miParser('test.c')
