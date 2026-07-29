document.addEventListener("DOMContentLoaded", function () {
    const formulaPanel = document.getElementById("formula-panel");

    if (!formulaPanel || !window.MathJax || !window.MathJax.typesetPromise) {
        return;
    }

    const observer = new MutationObserver(function () {
        window.MathJax.typesetPromise().catch(function () {
            // Ignorar errores de render en cambios rápidos.
        });
    });

    observer.observe(formulaPanel, {
        childList: true,
        subtree: true,
        characterData: true
    });
});
// Manejo del selector desplegable
document.getElementById('desc-view-selector').addEventListener('change', function(e) {
    const views = document.querySelectorAll('.desc-sub-view');
    views.forEach(view => view.style.display = 'none');
    
    const selectedView = document.getElementById(e.target.value);
    if(selectedView) {
        selectedView.style.display = 'block';
        // Refrescar tabs de Foundation en la nueva vista
        $(document).foundation(); 
    }
});

// Lógica universal para agregar filas
document.querySelectorAll('.btn-add-fila').forEach(btn => {
    btn.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const tbody = document.getElementById(targetId);
        
        if(tbody && tbody.children.length > 0) {
            // Clona la primera fila para mantener los inputs correctos
            const nuevaFila = tbody.children[0].cloneNode(true);
            // Limpia los valores
            nuevaFila.querySelectorAll('input').forEach(input => input.value = '');
            tbody.appendChild(nuevaFila);
        }
    });
});

// Lógica universal para eliminar filas (Delegación)
document.addEventListener('click', function(e) {
    if(e.target.classList.contains('btn-del-fila')) {
        const tbody = e.target.closest('tbody');
        if(tbody && tbody.children.length > 1) { // Evita borrar la última fila
            e.target.closest('tr').remove();
        } else {
            mostrarError("No puedes eliminar la última fila.");
        }
    }
});

// Función para mostrar errores visuales
function mostrarError(mensaje) {
    const contenedor = document.getElementById('desc-error-container');
    contenedor.innerHTML = `
        <div class="callout alert" data-closable>
            <h5>⚠️ Error</h5>
            <p>${mensaje}</p>
            <button class="close-button" aria-label="Dismiss alert" type="button" data-close>
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `;
    // Inicializar el botón de cierre de Foundation
    $(document).foundation();
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        contenedor.innerHTML = '';
    }, 5000);
}

/* =========================================
   ÁLGEBRA LINEAL - SELECTOR DE MATRICES
   ========================================= */
/* =========================================
   ÁLGEBRA LINEAL - SELECTOR DE MATRICES
   ========================================= */
// Mostrar u ocultar el popup de manera controlada
function toggleMatrixPopup(e) {
    if (e) e.stopPropagation(); // Evita que el clic se propague y cause errores
    
    const popup = document.getElementById('matrix-popup');
    if (popup) {
        const isHidden = popup.style.display === 'none' || popup.style.display === '';
        popup.style.display = isHidden ? 'block' : 'none';
        
        // Reiniciamos visualmente a 1x1 cada vez que se abre
        if (isHidden) {
            highlightCells(1, 1);
            const sizeTxt = document.getElementById('matrixSizeTxt');
            if (sizeTxt) sizeTxt.textContent = "Tamaño de la matriz: 1x1";
        }
    }
}

// Cerrar el popup si el usuario hace clic en cualquier otro lado de la pantalla
document.addEventListener('click', (e) => {
    const popup = document.getElementById('matrix-popup');
    if (popup && popup.style.display === 'block') {
        // Si el clic no fue dentro del popup ni en su botón contenedor
        if (!popup.contains(e.target) && !e.target.closest('.al-custom-size-wrapper')) {
            popup.style.display = 'none';
        }
    }
});

// Inicializar la cuadrícula 10x10
function initMatrixGrid() {
    const grid = document.getElementById('matrixGrid');
    if (!grid) return;
    grid.innerHTML = ''; // Limpiar cuadrícula
    
    const sizeTxt = document.getElementById('matrixSizeTxt');
    const cols = 10; 
    const rows = 10;

    for (let r = 1; r <= rows; r++) {
        for (let c = 1; c <= cols; c++) {
            const cell = document.createElement('div');
            cell.className = 'matrix-cell';
            cell.dataset.row = r;
            cell.dataset.col = c;
            
            // Evento para resaltar al pasar el ratón
            cell.addEventListener('mouseover', () => {
                highlightCells(r, c);
                if(sizeTxt) sizeTxt.textContent = `Tamaño de la matriz: ${r}x${c}`;
            });
            
            // Evento para insertar la matriz al hacer clic (Corregido)
            cell.addEventListener('click', (e) => {
                e.stopPropagation(); // Detiene el clic para que no interfiera
                insertMatrix(r, c);  // Inserta la matriz en el workspace
                
                // Ocultar el popup inmediatamente después de insertar
                const popup = document.getElementById('matrix-popup');
                if (popup) popup.style.display = 'none'; 
            });
            
            grid.appendChild(cell);
        }
    }
}

// Función para colorear las celdas de gris
function highlightCells(maxRow, maxCol) {
    const cells = document.querySelectorAll('.matrix-cell');
    cells.forEach(cell => {
        const r = parseInt(cell.dataset.row);
        const c = parseInt(cell.dataset.col);
        // Si la celda está dentro del rango seleccionado, añade la clase 'active'
        if (r <= maxRow && c <= maxCol) {
            cell.classList.add('active');
        } else {
            cell.classList.remove('active');
        }
    });
}

// Ejecutar la inicialización cuando el documento cargue
document.addEventListener('DOMContentLoaded', () => {
    initMatrixGrid();
});

// Lógica de inyección en el Editor Visual
let matrixCounter = 0;

function insertMatrix(rows, cols) {
    const editor = document.getElementById('al-visual-editor');
    const placeholder = document.getElementById('al-placeholder');
    if (placeholder) placeholder.remove();

    const wrapper = document.createElement('div');
    wrapper.className = 'matrix-wrapper';
    wrapper.id = `matrix-${matrixCounter++}`;

    // Controles flotantes (Eliminar)
    const controls = document.createElement('div');
    controls.className = 'matrix-controls';
    controls.innerHTML = `<button class="matrix-btn-action" onclick="this.closest('.matrix-wrapper').remove()" title="Eliminar matriz">🗑️</button>`;

    // Contenedor Grid para las celdas
    const brackets = document.createElement('div');
    brackets.className = 'matrix-brackets al-matrix-data';
    brackets.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    brackets.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
    brackets.dataset.rows = rows;
    brackets.dataset.cols = cols;

    // Generar Inputs
    for (let i = 0; i < rows * cols; i++) {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'matrix-cell-input';
        input.dataset.index = i;
        
        // Navegación por teclado (Flechas)
        input.addEventListener('keydown', (e) => handleMatrixNav(e, input, rows, cols));
        brackets.appendChild(input);
    }

    wrapper.appendChild(controls);
    wrapper.appendChild(brackets);
    
    // NUEVO: Lógica de selección al hacer clic en la matriz
    wrapper.addEventListener('click', (e) => {
        document.querySelectorAll('.matrix-wrapper, .scalar-wrapper').forEach(el => el.classList.remove('selected'));
        wrapper.classList.add('selected');
    });

    editor.appendChild(wrapper);
    
    // Auto-focus en la primera celda
    brackets.querySelector('input').focus();
}

function addMatrixOperator(op) {
    const editor = document.getElementById('al-visual-editor');
    const placeholder = document.getElementById('al-placeholder');
    if (placeholder) placeholder.remove();

    const span = document.createElement('span');
    span.className = 'al-visual-operator al-operator-data';
    span.innerText = op;
    span.onclick = () => span.remove(); // Permite eliminar haciendo clic
    editor.appendChild(span);
}

function handleMatrixNav(e, currentInput, rows, cols) {
    const currentIdx = parseInt(currentInput.dataset.index);
    const container = currentInput.closest('.matrix-brackets');
    const inputs = container.querySelectorAll('.matrix-cell-input');
    let nextIdx = null;

    if (e.key === 'ArrowRight') nextIdx = currentIdx + 1;
    if (e.key === 'ArrowLeft') nextIdx = currentIdx - 1;
    if (e.key === 'ArrowDown') nextIdx = currentIdx + cols;
    if (e.key === 'ArrowUp') nextIdx = currentIdx - cols;

    if (nextIdx !== null && nextIdx >= 0 && nextIdx < inputs.length) {
        e.preventDefault();
        inputs[nextIdx].focus();
    }
}
/* =========================================
   ÁLGEBRA LINEAL - NAVEGACIÓN DE SUB-VISTAS
   ========================================= */
document.addEventListener('DOMContentLoaded', () => {
    const alSelector = document.getElementById('al-view-selector');
    
    if (alSelector) {
        alSelector.addEventListener('change', function(e) {
            // Ocultar todas las sub-vistas
            document.querySelectorAll('.al-sub-view').forEach(view => {
                view.style.display = 'none';
            });
            
            // Mostrar la sub-vista seleccionada
            const targetId = e.target.value;
            const targetView = document.getElementById(targetId);
            if (targetView) {
                targetView.style.display = 'block';
            }
        });
    }
});

// Nueva función para agregar escalares
function addScalar() {
    const editor = document.getElementById('al-visual-editor');
    const placeholder = document.getElementById('al-placeholder');
    if (placeholder) placeholder.remove();

    const wrapper = document.createElement('div');
    wrapper.className = 'scalar-wrapper';
    
    wrapper.innerHTML = `
        <div class="matrix-controls" style="top: -25px;">
            <button class="matrix-btn-action" onclick="this.closest('.scalar-wrapper').remove()" title="Eliminar escalar">🗑️</button>
        </div>
        <input type="number" class="scalar-input" placeholder="n">
    `;

    // Selección al hacer clic
    wrapper.addEventListener('click', (e) => {
        document.querySelectorAll('.matrix-wrapper, .scalar-wrapper').forEach(el => el.classList.remove('selected'));
        wrapper.classList.add('selected');
    });

    editor.appendChild(wrapper);
    wrapper.querySelector('input').focus();
}
// NUEVO: Eventos globales para eliminar con teclado y quitar selección
document.addEventListener('keydown', (e) => {
    if (e.key === 'Delete' || e.key === 'Backspace') {
        const selected = document.querySelector('.matrix-wrapper.selected, .scalar-wrapper.selected');
        
        // Solo elimina si hay algo seleccionado y el usuario NO está escribiendo dentro de un input
        if (selected && document.activeElement.tagName !== 'INPUT') {
            selected.remove();
            
            // Restaura el placeholder si el editor queda vacío
            const editor = document.getElementById('al-visual-editor');
            if (editor && editor.children.length === 0) {
                editor.innerHTML = '<div id="al-placeholder" style="color: #999; font-style: italic;">Selecciona un tamaño arriba para comenzar...</div>';
            }
        }
    }
});

// NUEVO: Quitar selección al hacer clic fuera del editor
document.addEventListener('click', (e) => {
    if (!e.target.closest('.matrix-wrapper') && !e.target.closest('.scalar-wrapper') && !e.target.closest('.al-editor-actions')) {
        document.querySelectorAll('.matrix-wrapper, .scalar-wrapper').forEach(el => el.classList.remove('selected'));
    }
});

/* =========================================
   ÁLGEBRA LINEAL - GRAFICADORA DE SISTEMAS
   ========================================= */

function cambiarDimensionSistema() {
    const dim = document.getElementById('sys-dimension').value;
    const container = document.getElementById('sys-inputs-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (dim === "2") {
        container.innerHTML = `
            <p style="font-size: 0.85rem; color: #666; margin-bottom: 10px;">Ecuación 1: $A_1x + B_1y = C_1$</p>
            <div style="display: flex; gap: 5px; align-items: center; margin-bottom: 8px;">
                <input type="number" id="s2-a1" value="1" style="width: 50px; text-align: center;" placeholder="A1"> x + 
                <input type="number" id="s2-b1" value="1" style="width: 50px; text-align: center;" placeholder="B1"> y = 
                <input type="number" id="s2-c1" value="5" style="width: 60px; text-align: center;" placeholder="C1">
            </div>
            <p style="font-size: 0.85rem; color: #666; margin-bottom: 10px; margin-top: 15px;">Ecuación 2: $A_2x + B_2y = C_2$</p>
            <div style="display: flex; gap: 5px; align-items: center; margin-bottom: 8px;">
                <input type="number" id="s2-a2" value="2" style="width: 50px; text-align: center;" placeholder="A2"> x + 
                <input type="number" id="s2-b2" value="-1" style="width: 50px; text-align: center;" placeholder="B2"> y = 
                <input type="number" id="s2-c2" value="4" style="width: 60px; text-align: center;" placeholder="C2">
            </div>
        `;
    } else {
        container.innerHTML = `
            <p style="font-size: 0.85rem; color: #666; margin-bottom: 10px;">Sistema 3x3 ($Ax + By + Cz = D$)</p>
            <div style="display: flex; gap: 5px; align-items: center; margin-bottom: 6px;">
                <input type="number" id="s3-a1" value="1" style="width: 40px;" placeholder="A1">x+<input type="number" id="s3-b1" value="1" style="width: 40px;" placeholder="B1">y+<input type="number" id="s3-c1" value="1" style="width: 40px;" placeholder="C1">z=<input type="number" id="s3-d1" value="6" style="width: 50px;" placeholder="D1">
            </div>
            <div style="display: flex; gap: 5px; align-items: center; margin-bottom: 6px;">
                <input type="number" id="s3-a2" value="2" style="width: 40px;" placeholder="A2">x+<input type="number" id="s3-b2" value="-1" style="width: 40px;" placeholder="B2">y+<input type="number" id="s3-c2" value="1" style="width: 40px;" placeholder="C2">z=<input type="number" id="s3-d2" value="3" style="width: 50px;" placeholder="D2">
            </div>
            <div style="display: flex; gap: 5px; align-items: center; margin-bottom: 6px;">
                <input type="number" id="s3-a3" value="1" style="width: 40px;" placeholder="A3">x+<input type="number" id="s3-b3" value="2" style="width: 40px;" placeholder="B3">y+<input type="number" id="s3-c3" value="-1" style="width: 40px;" placeholder="C3">z=<input type="number" id="s3-d3" value="2" style="width: 50px;" placeholder="D3">
            </div>
        `;
    }
}

// Inicializar los inputs 2x2 por defecto al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    cambiarDimensionSistema();
});