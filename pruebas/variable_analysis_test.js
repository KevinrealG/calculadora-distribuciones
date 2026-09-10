const assert = require('assert');
const { analizarTipoVariable, parsearDatos } = require('../js/variable_analysis.js');

const datosCuantitativos = parsearDatos('12, 15, 18, 20, 25');
assert.strictEqual(analizarTipoVariable(datosCuantitativos).tipo, 'Cuantitativa');

const datosCualitativos = parsearDatos('Rojo, Azul, Verde, Rojo, Azul');
assert.strictEqual(analizarTipoVariable(datosCualitativos).tipo, 'Cualitativa');

const datosMixtos = parsearDatos('Rojo, 12, Azul');
assert.strictEqual(analizarTipoVariable(datosMixtos).tipo, 'Mixta');

console.log('Pruebas de análisis cualitativa vs cuantitativa: OK');
