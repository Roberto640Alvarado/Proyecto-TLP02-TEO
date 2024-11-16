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
    [0, 'if', ['if', 'LPAREN', 5, 'RPAREN', 'inicioBloque', 0, 'finBloque', 1]],
    [0, 'finBloque', []],  #Permitir que un bloque termine directamente
    [0, 'eof', ['eof']],  #Permitir terminar directamente en `eof`

    #Manejo del bloque else 
    [1, 'else', ['else', 'inicioBloque', 0, 'finBloque']],  #Si hay un else, abre un bloque nuevo
    [1, 'finBloque', []],  #Si no hay else, acepta epsilon para terminar el bloque
    [1, 'eof', []],  #Permite finalizar directamente si llega al final del archivo

    #Producción para expresiones condicionales (if)
    [5, 'identificador', [6]],  #Condiciones que empiezan con identificadores
    [5, 'NUMBER', [6]],  #Condiciones que empiezan con números
    [5, 'LPAREN', ['LPAREN', 5, 'RPAREN']],  #Condiciones con paréntesis anidados

    #Producción para términos en condiciones (comparadores y operandos)
    [6, 'identificador', ['identificador', 7]],  #Términos que usan identificadores
    [6, 'NUMBER', ['NUMBER', 7]],  #Términos que usan números
    [6, 'char_literal', ['char_literal', 7]],  #Términos que usan caracteres
    [6, 'LPAREN', ['LPAREN', 5, 'RPAREN']],  #Términos entre paréntesis

    #Producción para operadores de comparación
    [7, 'GREATER', ['GREATER', 6]],  #Mayor que
    [7, 'LESS', ['LESS', 6]],  #Menor que
    [7, 'RPAREN', []],  #Fin de la condición
    [7, 'finBloque', []],  #Fin del bloque si se encuentra directamente
    [7, 'eof', []],  #Permite terminar al final del archivo
]
