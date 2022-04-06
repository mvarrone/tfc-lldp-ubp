import os
import shutil

import requests


def deploy():
    path1 = "D://Documentos//Mati//tfc//frontend//dist"  # compiled dist folder
    path2 = "C://nginx-1.21.6//projects//tfc//dist"  # nginx project folder

    value_1 = os.path.isdir(path1)
    if not value_1:
        return "\ndist folder not found at tfc/frontend"

    value_2 = os.path.isdir(path2)
    if value_2:
        mydir = path2
        try:
            shutil.rmtree(mydir)
            shutil.move(path1, path2)
            print("\nDone\n")
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        try:
            shutil.move(path1, path2)
            print("\nDone\n")
        except Exception as e:
            print(e)


def write_info(path, text):
    with open(path, 'a') as f:
        f.write(text)


def get_api_json():
    base_url = "https://www.lldp.duckdns.org:5000"
    full_url = base_url + "/openapi.json"

    payload = {}
    headers = {}

    response = requests.request("GET", full_url, headers=headers, data=payload)

    if response.status_code == 200:
        if not os.path.exists("postman"):
            os.mkdir("postman")
        else:
            shutil.rmtree("postman")
            os.mkdir("postman")

        write_info('postman/openapi.json', response.text)

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
    - CURRENT VALUE: """ + base_url + """
    - Be sure this field is checked
9. Click on Save Button (upper right located)
10. Now, you can test every endpoint

    Example: {{baseUrl}}/logs

### Authentication

1. Configure access token as a global variable

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

    - On "tfc" collection, go to "Authorization" tab and select:

        Type: Bearer Token
        Token: {{token_tfc}}

3. Configure endpoints to inherit auth from parent collection

    - For every endpoint:

        Go to "Authorization" tab and select "Inherit auth from parent" (in Type section)
    
    Under this, you will see "This request is using Bearer Token from collection tfc."

4. Test every endpoint

    -At this point, it should be possible to get successful responses for every endpoint

    Every endpoint will look for this "token_tfc" global variable and will include this one inside headers like:

        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtdmFycm9uZSIsImV4cCI6MTY0OTIwODcyMn0.kN-uZtGBNb2Qvp6O-YgZW8jc8ZCoO2a3N7k8S7toSmQ'
        }

    Note: This access example token is no longer valid when uploaded to GitHub.

"""

        write_info('postman/README.md', postman_text)

        return "\nAPI docs copied to postman/openapi.json and README.md created\n"
    else:
        return "\nStatus code: " + str(response.status_code) + "\n"


if __name__ == "__main__":
    print(deploy())
    print(get_api_json())
