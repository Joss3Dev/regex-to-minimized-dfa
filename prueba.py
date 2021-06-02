from compilador import compilador
from main import LectorExpresionRegular, AFNaAFD, GestorEstados


def main():
    print('Bienvenido al programa de conversion de Definiciones Regulares a Analizador Lexico.')
    ejecutar = True
    while ejecutar:
        print('Los operadores que se pueden utilizar para construir las Definiciones Regulares son:')
        print('Para concatenar: .')
        print('Para un OR: |')
        print('Para repeticion: * y +')
        print('Para un caracter opcional: ?')
        print('Parentesis para agrupar: ( )')
        print('Ejemplo: b.(b*.a.b|a?.b.a+)')
        print()
        alfabeto = input('Ingrese el alfabeto (ningun caracter debe ser igual a algun operador):')
        lector = LectorExpresionRegular(alfabeto)
        fin = False
        continuar = '1'
        while not fin:
            if continuar == '1':
                lado_izq = input('Ingrese el lado izquierdo:')
                patron = input('Ingrese el patron del token "'+str(lado_izq)+'" :')
                lector.set_regex(lado_izq, patron)
            continuar = input('Ingrese 1 si desea agregar otro token, 0 en caso contrario:')
            if continuar == '1':
                fin = False
            elif continuar == '0':
                fin = True
            else:
                print("Opcion desconocida.")
        tokens = lector.parsear()
        gestor = GestorEstados(lector)

        print_tokens(tokens)

        stack_afn = []
        for t in tokens:
            gestor.gestores[t.nombre](t, stack_afn)

        assert len(stack_afn) == 1
        afn = gestor.afn
        print()
        print('Tabla de trancisiones del AFN:')
        afn.imprimir_tabla_transiciones()
        convertido_a_afd = AFNaAFD(afn)
        afd = convertido_a_afd.conversion()
        print()
        print('Tabla de trancisiones del AFD sin minimizar:')
        afd.imprimir_tabla_transiciones()
        afd_min, pi = afd.minimizar()
        print()
        print('Tabla de trancisiones del AFD Minimizado:')
        afd_min.imprimir_tabla_transiciones()
        opciones = True
        while opciones:
            print('Ingrese el numero de la opcion que desea realizar:')
            print('(1) Evaluar cadenas en el AFD.')
            print('(2) Ver la tabla de trancisiones del AFN.')
            print('(3) Ver la tabla de trancisiones del AFD sin minimizar.')
            print('(4) Ver la tabla de trancisiones del AFD Minimizado.')
            print('(5) Ingresar otra Definicion Regular.')
            print('(6) Finalizar el programa.')
            opcion = input()
            if opcion == '1':
                evaluar = True
                opcion_evaluar = '2'
                while evaluar:
                    if opcion_evaluar == '2':
                        cadena_evaluar = input('Ingrese la cadena que desee evaluar:')
                        tabla_simbolos = afd_min.evaluar_cadena(cadena_evaluar)
                    print('Ingrese el numero de la opcion que desea realizar:')
                    print('(1) Ver la tabla de simbolos.')
                    print('(2) Evaluar otra cadena.')
                    print('(3) Atras.')
                    opcion_evaluar = input()
                    if opcion_evaluar == '1':
                        afd_min.imprimir_tabla_simbolos()
                    elif opcion_evaluar == '2':
                        evaluar = True
                    elif opcion_evaluar == '3':
                        evaluar = False
                    else:
                        print('Opcion desconocida.')
            elif opcion == '2':
                print('Tabla de trancisiones del AFN:')
                afn.imprimir_tabla_transiciones()
            elif opcion == '3':
                print('Tabla de trancisiones del AFD sin minimizar:')
                afd.imprimir_tabla_transiciones()
            elif opcion == '4':
                print('Tabla de trancisiones del AFD Minimizado:')
                afd_min.imprimir_tabla_transiciones()
            elif opcion == '5':
                opciones = False
                ejecutar = True
            elif opcion == '6':
                opciones = False
                ejecutar = False
            else:
                print('Opcion desconocida.')


def print_tokens(tokens):
    for t in tokens:
        print(t)


if __name__ == "__main__":
        main()
