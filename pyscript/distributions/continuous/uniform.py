"""
===========================================================
Probability Calculator
Continuous Uniform Distribution
Author : Kevin Sossa
===========================================================
"""

import numpy as np
from scipy.stats import uniform

from core.continuous_distribution import ContinuousDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SelectField
from ui.helpers import float_value, selected_value
from ui.validation import Validator


@CalculatorFactory.register(
    name="Uniforme Continua",
    category="Continuous"
)
class UniformContinuous(ContinuousDistribution):

    def __init__(self):
        super().__init__()
        self.name = "Uniforme Continua"
        
        self.a = 0.0
        self.b = 10.0
        self.x1 = 2.0
        self.x2 = 7.0
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
                id="a",
                label="Límite inferior (a)",
                value=self.a,
                step=0.1
            ),
            NumberField(
                id="b",
                label="Límite superior (b)",
                value=self.b,
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
        self.a = float_value("a")
        self.b = float_value("b")
        self.x1 = float_value("x1")
        self.x2 = float_value("x2")

    # --------------------------------------------------

    def validate(self):
        validators = [
            Validator.numeric(self.a, "a"),
            Validator.numeric(self.b, "b"),
            Validator.numeric(self.x1, "x₁"),
            Validator.numeric(self.x2, "x₂")
        ]

        for result in validators:
            if not result.valid:
                raise ValueError(result.message)
                
        if self.a >= self.b:
            raise ValueError("El límite inferior (a) debe ser menor que el límite superior (b).")
            
        if self.prob_type == "between" and self.x1 >= self.x2:
            raise ValueError("Para el cálculo entre dos valores, x₁ debe ser menor que x₂.")

    # --------------------------------------------------

    def run(self):
        # Scipy usa loc=a y scale=b-a
        loc = self.a
        scale = self.b - self.a

        # 1. Cálculo de probabilidad
        if self.prob_type == "less":
            self.result = uniform.cdf(self.x1, loc, scale)
            prob_label = f"P(X ≤ {self.x1:.3f})"
        elif self.prob_type == "greater":
            self.result = uniform.sf(self.x1, loc, scale)
            prob_label = f"P(X ≥ {self.x1:.3f})"
        elif self.prob_type == "between":
            self.result = uniform.cdf(self.x2, loc, scale) - uniform.cdf(self.x1, loc, scale)
            prob_label = f"P({self.x1:.3f} ≤ X ≤ {self.x2:.3f})"

        # 2. Datos para la curva completa (añadiendo márgenes para visualizar el rectángulo)
        margin = scale * 0.15
        x_min = self.a - margin
        x_max = self.b + margin
        
        # Generar puntos adicionales en 'a' y 'b' para líneas verticales precisas
        x_curve = sorted(list(np.linspace(x_min, x_max, 300)) + [self.a - 1e-9, self.a, self.b, self.b + 1e-9])
        y_curve = [uniform.pdf(val, loc, scale) for val in x_curve]

        # 3. Datos para el área sombreada
        fill_start = max(self.a, self.x1) if self.prob_type in ["greater", "between"] else self.a
        fill_end = min(self.b, self.x1) if self.prob_type == "less" else (min(self.b, self.x2) if self.prob_type == "between" else self.b)
        
        if fill_start < fill_end:
            x_fill = list(np.linspace(fill_start, fill_end, 100))
            y_fill = [uniform.pdf(val, loc, scale) for val in x_fill]
        else:
            x_fill, y_fill = [], []

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------
        self.chart_data = {
            "type": "continuous",
            "title": "Distribución Uniforme Continua",
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
        quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
        rows = []
        for q in quantiles:
            val = uniform.ppf(q, loc, scale)
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
        a (mínimo) = <b>{self.a}</b><br>
        b (máximo) = <b>{self.b}</b><br>
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
                <mrow>
                  <mo>{</mo>
                  <mtable>
                    <mtr>
                      <mtd>
                        <mfrac>
                          <mn>1</mn>
                          <mrow>
                            <mi>b</mi>
                            <mo>&#x2212;</mo>
                            <mi>a</mi>
                          </mrow>
                        </mfrac>
                      </mtd>
                      <mtd>
                        <mtext>si&nbsp;</mtext>
                        <mi>a</mi>
                        <mo>&#x2264;</mo>
                        <mi>x</mi>
                        <mo>&#x2264;</mo>
                        <mi>b</mi>
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