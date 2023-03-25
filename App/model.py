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
from DISClib.ADT import map as mp
from DISClib.ADT import queue as qu
from DISClib.ADT import stack as st
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import mapentry as me

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.

    Crea una lista vacia para guardar todos los registros.

    Se crean indices (Maps) por los siguientes criterios:
               Año 
               Nombre sector económico
               Código subsector económico

    Retorna la estructura de datos inicializada.
    """

    data_structs = {
               "Regs": None,
               "Código sector económico": None,
               "Código subsector económico": None
                   }
    
    """
    Esta lista contiene todo los registros encontrados
    en los archivos de carga.  Estos registros estan
    ordenados por año. Son referenciados
    por los indices creados a continuacion.
    """

    data_structs["Regs"] = lt.newList('SINGLE_LINKED',cmpRegsAnio)
    
    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada."""
    """
    Este indice crea un map cuya llave es un año y el valor es un diccionario
    con una llave para el año y la otra llave con los registros asociados
    a ese año.
    """
    data_structs["Año"] = mp.newMap(20,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmpRegsAnio)
    
    """
    Este indice crea un map cuya llave es el código de un sector económico y el valor 
    es un diccionario con una llave para el código y la otra llave con los registros 
    asociados a ese sector.
    """
    data_structs["Código sector económico"] = mp.newMap(1000,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmpRegsAnio)
    
    """
    Este indice crea un map cuya llave es el código de un subsector económico y el valor 
    es un diccionario con una llave para el código y la otra llave con los registros 
    asociados a ese subsector.
    """
    data_structs["Código subsector económico"] = mp.newMap(2000,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmpRegsAnio)
    
    return data_structs


# Funciones para creacion de datos


def newAnio(aniopub):
    """
    Crea la estructura de libros asociados a un año.
    """
    entry = {"Año": "", "Regs": None}
    entry["Año"] = aniopub
    entry["Regs"] = lt.newList('SINGLE_LINKED', cmpRegsAnio)
    return entry


def newSector(codsector):
    """
    Crea la estructura de libros asociados a un sector económico.
    """
    entry = {"Sector": "", "Regs": None}
    entry["Sector"] = codsector
    entry["Regs"] = lt.newList('SINGLE_LINKED', sort_by_actividad_economica)
    return entry


def newSubsector(codsubsector):
    """
    Crea la estructura de libros asociados a un subsector económico.
    """
    entry = {"Subsector": "", "Regs": None}
    entry["Subsector"] = codsubsector
    entry["Regs"] = lt.newList('SINGLE_LINKED', sort_by_actividad_economica)
    return entry


# Funciones para agregar informacion al modelo


def addReg(data_structs, reg):
    """
    Función para agregar un registro a la lista.
    """
    lt.addLast(data_structs["Regs"], reg)
    addRegAnio(data_structs, reg)
    addRegSector(data_structs, reg)
    addRegSubsector(data_structs, reg)


def addRegAnio(data_structs, reg):
    anio = reg["Año"]
    if not mp.contains(data_structs["Año"], anio):
        nuevo_anio = newAnio(anio)
        mp.put(data_structs["Año"], anio, nuevo_anio)
        lt.addLast(nuevo_anio["Regs"], reg)
    else:
        entry = mp.get(data_structs["Año"], anio)
        anio_existente = me.getValue(entry)
        lt.addLast(anio_existente["Regs"], reg)


def addRegSector(data_structs, reg):
    anio = reg["Código sector económico"]
    if not mp.contains(data_structs["Código sector económico"], anio):
        nuevo_anio = newAnio(anio)
        mp.put(data_structs["Código sector económico"], anio, nuevo_anio)
        lt.addLast(nuevo_anio["Regs"], reg)
    else:
        entry = mp.get(data_structs["Código sector económico"], anio)
        sector_existente = me.getValue(entry)
        lt.addLast(sector_existente["Regs"], reg)


def addRegSubsector(data_structs, reg):
    anio = reg["Código subsector económico"]
    if not mp.contains(data_structs["Código subsector económico"], anio):
        nuevo_anio = newAnio(anio)
        mp.put(data_structs["Código subsector económico"], anio, nuevo_anio)
        lt.addLast(nuevo_anio["Regs"], reg)
    else:
        entry = mp.get(data_structs["Código subsector económico"], anio)
        subsector_existente = me.getValue(entry)
        lt.addLast(subsector_existente["Regs"], reg)



# Funciones de consulta


def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    return lt.getElement(data_structs["Regs"], id)


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    return lt.size(data_structs["Regs"])

def getRegsByYears(data_structs, year):
    exists = mp.contains(data_structs["Año"], year)
    if exists:
        entry = mp.get(data_structs["Año"], year)
        return me.getValue(entry)
    return None

def getRegsByEconomicSector(data_structs, sector_code):
    exists = mp.contains(data_structs["Código sector económico"], sector_code)
    if exists:
        entry = mp.get(data_structs["Código sector económico"], sector_code)
        return me.getValue(entry)
    return None

def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def sort_crit_saldo_a_favor (dato1,dato2):
    """
    Ordena los datos de menor a mayor acorde a Total saldo a favor.   
    """
    if dato1["Total saldo a favor"] < dato2["Total saldo a favor"]:
        return True
    else:
        return False


def max_saldo_a_favor(data_structs, anio, cod_sec_econ):
    """
    Función que soluciona el requerimiento 2
    """
    data_structs_2 = new_data_structs()
    data_anio = getRegsByYears(data_structs, anio)
    for reg in lt.iterator(data_anio["Regs"]):
        addReg(data_structs_2, reg)

    data_sec = getRegsByEconomicSector(data_structs_2, cod_sec_econ)
    sorted_data = sa.sort(data_sec["Regs"], sort_crit_saldo_a_favor)
    return lt.lastElement(sorted_data)


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista


def cmpRegsAnio(anio_1, me_anio_2):
    """
    Compara los registros por año, ordenándolos de menor a mayor. 
    """
    anio_2 = me.getKey(me_anio_2)
    if (anio_1 == anio_2):
        return 0
    elif (anio_1 > anio_2):
        return 1
    else:
        return -1
    
def sort_by_actividad_economica(act_1, me_act_2):
    """
    Compara los registros por año, ordenándolos de menor a mayor. 
    """
    anio_2 = me.getKey(me_act_2)
    if (act_1 == anio_2):
        return 0
    elif (act_1 > anio_2):
        return 1
    else:
        return -1


# Funciones de ordenamiento


def compareYearAndActivity(reg_1,reg_2):
    if reg_1["Año"] < reg_2["Año"]:
        return True
    elif reg_1["Año"] == reg_2["Año"]:
        return reg_1["Código actividad económica"] < reg_2["Código actividad económica"]
    else:
        return False


def sort_by_anio_act_eco(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    return sa.sort(data_structs["Regs"], compareYearAndActivity)
