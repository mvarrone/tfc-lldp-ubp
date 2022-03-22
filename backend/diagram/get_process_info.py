import time
from multiprocessing.dummy import Pool as ThreadPool
from pprint import pprint

from netmiko import ConnectHandler

from db.db_functions import (check_db, check_db_for_logs,
                             check_db_table_device_types)
from db.get_data_sqlite_db import datos_para_netmiko
from log.log_function import (write_to_log, write_to_log_error_diagram,
                              write_to_log_error_diagram_at_least_one,
                              write_to_log_error_diagram_no_devices)

# from pruebas.test_2 import convert #usar test_4 ?


def get_diagram(dict_fastapi):
    check_db(dict_fastapi)
    write_to_log(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)

    t1 = time.perf_counter()

    # Conexión a base de datos
    print("\nDentro de get_diagram()\n")
    lista = datos_para_netmiko()
    pprint(lista)

    cantidad_dispositivos = len(lista)

    if cantidad_dispositivos == 0:
        print("\nNo hay ningún dispositivo cargado")

        t2 = time.perf_counter()
        total = t2-t1

        if total < 1:
            total_time = round(total * 1000, 2)
            unit = "ms"
            print("\nTime: " + str(total_time) + " ms\n")
        else:
            total_time = round(total, 2)
            unit = "s"
            print("\nTime: " + str(total_time) + " s\n")

        info_error = {
            "error": "no_devices_in_db",
            "time": total_time,
            "unit": unit
        }
        write_to_log_error_diagram_no_devices(dict_fastapi, info_error)
        return {"error": "no_devices_in_db"}
        # return {"error": "no_devices_in_db", "time": total_time, "unit": unit}

    if cantidad_dispositivos == 1:
        print("\nHay " + str(cantidad_dispositivos) + " dispositivo cargado")
    else:
        print("\nHay " + str(cantidad_dispositivos) + " dispositivos cargados")

    variable_error = False  # Sirve para cuando hay por lo menos 1 dispositivo con error

    lista_hostname = []
    lista_output = []
    lista_hostnames_id = []

    global contador_errores
    contador_errores = 0

    global lista_para_borrar_dispositivos
    lista_para_borrar_dispositivos = []

    global lista_errores_dispositivos
    lista_errores_dispositivos = []

    global lista_errores_descripcion
    lista_errores_descripcion = []

    def my_function(device):
        if device["device_type"] == "cisco_ios":
            command = "show lldp neighbors"

        if device["device_type"] == "juniper_junos":
            command = "show lldp neighbors"

        try:
            with ConnectHandler(**device) as net_connect:
                hostname = net_connect.find_prompt()[:-1]
                output = net_connect.send_command(command, use_textfsm=True)
                print(output)

                lista_hostname.append(hostname)
                lista_output.append(output)
                lista_hostnames_id.append(len(lista_hostname))
        except Exception as e:
            # print("\nSe produjo un error al intentar conectarse a " +
            # str(device["host"]) + ":" + str(device["port"]) +
            # " (" + str(device["device_type"]) + ")")
            # print(e.args)
            # print("\n")

            global contador_errores
            contador_errores = contador_errores + 1

            lista_para_borrar_dispositivos.append(device["host"])
            lista_errores_dispositivos.append(
                device["host"] + ":" + str(device["port"]) + " - " + device["device_type"])
            lista_errores_descripcion.append(e.args)

        # time.sleep(1)

    num_threads = cantidad_dispositivos

    # ---- Create list for passing to config worker
    config_params_list = []
    for device in lista:
        config_params_list.append(device)

    # print('\n--- Creating threadpool, launching get config threads ----\n')
    threads = ThreadPool(num_threads)
    results = threads.map(my_function, config_params_list)

    threads.close()
    threads.join()

    print("\nLa cantidad de errores fue " + str(contador_errores))
    print("\nLa lista de errores es ")
    print(lista_errores_dispositivos)

    print("\nLa lista de descripcion de errores es ")
    print(lista_errores_descripcion)

    print("\nLa lista lista_para_borrar_dispositivos es ")
    print(lista_para_borrar_dispositivos)

    if contador_errores == cantidad_dispositivos:
        print("\nNo se pudo conectar a ningún dispositivo\n")

        t2 = time.perf_counter()
        total = t2-t1

        if total < 1:
            total_time = round(total * 1000, 2)
            unit = "ms"
            print("\nTime: " + str(total_time) + " ms\n")
        else:
            total_time = round(total, 2)
            unit = "s"
            print("\nTime: " + str(total_time) + " s\n")

        info_error = {
            "error": "all_down",
            "time": total_time,
            "unit": unit,
            "devices_errored": lista_errores_dispositivos,
            "devices_errored_descr": lista_errores_descripcion
        }
        write_to_log_error_diagram(dict_fastapi, info_error)
        return {"error": "all_down"}

    if contador_errores > 0:
        print("\nNo se pudo conectar a " +
              str(contador_errores) + " equipos")
        variable_error = True
        # write_to_log_error_diagram_at_least_one(dict_fastapi, info_error)

    # Borrar de la lista el/los dispositivos a los cuales no se pudo conectar /
    # obtener info
    print("\n----------Proceso: Borrar dispositivo(s)----------")

    print("\nLa lista lista_para_borrar_dispositivos es ")
    print(lista_para_borrar_dispositivos)

    print("\n")

    for dev in lista_para_borrar_dispositivos:
        print(dev)

    print("\n")

    print("\nlista_output")
    print(lista_output)

    cantidad_dispositivos = cantidad_dispositivos - contador_errores

    print("\n----------Fin: Borrar dispositivo(s)----------\n")

    # print('\n---- End get config threadpool ----\n')

    # time.sleep(1)

    # t1 = time.perf_counter()

    # print("\nlista_hostname\n")
    # print(lista_hostname)

    # print("\nlista_output\n")
    # pprint(lista_output)

    # print("\nlista_hostnames_id\n")
    # print(lista_hostnames_id)

    # print("\nlen(lista_output) = " + str(len(lista_output)) + "\n")

    max_columnas = []
    for x in range(len(lista_output)):
        # print(lista_output)
        for y in range(len(lista_output[x])):
            # print("\n")
            # print("\nx = " + str(x))
            # print("y = " + str(y))

            # print("lista_output[" + str(x) + "][" + str(y) + "]")
            print(lista_output[x][y])

            filas = x + 1
            columnas = y + 1
            max_columnas.append(columnas)

    # print("\nmax_columnas")
    # print(max_columnas)

    # print("\nmax(max_columnas)")
    columnas = max(max_columnas)

    print(columnas)

    # print("\nfilas = " + str(filas))
    # print("columnas = " + str(columnas))

    tabla = [[0 for _ in range(columnas)] for _ in range(filas)]
    local_interface = [[0 for _ in range(columnas)] for _ in range(filas)]
    remote_interface = [[0 for _ in range(columnas)] for _ in range(filas)]

    # print(tabla)
    # print("\n")

    for x in range(len(lista_output)):
        #
        # print(lista_output[x])
        # print("\n")
        for y in range(len(lista_output[x])):
            # print("x = " + str(x))
            # print("y = " + str(y))
            # print(lista_output[x][y])
            # print(lista_output[x][y]["neighbor"])
            vecino = lista_output[x][y]["neighbor"].split(".")[0]
            # print(vecino)
            # print("\n")
            tabla[x][y] = vecino
            # print(x)
            # print(y)
            local_interface[x][y] = lista_output[x][y]["local_interface"]
            remote_interface[x][y] = lista_output[x][y]["neighbor_interface"]

    # print("\nlocal_interface\n")
    # print(local_interface)

    print("\nlocal_interface (local_interface sin ceros)\n")
    for a in range(filas):
        for b in reversed(range(columnas)):
            if local_interface[a][b] == 0:
                local_interface[a].pop(b)
    print(local_interface)

    # print("\nremote_interface\n")
    # print(remote_interface)

    print("\nremote_interface (remote_interface sin ceros)\n")
    for a in range(filas):
        for b in reversed(range(columnas)):
            if remote_interface[a][b] == 0:
                remote_interface[a].pop(b)
    print(remote_interface)

    # print("\ntabla\n")
    # print(tabla)

    print("\ntabla (tabla sin ceros)\n")
    for a in range(filas):
        for b in reversed(range(columnas)):
            if tabla[a][b] == 0:
                # print(tabla)
                # print("a = " + str(a))
                # print("b = " + str(b))
                tabla[a].pop(b)
    print(tabla)

    print("\n--- Fin prueba")

    print("\nlista_hostname\n")
    print(lista_hostname)

    print("\nlista_hostnames_id\n")
    print(lista_hostnames_id)

    list = []
    for name in config_params_list:
        list.append(name["device_type"])

    lista_vendor_name = list

    # resultado = convert(list)
    # print("\nEste es el resultado")
    # print(resultado)
    # lista_vendor_name = resultado

    # lista_vendor_name = ["Cisco",
    #                      "Cisco",
    #                      "Cisco",
    #                      "Cisco",
    #                      "Cisco",
    #                      "Cisco",
    #                      "Cisco"]

    # print("\nlista_vendor_name\n")
    # print(lista_vendor_name)

    # --- nodes

    print("\n--- nodes")

    dict = {}
    nodes = []

    for x in range(1, cantidad_dispositivos+1):
        # print(x)
        dict = {
            "id": x,
            "label": lista_hostname[x-1],
            "title": lista_vendor_name[x-1]
        }
        nodes.append(dict)

    print("\nResultado de nodes\n")
    pprint(nodes)

    # --- vecinos

    print("\n--- vecinos\n")

    for a in range(len(lista_hostname)):
        print("Vecino(s) de " + lista_hostname[a])

        print(tabla[a])
        print("\n")

    print("\n")

    dict = {}
    edges = []
    lista_labels_from = []
    lista_labels_to = []

    for a in range(len(lista_hostname)):
        if nodes[a]["label"] == lista_hostname[a]:
            # print("label: " + str(nodes[a]["label"]))
            from_A = nodes[a]["id"]
            # print("id: " + str(from_A) + "\n")
        for b in range(len(lista_hostname)):
            for c in range(len(tabla[a])):
                if nodes[b]["label"] == tabla[a][c]:
                    lista_labels_from.append(nodes[a]["label"])
                    # print("label: " + str(nodes[b]["label"]))
                    # print("id: " + str(nodes[b]["id"]))
                    to_B = nodes[b]["id"]
                    dict = {
                        "from": from_A,
                        "to": to_B
                    }
                    edges.append(dict)
                    lista_labels_to.append(nodes[b]["label"])

    # print("\nResultado de edges\n")
    # pprint(edges)

    # print(type(edges))
    # print(len(edges))

    # print("\nlista_labels_from\n")
    # print(lista_labels_from)

    # print("\nlista_local\n")
    # print(lista_local)

    # print("\nlista_labels_to\n")
    # print(lista_labels_to)

    # print("\nlista_remoto\n")
    # print(lista_remoto)

    print("\n")

    # --- armar titles

    print("--- armar titles")

    lista_para_titulo = []
    listaA = []
    listaB = []

    lista_device_A = []
    lista_device_B = []
    for a in range(len(lista_hostname)):
        for b in range(len(local_interface[a])):
            titulo = lista_hostname[a] + ": " + local_interface[a][b] + \
                " <=> " + \
                tabla[a][b] + ": " + remote_interface[a][b]
            # print(titulo)
            lista_para_titulo.append(titulo)
            listaA.append(local_interface[a][b])
            listaB.append(remote_interface[a][b])
            lista_device_A.append(lista_hostname[a])
            lista_device_B.append(tabla[a][b])

    print("\nlista_para_titulo")
    print(lista_para_titulo)

    print("\nlista_device_A")
    print(lista_device_A)

    print("\nlistaA")
    print(listaA)

    print("\nlista_device_B")
    print(lista_device_B)

    print("\nlistaB")
    print(listaB)

    dictionary = {}
    edges_3 = []
    for g in range(len(lista_device_A)):
        # print(lista_device_A[g] + " <=> " + lista_device_B[g])

        for u in range(len(lista_hostname)):
            if lista_device_A[g] == lista_hostname[u]:
                desdee = lista_hostnames_id[u]
                # print(desdee)
            if lista_device_B[g] == lista_hostname[u]:
                hastaa = lista_hostnames_id[u]
                # print(hastaa)

        dictionary = {
            "from": desdee,
            "to": hastaa
        }
        edges_3.append(dictionary)

    print("\nedges_3")
    print(edges_3)

    print("\n")
    dict_2 = {}
    edges_2 = []

    # print("\nedges")
    # print(edges)
    # print("\n")

    for h in range(len(edges_3)):
        # print(lista_para_titulo[h])
        # print(edges[h])
        # print("\n")

        dict_2 = {
            "from": edges_3[h]["from"],
            "to": edges_3[h]["to"],
            "title": lista_device_A[h] + ": " + listaA[h] +
            " <=> " +
            lista_device_B[h] + ": " + listaB[h]
        }
        edges_2.append(dict_2)

    print("\n")
    pprint(edges_2)
    print("\n---------- aaaaa ---------------")

    edges = edges_2

    # print(edges)

    # --- edges (sin duplicar)

    # duplicado: --> from:1 to:3 y from:3 to:1

    contador = 0
    for a in reversed(range(len(edges))):
        desde_original = edges[a]["from"]
        hacia_original = edges[a]["to"]
        for b in range(len(edges)):
            hacia_despues = edges[b]["to"]
            desde_despues = edges[b]["from"]
            if desde_original == hacia_despues:
                if desde_despues == hacia_original:
                    contador = contador + 1
                    del edges[b]
                    break

    print("\nResultado de edges (sin duplicar)")
    pprint(edges)

    # --- data

    print("\n--- data\n")

    data = {
        "nodes": nodes,
        "edges": edges,
    }
    pprint(data)

    # --- fin script

    t2 = time.perf_counter()
    total = t2-t1

    if total < 1:
        total_time = round(total * 1000, 2)
        unit = "ms"
        print("\nTime: " + str(total_time) + unit + "\n")
    else:
        total_time = round(total, 2)
        unit = "s"
        print("\nTime: " + str(total_time) + unit + "\n")

    if variable_error:
        data = {
            "nodes": nodes,
            "edges": edges,
            "time": total_time,
            "unit": unit,
            "error": "at_least_one_down",
            "cant_errores": contador_errores
        }

        info_error = {
            "error": "at_least_one_down",
            "time": total_time,
            "unit": unit,
            "devices_errored": lista_errores_dispositivos,
            "devices_errored_descr": lista_errores_descripcion,
            "cant_errores": contador_errores
        }
        write_to_log_error_diagram_at_least_one(dict_fastapi, info_error)
    else:
        data = {
            "nodes": nodes,
            "edges": edges,
            "time": total_time,
            "unit": unit,
            "error": ""
        }
    return data


def get_diagram_example(dict_fastapi):
    check_db(dict_fastapi)
    write_to_log(dict_fastapi)
    check_db_table_device_types(dict_fastapi)
    check_db_for_logs(dict_fastapi)

    example_data = {
        "nodes": [
            {
                "id": 1,
                "label": "R1",
                "title": "Cisco"
            },
            {
                "id": 2,
                "label": "R2",
                "title": "Huawei"
            },
            {
                "id": 3,
                "label": "R3",
                "title": "Juniper"
            },
            {
                "id": 4,
                "label": "R4",
                "title": "Arista"
            },
            {
                "id": 5,
                "label": "R5",
                "title": "Aruba"
            },
            {
                "id": 6,
                "label": "R6",
                "title": "Huawei"
            },
            {
                "id": 7,
                "label": "R7",
                "title": "Cisco"
            },
            {
                "id": 8,
                "label": "R8",
                "title": "Broadcom"
            },
            {
                "id": 9,
                "label": "R9",
                "title": "HP"
            },
            {
                "id": 10,
                "label": "R10",
                "title": "Juniper"
            },
            {
                "id": 11,
                "label": "R11",
                "title": "Cisco"
            },
            {
                "id": 12,
                "label": "R12",
                "title": "Cisco"
            },
            {
                "id": 13,
                "label": "R13",
                "title": "Huawei"
            },
            {
                "id": 14,
                "label": "R14",
                "title": "Juniper"
            },
            {
                "id": 15,
                "label": "R15",
                "title": "Aruba"
            }
        ],
        "edges": [
            {
                "from": 1,
                "to": 2,
                "title": "R1:g0/1 <-> R2:GE0/0/3"
            },
            {
                "from": 1,
                "to": 2,
                "title": "R1:g0/2 <-> R2:GE1/1/1"
            },
            {
                "from": 1,
                "to": 3,
                "title": "R1:g2/1 <-> R3:xe-3/0/4.0"
            },
            {
                "from": 1,
                "to": 3,
                "title": "R1:g3/1 <-> R3:xe-0/0/2.0"
            },
            {
                "from": 2,
                "to": 4
            },
            {
                "from": 2,
                "to": 5
            },
            {
                "from": 3,
                "to": 6
            },
            {
                "from": 3,
                "to": 7
            },
            {
                "from": 4,
                "to": 8
            },
            {
                "from": 4,
                "to": 9
            },
            {
                "from": 5,
                "to": 10
            },
            {
                "from": 5,
                "to": 11
            },
            {
                "from": 6,
                "to": 12
            },
            {
                "from": 6,
                "to": 13
            },
            {
                "from": 7,
                "to": 14
            },
            {
                "from": 7,
                "to": 15
            }
        ]
    }
    return example_data
