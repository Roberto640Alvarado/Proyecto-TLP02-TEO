#ll1_tables.py

##################################################################################################
#                        TABLA DE PRODUCCIONES LL(1) PARA EL ANALIZADOR SINTÁCTICO               #
##################################################################################################


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

##################################################################################################
#       TABLA UNIFICADA ACTUALIZADA DE PRODUCCIONES LL(1) PARA VARIABLES Y FUNCIONES             #
##################################################################################################

tabla_unificada = [
    #Producción inicial S: procesa declaraciones, definiciones de funciones y asignaciones
    [0, 'int', [1, 'identificador', 2, 0]],
    [0, 'float', [1, 'identificador', 2, 0]],
    [0, 'char', [1, 'identificador', 2, 0]],
    [0, 'void', [1, 'identificador', 2, 0]],
    [0, 'identificador', [7, 0]],  #Para asignaciones y expresiones
    [0, 'return', [15, 0]],        #Para sentencias return
    [0, 'if', [9, 0]],             #Estructuras if
    [0, 'while', [10, 0]],         #Estructuras while
    [0, 'printf', [16, 0]],        #Sentencias printf
    [0, 'scanf', [17, 0]],         #Sentencias scanf
    [0, 'comentario', [14, 0]],    #Comentarios
    [0, 'comentario_bloque', [14, 0]], #Comentarios de bloque
    [0, 'inicioBloque', ['inicioBloque', 0, 'finBloque']],  #Bloques anidados
    [0, 'finBloque', []],          #Permite cerrar bloques
    [0, 'eof', ['eof']],           #Fin del archivo

    #Producción para Type: tipos de datos
    [1, 'int', ['int']],
    [1, 'float', ['float']],
    [1, 'char', ['char']],
    [1, 'void', ['void']],

    #Producción para DeclarationPrime: decide entre función o variable
    [2, 'LPAREN', ['LPAREN', 3, 'RPAREN', 4]],   #Función
    [2, 'asignacion', [5]],                      #Variable con asignación
    [2, 'coma', [6]],                            #Lista de variables
    [2, 'finInstruccion', ['finInstruccion']],   #Fin de declaración de variable

    #Producción para ParameterList: parámetros de función
    [3, 'int', [1, 'identificador', 8]],
    [3, 'float', [1, 'identificador', 8]],
    [3, 'char', [1, 'identificador', 8]],
    [3, 'RPAREN', []],  #Sin parámetros (ε)

    #Producción para ParameterListPrime: más parámetros
    [8, 'coma', ['coma', 3]],
    [8, 'RPAREN', []],  #Fin de la lista de parámetros

    #Producción para Block: cuerpo de la función
    [4, 'inicioBloque', ['inicioBloque', 11, 'finBloque']],  #Usamos 11 para las sentencias dentro del bloque

    #Producción para VariableDeclarator (asignación opcional)
    [5, 'asignacion', ['asignacion', 9, 10]],
    [5, 'finInstruccion', ['finInstruccion']],
    [5, 'coma', [6]],

    #Producción para VariableDeclaratorList: lista de variables
    [6, 'coma', ['coma', 'identificador', 5]],
    [6, 'finInstruccion', ['finInstruccion']],

    #Producción para Expression: E
    [9, 'identificador', [12]],
    [9, 'NUMBER', [12]],
    [9, 'FLOAT', [12]],
    [9, 'LPAREN', [12]],
    [9, 'char_literal', [12]],

    #Producción para E_rel: E_add E_rel'
    [12, 'identificador', [22, 23]],
    [12, 'NUMBER', [22, 23]],
    [12, 'FLOAT', [22, 23]],
    [12, 'LPAREN', [22, 23]],
    [12, 'char_literal', [22, 23]],

    #Producción para E_rel': ('>' | '<') E_add E_rel' | ε
    [23, 'GREATER', ['GREATER', 22, 23]],
    [23, 'LESS', ['LESS', 22, 23]],
    [23, 'PLUS', []],
    [23, 'MINUS', []],
    [23, 'TIMES', []],
    [23, 'DIVIDE', []],
    [23, 'finInstruccion', []],
    [23, 'coma', []],
    [23, 'RPAREN', []],
    [23, 'finBloque', []],

    #Producción para E_add: E_mul E_add'
    [22, 'identificador', [24, 25]],
    [22, 'NUMBER', [24, 25]],
    [22, 'FLOAT', [24, 25]],
    [22, 'LPAREN', [24, 25]],
    [22, 'char_literal', [24, 25]],

    #Producción para E_add': ('+' | '-') E_mul E_add' | ε
    [25, 'PLUS', ['PLUS', 24, 25]],
    [25, 'MINUS', ['MINUS', 24, 25]],
    [25, 'GREATER', []],
    [25, 'LESS', []],
    [25, 'finInstruccion', []],
    [25, 'coma', []],
    [25, 'RPAREN', []],
    [25, 'finBloque', []],

    #Producción para E_mul: E_unary E_mul'
    [24, 'identificador', [26, 27]],
    [24, 'NUMBER', [26, 27]],
    [24, 'FLOAT', [26, 27]],
    [24, 'LPAREN', [26, 27]],
    [24, 'char_literal', [26, 27]],

    #Producción para E_mul': ('*' | '/') E_unary E_mul' | ε
    [27, 'TIMES', ['TIMES', 26, 27]],
    [27, 'DIVIDE', ['DIVIDE', 26, 27]],
    [27, 'PLUS', []],
    [27, 'MINUS', []],
    [27, 'GREATER', []],
    [27, 'LESS', []],
    [27, 'finInstruccion', []],
    [27, 'coma', []],
    [27, 'RPAREN', []],
    [27, 'finBloque', []],

    #Producción para E_unary
    [26, 'identificador', [28]],
    [26, 'NUMBER', [28]],
    [26, 'FLOAT', [28]],
    [26, 'LPAREN', [28]],
    [26, 'char_literal', [28]],

    #Producción para Primary
    [28, 'identificador', ['identificador']],
    [28, 'NUMBER', ['NUMBER']],
    [28, 'FLOAT', ['FLOAT']],
    [28, 'LPAREN', ['LPAREN', 9, 'RPAREN']],
    [28, 'char_literal', ['char_literal']],

    #Producción para continuar después de la asignación/expresión
    [10, 'coma', [6]],
    [10, 'finInstruccion', ['finInstruccion']],

    #Producción para asignaciones y expresiones (Statement)
    [7, 'identificador', ['identificador', 'asignacion', 9, 'finInstruccion']],

    #Producción para comentarios
    [14, 'comentario', ['comentario']],
    [14, 'comentario_bloque', ['comentario_bloque']],

    #Producción para sentencias return
    [15, 'return', ['return', 18, 'finInstruccion']],

    #Producción para expresión opcional en return
    [18, 'identificador', [9]],
    [18, 'NUMBER', [9]],
    [18, 'FLOAT', [9]],
    [18, 'LPAREN', [9]],
    [18, 'char_literal', [9]],
    [18, 'finInstruccion', []],  # Permite 'return;' sin expresión

    #Producción para estructuras if
    [9, 'if', ['if', 'LPAREN', 9, 'RPAREN', 'inicioBloque', 11, 'finBloque', 19]],

    #Producción para else opcional
    [19, 'else', ['else', 'inicioBloque', 11, 'finBloque']],
    [19, 'int', []],
    [19, 'float', []],
    [19, 'char', []],
    [19, 'identificador', []],
    [19, 'return', []],
    [19, 'if', []],
    [19, 'while', []],
    [19, 'printf', []],
    [19, 'scanf', []],
    [19, 'comentario', []],
    [19, 'comentario_bloque', []],
    [19, 'finBloque', []],
    [19, 'eof', []],

    #Producción para estructuras while
    [10, 'while', ['while', 'LPAREN', 9, 'RPAREN', 'inicioBloque', 11, 'finBloque']],

    #Producción para sentencias printf
    [16, 'printf', ['printf', 'LPAREN', 'cadena', 20, 'RPAREN', 'finInstruccion']],

    #Producción para lista de argumentos en printf
    [20, 'coma', ['coma', 9]],
    [20, 'RPAREN', []],

    #Producción para sentencias scanf
    [17, 'scanf', ['scanf', 'LPAREN', 'cadena', 'coma', '&', 'identificador', 21, 'RPAREN', 'finInstruccion']],

    #Producción para lista de variables en scanf
    [21, 'coma', ['coma', '&', 'identificador', 21]],
    [21, 'RPAREN', []],

    #Producción para sentencias dentro del bloque de la función
    [11, 'int', [1, 'identificador', 2, 11]],          #Declaraciones de variables
    [11, 'float', [1, 'identificador', 2, 11]],
    [11, 'char', [1, 'identificador', 2, 11]],
    [11, 'void', [1, 'identificador', 2, 11]],         #Funciones anidadas si se permite
    [11, 'identificador', [7, 11]],                    #Asignaciones
    [11, 'return', [15, 11]],                          #Sentencias return
    [11, 'if', [9, 11]],                               #Estructuras if
    [11, 'while', [10, 11]],                           #Estructuras while
    [11, 'printf', [16, 11]],                          #Sentencias printf
    [11, 'scanf', [17, 11]],                           #Sentencias scanf
    [11, 'comentario', [14, 11]],                      #Comentarios
    [11, 'comentario_bloque', [14, 11]],               #Comentarios de bloque
    [11, 'finBloque', []],                             #Fin del bloque
    [11, 'eof', []],                                   #Fin del archivo
]
