# How to import API documentation into Postman

- Open Postman
- Go to "APIs", select "Create an API", select "Import" tab
- Under "Import local schema files", hit "Select files" Button

- Select openapi.json located inside postman directory
- On next page, click on Import button and then on Close button
- API docs is imported on Collections and APIs Tabs. Use what you like
- Go to FastAPIDocumentation > draft > FastAPIDocumentation > Variables
- Set baseUrl:
  VARIABLE: baseUrl
  INITIAL VALUE: /
  CURRENT VALUE: https://www.lldp.duckdns.org:5000
  Be sure this field is checked
- Click on Save Button (upper right located)
- Now, you can test every endpoint
  Example: {{baseUrl}}/logs
