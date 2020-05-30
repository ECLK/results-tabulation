import axios from 'axios';
import {TABULATION_API_URL} from "./config";

const instance = axios.create({
    baseURL: TABULATION_API_URL
});

export default instance;
;