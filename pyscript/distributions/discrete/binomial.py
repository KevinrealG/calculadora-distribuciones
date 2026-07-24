"""
===========================================================

Probability Calculator

Binomial Distribution

Author : Kevin Sossa

===========================================================
"""

from scipy.stats import binom

from core.discrete_distribution import DiscreteDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SliderField, SelectField
from ui.helpers import int_value, float_value, selected_value
from ui.validation import binomial


@CalculatorFactory.register(
    name="Binomial",
    category="Discrete"
)
class Binomial(DiscreteDistribution):

    def __init__(self):

        super().__init__()

        self.name = "Binomial"

        self.n = 10
        self.p = 0.50
        self.k = 5
        self.prob_type = "equal"

    # --------------------------------------------------

    def parameters(self):

        return [

            SelectField(
                id="prob_type",
                label="Tipo de Probabilidad",
                options={
                    "equal": "P(X = k)",
                    "less": "P(X ≤ k)",
                    "greater": "P(X ≥ k)",
                    "less_strict": "P(X < k)",
                    "greater_strict": "P(X > k)",
                    #"between": "P(k₁ ≤ X ≤ k₂)"

                },
                value=self.prob_type
            ),

            NumberField(
                id="n",
                label="Número de ensayos (n)",
                value=self.n,
                minimum=1
            ),

            SliderField(
                id="p",
                label="Probabilidad de éxito (p)",
                value=self.p,
                minimum=0,
                maximum=1,
                step=0.01
            ),

            NumberField(
                id="k",
                label="Número de éxitos (k)",
                value=self.k,
                minimum=0
            )

        ]

    # --------------------------------------------------

    def read_parameters(self):
        
        self.prob_type = selected_value("prob_type")
        self.n = int_value("n")
        self.p = float_value("p")
        self.k = int_value("k")

    # --------------------------------------------------

    def validate(self):

        result = binomial(
            self.n,
            self.p,
            self.k
        )

        if not result.valid:

            raise ValueError(result.message)

    # --------------------------------------------------

    def run(self):

        # Calcular resultado principal según el tipo de probabilidad
        if self.prob_type == "equal":
            self.result = binom.pmf(self.k, self.n, self.p)
        elif self.prob_type == "less":
            self.result = binom.cdf(self.k, self.n, self.p)
        elif self.prob_type == "less_strict":
            self.result = binom.cdf(self.k - 1, self.n, self.p) if self.k > 0 else 0.0
        elif self.prob_type == "greater":
            self.result = binom.sf(self.k - 1, self.n, self.p) if self.k > 0 else 1.0
        elif self.prob_type == "greater_strict":
            self.result = binom.sf(self.k, self.n, self.p)
        elif self.prob_type == "between":
            k1 = int_value("k1")
            k2 = int_value("k2")
            self.result = binom.cdf(k2, self.n, self.p) - binom.cdf(k1 - 1, self.n, self.p)


        x = list(range(self.n + 1))

        y = [
            binom.pmf(i, self.n, self.p)
            for i in x
        ]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------

        self.chart_data = {
            "type": "bar",
            "title": "Distribución Binomial",
            "x": x,
            "y": y,
            "x_label": "Número de éxitos",
            "y_label": "P(X=k)",
            "highlight_k": self.k,
            "prob_type": self.prob_type
        }

        # ------------------------------------------
        # Tabla
        # ------------------------------------------

        rows = []
        cumulative = 0

        for i in x:
            p_val = binom.pmf(i, self.n, self.p)
            cumulative += p_val
            rows.append([i, p_val, cumulative])

        self.table_data = {
            "title": "Tabla de Probabilidades",
            "headers": ["k", "P(X=k)", "F(X≤k)"],
            "rows": rows,
            "highlight_k": self.k,
            "prob_type": self.prob_type
        }

        # ------------------------------------------
        # Resumen
        # ------------------------------------------
        
        prob_labels = {
            "equal": "P(X = k)",
            "less": "P(X ≤ k)",
            "greater": "P(X ≥ k)",
            "less_strict": "P(X < k)",
            "greater_strict": "P(X > k)",
            "between": "P(k₁ ≤ X ≤ k₂)"
        }

        mean = binom.mean(self.n, self.p)
        variance = binom.var(self.n, self.p)
        std = variance ** 0.5
        skewness = (1 - 2 * self.p) / (variance ** 0.5)
        mode = int((self.n + 1) * self.p)

        self.summary_html = f"""
        <div class="callout primary">
        <h5>📐 Estadísticas</h5>
        <div class="summary-stats">
        <p><strong>Media (μ) =</strong> <b>{mean:.6f}</b></p>
        <p><strong>Varianza (σ²) =</strong> <b>{variance:.6f}</b></p>
        <p><strong>Desviación estándar (σ) =</strong> <b>{std:.6f}</b></p>
        <p><strong>Coeficiente de asimetría =</strong> <b>{skewness:.6f}</b></p>
        <p><strong>Moda =</strong> <b>{mode}</b></p>
        <p><strong>Cálculo =</strong> <b>{prob_labels.get(self.prob_type)}</b></p>
        </div>
        </div>
        """

        # ------------------------------------------
        # Fórmula (con MathML)
        # ------------------------------------------

        self.formula_html = r"""
        <h4>
        Función de Probabilidad
        </h4>
        <div style="font-size: 1.2em; overflow-x: auto; padding: 10px;">
            <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
              <mrow>
                <mi>P</mi>
                <mo>(</mo>
                <mi>X</mi>
                <mo>=</mo>
                <mi>k</mi>
                <mo>)</mo>
                <mo>=</mo>
                <mrow>
                  <mo>(</mo>
                  <mfrac linethickness="0">
                    <mi>n</mi>
                    <mi>k</mi>
                  </mfrac>
                  <mo>)</mo>
                </mrow>
                <msup>
                  <mi>p</mi>
                  <mi>k</mi>
                </msup>
                <msup>
                  <mrow>
                    <mo>(</mo>
                    <mn>1</mn>
                    <mo>&#x2212;</mo>
                    <mi>p</mi>
                    <mo>)</mo>
                  </mrow>
                  <mrow>
                    <mi>n</mi>
                    <mo>&#x2212;</mo>
                    <mi>k</mi>
                  </mrow>
                </msup>
              </mrow>
              <mtext>
                donde:
                </mtext>
                <mrow>
                    <mi>n</mi>
                    <mo>=</mo>
                    <mtext>número de ensayos</mtext>
                </mrow>
                <mrow>
                    <mi>k</mi>
                    <mo>=</mo>
                    <mtext>número de éxitos</mtext>
                </mrow>
                <mrow>
                    <mi>p</mi>
                    <mo>=</mo>
                    <mtext>probabilidad de éxito</mtext>
                </mrow>


            
            </math>
        </div>
        """

        # ------------------------------------------
        # Descripción
        # ------------------------------------------

        self.description_text = """
        La distribución Binomial modela el número
        de éxitos en una secuencia de n ensayos
        independientes de Bernoulli con una
        probabilidad constante p de éxito.
        """

        # ------------------------------------------
        # Interpretación
        # ------------------------------------------
        
        inter_texts = {
            "equal": f"obtener exactamente <b>{self.k}</b> éxitos",
            "less": f"obtener <b>{self.k}</b> éxitos o menos",
            "greater": f"obtener <b>{self.k}</b> éxitos o más",
            "less_strict": f"obtener menos de <b>{self.k}</b> éxitos",
            "greater_strict": f"obtener más de <b>{self.k}</b> éxitos"
        }

        self.interpretation_text = f"""
        La probabilidad de {inter_texts.get(self.prob_type)}
        en <b>{self.n}</b> ensayos
        es
        <h3>
        {self.result:.6f}
        </h3>
        """