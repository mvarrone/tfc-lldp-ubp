# How to import API documentation into Postman

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
    - CURRENT VALUE: https://www.lldp.duckdns.org:5000
    - Be sure this field is checked
9. Click on Save Button (upper right located)
10. Now, you can test every endpoint

    Example: {{baseUrl}}/logs

### Authentication

1. Configure access token as a global variable

    - In /login POST Method
    
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

    - For every endpoint, go to "Authorization" tab and select "Inherit auth from parent" (in Type section)
    
    Under this, you will see "This request is using Bearer Token from collection tfc."

4. Test every endpoint

    -At this point, it should be possible to get successful responses for every endpoint
    Every endpoint will look for this "token_tfc" global variable and will include this one inside headers like:

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtdmFycm9uZSIsImV4cCI6MTY0OTIwODcyMn0.kN-uZtGBNb2Qvp6O-YgZW8jc8ZCoO2a3N7k8S7toSmQ'
    }

    Note: This access example token is no longer valid when uploaded to GitHub.

