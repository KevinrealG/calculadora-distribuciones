"""
===========================================================

Probability Calculator

Negative Binomial Distribution

Author : Kevin Sossa

===========================================================
"""

from scipy.stats import nbinom

from core.discrete_distribution import DiscreteDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SliderField, SelectField
from ui.helpers import int_value, float_value, selected_value
from ui.validation import Validator

@CalculatorFactory.register(
name="Binomial Negativa",
category="Discrete"
)
class NegativeBinomial(DiscreteDistribution):

    def __init__(self):

        super().__init__()

        self.name = "Binomial Negativa"

        self.r = 5
        self.p = 0.50
        self.k = 3
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
                id="r",
                label="Número de éxitos esperados (r)",
                value=self.r,
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
                label="Número de fracasos (k)",
                value=self.k,
                minimum=0
            )

        ]

    # --------------------------------------------------

    def read_parameters(self):

        self.prob_type = selected_value("prob_type")
        self.r = int_value("r")
        self.p = float_value("p")
        self.k = int_value("k")

    # --------------------------------------------------

    def validate(self):
        
        validators = [
            Validator.integer(self.r, "r"),
            Validator.minimum(self.r, 1, "r"),
            Validator.between(self.p, 0, 1, "p"),
            Validator.integer(self.k, "k"),
            Validator.minimum(self.k, 0, "k")
        ]

        for result in validators:

            if not result.valid:

                raise ValueError(result.message)

    # --------------------------------------------------

    def run(self):
        
        # Calcular resultado principal según el tipo
        if self.prob_type == "equal":
            self.result = nbinom.pmf(self.k, self.r, self.p)
        elif self.prob_type == "less":
            self.result = nbinom.cdf(self.k, self.r, self.p)
        elif self.prob_type == "less_strict":
            self.result = nbinom.cdf(self.k - 1, self.r, self.p) if self.k > 0 else 0.0
        elif self.prob_type == "greater":
            self.result = nbinom.sf(self.k - 1, self.r, self.p) if self.k > 0 else 1.0
        elif self.prob_type == "greater_strict":
            self.result = nbinom.sf(self.k, self.r, self.p)

        # Calcular un rango razonable para el gráfico
        max_k = int(nbinom.ppf(0.999, self.r, self.p))
        
        if max_k < self.k + 5:
            max_k = self.k + 5
            
        if max_k > 100 and self.k < 95:
            max_k = 100
        elif max_k > 100:
            max_k = self.k + 5

        x = list(range(max_k + 1))

        y = [
            nbinom.pmf(i, self.r, self.p)
            for i in x
        ]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------

        self.chart_data = {
            "type": "bar",
            "title": "Distribución Binomial Negativa",
            "x": x,
            "y": y,
            "x_label": "Número de fracasos antes de r éxitos",
            "y_label": "P(X=x)",
            "highlight_k": self.k,
            "prob_type": self.prob_type
        }

        # ------------------------------------------
        # Tabla
        # ------------------------------------------

        rows = []
        cumulative = 0

        for i in x:
            p_val = nbinom.pmf(i, self.r, self.p)
            cumulative += p_val
            rows.append([i, p_val, cumulative])

        self.table_data = {
            "title": "Tabla de Probabilidades",
            "headers": ["x", "P(X=x)", "F(X≤x)"],
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

        mean = nbinom.mean(self.r, self.p)
        variance = nbinom.var(self.r, self.p)
        std = variance ** 0.5
        skewness = (2 - self.p) / ((self.r * (1 - self.p)) ** 0.5)
        mode = max(0, int((self.r - 1) * (1 - self.p) / self.p))

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
        <h4>
        Función de Probabilidad
        </h4>
        <p>
        P(X=x) = C(x+r-1, x) p<sup>r</sup>(1-p)<sup>x</sup>
        </p>
        <p><small><i>Donde x = número de fracasos y r = número de éxitos.</i></small></p>
        """

        # ------------------------------------------
        # Descripción
        # ------------------------------------------

        self.description_text = """
        La distribución Binomial Negativa modela el número
        de fracasos que ocurren en una secuencia de 
        ensayos de Bernoulli antes de alcanzar un número 
        específico de éxitos (r), con una probabilidad 
        constante (p) de éxito en cada ensayo.
        """

        # ------------------------------------------
        # Interpretación
        # ------------------------------------------

        inter_texts = {
            "equal": f"obtener exactamente <b>{self.k}</b> fracasos",
            "less": f"obtener <b>{self.k}</b> fracasos o menos",
            "greater": f"obtener <b>{self.k}</b> fracasos o más",
            "less_strict": f"obtener menos de <b>{self.k}</b> fracasos",
            "greater_strict": f"obtener más de <b>{self.k}</b> fracasos"
        }

        self.interpretation_text = f"""
        La probabilidad de {inter_texts.get(self.prob_type)}
        antes de obtener el éxito número <b>{self.r}</b>
        es
        <h3>
        {self.result:.6f}
        </h3>
        """
