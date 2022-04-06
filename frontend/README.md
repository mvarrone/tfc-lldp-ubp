# Info about frontend

      Install dependencies using package.json

- cd frontend
- yarn install

      Run development server

- yarn serve
- Test using localhost:80 or ipv4address:80

      Stop development server

- Ctrl + C to stop development server

      Building the project

- yarn build
- Wait for a minute approximately
- cd backend
- Edit backend\deploy_to_nginx.py and configure "path1" and "path2" variables inside deploy() function
- Edit nginx folder on your pc
  - conf/nginx.conf
  - create a directory like this: nginx-x.xx.x/projects/tfc/ssl_keys. Inside this, put cert.key and cert.pem files
- cd backend
- py .\deploy_to_nginx.py
- Inside nginx-x.xx.x/projects/tfc will be "dist" folder (recently built using yarn build)

      Run production server

- cd C:\nginx-1.21.6\
- start .\nginx.exe
- tasklist /fi "imagename eq nginx.exe" -> It should list 2 processes named nginx.exe

      Example: tasklist /fi "imagename eq nginx.exe"

      Nombre de imagen PID Nombre de sesión Núm. de ses Uso de memor

      ========================= ======== ================ =========== ============

      nginx.exe 14748 Console 1 7.824 KB

      nginx.exe 12948 Console 1 8.668 KB

- Test using www.lldp.duckdns.org (It should be working with SSL)
- You should be able to check digital certificate and view lock icon before FQDN

      Stop production server

- cd C:\nginx-1.21.6\
- .\nginx.exe -s stop
- tasklist /fi "imagename eq nginx.exe" -> It should look like this:

      Example: tasklist /fi "imagename eq nginx.exe"

      INFORMACIÓN: no hay tareas ejecutándose que coincidan con los criterios especificados.

            Tasks to be performed on this README.md

_READY_

      1. Postman:

      a) Write instructions on how to import API docs into Postman --> How to import API documentation into Postman
      b) Write instructions on how to create and set a global variable for access token --> Authentication

      2. Frontend: put cert.pem and cert.key on nginx-x.xx.x/projects/tfc/ssl_keys on frontend/README.md instructions

_IN PROGRESS_

      1. DDNS: For example, www.duckdns.org. Create and account using Google and configure on pc (me) or router
      2. Let´s Encrypt: For create and renew digital certificates
      3. Backend: put cert.pem and cert.key on backend/ssl_keys on backend/README.md instructions and uncomment last 2 lines on backend/main.py (uvicorn.run)
      Those lines are:
            ssl_keyfile="./ssl_keys/cert.key",
            ssl_certfile="./ssl_keys/cert.pem"
      4. nginx: Write instructions on installation and configuration. Attach nginx.conf file
      5. Port Mapping/PAT: Open port 80 and 443 (Frontend) and 5000 (Backend) on router
