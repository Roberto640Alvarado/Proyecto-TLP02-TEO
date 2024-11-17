#ll1_tables.py

#Tabla LL(1) de producciones principal para variables, asignaciones, expresiones y operadores
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

# Tabla LL(1) de producciones para scanf y printf
tabla_scanf_printf = [
    # Producción principal para el programa
    [0, 'scanf', [1, 0]],                        # Procesa scanf y continúa con más instrucciones
    [0, 'printf', [2, 0]],                       # Procesa printf y continúa con más instrucciones
    [0, 'eof', ['eof']],                         # Fin de entrada, permite terminar en eof

    # Producción para scanf
    [1, 'scanf', ['scanf', 'LPAREN', 3, 'COMA', 5, 'RPAREN', 'SEMICOLON']],  # scanf("%d", var);

    # Producción para printf
    [2, 'printf', ['printf', 'LPAREN', 3, 6, 'RPAREN', 'SEMICOLON']],        # printf("%d", var);

    # Producción para formatos (formato de scanf/printf)
    [3, 'FORMAT', ['FORMAT']],  # Formato específico ("%d", "%c", "%f")

    # Producción para lista de variables (scanf)
    [5, 'identificador', ['identificador', 7]],  # Procesa una variable o lista de variables

    # Producción para lista de valores (printf)
    [6, 'COMA', ['COMA', 8]],  # Procesa lista de valores si está presente
    [6, 'RPAREN', []],         # Caso vacío (no hay valores adicionales)

    # Producción recursiva para lista de variables
    [7, 'COMA', ['COMA', 'identificador', 7]],  # Continúa procesando lista de variables
    [7, 'RPAREN', []],                          # Caso vacío (fin de la lista)

    # Producción recursiva para lista de valores
    [8, 'NUMBER', ['NUMBER', 8]],        # Valores adicionales numéricos (int)
    [8, 'FLOAT', ['FLOAT', 8]],          # Valores adicionales flotantes (float)
    [8, 'CHAR', ['CHAR', 8]],            # Valores adicionales de tipo caracter (char)
    [8, 'RPAREN', []],                   # Caso vacío (fin de la lista)

    # Terminales básicos para valores y variables
    [9, 'identificador', ['identificador']],  # Variable o identificador
    [9, 'NUMBER', ['NUMBER']],               # Valor numérico (int)
    [9, 'FLOAT', ['FLOAT']],                 # Valor flotante (float)
    [9, 'CHAR', ['CHAR']]                    # Valor de tipo caracter (char)
]

# Tabla LL(1) para funciones en C: Declaración y Definición
tabla_funciones = [
    # Producción principal para declaraciones (D)
    [0, 'void', [1, 'identificador', 'LPAREN', 2, 'RPAREN', 'SEMICOLON']],  # void fn();
    [0, 'int', [1, 'identificador', 'LPAREN', 2, 'RPAREN', 'SEMICOLON']],   # int fn();
    [0, 'float', [1, 'identificador', 'LPAREN', 2, 'RPAREN', 'SEMICOLON']], # float fn();

    # Producción principal para definiciones (F)
    [1, 'void', [1, 'identificador', 'LPAREN', 2, 'RPAREN', 'inicioBloque', 3, 'finBloque']],  # void fn() { ... }
    [1, 'int', [1, 'identificador', 'LPAREN', 2, 'RPAREN', 'inicioBloque', 3, 'finBloque']],   # int fn() { ... }
    [1, 'float', [1, 'identificador', 'LPAREN', 2, 'RPAREN', 'inicioBloque', 3, 'finBloque']], # float fn() { ... }

    # Producción para lista de parámetros (LP)
    [2, 'int', [1, 'identificador', 4]],    # int x, ...
    [2, 'float', [1, 'identificador', 4]],  # float y, ...
    [2, 'void', ['void']],                  # void (sin parámetros)
    [2, 'RPAREN', []],                      # Caso vacío (sin parámetros)

    # Producción recursiva para lista de parámetros adicionales
    [4, 'COMA', ['COMA', 1, 'identificador', 4]],  # int x, int y, ...
    [4, 'RPAREN', []],                             # Fin de lista de parámetros

    # Producción para lista de instrucciones (LI)
    [3, 'int', [1, 'identificador', 'SEMICOLON', 3]],      # Declaración dentro del bloque
    [3, 'float', [1, 'identificador', 'SEMICOLON', 3]],    # Declaración dentro del bloque
    [3, 'return', ['return', 5, 'SEMICOLON', 3]],          # return expr;
    [3, 'if', ['if', 'LPAREN', 5, 'RPAREN', 'inicioBloque', 3, 'finBloque', 3]],  # if (expr) { ... }
    [3, 'finBloque', []],                                  # Fin del bloque
    [3, 'eof', ['eof']],                                   # Fin de archivo

    # Producción para expresiones (E)
    [5, 'identificador', [6]],             # Expr: id = ...
    [5, 'NUMBER', [6]],                    # Expr: num = ...
    [5, 'LPAREN', ['LPAREN', 5, 'RPAREN']],# Expr: (expr)
    
    # Producción para términos en expresiones
    [6, 'identificador', ['identificador', 7]],  # Term: id op ...
    [6, 'NUMBER', ['NUMBER', 7]],                # Term: num op ...
    [6, 'LPAREN', ['LPAREN', 5, 'RPAREN']],      # Term: (expr)
    
    # Producción para operadores en expresiones
    [7, 'PLUS', ['PLUS', 6]],   # +
    [7, 'MINUS', ['MINUS', 6]], # -
    [7, 'TIMES', ['TIMES', 6]], # *
    [7, 'DIVIDE', ['DIVIDE', 6]],# /
    [7, 'SEMICOLON', []],       # Fin expr
    [7, 'RPAREN', []]           # Fin expr
]