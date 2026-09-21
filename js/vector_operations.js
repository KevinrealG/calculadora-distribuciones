(function () {
    const api = {};

    function isArray(value) {
        return Array.isArray(value);
    }

    function clampDimension(values, targetLength) {
        if (!isArray(values)) return Array(targetLength).fill(0);
        return values.slice(0, targetLength).concat(Array(Math.max(0, targetLength - values.length)).fill(0));
    }

    api.vectorFromTwoPoints = function vectorFromTwoPoints(start, end) {
        const a = clampDimension(start, 3);
        const b = clampDimension(end, 3);
        return a.map((value, index) => b[index] - value);
    };

    api.vectorFromPointAndOrigin = function vectorFromPointAndOrigin(point, origin) {
        const p = clampDimension(point, 3);
        const o = clampDimension(origin, 3);
        return p.map((value, index) => value - o[index]);
    };

    api.vectorFromDirectionAndMagnitude = function vectorFromDirectionAndMagnitude(direction, magnitude) {
        const mag = Number(magnitude) || 0;
        if (isArray(direction)) {
            const dir = clampDimension(direction, 3);
            const norm = api.vectorMagnitude(dir);
            if (norm === 0) return [0, 0, 0].slice(0, dir.length);
            return dir.map(value => (value / norm) * mag);
        }

        const angleInRadians = ((Number(direction) || 0) * Math.PI) / 180;
        return [Math.cos(angleInRadians) * mag, Math.sin(angleInRadians) * mag];
    };

    api.vectorMagnitude = function vectorMagnitude(vector) {
        const values = clampDimension(vector, 3);
        return Math.sqrt(values.reduce((sum, value) => sum + value * value, 0));
    };

    api.normalizeVector = function normalizeVector(vector) {
        const values = clampDimension(vector, 3);
        const norm = api.vectorMagnitude(values);
        if (norm === 0) return [0, 0, 0].slice(0, values.length);
        return values.map(value => value / norm);
    };

    api.dotProduct = function dotProduct(u, v) {
        const a = clampDimension(u, 3);
        const b = clampDimension(v, 3);
        return a.reduce((sum, value, index) => sum + value * b[index], 0);
    };

    api.directionAngle2D = function directionAngle2D(vector) {
        const values = clampDimension(vector, 2);
        const [x, y] = values;
        if (api.vectorMagnitude(values) === 0) return 0;
        return (Math.atan2(y, x) * 180) / Math.PI;
    };

    api.directionAzimuth = function directionAzimuth(vector) {
        const values = clampDimension(vector, 3);
        const [x, y] = values;
        if (api.vectorMagnitude(values) === 0) return 0;
        return (Math.atan2(y, x) * 180) / Math.PI;
    };

    api.directionElevation = function directionElevation(vector) {
        const values = clampDimension(vector, 3);
        const [x, y, z] = values;
        const horizontal = Math.sqrt(x * x + y * y);
        if (horizontal === 0 && z === 0) return 0;
        return (Math.atan2(z, horizontal) * 180) / Math.PI;
    };

    api.angleBetweenVectors = function angleBetweenVectors(u, v) {
        const a = clampDimension(u, 3);
        const b = clampDimension(v, 3);
        const magA = api.vectorMagnitude(a);
        const magB = api.vectorMagnitude(b);
        if (magA === 0 || magB === 0) return 0;
        const cosTheta = api.dotProduct(a, b) / (magA * magB);
        return (Math.acos(Math.max(-1, Math.min(1, cosTheta))) * 180) / Math.PI;
    };

    if (typeof window !== 'undefined') {
        window.VectorOperations = api;
    }

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = api;
    }
})();
