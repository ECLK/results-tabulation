# Deploying tabulation BACKEND on production environments

## Prerequisites

Production environment created by following https://github.com/ECLK/Deployment
WSO2 API Manager with IS as km
Platformer cloud account connected to Prod k8s cluster for CI/CD
Deploy https://github.com/ECLK/auth-app using platformer cloud

##  Application Setup

### On Platformer cloud

* Create an app for tabulation backend
* Connect ECLK/results-tabulation-api in the Repository section
* Create appropriate BUILD CONFIG
    * Dockerfile path - ./rest/results-tabulation-api/Dockerfile
    * Build context - ./rest/results-tabulation-api
* Setup Environment variables on RUN TIME
    * ENV_CONFIG - path to the environment config file
* Add Config file on CONFIG FILES
```
DEBUG = False

DATABASE_PLUGIN = "mysql+pymysql"
DATABASE_USERNAME = ""
DATABASE_PASSWORD = ""
DATABASE_HOST = ""
DATABASE_PORT = ""
DATABASE_NAME = ""


RESULT_DISSEMINATION_SYSTEM_URL = ""
RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE = "2019PRE"
RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE = "PRESIDENTIAL-FIRST"
RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF = "PRESIDENTIAL-PREF"

PROD_ENV = True

```

### On API Manager

On publisher app
* Create a new API and select Design a New REST API
* On DESIGN tab Under API Definition import the swagger file
* On IMPLEMENT tab provide tabulation backend internal URL. this can be found in the platformer cloud app overview.
* Save and Publish

On Store app
* Add APPLICATION for tabulation with Token Type OAuth
* Subscribe to the newly created app from tabulation API
* Go to application -> production keys and set callback URL - this should be the /tabulation/auth/callback on UI
* Copy Consumer Key and Consumer Secret and update auth.js of the auth app

## Application Maintaining

### Rollback to the previous version
* Go to BUILD tab on platformer cloud app
* Click Action -> Deploy on the version desired to rollback from the build list

### Swagger file updates
* Go to API store tabulation API
* Edit API
* Edit source under the API Definition
* Replace new swagger file content and save changes

### Change Environment variables
* Go to platformer cloud tabulation-api app
* Under RUN TIME tab add or edit ENV
* Click on Apply
