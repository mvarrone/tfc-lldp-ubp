import threading
import time
from pprint import pprint

from netmiko import ConnectHandler

t1 = time.perf_counter()

cisco1 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.81",
    "username": "jeremy",
    "password": "ccna",
    "secret": "ccna",
    "conn_timeout": 20
}

cisco2 = {
    "device_type": "cisco_ios",
    "host": "10.10.10.1",
    "username": "jeremy",
    "password": "ccna",
    "secret": "ccna",
    "conn_timeout": 10
}

cisco3 = {
    "device_type": "cisco_ios",
    "host": "10.10.10.2",
    "username": "jeremy",
    "password": "ccna",
    "secret": "ccna",
    "conn_timeout": 10
}

lista = [
    cisco1,
    cisco2,
    cisco3
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
    # command = "show lldp neighbors"
    command = "show cdp neighbors"
    with ConnectHandler(**device) as net_connect:
        hostname = net_connect.find_prompt()[:-1]
        output = net_connect.send_command(command, use_textfsm=True)

        lista_hostname.append(hostname)
        lista_output.append(output)
        lista_hostnames_id.append(len(lista_hostname))
        # time.sleep(1)


config_threads_list = []
for device in lista:
    # print('\nCreating thread for: \n', device)
    config_threads_list.append(threading.Thread(target=abc, args=(device,)))

# print('\n---- Begin get config threading ----\n')
for config_thread in config_threads_list:
    config_thread.start()

for config_thread in config_threads_list:
    config_thread.join()

# print('\n---- End get config threading ----\n')

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
