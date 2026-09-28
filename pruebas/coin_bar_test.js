const assert = require('assert');
const { buildCoinBars } = require('../js/coin_bars.js');

const html = buildCoinBars({ heads: 7, tails: 3 });

assert.match(html, /bar-cara/);
assert.match(html, /bar-sello/);
assert.match(html, /Cara/);
assert.match(html, /Sello/);

console.log('Pruebas de barras de conteo: OK');
