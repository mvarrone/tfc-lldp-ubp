import asyncio
import time

import netdev

cisco1 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.100",
    "username": "jeremy",
    "password": "ccna",
    "secret": "ccna",
    # "conn_timeout": 20
}

cisco2 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.101",
    "username": "george",
    "password": "chair04",
    "secret": "ccna",
    # "conn_timeout": 10
}

cisco3 = {
    "device_type": "cisco_ios",
    "host": "192.168.1.102",
    "username": "chris",
    "password": "notebook1",
    "secret": "ccna2",
    # "conn_timeout": 10
}

lista = [cisco1,
         cisco2,
         cisco3]


async def funcion(dev):
    async with netdev.create(**dev) as device_conn:
        output = await device_conn.send_command('show cdp neighbors')
        return output


def main():
    start_time = time.time()

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(funcion(dev))
        for dev in lista
    ]

    loop.run_until_complete(asyncio.wait(tasks))

    for task in tasks:
        print(task.result())

    # print('It took {} seconds to run'.format(time.time() - start_time))
    print("\nIt took " + str(round(time.time() - start_time, 2)) + " seconds\n")


if __name__ == '__main__':
    main()
