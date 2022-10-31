from simpleai.search import CspProblem, backtrack

def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    
    esquinas = [(
        (0, 0), (0, columnas - 1), (filas - 1, 0), (filas - 1, columnas - 1),
    )]
    
    # Definimos las variables
    #Las variables son las paredes, las cajas, los objetivos y el jugador. 
    filas = 3
    columnas = 4
    cantidad_paredes = 3
    cantidad_cajas_objetivos = 2
    paredes = []
    cajas = []
    objetivos = []
    jugador = [('jugador')]
    
    #Definimos la cantidad de paredes, cajas y objetivos. 
    for x in range(cantidad_paredes):
        paredes.append('pared' + str(x))
    
    for x in range(cantidad_cajas_objetivos):
        cajas.append('caja', + str(x))
        objetivos.append('objetivo', + str(x))
    
    variables = [jugador + paredes + cajas + objetivos]
    
    #Definimos los dominios
    #Los dominios son las posiciones del mapa (fila, columna) que se le pueden asignar a las variables(jugador, paredes, cajas, objetivos)
    
    dominio = {}
    for variable in variables:
        for f in range(filas):
            for c in range(columnas):
                #Restringir el dominio de la variable cajas -> no se pueden ubicar en las esquinas. 
                if (f,c) not in esquinas and variable in cajas:
                    dominio[variable] = [(f,c)]
                else:
                    dominio[variable] = [(f,c)]
                