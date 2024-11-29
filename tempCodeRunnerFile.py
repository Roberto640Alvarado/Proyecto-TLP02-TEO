def modo_panico(tok, puntos_sincronizacion, stack):
    """Modo de recuperación en caso de errores sintácticos."""
    print(colored(f"Entrando en modo pánico... Se encontró: {tok.type} ({tok.value})", "yellow"))
    while tok and tok.type not in puntos_sincronizacion:
        tok = lexer.token()
        if tok:
            print(colored(f"Avanzando al token: {tok.type} ({tok.value})", "yellow"))
    if tok:
        print(colored(f"Recuperado en token: {tok.type} ({tok.value})", "yellow"))
        ajustar_pila_para_recuperacion(stack, tok)
    else:
        print(colored("Fin del archivo alcanzado durante la recuperación.", "yellow"))
    return tok