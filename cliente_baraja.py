#!/usr/bin/python

# Equipo: Mustafar
# Fecha: 10 de abril de 2020
# Integrantes:
#
#   Félix López Juan Pablo
#   López Velásquez Octavio
#   Serna Navarro Ángel Emilio
'''
    Cliente baraja
    Programa: cliente_baraja.
'''

import xmlrpc.client
import argparse
import servidor_baraja
import tarjetas
import time


def mostrar_bienvenida(jugador, ip, puerto):
    '''
        Imprime el mensaje de bienvenida
    '''
    print("Hola, ", jugador,  "\b!")
    print("Dirección IP: ", ip)
    print("Puerto: ", puerto)


def despliega_menu():
    print("--------------------------\n")
    print("** MENU **\n")
    print("1.- Pedir mano.")
    print("2.- Mostrar jugadores.")
    print("3.- Mostrar manos de todos.")
    print("4.- Volver a jugar.")
    print("5.- Mostrar marcador (ver el estado de la partida).")
    print("0.- Salir.")
    o = input("\nOpción:> ")

    # agregar número si agregas opción nueva
    opciones = ['1', '2', '3', '4', '5', '0']
    if o in opciones:
        return int(o)
    else:
        print("Por favor, elige una opción dentro del rango de opciones.")
        return despliega_menu()


def mostrar_mano(jugador, mano):
    '''
        muestra la mano de un jugador
        recibe: nombre del jugador, uso: "Emilio"
        recibe: diccionario de cartas del jugador, uso: mano
    '''
    print(str(jugador) + ", tu mano es: ")
    print("===========================")

    for carta in mano:
        print(carta)
    print("===========================\n")

def mostrar_jugadores(lista_jugadores):
    '''
        imprime todos los jugadores de una lista
        recibe: una lista de nombres de jugadores (str), uso: lista_jugadores
    '''
    print("* Jugadores:", str(len(lista_jugadores)) + "\n")
    i = 1
    for jugador in lista_jugadores:
        print(" - Jugador(a)", str(i) + ":", jugador)
        i += 1


def mostrar_manos_todos(lista_nombres_jugadores, lista_cartas_todos):
    '''
        imprime las manos de todos los jugadores y dice quien ganó
        recibe: una lista de nombres de jugadores (str), uso: lista_jugadores
        recibe: una lista de las cartas de todos (Carta), uso: lista_cartas_todos
    '''
    if len(lista_nombres_jugadores) > 0:
        for jugador, mano in zip(lista_nombres_jugadores, lista_cartas_todos):
            mostrar_mano(jugador, mano)
            print("\n")

        # función chila que diga quién ganó aki
    else:
        print("No existen jugadores dentro de la partida. Intenta agregar algunos.")


def main(jugador, ip, puerto):
    print("\n== JUEGO DE BARAJA FRANCESA (ahora con servidor)==\n")
    print("Iniciando...\n")

    try:
        proxy = xmlrpc.client.ServerProxy(
            "http://" + str(ip) + ":" + str(puerto))
        mostrar_bienvenida(jugador, ip, puerto)
        # print(proxy.prueba_conexion(jugador))  # SOLO USAR PARA TESTING
        opcion = 666
        tiene_mano = False
        jugado = False
        mano = []
        lista_nombres_jugadores = []
        lista_cartas_todos = []
        while opcion != 0:
            opcion = despliega_menu()
            print("\n")
            if opcion == 1:
                mano = proxy.genera_mano(jugador)
                tiene_mano = True
                if mano != 0:
                    mostrar_mano(jugador, mano)
                else:
                    print("No es posible dar más cartas.")
            elif opcion == 2:
                lista_nombres_jugadores = proxy.mostrar_jugadores()

                if len(lista_nombres_jugadores) > 0:
                    mostrar_jugadores(lista_nombres_jugadores)
                else:
                    print("Aún no se han agregado jugadores. Intenta agregar algunos.")
            elif opcion == 3:
                lista = proxy.obten_mano_todos()
                lista_nombres_jugadores = lista[0]
                lista_cartas_todos = lista[1]
                mostrar_manos_todos(
                    lista_nombres_jugadores, lista_cartas_todos)
                jugado = True
            elif opcion == 4:
                if jugado == True:
                    if len(mano) != 0:
                        num_cartas = len(mano)
                        mano = proxy.cambiar_mano(num_cartas,jugador)
                        tiene_mano = True
                        mostrar_mano(jugador,mano)
                        time.sleep(3.0)
                        print("\n")
                        if len(lista_nombres_jugadores) > 1:
                            mostrar_manos_todos(
                                lista_nombres_jugadores, lista_cartas_todos)
                        else:
                            print("No hay suficientes jugadores en la partida. Intenta agregar más de uno.")
                            time.sleep(3)
                    else:
                        print("No cuentas con una mano aún. Intenta pedir mano (1.)")
                        time.sleep(3)
                else:
                    print("Ninguna partida ha sido iniciada por el momento.")
                    time.sleep(3)
            elif opcion == 5:
                pass
        if tiene_mano == True:  # ya tienes una mano
            proxy.salir(jugador)
        print("\n¡Gracias por jugar!\n")
    except ConnectionError:
        print("Ha habido un error de conexión con el servidor.\n")
    except KeyboardInterrupt:
        if tiene_mano == True:  # ya tienes una mano
            print("No")
            proxy.salir(jugador)
        print(str(jugador) + ", haz salido de la partida.")
    except:
        print("Has salido de la partida. Tu mano ha sido devuelta a la baraja.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jugador', dest='jugador',
                        help="Nombre del Jugador", required=True)
    # parser.add_argument('-j', '--jugador', dest='jugador',
    #                    help="Nombre del Jugador", required=False, default="TEST")  # SOLO DEBUG
    parser.add_argument('-d', '--direccion', dest='direccion',
                        help="Dirección IP", required=False, default="localhost")
    parser.add_argument('-p', '--puerto', dest='puerto',
                        help="Puerto", required=False, default=9000)

    args = parser.parse_args()
    jugador = args.jugador
    direccion = args.direccion
    puerto = args.puerto

    main(jugador, direccion, puerto)
