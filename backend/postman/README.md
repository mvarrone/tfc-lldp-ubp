# How to import API documentation into Postman

        * Open Postman
        * Go to "APIs", select "Create an API", select "Import" tab
        3) Under "Import local schema files", hit "Select files" Button
        4) Select openapi.json located inside postman directory
        5) On next page, click on Import button and then on Close button
        6) API docs is imported on Collections and APIs Tabs. Use what you like
        7) Go to FastAPIDocumentation > draft > FastAPIDocumentation > Variables
        8) Set baseUrl:
            VARIABLE: baseUrl
            INITIAL VALUE: /
            CURRENT VALUE: https://www.lldp.duckdns.org:5000
            Be sure this field is checked
        9) Click on Save Button (upper right located)
        10) Now, you can test every endpoint
            Example: {{baseUrl}}/logs
