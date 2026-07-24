"""
===========================================================

Probability Calculator

Poisson Distribution

Author : Kevin Sossa

===========================================================
"""

from scipy.stats import poisson

from core.discrete_distribution import DiscreteDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SelectField
from ui.helpers import int_value, float_value, selected_value
from ui.validation import Validator


@CalculatorFactory.register(
    name="Poisson",
    category="Discrete"
)
class Poisson(DiscreteDistribution):

    def __init__(self):
        super().__init__()
        self.name = "Poisson"
        
        self.lmbda = 4.0  # Tasa de ocurrencia (lambda)
        self.k = 2        # Número de eventos
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
                    "greater_strict": "P(X > k)"
                },
                value=self.prob_type
            ),
            NumberField(
                id="lmbda",
                label="Tasa de ocurrencia (λ)",
                value=self.lmbda,
                minimum=0.0001,
                step=0.1
            ),
            NumberField(
                id="k",
                label="Número de eventos (k)",
                value=self.k,
                minimum=0
            )
        ]

    # --------------------------------------------------

    def read_parameters(self):
        self.prob_type = selected_value("prob_type")
        self.lmbda = float_value("lmbda")
        self.k = int_value("k")

    # --------------------------------------------------

    def validate(self):
        validators = [
            Validator.numeric(self.lmbda, "λ"), Validator.positive(self.lmbda, "λ"),
            Validator.integer(self.k, "k"), Validator.minimum(self.k, 0, "k")
        ]

        for result in validators:
            if not result.valid:
                raise ValueError(result.message)

    # --------------------------------------------------

    def run(self):
        # Calcular resultado principal según el tipo
        if self.prob_type == "equal":
            self.result = poisson.pmf(self.k, self.lmbda)
        elif self.prob_type == "less":
            self.result = poisson.cdf(self.k, self.lmbda)
        elif self.prob_type == "less_strict":
            self.result = poisson.cdf(self.k - 1, self.lmbda) if self.k > 0 else 0.0
        elif self.prob_type == "greater":
            self.result = poisson.sf(self.k - 1, self.lmbda) if self.k > 0 else 1.0
        elif self.prob_type == "greater_strict":
            self.result = poisson.sf(self.k, self.lmbda)

        # Determinar un límite superior dinámico para el gráfico (99.99% acumulado)
        max_x = int(poisson.ppf(0.9999, self.lmbda))
        if max_x < self.k + 5:
            max_x = self.k + 5
            
        x = list(range(0, max_x + 1))
        y = [poisson.pmf(i, self.lmbda) for i in x]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------
        self.chart_data = {
            "type": "bar",
            "title": "Distribución Poisson",
            "x": x,
            "y": y,
            "x_label": "Número de eventos (k)",
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
            p_val = poisson.pmf(i, self.lmbda)
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
            "greater_strict": "P(X > k)"
        }

        mean = poisson.mean(self.lmbda)
        variance = poisson.var(self.lmbda)
        std = variance ** 0.5
        skewness = 1 / (variance ** 0.5)
        mode = int(self.lmbda)

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
                <mi>k</mi>
                <mo>)</mo>
                <mo>=</mo>
                <mfrac>
                  <mrow>
                    <msup>
                      <mi>e</mi>
                      <mrow>
                        <mo>&#x2212;</mo>
                        <mi>&#x03BB;</mi>
                      </mrow>
                    </msup>
                    <msup>
                      <mi>&#x03BB;</mi>
                      <mi>k</mi>
                    </msup>
                  </mrow>
                  <mrow>
                    <mi>k</mi>
                    <mo>!</mo>
                  </mrow>
                </mfrac>
              </mrow>
            </math>
        </div>
        
        <div class="callout" style="margin-top: 15px;">
            <strong>Descripción de variables:</strong>
            <ul>
                <li><b>λ (lambda)</b>: Tasa media de ocurrencia del evento en un intervalo dado (tiempo, área, volumen, etc.).</li>
                <li><b>k</b>: Número exacto de eventos observados.</li>
                <li><b>e</b>: Base del logaritmo natural (aprox. 2.71828).</li>
            </ul>
        </div>
        """

        # ------------------------------------------
        # Descripción
        # ------------------------------------------
        self.description_text = """
        La distribución Poisson modela la probabilidad de que 
        ocurra un número determinado de eventos en un intervalo
        fijo de tiempo o espacio, dado que estos eventos ocurren 
        con una tasa media constante (λ) y son independientes.
        """

        # ------------------------------------------
        # Interpretación
        # ------------------------------------------
        inter_texts = {
            "equal": f"ocurran exactamente <b>{self.k}</b> eventos",
            "less": f"ocurran <b>{self.k}</b> eventos o menos",
            "greater": f"ocurran <b>{self.k}</b> eventos o más",
            "less_strict": f"ocurran menos de <b>{self.k}</b> eventos",
            "greater_strict": f"ocurran más de <b>{self.k}</b> eventos"
        }

        self.interpretation_text = f"""
        Dado un promedio de <b>{self.lmbda}</b> ocurrencias,
        la probabilidad de que {inter_texts.get(self.prob_type)}
        es
        <h3>
        {self.result:.6f}
        </h3>
        """