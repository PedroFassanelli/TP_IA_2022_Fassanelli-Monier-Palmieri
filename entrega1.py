from simpleai.search import SearchProblem, astar, breadth_first, depth_first
from simpleai.search.viewers import WebViewer, BaseViewer

def jugar(paredes, cajas, objetivos, jugador, maximos_movimientos):
    
    '''
    A partir de las coordenadas de paredes, cajas, objetivos, jugador y cantidad maxima de movimientos recibidos
    como parametros, se arma el estado, ese estado se pasa al problema que retorna el resultado. 
    '''

    #El estado inicial es una tupla que tiene:
    # - tupla de tuplas con la posiciones de las cajas
    # - posicion del jugador
    # - cantidad maxima de movimientos realizados
    
    estado_inicial = (tuple(cajas), jugador, maximos_movimientos)
    print(estado_inicial)
    
    #(
    # ((0, 3), (2, 4)),  #Cajas 
    # (2, 2),     #Posicion del jugador
    # 30          #Movimientos disponibles
    # )
    
    ACCIONES_MOVER = [('Arriba', (-1, 0)),
                  ('Abajo', (1, 0)),
                  ('Izquierda', (0, -1)),
                  ('Derecha', (0, 1))]
    
    class SokobanProblem(SearchProblem):
        def is_goal(self, state):
            cajas, jugador, movimientos = state
            #Si todas las cajas estan en las posiciones objetivo. 
            return cajas == objetivos
        
        def cost(self, state1, action, state2):
            return 1
        
        def actions(self, state):
            #Las acciones posibles son: 
            # -Mover al jugador a una casilla adyacente, evitando las paredes. 
            # -Si en la casilla adyacente al jugador hay una caja, el jugador puede empujar la caja a una posicion adyacente que no tenga otra caja. 
            acciones_disponibles = []
            cajas, jugador, movimientos = state
            f_jugador, c_jugador = jugador

            if movimientos > 0:
                for nombre, (f, c) in ACCIONES_MOVER:
                    jugador_nueva_fila = f_jugador + f
                    jugador_nueva_columna = c_jugador + c
                    jugador_nueva_posicion = (jugador_nueva_fila, jugador_nueva_columna)
                    
                    if jugador_nueva_posicion not in paredes:
                        #Muevo si no hay pared, y la caja adyacente puede moverse.
                        if jugador_nueva_posicion in cajas:
                            caja_nueva_fila = jugador_nueva_fila + f
                            caja_nueva_columna = jugador_nueva_columna + c
                            caja_nueva_posicion = (caja_nueva_fila, caja_nueva_columna)
                            if caja_nueva_posicion not in paredes and caja_nueva_posicion not in cajas:                       
                                acciones_disponibles.append('Empujar', jugador_nueva_posicion, caja_nueva_posicion)   #El jugador se mueve con la caja.
                        else:
                            acciones_disponibles.append(nombre, jugador_nueva_posicion)    #No hay ni pared, ni caja adyacente, muevo al jugador. 
            return acciones_disponibles
        
        def result(self, state, action):
            cajas, jugador, movimientos = state
            #Identificamos hacia donde se mueve
            
            '''             
            direccion = ''
            if (jugador[0] - nueva_pos_jugador[0]) == 1:
                direccion = 'arriba' 
            if (jugador[0] - nueva_pos_jugador[0]) == -1:
                direccion = 'abajo'
            if (jugador[1] - nueva_pos_jugador[1]) == 1:
                direccion = 'izquierda'
            if (jugador[1] - nueva_pos_jugador[1]) == 1:
                direccion = 'derecha'
             '''
            
            if action[0] == 'Empujar':
                #Muevo al jugador y la caja
                nueva_pos_jugador = action[1]
                nueva_pos_caja = action[2]
                cajas = tuple([nueva_pos_caja if caja == jugador else caja for caja in cajas])   #TODO: Chequear esto
                jugador = nueva_pos_jugador
                movimientos -= 1
            else:
                #Solamente muevo de posicion al jugador. 
                nueva_pos_jugador = action[1]
                movimientos -=1
                jugador = nueva_pos_jugador
                
            return (cajas, jugador, movimientos)

        def heuristic(self, state):
            #Cantidad de cajas mal ubicadas (por lo menos 1 movimiento por cada caja mal ubicada)
            cajas_mal = 0
            cajas, jugador, movimientos = state
            for caja in cajas:
                if caja not in objetivos:
                    cajas_mal += 1
            
            return cajas_mal

    
    #problem = SokobanProblem(estado_inicial)
    # viewer = WebViewer()
    
   # result = astar(problem, graph_search=False)
    #result = astar(problem, graph_search=True, viewer=WebViewer())
    # result = breadth_first(problem, graph_search=True)
    # result = limited_depth_first(problem, graph_search=True, viewer=viewer, depth_limit=3)
    #result = depth_first(problem,  graph_search=True)
    
    #secuencia = []
    # Recorrer el resultado agregando a la lista secuencia, las acciones seleccionadas por el algoritmo
    #for action, state in result.path():
        # print("Action:", action)
        # print("State:", state)
        # print()
        # Descartar la primera acción que es None
        #if (action is not None):
            #secuencia.append(action)
    #return secuencia
    
if __name__ == '__main__':
    print('Resolviendo...')

    paredes = [(5, 1), (6, 1), (6, 2)]
    cajas = [(0,3),(2,4),(3,2)]
    objetivos = [(1,3),(4,5)]
    jugador = (2,2)
    maximos_movimientos = 30
    
    secuencia = jugar(paredes, cajas, objetivos, jugador, maximos_movimientos)
    print(secuencia)