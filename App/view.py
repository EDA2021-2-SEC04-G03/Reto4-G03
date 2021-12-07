﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

from os import path
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from prettytable import PrettyTable
from DISClib.ADT import minpq as mpq
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
archivoAeropuertos = 'airports-utf8-small.csv'
archivoRutas='routes-utf8-small.csv'
archivoCiudades='worldcities-utf8.csv'

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Encontrar puntos de interconexión aérea")
    print("2- Encontrar clústeres de tráfico aéreo")
    print("3- Encontrar la ruta más corta entre ciudades")
    print("4- Utilizar las millas de viajero")
    print("5- Cuantificar el efecto de un aeropuerto cerrado")

cont=controller.init()

def opcionCero(cont):
    controller.loadArchivos(cont,archivoAeropuertos,archivoCiudades,archivoRutas)
    aeropuertosNoDirigido= gr.numVertices(cont["grafo conecciones"])
    rutasNoDirigido= gr.numEdges(cont["grafo conecciones"])
    aeropuertosDirigido= gr.numVertices(cont["digrafo conecciones"])
    rutasDirigido= gr.numEdges(cont["digrafo conecciones"])
    ciudades= m.get(cont['ciudades'],"contadorContador")["value"]
    iataAeDirigido= lt.getElement(gr.vertices(cont["digrafo conecciones"]),1)
    infoAeDirigido=m.get(cont["aeropuertos"],iataAeDirigido)["value"]
    iataAeNoDirigido= lt.getElement(gr.vertices(cont["grafo conecciones"]),1)
    infoAeNoDirigido=m.get(cont["aeropuertos"],iataAeNoDirigido)["value"]
    #TODO
    ultimaCiudad= lt.getElement((lt.getElement(m.valueSet(cont["ciudades"]),m.size(cont["ciudades"])-1)),1)
    #prints
    total = PrettyTable() 
    total.field_names = ["Grafo Dirigido","","Grafo No Dirigido"," ","Ciudades", "   "]
    total.add_row(["Total de aeropuertos",str(aeropuertosDirigido),"Total de aeropuertos",str(aeropuertosNoDirigido),"Total Ciudades",ciudades])
    total.add_row(["Total de rutas",str(rutasDirigido),"Total de rutas",str(rutasNoDirigido)," "," "])
    total.max_width = 25
    print(total)
    aeropuertos=PrettyTable() 
    aeropuertos.field_names = ["Grafo","Nombre", "Ciudad", "País", "Latitud","Longitud"]
    aeropuertos.add_row(["No Dirigido",str(infoAeNoDirigido["Name"]),str(infoAeNoDirigido["City"]),
                        str(infoAeNoDirigido["Country"]),str(infoAeNoDirigido["Latitude"]),str(infoAeNoDirigido["Longitude"])])
    aeropuertos.add_row(["Dirigido",str(infoAeDirigido["Name"]),str(infoAeDirigido["City"]),
                        str(infoAeDirigido["Country"]),str(infoAeDirigido["Latitude"]),str(infoAeDirigido["Longitude"])])
    aeropuertos.max_width = 10
    print("Primeros aeropuertos cargados")
    print(aeropuertos)
    ciudad=PrettyTable() 
    ciudad.field_names = ["Nombre Ciudad", "Páis", "latitud", "Longitud", "Población","ID"]
    ciudad.add_row([str(ultimaCiudad["city_ascii"]),str(ultimaCiudad["country"]),str(ultimaCiudad["lat"]),str(ultimaCiudad["lng"]),str(ultimaCiudad["population"]),str(ultimaCiudad["id"])])
    ciudad.max_width = 25
    print("Ultima Ciudad Cargada")
    print(ciudad)

def opcionUno (analyzer):
    (minPqDirigido,minPqNodirigido)=controller.requerimiento1(analyzer)
    print("dirigido")
    idir=1
    while idir<5:
        iata=mpq.delMin(minPqDirigido)
        ae=m.get(analyzer["digrafo conecciones"],iata)
        print(ae["name"])
        idir+=1

def opcionTres(analyzer,ciudadOrigen,ciudadDestino):
    listaOrigen= controller.ciudadesHomonimas(analyzer,ciudadOrigen)
    listaDestino= controller.ciudadesHomonimas(analyzer,ciudadDestino)
    (infoCiudadOrigen,infoCiudadDestino)=viewCiudadesHomonimas(listaOrigen,listaDestino)
    (origen,destino,path)= controller.requerimiento3(analyzer,infoCiudadOrigen,infoCiudadDestino)
    print(origen)
    print(destino)
    (disTerrestreOrigen,iataOrigen)=origen
    (disTerrestreDestino,iataDestino)=destino


def opcionDos(analyzer,codigo1,codigo2):
    (componentesConectados, iatasConectados)=controller.clusteresTraficoAereo(analyzer,codigo1,codigo2)
    print("Número total de clústeres presentes en la red de transporte aéreo:  " + str(componentesConectados))
    if iatasConectados==True:
        respuesta= " SI "
    else:
        respuesta= " NO "
    print("______________________________________________________________________________")
    print("Los dos aeropuertos con IATA "+str(codigo1)+" y "+str(codigo2)+ respuesta +"están en el mismo clúster")
    print("______________________________________________________________________________")
def viewCiudadesHomonimas(listaOrigen,listaDestino):
    if listaOrigen== None or listaDestino== None:
        print("no se encontró alguna de las ciudades, revise la información")
        sys.exit(0)
    else:
        if lt.size(listaOrigen)==1:
            infoCiudadOrigen= lt.getElement(listaOrigen,1)
        elif lt.size(listaOrigen)>1:
            print("\nLa ciudad de origen indicada("+ciudadOrigen +") es homónima con varias ciudades, a continuación esta la lista: ")
            printListaCiudades(listaOrigen)
            numeroO= int(input("Por favor seleccione el número de la ciudad que desea escoger como origen: "))
            if numeroO<= lt.size(listaOrigen):
                infoCiudadOrigen= lt.getElement(listaOrigen,numeroO)
            else:
                print("El número marcado no esta dentro de las opciones")
                sys.exit(0)
        if lt.size(listaDestino)==1:
            infoCiudadDestino= lt.getElement(listaDestino,1)   
        if lt.size(listaDestino)>1:
            print("\nLa ciudad de destino indicada ("+ciudadDestino +") es homónima con varias ciudades, a continuación esta la lista:")
            printListaCiudades(listaDestino)
            numeroD= int(input("Por favor seleccione el número de la ciudad que desea escoger como destino: "))
            if numeroD<= lt.size(listaDestino):
                infoCiudadDestino= lt.getElement(listaDestino,numeroD)
            else:
                print("El número marcado no esta dentro de las opciones")
                sys.exit(0)
    return(infoCiudadOrigen,infoCiudadDestino)

def printListaCiudades(listaCiudades):
    x = PrettyTable() 
    x.field_names = ["#","Nombre Ciudad", "Páis", "latitud", "Longitud", "Población","ID"]
    cont=1
    for i in lt.iterator(listaCiudades):
        x.add_row([str(cont),str(i["city_ascii"]),str(i["country"]),str(i["lat"]),str(i["lng"]),str(i["population"]),str(i["id"])])
        x.max_width = 25
        cont+=1
    print(x)
    
"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        opcionCero(cont)

    elif int(inputs[0]) == 1:
        print("Encontrando puntos de interconexión aérea")
        print("Lista de aeropuertos (IATA, nombre, ciudad, país)"+
        "\nNúmero de aeropuertos interconectados.")
    elif int(inputs[0]) == 2:
        codigo1 = input('Ingrese Código IATA del aeropuerto 1: ')
        codigo2= input('Ingrese Código IATA del aeropuerto 2: ')
        print("Encontrando clústeres de tráfico aéreo")
        print("------------------------------------------------------------------------------")
        print("______________________________________________________________________________")
        opcionDos(cont,codigo1,codigo2)

    elif int(inputs[0]) == 3:
        ciudadOrigen = input('Ingrese la ciudad de origen: ')
        ciudadDestino = input('Ingrese la ciudad de destino: ')
        opcionTres(cont,ciudadOrigen,ciudadDestino)
        print("Encontrando la ruta más corta entre las ciudades")
        print("Aeropuerto de Origen"+
        "\nAeropuerto de Destino."+
        "\nRuta (incluir la distancia de viaje [km] de cada segmento de viaje aéreo)."+
        "\nDistancia total de la ruta (incluir la distancia terrestre entre la ciudad de origen y el aeropuerto de origen y entre el aeropuerto destino y la ciudad de destino).")
    elif int(inputs[0]) == 4:
        ciudad_origen = input('Ingrese la ciudad de origen')
        cant_millas = input('Ingrese la Cantidad de millas disponibles del viajero.')
        print("El número de nodos conectados a la red de expansión mínima."+
        "\nEl costo total (distancia en [km]) de la red de expansión mínima."+
        "\nPresentar la rama más larga (mayor número de arcos entre la raíz y la hoja) que hace partem de la red de expansión mínima."+
        "\nPresentar la lista de ciudades que se recomienda visitar de acuerdo con la cantidad de millas disponibles por el usuario.")

    elif int(inputs[0]) == 5:
        codigo = input('Ingrese Código IATA del aeropuerto en cuestion.')
        print("Cuantificando el efecto de un aeropuerto cerrado")
        print("Número de vuelos de salida afectados:  "+
        "\nNúmero de vuelos de entrada afectados: "+
        "\nNúmero de ciudades afectadas."+
        "\n• Lista de ciudades afectadas") 
    else:
        sys.exit(0)



sys.exit(0)


