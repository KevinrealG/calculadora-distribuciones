const assert = require('assert');
const {
  vectorFromTwoPoints,
  vectorFromPointAndOrigin,
  vectorFromDirectionAndMagnitude,
  vectorMagnitude,
  normalizeVector,
  directionAngle2D,
  angleBetweenVectors,
} = require('../js/vector_operations.js');

const vAB = vectorFromTwoPoints([0, 0], [3, 4]);
assert.deepStrictEqual(vAB, [3, 4]);

const vPO = vectorFromPointAndOrigin([2, -1], [0, 0]);
assert.deepStrictEqual(vPO, [2, -1]);

const vDir = vectorFromDirectionAndMagnitude(2, 90);
assert.ok(Math.abs(vDir[0]) < 1e-10);
assert.ok(Math.abs(vDir[1] - 2) < 1e-10);

assert.ok(Math.abs(vectorMagnitude([3, 4]) - 5) < 1e-9);
assert.ok(Math.abs(directionAngle2D([1, 1]) - 45) < 1e-6);
assert.ok(Math.abs(angleBetweenVectors([1, 0], [0, 1]) - 90) < 1e-6);

console.log('Pruebas de operaciones con vectores: OK');
