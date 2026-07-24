"""
===========================================================

Probability Calculator

DiscreteDistribution

Clase base para distribuciones discretas.

Author : Kevin Sossa

===========================================================
"""

import numpy as np

from core.base_distribution import BaseDistribution

from ui import charts
from ui import tables


class DiscreteDistribution(BaseDistribution):

    """
    Clase base para todas las distribuciones discretas.

    Las clases hijas solamente implementan:

        pmf(x)

        cdf(x)

        mean()

        variance()

        read_parameters()

        validate()

    """

    # ------------------------------------------------------

    def __init__(self):

        super().__init__()

        self.x = None

        self.y = None

        self.cdf_values = None

        self.k = None

        self.max_x = None

    # ------------------------------------------------------
    # Métodos que implementan las clases hijas
    # ------------------------------------------------------

    def pmf(self, x):

        raise NotImplementedError()

    def cdf(self, x):

        raise NotImplementedError()

    def mean(self):

        if self.x is None or self.y is None:

            raise NotImplementedError()

        return float(np.sum(self.x * self.y))

    def variance(self):

        if self.x is None or self.y is None:

            raise NotImplementedError()

        mean_value = self.mean()

        return float(np.sum(((self.x - mean_value) ** 2) * self.y))

    # ------------------------------------------------------
    # Estadísticas generales
    # ------------------------------------------------------

    def mode(self):

        if self.x is None or self.y is None:

            return None

        return int(self.x[np.argmax(self.y)])

    # ------------------------------------------------------

    def skewness(self):

        if self.x is None or self.y is None:

            return None

        mean = self.mean()

        variance = self.variance()

        if variance <= 0:

            return 0.0

        std = np.sqrt(variance)

        centered = self.x - mean

        return float(

            np.sum(

                self.y * ((centered / std) ** 3)

            )

        )

    # ------------------------------------------------------
    # Cálculo principal
    # ------------------------------------------------------

    def compute(self):

        self.x = np.arange(

            0,

            self.max_x + 1

        )

        self.y = self.pmf(self.x)

        self.cdf_values = self.cdf(self.x)

        self.result = self.pmf(self.k)

    # ------------------------------------------------------
    # Resumen
    # ------------------------------------------------------

    def create_summary(self):

        self.summary_data = {

            "Media":

                self.mean(),

            "Varianza":

                self.variance(),

            "Desviación":

                np.sqrt(

                    self.variance()

                ),

            "P(X = k)":

                self.result,

            "P(X ≤ k)":

                self.cdf(self.k)

        }

    # ------------------------------------------------------
    # Tabla
    # ------------------------------------------------------

    def create_table(self):

        rows = []

        for i in range(

                len(self.x)

        ):

            rows.append([

                int(self.x[i]),

                self.y[i],

                self.cdf_values[i]

            ])

        self.table_data = (

            [

                "x",

                "P(X=x)",

                "P(X≤x)"

            ],

            rows

        )

    # ------------------------------------------------------
    # Gráfica
    # ------------------------------------------------------

    def create_chart(self):

        self.chart_data = {

            "type": "bar",

            "args": {

                "x": self.x,

                "y": self.y,

                "title": self.title,

                "x_title": "x",

                "y_title": "P(X=x)",

                "highlight": int(self.k)

            }

        }

    # ------------------------------------------------------
    # Fórmula
    # ------------------------------------------------------

    def create_formula(self):

        pass

    # ------------------------------------------------------
    # Descripción
    # ------------------------------------------------------

    def create_description(self):

        pass

    # ------------------------------------------------------
    # Interpretación
    # ------------------------------------------------------

    def create_interpretation(self):

        self.interpretation_text = f"""

        La probabilidad de obtener

        <b>{self.k}</b>

        es

        <b>{self.result:.6f}</b>.

        """
