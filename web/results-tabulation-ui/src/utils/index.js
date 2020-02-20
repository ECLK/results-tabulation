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
