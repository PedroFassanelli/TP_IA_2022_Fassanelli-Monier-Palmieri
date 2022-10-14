from simpleai.search import SearchProblem, astar, breadth_first, depth_first
from simpleai.search.viewers import WebViewer, BaseViewer

def jugar(paredes, cajas, objetivos, jugador, maximos_movimientos):
    
    '''
    A partir de las coordenadas de paredes, cajas, objetivos, jugador y cantidad maxima de movimientos recibidos
    como parametros, se arma el estado, ese estado se pasa al problema que retorna el resultado. 
    '''

    #El estado inicial es una tupla que tiene:
    # - tupla de tuplas con la posiciones de las cajas
    # - tupla de tuplas con la posiciones de los objetivos
    # - posicion del jugador
    # - cantidad maxima de movimientos realizados
    
    estado_inicial = (tuple(cajas), tuple(objetivos), jugador, maximos_movimientos)
    
    #(((0, 3), (2, 4)), ((1, 3), (4, 5)), (2, 2), 30)
    #    cajas           objetivos        jugador   maximos_movimientos
    
    class SokobanProblem(SearchProblem):
        def is_goal(self, state):
            cajas, objetivos, jugador, movimientos = state
            #Otra opcion es que la cantidad de cajas u objetivos sea 0, cada vez que una caja llegue al objetivo, sacarla de la lista. 
            #return len(cajas) == 0 o len(objetivos) == 0
            return cajas == objetivos
        
        def cost(self, state1, action, state2):
            return 1
        
        def actions(self, state):
            #Las acciones posibles son: 
            # -Mover al jugador a una casilla adyacente, evitando las paredes. 
            # -Si en la casilla adyacente al jugador hay una caja, el jugador puede empujar la caja a una posicion adyacente que no tenga otra caja. 
            acciones_disponibles = []
            cajas, objetivos, jugador, movimientos = state
            (f_jugador, c_jugador) = jugador

            if movimientos > 0:
                for f, c in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    jugador_nueva_fila = f_jugador + f
                    jugador_nueva_columna = c_jugador + c
                    jugador_nueva_posicion = (jugador_nueva_fila, jugador_nueva_columna)
                    
                    if jugador_nueva_posicion not in paredes:
                        acciones_disponibles.append(jugador_nueva_posicion)
                        if jugador_nueva_posicion in cajas:
                            caja_nueva_fila = jugador_nueva_fila + f
                            caja_nueva_columna = jugador_nueva_columna + c
                            caja_nueva_posicion = (caja_nueva_fila, caja_nueva_columna)
                            if caja_nueva_posicion not in paredes and caja_nueva_posicion not in cajas:                       
                                acciones_disponibles.append(caja_nueva_posicion)
            return acciones_disponibles
        
        def result(self, state, action):
            cajas, objetivos, jugador, movimientos = state
            nueva_pos_jugador, nueva_pos_caja = action 
            pass
        def heuristic(self, state):
            pass
    
    problem = SokobanProblem(estado_inicial)
    # viewer = WebViewer()
    
    #result = astar(problem, graph_search=False)
    #result = astar(problem, graph_search=True, viewer=WebViewer())
    # result = breadth_first(problem, graph_search=True)
    # result = limited_depth_first(problem, graph_search=True, viewer=viewer, depth_limit=3)
    #result = depth_first(problem,  graph_search=True)
    
    secuencia = []
    # Recorrer el resultado agregando a la lista secuencia, las acciones seleccionadas por el algoritmo
    for action, state in result.path():
        # print("Action:", action)
        # print("State:", state)
        # print()
        # Descartar la primera acción que es None
        if (action is not None):
            secuencia.append(action)
    return secuencia
    
if __name__ == '__main__':
    print('Resolviendo...')

    paredes = [(5, 1), (6, 1), (6, 2)]
    cajas = [(0,3),(2,4),(3,2)]
    objetivos = [(1,3),(4,5)]
    jugador = (2,2)
    maximos_movimientos = 30
    
    secuencia = jugar(paredes, cajas, objetivos, jugador, maximos_movimientos)
    print(secuencia)