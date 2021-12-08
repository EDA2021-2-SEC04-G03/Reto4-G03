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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

def loadArchivos (analyzer,archivoAeropuertos,archivoCiudades,archivoRutas):
    rutasFile = cf.data_dir + archivoRutas
    aeropuertosFile = cf.data_dir + archivoAeropuertos
    ciudadesFile = cf.data_dir + archivoCiudades
    rutasInputFile = csv.DictReader(open(rutasFile, encoding="utf-8"),
                                delimiter=",")
    ciudadesInputFile= csv.DictReader(open(ciudadesFile, encoding="utf-8"),
                                delimiter=",")
    aeropuertosInputFile= csv.DictReader(open(aeropuertosFile, encoding="utf-8"),
                                delimiter=",")    
    contadorDirigido= 0    
    ultimoAeDir=None                  
    for aeropuerto in aeropuertosInputFile:
        ultimoAeDir= aeropuerto
        if contadorDirigido==0:
            primerAeDir=aeropuerto
        model.addAeropuerto(analyzer,aeropuerto)
        contadorDirigido= contadorDirigido +1
    contadorCiudades=0
    ultimaCiudad=None
    for ciudad in ciudadesInputFile:
        ultimaCiudad=ciudad
        if contadorCiudades==0:
            primeraCiudad= ciudad
        contadorCiudades=contadorCiudades+1
        model.addCiudad(analyzer,ciudad,contadorCiudades) 
    contNoDir=0  
    primerAeNoDir=None
    for vuelo in rutasInputFile:
        (primerin,contin)= model.addStopConnection(analyzer, vuelo,contNoDir,primerAeNoDir)
        if primerin!= None:
            primerAeNoDir= primerin
            contNoDir= contin

    return (primeraCiudad,ultimaCiudad,primerAeDir,ultimoAeDir,primerAeNoDir)
#
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def ciudadesHomonimas(analyzer,ciudad):
    return model.ciudadesHomonimas(analyzer,ciudad)
def requerimiento3(analyzer,infoCiudadOrigen,infoCiudadDestino):
    return model.requerimiento3(analyzer,infoCiudadOrigen,infoCiudadDestino)
def clusteresTraficoAereo(analyzer, IATA1,IATA2):
    return model.clusteresTraficoAereo(analyzer, IATA1,IATA2)
def requerimiento1 (analyzer):
    return model.interconexionAerea(analyzer)
