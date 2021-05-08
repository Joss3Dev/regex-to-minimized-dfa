from compilador import compilador
from main import LectorExpresionRegular, AFD

alfabeto = 'ab'
lector = LectorExpresionRegular(alfabeto)
afn = compilador(lector)
afn.imprimir_tabla_transiciones()
convertido_a_afd = AFD(afn)
afd = convertido_a_afd.conversion()