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
        return (abs(pos1-pos2) + abs(pos1-pos2)) == 1

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
        objetivos, paredes = variables 

        for obj in objetivos:
            if obj in paredes:
                return False
        return True 
    constraints.append(([OBJETIVOS] + PAREDES, obj_no_en_paredes))

    #Restriccion: Todas las cajas no deben estar en posiciones objetivos. Algunas cajas comienzan sobre objetivos. 
    def cajas_no_en_todos_obj(variables, values):
        cajas, objetivos = variables
        for caja in cajas:
            if caja not in objetivos:
                return True             #No todas las cajas estan en los objetivos
        return False
    constraints.append(([CAJAS] + OBJETIVOS, cajas_no_en_todos_obj))

    #Restriccion: Las cajas no deben tener mas de una pared adyacente.
    #Restriccion: Las cajas en los bordes no deben tener ninguna pared adyacente. 
    def caja_no_ady_pared(variables, values):
        cajas, *paredes = values
        cantidad_paredes_adyacentes = 0
        for caja in cajas:
            for pared in paredes:
                if adjacent([caja, pared]):
                    cantidad_paredes_adyacentes += 1
                    if en_borde(caja):
                        return cantidad_paredes_adyacentes == 0
                    else:
                        return cantidad_paredes_adyacentes <= 1
    constraints.append(([CAJAS] + PAREDES, caja_no_ady_pared))
    
    problem = CspProblem(problem_variables, domains, constraints)
    result = backtrack(problem)
    return(result)

# if __name__ == '__main__':
#     print('Trabajo Práctico Inteligencia Artificial')
#     filas=5
#     columnas=4
#     cantidad_paredes=3
#     cantidad_cajas_objetivos=2
#     mapa = armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos )
#     print(mapa)