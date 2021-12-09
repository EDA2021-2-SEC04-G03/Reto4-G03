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
import sys
from DISClib.ADT import list as lt
from DISClib.ADT import minpq as mpq
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim as prim
from DISClib.ADT import queue as q
from math import sin, cos, sqrt, atan2, radians,pi
sys.setrecursionlimit(2**20)
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


# Construccion de modelos
def newAnalyzer():
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
    analyzer['indiceLatitud'] = om.newMap(omaptype='RBT',
                                      comparefunction=cmpCoordenada)
    return analyzer

# Funciones para agregar informacion al catalogo
def addStopConnection(analyzer, vuelo):    
    origin = vuelo['Departure']
    destination = vuelo['Destination']
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
 
def haversineDistance(analyzer, ruta):
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
    updateLatitud(analyzer["indiceLatitud"],aeropuerto)
    return analyzer
def updateLatitud(map, registro):
    #redondear las llave a dos decimales##
    latitud= round(float(registro["Latitude"]),2)
    if om.isEmpty(map)==True or om.contains(map,latitud)==False:
        longitud=round(float(registro["Longitude"]),2)
        mapaNuevoLongitud= om.newMap(omaptype='RBT',comparefunction=cmpCoordenada)
        listaNueva=lt.newList("ARRAY_LIST")
        lt.addLast(listaNueva,registro)
        om.put(mapaNuevoLongitud,longitud,listaNueva)
        om.put(map,latitud,mapaNuevoLongitud)
    else:
        longitud=round(float(registro["Longitude"]),2)
        mapaExistenteLongitud= om.get(map,latitud)["value"]
        addOrCreateListInMap(mapaExistenteLongitud,longitud,registro)
        om.put(map,latitud,mapaExistenteLongitud)
    return map

def addOrCreateListInMap(mapa, llave, elemento):
    if om.contains(mapa,llave)==False:
        lista_nueva=lt.newList("ARRAY_LIST")
        lt.addLast(lista_nueva,elemento)
        om.put(mapa,llave,lista_nueva)
    else:
        pareja=om.get(mapa,llave)
        lista_existente=me.getValue(pareja)
        lt.addLast(lista_existente,elemento)
        om.put(mapa,llave,lista_existente)
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

def cmpCoordenada(latitud1,latitud2):
    """
    Compara dos fechas
    """
    if (latitud1 == latitud2):
        return 0
    elif (latitud1 > latitud2):
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

def cmpLista(vertice1,vertice2):
    grado1=vertice1[0]
    grado2=vertice2[0]
    if (grado1 == grado2):
        return 0
    elif (grado1 > grado2):
        return 1
    else:
        return -1
def cmpGrado(vertice1,vertice2):
    grado1=vertice1[1]
    grado2=vertice2[1]
    return  (grado1 < grado2)
# Funciones Req
#Req 1
def interconexionAerea(analyzer):
    listaVerticesDirigido = gr.vertices(analyzer["digrafo conecciones"])
    minPqDirigido=mpq.newMinPQ(cmpGrado)
    for vertice in lt.iterator(listaVerticesDirigido):
        ingrado=gr.indegree(analyzer["digrafo conecciones"],vertice)
        outgrado= gr.outdegree(analyzer["digrafo conecciones"],vertice)
        gradoTotal= ingrado+outgrado
        if gradoTotal> 0:
            info=[vertice, gradoTotal,ingrado,outgrado]
            mpq.insert(minPqDirigido,info)
    listaVerticesNodirigido = gr.vertices(analyzer['grafo conecciones'])
    minPqNodirigido=mpq.newMinPQ(cmpGrado)
    for vertice in lt.iterator(listaVerticesNodirigido):
        grado=gr.degree(analyzer['grafo conecciones'],vertice)
        info=[vertice,grado]
        if grado!= 0:
            mpq.insert(minPqNodirigido,info)
    return (minPqDirigido,minPqNodirigido)

#Req 2#
def clusteresTraficoAereo(analyzer, IATA1,IATA2):
    if analyzer['components']==None:
        analyzer['components']=scc.KosarajuSCC(analyzer["digrafo conecciones"])
    #número de conectados
    conectados=scc.connectedComponents(analyzer['components'])
    #verifica si los dos aeropuertos estan en el mismo cluster
    iatasConectados=scc.stronglyConnected(analyzer['components'],IATA1,IATA2)
    return(conectados,iatasConectados)


#Req3#
def ciudadesHomonimas(analyzer,ciudad):
    pareja=m.get(analyzer['ciudades'],ciudad)
    listaCiudades=None
    if pareja != None:
        listaCiudades= me.getValue(pareja)
    return listaCiudades
def requerimiento3(analyzer,infoCiudadOrigen,infoCiudadDestino):
    origen= aeropuertoCercano(analyzer,infoCiudadOrigen)
    destino= aeropuertoCercano(analyzer,infoCiudadDestino)
    (disTerrestreOrigen,iataOrigen)=origen
    (disTerrestreDestino,iataDestino)=destino
    path=minimumCostPath(analyzer,iataOrigen,iataDestino)
    return (origen,destino,path)
def aeropuertoCercano(analyzer,infoCiudad):
    kilometros= 10
    seHaEncontrado= False
    listaAeropuertosArea= lt.newList("ARRAY_LIST")
    while seHaEncontrado==False and kilometros<10000:
        (latMax,latMin,lonMax,lonMin)=coordenadasMaximas(infoCiudad,kilometros)
        listaAeropuertosArea= aeropuertosPorZonaGeografica(analyzer,lonMin,lonMax,latMin,latMax)
        if lt.isEmpty(listaAeropuertosArea)==False:
            seHaEncontrado=True
        else:
            kilometros= kilometros +10
    #calcular distancia por cada uno y ver cual es el menor###
    if lt.isEmpty(listaAeropuertosArea)==False:
        distanciaMin=None
        iatamin=""
        for aeropuerto in lt.iterator(listaAeropuertosArea):
            distancia= distanciaAeropuerto(aeropuerto,infoCiudad)
            if distanciaMin== None:
                distanciaMin= distancia
                iatamin= aeropuerto["IATA"]
            elif distancia< distanciaMin:
                distanciaMin=distancia
                iatamin= aeropuerto["IATA"]
    return (distanciaMin,iatamin)

def coordenadasMaximas(ciudad,km):
    # código adaptado de https://stackoverflow.com/questions/7477003/calculating-new-longitude-latitude-from-old-n-meters
    #RADIO aprox de la tierra
    R = 6378.137
    rangoMetros= km*1000
    latitude = float(ciudad["lat"])
    longitude =float(ciudad["lng"])
    #un metro en grados
    m = (1 / ((2 * pi / 360) * R)) / 1000
    #Nuevas lat y lon max
    latMax=latitude + (rangoMetros * m)
    latMin=latitude  -  (rangoMetros * m)
    lonMax= longitude + (rangoMetros * m) / cos(latitude * (pi / 180))
    lonMin=longitude - (rangoMetros * m) / cos(latitude * (pi / 180))
    return (latMax,latMin,lonMax,lonMin)
def aeropuertosPorZonaGeografica(catologo,longitudMin,longitudMax,latitudMin,latitudMax):
    mapLatitud=catologo["indiceLatitud"]
    ListadeMapasenRangoLatitud=om.values(mapLatitud,latitudMin,latitudMax)
    ListaRangoLatyLon= lt.newList("ARRAYLIST")
    for mapaLongitudes in lt.iterator(ListadeMapasenRangoLatitud):
        listaRegistros= om.values(mapaLongitudes,longitudMin,longitudMax)
        for registros in lt.iterator(listaRegistros):
            for registro in lt.iterator(registros):
                lt.addLast(ListaRangoLatyLon,registro)
    return(ListaRangoLatyLon)
def distanciaAeropuerto(aeropuerto, ciudad):
    # código adaptado de https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(float(ciudad["lat"]))
    lon1 = radians(float(ciudad["lng"]))
    lat2 = radians(float(aeropuerto["Latitude"]))
    lon2 = radians(float(aeropuerto["Longitude"]))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
def minimumCostPath(analyzer, initialStation,destStation):
    paths= djk.Dijkstra(analyzer['digrafo conecciones'], initialStation)
    path = djk.pathTo(paths, destStation)
    return path

#Req 4#
def millasViajero(analyzer,ciudadOrigen,millas):
    grafo=analyzer["digrafo conecciones"]
    caminoMinimo=prim.PrimMST(grafo)
    minimo=caminoMinimo["mst"]
    listaNodos=lt.newList("ARRAY_LIST")
    while not q.isEmpty(minimo):
        edge=q.dequeue(minimo)
        lt.addLast(listaNodos,edge)
    search=dfs.DepthFirstSearch(analyzer["digrafo conecciones"],ciudadOrigen)
    info=None
    num=None
    costoTotal=0
    verticeInicial=None
    for ae in lt.iterator(listaNodos):
        if ae!=ciudadOrigen:
            path=djk.pathTo(search,ae)
            if num==None:
                num=lt.size(path)
                info=path
                verticeInicial=ae
            else:
                if lt.size(path)>num:
                    num=lt.size(path)
                    info=path
                    nuevo=ae
                    peso=gr.getEdge(analyzer["digrafo conecciones"],verticeInicial,nuevo)["weight"]
                    costoTotal+=peso
                    verticeInicial=nuevo
    costoTotalMi=costoTotal/1.60
    if costoTotalMi>millas:
        diferencia=costoTotalMi-millas
        cant="Faltante"
    else:
        diferencia=millas-costoTotalMi
        cant="Excedente"
    return (listaNodos,costoTotal,info,diferencia,cant)
#Req5#
def aeropuertoCerradoDigr(analyzer,iata):
    #digrafo
    originalVerticesDigr=gr.vertices(analyzer["digrafo conecciones"])
    originalArcosDigr=gr.edges(analyzer["digrafo conecciones"])
    rutasAfectadas=0
    aeropuertosAfectados=lt.newList("ARRAY_LIST")
    for ruta in lt.iterator(originalArcosDigr):
        if ruta["vertexA"]==iata : 
            rutasAfectadas=rutasAfectadas+1
            info=m.get(analyzer["aeropuertos"],ruta["vertexB"])["value"]
            lt.addLast(aeropuertosAfectados,info)
        elif ruta["vertexB"]==iata : 
            rutasAfectadas=rutasAfectadas+1
            info=m.get(analyzer["aeropuertos"],ruta["vertexA"])["value"]
            lt.addLast(aeropuertosAfectados,info)
    return(originalVerticesDigr,originalArcosDigr,rutasAfectadas,aeropuertosAfectados)

def aeropuertoCerradogr(analyzer,iata):
    #grafo
    originalVerticesgr=gr.vertices(analyzer["grafo conecciones"])
    originalArcosgr=gr.edges(analyzer["grafo conecciones"])
    num=gr.numEdges(analyzer["grafo conecciones"])
    rutasAfectadasgr=0
    aeropuertosAfectadosgr=lt.newList("ARRAY_LIST")
    for ruta in lt.iterator(originalArcosgr):
        if ruta["vertexA"]==iata : 
            rutasAfectadasgr=rutasAfectadasgr+1
            info=m.get(analyzer["aeropuertos"],ruta["vertexB"])["value"]
            lt.addLast(aeropuertosAfectadosgr,info)
        elif ruta["vertexB"]==iata : 
            rutasAfectadasgr=rutasAfectadasgr+1
            info=m.get(analyzer["aeropuertos"],ruta["vertexA"])["value"]
            lt.addLast(aeropuertosAfectadosgr,info)
    return(num,originalVerticesgr,originalArcosgr,rutasAfectadasgr,aeropuertosAfectadosgr)
