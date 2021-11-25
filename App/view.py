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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
archivoAeropuertos = 'airports_full.csv'
archivoRutas='routes_full.csv'
archivoCiudades='worldcities.csv'

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Encontrar puntos de interconexión aérea")
    print("2- Encontrar clústeres de tráfico aéreo")
    print("3- Encontrar la ruta más corta entre ciudades")
    print("4- Utilizar las millas de viajero")
    print("5- Cuantificar el efecto de un aeropuerto cerrado")

cont=controller.init()

def opcionCero():
    controller.loadArchivos(cont,archivoAeropuertos,archivoCiudades,archivoRutas)



"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        opcionCero()
        print("El total de aeropuertos en cada grafo"+
        "\n El total de rutas aéreas en cada grafo"+
        "\nEl total de ciudades" + 
        "\nMostrar la información del primer aeropuerto cargado (nombre, ciudad, país, latitud y longitud) en cada grafo."+
        "\nMostrar la información de población, latitud y longitud, de la última ciudad cargada")

    elif int(inputs[0]) == 1:
        print("Encontrando puntos de interconexión aérea")
        print("Lista de aeropuertos (IATA, nombre, ciudad, país)"+
        "\nNúmero de aeropuertos interconectados.")
    elif int(inputs[0]) == 2:
        codigo1 = input('Ingrese Código IATA del aeropuerto 1.')
        codigo2= input('Ingrese Código IATA del aeropuerto 2.')
        print("Encontrando clústeres de tráfico aéreo")
        print("Número total de clústeres presentes en la red de transporte aéreo."+
        "\nInformar si los dos aeropuertos están en el mismo clúster o no")
    elif int(inputs[0]) == 3:
        ciudad_origen = input('Ingrese la ciudad de origen')
        ciudad_destino = input('Ingrese la ciudad de destino')
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


