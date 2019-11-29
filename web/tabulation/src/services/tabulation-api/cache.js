const CACHE_KEY = "tabulationUiCache";

export default function getCache() {
    if (!window[CACHE_KEY]) {
        window[CACHE_KEY] = {};
    }

    return window[CACHE_KEY];
}

