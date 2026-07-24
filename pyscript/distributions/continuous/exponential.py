"""
===========================================================
Probability Calculator
Exponential Distribution
Author : Kevin Sossa
===========================================================
"""

import numpy as np
from scipy.stats import expon

from core.continuous_distribution import ContinuousDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SelectField
from ui.helpers import float_value, selected_value
from ui.validation import Validator


@CalculatorFactory.register(
    name="Exponencial",
    category="Continuous"
)
class Exponential(ContinuousDistribution):

    def __init__(self):
        super().__init__()
        self.name = "Exponencial"
        
        self.lam = 1.0  # Tasa (lambda)
        self.x1 = 1.0
        self.x2 = 3.0
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
                id="lam",
                label="Tasa (λ)",
                value=self.lam,
                minimum=0.0001,
                step=0.1
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
        self.lam = float_value("lam")
        self.x1 = float_value("x1")
        self.x2 = float_value("x2")

    # --------------------------------------------------

    def validate(self):
        validators = [
            Validator.numeric(self.lam, "λ (tasa)"),
            Validator.positive(self.lam, "λ (tasa)"),
            Validator.numeric(self.x1, "x₁"),
            Validator.numeric(self.x2, "x₂")
        ]

        for result in validators:
            if not result.valid:
                raise ValueError(result.message)
                
        if self.x1 < 0:
            raise ValueError("El valor de x₁ no puede ser negativo.")
            
        if self.prob_type == "between":
            if self.x2 < 0:
                raise ValueError("El valor de x₂ no puede ser negativo.")
            if self.x1 >= self.x2:
                raise ValueError("Para el cálculo entre dos valores, x₁ debe ser menor que x₂.")

    # --------------------------------------------------

    def run(self):
        # scipy.stats.expon usa scale = 1 / lambda
        scale = 1.0 / self.lam

        # 1. Cálculo de probabilidad
        if self.prob_type == "less":
            self.result = expon.cdf(self.x1, scale=scale)
            prob_label = f"P(X ≤ {self.x1:.3f})"
        elif self.prob_type == "greater":
            self.result = expon.sf(self.x1, scale=scale)
            prob_label = f"P(X ≥ {self.x1:.3f})"
        elif self.prob_type == "between":
            self.result = expon.cdf(self.x2, scale=scale) - expon.cdf(self.x1, scale=scale)
            prob_label = f"P({self.x1:.3f} ≤ X ≤ {self.x2:.3f})"

        # 2. Datos para la curva completa
        x_min = 0.0
        limit_x = max(expon.ppf(0.99, scale=scale), self.x1 + 1.0)
        if self.prob_type == "between":
            limit_x = max(limit_x, self.x2 + 1.0)
            
        x_max = limit_x
        x_curve = list(np.linspace(x_min, x_max, 200))
        y_curve = [expon.pdf(val, scale=scale) for val in x_curve]

        # 3. Datos para el área sombreada
        if self.prob_type == "less":
            x_fill = list(np.linspace(x_min, self.x1, 100))
        elif self.prob_type == "greater":
            x_fill = list(np.linspace(self.x1, x_max, 100))
        elif self.prob_type == "between":
            x_fill = list(np.linspace(self.x1, self.x2, 100))
            
        y_fill = [expon.pdf(val, scale=scale) for val in x_fill]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------
        self.chart_data = {
            "type": "continuous",
            "title": f"Distribución Exponencial (λ = {self.lam})",
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
            val = expon.ppf(q, scale=scale)
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
        λ (tasa) = <b>{self.lam}</b><br>
        Media (1/λ) = <b>{scale:.4f}</b><br>
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
                <mi>&#x03BB;</mi>
                <mo>)</mo>
                <mo>=</mo>
                <mrow>
                  <mo>{</mo>
                  <mtable>
                    <mtr>
                      <mtd>
                        <mi>&#x03BB;</mi>
                        <msup>
                          <mi>e</mi>
                          <mrow>
                            <mo>&#x2212;</mo>
                            <mi>&#x03BB;</mi>
                            <mi>x</mi>
                          </mrow>
                        </msup>
                      </mtd>
                      <mtd>
                        <mtext>si&nbsp;</mtext>
                        <mi>x</mi>
                        <mo>&#x2265;</mo>
                        <mn>0</mn>
                      </mtd>
                    </mtr>
                    <mtr>
                      <mtd>
                        <mn>0</mn>
                      </mtd>
                      <mtd>
                        <mtext>en otro caso</mtext>
                      </mtd>
                    </mtr>
                  </mtable>
                </mrow>

              </mrow>
              <mrow>
               <mtext>Donde:</mtext>
                <mtext>&#x03BB; = Tasa (lambda)</mtext>
                <mtext>&nbsp;&nbsp;&nbsp;&nbsp;x = Variable aleatoria</mtext>
                
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
        La distribución Exponencial modela fenómenos continuos que ocurren de manera aleatoria a lo largo del tiempo o espacio,
        especialmente en procesos de espera o tiempo entre eventos. La probabilidad corresponde al área bajo la curva de densidad.
        """