"""
===========================================================

Probability Calculator

Hypergeometric Distribution

Author : Kevin Sossa

===========================================================
"""

from scipy.stats import hypergeom

from core.discrete_distribution import DiscreteDistribution
from calculator_factory import CalculatorFactory

from ui.panels import NumberField, SelectField
from ui.helpers import int_value, selected_value
from ui.validation import Validator


@CalculatorFactory.register(
    name="Hipergeométrica",
    category="Discrete"
)
class Hypergeometric(DiscreteDistribution):

    def __init__(self):
        super().__init__()
        self.name = "Hipergeométrica"
        
        # Valores por defecto
        self.N_pop = 20  # Población total (N)
        self.K_pop = 7   # Éxitos en la población (K)
        self.n_samp = 12 # Tamaño de la muestra (n)
        self.k = 4       # Éxitos en la muestra (k)
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
                id="N_pop",
                label="Tamaño de la población (N)",
                value=self.N_pop,
                minimum=1
            ),
            NumberField(
                id="K_pop",
                label="Éxitos en la población (K)",
                value=self.K_pop,
                minimum=0
            ),
            NumberField(
                id="n_samp",
                label="Tamaño de la muestra (n)",
                value=self.n_samp,
                minimum=1
            ),
            NumberField(
                id="k",
                label="Éxitos en la muestra (k)",
                value=self.k,
                minimum=0
            )
        ]

    # --------------------------------------------------

    def read_parameters(self):
        self.prob_type = selected_value("prob_type")
        self.N_pop = int_value("N_pop")
        self.K_pop = int_value("K_pop")
        self.n_samp = int_value("n_samp")
        self.k = int_value("k")

    # --------------------------------------------------

    def validate(self):
        validators = [
            Validator.integer(self.N_pop, "N"), Validator.minimum(self.N_pop, 1, "N"),
            Validator.integer(self.K_pop, "K"), Validator.minimum(self.K_pop, 0, "K"),
            Validator.integer(self.n_samp, "n"), Validator.minimum(self.n_samp, 1, "n"),
            Validator.integer(self.k, "k"), Validator.minimum(self.k, 0, "k")
        ]

        for result in validators:
            if not result.valid:
                raise ValueError(result.message)

        if self.K_pop > self.N_pop:
            raise ValueError("Los éxitos (K) no pueden ser mayores que la población (N).")
        if self.n_samp > self.N_pop:
            raise ValueError("La muestra (n) no puede ser mayor que la población (N).")
        if self.k > self.K_pop:
            raise ValueError("Los éxitos en la muestra (k) no pueden superar los éxitos totales (K).")
        if self.k > self.n_samp:
            raise ValueError("Los éxitos (k) no pueden superar el tamaño de la muestra (n).")
            
        min_k = max(0, self.n_samp - (self.N_pop - self.K_pop))
        if self.k < min_k:
            raise ValueError(f"Para esta configuración, k debe ser al menos {min_k}.")

    # --------------------------------------------------

    def run(self):
        # Mapeo de parámetros de Scipy: hypergeom(M, n, N) 
        # M = Población total (N_pop)
        # n = Éxitos en la población (K_pop)
        # N = Tamaño de la muestra (n_samp)
        
        # Calcular resultado principal según el tipo
        if self.prob_type == "equal":
            self.result = hypergeom.pmf(self.k, self.N_pop, self.K_pop, self.n_samp)
        elif self.prob_type == "less":
            self.result = hypergeom.cdf(self.k, self.N_pop, self.K_pop, self.n_samp)
        elif self.prob_type == "less_strict":
            self.result = hypergeom.cdf(self.k - 1, self.N_pop, self.K_pop, self.n_samp) if self.k > 0 else 0.0
        elif self.prob_type == "greater":
            self.result = hypergeom.sf(self.k - 1, self.N_pop, self.K_pop, self.n_samp) if self.k > 0 else 1.0
        elif self.prob_type == "greater_strict":
            self.result = hypergeom.sf(self.k, self.N_pop, self.K_pop, self.n_samp)

        # Determinar el dominio válido para x
        min_x = max(0, self.n_samp - (self.N_pop - self.K_pop))
        max_x = min(self.K_pop, self.n_samp)
        
        x = list(range(min_x, max_x + 1))
        y = [hypergeom.pmf(i, self.N_pop, self.K_pop, self.n_samp) for i in x]

        # ------------------------------------------
        # Gráfico
        # ------------------------------------------
        self.chart_data = {
            "type": "bar",
            "title": "Distribución Hipergeométrica",
            "x": x,
            "y": y,
            "x_label": "Número de éxitos en la muestra (k)",
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
            p_val = hypergeom.pmf(i, self.N_pop, self.K_pop, self.n_samp)
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

        mean = hypergeom.mean(self.N_pop, self.K_pop, self.n_samp)
        variance = hypergeom.var(self.N_pop, self.K_pop, self.n_samp)
        std = variance ** 0.5
        skewness = (1 - 2 * (self.K_pop / self.N_pop)) / (std / (self.n_samp ** 0.5))
        mode = max(min_x, int((self.n_samp + 1) * (self.K_pop / self.N_pop)))

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
                    <mrow>
                      <mo>(</mo>
                      <mfrac linethickness="0">
                        <mi>K</mi>
                        <mi>k</mi>
                      </mfrac>
                      <mo>)</mo>
                    </mrow>
                    <mrow>
                      <mo>(</mo>
                      <mfrac linethickness="0">
                        <mrow>
                          <mi>N</mi>
                          <mo>&#x2212;</mo>
                          <mi>K</mi>
                        </mrow>
                        <mrow>
                          <mi>n</mi>
                          <mo>&#x2212;</mo>
                          <mi>k</mi>
                        </mrow>
                      </mfrac>
                      <mo>)</mo>
                    </mrow>
                  </mrow>
                  <mrow>
                    <mo>(</mo>
                    <mfrac linethickness="0">
                      <mi>N</mi>
                      <mi>n</mi>
                    </mfrac>
                    <mo>)</mo>
                  </mrow>
                </mfrac>
              </mrow>
            </math>
        </div>
        
        <div class="callout" style="margin-top: 15px;">
            <strong>Descripción de variables:</strong>
            <ul>
                <li><b>N</b>: Tamaño total de la población.</li>
                <li><b>K</b>: Número total de elementos considerados "éxitos" dentro de la población.</li>
                <li><b>n</b>: Tamaño de la muestra extraída (sin reemplazo).</li>
                <li><b>k</b>: Número de éxitos que se desean obtener o probar en la muestra.</li>
            </ul>
        </div>
        """

        # ------------------------------------------
        # Descripción
        # ------------------------------------------
        self.description_text = """
        La distribución Hipergeométrica modela la probabilidad
        de obtener un número específico de éxitos en una 
        muestra de tamaño n, extraída de una población 
        finita de tamaño N <b>sin reemplazo</b>.
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
        Al extraer una muestra de <b>{self.n_samp}</b> elementos de una población de <b>{self.N_pop}</b>,
        la probabilidad de {inter_texts.get(self.prob_type)}
        es
        <h3>
        {self.result:.6f}
        </h3>
        """