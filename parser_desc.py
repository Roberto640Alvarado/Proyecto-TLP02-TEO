# ------------------------------------------------------------
# Lexer y parser para C #Equipo
# ------------------------------------------------------------
import ply.lex as lex
from ll1_tables import tabla_comentarios, tabla_condicionales, tabla_scanf_printf, tabla_while, tabla_unificada
from terminals import *  #Tokens y reglas de expresión regular
from non_terminals import *  #Los no terminales
from tabulate import tabulate
from termcolor import colored

#Tablas LL1 
tablas_ll1 = {
    "tabla_unificada": tabla_unificada,
    "tabla_comentarios": tabla_comentarios,
    "tabla_condicionales": tabla_condicionales,
    "tabla_scanf_printf": tabla_scanf_printf,
    "tabla_while": tabla_while
}

#Lista de puntos de sincronización
puntos_sincronizacion = ['finInstruccion', 'finBloque', 'inicioBloque', 'if', 'while', 'for', 'return', 'eof']


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
        lexer.lineno = 1  # Reiniciar el número de línea
        
        # Obtener todos los tokens en una lista para mostrarlos en una tabla
        tokens = []
        tok = lexer.token()
        while tok:
            tokens.append(tok)
            tok = lexer.token()
        
        # Imprimir los tokens
        print("\n" + colored("<<<<<<<<<<<<<<<<< Tabla de Tokens >>>>>>>>>>>>>>>>>", "yellow", attrs=['bold']))
        print_tokens_table(tokens)
        
        # Reiniciar el lexer para procesar los tokens en el parser
        lexer.input(fuente)
        lexer.lineno = 1  
        tok = lexer.token()
        x = stack[-1]

        print("\n" + colored("<<<<<<<<<<<<<<<<< Proceso de Análisis Sintáctico >>>>>>>>>>>>>>>>>", "cyan", attrs=['bold', 'underline']))
        print("\n")
        while True:
            print(
                colored(f"Token: {tok.type}", "green") + 
                f" | Valor: {colored(tok.value, 'yellow')}" + 
                f" | Línea: {colored(tok.lineno, 'cyan')}" + 
                f" | Pila: {colored(', '.join(map(str, stack)), 'magenta')}"
            )
            
            if x == tok.type and x == 'eof':
                if 'finBloque' in stack:
                    print(colored(f"\nError: Falta 'finBloque' antes de finalizar el archivo.", "red", attrs=['bold']))
                    return
                print(colored("\nArchivo terminado exitosamente. No se encontraron errores sintácticos.", "green", attrs=['bold']))
                return
            elif x == tok.type and x != 'eof':
                # Coincidencia exacta entre el token y el top de la pila
                stack.pop()
                if stack:
                    x = stack[-1]
                else:
                    x = None
                tok = lexer.token()
            elif x == 'finBloque':
                # Validar cierre de bloque
                if tok.type == 'finBloque':
                    stack.pop()
                    tok = lexer.token()
                    if stack:
                        x = stack[-1]
                    else:
                        x = None
                else:
                    print(colored(f"\nError: Se esperaba 'finBloque', pero se encontró {tok.type}.", "red", attrs=['bold']))
                    print(colored(f"Línea: {tok.lineno}", "yellow"))
                    # Modo pánico
                    tok = modo_panico(tok, puntos_sincronizacion, stack)
                    if not tok or tok.type == 'eof':
                        break  # Fin del archivo
                    if stack:
                        x = stack[-1]
                    else:
                        x = None
            elif x not in tokens:
                celda = None
                for nombre_tabla, tabla in tablas_ll1.items():
                    celda = buscar_en_tabla(x, tok.type, tabla)
                    if celda is not None:
                        print(colored(f"Producción encontrada: {x} -> {celda}", "blue"))
                        break
                if celda is None:
                    print(colored(f"\nError: NO se esperaba {tok.type}", "red", attrs=['bold']))
                    print(colored(f"Línea: {tok.lineno}", "yellow"))
                    # Modo pánico
                    tok = modo_panico(tok, puntos_sincronizacion, stack)
                    if not tok or tok.type == 'eof':
                        break  # Fin del archivo
                    if stack:
                        x = stack[-1]
                    else:
                        x = None
                    continue
                else:
                    stack.pop()
                    agregar_pila(celda)
                    if stack:
                        x = stack[-1]
                    else:
                        x = None
            else:
                print(colored(f"Error: Se esperaba {x} pero se encontró {tok.type}", "red"))
                print(colored(f"Línea: {tok.lineno}", "yellow"))
                print(colored("Pila actual:", "magenta"), stack)
                # Modo pánico
                tok = modo_panico(tok, puntos_sincronizacion, stack)
                if not tok or tok.type == 'eof':
                    break  # Fin del archivo
                if stack:
                    x = stack[-1]
                else:
                    x = None
    except FileNotFoundError:
        print(colored(f"El archivo '{nombre_archivo}' no se encontró.", "red"))
    except Exception as e:
        print(colored(f"Ocurrió un error: {e}", "red"))

def modo_panico(tok, puntos_sincronizacion, stack):
    print(colored("Entrando en modo pánico...", "yellow"))
    # Avanzar tokens hasta encontrar un punto de sincronización
    while tok and tok.type not in puntos_sincronizacion:
        tok = lexer.token()
    if tok:
        print(colored(f"Recuperado en token: {tok.type}", "yellow"))
        # Ajustar la pila del parser
        ajustar_pila_para_recuperacion(stack, tok)
    else:
        print(colored("Fin del archivo alcanzado durante la recuperación.", "yellow"))
    return tok

def ajustar_pila_para_recuperacion(stack, tok):
    while stack:
        x = stack[-1]
        # Si x puede derivar al token actual, dejamos de desapilar
        if x in tokens or puede_derivar(x, tok.type):
            break
        else:
            stack.pop()

def puede_derivar(no_terminal, terminal):
    for tabla in tablas_ll1.values():
        for produccion in tabla:
            if produccion[0] == no_terminal and produccion[1] == terminal:
                return True
    return False


def buscar_en_tabla(no_terminal, terminal, tabla):
    for i in range(len(tabla)):
        if tabla[i][0] == no_terminal and tabla[i][1] == terminal:
            return tabla[i][2]

def agregar_pila(produccion):
    for elemento in reversed(produccion):
        if elemento != 'vacia': 
            stack.append(elemento)

miParser('test.c')