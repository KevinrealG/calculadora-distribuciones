"""
===========================================================

Probability Calculator

main.py

Punto de entrada de la aplicación.

Author : Kevin Sossa

===========================================================
"""
print("Main iniciado")
from pyscript import document
from router import Router
from calculator_factory import CalculatorFactory
from distributions.discrete.binomial import Binomial
from pyodide.ffi import create_proxy
from distributions.discrete.negative_binomial import NegativeBinomial
from distributions.discrete.poisson import Poisson
from distributions.discrete.hypergeometric import Hypergeometric
from distributions.continuous.normal import Normal
from distributions.discrete.uniforme_discreta import UniformDiscrete
from distributions.continuous.t_student import TStudent
from distributions.continuous.uniform import UniformContinuous
from distributions.continuous.chi_square import ChiSquare
from distributions.continuous.exponential import Exponential
from distributions.continuous.fisher import Fisher
#from distributions.continuous.uniform import Uniform
#from distributions.discrete.geometric import Geometric

class Application:

    """
    Clase principal de la aplicación.

    Su única responsabilidad es inicializar
    la interfaz y delegar el trabajo al Router.
    """

    def __init__(self):

        self.router = Router()
        self.calculate_proxy = create_proxy(

            self.router.calculate

        )

        self.change_proxy = create_proxy(

            self.router.change_distribution

        )

    # --------------------------------------------------
    # Inicio
    # --------------------------------------------------

    def start(self):

        self.load_catalog()

        self.register_events()

        self.router.load_default()

    # --------------------------------------------------
    # Cargar catálogo
    # --------------------------------------------------

    def load_catalog(self):

        select = document.getElementById(

            "distribution-select"

        )

        select.innerHTML = ""

        catalog = CalculatorFactory.catalog()

        for item in catalog:

            option = document.createElement(

                "option"

            )

            option.value = item["id"]

            option.textContent = item["name"]

            select.appendChild(

                option

            )

    # --------------------------------------------------
    # Eventos
    # --------------------------------------------------

    def register_events(self):

        document.getElementById(

            "distribution-select"

        ).addEventListener(

            "change",

            self.change_proxy

        )

        document.getElementById(
            "calculate-btn"
        ).addEventListener(
            "click",
            self.calculate_proxy
        )
        document.getElementById(
            "distribution-select"
        ).addEventListener(
            "change",
            self.change_proxy
        )


# =========================================================

app = Application()

app.start()
# Ocultar el spinner de carga al terminar de cargar la app
loader = document.getElementById("loading-overlay")
if loader:
    loader.style.display = "none"