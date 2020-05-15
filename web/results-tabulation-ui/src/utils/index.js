import {API_MESSAGES_EN} from "../locale/messages_en";

export * from "../auth";
export * from "./history";

export function getNumOrZero(num) {
    if (!num) {
        num = 0
    } else if (typeof num != "number") {
        try {
            num = Number(num);
            num = getNumOrZero(num)
        } catch (e) {
            num = 0
        }
    }

    return num
}

export function isNumeric(n) {
    return !isNaN(parseInt(n)) && isFinite(n);
}

export function processNumericValue(value) {
    if (value === "") {
        return 0
    }
    if (isNumeric(value)) {
        let val = parseInt(value);
        return val > 0 ? val : val * (-1)
    }
    return value
}

export function getFirstOrNull(list) {
    if (list && list.length > 0) {
        return list[0];
    }

    return null;
}

export function fieldMatch(key, value) {
    if (!key || !value) {
        return true
    }
    return key.toLowerCase().includes(value.toLowerCase());
}

export function getDeepObjectValue(path, object) {
    return path.reduce((x, value) => (x && x[value]) ? x[value] : null, object);
}

export function getErrorCode(e) {
    return getDeepObjectValue(['response', 'data', 'code'], e);
}

export function getErrorMessage(errorCode) {
    return API_MESSAGES_EN[errorCode] ? API_MESSAGES_EN[errorCode] : "Unknown Error";
}

export function sum(list, skipInvalidValues = false) {
    let _sum = null;
    if (skipInvalidValues) {
        _sum = 0;
    }

    for (let i = 0; i < list.length; i++) {
        const value = list[i];

        if (skipInvalidValues && typeof value !== "number") {
            continue;
        }

        if(i == 0) {
            _sum = value;
        } else {
            _sum += value
        }
    }

    return _sum;
}