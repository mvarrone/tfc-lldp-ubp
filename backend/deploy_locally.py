import os
import shutil
import subprocess
import webbrowser

import requests

BASE_FRONTEND_URL = "https://www.lldp.duckdns.org"
BASE_BACKEND_URL = "https://www.lldp.duckdns.org:5000"
BASE_NGINX_PATH = "C:/nginx-1.21.6"
COMPILED_DIST_PATH = "D://Documentos//Mati//tfc//frontend//dist"
# NGINX_PROJECT_PATH is used in nginx.conf --> server{ location{ root } }
NGINX_PROJECT_PATH = "C://nginx-1.21.6//projects//tfc//dist"


def build():
    os.chdir("../frontend")
    if subprocess.call('yarn build', shell=True) == 0:
        return "OK"


def cut_dist_folder():
    path1 = COMPILED_DIST_PATH
    path2 = NGINX_PROJECT_PATH

    value_1 = os.path.isdir(path1)
    if not value_1:
        return "dist folder not found at tfc/frontend"

    value_2 = os.path.isdir(path2)
    if value_2:
        mydir = path2
        try:
            shutil.rmtree(mydir)
            shutil.move(path1, path2)
            # print("\nDone\n")
            msg = "OK"
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        try:
            shutil.move(path1, path2)
            # print("\nDone\n")
            msg = "OK"
        except Exception as e:
            # print(e)
            msg = e
    return msg


def write_info(path, text):
    with open(path, 'a') as f:
        f.write(text)


def create_api_docs_in_json_file(url):
    os.chdir("../backend")

    full_url = url + "/openapi.json"

    payload = headers = {}

    try:
        response = requests.request(
            "GET", full_url, headers=headers, data=payload)
    except Exception as e:
        return {
            "error": True,
            "info": "FAIL\n\nError:\n\n" + str(e.args) + "\n",
            "status_code": 500
        }

    if response.status_code == 200:
        if not os.path.exists("postman"):
            os.mkdir("postman")
        else:
            shutil.rmtree("postman")
            os.mkdir("postman")

        write_info('postman/openapi.json', response.text)

        return {
            "info": "OK",
            "status_code": response.status_code,
        }

    return {
        "info": "Bad status code on response: " + str(response.status_code),
        "status_code": response.status_code
    }


def create_README_file(url):
    postman_text = """# How to import API documentation into Postman

1. Open Postman
2. Go to "APIs", select "New", inside "Advanced" section select "API" and then "Import" tab
3. Under "Import local schema files", hit "Select files" Button
4. Select openapi.json located inside postman directory
5. On next page, click on Import button and then on Close button
6. API docs is imported on Collections and APIs Tabs. Use what you like
7. Go to FastAPIDocumentation > draft > FastAPIDocumentation > Variables
8. Set baseUrl:
    - VARIABLE: baseUrl
    - INITIAL VALUE: /
    - CURRENT VALUE: """ + url + """
    - Be sure this field is checked
9. Click on Save Button (upper right located)
10. Now, you can test every endpoint

    Example: {{baseUrl}}/logs

### Authentication

1. Configure access token as a global variable for automation tests

    - Inside /login POST Method
    
    a) In "Authorization" tab, select:

        Type: No Auth
    
    b) In "Body" tab, select:

        form-data
        
        key    value
        username my_username
        password my_password

    c) Go to "Tests" tab and copy:

        pm.test("Status test", function () {

        pm.response.to.have.status(200);

        pm.globals.set("token_tfc", JSON.parse(responseBody).access_token);
        });

    This will create and set a global variable named "token_tfc" with access token value retrieved from response body AFTER this method is executed.

2. Configure collection to get this global variable

    a) On "tfc" collection, go to "Authorization" tab and select:

        Type: Bearer Token

        Token: {{token_tfc}}

3. Configure endpoints to inherit auth from parent collection

    a) For every endpoint:

        Go to "Authorization" tab and select "Inherit auth from parent" (in Type section)
    
    Under this, you will see "This request is using Bearer Token from collection tfc."

4. Test every endpoint

    At this point, it should be possible to get successful responses for every endpoint

    Every endpoint will look for this "token_tfc" global variable and will include this one inside headers like:

        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtdmFycm9uZSIsImV4cCI6MTY0OTIwODcyMn0.kN-uZtGBNb2Qvp6O-YgZW8jc8ZCoO2a3N7k8S7toSmQ'
        }

    Note: This example access token is no longer valid when uploaded to GitHub.

"""
    write_info('postman/README.md', postman_text)
    return "OK"

# >>> proc = subprocess.Popen('ls', stdout=subprocess.PIPE)
# >>> output = proc.stdout.read()
# >>> print output


def check_nginx_status(base_nginx_path):
    proc = subprocess.Popen(
        'tasklist /fi "imagename eq nginx.exe"', stdout=subprocess.PIPE)
    output = str(proc.stdout.read())

    if "nginx.exe" in output:
        return "OK"
    else:
        os.chdir(base_nginx_path)
        if subprocess.call('start nginx.exe', shell=True) == 0:
            return "OK, now is active"


def open_browser(url):
    if webbrowser.open(url, new=2):
        return "OK, opening browser tab ..."


if __name__ == "__main__":
    print("\n===== TRYING TO DEPLOY =====\n")
    build_response = build()
    print("\n===== RESULTS =====")
    print("\n1. Build:", build_response)
    print("2. Cut:", cut_dist_folder())
    response = create_api_docs_in_json_file(BASE_BACKEND_URL)
    print("3. Create backend/postman/openapi.json:", response["info"])

    if response["status_code"] == 200:
        print(
            "4. Create backend/postman/README.md:",
            create_README_file(BASE_BACKEND_URL))
    else:
        print("4. Create backend/postman/README.md:", "Not executed")
    print("5. nginx:", check_nginx_status(BASE_NGINX_PATH))
    print("6. Browser:", open_browser(BASE_FRONTEND_URL), "\n")

# push code to GitHub
