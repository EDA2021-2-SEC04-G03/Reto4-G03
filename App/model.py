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
from math import sin, cos, sqrt, atan2, radians
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
                    'ciudades':None, 
                    'digrafo conecciones': None,
                    'grafo conecciones':None,
                    'components': None,
                    'paths': None
                    }

    analyzer['aeropuertos'] = m.newMap(numelements=15000,
                                     maptype='PROBING',
                                     comparefunction=compareIATA)

    analyzer['ciudades'] = m.newMap(maptype="CHAINING",loadfactor=4)
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
def addStopConnection(analyzer, vuelo):    
    origin = vuelo['Departure']
    destination = vuelo['Destination']
    cleanServiceDistance(analyzer,vuelo)
    distancia = float(vuelo['distance_km'])
    distancia = abs(distancia)
    addStop(analyzer['digrafo conecciones'], origin)
    addStop(analyzer['digrafo conecciones'], destination)
    addConnection(analyzer['digrafo conecciones'], origin, destination, distancia)
    if gr.getEdge(analyzer['digrafo conecciones'],destination,origin)!=None:
        addStop(analyzer['grafo conecciones'], origin)
        addStop(analyzer['grafo conecciones'], destination)
        addConnection(analyzer['grafo conecciones'], origin, destination, distancia)
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
 
def cleanServiceDistance(analyzer, ruta):
    #TODO arreglar esta cosa con distancia calculada#
    if ruta['distance_km'] == '' or ruta['distance_km'] == 0:
        origenIATA= ruta["Departure"]
        destinoIATA= ruta["Destination"]
        infoOrigen= m.get(analyzer["aeropuertos"],origenIATA)["value"]
        infoDestino=m.get(analyzer["aeropuertos"],destinoIATA)["value"]
        # código adaptado de https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
        # approximate radius of earth in km
        R = 6373.0
        lat1 = radians(infoOrigen["Latitude"])
        lon1 = radians(infoOrigen["Longitude"])
        lat2 = radians(infoDestino["Latitude"])
        lon2 = radians(infoDestino["Longitude"])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        ruta['distance_km'] = distance

def addStop(grafo, iata):
    if not gr.containsVertex(grafo, iata):
        gr.insertVertex(grafo, iata)

def addConnection(grafo, origin, destination, distance):
    edge = gr.getEdge(grafo, origin, destination)
    if edge is None:
        gr.addEdge(grafo, origin, destination, distance)

def addAeropuerto(analyzer,aeropuerto):
    if not m.contains(analyzer['aeropuertos'], aeropuerto["IATA"]):
        m.put(analyzer['aeropuertos'], aeropuerto["IATA"],aeropuerto)
        addStop(analyzer['digrafo conecciones'], aeropuerto["IATA"])

    return analyzer
def addCiudad(analyzer,ciudad,contador):  
    m.put(analyzer['ciudades'],"contadorContador",contador) 
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
    listaCiudades=None
    if pareja != None:
        listaCiudades= me.getValue(pareja)
    return listaCiudades

def requerimiento3(infoCiudadOrigen,infoCiudadDestino):
    ruta=1
    return ruta