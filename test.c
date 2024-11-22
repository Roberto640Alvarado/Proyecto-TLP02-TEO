int x,z;
float y = 3.0;

int suma(int a, int b) {
    //comentario
    int resultado;
    if(a > b) {
        resultado = a - b;
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

void saludo() {
    printf("Hola mundo");
}

int main(){
    int num1, num2, resultado;
    printf("Ingrese el primer número: ");
    scanf("%d", &num1);

    //resultado = suma(num1, num2);

    //saludo();
    return 0;
}
