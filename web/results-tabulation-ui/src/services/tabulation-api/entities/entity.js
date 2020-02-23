import getCache from "../cache";

export default class Entity {
    constructor(entityId) {
        const cache = getCache();
        if (!cache[entityId]) {
            cache[entityId] = {map: {}, list: []};
        }

        this.cache = cache[entityId];
    }

    list() {
        return this.cache.list;
    }

    map() {
        return this.cache.map;
    }

    async push(obj, pk) {
        const pkValue = obj[pk];

        if (this.cache.map[pkValue]) {
            // Update if already exists.
            Object.assign(this.cache.map[pkValue], obj)
        } else {
            // Created if doesn't exists.
            this.cache.map[pkValue] = obj; // TODO
            this.cache.list = [...this.cache.list, pkValue];
        }

        return obj;
    }

    async pushList(list, pk) {
        for (let i = 0; i < list.length; i++) {
            this.push(list[i], pk);
        }
    }

    async fetchAndPush(id) {
        //TODO
    }

    async getById(id) {
        return this.map()[id];
    }
}
