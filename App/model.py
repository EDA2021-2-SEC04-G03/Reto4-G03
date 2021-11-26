"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


# Construccion de modelos
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    analyzer = {
                    'aeropuertos': None,
                    'ciudades':None, #llave ciudad valor lista
                    'digrafo conecciones': None,
                    'grafo conecciones':None,
                    'components': None,
                    'paths': None
                    }

    analyzer['aeropuertos'] = m.newMap(numelements=15000,
                                     maptype='PROBING',
                                     comparefunction=compareIATA)

    analyzer['ciudades'] = m.newMap(numelements=15000,
                                     maptype='PROBING',
                                     comparefunction=compareIATA)
    analyzer['digrafo conecciones'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=100000,
                                              comparefunction=compareIATA)
    analyzer['grafo conecciones'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=100000,
                                              comparefunction=compareIATA)
    return analyzer

# Funciones para agregar informacion al catalogo
def addStopConnection(analyzer, ultimoVuelo, vuelo):    
    origin = vuelo['Departure']
    destination = vuelo['Destination']
    cleanServiceDistance(ultimoVuelo, vuelo)
    distancia = float(vuelo['distance_km']) - float(ultimoVuelo['distance_km'])
    distancia = abs(distancia)
    addStop(analyzer, origin)
    addStop(analyzer, destination)
    addConnection(analyzer, origin, destination, distancia)
    return analyzer

def addRouteConnections(analyzer):
    lststops = m.keySet(analyzer['aeropuertos'])
    for key in lt.iterator(lststops):
        lista = m.get(analyzer['aeropuertos'], key)['value']
        prevrout = None
        for route in lt.iterator(lista):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0) #no ponerlo en cero, buscar todos los arcos que ya existan y buscar el mayor
                #si no, calcular distancia para rellenar
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route

#Funciones para creacion de datos
 
def cleanServiceDistance(lastservice, service):
    if service['distance_km'] == '':
        service['distance_km'] = 0
    if lastservice['distance_km'] == '':
        lastservice['distance_km'] = 0

def addStop(analyzer, stopid):
    if not gr.containsVertex(analyzer['aeropuertos'], stopid):
        gr.insertVertex(analyzer['aeropuertos'], stopid)
    return analyzer

def addConnection(analyzer, origin, destination, distance):
    edge = gr.getEdge(analyzer['aeropuertos'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['aeropuertos'], origin, destination, distance)
    return analyzer  

def addAeropuerto(analyzer,aeropuerto):
    if not m.contains(analyzer['aeropuertos'], aeropuerto["IATA"]):
        m.put(analyzer['aeropuertos'], aeropuerto["IATA"],aeropuerto)
    return analyzer
def addCiudad(analyzer,ciudad):    
    if m.contains(analyzer['ciudades'],ciudad["city"])== False:
        listaNueva=lt.newList("ARRAY_LIST")
        lt.addLast(listaNueva,ciudad)
        m.put(analyzer['ciudades'],ciudad["city"],listaNueva)
    else:
        pareja=m.get(analyzer['ciudades'],ciudad["city"])
        listaExistente=me.getValue(pareja)
        lt.addLast(listaExistente,ciudad)
        m.put(analyzer['ciudades'],ciudad["city"],listaExistente)
    return analyzer
# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareIATA(IATA, keyIATA):
    """
    Compara dos estaciones
    """
    IATAcode = keyIATA['key']
    if (IATA == IATAcode):
        return 0
    elif (IATA > IATAcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

# Funciones Req
#Req3#
def ciudadesHomonimas(analyzer,ciudad):
    pareja=m.get(analyzer['ciudades'],ciudad)
    listaCiudades= me.getValue(pareja)
    return listaCiudades