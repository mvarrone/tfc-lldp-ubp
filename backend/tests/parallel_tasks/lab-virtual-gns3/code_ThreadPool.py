import time
from multiprocessing.dummy import Pool as ThreadPool
from pprint import pprint

from netmiko import ConnectHandler

t1 = time.perf_counter()

cisco1 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.100",
    "username": "jeremy",
    "password": "ccna",
    "secret": "ccna",
    "conn_timeout": 20
}

cisco2 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.101",
    "username": "george",
    "password": "chair04",
    "secret": "ccna",
    "conn_timeout": 10
}

cisco3 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.102",
    "username": "chris",
    "password": "notebook1",
    "secret": "ccna2",
    "conn_timeout": 10
}

cisco4 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.103",
    "username": "mati",
    "password": "lapicera",
    "secret": "vaso",
    "conn_timeout": 10
}

cisco5 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.104",
    "username": "remera",
    "password": "lapiz",
    "secret": "papel",
    "conn_timeout": 10
}

cisco6 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.105",
    "username": "hola",
    "password": "holave",
    "secret": "holavee",
    "conn_timeout": 10
}

cisco7 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.106",
    "username": "celular",
    "password": "llave",
    "secret": "puerta",
    "conn_timeout": 10
}

lista = [
    cisco1,
    cisco2,
    cisco3,
    cisco4,
    cisco5,
    cisco6,
    cisco7
]

cantidad_dispositivos = len(lista)

if cantidad_dispositivos == 0:
    print("\nNo hay ningún dispositivo cargado")

if cantidad_dispositivos == 1:
    print("\nHay " + str(cantidad_dispositivos) + " dispositivo cargado")
else:
    print("\nHay " + str(cantidad_dispositivos) + " dispositivos cargados")

lista_hostname = []
lista_output = []
lista_hostnames_id = []


def abc(device):
    # print("\nDispositivo: ")
    # print(device)
    command = "show lldp neighbors"
    with ConnectHandler(**device) as net_connect:
        hostname = net_connect.find_prompt()[:-1]
        output = net_connect.send_command(command, use_textfsm=True)

        lista_hostname.append(hostname)
        lista_output.append(output)
        lista_hostnames_id.append(len(lista_hostname))
        # time.sleep(1)


num_threads = cantidad_dispositivos

# ---- Create list for passing to config worker
config_params_list = []
for device in lista:
    config_params_list.append(device)

# print('\n--- Creating threadpool, launching get config threads ----\n')
threads = ThreadPool(num_threads)
results = threads.map(abc, config_params_list)

threads.close()
threads.join()

# print('\n---- End get config threadpool ----\n')

# time.sleep(1)

print("\nlista_hostname\n")
print(lista_hostname)

print("\nlista_output\n")
pprint(lista_output)

print("\nlista_hostnames_id\n")
print(lista_hostnames_id)

print("\nlen(lista_output) = " + str(len(lista_output)) + "\n")

# --- fin script

t2 = time.perf_counter()
total = t2-t1

if total < 1:
    print("\nTime: " + str(round(total * 1000, 2)) + " ms\n")
else:
    print("\nTime: " + str(round(total, 2)) + " s\n")
