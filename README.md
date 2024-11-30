# Proyecto TLP02-2024 - Compilador de C Estándar

## Integrantes:

- Albeño Ortega, Douglas Alejandro (00166120)
- Alfaro Angel, Katerin Alexandra (00240620)
- Alvarado Beltrán, Roberto Carlos (00176620)
- Arucha Aguilar, Edwin Enrique (00175420)
- Gallardo Ayala, Raúl Antonio (00145620)
- Iglesias Moreno, David Alejandro (00047920)

---

## Descripción

El presente proyecto tiene como objetivo el desarrollo de un analizador sintáctico para un subconjunto del lenguaje de programación C estándar, implementando gramáticas libres de contexto y técnicas de análisis descendente LL(1).  
Este tipo de analizador es una herramienta fundamental en la construcción de compiladores, ya que permite:

- Procesar código fuente.
- Verificar la conformidad con las reglas sintácticas del lenguaje.
- Gestionar errores de forma eficiente.

Adicionalmente, si no se detectan errores durante el análisis sintáctico:
- Se generará un **árbol sintáctico** que representará la estructura del código evaluado.
- Se realizará un análisis semántico para validar la coherencia del programa.
En caso de encontrar errores, se mostrará una tabla detallada con los errores sintácticos identificados.

---

## Instalación de bibliotecas necesarias

Antes de ejecutar el proyecto correctamente, es fundamental instalar las librerías necesarias:

### PLY (Python Lex-Yacc)  
PLY es una herramienta muy útil que permite construir analizadores léxicos y sintácticos en Python.  
**Comando de instalación:**  
```bash
pip install ply
```

### Tabulate  
La biblioteca Tabulate es una solución flexible y sencilla para presentar datos en formato tabular dentro de aplicaciones de Python.  
**Comando de instalación:**  
```bash
pip install tabulate
```

### Termcolor  
Termcolor mejora la visualización de texto en terminales mediante colores y estilos.  
**Comando de instalación:**  
```bash
pip install termcolor
```

---

## Guía de uso

Una vez instaladas las librerías mencionadas anteriormente, se debe ejecutar el archivo “parser_desc.py” por medio del comando:  
```bash
python parser_desc.py
```

---

## Funcionamiento

### Tokens
Al ejecutar el archivo, la consola mostrará una tabla detallada con los **tokens** identificados durante el análisis. Esta tabla proporciona información clara sobre los elementos léxicos encontrados en el código.

### Opciones de detalle
Al final de la tabla, se presentará una opción para que el usuario decida si desea visualizar el proceso del parser con un nivel de detalle más profundo o continuar sin esa información adicional.

- Si acepta, se mostrará de manera detallada el proceso del parser, desglosando línea por línea la información analizada junto con los valores correspondientes.
- Si rechaza, se presentará una versión más ordenada y resumida de la información, enfocándose únicamente en los aspectos esenciales del análisis.

### Manejo de errores
El parser utiliza un enfoque de **modo pánico**, buscando automáticamente la siguiente instrucción válida para continuar el análisis. Si encuentra errores adicionales, estos se registrarán y se mostrarán detalladamente en la salida.

### Árbol sintáctico y análisis semántico
- **Sin errores:**  
  Si no se detectan errores sintácticos, se generará un **árbol sintáctico** que representará la estructura del código analizado, el cual se guardará automáticamente en un archivo de texto. Además, se realizará un análisis semántico para validar la coherencia del programa.
  
- **Con errores:**  
  Si se detectan errores durante el análisis, se generará una **tabla de errores** detallando los problemas encontrados para facilitar su corrección. 

