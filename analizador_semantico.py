# Analizador Semántico (en este caso, verificamos algunas reglas simples)
class AnalizadorSemantico:
    def __init__(self):
        self.errores = []

    def analizar(self, nodo):
        # Analizamos recursivamente el árbol
        if nodo.valor == "DeclaraciónTipo":
            # Aquí verificamos si la declaración de tipo es válida
            if not self.es_tipo_valido(nodo.token_value):
                self.errores.append(f"Error semántico: Tipo inválido '{nodo.token_value}' en la línea {nodo.token_value}")

        # Analizar los hijos del nodo
        for hijo in nodo.hijos:
            self.analizar(hijo)

    def es_tipo_valido(self, tipo):
        # Lista simple de tipos válidos
        tipos_validos = ["int", "float", "char"]
        return tipo in tipos_validos

    def imprimir_errores(self):
        if not self.errores:
            print("No se encontraron errores semánticos.")
        else:
            for error in self.errores:
                print(error)

# Función principal para usar el analizador semántico
def analizar_codigo(nombre_archivo):
    arbol_sintactico = miParser(nombre_archivo)  # Obtener el árbol sintáctico

    if arbol_sintactico:
        analizador = AnalizadorSemantico()
        analizador.analizar(arbol_sintactico)
        analizador.imprimir_errores()  # Imprimir los errores semánticos
