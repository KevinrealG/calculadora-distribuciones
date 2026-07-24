"""
===========================================================
Probability Calculator
T-Student Distribution
Author : Kevin Sossa
===========================================================
"""

import numpy as np
from scipy.stats import t

from core.continuous_distribution import ContinuousDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SelectField
from ui.helpers import float_value, selected_value
from ui.validation import Validator


@CalculatorFactory.register(
    name="T-Student",
    category="Continuous"
)
class TStudent(ContinuousDistribution):

    def __init__(self):
        super().__init__()
        self.name = "T-Student"
        
        self.df = 10.0
        self.x1 = -1.96
        self.x2 = 1.96
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
                label="Grados de libertad (ν)",
                value=self.df,
                minimum=0.0001,
                step=1.0
            ),
            NumberField(
                id="x1",
                label="Valor inferior (x₁)",
                value=self.x1,
                step=0.01
            ),
            NumberField(
                id="x2",
                label="Valor superior (x₂) [Solo para 'Entre']",
                value=self.x2,
                step=0.01
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
            Validator.numeric(self.df, "ν (grados de libertad)"),
            Validator.positive(self.df, "ν (grados de libertad)"),
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
            self.result = t.cdf(self.x1, self.df)
            prob_label = f"P(X ≤ {self.x1:.3f})"
        elif self.prob_type == "greater":
            self.result = t.sf(self.x1, self.df)
            prob_label = f"P(X ≥ {self.x1:.3f})"
        elif self.prob_type == "between":
            self.result = t.cdf(self.x2, self.df) - t.cdf(self.x1, self.df)
            prob_label = f"P({self.x1:.3f} ≤ X ≤ {self.x2:.3f})"

        # 2. Datos para la curva completa
        # Se ajustan los límites dinámicamente para que la gráfica siempre se vea bien
        limit_x = max(5.0, abs(self.x1) + 1.0)
        if self.prob_type == "between":
            limit_x = max(limit_x, abs(self.x2) + 1.0)
            
        x_min, x_max = -limit_x, limit_x
        x_curve = list(np.linspace(x_min, x_max, 200))
        y_curve = [t.pdf(val, self.df) for val in x_curve]

        # 3. Datos para el área sombreada
        if self.prob_type == "less":
            x_fill = list(np.linspace(x_min, self.x1, 100))
        elif self.prob_type == "greater":
            x_fill = list(np.linspace(self.x1, x_max, 100))
        elif self.prob_type == "between":
            x_fill = list(np.linspace(self.x1, self.x2, 100))
            
        y_fill = [t.pdf(val, self.df) for val in x_fill]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------
        self.chart_data = {
            "type": "continuous",
            "title": f"Distribución T-Student (ν = {self.df})",
            "x": x_curve,
            "y": y_curve,
            "fill_x": x_fill,
            "fill_y": y_fill,
            "x_label": "t",
            "y_label": "Densidad",
            "prob_label": prob_label
        }

        # ------------------------------------------
        # Tabla (Muestra cuantiles representativos)
        # ------------------------------------------
        quantiles = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
        rows = []
        for q in quantiles:
            val = t.ppf(q, self.df)
            rows.append([f"{q*100:.0f}%", val])

        self.table_data = {
            "title": "Tabla de Cuantiles",
            "headers": ["Cuantil", "Valor de t"],
            "rows": rows
        }

        # ------------------------------------------
        # Resumen
        # ------------------------------------------
        self.summary_html = f"""
        <div class="callout primary">
        <h5>Resumen</h5>
        <p>
        ν (grados de libertad) = <b>{self.df}</b><br>
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
                  <mrow>
                    <mi mathvariant="normal">&#x0393;</mi>
                    <mo>(</mo>
                    <mfrac>
                      <mrow>
                        <mi>&#x03BD;</mi>
                        <mo>+</mo>
                        <mn>1</mn>
                      </mrow>
                      <mn>2</mn>
                    </mfrac>
                    <mo>)</mo>
                  </mrow>
                  <mrow>
                    <msqrt>
                      <mrow>
                        <mi>&#x03BD;</mi>
                        <mi>&#x03C0;</mi>
                      </mrow>
                    </msqrt>
                    <mi mathvariant="normal">&#x0393;</mi>
                    <mo>(</mo>
                    <mfrac>
                      <mi>&#x03BD;</mi>
                      <mn>2</mn>
                    </mfrac>
                    <mo>)</mo>
                  </mrow>
                </mfrac>
                <msup>
                  <mrow>
                    <mo>(</mo>
                    <mn>1</mn>
                    <mo>+</mo>
                    <mfrac>
                      <msup>
                        <mi>x</mi>
                        <mn>2</mn>
                      </msup>
                      <mi>&#x03BD;</mi>
                    </mfrac>
                    <mo>)</mo>
                  </mrow>
                  <mrow>
                    <mo>&#x2212;</mo>
                    <mfrac>
                      <mrow>
                        <mi>&#x03BD;</mi>
                        <mo>+</mo>
                        <mn>1</mn>
                      </mrow>
                      <mn>2</mn>
                    </mfrac>
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
        La distribución T-Student modela fenómenos continuos que se agrupan simétricamente
        alrededor de una media, especialmente cuando el tamaño de la muestra es pequeño y la varianza poblacional es desconocida.
        La probabilidad corresponde al área bajo la curva.
        """