import ply.lex as lex
from termcolor import colored
import terminals  #Archivo con los tokens

def ejecutar_analizador(input_file):
    #Leer el archivo de entrada
    try:
        with open(input_file, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(colored(f"El archivo {input_file} no existe.", "red"))
        return

    #Crear el analizador léxico
    lexer = lex.lex(module=terminals)

    lexer.input(source_code)

    symbol_table = {}

    tokens = []
    tok = lexer.token()
    while tok:
        tokens.append(tok)
        tok = lexer.token()

    errors = []

    #Analizador semántico
    i = 0
    current_function = None
    while i < len(tokens):
        token = tokens[i]

        if token.type in ("int", "float", "char", "void"):
            #Declaración de variable o función
            var_type = token.type
            if i + 1 < len(tokens) and tokens[i + 1].type == "identificador":
                var_name = tokens[i + 1].value
                if i + 2 < len(tokens) and tokens[i + 2].type == "LPAREN":
                    #Es una función
                    if var_name in symbol_table:
                        errors.append(f"Error: Función '{var_name}' redeclarada en la línea {token.lineno}.")
                    else:
                        symbol_table[var_name] = {"type": var_type, "category": "function", "has_return": False}
                        current_function = var_name  #Seguimiento de la función actual
                else:
                    #Es una variable
                    if var_name in symbol_table:
                        errors.append(f"Error: Variable '{var_name}' redeclarada en la línea {token.lineno}.")
                    else:
                        symbol_table[var_name] = {"type": var_type, "category": "variable"}
                i += 2
                while i < len(tokens) and tokens[i].type == "coma":
                    i += 1
                    if i < len(tokens) and tokens[i].type == "identificador":
                        var_name = tokens[i].value
                        if var_name in symbol_table:
                            errors.append(f"Error: Variable '{var_name}' redeclarada en la línea {token.lineno}.")
                        else:
                            symbol_table[var_name] = {"type": var_type, "category": "variable"}
                        i += 1
                continue

        elif token.type == "return":
            #Verificar el tipo de retorno
            if current_function:
                func_info = symbol_table[current_function]
                func_type = func_info["type"]
                func_info["has_return"] = True
                if func_type == "void" and i + 1 < len(tokens) and tokens[i + 1].type != "finInstruccion":
                    errors.append(f"Error: La función 'void {current_function}' no debe retornar ningún valor (línea {token.lineno}).")
                elif func_type in ("int", "float") and (i + 1 >= len(tokens) or tokens[i + 1].type == "finInstruccion"):
                    errors.append(f"Error: La función '{current_function}' debe retornar un valor del tipo '{func_type}' (línea {token.lineno}).")

        elif token.type == "identificador":
            #Verificar si es una variable o función declarada
            var_name = token.value
            if var_name not in symbol_table:
                errors.append(f"Error: Identificador '{var_name}' no declarado en la línea {token.lineno}.")

        if token.type == "finBloque":
            #Cerrar el alcance de una función
            current_function = None

        i += 1

    #Validar funciones que requieren retorno pero no lo tienen
    for name, info in symbol_table.items():
        if info["category"] == "function" and info["type"] in ("int", "float") and not info["has_return"]:
            if name != "main":  #Excepción: main puede no retornar explícitamente en algunos casos
                errors.append(f"Error: La función '{name}' de tipo '{info['type']}' no tiene una sentencia de retorno.")

    #Mostrar resultados del análisis semántico
    print(colored("\n<<<<<<<<<<<<<<<<<<<<<< Análisis Semántico >>>>>>>>>>>>>>>>>>>>>>>", "cyan", attrs=["bold"]))
    print(colored("Errores:", "yellow", attrs=["bold"]))
    if errors:
        for error in errors:
            print(colored(error, "red"))
    else:
        print(colored("No se encontraron errores semánticos.", "green", attrs=["bold"]))


if __name__ == "__main__":
    #Define el archivo que quieres analizar
    ejecutar_analizador("test.c")

