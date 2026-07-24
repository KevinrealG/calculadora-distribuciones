"""
===========================================================

Probability Calculator

Geometric Distribution

Author : Kevin Sossa

===========================================================
"""

from scipy.stats import geom

from core.discrete_distribution import DiscreteDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SliderField
from ui.helpers import int_value, float_value
from ui.validation import geometric as geometric_validation


@CalculatorFactory.register(
    name="Geometric",
    category="Discrete"
)
class Geometric(DiscreteDistribution):

    def __init__(self):

        super().__init__()

        self.name = "Geometric"

        self.p = 0.30
        self.k = 3

    # --------------------------------------------------

    def parameters(self):

        return [

            SliderField(
                id="p",
                label="Probabilidad de éxito (p)",
                value=self.p,
                minimum=0.001,
                maximum=1,
                step=0.01
            ),

            NumberField(
                id="k",
                label="Ensayo del primer éxito (k)",
                value=self.k,
                minimum=1
            )

        ]

    # --------------------------------------------------

    def read_parameters(self):

        self.p = float_value("p")
        self.k = int_value("k")

    # --------------------------------------------------

    def validate(self):

        result = geometric_validation(

            self.p,
            self.k

        )

        if not result.valid:

            raise ValueError(result.message)

    # --------------------------------------------------

    def run(self):

        # ------------------------------------------
        # Resultado principal
        # ------------------------------------------

        self.result = geom.pmf(

            self.k,

            self.p

        )

        # ------------------------------------------
        # Rango para gráfico
        # ------------------------------------------

        xmax = max(

            self.k + 5,

            int(10 / self.p)

        )

        xmax = min(xmax, 50)

        x = list(

            range(

                1,

                xmax + 1

            )

        )

        y = [

            geom.pmf(i, self.p)

            for i in x

        ]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------

        self.chart_data = {

            "type": "bar",

            "title": "Distribución Geométrica",

            "x": x,

            "y": y,

            "x_label": "Ensayo del primer éxito",

            "y_label": "P(X = k)",

            "highlight_k": self.k

        }

        # ------------------------------------------
        # Tabla
        # ------------------------------------------

        rows = []

        cumulative = 0

        for i in x:

            probability = geom.pmf(

                i,

                self.p

            )

            cumulative += probability

            rows.append(

                [

                    i,

                    probability,

                    cumulative

                ]

            )

        self.table_data = {

            "title": "Tabla de Probabilidades",

            "headers": [

                "k",

                "P(X=k)",

                "F(X≤k)"

            ],

            "rows": rows,

            "highlight_k": self.k

        }

        # ------------------------------------------
        # Resumen
        # ------------------------------------------

        mean = geom.mean(self.p)
        variance = geom.var(self.p)
        std = variance ** 0.5
        skewness = (2 - self.p) / ((1 - self.p) ** 0.5)
        mode = 1

        self.summary_html = f"""

        <div class="callout primary">

            <h5>📐 Estadísticas</h5>

            <div class="summary-stats">

            <p><strong>Media (μ) =</strong> <b>{mean:.6f}</b></p>
            <p><strong>Varianza (σ²) =</strong> <b>{variance:.6f}</b></p>
            <p><strong>Desviación estándar (σ) =</strong> <b>{std:.6f}</b></p>
            <p><strong>Coeficiente de asimetría =</strong> <b>{skewness:.6f}</b></p>
            <p><strong>Moda =</strong> <b>{mode}</b></p>
            <p><strong>Cálculo =</strong> <b>{self.prob_type}</b></p>

            </div>

        </div>

        """

        # ------------------------------------------
        # Fórmula
        # ------------------------------------------

        self.formula_html = r"""

        <h4>

        Función de Probabilidad

        </h4>
        <div style="font-size: 1.25rem; overflow-x: auto; padding: 10px 0;">

        <math xmlns="http://www.w3.org/1998/Math/MathML">
        <mi>P</mi>
        <mo>(</mo>
        <mi>X</mi>
        <mo>=</mo>
        <mi>k</mi>
        <mo>)</mo>
        <mo>=</mo>
        <msup>
            <mrow>
            <mo>(</mo>
            <mn>1</mn>
            <mo>-</mo>
            <mi>p</mi>
            <mo>)</mo>
            </mrow>
            <mrow>
            <mi>k</mi>
            <mo>-</mo>
            <mn>1</mn>
            </mrow>
        </msup>
        <mi>p</mi>
        </math>
        </div>

        """

        # ------------------------------------------
        # Descripción
        # ------------------------------------------

        self.description_text = """

        La distribución Geométrica modela el número
        de ensayos necesarios hasta obtener el primer
        éxito en una secuencia de ensayos de Bernoulli
        independientes con probabilidad constante de
        éxito p.

        """

        # ------------------------------------------
        # Interpretación
        # ------------------------------------------

        self.interpretation_text = f"""

        La probabilidad de que el primer éxito ocurra
        exactamente en el ensayo

        <b>{self.k}</b>

        con una probabilidad de éxito de

        <b>{self.p:.3f}</b>

        es

        <h3>

        {self.result:.6f}

        </h3>

        """