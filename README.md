# tfc-lldp-ubp

Project intention is to show a network topology using LLDP

This is achieved by connecting to multiple devices through SSH (provided by Netmiko) and executing correspondant commands depending on the network device operating system.

- Frontend: Vue.JS

- Backend: Python3, FastAPI

- db: sqlite3

- Login: Authentication implementing JWTokens from FastAPI Security

- DDNS: duckdns.org

      Example using GNS3 Emulator

![Captura de pantalla (863)](https://user-images.githubusercontent.com/70659542/159499409-9cf6481f-19cb-4994-819c-e666b998432a.png)

Note: "Switch1" and "Cloud1" not represented in web app due to they are not manageable devices

Live Demo: https://www.lldp.duckdns.org

FastAPI Documentation: https://www.lldp.duckdns.org:5000/documentation
