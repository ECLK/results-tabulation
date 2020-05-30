# Deploying tabulation FRONTEND on production environments

## Prerequisites

Production environment created by following https://github.com/ECLK/Deployment
WSO2 API Manager with IS as km
Tabulation BACKEND running on the environment
Platformer cloud account connected to Prod k8s cluster for CI/CD
Deploy https://github.com/ECLK/auth-app using platformer cloud

##  Application Setup

### On Platformer cloud

* Create an app for tabulation frontend
* Connect ECLK/results-tabulation-api in the Repository section
* Create appropriate BUILD CONFIG
    * Dockerfile path - ./results-tabulation-ui/prod.Dockerfile
    * Build context - ./results-tabulation-ui
* Add Config file on CONFIG FILES - /app/src/configs/app.js 
```
const DEFAULT_CONFIG = {
    BASE_PATH: "tabulation",
    HOME_PATH: "/home",
    LOGIN_PATH: "/login",
    LOGOUT_PATH: "/logout",
    IS_ENDPOINT: "",
    CLIENT_ID: "",
    CLIENT_HOST: " tabulations url ",
    LOGIN_CALLBACK_URL: "tabulations url/tabulation/login",
    LOGOUT_CALLBACK_URL: "tabulations url/tabulation/logout"
};


```
* Add DNS URL

## Application Maintaining

### Rollback to the previous version
* Go to BUILD tab on platformer cloud app
* Click Action -> Deploy on the version desired to rollback from the build list

### Change Environment variables
* Go to platformer cloud tabulation-api app
* Under RUN TIME tab add or edit ENV
* Click on Apply
