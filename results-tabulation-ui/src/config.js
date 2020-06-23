export let AUTH_APP_URL = "http://localhost:3001";
export let TABULATION_API_URL = 'http://localhost:8280/tabulation/0.1.0';
export let DEBUG = false;

if (process.env.REACT_APP_AUTH_APP_URL) {
    AUTH_APP_URL = process.env.REACT_APP_AUTH_APP_URL;
}

if (process.env.REACT_APP_TABULATION_API_URL) {
    TABULATION_API_URL = process.env.REACT_APP_TABULATION_API_URL;
}

if (process.env.REACT_APP_DEBUG) {
    DEBUG = process.env.REACT_APP_DEBUG;
}
