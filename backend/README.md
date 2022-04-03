# Info about backend

      Create and activate a virtual environment

      - pip install virtualenv
      - cd tfc
      - python -m venv venv
      - .\venv\Scripts\activate

      Install dependencies

- cd backend
- pip install -r .\requirements.txt

      Set environment variable for Netmiko

- setx NET_TEXTFSM "D:\Documentos\Mati\tfc\venv\Lib\site-packages\ntc_templates\templates"
- [System.Environment]::GetEnvironmentVariables() or [system.environment]::GetEnvironmentVariable('NET_TEXTFSM') for checking environment variable is created and well located
- Reboot operating system due to setx implements permanent variables and that is necessary

      Run backend server

- py main.py

      Optional

- pip list --local -> To list all dependencies installed on the virtual environment
- deactivate -> To deactivate virtual environment
- rmdir venv /s and then Y -> To remove virtual environment
