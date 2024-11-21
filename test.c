int x,z;
float y = 3.0;

int suma(int a, int b) {
    //comentario
    int resultado;
    if(a > b) {
        resultado = a -+ b;
    } else {
        resultado = a + b;
    }

    while (a < b) {
        a = a + 1;
    }

    /*esto es un comentario
    de varias lineas*/
    
    return resultado;
}

int main(){
    return 0;
}

void saludo() {
    printf("Hola mundo");
}
