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
    #Producción para S: punto de entrada para comentarios (una línea o bloque)
    [0, 'comentario', [1, 0]],         #Maneja comentarios de una línea y continúa con otras producciones
    [0, 'comentario_bloque', [2, 0]],  #Maneja comentarios multilínea y continúa con otras producciones
    [0, 'eof', ['eof']],               #Fin del archivo

    #Producción para A' (comentarios de una línea)
    [1, 'comentario', ['comentario']],  #Solo acepta el token de un comentario simple

    #Producción para A'' (comentarios multilínea)
    [2, 'comentario_bloque', ['comentario_bloque']]  #Solo acepta el token de un comentario bloque
]
