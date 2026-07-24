"""
===========================================================
Probability Calculator
F-Fisher Distribution
Author : Kevin Sossa
===========================================================
"""

import numpy as np
from scipy.stats import f

from core.continuous_distribution import ContinuousDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SelectField
from ui.helpers import float_value, selected_value
from ui.validation import Validator


@CalculatorFactory.register(
    name="F de Fisher",
    category="Continuous"
)
class Fisher(ContinuousDistribution):

    def __init__(self):
        super().__init__()
        self.name = "F de Fisher"
        
        self.df1 = 5.0
        self.df2 = 5.0
        self.x1 = 2.0
        self.x2 = 5.0
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
                id="df1",
                label="Grados de libertad numerador (d₁)",
                value=self.df1,
                minimum=0.0001,
                step=1.0
            ),
            NumberField(
                id="df2",
                label="Grados de libertad denominador (d₂)",
                value=self.df2,
                minimum=0.0001,
                step=1.0
            ),
            NumberField(
                id="x1",
                label="Valor inferior (x₁)",
                value=self.x1,
                minimum=0.0,
                step=0.1
            ),
            NumberField(
                id="x2",
                label="Valor superior (x₂) [Solo para 'Entre']",
                value=self.x2,
                minimum=0.0,
                step=0.1
            )
        ]

    # --------------------------------------------------

    def read_parameters(self):
        self.prob_type = selected_value("prob_type")
        self.df1 = float_value("df1")
        self.df2 = float_value("df2")
        self.x1 = float_value("x1")
        self.x2 = float_value("x2")

    # --------------------------------------------------

    def validate(self):
        validators = [
            Validator.numeric(self.df1, "d₁ (grados numerador)"),
            Validator.positive(self.df1, "d₁ (grados numerador)"),
            Validator.numeric(self.df2, "d₂ (grados denominador)"),
            Validator.positive(self.df2, "d₂ (grados denominador)"),
            Validator.numeric(self.x1, "x₁"),
            Validator.numeric(self.x2, "x₂")
        ]

        for result in validators:
            if not result.valid:
                raise ValueError(result.message)
                
        if self.x1 < 0:
            raise ValueError("El valor de x₁ no puede ser negativo en la distribución F.")
            
        if self.prob_type == "between":
            if self.x2 < 0:
                raise ValueError("El valor de x₂ no puede ser negativo.")
            if self.x1 >= self.x2:
                raise ValueError("Para el cálculo entre dos valores, x₁ debe ser menor que x₂.")

    # --------------------------------------------------

    def run(self):
        # 1. Cálculo de probabilidad
        if self.prob_type == "less":
            self.result = f.cdf(self.x1, self.df1, self.df2)
            prob_label = f"P(X ≤ {self.x1:.3f})"
        elif self.prob_type == "greater":
            self.result = f.sf(self.x1, self.df1, self.df2)
            prob_label = f"P(X ≥ {self.x1:.3f})"
        elif self.prob_type == "between":
            self.result = f.cdf(self.x2, self.df1, self.df2) - f.cdf(self.x1, self.df1, self.df2)
            prob_label = f"P({self.x1:.3f} ≤ X ≤ {self.x2:.3f})"

        # 2. Datos para la curva completa
        # Limitamos el cuantil superior para evitar gráficos distorsionados en df pequeñas
        upper_q = f.ppf(0.95, self.df1, self.df2)
        if np.isinf(upper_q) or np.isnan(upper_q):
            upper_q = 10.0
            
        x_min = 0.0
        limit_x = max(upper_q * 1.5, self.x1 + 1.0)
        if self.prob_type == "between":
            limit_x = max(limit_x, self.x2 + 1.0)
            
        x_max = limit_x
        # Prevenir singularidad exacta en 0 si df1 < 2
        x_start = 1e-4 if self.df1 < 2 else 0.0
        x_curve = list(np.linspace(x_start, x_max, 250))
        y_curve = [f.pdf(val, self.df1, self.df2) for val in x_curve]

        # 3. Datos para el área sombreada
        if self.prob_type == "less":
            x_fill = list(np.linspace(x_start, self.x1, 100))
        elif self.prob_type == "greater":
            x_fill = list(np.linspace(self.x1, x_max, 100))
        elif self.prob_type == "between":
            x_fill = list(np.linspace(self.x1, self.x2, 100))
            
        y_fill = [f.pdf(val, self.df1, self.df2) for val in x_fill]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------
        self.chart_data = {
            "type": "continuous",
            "title": f"Distribución F-Fisher (d₁={self.df1}, d₂={self.df2})",
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
            val = f.ppf(q, self.df1, self.df2)
            # Manejar posibles valores infinitos si los hay
            val_str = f"{val:.4f}" if not np.isinf(val) else "∞"
            rows.append([f"{q*100:.0f}%", val_str])

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
        d₁ (grados numerador) = <b>{self.df1}</b><br>
        d₂ (grados denominador) = <b>{self.df2}</b><br>
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
                <msub>
                  <mi>d</mi>
                  <mn>1</mn>
                </msub>
                <mo>,</mo>
                <msub>
                  <mi>d</mi>
                  <mn>2</mn>
                </msub>
                <mo>)</mo>
                <mo>=</mo>
                <mfrac>
                  <mrow>
                    <mi mathvariant="normal">&#x0393;</mi>
                    <mo>(</mo>
                    <mfrac>
                      <mrow>
                        <msub>
                          <mi>d</mi>
                          <mn>1</mn>
                        </msub>
                        <mo>+</mo>
                        <msub>
                          <mi>d</mi>
                          <mn>2</mn>
                        </msub>
                      </mrow>
                      <mn>2</mn>
                    </mfrac>
                    <mo>)</mo>
                  </mrow>
                  <mrow>
                    <mi mathvariant="normal">&#x0393;</mi>
                    <mo>(</mo>
                    <mfrac>
                      <msub>
                        <mi>d</mi>
                        <mn>1</mn>
                      </msub>
                      <mn>2</mn>
                    </mfrac>
                    <mo>)</mo>
                    <mi mathvariant="normal">&#x0393;</mi>
                    <mo>(</mo>
                    <mfrac>
                      <msub>
                        <mi>d</mi>
                        <mn>2</mn>
                      </msub>
                      <mn>2</mn>
                    </mfrac>
                    <mo>)</mo>
                  </mrow>
                </mfrac>
                <msup>
                  <mrow>
                    <mo>(</mo>
                    <mfrac>
                      <msub>
                        <mi>d</mi>
                        <mn>1</mn>
                      </msub>
                      <msub>
                        <mi>d</mi>
                        <mn>2</mn>
                      </msub>
                    </mfrac>
                    <mo>)</mo>
                  </mrow>
                  <mrow>
                    <mfrac>
                      <msub>
                        <mi>d</mi>
                        <mn>1</mn>
                      </msub>
                      <mn>2</mn>
                    </mfrac>
                  </mrow>
                </msup>
                <msup>
                  <mi>x</mi>
                  <mrow>
                    <mfrac>
                      <msub>
                        <mi>d</mi>
                        <mn>1</mn>
                      </msub>
                      <mn>2</mn>
                    </mfrac>
                    <mo>&#x2212;</mo>
                    <mn>1</mn>
                  </mrow>
                </msup>
                <msup>
                  <mrow>
                    <mo>(</mo>
                    <mn>1</mn>
                    <mo>+</mo>
                    <mfrac>
                      <msub>
                        <mi>d</mi>
                        <mn>1</mn>
                      </msub>
                      <msub>
                        <mi>d</mi>
                        <mn>2</mn>
                      </msub>
                    </mfrac>
                    <mi>x</mi>
                    <mo>)</mo>
                  </mrow>
                  <mrow>
                    <mo>&#x2212;</mo>
                    <mfrac>
                      <mrow>
                        <msub>
                          <mi>d</mi>
                          <mn>1</mn>
                        </msub>
                        <mo>+</mo>
                        <msub>
                          <mi>d</mi>
                          <mn>2</mn>
                        </msub>
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
        La distribución F-Fisher modela fenómenos continuos que se agrupan simétricamente
        alrededor de una media, especialmente cuando se comparan varianzas de dos poblaciones. La probabilidad corresponde al área bajo la curva.
        """