# Proyecto TLP02-2024 - Compilador de C Estándar

## Integrantes: 

- Albeño Ortega, Douglas Alejandro (00166120)
- Alfaro Angel, Katerin Alexandra (00240620)
- Alvarado Beltrán, Roberto Carlos (00176620)
- Arucha Aguilar, Edwin Enrique (00175420)
- Gallardo Ayala, Raúl Antonio (00145620)
- Iglesias Moreno, David Alejandro (00047920)
          

## Descripción

El presente proyecto tiene como objetivo el desarrollo de un analizador sintáctico para un subconjunto del lenguaje de programación C estándar, implementando gramáticas libres de contexto y técnicas de análisis descendente LL(1).  
Este tipo de analizador es una herramienta fundamental en la construcción de compiladores, ya que permite:

- Procesar código fuente.
- Verificar la conformidad con las reglas sintácticas del lenguaje.
- Gestionar errores de forma eficiente.

## Instalación de bibliotecas necesarias

Antes de ejecutar el proyecto correctamente, es fundamental instalar las librerías necesarias:

### PLY (Python Lex-Yacc)  
PLY es una herramienta muy útil que permite construir analizadores léxicos y sintácticos en Python.  
**Comando de instalación:**  
``` bash
pip install ply
```
### Tabulate: 
La biblioteca Tabulate es una solución flexible y sencilla para presentar datos en formato tabular dentro de aplicaciones de Python.
Comando de instalación: 
**Comando de instalación:**  
``` bash
pip install tabulate
```
### Termcolor: 
La biblioteca Tabulate es una solución flexible y sencilla para presentar datos en formato tabular dentro de aplicaciones de Python.
Comando de instalación: 
**Comando de instalación:**  
``` bash
pip install termcolor
```

## Guía de uso 
Una vez instaladas las librerías mencionadas anteriormente, se debe ejecutar el archivo “parser_desc.py” por medio del comando: 
``` bash
python parser_desc.py
```
## Funcionamiento 
- **Tokens:**
Una vez que se ejecuta el archivo, la consola mostrará una tabla detallada con los tokens identificados durante el análisis.
Esta tabla proporciona información sobre los elementos léxicos encontrados en el código, facilitando la comprensión y validación del proceso.

- **Opciones de detalle:**
Al final de la tabla, se presentará una opción para que el usuario decida si desea visualizar el proceso del parser con un nivel de detalle más profundo o continuar sin esa información adicional.

  Si acepta, se mostrará de manera detallada el proceso del parser, desglosando línea por línea la información analizada junto con los valores correspondientes.

  Si rechaza, se presentará una versión más ordenada y resumida de la información, enfocándose únicamente en los aspectos esenciales del análisis.

- **Manejo de errores:**
Cuando el parser entra en **modo pánico**, busca automáticamente la siguiente instrucción válida para continuar con el análisis según las reglas definidas en las tablas LL(1).

  Este mecanismo permite al parser intentar recuperar la continuidad del proceso incluso después de un error.
  Si durante esta evaluación se encuentran inconvenientes adicionales, como inconsistencias o errores, estos serán registrados y mostrados claramente en la salida con detalles específicos del problema identificado.

- **Árbol sintáctico:**
Si el análisis se realiza sin errores, se generará un **árbol sintáctico** que representará la estructura del código evaluado.
Este árbol se guardará automáticamente en un archivo de texto para su posterior consulta.

- **Reporte de errores:**
Al final del proceso, se generará una tabla detallando los errores sintácticos encontrados durante el análisis, proporcionando información clara y precisa para facilitar su corrección.
