from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)


def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    
    # Definimos las variables
    #Las variables son las paredes, las cajas, los objetivos y el jugador. 

    #Definimos la cantidad de paredes, cajas y objetivos. 
    PAREDES = [f'pared_{i}' for i in range(cantidad_paredes)]
    CAJAS = [f'caja_{i}' for i in range(cantidad_cajas_objetivos)]
    OBJETIVOS = [f'objetivo_{i}' for i in range(cantidad_cajas_objetivos)]
    JUGADOR = 'jugador'

    CASILLAS = [(f,c) for f in range(filas) for c in range(columnas)]
    ESQUINAS = [(0,0), (0, columnas -1), (filas - 1, 0), (filas - 1, columnas -1)]

    problem_variables = PAREDES + CAJAS + OBJETIVOS + [JUGADOR]
    #print(problem_variables)
    
    #Definimos los dominios
    #Los dominios son las posiciones del mapa (fila, columna) que se le pueden asignar a las variables(jugador, paredes, cajas, objetivos)
    
    domains = {}
    for variable in problem_variables:
        domains[variable] = CASILLAS

    #Restringir el dominio de la variable cajas -> no se pueden ubicar en las esquinas. 
    CASILLAS_SIN_ESQUINAS = [casilla for casilla in CASILLAS if casilla not in ESQUINAS]
    domains.update([(objeto, CASILLAS_SIN_ESQUINAS) for objeto in problem_variables if objeto in CAJAS])

    #print(domains)
    #Definimos las restricciones
    constraints = []

    #Funcion que retorna si dos posiciones son adyacentes. 
    def adjacent(posiciones):
        pos1, pos2 = posiciones
        distancia = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        return distancia == 1

    #Funcion que retorna si una posicion esta en el borde del mapa. 
    def en_borde(posicion):
        return posicion[0] in (0, filas - 1) or posicion[1] in (0, columnas - 1)

    #Restriccion: no puede haber dos objetos fisicos (paredes, cajas y jugador) en la misma posicion. 
    def dos_objetos_fisicos_misma_posicion(variables, values):
        return len(values) == len(set(values))

    for varable1, variable2 in combinations(problem_variables,2):
        constraints.append(((varable1, variable2), dos_objetos_fisicos_misma_posicion))
        
    #Restriccion: los objetivos no pueden estar en la misma posicion que las paredes. 
    def obj_no_en_paredes(variables, values):
        objetivos, *paredes = variables 
        for pared in paredes:
            if pared in objetivos:
                return False
        return True 
    constraints.append((tuple(OBJETIVOS + PAREDES), obj_no_en_paredes))
    
    #ValueError: too many values to unpack (expected 2) -> no se puede desempaquetar una lista de 1 elemento. 
    # Agregamos un * para que se desempaquete como una lista de 1 elemento.

    #Restriccion: Todas las cajas no deben estar en posiciones objetivos. Algunas cajas comienzan sobre objetivos. 
    def cajas_no_en_todos_obj(variables, values):
        cajas, *objetivos = variables
        for caja in cajas:
            if caja not in objetivos:
                return True             #No todas las cajas estan en los objetivos
        return False
    constraints.append((tuple(CAJAS + OBJETIVOS), cajas_no_en_todos_obj))
    
    
    #Funcion que devuelve las posiciones adyacentes a una posicion.
    def posiciones_adyacentes(fila_caja, columna_caja):
        adyacentes = []
        if fila_caja > 0:
            adyacentes.append((fila_caja-1, columna_caja))
        if fila_caja < filas - 1:
            adyacentes.append((fila_caja+1, columna_caja))
        if columna_caja > 0:
            adyacentes.append((fila_caja, columna_caja-1))
        if columna_caja < columnas - 1:
            adyacentes.append((fila_caja, columna_caja+1))
        return adyacentes

    #Funcion para comprobar si una posicion esta en el borde del mapa. 
    def es_borde(fila, columna):
        return fila in (0, filas - 1) or columna in (0, columnas - 1)
    
    #Restriccion: Las cajas no deben tener mas de una pared adyacente.
    #Restriccion: Las cajas en los bordes no deben tener ninguna pared adyacente. 
    def cantidad_paredes_adyacentes_caja(variables, values):
        fila_c, columna_c = values[0]
        
        adyacentes = []
        cantidad_paredes = 0
        adyacentes = posiciones_adyacentes(fila_c, columna_c)
        for pared in values:
            if pared in adyacentes:
                cantidad_paredes +=1
        if es_borde(fila_c, columna_c):            #Si la caja esta en el borde, no puede tener paredes adyacentes.
            return cantidad_paredes == 0
        else:
            return cantidad_paredes <= 1                 #Si la caja no esta en el borde, puede tener hasta una pared adyacente.
        
    #constraints.append((tuple(CAJAS + PAREDES), cantidad_paredes_adyacentes_caja))  #Tarda mucho en ejecutar los tests
    #Probamos con restriccion binaria y preguntamos si las paredes son mas de una o no para pasar el test. 
    if len(PAREDES) > 1:
        for pared1, pared2 in combinations(PAREDES, 2):
            for caja in CAJAS:
                constraints.append(((caja, pared1, pared2), cantidad_paredes_adyacentes_caja))
    else:
        constraints.append((tuple(CAJAS + PAREDES), cantidad_paredes_adyacentes_caja))
                
    #Codigo para ejecutar la solucion
    
    problema = CspProblem(problem_variables, domains, constraints)

    solucion = backtrack(
        problema,
        inference=False,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE,
    )

    lista_paredes = []
    lista_cajas = []
    lista_objetivos = []
    jugador = solucion['jugador']

    for pared in PAREDES:
        lista_paredes.append(solucion[pared])

    lista_cajas = []
    for caja in CAJAS:
        lista_cajas.append(solucion[caja])

    lista_objetivos = []
    for objetivo in OBJETIVOS:
        lista_objetivos.append(solucion[objetivo])

    return (lista_paredes, lista_cajas, lista_objetivos, jugador)