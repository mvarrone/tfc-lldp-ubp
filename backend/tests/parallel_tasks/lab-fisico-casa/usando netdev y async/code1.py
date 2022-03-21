import asyncio
import time

import netdev

t1 = time.perf_counter()


async def task(param):
    async with netdev.create(**param) as ios:
        # Testing sending simple command
        out = await ios.send_command("show cdp neighbors")
        print(out)


async def run():
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

    devices = [cisco1, cisco2, cisco3]
    tasks = [task(dev) for dev in devices]
    await asyncio.wait(tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())

t2 = time.perf_counter()
total = t2-t1

if total < 1:
    print("\nTime: " + str(round(total * 1000, 2)) + " ms\n")
else:
    print("\nTime: " + str(round(total, 2)) + " s\n")
