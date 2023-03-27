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

import sys

import config as cf
import controller

from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import queue as qu
from DISClib.ADT import stack as st
from DISClib.DataStructures import mapentry as me

assert cf
import traceback

from tabulate import tabulate

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    lista_datos = controller.loadData(control)
    registros_mostrar = []
    registros_anio = []
    headers = [ "Año",
                "Código actividad económica",
                "Nombre actividad económica",
                "Código sector económico",
                "Nombre sector económico",
                "Código subsector económico",
                "Nombre subsector económico",
                "Total ingresos netos",
                "Total costos y gastos",
                "Total saldo a pagar",
                "Total saldo a favor" ]
    
    anio = lt.firstElement(lista_datos)["Año"]
    for reg in lt.iterator(lista_datos):
        if reg["Año"] != anio:
            anio = reg["Año"]
            if len(registros_anio) < 6:
                registros_mostrar.extend(registros_anio)
            else:
                registros_mostrar.extend(registros_anio[:3])
                registros_mostrar.extend(registros_anio[-3:])
            registros_anio = []

        columnas_mostrar = []
        for columna in headers:
            columnas_mostrar.append(reg[columna])
        registros_anio.append(columnas_mostrar)
    
    width=9
    tabla = tabulate(registros_mostrar,headers,tablefmt="grid", maxcolwidths=width, maxheadercolwidths=width)
    print(tabla)


def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_max_saldo_a_favor(control, anio, codigo):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    registro = controller.return_max_saldo_a_favor(control, anio, codigo)
    headers = [ "Código actividad económica",
                "Nombre actividad económica",
                "Código subsector económico",
                "Nombre subsector económico",
                "Total ingresos netos",
                "Total costos y gastos",
                "Total saldo a pagar",
                "Total saldo a favor" ]
    
    columnas_mostrar = []
    for columna in headers:
        columnas_mostrar.append(registro[columna])
    
    width=9
    tabla = tabulate([columnas_mostrar],headers,tablefmt="grid", maxcolwidths=width, maxheadercolwidths=width)
    print(tabla)


def print_min_total_retenciones(control, anio):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    registro = controller.return_min_total_retenciones(control, anio)
    headers = [ "Código sector económico",
                "Nombre sector económico",
                "Código subsector económico",
                "Nombre subsector económico",
                "Total retenciones del subsector económico",
                "Total ingresos netos del subsector económico",
                "Total costos y gastos del subsector económico",
                "Total saldo a pagar del subsector económico",
                "Total saldo a favor del subsector económico" ]
    total_retenciones = 0
    total_ingresos = 0
    total_costos = 0
    total_saldo_pagar = 0
    total_saldo_favor = 0
    primer_registro = lt.firstElement(registro)
    cod_sector = primer_registro["Código sector económico"]
    nom_sector = primer_registro["Nombre sector económico"]
    cod_subsector = primer_registro["Código subsector económico"]
    nom_subsector = primer_registro["Nombre subsector económico"]


    for reg in lt.iterator(registro):
        total_retenciones += int(reg["Total retenciones"])
        total_ingresos += int(reg["Total ingresos netos"])
        total_costos += int(reg["Total costos y gastos"])
        total_saldo_pagar += int(reg["Total saldo a pagar"])
        total_saldo_favor += int(reg["Total saldo a favor"])

    column_info = [
        cod_sector,
        nom_sector,
        cod_subsector,
        nom_subsector,
        total_retenciones,
        total_ingresos,
        total_costos,
        total_saldo_pagar,
        total_saldo_favor
    ]

    
    width=9
    tabla = tabulate([column_info],headers,tablefmt="grid", maxcolwidths=width, maxheadercolwidths=width)
    print(tabla)

    headers2 = [ "Código actividad económica",
                 "Nombre actividad económica",
                 "Total retenciones",
                 "Total ingresos netos",
                 "Total costos y gastos",
                 "Total saldo a pagar",
                 "Total saldo a favor" ]

    datos_mostrar = []
    for reg in lt.iterator(registro):
        fila_mostrar = []
        for columna in headers2:
            fila_mostrar.append(reg[columna])
        datos_mostrar.append(fila_mostrar)
    
    if len(datos_mostrar) > 6:
        print("3 actividades económicas que menos y más contribuyeron para el año " + anio)
        datos_mostrar = datos_mostrar[:3] + datos_mostrar[-3:]
        width=10
        print(tabulate(datos_mostrar,headers,tablefmt="grid",maxcolwidths=width,maxheadercolwidths=width))
    else:
        print("Hay únicamente " + str(len(datos_mostrar)) + " actividades económicas para el año " + anio )
        width=10
        print(tabulate(datos_mostrar,headers,tablefmt="grid",maxcolwidths=width,maxheadercolwidths=width))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_mins_costos_gastos(control, num_act_econ, anio, cod_subsec_econ):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    registro = controller.return_mins_costos_gastos(control, num_act_econ, anio, cod_subsec_econ)
    headers = [ "Código actividad económica",
                "Nombre actividad económica",
                "Código subsector económico",
                "Nombre subsector económico",
                "Total ingresos netos",
                "Total costos y gastos",
                "Total saldo a pagar",
                "Total saldo a favor" ]
    
    datos_mostrar = []
    for reg in lt.iterator(registro):
        fila_mostrar = []
        for columna in headers:
            fila_mostrar.append(reg[columna])
        datos_mostrar.append(fila_mostrar)

    width=9
    tabla = tabulate(datos_mostrar,headers,tablefmt="grid", maxcolwidths=width, maxheadercolwidths=width)
    print(tabla)


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        try:
            if int(inputs) == 1:
                print("Cargando información de los archivos ....\n")
                load_data(control)
            elif int(inputs) == 2:
                print_req_1(control)

            elif int(inputs) == 3:
                anio = input("Año para el cual desea consultar ")
                codigo = input("Código sector para la cual desea consultar ")
                print_max_saldo_a_favor(control,anio, codigo)

            elif int(inputs) == 4:
                anio = input("Año para el cual desea consultar ")
                print_min_total_retenciones(control, anio)

            elif int(inputs) == 5:
                print_req_4(control)

            elif int(inputs) == 6:
                print_req_5(control)

            elif int(inputs) == 7:
                print_req_6(control)

            elif int(inputs) == 8:
                anio = input("Año para el cual desea consultar ")
                num_act_econ = int(input("Número de actividades económicas a identificar (ej.: TOP 3, 5, 10 o 20) "))
                cod_subsec_econ = input("Código subsector económico a consultar ")
                print_mins_costos_gastos(control, num_act_econ, anio, cod_subsec_econ)

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)
