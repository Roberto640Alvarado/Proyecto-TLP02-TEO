# ------------------------------------------------------------
# Lexer y parser para C con soporte para múltiples tablas LL1
# ------------------------------------------------------------
import ply.lex as lex
from ll1_tables import tabla_comentarios, tabla_condicionales, tabla_scanf_printf, tabla_while, tabla_unificada
from terminals import *  #Tokens y reglas de expresión regular
from non_terminals import *  #Los no terminales
from tabulate import tabulate
from termcolor import colored

#Clase Nodo para el Árbol Sintáctico
class Nodo:
    def __init__(self, valor, token_value=None):
        self.valor = valor
        self.token_value = token_value
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def __str__(self, nivel=0):
        resultado = "  " * nivel + str(self.valor)
        if self.token_value:  #Mostrar el valor del token si está disponible
            resultado += f" ({self.token_value})"
        resultado += "\n"
        for hijo in self.hijos:
            resultado += hijo.__str__(nivel + 1)
        return resultado

#Diccionario de nombres para producciones
producciones_nombres = {
    0: 'Programa',
    1: 'DeclaraciónTipo',
    2: 'DeclaraciónResto',
    3: 'ListaParámetros',
    4: 'Bloque',
    5: 'Asignación',
    6: 'ListaVariables',
    7: 'Instrucción',
    8: 'ParámetrosExtra',
    9: 'Expresión',
    10: 'DeclaraciónExtra',
    11: 'InstruccionesBloque',
    12: 'ExpresiónRelacional',
    13: 'OperadorRelacional',
    14: 'Comentario',
    15: 'Return',
    16: 'Printf',
    17: 'Scanf',
    18: 'ExpresiónReturn',
    19: 'ElseOpcional',
    20: 'ListaArgumentos',
    21: 'ListaVariablesScanf',
    22: 'ExpresiónAdición',
    23: 'ExpresiónRelacionalExtra',
    24: 'ExpresiónMultiplicación',
    25: 'ExpresiónAdiciónExtra',
    26: 'ExpresiónUnaria',
    27: 'ExpresiónMultiplicaciónExtra',
    28: 'Primaria',
    29: 'LlamadaFunción',
    30: 'Argumentos',
    31: 'ArgumentosExtra',
    32: 'AsignaciónVariable'
}

#Lista de puntos de sincronización
puntos_sincronizacion = ['void', 'finInstruccion', 'finBloque', 'inicioBloque', 'if', 'while', 'for', 'return', 'eof']

#Lista global para almacenar errores sintácticos
errores_sintacticos = []

#Tablas LL1
tablas_ll1 = {
    "tabla_unificada": tabla_unificada,
    "tabla_comentarios": tabla_comentarios,
    "tabla_condicionales": tabla_condicionales,
    "tabla_scanf_printf": tabla_scanf_printf,
    "tabla_while": tabla_while
}

#Construye el lexer
lexer = lex.lex()

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Función para imprimir los tokens en una tabla
def print_tokens_table(tokens):
    headers = ["ID", "Tipo", "Valor", "Línea", "Posición"]
    formatted_data = [[idx + 1, tok.type, tok.value, tok.lineno, tok.lexpos] for idx, tok in enumerate(tokens)]
    
    table = tabulate(formatted_data, headers, tablefmt="fancy_grid")
    print(colored(table, "green"))

#Guardar árbol en archivo
def guardar_arbol_en_archivo(arbol, nombre_archivo):
    with open(nombre_archivo, "w") as archivo:
        archivo.write(str(arbol))

#Función que realiza el análisis sintáctico
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
        lexer.lineno = 1  #Reiniciar el número de línea
        tok = lexer.token()

        #Nodo raíz del árbol sintáctico
        arbol = Nodo("Programa")  #"Programa" es el no terminal inicial
        stack = [("eof", None), (0, arbol)]  #Pila con nodos del árbol

        #Preguntar si se desea ver el detalle del parser
        detalleParser = input("¿Desea ver el detalle del parser? (s/n): ")
        if detalleParser == 's':
            detalleParser = True
        else:
            detalleParser = False

        print("\n" + colored("<<<<<<<<<<<<<<<<< Proceso de Análisis Sintáctico >>>>>>>>>>>>>>>>>", "cyan", attrs=['bold', 'underline']))
        print("\n")
        while True:
            if not stack:
                print(colored("Error fatal: pila vacía.", "red"))
                break

            x, nodo_actual = stack.pop()  #Pop con el nodo asociado

            pila_color = colored([s[0] for s in stack], "magenta")
            #Usar lexer.lineno para obtener la línea actual
            linea_actual = lexer.lineno if tok else -1

            if detalleParser:     
                print(f"Token actual: {colored(tok.type, 'cyan')} | Valor: {colored(tok.value, 'yellow')} | Línea: {colored(linea_actual, 'green')} | Pila: {pila_color}")

            if x == tok.type and x == 'eof':
                print("Cadena terminada exitosamente")
                print("\n<<<<<<<<<<<<<<<<<<<<<< Árbol Sintáctico >>>>>>>>>>>>>>>>>>>>>>>")
                guardar_arbol_en_archivo(arbol, "Arbol_Sintactico.txt")
                print("Árbol sintáctico guardado en 'Arbol_Sintactico.txt'")
                break

            elif x == tok.type and x != 'eof':
                #Agregar el valor del token al nodo del árbol
                nodo_actual.agregar_hijo(Nodo(tok.type, tok.value))
                tok = lexer.token()  #Obtener el siguiente token

            elif isinstance(x, int):  #No terminal
                for nombre_tabla, tabla in tablas_ll1.items():
                    celda = buscar_en_tabla(x, tok.type, tabla)
                    if celda is not None:
                        nombre_no_terminal = producciones_nombres.get(x, f"Producción_{x}")  #Nombre descriptivo
                        print(colored(f"Producción encontrada: {nombre_no_terminal} -> {celda}", "blue"))
                        nuevos_hijos = []
                        for simbolo in reversed(celda):
                            if simbolo != 'vacia':
                                hijo = Nodo(producciones_nombres.get(simbolo, simbolo))  #Uso de nombres descriptivos
                                nuevos_hijos.append(hijo)
                                stack.append((simbolo, hijo))  #Agregar a la pila
                        nodo_actual.hijos.extend(reversed(nuevos_hijos))  #Agregar los nodos hijos al árbol
                        break
                else:
                    #Si no se encuentra una producción válida, usar modo pánico
                    registrar_error(tok, "Producción inválida")
                    tok = modo_panico(tok, puntos_sincronizacion, stack)  # Activar modo pánico
                    if tok is None:  #Si no se puede recuperar, detener el análisis
                        break

            else:
                #Error de no coincidencia entre pila y token actual, usar modo pánico
                registrar_error(tok, f"Se esperaba '{x}' pero se encontró '{tok.type}'")
                tok = modo_panico(tok, puntos_sincronizacion, stack)  # Activar modo pánico
                if tok is None:  #Si no se puede recuperar, detener el análisis
                    break

        #Imprimir la tabla de errores sintácticos al final
        print_errors_table()
        return arbol if not errores_sintacticos else None

    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def registrar_error(token, mensaje):
    """Registra un error sintáctico con el valor del token."""
    errores_sintacticos.append({
        "Línea": token.lineno if token else "EOF",
        "Encontrado": f"{token.type} ({token.value})" if token else "EOF",
        "Valor": mensaje
    })


def print_errors_table():
    """Imprime la tabla de errores sintácticos al final del análisis."""
    if errores_sintacticos:
        headers = ["Línea", "Encontrado", "Mensaje"]
        formatted_data = [
            [error["Línea"], error["Encontrado"], error["Valor"]]
            for error in errores_sintacticos
        ]
        table = tabulate(formatted_data, headers, tablefmt="fancy_grid")
        print(colored("\n<<<<<<<<<<<<<<<<< Errores Sintácticos >>>>>>>>>>>>>>>>>", "red", attrs=['bold']))
        print(colored(table, "red"))
    else:
        print(colored("\nNo se encontraron errores sintácticos.", "green", attrs=['bold']))



def modo_panico(tok, puntos_sincronizacion, stack):
    """Modo de recuperación en caso de errores sintácticos."""
    print(colored(f"Entrando en modo pánico... Se encontró: {tok.type} ({tok.value})", "yellow"))
    #Avanzar tokens hasta encontrar un punto de sincronización
    while tok and tok.type not in puntos_sincronizacion:
        tok = lexer.token()
    if tok:
        print(colored(f"Recuperado en token: {tok.type} ({tok.value})", "yellow"))
        #Ajustar la pila del parser para continuar desde el nuevo token
        ajustar_pila_para_recuperacion(stack, tok)
    else:
        print(colored("Fin del archivo alcanzado durante la recuperación.", "yellow"))
    return tok



def ajustar_pila_para_recuperacion(stack, tok):
    """Ajusta la pila para intentar sincronización con el token actual."""
    while stack:
        x = stack[-1][0]  #Obtener el elemento actual de la pila
        #Si x puede derivar al token actual, dejamos de desapilar
        if x == tok.type or puede_derivar(x, tok.type):
            print(colored(f"Sincronización lograda con {x} en la pila.", "green"))
            return
        else:
            print(colored(f"Desapilando {x} durante la recuperación.", "yellow"))
            stack.pop()
    #Si la pila quedó vacía, inicializamos el estado para continuar
    if not stack:
        #Reinicializar la pila con el token actual si es válido
        if tok.type in puntos_sincronizacion:
            stack.append(("eof", None))
            stack.append((0, Nodo("Programa")))

def puede_derivar(no_terminal, terminal):
    """Verifica si un no terminal puede derivar un terminal."""
    for tabla in tablas_ll1.values():
        for produccion in tabla:
            if produccion[0] == no_terminal and produccion[1] == terminal:
                return True
    return False

#Buscar en la tabla
def buscar_en_tabla(no_terminal, terminal, tabla):
    for produccion in tabla:
        if produccion[0] == no_terminal and produccion[1] == terminal:
            print(f"Producción encontrada: {no_terminal} -> {produccion[2]} con terminal {terminal}")
            return produccion[2]
    return None

miParser('test.c')
