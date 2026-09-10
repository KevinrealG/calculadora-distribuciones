function parsearDatos(texto) {
    if (!texto || !texto.trim()) return [];

    return texto
        .split(/[;\n]+/)
        .flatMap(part => part.split(','))
        .map(item => item.trim())
        .filter(Boolean);
}

function normalizarNumero(valor) {
    if (valor === null || valor === undefined || valor === '') return NaN;
    const texto = String(valor).trim().replace(/\./g, '').replace(',', '.');
    const numero = Number(texto);
    return Number.isFinite(numero) ? numero : NaN;
}

function parsearDatosAgrupados(texto) {
    if (!texto || !texto.trim()) return [];

    const lineas = texto
        .split(/\r?\n/)
        .map(linea => linea.trim())
        .filter(Boolean)
        .filter(linea => !/^curso|^grupo|^categoria|^variable/i.test(linea));

    const registros = [];

    lineas.forEach(linea => {
        const partes = linea.split(/\t|\s*;\s*|\s*\|\s*/).map(p => p.trim()).filter(Boolean);
        if (partes.length >= 2) {
            const grupo = partes[0];
            const valor = normalizarNumero(partes[1]);
            if (grupo && !Number.isNaN(valor)) {
                registros.push({ grupo, valor });
            }
        }
    });

    return registros;
}

function calcularCuartil(datos, q) {
    const valores = [...datos].sort((a, b) => a - b);
    if (!valores.length) return 0;
    if (valores.length === 1) return valores[0];

    const posicion = (valores.length - 1) * q;
    const inferior = Math.floor(posicion);
    const superior = Math.ceil(posicion);
    const fraccion = posicion - inferior;

    if (inferior === superior) return valores[inferior];
    return valores[inferior] + (valores[superior] - valores[inferior]) * fraccion;
}

function calcularEstadisticosGrupo(valores) {
    const numero = valores.map(v => Number(v));
    const n = numero.length;
    if (!n) {
        return null;
    }

    const sum = numero.reduce((acc, value) => acc + value, 0);
    const mean = sum / n;
    const sorted = [...numero].sort((a, b) => a - b);
    const median = n % 2 === 0 ? (sorted[n / 2 - 1] + sorted[n / 2]) / 2 : sorted[Math.floor(n / 2)];
    const varianza = numero.reduce((acc, value) => acc + (value - mean) ** 2, 0) / (n - 1 || 1);
    const desviacion = Math.sqrt(varianza);

    return {
        n,
        media: mean,
        mediana: median,
        desviacion: desviacion,
        minimo: sorted[0],
        maximo: sorted[n - 1],
        q1: calcularCuartil(numero, 0.25),
        q3: calcularCuartil(numero, 0.75)
    };
}

function analizarTipoVariable(datos) {
    const valores = parsearDatos(Array.isArray(datos) ? datos.join(',') : datos || '');

    if (!valores.length) {
        return { tipo: 'Sin datos', detalle: 'No hay datos para clasificar.', esCuantitativa: false, esCualitativa: false };
    }

    const numericos = valores.filter(valor => /^-?\d+(\.\d+)?$/.test(valor));
    const noNumericos = valores.filter(valor => !/^-?\d+(\.\d+)?$/.test(valor));

    if (!numericos.length && noNumericos.length) {
        return {
            tipo: 'Cualitativa',
            detalle: 'Todos los valores son categorías o etiquetas, no medidas numéricas.',
            esCuantitativa: false,
            esCualitativa: true,
            categorias: [...new Set(noNumericos)]
        };
    }

    if (numericos.length && !noNumericos.length) {
        return {
            tipo: 'Cuantitativa',
            detalle: 'Todos los valores son numéricos, por lo que se puede analizar cuantitativamente.',
            esCuantitativa: true,
            esCualitativa: false,
            datos: numericos.map(Number)
        };
    }

    return {
        tipo: 'Mixta',
        detalle: 'Se detectaron valores numéricos y no numéricos; la muestra combina categorías y magnitudes.',
        esCuantitativa: false,
        esCualitativa: false,
        numericos,
        noNumericos
    };
}

function clasificarVariableDesdeTexto(texto) {
    const datos = parsearDatos(texto);
    const analisis = analizarTipoVariable(datos);

    const valores = {
        total: datos.length,
        numericos: analisis.numericos ? analisis.numericos.length : 0,
        noNumericos: analisis.noNumericos ? analisis.noNumericos.length : 0,
        categorias: analisis.categorias ? analisis.categorias.length : 0,
        tipo: analisis.tipo,
        detalle: analisis.detalle
    };

    return { ...analisis, valores };
}

function analizarDatosPorGrupo(texto) {
    const registros = parsearDatosAgrupados(texto);

    if (!registros.length) {
        return {
            ok: false,
            mensaje: 'Ingresa datos con dos columnas: categoría y valor numérico (ej. CURSO\t3,4).',
            grupos: []
        };
    }

    const grupos = new Map();
    registros.forEach(({ grupo, valor }) => {
        if (!grupos.has(grupo)) grupos.set(grupo, []);
        grupos.get(grupo).push(valor);
    });

    const entradas = [...grupos.entries()].map(([grupo, valores]) => ({
        grupo,
        valores,
        estadisticos: calcularEstadisticosGrupo(valores)
    }));

    return {
        ok: true,
        mensaje: 'Análisis por grupos disponible.',
        grupos: entradas
    };
}

function renderizarAnalisisPorGrupo(texto) {
    const analisis = analizarDatosPorGrupo(texto);

    if (!analisis.ok) {
        return { ok: false, html: `<p style="color:#dc2626;">${analisis.mensaje}</p>` };
    }

    const tablas = analisis.grupos.map(({ grupo, valores, estadisticos }) => `
        <tr>
            <td>${grupo}</td>
            <td>${estadisticos.n}</td>
            <td>${estadisticos.media.toFixed(2)}</td>
            <td>${estadisticos.mediana.toFixed(2)}</td>
            <td>${estadisticos.desviacion.toFixed(2)}</td>
            <td>${estadisticos.minimo.toFixed(2)}</td>
            <td>${estadisticos.maximo.toFixed(2)}</td>
            <td>${estadisticos.q1.toFixed(2)}</td>
            <td>${estadisticos.q3.toFixed(2)}</td>
        </tr>
    `).join('');

    const html = `
        <div style="display:grid; gap:16px;">
            <div class="callout success">
                <h5>Tipo detectado: Variable cualitativa + cuantitativa</h5>
                <p>Se compararon ${analisis.grupos.length} grupos según la variable numérica.</p>
            </div>
            <div id="comparative-boxplot" style="width:100%; height:380px;"></div>
            <table class="hover">
                <thead>
                    <tr>
                        <th>Grupo</th>
                        <th>n</th>
                        <th>Media</th>
                        <th>Mediana</th>
                        <th>Desv. Std.</th>
                        <th>Mín.</th>
                        <th>Máx.</th>
                        <th>Q1</th>
                        <th>Q3</th>
                    </tr>
                </thead>
                <tbody>${tablas}</tbody>
            </table>
        </div>
    `;

    if (typeof window !== 'undefined' && window.Plotly) {
        const traces = analisis.grupos.map(({ grupo, valores }) => ({
            type: 'box',
            name: grupo,
            y: valores,
            boxpoints: false,
            jitter: 0.3,
            whiskerwidth: 0.5,
            marker: { color: '#4f46e5' }
        }));

        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#374151' },
            title: 'Boxplot comparativo por grupos',
            yaxis: { title: 'Valor numérico' },
            xaxis: { title: 'Categoría' },
            margin: { t: 40, b: 80, l: 50, r: 20 }
        };

        const config = { responsive: true, displaylogo: false };
        requestAnimationFrame(() => {
            Plotly.newPlot('comparative-boxplot', traces, layout, config);
        });
    }

    return { ok: true, html };
}

if (typeof window !== 'undefined') {
    window.parsearDatos = parsearDatos;
    window.analizarTipoVariable = analizarTipoVariable;
    window.clasificarVariableDesdeTexto = clasificarVariableDesdeTexto;
    window.parsearDatosAgrupados = parsearDatosAgrupados;
    window.analizarDatosPorGrupo = analizarDatosPorGrupo;
    window.renderizarAnalisisPorGrupo = renderizarAnalisisPorGrupo;
}

if (typeof module !== 'undefined') {
    module.exports = {
        parsearDatos,
        normalizarNumero,
        analizarTipoVariable,
        clasificarVariableDesdeTexto,
        parsearDatosAgrupados,
        analizarDatosPorGrupo,
        renderizarAnalisisPorGrupo
    };
}
