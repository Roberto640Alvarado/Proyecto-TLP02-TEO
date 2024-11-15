# l1_tables.py

#Tabla LL(1) de producciones principal para variables y asignaciones
tabla_variables = [
    #Producción para S: permite que S procese declaraciones y asignaciones
    [0, 'int', [1, 'identificador', 2, 0]],       #int x; y continua con otra declaración o asignación
    [0, 'float', [1, 'identificador', 2, 0]],     #float y; y continua con otra declaración o asignación
    [0, 'char', [1, 'identificador', 2, 0]],      #char z; y continua con otra declaración o asignación
    [0, 'identificador', [3, 0]],                 #Asignación: x = 5; y continua con otra declaración o asignación
    [0, 'eof', ['eof']],                          #Fin de entrada, permite que termine en eof
    
    #Producción para TT: maneja tipos de datos
    [1, 'int', ['int']],
    [1, 'float', ['float']],
    [1, 'char', ['char']],
    
    #Producción para D: maneja el final de la declaración o más identificadores con asignación opcional
    [2, 'finInstruccion', ['finInstruccion']],            #Fin de instrucción, por ejemplo: x;
    [2, 'asignacion', ['asignacion', 4, 'finInstruccion']], #Asignación inicial: float z = 3.14;
    [2, 'coma', ['coma', 'identificador', 2]],            #Coma para una lista de identificadores, por ejemplo: x, y;
    
    #Producción para asignaciones (acepta tanto NUMBER como char_literal)
    [3, 'identificador', ['identificador', 'asignacion', 4, 'finInstruccion']],
    
    #Producción para valores asignables (acepta números y literales de caracteres)
    [4, 'NUMBER', ['NUMBER']],
    [4, 'char_literal', ['char_literal']]
]
