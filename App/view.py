"""
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

import prettytable
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
    ultimaCiudad= lt.getElement((lt.getElement(m.valueSet(cont["ciudades"]),m.size(cont["ciudades"])-1)),1)
    #prints
    total = PrettyTable()
    total.field_names = ["Grafo Dirigido","","Grafo No Dirigido"," ","Ciudades", "   "]
    total.add_row(["Total de aeropuertos (vértices)",str(aeropuertosDirigido),"Total de aeropuertos (vértices)",str(aeropuertosNoDirigido),"Total Ciudades",ciudades])
    total.add_row(["Total de rutas (Edges)",str(rutasDirigido),"Total de rutas (Edges)",str(rutasNoDirigido)," "," "])
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
    print("Primera y Última Ciudad Cargada")
    print(ciudad)

def opcionUno (analyzer):
    (minPqDirigido,minPqNodirigido)=controller.requerimiento1(analyzer)
    print("==================================")
    print("Grafo Dirigido")
    print("==================================")
    print("Número de aeropuertos interconectados "+ (str(mpq.size(minPqDirigido))))
    print("Los 5 aeropuertos mas interconectados en la red son:")
    printDirigido(analyzer,minPqDirigido)
    print("==================================")
    print("Grafo No Dirigido")
    print("==================================")
    print("Número de aeropuertos interconectados "+ (str(mpq.size(minPqNodirigido))))
    print("Los 5 aeropuertos mas interconectados en la red son:")
    printNoDirigido(analyzer,minPqNodirigido)

def printNoDirigido(analyzer,minpq):
    cont=0
    tabla= PrettyTable()
    tabla.field_names = ["IATA","Nombre", "Ciudad", "País","Conexiones"]
    while cont<5:
        cont=cont+1
        info=mpq.delMin(minpq)
        iata= info[0]
        grado= info[1]
        infoiata= m.get(analyzer['aeropuertos'],iata)["value"]
        tabla.add_row([iata,str(infoiata["Name"]),str(infoiata["City"]),
                        str(infoiata["Country"]),str(grado)])
    tabla.max_width = 25
    print(tabla)

def printDirigido(analyzer,minpq):
    cont=0
    tabla= PrettyTable()
    tabla.field_names = ["IATA","Nombre", "Ciudad", "País","Conexiones Totales","Salida","Entrada"]
    while cont<5:
        cont=cont+1
        info=mpq.delMin(minpq)
        iata= info[0]
        grado= info[1]
        salida= info[3]
        entrada= info[2]
        infoiata= m.get(analyzer['aeropuertos'],iata)["value"]
        tabla.add_row([iata,str(infoiata["Name"]),str(infoiata["City"]),
                        str(infoiata["Country"]),grado,salida,entrada])
    tabla.max_width = 15
    print(tabla)

def opcionTres(analyzer,ciudadOrigen,ciudadDestino):
    listaOrigen= controller.ciudadesHomonimas(analyzer,ciudadOrigen)
    listaDestino= controller.ciudadesHomonimas(analyzer,ciudadDestino)
    (infoCiudadOrigen,infoCiudadDestino)=viewCiudadesHomonimas(listaOrigen,listaDestino)
    (origen,destino,path)= controller.requerimiento3(analyzer,infoCiudadOrigen,infoCiudadDestino)
    (disTerrestreOrigen,iataOrigen)=origen
    (disTerrestreDestino,iataDestino)=destino
    tOrigen=PrettyTable()
    tOrigen.field_names= ["IATA","Nombre","Ciudad","País"]
    aeOrigen= m.get(analyzer["aeropuertos"],iataOrigen)["value"]
    tOrigen.add_row([aeOrigen["IATA"],aeOrigen["Name"],aeOrigen["City"],aeOrigen["Country"]])
    tDestino=PrettyTable()
    tDestino.field_names= ["IATA","Nombre","Ciudad","País"]
    aeDestino= m.get(analyzer["aeropuertos"],iataDestino)["value"]
    tDestino.add_row([aeDestino["IATA"],aeDestino["Name"],aeDestino["City"],aeDestino["Country"]])
    tabla= PrettyTable()
    tabla.field_names=["Origen","Destino","Distancia Km","Tipo de Trayectoria"]
    tabla.add_row([ciudadOrigen,iataOrigen,round(disTerrestreOrigen,3),"Terrestre"])  
    pesoTotal= disTerrestreOrigen+disTerrestreDestino
    for trayecto in lt.iterator(path):
        inicio= trayecto["vertexA"]
        fin=trayecto["vertexB"]
        pesoVuelo= trayecto["weight"]
        tabla.add_row([inicio,fin,pesoVuelo,"Aérea"])  
        pesoTotal=pesoTotal+pesoVuelo
    tabla.add_row([ciudadDestino,iataDestino,round(disTerrestreDestino,3),"Terrestre"])  
    tabla.add_row([" ","",round(pesoTotal,3),"TOTAL"])  
    tabla.max_width = 25
    print("El aeropuerto de Salida cercano a "+ciudadOrigen+ " es:")
    tOrigen.max_width = 25
    print(tOrigen)
    print("El aeropuerto de llegada cercano a "+ciudadDestino+ " es:")
    tDestino.max_width = 25
    print(tDestino)
    print("Ruta recomendada:")
    print(tabla)


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
        opcionUno(cont)
        print("Encontrando puntos de interconexión aérea.............")
        
    elif int(inputs[0]) == 2:
        codigo1 = input('Ingrese Código IATA del aeropuerto 1: ')
        codigo2= input('Ingrese Código IATA del aeropuerto 2: ')
        print("Encontrando clústeres de tráfico aéreo")
        print("------------------------------------------------------------------------------")
        opcionDos(cont,codigo1,codigo2)

    elif int(inputs[0]) == 3:
        ciudadOrigen = input('Ingrese la ciudad de origen: ')
        ciudadDestino = input('Ingrese la ciudad de destino: ')
        print("Encontrando la ruta más corta entre las ciudades")
        print("------------------------------------------------------------------------------")
        opcionTres(cont,ciudadOrigen,ciudadDestino)
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


