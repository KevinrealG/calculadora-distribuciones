"""
===========================================================
Probability Calculator
Chi-Square Distribution
Author : Kevin Sossa
===========================================================
"""

import numpy as np
from scipy.stats import chi2

from core.continuous_distribution import ContinuousDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SelectField
from ui.helpers import float_value, selected_value
from ui.validation import Validator


@CalculatorFactory.register(
    name="Chi Cuadrado",
    category="Continuous"
)
class ChiSquare(ContinuousDistribution):

    def __init__(self):
        super().__init__()
        self.name = "Chi Cuadrado"
        
        self.df = 5.0
        self.x1 = 2.0
        self.x2 = 10.0
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
                id="df",
                label="Grados de libertad (k)",
                value=self.df,
                minimum=0.0001,
                step=1.0
            ),
            NumberField(
                id="x1",
                label="Valor inferior (x₁)",
                value=self.x1,
                step=0.1,
                minimum=0.0
            ),
            NumberField(
                id="x2",
                label="Valor superior (x₂) [Solo para 'Entre']",
                value=self.x2,
                step=0.1,
                minimum=0.0
            )
        ]

    # --------------------------------------------------

    def read_parameters(self):
        self.prob_type = selected_value("prob_type")
        self.df = float_value("df")
        self.x1 = float_value("x1")
        self.x2 = float_value("x2")

    # --------------------------------------------------

    def validate(self):
        validators = [
            Validator.numeric(self.df, "k (grados de libertad)"),
            Validator.positive(self.df, "k (grados de libertad)"),
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
            self.result = chi2.cdf(self.x1, self.df)
            prob_label = f"P(X ≤ {self.x1:.3f})"
        elif self.prob_type == "greater":
            self.result = chi2.sf(self.x1, self.df)
            prob_label = f"P(X ≥ {self.x1:.3f})"
        elif self.prob_type == "between":
            self.result = chi2.cdf(self.x2, self.df) - chi2.cdf(self.x1, self.df)
            prob_label = f"P({self.x1:.3f} ≤ X ≤ {self.x2:.3f})"

        # 2. Datos para la curva completa
        # El límite superior del gráfico se ajusta dinámicamente según la probabilidad
        x_min = 0.0
        limit_x = max(chi2.ppf(0.99, self.df), self.x1 + 2.0)
        if self.prob_type == "between":
            limit_x = max(limit_x, self.x2 + 2.0)
            
        x_max = limit_x
        x_curve = list(np.linspace(x_min, x_max, 200))
        y_curve = [chi2.pdf(val, self.df) for val in x_curve]

        # 3. Datos para el área sombreada
        if self.prob_type == "less":
            fill_end = self.x1
            x_fill = list(np.linspace(x_min, fill_end, 100))
        elif self.prob_type == "greater":
            fill_start = self.x1
            x_fill = list(np.linspace(fill_start, x_max, 100))
        elif self.prob_type == "between":
            x_fill = list(np.linspace(self.x1, self.x2, 100))
            
        y_fill = [chi2.pdf(val, self.df) for val in x_fill]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------
        self.chart_data = {
            "type": "continuous",
            "title": f"Distribución Chi Cuadrado (k = {self.df})",
            "x": x_curve,
            "y": y_curve,
            "fill_x": x_fill,
            "fill_y": y_fill,
            "x_label": "x",
            "y_label": "Densidad f(x)",
            "prob_label": prob_label
        }

        # ------------------------------------------
        # Tabla (Muestra cuantiles representativos)
        # ------------------------------------------
        quantiles = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
        rows = []
        for q in quantiles:
            val = chi2.ppf(q, self.df)
            rows.append([f"{q*100:.0f}%", val])

        self.table_data = {
            "title": "Tabla de Cuantiles",
            "headers": ["Cuantil", "Valor de x"],
            "rows": rows
        }

        # ------------------------------------------
        # Resumen
        # ------------------------------------------
        self.summary_html = f"""
        <div class="callout primary">
        <h5>Resumen</h5>
        <p>
        k (grados de libertad) = <b>{self.df}</b><br>
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
                <mo>;</mo>
                <mi>k</mi>
                <mo>)</mo>
                <mo>=</mo>
                <mfrac>
                  <mrow>
                    <msup>
                      <mi>x</mi>
                      <mrow>
                        <mfrac>
                          <mi>k</mi>
                          <mn>2</mn>
                        </mfrac>
                        <mo>&#x2212;</mo>
                        <mn>1</mn>
                      </mrow>
                    </msup>
                    <msup>
                      <mi>e</mi>
                      <mrow>
                        <mo>&#x2212;</mo>
                        <mfrac>
                          <mi>x</mi>
                          <mn>2</mn>
                        </mfrac>
                      </mrow>
                    </msup>
                  </mrow>
                  <mrow>
                    <msup>
                      <mn>2</mn>
                      <mfrac>
                        <mi>k</mi>
                        <mn>2</mn>
                      </mfrac>
                    </msup>
                    <mi mathvariant="normal">&#x0393;</mi>
                    <mo>(</mo>
                    <mfrac>
                      <mi>k</mi>
                      <mn>2</mn>
                    </mfrac>
                    <mo>)</mo>
                  </mrow>
                </mfrac>
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
        La distribución Chi-Cuadrado modela fenómenos continuos que se agrupan simétricamente
        alrededor de una media, especialmente cuando el tamaño de la muestra es pequeño y la varianza poblacional es desconocida.
        La probabilidad corresponde al área bajo la curva.
        """