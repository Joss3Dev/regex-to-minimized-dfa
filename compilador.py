from main import *


alfabeto = 'ab'


def compilador(lector):

    def print_tokens(tokens):
        for t in tokens:
            print(t)

    lector.set_regex('x', 'a+.(b|a).b?')
    lector.set_regex('y', 'b.(b*.a.b|a?.b.a+).a?')
    tokens = lector.parsear()
    gestor = GestorEstados(lector)

    print_tokens(tokens)

    stack_afn = []
    for t in tokens:
        gestor.gestores[t.nombre](t, stack_afn)

    assert len(stack_afn) == 1
    return gestor.afn
