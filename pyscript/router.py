"""
===========================================================

Probability Calculator

router.py

Controlador principal de la aplicación.

Author : Kevin Sossa

===========================================================
"""

from pyscript import document

from calculator_factory import CalculatorFactory
from ui import panels
from ui import charts
from ui import tables


class Router:

    """
    Coordina la aplicación.

    No realiza cálculos.
    No conoce fórmulas.
    No conoce scipy.

    Únicamente conecta:

        UI
        CalculatorFactory
        Distribuciones
    """

    # --------------------------------------------------

    def __init__(self):

        self.current = None

    # --------------------------------------------------
    # Distribución por defecto
    # --------------------------------------------------

    def load_default(self):

        select = document.getElementById(

            "distribution-select"

        )

        if select.options.length == 0:

            return

        first = select.options.item(0).value

        self.load(

            first

        )

    # --------------------------------------------------
    # Cargar distribución
    # --------------------------------------------------

    def load(

        self,

        distribution_name

    ):

        self.current = CalculatorFactory.create(

            distribution_name

        )

        self.render()

    # --------------------------------------------------
    # Cambio desde el Select
    # --------------------------------------------------

    def change_distribution(

        self,

        event

    ):

        value = event.target.value

        self.load(

            value

        )

    # --------------------------------------------------
    # Renderizar interfaz
    # --------------------------------------------------

    def render(self):

        if self.current is None:

            return

        # --------------------------
        # Panel de parámetros
        # --------------------------

        panels.render(

            self.current.parameters()

        )

        # --------------------------
        # Limpiar resultados
        # --------------------------

        charts.clear()

        tables.clear()

        document.getElementById(

            "summary-panel"

        ).innerHTML = ""

        document.getElementById(

            "formula-panel"

        ).innerHTML = ""

        document.getElementById(

            "description-panel"

        ).innerHTML = ""

        document.getElementById(

            "interpretation-panel"

        ).innerHTML = ""

        document.getElementById(

            "result-panel"

        ).innerHTML = ""

    # --------------------------------------------------
    # Calcular
    # --------------------------------------------------

    def calculate(self, event=None):

        print("1. Entró al botón")

        if self.current is None:
            print("No hay distribución")
            return

        print("2. Leyendo parámetros")
        self.current.read_parameters()

        print("3. Validando")
        self.current.validate()

        print("4. Ejecutando")
        self.current.run()

        print("5. Mostrando")
        self.show()

        print("6. Fin")

    # --------------------------------------------------
    # Mostrar resultado
    # --------------------------------------------------

    def show(self):

        charts.render(

            self.current.chart_data

        )

        tables.render(

            self.current.table_data

        )

        document.getElementById(

            "summary-panel"

        ).innerHTML = self.current.summary_html

        document.getElementById(

            "formula-panel"

        ).innerHTML = self.current.formula_html

        document.getElementById(

            "description-panel"

        ).innerHTML = self.current.description_text

        document.getElementById(

            "interpretation-panel"

        ).innerHTML = self.current.interpretation_text

        document.getElementById(

            "result-panel"

        ).innerHTML = f"""

        <div class="callout success">

            <h4>

                Resultado

            </h4>

            <h3>

                {self.current.result:.6f}

            </h3>

        </div>

        """

    # --------------------------------------------------
    # Reiniciar
    # --------------------------------------------------

    def reset(self):

        self.render()

    # --------------------------------------------------
    # Distribución actual
    # --------------------------------------------------

    def current_distribution(self):

        return self.current