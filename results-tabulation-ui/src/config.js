export let AUTH_APP_URL = "http://localhost:3001";
export let TABULATION_API_URL = 'http://localhost:5000';
export let DEBUG = false;
export let TABULATION_API_PAGINATION_LIMIT = 500;
export let USE_PDF_SERVICE = true;

if (process.env.REACT_APP_AUTH_APP_URL) {
    AUTH_APP_URL = process.env.REACT_APP_AUTH_APP_URL;
}

if (process.env.REACT_APP_TABULATION_API_URL) {
    TABULATION_API_URL = process.env.REACT_APP_TABULATION_API_URL;
}

if (process.env.REACT_APP_DEBUG) {
    DEBUG = getBooleanEnvVar(process.env.REACT_APP_DEBUG, DEBUG);
}

if (process.env.REACT_APP_TABULATION_API_PAGINATION_LIMIT) {
    TABULATION_API_PAGINATION_LIMIT = getIntEnvVar(process.env.REACT_APP_TABULATION_API_PAGINATION_LIMIT, TABULATION_API_PAGINATION_LIMIT);
}

if (process.env.REACT_APP_USE_PDF_SERVICE) {
    USE_PDF_SERVICE = getBooleanEnvVar(process.env.REACT_APP_USE_PDF_SERVICE, USE_PDF_SERVICE);
}

function getBooleanEnvVar(envVar, defaultValue) {
    if (envVar) {
        envVar = envVar.toLowerCase();
        if (envVar === "true") {
            envVar = true;
        } else if (envVar === "false") {
            envVar = false;
        } else {
            envVar = defaultValue;
        }
    } else {
        envVar = defaultValue;
    }

    return envVar;
}


function getIntEnvVar(envVar, defaultValue) {
    if (envVar) {
        try {
            envVar = parseInt(envVar);
        } catch (e) {
            envVar = defaultValue;
        }
    } else {
        envVar = defaultValue;
    }

    return envVar;
}
