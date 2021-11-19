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
                    'digrafo conecciones': None,
                    'grafo conecciones':None,
                    'components': None,
                    'paths': None
                    }

    analyzer['aeropuertos'] = m.newMap(numelements=15000,
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

# Funciones para creacion de datos

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

# Funciones de ordenamiento
