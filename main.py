import numpy as np
import sys


class TablaSimbolos:
    indice = 0
    tabla = {}

    def cargar_tabla(self, token, valor):
        self.tabla[self.indice] = [token, valor]
        self.aumentar_indice()

    def aumentar_indice(self):
        self.indice += 1


class Token:
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def __str__(self):
        return self.nombre + ":" + self.valor

    def __repr__(self):
        return str(self)


class ExpresionRegular:
    def __init__(self, patron):
        self.patron = patron
        self.actual = 0
        self.longitud = len(self.patron)

    def __str__(self):
        return 'REGEX: ' + self.patron

    def __repr__(self):
        return str(self)

    def get_token(self, lector):
        if self.actual < self.longitud:
            c = self.patron[self.actual]
            self.actual += 1
            if c not in lector.simbolos.keys():
                token_ret = Token('PALABRA', c)
            else:
                token_ret = Token(lector.simbolos[c], c)
            return token_ret
        else:
            return Token('NULL', '')


class LectorExpresionRegular:
    def __init__(self, alfabeto):
        self.expresiones = []
        self.alfabeto = alfabeto
        self.simbolos = {'(': 'PAR_IZQ', ')': 'PAR_DER', '.': 'CONCAT', '*': 'AST', '|': 'OR', '+': 'MAS', '?': 'INTERR'}
        self.actual = 0
        self.tokens = []
        self.sig_token = None

    def __str__(self):
        return 'Lector: ' + self.alfabeto

    def __repr__(self):
        return str(self)

    def set_regex(self, patron):
        expresion = ExpresionRegular(patron)
        self.expresiones.append(expresion)
        if not self.sig_token:
            self.sig_token = self.get_token()

    def get_token(self):
        # No hace falta validar el token como en el get_token de ExpresionRegular ya que el for en parsear
        # ejecuta solo con las expresiones que hay en self
        token = self.expresiones[self.actual].get_token(self)
        if token.valor == '':
            self.actual += 1
        return token

    def consumir(self, nombre):
        if self.sig_token.nombre == nombre:
            self.sig_token = self.get_token()
        elif self.sig_token.nombre != nombre:
            raise ValueError("Caracter desconocido en la Expresion Regular.")

    def parsear(self):
        for exp in self.expresiones:
            self.exp()
        for i in range(len(self.expresiones)-1):
            self.tokens.append(Token('OR', '|'))
        return self.tokens

    def exp(self):
        self.term()
        if self.sig_token.nombre == 'OR':
            token = self.sig_token
            self.consumir('OR')
            self.exp()
            self.tokens.append(token)

    def term(self):
        self.factor()
        if self.sig_token.nombre == 'CONCAT':
            token = self.sig_token
            self.consumir('CONCAT')
            self.term()
            self.tokens.append(token)

    def factor(self):
        self.palabra()
        if self.sig_token.nombre in ['AST', 'MAS', 'INTERR']:
            self.tokens.append(self.sig_token)
            self.consumir(self.sig_token.nombre)

    def palabra(self):
        self.null()
        if self.sig_token.nombre == 'PAR_IZQ':
            self.consumir('PAR_IZQ')
            self.exp()
            self.consumir('PAR_DER')
        elif self.sig_token.nombre == 'PALABRA':
            self.tokens.append(self.sig_token)
            self.consumir('PALABRA')

    def null(self):
        if self.sig_token.nombre == 'NULL':
            self.consumir('NULL')


class Estado:
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return str(self.valor)

    def __repr__(self):
        return str(self)


class AFN:
    def __init__(self, alfabeto):
        self.d_estados = []
        self.estados = []
        self.estado_ini = []
        self.estados_fin = []
        self.alfabeto = alfabeto

    def __str__(self):
        return 'AFN: ' + self.alfabeto

    def __repr__(self):
        return str(self)

    def imprimir_tabla_transiciones(self):
        print(end='\t')
        for caracter in self.alfabeto:
            print(caracter, end='\t\t')
        print('ε')
        for estado in self.estados:
            print(str(estado.valor) + ':', end='\t')
            cant_alfab = len(self.alfabeto)
            for caracter in range(cant_alfab+1):
                if caracter != cant_alfab:
                    print(self.d_estados[self.pos_estado(estado)][caracter], end='\t\t')
                else:
                    print(self.d_estados[self.pos_estado(estado)][caracter], end='\t\t')
            print()
        #
        # np_afn = np.array(self.d_estados)
        # np.set_printoptions(threshold=sys.maxsize)
        # print(np_afn)


    def cargar_estado(self, estado, transiciones, tipo=None):
        self.estados.append(estado)
        self.d_estados.append([])
        pos = self.pos_estado(estado)
        # Asumiendo que transiciones ya viene con todas las posiciones del alfabeto ya sea ocupado o vacio,
        # hasta la transicion vacia.
        if len(self.d_estados[pos]) == 0:
            self.d_estados[pos] = transiciones
        else:
            for i, caracter in enumerate(self.alfabeto):
                self.d_estados[pos][i].append(transiciones[i])
        if tipo == 'INI':
            self.estado_ini.append(estado)
        elif tipo == 'FIN':
            self.estados_fin.append(estado)

    def agregar_transicion(self, estado_a_agregar, estado, caracter=None):
        if not caracter:
            caracter = -1
        else:
            caracter = self.pos_car(caracter)
        self.d_estados[self.pos_estado(estado)][caracter].append(estado_a_agregar)

    def eliminar_transicion(self, estado_a_eliminar, estado, caracter=None):
        if not caracter:
            caracter = -1
        else:
            caracter = self.pos_car(caracter)
        self.d_estados[self.pos_estado(estado)][caracter].remove(estado_a_eliminar)

    def contatenar(self, estado_fin_1, estado_ini_2):
        self.eliminar_ini(estado_ini_2)
        self.eliminar_fin(estado_fin_1)
        self.agregar_transicion(estado_ini_2, estado_fin_1)

    def get_transiciones(self, estado):
        return self.d_estados[self.pos_estado(estado)]

    def eliminar_ini(self, estado):
        self.estado_ini.remove(estado)

    def eliminar_fin(self, estado):
        self.estados_fin.remove(estado)

    def pos_car(self, caracter):
        return self.alfabeto.index(caracter)

    def pos_estado(self, estado):
        return self.estados.index(estado)


class GestorEstados:
    def __init__(self, lector):
        self.gestores = {'PALABRA': self.manejar_palabra, 'CONCAT': self.manejar_concat, 'OR': self.manejar_or,
                         'AST': self.manejar_rep, 'MAS': self.manejar_rep, 'INTERR': self.manejar_interr}
        self.lector = lector
        self.cant_estados = 0
        self.afn = AFN(lector.alfabeto)

    def crear_estado(self):
        self.cant_estados += 1
        return Estado(self.cant_estados)

    def manejar_palabra(self, t, afn_stack):
        e0 = self.crear_estado()
        e1 = self.crear_estado()
        transiciones_e0 = [[] for c in self.afn.alfabeto]
        transiciones_e0.append([])
        transiciones_e0[self.afn.pos_car(t.valor)].append(e1)
        transiciones_e1 = [[] for c in self.afn.alfabeto]
        transiciones_e1.append([])
        self.afn.cargar_estado(e0, transiciones_e0, 'INI')
        self.afn.cargar_estado(e1, transiciones_e1, 'FIN')
        ini = e0
        fin = e1
        elemento = (ini, fin)
        afn_stack.append(elemento)

    def manejar_concat(self, t, afn_stack):
        transicion2 = afn_stack.pop()
        transicion1 = afn_stack.pop()
        self.afn.contatenar(transicion1[1], transicion2[0])
        elemento = (transicion1[0], transicion2[1])
        afn_stack.append(elemento)

    def manejar_or(self, t, afn_stack):
        transicion2 = afn_stack.pop()
        transicion1 = afn_stack.pop()
        self.afn.eliminar_ini(transicion1[0])
        self.afn.eliminar_ini(transicion2[0])
        self.afn.eliminar_fin(transicion1[1])
        self.afn.eliminar_fin(transicion2[1])

        e0 = self.crear_estado()
        transiciones_e0 = [[] for c in self.afn.alfabeto]
        transiciones_e0.append([])
        transiciones_e0[-1].append(transicion1[0])
        transiciones_e0[-1].append(transicion2[0])
        self.afn.cargar_estado(e0, transiciones_e0, 'INI')

        e1 = self.crear_estado()
        transiciones_e1 = [[] for c in self.afn.alfabeto]
        transiciones_e1.append([])
        self.afn.cargar_estado(e1, transiciones_e1, 'FIN')

        self.afn.agregar_transicion(e1, transicion1[1])
        self.afn.agregar_transicion(e1, transicion2[1])
        elemento = (e0, e1)
        afn_stack.append(elemento)

    def manejar_rep(self, t, afn_stack):
        transicion = afn_stack.pop()

        self.afn.eliminar_ini(transicion[0])
        self.afn.eliminar_fin(transicion[1])

        e0 = self.crear_estado()
        e1 = self.crear_estado()
        transiciones_e0 = [[] for c in self.afn.alfabeto]
        transiciones_e0.append([])
        transiciones_e0[-1].append(transicion[0])
        if t.nombre == 'AST':
            transiciones_e0[-1].append(e1)
        self.afn.cargar_estado(e0, transiciones_e0, 'INI')

        transiciones_e1 = [[] for c in self.afn.alfabeto]
        transiciones_e1.append([])
        self.afn.cargar_estado(e1, transiciones_e1, 'FIN')

        self.afn.agregar_transicion(e1, transicion[1])
        self.afn.agregar_transicion(transicion[0], transicion[1])

        elemento = (e0, e1)
        afn_stack.append(elemento)

    def manejar_interr(self, t, afn_stack):
        transicion = afn_stack.pop()
        self.afn.agregar_transicion(transicion[1], transicion[0])
        afn_stack.append(transicion)


class EstadoAFD:
    def __init__(self, valor, estados):
        self.valor = valor
        self.estados = estados
        self.marcado = False


# Hacer uno aparte para el AFD, este solo genera la conversion pero no tiene su ini, fin ni trancisiones
# lo mismo con el estado, mejor hacerle un diccionario
class AFD:

    def __init__(self, afn):
        self.afn = afn
        self.nro = 0
        self.d_estados = []
        self.estado_ini = []
        self.estados_fin = []

    def crear_estado(self, estados):
        estado_nuevo = EstadoAFD(self.nro, estados)
        self.nro += 1
        self.d_estados.append(estado_nuevo)
        return estado_nuevo

    def buscar_estado_en_afd(self, estados_en_afn):
        existe = False
        cant_estados_afd = len(self.d_estados)
        i = 0
        e = set(estados_en_afn)
        while not existe and i < cant_estados_afd:
            estado = self.d_estados[i]
            estados_en_afd = set(estado.estados)
            if estados_en_afd == e:
                existe = estado
            i += 1
        return existe

    def cerradura_eps(self, estados):
        estados_eps = set()
        for e in estados:
            estados_eps |= set([e])
            trans_eps = self.afn.get_transiciones(e)[-1]
            if len(trans_eps) > 0:
                estados_eps |= set(self.cerradura_eps(trans_eps))
        return list(estados_eps)

    def mover(self, estados, caracter):
        mov = set()
        pos_car = self.afn.pos_car(caracter)
        for e in estados:
            transiciones_e = self.afn.get_transiciones(e)[pos_car]
            if len(transiciones_e):
                mov |= set(transiciones_e)
        return list(mov)

    def conversion(self):
        cola = [self.crear_estado(self.cerradura_eps(self.afn.estado_ini))]
        while len(cola) > 0:
            estado_afd = cola.pop(0)
            if not estado_afd.marcado:
                estado_afd.marcado = True
                for c in self.afn.alfabeto:
                    mover = self.mover(estado_afd.estados, c)
                    c_eps = self.cerradura_eps(mover)
                    existe = self.buscar_estado_en_afd(c_eps) # busca si es que no existe en d_estados otro estado con esos estados
                    if not existe:
                        u = self.crear_estado(c_eps) # si no existe asigna a "u" esos estados y lo agrega a la cola y a d_estados
                        # crear el vinculo desde estado_afd hacia u con el caracter c
                        cola.append(u)
                    else:
                        # crear el vinculo desde estado_afd hacia existe con el caracter c
        return self.d_estados
