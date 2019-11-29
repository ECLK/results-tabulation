export let AUTH_APP_URL = "http://localhost:3001";
export let TABULATION_API_URL = 'http://localhost:5000';

if (process.env.REACT_APP_AUTH_APP_URL) {
    AUTH_APP_URL = process.env.REACT_APP_AUTH_APP_URL;
}

if (process.env.REACT_APP_TABULATION_API_URL) {
    TABULATION_API_URL = process.env.REACT_APP_TABULATION_API_URL;
}
