#ll1_tables.py

##################################################################################################
#                        TABLA DE PRODUCCIONES LL(1) PARA EL ANALIZADOR SINTÁCTICO               #
##################################################################################################


############################################################
#         TABLA: Variables, Operadores aritmeticos         #
############################################################
tabla_variables = [
    #Producción para S: permite que S procese declaraciones y asignaciones
    [0, 'int', [1, 'identificador', 2, 0]],       #int x; y continúa con otra declaración o asignación
    [0, 'float', [1, 'identificador', 2, 0]],     #float y; y continúa con otra declaración o asignación
    [0, 'char', [1, 'identificador', 2, 0]],      #char z; y continúa con otra declaración o asignación
    [0, 'identificador', [3, 0]],                 #Asignación: x = 5; y continúa con otra declaración o asignación
    [0, 'eof', ['eof']],                          #Fin de entrada, permite que termine en eof

    #Producción para TT: maneja tipos de datos
    [1, 'int', ['int']],
    [1, 'float', ['float']],
    [1, 'char', ['char']],

    #Producción para D: maneja el final de la declaración o más identificadores con asignación opcional
    [2, 'finInstruccion', ['finInstruccion']],              #Fin de instrucción, por ejemplo: x;
    [2, 'asignacion', ['asignacion', 5, 'finInstruccion']], #Asignación inicial con expresiones: x = 5 + 3;
    [2, 'coma', ['coma', 'identificador', 2]],              #Coma para una lista de identificadores, por ejemplo: x, y;

    #Producción para asignaciones (acepta expresiones aritméticas)
    [3, 'identificador', ['identificador', 'asignacion', 5, 'finInstruccion']],

    #Producción para valores asignables (acepta números y literales de caracteres)
    [4, 'NUMBER', ['NUMBER']],           #Valores asignables como números
    [4, 'char_literal', ['char_literal']],  #Valores asignables como literales de caracteres

    #Producción para expresiones (E)
    [5, 'NUMBER', [6]],                     #E -> T
    [5, 'identificador', [6]],              #E -> T
    [5, 'LPAREN', ['LPAREN', 5, 'RPAREN']], #E -> (E)
    [5, 'char_literal', [4]],               #E -> char_literal

    #Producción para T (términos con operadores)
    [6, 'NUMBER', ['NUMBER', 7]],           #T -> F T'
    [6, 'identificador', ['identificador', 7]], #T -> F T'
    [6, 'char_literal', ['char_literal', 7]],   #T -> F T' 
    [7, 'PLUS', ['PLUS', 6, 7]],            #T' -> + T T'
    [7, 'MINUS', ['MINUS', 6, 7]],          #T' -> - T T'
    [7, 'TIMES', ['TIMES', 6, 7]],          #T' -> * T T'
    [7, 'DIVIDE', ['DIVIDE', 6, 7]],        #T' -> / T T'
    [7, 'finInstruccion', []],              #T' -> ε
    [7, 'RPAREN', []]                   #T' -> ε para finalizar con paréntesis
   
]

############################################################
#                   TABLA: Comentarios                     #
############################################################
tabla_comentarios = [ #Tabla LL(1) de producciones para comentarios
    #Producción principal para manejar comentarios
    [0, 'comentario', [1, 0]],          #Maneja un comentario de una línea y continúa
    [0, 'comentario_bloque', [2, 0]],   #Maneja un comentario bloque y continúa
    [0, 'eof', ['eof']],                #Permite terminar directamente con eof

    #Producción para manejar el token 'comentario'
    [1, 'comentario', ['comentario']],  #Consume el token 'comentario'
    [1, 'eof', ['eof']],                #Si se encuentra un eof después, permite terminar correctamente
    [1, 'finBloque', []],               #Si hay un bloque pendiente, permite salir

    #Producción para manejar el token 'comentario_bloque'
    [2, 'comentario_bloque', ['comentario_bloque']],  #Consume el token 'comentario_bloque'
    [2, 'eof', ['eof']],                              #Si se encuentra un eof después, permite terminar correctamente
    [2, 'finBloque', []],                             #Si hay un bloque pendiente, permite salir
]

############################################################
#       TABLA: Condicionales y Operadores Logicos          #
############################################################
tabla_condicionales = [ #Tabla LL(1) de producciones para condicionales
    #Producción principal para condicionales
    [0, 'if', ['if', 'LPAREN', 5, 'RPAREN', 'inicioBloque', 0, 'finBloque', 0]],  #Permite más instrucciones después del bloque
    [0, 'else', ['else', 'inicioBloque', 0, 'finBloque', 0]],                     #Permite más instrucciones después del bloque else
    [0, 'finBloque', []],                    #Consume el finBloque y termina el bloque actual
    [0, 'eof', ['eof']],                     #Permite terminar con eof

    # Manejo del bloque `else`
    [1, 'else', ['else', 'inicioBloque', 0, 'finBloque', 0]],  #Permite continuar después del bloque else
    [1, 'finBloque', []],                                     #Consume el finBloque y termina
    [1, 'eof', []],                                           #Permite finalizar directamente si llega al final del archivo

    #Producción para expresiones condicionales (if)
    [5, 'identificador', [6]],             #Condiciones que empiezan con identificadores
    [5, 'NUMBER', [6]],                    #Condiciones que empiezan con números
    [5, 'LPAREN', ['LPAREN', 5, 'RPAREN']],#Condiciones con paréntesis anidados

    #Producción para términos en condiciones (comparadores y operandos)
    [6, 'identificador', ['identificador', 7]],  #Términos que usan identificadores
    [6, 'NUMBER', ['NUMBER', 7]],                #Términos que usan números
    [6, 'char_literal', ['char_literal', 7]],    #Términos que usan caracteres
    [6, 'LPAREN', ['LPAREN', 5, 'RPAREN']],      #Términos entre paréntesis

    #Producción para operadores de comparación
    [7, 'GREATER', ['GREATER', 6]],  #Mayor que
    [7, 'LESS', ['LESS', 6]],        #Menor que
    [7, 'RPAREN', []],               #Fin de la condición
    [7, 'finBloque', []],            #Fin del bloque si se encuentra directamente
    [7, 'eof', []],                  #Permite terminar al final del archivo
]

############################################################
#                     TABLA: Scanf y Printf                #
############################################################
tabla_scanf_printf = [ #Tabla LL(1) de producciones para scanf y printf
    #Producción principal para el programa
    [0, 'scanf', [1, 0]],                        #Procesa scanf y continúa con más instrucciones
    [0, 'printf', [2, 0]],                       #Procesa printf y continúa con más instrucciones
    [0, 'eof', ['eof']],                         #Fin de entrada, permite terminar en eof

    #Producción para scanf
    [1, 'scanf', ['scanf', 'LPAREN', 3, 'coma', 5, 'RPAREN', 'finInstruccion']],  #scanf("%d", &var);

    #Producción para printf
    [2, 'printf', ['printf', 'LPAREN', 3, 6, 'RPAREN', 'finInstruccion']],        #printf("%d", var);

    #Producción para cadenas o formatos (formato de scanf/printf)
    [3, 'cadena', ['cadena']],                                                   #Cadena regular
    [3, 'FORMAT', ['FORMAT']],                                                   #O formato ("%d", "%f")

    #Producción para lista de variables en scanf
    [5, 'AMPERSAND', ['AMPERSAND', 'identificador', 7]],  # Procesa &var o lista de variables

    #Producción para lista de valores en printf
    [6, 'coma', ['coma', 8]],  #Procesa lista de valores si está presente
    [6, 'RPAREN', []],         #Caso vacío (no hay valores adicionales)

    #Producción recursiva para lista de variables
    [7, 'coma', ['coma', 'AMPERSAND', 'identificador', 7]],  #Continúa procesando lista de variables (&var, &var2, ...)
    [7, 'RPAREN', []],                                       #Caso vacío (fin de la lista)

    #Producción recursiva para lista de valores
    [8, 'NUMBER', ['NUMBER', 8]],                #Valores adicionales numéricos
    [8, 'FLOAT', ['FLOAT', 8]],                  #Valores adicionales flotantes
    [8, 'CHAR', ['CHAR', 8]],                    #Valores adicionales de tipo caracter
    [8, 'identificador', ['identificador', 8]],  #Variables o identificadores
    [8, 'RPAREN', []],                           #Caso vacío (fin de la lista)
]

############################################################
#         TABLA: Instrucciones de iteración: while         #
############################################################
tabla_while = [ #Tabla LL(1) de producciones para ciclos while
    #Producción principal para `while`
    [0, 'while', ['while', 'LPAREN', 1, 'RPAREN', 'inicioBloque', 0, 'finBloque', 0]],

    #Producción para condiciones dentro del `while`
    [1, 'identificador', [2]],             #Condiciones que empiezan con identificadores
    [1, 'NUMBER', [2]],                    #Condiciones que empiezan con números
    [1, 'LPAREN', ['LPAREN', 1, 'RPAREN']],#Condiciones con paréntesis anidados

    #Producción para términos en condiciones (operandos de comparación)
    [2, 'identificador', ['identificador', 3]],  #Términos que usan identificadores
    [2, 'NUMBER', ['NUMBER', 3]],                #Términos que usan números

    #Producción para operadores de comparación (solo `>` y `<`)
    [3, 'GREATER', ['GREATER', 2]],  #Mayor que
    [3, 'LESS', ['LESS', 2]],        #Menor que
    [3, 'RPAREN', []],               #Fin de la condición
]

############################################################
#                      TABLA: Funciones                    #
############################################################
tabla_funciones = [
    #Producción principal para declaración/definición de funciones
    [0, 'void', ['void', 'identificador', 'LPAREN', 1, 'RPAREN', 3, 0]],   #void func() { Bloque }
    [0, 'int', ['int', 'identificador', 'LPAREN', 1, 'RPAREN', 3, 0]],     #int func() { Bloque }
    [0, 'float', ['float', 'identificador', 'LPAREN', 1, 'RPAREN', 3, 0]], #float func() { Bloque }
    [0, 'eof', ['eof']],                                                  #Fin del archivo

    #Producción para parámetros dentro de ( )
    [1, 'int', ['int', 'identificador', 2]],       #int x
    [1, 'float', ['float', 'identificador', 2]],   #float y
    [1, 'char', ['char', 'identificador', 2]],     #char z
    [1, 'RPAREN', []],                             #Sin parámetros (ε)

    #Producción para lista de parámetros
    [2, 'coma', ['coma', 1]],                      #, siguiente parámetro
    [2, 'RPAREN', []],                             #Fin de la lista (ε)

    #Producción para el bloque o cuerpo de la función
    [3, 'inicioBloque', ['inicioBloque', 4, 'finBloque']],  #{ Cuerpo de la función }

    #Producción para instrucciones dentro del cuerpo
    [4, 'int', [0]],              #Reutiliza la tabla de variables
    [4, 'float', [0]],            #Reutiliza la tabla de variables
    [4, 'char', [0]],             #Reutiliza la tabla de variables
    [4, 'identificador', [0]],    #Reutiliza la tabla de asignaciones
    [4, 'printf', [0]],           #Reutiliza la tabla de scanf/printf
    [4, 'scanf', [0]],            #Reutiliza la tabla de scanf/printf
    [4, 'if', [0]],               #Reutiliza la tabla de condicionales
    [4, 'while', [0]],            #Reutiliza la tabla de ciclos
    [4, 'comentario', [0]],       #Reutiliza la tabla de comentarios
    [4, 'comentario_bloque', [0]],#Reutiliza la tabla de comentarios
    [4, 'finBloque', []],         #Permite cerrar el bloque
    [4, 'eof', []],               #Termina al final del archivo
]