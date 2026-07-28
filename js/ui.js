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
function toggleMatrixPopup() {
    const popup = document.getElementById('matrixPopup');
    popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
    if(popup.style.display === 'block' && document.getElementById('matrixGrid').children.length === 0) {
        initMatrixGrid();
    }
}

function initMatrixGrid() {
    const grid = document.getElementById('matrixGrid');
    const sizeTxt = document.getElementById('matrixSizeTxt');
    const cols = 10;
    const rows = 10;

    for (let r = 1; r <= rows; r++) {
        for (let c = 1; c <= cols; c++) {
            const cell = document.createElement('div');
            cell.className = 'matrix-cell';
            cell.dataset.row = r;
            cell.dataset.col = c;
            
            cell.addEventListener('mouseover', function() {
                highlightCells(r, c);
                sizeTxt.textContent = `Tamaño: ${r}x${c}`;
            });
            
            cell.addEventListener('click', function() {
                console.log(`Matriz seleccionada: ${r}x${c}`);
                // Futura integración con Python/PyScript
                toggleMatrixPopup(); 
            });

            grid.appendChild(cell);
        }
    }
}

function highlightCells(maxRow, maxCol) {
    const cells = document.querySelectorAll('.matrix-cell');
    cells.forEach(cell => {
        const r = parseInt(cell.dataset.row);
        const c = parseInt(cell.dataset.col);
        if (r <= maxRow && c <= maxCol) {
            cell.classList.add('hovered');
        } else {
            cell.classList.remove('hovered');
        }
    });
}