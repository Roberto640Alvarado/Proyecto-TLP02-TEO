# ------------------------------------------------------------
# Lexer y parser para C #Equipo
# ------------------------------------------------------------
import ply.lex as lex
from ll1_tables import tabla_variables, tabla_comentarios, tabla_condicionales
from terminals import *  #Tokens y reglas de expresión regular
from non_terminals import *  #Los no terminales
from tabulate import tabulate
from termcolor import colored

#Tablas LL1 
tablas_ll1 = {
    "tabla_variables": tabla_variables,
    "tabla_comentarios": tabla_comentarios,
    "tabla_condicionales": tabla_condicionales
    
}

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
        print("\n" + colored("<<<<<<<<<<<<<<<<< Tabla de Tokens >>>>>>>>>>>>>>>>>", "yellow", attrs=['bold']))
        print_tokens_table(tokens)
        
        #Reiniciar el lexer para procesar los tokens en el parser
        lexer.input(fuente)
        tok = lexer.token()
        x = stack[-1]

        print("\n" + colored("<<<<<<<<<<<<<<<<< Proceso de Análisis Sintáctico >>>>>>>>>>>>>>>>>", "cyan", attrs=['bold', 'underline']))
        while True:
            print(colored(f"Token actual: {tok.type}", "green") + 
                  f", Valor: {tok.value}, Línea: {tok.lineno}" + 
                  colored(f" | Pila: {stack}", "magenta"))
            
            if x == tok.type and x == 'eof':
                print(colored("\nCadena terminada exitosamente. No se encontraron errores sintácticos.", "green", attrs=['bold']))
                return
            else:
                if x == tok.type and x != 'eof':
                    #Coincidencia exacta entre el token y el top de la pila
                    stack.pop()
                    x = stack[-1]
                    tok = lexer.token()
                elif x == 'finBloque' and tok.type == 'finBloque':
                    #Consume el finBloque y avanza
                    stack.pop()
                    tok = lexer.token()
                    if stack:
                        x = stack[-1]  #Actualiza el valor en la cima de la pila
                    continue
                elif x in ['comentario', 'comentario_bloque']:
                    #Manejo de comentarios (de una línea o bloque)
                    if x == tok.type:
                        stack.pop()
                        tok = lexer.token()
                    elif tok.type == 'eof':
                        stack.pop()
                    else:
                        print(colored(f"Error: se esperaba {x} pero se encontró {tok.type}", "red"))
                        return
                elif x not in tokens:
                    #Buscar en las tablas LL(1) si el top de la pila es un no terminal
                    celda = None
                    for nombre_tabla, tabla in tablas_ll1.items():
                        celda = buscar_en_tabla(x, tok.type, tabla)
                        if celda is not None:
                            print(colored(f"Producción encontrada: {x} -> {celda}", "blue"))
                            break
                    if celda is None:
                        print(colored(f"\nError: NO se esperaba {tok.type}", "red", attrs=['bold']))
                        print(colored(f"Producción esperada para {x}: {[p[1] for p in tabla if p[0] == x]}", "yellow"))
                        print(colored(f"En posición: {tok.lexpos}", "yellow"))
                        return
                    else:
                        stack.pop()
                        agregar_pila(celda)
                        x = stack[-1]
                else:
                    print(colored(f"Error: se esperaba {x} pero se encontró {tok.type}", "red"))
                    print(colored(f"En la posición: {tok.lexpos}", "yellow"))
                    print(colored("Pila actual:", "magenta"), stack)
                    return
    except FileNotFoundError:
        print(colored(f"El archivo '{nombre_archivo}' no se encontró.", "red"))
    except Exception as e:
        print(colored(f"Ocurrió un error: {e}", "red"))

def buscar_en_tabla(no_terminal, terminal, tabla):
    for i in range(len(tabla)):
        if tabla[i][0] == no_terminal and tabla[i][1] == terminal:
            return tabla[i][2]

def agregar_pila(produccion):
    for elemento in reversed(produccion):
        if elemento != 'vacia': 
            stack.append(elemento)

miParser('test.c')
