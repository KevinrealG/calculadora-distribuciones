"""
===========================================================
Probability Calculator
Discrete Uniform Distribution
Author : Kevin Sossa
===========================================================
"""

from scipy.stats import randint

from core.discrete_distribution import DiscreteDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SelectField
from ui.helpers import int_value, selected_value
from ui.validation import Validator


@CalculatorFactory.register(
    name="Uniforme Discreta",
    category="Discrete"
)
class UniformDiscrete(DiscreteDistribution):

    def __init__(self):
        super().__init__()
        self.name = "Uniforme Discreta"
        
        self.a = 1  
        self.b = 6  
        self.x1 = 2  
        self.x2 = 4  
        self.prob_type = "between"

    # --------------------------------------------------

    def parameters(self):
        return [
            SelectField(
                id="prob_type",
                label="Tipo de Probabilidad",
                options={
                    "equal": "P(X = x₁)",
                    "less": "P(X ≤ x₁)",
                    "greater": "P(X ≥ x₁)",
                    "less_strict": "P(X < x₁)",
                    "greater_strict": "P(X > x₁)",
                    "between": "P(x₁ ≤ X ≤ x₂)"
                },
                value=self.prob_type
            ),
            NumberField(
                id="a",
                label="Límite inferior (a)",
                value=self.a
            ),
            NumberField(
                id="b",
                label="Límite superior (b)",
                value=self.b
            ),
            NumberField(
                id="x1",
                label="Valor (x₁)",
                value=self.x1
            ),
            NumberField(
                id="x2",
                label="Valor superior (x₂) [Solo 'Entre']",
                value=self.x2
            )
        ]

    # --------------------------------------------------

    def read_parameters(self):
        self.prob_type = selected_value("prob_type")
        self.a = int_value("a")
        self.b = int_value("b")
        self.x1 = int_value("x1")
        self.x2 = int_value("x2")

    # --------------------------------------------------

    def validate(self):
        validators = [
            Validator.integer(self.a, "a"),
            Validator.integer(self.b, "b"),
            Validator.integer(self.x1, "x₁"),
            Validator.integer(self.x2, "x₂")
        ]

        for result in validators:
            if not result.valid:
                raise ValueError(result.message)
                
        if self.a > self.b:
            raise ValueError("El límite inferior (a) no puede ser mayor que el superior (b).")
            
        if self.prob_type == "between" and self.x1 >= self.x2:
            raise ValueError("Para el cálculo entre dos valores, x₁ debe ser menor que x₂.")

    # --------------------------------------------------

    def run(self):
        high = self.b + 1
        
        if self.prob_type == "equal":
            self.result = randint.pmf(self.x1, self.a, high)
        elif self.prob_type == "less":
            self.result = randint.cdf(self.x1, self.a, high)
        elif self.prob_type == "less_strict":
            self.result = randint.cdf(self.x1 - 1, self.a, high)
        elif self.prob_type == "greater":
            self.result = randint.sf(self.x1 - 1, self.a, high)
        elif self.prob_type == "greater_strict":
            self.result = randint.sf(self.x1, self.a, high)
        elif self.prob_type == "between":
            self.result = randint.cdf(self.x2, self.a, high) - randint.cdf(self.x1 - 1, self.a, high)

        x = list(range(self.a - 1, self.b + 2))
        y = [randint.pmf(i, self.a, high) for i in x]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------
        self.chart_data = {
            "type": "bar",
            "title": "Distribución Uniforme Discreta",
            "x": x,
            "y": y,
            "x_label": "Valores",
            "y_label": "P(X)",
            "highlight_x1": self.x1,
            "highlight_x2": self.x2,
            "prob_type": self.prob_type
        }

        # ------------------------------------------
        # Tabla
        # ------------------------------------------
        rows = []
        cumulative = 0
        for i in range(self.a, self.b + 1):
            p_val = randint.pmf(i, self.a, high)
            cumulative += p_val
            rows.append([i, p_val, cumulative])

        self.table_data = {
            "title": "Tabla de Probabilidades",
            "headers": ["X", "P(X)", "F(X)"],
            "rows": rows,
            "highlight_x1": self.x1,
            "highlight_x2": self.x2,
            "prob_type": self.prob_type
        }

        # ------------------------------------------
        # Resumen
        # ------------------------------------------
        prob_labels = {
            "equal": "P(X = x₁)",
            "less": "P(X ≤ x₁)",
            "greater": "P(X ≥ x₁)",
            "less_strict": "P(X < x₁)",
            "greater_strict": "P(X > x₁)",
            "between": "P(x₁ ≤ X ≤ x₂)"
        }

        self.summary_html = f"""
        <div class="callout primary">
        <h5>Resumen</h5>
        <p>
        a (mínimo) = <b>{self.a}</b><br>
        b (máximo) = <b>{self.b}</b><br>
        Cálculo = <b>{prob_labels.get(self.prob_type)}</b>
        </p>
        </div>
        """

        # ------------------------------------------
        # Fórmula
        # ------------------------------------------
        self.formula_html = r"""
        <h4>Función de Probabilidad</h4>
        <div style="font-size: 1.2em; overflow-x: auto; padding: 10px;">
            <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
              <mrow>
                <mi>P</mi>
                <mo>(</mo>
                <mi>X</mi>
                <mo>=</mo>
                <mi>x</mi>
                <mo>)</mo>
                <mo>=</mo>
                <mfrac>
                  <mn>1</mn>
                  <mrow>
                    <mi>b</mi>
                    <mo>&#x2212;</mo>
                    <mi>a</mi>
                    <mo>+</mo>
                    <mn>1</mn>
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
            inter_text = f"esté entre <b>{self.x1}</b> y <b>{self.x2}</b> (inclusive)"
        else:
            inter_texts = {
                "equal": f"sea exactamente <b>{self.x1}</b>",
                "less": f"sea <b>{self.x1}</b> o menos",
                "greater": f"sea <b>{self.x1}</b> o más",
                "less_strict": f"sea estrictamente menor que <b>{self.x1}</b>",
                "greater_strict": f"sea estrictamente mayor que <b>{self.x1}</b>"
            }
            inter_text = inter_texts.get(self.prob_type)

        self.interpretation_text = f"""
        La probabilidad de que el valor {inter_text} es
        <h3>{self.result:.6f}</h3>
        """
        self.description_text = """
        La distribución Uniforme Discreta modela fenómenos discretos donde todos los valores posibles
        tienen la misma probabilidad de ocurrir. La probabilidad corresponde a la proporción de casos favorables
        respecto al total de casos posibles.
        """