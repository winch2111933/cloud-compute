# Waqq.ly - Find Your Freindly Dog Walker App
Waqq.ly is a cloud-hosted web application on Microsoft Azure designed to connect dog owners with local dog walkers. 

This GitHub repository contains all necessary code to deploy the prototype, following the steps below.

## Azure SQL Database
The backend database is hosted on Microsoft's relational Database as a Service platform Azure SQL Database. Follow the below steps to create the Azure resource and SQL objects.

- Login to the Azure Portal, go to Create a resource and select Azure SQL Database to create a new SQL resource using SQL authentication.
- **Basic Configuration:**
  - Select the appropriate subscription.
  - Select an existing resource group or create a new one by clicking 'Create new'.
  - Enter the database name waqqly_db.
  - Click on 'Create new' to set up a new server. Provide the server name waqqly_db_svr, admin login, password, and select the region. Click 'OK' to create the server.
- **Select Compute + Storage (DTUs):**
  - Click on the 'Compute + storage' link. 
  - In the 'Service tier' dropdown, select 'Basic'. Under 'DTUs', choose '5 DTUs'. 
  - Click 'Apply' to save the settings.
- **Configure Networking:**
  - Go to the 'Networking' tab.
  - For 'Connectivity method', select 'Public endpoint'.
  - Set 'Add current client IP address' to 'Yes'.
  - Set 'Allow Azure services and resources to access this server' to 'Yes'.
- **Review + Create:**
  - Go to the 'Review + create' tab.
  - Click on 'Create' to start the deployment process.
- **Create SQL Objects:**
  - After the deployment process is complete, open the 'Query editor', sign in, and run the SQL setup script named "create_db.sql".
- **SQL Connection String:**
  - Go to 'Settings > Connection strings' within the database, and copy the 'ODBC' connection string and save for later.

## Azure Function for API
The middle layer of the application stack is hosted on Azure Functions. To set up the Azure Function you will need the following installed:
1. Visual Studio Code (VS Code)
2. Python 3.10
3. Python Extension for VS Code
4. Azure Functions Extension for VS Code

- **Create the Azure Function Resource:**
  - Log in to the Azure Portal and navigate to Create a Resource.
  - In the search bar, type 'Function App' and select it from the dropdown list. Click on the 'Create' button.
- **Configure Basic Settings:**
  - Select the appropriate subscription.
  - Select an existing resource group or create a new one by clicking 'Create new'.
  - Name the Function App "waqqly-api"
  - Select Python as the runtime stack 
- **Configure Hosting:**
  - Select Linux for the OS and choose 'Consumption (Serverless)' for pay-per-execution plan.
  - Click on 'Create' to start the deployment process.
- **Open VS Code:**
  - Access the Azure extension (Shift+Alt+A), and sign in with your Azure account.
  - Right-click the Function App folder named 'api' and select 'Deploy to Function App', then add a new setting named SqlConnectionString with the connection string from the Azure SQL Database.
  - Copy the Function URLs for 'search', 'walker' and 'dog' by right-clicking each and save the links.
  - In the Web folder of the repository, update 'index.html', 'enterwalker.html' and 'enterdog.html' by replacing the variable string assigned to const funcUrl = with the urls saved from creating the Azure Function App APIs.
  - In the Azure Portal, open the Function App and go to 'API > CORS'. Add an asterisk (*) to Allowed Origins and remove any others.

## Azure Static Web App
The front end website is hosted on an Azure Static Web App containing HTML, CSS, JavaScript and image files.

- **Create an Azure Static Web App:**
  - Log in to the Azure Portal and navigate to Create a Resource. 
  - Click on the 'Create a resource' button in the upper left corner.
  - In the search bar, type 'Static Web App' and select it from the dropdown list.
  - Click on the 'Create' button.
- **Configure Basic Settings:**
  - Select the appropriate subscription.
  - Select an existing resource group or create a new one by clicking 'Create new'.
  - Name the app "waqqly-static-web-app" and select a region.
  - Choose 'Free' hosting plan.
- **Configure Deployment:**
  - Select 'GitHub' as the source.
  - Click 'Sign in with GitHub' and authorise Azure to access your GitHub account.
  - Select the GitHub user under which the repository is located.
  - Select the repository that contains the web pages and the main branch.
  - Enter ./web as the folder where the web pages are located. Leave API blank.
  - Click on 'Create' to start the deployment process.