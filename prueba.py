from compilador import compilador
from main import LectorExpresionRegular, AFNaAFD


class Prueba:
    def prueba(self):
        alfabeto = 'ab'
        lector = LectorExpresionRegular(alfabeto)
        afn = compilador(lector)
        afn.imprimir_tabla_transiciones()
        convertido_a_afd = AFNaAFD(afn)
        afd = convertido_a_afd.conversion()
        afd.imprimir_tabla_transiciones()
        return afd
