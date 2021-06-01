from main import *


alfabeto = 'ab'


def compilador(lector):

    def print_tokens(tokens):
        for t in tokens:
            print(t)

    # lector.set_regex('digito', '0|1|2|3|4|5|6|7|8|9')
    lector.set_regex('digito', '0')
    lector.set_regex('digitos', 'digito.digito*')
    lector.set_regex('numero', 'digitos.(,.digitos)?.(E.-?.digitos)?')
    # lector.set_regex('letra', 'A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z')
    lector.set_regex('letra', 'A')
    lector.set_regex('id', 'letra(letra|digito)*')
    lector.set_regex('if', 'if')
    lector.set_regex('then', 'then')
    lector.set_regex('else', 'else')
    # lector.set_regex('oprel', '<|>|<=|>=|=|<>')
    lector.set_regex('oprel', '<')
    tokens = lector.parsear()
    gestor = GestorEstados(lector)

    print_tokens(tokens)

    stack_afn = []
    for t in tokens:
        gestor.gestores[t.nombre](t, stack_afn)

    assert len(stack_afn) == 1
    afn = gestor.afn
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
    return afn, afd, afd_min
