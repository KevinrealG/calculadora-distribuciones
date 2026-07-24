"""
===========================================================
Probability Calculator
Normal Distribution
Author : Kevin Sossa
===========================================================
"""

import numpy as np
from scipy.stats import norm

from core.continuous_distribution import ContinuousDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SelectField
from ui.helpers import float_value, selected_value
from ui.validation import Validator


@CalculatorFactory.register(
    name="Normal",
    category="Continuous"
)
class Normal(ContinuousDistribution):

    def __init__(self):
        super().__init__()
        self.name = "Normal"
        self.mu = 100.0
        self.sigma = 15.0
        self.x1 = 85.0
        self.x2 = 115.0
        self.prob_type = "between"

    # --------------------------------------------------

    def parameters(self):
        return [
            SelectField(
                id="prob_type",
                label="Tipo de Probabilidad",
                options={
                    "less": "P(X ≤ x₁)",
                    "greater": "P(X ≥ x₁)",
                    "between": "P(x₁ ≤ X ≤ x₂)"
                },
                value=self.prob_type
            ),
            NumberField(
                id="mu",
                label="Media (μ)",
                value=self.mu,
                step=0.1
            ),
            NumberField(
                id="sigma",
                label="Desviación Estándar (σ)",
                value=self.sigma,
                minimum=0.0001,
                step=0.1
            ),
            NumberField(
                id="x1",
                label="Valor inferior (x₁)",
                value=self.x1,
                step=0.1
            ),
            NumberField(
                id="x2",
                label="Valor superior (x₂) [Solo para 'Entre']",
                value=self.x2,
                step=0.1
            )
        ]

    # --------------------------------------------------

    def read_parameters(self):
        self.prob_type = selected_value("prob_type")
        self.mu = float_value("mu")
        self.sigma = float_value("sigma")
        self.x1 = float_value("x1")
        self.x2 = float_value("x2")

    # --------------------------------------------------

    def validate(self):
        validators = [
            Validator.numeric(self.mu, "μ"),
            Validator.numeric(self.sigma, "σ"), Validator.positive(self.sigma, "σ"),
            Validator.numeric(self.x1, "x₁"),
            Validator.numeric(self.x2, "x₂")
        ]

        for result in validators:
            if not result.valid:
                raise ValueError(result.message)
                
        if self.prob_type == "between" and self.x1 >= self.x2:
            raise ValueError("Para el cálculo entre dos valores, x₁ debe ser menor que x₂.")

    # --------------------------------------------------

    def run(self):
        # 1. Cálculo de probabilidad
        if self.prob_type == "less":
            self.result = norm.cdf(self.x1, self.mu, self.sigma)
            prob_label = f"P(X ≤ {self.x1:.2f})"
        elif self.prob_type == "greater":
            self.result = norm.sf(self.x1, self.mu, self.sigma)
            prob_label = f"P(X ≥ {self.x1:.2f})"
        elif self.prob_type == "between":
            self.result = norm.cdf(self.x2, self.mu, self.sigma) - norm.cdf(self.x1, self.mu, self.sigma)
            prob_label = f"P({self.x1:.2f} ≤ X ≤ {self.x2:.2f})"

        # 2. Datos para la curva completa (± 4 desviaciones estándar)
        x_min = self.mu - 4 * self.sigma
        x_max = self.mu + 4 * self.sigma
        x_curve = list(np.linspace(x_min, x_max, 200))
        y_curve = [norm.pdf(val, self.mu, self.sigma) for val in x_curve]

        # 3. Datos para el área sombreada
        if self.prob_type == "less":
            x_fill = list(np.linspace(x_min, self.x1, 100))
        elif self.prob_type == "greater":
            x_fill = list(np.linspace(self.x1, x_max, 100))
        elif self.prob_type == "between":
            x_fill = list(np.linspace(self.x1, self.x2, 100))
            
        y_fill = [norm.pdf(val, self.mu, self.sigma) for val in x_fill]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------
        self.chart_data = {
            "type": "continuous",
            "title": f"Distribución Normal: μ = {self.mu}, σ = {self.sigma}",
            "x": x_curve,
            "y": y_curve,
            "fill_x": x_fill,
            "fill_y": y_fill,
            "x_label": "X",
            "y_label": "Densidad",
            "prob_label": prob_label
        }

        # ------------------------------------------
        # Tabla (Muestra cuantiles representativos)
        # ------------------------------------------
        quantiles = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
        rows = []
        for q in quantiles:
            val = norm.ppf(q, self.mu, self.sigma)
            rows.append([f"{q*100:.0f}%", val])

        self.table_data = {
            "title": "Tabla de Cuantiles",
            "headers": ["Cuantil", "Valor de X"],
            "rows": rows
        }

        # ------------------------------------------
        # Resumen
        # ------------------------------------------
        self.summary_html = f"""
        <div class="callout primary">
        <h5>Resumen</h5>
        <p>
        μ (media) = <b>{self.mu}</b><br>
        σ (desv. est.) = <b>{self.sigma}</b><br>
        Cálculo = <b>{prob_label}</b>
        </p>
        </div>
        """

        # ------------------------------------------
        # Fórmula
        # ------------------------------------------
        self.formula_html = r"""
        <h4>Función de Densidad de Probabilidad</h4>
        <div style="font-size: 1.2em; overflow-x: auto; padding: 10px;">
            <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
              <mrow>
                <mi>f</mi>
                <mo>(</mo>
                <mi>x</mi>
                <mo>)</mo>
                <mo>=</mo>
                <mfrac>
                  <mn>1</mn>
                  <mrow>
                    <mi>&#x03C3;</mi>
                    <msqrt>
                      <mrow>
                        <mn>2</mn>
                        <mi>&#x03C0;</mi>
                      </mrow>
                    </msqrt>
                  </mrow>
                </mfrac>
                <msup>
                  <mi>e</mi>
                  <mrow>
                    <mo>&#x2212;</mo>
                    <mfrac>
                      <mn>1</mn>
                      <mn>2</mn>
                    </mfrac>
                    <msup>
                      <mrow>
                        <mo>(</mo>
                        <mfrac>
                          <mrow>
                            <mi>x</mi>
                            <mo>&#x2212;</mo>
                            <mi>&#x03BC;</mi>
                          </mrow>
                          <mi>&#x03C3;</mi>
                        </mfrac>
                        <mo>)</mo>
                      </mrow>
                      <mn>2</mn>
                    </msup>
                  </mrow>
                </msup>
              </mrow>
            </math>
        </div>
        """

        # ------------------------------------------
        # Interpretación
        # ------------------------------------------
        if self.prob_type == 'between':
            inter_text = f"entre <b>{self.x1}</b> y <b>{self.x2}</b>"
        else:
            inter_text = f"{'menor o igual a' if self.prob_type == 'less' else 'mayor o igual a'} <b>{self.x1}</b>"

        self.interpretation_text = f"""
        La probabilidad de que la variable asuma un valor {inter_text} es
        <h3>{self.result:.6f}</h3>
        """
        self.description_text = """
        La distribución Normal modela fenómenos continuos que se agrupan simétricamente 
        alrededor de una media. La probabilidad corresponde al área bajo la curva.
        """