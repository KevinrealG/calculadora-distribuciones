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
