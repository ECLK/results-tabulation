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
    DEBUG = process.env.REACT_APP_DEBUG;
}

if (process.env.TABULATION_API_PAGINATION_LIMIT) {
    TABULATION_API_PAGINATION_LIMIT = process.env.TABULATION_API_PAGINATION_LIMIT;
}

if (process.env.USE_PDF_SERVICE) {
    USE_PDF_SERVICE = process.env.USE_PDF_SERVICE;
}
