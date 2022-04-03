# Info about frontend

      Install dependencies using package.json

- cd frontend
- yarn install

      Run development server

- yarn serve
- Test using localhost:80 or ipv4address:80

      For building the project

- Ctrl + C to stop development server
- yarn build
- Wait for a minute approximately
- cd backend
- Edit .\deploy_to_nginx.py and configure "path1" and "path2" variables inside deploy() function
- Edit nginx folder on your pc
  - conf/nginx.conf
  - create a directory like this: nginx-x.xx.x/projects/tfc/ssl_keys. Inside this, put cert.key and cert.pem files
- py .\deploy_to_nginx.py

  - Inside nginx-x.xx.x/projects/tfc will be "dist" folder

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
  INFORMACIÓN: no hay tareas ejecutándose que coincidan con los
  criterios especificados.
